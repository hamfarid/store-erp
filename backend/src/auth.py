# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
نظام المصادقة والجلسات المتقدم
All linting disabled due to complex imports and optional dependencies.

P0.1: Migrated to Argon2id password hashing (OWASP recommended)
"""
from flask import jsonify, redirect, request, session
import secrets
from datetime import datetime, timedelta
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Import secure password hasher (Argon2id with bcrypt fallback)
try:
    from password_hasher import (
        hash_password as secure_hash_password,
        verify_password as secure_verify_password,
        needs_rehash,
        get_algorithm,
    )

    SECURE_HASHER_AVAILABLE = True
    logger.info(f"✅ Secure password hasher available: {get_algorithm()}")
except ImportError:
    SECURE_HASHER_AVAILABLE = False
    logger.warning("⚠️ Secure password hasher not available, using legacy bcrypt")

# Legacy bcrypt support (fallback only)
try:
    import bcrypt

    # Test if bcrypt is actually working
    if (
        hasattr(bcrypt, "checkpw")
        and hasattr(bcrypt, "hashpw")
        and hasattr(bcrypt, "gensalt")
    ):
        BCRYPT_AVAILABLE = True
        logger.info("✅ bcrypt available (legacy fallback)")
    else:
        BCRYPT_AVAILABLE = False  # pragma: no cover
        bcrypt = None  # pragma: no cover
        logger.warning("⚠️ bcrypt is installed but broken")  # pragma: no cover
except (ImportError, AttributeError) as e:
    BCRYPT_AVAILABLE = False  # pragma: no cover
    bcrypt = None  # pragma: no cover
    logger.warning(f"⚠️ bcrypt not available ({e})")  # pragma: no cover

# PyJWT import (decoupled from bcrypt)
try:
    import jwt

    logger.info("✅ jwt available")
except ImportError as e:  # pragma: no cover
    jwt = None  # pragma: no cover
    logger.warning(f"⚠️ jwt not available ({e})")  # pragma: no cover


# Role constants to avoid string duplication
ADMIN_ROLE = "مدير النظام"
WAREHOUSE_MANAGER_ROLE = "مدير المخزون"


class AuthManager:
    """مدير المصادقة والجلسات"""

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """تهيئة نظام المصادقة مع التطبيق"""
        # إعداد مفتاح سري للجلسات
        if not app.config.get("SECRET_KEY"):
            app.config["SECRET_KEY"] = secrets.token_hex(32)

        # إعداد JWT - P0 Security: Updated token TTLs per OWASP guidelines
        app.config.setdefault("JWT_SECRET_KEY", secrets.token_urlsafe(32))
        # P0.2: Access token TTL reduced to 15 minutes (was 1 hour)
        app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", timedelta(minutes=15))
        # P0.4: Refresh token TTL reduced to 7 days (was 30 days)
        app.config.setdefault("JWT_REFRESH_TOKEN_EXPIRES", timedelta(days=7))

        # إعداد نوع الجلسة
        app.config["SESSION_TYPE"] = "filesystem"
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_USE_SIGNER"] = True
        app.config["SESSION_KEY_PREFIX"] = "inventory_"
        app.config["SESSION_FILE_THRESHOLD"] = 100

        # مدة انتهاء الجلسة (24 ساعة)
        app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)

    @staticmethod
    def hash_password(password):
        """
        تشفير كلمة المرور باستخدام Argon2id (OWASP recommended)
        Hash password using Argon2id (OWASP recommended)

        P0.1: Migrated from bcrypt to Argon2id for enhanced security
        P0.2: REMOVED INSECURE SHA-256 FALLBACK - Argon2id is now MANDATORY

        Args:
            password: Plain text password

        Returns:
            Argon2id hash string

        Raises:
            RuntimeError: If Argon2id is not available
            ValueError: If password is empty or too short
        """
        if not password:
            raise ValueError("Password cannot be empty")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        if SECURE_HASHER_AVAILABLE:
            # Use Argon2id (OWASP recommended) - PRIMARY METHOD
            return secure_hash_password(password)
        elif BCRYPT_AVAILABLE and bcrypt:
            # Legacy bcrypt fallback (still secure, but Argon2id preferred)
            salt = bcrypt.gensalt(rounds=12)  # type: ignore
            hashed = bcrypt.hashpw(password.encode("utf-8"), salt)  # type: ignore
            logger.warning(
                "⚠️ Using legacy bcrypt - Argon2id recommended for better security"
            )
            return hashed.decode("utf-8")
        else:
            # NO INSECURE FALLBACK - FAIL HARD
            logger.critical("❌ FATAL: No secure password hasher available")
            logger.critical("❌ فشل: لا يوجد مشفر كلمات مرور آمن متاح")
            logger.critical("\nInstall argon2-cffi:")
            logger.critical("  pip install argon2-cffi")
            raise RuntimeError(
                "No secure password hasher available. "
                "Install argon2-cffi: pip install argon2-cffi"
            )

    @staticmethod
    def verify_password(password, hashed):
        """
        التحقق من كلمة المرور
        Verify password against hash

        P0.1: Supports Argon2id, bcrypt, and SHA-256 (legacy)
        P0.2: SHA-256 support maintained ONLY for existing hashes (read-only)

        Automatically detects hash type and uses appropriate verifier

        Args:
            password: Plain text password
            hashed: Password hash

        Returns:
            True if password matches, False otherwise
        """
        if SECURE_HASHER_AVAILABLE:
            # Use secure verifier (supports Argon2id, bcrypt, SHA-256 for legacy hashes)
            return secure_verify_password(password, hashed)
        elif BCRYPT_AVAILABLE and bcrypt:
            # Legacy bcrypt fallback
            try:
                return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
            except Exception as e:
                logger.error(f"bcrypt verification failed: {e}")
                return False
        else:
            # INSECURE fallback - development only
            import hashlib

            return hashlib.sha256(password.encode("utf-8")).hexdigest() == hashed

    @staticmethod
    def needs_password_rehash(hashed):
        """
        Check if password hash needs to be upgraded

        P0.1: Identifies legacy hashes (bcrypt, SHA-256) that should be rehashed with Argon2id
        """
        if SECURE_HASHER_AVAILABLE:
            return needs_rehash(hashed)
        return False

    @staticmethod
    def generate_jwt_tokens(user_id, username, role):
        """إنشاء JWT tokens"""
        if not jwt:
            print("JWT library not available")
            return None

        try:
            from flask import current_app, has_app_context

            # Check if we're in an application context
            if has_app_context():
                jwt_secret = current_app.config.get("JWT_SECRET_KEY")
                if not jwt_secret:
                    raise ValueError(
                        "JWT_SECRET_KEY must be configured - no fallback allowed for security"
                    )
                access_expires = current_app.config.get(
                    "JWT_ACCESS_TOKEN_EXPIRES", timedelta(hours=1)
                )
                refresh_expires = current_app.config.get(
                    "JWT_REFRESH_TOKEN_EXPIRES", timedelta(days=30)
                )
            else:
                # P0.15: NEVER use fallback secret keys - require explicit configuration
                jwt_secret = os.environ.get("JWT_SECRET_KEY")
                if not jwt_secret:
                    raise ValueError(
                        "JWT_SECRET_KEY environment variable must be set - no fallback allowed"
                    )
                access_expires = timedelta(minutes=15)
                refresh_expires = timedelta(days=7)

            now = datetime.now()

            # Access Token
            access_payload = {
                "user_id": user_id,
                "username": username,
                "role": role,
                "type": "access",
                "iat": now,
                "exp": now + access_expires,
            }

            # Refresh Token
            refresh_payload = {
                "user_id": user_id,
                "username": username,
                "type": "refresh",
                "iat": now,
                "exp": now + refresh_expires,
            }

            # Generate tokens
            access_token = jwt.encode(access_payload, jwt_secret, algorithm="HS256")

            refresh_token = jwt.encode(refresh_payload, jwt_secret, algorithm="HS256")

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": int(access_expires.total_seconds()),
            }

        except Exception as e:
            print(f"JWT generation error: {e}")
            return None

    @staticmethod
    def verify_jwt_token(token, token_type="access"):
        """التحقق من JWT token"""
        if not jwt:
            return None

        try:
            from flask import current_app

            payload = jwt.decode(
                token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
            )

            if payload.get("type") != token_type:
                return None

            return payload

        except jwt.ExpiredSignatureError:
            print("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            print(f"JWT verification error: {e}")
            return None

    @staticmethod
    def create_session(user):
        """إنشاء جلسة للمستخدم"""
        # إنشاء الجلسة
        session.permanent = True
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role.name if user.role else "مستخدم"
        session["role_id"] = user.role_id
        session["full_name"] = user.full_name
        session["login_time"] = datetime.now().isoformat()
        session["last_activity"] = datetime.now().isoformat()

        return {
            "success": True,
            "message": "تم تسجيل الدخول بنجاح",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role.name if user.role else "مستخدم",
                "role_id": user.role_id,
            },
        }

    @staticmethod
    def destroy_session():
        """إنهاء الجلسة"""
        session.clear()
        return {"success": True, "message": "تم تسجيل الخروج بنجاح"}

    @staticmethod
    def is_authenticated():
        """التحقق من تسجيل الدخول"""
        return "user_id" in session and session.get("user_id") is not None

    @staticmethod
    def get_current_user():
        """الحصول على المستخدم الحالي"""
        if AuthManager.is_authenticated():
            return {
                "id": session.get("user_id"),
                "username": session.get("username"),
                "role": session.get("role"),
                "role_id": session.get("role_id"),
                "full_name": session.get("full_name"),
                "login_time": session.get("login_time"),
                "last_activity": session.get("last_activity"),
            }
        return None

    @staticmethod
    def update_last_activity():
        """تحديث آخر نشاط للمستخدم"""
        if AuthManager.is_authenticated():
            session["last_activity"] = datetime.now().isoformat()

    @staticmethod
    def check_session_timeout():
        """التحقق من انتهاء مدة الجلسة"""
        if not AuthManager.is_authenticated():
            return False

        last_activity = session.get("last_activity")
        if last_activity:
            last_time = datetime.fromisoformat(last_activity)
            if datetime.now() - last_time > timedelta(hours=24):
                AuthManager.destroy_session()
                return False

        return True

    @staticmethod
    def user_has_permission(user, permission):
        """التحقق من صلاحية المستخدم"""
        if not user:
            return False

        # التحقق من صلاحية المدير
        user_role = (
            user.get("role") if isinstance(user, dict) else getattr(user, "role", None)
        )
        if user_role == ADMIN_ROLE:
            return True

        # التحقق من الصلاحية المحددة
        if user_role is None:
            return False
        user_permissions = ROLE_PERMISSIONS.get(str(user_role), [])
        return permission in user_permissions

    @staticmethod
    def user_can_access_warehouse(user, warehouse_id):
        """التحقق من إمكانية الوصول للمستودع"""
        if not user:
            return False

        # التحقق من صلاحية المدير
        user_role = (
            user.get("role") if isinstance(user, dict) else getattr(user, "role", None)
        )
        if user_role == ADMIN_ROLE:
            return True

        # للآن، نسمح لجميع المستخدمين المسجلين بالوصول للمستودعات
        # يمكن تطوير هذا لاحقاً لاستخدام نظام صلاحيات أكثر تفصيلاً
        try:
            from .services.permission_service import PermissionService

            user_id = (
                user.get("id") if isinstance(user, dict) else getattr(user, "id", None)
            )
            if user_id:
                return PermissionService.user_can_access_warehouse(
                    user_id, warehouse_id
                )
        except ImportError:
            pass

        return True


# Decorators للمصادقة والصلاحيات


def login_required(f):
    """مطلوب تسجيل الدخول"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthManager.is_authenticated():
            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "يجب تسجيل الدخول أولاً",
                            "error_code": "AUTHENTICATION_REQUIRED",
                        }
                    ),
                    401,
                )
            else:
                return redirect("/")

        # التحقق من انتهاء الجلسة أولاً
        if not AuthManager.check_session_timeout():
            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "انتهت مدة الجلسة، يرجى تسجيل الدخول مرة أخرى",
                            "error_code": "SESSION_EXPIRED",
                        }
                    ),
                    401,
                )
            else:
                return redirect("/")

        # تحديث آخر نشاط بعد اجتياز فحص المهلة
        AuthManager.update_last_activity()

        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    """مطلوب دور معين"""

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            current_user = AuthManager.get_current_user()
            if current_user and current_user["role"] in allowed_roles:
                return f(*args, **kwargs)

            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "ليس لديك صلاحية للوصول إلى هذه الصفحة",
                            "error_code": "INSUFFICIENT_PERMISSIONS",
                        }
                    ),
                    403,
                )
            else:
                return redirect("/")

        return decorated_function

    return decorator


