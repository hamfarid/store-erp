#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.69: Email Service Integration

Email sending functionality with templates and async support.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from pathlib import Path

logger = logging.getLogger(__name__)


# =============================================================================
# Configuration
# =============================================================================


@dataclass
class EmailConfig:
    """Email configuration."""

    smtp_server: str = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.environ.get("MAIL_PORT", "587"))
    use_tls: bool = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    use_ssl: bool = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    username: str = os.environ.get("MAIL_USERNAME", "")
    password: str = os.environ.get("MAIL_PASSWORD", "")
    default_sender: str = os.environ.get("MAIL_DEFAULT_SENDER", "")
    max_recipients: int = int(os.environ.get("MAIL_MAX_RECIPIENTS", "50"))


# =============================================================================
# Email Templates
# =============================================================================

EMAIL_TEMPLATES = {
    "welcome": {
        "subject": "مرحباً بك في {app_name}",
        "html": """
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
        <h1 style="color: #4F46E5;">مرحباً {name}! 👋</h1>
        <p>شكراً لتسجيلك في {app_name}.</p>
        <p>يمكنك الآن البدء في استخدام جميع ميزات النظام.</p>
        <a href="{login_url}" style="display: inline-block; background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-top: 20px;">تسجيل الدخول</a>
    </div>
</body>
</html>
""",
        "text": "مرحباً {name}! شكراً لتسجيلك في {app_name}. يمكنك الآن تسجيل الدخول: {login_url}",
    },
    "password_reset": {
        "subject": "إعادة تعيين كلمة المرور - {app_name}",
        "html": """
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
        <h1 style="color: #4F46E5;">إعادة تعيين كلمة المرور 🔐</h1>
        <p>مرحباً {name},</p>
        <p>تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بك.</p>
        <p>انقر على الزر أدناه لإعادة تعيين كلمة المرور:</p>
        <a href="{reset_url}" style="display: inline-block; background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0;">إعادة تعيين كلمة المرور</a>
        <p style="color: #666; font-size: 12px;">هذا الرابط صالح لمدة 24 ساعة فقط.</p>
        <p style="color: #666; font-size: 12px;">إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذا البريد.</p>
    </div>
</body>
</html>
""",
        "text": "مرحباً {name}, انقر على الرابط التالي لإعادة تعيين كلمة المرور: {reset_url}",
    },
    "invoice": {
        "subject": "فاتورة جديدة #{invoice_number} - {app_name}",
        "html": """
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
        <h1 style="color: #4F46E5;">فاتورة #{invoice_number} 📄</h1>
        <p>مرحباً {customer_name},</p>
        <p>مرفق فاتورتك الجديدة.</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background: #f8f9fa;">
                <td style="padding: 10px; border: 1px solid #ddd;">رقم الفاتورة</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{invoice_number}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">التاريخ</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{date}</td>
            </tr>
            <tr style="background: #f8f9fa;">
                <td style="padding: 10px; border: 1px solid #ddd;">المبلغ الإجمالي</td>
                <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #4F46E5;">{total}</td>
            </tr>
        </table>
        <a href="{invoice_url}" style="display: inline-block; background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">عرض الفاتورة</a>
    </div>
</body>
</html>
""",
        "text": "فاتورة #{invoice_number} بقيمة {total}. التاريخ: {date}. عرض الفاتورة: {invoice_url}",
    },
    "low_stock_alert": {
        "subject": "⚠️ تنبيه: مخزون منخفض - {app_name}",
        "html": """
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
        <h1 style="color: #f59e0b;">⚠️ تنبيه مخزون منخفض</h1>
        <p>المنتجات التالية وصلت إلى الحد الأدنى للمخزون:</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background: #4F46E5; color: white;">
                <th style="padding: 10px; text-align: right;">المنتج</th>
                <th style="padding: 10px; text-align: center;">الكمية الحالية</th>
                <th style="padding: 10px; text-align: center;">الحد الأدنى</th>
            </tr>
            {products_rows}
        </table>
        <a href="{inventory_url}" style="display: inline-block; background: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">عرض المخزون</a>
    </div>
</body>
</html>
""",
        "text": "تنبيه مخزون منخفض:\n{products_text}\nعرض المخزون: {inventory_url}",
    },
    "order_confirmation": {
        "subject": "تأكيد الطلب #{order_number} - {app_name}",
        "html": """
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
        <h1 style="color: #10b981;">✅ تم تأكيد الطلب</h1>
        <p>مرحباً {customer_name},</p>
        <p>تم استلام طلبك بنجاح.</p>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>رقم الطلب:</strong> {order_number}</p>
            <p><strong>التاريخ:</strong> {date}</p>
            <p><strong>المبلغ الإجمالي:</strong> {total}</p>
        </div>
        <p>سيتم إرسال إشعار عند شحن طلبك.</p>
    </div>
</body>
</html>
""",
        "text": "تم تأكيد الطلب #{order_number}. المبلغ: {total}. التاريخ: {date}",
    },
}


# =============================================================================
# Email Service
# =============================================================================


