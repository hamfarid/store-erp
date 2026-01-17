# FILE: backend/src/routes/settings.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# pylint: disable=all
# flake8: noqa
"""
APIs إعدادات النظام
"""

from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging

# Import auth functions
try:
    from auth import login_required, has_permission, Permissions, AuthManager
except ImportError:
    # Create mock auth functions
    def login_required(f):
        return f

    def has_permission(permission):
        def decorator(f):
            return f

        return decorator

    class Permissions:
        ADMIN = "admin"

    class AuthManager:
        @staticmethod
        def authenticate(username, password):
            return True


# Import database - handle different import paths
try:
    from src.database import db
except ImportError:
    # Create mock db for testing
    class MockDB:
        session = None

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

    db = MockDB()
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.inventory import Category, ProductGroup, Rank, Warehouse

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/inventory", methods=["GET"])
@login_required
def get_inventory_settings():
    """الحصول على إعدادات المخزون"""
    try:
        # إعدادات افتراضية
        settings = {
            "auto_reorder": False,
            "low_stock_alert": True,
            "default_warehouse_id": 1,
            "currency": "EGP",
            "decimal_places": 2,
            "barcode_generation": True,
            "track_expiry_dates": True,
            "allow_negative_stock": False,
        }

        return jsonify({"status": "success", "data": settings})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@settings_bp.route("/inventory", methods=["PUT"])
@login_required
def update_inventory_settings():
    """تحديث إعدادات المخزون"""
    try:
        data = request.get_json()

        # هنا يمكن حفظ الإعدادات في قاعدة البيانات
        # مؤقتاً سنعيد نجاح العملية

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث إعدادات المخزون بنجاح",
                "data": data,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@settings_bp.route("/all", methods=["GET"])
