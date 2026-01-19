"""
Email Service Module
خدمة البريد الإلكتروني

Version: 1.0.0
Created: 2025-12-19

Supports:
- SMTP (SendGrid, AWS SES, Gmail, Custom SMTP)
- Email verification
- Password reset
- Welcome emails
- Notification emails
"""

import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class EmailProvider(str, Enum):
    """أنواع مزودي البريد الإلكتروني"""
    SENDGRID = "sendgrid"
    AWS_SES = "aws_ses"
    GMAIL = "gmail"
    CUSTOM_SMTP = "custom"


@dataclass
class EmailConfig:
    """إعدادات البريد الإلكتروني"""
    provider: EmailProvider = EmailProvider.CUSTOM_SMTP
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@gaara-scan.ai"
    from_name: str = "Gaara Scan AI"
    use_tls: bool = True
    use_ssl: bool = False
    timeout: int = 30

    @classmethod
    def from_env(cls) -> "EmailConfig":
        """إنشاء الإعدادات من متغيرات البيئة"""
        return cls(
            provider=EmailProvider(os.getenv("EMAIL_PROVIDER", "custom")),
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("FROM_EMAIL", "noreply@gaara-scan.ai"),
            from_name=os.getenv("FROM_NAME", "Gaara Scan AI"),
            use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
            use_ssl=os.getenv("SMTP_USE_SSL", "false").lower() == "true",
        )


