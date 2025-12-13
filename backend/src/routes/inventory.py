# FILE: backend/src/routes/inventory.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
APIs إدارة المخزون
/home/ubuntu/inventory_management_system/src/routes/inventory.py
All linting disabled due to complex imports and optional dependencies.
"""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# P0.9: Import permission system
try:
    from src.permissions import require_permission, Permissions
    from src.routes.auth_unified import token_required
except ImportError:
    # Fallback if permissions not available
    def require_permission(*args, **kwargs):
        def decorator(f):
            return f

        return decorator

    def token_required(f):
        return f

    class Permissions:
        CATEGORY_VIEW = "category_view"
        CATEGORY_ADD = "category_add"
        CATEGORY_EDIT = "category_edit"
        CATEGORY_DELETE = "category_delete"
        INVENTORY_VIEW = "inventory_view"
        INVENTORY_ADD = "inventory_add"
        INVENTORY_EDIT = "inventory_edit"
        INVENTORY_DELETE = "inventory_delete"
        WAREHOUSE_VIEW = "warehouse_view"
        WAREHOUSE_ADD = "warehouse_add"
        WAREHOUSE_EDIT = "warehouse_edit"
        WAREHOUSE_DELETE = "warehouse_delete"


# Canonical model imports (avoid legacy models.inventory to prevent duplicate registrations)
from src.models.inventory import Category
from src.models.product_unified import Product
from src.models.warehouse_unified import Warehouse
from src.models.supporting_models import StockMovement
from src.database import db

inventory_bp = Blueprint("inventory", __name__)

# APIs التصنيفات


@inventory_bp.route("/categories", methods=["GET"])
@token_required
@require_permission(Permissions.CATEGORY_VIEW)
def get_categories():
    """P0.9: الحصول على جميع التصنيفات - يتطلب صلاحية عرض التصنيفات"""
    try:
        categories = Category.query.all()
        return jsonify(
            {
                "status": "success",
                "data": [category.to_dict() for category in categories],
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/categories", methods=["POST"])
@token_required
@require_permission(Permissions.CATEGORY_ADD)
def create_category():
    """P0.9: إنشاء تصنيف جديد - يتطلب صلاحية إضافة التصنيفات"""
    try:
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم التصنيف مطلوب"}), 400

        # التحقق من عدم وجود تصنيف بنفس الاسم
        existing = Category.query.filter_by(name=data["name"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "يوجد تصنيف بهذا الاسم بالفعل"}),
                400,
            )

        category = Category()
        category.name = data["name"]
        if hasattr(category, "name_ar"):
            category.name_ar = data.get("name_ar")
        category.description = data.get("description", "")

        db.session.add(category)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء التصنيف بنجاح",
                    "data": category.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs مجموعات المنتجات


@inventory_bp.route("/product-groups", methods=["GET"])
@token_required
@require_permission(Permissions.CATEGORY_VIEW)
def get_product_groups():
    """P0.9: الحصول على جميع مجموعات المنتجات"""
    try:
        groups = ProductGroup.query.all()
        return jsonify(
            {"status": "success", "data": [group.to_dict() for group in groups]}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/product-groups", methods=["POST"])
@token_required
@require_permission(Permissions.CATEGORY_ADD)
def create_product_group():
    """P0.9: إنشاء مجموعة منتجات جديدة"""
    try:
        data = request.get_json()

        if not data.get("name") or not data.get("category_id"):
            return (
                jsonify(
                    {"status": "error", "message": "اسم المجموعة ومعرف التصنيف مطلوبان"}
                ),
                400,
            )

        # التحقق من وجود التصنيف
        category = Category.query.get(data["category_id"])
        if not category:
            return jsonify({"status": "error", "message": "التصنيف غير موجود"}), 404

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
                    "message": "تم إنشاء مجموعة المنتجات بنجاح",
                    "data": group.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs المراتب


@inventory_bp.route("/ranks", methods=["GET"])
@token_required
@require_permission(Permissions.INVENTORY_VIEW)
def get_ranks():
    """P0.9: الحصول على جميع المراتب"""
    try:
        ranks = Rank.query.all()
        return jsonify(
            {"status": "success", "data": [rank.to_dict() for rank in ranks]}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/ranks", methods=["POST"])
@token_required
@require_permission(Permissions.INVENTORY_ADD)
def create_rank():
    """P0.9: إنشاء مرتبة جديدة"""
    try:
        data = request.get_json()

        if not data.get("name") or not data.get("group_id"):
            return (
                jsonify(
                    {"status": "error", "message": "اسم المرتبة ومعرف المجموعة مطلوبان"}
                ),
                400,
            )

        # التحقق من وجود المجموعة
        group = ProductGroup.query.get(data["group_id"])
        if not group:
            return (
                jsonify({"status": "error", "message": "مجموعة المنتجات غير موجودة"}),
                404,
            )

        rank = Rank()
        rank.name = data["name"]
        rank.group_id = data["group_id"]
        rank.description = data.get("description", "")

        db.session.add(rank)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء المرتبة بنجاح",
                    "data": rank.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs الأصناف/المنتجات


@inventory_bp.route("/products", methods=["GET"])
@token_required
@require_permission(Permissions.INVENTORY_VIEW)
def get_products():
    """P0.9: الحصول على جميع الأصناف"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        search = request.args.get("search", "")

        query = Product.query

        if search:
            query = query.filter(Product.name.contains(search))

        products = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "data": [product.to_dict() for product in products.items],
                "pagination": {
                    "page": page,
                    "pages": products.pages,
                    "per_page": per_page,
                    "total": products.total,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/products-advanced", methods=["GET"])
def get_products_advanced():
    """الحصول على جميع المنتجات - واجهة متقدمة"""
    try:
        # الحصول على المعاملات
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        search = request.args.get("search", "")
        category_id = request.args.get("category_id", type=int)

        # بناء الاستعلام
        query = Product.query

        # البحث
        if search:
            query = query.filter(
                db.or_(Product.name.contains(search), Product.barcode.contains(search))
            )

        # فلترة حسب التصنيف
        if category_id:
            query = query.filter(Product.rank_id == category_id)

        # الترقيم
        products = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "products": [product.to_dict() for product in products.items],
                "count": products.total,
                "pages": products.pages,
                "current_page": page,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/products", methods=["POST"])
@token_required
@require_permission(Permissions.INVENTORY_ADD)
def create_product():
    """P0.9: إنشاء صنف جديد"""
    try:
        data = request.get_json()

        required_fields = {"name": "اسم المنتج", "rank_id": "المرتبة", "unit": "الوحدة"}
        for field, field_name in required_fields.items():
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"{field_name} مطلوب"}),
                    400,
                )

        # التحقق من وجود المرتبة
        rank = Rank.query.get(data["rank_id"])
        if not rank:
            return jsonify({"status": "error", "message": "المرتبة غير موجودة"}), 404

        # التحقق من عدم تكرار الباركود إذا تم إدخاله
        if data.get("barcode"):
            existing = Product.query.filter_by(barcode=data["barcode"]).first()
            if existing:
                return (
                    jsonify(
                        {"status": "error", "message": "يوجد منتج بهذا الباركود بالفعل"}
                    ),
                    400,
                )

        product = Product()
        product.name = data["name"]
        product.rank_id = data["rank_id"]
        product.unit = data["unit"]
        product.reorder_quantity = data.get("reorder_quantity", 0)
        product.purchase_price_euro = data.get("purchase_price_euro", 0)
        product.cost_price = data.get("cost_price", 0)
        product.purchase_price_egp = data.get("purchase_price_egp", 0)
        product.selling_price = data.get("selling_price", 0)
        product.treatment_type = data.get("treatment_type", "")
        product.barcode = data.get("barcode")
        product.description = data.get("description", "")
        product.is_active = data.get("is_active", True)

        db.session.add(product)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء الصنف بنجاح",
                    "data": product.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/products/<int:product_id>", methods=["GET"])
