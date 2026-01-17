#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/inventory.py
مسارات إدارة المخزون المحسنة
Enhanced Inventory Management Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.inventory import Inventory
from src.models.product import Product
from src.models.warehouse import Warehouse
from src.decorators.auth_decorators import token_required
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/api/inventory", methods=["GET"])
@token_required
def get_inventory():
    """الحصول على قائمة المخزون"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 50, type=int)
        warehouse_id = request.args.get("warehouse_id", type=int)
        product_id = request.args.get("product_id", type=int)

        query = Inventory.query

        # تطبيق المرشحات
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        if product_id:
            query = query.filter_by(product_id=product_id)

        # الترقيم
        inventory_items = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "success": True,
                "data": [item.to_dict() for item in inventory_items.items],
                "pagination": {
                    "page": page,
                    "pages": inventory_items.pages,
                    "per_page": per_page,
                    "total": inventory_items.total,
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المخزون: {e}")
        return jsonify({"success": False, "error": "فشل في الحصول على المخزون"}), 500


@inventory_bp.route("/api/inventory/summary", methods=["GET"])
@token_required
def get_inventory_summary():
    """الحصول على ملخص المخزون"""
    try:
        # إحصائيات عامة
        total_products = db.session.query(Inventory.product_id).distinct().count()
        total_quantity = db.session.query(db.func.sum(Inventory.quantity)).scalar() or 0
        low_stock_count = Inventory.query.filter(
            Inventory.quantity <= Inventory.min_stock_level
        ).count()

        # المنتجات الأكثر كمية
        top_products = (
            db.session.query(
                Inventory.product_id,
                Product.name,
                db.func.sum(Inventory.quantity).label("total_quantity"),
            )
            .join(Product)
            .group_by(Inventory.product_id, Product.name)
            .order_by(db.func.sum(Inventory.quantity).desc())
            .limit(10)
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": {
                    "total_products": total_products,
                    "total_quantity": total_quantity,
                    "low_stock_count": low_stock_count,
                    "top_products": [
                        {
                            "product_id": item[0],
                            "product_name": item[1],
                            "total_quantity": item[2],
                        }
                        for item in top_products
                    ],
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على ملخص المخزون: {e}")
        return (
            jsonify({"success": False, "error": "فشل في الحصول على ملخص المخزون"}),
            500,
        )


@inventory_bp.route("/api/inventory/low-stock", methods=["GET"])
@token_required
def get_low_stock_items():
    """الحصول على المنتجات منخفضة المخزون"""
    try:
        low_stock_items = (
            db.session.query(Inventory, Product, Warehouse)
            .join(Product)
            .join(Warehouse)
            .filter(Inventory.quantity <= Inventory.min_stock_level)
            .all()
        )

        result = []
        for inventory, product, warehouse in low_stock_items:
            result.append(
                {
                    "inventory_id": inventory.id,
                    "product_id": product.id,
                    "product_name": product.name,
                    "warehouse_id": warehouse.id,
                    "warehouse_name": warehouse.name,
                    "current_quantity": inventory.quantity,
                    "min_stock_level": inventory.min_stock_level,
                    "shortage": inventory.min_stock_level - inventory.quantity,
                }
            )

        return jsonify({"success": True, "data": result, "total": len(result)})

    except Exception as e:
        logger.error(f"خطأ في الحصول على المنتجات منخفضة المخزون: {e}")
        return (
            jsonify(
                {"success": False, "error": "فشل في الحصول على المنتجات منخفضة المخزون"}
            ),
            500,
        )


@inventory_bp.route("/api/inventory/adjust", methods=["POST"])
@token_required
def adjust_inventory():
    """تعديل كمية المخزون"""
    try:
        data = request.get_json()

        required_fields = [
            "product_id",
            "warehouse_id",
            "adjustment_quantity",
            "reason",
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"success": False, "error": "جميع الحقول مطلوبة"}), 400

        # البحث عن عنصر المخزون أو إنشاؤه
        inventory_item = Inventory.query.filter_by(
            product_id=data["product_id"], warehouse_id=data["warehouse_id"]
        ).first()

        if not inventory_item:
            inventory_item = Inventory(
                product_id=data["product_id"],
                warehouse_id=data["warehouse_id"],
                quantity=0,
            )
            db.session.add(inventory_item)

        # تطبيق التعديل
        old_quantity = inventory_item.quantity
        inventory_item.quantity += data["adjustment_quantity"]
        inventory_item.last_updated = datetime.utcnow()

        # تسجيل حركة المخزون (يمكن إضافة جدول منفصل لهذا)

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "data": {
                    "inventory_id": inventory_item.id,
                    "old_quantity": old_quantity,
                    "new_quantity": inventory_item.quantity,
                    "adjustment": data["adjustment_quantity"],
                },
                "message": "تم تعديل المخزون بنجاح",
            }
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تعديل المخزون: {e}")
        return jsonify({"success": False, "error": "فشل في تعديل المخزون"}), 500


@inventory_bp.route("/api/inventory/transfer", methods=["POST"])
@token_required
def transfer_inventory():
    """نقل المخزون بين المستودعات"""
    try:
        data = request.get_json()

        required_fields = [
            "product_id",
            "from_warehouse_id",
            "to_warehouse_id",
            "quantity",
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"success": False, "error": "جميع الحقول مطلوبة"}), 400

        if data["from_warehouse_id"] == data["to_warehouse_id"]:
            return (
                jsonify({"success": False, "error": "لا يمكن النقل إلى نفس المستودع"}),
                400,
            )

        # التحقق من توفر الكمية في المستودع المصدر
        source_inventory = Inventory.query.filter_by(
            product_id=data["product_id"], warehouse_id=data["from_warehouse_id"]
        ).first()

        if not source_inventory or source_inventory.quantity < data["quantity"]:
            return (
                jsonify(
                    {"success": False, "error": "الكمية غير متوفرة في المستودع المصدر"}
                ),
                400,
            )

        # خصم من المستودع المصدر
        source_inventory.quantity -= data["quantity"]
        source_inventory.last_updated = datetime.utcnow()

        # إضافة إلى المستودع الهدف
        target_inventory = Inventory.query.filter_by(
            product_id=data["product_id"], warehouse_id=data["to_warehouse_id"]
        ).first()

        if not target_inventory:
            target_inventory = Inventory(
                product_id=data["product_id"],
                warehouse_id=data["to_warehouse_id"],
                quantity=0,
            )
            db.session.add(target_inventory)

        target_inventory.quantity += data["quantity"]
        target_inventory.last_updated = datetime.utcnow()

        db.session.commit()

        return jsonify({"success": True, "message": "تم نقل المخزون بنجاح"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في نقل المخزون: {e}")
        return jsonify({"success": False, "error": "فشل في نقل المخزون"}), 500
