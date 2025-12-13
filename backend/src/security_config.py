#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 إعدادات الأمان المتقدمة
Advanced Security Configuration
"""

import os
from datetime import timedelta


class SecurityConfig:
    """إعدادات الأمان الشاملة"""

    # إعدادات كلمات المرور
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SYMBOLS = True
    PASSWORD_HISTORY_COUNT = 5  # عدد كلمات المرور السابقة المحظورة

    # إعدادات الجلسات
    SESSION_TIMEOUT = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Strict"

    # إعدادات JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALGORITHM = "HS256"

    # إعدادات محاولات تسجيل الدخول
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_DURATION = timedelta(hours=1)
    LOCKOUT_ESCALATION = True  # زيادة مدة الحظر مع كل محاولة

    # إعدادات Rate Limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = timedelta(hours=1)

    # إعدادات CORS
    CORS_ORIGINS = ["http://localhost:3000", "https://yourdomain.com"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_MAX_AGE = timedelta(hours=24)

    # إعدادات التشفير
    ENCRYPTION_ALGORITHM = "AES-256-GCM"
    HASH_ALGORITHM = "SHA-256"
    SALT_LENGTH = 32

    # إعدادات Headers الأمنية
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    # إعدادات المراقبة
    MONITORING_ENABLED = True
    LOG_FAILED_LOGINS = True
    LOG_SUSPICIOUS_ACTIVITY = True
    ALERT_ON_MULTIPLE_FAILURES = True

    # إعدادات النسخ الاحتياطية
    BACKUP_ENCRYPTION = True
    BACKUP_RETENTION_DAYS = 30
    BACKUP_VERIFICATION = True

    # إعدادات التدقيق
    AUDIT_LOG_ENABLED = True
    AUDIT_LOG_RETENTION_DAYS = 90
    AUDIT_SENSITIVE_OPERATIONS = True

    @classmethod
    def get_security_level(cls):
        """تحديد مستوى الأمان الحالي"""
        score = 0
        max_score = 100

        # فحص كلمات المرور
        if cls.PASSWORD_MIN_LENGTH >= 8:
            score += 10
        if cls.PASSWORD_REQUIRE_UPPERCASE and cls.PASSWORD_REQUIRE_LOWERCASE:
            score += 10
        if cls.PASSWORD_REQUIRE_NUMBERS and cls.PASSWORD_REQUIRE_SYMBOLS:
            score += 10

        # فحص الجلسات
        if cls.SESSION_TIMEOUT <= timedelta(hours=1):
            score += 10
        if cls.SESSION_COOKIE_SECURE and cls.SESSION_COOKIE_HTTPONLY:
            score += 10

        # فحص JWT
        if cls.JWT_ACCESS_TOKEN_EXPIRES <= timedelta(hours=1):
            score += 10

        # فحص Rate Limiting
        if cls.RATE_LIMIT_ENABLED:
            score += 10

        # فحص المراقبة
        if cls.MONITORING_ENABLED and cls.LOG_FAILED_LOGINS:
            score += 10

        # فحص النسخ الاحتياطية
        if cls.BACKUP_ENCRYPTION:
            score += 10

        # فحص التدقيق
        if cls.AUDIT_LOG_ENABLED:
            score += 10

        return {
            "score": score,
            "max_score": max_score,
            "percentage": (score / max_score) * 100,
            "level": cls._get_security_grade(score, max_score),
        }

    @staticmethod
    def _get_security_grade(score, max_score):
        """تحديد درجة الأمان"""
        percentage = (score / max_score) * 100

        if percentage >= 90:
            return "A+ (ممتاز)"
        elif percentage >= 80:
            return "A (جيد جداً)"
        elif percentage >= 70:
            return "B (جيد)"
        elif percentage >= 60:
            return "C (مقبول)"
        else:
            return "D (ضعيف)"


# إعدادات البيئة
class ProductionSecurityConfig(SecurityConfig):
    """إعدادات أمان الإنتاج"""

    # إعدادات أكثر صرامة للإنتاج
    PASSWORD_MIN_LENGTH = 12
    SESSION_TIMEOUT = timedelta(minutes=15)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    MAX_LOGIN_ATTEMPTS = 2
    LOCKOUT_DURATION = timedelta(hours=2)
    RATE_LIMIT_REQUESTS = 50


class DevelopmentSecurityConfig(SecurityConfig):
    """إعدادات أمان التطوير"""

    # إعدادات أكثر مرونة للتطوير
    SESSION_TIMEOUT = timedelta(hours=8)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=30)
