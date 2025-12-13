# FILE: backend/src/routes/integration_apis.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
APIs التكامل بين المديولات
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging
from datetime import datetime

integration_bp = Blueprint("integration", __name__)

# ==================== APIs تكامل المخزون والمحاسبة ====================


@integration_bp.route(
    "/api/integration/inventory-accounting/journal-entry", methods=["POST"]
)
def create_inventory_journal_entry():
    """إنشاء قيد محاسبي لحركة مخزون"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = [
            "movement_id",
            "movement_type",
            "product_id",
            "quantity",
            "unit_cost",
        ]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "error": f"الحقل {field} مطلوب"}),
                    400,
                )

        # محاكاة إنشاء القيد المحاسبي
        total_value = data["quantity"] * data["unit_cost"]

        journal_entry = {
            "id": 123,
            "date": datetime.now().date().isoformat(),
            "reference": f"INV-{data['movement_id']}",
            "description": f"حركة مخزون - {data['movement_type']}",
            "total_debit": total_value,
            "total_credit": total_value,
            "lines": [
                {
                    "account_code": "1001",
                    "account_name": "المخزون",
                    "debit": total_value if data["movement_type"] == "receipt" else 0,
                    "credit": total_value if data["movement_type"] == "delivery" else 0,
                },
                {
                    "account_code": (
                        "2001" if data["movement_type"] == "receipt" else "5001"
                    ),
                    "account_name": (
                        "الموردين"
                        if data["movement_type"] == "receipt"
                        else "تكلفة البضاعة المباعة"
                    ),
                    "debit": 0 if data["movement_type"] == "receipt" else total_value,
                    "credit": total_value if data["movement_type"] == "receipt" else 0,
                },
            ],
            "created_at": datetime.now().isoformat(),
        }

        return jsonify(
            {
                "status": "success",
                "journal_entry": journal_entry,
                "message": "تم إنشاء القيد المحاسبي بنجاح",
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@integration_bp.route(
    "/api/integration/inventory-accounting/reconciliation", methods=["GET"]
)
def get_inventory_accounting_reconciliation():
    """مطابقة المخزون مع المحاسبة"""
    try:
        # محاكاة بيانات المطابقة
        reconciliation_data = {
            "inventory_value": 125000.00,
            "accounting_balance": 124850.00,
            "difference": 150.00,
            "variance_percentage": 0.12,
            "is_balanced": False,
            "discrepancies": [
                {
                    "product_id": 1,
                    "product_name": "بذور طماطم",
                    "inventory_value": 5000.00,
                    "accounting_value": 4950.00,
                    "difference": 50.00,
                },
                {
                    "product_id": 2,
                    "product_name": "سماد NPK",
                    "inventory_value": 3000.00,
                    "accounting_value": 2900.00,
                    "difference": 100.00,
                },
            ],
            "last_reconciliation_date": "2024-11-30",
            "generated_at": datetime.now().isoformat(),
        }

        return jsonify({"status": "success", "reconciliation": reconciliation_data})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ==================== APIs تكامل المبيعات والمخزون ====================


@integration_bp.route(
    "/api/integration/sales-inventory/process-order", methods=["POST"]
)
def process_sale_order():
    """معالجة أمر بيع وتأثيره على المخزون"""
    try:
        data = request.get_json()

        # التحقق من البيانات
        if "order_id" not in data or "lines" not in data:
            return jsonify({"status": "error", "error": "بيانات الطلب غير مكتملة"}), 400

        # محاكاة معالجة الطلب
        movements_created = []

        for line in data["lines"]:
            movement = {
                "id": len(movements_created) + 1,
                "movement_number": f"MOV-SO-{data['order_id']}-{len(movements_created) + 1}",
                "movement_type": "delivery",
                "product_id": line["product_id"],
                "product_name": line.get("product_name", "منتج"),
                "quantity_planned": line["quantity"],
                "quantity_done": 0,
                "state": "confirmed",
                "reference_type": "sale_order",
                "reference_id": data["order_id"],
                "warehouse_id": line.get("warehouse_id", 1),
                "created_at": datetime.now().isoformat(),
            }
            movements_created.append(movement)

        return jsonify(
            {
                "status": "success",
                "movements_created": movements_created,
                "message": f"تم إنشاء {len(movements_created)} حركة مخزون لأمر البيع",
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@integration_bp.route(
    "/api/integration/sales-inventory/check-availability", methods=["POST"]
)
def check_product_availability():
    """التحقق من توفر المنتجات لأمر البيع"""
    try:
        data = request.get_json()

        if "products" not in data:
            return jsonify({"status": "error", "error": "قائمة المنتجات مطلوبة"}), 400

        # محاكاة التحقق من التوفر
        availability_results = []

        for product in data["products"]:
            # محاكاة بيانات المخزون
            current_stock = 100.0  # كمية افتراضية
            requested_quantity = product["quantity"]

            result = {
                "product_id": product["product_id"],
                "product_name": product.get("product_name", "منتج"),
                "requested_quantity": requested_quantity,
                "available_quantity": current_stock,
                "is_available": current_stock >= requested_quantity,
                "shortage": max(0, requested_quantity - current_stock),
                "warehouse_id": product.get("warehouse_id", 1),
            }

            # إضافة معلومات اللوط إذا كان المنتج يتطلب تتبع
            if product.get("requires_batch_tracking"):
                result["available_batches"] = [
                    {
                        "batch_id": 1,
                        "batch_number": "LOT-2024-001",
                        "available_quantity": 50.0,
                        "expiry_date": "2025-12-31",
                    },
                    {
                        "batch_id": 2,
                        "batch_number": "LOT-2024-002",
                        "available_quantity": 50.0,
                        "expiry_date": "2025-06-30",
                    },
                ]

            availability_results.append(result)

        # تحديد الحالة العامة
        all_available = all(result["is_available"] for result in availability_results)

        return jsonify(
            {
                "status": "success",
                "all_available": all_available,
                "products": availability_results,
                "checked_at": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ==================== APIs تكامل المشتريات والمخزون ====================


@integration_bp.route(
    "/api/integration/purchases-inventory/process-receipt", methods=["POST"]
)
def process_purchase_receipt():
    """معالجة استلام مشتريات"""
    try:
        data = request.get_json()

        # التحقق من البيانات
        required_fields = ["purchase_order_id", "supplier_id", "lines"]
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "error": f"الحقل {field} مطلوب"}), 400

        # محاكاة معالجة الاستلام
        movements_created = []
        batches_created = []

        for line in data["lines"]:
            # إنشاء حركة مخزون
            movement = {
                "id": len(movements_created) + 1,
                "movement_number": f"MOV-PO-{data['purchase_order_id']}-{len(movements_created) + 1}",
                "movement_type": "receipt",
                "product_id": line["product_id"],
                "product_name": line.get("product_name", "منتج"),
                "quantity_planned": line["quantity_ordered"],
                "quantity_done": line.get(
                    "quantity_received", line["quantity_ordered"]
                ),
                "state": "done",
                "reference_type": "purchase_order",
                "reference_id": data["purchase_order_id"],
                "warehouse_id": line.get("warehouse_id", 1),
                "unit_cost": line.get("unit_cost", 0),
                "created_at": datetime.now().isoformat(),
            }
            movements_created.append(movement)

            # إنشاء لوط إذا كان مطلوباً
            if line.get("batch_data"):
                lot = {
                    "id": len(batches_created) + 1,
                    "batch_number": line["batch_data"]["batch_number"],
                    "product_id": line["product_id"],
                    "initial_quantity": line.get(
                        "quantity_received", line["quantity_ordered"]
                    ),
                    "current_quantity": line.get(
                        "quantity_received", line["quantity_ordered"]
                    ),
                    "production_date": line["batch_data"].get("production_date"),
                    "expiry_date": line["batch_data"].get("expiry_date"),
                    "supplier_batch_number": line["batch_data"].get(
                        "supplier_batch_number"
                    ),
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                }
                batches_created.append(lot)

        return jsonify(
            {
                "status": "success",
                "movements_created": movements_created,
                "batches_created": batches_created,
                "message": f"تم استلام {len(movements_created)} منتج بنجاح",
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ==================== APIs إدارة الصلاحيات والشركات ====================


@integration_bp.route("/api/integration/user-warehouses/<int:user_id>", methods=["GET"])
def get_user_accessible_warehouses(user_id):
    """الحصول على المخازن المتاحة للمستخدم"""
    try:
        # محاكاة المخازن المتاحة للمستخدم
        accessible_warehouses = [
            {
                "id": 1,
                "name": "المخزن الرئيسي",
                "code": "WH-001",
                "company_id": 1,
                "company_name": "الشركة الرئيسية",
                "branch_id": 1,
                "branch_name": "الفرع الرئيسي",
                "permissions": ["read", "write", "manage"],
            },
            {
                "id": 2,
                "name": "مخزن الفرع الثاني",
                "code": "WH-002",
                "company_id": 1,
                "company_name": "الشركة الرئيسية",
                "branch_id": 2,
                "branch_name": "الفرع الثاني",
                "permissions": ["read"],
            },
        ]

        return jsonify(
            {
                "status": "success",
                "warehouses": accessible_warehouses,
                "count": len(accessible_warehouses),
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ==================== APIs التقارير المتكاملة ====================


@integration_bp.route(
    "/api/integration/reports/comprehensive-inventory", methods=["GET"]
)
def get_comprehensive_inventory_report():
    """تقرير مخزون شامل متكامل"""
    try:
        # محاكاة تقرير شامل
        comprehensive_report = {
            "summary": {
                "total_products": 150,
                "total_quantity": 5000.0,
                "total_value": 125000.0,
                "low_stock_products": 5,
                "expiring_batches": 3,
                "inactive_products": 10,
            },
            "inventory_by_category": [
                {
                    "category": "بذور",
                    "products_count": 50,
                    "total_quantity": 2000.0,
                    "total_value": 60000.0,
                    "percentage": 48.0,
                },
                {
                    "category": "أسمدة",
                    "products_count": 30,
                    "total_quantity": 1500.0,
                    "total_value": 45000.0,
                    "percentage": 36.0,
                },
            ],
            "inventory_by_warehouse": [
                {
                    "warehouse_id": 1,
                    "warehouse_name": "المخزن الرئيسي",
                    "products_count": 100,
                    "total_value": 80000.0,
                    "utilization_percentage": 75.0,
                },
                {
                    "warehouse_id": 2,
                    "warehouse_name": "مخزن الفرع",
                    "products_count": 50,
                    "total_value": 45000.0,
                    "utilization_percentage": 60.0,
                },
            ],
            "accounting_integration": {
                "inventory_account_balance": 124850.0,
                "variance": 150.0,
                "variance_percentage": 0.12,
                "last_reconciliation": "2024-11-30",
            },
            "alerts": [
                {
                    "type": "low_stock",
                    "message": "5 منتجات تحتاج إعادة طلب",
                    "urgency": "high",
                },
                {
                    "type": "expiring_batches",
                    "message": "3 لوط قريبة الانتهاء",
                    "urgency": "medium",
                },
            ],
            "generated_at": datetime.now().isoformat(),
        }

        return jsonify({"status": "success", "report": comprehensive_report})

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