class EmailService:
    """
    P2.69: Email service for sending transactional emails.

    Features:
    - SMTP support
    - HTML and plain text emails
    - Email templates
    - Attachments
    - Async sending (with Celery if available)
    """

    def __init__(self, config: EmailConfig = None):
        self.config = config or EmailConfig()
        self._connection = None

    def send(
        self,
        to: List[str],
        subject: str,
        html: str = None,
        text: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[Dict[str, Any]] = None,
        reply_to: str = None,
        sender: str = None,
    ) -> bool:
        """
        Send an email.

        Args:
            to: List of recipient email addresses
            subject: Email subject
            html: HTML body
            text: Plain text body
            cc: CC recipients
            bcc: BCC recipients
            attachments: List of {'filename': str, 'content': bytes, 'mimetype': str}
            reply_to: Reply-to address
            sender: Sender address (defaults to config)

        Returns:
            True if sent successfully
        """
        if not to:
            logger.warning("P2.69: No recipients specified")
            return False

        if len(to) > self.config.max_recipients:
            logger.warning(
                f"P2.69: Too many recipients ({len(to)}), max is {self.config.max_recipients}"
            )
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender or self.config.default_sender
            msg["To"] = ", ".join(to)

            if cc:
                msg["Cc"] = ", ".join(cc)
            if reply_to:
                msg["Reply-To"] = reply_to

            # Add text body
            if text:
                msg.attach(MIMEText(text, "plain", "utf-8"))

            # Add HTML body
            if html:
                msg.attach(MIMEText(html, "html", "utf-8"))

            # Add attachments
            if attachments:
                for attachment in attachments:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment["content"])
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={attachment['filename']}",
                    )
                    msg.attach(part)

            # Collect all recipients
            all_recipients = list(to)
            if cc:
                all_recipients.extend(cc)
            if bcc:
                all_recipients.extend(bcc)

            # Send email
            with self._get_connection() as server:
                server.sendmail(
                    sender or self.config.default_sender,
                    all_recipients,
                    msg.as_string(),
                )

            logger.info(f"P2.69: Email sent to {len(all_recipients)} recipients")
            return True

        except Exception as e:
            logger.error(f"P2.69: Failed to send email: {e}")
            return False

    def send_template(
        self, template_name: str, to: List[str], context: Dict[str, Any], **kwargs
    ) -> bool:
        """
        Send an email using a predefined template.

        Args:
            template_name: Name of the template
            to: List of recipients
            context: Template variables
            **kwargs: Additional arguments for send()
        """
        template = EMAIL_TEMPLATES.get(template_name)

        if not template:
            logger.error(f"P2.69: Template '{template_name}' not found")
            return False

        # Format template with context
        subject = template["subject"].format(**context)
        html = template["html"].format(**context)
        text = template.get("text", "").format(**context)

        return self.send(to=to, subject=subject, html=html, text=text, **kwargs)

    def _get_connection(self):
        """Get SMTP connection."""
        if self.config.use_ssl:
            server = smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port)
        else:
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            if self.config.use_tls:
                server.starttls()

        if self.config.username and self.config.password:
            server.login(self.config.username, self.config.password)

        return server

    # ==========================================================================
    # Convenience Methods
    # ==========================================================================

    def send_welcome_email(
        self, email: str, name: str, app_name: str, login_url: str
    ) -> bool:
        """Send welcome email to new user."""
        return self.send_template(
            "welcome",
            to=[email],
            context={"name": name, "app_name": app_name, "login_url": login_url},
        )

    def send_password_reset(
        self, email: str, name: str, reset_url: str, app_name: str
    ) -> bool:
        """Send password reset email."""
        return self.send_template(
            "password_reset",
            to=[email],
            context={"name": name, "reset_url": reset_url, "app_name": app_name},
        )

    def send_invoice(
        self,
        email: str,
        customer_name: str,
        invoice_number: str,
        date: str,
        total: str,
        invoice_url: str,
        app_name: str,
        attachment: bytes = None,
    ) -> bool:
        """Send invoice email."""
        attachments = []
        if attachment:
            attachments.append(
                {
                    "filename": f"Invoice_{invoice_number}.pdf",
                    "content": attachment,
                    "mimetype": "application/pdf",
                }
            )

        return self.send_template(
            "invoice",
            to=[email],
            context={
                "customer_name": customer_name,
                "invoice_number": invoice_number,
                "date": date,
                "total": total,
                "invoice_url": invoice_url,
                "app_name": app_name,
            },
            attachments=attachments,
        )

    def send_low_stock_alert(
        self,
        emails: List[str],
        products: List[Dict[str, Any]],
        inventory_url: str,
        app_name: str,
    ) -> bool:
        """Send low stock alert to admins."""
        # Build products table rows
        products_rows = ""
        products_text = ""

        for p in products:
            products_rows += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{p['name']}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: #f59e0b; font-weight: bold;">{p['quantity']}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{p['min_level']}</td>
            </tr>
            """
            products_text += (
                f"- {p['name']}: {p['quantity']} (الحد الأدنى: {p['min_level']})\n"
            )

        return self.send_template(
            "low_stock_alert",
            to=emails,
            context={
                "products_rows": products_rows,
                "products_text": products_text,
                "inventory_url": inventory_url,
                "app_name": app_name,
            },
        )


# Global instance
email_service = EmailService()


__all__ = ["EmailService", "EmailConfig", "email_service", "EMAIL_TEMPLATES"]
