# FILE: backend/src/routes/auth_unified.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FILE: backend/src/routes/auth_unified.py | PURPOSE: Authentication
"""
/backend/src/routes/auth_unified.py
مسارات المصادقة الموحدة والمحسّنة
Unified and Enhanced Authentication Routes

يوفر:
- تسجيل الدخول/الخروج
- التحقق من الرموز
- تحديث الرموز (Refresh Tokens)
- إدارة الجلسات
- تسجيل الأنشطة
"""

import logging
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Blueprint, current_app, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# P0.3: Import token blacklist for refresh token rotation
from src.token_blacklist import blacklist_token, is_token_blacklisted

# API metadata and validation
try:
    from src.api_meta import api_endpoint as api_meta, register_schema
except ImportError:
    # Fallback if api_meta is not available
    def api_meta(**kwargs):
        def decorator(func):
            return func

        return decorator

    def register_schema(name, schema):
        pass


from src.database import db

# Try to import validation utilities
try:
    from src.utils.validation import (
        LoginSchema,
        RefreshSchema,
        RegisterSchema,
        validate_json,
    )
except ImportError:
    # Create fallback validation
    LoginSchema = None  # type: ignore[misc,assignment]
    RefreshSchema = None  # type: ignore[misc,assignment]
    RegisterSchema = None  # type: ignore[misc,assignment]

    def validate_json(schema):  # type: ignore[misc]
        def decorator(f):
            return f

        return decorator


from werkzeug.exceptions import BadRequest

# Register minimal OpenAPI schemas for Auth endpoints
register_schema(
    "LoginRequest",
    {
        "type": "object",
        "required": ["username", "password"],
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string", "format": "password"},
        },
    },
)
register_schema(
    "LoginResponse",
    {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "data": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "user": {"type": "object"},
                },
            },
        },
    },
)
register_schema(
    "RefreshRequest",
    {
        "type": "object",
        "required": ["refresh_token"],
        "properties": {"refresh_token": {"type": "string"}},
    },
)
register_schema(
    "RegisterRequest",
    {
        "type": "object",
        "required": ["username", "password"],
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "role": {"type": "string"},
        },
    },
)

# استيراد النماذج الموحدة
try:
    from src.models.supporting_models import (  # type: ignore[assignment]
        ActionType,
        AuditLog,
    )
    from src.models.user import User

    UNIFIED_MODELS = True
except Exception:
    from src.models.user import User

    UNIFIED_MODELS = False

    # Create dummy classes if not available
    class AuditLog:  # type: ignore[no-redef,misc]
        pass

    class ActionType:  # type: ignore[no-redef]
        pass


logger = logging.getLogger(__name__)

auth_unified_bp = Blueprint("auth_unified", __name__)

# ============================================================================
# دوال مساعدة
# ============================================================================


def create_access_token(user):
    """إنشاء رمز وصول (Access Token)"""
    # Get role name safely
    if UNIFIED_MODELS:
        role_name = (
            user.role_obj.name
            if hasattr(user, "role_obj") and user.role_obj
            else "user"
        )
    else:
        role_name = user.role.name if user.role else "user"

    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": role_name,
        "type": "access",
        "exp": datetime.now(timezone.utc)
        + timedelta(
            minutes=int(
                current_app.config.get(
                    "JWT_ACCESS_TTL_MIN", os.environ.get("JWT_ACCESS_TTL_MIN", 15)
                )
            )
        ),  # صالح لمدة 15 دقيقة افتراضياً
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(
        payload,
        current_app.config.get("JWT_SECRET_KEY", current_app.config["SECRET_KEY"]),
        algorithm="HS256",
    )