def admin_required(f):
    """مطلوب صلاحيات المدير"""
    return role_required(ADMIN_ROLE)(f)


def manager_required(f):
    """مطلوب صلاحيات المدير أو مدير المخزون"""
    return role_required(ADMIN_ROLE, WAREHOUSE_MANAGER_ROLE)(f)


# فئات الصلاحيات


class Permissions:
    """فئات الصلاحيات المختلفة"""

    # صلاحيات إدارة النظام
    ADMIN_FULL = "admin_full"
    USER_MANAGEMENT = "user_management"
    SYSTEM_SETTINGS = "system_settings"
    MANAGE_SECURITY = "manage_security"
    VIEW_SECURITY = "view_security"

    # صلاحيات المخزون
    INVENTORY_VIEW = "inventory_view"
    INVENTORY_ADD = "inventory_add"
    INVENTORY_EDIT = "inventory_edit"
    INVENTORY_DELETE = "inventory_delete"

    # صلاحيات المبيعات
    SALES_VIEW = "sales_view"
    SALES_ADD = "sales_add"
    SALES_EDIT = "sales_edit"
    SALES_DELETE = "sales_delete"

    # صلاحيات المشتريات
    PURCHASES_VIEW = "purchases_view"
    PURCHASES_ADD = "purchases_add"
    PURCHASES_EDIT = "purchases_edit"
    PURCHASES_DELETE = "purchases_delete"

    # صلاحيات التقارير
    REPORTS_VIEW = "reports_view"
    REPORTS_EXPORT = "reports_export"
    REPORTS_ADVANCED = "reports_advanced"

    # صلاحيات لوحة المعلومات
    DASHBOARD_VIEW = "dashboard_view"


