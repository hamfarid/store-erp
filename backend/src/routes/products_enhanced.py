# -*- coding: utf-8 -*-
# FILE: backend/src/routes/products_enhanced.py | PURPOSE: Enhanced
# Product API Routes | OWNER: Backend | RELATED: products_fixed.py |
# LAST-AUDITED: 2025-10-28

"""
مسارات API المحسنة للمنتجات
Enhanced Product API Routes

يتضمن:
- CRUD operations آمنة للمنتجات
- البحث والفلترة المتقدمة
- إدارة الفئات والعلامات التجارية
- تحميل الصور وإدارة الملفات
- إحصائيات وتقارير المنتجات
- Cache optimization
- Rate limiting
- Input validation شامل
"""

from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.orm import joinedload
import os
import uuid
from datetime import datetime
from PIL import Image
import io

from src.database import db
from src.models.enhanced_models import (
    Product,
    Category,
    Brand,
    ProductImage,
    StockMovement,
)
from src.schemas.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductSearchSchema,
    CategorySchema,
    BrandSchema,
    ProductImageSchema,
)
from src.cache_manager import cache_manager
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

# إنشاء Blueprint
products_bp = Blueprint("products", __name__, url_prefix="/api/products")

# Schemas للتحقق من البيانات
product_create_schema = ProductCreateSchema()
product_update_schema = ProductUpdateSchema()
product_search_schema = ProductSearchSchema()
category_schema = CategorySchema()
brand_schema = BrandSchema()
product_image_schema = ProductImageSchema()

# إعدادات تحميل الملفات
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
IMAGE_SIZES = {"thumbnail": (150, 150), "medium": (400, 400), "large": (800, 800)}


