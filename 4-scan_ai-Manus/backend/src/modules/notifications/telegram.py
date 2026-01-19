"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/notifications/telegram.py
الوصف: خدمة إرسال الإشعارات عبر تيليجرام
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد المسجل
logger = logging.getLogger(__name__)


class TelegramNotificationService:
    """خدمة إرسال الإشعارات عبر تيليجرام"""

    def __init__(self):
        """
        تهيئة خدمة إشعارات تيليجرام
        """
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.default_chat_id = os.getenv('TELEGRAM_DEFAULT_CHAT_ID', '')
        self.admin_chat_ids = self._parse_admin_chat_ids(
            os.getenv('TELEGRAM_ADMIN_CHAT_IDS', ''))
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.enabled = os.getenv(
            'TELEGRAM_NOTIFICATIONS_ENABLED',
            'false').lower() == 'true'

        # التحقق من توفر الإعدادات الأساسية
        if self.enabled and (not self.bot_token or not self.default_chat_id):
            logger.warning(
                "تم تفعيل إشعارات تيليجرام لكن لم يتم توفير رمز البوت أو معرف المحادثة الافتراضي")

    def _parse_admin_chat_ids(self, admin_chat_ids_str: str) -> List[str]:
        """
        تحليل قائمة معرفات محادثات المسؤولين من النص

        المعلمات:
            admin_chat_ids_str: نص يحتوي على معرفات محادثات المسؤولين مفصولة بفواصل

        العائد:
            List[str]: قائمة معرفات محادثات المسؤولين
        """
        if not admin_chat_ids_str:
            return []

        return [chat_id.strip()
                for chat_id in admin_chat_ids_str.split(',') if chat_id.strip()]

    def send_message(self,
                     message: str,
                     chat_id: Optional[str] = None,
                     parse_mode: str = "HTML",
                     disable_notification: bool = False,
                     reply_markup: Optional[Dict[str,
                                                 Any]] = None) -> Dict[str,
                                                                       Any]:
        """
        إرسال رسالة عبر تيليجرام

        المعلمات:
            message: نص الرسالة
            chat_id: معرف المحادثة (اختياري، يستخدم المعرف الافتراضي إذا لم يتم تحديده)
            parse_mode: وضع تحليل النص (HTML أو Markdown)
            disable_notification: تعطيل الإشعارات الصوتية
            reply_markup: تخطيط أزرار الرد (اختياري)

        العائد:
            Dict[str, Any]: استجابة API تيليجرام

        يثير:
            ValueError: إذا لم يتم تفعيل إشعارات تيليجرام أو لم يتم توفير معرف المحادثة
            Exception: إذا فشل إرسال الرسالة
        """
        if not self.enabled:
            raise ValueError("إشعارات تيليجرام غير مفعلة")

        # استخدام معرف المحادثة الافتراضي إذا لم يتم تحديد معرف
        target_chat_id = chat_id or self.default_chat_id

        if not target_chat_id:
            raise ValueError(
                "لم يتم توفير معرف المحادثة ولا يوجد معرف افتراضي")

        # تحضير بيانات الطلب
        data = {
            "chat_id": target_chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification
        }

        # إضافة تخطيط أزرار الرد إذا تم توفيره
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)

        try:
            # إرسال الطلب إلى API تيليجرام
            response = requests.post(f"{self.api_url}/sendMessage", data=data)
            response.raise_for_status()  # رفع استثناء إذا كان الرد غير ناجح

            return response.json()
        except Exception as e:
            logger.error(f"فشل إرسال رسالة تيليجرام: {str(e)}")
            raise

    def send_notification(self,
                          title: str,
                          content: str,
                          notification_type: str = "info",
                          priority: str = "medium",
                          chat_id: Optional[str] = None,
                          metadata: Optional[Dict[str,
                                                  Any]] = None) -> Dict[str,
                                                                        Any]:
        """
        إرسال إشعار منسق عبر تيليجرام

        المعلمات:
            title: عنوان الإشعار
            content: محتوى الإشعار
            notification_type: نوع الإشعار (info, success, warning, error, system, security)
            priority: أولوية الإشعار (low, medium, high, urgent)
            chat_id: معرف المحادثة (اختياري، يستخدم المعرف الافتراضي إذا لم يتم تحديده)
            metadata: بيانات وصفية إضافية (اختياري)

        العائد:
            Dict[str, Any]: استجابة API تيليجرام

        يثير:
            ValueError: إذا لم يتم تفعيل إشعارات تيليجرام أو لم يتم توفير معرف المحادثة
            Exception: إذا فشل إرسال الإشعار
        """
        # تحديد الرمز التعبيري حسب نوع الإشعار
        type_emoji = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "system": "🖥️",
            "security": "🔒",
            "task": "📋",
            "message": "💬",
            "update": "🔄"
        }.get(notification_type, "ℹ️")

        # تحديد الرمز التعبيري حسب الأولوية
        priority_emoji = {
            "low": "🔽",
            "medium": "➖",
            "high": "🔼",
            "urgent": "‼️"
        }.get(priority, "➖")

        # تنسيق الرسالة بتنسيق HTML
        formatted_message = f"""
<b>{type_emoji} {title}</b> {priority_emoji}

{content}
"""

        # إضافة البيانات الوصفية إذا تم توفيرها
        if metadata:
            metadata_text = "\n<b>معلومات إضافية:</b>\n"
            for key, value in metadata.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False, indent=2)
                metadata_text += f"<code>{key}</code>: {value}\n"

            formatted_message += metadata_text

        # إرسال الرسالة المنسقة
        return self.send_message(formatted_message, chat_id)

    def send_admin_notification(self,
                                title: str,
                                content: str,
                                notification_type: str = "system",
                                priority: str = "high",
                                metadata: Optional[Dict[str,
                                                        Any]] = None) -> List[Dict[str,
                                                                                   Any]]:
        """
        إرسال إشعار إلى جميع المسؤولين

        المعلمات:
            title: عنوان الإشعار
            content: محتوى الإشعار
            notification_type: نوع الإشعار
            priority: أولوية الإشعار
            metadata: بيانات وصفية إضافية (اختياري)

        العائد:
            List[Dict[str, Any]]: قائمة استجابات API تيليجرام

        يثير:
            ValueError: إذا لم يتم تفعيل إشعارات تيليجرام أو لم يتم توفير معرفات محادثات المسؤولين
            Exception: إذا فشل إرسال الإشعار
        """
        if not self.enabled:
            raise ValueError("إشعارات تيليجرام غير مفعلة")

        if not self.admin_chat_ids:
            raise ValueError("لم يتم توفير معرفات محادثات المسؤولين")

        responses = []
        errors = []

        # إرسال الإشعار إلى كل مسؤول
        for admin_chat_id in self.admin_chat_ids:
            try:
                response = self.send_notification(
                    title=title,
                    content=content,
                    notification_type=notification_type,
                    priority=priority,
                    chat_id=admin_chat_id,
                    metadata=metadata
                )
                responses.append(response)
            except Exception as e:
                logger.error(
                    f"فشل إرسال إشعار للمسؤول {admin_chat_id}: {str(e)}")
                errors.append({"chat_id": admin_chat_id, "error": str(e)})

        # إذا فشلت جميع عمليات الإرسال، رفع استثناء
        if len(errors) == len(self.admin_chat_ids):
            raise Exception(f"فشل إرسال الإشعار إلى جميع المسؤولين: {errors}")

        return responses

    def send_security_alert(self,
                            title: str,
                            content: str,
                            priority: str = "high",
                            metadata: Optional[Dict[str,
                                                    Any]] = None) -> List[Dict[str,
                                                                               Any]]:
        """
        إرسال تنبيه أمني إلى جميع المسؤولين

        المعلمات:
            title: عنوان التنبيه
            content: محتوى التنبيه
            priority: أولوية التنبيه
            metadata: بيانات وصفية إضافية (اختياري)

        العائد:
            List[Dict[str, Any]]: قائمة استجابات API تيليجرام
        """
        return self.send_admin_notification(
            title=f"🚨 تنبيه أمني: {title}",
            content=content,
            notification_type="security",
            priority=priority,
            metadata=metadata
        )

    def send_user_blocked_alert(self,
                                username: str,
                                ip_address: str,
                                failed_attempts: int,
                                timestamp: str,
                                additional_info: Optional[Dict[str,
                                                               Any]] = None) -> List[Dict[str,
                                                                                          Any]]:
        """
        إرسال تنبيه حظر مستخدم إلى جميع المسؤولين

        المعلمات:
            username: اسم المستخدم المحظور
            ip_address: عنوان IP للمستخدم
            failed_attempts: عدد محاولات الدخول الفاشلة
            timestamp: الطابع الزمني للحظر
            additional_info: معلومات إضافية (اختياري)

        العائد:
            List[Dict[str, Any]]: قائمة استجابات API تيليجرام
        """
        content = f"""
تم حظر المستخدم <b>{username}</b> بعد <b>{failed_attempts}</b> محاولات دخول فاشلة.

<b>تفاصيل الحظر:</b>
• عنوان IP: <code>{ip_address}</code>
• وقت الحظر: {timestamp}

يمكن للمسؤول إلغاء الحظر من خلال لوحة إدارة المستخدمين.
"""

        metadata = {
            "username": username,
            "ip_address": ip_address,
            "failed_attempts": failed_attempts,
            "timestamp": timestamp
        }

        if additional_info:
            metadata.update(additional_info)

        return self.send_security_alert(
            title="حظر مستخدم",
            content=content,
            priority="high",
            metadata=metadata
        )
