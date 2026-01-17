"""
نظام الأمان المتقدم
Advanced Security System
"""

import secrets
import time
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta, timezone
import re

# ============================================================================
# CSRF Protection
# ============================================================================


class CSRFProtection:
    """حماية CSRF"""

    def __init__(self):
        self.tokens = {}

    def generate_token(self, session_id):
        """توليد CSRF token"""
        token = secrets.token_urlsafe(32)
        self.tokens[session_id] = {
            "token": token,
            "created_at": datetime.now(timezone.utc),
        }
        return token

    def validate_token(self, session_id, token):
        """التحقق من CSRF token"""
        if session_id not in self.tokens:
            return False

        stored = self.tokens[session_id]

        # Check if token expired (1 hour)
        if datetime.now(timezone.utc) - stored["created_at"] > timedelta(hours=1):
            del self.tokens[session_id]
            return False

        return stored["token"] == token


csrf_protection = CSRFProtection()


# ============================================================================
# Rate Limiting
# ============================================================================


class RateLimiter:
    """تحديد معدل الطلبات"""

    def __init__(self):
        self.requests = {}

    def is_allowed(self, identifier, max_requests=100, window=60):
        """
        التحقق من السماح بالطلب

        Args:
            identifier: معرف المستخدم (IP أو user_id)
            max_requests: الحد الأقصى للطلبات
            window: النافذة الزمنية بالثواني
        """
        now = time.time()

        # Clean old entries
        self.requests = {
            k: v for k, v in self.requests.items() if now - v["start_time"] < window
        }

        if identifier not in self.requests:
            self.requests[identifier] = {"count": 1, "start_time": now}
            return True

        entry = self.requests[identifier]

        if now - entry["start_time"] >= window:
            # Reset window
            self.requests[identifier] = {"count": 1, "start_time": now}
            return True

        if entry["count"] >= max_requests:
            return False

        entry["count"] += 1
        return True


rate_limiter = RateLimiter()


def rate_limit(max_requests=100, window=60):
    """
    Decorator لتحديد معدل الطلبات

    Usage:
        @rate_limit(max_requests=10, window=60)
        def my_route():
            pass
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get identifier (IP or user_id)
            identifier = request.remote_addr

            if not rate_limiter.is_allowed(identifier, max_requests, window):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "تم تجاوز الحد الأقصى للطلبات",
                            "error_en": "Rate limit exceeded",
                            "retry_after": window,
                        }
                    ),
                    429,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# ============================================================================
# Input Sanitization
# ============================================================================


def sanitize_input(text):
    """تنظيف المدخلات من الأحرف الخطرة"""
    if not isinstance(text, str):
        return text

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Remove SQL injection attempts
    dangerous_patterns = [
        r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b)",
        r"(--|;|\/\*|\*\/)",
        r"(\bOR\b\s+\d+\s*=\s*\d+)",
        r"(\bAND\b\s+\d+\s*=\s*\d+)",
    ]

    for pattern in dangerous_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Remove script tags
    text = re.sub(
        r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL
    )

    return text.strip()


def sanitize_dict(data):
    """تنظيف جميع القيم في dictionary"""
    if not isinstance(data, dict):
        return data

    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_input(v) if isinstance(v, str) else v for v in value
            ]
        else:
            sanitized[key] = value

    return sanitized


# ============================================================================
# Password Security
# ============================================================================


class PasswordPolicy:
    """سياسة كلمات المرور"""

    @staticmethod
    def validate_strength(password):
        """
        التحقق من قوة كلمة المرور

        Returns:
            tuple: (is_valid, errors, strength_score)
        """
        errors = []
        score = 0

        # Length check
        if len(password) < 8:
            errors.append("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
        else:
            score += 1

        if len(password) >= 12:
            score += 1

        # Uppercase check
        if not re.search(r"[A-Z]", password):
            errors.append("يجب أن تحتوي على حرف كبير واحد على الأقل")
        else:
            score += 1

        # Lowercase check
        if not re.search(r"[a-z]", password):
            errors.append("يجب أن تحتوي على حرف صغير واحد على الأقل")
        else:
            score += 1

        # Digit check
        if not re.search(r"\d", password):
            errors.append("يجب أن تحتوي على رقم واحد على الأقل")
        else:
            score += 1

        # Special character check
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("يجب أن تحتوي على رمز خاص واحد على الأقل")
        else:
            score += 1

        # Common passwords check
        common_passwords = ["password", "12345678", "qwerty", "admin123", "password123"]
        if password.lower() in common_passwords:
            errors.append("كلمة المرور شائعة جداً")
            score = 0

        is_valid = len(errors) == 0

        # Calculate strength
        if score <= 2:
            strength = "ضعيف"
        elif score <= 4:
            strength = "متوسط"
        else:
            strength = "قوي"

        return is_valid, errors, strength


# ============================================================================
# File Upload Security
# ============================================================================


class FileUploadSecurity:
    """أمان رفع الملفات"""

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
    }
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def allowed_file(filename):
        """التحقق من امتداد الملف"""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in FileUploadSecurity.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def validate_file_size(file):
        """التحقق من حجم الملف"""
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning

        return size <= FileUploadSecurity.MAX_FILE_SIZE

    @staticmethod
    def generate_safe_filename(filename):
        """توليد اسم ملف آمن"""
        # Remove path components
        filename = filename.split("/")[-1].split("\\")[-1]

        # Remove dangerous characters
        filename = re.sub(r"[^a-zA-Z0-9._-]", "", filename)

        # Add timestamp to prevent collisions
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        return f"{name}_{timestamp}.{ext}" if ext else f"{name}_{timestamp}"


# ============================================================================
# Security Headers
# ============================================================================


def add_security_headers(response):
    """إضافة headers أمنية"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# ============================================================================
# Audit Log
# ============================================================================


def log_security_event(event_type, user_id=None, ip_address=None, details=None):
    """تسجيل حدث أمني"""
    from src.utils.logging_config import logger

    event = {
        "type": event_type,
        "user_id": user_id,
        "ip_address": ip_address or request.remote_addr,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details or {},
    }

    logger.warning(f"Security Event: {event_type}", extra=event)