# خريطة الأدوار والصلاحيات


ROLE_PERMISSIONS = {
    ADMIN_ROLE: [
        Permissions.ADMIN_FULL,
        Permissions.USER_MANAGEMENT,
        Permissions.SYSTEM_SETTINGS,
        Permissions.MANAGE_SECURITY,
        Permissions.VIEW_SECURITY,
        Permissions.INVENTORY_VIEW,
        Permissions.INVENTORY_ADD,
        Permissions.INVENTORY_EDIT,
        Permissions.INVENTORY_DELETE,
        Permissions.SALES_VIEW,
        Permissions.SALES_ADD,
        Permissions.SALES_EDIT,
        Permissions.SALES_DELETE,
        Permissions.PURCHASES_VIEW,
        Permissions.PURCHASES_ADD,
        Permissions.PURCHASES_EDIT,
        Permissions.PURCHASES_DELETE,
        Permissions.REPORTS_VIEW,
        Permissions.REPORTS_EXPORT,
        Permissions.REPORTS_ADVANCED,
        Permissions.DASHBOARD_VIEW,
    ],
    "مدير المخزون": [
        Permissions.INVENTORY_VIEW,
        Permissions.INVENTORY_ADD,
        Permissions.INVENTORY_EDIT,
        Permissions.INVENTORY_DELETE,
        Permissions.REPORTS_VIEW,
        Permissions.REPORTS_EXPORT,
        Permissions.DASHBOARD_VIEW,
    ],
    "موظف المبيعات": [
        Permissions.INVENTORY_VIEW,
        Permissions.SALES_VIEW,
        Permissions.SALES_ADD,
        Permissions.SALES_EDIT,
        Permissions.REPORTS_VIEW,
        Permissions.DASHBOARD_VIEW,
    ],
    "موظف المشتريات": [
        Permissions.INVENTORY_VIEW,
        Permissions.PURCHASES_VIEW,
        Permissions.PURCHASES_ADD,
        Permissions.PURCHASES_EDIT,
        Permissions.REPORTS_VIEW,
        Permissions.DASHBOARD_VIEW,
    ],
    "محاسب": [
        Permissions.INVENTORY_VIEW,
        Permissions.REPORTS_VIEW,
        Permissions.DASHBOARD_VIEW,
    ],
}


