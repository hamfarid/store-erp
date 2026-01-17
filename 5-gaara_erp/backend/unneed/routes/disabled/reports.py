#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/reports.py
مسارات التقارير المحسنة
Enhanced Reports Routes
"""

from flask import Blueprint, request, jsonify
from src.database import db
from src.models.product import Product
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.inventory import Inventory
from src.models.warehouse import Warehouse
from src.decorators.auth_decorators import token_required
import logging
from datetime import datetime, timedelta
from sqlalchemy import func, desc

logger = logging.getLogger(__name__)

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/api/reports/dashboard", methods=["GET"])
@token_required
def dashboard_report():
    """تقرير لوحة المعلومات"""
    try:
        # إحصائيات عامة
        total_products = Product.query.count()
        total_customers = Customer.query.count()
        total_suppliers = Supplier.query.count()
        total_warehouses = Warehouse.query.count()

        # إحصائيات المخزون
        total_inventory_value = (
            db.session.query(func.sum(Inventory.quantity * Product.price))
            .join(Product)
            .scalar()
            or 0
        )

        low_stock_count = Inventory.query.filter(
            Inventory.quantity <= Inventory.min_stock_level
        ).count()

        return jsonify(
            {
                "success": True,
                "data": {
                    "overview": {
                        "total_products": total_products,
                        "total_customers": total_customers,
                        "total_suppliers": total_suppliers,
                        "total_warehouses": total_warehouses,
                    },
                    "inventory": {
                        "total_value": float(total_inventory_value),
                        "low_stock_items": low_stock_count,
                    },
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في تقرير لوحة المعلومات: {e}")
        return (
            jsonify({"success": False, "error": "فشل في إنشاء تقرير لوحة المعلومات"}),
            500,
        )


@reports_bp.route("/api/reports/inventory", methods=["GET"])
@token_required
def inventory_report():
    """تقرير المخزون"""
    try:
        warehouse_id = request.args.get("warehouse_id", type=int)
        category_id = request.args.get("category_id", type=int)

        query = (
            db.session.query(
                Product.id,
                Product.name,
                Product.sku,
                Warehouse.name.label("warehouse_name"),
                Inventory.quantity,
                Inventory.min_stock_level,
                Inventory.max_stock_level,
                Product.price,
                (Inventory.quantity * Product.price).label("total_value"),
            )
            .join(Inventory)
            .join(Warehouse)
        )

        # تطبيق المرشحات
        if warehouse_id:
            query = query.filter(Inventory.warehouse_id == warehouse_id)
        if category_id:
            query = query.filter(Product.category_id == category_id)

        results = query.all()

        # تحويل النتائج
        inventory_data = []
        total_value = 0

        for row in results:
            item_data = {
                "product_id": row.id,
                "product_name": row.name,
                "sku": row.sku,
                "warehouse_name": row.warehouse_name,
                "quantity": row.quantity,
                "min_stock_level": row.min_stock_level,
                "max_stock_level": row.max_stock_level,
                "unit_price": float(row.price) if row.price else 0,
                "total_value": float(row.total_value) if row.total_value else 0,
                "stock_status": (
                    "منخفض" if row.quantity <= row.min_stock_level else "طبيعي"
                ),
            }
            inventory_data.append(item_data)
            total_value += item_data["total_value"]

        return jsonify(
            {
                "success": True,
                "data": {
                    "items": inventory_data,
                    "summary": {
                        "total_items": len(inventory_data),
                        "total_value": total_value,
                    },
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في تقرير المخزون: {e}")
        return jsonify({"success": False, "error": "فشل في إنشاء تقرير المخزون"}), 500


@reports_bp.route("/api/reports/sales", methods=["GET"])
@token_required
def sales_report():
    """تقرير المبيعات"""
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # تحويل التواريخ
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_date = datetime.now() - timedelta(days=30)

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = datetime.now()

        # هنا يجب إضافة استعلامات المبيعات الفعلية
        # حالياً سنعيد بيانات وهمية

        return jsonify(
            {
                "success": True,
                "data": {
                    "period": {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                    },
                    "summary": {
                        "total_sales": 0,
                        "total_orders": 0,
                        "average_order_value": 0,
                    },
                    "message": "تقرير المبيعات قيد التطوير",
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في تقرير المبيعات: {e}")
        return jsonify({"success": False, "error": "فشل في إنشاء تقرير المبيعات"}), 500


@reports_bp.route("/api/reports/products", methods=["GET"])
@token_required
def products_report():
    """تقرير المنتجات"""
    try:
        # المنتجات الأكثر مبيعاً (بناءً على المخزون المتاح)
        top_products = (
            db.session.query(
                Product.id,
                Product.name,
                Product.sku,
                func.sum(Inventory.quantity).label("total_stock"),
            )
            .join(Inventory)
            .group_by(Product.id, Product.name, Product.sku)
            .order_by(desc("total_stock"))
            .limit(10)
            .all()
        )

        # المنتجات بدون مخزون
        out_of_stock = (
            db.session.query(Product)
            .outerjoin(Inventory)
            .filter((Inventory.quantity == 0) | (Inventory.quantity.is_(None)))
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": {
                    "top_products": [
                        {
                            "product_id": item.id,
                            "name": item.name,
                            "sku": item.sku,
                            "total_stock": item.total_stock,
                        }
                        for item in top_products
                    ],
                    "out_of_stock": [
                        {"product_id": item.id, "name": item.name, "sku": item.sku}
                        for item in out_of_stock
                    ],
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في تقرير المنتجات: {e}")
        return jsonify({"success": False, "error": "فشل في إنشاء تقرير المنتجات"}), 500


@reports_bp.route("/api/reports/export", methods=["POST"])
@token_required
def export_report():
    """تصدير التقارير"""
    try:
        data = request.get_json()
        report_type = data.get("report_type")
        format_type = data.get("format", "json")  # json, csv, excel

        if not report_type:
            return jsonify({"success": False, "error": "نوع التقرير مطلوب"}), 400

        # هنا يمكن إضافة منطق التصدير الفعلي

        return jsonify(
            {
                "success": True,
                "data": {
                    "report_type": report_type,
                    "format": format_type,
                    "message": "ميزة التصدير قيد التطوير",
                },
            }
        )

    except Exception as e:
        logger.error(f"خطأ في تصدير التقرير: {e}")
        return jsonify({"success": False, "error": "فشل في تصدير التقرير"}), 500