class EmailService:
    """
    خدمة البريد الإلكتروني المركزية
    Centralized Email Service
    """

    def __init__(self, config: Optional[EmailConfig] = None):
        """تهيئة الخدمة"""
        self.config = config or EmailConfig.from_env()
        self._templates_dir = Path(__file__).parent / "email_templates"

    def _create_smtp_connection(self):
        """إنشاء اتصال SMTP"""
        try:
            if self.config.use_ssl:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(
                    self.config.smtp_host,
                    self.config.smtp_port,
                    context=context,
                    timeout=self.config.timeout
                )
            else:
                server = smtplib.SMTP(
                    self.config.smtp_host,
                    self.config.smtp_port,
                    timeout=self.config.timeout
                )
                if self.config.use_tls:
                    server.starttls()

            if self.config.smtp_user and self.config.smtp_password:
                server.login(self.config.smtp_user, self.config.smtp_password)

            return server
        except Exception as e:
            logger.error(f"Failed to create SMTP connection: {e}")
            raise

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        reply_to: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        إرسال بريد إلكتروني

        Args:
            to_email: البريد الإلكتروني للمستلم
            subject: عنوان الرسالة
            html_content: محتوى HTML
            text_content: محتوى نصي (اختياري)
            reply_to: بريد الرد (اختياري)
            cc: قائمة CC (اختياري)
            bcc: قائمة BCC (اختياري)

        Returns:
            bool: نجاح أو فشل الإرسال
        """
        try:
            # إنشاء الرسالة
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.config.from_name} <{self.config.from_email}>"
            msg["To"] = to_email

            if reply_to:
                msg["Reply-To"] = reply_to
            if cc:
                msg["Cc"] = ", ".join(cc)

            # إضافة المحتوى النصي
            if text_content:
                msg.attach(MIMEText(text_content, "plain", "utf-8"))

            # إضافة محتوى HTML
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            # إرسال البريد
            with self._create_smtp_connection() as server:
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)

                server.sendmail(
                    self.config.from_email,
                    recipients,
                    msg.as_string()
                )

            logger.info(f"✅ Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def send_verification_email(
        self,
        to_email: str,
        name: str,
        verification_token: str,
        base_url: str = "https://app.gaara-scan.ai"
    ) -> bool:
        """
        إرسال بريد التحقق من الحساب

        Args:
            to_email: البريد الإلكتروني
            name: اسم المستخدم
            verification_token: رمز التحقق
            base_url: عنوان التطبيق
        """
        verification_link = f"{base_url}/verify-email?token={verification_token}"

        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, sans-serif; direction: rtl; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #27ae60; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌱 Gaara Scan AI</h1>
                </div>
                <div class="content">
                    <h2>مرحباً {name}!</h2>
                    <p>شكراً لتسجيلك في نظام Gaara Scan AI.</p>
                    <p>يرجى النقر على الزر أدناه لتأكيد بريدك الإلكتروني:</p>
                    <center>
                        <a href="{verification_link}" class="button">تأكيد البريد الإلكتروني</a>
                    </center>
                    <p>أو انسخ الرابط التالي:</p>
                    <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 5px;">
                        {verification_link}
                    </p>
                    <p><strong>هذا الرابط صالح لمدة 24 ساعة.</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 Gaara Scan AI - نظام تشخيص أمراض النباتات</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        مرحباً {name}!

        شكراً لتسجيلك في نظام Gaara Scan AI.

        يرجى النقر على الرابط التالي لتأكيد بريدك الإلكتروني:
        {verification_link}

        هذا الرابط صالح لمدة 24 ساعة.

        --
        فريق Gaara Scan AI
        """

        return self.send_email(
            to_email=to_email,
            subject="تأكيد بريدك الإلكتروني - Gaara Scan AI",
            html_content=html_content,
            text_content=text_content
        )

    def send_password_reset_email(
        self,
        to_email: str,
        name: str,
        reset_token: str,
        base_url: str = "https://app.gaara-scan.ai"
    ) -> bool:
        """
        إرسال بريد إعادة تعيين كلمة المرور

        Args:
            to_email: البريد الإلكتروني
            name: اسم المستخدم
            reset_token: رمز إعادة التعيين
            base_url: عنوان التطبيق
        """
        reset_link = f"{base_url}/reset-password?token={reset_token}"

        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, sans-serif; direction: rtl; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #c0392b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 إعادة تعيين كلمة المرور</h1>
                </div>
                <div class="content">
                    <h2>مرحباً {name}!</h2>
                    <p>تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بحسابك.</p>
                    <center>
                        <a href="{reset_link}" class="button">إعادة تعيين كلمة المرور</a>
                    </center>
                    <div class="warning">
                        <strong>⚠️ تنبيه:</strong>
                        <ul>
                            <li>هذا الرابط صالح لمدة ساعة واحدة فقط</li>
                            <li>إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذا البريد</li>
                        </ul>
                    </div>
                    <p>أو انسخ الرابط التالي:</p>
                    <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 5px;">
                        {reset_link}
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Gaara Scan AI - نظام تشخيص أمراض النباتات</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        مرحباً {name}!

        تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بحسابك.

        يرجى النقر على الرابط التالي لإعادة تعيين كلمة المرور:
        {reset_link}

        هذا الرابط صالح لمدة ساعة واحدة فقط.

        إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذا البريد.

        --
        فريق Gaara Scan AI
        """

        return self.send_email(
            to_email=to_email,
            subject="إعادة تعيين كلمة المرور - Gaara Scan AI",
            html_content=html_content,
            text_content=text_content
        )

    def send_welcome_email(
        self,
        to_email: str,
        name: str
    ) -> bool:
        """
        إرسال بريد الترحيب

        Args:
            to_email: البريد الإلكتروني
            name: اسم المستخدم
        """
        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, sans-serif; direction: rtl; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .feature {{ display: flex; align-items: center; margin: 15px 0; padding: 10px; background: white; border-radius: 5px; }}
                .feature-icon {{ font-size: 30px; margin-left: 15px; }}
                .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌱 مرحباً بك في Gaara Scan AI!</h1>
                </div>
                <div class="content">
                    <h2>أهلاً {name}! 👋</h2>
                    <p>يسعدنا انضمامك إلى نظام Gaara Scan AI لتشخيص أمراض النباتات.</p>

                    <h3>ميزات النظام:</h3>
                    <div class="feature">
                        <span class="feature-icon">📸</span>
                        <div>
                            <strong>تشخيص بالصور</strong>
                            <p>التقط صورة لنباتك واحصل على تشخيص فوري</p>
                        </div>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🤖</span>
                        <div>
                            <strong>ذكاء اصطناعي متقدم</strong>
                            <p>نماذج AI مدربة على آلاف الصور</p>
                        </div>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">💊</span>
                        <div>
                            <strong>توصيات العلاج</strong>
                            <p>احصل على توصيات علاجية مخصصة</p>
                        </div>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">📊</span>
                        <div>
                            <strong>تتبع المزرعة</strong>
                            <p>إدارة شاملة لمحاصيلك ومزارعك</p>
                        </div>
                    </div>
                </div>
                <div class="footer">
                    <p>© 2025 Gaara Scan AI - نظام تشخيص أمراض النباتات</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            to_email=to_email,
            subject="مرحباً بك في Gaara Scan AI! 🌱",
            html_content=html_content
        )

    def send_diagnosis_notification(
        self,
        to_email: str,
        name: str,
        diagnosis_result: Dict[str, Any]
    ) -> bool:
        """
        إرسال إشعار نتيجة التشخيص

        Args:
            to_email: البريد الإلكتروني
            name: اسم المستخدم
            diagnosis_result: نتيجة التشخيص
        """
        disease_name = diagnosis_result.get("disease_name", "غير محدد")
        confidence = diagnosis_result.get("confidence", 0) * 100
        treatment = diagnosis_result.get("treatment", "يرجى مراجعة خبير زراعي")

        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, sans-serif; direction: rtl; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .result {{ background: white; padding: 20px; border-radius: 10px; border-right: 4px solid #8e44ad; }}
                .confidence {{ font-size: 24px; color: #27ae60; font-weight: bold; }}
                .treatment {{ background: #e8f5e9; padding: 15px; border-radius: 5px; margin-top: 20px; }}
                .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔬 نتيجة التشخيص</h1>
                </div>
                <div class="content">
                    <h2>مرحباً {name}!</h2>
                    <p>تم الانتهاء من تحليل صورة النبات الخاصة بك.</p>

                    <div class="result">
                        <h3>التشخيص: {disease_name}</h3>
                        <p>نسبة الثقة: <span class="confidence">{confidence:.1f}%</span></p>
                    </div>

                    <div class="treatment">
                        <h4>💊 التوصية العلاجية:</h4>
                        <p>{treatment}</p>
                    </div>

                    <p style="margin-top: 20px;">
                        <strong>ملاحظة:</strong> هذا التشخيص تقديري ويُنصح بمراجعة خبير زراعي للحالات الحرجة.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Gaara Scan AI - نظام تشخيص أمراض النباتات</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(
            to_email=to_email,
            subject=f"نتيجة التشخيص: {disease_name} - Gaara Scan AI",
            html_content=html_content
        )


# ===== Singleton Instance =====
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """الحصول على مثيل خدمة البريد الإلكتروني"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


# ===== Convenience Functions =====

async def send_password_reset_email(email: str, token: str, name: str) -> bool:
    """دالة مساعدة لإرسال بريد إعادة تعيين كلمة المرور"""
    service = get_email_service()
    return service.send_password_reset_email(email, name, token)


async def send_verification_email(email: str, token: str, name: str) -> bool:
    """دالة مساعدة لإرسال بريد التحقق"""
    service = get_email_service()
    return service.send_verification_email(email, name, token)


async def send_welcome_email(email: str, name: str) -> bool:
    """دالة مساعدة لإرسال بريد الترحيب"""
    service = get_email_service()
    return service.send_welcome_email(email, name)
