"""
Authentication Routes
مسارات المصادقة والتحقق المحسنة
"""

from flask import Blueprint, request, jsonify, session
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

# إنشاء Blueprint
auth_bp = Blueprint("auth", __name__)

logger = logging.getLogger(__name__)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    تسجيل الدخول المحسن
    P0.1.2: Added failed login lockout mechanism
    """
    try:
        from src.services.cache_service import login_lockout_manager

        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        use_jwt = data.get("use_jwt", False)  # خيار لاستخدام JWT

        if not username or not password:
            # P0.2.4: Use unified error envelope
            return error_response(
                message="اسم المستخدم وكلمة المرور مطلوبان / Username and password are required",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # P0.1.2: Check if account is locked
        is_locked, unlock_time = login_lockout_manager.is_locked(username)
        if is_locked:
            # time imported at module level
            remaining_seconds = int(unlock_time - time.time())
            remaining_minutes = remaining_seconds // 60
            # P0.2.4: Use unified error envelope
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
                    mfa_code = data.get("mfa_code")

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
                            message="خطأ في نظام المصادقة الثنائية / MFA system error",
                            code=ErrorCodes.SYS_INTERNAL_ERROR,
                            status_code=500,
                        )

                # P0.1.2: Reset failed attempts on successful login (after MFA if enabled)
                login_lockout_manager.reset_attempts(username)

                # تسجيل دخول ناجح
                if use_jwt:
                    # استخدام JWT tokens
                    tokens = AuthManager.generate_jwt_tokens(
                        user.id,
                        user.username,
                        (
                            user.role_obj.name
                            if getattr(user, "role_obj", None)
                            else (user.role if getattr(user, "role", None) else "user")
                        ),
                    )
                    if tokens:
                        # P0.2.4: Use unified success envelope
                        return success_response(
                            data={
                                "user": {
                                    "id": user.id,
                                    "username": user.username,
                                    "full_name": user.full_name,
                                    "role": (
                                        user.role_obj.name
                                        if getattr(user, "role_obj", None)
                                        else (
                                            user.role
                                            if getattr(user, "role", None)
                                            else "user"
                                        )
                                    ),
                                },
                                "tokens": tokens,
                            },
                            message="تم تسجيل الدخول بنجاح / Login successful",
                            status_code=200,
                        )

                # استخدام Session (الطريقة التقليدية)
                session_data = AuthManager.create_session(user)
                # P0.2.4: Wrap session data in success envelope
                return success_response(
                    data=session_data,
                    message="تم تسجيل الدخول بنجاح / Login successful",
                    status_code=200,
                )
            elif user:
                # P0.1.2: Record failed attempt if user exists but password wrong
                login_lockout_manager.record_failed_attempt(username)
                # Re-check lock status after recording attempt
                is_locked_now, unlock_time = login_lockout_manager.is_locked(username)
                if is_locked_now:
                    remaining_seconds = int(unlock_time - time.time())
                    remaining_minutes = max(0, remaining_seconds // 60)
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
                remaining = login_lockout_manager.get_remaining_attempts(username)
                logger.warning(
                    f"Failed login attempt for user: {username}. Remaining attempts: {remaining}"
                )

        except Exception as db_error:
            logger.warning(f"Database error during login: {db_error}")
            # Fallback to mock authentication
            pass

        # Mock authentication للتطوير
        if username == "admin" and password == "admin123":
            # P0.1.2: Reset failed attempts on successful login
            login_lockout_manager.reset_attempts(username)

            if use_jwt:
                print(f"🔐 JWT requested for user: {username}")
                tokens = AuthManager.generate_jwt_tokens(1, username, "admin")
                print(f"🔐 JWT tokens generated: {tokens is not None}")
                if tokens:
                    print(f"🔐 Returning JWT tokens: {list(tokens.keys())}")
                    # P0.2.4: Use unified success envelope
                    return success_response(
                        data={
                            "user": {"id": 1, "username": username, "role": "admin"},
                            "tokens": tokens,
                        },
                        message="تم تسجيل الدخول بنجاح (وضع التطوير) / Login successful (dev mode)",
                        status_code=200,
                    )
                else:
                    print("🔐 JWT generation failed, falling back to session")

            # Session fallback
            session["user_id"] = 1
            session["username"] = username
            session["role"] = "admin"
            # P0.2.4: Use unified success envelope
            return success_response(
                data={"user": {"id": 1, "username": username, "role": "admin"}},
                message="تم تسجيل الدخول بنجاح (وضع التطوير) / Login successful (dev mode)",
                status_code=200,
            )
        else:
            # P0.1.2: Record failed attempt for invalid credentials
            login_lockout_manager.record_failed_attempt(username)
            # Re-check lock status after recording attempt
            is_locked_now, unlock_time = login_lockout_manager.is_locked(username)
            if is_locked_now:
                remaining_seconds = int(unlock_time - time.time())
                remaining_minutes = max(0, remaining_seconds // 60)
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
            remaining = login_lockout_manager.get_remaining_attempts(username)

            message = "اسم المستخدم أو كلمة المرور غير صحيحة / Invalid credentials"
            if remaining <= 2 and remaining > 0:
                message += (
                    f" (محاولات متبقية: {remaining} / {remaining} attempts remaining)"
                )

            # P0.2.4: Use unified error envelope
            return error_response(
                message=message,
                code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
                details={"remaining_attempts": remaining} if remaining <= 2 else None,
                status_code=401,
            )

    except Exception as e:
        logger.error(f"Login error: {e}")
        # P0.2.4: Use unified error envelope
        return error_response(
            message="خطأ في تسجيل الدخول / Login error",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    """
    تجديد JWT token
    P0.2.4: Updated to use unified error envelope
    """
    try:
        data = request.get_json(silent=True) or {}
        refresh_token = data.get("refresh_token")

        if not refresh_token:
            # P0.2.4: Use unified error envelope
            return error_response(
                message="Refresh token مطلوب / Refresh token required",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # التحقق من refresh token
        payload = AuthManager.verify_jwt_token(refresh_token, "refresh")
        if not payload:
            # P0.2.4: Use unified error envelope
            return error_response(
                message="Refresh token غير صالح أو منتهي الصلاحية / Invalid or expired refresh token",
                code=ErrorCodes.AUTH_TOKEN_EXPIRED,
                status_code=401,
            )

        # إنشاء access token جديد
        new_tokens = AuthManager.generate_jwt_tokens(
            payload["user_id"], payload["username"], payload.get("role", "user")
        )

        if new_tokens:
            # P0.2.4: Use unified success envelope (compat: expose access_token at top-level)
            return success_response(
                data={
                    "access_token": new_tokens.get("access_token"),
                    "tokens": new_tokens,
                },
                message="تم تجديد Token بنجاح / Token refreshed successfully",
                status_code=200,
            )
        else:
            # P0.2.4: Use unified error envelope
            return error_response(
                message="فشل في تجديد Token / Failed to refresh token",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=500,
            )

    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        # P0.2.4: Use unified error envelope
        return error_response(
            message="خطأ في تجديد Token / Token refresh error",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """
    تسجيل الخروج
    P0.1.1: Added JWT token revocation on logout
    """
    try:
        from flask import request
        from src.auth import AuthManager

        # Clear session
        session.clear()

        # P0.1.1: Revoke JWT tokens if provided
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]
            AuthManager.revoke_jwt_token(access_token)

        # Also check for refresh token in request body
        data = request.get_json(silent=True) or {}
        refresh_token = data.get("refresh_token")
        if refresh_token:
            AuthManager.revoke_jwt_token(refresh_token)

        # P0.2.4: Use unified success envelope
        return success_response(
            message="تم تسجيل الخروج بنجاح / Logout successful", status_code=200
        )
    except Exception as e:
        logger.error(f"Logout error: {e}")
        # P0.2.4: Use unified error envelope
        return error_response(
            message="خطأ في تسجيل الخروج / Logout error",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_bp.route("/api/auth/status", methods=["GET"])
def auth_status():
    """
    فحص حالة المصادقة
    P0.2.4: Updated to use unified success envelope
    """
    try:
        # Prefer JWT Authorization header when present
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]
            payload = AuthManager.verify_jwt_token(access_token, "access")
            if payload:
                return success_response(
                    data={
                        "authenticated": True,
                        "username": payload.get("username"),
                        "user": {
                            "id": payload.get("user_id"),
                            "username": payload.get("username"),
                            "role": payload.get("role", "user"),
                        },
                    },
                    message="مصادق / Authenticated",
                    status_code=200,
                )

        if "user_id" in session:
            # P0.2.4: Use unified success envelope
            return success_response(
                data={
                    "authenticated": True,
                    "username": session.get(
                        "username"
                    ),  # compat for tests expecting data.username
                    "user": {
                        "id": session.get("user_id"),
                        "username": session.get("username"),
                        "role": "admin",
                    },
                },
                message="مصادق / Authenticated",
                status_code=200,
            )
        else:
            # If Authorization header was supplied but invalid, return 401
            if auth_header.startswith("Bearer "):
                # Distinguish revoked vs expired/invalid for clearer client handling
                try:
                    import jwt as pyjwt  # type: ignore
                    from flask import current_app

                    # Try to decode without expiry check just to extract JTI
                    unsafe_payload = pyjwt.decode(
                        access_token,
                        current_app.config.get(
                            "JWT_SECRET_KEY", "fallback-secret-key-12345"
                        ),
                        algorithms=["HS256"],
                        options={"verify_exp": False},
                    )
                    from src.services.cache_service import jwt_revocation_list

                    jti = (
                        unsafe_payload.get("jti")
                        if isinstance(unsafe_payload, dict)
                        else None
                    )
                    if jti and jwt_revocation_list.is_revoked(jti):
                        return error_response(
                            message="تم إلغاء صلاحية الرمز / Token revoked",
                            code=ErrorCodes.AUTH_TOKEN_REVOKED,
                            status_code=401,
                        )
                except Exception:
                    pass
                return error_response(
                    message="رمز الدخول غير صالح أو منتهي / Invalid or expired token",
                    code=ErrorCodes.AUTH_TOKEN_EXPIRED,
                    status_code=401,
                )
            # Otherwise anonymous, but not an error
            return success_response(
                data={"authenticated": False},
                message="غير مصادق / Not authenticated",
                status_code=200,
            )
    except Exception as e:
        logger.error(f"Auth status error: {e}")
        # P0.2.4: Use unified error envelope
        return error_response(
            message="خطأ في فحص حالة المصادقة / Auth status check error",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """تسجيل مستخدم جديد"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password:
            return (
                jsonify(
                    {"success": False, "message": "اسم المستخدم وكلمة المرور مطلوبان"}
                ),
                400,
            )

        # Mock registration for now
        return jsonify(
            {
                "success": True,
                "message": "تم إنشاء الحساب بنجاح (قيد التطوير)",
                "user": {"username": username, "email": email},
            }
        )

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"success": False, "message": "خطأ في إنشاء الحساب"}), 500


@auth_bp.record_once
def _attach_rate_limits(state):
    """Attach stricter rate limits to sensitive auth endpoints."""
    try:
        app = state.app
        limiter = app.extensions.get("limiter") if hasattr(app, "extensions") else None
        # Some versions store extensions under a set
        if isinstance(limiter, set):
            limiter = next(iter(limiter), None)
        if limiter is None:
            sm = app.config.get("SECURITY_MIDDLEWARE", {})
            limiter = sm.get("limiter") if isinstance(sm, dict) else None
        if limiter and hasattr(limiter, "limit"):
            # Apply per-endpoint limits
            limiter.limit("5 per minute")(login)
            limiter.limit("10 per minute")(refresh_token)
            limiter.limit("10 per minute")(logout)
    except Exception as e:  # noqa: BLE001
        logger.warning("Rate limit attach failed: %s", e)