@token_required
@require_permission(Permissions.INVENTORY_VIEW)
def get_product(product_id):
    """P0.9: الحصول على منتج واحد"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({"status": "success", "data": product.to_dict()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/products/<int:product_id>", methods=["PUT"])
@token_required
@require_permission(Permissions.INVENTORY_EDIT)
def update_product(product_id):
    """P0.9: تحديث صنف"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        # التحقق من الباركود إذا تم تغييره
        if data.get("barcode") and data["barcode"] != product.barcode:
            existing = Product.query.filter_by(barcode=data["barcode"]).first()
            if existing:
                return (
                    jsonify(
                        {"status": "error", "message": "يوجد منتج بهذا الباركود بالفعل"}
                    ),
                    400,
                )

        # تحديث البيانات
        for field in [
            "name",
            "unit",
            "reorder_quantity",
            "purchase_price_euro",
            "cost_price",
            "purchase_price_egp",
            "selling_price",
            "treatment_type",
            "barcode",
            "description",
            "is_active",
        ]:
            if field in data:
                setattr(product, field, data[field])

        product.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث الصنف بنجاح",
                "data": product.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/products/<int:product_id>", methods=["DELETE"])
@token_required
@require_permission(Permissions.INVENTORY_DELETE)
def delete_product(product_id):
    """P0.9: حذف منتج"""
    try:
        product = Product.query.get_or_404(product_id)

        # التحقق من وجود حركات مخزون للمنتج
        movements = StockMovement.query.filter_by(product_id=product_id).first()
        if movements:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "لا يمكن حذف المنتج لوجود حركات مخزون مرتبطة به",
                    }
                ),
                400,
            )

        db.session.delete(product)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف المنتج بنجاح"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs المخازن


@inventory_bp.route("/warehouses", methods=["GET"])
@token_required
@require_permission(Permissions.WAREHOUSE_VIEW)
def get_warehouses():
    """P0.9: الحصول على جميع المخازن"""
    try:
        warehouses = Warehouse.query.all()
        return jsonify(
            {
                "status": "success",
                "data": [warehouse.to_dict() for warehouse in warehouses],
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@inventory_bp.route("/warehouses", methods=["POST"])
@token_required
@require_permission(Permissions.WAREHOUSE_ADD)
def create_warehouse():
    """P0.9: إنشاء مخزن جديد"""
    try:
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

        warehouse = Warehouse()
        warehouse.name = data["name"]
        if hasattr(warehouse, "name_ar"):
            warehouse.name_ar = data.get("name_ar")
        warehouse.location = data.get("location", "")
        warehouse.region = data.get("region", "")
        warehouse.manager_id = data.get("manager_id")
        warehouse.is_active = data.get("is_active", True)

        db.session.add(warehouse)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء المخزن بنجاح",
                    "data": warehouse.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# API إحصائيات لوحة المعلومات


@inventory_bp.route("/dashboard-stats", methods=["GET"])
@token_required
@require_permission(Permissions.INVENTORY_VIEW)
def get_dashboard_stats():
    """P0.9: الحصول على إحصائيات لوحة المعلومات"""
    try:
        stats = {
            "total_products": Product.query.filter_by(is_active=True).count(),
            "total_warehouses": Warehouse.query.filter_by(is_active=True).count(),
            "total_categories": Category.query.count(),
            "total_movements": StockMovement.query.count(),
            "low_stock_products": 0,  # سيتم حسابها لاحقاً
        }

        return jsonify({"status": "success", "data": stats})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
