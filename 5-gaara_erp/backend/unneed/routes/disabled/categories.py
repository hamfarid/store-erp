#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/categories.py
مسارات إدارة الفئات
Categories Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.category import Category
from src.decorators.auth_decorators import token_required
import logging

logger = logging.getLogger(__name__)

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/api/categories", methods=["GET"])
@token_required
def get_categories():
    """الحصول على قائمة الفئات"""
    try:
        categories = Category.query.all()
        return jsonify(
            {
                "success": True,
                "data": [category.to_dict() for category in categories],
                "total": len(categories),
            }
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئات: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على الفئات"}), 500


@categories_bp.route("/api/categories", methods=["POST"])
@token_required
def create_category():
    """إنشاء فئة جديدة"""
    try:
        data = request.get_json()

        if not data or not data.get("name"):
            return jsonify({"success": False, "error": "اسم الفئة مطلوب"}), 400

        category = Category(
            name=data["name"],
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
        )

        db.session.add(category)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "data": category.to_dict(),
                    "message": "تم إنشاء الفئة بنجاح",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء الفئة: {e}")
        return jsonify({"success": False, "error": "فشل في إنشاء الفئة"}), 500


@categories_bp.route("/api/categories/<int:category_id>", methods=["GET"])
@token_required
def get_category(category_id):
    """الحصول على فئة محددة"""
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify({"success": True, "data": category.to_dict()})
    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئة: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على الفئة"}), 500


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

        return jsonify(
            {
                "success": True,
                "data": category.to_dict(),
                "message": "تم تحديث الفئة بنجاح",
            }
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث الفئة: {e}")
        return jsonify({"success": False, "error": "فشل في تحديث الفئة"}), 500


@categories_bp.route("/api/categories/<int:category_id>", methods=["DELETE"])
@token_required
def delete_category(category_id):
    """حذف فئة"""
    try:
        category = Category.query.get_or_404(category_id)

        # التحقق من وجود منتجات في هذه الفئة
        if category.products:
            return (
                jsonify(
                    {"success": False, "error": "لا يمكن حذف فئة تحتوي على منتجات"}
                ),
                400,
            )

        db.session.delete(category)
        db.session.commit()

        return jsonify({"success": True, "message": "تم حذف الفئة بنجاح"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف الفئة: {e}")
        return jsonify({"success": False, "error": "فشل في حذف الفئة"}), 500
