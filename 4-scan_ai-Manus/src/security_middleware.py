# File: /home/ubuntu/clean_project/src/security_middleware.py
"""
مسار الملف: /home/ubuntu/clean_project/src/security_middleware.py

وسطاء الأمان للحماية من الهجمات الشائعة
تتضمن حماية من CSRF، XSS، SQL Injection، وهجمات أخرى
"""

import re
import time
import hashlib
import secrets
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from functools import wraps
import json
import logging
from urllib.parse import quote, unquote

class SecurityMiddleware:
    """وسطاء الأمان الشامل"""
    
    def __init__(self):
        self.rate_limits: Dict[str, List[datetime]] = {}
        self.csrf_tokens: Dict[str, Dict[str, Any]] = {}
        self.security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        
        # قوائم الحماية
        self.sql_injection_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
            r"(--|#|/\*|\*/)",
            r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
            r"(\b(OR|AND)\s+['\"].*['\"])",
            r"(INFORMATION_SCHEMA|SYSOBJECTS|SYSCOLUMNS)"
        ]
        
        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>",
            r"<object[^>]*>",
            r"<embed[^>]*>",
            r"<link[^>]*>",
            r"<meta[^>]*>"
        ]
        
        self.path_traversal_patterns = [
            r"\.\./",
            r"\.\.\\",
            r"%2e%2e%2f",
            r"%2e%2e%5c"
        ]
        
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام السجلات الأمنية"""
        self.security_logger = logging.getLogger('security_middleware')
        handler = logging.FileHandler('security_middleware.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.security_logger.addHandler(handler)
        self.security_logger.setLevel(logging.INFO)
    
    def rate_limit(self, max_requests: int = 100, window_minutes: int = 15):
        """ديكوريتر للحد من معدل الطلبات"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # استخراج IP من السياق (يجب تطبيقه حسب إطار العمل)
                client_ip = self.get_client_ip(kwargs)
                
                if self.is_rate_limited(client_ip, max_requests, window_minutes):
                    self.security_logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                    raise Exception("تم تجاوز الحد المسموح من الطلبات")
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def is_rate_limited(self, identifier: str, max_requests: int, window_minutes: int) -> bool:
        """فحص ما إذا كان المعرف محدود المعدل"""
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # إزالة الطلبات القديمة
        self.rate_limits[identifier] = [
            request_time for request_time in self.rate_limits[identifier]
            if request_time > window_start
        ]
        
        # إضافة الطلب الحالي
        self.rate_limits[identifier].append(now)
        
        # فحص الحد الأقصى
        return len(self.rate_limits[identifier]) > max_requests
    
    def validate_input(self, data: Any, input_type: str = "general") -> bool:
        """التحقق من صحة المدخلات"""
        if isinstance(data, str):
            return self.validate_string_input(data, input_type)
        elif isinstance(data, dict):
            return all(self.validate_input(v, input_type) for v in data.values())
        elif isinstance(data, list):
            return all(self.validate_input(item, input_type) for item in data)
        
        return True
    
    def validate_string_input(self, text: str, input_type: str) -> bool:
        """التحقق من صحة النص"""
        if not text:
            return True
        
        # فحص SQL Injection
        if self.detect_sql_injection(text):
            self.security_logger.warning(f"SQL injection attempt detected: {text[:100]}")
            return False
        
        # فحص XSS
        if self.detect_xss(text):
            self.security_logger.warning(f"XSS attempt detected: {text[:100]}")
            return False
        
        # فحص Path Traversal
        if self.detect_path_traversal(text):
            self.security_logger.warning(f"Path traversal attempt detected: {text[:100]}")
            return False
        
        # فحص خاص حسب نوع المدخل
        if input_type == "email":
            return self.validate_email(text)
        elif input_type == "filename":
            return self.validate_filename(text)
        elif input_type == "url":
            return self.validate_url(text)
        
        return True
    
    def detect_sql_injection(self, text: str) -> bool:
        """كشف محاولات SQL Injection"""
        text_lower = text.lower()
        
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    def detect_xss(self, text: str) -> bool:
        """كشف محاولات XSS"""
        text_lower = text.lower()
        
        for pattern in self.xss_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    def detect_path_traversal(self, text: str) -> bool:
        """كشف محاولات Path Traversal"""
        text_lower = text.lower()
        
        for pattern in self.path_traversal_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    def validate_email(self, email: str) -> bool:
        """التحقق من صحة البريد الإلكتروني"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_filename(self, filename: str) -> bool:
        """التحقق من صحة اسم الملف"""
        # منع الأحرف الخطيرة
        dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        if any(char in filename for char in dangerous_chars):
            return False
        
        # منع أسماء الملفات المحجوزة في Windows
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                         'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                         'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        
        if filename.upper() in reserved_names:
            return False
        
        return True
    
    def validate_url(self, url: str) -> bool:
        """التحقق من صحة الرابط"""
        # فحص أساسي للرابط
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(pattern, url):
            return False
        
        # منع الروابط المحلية الخطيرة
        dangerous_hosts = ['localhost', '127.0.0.1', '0.0.0.0', '::1']
        for host in dangerous_hosts:
            if host in url.lower():
                return False
        
        return True
    
    def sanitize_input(self, data: Any) -> Any:
        """تنظيف المدخلات"""
        if isinstance(data, str):
            return self.sanitize_string(data)
        elif isinstance(data, dict):
            return {k: self.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_input(item) for item in data]
        
        return data
    
    def sanitize_string(self, text: str) -> str:
        """تنظيف النص"""
        if not text:
            return text
        
        # إزالة الأحرف الخطيرة
        text = re.sub(r'[<>"\']', '', text)
        
        # تشفير الأحرف الخاصة
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text.strip()
    
    def generate_csrf_token(self, session_id: str) -> str:
        """إنشاء رمز CSRF"""
        token = secrets.token_urlsafe(32)
        
        self.csrf_tokens[token] = {
            'session_id': session_id,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=1)
        }
        
        return token
    
    def validate_csrf_token(self, token: str, session_id: str) -> bool:
        """التحقق من صحة رمز CSRF"""
        if token not in self.csrf_tokens:
            return False
        
        token_data = self.csrf_tokens[token]
        
        # فحص انتهاء الصلاحية
        if datetime.now() > token_data['expires_at']:
            del self.csrf_tokens[token]
            return False
        
        # فحص الجلسة
        if token_data['session_id'] != session_id:
            return False
        
        return True
    
    def clean_expired_tokens(self):
        """تنظيف الرموز المنتهية الصلاحية"""
        now = datetime.now()
        expired_tokens = [
            token for token, data in self.csrf_tokens.items()
            if now > data['expires_at']
        ]
        
        for token in expired_tokens:
            del self.csrf_tokens[token]
    
    def get_security_headers(self) -> Dict[str, str]:
        """الحصول على headers الأمان"""
        return self.security_headers.copy()
    
    def hash_password_secure(self, password: str, salt: Optional[str] = None) -> tuple:
        """تشفير كلمة المرور بطريقة آمنة"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # استخدام PBKDF2 مع SHA-256
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iterations
        )
        
        return password_hash.hex(), salt
    
    def verify_password_secure(self, password: str, stored_hash: str, salt: str) -> bool:
        """التحقق من كلمة المرور"""
        password_hash, _ = self.hash_password_secure(password, salt)
        return password_hash == stored_hash
    
    def encrypt_sensitive_data(self, data: str, key: Optional[str] = None) -> tuple:
        """تشفير البيانات الحساسة"""
        # تشفير بسيط باستخدام XOR (يمكن تحسينه باستخدام مكتبات تشفير متقدمة)
        if key is None:
            key = secrets.token_hex(16)
        
        encrypted = ""
        for i, char in enumerate(data):
            key_char = key[i % len(key)]
            encrypted += chr(ord(char) ^ ord(key_char))
        
        return encrypted.encode('utf-8').hex(), key
    
    def decrypt_sensitive_data(self, encrypted_data: str, key: str) -> str:
        """فك تشفير البيانات الحساسة"""
        try:
            encrypted_bytes = bytes.fromhex(encrypted_data)
            encrypted = encrypted_bytes.decode('utf-8')
            
            decrypted = ""
            for i, char in enumerate(encrypted):
                key_char = key[i % len(key)]
                decrypted += chr(ord(char) ^ ord(key_char))
            
            return decrypted
        except:
            return ""
    
    def log_security_event(self, event_type: str, description: str, 
                          severity: str = "medium", additional_data: Optional[Dict] = None):
        """تسجيل حدث أمني"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'description': description,
            'severity': severity,
            'additional_data': additional_data or {}
        }
        
        log_message = f"[{severity.upper()}] {event_type}: {description}"
        
        if severity == "critical":
            self.security_logger.critical(log_message)
        elif severity == "high":
            self.security_logger.error(log_message)
        elif severity == "medium":
            self.security_logger.warning(log_message)
        else:
            self.security_logger.info(log_message)
    
    def get_client_ip(self, request_data: Dict) -> str:
        """استخراج IP العميل"""
        # يجب تطبيق هذا حسب إطار العمل المستخدم
        return request_data.get('client_ip', '127.0.0.1')
    
    def validate_file_upload(self, filename: str, file_content: bytes, 
                           allowed_extensions: List[str], max_size: int = 5 * 1024 * 1024) -> bool:
        """التحقق من صحة رفع الملف"""
        # فحص اسم الملف
        if not self.validate_filename(filename):
            return False
        
        # فحص الامتداد
        file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
        if file_extension not in [ext.lower() for ext in allowed_extensions]:
            self.security_logger.warning(f"Invalid file extension: {file_extension}")
            return False
        
        # فحص الحجم
        if len(file_content) > max_size:
            self.security_logger.warning(f"File too large: {len(file_content)} bytes")
            return False
        
        # فحص نوع الملف من المحتوى
        if not self.validate_file_content(file_content, file_extension):
            return False
        
        return True
    
    def validate_file_content(self, file_content: bytes, expected_extension: str) -> bool:
        """التحقق من محتوى الملف"""
        # فحص أساسي للتوقيعات الشائعة
        file_signatures = {
            'jpg': [b'\xff\xd8\xff'],
            'jpeg': [b'\xff\xd8\xff'],
            'png': [b'\x89\x50\x4e\x47'],
            'gif': [b'\x47\x49\x46\x38'],
            'pdf': [b'\x25\x50\x44\x46'],
            'zip': [b'\x50\x4b\x03\x04', b'\x50\x4b\x05\x06'],
            'txt': []  # النص لا يحتاج فحص توقيع
        }
        
        if expected_extension in file_signatures:
            signatures = file_signatures[expected_extension]
            if signatures:  # إذا كان هناك توقيعات للفحص
                return any(file_content.startswith(sig) for sig in signatures)
        
        return True  # السماح بالملفات غير المعروفة

# مثيل عام للوسطاء
security_middleware = SecurityMiddleware()

def secure_endpoint(max_requests: int = 100, window_minutes: int = 15, 
                   require_csrf: bool = False, validate_input: bool = True):
    """ديكوريتر شامل لتأمين نقاط النهاية"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # تطبيق الحد من معدل الطلبات
            client_ip = security_middleware.get_client_ip(kwargs)
            if security_middleware.is_rate_limited(client_ip, max_requests, window_minutes):
                raise Exception("تم تجاوز الحد المسموح من الطلبات")
            
            # التحقق من CSRF إذا كان مطلوباً
            if require_csrf:
                csrf_token = kwargs.get('csrf_token')
                session_id = kwargs.get('session_id')
                if not csrf_token or not session_id or not security_middleware.validate_csrf_token(csrf_token, session_id):
                    raise Exception("رمز CSRF غير صحيح")
            
            # التحقق من صحة المدخلات
            if validate_input:
                for key, value in kwargs.items():
                    if not security_middleware.validate_input(value):
                        raise Exception(f"مدخل غير صحيح: {key}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    # اختبار الوسطاء
    print("بدء اختبار وسطاء الأمان...")
    
    # اختبار كشف SQL Injection
    sql_test = "SELECT * FROM users WHERE id = 1 OR 1=1"
    print(f"SQL Injection detected: {security_middleware.detect_sql_injection(sql_test)}")
    
    # اختبار كشف XSS
    xss_test = "<script>alert('XSS')</script>"
    print(f"XSS detected: {security_middleware.detect_xss(xss_test)}")
    
    # اختبار تشفير كلمة المرور
    password = "test_password_123"
    hashed, salt = security_middleware.hash_password_secure(password)
    verified = security_middleware.verify_password_secure(password, hashed, salt)
    print(f"Password verification: {verified}")
    
    # اختبار إنشاء رمز CSRF
    csrf_token = security_middleware.generate_csrf_token("session_123")
    csrf_valid = security_middleware.validate_csrf_token(csrf_token, "session_123")
    print(f"CSRF token valid: {csrf_valid}")
    
    print("انتهى اختبار وسطاء الأمان")

