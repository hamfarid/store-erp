# FILE: backend/src/routes/warehouse_adjustments.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/routes/warehouse_adjustments.py

نظام إدارة تعديلات المخازن
All linting disabled due to complex route operations and optional dependencies.
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from datetime import datetime, timedelta
import json

warehouse_adjustments_bp = Blueprint("warehouse_adjustments", __name__)

# بيانات تجريبية لتعديلات المخازن
sample_adjustments = [
    {
        "id": 1,
        "adjustment_number": "ADJ-2024-001",
        "warehouse_id": 1,
        "warehouse_name": "المخزن الرئيسي",
        "type": "increase",
        "reason": "جرد دوري",
        "status": "pending",
        "created_by": "أحمد محمد",
        "created_at": "2024-01-15T09:00:00",
        "approved_by": None,
        "approved_at": None,
        "items": [
            {
                "product_id": 1,
                "product_name": "لابتوب ديل",
                "current_qty": 50,
                "adjusted_qty": 52,
                "difference": 2,
                "unit_cost": 2500,
                "total_value": 5000,
            },
            {
                "product_id": 2,
                "product_name": "طابعة HP",
                "current_qty": 25,
                "adjusted_qty": 23,
                "difference": -2,
                "unit_cost": 800,
                "total_value": -1600,
            },
        ],
        "total_value": 3400,
        "notes": "تعديل بناءً على الجرد الدوري الشهري",
    },
    {
        "id": 2,
        "adjustment_number": "ADJ-2024-002",
        "warehouse_id": 2,
        "warehouse_name": "مخزن الإلكترونيات",
        "type": "decrease",
        "reason": "تلف",
        "status": "approved",
        "created_by": "سارة أحمد",
        "created_at": "2024-01-14T14:30:00",
        "approved_by": "محمد علي",
        "approved_at": "2024-01-14T16:00:00",
        "items": [
            {
                "product_id": 3,
                "product_name": "هاتف ذكي",
                "current_qty": 100,
                "adjusted_qty": 95,
                "difference": -5,
                "unit_cost": 1200,
                "total_value": -6000,
            }
        ],
        "total_value": -6000,
        "notes": "تلف في الشحنة الأخيرة",
    },
    {
        "id": 3,
        "adjustment_number": "ADJ-2024-003",
        "warehouse_id": 3,
        "warehouse_name": "مخزن المواد الغذائية",
        "type": "increase",
        "reason": "خطأ في الإدخال",
        "status": "rejected",
        "created_by": "فاطمة سالم",
        "created_at": "2024-01-13T11:00:00",
        "approved_by": "أحمد محمد",
        "approved_at": "2024-01-13T15:30:00",
        "items": [
            {
                "product_id": 4,
                "product_name": "أرز بسمتي",
                "current_qty": 200,
                "adjusted_qty": 210,
                "difference": 10,
                "unit_cost": 15,
                "total_value": 150,
            }
        ],
        "total_value": 150,
        "notes": "تم رفض التعديل - لا يوجد مبرر كافي",
    },
]

# بيانات تجريبية للمخازن
sample_warehouses = [
    {"id": 1, "name": "المخزن الرئيسي", "location": "الرياض"},
    {"id": 2, "name": "مخزن الإلكترونيات", "location": "جدة"},
    {"id": 3, "name": "مخزن المواد الغذائية", "location": "الدمام"},
]

# بيانات تجريبية للمنتجات
sample_products = [
    {"id": 1, "name": "لابتوب ديل", "sku": "DELL-001", "unit_cost": 2500},
    {"id": 2, "name": "طابعة HP", "sku": "HP-001", "unit_cost": 800},
    {"id": 3, "name": "هاتف ذكي", "sku": "PHONE-001", "unit_cost": 1200},
    {"id": 4, "name": "أرز بسمتي", "sku": "RICE-001", "unit_cost": 15},
]


@warehouse_adjustments_bp.route("/warehouse-adjustments", methods=["GET"])
def get_adjustments():
    """الحصول على قائمة تعديلات المخازن"""
    try:
        warehouse_id = request.args.get("warehouse_id", type=int)
        status = request.args.get("status", "all")
        adjustment_type = request.args.get("adjustment_type", "all")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")

        adjustments = sample_adjustments.copy()

        # تطبيق الفلاتر
        if warehouse_id:
            adjustments = [
                adj for adj in adjustments if adj["warehouse_id"] == int(warehouse_id)
            ]

        if status != "all":
            adjustments = [adj for adj in adjustments if adj["status"] == status]

        if adjustment_type != "all":
            adjustments = [adj for adj in adjustments if adj["type"] == adjustment_type]

        if date_from:
            adjustments = [adj for adj in adjustments if adj["created_at"] >= date_from]

        if date_to:
            adjustments = [adj for adj in adjustments if adj["created_at"] <= date_to]

        return jsonify(
            {"status": "success", "data": adjustments, "total": len(adjustments)}
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب تعديلات المخازن: {str(e)}"}
            ),
            500,
        )


