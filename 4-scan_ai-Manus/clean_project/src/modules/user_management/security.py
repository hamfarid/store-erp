"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/user_management/security.py
الوصف: خدمة أمان المستخدمين وإدارة الحظر
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session

from src.database import db_session
from src.modules.user_management.models import User
from src.modules.notifications.telegram import TelegramNotificationService
from src.modules.activity_log.integration import ActivityLogger

# إعداد المسجل
logger = logging.getLogger(__name__)


class UserSecurityService:
    """خدمة أمان المستخدمين وإدارة الحظر"""

    def __init__(self, db: Session = None):
        """
        تهيئة خدمة أمان المستخدمين

        المعلمات:
            db: جلسة قاعدة البيانات (اختياري)
        """
        self.db = db or db_session
        self.telegram_service = TelegramNotificationService()
        self.activity_logger = ActivityLogger()
        self.max_failed_attempts = 5
        self.lockout_duration_minutes = 30

    def record_failed_login(
        self, username: str, ip_address: str, user_agent: str = None
    ) -> Tuple[bool, Optional[User]]:
        """
        تسجيل محاولة تسجيل دخول فاشلة

        المعلمات:
            username: اسم المستخدم
            ip_address: عنوان IP
            user_agent: معلومات متصفح المستخدم (اختياري)

        العائد:
            Tuple[bool, Optional[User]]:
                - الأول: True إذا تم حظر المستخدم، False إذا لم يتم حظره
                - الثاني: كائن المستخدم إذا وجد، وإلا None
        """
        # البحث عن المستخدم
        user = self.db.query(User).filter(User.username == username).first()

        if not user:
            # تسجيل محاولة دخول فاشلة لمستخدم غير موجود
            self.activity_logger.log_security_event(
                event_type="failed_login_attempt",
                details={
                    "username": username,
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    "reason": "user_not_found",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
            return False, None

        # التحقق مما إذا كان المستخدم محظوراً بالفعل
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            # تسجيل محاولة دخول لمستخدم محظور
            self.activity_logger.log_security_event(
                event_type="blocked_user_login_attempt",
                user_id=user.id,
                details={
                    "username": username,
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    "locked_until": user.locked_until.isoformat(),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
            return True, user

        # زيادة عدد محاولات تسجيل الدخول الفاشلة
        user.failed_login_attempts += 1

        # تسجيل محاولة الدخول الفاشلة
        self.activity_logger.log_security_event(
            event_type="failed_login_attempt",
            user_id=user.id,
            details={
                "username": username,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "failed_attempts": user.failed_login_attempts,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        # التحقق مما إذا كان يجب حظر المستخدم
        if user.failed_login_attempts >= self.max_failed_attempts:
            # حظر المستخدم
            user.locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=self.lockout_duration_minutes
            )

            # تسجيل حدث حظر المستخدم
            self.activity_logger.log_security_event(
                event_type="user_blocked",
                user_id=user.id,
                details={
                    "username": username,
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    "failed_attempts": user.failed_login_attempts,
                    "locked_until": user.locked_until.isoformat(),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

            # إرسال إشعار للمسؤولين عبر تيليجرام
            try:
                self.notify_admins_about_blocked_user(user, ip_address, user_agent)
            except Exception as e:
                logger.error(f"فشل إرسال إشعار تيليجرام عن حظر المستخدم: {str(e)}")

            self.db.commit()
            return True, user

        self.db.commit()
        return False, user

    def reset_failed_attempts(self, user_id: str) -> bool:
        """
        إعادة تعيين عدد محاولات تسجيل الدخول الفاشلة

        المعلمات:
            user_id: معرف المستخدم

        العائد:
            bool: True إذا تم إعادة التعيين بنجاح، False إذا لم يتم العثور على المستخدم
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return False

        user.failed_login_attempts = 0
        user.locked_until = None

        # تسجيل حدث إعادة تعيين محاولات الدخول
        self.activity_logger.log_security_event(
            event_type="reset_failed_attempts",
            user_id=user.id,
            details={
                "username": user.username,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        self.db.commit()
        return True

    def unblock_user(self, user_id: str, admin_id: str) -> bool:
        """
        إلغاء حظر مستخدم

        المعلمات:
            user_id: معرف المستخدم
            admin_id: معرف المسؤول الذي قام بإلغاء الحظر

        العائد:
            bool: True إذا تم إلغاء الحظر بنجاح، False إذا لم يتم العثور على المستخدم
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        admin = self.db.query(User).filter(User.id == admin_id).first()

        if not user or not admin:
            return False

        was_blocked = user.locked_until and user.locked_until > datetime.now(
            timezone.utc
        )

        user.failed_login_attempts = 0
        user.locked_until = None

        # تسجيل حدث إلغاء الحظر
        self.activity_logger.log_security_event(
            event_type="user_unblocked",
            user_id=user.id,
            details={
                "username": user.username,
                "admin_id": admin_id,
                "admin_username": admin.username,
                "was_blocked": was_blocked,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        self.db.commit()
        return True

    def is_user_blocked(self, user_id: str) -> bool:
        """
        التحقق مما إذا كان المستخدم محظوراً

        المعلمات:
            user_id: معرف المستخدم

        العائد:
            bool: True إذا كان المستخدم محظوراً، False إذا لم يكن محظوراً أو لم يتم العثور عليه
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return False

        return user.locked_until and user.locked_until > datetime.now(timezone.utc)

    def get_blocked_users(self) -> List[User]:
        """
        الحصول على قائمة المستخدمين المحظورين

        العائد:
            List[User]: قائمة المستخدمين المحظورين
        """
        current_time = datetime.now(timezone.utc)
        return (
            self.db.query(User)
            .filter(User.locked_until.isnot(None))
            .filter(User.locked_until > current_time)
            .all()
        )

    def notify_admins_about_blocked_user(
        self, user: User, ip_address: str, user_agent: str = None
    ) -> None:
        """
        إرسال إشعار للمسؤولين عن حظر مستخدم

        المعلمات:
            user: كائن المستخدم المحظور
            ip_address: عنوان IP
            user_agent: معلومات متصفح المستخدم (اختياري)
        """
        message = f"""
🚨 تنبيه أمني: تم حظر مستخدم 🚨

المستخدم: {user.username}
البريد الإلكتروني: {user.email}
عدد المحاولات الفاشلة: {user.failed_login_attempts}
مدة الحظر: {self.lockout_duration_minutes} دقيقة
عنوان IP: {ip_address}
تاريخ الحظر: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

يرجى مراجعة نشاط المستخدم والتحقق من الأمان.
        """

        try:
            self.telegram_service.send_security_alert(message.strip())
        except Exception as e:
            logger.error(f"فشل إرسال إشعار تيليجرام: {str(e)}")

    def clean_expired_blocks(self) -> int:
        """
        تنظيف الحظر المنتهي الصلاحية

        العائد:
            int: عدد المستخدمين الذين تم إلغاء حظرهم
        """
        current_time = datetime.now(timezone.utc)
        expired_blocks = (
            self.db.query(User)
            .filter(User.locked_until.isnot(None))
            .filter(User.locked_until <= current_time)
        )

        count = expired_blocks.count()

        if count > 0:
            expired_blocks.update(
                {"locked_until": None, "failed_login_attempts": 0},
                synchronize_session=False,
            )
            self.db.commit()

        return count
