"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/security/access_control.py
وحدة التحكم في الوصول والصلاحيات
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..activity_log.service import ActivityLogService
from ..notifications.telegram import TelegramNotifier
from ..user_management.models import User
from ..user_management.service import UserService

# إعداد السجل
logger = logging.getLogger(__name__)

# إعداد OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ثوابت الأمان
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MAX_LOGIN_ATTEMPTS = 5


class AccessControl:
    """فئة للتحكم في الوصول والصلاحيات"""

    def __init__(
            self,
            secret_key: str,
            activity_log_service: ActivityLogService,
            user_service: UserService,
            telegram_notifier: TelegramNotifier):
        """
        تهيئة فئة التحكم في الوصول

        Args:
            secret_key: مفتاح التشفير السري
            activity_log_service: خدمة سجل النشاط
            user_service: خدمة إدارة المستخدمين
            telegram_notifier: خدمة إشعارات تيليجرام
        """
        self.secret_key = secret_key
        self.activity_log_service = activity_log_service
        self.user_service = user_service
        self.telegram_notifier = telegram_notifier
        self.blocked_ips = {}  # قاموس لتخزين عناوين IP المحظورة

    async def create_access_token(
            self,
            data: dict,
            expires_delta: Optional[timedelta] = None) -> str:
        """
        إنشاء رمز وصول JWT

        Args:
            data: البيانات المراد تضمينها في الرمز
            expires_delta: مدة صلاحية الرمز

        Returns:
            رمز الوصول المشفر
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=ALGORITHM)
        return encoded_jwt

    async def verify_token(self, token: str = Depends(
            oauth2_scheme)) -> Dict[str, Any]:
        """
        التحقق من صحة رمز الوصول

        Args:
            token: رمز الوصول JWT

        Returns:
            بيانات المستخدم المستخرجة من الرمز

        Raises:
            HTTPException: في حالة فشل التحقق من الرمز
        """
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return payload
        except JWTError:
            raise credentials_exception

    async def get_current_user(
            self, token: str = Depends(oauth2_scheme)) -> User:
        """
        الحصول على المستخدم الحالي من رمز الوصول

        Args:
            token: رمز الوصول JWT

        Returns:
            كائن المستخدم الحالي

        Raises:
            HTTPException: في حالة عدم وجود المستخدم أو حظره
        """
        payload = await self.verify_token(token)
        username: str = payload.get("sub")
        user = await self.user_service.get_user_by_username(username)

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        if user.is_blocked:
            raise HTTPException(status_code=403, detail="User is blocked")

        return user

    async def check_permission(
            self,
            user: User,
            required_permission: str) -> bool:
        """
        التحقق من صلاحية المستخدم

        Args:
            user: كائن المستخدم
            required_permission: الصلاحية المطلوبة

        Returns:
            True إذا كان المستخدم يملك الصلاحية، False خلاف ذلك
        """
        # التحقق من وجود المستخدم وعدم حظره
        if user is None or user.is_blocked:
            return False

        # المسؤول يملك جميع الصلاحيات
        if user.is_admin:
            return True

        # التحقق من وجود الصلاحية في قائمة صلاحيات المستخدم
        return required_permission in user.permissions

    async def require_permission(
            self,
            user: User,
            required_permission: str,
            request: Request) -> None:
        """
        طلب صلاحية محددة للوصول

        Args:
            user: كائن المستخدم
            required_permission: الصلاحية المطلوبة
            request: كائن الطلب

        Raises:
            HTTPException: في حالة عدم وجود الصلاحية المطلوبة
        """
        if not await self.check_permission(user, required_permission):
            # تسجيل محاولة الوصول غير المصرح به
            client_ip = request.client.host
            await self.activity_log_service.log_security_event(
                user_id=user.id if user else None,
                event_type="unauthorized_access",
                details=f"Attempted to access resource requiring {required_permission}",
                ip_address=client_ip,
                module="security",
                severity="high"
            )

            # إرسال إشعار للمسؤول
            await self.telegram_notifier.send_admin_notification(
                f"محاولة وصول غير مصرح به: المستخدم {user.username if user else 'غير معروف'} "
                f"حاول الوصول إلى مورد يتطلب صلاحية {required_permission} من العنوان {client_ip}"
            )

            raise HTTPException(
                status_code=403,
                detail="Not enough permissions")

    async def handle_login_attempt(
            self,
            username: str,
            success: bool,
            request: Request) -> None:
        """
        معالجة محاولة تسجيل الدخول

        Args:
            username: اسم المستخدم
            success: نجاح محاولة تسجيل الدخول
            request: كائن الطلب
        """
        client_ip = request.client.host
        user = await self.user_service.get_user_by_username(username)

        if success:
            # إعادة تعيين عدد محاولات تسجيل الدخول الفاشلة
            if user:
                await self.user_service.reset_failed_login_attempts(user.id)

            # تسجيل نجاح تسجيل الدخول
            await self.activity_log_service.log_security_event(
                user_id=user.id if user else None,
                event_type="login_success",
                details=f"Successful login for user {username}",
                ip_address=client_ip,
                module="security",
                severity="info"
            )
        else:
            # زيادة عدد محاولات تسجيل الدخول الفاشلة
            if user:
                await self.user_service.increment_failed_login_attempts(user.id)

                # التحقق من تجاوز الحد الأقصى لمحاولات تسجيل الدخول الفاشلة
                if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
                    # حظر المستخدم
                    await self.user_service.block_user(user.id)

                    # إرسال إشعار للمسؤول
                    await self.telegram_notifier.send_admin_notification(
                        f"تم حظر المستخدم {username} بعد {MAX_LOGIN_ATTEMPTS} محاولات تسجيل دخول فاشلة "
                        f"من العنوان {client_ip}"
                    )

            # تسجيل فشل تسجيل الدخول
            await self.activity_log_service.log_security_event(
                user_id=user.id if user else None,
                event_type="login_failure",
                details=f"Failed login attempt for user {username}",
                ip_address=client_ip,
                module="security",
                severity="warning"
            )

    async def is_ip_blocked(self, request: Request) -> bool:
        """
        التحقق مما إذا كان عنوان IP محظوراً

        Args:
            request: كائن الطلب

        Returns:
            True إذا كان عنوان IP محظوراً، False خلاف ذلك
        """
        client_ip = request.client.host
        return client_ip in self.blocked_ips

    async def block_ip(
            self,
            ip_address: str,
            duration_minutes: int = 30) -> None:
        """
        حظر عنوان IP

        Args:
            ip_address: عنوان IP المراد حظره
            duration_minutes: مدة الحظر بالدقائق
        """
        self.blocked_ips[ip_address] = datetime.utcnow(
        ) + timedelta(minutes=duration_minutes)

        # تسجيل حظر عنوان IP
        await self.activity_log_service.log_security_event(
            user_id=None,
            event_type="ip_blocked",
            details=f"IP address {ip_address} blocked for {duration_minutes} minutes",
            ip_address=ip_address,
            module="security",
            severity="high"
        )

        # إرسال إشعار للمسؤول
        await self.telegram_notifier.send_admin_notification(
            f"تم حظر عنوان IP {ip_address} لمدة {duration_minutes} دقيقة"
        )

    async def cleanup_blocked_ips(self) -> None:
        """تنظيف قائمة عناوين IP المحظورة منتهية الصلاحية"""
        now = datetime.utcnow()
        expired_ips = [
            ip for ip,
            expiry in self.blocked_ips.items() if expiry < now]
        for ip in expired_ips:
            del self.blocked_ips[ip]