def allowed_file(filename):
    """التحقق من امتداد الملف المسموح"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def optimize_image(image_file, size=None, quality=85):
    """تحسين وضغط الصورة"""
    try:
        # فتح الصورة
        img = Image.open(image_file)

        # تحويل إلى RGB إذا كانت RGBA
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background

        # تغيير الحجم إذا تم تحديده
        if size:
            img.thumbnail(size, Image.Resampling.LANCZOS)

        # حفظ الصورة المحسنة
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output

    except Exception as e:
        current_app.logger.error(f"Image optimization error: {str(e)}")
        return None


def save_product_image(file, product_id):
    """حفظ صورة المنتج بأحجام متعددة"""
    try:
        if not file or not allowed_file(file.filename):
            return None

        # إنشاء اسم ملف آمن
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        # إنشاء مجلد المنتج
        upload_folder = os.path.join(
            current_app.config.get("UPLOAD_FOLDER", "uploads"),
            "products",
            str(product_id),
        )
        os.makedirs(upload_folder, exist_ok=True)

        # حفظ الصورة الأصلية
        original_path = os.path.join(upload_folder, f"original_{unique_filename}")
        file.save(original_path)

        # إنشاء أحجام مختلفة
        image_paths = {"original": original_path}

        for size_name, size_dimensions in IMAGE_SIZES.items():
            optimized_image = optimize_image(original_path, size_dimensions)
            if optimized_image:
                size_path = os.path.join(
                    upload_folder, f"{size_name}_{unique_filename}"
                )
                with open(size_path, "wb") as f:
                    f.write(optimized_image.getvalue())
                image_paths[size_name] = size_path

        return {
            "filename": unique_filename,
            "paths": image_paths,
            "url": f"/api/products/{product_id}/images/{unique_filename}",
        }

    except Exception as e:
        current_app.logger.error(f"Save image error: {str(e)}")
        return None


@products_bp.route("/", methods=["GET"])
@cache_manager.cached(timeout=300, query_string=True)
def get_products():
    """الحصول على قائمة المنتجات مع البحث والفلترة"""
    try:
        # التحقق من صحة معاملات البحث
        search_params = product_search_schema.load(request.args.to_dict())

        # بناء الاستعلام الأساسي
        query = Product.query.options(
            joinedload(Product.category),
            joinedload(Product.brand),
            joinedload(Product.images),
        )

        # تطبيق الفلاتر
        if search_params.get("search"):
            search_term = f"%{search_params['search']}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.name_ar.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.description_ar.ilike(search_term),
                    Product.sku.ilike(search_term),
                    Product.barcode.ilike(search_term),
                )
            )

        if search_params.get("category_id"):
            query = query.filter(Product.category_id == search_params["category_id"])

        if search_params.get("brand_id"):
            query = query.filter(Product.brand_id == search_params["brand_id"])

        if search_params.get("min_price"):
            query = query.filter(Product.price >= search_params["min_price"])

        if search_params.get("max_price"):
            query = query.filter(Product.price <= search_params["max_price"])

        if search_params.get("in_stock") is not None:
            if search_params["in_stock"]:
                query = query.filter(Product.stock_quantity > 0)
            else:
                query = query.filter(Product.stock_quantity <= 0)

        if search_params.get("is_active") is not None:
            query = query.filter(Product.is_active == search_params["is_active"])

        # الترتيب
        sort_by = search_params.get("sort_by", "name")
        sort_order = search_params.get("sort_order", "asc")

        if hasattr(Product, sort_by):
            if sort_order == "desc":
                query = query.order_by(desc(getattr(Product, sort_by)))
            else:
                query = query.order_by(asc(getattr(Product, sort_by)))

        # التصفح (Pagination)
        page = search_params.get("page", 1)
        per_page = min(search_params.get("per_page", 20), 100)  # حد أقصى 100 عنصر

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        # تحضير البيانات
        products_data = []
        for product in paginated.items:
            product_dict = product.to_dict()

            # إضافة معلومات الصور
            if product.images:
                product_dict["images"] = [img.to_dict() for img in product.images]

            # إضافة معلومات المخزون
            product_dict["stock_status"] = (
                "in_stock" if product.stock_quantity > 0 else "out_of_stock"
            )
            if product.stock_quantity <= product.reorder_level:
                product_dict["stock_status"] = "low_stock"

            products_data.append(product_dict)

        return success_response(
            data={
                "products": products_data,
                "pagination": {
                    "page": paginated.page,
                    "per_page": paginated.per_page,
                    "total": paginated.total,
                    "pages": paginated.pages,
                    "has_next": paginated.has_next,
                    "has_prev": paginated.has_prev,
                },
                "filters_applied": search_params,
            },
            message="تم جلب المنتجات بنجاح",
            status_code=200,
        )

    except ValidationError as e:
        return error_response(
            message="معاملات البحث غير صحيحة",
            code=ErrorCodes.VAL_INVALID_INPUT,
            details=e.messages,
            status_code=400,
        )

    except Exception as e:
        current_app.logger.error(f"Get products error: {str(e)}")
        return error_response(
            message="خطأ في جلب المنتجات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/<int:product_id>", methods=["GET"])
@cache_manager.cached(timeout=600)
def get_product(product_id):
    """الحصول على منتج محدد"""
    try:
        product = Product.query.options(
            joinedload(Product.category),
            joinedload(Product.brand),
            joinedload(Product.images),
        ).get(product_id)

        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        # تحضير بيانات المنتج
        product_data = product.to_dict()

        # إضافة معلومات الصور
        if product.images:
            product_data["images"] = [img.to_dict() for img in product.images]

        # إضافة معلومات المخزون
        product_data["stock_status"] = (
            "in_stock" if product.stock_quantity > 0 else "out_of_stock"
        )
        if product.stock_quantity <= product.reorder_level:
            product_data["stock_status"] = "low_stock"

        # إضافة حركات المخزون الأخيرة
        recent_movements = (
            StockMovement.query.filter_by(product_id=product_id)
            .order_by(desc(StockMovement.created_at))
            .limit(10)
            .all()
        )

        product_data["recent_stock_movements"] = [
            movement.to_dict() for movement in recent_movements
        ]

        return success_response(
            data={"product": product_data},
            message="تم جلب المنتج بنجاح",
            status_code=200,
        )

    except Exception as e:
        current_app.logger.error(f"Get product error: {str(e)}")
        return error_response(
            message="خطأ في جلب المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    """إنشاء منتج جديد"""
    try:
        current_user_id = get_jwt_identity()

        # التحقق من صحة البيانات
        data = product_create_schema.load(request.json)

        # التحقق من عدم تكرار SKU أو الباركود
        existing_product = Product.query.filter(
            or_(Product.sku == data["sku"], Product.barcode == data.get("barcode"))
        ).first()

        if existing_product:
            return error_response(
                message="SKU أو الباركود مستخدم مسبقاً",
                code=ErrorCodes.VAL_DUPLICATE_VALUE,
                details={
                    "sku": (
                        "SKU مستخدم مسبقاً"
                        if existing_product.sku == data["sku"]
                        else None
                    ),
                    "barcode": (
                        "الباركود مستخدم مسبقاً"
                        if existing_product.barcode == data.get("barcode")
                        else None
                    ),
                },
                status_code=400,
            )

        # التحقق من وجود الفئة والعلامة التجارية
        if data.get("category_id"):
            category = Category.query.get(data["category_id"])
            if not category:
                return error_response(
                    message="الفئة غير موجودة",
                    code=ErrorCodes.RES_NOT_FOUND,
                    status_code=400,
                )

        if data.get("brand_id"):
            brand = Brand.query.get(data["brand_id"])
            if not brand:
                return error_response(
                    message="العلامة التجارية غير موجودة",
                    code=ErrorCodes.RES_NOT_FOUND,
                    status_code=400,
                )

        # إنشاء المنتج
        product = Product(
            name=data["name"],
            name_ar=data.get("name_ar", ""),
            description=data.get("description", ""),
            description_ar=data.get("description_ar", ""),
            sku=data["sku"],
            barcode=data.get("barcode"),
            price=data["price"],
            cost=data.get("cost", 0),
            stock_quantity=data.get("stock_quantity", 0),
            reorder_level=data.get("reorder_level", 10),
            category_id=data.get("category_id"),
            brand_id=data.get("brand_id"),
            weight=data.get("weight"),
            dimensions=data.get("dimensions"),
            is_active=data.get("is_active", True),
            created_by=current_user_id,
            created_at=datetime.utcnow(),
        )

        db.session.add(product)
        db.session.flush()  # للحصول على product.id

        # إضافة حركة مخزون أولية إذا كان هناك مخزون
        if product.stock_quantity > 0:
            initial_movement = StockMovement(
                product_id=product.id,
                movement_type="initial",
                quantity=product.stock_quantity,
                reference_type="product_creation",
                reference_id=product.id,
                notes="المخزون الأولي عند إنشاء المنتج",
                created_by=current_user_id,
                created_at=datetime.utcnow(),
            )
            db.session.add(initial_movement)

        db.session.commit()

        # مسح الكاش
        cache_manager.delete_memoized("get_products")
        cache_manager.delete_memoized("get_categories")

        return success_response(
            data={"product": product.to_dict()},
            message="تم إنشاء المنتج بنجاح",
            status_code=201,
        )

    except ValidationError as e:
        return error_response(
            message="بيانات غير صحيحة",
            code=ErrorCodes.VAL_INVALID_INPUT,
            details=e.messages,
            status_code=400,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create product error: {str(e)}")
        return error_response(
            message="خطأ في إنشاء المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    """تحديث منتج موجود"""
    try:
        current_user_id = get_jwt_identity()

        product = Product.query.get(product_id)
        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        # التحقق من صحة البيانات
        data = product_update_schema.load(request.json)

        # التحقق من عدم تكرار SKU أو الباركود (باستثناء المنتج الحالي)
        if "sku" in data or "barcode" in data:
            existing_query = Product.query.filter(Product.id != product_id)

            if "sku" in data:
                existing_query = existing_query.filter(Product.sku == data["sku"])

            if "barcode" in data and data["barcode"]:
                existing_query = existing_query.filter(
                    Product.barcode == data["barcode"]
                )

            existing_product = existing_query.first()
            if existing_product:
                return error_response(
                    message="SKU أو الباركود مستخدم مسبقاً",
                    code=ErrorCodes.VAL_DUPLICATE_VALUE,
                    status_code=400,
                )

        # التحقق من وجود الفئة والعلامة التجارية
        if data.get("category_id"):
            category = Category.query.get(data["category_id"])
            if not category:
                return error_response(
                    message="الفئة غير موجودة",
                    code=ErrorCodes.RES_NOT_FOUND,
                    status_code=400,
                )

        if data.get("brand_id"):
            brand = Brand.query.get(data["brand_id"])
            if not brand:
                return error_response(
                    message="العلامة التجارية غير موجودة",
                    code=ErrorCodes.RES_NOT_FOUND,
                    status_code=400,
                )

        # حفظ الكمية القديمة لتتبع التغييرات
        old_quantity = product.stock_quantity

        # تحديث بيانات المنتج
        for field, value in data.items():
            if hasattr(product, field):
                setattr(product, field, value)

        product.updated_by = current_user_id
        product.updated_at = datetime.utcnow()

        # إضافة حركة مخزون إذا تغيرت الكمية
        if "stock_quantity" in data and data["stock_quantity"] != old_quantity:
            quantity_change = data["stock_quantity"] - old_quantity
            movement_type = (
                "adjustment_increase" if quantity_change > 0 else "adjustment_decrease"
            )

            stock_movement = StockMovement(
                product_id=product.id,
                movement_type=movement_type,
                quantity=abs(quantity_change),
                reference_type="manual_adjustment",
                reference_id=product.id,
                notes=f'تعديل يدوي للمخزون من {old_quantity} إلى {data["stock_quantity"]}',
                created_by=current_user_id,
                created_at=datetime.utcnow(),
            )
            db.session.add(stock_movement)

        db.session.commit()

        # مسح الكاش
        cache_manager.delete_memoized("get_product", product_id)
        cache_manager.delete_memoized("get_products")

        return success_response(
            data={"product": product.to_dict()},
            message="تم تحديث المنتج بنجاح",
            status_code=200,
        )

    except ValidationError as e:
        return error_response(
            message="بيانات غير صحيحة",
            code=ErrorCodes.VAL_INVALID_INPUT,
            details=e.messages,
            status_code=400,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update product error: {str(e)}")
        return error_response(
            message="خطأ في تحديث المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    """حذف منتج (حذف ناعم)"""
    try:
        current_user_id = get_jwt_identity()

        product = Product.query.get(product_id)
        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        # حذف ناعم (تعطيل المنتج بدلاً من حذفه)
        product.is_active = False
        product.deleted_by = current_user_id
        product.deleted_at = datetime.utcnow()

        db.session.commit()

        # مسح الكاش
        cache_manager.delete_memoized("get_product", product_id)
        cache_manager.delete_memoized("get_products")

        return success_response(message="تم حذف المنتج بنجاح", status_code=200)

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete product error: {str(e)}")
        return error_response(
            message="خطأ في حذف المنتج",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/<int:product_id>/images", methods=["POST"])
@jwt_required()
def upload_product_image(product_id):
    """تحميل صورة للمنتج"""
    try:
        current_user_id = get_jwt_identity()

        product = Product.query.get(product_id)
        if not product:
            return error_response(
                message="المنتج غير موجود",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        # التحقق من وجود ملف
        if "image" not in request.files:
            return error_response(
                message="لم يتم تحديد ملف",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        file = request.files["image"]
        if file.filename == "":
            return error_response(
                message="لم يتم اختيار ملف",
                code=ErrorCodes.VAL_MISSING_FIELD,
                status_code=400,
            )

        # التحقق من حجم الملف
        if len(file.read()) > MAX_FILE_SIZE:
            return error_response(
                message=f"حجم الملف كبير جداً. الحد الأقصى {MAX_FILE_SIZE // (1024 * 1024)}MB",
                code=ErrorCodes.VAL_INVALID_INPUT,
                status_code=400,
            )

        file.seek(0)  # إعادة تعيين مؤشر الملف

        # حفظ الصورة
        image_info = save_product_image(file, product_id)
        if not image_info:
            return error_response(
                message="فشل في حفظ الصورة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=500,
            )

        # حفظ معلومات الصورة في قاعدة البيانات
        product_image = ProductImage(
            product_id=product_id,
            filename=image_info["filename"],
            original_filename=file.filename,
            file_path=image_info["paths"]["original"],
            file_size=len(file.read()),
            mime_type=file.content_type,
            is_primary=len(product.images) == 0,  # أول صورة تكون أساسية
            uploaded_by=current_user_id,
            created_at=datetime.utcnow(),
        )

        db.session.add(product_image)
        db.session.commit()

        # مسح الكاش
        cache_manager.delete_memoized("get_product", product_id)

        return success_response(
            data={"image": product_image.to_dict(), "url": image_info["url"]},
            message="تم تحميل الصورة بنجاح",
            status_code=201,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Upload image error: {str(e)}")
        return error_response(
            message="خطأ في تحميل الصورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/<int:product_id>/images/<filename>")
def get_product_image(product_id, filename):
    """الحصول على صورة المنتج"""
    try:
        # التحقق من وجود المنتج والصورة
        product_image = ProductImage.query.filter_by(
            product_id=product_id, filename=filename
        ).first()

        if not product_image:
            return error_response(
                message="الصورة غير موجودة",
                code=ErrorCodes.RES_NOT_FOUND,
                status_code=404,
            )

        # تحديد حجم الصورة المطلوب
        size = request.args.get("size", "original")
        if size not in ["original", "thumbnail", "medium", "large"]:
            size = "original"

        # بناء مسار الملف
        upload_folder = os.path.join(
            current_app.config.get("UPLOAD_FOLDER", "uploads"),
            "products",
            str(product_id),
        )

        if size == "original":
            file_path = os.path.join(upload_folder, f"original_{filename}")
        else:
            file_path = os.path.join(upload_folder, f"{size}_{filename}")

        # التحقق من وجود الملف
        if not os.path.exists(file_path):
            # محاولة الحصول على الصورة الأصلية كبديل
            original_path = os.path.join(upload_folder, f"original_{filename}")
            if os.path.exists(original_path):
                file_path = original_path
            else:
                return error_response(
                    message="ملف الصورة غير موجود",
                    code=ErrorCodes.RES_NOT_FOUND,
                    status_code=404,
                )

        return send_file(file_path, mimetype=product_image.mime_type)

    except Exception as e:
        current_app.logger.error(f"Get image error: {str(e)}")
        return error_response(
            message="خطأ في جلب الصورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/categories", methods=["GET"])
@cache_manager.cached(timeout=3600)
def get_categories():
    """الحصول على قائمة الفئات"""
    try:
        categories = (
            Category.query.filter_by(is_active=True).order_by(Category.name).all()
        )

        categories_data = []
        for category in categories:
            category_dict = category.to_dict()
            # إضافة عدد المنتجات في الفئة
            category_dict["products_count"] = Product.query.filter_by(
                category_id=category.id, is_active=True
            ).count()
            categories_data.append(category_dict)

        return success_response(
            data={"categories": categories_data},
            message="تم جلب الفئات بنجاح",
            status_code=200,
        )

    except Exception as e:
        current_app.logger.error(f"Get categories error: {str(e)}")
        return error_response(
            message="خطأ في جلب الفئات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/brands", methods=["GET"])
@cache_manager.cached(timeout=3600)
def get_brands():
    """الحصول على قائمة العلامات التجارية"""
    try:
        brands = Brand.query.filter_by(is_active=True).order_by(Brand.name).all()

        brands_data = []
        for brand in brands:
            brand_dict = brand.to_dict()
            # إضافة عدد المنتجات للعلامة التجارية
            brand_dict["products_count"] = Product.query.filter_by(
                brand_id=brand.id, is_active=True
            ).count()
            brands_data.append(brand_dict)

        return success_response(
            data={"brands": brands_data},
            message="تم جلب العلامات التجارية بنجاح",
            status_code=200,
        )

    except Exception as e:
        current_app.logger.error(f"Get brands error: {str(e)}")
        return error_response(
            message="خطأ في جلب العلامات التجارية",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@products_bp.route("/stats", methods=["GET"])
@jwt_required()
@cache_manager.cached(timeout=900)
def get_products_stats():
    """الحصول على إحصائيات المنتجات"""
    try:
        # إحصائيات عامة
        total_products = Product.query.filter_by(is_active=True).count()
        total_categories = Category.query.filter_by(is_active=True).count()
        total_brands = Brand.query.filter_by(is_active=True).count()

        # إحصائيات المخزون
        in_stock = Product.query.filter(
            Product.is_active, Product.stock_quantity > 0
        ).count()

        out_of_stock = Product.query.filter(
            Product.is_active, Product.stock_quantity <= 0
        ).count()

        low_stock = Product.query.filter(
            Product.is_active,
            Product.stock_quantity <= Product.reorder_level,
            Product.stock_quantity > 0,
        ).count()

        # إجمالي قيمة المخزون
        total_stock_value = (
            db.session.query(func.sum(Product.price * Product.stock_quantity))
            .filter(Product.is_active)
            .scalar()
            or 0
        )

        # أكثر الفئات مبيعاً (بناءً على عدد المنتجات)
        top_categories = (
            db.session.query(
                Category.name,
                Category.name_ar,
                func.count(Product.id).label("products_count"),
            )
            .join(Product)
            .filter(Product.is_active, Category.is_active)
            .group_by(Category.id)
            .order_by(desc("products_count"))
            .limit(5)
            .all()
        )

        # أكثر العلامات التجارية مبيعاً
        top_brands = (
            db.session.query(
                Brand.name,
                Brand.name_ar,
                func.count(Product.id).label("products_count"),
            )
            .join(Product)
            .filter(Product.is_active, Brand.is_active)
            .group_by(Brand.id)
            .order_by(desc("products_count"))
            .limit(5)
            .all()
        )

        return success_response(
            data={
                "general": {
                    "total_products": total_products,
                    "total_categories": total_categories,
                    "total_brands": total_brands,
                },
                "stock": {
                    "in_stock": in_stock,
                    "out_of_stock": out_of_stock,
                    "low_stock": low_stock,
                    "total_value": float(total_stock_value),
                },
                "top_categories": [
                    {
                        "name": cat.name,
                        "name_ar": cat.name_ar,
                        "products_count": cat.products_count,
                    }
                    for cat in top_categories
                ],
                "top_brands": [
                    {
                        "name": brand.name,
                        "name_ar": brand.name_ar,
                        "products_count": brand.products_count,
                    }
                    for brand in top_brands
                ],
            },
            message="تم جلب الإحصائيات بنجاح",
            status_code=200,
        )

    except Exception as e:
        current_app.logger.error(f"Get stats error: {str(e)}")
        return error_response(
            message="خطأ في جلب الإحصائيات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


# معالج أخطاء Blueprint
@products_bp.errorhandler(413)
def file_too_large(e):
    return error_response(
        message="حجم الملف كبير جداً", code=ErrorCodes.VAL_INVALID_INPUT, status_code=413
    )


@products_bp.errorhandler(415)
def unsupported_media_type(e):
    return error_response(
        message="نوع الملف غير مدعوم",
        code=ErrorCodes.VAL_INVALID_INPUT,
        status_code=415,
    )
