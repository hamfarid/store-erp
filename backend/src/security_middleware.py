#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ Middleware أمني للنظام
Security Middleware for Enhanced Protection
"""

from functools import wraps
from flask import request, jsonify, current_app
import time
import hashlib
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta

# Initialize logger
logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Middleware أمني شامل"""

    def __init__(self, app=None):
        self.app = app
        self.failed_attempts = defaultdict(deque)
        self.blocked_ips = {}
        self.rate_limits = defaultdict(deque)

        if app:
            self.init_app(app)

    def init_app(self, app):
        """تهيئة الـ middleware مع التطبيق"""
        self.app = app

        # إعدادات افتراضية
        app.config.setdefault("MAX_LOGIN_ATTEMPTS", 3)
        app.config.setdefault("LOCKOUT_DURATION", 3600)
        app.config.setdefault("RATE_LIMIT_REQUESTS", 100)
        app.config.setdefault("RATE_LIMIT_WINDOW", 3600)

        # تطبيق الـ middleware
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def get_client_ip(self):
        """الحصول على IP العميل"""
        if request.headers.get("X-Forwarded-For"):
            return request.headers.get("X-Forwarded-For").split(",")[0].strip()
        elif request.headers.get("X-Real-IP"):
            return request.headers.get("X-Real-IP")
        else:
            return request.remote_addr

    def is_ip_blocked(self, ip):
        """التحقق من حظر IP"""
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        return False

    def block_ip(self, ip, duration=None):
        """حظر IP لفترة محددة"""
        if duration is None:
            duration = current_app.config.get("LOCKOUT_DURATION", 3600)

        self.blocked_ips[ip] = datetime.now() + timedelta(seconds=duration)

    def check_rate_limit(self, ip):
        """فحص حد المعدل"""
        now = time.time()
        window = current_app.config.get("RATE_LIMIT_WINDOW", 3600)
        max_requests = current_app.config.get("RATE_LIMIT_REQUESTS", 100)

        # تنظيف الطلبات القديمة
        while self.rate_limits[ip] and self.rate_limits[ip][0] < now - window:
            self.rate_limits[ip].popleft()

        # فحص الحد
        if len(self.rate_limits[ip]) >= max_requests:
            return False

        # إضافة الطلب الحالي
        self.rate_limits[ip].append(now)
        return True

    def log_failed_attempt(self, ip):
        """تسجيل محاولة فاشلة"""
        now = time.time()
        window = 3600  # ساعة واحدة

        # تنظيف المحاولات القديمة
        while self.failed_attempts[ip] and self.failed_attempts[ip][0] < now - window:
            self.failed_attempts[ip].popleft()

        # إضافة المحاولة الحالية
        self.failed_attempts[ip].append(now)

        # فحص الحد الأقصى
        max_attempts = current_app.config.get("MAX_LOGIN_ATTEMPTS", 3)
        if len(self.failed_attempts[ip]) >= max_attempts:
            self.block_ip(ip)
            return True

        return False

    def before_request(self):
        """معالجة قبل الطلب"""
        ip = self.get_client_ip()

        # فحص IP محظور
        if self.is_ip_blocked(ip):
            return (
                jsonify(
                    {
                        "error": "IP محظور مؤقتاً",
                        "message": "تم حظر عنوان IP الخاص بك بسبب نشاط مشبوه",
                    }
                ),
                429,
            )

        # فحص حد المعدل
        if not self.check_rate_limit(ip):
            return (
                jsonify(
                    {
                        "error": "تجاوز حد المعدل",
                        "message": "تم تجاوز الحد الأقصى للطلبات",
                    }
                ),
                429,
            )

    def after_request(self, response):
        """معالجة بعد الطلب"""
        # إضافة headers أمنية
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


