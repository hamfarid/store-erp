# FILE: backend/src/routes/users_unified.py
# PURPOSE: Routes with P0.2.4 error envelope
# OWNER: Backend
# RELATED: middleware/error_envelope_middleware.py
# LAST-AUDITED: 2025-10-25

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/users_unified.py
مسارات إدارة المستخدمين الموحدة
Unified Users Management Routes

يوفر:
- قائمة المستخدمين
- إنشاء مستخدم
- تحديث مستخدم
- حذف مستخدم
- إدارة الأدوار
- إدارة الصلاحيات
"""

from flask import Blueprint, request, jsonify, g

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.database import db
from datetime import datetime
import logging

# P0.19: Import validation schemas
try:
    from src.utils.validation import (
        validate_json,
        UserCreateSchema,
        UserUpdateSchema,
        RoleCreateSchema,
    )
except ImportError:
    UserCreateSchema = None
    UserUpdateSchema = None
    RoleCreateSchema = None

    def validate_json(schema):
        def decorator(f):
            return f

        return decorator


# استيراد النماذج الموحدة
try:
    from src.models.user import User

    try:
        from src.models.user import create_default_roles
    except ImportError:

        def create_default_roles():  # type: ignore[misc]
            """Fallback function if not available"""
            pass

    try:
        from src.models.supporting_models import AuditLog, ActionType
    except ImportError:
        # Create dummy classes if not available
        class ActionType:  # type: ignore[no-redef]
            CREATE = "create"
            UPDATE = "update"
            DELETE = "delete"

        class AuditLog:  # type: ignore[no-redef]
            pass

    from src.models.user import Role

    UNIFIED_MODELS = True
except ImportError:
    from src.models.user import User
    from src.models.user import Role

    UNIFIED_MODELS = False

    # Create dummy classes if not available
    class ActionType:  # type: ignore[no-redef]
        CREATE = "create"
        UPDATE = "update"
        DELETE = "delete"

    class AuditLog:  # type: ignore[no-redef]
        pass

    def create_default_roles():  # type: ignore[misc]
        """Fallback function if not available"""
        pass


# استيراد decorators من ملف المصادقة الموحد
try:
    from src.routes.auth_unified import token_required, admin_required, log_activity
except ImportError:
    # Fallback decorators
    from functools import wraps

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated

    def log_activity(user_id, action, details=None):
        pass


logger = logging.getLogger(__name__)

users_unified_bp = Blueprint("users_unified", __name__)


# ============================================================================
# مسارات المستخدمين
# ============================================================================


@users_unified_bp.route("/api/users/me", methods=["GET"])
@token_required
def get_current_user():
    """
    الحصول على بيانات المستخدم الحالي من JWT token
    Get current user profile from JWT token
    """
    try:
        # Get user ID from JWT token (stored by token_required decorator in request object)
        current_user_id = getattr(request, "current_user_id", None)

        if not current_user_id:
            return error_response(
                message="مستخدم غير مصرح به",
                code=ErrorCodes.AUTH_INVALID_TOKEN,
                status_code=401,
            )

        # Get user from database
        user = User.query.get(current_user_id)

        if not user:
            return error_response(
                message="المستخدم غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        return success_response(
            data=user.to_dict(),
            message="تم الحصول على بيانات المستخدم بنجاح",
            status_code=200,
        )

    except Exception as e:
        import traceback

        error_detail = traceback.format_exc()
        logger.error(f"خطأ في الحصول على المستخدم الحالي: {e}")
        logger.error(f"Traceback: {error_detail}")
        return error_response(
            message="حدث خطأ أثناء الحصول على بيانات المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/users", methods=["GET"])
@token_required
@admin_required
def get_users():
    """
    الحصول على قائمة المستخدمين

    Query Parameters:
        page: رقم الصفحة (افتراضي: 1)
        per_page: عدد العناصر في الصفحة (افتراضي: 10)
        search: البحث في الاسم أو البريد
        role: تصفية حسب الدور
        is_active: تصفية حسب الحالة
    """
    try:
        # معاملات الاستعلام
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        search = request.args.get("search", "")
        role_filter = request.args.get("role", "")
        is_active = request.args.get("is_active", "")

        # بناء الاستعلام
        from sqlalchemy import select

        query = User.query

        # البحث
        if search:
            query = query.filter(
                db.or_(
                    User.username.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%"),
                )
            )

        # تصفية حسب الدور
        if role_filter:
            if UNIFIED_MODELS:
                query = query.join(Role).filter(Role.name == role_filter)
            else:
                query = query.filter(User.role == role_filter)

        # تصفية حسب الحالة
        if is_active:
            is_active_bool = is_active.lower() == "true"
            query = query.filter(User.is_active.is_(is_active_bool))

        # الترتيب
        query = query.order_by(User.created_at.desc())

        # التصفح
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "users": [user.to_dict() for user in pagination.items],
                        "pagination": {
                            "page": page,
                            "per_page": per_page,
                            "total": pagination.total,
                            "pages": pagination.pages,
                            "has_next": pagination.has_next,
                            "has_prev": pagination.has_prev,
                        },
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدمين: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على المستخدمين",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """
    الحصول على مستخدم محدد
    """
    try:
        user = User.query.get(user_id)

        if not user:
            return error_response(
                message="المستخدم غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        return success_response(
            data=user.to_dict(), message="تم الحصول على المستخدم بنجاح", status_code=200
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدم: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/users", methods=["POST"])
@token_required
@admin_required
@validate_json(UserCreateSchema)
def create_user():
    """
    P0.19: إنشاء مستخدم جديد مع التحقق من صحة البيانات

    Body:
        username: اسم المستخدم (مطلوب)
        password: كلمة المرور (مطلوب)
        email: البريد الإلكتروني
        full_name: الاسم الكامل
        phone: رقم الهاتف
        role_id: معرف الدور (للنماذج الموحدة)
        role: اسم الدور (للنماذج القديمة)
        is_active: الحالة (افتراضي: true)
    """
    try:
        # Use validated data from decorator if available
        data = getattr(g, "validated_data", None) or request.get_json()

        # التحقق من البيانات المطلوبة
        if not data or not data.get("username") or not data.get("password"):
            return error_response(
                message="اسم المستخدم وكلمة المرور مطلوبان",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # التحقق من عدم وجود المستخدم
        if User.query.filter_by(username=data["username"]).first():
            return error_response(
                message="اسم المستخدم موجود بالفعل",
                code=ErrorCodes.DB_DUPLICATE_ENTRY,
                status_code=400,
            )

        # التحقق من البريد الإلكتروني
        email = data.get("email")
        if email and User.query.filter_by(email=email).first():
            return error_response(
                message="البريد الإلكتروني مستخدم بالفعل",
                code=ErrorCodes.DB_DUPLICATE_ENTRY,
                status_code=400,
            )

        # إنشاء المستخدم
        user = User()  # type: ignore[call-arg]
        user.username = data["username"]  # type: ignore[assignment]
        # type: ignore[assignment]
        user.email = data.get("email", "")
        # type: ignore[assignment]
        user.full_name = data.get("full_name", "")
        # type: ignore[assignment]
        user.phone = data.get("phone", "")
        # type: ignore[assignment]
        user.is_active = data.get("is_active", True)

        # تعيين كلمة المرور
        user.set_password(data["password"])

        # تعيين الدور
        if UNIFIED_MODELS:
            role_id = data.get("role_id")
            if role_id:
                # type: ignore[possibly-unbound,misc]
                role = Role.query.get(role_id)
                if not role:
                    return error_response(
                        message="الدور غير موجود",
                        code=ErrorCodes.VAL_INVALID_REFERENCE,
                        status_code=404,
                    )
                user.role_id = role_id
            else:
                # الدور الافتراضي
                # type: ignore[possibly-unbound,misc]
                default_role = Role.query.filter_by(name="user").first()
                if default_role:
                    user.role_id = default_role.id
        else:
            user.role = data.get("role", "user")

        db.session.add(user)
        db.session.commit()

        # تسجيل النشاط
        action_type = ActionType.CREATE if UNIFIED_MODELS else "create"
        log_activity(
            request.current_user_id,  # type: ignore[attr-defined]
            action_type,  # type: ignore[possibly-unbound]
            {"entity": "user", "entity_id": user.id, "username": user.username},
        )

        return (
            success_response(
                data=user.to_dict(), message="تم إنشاء المستخدم بنجاح", status_code=200
            ),
            201,
        )

    except Exception as e:
        logger.error(f"خطأ في إنشاء المستخدم: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء إنشاء المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/users/<int:user_id>", methods=["PUT"])
@token_required
@admin_required
def update_user(user_id):
    """
    تحديث مستخدم

    Body:
        email: البريد الإلكتروني
        full_name: الاسم الكامل
        phone: رقم الهاتف
        role_id: معرف الدور
        is_active: الحالة
    """
    try:
        user = User.query.get(user_id)

        if not user:
            return error_response(
                message="المستخدم غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        data = request.get_json()

        # تحديث البيانات
        if "email" in data:
            # التحقق من عدم تكرار البريد
            existing = User.query.filter(
                User.email == data["email"], User.id != user_id
            ).first()
            if existing:
                return error_response(
                    message="البريد الإلكتروني مستخدم بالفعل",
                    code=ErrorCodes.DB_DUPLICATE_ENTRY,
                    status_code=400,
                )
            user.email = data["email"]

        if "full_name" in data:
            user.full_name = data["full_name"]

        if "phone" in data:
            user.phone = data["phone"]

        if "is_active" in data:
            user.is_active = data["is_active"]

        if "role_id" in data and UNIFIED_MODELS:
            # type: ignore[possibly-unbound,misc]
            role = Role.query.get(data["role_id"])
            if not role:
                return error_response(
                    message="الدور غير موجود",
                    code=ErrorCodes.VAL_INVALID_REFERENCE,
                    status_code=404,
                )
            user.role_id = data["role_id"]

        if "role" in data and not UNIFIED_MODELS:
            user.role = data["role"]

        user.updated_at = datetime.now(datetime.UTC)
        db.session.commit()

        # تسجيل النشاط
        action_type = ActionType.UPDATE if UNIFIED_MODELS else "update"
        log_activity(
            request.current_user_id,  # type: ignore[attr-defined]
            action_type,  # type: ignore[possibly-unbound]
            {"entity": "user", "entity_id": user.id, "username": user.username},
        )

        return (
            success_response(
                data=user.to_dict(), message="تم تحديث المستخدم بنجاح", status_code=200
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في تحديث المستخدم: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء تحديث المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(user_id):
    """
    حذف مستخدم
    """
    try:
        user = User.query.get(user_id)

        if not user:
            return error_response(
                message="المستخدم غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        # منع حذف المستخدم الحالي
        if user.id == request.current_user_id:  # type: ignore[attr-defined]
            return error_response(
                message="لا يمكنك حذف حسابك الخاص",
                code=ErrorCodes.VAL_INVALID_FORMAT,
                status_code=400,
            )

        username = user.username

        # حذف المستخدم
        db.session.delete(user)
        db.session.commit()

        # تسجيل النشاط
        action_type = ActionType.DELETE if UNIFIED_MODELS else "delete"
        log_activity(
            request.current_user_id,  # type: ignore[attr-defined]
            action_type,  # type: ignore[possibly-unbound]
            {"entity": "user", "entity_id": user_id, "username": username},
        )

        return success_response(message="تم حذف المستخدم بنجاح", status_code=200), 200

    except Exception as e:
        logger.error(f"خطأ في حذف المستخدم: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء حذف المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


# ============================================================================
# مسارات الأدوار (للنماذج الموحدة فقط)
# ============================================================================


@users_unified_bp.route("/api/roles", methods=["GET"])
@token_required
def get_roles():
    """
    الحصول على قائمة الأدوار
    """
    if not UNIFIED_MODELS:
        return error_response(
            message="هذه الميزة متاحة فقط مع النماذج الموحدة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=501,
        )

    try:
        roles = Role.query.all()  # type: ignore[possibly-unbound,misc]

        return (
            success_response(
                data=[role.to_dict() for role in roles],
                message="Success",
                status_code=200,
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على الأدوار: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على الأدوار",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/roles/<int:role_id>", methods=["GET"])
@token_required
def get_role(role_id):
    """
    الحصول على دور محدد
    """
    if not UNIFIED_MODELS:
        return error_response(
            message="هذه الميزة متاحة فقط مع النماذج الموحدة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=501,
        )

    try:
        role = Role.query.get(role_id)  # type: ignore[possibly-unbound,misc]

        if not role:
            return error_response(
                message="الدور غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        return (
            success_response(data=role.to_dict(), message="Success", status_code=200),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على الدور: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على الدور",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/roles", methods=["POST"])
@token_required
@admin_required
@validate_json(RoleCreateSchema)
def create_role():
    """
    P0.19: إنشاء دور جديد مع التحقق من صحة البيانات

    Body:
        name: اسم الدور (مطلوب)
        display_name: الاسم المعروض
        description: الوصف
        permissions: قائمة الصلاحيات
    """
    if not UNIFIED_MODELS:
        return error_response(
            message="هذه الميزة متاحة فقط مع النماذج الموحدة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=501,
        )

    try:
        # Use validated data from decorator if available
        data = getattr(g, "validated_data", None) or request.get_json()

        if not data or not data.get("name"):
            return error_response(
                message="اسم الدور مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من عدم وجود الدور
        # type: ignore[possibly-unbound,misc]
        if Role.query.filter_by(name=data["name"]).first():
            return error_response(
                message="الدور موجود بالفعل",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # إنشاء الدور
        role = Role()  # type: ignore[call-arg]
        role.name = data["name"]  # type: ignore[assignment]
        # type: ignore[assignment]
        role.display_name = data.get("display_name", data["name"])
        # type: ignore[assignment]
        role.description = data.get("description", "")

        # تعيين الصلاحيات
        if "permissions" in data:
            role.set_permissions(data["permissions"])

        db.session.add(role)
        db.session.commit()

        # تسجيل النشاط
        # type: ignore[attr-defined,possibly-unbound]
        log_activity(
            request.current_user_id,
            ActionType.CREATE,
            {"entity": "role", "entity_id": role.id, "name": role.name},
        )

        return (
            success_response(
                data=role.to_dict(), message="تم إنشاء الدور بنجاح", status_code=200
            ),
            201,
        )

    except Exception as e:
        logger.error(f"خطأ في إنشاء الدور: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء إنشاء الدور",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/roles/<int:role_id>", methods=["PUT"])
@token_required
@admin_required
def update_role(role_id):
    """
    تحديث دور

    Body:
        display_name: الاسم المعروض
        description: الوصف
        permissions: قائمة الصلاحيات
    """
    if not UNIFIED_MODELS:
        return error_response(
            message="هذه الميزة متاحة فقط مع النماذج الموحدة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=501,
        )

    try:
        role = Role.query.get(role_id)  # type: ignore[possibly-unbound,misc]

        if not role:
            return error_response(
                message="الدور غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        data = request.get_json()

        # تحديث البيانات
        if "display_name" in data:
            role.display_name = data["display_name"]

        if "description" in data:
            role.description = data["description"]

        if "permissions" in data:
            role.set_permissions(data["permissions"])

        role.updated_at = datetime.now(datetime.UTC)
        db.session.commit()

        # تسجيل النشاط
        # type: ignore[attr-defined,possibly-unbound]
        log_activity(
            request.current_user_id,
            ActionType.UPDATE,
            {"entity": "role", "entity_id": role.id, "name": role.name},
        )

        return (
            success_response(
                data=role.to_dict(), message="تم تحديث الدور بنجاح", status_code=200
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في تحديث الدور: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء تحديث الدور",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_unified_bp.route("/api/roles/<int:role_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_role(role_id):
    """
    حذف دور
    """
    if not UNIFIED_MODELS:
        return error_response(
            message="هذه الميزة متاحة فقط مع النماذج الموحدة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=501,
        )

    try:
        role = Role.query.get(role_id)  # type: ignore[possibly-unbound,misc]

        if not role:
            return error_response(
                message="الدور غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # منع حذف الأدوار الافتراضية
        if role.name in ["admin", "manager", "user"]:
            return error_response(
                message="لا يمكن حذف الأدوار الافتراضية",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من عدم وجود مستخدمين بهذا الدور
        if role.users:
            user_count = len(role.users)
            error_msg = f"لا يمكن حذف الدور لأنه مستخدم " f"من قبل {user_count} مستخدم"
            return jsonify({"success": False, "error": error_msg}), 400

        name = role.name

        # حذف الدور
        db.session.delete(role)
        db.session.commit()

        # تسجيل النشاط
        # type: ignore[attr-defined,possibly-unbound]
        log_activity(
            request.current_user_id,
            ActionType.DELETE,
            {"entity": "role", "entity_id": role_id, "name": name},
        )

        return success_response(message="تم حذف الدور بنجاح", status_code=200), 200

    except Exception as e:
        logger.error(f"خطأ في حذف الدور: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء حذف الدور",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