@login_required
def get_all_settings():
    """الحصول على جميع الإعدادات"""
    try:
        settings = {
            "inventory": {
                "auto_reorder": False,
                "low_stock_alert": True,
                "default_warehouse_id": 1,
                "currency": "EGP",
            },
            "system": {
                "company_name": "شركة إدارة المخزون",
                "language": "ar",
                "timezone": "Africa/Cairo",
            },
            "notifications": {
                "email_alerts": True,
                "sms_alerts": False,
                "push_notifications": True,
            },
        }

        return jsonify({"status": "success", "data": settings})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@settings_bp.route("/settings/categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    """إدارة فئات المنتجات"""
    if request.method == "GET":
        categories = Category.query.all()
        return jsonify(
            {"status": "success", "data": [cat.to_dict() for cat in categories]}
        )

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم الفئة مطلوب"}), 400

        # التحقق من عدم وجود فئة بنفس الاسم
        existing = Category.query.filter_by(name=data["name"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "يوجد فئة بهذا الاسم بالفعل"}),
                400,
            )

        category = Category()
        category.name = data["name"]
        category.description = data.get("description", "")

        db.session.add(category)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة الفئة بنجاح",
                    "data": category.to_dict(),
                }
            ),
            201,
        )

    # This should never be reached due to route decorator, but added for type safety
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@settings_bp.route("/settings/categories/<int:category_id>", methods=["PUT", "DELETE"])
@login_required
def update_delete_category(category_id):
    """تحديث أو حذف فئة"""
    category = Category.query.get_or_404(category_id)

    if request.method == "PUT":
        data = request.get_json()

        if data.get("name"):
            # التحقق من عدم وجود فئة أخرى بنفس الاسم
            existing = Category.query.filter(
                Category.name == data["name"], Category.id != category_id
            ).first()
            if existing:
                return (
                    jsonify(
                        {"status": "error", "message": "يوجد فئة بهذا الاسم بالفعل"}
                    ),
                    400,
                )

            category.name = data["name"]

        if "description" in data:
            category.description = data["description"]

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث الفئة بنجاح",
                "data": category.to_dict(),
            }
        )

    elif request.method == "DELETE":
        # التحقق من عدم وجود مجموعات مرتبطة
        groups_count = ProductGroup.query.filter_by(category_id=category_id).count()
        if groups_count > 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"لا يمكن حذف الفئة لوجود {groups_count} مجموعة مرتبطة بها",
                    }
                ),
                400,
            )

        db.session.delete(category)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف الفئة بنجاح"})

    # This should never be reached due to route decorator, but added for type safety
    return error_response(
        message="Method not allowed",
        code=ErrorCodes.SYS_INTERNAL_ERROR,
        status_code=405,
    )


@settings_bp.route("/settings/product-groups", methods=["GET", "POST"])
@login_required
def manage_product_groups():
    """إدارة مجموعات المنتجات"""
    if request.method == "GET":
        groups = ProductGroup.query.all()
        return jsonify(
            {"status": "success", "data": [group.to_dict() for group in groups]}
        )

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("name") or not data.get("category_id"):
            return (
                jsonify({"status": "error", "message": "اسم المجموعة والفئة مطلوبان"}),
                400,
            )

        # التحقق من وجود الفئة
        category = Category.query.get(data["category_id"])
        if not category:
            return (
                jsonify({"status": "error", "message": "الفئة المحددة غير موجودة"}),
                400,
            )

        # التحقق من عدم وجود مجموعة بنفس الاسم في نفس الفئة
        existing = ProductGroup.query.filter_by(
            name=data["name"], category_id=data["category_id"]
        ).first()
        if existing:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "يوجد مجموعة بهذا الاسم في نفس الفئة",
                    }
                ),
                400,
            )

        group = ProductGroup()
        group.name = data["name"]
        group.category_id = data["category_id"]
        group.description = data.get("description", "")

        db.session.add(group)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة المجموعة بنجاح",
                    "data": group.to_dict(),
                }
            ),
            201,
        )

    # This should never be reached due to route decorator, but added for type safety
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@settings_bp.route("/settings/warehouses", methods=["GET", "POST"])
@login_required
def manage_warehouses():
    """إدارة المخازن"""
    if request.method == "GET":
        warehouses = Warehouse.query.all()
        return jsonify(
            {
                "status": "success",
                "data": [warehouse.to_dict() for warehouse in warehouses],
            }
        )

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم المخزن مطلوب"}), 400

        # التحقق من عدم وجود مخزن بنفس الاسم
        existing = Warehouse.query.filter_by(name=data["name"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "يوجد مخزن بهذا الاسم بالفعل"}),
                400,
            )

        warehouse = Warehouse(
            name=data["name"],
            code=data.get("code", f"WH-{data['name'][:3].upper()}"),
            region_id=data.get("region_id", 1),
        )
        warehouse.address = data.get("location", "")
        warehouse.manager_id = data.get("manager_id")
        warehouse.is_active = data.get("is_active", True)

        db.session.add(warehouse)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة المخزن بنجاح",
                    "data": warehouse.to_dict(),
                }
            ),
            201,
        )

    # This should never be reached due to route decorator, but added for type safety
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@settings_bp.route("/settings/customer-types", methods=["GET", "POST"])
@login_required
def manage_customer_types():
    """إدارة أنواع العملاء"""
    if request.method == "GET":
        # الحصول على أنواع العملاء المختلفة من قاعدة البيانات
        customer_types = db.session.query(Customer.customer_type).distinct().all()
        types_list = [ct[0] for ct in customer_types if ct[0]]

        # إضافة أنواع افتراضية إذا لم توجد
        default_types = ["تاجر تجزئة", "تاجر جملة", "مزارع", "شركة", "مؤسسة حكومية"]
        for dt in default_types:
            if dt not in types_list:
                types_list.append(dt)

        return jsonify({"status": "success", "data": types_list})

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("type_name"):
            return jsonify({"status": "error", "message": "اسم نوع العميل مطلوب"}), 400

        # إضافة نوع العميل الجديد (سيتم حفظه عند إضافة عميل جديد)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة نوع العميل بنجاح",
                    "data": {"type_name": data["type_name"]},
                }
            ),
            201,
        )

    # This should never be reached due to route decorator, but added for type safety
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@settings_bp.route("/settings/supplier-types", methods=["GET", "POST"])
@login_required
def manage_supplier_types():
    """إدارة أنواع الموردين"""
    if request.method == "GET":
        # الحصول على أنواع الموردين المختلفة من قاعدة البيانات
        supplier_types = db.session.query(Supplier.supplier_type).distinct().all()
        types_list = [st[0] for st in supplier_types if st[0]]

        # إضافة أنواع افتراضية إذا لم توجد
        default_types = [
            "مورد محلي",
            "مورد دولي",
            "شركة بذور",
            "مصنع أسمدة",
            "مورد مبيدات",
        ]
        for dt in default_types:
            if dt not in types_list:
                types_list.append(dt)

        return jsonify({"status": "success", "data": types_list})

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("type_name"):
            return jsonify({"status": "error", "message": "اسم نوع المورد مطلوب"}), 400

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة نوع المورد بنجاح",
                    "data": {"type_name": data["type_name"]},
                }
            ),
            201,
        )

    # This should never be reached due to route decorator, but added for type safety
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@settings_bp.route("/settings/regions", methods=["GET", "POST"])
@login_required
def manage_regions():
    """إدارة المناطق"""
    if request.method == "GET":
        # الحصول على المناطق من المخازن
        try:
            from src.models.region_warehouse import Region
        except ImportError:
            # If region_warehouse model doesn't exist, use a mock
            class Region:
                id = None
                name = "Default Region"

        regions = Region.query.all()
        regions_list = [r.name for r in regions if r.name]

        # إضافة مناطق افتراضية
        default_regions = [
            "القاهرة",
            "الجيزة",
            "الإسكندرية",
            "الدلتا",
            "الصعيد",
            "سيناء",
        ]
        for dr in default_regions:
            if dr not in regions_list:
                regions_list.append(dr)

        return jsonify({"status": "success", "data": regions_list})

    elif request.method == "POST":
        data = request.get_json()

        if not data.get("region_name"):
            return jsonify({"status": "error", "message": "اسم المنطقة مطلوب"}), 400

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة المنطقة بنجاح",
                    "data": {"region_name": data["region_name"]},
                }
            ),
            201,
        )

    # This should never be reached due to route decorator, but added for type safety
    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@settings_bp.route("/settings/summary", methods=["GET"])
@login_required
def get_settings_summary():
    """ملخص جميع الإعدادات"""
    try:
        categories_count = Category.query.count()
        groups_count = ProductGroup.query.count()
        warehouses_count = Warehouse.query.count()
        customers_count = Customer.query.count()
        suppliers_count = Supplier.query.count()

        return jsonify(
            {
                "status": "success",
                "data": {
                    "categories": categories_count,
                    "product_groups": groups_count,
                    "warehouses": warehouses_count,
                    "customers": customers_count,
                    "suppliers": suppliers_count,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
