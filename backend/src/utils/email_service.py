"""
Email Service Module
@file backend/src/utils/email_service.py

خدمة إرسال البريد الإلكتروني
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class EmailConfig:
    """Email configuration from environment variables"""
    
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    DEFAULT_FROM = os.getenv('EMAIL_FROM', 'noreply@store-erp.com')
    DEFAULT_FROM_NAME = os.getenv('EMAIL_FROM_NAME', 'Store ERP')


class EmailTemplate:
    """Email templates for common scenarios"""
    
    @staticmethod
    def password_reset(reset_link: str, user_name: str) -> Dict[str, str]:
        """Template for password reset emails"""
        return {
            'subject': 'إعادة تعيين كلمة المرور - Store ERP',
            'html': f'''
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #3b82f6;">إعادة تعيين كلمة المرور</h2>
                <p>مرحباً {user_name}،</p>
                <p>لقد تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بحسابك.</p>
                <p>
                    <a href="{reset_link}" 
                       style="display: inline-block; padding: 12px 24px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 6px;">
                        إعادة تعيين كلمة المرور
                    </a>
                </p>
                <p>هذا الرابط صالح لمدة ساعة واحدة فقط.</p>
                <p>إذا لم تطلب إعادة تعيين كلمة المرور، يمكنك تجاهل هذا البريد.</p>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;" />
                <p style="color: #6b7280; font-size: 12px;">Store ERP - نظام إدارة المخازن</p>
            </div>
            ''',
            'text': f'''
            إعادة تعيين كلمة المرور
            
            مرحباً {user_name}،
            
            لقد تلقينا طلباً لإعادة تعيين كلمة المرور الخاصة بحسابك.
            
            اضغط على الرابط التالي لإعادة تعيين كلمة المرور:
            {reset_link}
            
            هذا الرابط صالح لمدة ساعة واحدة فقط.
            
            إذا لم تطلب إعادة تعيين كلمة المرور، يمكنك تجاهل هذا البريد.
            
            Store ERP - نظام إدارة المخازن
            '''
        }
    
    @staticmethod
    def two_factor_code(code: str, user_name: str) -> Dict[str, str]:
        """Template for 2FA verification code"""
        return {
            'subject': 'رمز التحقق - Store ERP',
            'html': f'''
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #3b82f6;">رمز التحقق</h2>
                <p>مرحباً {user_name}،</p>
                <p>رمز التحقق الخاص بك هو:</p>
                <p style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #3b82f6; text-align: center; padding: 20px;">
                    {code}
                </p>
                <p>هذا الرمز صالح لمدة 5 دقائق فقط.</p>
                <p>إذا لم تطلب هذا الرمز، قم بتغيير كلمة المرور فوراً.</p>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;" />
                <p style="color: #6b7280; font-size: 12px;">Store ERP - نظام إدارة المخازن</p>
            </div>
            ''',
            'text': f'''
            رمز التحقق
            
            مرحباً {user_name}،
            
            رمز التحقق الخاص بك هو: {code}
            
            هذا الرمز صالح لمدة 5 دقائق فقط.
            
            إذا لم تطلب هذا الرمز، قم بتغيير كلمة المرور فوراً.
            
            Store ERP - نظام إدارة المخازن
            '''
        }
    
    @staticmethod
    def welcome(user_name: str, login_link: str) -> Dict[str, str]:
        """Template for welcome email"""
        return {
            'subject': 'مرحباً بك في Store ERP',
            'html': f'''
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #3b82f6;">مرحباً بك في Store ERP!</h2>
                <p>مرحباً {user_name}،</p>
                <p>تم إنشاء حسابك بنجاح في نظام Store ERP.</p>
                <p>
                    <a href="{login_link}" 
                       style="display: inline-block; padding: 12px 24px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 6px;">
                        تسجيل الدخول
                    </a>
                </p>
                <p>نتمنى لك تجربة ممتعة!</p>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;" />
                <p style="color: #6b7280; font-size: 12px;">Store ERP - نظام إدارة المخازن</p>
            </div>
            ''',
            'text': f'''
            مرحباً بك في Store ERP!
            
            مرحباً {user_name}،
            
            تم إنشاء حسابك بنجاح في نظام Store ERP.
            
            يمكنك تسجيل الدخول من خلال الرابط التالي:
            {login_link}
            
            نتمنى لك تجربة ممتعة!
            
            Store ERP - نظام إدارة المخازن
            '''
        }
    
    @staticmethod
    def invoice(invoice_data: Dict[str, Any]) -> Dict[str, str]:
        """Template for invoice email"""
        items_html = ''
        for item in invoice_data.get('items', []):
            items_html += f'''
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{item.get('name', '')}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; text-align: center;">{item.get('quantity', 0)}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; text-align: left;">{item.get('price', 0):.2f}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; text-align: left;">{item.get('total', 0):.2f}</td>
            </tr>
            '''
        
        return {
            'subject': f'فاتورة رقم {invoice_data.get("number", "")} - Store ERP',
            'html': f'''
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #3b82f6;">فاتورة</h2>
                <p>رقم الفاتورة: {invoice_data.get('number', '')}</p>
                <p>التاريخ: {invoice_data.get('date', '')}</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <thead>
                        <tr style="background-color: #f3f4f6;">
                            <th style="padding: 8px; text-align: right;">المنتج</th>
                            <th style="padding: 8px; text-align: center;">الكمية</th>
                            <th style="padding: 8px; text-align: left;">السعر</th>
                            <th style="padding: 8px; text-align: left;">الإجمالي</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>
                <p style="font-size: 18px; font-weight: bold;">
                    الإجمالي: {invoice_data.get('total', 0):.2f} ج.م
                </p>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;" />
                <p style="color: #6b7280; font-size: 12px;">Store ERP - نظام إدارة المخازن</p>
            </div>
            ''',
            'text': f'فاتورة رقم {invoice_data.get("number", "")}'
        }


class EmailService:
    """Main email service class"""
    
    def __init__(self):
        self.config = EmailConfig()
        self._connection = None
    
    def _get_connection(self):
        """Get or create SMTP connection"""
        if not self.config.SMTP_USER or not self.config.SMTP_PASSWORD:
            raise ValueError("Email credentials not configured")
        
        server = smtplib.SMTP(self.config.SMTP_HOST, self.config.SMTP_PORT)
        if self.config.SMTP_USE_TLS:
            server.starttls()
        server.login(self.config.SMTP_USER, self.config.SMTP_PASSWORD)
        return server
    
    def send_email(
        self,
        to: List[str],
        subject: str,
        html_content: Optional[str] = None,
        text_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send an email
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content of the email
            attachments: List of attachments [{'filename': str, 'content': bytes, 'mime_type': str}]
            cc: List of CC recipients
            bcc: List of BCC recipients
            reply_to: Reply-to address
        
        Returns:
            bool: True if email was sent successfully
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f'{self.config.DEFAULT_FROM_NAME} <{self.config.DEFAULT_FROM}>'
            msg['To'] = ', '.join(to)
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if reply_to:
                msg['Reply-To'] = reply_to
            
            # Add text content
            if text_content:
                msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
            
            # Add HTML content
            if html_content:
                msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # Add attachments
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['content'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{attachment["filename"]}"'
                    )
                    msg.attach(part)
            
            # Get all recipients
            all_recipients = to + (cc or []) + (bcc or [])
            
            # Send email
            with self._get_connection() as server:
                server.sendmail(self.config.DEFAULT_FROM, all_recipients, msg.as_string())
            
            logger.info(f"Email sent successfully to {to}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_password_reset(self, email: str, reset_link: str, user_name: str) -> bool:
        """Send password reset email"""
        template = EmailTemplate.password_reset(reset_link, user_name)
        return self.send_email(
            to=[email],
            subject=template['subject'],
            html_content=template['html'],
            text_content=template['text']
        )
    
    def send_two_factor_code(self, email: str, code: str, user_name: str) -> bool:
        """Send 2FA verification code"""
        template = EmailTemplate.two_factor_code(code, user_name)
        return self.send_email(
            to=[email],
            subject=template['subject'],
            html_content=template['html'],
            text_content=template['text']
        )
    
    def send_welcome(self, email: str, user_name: str, login_link: str) -> bool:
        """Send welcome email"""
        template = EmailTemplate.welcome(user_name, login_link)
        return self.send_email(
            to=[email],
            subject=template['subject'],
            html_content=template['html'],
            text_content=template['text']
        )
    
    def send_invoice(self, email: str, invoice_data: Dict[str, Any], pdf_attachment: Optional[bytes] = None) -> bool:
        """Send invoice email"""
        template = EmailTemplate.invoice(invoice_data)
        attachments = None
        if pdf_attachment:
            attachments = [{
                'filename': f'invoice_{invoice_data.get("number", "")}.pdf',
                'content': pdf_attachment,
                'mime_type': 'application/pdf'
            }]
        
        return self.send_email(
            to=[email],
            subject=template['subject'],
            html_content=template['html'],
            text_content=template['text'],
            attachments=attachments
        )


# Singleton instance
email_service = EmailService()


def send_email_async(func):
    """Decorator to send emails asynchronously"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In production, use Celery or another task queue
        # For now, just call the function directly
        return func(*args, **kwargs)
    return wrapper
