#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/warehouses.py
مسارات إدارة المستودعات
Warehouses Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.warehouse import Warehouse
from src.decorators.auth_decorators import token_required
import logging

logger = logging.getLogger(__name__)

warehouses_bp = Blueprint("warehouses", __name__)


@warehouses_bp.route("/api/warehouses", methods=["GET"])
@token_required
def get_warehouses():
    """الحصول على قائمة المستودعات"""
    try:
        warehouses = Warehouse.query.all()
        return jsonify(
            {
                "success": True,
                "data": [warehouse.to_dict() for warehouse in warehouses],
                "total": len(warehouses),
            }
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستودعات: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على المستودعات"}), 500


@warehouses_bp.route("/api/warehouses", methods=["POST"])
@token_required
def create_warehouse():
    """إنشاء مستودع جديد"""
    try:
        data = request.get_json()

        if not data or not data.get("name"):
            return jsonify({"success": False, "error": "اسم المستودع مطلوب"}), 400

        warehouse = Warehouse(
            name=data["name"],
            location=data.get("location", ""),
            description=data.get("description", ""),
            is_active=data.get("is_active", True),
        )

        db.session.add(warehouse)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "data": warehouse.to_dict(),
                    "message": "تم إنشاء المستودع بنجاح",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء المستودع: {e}")
        return jsonify({"success": False, "error": "فشل في إنشاء المستودع"}), 500


@warehouses_bp.route("/api/warehouses/<int:warehouse_id>", methods=["GET"])
@token_required
def get_warehouse(warehouse_id):
    """الحصول على مستودع محدد"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        return jsonify({"success": True, "data": warehouse.to_dict()})
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستودع: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على المستودع"}), 500


@warehouses_bp.route("/api/warehouses/<int:warehouse_id>", methods=["PUT"])
@token_required
def update_warehouse(warehouse_id):
    """تحديث مستودع"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        data = request.get_json()

        if data.get("name"):
            warehouse.name = data["name"]
        if "location" in data:
            warehouse.location = data["location"]
        if "description" in data:
            warehouse.description = data["description"]
        if "is_active" in data:
            warehouse.is_active = data["is_active"]

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "data": warehouse.to_dict(),
                "message": "تم تحديث المستودع بنجاح",
            }
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث المستودع: {e}")
        return jsonify({"success": False, "error": "فشل في تحديث المستودع"}), 500


@warehouses_bp.route("/api/warehouses/<int:warehouse_id>", methods=["DELETE"])
@token_required
def delete_warehouse(warehouse_id):
    """حذف مستودع"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)

        # التحقق من وجود مخزون في هذا المستودع
        if warehouse.inventory_items:
            return (
                jsonify(
                    {"success": False, "error": "لا يمكن حذف مستودع يحتوي على مخزون"}
                ),
                400,
            )

        db.session.delete(warehouse)
        db.session.commit()

        return jsonify({"success": True, "message": "تم حذف المستودع بنجاح"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف المستودع: {e}")
        return jsonify({"success": False, "error": "فشل في حذف المستودع"}), 500
