# FILE: backend/src/routes/partners_unified.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مسارات العملاء والموردين الموحدة
Unified Customers & Suppliers Routes
"""

from flask import Blueprint, request, jsonify, g

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.database import db
from datetime import datetime
import logging

# P0.19: Import validation schemas
try:
    from src.utils.validation import validate_json, CustomerSchema, SupplierSchema
except ImportError:
    CustomerSchema = None
    SupplierSchema = None

    def validate_json(schema):
        def decorator(f):
            return f

        return decorator


# P0.9: Import permission system
try:
    from src.permissions import require_permission, Permissions
except ImportError:

    def require_permission(*args, **kwargs):
        def decorator(f):
            return f

        return decorator

    class Permissions:
        CUSTOMER_VIEW = "customer_view"
        CUSTOMER_ADD = "customer_add"
        CUSTOMER_EDIT = "customer_edit"
        CUSTOMER_DELETE = "customer_delete"
        SUPPLIER_VIEW = "supplier_view"
        SUPPLIER_ADD = "supplier_add"
        SUPPLIER_EDIT = "supplier_edit"
        SUPPLIER_DELETE = "supplier_delete"


# استيراد النماذج
try:
    from src.models.customer import Customer, CustomerCategory

    CUSTOMER_MODEL = True
except ImportError:
    Customer = None
    CustomerCategory = None
    CUSTOMER_MODEL = False

try:
    from src.models.supplier import Supplier

    SUPPLIER_MODEL = True
except ImportError:
    Supplier = None
    SUPPLIER_MODEL = False

# استيراد decorators
try:
    from src.routes.auth_unified import token_required, admin_required, log_activity
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
partners_unified_bp = Blueprint("partners_unified", __name__)


# ============================================================================
# مسارات العملاء
# ============================================================================


@partners_unified_bp.route("/api/customers", methods=["GET"])
@token_required
@require_permission(Permissions.CUSTOMER_VIEW)
def get_customers():
    """P0.9: الحصول على قائمة العملاء"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        search = request.args.get("search", "")

        query = Customer.query

        if search:
            search_filter = db.or_(Customer.name.ilike(f"%{search}%"))
            if hasattr(Customer, "email"):
                search_filter = db.or_(
                    search_filter, Customer.email.ilike(f"%{search}%")
                )
            if hasattr(Customer, "phone"):
                search_filter = db.or_(
                    search_filter, Customer.phone.ilike(f"%{search}%")
                )
            query = query.filter(search_filter)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "customers": [c.to_dict() for c in pagination.items],
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
        logger.error(f"خطأ في الحصول على العملاء: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/customers/<int:customer_id>", methods=["GET"])
