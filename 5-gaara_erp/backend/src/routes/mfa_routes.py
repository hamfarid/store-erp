# FILE: backend/src/routes/mfa_routes.py | PURPOSE: P0.1.3 - MFA
# (Multi-Factor Authentication) endpoints | OWNER: Backend Security |
# RELATED: auth_routes.py, models/user.py | LAST-AUDITED: 2025-10-25

"""
MFA (Multi-Factor Authentication) Routes
TOTP-based MFA using pyotp library
"""

from flask import Blueprint, request, jsonify
import logging
import io
import base64

# P0.1.3: Import MFA dependencies
try:
    import pyotp
    import qrcode

    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    print(
        "⚠️ pyotp or qrcode not available. Install with: pip install pyotp qrcode[pil]"
    )

# Import error envelope helpers (absolute imports for pytest compatibility)
from src.auth import AuthManager
from src.models.user_unified import User
from src.database import db
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# Create blueprint
mfa_bp = Blueprint("mfa", __name__, url_prefix="/api/auth/mfa")
logger = logging.getLogger(__name__)


@mfa_bp.route("/setup", methods=["POST"])
def setup_mfa():
    """
    Setup MFA for user account

    Request:
        {
            "username": "admin",
            "password": "password"  // Required for security
        }

    Response:
        {
            "success": true,
            "code": "SUCCESS",
            "message": "MFA setup initiated",
            "data": {
                "secret": "BASE32SECRET",
                "qr_code": "data:image/png;base64,...",
                "provisioning_uri": "otpauth://totp/..."
            },
            "traceId": "uuid"
        }
    """
    if not PYOTP_AVAILABLE:
        return error_response(
            message="MFA not available. pyotp library not installed.",
            code=ErrorCodes.SYS_SERVICE_UNAVAILABLE,
            status_code=503,
        )

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return error_response(
                message="اسم المستخدم وكلمة المرور مطلوبان / Username and password required",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # Verify user credentials
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return error_response(
                message="بيانات الاعتماد غير صحيحة / Invalid credentials",
                code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
                status_code=401,
            )

        # Check if MFA already enabled
        if user.mfa_enabled:
            return error_response(
                message="المصادقة الثنائية مفعلة بالفعل / MFA already enabled",
                code=ErrorCodes.BIZ_INVALID_OPERATION,
                details={"mfa_enabled": True},
                status_code=400,
            )

        # Generate TOTP secret
        secret = pyotp.random_base32()

        # Create provisioning URI for QR code
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email, issuer_name="Arabic Inventory System"
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        qr_code_data_uri = f"data:image/png;base64,{qr_code_base64}"

        # Store secret temporarily (not enabled yet)
        user.mfa_secret = secret
        db.session.commit()

        logger.info(f"MFA setup initiated for user: {username}")

        return success_response(
            data={
                "secret": secret,
                "qr_code": qr_code_data_uri,
                "provisioning_uri": provisioning_uri,
                "instructions": {
                    "ar": "امسح رمز QR باستخدام تطبيق Google Authenticator أو Authy، ثم أدخل الرمز المكون من 6 أرقام للتحقق",
                    "en": "Scan the QR code with Google Authenticator or Authy, then enter the 6-digit code to verify",
                },
            },
            message="تم بدء إعداد المصادقة الثنائية / MFA setup initiated",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"MFA setup error: {e}")
        return error_response(
            message=f"خطأ في إعداد المصادقة الثنائية / MFA setup error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@mfa_bp.route("/verify", methods=["POST"])
def verify_mfa():
    """
    Verify MFA code and enable MFA for user

    Request:
        {
            "username": "admin",
            "code": "123456"  // 6-digit TOTP code
        }

    Response:
        {
            "success": true,
            "code": "SUCCESS",
            "message": "MFA enabled successfully",
            "data": {
                "mfa_enabled": true
            },
            "traceId": "uuid"
        }
    """
    if not PYOTP_AVAILABLE:
        return error_response(
            message="MFA not available. pyotp library not installed.",
            code=ErrorCodes.SYS_SERVICE_UNAVAILABLE,
            status_code=503,
        )

    try:
        data = request.get_json()
        username = data.get("username")
        code = data.get("code")

        if not username or not code:
            return error_response(
                message="اسم المستخدم والرمز مطلوبان / Username and code required",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # Get user
        user = User.query.filter_by(username=username).first()
        if not user:
            return error_response(
                message="المستخدم غير موجود / User not found",
                code=ErrorCodes.DB_NOT_FOUND,
                status_code=404,
            )

        # Check if secret exists
        if not user.mfa_secret:
            return error_response(
                message="لم يتم إعداد المصادقة الثنائية / MFA not set up",
                code=ErrorCodes.BIZ_INVALID_OPERATION,
                status_code=400,
            )

        # Verify TOTP code
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(
            code, valid_window=1
        ):  # Allow 1 time step tolerance (30 seconds)
            return error_response(
                message="رمز المصادقة غير صحيح / Invalid MFA code",
                code=ErrorCodes.AUTH_MFA_INVALID,
                status_code=401,
            )

        # Enable MFA
        user.mfa_enabled = True
        db.session.commit()

        logger.info(f"MFA enabled for user: {username}")

        return success_response(
            data={"mfa_enabled": True},
            message="تم تفعيل المصادقة الثنائية بنجاح / MFA enabled successfully",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"MFA verification error: {e}")
        return error_response(
            message=f"خطأ في التحقق من المصادقة الثنائية / MFA verification error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@mfa_bp.route("/disable", methods=["POST"])
def disable_mfa():
    """
    Disable MFA for user account

    Request:
        {
            "username": "admin",
            "password": "password",  // Required for security
            "code": "123456"  // Current valid TOTP code
        }

    Response:
        {
            "success": true,
            "code": "SUCCESS",
            "message": "MFA disabled successfully",
            "data": {
                "mfa_enabled": false
            },
            "traceId": "uuid"
        }
    """
    if not PYOTP_AVAILABLE:
        return error_response(
            message="MFA not available. pyotp library not installed.",
            code=ErrorCodes.SYS_SERVICE_UNAVAILABLE,
            status_code=503,
        )

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        code = data.get("code")

        if not username or not password or not code:
            return error_response(
                message="اسم المستخدم وكلمة المرور والرمز مطلوبان / Username, password and code required",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # Verify user credentials
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return error_response(
                message="بيانات الاعتماد غير صحيحة / Invalid credentials",
                code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
                status_code=401,
            )

        # Check if MFA is enabled
        if not user.mfa_enabled:
            return error_response(
                message="المصادقة الثنائية غير مفعلة / MFA not enabled",
                code=ErrorCodes.BIZ_INVALID_OPERATION,
                status_code=400,
            )

        # Verify TOTP code
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(code, valid_window=1):
            return error_response(
                message="رمز المصادقة غير صحيح / Invalid MFA code",
                code=ErrorCodes.AUTH_MFA_INVALID,
                status_code=401,
            )

        # Disable MFA
        user.mfa_enabled = False
        user.mfa_secret = None
        db.session.commit()

        logger.info(f"MFA disabled for user: {username}")

        return success_response(
            data={"mfa_enabled": False},
            message="تم تعطيل المصادقة الثنائية بنجاح / MFA disabled successfully",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"MFA disable error: {e}")
        return error_response(
            message=f"خطأ في تعطيل المصادقة الثنائية / MFA disable error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
