# FILE: backend/src/routes/users.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/users.py
مسارات إدارة المستخدمين
Users Management Routes
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.database import db
from src.models.user_unified import User
from src.decorators.auth_decorators import token_required, admin_required
from werkzeug.security import generate_password_hash
import logging

logger = logging.getLogger(__name__)

users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users", methods=["GET"])
@token_required
@admin_required
def get_users():
    """الحصول على قائمة المستخدمين"""
    try:
        users = User.query.all()
        return success_response(
            data={"total": len(users)}, message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدمين: {e}")
        return error_response(
            message="فشل في الحصول على المستخدمين",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_bp.route("/api/users", methods=["POST"])
@token_required
@admin_required
def create_user():
    """إنشاء مستخدم جديد"""
    try:
        data = request.get_json()

        if not data or not data.get("username") or not data.get("password"):
            return error_response(
                message="اسم المستخدم وكلمة المرور مطلوبان",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من عدم وجود المستخدم
        if User.query.filter_by(username=data["username"]).first():
            return error_response(
                message="اسم المستخدم موجود بالفعل",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        user = User()  # type: ignore[call-arg]
        user.username = data["username"]  # type: ignore[assignment]
        user.email = data.get("email", "")  # type: ignore[assignment]
        user.full_name = data.get("full_name", "")  # type: ignore[assignment]
        user.password_hash = generate_password_hash(data["password"])  # type: ignore[assignment]
        user.role = data.get("role", "user")  # type: ignore[assignment]
        user.is_active = data.get("is_active", True)  # type: ignore[assignment]

        db.session.add(user)
        db.session.commit()

        return (
            success_response(
                data=user.to_dict(), message="تم إنشاء المستخدم بنجاح", status_code=200
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء المستخدم: {e}")
        return error_response(
            message="فشل في إنشاء المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_bp.route("/api/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """الحصول على مستخدم محدد"""
    try:
        user = User.query.get_or_404(user_id)
        return success_response(data=user.to_dict(), message="Success", status_code=200)
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستخدم: {e}")
        return error_response(
            message="فشل في الحصول على المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_bp.route("/api/users/<int:user_id>", methods=["PUT"])
@token_required
@admin_required
def update_user(user_id):
    """تحديث مستخدم"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if data.get("username"):
            user.username = data["username"]
        if data.get("email"):
            user.email = data["email"]
        if data.get("full_name"):
            user.full_name = data["full_name"]
        if data.get("password"):
            user.password_hash = generate_password_hash(data["password"])
        if "role" in data:
            user.role = data["role"]
        if "is_active" in data:
            user.is_active = data["is_active"]

        db.session.commit()

        return success_response(
            data=user.to_dict(), message="تم تحديث المستخدم بنجاح", status_code=200
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث المستخدم: {e}")
        return error_response(
            message="فشل في تحديث المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@users_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(user_id):
    """حذف مستخدم"""
    try:
        user = User.query.get_or_404(user_id)

        # منع حذف المستخدم الحالي
        current_user = getattr(request, "current_user", None)
        if current_user and current_user.id == user_id:
            return error_response(
                message="لا يمكن حذف المستخدم الحالي",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        db.session.delete(user)
        db.session.commit()

        return success_response(message="تم حذف المستخدم بنجاح", status_code=200)

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف المستخدم: {e}")
        return error_response(
            message="فشل في حذف المستخدم",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
