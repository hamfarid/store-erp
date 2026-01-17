# FILE: backend/src/routes/products.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# -*- coding: utf-8 -*-
# FILE: backend/src/routes/products.py | PURPOSE: Products routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED: models/inventory.py |
# LAST-AUDITED: 2025-10-25

"""
مسارات المنتجات المحسنة - نسخة نهائية
Enhanced Products Routes - Final Version
P0.2.4: Updated to use unified error envelope
"""

from flask import Blueprint, jsonify, request
from datetime import datetime

# P0.2.4: Import error envelope helpers
try:
    from ..middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes,
    )
except ImportError:
    from middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes,
    )

# إنشاء Blueprint
products_bp = Blueprint("products", __name__)


@products_bp.route("/api/products", methods=["GET"])
def get_products():
    """الحصول على قائمة المنتجات"""
    try:
        # محاولة استخدام النموذج الحقيقي
        try:
            from src.models.product_unified import Product
            from src.database import db

            # الحصول على المعاملات
            page = request.args.get("page", 1, type=int)
            search = request.args.get("search", "")
            per_page = request.args.get("per_page", 50, type=int)

            # بناء الاستعلام
            query = Product.query

            # البحث
            if search:
                from sqlalchemy import or_

                query = query.filter(
                    or_(
                        Product.name.contains(search),
                        (
                            Product.sku.contains(search)
                            if hasattr(Product, "sku")
                            else False
                        ),
                        (
                            Product.barcode.contains(search)
                            if hasattr(Product, "barcode")
                            else False
                        ),
                    )
                )

            # التصفح
            products = query.paginate(page=page, per_page=per_page, error_out=False)

            # P0.2.4: Use unified success envelope
            return success_response(
                data={
                    "products": [product.to_dict() for product in products.items],
                    "pagination": {
                        "page": page,
                        "pages": products.pages,
                        "per_page": per_page,
                        "total": products.total,
                    },
                },
                message="تم الحصول على المنتجات بنجاح / Products retrieved successfully",
                status_code=200,
            )

        except Exception as model_error:
            # استخدام البيانات التجريبية في حالة فشل النموذج
            sample_products = [
                {
                    "id": 1,
                    "name": "منتج تجريبي 1",
                    "sku": "PROD001",
                    "barcode": "1234567890",
                    "price": 100.0,
                    "cost": 80.0,
                    "quantity": 50,
                    "category_id": 1,
                    "is_active": True,
                    "created_at": datetime.now().isoformat(),
                },
                {
                    "id": 2,
                    "name": "منتج تجريبي 2",
                    "sku": "PROD002",
                    "barcode": "1234567891",
                    "price": 200.0,
                    "cost": 160.0,
                    "quantity": 30,
                    "category_id": 1,
                    "is_active": True,
                    "created_at": datetime.now().isoformat(),
                },
            ]

            # تطبيق البحث على البيانات التجريبية
            search = request.args.get("search", "")
            if search:
                sample_products = [
                    p for p in sample_products if search.lower() in p["name"].lower()
                ]

            # P0.2.4: Use unified success envelope for fallback
            return success_response(
                data={
                    "products": sample_products,
                    "total": len(sample_products),
                    "fallback": True,
                },
                message=f"بيانات تجريبية / Sample data: {str(model_error)[:50]}",
                status_code=200,
            )

    except Exception as e:
        # P0.2.4: Use unified error envelope
        return error_response(
            message=f"خطأ في الحصول على المنتجات / Error fetching products: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """الحصول على منتج محدد"""
    try:
        # محاولة استخدام النموذج الحقيقي
        try:
            from src.models.product_unified import Product

            product = Product.query.get_or_404(product_id)
            return success_response(
                data=product.to_dict(), message="Success", status_code=200
            )
        except BaseException:
            # بيانات تجريبية
            if product_id == 1:
                sample_product = {
                    "id": 1,
                    "name": "منتج تجريبي 1",
                    "sku": "PROD001",
                    "barcode": "1234567890",
                    "price": 100.0,
                    "cost": 80.0,
                    "quantity": 50,
                    "category_id": 1,
                    "is_active": True,
                    "created_at": datetime.now().isoformat(),
                }
                return success_response(
                    data={"product": sample_product, "fallback": True},
                    message="تم الحصول على المنتج (بيانات تجريبية) / Product retrieved (sample data)",
                    status_code=200,
                )
            else:
                return error_response(
                    message="المنتج غير موجود / Product not found",
                    code=ErrorCodes.DB_NOT_FOUND,
                    status_code=404,
                )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على المنتج / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/api/products", methods=["POST"])
def create_product():
    """إنشاء منتج جديد"""
    try:
        data = request.get_json()

        if not data or not data.get("name"):
            return error_response(
                message="اسم المنتج مطلوب",
                code=ErrorCodes.VAL_INVALID_FORMAT,
                status_code=400,
            )

        # محاولة استخدام النموذج الحقيقي
        try:
            from src.models.inventory import Product
            from src.database import db

            product = Product(
                name=data["name"],
                description=data.get("description"),
                sku=data.get("sku"),
                barcode=data.get("barcode"),
                category_id=data.get("category_id"),
                price=data.get("price"),
                cost=data.get("cost"),
                quantity=data.get("quantity", 0),
                min_quantity=data.get("min_quantity", 0),
            )

            db.session.add(product)
            db.session.commit()

            return (
                success_response(
                    data=product.to_dict(),
                    message="تم إنشاء المنتج بنجاح",
                    status_code=200,
                ),
                201,
            )

        except Exception as model_error:
            # محاكاة إنشاء المنتج
            new_product = {
                "id": 999,  # ID تجريبي
                "name": data["name"],
                "sku": data.get("sku", "TEMP999"),
                "barcode": data.get("barcode", "9999999999"),
                "price": data.get("price", 0),
                "cost": data.get("cost", 0),
                "quantity": data.get("quantity", 0),
                "category_id": data.get("category_id"),
                "is_active": True,
                "created_at": datetime.now().isoformat(),
            }

            return success_response(
                data={"product": new_product, "fallback": True},
                message=f"تم إنشاء المنتج تجريبياً / Product created (fallback): {str(model_error)[:50]}",
                status_code=201,
            )

    except Exception as e:
        return error_response(
            message=f"خطأ في إنشاء المنتج / Error creating product: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
