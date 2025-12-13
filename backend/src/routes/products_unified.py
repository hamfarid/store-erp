# Ensure error envelope utilities are available
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# FILE: backend/src/routes/products_unified.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/backend/src/routes/products_unified.py
مسارات المنتجات الموحدة والمحسّنة
Unified and Enhanced Products Routes

يوفر:
- قائمة المنتجات (مع تصفح وبحث متقدم)
- الحصول على منتج
- إنشاء منتج
- تحديث منتج
- حذف منتج
- إحصائيات المنتجات
- المنتجات منخفضة المخزون
"""

import logging
from datetime import datetime

from flask import Blueprint, jsonify, request
from src.database import db

# Validation and API metadata
try:
    from src.utils.validation import (
        ProductCreateSchema,
        ProductUpdateSchema,
        UpdateStockSchema,
        validate_json,
    )
except ImportError:
    # Fallback implementations
    validate_json = lambda *_a, **_k: (lambda f: f)  # type: ignore

    class ProductCreateSchema: ...  # type: ignore

    class ProductUpdateSchema: ...  # type: ignore

    class UpdateStockSchema: ...  # type: ignore


try:
    from src.api_meta import api_endpoint as api_meta, register_schema
except ImportError:

    def _noop(f):
        return f

    def api_meta(*_a, **_k):  # type: ignore
        return _noop

    def register_schema(_name: str, _schema: dict):  # type: ignore
        return None


# Register schemas
register_schema(
    "ProductCreateRequest",
    {
        "type": "object",
        "required": ["name", "cost_price", "sale_price"],
        "properties": {
            "name": {"type": "string"},
            "cost_price": {"type": "number"},
            "sale_price": {"type": "number"},
            "sku": {"type": "string"},
            "barcode": {"type": "string"},
            "category_id": {"type": "integer"},
            "is_active": {"type": "boolean"},
        },
    },
)
register_schema(
    "ProductUpdateRequest",
    {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "cost_price": {"type": "number"},
            "sale_price": {"type": "number"},
            "sku": {"type": "string"},
            "barcode": {"type": "string"},
            "category_id": {"type": "integer"},
            "is_active": {"type": "boolean"},
        },
    },
)
register_schema(
    "UpdateStockRequest",
    {
        "type": "object",
        "required": ["quantity"],
        "properties": {"quantity": {"type": "number"}, "reason": {"type": "string"}},
    },
)

# --- Additional OpenAPI schemas (generic, tolerant) ---
try:
    register_schema("Product", {"type": "object", "additionalProperties": True})
    register_schema(
        "ProductList",
        {"type": "array", "items": {"$ref": "#/components/schemas/Product"}},
    )
    register_schema(
        "Pagination",
        {
            "type": "object",
            "properties": {
                "page": {"type": "integer"},
                "per_page": {"type": "integer"},
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "has_next": {"type": "boolean"},
                "has_prev": {"type": "boolean"},
            },
        },
    )
    register_schema(
        "ProductResponse",
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "data": {"$ref": "#/components/schemas/Product"},
            },
        },
    )
    register_schema(
        "ProductListResponse",
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "data": {"$ref": "#/components/schemas/ProductList"},
                "total": {"type": "integer"},
            },
        },
    )
    register_schema(
        "PaginatedProductListResponse",
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "data": {"$ref": "#/components/schemas/ProductList"},
                "pagination": {"$ref": "#/components/schemas/Pagination"},
            },
        },
    )
    register_schema("Category", {"type": "object", "additionalProperties": True})
    register_schema(
        "CategoryListResponse",
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Category"},
                },
            },
        },
    )
    register_schema("ProductsStats", {"type": "object", "additionalProperties": True})
    register_schema(
        "ProductsStatsResponse",
        {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "data": {"$ref": "#/components/schemas/ProductsStats"},
            },
        },
    )
except Exception:
    pass

# استيراد النماذج الموحدة
try:
    from src.models.inventory import Category
    from src.models.product_unified import Product, ProductType, TrackingType
    from src.models.supporting_models import ActionType

    UNIFIED_MODELS = True
except ImportError:
    try:
        from src.models.inventory import Category
        from src.models.inventory import Product

        UNIFIED_MODELS = False
    except ImportError:
        Product = None
        Category = None
        UNIFIED_MODELS = False

# استيراد decorators
try:
    from src.routes.auth_unified import admin_required, log_activity, token_required
except ImportError:
    from functools import wraps

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated

    def log_activity(user_id, action, details=None):
        pass


logger = logging.getLogger(__name__)

products_unified_bp = Blueprint("products_unified", __name__)


# ============================================================================
# مسارات المنتجات
# ============================================================================


@products_unified_bp.route("/api/products", methods=["GET"])
@token_required
@api_meta(
    summary="List products",
    tags=["Products"],
    response_schema="PaginatedProductListResponse",
)
def get_products():
    """
    الحصول على قائمة المنتجات

    Query Parameters:
        page: رقم الصفحة (افتراضي: 1)
        per_page: عدد العناصر (افتراضي: 20)
        search: البحث في الاسم/SKU/Barcode
        category_id: تصفية حسب الفئة
        product_type: تصفية حسب النوع (storable, consumable, service, digital)
        is_active: تصفية حسب الحالة
        low_stock: المنتجات منخفضة المخزون
        out_of_stock: المنتجات نافدة
        sort_by: الترتيب حسب (name, sku, price, stock)
        sort_order: اتجاه الترتيب (asc, desc)
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # معاملات الاستعلام
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        search = request.args.get("search", "")
        category_id = request.args.get("category_id", type=int)
        product_type = request.args.get("product_type", "")
        is_active = request.args.get("is_active", "")
        low_stock = request.args.get("low_stock", "").lower() == "true"
        out_of_stock = request.args.get("out_of_stock", "").lower() == "true"
        sort_by = request.args.get("sort_by", "name")
        sort_order = request.args.get("sort_order", "asc")

        # بناء الاستعلام
        query = Product.query

        # البحث
        if search:
            search_filter = db.or_(Product.name.ilike(f"%{search}%"))

            # إضافة حقول إضافية للبحث إذا كانت موجودة
            if hasattr(Product, "sku"):
                search_filter = db.or_(search_filter, Product.sku.ilike(f"%{search}%"))
            if hasattr(Product, "barcode"):
                search_filter = db.or_(
                    search_filter, Product.barcode.ilike(f"%{search}%")
                )
            if hasattr(Product, "name_en") and UNIFIED_MODELS:
                search_filter = db.or_(
                    search_filter, Product.name_en.ilike(f"%{search}%")
                )

            query = query.filter(search_filter)

        # تصفية حسب الفئة
        if category_id:
            query = query.filter(Product.category_id == category_id)

        # تصفية حسب النوع
        if product_type and UNIFIED_MODELS:
            try:
                ptype = ProductType[product_type.upper()]
                query = query.filter(Product.product_type == ptype)
            except KeyError:
                pass

        # تصفية حسب الحالة
        if is_active:
            query = query.filter(Product.is_active == (is_active.lower() == "true"))

        # تصفية المنتجات منخفضة المخزون
        if (
            low_stock
            and hasattr(Product, "current_stock")
            and hasattr(Product, "min_quantity")
        ):
            query = query.filter(
                Product.current_stock <= Product.min_quantity, Product.current_stock > 0
            )

        # تصفية المنتجات نافدة
        if out_of_stock and hasattr(Product, "current_stock"):
            query = query.filter(Product.current_stock <= 0)

        # الترتيب
        sort_column = getattr(Product, sort_by, Product.name)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # التصفح
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "products": [product.to_dict() for product in pagination.items],
                        "pagination": {
                            "page": page,
                            "per_page": per_page,
                            "total": pagination.total,
                            "pages": pagination.pages,
                            "has_next": pagination.has_next,
                            "has_prev": pagination.has_prev,
                        },
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المنتجات: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على المنتجات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/<int:product_id>", methods=["GET"])
@token_required
@api_meta(summary="Get product", tags=["Products"], response_schema="ProductResponse")
def get_product(product_id):
    """
    الحصول على منتج محدد
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        product = Product.query.get(product_id)

        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        return (
            success_response(
                data=product.to_dict(), message="Success", status_code=200
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المنتج: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products", methods=["POST"])
@token_required
@validate_json(ProductCreateSchema)
@api_meta(
    summary="Create product",
    tags=["Products"],
    request_schema="ProductCreateRequest",
    response_schema="ProductResponse",
)
def create_product():
    """
    إنشاء منتج جديد

    Body:
        name: اسم المنتج (مطلوب)
        sku: رمز المنتج
        barcode: الباركود
        category_id: معرف الفئة
        product_type: نوع المنتج (storable, consumable, service, digital)
        tracking_type: نوع التتبع (none, lot, serial, expiry)
        cost_price: سعر التكلفة (مطلوب)
        sale_price: سعر البيع (مطلوب)
        wholesale_price: سعر الجملة
        min_price: الحد الأدنى للسعر
        current_stock: المخزون الحالي
        min_quantity: الحد الأدنى للكمية
        max_quantity: الحد الأقصى للكمية
        reorder_point: نقطة إعادة الطلب
        is_active: الحالة (افتراضي: true)
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data or not data.get("name"):
            return error_response(
                message="اسم المنتج مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        if not data.get("cost_price") or not data.get("sale_price"):
            return error_response(
                message="سعر التكلفة وسعر البيع مطلوبان",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من عدم تكرار SKU
        if data.get("sku") and hasattr(Product, "sku"):
            existing = Product.query.filter_by(sku=data["sku"]).first()
            if existing:
                return error_response(
                    message="رمز المنتج (SKU) موجود بالفعل",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        # التحقق من عدم تكرار Barcode
        if data.get("barcode") and hasattr(Product, "barcode"):
            existing = Product.query.filter_by(barcode=data["barcode"]).first()
            if existing:
                return error_response(
                    message="الباركود موجود بالفعل",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        # إنشاء المنتج
        product_data = {"name": data["name"], "is_active": data.get("is_active", True)}

        # إضافة الحقول الاختيارية
        optional_fields = [
            "sku",
            "barcode",
            "name_en",
            "category_id",
            "supplier_id",
            "warehouse_id",
            "cost_price",
            "sale_price",
            "wholesale_price",
            "min_price",
            "current_stock",
            "min_quantity",
            "max_quantity",
            "reorder_point",
            "description",
            "description_en",
            "specifications",
            "unit",
            "unit_en",
            "weight",
            "dimensions",
            "image_url",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]

        for field in optional_fields:
            if field in data and hasattr(Product, field):
                product_data[field] = data[field]

        # معالجة Enums للنماذج الموحدة
        if UNIFIED_MODELS:
            if "product_type" in data:
                try:
                    product_data["product_type"] = ProductType[
                        data["product_type"].upper()
                    ]
                except KeyError:
                    product_data["product_type"] = ProductType.STORABLE

            if "tracking_type" in data:
                try:
                    product_data["tracking_type"] = TrackingType[
                        data["tracking_type"].upper()
                    ]
                except KeyError:
                    product_data["tracking_type"] = TrackingType.NONE

        product = Product(**product_data)

        db.session.add(product)
        db.session.commit()

        # تسجيل النشاط
        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                ActionType.CREATE if UNIFIED_MODELS else "create",
                {"entity": "product", "entity_id": product.id, "name": product.name},
            )

        return (
            success_response(
                data=product.to_dict(), message="تم إنشاء المنتج بنجاح", status_code=200
            ),
            201,
        )

    except Exception as e:
        logger.error(f"خطأ في إنشاء المنتج: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء إنشاء المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/<int:product_id>", methods=["PUT"])
@token_required
@validate_json(ProductUpdateSchema)
@api_meta(
    summary="Update product",
    tags=["Products"],
    request_schema="ProductUpdateRequest",
    response_schema="ProductResponse",
)
def update_product(product_id):
    """
    تحديث منتج

    Body: نفس حقول الإنشاء (جميعها اختيارية)
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        product = Product.query.get(product_id)

        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        data = request.get_json()

        # التحقق من عدم تكرار SKU
        if data.get("sku") and hasattr(Product, "sku"):
            existing = Product.query.filter(
                Product.sku == data["sku"], Product.id != product_id
            ).first()
            if existing:
                return error_response(
                    message="رمز المنتج (SKU) موجود بالفعل",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        # التحقق من عدم تكرار Barcode
        if data.get("barcode") and hasattr(Product, "barcode"):
            existing = Product.query.filter(
                Product.barcode == data["barcode"], Product.id != product_id
            ).first()
            if existing:
                return error_response(
                    message="الباركود موجود بالفعل",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        # تحديث الحقول
        updatable_fields = [
            "name",
            "sku",
            "barcode",
            "name_en",
            "category_id",
            "supplier_id",
            "warehouse_id",
            "cost_price",
            "sale_price",
            "wholesale_price",
            "min_price",
            "current_stock",
            "min_quantity",
            "max_quantity",
            "reorder_point",
            "description",
            "description_en",
            "specifications",
            "unit",
            "unit_en",
            "weight",
            "dimensions",
            "image_url",
            "is_active",
            "meta_title",
            "meta_description",
            "meta_keywords",
        ]

        for field in updatable_fields:
            if field in data and hasattr(Product, field):
                setattr(product, field, data[field])

        # معالجة Enums
        if UNIFIED_MODELS:
            if "product_type" in data:
                try:
                    product.product_type = ProductType[data["product_type"].upper()]
                except KeyError:
                    pass

            if "tracking_type" in data:
                try:
                    product.tracking_type = TrackingType[data["tracking_type"].upper()]
                except KeyError:
                    pass

        # تحديث التاريخ
        if hasattr(Product, "updated_at"):
            product.updated_at = datetime.utcnow()

        db.session.commit()

        # تسجيل النشاط
        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                ActionType.UPDATE if UNIFIED_MODELS else "update",
                {"entity": "product", "entity_id": product.id, "name": product.name},
            )

        return success_response(
            data=product.to_dict(), message="تم تحديث المنتج بنجاح", status_code=200
        )

    except Exception as e:
        logger.error(f"خطأ في تحديث المنتج: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء تحديث المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/<int:product_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_product(product_id):
    """
    حذف منتج
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        product = Product.query.get(product_id)

        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # التحقق من عدم وجود معاملات مرتبطة
        # يمكن إضافة فحوصات إضافية هنا

        name = product.name

        # حذف المنتج
        db.session.delete(product)
        db.session.commit()

        # تسجيل النشاط
        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                ActionType.DELETE if UNIFIED_MODELS else "delete",
                {"entity": "product", "entity_id": product_id, "name": name},
            )

        return success_response(message="تم حذف المنتج بنجاح", status_code=200)

    except Exception as e:
        logger.error(f"خطأ في حذف المنتج: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء حذف المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


# ============================================================================
# مسارات إضافية
# ============================================================================


@products_unified_bp.route("/api/products/low-stock", methods=["GET"])
@token_required
@api_meta(
    summary="Low stock products",
    tags=["Products"],
    response_schema="ProductListResponse",
)
def get_low_stock_products():
    """
    الحصول على المنتجات منخفضة المخزون
    """
    try:
        if not Product:
            return success_response(
                data={"total": 0}, message="Success", status_code=200
            )

        if not hasattr(Product, "current_stock") or not hasattr(
            Product, "min_quantity"
        ):
            # If attributes don't exist, return empty result instead of error
            return success_response(
                data={"total": 0}, message="Success", status_code=200
            )

        # المنتجات منخفضة المخزون
        products = Product.query.filter(
            Product.current_stock <= Product.min_quantity,
            Product.current_stock > 0,
            Product.is_active.is_(True),
        ).all()

        return success_response(
            data={"total": len(products)}, message="Success", status_code=200
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المنتجات منخفضة المخزون: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على المنتجات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/out-of-stock", methods=["GET"])
@token_required
@api_meta(
    summary="Out of stock products",
    tags=["Products"],
    response_schema="ProductListResponse",
)
def get_out_of_stock_products():
    """
    الحصول على المنتجات نافدة
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        if not hasattr(Product, "current_stock"):
            return error_response(
                message="حقل المخزون غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # المنتجات نافدة
        products = Product.query.filter(
            Product.current_stock <= 0, Product.is_active.is_(True)
        ).all()

        return success_response(
            data={"total": len(products)}, message="Success", status_code=200
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على المنتجات نافدة: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على المنتجات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/stats", methods=["GET"])
@token_required
@api_meta(
    summary="Products stats", tags=["Products"], response_schema="ProductsStatsResponse"
)
def get_products_stats():
    """
    الحصول على إحصائيات المنتجات
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # إحصائيات عامة
        total_products = Product.query.count()
        active_products = Product.query.filter_by(is_active=True).count()
        inactive_products = total_products - active_products

        stats = {
            "total_products": total_products,
            "active_products": active_products,
            "inactive_products": inactive_products,
        }

        # إحصائيات المخزون (إذا كانت متاحة)
        if hasattr(Product, "current_stock"):
            total_stock = (
                db.session.query(db.func.sum(Product.current_stock)).scalar() or 0
            )
            stats["total_stock"] = float(total_stock)

            if hasattr(Product, "min_quantity"):
                low_stock = Product.query.filter(
                    Product.current_stock <= Product.min_quantity,
                    Product.current_stock > 0,
                ).count()
                out_of_stock = Product.query.filter(Product.current_stock <= 0).count()

                stats["low_stock_products"] = low_stock
                stats["out_of_stock_products"] = out_of_stock

        # إحصائيات القيمة (إذا كانت متاحة)
        if hasattr(Product, "cost_price") and hasattr(Product, "current_stock"):
            total_value = (
                db.session.query(
                    db.func.sum(Product.cost_price * Product.current_stock)
                ).scalar()
                or 0
            )
            stats["total_inventory_value"] = float(total_value)

        # إحصائيات حسب النوع (للنماذل الموحدة)
        if UNIFIED_MODELS and hasattr(Product, "product_type"):
            try:
                by_type = {}
                for ptype in ProductType:
                    count = Product.query.filter_by(product_type=ptype).count()
                    by_type[ptype.value] = count
                stats["by_type"] = by_type
            except Exception as e:
                logger.warning(f"Could not get stats by type: {e}")

        # إحصائيات حسب الفئة
        if hasattr(Product, "category_id") and Category:
            try:
                by_category = (
                    db.session.query(
                        Category.name, db.func.count(Product.id).label("count")
                    )
                    .join(Product)
                    .group_by(Category.name)
                    .all()
                )

                stats["by_category"] = [
                    {"category": cat, "count": count} for cat, count in by_category
                ]
            except Exception as e:
                logger.warning(f"Could not get stats by category: {e}")

        return success_response(data=stats, message="Success", status_code=200)

    except Exception as e:
        import traceback

        error_detail = traceback.format_exc()
        logger.error(f"خطأ في الحصول على إحصائيات المنتجات: {e}")
        logger.error(f"Traceback: {error_detail}")
        return error_response(
            message="حدث خطأ أثناء الحصول على الإحصائيات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route(
    "/api/products/<int:product_id>/update-stock", methods=["POST"]
)
@token_required
@validate_json(UpdateStockSchema)
@api_meta(
    summary="Update product stock",
    tags=["Products"],
    request_schema="UpdateStockRequest",
)
def update_product_stock(product_id):
    """
    تحديث مخزون منتج

    Body:
        quantity: الكمية الجديدة (مطلوب)
        reason: سبب التحديث (اختياري)
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        if not hasattr(Product, "current_stock"):
            return error_response(
                message="حقل المخزون غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        product = Product.query.get(product_id)

        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        data = request.get_json()

        if "quantity" not in data:
            return error_response(
                message="الكمية مطلوبة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        old_stock = product.current_stock
        new_stock = data["quantity"]

        # استخدام دالة update_stock إذا كانت متاحة
        if hasattr(product, "update_stock"):
            product.update_stock(new_stock)
        else:
            product.current_stock = new_stock

        db.session.commit()

        # تسجيل النشاط
        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                ActionType.UPDATE if UNIFIED_MODELS else "update",
                {
                    "entity": "product_stock",
                    "entity_id": product.id,
                    "name": product.name,
                    "old_stock": old_stock,
                    "new_stock": new_stock,
                    "reason": data.get("reason", ""),
                },
            )

        return success_response(
            data=product.to_dict(), message="تم تحديث المخزون بنجاح", status_code=200
        )

    except Exception as e:
        logger.error(f"خطأ في تحديث المخزون: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ أثناء تحديث المخزون",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/categories", methods=["GET"])
@token_required
@api_meta(
    summary="List categories", tags=["Products"], response_schema="CategoryListResponse"
)
def get_product_categories():
    """
    الحصول على قائمة الفئات
    """
    try:
        if not Category:
            return error_response(
                message="نموذج الفئات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        categories = Category.query.all()

        return success_response(
            data=[cat.to_dict() for cat in categories],
            message="Success",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على الفئات: {e}")
        return error_response(
            message="حدث خطأ أثناء الحصول على الفئات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/search", methods=["GET"])
@token_required
@api_meta(
    summary="Search products", tags=["Products"], response_schema="ProductListResponse"
)
def search_products():
    """
    البحث السريع في المنتجات

    Query Parameters:
        q: نص البحث (مطلوب)
        limit: عدد النتائج (افتراضي: 10)
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        query_text = request.args.get("q", "")
        limit = request.args.get("limit", 10, type=int)

        if not query_text:
            return error_response(
                message="نص البحث مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # البحث
        search_filter = db.or_(Product.name.ilike(f"%{query_text}%"))

        if hasattr(Product, "sku"):
            search_filter = db.or_(search_filter, Product.sku.ilike(f"%{query_text}%"))
        if hasattr(Product, "barcode"):
            search_filter = db.or_(
                search_filter, Product.barcode.ilike(f"%{query_text}%")
            )

        products = Product.query.filter(search_filter).limit(limit).all()

        return success_response(
            data=[p.to_dict() for p in products], message="Success", status_code=200
        )

    except Exception as e:
        logger.error(f"خطأ في البحث عن المنتجات: {e}")
        return error_response(
            message="حدث خطأ أثناء البحث",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_unified_bp.route("/api/products/export", methods=["GET"])
@token_required
def export_products():
    """
    تصدير المنتجات (CSV/JSON)

    Query Parameters:
        format: صيغة التصدير (csv, json) - افتراضي: json
    """
    try:
        if not Product:
            return error_response(
                message="نموذج المنتجات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        export_format = request.args.get("format", "json").lower()

        products = Product.query.all()
        products_data = [product.to_dict() for product in products]

        if export_format == "csv":
            # يمكن إضافة تصدير CSV هنا
            return error_response(
                message="تصدير CSV غير مدعوم حالياً",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # تسجيل النشاط
        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                ActionType.EXPORT if UNIFIED_MODELS else "export",
                {
                    "entity": "products",
                    "format": export_format,
                    "count": len(products_data),
                },
            )

        return success_response(
            data={
                "products": products_data,
                "total": len(products_data),
                "format": export_format,
            },
            message="تم تصدير المنتجات بنجاح / Products exported successfully",
            status_code=200,
        )

    except Exception as e:
        logger.error(f"خطأ في تصدير المنتجات: {e}")
        return error_response(
            message="حدث خطأ أثناء التصدير",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


# ============================================================================
# مسارات متقدمة (للنماذج الموحدة فقط)
# ============================================================================

if UNIFIED_MODELS:

    @products_unified_bp.route(
        "/api/products/<int:product_id>/profit-margin", methods=["GET"]
    )
    @token_required
    def get_product_profit_margin(product_id):
        """
        حساب هامش الربح لمنتج
        """
        try:
            product = Product.query.get(product_id)

            if not product:
                return error_response(
                    message="المنتج غير موجود",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=404,
                )

            if hasattr(product, "calculate_profit_margin"):
                margin = product.calculate_profit_margin()

                return (
                    jsonify(
                        {
                            "success": True,
                            "data": {
                                "product_id": product.id,
                                "product_name": product.name,
                                "cost_price": float(product.cost_price),
                                "sale_price": float(product.sale_price),
                                "profit_margin": margin,
                            },
                        }
                    ),
                    200,
                )
            else:
                return error_response(
                    message="حساب هامش الربح غير متاح",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=501,
                )

        except Exception as e:
            logger.error(f"خطأ في حساب هامش الربح: {e}")
            return error_response(
                message="حدث خطأ أثناء الحساب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=500,
            )

    @products_unified_bp.route(
        "/api/products/by-type/<string:product_type>", methods=["GET"]
    )
    @token_required
    def get_products_by_type(product_type):
        """
        الحصول على المنتجات حسب النوع
        """
        try:
            try:
                ptype = ProductType[product_type.upper()]
            except KeyError:
                return error_response(
                    message="نوع المنتج غير صحيح",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

            products = Product.query.filter_by(product_type=ptype).all()

            return success_response(
                data={
                    "products": [product.to_dict() for product in products],
                    "total": len(products),
                    "product_type": product_type,
                },
                message="تم الحصول على المنتجات بنجاح / Products retrieved successfully",
                status_code=200,
            )

        except Exception as e:
            logger.error(f"خطأ في الحصول على المنتجات حسب النوع: {e}")
            return error_response(
                message="حدث خطأ أثناء الحصول على المنتجات",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=500,
            )

            logger.error(f"خطأ في الحصول على المنتجات حسب النوع: {e}")
            return error_response(
                message="حدث خطأ أثناء الحصول على المنتجات",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=500,
            )
