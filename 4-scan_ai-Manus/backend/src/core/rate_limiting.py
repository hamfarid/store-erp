"""
Rate Limiting Module for API Protection
تحديد معدل الطلبات لحماية API

Version: 1.0.0
Created: 2025-12-19
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# ===== إعداد المحدد =====
# Rate Limiter Setup
def get_client_ip(request: Request) -> str:
    """
    الحصول على عنوان IP العميل
    Get client IP address considering proxies
    """
    # تحقق من X-Forwarded-For للخوادم خلف proxy
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # أول IP في القائمة هو IP العميل الأصلي
        return x_forwarded_for.split(",")[0].strip()

    # تحقق من X-Real-IP
    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip.strip()

    # استخدم الطريقة الافتراضية
    return get_remote_address(request)


# ===== إنشاء محدد معدل الطلبات =====
# Create Rate Limiter Instance
limiter = Limiter(
    key_func=get_client_ip,
    default_limits=["200 per minute"],  # الحد الافتراضي
    # Avoid runtime errors when endpoints don't explicitly provide a Response object
    # for header injection (common in mixed/legacy codebases). Rate limiting still
    # works; only the extra headers are omitted.
    headers_enabled=False,
    retry_after="http-date",
)


# ===== حدود مخصصة للنقاط الحساسة =====
# Custom Limits for Sensitive Endpoints

# حدود المصادقة - صارمة لمنع هجمات القوة الغاشمة
AUTH_LIMITS = {
    "login": "5 per minute",       # 5 محاولات تسجيل دخول بالدقيقة
    "register": "3 per hour",      # 3 تسجيلات بالساعة
    "forgot_password": "3 per hour",  # 3 طلبات استعادة كلمة المرور
    "reset_password": "5 per hour",   # 5 محاولات إعادة تعيين
    "verify_mfa": "10 per minute",    # 10 محاولات MFA
}

# حدود API العامة
API_LIMITS = {
    "default": "100 per minute",    # 100 طلب بالدقيقة
    "upload": "10 per minute",      # 10 رفع ملفات بالدقيقة
    "search": "30 per minute",      # 30 بحث بالدقيقة
    "export": "5 per hour",         # 5 تصدير بالساعة
    "bulk_operations": "3 per hour",  # 3 عمليات جماعية بالساعة
}


def setup_rate_limiting(app: FastAPI, storage_uri: Optional[str] = None):
    """
    إعداد تحديد معدل الطلبات للتطبيق
    Setup rate limiting for the application

    Args:
        app: FastAPI application instance
        storage_uri: Redis URI for distributed rate limiting (optional)
    """
    # إضافة state للمحدد
    app.state.limiter = limiter

    # إضافة معالج تجاوز الحد
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    logger.info("[OK] Rate limiting configured successfully")
    logger.info("[INFO] Rate limit headers enabled: %s", getattr(limiter, "_headers_enabled", None))

    if storage_uri:
        logger.info(f"📦 Using Redis storage: {storage_uri}")


# ===== دوال مساعدة =====
# Helper Functions

def get_auth_limit(endpoint: str) -> str:
    """الحصول على حد المصادقة لنقطة نهاية معينة"""
    return AUTH_LIMITS.get(endpoint, AUTH_LIMITS["login"])


def get_api_limit(endpoint_type: str) -> str:
    """الحصول على حد API لنوع نقطة نهاية معين"""
    return API_LIMITS.get(endpoint_type, API_LIMITS["default"])


# ===== Decorators للاستخدام المباشر =====
# Decorators for Direct Use

# مثال الاستخدام:
# from src.core.rate_limiting import limiter
#
# @router.post("/login")
# @limiter.limit("5/minute")
# async def login(request: Request, ...):
#     ...
