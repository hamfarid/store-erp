"""
مزخرفات الصلاحيات والأذونات
# type: ignore  # تجاهل تحذيرات النوع
"""

from functools import wraps
from typing import Any, Dict

try:
    from flask import session, jsonify, request, abort  # type: ignore
except ImportError:
    # Fallback when Flask is not available
    def jsonify(data: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        return {"data": data}

    class MockRequest:  # type: ignore
        args: Dict[str, Any] = {}
        json: Dict[str, Any] = {}
        form: Dict[str, Any] = {}
        is_json: bool = False

    request = MockRequest()  # type: ignore
    session: Dict[str, Any] = {}  # type: ignore

    def abort(code: int) -> None:  # type: ignore
        raise Exception(f"HTTP {code}")


try:
    from auth import AuthManager  # type: ignore
except ImportError:
    # Fallback when auth module is not available
    class AuthManager:  # type: ignore
        @staticmethod
        def get_current_user():
            return None

        @staticmethod
        def user_has_permission(user, permission):
            return True

        @staticmethod
        def user_can_access_warehouse(user, warehouse_id):
            return True


def _is_admin_user(u: Any) -> bool:
    """Return True if the user is an admin (supports dict or object)."""
    try:
        if isinstance(u, dict):
            return bool(u.get("is_admin") or u.get("role") == "admin")
        return bool(
            getattr(u, "is_admin", False) or getattr(u, "role", None) == "admin"
        )
    except Exception:
        return False


def require_login(f):
    """مزخرف يتطلب تسجيل الدخول"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_id = session.get("user_id") if session else None
            if not user_id:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "يجب تسجيل الدخول للوصول إلى هذه الصفحة",
                        }
                    ),
                    401,
                )

            return f(*args, **kwargs)
        except Exception as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"خطأ في التحقق من تسجيل الدخول: {str(e)}",
                    }
                ),
                500,
            )

    return decorated_function


def require_permission(permission):
    """مزخرف يتطلب صلاحية معينة"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                user_id = session.get("user_id") if session else None
                if not user_id:
                    return (
                        jsonify({"success": False, "error": "يجب تسجيل الدخول أولاً"}),
                        401,
                    )

                current_user = AuthManager.get_current_user()
                if not current_user:
                    return (
                        jsonify({"success": False, "error": "المستخدم غير موجود"}),
                        404,
                    )

                # التحقق من صلاحية المدير
                if _is_admin_user(current_user):
                    return f(*args, **kwargs)

                # التحقق من الصلاحية المحددة
                if not AuthManager.user_has_permission(current_user, permission):
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": "ليس لديك صلاحية للوصول إلى هذه الصفحة",
                            }
                        ),
                        403,
                    )

                return f(*args, **kwargs)
            except Exception as e:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": f"خطأ في التحقق من الصلاحيات: {str(e)}",
                        }
                    ),
                    500,
                )

        return decorated_function

    return decorator


def require_admin(f):
    """مزخرف يتطلب صلاحيات المدير"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_id = session.get("user_id") if session else None
            if not user_id:
                return (
                    jsonify({"success": False, "error": "يجب تسجيل الدخول أولاً"}),
                    401,
                )

            current_user = AuthManager.get_current_user()
            if not current_user:
                return jsonify({"success": False, "error": "المستخدم غير موجود"}), 404

            if not _is_admin_user(current_user):
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": "يجب أن تكون مديراً للوصول إلى هذه الصفحة",
                        }
                    ),
                    403,
                )

            return f(*args, **kwargs)
        except Exception as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"خطأ في التحقق من صلاحيات المدير: {str(e)}",
                    }
                ),
                500,
            )

    return decorated_function


def require_warehouse_access(warehouse_id_param="warehouse_id"):
    """مزخرف يتطلب الوصول إلى مستودع معين"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                user_id = session.get("user_id") if session else None
                if not user_id:
                    return (
                        jsonify({"success": False, "error": "يجب تسجيل الدخول أولاً"}),
                        401,
                    )

                # الحصول على معرف المستودع
                warehouse_id = None
                if hasattr(request, "args") and request.args:
                    warehouse_id = request.args.get(warehouse_id_param)
                elif hasattr(request, "json") and request.json:
                    warehouse_id = request.json.get(warehouse_id_param)
                elif hasattr(request, "form") and request.form:
                    warehouse_id = request.form.get(warehouse_id_param)

                if not warehouse_id:
                    return (
                        jsonify({"success": False, "error": "معرف المستودع مطلوب"}),
                        400,
                    )

                current_user = AuthManager.get_current_user()
                if not current_user:
                    return (
                        jsonify({"success": False, "error": "المستخدم غير موجود"}),
                        404,
                    )

                # التحقق من صلاحية المدير
                if _is_admin_user(current_user):
                    return f(*args, **kwargs)

                # التحقق من الوصول إلى المستودع
                if not AuthManager.user_can_access_warehouse(
                    current_user, warehouse_id
                ):
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": "ليس لديك صلاحية للوصول إلى هذا المستودع",
                            }
                        ),
                        403,
                    )

                return f(*args, **kwargs)
            except Exception as e:
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": f"خطأ في التحقق من الوصول للمستودع: {str(e)}",
                        }
                    ),
                    500,
                )

        return decorated_function

    return decorator
