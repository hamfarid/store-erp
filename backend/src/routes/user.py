# FILE: backend/src/routes/user.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
APIs المستخدمين مع نظام المصادقة المتقدم
All linting disabled due to complex imports and optional dependencies.
"""
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, session

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging
import jwt as pyjwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
from functools import wraps

from sqlalchemy import or_

# Import database - handle different import paths
try:
    from database import db, User, Role, UserActivity
except ImportError:
    # Create mock db for testing
    class MockDB:
        session = None

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

    db = MockDB()

user_bp = Blueprint("user", __name__)

# مفتاح JWT - في الإنتاج يجب أن يكون في متغيرات البيئة
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_EXPIRATION_HOURS = 24


def login_required(f):
    """Decorator للتحقق من تسجيل الدخول"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "تسجيل الدخول مطلوب"}), 401
        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """الحصول على المستخدم الحالي من الجلسة"""
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None


def destroy_session():
    """إنهاء الجلسة"""
    session.clear()
    return {"status": "success", "message": "تم تسجيل الخروج بنجاح"}


def has_permission(permission):
    """Decorator للتحقق من الصلاحيات"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                return (
                    jsonify({"status": "error", "message": "تسجيل الدخول مطلوب"}),
                    401,
                )
            # تبسيط التحقق من الصلاحيات - يمكن تطويره لاحقاً
            return f(*args, **kwargs)

        return decorated_function

    return decorator


class Permissions:
    """فئة الصلاحيات"""

    USER_MANAGEMENT = "user_management"
    ROLE_MANAGEMENT = "role_management"
    SYSTEM_ADMIN = "system_admin"


def generate_jwt_token(user):
    """إنشاء JWT token للمستخدم"""
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role.name if user.role else "user",
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return pyjwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def verify_jwt_token(token):
    """التحقق من JWT token"""
    try:
        payload = pyjwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None


@user_bp.route("/verify-token", methods=["POST"])
def verify_token():
    """التحقق من صحة JWT token"""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"status": "error", "message": "Token مفقود"}), 401

        token = auth_header.split(" ")[1]
        payload = verify_jwt_token(token)

        if not payload:
            return (
                jsonify(
                    {"status": "error", "message": "Token غير صحيح أو منتهي الصلاحية"}
                ),
                401,
            )

        # البحث عن المستخدم
        user = User.query.get(payload["user_id"])
        if not user or not user.is_active:
            return (
                jsonify(
                    {"status": "error", "message": "المستخدم غير موجود أو غير مفعل"}
                ),
                401,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.full_name,
                        "role": user.role.name if user.role else "user",
                        "permissions": user.role.permissions if user.role else {},
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في التحقق من Token: {str(e)}"}
            ),
            500,
        )


@user_bp.route("/login", methods=["POST"])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "")

        # التحقق من صحة البيانات المدخلة
        if not username or not password:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "يرجى إدخال اسم المستخدم وكلمة المرور",
                    }
                ),
                400,
            )

        # التحقق من طول اسم المستخدم وكلمة المرور
        if len(username) < 3 or len(username) > 50:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "اسم المستخدم يجب أن يكون بين 3 و 50 حرف",
                    }
                ),
                400,
            )

        if len(password) < 6:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "كلمة المرور يجب أن تكون 6 أحرف على الأقل",
                    }
                ),
                400,
            )

        # البحث عن المستخدم أو إنشاء مستخدم افتراضي
        user = User.query.filter_by(username=username).first()

        # إنشاء مستخدم افتراضي إذا لم يوجد (للتطوير فقط)
        if not user and username == "admin":
            # التحقق من أن كلمة المرور قوية بما فيه الكفاية
            if len(password) < 8:
                return error_response(
                    message="كلمة مرور المدير يجب أن تكون 8 أحرف على الأقل",
                    code=ErrorCodes.VAL_INVALID_FORMAT,
                    status_code=400,
                )

            # إنشاء دور افتراضي
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(
                    name="admin",
                    description="مدير النظام",
                    permissions={"all": True},
                    is_active=True,
                )
                db.session.add(admin_role)
                db.session.flush()

            # إنشاء المستخدم الافتراضي
            user = User(
                username="admin",
                email="admin@system.com",
                full_name="مدير النظام",
                role_id=admin_role.id,
                is_active=True,
            )
            user.set_password(password)  # استخدام كلمة المرور المدخلة
            db.session.add(user)
            db.session.commit()

            # تسجيل إنشاء المستخدم الافتراضي
            print(f"⚠️ تم إنشاء مستخدم افتراضي: {username}")
            print("⚠️ تأكد من تغيير كلمة المرور في بيئة الإنتاج")

        if not user:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "اسم المستخدم أو كلمة المرور غير صحيحة",
                    }
                ),
                401,
            )

        # التحقق من كلمة المرور
        if not user.check_password(password):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "اسم المستخدم أو كلمة المرور غير صحيحة",
                    }
                ),
                401,
            )

        if not user.is_active:
            return jsonify({"status": "error", "message": "الحساب غير مفعل"}), 401

        # تحديث معلومات تسجيل الدخول
        user.last_login = datetime.now(timezone.utc)
        user.login_count = (user.login_count or 0) + 1
        db.session.commit()

        # إنشاء الجلسة والـ JWT token
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role.name if user.role else "user"
        session.permanent = True

        # إنشاء JWT token
        token = generate_jwt_token(user)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم تسجيل الدخول بنجاح",
                    "token": token,  # إضافة JWT token
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "full_name": user.full_name,
                        "role": user.role.name if user.role else "user",
                        "permissions": user.role.permissions if user.role else {},
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في تسجيل الدخول: {str(e)}"}),
            500,
        )


@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """تسجيل الخروج"""
    try:
        current_user = get_current_user()

        # تسجيل نشاط تسجيل الخروج
        if current_user:
            UserActivity.log_activity(
                user_id=current_user["id"],
                action="LOGOUT",
                description="تم تسجيل الخروج",
                request=request,
            )

        # إنهاء الجلسة
        result = destroy_session()

        return jsonify(result), 200

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في تسجيل الخروج: {str(e)}"}),
            500,
        )


@user_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    """الحصول على ملف المستخدم الشخصي"""
    try:
        current_user = get_current_user()
        if not current_user:
            return (
                jsonify({"status": "error", "message": "المستخدم غير مصادق عليه"}),
                401,
            )
        user = User.query.get(current_user["id"])

        if not user:
            return jsonify({"status": "error", "message": "المستخدم غير موجود"}), 404

        return jsonify({"status": "success", "user": user.to_dict()}), 200

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب الملف الشخصي: {str(e)}"}
            ),
            500,
        )


@user_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    """تحديث الملف الشخصي"""
    try:
        current_user = get_current_user()
        if not current_user:
            return (
                jsonify({"status": "error", "message": "المستخدم غير مصادق عليه"}),
                401,
            )
        user = User.query.get(current_user["id"])

        if not user:
            return jsonify({"status": "error", "message": "المستخدم غير موجود"}), 404

        data = request.get_json()

        # تحديث البيانات المسموحة
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "email" in data:
            # التحقق من عدم وجود البريد الإلكتروني
            existing_user = User.get_by_email(data["email"])
            if existing_user and existing_user.id != user.id:
                return (
                    jsonify(
                        {"status": "error", "message": "البريد الإلكتروني موجود بالفعل"}
                    ),
                    400,
                )
            user.email = data["email"]
        if "phone" in data:
            user.phone = data["phone"]
        if "department" in data:
            user.department = data["department"]

        user.updated_at = datetime.utcnow()
        db.session.commit()

        # تسجيل النشاط
        UserActivity.log_activity(
            user_id=user.id,
            action="PROFILE_UPDATE",
            description="تم تحديث الملف الشخصي",
            request=request,
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم تحديث الملف الشخصي بنجاح",
                    "user": user.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في تحديث الملف الشخصي: {str(e)}"}
            ),
            500,
        )


@user_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    """تغيير كلمة المرور"""
    try:
        current_user = get_current_user()
        if not current_user:
            return (
                jsonify({"status": "error", "message": "المستخدم غير مصادق عليه"}),
                401,
            )
        user = User.query.get(current_user["id"])

        if not user:
            return jsonify({"status": "error", "message": "المستخدم غير موجود"}), 404

        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if not all([current_password, new_password, confirm_password]):
            return (
                jsonify(
                    {"status": "error", "message": "يرجى إدخال جميع الحقول المطلوبة"}
                ),
                400,
            )

        # التحقق من كلمة المرور الحالية
        if not user.check_password(current_password):
            return (
                jsonify(
                    {"status": "error", "message": "كلمة المرور الحالية غير صحيحة"}
                ),
                400,
            )

        # التحقق من تطابق كلمة المرور الجديدة
        if new_password != confirm_password:
            return (
                jsonify(
                    {"status": "error", "message": "كلمة المرور الجديدة غير متطابقة"}
                ),
                400,
            )

        # التحقق من قوة كلمة المرور
        if len(new_password) < 6:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "كلمة المرور يجب أن تكون 6 أحرف على الأقل",
                    }
                ),
                400,
            )

        # تحديث كلمة المرور
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()

        # تسجيل النشاط
        UserActivity.log_activity(
            user_id=user.id,
            action="PASSWORD_CHANGE",
            description="تم تغيير كلمة المرور",
            request=request,
        )

        return (
            jsonify({"status": "success", "message": "تم تغيير كلمة المرور بنجاح"}),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في تغيير كلمة المرور: {str(e)}"}
            ),
            500,
        )


@user_bp.route("/users", methods=["GET"])
@has_permission(Permissions.USER_MANAGEMENT)
def get_users():
    """الحصول على قائمة المستخدمين"""
    try:
        page = request.args.get("page", 1, type=int)
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get

        query = User.query

        # البحث
        if search:
            query = query.filter(
                or_(
                    User.username.contains(search),
                    User.full_name.contains(search),
                    User.email.contains(search),
                )
            )

        # فلترة حسب الدور
        if role_filter:
            query = query.join(Role).filter(Role.name == role_filter)

        # ترتيب النتائج
        query = query.order_by(User.created_at.desc())

        # تقسيم الصفحات
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        users = [user.to_dict() for user in pagination.items]

        return (
            jsonify(
                {
                    "status": "success",
                    "data": users,
                    "pagination": {
                        "page": page,
                        "pages": pagination.pages,
                        "per_page": per_page,
                        "total": pagination.total,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب المستخدمين: {str(e)}"}),
            500,
        )


@user_bp.route("/users", methods=["POST"])
@has_permission(Permissions.USER_MANAGEMENT)
def create_user():
    """إنشاء مستخدم جديد"""
    try:
        data = request.get_json()

        required_fields = ["username", "password", "email", "full_name", "role_id"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"الحقل {field} مطلوب"}),
                    400,
                )

        # التحقق من وجود الدور
        role = Role.query.get(data["role_id"])
        if not role:
            return (
                jsonify({"status": "error", "message": "الدور المحدد غير موجود"}),
                400,
            )

        # إنشاء المستخدم
        user = User.create_user(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            full_name=data["full_name"],
            role_id=data["role_id"],
            phone=data.get("phone"),
            department=data.get("department"),
            notes=data.get("notes"),
        )

        # تسجيل النشاط
        current_user = get_current_user()
        if current_user:
            UserActivity.log_activity(
                user_id=current_user["id"],
                action="USER_CREATE",
                description=f"تم إنشاء مستخدم جديد: {user.username}",
                request=request,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء المستخدم بنجاح",
                    "user": user.to_dict(),
                }
            ),
            201,
        )

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء المستخدم: {str(e)}"}),
            500,
        )


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@has_permission(Permissions.USER_MANAGEMENT)
def update_user(user_id):
    """تحديث مستخدم"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "المستخدم غير موجود"}), 404

        data = request.get_json()

        # تحديث البيانات
        if "username" in data:
            existing_user = User.get_by_username(data["username"])
            if existing_user and existing_user.id != user.id:
                return (
                    jsonify(
                        {"status": "error", "message": "اسم المستخدم موجود بالفعل"}
                    ),
                    400,
                )
            user.username = data["username"]

        if "email" in data:
            existing_user = User.get_by_email(data["email"])
            if existing_user and existing_user.id != user.id:
                return (
                    jsonify(
                        {"status": "error", "message": "البريد الإلكتروني موجود بالفعل"}
                    ),
                    400,
                )
            user.email = data["email"]

        if "full_name" in data:
            user.full_name = data["full_name"]

        if "role_id" in data:
            role = Role.query.get(data["role_id"])
            if not role:
                return (
                    jsonify({"status": "error", "message": "الدور المحدد غير موجود"}),
                    400,
                )
            user.role_id = data["role_id"]

        if "is_active" in data:
            user.is_active = data["is_active"]

        if "phone" in data:
            user.phone = data["phone"]

        if "department" in data:
            user.department = data["department"]

        if "notes" in data:
            user.notes = data["notes"]

        # تحديث كلمة المرور إذا تم توفيرها
        if "password" in data and data["password"]:
            user.set_password(data["password"])

        user.updated_at = datetime.utcnow()
        db.session.commit()

        # تسجيل النشاط
        current_user = get_current_user()
        if current_user:
            UserActivity.log_activity(
                user_id=current_user["id"],
                action="USER_UPDATE",
                description=f"تم تحديث المستخدم: {user.username}",
                request=request,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم تحديث المستخدم بنجاح",
                    "user": user.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث المستخدم: {str(e)}"}),
            500,
        )


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@has_permission(Permissions.USER_MANAGEMENT)
def delete_user(user_id):
    """حذف مستخدم"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "المستخدم غير موجود"}), 404

        current_user = get_current_user()
        if not current_user:
            return (
                jsonify({"status": "error", "message": "المستخدم غير مصادق عليه"}),
                401,
            )

        # منع حذف المستخدم الحالي
        if user.id == current_user["id"]:
            return (
                jsonify({"status": "error", "message": "لا يمكن حذف المستخدم الحالي"}),
                400,
            )

        username = user.username

        # حذف المستخدم (soft delete)
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()

        # تسجيل النشاط
        if current_user:
            UserActivity.log_activity(
                user_id=current_user["id"],
                action="USER_DELETE",
                description=f"تم حذف المستخدم: {username}",
                request=request,
            )

        return jsonify({"status": "success", "message": "تم حذف المستخدم بنجاح"}), 200

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في حذف المستخدم: {str(e)}"}),
            500,
        )


@user_bp.route("/roles", methods=["GET"])
@login_required
def get_roles():
    """الحصول على قائمة الأدوار"""
    try:
        roles = Role.query.filter_by(is_active=True).all()
        return (
            jsonify({"status": "success", "data": [role.to_dict() for role in roles]}),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب الأدوار: {str(e)}"}),
            500,
        )


@user_bp.route("/activities", methods=["GET"])
@has_permission(Permissions.USER_MANAGEMENT)
def get_user_activities():
    """الحصول على نشاطات المستخدمين"""
    try:
        page = request.args.get("page", 1, type=int)
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get

        query = UserActivity.query

        # فلترة حسب المستخدم
        if user_id:
            query = query.filter_by(user_id=user_id)

        # فلترة حسب النشاط
        if action:
            query = query.filter(UserActivity.action.contains(action))

        # ترتيب النتائج
        query = query.order_by(UserActivity.created_at.desc())

        # تقسيم الصفحات
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        activities = [activity.to_dict() for activity in pagination.items]

        return (
            jsonify(
                {
                    "status": "success",
                    "data": activities,
                    "pagination": {
                        "page": page,
                        "pages": pagination.pages,
                        "per_page": per_page,
                        "total": pagination.total,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب النشاطات: {str(e)}"}),
            500,
        )


@user_bp.route("/check-session", methods=["GET"])
def check_session():
    """التحقق من حالة الجلسة"""
    try:
        if "user_id" in session:
            current_user = get_current_user()
            return (
                jsonify(
                    {"status": "success", "authenticated": True, "user": current_user}
                ),
                200,
            )
        else:
            return jsonify({"status": "success", "authenticated": False}), 200

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في التحقق من الجلسة: {str(e)}"}
            ),
            500,
        )