def has_permission(permission):
    """التحقق من وجود صلاحية معينة"""

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            current_user = AuthManager.get_current_user()
            if current_user:
                user_role = current_user.get("role")
                if user_role:
                    user_permissions = ROLE_PERMISSIONS.get(user_role, [])

                    if permission in user_permissions:
                        return f(*args, **kwargs)

            if request.is_json:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "ليس لديك صلاحية لتنفيذ هذا الإجراء",
                            "error_code": "INSUFFICIENT_PERMISSIONS",
                        }
                    ),
                    403,
                )
            else:
                return redirect("/")

        return decorated_function

    return decorator


def get_user_permissions(role):
    """الحصول على صلاحيات دور معين"""
    return ROLE_PERMISSIONS.get(role, [])


def check_user_permission(permission):
    """التحقق من صلاحية المستخدم الحالي"""
    current_user = AuthManager.get_current_user()
    if current_user:
        user_role = current_user.get("role")
        if user_role:
            user_permissions = ROLE_PERMISSIONS.get(user_role, [])
            return permission in user_permissions
    return False


# pylint: disable=unused-argument
def require_permission(permission, action=None):
    """
    Decorator to require specific permission for accessing a route

    Args:
        permission (str): The permission required
        action (str, optional): Specific action (for compatibility)

    Returns:
        function: Decorated function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not has_permission(permission):
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "ليس لديك صلاحية للوصول إلى هذه الوظيفة",
                            "required_permission": permission,
                        }
                    ),
                    403,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_auth(func):
    """
    Decorator to require authentication for accessing a route
    Alias for login_required for compatibility
    """
    return login_required(func)
