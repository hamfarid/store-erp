"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/security/url_validator.py
وحدة التحقق من صحة عناوين URL ومنع تجاوز الصلاحيات
"""

import logging
import re

from fastapi import Request, HTTPException

from src.modules.security.access_control import AccessControl
from src.modules.activity_log.service import ActivityLogService
from src.modules.notifications.telegram import TelegramNotifier

# إعداد السجل
logger = logging.getLogger(__name__)


class URLValidator:
    """فئة للتحقق من صحة عناوين URL ومنع تجاوز الصلاحيات"""

    def __init__(self, access_control: AccessControl, activity_log_service: ActivityLogService,
                 telegram_notifier: TelegramNotifier):
        """
        تهيئة فئة التحقق من صحة عناوين URL

        Args:
            access_control: فئة التحكم في الوصول
            activity_log_service: خدمة سجل النشاط
            telegram_notifier: خدمة إشعارات تيليجرام
        """
        self.access_control = access_control
        self.activity_log_service = activity_log_service
        self.telegram_notifier = telegram_notifier

        # قائمة المسارات المحمية التي تتطلب صلاحيات خاصة
        self.protected_paths = {
            r'^/admin.*': 'admin',
            r'^/settings.*': 'settings_access',
            r'^/users.*': 'user_management',
            r'^/security.*': 'security_management',
            r'^/backup.*': 'backup_management',
            r'^/logs.*': 'logs_access',
            r'^/modules.*': 'module_management',
            r'^/api/admin.*': 'admin_api',
            r'^/api/settings.*': 'settings_api',
            r'^/api/users.*': 'user_management_api',
            r'^/api/security.*': 'security_management_api',
            r'^/api/backup.*': 'backup_management_api',
            r'^/api/logs.*': 'logs_access_api',
            r'^/api/modules.*': 'module_management_api',
        }

        # قائمة المسارات المحظورة تماماً
        self.forbidden_paths = [
            r'^/\..*',  # ملفات مخفية
            r'^/etc/.*',
            r'^/var/.*',
            r'^/proc/.*',
            r'^/sys/.*',
            r'^/root/.*',
            r'^/home/.*',
            r'^/usr/.*',
            r'^/bin/.*',
            r'^/sbin/.*',
            r'^/lib/.*',
            r'^/opt/.*',
            r'^/mnt/.*',
            r'^/media/.*',
            r'^/srv/.*',
            r'^/tmp/.*',
            r'^/run/.*',
            r'^/dev/.*',
            r'^/boot/.*',
        ]

    async def validate_url(self, request: Request) -> None:
        """
        التحقق من صحة عنوان URL ومنع تجاوز الصلاحيات

        Args:
            request: كائن الطلب

        Raises:
            HTTPException: في حالة وجود محاولة تجاوز الصلاحيات
        """
        path = request.url.path

        # التحقق من المسارات المحظورة
        for pattern in self.forbidden_paths:
            if re.match(pattern, path):
                # تسجيل محاولة الوصول إلى مسار محظور
                client_ip = request.client.host
                await self.activity_log_service.log_security_event(
                    user_id=None,
                    event_type="forbidden_path_access",
                    details=f"Attempted to access forbidden path: {path}",
                    ip_address=client_ip,
                    module="security",
                    severity="critical"
                )

                # إرسال إشعار للمسؤول
                await self.telegram_notifier.send_admin_notification(
                    f"محاولة وصول خطيرة: تم محاولة الوصول إلى مسار محظور {path} "
                    f"من العنوان {client_ip}"
                )

                # حظر عنوان IP
                await self.access_control.block_ip(client_ip, duration_minutes=60)

                raise HTTPException(status_code=403, detail="Access forbidden")

        # التحقق من المسارات المحمية
        for pattern, permission in self.protected_paths.items():
            if re.match(pattern, path):
                # الحصول على المستخدم الحالي
                try:
                    user = await self.access_control.get_current_user(request)
                except HTTPException as exc:
                    # إعادة التوجيه إلى صفحة تسجيل الدخول
                    raise HTTPException(
                        status_code=401,
                        detail="Authentication required",
                        headers={"WWW-Authenticate": "Bearer"}
                    ) from exc

                # التحقق من الصلاحية
                if not await self.access_control.check_permission(user, permission):
                    # تسجيل محاولة الوصول غير المصرح به
                    client_ip = request.client.host
                    await self.activity_log_service.log_security_event(
                        user_id=user.id,
                        event_type="unauthorized_access",
                        details=f"Attempted to access protected path: {path} requiring permission: {permission}",
                        ip_address=client_ip,
                        module="security",
                        severity="high"
                    )

                    # إرسال إشعار للمسؤول
                    await self.telegram_notifier.send_admin_notification(
                        f"محاولة وصول غير مصرح به: المستخدم {user.username} "
                        f"حاول الوصول إلى مسار محمي {path} يتطلب صلاحية {permission} "
                        f"من العنوان {client_ip}"
                    )

                    # زيادة عدد محاولات الوصول غير المصرح به
                    await self.increment_unauthorized_access_attempts(user.id, client_ip)

                    raise HTTPException(status_code=403, detail="Not enough permissions")

    async def increment_unauthorized_access_attempts(self, user_id: int, ip_address: str) -> None:
        """
        زيادة عدد محاولات الوصول غير المصرح به

        Args:
            user_id: معرف المستخدم
            ip_address: عنوان IP
        """
        # هنا يمكن تنفيذ منطق لتتبع عدد محاولات الوصول غير المصرح به
        # وحظر المستخدم أو عنوان IP إذا تجاوز عدد معين من المحاولات
        logger.info("تسجيل محاولة وصول غير مصرح به للمستخدم %s من العنوان %s", user_id, ip_address)

    def is_safe_redirect_url(self, url: str) -> bool:
        """
        التحقق مما إذا كان عنوان URL آمناً لإعادة التوجيه

        Args:
            url: عنوان URL

        Returns:
            True إذا كان عنوان URL آمناً، False خلاف ذلك
        """
        # التحقق من أن عنوان URL نسبي أو من نفس النطاق
        if not url:
            return False

        # إذا كان العنوان نسبياً، فهو آمن
        if url.startswith('/') and not url.startswith('//'):
            return True

        # إذا كان العنوان مطلقاً، تحقق من أنه من نفس النطاق
        # هذا يتطلب معرفة النطاق الأساسي للتطبيق
        # يمكن تنفيذ هذا المنطق حسب احتياجات التطبيق

        return False