def require_auth(f):
    """decorator للمصادقة المطلوبة"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # فحص المصادقة هنا
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "مصادقة مطلوبة"}), 401

        return f(*args, **kwargs)

    return decorated_function


def require_role(required_role):
    """
    Decorator to require specific role
    ديكوريتر لطلب دور محدد

    P0.3: Implemented proper RBAC with JWT claims

    Args:
        required_role: Role name required (e.g., 'مدير النظام', 'مدير المخزون')

    Usage:
        @require_role('مدير النظام')
        def admin_only_route():
            ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                logger.warning("Missing or invalid Authorization header")
                return (
                    jsonify(
                        {
                            "error": "مصادقة مطلوبة",
                            "error_en": "Authentication required",
                        }
                    ),
                    401,
                )

            # Extract token
            token = auth_header.split(" ")[1]

            try:
                # Import JWT here to avoid circular imports
                import jwt
                from flask import current_app

                # Decode and verify token
                payload = jwt.decode(
                    token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
                )

                # Get user role from token
                user_role = payload.get("role")

                if not user_role:
                    logger.warning(
                        f"Token missing role claim for user {payload.get('user_id')}"
                    )
                    return (
                        jsonify(
                            {
                                "error": "الدور غير محدد في الرمز",
                                "error_en": "Role not specified in token",
                            }
                        ),
                        403,
                    )

                # Check if user has required role
                if user_role != required_role:
                    logger.warning(
                        f"Access denied: User {payload.get('user_id')} "
                        f"has role '{user_role}', required '{required_role}'"
                    )
                    return (
                        jsonify(
                            {
                                "error": f"يتطلب دور: {required_role}",
                                "error_en": f"Required role: {required_role}",
                                "user_role": user_role,
                                "required_role": required_role,
                            }
                        ),
                        403,
                    )

                # Store user info in request context for use in route
                request.user_id = payload.get("user_id")
                request.user_role = user_role
                request.username = payload.get("username")

                logger.info(
                    f"Access granted: User {request.username} "
                    f"with role '{user_role}' accessing {request.path}"
                )

                return f(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                logger.warning("Expired token")
                return (
                    jsonify(
                        {"error": "انتهت صلاحية الرمز", "error_en": "Token expired"}
                    ),
                    401,
                )
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid token: {e}")
                return (
                    jsonify({"error": "رمز غير صالح", "error_en": "Invalid token"}),
                    401,
                )
            except Exception as e:
                logger.error(f"Authorization error: {e}")
                return (
                    jsonify(
                        {
                            "error": "خطأ في التحقق من الصلاحيات",
                            "error_en": "Authorization error",
                        }
                    ),
                    500,
                )

        return decorated_function

    return decorator


def require_admin(f):
    """
    Decorator to require admin role
    ديكوريتر لطلب دور المدير

    P0.3: Implemented proper admin authorization check

    Usage:
        @require_admin
        def admin_only_route():
            ...
    """
    return require_role("مدير النظام")(f)


def require_permission(permission):
    """
    Decorator to require specific permission
    ديكوريتر لطلب صلاحية محددة

    P0.3: Implemented permission-based access control

    Args:
        permission: Permission name (e.g., 'manage_users', 'view_reports')

    Usage:
        @require_permission('manage_users')
        def manage_users_route():
            ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return (
                    jsonify(
                        {
                            "error": "مصادقة مطلوبة",
                            "error_en": "Authentication required",
                        }
                    ),
                    401,
                )

            # Extract token
            token = auth_header.split(" ")[1]

            try:
                import jwt
                from flask import current_app

                # Decode token
                payload = jwt.decode(
                    token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
                )

                # Get user permissions from token
                user_permissions = payload.get("permissions", [])

                # Admin has all permissions
                user_role = payload.get("role")
                if user_role == "مدير النظام":
                    logger.info(
                        f"Admin user {payload.get('username')} granted permission '{permission}'"
                    )
                    request.user_id = payload.get("user_id")
                    request.user_role = user_role
                    request.username = payload.get("username")
                    return f(*args, **kwargs)

                # Check if user has required permission
                if permission not in user_permissions:
                    logger.warning(
                        f"Permission denied: User {payload.get('user_id')} "
                        f"missing permission '{permission}'"
                    )
                    return (
                        jsonify(
                            {
                                "error": f"يتطلب صلاحية: {permission}",
                                "error_en": f"Required permission: {permission}",
                                "user_permissions": user_permissions,
                            }
                        ),
                        403,
                    )

                # Store user info
                request.user_id = payload.get("user_id")
                request.user_role = user_role
                request.username = payload.get("username")

                logger.info(
                    f"Permission granted: User {request.username} "
                    f"with permission '{permission}' accessing {request.path}"
                )

                return f(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return (
                    jsonify(
                        {"error": "انتهت صلاحية الرمز", "error_en": "Token expired"}
                    ),
                    401,
                )
            except jwt.InvalidTokenError:
                return (
                    jsonify({"error": "رمز غير صالح", "error_en": "Invalid token"}),
                    401,
                )
            except Exception as e:
                logger.error(f"Permission check error: {e}")
                return (
                    jsonify(
                        {
                            "error": "خطأ في التحقق من الصلاحيات",
                            "error_en": "Permission check error",
                        }
                    ),
                    500,
                )

        return decorated_function

    return decorator


# إنشاء instance عام
security_middleware = SecurityMiddleware()