@token_required
@require_permission(Permissions.CUSTOMER_VIEW)
def get_customer(customer_id):
    """P0.9: الحصول على عميل محدد"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        customer = Customer.query.get(customer_id)
        if not customer:
            return error_response(
                message="العميل غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        return success_response(
            data=customer.to_dict(), message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/customers", methods=["POST"])
@token_required
@require_permission(Permissions.CUSTOMER_ADD)
@validate_json(CustomerSchema)
def create_customer():
    """P0.9+P0.19: إنشاء عميل جديد مع التحقق من صحة البيانات والصلاحيات"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # Use validated data from decorator if available
        data = getattr(g, "validated_data", None) or request.get_json()
        if not data or not data.get("name"):
            return error_response(
                message="اسم العميل مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من تكرار البريد
        if data.get("email") and hasattr(Customer, "email"):
            existing = Customer.query.filter_by(email=data["email"]).first()
            if existing:
                return error_response(
                    message="البريد موجود",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        customer_data = {"name": data["name"], "is_active": data.get("is_active", True)}

        optional_fields = [
            "customer_code",
            "email",
            "phone",
            "mobile",
            "address",
            "city",
            "country",
            "postal_code",
            "company_name",
            "tax_number",
            "credit_limit",
            "payment_terms",
            "currency",
            "discount_rate",
            "notes",
            "tags",
        ]

        for field in optional_fields:
            if field in data and hasattr(Customer, field):
                customer_data[field] = data[field]

        if "category" in data and CustomerCategory:
            try:
                customer_data["category"] = CustomerCategory[data["category"].upper()]
            except KeyError:
                pass

        customer = Customer(**customer_data)
        db.session.add(customer)
        db.session.commit()

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "create",
                {"entity": "customer", "entity_id": customer.id, "name": customer.name},
            )

        return success_response(
            data=customer.to_dict(), message="تم إنشاء العميل بنجاح", status_code=201
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/customers/<int:customer_id>", methods=["PUT"])
@token_required
@require_permission(Permissions.CUSTOMER_EDIT)
def update_customer(customer_id):
    """P0.9: تحديث عميل"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        customer = Customer.query.get(customer_id)
        if not customer:
            return error_response(
                message="العميل غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        data = request.get_json()

        # التحقق من تكرار البريد
        if data.get("email") and hasattr(Customer, "email"):
            existing = Customer.query.filter(
                Customer.email == data["email"], Customer.id != customer_id
            ).first()
            if existing:
                return error_response(
                    message="البريد موجود",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        updatable_fields = [
            "name",
            "customer_code",
            "email",
            "phone",
            "mobile",
            "address",
            "city",
            "country",
            "postal_code",
            "company_name",
            "tax_number",
            "credit_limit",
            "payment_terms",
            "currency",
            "discount_rate",
            "notes",
            "tags",
            "is_active",
        ]

        for field in updatable_fields:
            if field in data and hasattr(Customer, field):
                setattr(customer, field, data[field])

        if "category" in data and CustomerCategory:
            try:
                customer.category = CustomerCategory[data["category"].upper()]
            except KeyError:
                pass

        if hasattr(Customer, "updated_at"):
            customer.updated_at = datetime.utcnow()

        db.session.commit()

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "update",
                {"entity": "customer", "entity_id": customer.id, "name": customer.name},
            )

        return success_response(
            data=customer.to_dict(), message="تم تحديث العميل بنجاح", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/customers/<int:customer_id>", methods=["DELETE"])
@token_required
@require_permission(Permissions.CUSTOMER_DELETE)
def delete_customer(customer_id):
    """P0.9: حذف عميل"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        customer = Customer.query.get(customer_id)
        if not customer:
            return error_response(
                message="العميل غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        name = customer.name
        db.session.delete(customer)
        db.session.commit()

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "delete",
                {"entity": "customer", "entity_id": customer_id, "name": name},
            )

        return success_response(message="تم حذف العميل بنجاح", status_code=200)
    except Exception as e:
        logger.error(f"خطأ: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


# ============================================================================
# مسارات الموردين
# ============================================================================


@partners_unified_bp.route("/api/suppliers", methods=["GET"])
@token_required
@require_permission(Permissions.SUPPLIER_VIEW)
def get_suppliers():
    """P0.9: الحصول على قائمة الموردين"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        search = request.args.get("search", "")

        query = Supplier.query

        if search:
            search_filter = db.or_(Supplier.name.ilike(f"%{search}%"))
            if hasattr(Supplier, "email"):
                search_filter = db.or_(
                    search_filter, Supplier.email.ilike(f"%{search}%")
                )
            if hasattr(Supplier, "phone"):
                search_filter = db.or_(
                    search_filter, Supplier.phone.ilike(f"%{search}%")
                )
            query = query.filter(search_filter)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "suppliers": [s.to_dict() for s in pagination.items],
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
        logger.error(f"خطأ في الحصول على الموردين: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers/<int:supplier_id>", methods=["GET"])
@token_required
@require_permission(Permissions.SUPPLIER_VIEW)
def get_supplier(supplier_id):
    """P0.9: الحصول على مورد محدد"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            return error_response(
                message="المورد غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        return success_response(
            data=supplier.to_dict(), message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers", methods=["POST"])
@token_required
@require_permission(Permissions.SUPPLIER_ADD)
@validate_json(SupplierSchema)
def create_supplier():
    """P0.9+P0.19: إنشاء مورد جديد مع التحقق من صحة البيانات والصلاحيات"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # Use validated data from decorator if available
        data = getattr(g, "validated_data", None) or request.get_json()
        if not data or not data.get("name"):
            return error_response(
                message="اسم المورد مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من تكرار البريد
        if data.get("email") and hasattr(Supplier, "email"):
            existing = Supplier.query.filter_by(email=data["email"]).first()
            if existing:
                return error_response(
                    message="البريد موجود",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        supplier_data = {"name": data["name"], "is_active": data.get("is_active", True)}

        optional_fields = [
            "company_type",
            "email",
            "phone",
            "mobile",
            "website",
            "address",
            "tax_number",
            "payment_terms",
            "preferred_payment_method",
            "currency",
            "language",
            "notes",
        ]

        for field in optional_fields:
            if field in data and hasattr(Supplier, field):
                supplier_data[field] = data[field]

        supplier = Supplier(**supplier_data)
        db.session.add(supplier)
        db.session.commit()

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "create",
                {"entity": "supplier", "entity_id": supplier.id, "name": supplier.name},
            )

        return success_response(
            data=supplier.to_dict(), message="تم إنشاء المورد بنجاح", status_code=201
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers/<int:supplier_id>", methods=["PUT"])
@token_required
def update_supplier(supplier_id):
    """تحديث مورد"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            return error_response(
                message="المورد غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        data = request.get_json()

        # التحقق من تكرار البريد
        if data.get("email") and hasattr(Supplier, "email"):
            existing = Supplier.query.filter(
                Supplier.email == data["email"], Supplier.id != supplier_id
            ).first()
            if existing:
                return error_response(
                    message="البريد موجود",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )

        updatable_fields = [
            "name",
            "company_type",
            "email",
            "phone",
            "mobile",
            "website",
            "address",
            "tax_number",
            "payment_terms",
            "preferred_payment_method",
            "currency",
            "language",
            "notes",
            "is_active",
        ]

        for field in updatable_fields:
            if field in data and hasattr(Supplier, field):
                setattr(supplier, field, data[field])

        if hasattr(Supplier, "updated_at"):
            supplier.updated_at = datetime.utcnow()

        db.session.commit()

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "update",
                {"entity": "supplier", "entity_id": supplier.id, "name": supplier.name},
            )

        return success_response(
            data=supplier.to_dict(), message="تم تحديث المورد بنجاح", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers/<int:supplier_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_supplier(supplier_id):
    """حذف مورد"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            return error_response(
                message="المورد غير موجود",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        name = supplier.name
        db.session.delete(supplier)
        db.session.commit()

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "delete",
                {"entity": "supplier", "entity_id": supplier_id, "name": name},
            )

        return success_response(message="تم حذف المورد بنجاح", status_code=200)
    except Exception as e:
        logger.error(f"خطأ: {e}")
        db.session.rollback()
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


# ============================================================================
# مسارات إضافية
# ============================================================================


@partners_unified_bp.route("/api/customers/stats", methods=["GET"])
@token_required
def get_customers_stats():
    """إحصائيات العملاء"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        total = Customer.query.count()
        active = Customer.query.filter_by(is_active=True).count()
        inactive = total - active

        stats = {
            "total_customers": total,
            "active_customers": active,
            "inactive_customers": inactive,
        }

        # إحصائيات حسب الفئة
        if hasattr(Customer, "category") and CustomerCategory:
            by_category = {}
            for cat in CustomerCategory:
                count = Customer.query.filter_by(category=cat).count()
                by_category[cat.value] = count
            stats["by_category"] = by_category

        return success_response(data=stats, message="Success", status_code=200)
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers/stats", methods=["GET"])
@token_required
def get_suppliers_stats():
    """إحصائيات الموردين"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        total = Supplier.query.count()
        active = Supplier.query.filter_by(is_active=True).count()
        inactive = total - active

        stats = {
            "total_suppliers": total,
            "active_suppliers": active,
            "inactive_suppliers": inactive,
        }

        return success_response(data=stats, message="Success", status_code=200)
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/customers/search", methods=["GET"])
@token_required
def search_customers():
    """البحث السريع في العملاء"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
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

        search_filter = db.or_(Customer.name.ilike(f"%{query_text}%"))
        if hasattr(Customer, "email"):
            search_filter = db.or_(
                search_filter, Customer.email.ilike(f"%{query_text}%")
            )
        if hasattr(Customer, "phone"):
            search_filter = db.or_(
                search_filter, Customer.phone.ilike(f"%{query_text}%")
            )

        customers = Customer.query.filter(search_filter).limit(limit).all()

        return success_response(
            data={"total": len(customers)}, message="Success", status_code=200
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers/search", methods=["GET"])
@token_required
def search_suppliers():
    """البحث السريع في الموردين"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
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

        search_filter = db.or_(Supplier.name.ilike(f"%{query_text}%"))
        if hasattr(Supplier, "email"):
            search_filter = db.or_(
                search_filter, Supplier.email.ilike(f"%{query_text}%")
            )
        if hasattr(Supplier, "phone"):
            search_filter = db.or_(
                search_filter, Supplier.phone.ilike(f"%{query_text}%")
            )

        suppliers = Supplier.query.filter(search_filter).limit(limit).all()

        return (
            success_response(
                data={"total": len(suppliers)}, message="Success", status_code=200
            ),
            200,
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/customers/export", methods=["GET"])
@token_required
def export_customers():
    """تصدير العملاء"""
    try:
        if not Customer:
            return error_response(
                message="نموذج العملاء غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        export_format = request.args.get("format", "json").lower()
        customers = Customer.query.all()
        customers_data = [c.to_dict() for c in customers]

        if export_format == "csv":
            return error_response(
                message="تصدير CSV غير مدعوم حالياً",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "export",
                {
                    "entity": "customers",
                    "format": export_format,
                    "count": len(customers_data),
                },
            )

        return success_response(
            data={
                "customers": customers_data,
                "total": len(customers_data),
                "format": export_format,
            },
            message="تم تصدير العملاء بنجاح / Customers exported successfully",
            status_code=200,
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )


@partners_unified_bp.route("/api/suppliers/export", methods=["GET"])
@token_required
def export_suppliers():
    """تصدير الموردين"""
    try:
        if not Supplier:
            return error_response(
                message="نموذج الموردين غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        export_format = request.args.get("format", "json").lower()
        suppliers = Supplier.query.all()
        suppliers_data = [s.to_dict() for s in suppliers]

        if export_format == "csv":
            return error_response(
                message="تصدير CSV غير مدعوم حالياً",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        if hasattr(request, "current_user_id"):
            log_activity(
                request.current_user_id,
                "export",
                {
                    "entity": "suppliers",
                    "format": export_format,
                    "count": len(suppliers_data),
                },
            )

        return success_response(
            data={
                "suppliers": suppliers_data,
                "total": len(suppliers_data),
                "format": export_format,
            },
            message="تم تصدير الموردين بنجاح / Suppliers exported successfully",
            status_code=200,
        )
    except Exception as e:
        logger.error(f"خطأ: {e}")
        return error_response(
            message="حدث خطأ", code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=500
        )
