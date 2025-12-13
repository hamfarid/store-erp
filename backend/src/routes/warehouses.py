# FILE: backend/src/routes/warehouses.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/warehouses.py
مسارات إدارة المستودعات
Warehouses Management Routes
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.database import db
from src.decorators.auth_decorators import token_required
import logging

# استيراد النماذج الموحدة
try:
    from src.models.warehouse_unified import Warehouse

    UNIFIED_MODELS = True
except ImportError:
    Warehouse = None
    UNIFIED_MODELS = False

logger = logging.getLogger(__name__)

warehouses_bp = Blueprint("warehouses", __name__)


@warehouses_bp.route("/api/warehouses", methods=["GET"])
@token_required
def get_warehouses():
    """الحصول على قائمة المستودعات"""
    try:
        warehouses = Warehouse.query.all()
        return success_response(
            data={"total": len(warehouses)}, message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستودعات: {e}")
        return error_response(
            message="فشل في الحصول على المستودعات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@warehouses_bp.route("/api/warehouses", methods=["POST"])
@token_required
def create_warehouse():
    """إنشاء مستودع جديد"""
    try:
        data = request.get_json()

        if not data or not data.get("name"):
            return error_response(
                message="اسم المستودع مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        warehouse = Warehouse()  # type: ignore[call-arg]
        warehouse.name = data["name"]  # type: ignore[assignment]
        warehouse.location = data.get("location", "")  # type: ignore[assignment]
        warehouse.description = data.get("description", "")  # type: ignore[assignment]
        warehouse.is_active = data.get("is_active", True)  # type: ignore[assignment]

        db.session.add(warehouse)
        db.session.commit()

        return (
            success_response(
                data=warehouse.to_dict(),
                message="تم إنشاء المستودع بنجاح",
                status_code=200,
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء المستودع: {e}")
        return error_response(
            message="فشل في إنشاء المستودع",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@warehouses_bp.route("/api/warehouses/<int:warehouse_id>", methods=["GET"])
@token_required
def get_warehouse(warehouse_id):
    """الحصول على مستودع محدد"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        return success_response(
            data=warehouse.to_dict(), message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ في الحصول على المستودع: {e}")
        return error_response(
            message="فشل في الحصول على المستودع",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


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

        return success_response(
            data=warehouse.to_dict(), message="تم تحديث المستودع بنجاح", status_code=200
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث المستودع: {e}")
        return error_response(
            message="فشل في تحديث المستودع",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@warehouses_bp.route("/api/warehouses/<int:warehouse_id>", methods=["DELETE"])
@token_required
def delete_warehouse(warehouse_id):
    """حذف مستودع"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)

        # التحقق من وجود مخزون في هذا المستودع
        if warehouse.inventory_items:
            return error_response(
                message="لا يمكن حذف مستودع يحتوي على مخزون",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        db.session.delete(warehouse)
        db.session.commit()

        return success_response(message="تم حذف المستودع بنجاح", status_code=200)

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف المستودع: {e}")
        return error_response(
            message="فشل في حذف المستودع",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
