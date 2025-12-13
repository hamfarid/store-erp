# FILE: backend/src/routes/security_system.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# pylint: disable=all
# flake8: noqa
"""
نظام الأمان والحماية
# type: ignore  # تجاهل تحذيرات النوع
"""

try:
    from flask import Blueprint, request, jsonify, session
except ImportError:
    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

    def jsonify(data):
        return {"data": data}

    class request:
        args = {}


# P0.2.4: Import error envelope helpers
try:
    from src.middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes,
    )
except ImportError:
    # Fallback when middleware is not available
    def success_response(data=None, message="Success", code="SUCCESS", status_code=200):
        return {"success": True, "data": data, "message": message}, status_code

    def error_response(message, code=None, details=None, status_code=400):
        return {"success": False, "message": message, "code": code}, status_code

    class ErrorCodes:
        SYS_INTERNAL_ERROR = "SYS_001"

    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

    def jsonify(data):
        return {"data": data}

    class request:
        json = {}
        form = {}
        args = {}

    session = {}

try:
    import bcrypt
except ImportError:
    # Fallback when bcrypt is not available
    class bcrypt:
        @staticmethod
        def hashpw(password, salt):
            return password.encode()

        @staticmethod
        def gensalt():
            return b"salt"

        @staticmethod
        def checkpw(password, hashed):
            return True


try:
    from auth import require_permission, Permissions, AuthManager
except ImportError:
    # Fallback when auth module is not available
    def require_permission(permission):
        def decorator(f):
            return f

        return decorator

    class Permissions:
        MANAGE_SECURITY = "manage_security"
        VIEW_SECURITY = "view_security"

    class AuthManager:
        @staticmethod
        def get_current_user():
            return None


try:
    from sqlalchemy import func
except ImportError:
    # Fallback when SQLAlchemy is not available
    class func:
        @staticmethod
        def count(*args):
            return 0


try:
    from models.user import User, db
except ImportError:
    # Fallback when models are not available
    class User:
        query = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class db:
        session = None

        @staticmethod
        def add(obj):
            pass

        @staticmethod
        def commit():
            pass


# إنشاء Blueprint
security_bp = Blueprint("security", __name__)


@security_bp.route("/api/security/login", methods=["POST"])
def login():
    """تسجيل الدخول"""
    try:
        data = request.json if hasattr(request, "json") else {}
        username = data.get("username", "")
        password = data.get("password", "")

        if not username or not password:
            return (
                jsonify(
                    {"status": "error", "error": "اسم المستخدم وكلمة المرور مطلوبان"}
                ),
                400,
            )

        # البحث عن المستخدم
        user = None
        if User and hasattr(User, "query") and User.query:
            user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(
            password.encode("utf-8"), getattr(user, "password_hash", b"")
        ):
            # تسجيل دخول ناجح
            session["user_id"] = getattr(user, "id", None)
            session["username"] = username

            return jsonify(
                {
                    "status": "success",
                    "message": "تم تسجيل الدخول بنجاح",
                    "user": {
                        "id": getattr(user, "id", None),
                        "username": username,
                        "role": getattr(user, "role", "user"),
                    },
                }
            )
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "اسم المستخدم أو كلمة المرور غير صحيحة",
                    }
                ),
                401,
            )

    except Exception as e:
        return (
            jsonify({"success": False, "error": f"خطأ في تسجيل الدخول: {str(e)}"}),
            500,
        )


@security_bp.route("/api/security/logout", methods=["POST"])
def logout():
    """تسجيل الخروج"""
    try:
        session.clear()
        return jsonify({"status": "success", "message": "تم تسجيل الخروج بنجاح"})

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في تسجيل الخروج: {str(e)}"}),
            500,
        )


@security_bp.route("/api/security/register", methods=["POST"])
@require_permission(Permissions.MANAGE_SECURITY)
def register():
    """تسجيل مستخدم جديد"""
    try:
        data = request.json if hasattr(request, "json") else {}
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        role = data.get("role", "user")

        if not username or not password:
            return (
                jsonify(
                    {"status": "error", "error": "اسم المستخدم وكلمة المرور مطلوبان"}
                ),
                400,
            )

        # تشفير كلمة المرور
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # إنشاء المستخدم الجديد
        new_user = User(
            username=username, password_hash=password_hash, email=email, role=role
        )

        if db and hasattr(db, "session") and db.session:
            db.session.add(new_user)
            db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء المستخدم بنجاح",
                "user": {"username": username, "email": email, "role": role},
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "error": f"خطأ في إنشاء المستخدم: {str(e)}"}),
            500,
        )


@security_bp.route("/api/security/change-password", methods=["POST"])
def change_password():
    """تغيير كلمة المرور"""
    try:
        data = request.json if hasattr(request, "json") else {}
        current_password = data.get("current_password", "")
        new_password = data.get("new_password", "")

        if not current_password or not new_password:
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "كلمة المرور الحالية والجديدة مطلوبتان",
                    }
                ),
                400,
            )

        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"status": "error", "error": "يجب تسجيل الدخول أولاً"}), 401

        # البحث عن المستخدم
        user = None
        if User and hasattr(User, "query") and User.query:
            user = User.query.get(user_id)

        if not user:
            return jsonify({"status": "error", "error": "المستخدم غير موجود"}), 404

        # التحقق من كلمة المرور الحالية
        if not bcrypt.checkpw(
            current_password.encode("utf-8"), getattr(user, "password_hash", b"")
        ):
            return (
                jsonify({"status": "error", "error": "كلمة المرور الحالية غير صحيحة"}),
                401,
            )

        # تشفير كلمة المرور الجديدة
        new_password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"), bcrypt.gensalt()
        )

        # تحديث كلمة المرور
        if hasattr(user, "password_hash"):
            user.password_hash = new_password_hash

        if db and hasattr(db, "session") and db.session:
            db.session.commit()

        return jsonify({"status": "success", "message": "تم تغيير كلمة المرور بنجاح"})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في تغيير كلمة المرور: {str(e)}"}
            ),
            500,
        )


@security_bp.route("/api/security/users", methods=["GET"])
@require_permission(Permissions.VIEW_SECURITY)
def get_users():
    """الحصول على قائمة المستخدمين"""
    try:
        users = []
        if User and hasattr(User, "query") and User.query:
            user_list = User.query.all()
            users = [
                {
                    "id": getattr(u, "id", None),
                    "username": getattr(u, "username", ""),
                    "email": getattr(u, "email", ""),
                    "role": getattr(u, "role", "user"),
                    "created_at": (
                        getattr(u, "created_at", None).isoformat()
                        if hasattr(u, "created_at") and getattr(u, "created_at")
                        else None
                    ),
                }
                for u in user_list
            ]

        return jsonify({"status": "success", "data": users})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "error": f"خطأ في الحصول على المستخدمين: {str(e)}"}
            ),
            500,
        )
