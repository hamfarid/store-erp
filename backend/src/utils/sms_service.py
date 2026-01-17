"""
SMS Service Module
@file backend/src/utils/sms_service.py

خدمة إرسال الرسائل النصية
"""

import os
import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


class SMSProvider(ABC):
    """Abstract base class for SMS providers"""
    
    @abstractmethod
    def send(self, phone: str, message: str) -> bool:
        """Send SMS message"""
        pass
    
    @abstractmethod
    def send_bulk(self, phones: List[str], message: str) -> Dict[str, bool]:
        """Send SMS to multiple recipients"""
        pass
    
    @abstractmethod
    def get_balance(self) -> Optional[float]:
        """Get account balance"""
        pass


class TwilioProvider(SMSProvider):
    """Twilio SMS provider"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER', '')
        self.base_url = f'https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}'
    
    def send(self, phone: str, message: str) -> bool:
        """Send SMS via Twilio"""
        if not all([self.account_sid, self.auth_token, self.from_number]):
            logger.error("Twilio credentials not configured")
            return False
        
        try:
            response = requests.post(
                f'{self.base_url}/Messages.json',
                auth=(self.account_sid, self.auth_token),
                data={
                    'From': self.from_number,
                    'To': phone,
                    'Body': message
                }
            )
            
            if response.status_code == 201:
                logger.info(f"SMS sent to {phone}")
                return True
            else:
                logger.error(f"Failed to send SMS: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Twilio error: {str(e)}")
            return False
    
    def send_bulk(self, phones: List[str], message: str) -> Dict[str, bool]:
        """Send SMS to multiple recipients"""
        results = {}
        for phone in phones:
            results[phone] = self.send(phone, message)
        return results
    
    def get_balance(self) -> Optional[float]:
        """Get Twilio account balance"""
        try:
            response = requests.get(
                f'{self.base_url}/Balance.json',
                auth=(self.account_sid, self.auth_token)
            )
            if response.status_code == 200:
                return float(response.json().get('balance', 0))
            return None
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return None


class LocalSMSProvider(SMSProvider):
    """Local SMS gateway provider (for Saudi Arabia)"""
    
    def __init__(self):
        self.api_url = os.getenv('SMS_API_URL', '')
        self.api_key = os.getenv('SMS_API_KEY', '')
        self.sender_name = os.getenv('SMS_SENDER_NAME', 'StoreERP')
    
    def send(self, phone: str, message: str) -> bool:
        """Send SMS via local provider"""
        if not all([self.api_url, self.api_key]):
            logger.error("Local SMS credentials not configured")
            return False
        
        try:
            # Normalize Saudi phone number
            phone = self._normalize_phone(phone)
            
            response = requests.post(
                self.api_url,
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'phone': phone,
                    'message': message,
                    'sender': self.sender_name
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.info(f"SMS sent to {phone}")
                    return True
            
            logger.error(f"Failed to send SMS: {response.text}")
            return False
            
        except Exception as e:
            logger.error(f"SMS error: {str(e)}")
            return False
    
    def send_bulk(self, phones: List[str], message: str) -> Dict[str, bool]:
        """Send SMS to multiple recipients"""
        results = {}
        for phone in phones:
            results[phone] = self.send(phone, message)
        return results
    
    def get_balance(self) -> Optional[float]:
        """Get SMS balance"""
        try:
            response = requests.get(
                f'{self.api_url}/balance',
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            if response.status_code == 200:
                return float(response.json().get('balance', 0))
            return None
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return None
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize Saudi phone number to +966 format"""
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        if phone.startswith('00966'):
            phone = '+966' + phone[5:]
        elif phone.startswith('966'):
            phone = '+' + phone
        elif phone.startswith('05'):
            phone = '+966' + phone[1:]
        elif phone.startswith('5'):
            phone = '+966' + phone
        
        return phone


class SMSService:
    """Main SMS service with multiple provider support"""
    
    def __init__(self):
        self.providers = {
            'twilio': TwilioProvider(),
            'local': LocalSMSProvider()
        }
        self.default_provider = os.getenv('SMS_PROVIDER', 'local')
    
    def get_provider(self, provider_name: Optional[str] = None) -> SMSProvider:
        """Get SMS provider by name"""
        name = provider_name or self.default_provider
        return self.providers.get(name, self.providers['local'])
    
    def send(
        self,
        phone: str,
        message: str,
        provider: Optional[str] = None
    ) -> bool:
        """Send SMS message"""
        return self.get_provider(provider).send(phone, message)
    
    def send_bulk(
        self,
        phones: List[str],
        message: str,
        provider: Optional[str] = None
    ) -> Dict[str, bool]:
        """Send SMS to multiple recipients"""
        return self.get_provider(provider).send_bulk(phones, message)
    
    def get_balance(self, provider: Optional[str] = None) -> Optional[float]:
        """Get SMS balance"""
        return self.get_provider(provider).get_balance()


class SMSTemplates:
    """SMS message templates"""
    
    @staticmethod
    def verification_code(code: str) -> str:
        """Verification code template"""
        return f"رمز التحقق الخاص بك هو: {code}\nصالح لمدة 5 دقائق.\nStore ERP"
    
    @staticmethod
    def order_confirmation(order_number: str, total: float) -> str:
        """Order confirmation template"""
        return f"تم استلام طلبك رقم {order_number} بمبلغ {total:.2f} ج.م\nشكراً لتعاملكم معنا.\nStore ERP"
    
    @staticmethod
    def payment_received(amount: float, invoice_number: str) -> str:
        """Payment received template"""
        return f"تم استلام دفعة بمبلغ {amount:.2f} ج.م\nرقم الفاتورة: {invoice_number}\nStore ERP"
    
    @staticmethod
    def expiry_alert(product_name: str, expiry_date: str) -> str:
        """Product expiry alert template"""
        return f"تنبيه: المنتج {product_name} ينتهي بتاريخ {expiry_date}\nStore ERP"
    
    @staticmethod
    def low_stock_alert(product_name: str, quantity: int) -> str:
        """Low stock alert template"""
        return f"تنبيه: المخزون منخفض للمنتج {product_name}\nالكمية المتبقية: {quantity}\nStore ERP"
    
    @staticmethod
    def password_reset(reset_code: str) -> str:
        """Password reset template"""
        return f"رمز إعادة تعيين كلمة المرور: {reset_code}\nصالح لمدة ساعة واحدة.\nStore ERP"


# Singleton instance
sms_service = SMSService()
