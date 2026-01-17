# FILE: backend/src/routes/auth_routes_validated.py | PURPOSE: Auth routes
# with Pydantic validation (P2.1.2 example) | OWNER: Backend | RELATED:
# validators/auth_validators.py | LAST-AUDITED: 2025-10-27

"""
Authentication Routes with Pydantic Validation
مسارات المصادقة مع التحقق من صحة البيانات باستخدام Pydantic

This is an EXAMPLE implementation showing how to apply Pydantic validators to routes.
This demonstrates P2.1.2: Request/Response Validators integration.

To use this in production:
1. Test thoroughly
2. Replace auth_routes.py with this implementation
3. Update all route registrations in app.py
"""

from flask import Blueprint, request, jsonify, session
from pydantic import ValidationError
import logging
import time

# P0.2.4: Absolute imports to avoid package resolution issues under pytest
from src.auth import AuthManager
from src.models.user_unified import User
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# P2.1.2: Import Pydantic validators
from src.validators import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
    RefreshResponseSchema,
    UserSchema,
)

# إنشاء Blueprint
auth_validated_bp = Blueprint("auth_validated", __name__)

logger = logging.getLogger(__name__)


@auth_validated_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    تسجيل الدخول المحسن مع Pydantic validation
    P0.1.2: Added failed login lockout mechanism
    P2.1.2: Added Pydantic request validation
    """
    try:
        from src.services.cache_service import login_lockout_manager

        # P2.1.2: Validate request data with Pydantic
        try:
            data = request.get_json()
            validated_data = LoginRequestSchema(**data)
        except ValidationError as e:
            # Return validation errors in unified error envelope
            return error_response(
                message="خطأ في التحقق من البيانات / Validation error",
                code=ErrorCodes.VAL_INVALID_FORMAT,
                details={"validation_errors": e.errors()},
                status_code=400,
            )
        except Exception as e:
            return error_response(
                message="خطأ في قراءة البيانات / Invalid request data",
                code=ErrorCodes.VAL_INVALID_FORMAT,
                status_code=400,
            )

        username = validated_data.username
        password = validated_data.password
        mfa_code = validated_data.mfa_code

        # P0.1.2: Check if account is locked
        is_locked, unlock_time = login_lockout_manager.is_locked(username)
        if is_locked:
            remaining_seconds = int(unlock_time - time.time())
            remaining_minutes = remaining_seconds // 60
            return error_response(
                message=f"الحساب مقفل بسبب محاولات تسجيل دخول فاشلة متعددة. حاول مرة أخرى بعد {remaining_minutes} دقيقة / Account locked due to multiple failed login attempts",
                code=ErrorCodes.AUTH_ACCOUNT_LOCKED,
                details={
                    "locked_until": unlock_time,
                    "remaining_seconds": remaining_seconds,
                    "remaining_minutes": remaining_minutes,
                },
                status_code=429,
            )

        # البحث عن المستخدم في قاعدة البيانات
        try:
            user = User.query.filter_by(username=username).first()
            if user and AuthManager.verify_password(password, user.password_hash):
                # P0.1.3: Check if MFA is enabled for this user
                if user.mfa_enabled:
                    # If MFA code not provided, request it
                    if not mfa_code:
                        return error_response(
                            message="المصادقة الثنائية مطلوبة / MFA code required",
                            code=ErrorCodes.AUTH_MFA_REQUIRED,
                            details={"mfa_required": True, "username": username},
                            status_code=401,
                        )

                    # Verify MFA code
                    try:
                        import pyotp

                        totp = pyotp.TOTP(user.mfa_secret)
                        if not totp.verify(mfa_code, valid_window=1):
                            # Record failed attempt for invalid MFA code
                            login_lockout_manager.record_failed_attempt(username)
                            return error_response(
                                message="رمز المصادقة الثنائية غير صحيح / Invalid MFA code",
                                code=ErrorCodes.AUTH_MFA_INVALID,
                                status_code=401,
                            )
                    except ImportError:
                        logger.error("pyotp not available for MFA verification")
                        return error_response(
                            message="خدمة المصادقة الثنائية غير متوفرة / MFA service unavailable",
                            code=ErrorCodes.SYS_SERVICE_UNAVAILABLE,
                            status_code=503,
                        )

                # P0.1.2: Clear failed attempts on successful login
                login_lockout_manager.clear_failed_attempts(username)

                # P0.1.1: Generate JWT tokens with rotation
                access_token, refresh_token = AuthManager.generate_tokens(user.id)

                # تخزين معلومات المستخدم في الجلسة
                session["user_id"] = user.id
                session["username"] = user.username
                session["role"] = user.role

                # P2.1.2: Return validated response
                response_data = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "full_name": user.full_name,
                        "role": user.role,
                        "mfa_enabled": user.mfa_enabled,
                    },
                }

                return success_response(
                    data=response_data,
                    message="تم تسجيل الدخول بنجاح / Login successful",
                    status_code=200,
                )
            else:
                # P0.1.2: Record failed login attempt
                login_lockout_manager.record_failed_attempt(username)

                return error_response(
                    message="اسم المستخدم أو كلمة المرور غير صحيحة / Invalid username or password",
                    code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
                    status_code=401,
                )

        except Exception as db_error:
            logger.error(f"Database error during login: {str(db_error)}")
            return error_response(
                message="خطأ في قاعدة البيانات / Database error",
                code=ErrorCodes.DB_QUERY_ERROR,
                status_code=500,
            )

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return error_response(
            message="خطأ غير متوقع / Unexpected error",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_validated_bp.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    """
    تجديد رمز الوصول
    P0.1.1: JWT token rotation
    P2.1.2: Added Pydantic request validation
    """
    try:
        # P2.1.2: Validate request data with Pydantic
        try:
            data = request.get_json()
            validated_data = RefreshRequestSchema(**data)
        except ValidationError as e:
            return error_response(
                message="خطأ في التحقق من البيانات / Validation error",
                code=ErrorCodes.VAL_INVALID_FORMAT,
                details={"validation_errors": e.errors()},
                status_code=400,
            )

        refresh_token = validated_data.refresh_token

        # P0.1.1: Verify refresh token and generate new access token
        payload = AuthManager.verify_token(refresh_token, token_type="refresh")
        if not payload:
            return error_response(
                message="رمز التجديد غير صالح أو منتهي الصلاحية / Invalid or expired refresh token",
                code=ErrorCodes.AUTH_TOKEN_EXPIRED,
                status_code=401,
            )

        user_id = payload.get("user_id")
        if not user_id:
            return error_response(
                message="رمز التجديد غير صالح / Invalid refresh token",
                code=ErrorCodes.AUTH_TOKEN_INVALID,
                status_code=401,
            )

        # Generate new access token
        access_token = AuthManager.generate_access_token(user_id)

        # P2.1.2: Return validated response
        response_data = {"access_token": access_token}

        return success_response(
            data=response_data,
            message="تم تجديد رمز الوصول بنجاح / Access token refreshed successfully",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        return error_response(
            message="خطأ في تجديد الرمز / Error refreshing token",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_validated_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """
    تسجيل الخروج
    P0.1.1: Revoke JWT tokens
    """
    try:
        # Clear session
        session.clear()

        # TODO: Add token to blacklist/revocation list
        # This requires implementing a token blacklist in Redis or database

        return success_response(
            message="تم تسجيل الخروج بنجاح / Logout successful", status_code=200
        )

    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return error_response(
            message="خطأ في تسجيل الخروج / Error during logout",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_validated_bp.route("/api/auth/me", methods=["GET"])
def get_current_user():
    """
    الحصول على معلومات المستخدم الحالي
    P2.1.2: Returns validated user response
    """
    try:
        # Get user from session or JWT token
        user_id = session.get("user_id")

        if not user_id:
            # Try to get from Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = AuthManager.verify_token(token, token_type="access")
                if payload:
                    user_id = payload.get("user_id")

        if not user_id:
            return error_response(
                message="غير مصرح / Unauthorized",
                code=ErrorCodes.AUTH_UNAUTHORIZED,
                status_code=401,
            )

        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return error_response(
                message="المستخدم غير موجود / User not found",
                code=ErrorCodes.DB_RECORD_NOT_FOUND,
                status_code=404,
            )

        # P2.1.2: Return validated user response
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "mfa_enabled": user.mfa_enabled,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }

        return success_response(
            data=user_data,
            message="تم الحصول على معلومات المستخدم بنجاح / User information retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return error_response(
            message="خطأ في الحصول على معلومات المستخدم / Error getting user information",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