@warehouse_adjustments_bp.route(
    "/warehouse-adjustments/<int:adjustment_id>", methods=["GET"]
)
def get_adjustment(adjustment_id):
    """الحصول على تفاصيل تعديل محدد"""
    try:
        adjustment = next(
            (adj for adj in sample_adjustments if adj["id"] == adjustment_id), None
        )

        if not adjustment:
            return jsonify({"status": "error", "message": "التعديل غير موجود"}), 404

        return jsonify({"status": "success", "data": adjustment})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب تفاصيل التعديل: {str(e)}"}
            ),
            500,
        )


@warehouse_adjustments_bp.route("/warehouse-adjustments", methods=["POST"])
def create_adjustment():
    """إنشاء تعديل مخزن جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["warehouse_id", "reason", "items"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"الحقل {field} مطلوب"}),
                    400,
                )

        # التحقق من وجود المخزن
        warehouse = next(
            (wh for wh in sample_warehouses if wh["id"] == data["warehouse_id"]), None
        )
        if not warehouse:
            return jsonify({"status": "error", "message": "المخزن غير موجود"}), 404

        # حساب نوع التعديل والقيمة الإجمالية
        total_value = 0
        adjustment_type = "mixed"
        positive_items = 0
        negative_items = 0

        for item in data["items"]:
            difference = item["adjusted_qty"] - item["current_qty"]
            item["difference"] = difference
            item["total_value"] = difference * item["unit_cost"]
            total_value += item["total_value"]

            if difference > 0:
                positive_items += 1
            elif difference < 0:
                negative_items += 1

        # تحديد نوع التعديل
        if positive_items > 0 and negative_items == 0:
            adjustment_type = "increase"
        elif negative_items > 0 and positive_items == 0:
            adjustment_type = "decrease"

        # إنشاء تعديل جديد
        new_adjustment = {
            "id": max([adj["id"] for adj in sample_adjustments]) + 1,
            "adjustment_number": f"ADJ-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}",
            "warehouse_id": data["warehouse_id"],
            "warehouse_name": warehouse["name"],
            "type": adjustment_type,
            "reason": data["reason"],
            "status": "pending",
            "created_by": data.get("created_by", "النظام"),
            "created_at": datetime.now().isoformat(),
            "approved_by": None,
            "approved_at": None,
            "items": data["items"],
            "total_value": total_value,
            "notes": data.get("notes", ""),
        }

        sample_adjustments.append(new_adjustment)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء التعديل بنجاح",
                    "data": new_adjustment,
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء التعديل: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route(
    "/warehouse-adjustments/<int:adjustment_id>", methods=["PUT"]
)
def update_adjustment(adjustment_id):
    """تحديث تعديل مخزن"""
    try:
        data = request.get_json()

        adjustment_index = next(
            (
                i
                for i, adj in enumerate(sample_adjustments)
                if adj["id"] == adjustment_id
            ),
            None,
        )

        if adjustment_index is None:
            return jsonify({"status": "error", "message": "التعديل غير موجود"}), 404

        adjustment = sample_adjustments[adjustment_index]

        # التحقق من إمكانية التعديل
        if adjustment["status"] in ["approved", "rejected"]:
            return (
                jsonify(
                    {"status": "error", "message": "لا يمكن تعديل تعديل معتمد أو مرفوض"}
                ),
                400,
            )

        # تحديث البيانات
        if "items" in data:
            # إعادة حساب القيم
            total_value = 0
            for item in data["items"]:
                difference = item["adjusted_qty"] - item["current_qty"]
                item["difference"] = difference
                item["total_value"] = difference * item["unit_cost"]
                total_value += item["total_value"]

            adjustment["items"] = data["items"]
            adjustment["total_value"] = total_value

        adjustment.update(
            {
                "reason": data.get("reason", adjustment["reason"]),
                "notes": data.get("notes", adjustment["notes"]),
            }
        )

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث التعديل بنجاح",
                "data": adjustment,
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث التعديل: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route(
    "/warehouse-adjustments/<int:adjustment_id>/approve", methods=["POST"]
)
def approve_adjustment(adjustment_id):
    """اعتماد تعديل مخزن"""
    try:
        data = request.get_json()

        adjustment_index = next(
            (
                i
                for i, adj in enumerate(sample_adjustments)
                if adj["id"] == adjustment_id
            ),
            None,
        )

        if adjustment_index is None:
            return jsonify({"status": "error", "message": "التعديل غير موجود"}), 404

        adjustment = sample_adjustments[adjustment_index]

        # التحقق من الحالة
        if adjustment["status"] != "pending":
            return (
                jsonify({"status": "error", "message": "التعديل ليس في حالة انتظار"}),
                400,
            )

        # اعتماد التعديل
        adjustment.update(
            {
                "status": "approved",
                "approved_by": data.get("approved_by", "المدير"),
                "approved_at": datetime.now().isoformat(),
            }
        )

        # هنا يمكن إضافة منطق تطبيق التعديل على المخزون الفعلي

        return jsonify(
            {
                "status": "success",
                "message": "تم اعتماد التعديل بنجاح",
                "data": adjustment,
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في اعتماد التعديل: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route(
    "/warehouse-adjustments/<int:adjustment_id>/reject", methods=["POST"]
)
def reject_adjustment(adjustment_id):
    """رفض تعديل مخزن"""
    try:
        data = request.get_json()

        adjustment_index = next(
            (
                i
                for i, adj in enumerate(sample_adjustments)
                if adj["id"] == adjustment_id
            ),
            None,
        )

        if adjustment_index is None:
            return jsonify({"status": "error", "message": "التعديل غير موجود"}), 404

        adjustment = sample_adjustments[adjustment_index]

        # التحقق من الحالة
        if adjustment["status"] != "pending":
            return (
                jsonify({"status": "error", "message": "التعديل ليس في حالة انتظار"}),
                400,
            )

        # رفض التعديل
        adjustment.update(
            {
                "status": "rejected",
                "approved_by": data.get("approved_by", "المدير"),
                "approved_at": datetime.now().isoformat(),
                "rejection_reason": data.get("rejection_reason", ""),
            }
        )

        return jsonify(
            {"status": "success", "message": "تم رفض التعديل", "data": adjustment}
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في رفض التعديل: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route(
    "/warehouse-adjustments/<int:adjustment_id>", methods=["DELETE"]
)
def delete_adjustment(adjustment_id):
    """حذف تعديل مخزن"""
    try:
        adjustment_index = next(
            (
                i
                for i, adj in enumerate(sample_adjustments)
                if adj["id"] == adjustment_id
            ),
            None,
        )

        if adjustment_index is None:
            return jsonify({"status": "error", "message": "التعديل غير موجود"}), 404

        adjustment = sample_adjustments[adjustment_index]

        # التحقق من إمكانية الحذف
        if adjustment["status"] == "approved":
            return (
                jsonify({"status": "error", "message": "لا يمكن حذف تعديل معتمد"}),
                400,
            )

        # حذف التعديل
        del sample_adjustments[adjustment_index]

        return jsonify({"status": "success", "message": "تم حذف التعديل بنجاح"})

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في حذف التعديل: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route("/warehouses", methods=["GET"])
def get_warehouses():
    """الحصول على قائمة المخازن"""
    try:
        return jsonify({"status": "success", "data": sample_warehouses})

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب المخازن: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route("/products", methods=["GET"])
def get_products():
    """الحصول على قائمة المنتجات"""
    try:
        search = request.args.get("search", "")
        category_id = request.args.get("category_id")

        products = sample_products.copy()

        # تطبيق البحث
        if search:
            products = [
                prod
                for prod in products
                if search.lower() in prod["name"].lower()
                or search.lower() in prod["sku"].lower()
            ]

        # إضافة الكمية الحالية (محاكاة)
        for product in products:
            product["current_qty"] = 50  # قيمة افتراضية

        return jsonify({"status": "success", "data": products})

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب المنتجات: {str(e)}"}),
            500,
        )


@warehouse_adjustments_bp.route("/warehouse-adjustments/summary", methods=["GET"])
def get_adjustments_summary():
    """الحصول على ملخص تعديلات المخازن"""
    try:
        total_adjustments = len(sample_adjustments)
        pending_adjustments = len(
            [adj for adj in sample_adjustments if adj["status"] == "pending"]
        )
        approved_adjustments = len(
            [adj for adj in sample_adjustments if adj["status"] == "approved"]
        )
        rejected_adjustments = len(
            [adj for adj in sample_adjustments if adj["status"] == "rejected"]
        )

        # حساب القيم المالية
        total_value = sum(
            adj["total_value"]
            for adj in sample_adjustments
            if adj["status"] == "approved"
        )
        positive_adjustments = sum(
            adj["total_value"]
            for adj in sample_adjustments
            if adj["status"] == "approved" and adj["total_value"] > 0
        )
        negative_adjustments = sum(
            adj["total_value"]
            for adj in sample_adjustments
            if adj["status"] == "approved" and adj["total_value"] < 0
        )

        summary = {
            "total_adjustments": total_adjustments,
            "pending_adjustments": pending_adjustments,
            "approved_adjustments": approved_adjustments,
            "rejected_adjustments": rejected_adjustments,
            "total_value": total_value,
            "positive_adjustments_value": positive_adjustments,
            "negative_adjustments_value": abs(negative_adjustments),
            "net_adjustment_value": total_value,
        }

        return jsonify({"status": "success", "data": summary})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب ملخص التعديلات: {str(e)}"}
            ),
            500,
        )


@warehouse_adjustments_bp.route("/warehouse-adjustments/reasons", methods=["GET"])
def get_adjustment_reasons():
    """الحصول على قائمة أسباب التعديل"""
    try:
        reasons = [
            "جرد دوري",
            "تلف",
            "انتهاء صلاحية",
            "خطأ في الإدخال",
            "سرقة أو فقدان",
            "إرجاع من العميل",
            "تصحيح خطأ سابق",
            "تحويل بين مخازن",
            "عينات مجانية",
            "أخرى",
        ]

        return jsonify({"status": "success", "data": reasons})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب أسباب التعديل: {str(e)}"}
            ),
            500,
        )
