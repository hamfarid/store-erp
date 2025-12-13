# FILE: backend/src/routes/categories.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/categories.py
مسارات إدارة الفئات
Categories Management Routes
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.database import db
import logging

# استيراد decorators
try:
    from src.routes.auth_unified import token_required
except ImportError:
    from functools import wraps

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated


# استيراد النماذج
try:
    from src.models.inventory import Category

    UNIFIED_MODELS = True
except ImportError:
    Category = None
    UNIFIED_MODELS = False

logger = logging.getLogger(__name__)

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/api/categories", methods=["GET"])
@token_required
def get_categories():
    """الحصول على قائمة الفئات"""
    try:
        categories = Category.query.all()
        return success_response(
            data={
                "categories": [cat.to_dict() for cat in categories],
                "total": len(categories),
            },
            message="Success",
            status_code=200,
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئات: {e}")
        return error_response(
            message="فشل في الحصول على الفئات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@categories_bp.route("/api/categories", methods=["POST"])
@token_required
def create_category():
    """إنشاء فئة جديدة"""
    try:
        data = request.get_json()

        if not data or not data.get("name"):
            return error_response(
                message="اسم الفئة مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        category = Category()  # type: ignore[call-arg]
        category.name = data["name"]  # type: ignore[assignment]
        category.description = data.get("description", "")  # type: ignore[assignment]
        category.parent_id = data.get("parent_id")  # type: ignore[assignment]

        db.session.add(category)
        db.session.commit()

        return (
            success_response(
                data=category.to_dict(), message="تم إنشاء الفئة بنجاح", status_code=200
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء الفئة: {e}")
        return error_response(
            message="فشل في إنشاء الفئة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@categories_bp.route("/api/categories/<int:category_id>", methods=["GET"])
@token_required
def get_category(category_id):
    """الحصول على فئة محددة"""
    try:
        category = Category.query.get_or_404(category_id)
        return success_response(
            data=category.to_dict(), message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئة: {e}")
        return error_response(
            message="فشل في الحصول على الفئة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@categories_bp.route("/api/categories/<int:category_id>", methods=["PUT"])
@token_required
def update_category(category_id):
    """تحديث فئة"""
    try:
        category = Category.query.get_or_404(category_id)
        data = request.get_json()

        if data.get("name"):
            category.name = data["name"]
        if "description" in data:
            category.description = data["description"]
        if "parent_id" in data:
            category.parent_id = data["parent_id"]

        db.session.commit()

        return success_response(
            data=category.to_dict(), message="تم تحديث الفئة بنجاح", status_code=200
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث الفئة: {e}")
        return error_response(
            message="فشل في تحديث الفئة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@categories_bp.route("/api/categories/<int:category_id>", methods=["DELETE"])
@token_required
def delete_category(category_id):
    """حذف فئة"""
    try:
        category = Category.query.get_or_404(category_id)

        # التحقق من وجود منتجات في هذه الفئة
        if category.products:
            return error_response(
                message="لا يمكن حذف فئة تحتوي على منتجات",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        db.session.delete(category)
        db.session.commit()

        return success_response(message="تم حذف الفئة بنجاح", status_code=200)

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف الفئة: {e}")
        return error_response(
            message="فشل في حذف الفئة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