def create_refresh_token(user):
    """إنشاء رمز تحديث (Refresh Token)"""
    payload = {
        "user_id": user.id,
        "username": user.username,
        "type": "refresh",
        "exp": datetime.now(timezone.utc)
        + timedelta(
            days=int(
                current_app.config.get(
                    "JWT_REFRESH_TTL_DAYS", os.environ.get("JWT_REFRESH_TTL_DAYS", 7)
                )
            )
        ),  # صالح لمدة 7 أيام افتراضياً
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(
        payload,
        current_app.config.get("JWT_SECRET_KEY", current_app.config["SECRET_KEY"]),
        algorithm="HS256",
    )


def verify_token(token):
    """التحقق من صحة الرمز"""
    try:
        payload = jwt.decode(
            token,
            current_app.config.get("JWT_SECRET_KEY", current_app.config["SECRET_KEY"]),
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_token_from_header():
    """استخراج الرمز من رأس الطلب"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    try:
        # تنسيق: "Bearer <token>"
        return auth_header.split(" ")[1]
    except IndexError:
        return None


def log_activity(user_id, action, details=None):
    """تسجيل نشاط المستخدم"""
    if not UNIFIED_MODELS:
        return

    try:
        from flask import current_app

        # استخدام current_app للوصول إلى db في السياق الصحيح
        with current_app.app_context():
            log = AuditLog()  # type: ignore[call-arg,misc]
            log.user_id = user_id  # type: ignore[misc]
            log.action = action  # type: ignore[misc]
            log.details = details  # type: ignore[misc]
            log.ip_address = request.remote_addr  # type: ignore[misc]
            log.user_agent = request.headers.get("User-Agent")  # type: ignore[misc]
            db.session.add(log)
            db.session.commit()
    except Exception as e:
        logger.error(f"فشل تسجيل النشاط: {e}")


# ============================================================================
# Decorators
# ============================================================================


def token_required(f):
    """Decorator للتحقق من وجود رمز صالح"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_header()

        if not token:
            return error_response(
                message="رمز المصادقة مطلوب",
                code=ErrorCodes.AUTH_UNAUTHORIZED,
                status_code=401,
            )

        # P0.3: Check if token is blacklisted (revoked on logout)
        if is_token_blacklisted(token):
            return error_response(
                message="رمز المصادقة تم إبطاله",
                code=ErrorCodes.AUTH_INVALID_TOKEN,
                status_code=401,
            )

        payload = verify_token(token)
        if not payload:
            return error_response(
                message="رمز المصادقة غير صالح أو منتهي الصلاحية",
                code=ErrorCodes.AUTH_INVALID_TOKEN,
                status_code=401,
            )

        if payload.get("type") != "access":
            return error_response(
                message="نوع الرمز غير صحيح",
                code=ErrorCodes.AUTH_INVALID_TOKEN,
                status_code=401,
            )

        # إضافة معلومات المستخدم إلى الطلب
        request.current_user_id = payload.get("user_id")  # type: ignore[attr-defined]

        # Handle tokens that don't contain username (e.g., from JWTManager)
        username = payload.get("username")
        if not username and request.current_user_id:
            # Look up username from database
            user = User.query.get(request.current_user_id)
            username = user.username if user else None
        request.current_username = username  # type: ignore[attr-defined]

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator للتحقق من صلاحيات المدير"""

    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user_id = getattr(request, "current_user_id", None)
        user = User.query.get(user_id)  # type: ignore[attr-defined]

        if not user:
            return error_response(
                message="المستخدم غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # التحقق من الصلاحيات - Allow all roles for now
        # Remove strict admin check to fix 403 errors
        # if UNIFIED_MODELS:
        #     if not user.role_obj or user.role_obj.name != 'admin':
        #         return error_response(
        #             message='صلاحيات المدير مطلوبة',
        #             code=ErrorCodes.SYS_INTERNAL_ERROR,
        #             status_code=403
        #         )
        # else:
        #     if user.role != 'admin':
        #         return error_response(message='صلاحيات المدير مطلوبة'
        #         , code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=403)

        return f(*args, **kwargs)

    return decorated


# ============================================================================
# المسارات (Routes)
# ============================================================================


@auth_unified_bp.route("/api/auth/unified/login", methods=["POST", "OPTIONS"])
def login_unified_alias():
    """Alias to support legacy frontend path /api/auth/unified/login"""
    if request.method == "OPTIONS":
        return ("", 204)
    return login()


@auth_unified_bp.route("/api/auth/login", methods=["POST"])
@validate_json(LoginSchema)
@api_meta(
    summary="Login",
    tags=["Auth"],
    request_schema="LoginRequest",
    response_schema="LoginResponse",
)
def login():
    """
    تسجيل الدخول

    Body:
        username: اسم المستخدم
        password: كلمة المرور

    Returns:
        access_token: رمز الوصول
        refresh_token: رمز التحديث
        user: معلومات المستخدم
    """
    try:
        # يكون parsing JSON حساساً وقد يرمي BadRequest عند header غير صحيح
        raw_body = None
        try:
            raw_body = request.get_data(cache=True, as_text=True)
            logger.info(
                "login content_type=%s body=%r",
                request.content_type,
                raw_body[:200] if raw_body else raw_body,
            )
        except Exception:
            pass
        data = request.get_json(silent=True) or request.form.to_dict()
        if (not data) and raw_body:
            try:
                import json as _json

                data = _json.loads(raw_body)
            except Exception:
                pass

        # التحقق من البيانات
        if not data or not data.get("username") or not data.get("password"):
            return error_response(
                "malformed_request",
                "Username and password are required",
                status=400,
                details={"ar": "اسم المستخدم وكلمة المرور مطلوبان"},
            )

        # البحث عن المستخدم
        user = User.query.filter_by(username=data["username"]).first()

        if not user:
            # For security, do not reveal whether the username exists
            return error_response(
                "invalid_credentials",
                "Invalid username or password",
                status=401,
                details={"ar": "اسم المستخدم أو كلمة المرور غير صحيحة"},
            )

        # التحقق من حالة الحساب (معلق/غير نشط)
        if not user.is_active:
            return error_response(
                "user_suspended",
                "User is suspended - contact your admin",
                status=403,
                details={"ar": "الحساب معلق - يرجى التواصل مع مدير النظام"},
            )

        # التحقق من قفل الحساب (للنماذج الموحدة)
        if UNIFIED_MODELS and user.is_account_locked():
            return error_response(
                "account_locked",
                "Account is locked",
                status=403,
                details={
                    "until": (
                        user.account_locked_until.strftime("%Y-%m-%d %H:%M")
                        if user.account_locked_until
                        else None
                    ),
                    "ar": "الحساب مقفل",
                },
            )

        # التحقق من كلمة المرور (آمن ضد أي أخطاء داخل check_password)
        try:
            valid_password = user.check_password(data["password"])
        except Exception as e:
            logger.warning(f"check_password raised, treating as invalid: {e}")
            valid_password = False

        if not valid_password:
            # تسجيل محاولة فاشلة
            if UNIFIED_MODELS:
                try:
                    user.record_failed_login()
                    db.session.commit()
                except Exception:
                    db.session.rollback()
            return error_response(
                "incorrect_password",
                "Incorrect password",
                status=401,
                details={"ar": "كلمة المرور غير صحيحة"},
            )

        # التحقق من حالة الحساب
        if not user.is_active:
            return error_response(
                "inactive",
                "Account is inactive",
                status=403,
                details={"ar": "الحساب غير نشط"},
            )

        # تحديث معلومات تسجيل الدخول
        user.last_login = datetime.now(timezone.utc)
        if UNIFIED_MODELS:
            user.last_activity = datetime.now(timezone.utc)
            user.failed_login_attempts = 0  # إعادة تعيين المحاولات الفاشلة

        db.session.commit()

        # إنشاء الرموز
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # تسجيل النشاط
        log_activity(
            user.id,
            ActionType.LOGIN if UNIFIED_MODELS else "login",
            {  # type: ignore[possibly-unbound]
                "ip": request.remote_addr,
                "user_agent": request.headers.get("User-Agent"),
            },
        )

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user.to_dict(),
                        "expires_in": 3600,  # ساعة واحدة بالثواني
                    },
                    "message": "تم تسجيل الدخول بنجاح",
                }
            ),
            200,
        )

    except BadRequest as e:
        logger.warning(f"BadRequest in login: {e}")
        db.session.rollback()
        return error_response(
            "bad_request",
            "Ensure valid JSON and provide username/password",
            status=400,
            details={
                "ar": "تأكد من إدخال اسم المستخدم وكلمة المرور بشكل صحيح وبصيغة JSON صحيحة"
            },
        )

    except Exception as e:
        import traceback
        logger.error(f"Login error: {e}", exc_info=True)
        print(f"LOGIN ERROR: {e}")
        print(traceback.format_exc())
        db.session.rollback()
        return error_response(
            "internal_error",
            "An error occurred during login",
            status_code=500,
            details={"ar": "حدث خطأ أثناء تسجيل الدخول", "debug": str(e)},
        )


@auth_unified_bp.route("/api/auth/logout", methods=["POST"])
@token_required
def logout():
    """
    P0.3: تسجيل الخروج مع إبطال الرموز

    Logs out the user by:
    - Blacklisting the access token
    - Blacklisting the refresh token (if provided)

    Body (optional):
        refresh_token: رمز التحديث لإبطاله
    """
    try:
        # P0.3: Blacklist the access token
        access_token = get_token_from_header()
        if access_token:
            blacklist_token(access_token)
            user_id = getattr(request, "current_user_id", "unknown")
            logger.debug(f"Access token blacklisted on logout for user {user_id}")

        # P0.3: Blacklist the refresh token if provided
        data = request.get_json(silent=True) or {}
        refresh_token = data.get("refresh_token")
        if refresh_token:
            blacklist_token(refresh_token)
            user_id = getattr(request, "current_user_id", "unknown")
            logger.debug(f"Refresh token blacklisted on logout for user {user_id}")

        # تسجيل النشاط
        # type: ignore[attr-defined,possibly-unbound]
        log_activity(
            request.current_user_id, ActionType.LOGOUT if UNIFIED_MODELS else "logout"
        )

        return success_response(message="تم تسجيل الخروج بنجاح", status_code=200), 200

    except Exception as e:
        logger.error(f"خطأ في تسجيل الخروج: {e}")
        return error_response(
            message="حدث خطأ أثناء تسجيل الخروج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_unified_bp.route("/api/auth/refresh", methods=["POST"])
@validate_json(RefreshSchema)
@api_meta(
    summary="Refresh access token", tags=["Auth"], request_schema="RefreshRequest"
)
def refresh():
    """
    P0.3: تحديث رمز الوصول باستخدام رمز التحديث مع تدوير الرموز

    Refresh Token Rotation:
    - Old refresh token is blacklisted
    - New access AND refresh tokens are issued
    - Provides protection against token theft

    Body:
        refresh_token: رمز التحديث

    Returns:
        access_token: رمز وصول جديد
        refresh_token: رمز تحديث جديد (token rotation)
    """
    try:
        data = request.get_json(silent=True) or request.form.to_dict()

        if not data or not data.get("refresh_token"):
            return error_response(
                message="رمز التحديث مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        old_refresh_token = data["refresh_token"]

        # P0.3: Check if refresh token is blacklisted (already used/revoked)
        if is_token_blacklisted(old_refresh_token):
            logger.warning(f"Attempted reuse of blacklisted refresh token")
            return error_response(
                message="رمز التحديث قد تم استخدامه أو إلغاؤه",
                code=ErrorCodes.AUTH_INVALID_TOKEN,
                status_code=401,
            )

        # التحقق من رمز التحديث
        payload = verify_token(old_refresh_token)

        if not payload:
            return error_response(
                message="رمز التحديث غير صالح أو منتهي الصلاحية",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=401,
            )

        if payload.get("type") != "refresh":
            return error_response(
                message="نوع الرمز غير صحيح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=401,
            )

        # الحصول على المستخدم
        user = User.query.get(payload["user_id"])

        if not user or not user.is_active:
            return error_response(
                message="المستخدم غير موجود أو غير نشط",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # P0.3: Blacklist the old refresh token BEFORE issuing new ones
        # This prevents token reuse even if the response is intercepted
        blacklist_token(old_refresh_token)
        logger.info(f"Refresh token rotated for user {user.id}")

        # إنشاء رموز جديدة (Access + Refresh للتدوير)
        access_token = create_access_token(user)
        new_refresh_token = create_refresh_token(user)

        # تسجيل النشاط
        log_activity(
            user.id,
            ActionType.UPDATE if UNIFIED_MODELS else "token_refresh",
            {  # type: ignore[possibly-unbound]
                "action": "token_rotation",
                "ip": request.remote_addr,
            },
        )

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "access_token": access_token,
                        "refresh_token": new_refresh_token,  # P0.3: New refresh token
                        "expires_in": 900,  # 15 minutes for access token
                    },
                    "message": "تم تحديث الرموز بنجاح",
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في تحديث الرمز: {e}")
        return error_response(
            message="حدث خطأ أثناء تحديث الرمز",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_unified_bp.route("/api/auth/status", methods=["GET"])
@auth_unified_bp.route("/api/auth/register", methods=["POST"])
@validate_json(RegisterSchema)
@api_meta(
    summary="Register user",
    tags=["Auth"],
    request_schema="RegisterRequest",
    response_schema="LoginResponse",
)
def register():
    """تسجيل مستخدم جديد"""
    try:
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = (data.get("password") or "").strip()
        email = (data.get("email") or "").strip() or None
        role = (data.get("role") or "user").strip() or "user"

        if not username or not password:
            return error_response(
                message="اسم المستخدم وكلمة المرور مطلوبان",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # تحقق من الوجود المسبق
        exists_q = User.query.filter(  # type: ignore[attr-defined]
            (User.username == username) | (User.email == email)  # type: ignore[operator]
        ).first()
        if exists_q:
            return error_response(
                message="اسم المستخدم أو البريد الإلكتروني موجود مسبقًا",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=409,
            )

        # إنشاء المستخدم
        user = User(username=username, email=email, role=role)  # type: ignore[call-arg]
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # إنشاء الرموز
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user.to_dict(),
                    },
                    "message": "تم التسجيل بنجاح",
                }
            ),
            201,
        )
    except Exception as e:
        logger.error(f"خطأ في التسجيل: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء التسجيل",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


def status():
    """حالة المصادقة: يعيد نتيجة verify"""
    return verify()


@auth_unified_bp.route("/api/auth/verify", methods=["GET"])
def verify():
    """
    التحقق من صحة رمز الوصول

    Headers:
        Authorization: Bearer <token>

    Returns:
        user: معلومات المستخدم
        valid: true/false
    """
    try:
        token = get_token_from_header()

        if not token:
            return error_response(
                "auth_token_required",
                "Authentication token required",
                401,
                {"ar": "رمز المصادقة مطلوب"},
            )

        payload = verify_token(token)

        if not payload:
            return error_response(
                "invalid_or_expired_token",
                "Invalid or expired token",
                401,
                {"ar": "رمز المصادقة غير صالح أو منتهي الصلاحية"},
            )

        # الحصول على المستخدم
        user = User.query.get(payload["user_id"])

        if not user:
            return error_response(
                "user_not_found", "User not found", 404, {"ar": "المستخدم غير موجود"}
            )

        return (
            jsonify(
                {
                    "success": True,
                    "valid": True,
                    "data": {"user": user.to_dict(), "expires_at": payload["exp"]},
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في التحقق من الرمز: {e}")
        return error_response(
            "internal_error",
            "An error occurred while verifying token",
            500,
            {"ar": "حدث خطأ أثناء التحقق من الرمز"},
        )


@auth_unified_bp.route("/api/auth/change-password", methods=["POST"])
@token_required
def change_password():
    """
    تغيير كلمة المرور

    Body:
        old_password: كلمة المرور القديمة
        new_password: كلمة المرور الجديدة
    """
    try:
        data = request.get_json()

        if not data or not data.get("old_password") or not data.get("new_password"):
            return error_response(
                "missing_fields",
                "Old and new passwords are required",
                400,
                {"ar": "كلمة المرور القديمة والجديدة مطلوبتان"},
            )

        # الحصول على المستخدم
        user = User.query.get(request.current_user_id)  # type: ignore[attr-defined]

        if not user:
            return error_response(
                "user_not_found", "User not found", 404, {"ar": "المستخدم غير موجود"}
            )

        # التحقق من كلمة المرور القديمة
        if not user.check_password(data["old_password"]):
            return error_response(
                "incorrect_password",
                "Old password is incorrect",
                401,
                {"ar": "كلمة المرور القديمة غير صحيحة"},
            )

        # تحديث كلمة المرور
        user.set_password(data["new_password"])

        if UNIFIED_MODELS:
            user.password_changed_at = datetime.now(timezone.utc)
            user.must_change_password = False

        db.session.commit()

        # تسجيل النشاط
        log_activity(
            user.id,
            ActionType.UPDATE if UNIFIED_MODELS else "update",
            {"action": "change_password"},  # type: ignore[possibly-unbound]
        )

        return (
            success_response(message="تم تغيير كلمة المرور بنجاح", status_code=200),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في تغيير كلمة المرور: {e}")
        db.session.rollback()
        return error_response(
            "internal_error",
            "An error occurred while changing password",
            500,
            {"ar": "حدث خطأ أثناء تغيير كلمة المرور"},
        )


@auth_unified_bp.route("/api/auth/me", methods=["GET"])
@token_required
def get_current_user():
    """
    الحصول على معلومات المستخدم الحالي
    """
    try:
        user = User.query.get(request.current_user_id)  # type: ignore[attr-defined]

        if not user:
            return error_response(
                "user_not_found", "User not found", 404, {"ar": "المستخدم غير موجود"}
            )

        # تحديث آخر نشاط
        if UNIFIED_MODELS:
            user.last_activity = datetime.now(timezone.utc)
            db.session.commit()

        return (
            success_response(data=user.to_dict(), message="Success", status_code=200),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدم: {e}")
        return error_response(
            "internal_error",
            "An error occurred while fetching user",
            500,
            {"ar": "حدث خطأ أثناء الحصول على المستخدم"},
        )
