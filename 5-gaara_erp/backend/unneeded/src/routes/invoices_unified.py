# FILE: backend/src/routes/invoices_unified.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مسارات الفواتير الموحدة
Unified Invoices Routes

يدمج جميع مسارات الفواتير، المبيعات، والمشتريات في ملف واحد
Merges all invoice, sales, and purchase routes into one file
"""

import logging
from datetime import date, datetime
from decimal import Decimal

from flask import Blueprint, jsonify, request, session

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from sqlalchemy import func, or_

# استيراد النماذج الموحدة | Import unified models
try:
    from src.database import db
    from src.models.invoice_unified import (
        Invoice,
        InvoiceItem,
        InvoicePayment,
        InvoiceStatus,
        InvoiceType,
        PaymentStatus,
    )
    from src.models.product_unified import Product
    from src.models.user import User
    from src.models.warehouse_unified import Warehouse
except ImportError:
    # Disable legacy fallback to avoid mixed model registries and mapper conflicts
    Invoice = None
    InvoiceItem = None
    InvoicePayment = None
    InvoiceType = None
    InvoiceStatus = None
    PaymentStatus = None
    Product = None
    Warehouse = None
    User = None
    db = None

# استيراد النماذج المساعدة | Import supporting models
try:
    from src.models.customer import Customer
except ImportError:
    Customer = None

try:
    from src.models.supplier import Supplier
except ImportError:
    Supplier = None

# استيراد decorators الأمان | Import security decorators
try:
    from src.auth import admin_required, token_required
except ImportError:
    # Fallback decorators
    def token_required(f):
        return f

    def admin_required(f):
        return f


# استيراد دوال المساعدة | Import helper functions
try:
    from src.logging_system import log_activity
except ImportError:

    def log_activity(user_id, action, details):
        pass


# إعداد Logger
logger = logging.getLogger(__name__)

# إنشاء Blueprint
invoices_unified_bp = Blueprint("invoices_unified", __name__)


# ==================== دوال مساعدة | Helper Functions ====================


def calculate_invoice_totals(items_data):
    """حساب إجماليات الفاتورة"""
    subtotal = Decimal("0.00")

    for item in items_data:
        quantity = Decimal(str(item.get("quantity", 0)))
        price = Decimal(str(item.get("price", 0)))
        discount = Decimal(str(item.get("discount", 0)))

        item_total = (quantity * price) - discount
        subtotal += item_total

    return subtotal


def generate_invoice_number(invoice_type):
    """توليد رقم فاتورة تلقائي"""
    try:
        prefix = {
            "sales": "SAL",
            "purchase": "PUR",
            "sales_return": "SRT",
            "purchase_return": "PRT",
        }.get(invoice_type, "INV")

        # الحصول على آخر رقم فاتورة
        last_invoice = (
            Invoice.query.filter(Invoice.invoice_number.like(f"{prefix}%"))
            .order_by(Invoice.id.desc())
            .first()
        )

        if last_invoice:
            try:
                last_number = int(last_invoice.invoice_number.split("-")[1])
                new_number = last_number + 1
            except Exception:
                new_number = 1
        else:
            new_number = 1

        return f"{prefix}-{new_number:06d}"
    except Exception as e:
        logger.error(f"خطأ في توليد رقم الفاتورة: {e}")
        return f'INV-{datetime.now().strftime("%Y%m%d%H%M%S")}'


# ==================== مسارات الفواتير | Invoice Routes ====================


@invoices_unified_bp.route("/api/invoices", methods=["GET"])
@token_required
def get_invoices():
    """
    الحصول على قائمة الفواتير
    Get list of invoices

    Query Parameters:
        page (int): رقم الصفحة
        per_page (int): عدد العناصر في الصفحة
        search (str): البحث في رقم الفاتورة
        invoice_type (str): نوع الفاتورة (sales, purchase, sales_return, purchase_return)
        status (str): حالة الفاتورة
        customer_id (int): معرف العميل
        supplier_id (int): معرف المورد
        date_from (str): من تاريخ (YYYY-MM-DD)
        date_to (str): إلى تاريخ (YYYY-MM-DD)
        sort_by (str): الترتيب حسب (invoice_date, total_amount, etc.)
        order (str): اتجاه الترتيب (asc, desc)
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # معاملات الصفحة | Pagination parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        # معاملات البحث | Search parameters
        search = request.args.get("search", "")
        invoice_type = request.args.get("invoice_type", "")
        status = request.args.get("status", "")
        customer_id = request.args.get("customer_id", type=int)
        supplier_id = request.args.get("supplier_id", type=int)
        date_from = request.args.get("date_from", "")
        date_to = request.args.get("date_to", "")

        # معاملات الترتيب | Sort parameters
        sort_by = request.args.get("sort_by", "invoice_date")
        order = request.args.get("order", "desc")

        # بناء الاستعلام | Build query
        query = Invoice.query

        # البحث | Search
        if search:
            search_filter = or_(Invoice.invoice_number.ilike(f"%{search}%"))
            query = query.filter(search_filter)

        # التصفية حسب النوع | Filter by type
        if invoice_type:
            if InvoiceType:
                try:
                    type_enum = InvoiceType[invoice_type.upper()]
                    query = query.filter(Invoice.invoice_type == type_enum)
                except Exception:
                    query = query.filter(Invoice.invoice_type == invoice_type)
            else:
                query = query.filter(Invoice.invoice_type == invoice_type)

        # التصفية حسب الحالة | Filter by status
        if status:
            if InvoiceStatus:
                try:
                    status_enum = InvoiceStatus[status.upper()]
                    query = query.filter(Invoice.status == status_enum)
                except Exception:
                    query = query.filter(Invoice.status == status)
            else:
                query = query.filter(Invoice.status == status)

        # التصفية حسب العميل | Filter by customer
        if customer_id:
            query = query.filter(Invoice.customer_id == customer_id)

        # التصفية حسب المورد | Filter by supplier
        if supplier_id:
            query = query.filter(Invoice.supplier_id == supplier_id)

        # التصفية حسب التاريخ | Filter by date
        if date_from:
            try:
                from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
                query = query.filter(Invoice.invoice_date >= from_date)
            except Exception:
                pass

        if date_to:
            try:
                to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
                query = query.filter(Invoice.invoice_date <= to_date)
            except Exception:
                pass

        # الترتيب | Sorting
        if hasattr(Invoice, sort_by):
            sort_column = getattr(Invoice, sort_by)
            if order == "asc":
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(Invoice.invoice_date.desc())

        # التقسيم إلى صفحات | Pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        # تحويل إلى قاموس | Convert to dict
        invoices_data = []
        for invoice in pagination.items:
            invoice_dict = {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "invoice_type": (
                    invoice.invoice_type.value
                    if hasattr(invoice.invoice_type, "value")
                    else invoice.invoice_type
                ),
                "invoice_date": (
                    invoice.invoice_date.isoformat() if invoice.invoice_date else None
                ),
                "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                "customer_id": invoice.customer_id,
                "supplier_id": invoice.supplier_id,
                "warehouse_id": invoice.warehouse_id,
                "subtotal": float(invoice.subtotal) if invoice.subtotal else 0.00,
                "tax_amount": float(invoice.tax_amount) if invoice.tax_amount else 0.00,
                "discount_amount": (
                    float(invoice.discount_amount) if invoice.discount_amount else 0.00
                ),
                "total_amount": (
                    float(invoice.total_amount) if invoice.total_amount else 0.00
                ),
                "paid_amount": (
                    float(invoice.paid_amount) if invoice.paid_amount else 0.00
                ),
                "remaining_amount": (
                    float(invoice.remaining_amount)
                    if invoice.remaining_amount
                    else 0.00
                ),
                "status": (
                    invoice.status.value
                    if hasattr(invoice.status, "value")
                    else invoice.status
                ),
                "payment_status": (
                    invoice.payment_status.value
                    if hasattr(invoice.payment_status, "value")
                    else getattr(invoice, "payment_status", None)
                ),
                "notes": invoice.notes,
                "created_at": (
                    invoice.created_at.isoformat() if invoice.created_at else None
                ),
            }

            # إضافة معلومات العميل | Add customer info
            if invoice.customer_id and Customer:
                customer = Customer.query.get(invoice.customer_id)
                if customer:
                    invoice_dict["customer_name"] = customer.name

            # إضافة معلومات المورد | Add supplier info
            if invoice.supplier_id and Supplier:
                supplier = Supplier.query.get(invoice.supplier_id)
                if supplier:
                    invoice_dict["supplier_name"] = supplier.name

            invoices_data.append(invoice_dict)

        return (
            jsonify(
                {
                    "success": True,
                    "data": invoices_data,
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": pagination.total,
                        "pages": pagination.pages,
                        "has_next": pagination.has_next,
                        "has_prev": pagination.has_prev,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على الفواتير: {e}")
        return error_response(
            message="حدث خطأ في الحصول على الفواتير",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/<int:invoice_id>", methods=["GET"])
@token_required
def get_invoice(invoice_id):
    """
    الحصول على فاتورة محددة
    Get specific invoice
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return error_response(
                message="الفاتورة غير موجودة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # تحويل إلى قاموس | Convert to dict
        invoice_dict = {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "invoice_type": (
                invoice.invoice_type.value
                if hasattr(invoice.invoice_type, "value")
                else invoice.invoice_type
            ),
            "invoice_date": (
                invoice.invoice_date.isoformat() if invoice.invoice_date else None
            ),
            "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
            "delivery_date": (
                invoice.delivery_date.isoformat()
                if hasattr(invoice, "delivery_date") and invoice.delivery_date
                else None
            ),
            "customer_id": invoice.customer_id,
            "supplier_id": invoice.supplier_id,
            "warehouse_id": invoice.warehouse_id,
            "created_by": invoice.created_by,
            "subtotal": float(invoice.subtotal) if invoice.subtotal else 0.00,
            "tax_amount": float(invoice.tax_amount) if invoice.tax_amount else 0.00,
            "tax_rate": (
                float(invoice.tax_rate)
                if hasattr(invoice, "tax_rate") and invoice.tax_rate
                else 0.00
            ),
            "discount_amount": (
                float(invoice.discount_amount) if invoice.discount_amount else 0.00
            ),
            "discount_type": (
                invoice.discount_type if hasattr(invoice, "discount_type") else "fixed"
            ),
            "discount_value": (
                float(invoice.discount_value)
                if hasattr(invoice, "discount_value") and invoice.discount_value
                else 0.00
            ),
            "shipping_cost": (
                float(invoice.shipping_cost)
                if hasattr(invoice, "shipping_cost") and invoice.shipping_cost
                else 0.00
            ),
            "other_charges": (
                float(invoice.other_charges)
                if hasattr(invoice, "other_charges") and invoice.other_charges
                else 0.00
            ),
            "total_amount": (
                float(invoice.total_amount) if invoice.total_amount else 0.00
            ),
            "paid_amount": float(invoice.paid_amount) if invoice.paid_amount else 0.00,
            "remaining_amount": (
                float(invoice.remaining_amount) if invoice.remaining_amount else 0.00
            ),
            "currency": invoice.currency if hasattr(invoice, "currency") else "USD",
            "exchange_rate": (
                float(invoice.exchange_rate)
                if hasattr(invoice, "exchange_rate") and invoice.exchange_rate
                else 1.0
            ),
            "status": (
                invoice.status.value
                if hasattr(invoice.status, "value")
                else invoice.status
            ),
            "payment_status": (
                invoice.payment_status.value
                if hasattr(invoice.payment_status, "value")
                else getattr(invoice, "payment_status", None)
            ),
            "notes": invoice.notes,
            "terms_conditions": (
                invoice.terms_conditions
                if hasattr(invoice, "terms_conditions")
                else None
            ),
            "created_at": (
                invoice.created_at.isoformat() if invoice.created_at else None
            ),
            "updated_at": (
                invoice.updated_at.isoformat() if invoice.updated_at else None
            ),
        }

        # إضافة معلومات العميل | Add customer info
        if invoice.customer_id and Customer:
            customer = Customer.query.get(invoice.customer_id)
            if customer:
                invoice_dict["customer"] = {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email if hasattr(customer, "email") else None,
                    "phone": customer.phone if hasattr(customer, "phone") else None,
                }

        # إضافة معلومات المورد | Add supplier info
        if invoice.supplier_id and Supplier:
            supplier = Supplier.query.get(invoice.supplier_id)
            if supplier:
                invoice_dict["supplier"] = {
                    "id": supplier.id,
                    "name": supplier.name,
                    "email": supplier.email if hasattr(supplier, "email") else None,
                    "phone": supplier.phone if hasattr(supplier, "phone") else None,
                }

        # إضافة معلومات المستودع | Add warehouse info
        if invoice.warehouse_id and Warehouse:
            warehouse = Warehouse.query.get(invoice.warehouse_id)
            if warehouse:
                invoice_dict["warehouse"] = {
                    "id": warehouse.id,
                    "name": warehouse.name,
                }

        # إضافة العناصر | Add items
        if InvoiceItem:
            items = InvoiceItem.query.filter_by(invoice_id=invoice.id).all()
            invoice_dict["items"] = []
            for item in items:
                item_dict = {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": float(item.quantity) if item.quantity else 0,
                    "price": float(item.price) if item.price else 0.00,
                    "discount": (
                        float(item.discount)
                        if hasattr(item, "discount") and item.discount
                        else 0.00
                    ),
                    "tax": (
                        float(item.tax) if hasattr(item, "tax") and item.tax else 0.00
                    ),
                    "total": float(item.total) if item.total else 0.00,
                    "notes": item.notes if hasattr(item, "notes") else None,
                }

                # إضافة معلومات المنتج | Add product info
                if item.product_id and Product:
                    product = Product.query.get(item.product_id)
                    if product:
                        item_dict["product"] = {
                            "id": product.id,
                            "name": product.name,
                            "sku": product.sku if hasattr(product, "sku") else None,
                            "barcode": (
                                product.barcode if hasattr(product, "barcode") else None
                            ),
                        }

                invoice_dict["items"].append(item_dict)

        # إضافة الدفعات | Add payments
        if InvoicePayment:
            payments = InvoicePayment.query.filter_by(invoice_id=invoice.id).all()
            invoice_dict["payments"] = []
            for payment in payments:
                payment_dict = {
                    "id": payment.id,
                    "amount": float(payment.amount) if payment.amount else 0.00,
                    "payment_date": (
                        payment.payment_date.isoformat()
                        if payment.payment_date
                        else None
                    ),
                    "payment_method": (
                        payment.payment_method
                        if hasattr(payment, "payment_method")
                        else None
                    ),
                    "reference": (
                        payment.reference if hasattr(payment, "reference") else None
                    ),
                    "notes": payment.notes if hasattr(payment, "notes") else None,
                    "created_at": (
                        payment.created_at.isoformat() if payment.created_at else None
                    ),
                }
                invoice_dict["payments"].append(payment_dict)

        return (
            success_response(data=invoice_dict, message="Success", status_code=200),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على الفاتورة: {e}")
        return error_response(
            message="حدث خطأ في الحصول على الفاتورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices", methods=["POST"])
@token_required
def create_invoice():
    """
    إنشاء فاتورة جديدة
    Create new invoice

    Request Body:
        invoice_type (str): نوع الفاتورة (sales, purchase, sales_return, purchase_return)
        invoice_date (str): تاريخ الفاتورة (YYYY-MM-DD)
        due_date (str): تاريخ الاستحقاق (YYYY-MM-DD)
        customer_id (int): معرف العميل (للمبيعات)
        supplier_id (int): معرف المورد (للمشتريات)
        warehouse_id (int): معرف المستودع
        items (list): قائمة العناصر
        tax_rate (float): نسبة الضريبة
        discount_type (str): نوع الخصم (fixed, percentage)
        discount_value (float): قيمة الخصم
        shipping_cost (float): تكلفة الشحن
        notes (str): ملاحظات
    """
    try:
        if not Invoice or not InvoiceItem:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        data = request.get_json()

        # التحقق من البيانات المطلوبة | Validate required data
        if not data.get("invoice_type"):
            return error_response(
                message="نوع الفاتورة مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        if not data.get("items") or len(data["items"]) == 0:
            return error_response(
                message="يجب إضافة عنصر واحد على الأقل",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # التحقق من العميل أو المورد | Validate customer or supplier
        invoice_type = data["invoice_type"]
        if invoice_type in ["sales", "sales_return"]:
            if not data.get("customer_id"):
                return error_response(
                    message="معرف العميل مطلوب لفواتير المبيعات",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )
            if Customer:
                customer = Customer.query.get(data["customer_id"])
                if not customer:
                    return error_response(
                        message="العميل غير موجود",
                        code=ErrorCodes.SYS_INTERNAL_ERROR,
                        status_code=404,
                    )

        elif invoice_type in ["purchase", "purchase_return"]:
            if not data.get("supplier_id"):
                return error_response(
                    message="معرف المورد مطلوب لفواتير المشتريات",
                    code=ErrorCodes.SYS_INTERNAL_ERROR,
                    status_code=400,
                )
            if Supplier:
                supplier = Supplier.query.get(data["supplier_id"])
                if not supplier:
                    return error_response(
                        message="المورد غير موجود",
                        code=ErrorCodes.SYS_INTERNAL_ERROR,
                        status_code=404,
                    )

        # حساب الإجماليات | Calculate totals
        subtotal = calculate_invoice_totals(data["items"])

        # حساب الخصم | Calculate discount
        discount_amount = Decimal("0.00")
        if data.get("discount_value"):
            discount_value = Decimal(str(data["discount_value"]))
            if data.get("discount_type") == "percentage":
                discount_amount = (subtotal * discount_value) / Decimal("100")
            else:
                discount_amount = discount_value

        # حساب الضريبة | Calculate tax
        tax_amount = Decimal("0.00")
        if data.get("tax_rate"):
            tax_rate = Decimal(str(data["tax_rate"]))
            taxable_amount = subtotal - discount_amount
            tax_amount = (taxable_amount * tax_rate) / Decimal("100")

        # حساب الإجمالي | Calculate total
        shipping_cost = Decimal(str(data.get("shipping_cost", 0)))
        other_charges = Decimal(str(data.get("other_charges", 0)))
        total_amount = (
            subtotal - discount_amount + tax_amount + shipping_cost + other_charges
        )

        # توليد رقم الفاتورة | Generate invoice number
        invoice_number = data.get("invoice_number")
        if not invoice_number:
            invoice_number = generate_invoice_number(invoice_type)

        # التحقق من عدم تكرار رقم الفاتورة | Check for duplicate invoice number
        existing = Invoice.query.filter_by(invoice_number=invoice_number).first()
        if existing:
            return error_response(
                message="رقم الفاتورة موجود بالفعل",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # إنشاء الفاتورة | Create invoice
        invoice = Invoice()
        invoice.invoice_number = invoice_number

        # تعيين نوع الفاتورة | Set invoice type
        if InvoiceType:
            try:
                invoice.invoice_type = InvoiceType[invoice_type.upper()]
            except Exception:
                invoice.invoice_type = invoice_type
        else:
            invoice.invoice_type = invoice_type

        # التواريخ | Dates
        if data.get("invoice_date"):
            try:
                invoice.invoice_date = datetime.strptime(
                    data["invoice_date"], "%Y-%m-%d"
                ).date()
            except Exception:
                invoice.invoice_date = date.today()
        else:
            invoice.invoice_date = date.today()

        if data.get("due_date"):
            try:
                invoice.due_date = datetime.strptime(
                    data["due_date"], "%Y-%m-%d"
                ).date()
            except Exception:
                pass

        # الأطراف | Parties
        invoice.customer_id = data.get("customer_id")
        invoice.supplier_id = data.get("supplier_id")
        invoice.warehouse_id = data.get("warehouse_id")
        invoice.created_by = session.get("user_id", 1)

        # المبالغ | Amounts
        invoice.subtotal = subtotal
        invoice.tax_amount = tax_amount
        invoice.tax_rate = data.get("tax_rate", 0)
        invoice.discount_amount = discount_amount
        invoice.discount_type = data.get("discount_type", "fixed")
        invoice.discount_value = data.get("discount_value", 0)
        invoice.shipping_cost = shipping_cost
        invoice.other_charges = other_charges
        invoice.total_amount = total_amount
        invoice.paid_amount = Decimal("0.00")
        invoice.remaining_amount = total_amount

        # الحالة | Status
        if InvoiceStatus:
            invoice.status = InvoiceStatus.DRAFT
        else:
            invoice.status = "draft"

        if PaymentStatus:
            invoice.payment_status = PaymentStatus.UNPAID
        else:
            invoice.payment_status = "unpaid"

        # معلومات إضافية | Additional info
        invoice.notes = data.get("notes", "")
        if hasattr(invoice, "terms_conditions"):
            invoice.terms_conditions = data.get("terms_conditions", "")
        if hasattr(invoice, "currency"):
            invoice.currency = data.get("currency", "USD")
        if hasattr(invoice, "exchange_rate"):
            invoice.exchange_rate = data.get("exchange_rate", 1.0)

        db.session.add(invoice)
        db.session.flush()  # للحصول على معرف الفاتورة

        # إضافة العناصر | Add items
        for item_data in data["items"]:
            item = InvoiceItem()
            item.invoice_id = invoice.id
            item.product_id = item_data.get("product_id")
            item.quantity = item_data.get("quantity", 0)
            item.price = item_data.get("price", 0)

            if hasattr(item, "discount"):
                item.discount = item_data.get("discount", 0)
            if hasattr(item, "tax"):
                item.tax = item_data.get("tax", 0)

            # حساب الإجمالي للعنصر | Calculate item total
            quantity = Decimal(str(item.quantity))
            price = Decimal(str(item.price))
            discount = Decimal(str(item_data.get("discount", 0)))
            tax = Decimal(str(item_data.get("tax", 0)))

            item.total = (quantity * price) - discount + tax

            if hasattr(item, "notes"):
                item.notes = item_data.get("notes", "")

            db.session.add(item)

        db.session.commit()

        # تسجيل النشاط | Log activity
        log_activity(
            session.get("user_id", 1),
            "create_invoice",
            f"إنشاء فاتورة {invoice_number}",
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "تم إنشاء الفاتورة بنجاح",
                    "data": {
                        "id": invoice.id,
                        "invoice_number": invoice.invoice_number,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إنشاء الفاتورة: {e}")
        return error_response(
            message="حدث خطأ في إنشاء الفاتورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/<int:invoice_id>", methods=["PUT"])
@token_required
def update_invoice(invoice_id):
    """
    تحديث فاتورة
    Update invoice
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return error_response(
                message="الفاتورة غير موجودة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # التحقق من إمكانية التعديل | Check if editable
        if hasattr(invoice.status, "value"):
            status_value = invoice.status.value
        else:
            status_value = invoice.status

        if status_value in ["paid", "cancelled"]:
            return error_response(
                message="لا يمكن تعديل فاتورة مدفوعة أو ملغاة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        data = request.get_json()

        # تحديث البيانات | Update data
        if data.get("invoice_date"):
            try:
                invoice.invoice_date = datetime.strptime(
                    data["invoice_date"], "%Y-%m-%d"
                ).date()
            except Exception:
                pass

        if data.get("due_date"):
            try:
                invoice.due_date = datetime.strptime(
                    data["due_date"], "%Y-%m-%d"
                ).date()
            except Exception:
                pass

        if data.get("notes") is not None:
            invoice.notes = data["notes"]

        if data.get("status"):
            if InvoiceStatus:
                try:
                    invoice.status = InvoiceStatus[data["status"].upper()]
                except Exception:
                    invoice.status = data["status"]
            else:
                invoice.status = data["status"]

        db.session.commit()

        # تسجيل النشاط | Log activity
        log_activity(
            session.get("user_id", 1),
            "update_invoice",
            f"تحديث فاتورة {invoice.invoice_number}",
        )

        return success_response(message="تم تحديث الفاتورة بنجاح", status_code=200), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تحديث الفاتورة: {e}")
        return error_response(
            message="حدث خطأ في تحديث الفاتورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/<int:invoice_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_invoice(invoice_id):
    """
    حذف فاتورة (مدير فقط)
    Delete invoice (admin only)
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return error_response(
                message="الفاتورة غير موجودة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # التحقق من إمكانية الحذف | Check if deletable
        if hasattr(invoice.status, "value"):
            status_value = invoice.status.value
        else:
            status_value = invoice.status

        if status_value == "paid":
            return error_response(
                message="لا يمكن حذف فاتورة مدفوعة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        invoice_number = invoice.invoice_number

        # حذف العناصر | Delete items
        if InvoiceItem:
            InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()

        # حذف الدفعات | Delete payments
        if InvoicePayment:
            InvoicePayment.query.filter_by(invoice_id=invoice.id).delete()

        # حذف الفاتورة | Delete invoice
        db.session.delete(invoice)
        db.session.commit()

        # تسجيل النشاط | Log activity
        log_activity(
            session.get("user_id", 1), "delete_invoice", f"حذف فاتورة {invoice_number}"
        )

        return success_response(message="تم حذف الفاتورة بنجاح", status_code=200), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في حذف الفاتورة: {e}")
        return error_response(
            message="حدث خطأ في حذف الفاتورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/stats", methods=["GET"])
@token_required
def get_invoices_stats():
    """
    الحصول على إحصائيات الفواتير
    Get invoices statistics
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # إحصائيات عامة | General statistics
        total_invoices = Invoice.query.count()

        # إحصائيات حسب النوع | Statistics by type
        sales_count = Invoice.query.filter(
            Invoice.invoice_type.in_(["sales", InvoiceType.SALES])
            if InvoiceType
            else Invoice.invoice_type == "sales"
        ).count()

        purchase_count = Invoice.query.filter(
            Invoice.invoice_type.in_(["purchase", InvoiceType.PURCHASE])
            if InvoiceType
            else Invoice.invoice_type == "purchase"
        ).count()

        # إحصائيات حسب الحالة | Statistics by status
        draft_count = Invoice.query.filter(
            Invoice.status.in_(["draft", InvoiceStatus.DRAFT])
            if InvoiceStatus
            else Invoice.status == "draft"
        ).count()

        confirmed_count = Invoice.query.filter(
            Invoice.status.in_(["confirmed", InvoiceStatus.CONFIRMED])
            if InvoiceStatus
            else Invoice.status == "confirmed"
        ).count()

        paid_count = Invoice.query.filter(
            Invoice.status.in_(["paid", InvoiceStatus.PAID])
            if InvoiceStatus
            else Invoice.status == "paid"
        ).count()

        # إحصائيات المبالغ | Amount statistics
        total_sales = (
            db.session.query(func.sum(Invoice.total_amount))
            .filter(
                Invoice.invoice_type.in_(["sales", InvoiceType.SALES])
                if InvoiceType
                else Invoice.invoice_type == "sales"
            )
            .scalar()
            or 0
        )

        total_purchases = (
            db.session.query(func.sum(Invoice.total_amount))
            .filter(
                Invoice.invoice_type.in_(["purchase", InvoiceType.PURCHASE])
                if InvoiceType
                else Invoice.invoice_type == "purchase"
            )
            .scalar()
            or 0
        )

        total_paid = db.session.query(func.sum(Invoice.paid_amount)).scalar() or 0
        total_remaining = (
            db.session.query(func.sum(Invoice.remaining_amount)).scalar() or 0
        )

        return (
            jsonify(
                {
                    "success": True,
                    "data": {
                        "total_invoices": total_invoices,
                        "by_type": {
                            "sales": sales_count,
                            "purchase": purchase_count,
                        },
                        "by_status": {
                            "draft": draft_count,
                            "confirmed": confirmed_count,
                            "paid": paid_count,
                        },
                        "amounts": {
                            "total_sales": float(total_sales),
                            "total_purchases": float(total_purchases),
                            "total_paid": float(total_paid),
                            "total_remaining": float(total_remaining),
                        },
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات الفواتير: {e}")
        return error_response(
            message="حدث خطأ في الحصول على الإحصائيات",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/search", methods=["GET"])
@token_required
def search_invoices():
    """
    البحث السريع في الفواتير
    Quick search in invoices
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        query_text = request.args.get("q", "")
        limit = request.args.get("limit", 10, type=int)

        if not query_text:
            return success_response(data=[], message="Success", status_code=200), 200

        # البحث | Search
        invoices = (
            Invoice.query.filter(Invoice.invoice_number.ilike(f"%{query_text}%"))
            .limit(limit)
            .all()
        )

        results = []
        for invoice in invoices:
            results.append(
                {
                    "id": invoice.id,
                    "invoice_number": invoice.invoice_number,
                    "invoice_type": (
                        invoice.invoice_type.value
                        if hasattr(invoice.invoice_type, "value")
                        else invoice.invoice_type
                    ),
                    "invoice_date": (
                        invoice.invoice_date.isoformat()
                        if invoice.invoice_date
                        else None
                    ),
                    "total_amount": (
                        float(invoice.total_amount) if invoice.total_amount else 0.00
                    ),
                    "status": (
                        invoice.status.value
                        if hasattr(invoice.status, "value")
                        else invoice.status
                    ),
                }
            )

        return success_response(data=results, message="Success", status_code=200), 200

    except Exception as e:
        logger.error(f"خطأ في البحث في الفواتير: {e}")
        return error_response(
            message="حدث خطأ في البحث",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/export", methods=["GET"])
@token_required
def export_invoices():
    """
    تصدير الفواتير
    Export invoices
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        # الحصول على جميع الفواتير | Get all invoices
        invoices = Invoice.query.all()

        data = []
        for invoice in invoices:
            data.append(
                {
                    "id": invoice.id,
                    "invoice_number": invoice.invoice_number,
                    "invoice_type": (
                        invoice.invoice_type.value
                        if hasattr(invoice.invoice_type, "value")
                        else invoice.invoice_type
                    ),
                    "invoice_date": (
                        invoice.invoice_date.isoformat()
                        if invoice.invoice_date
                        else None
                    ),
                    "due_date": (
                        invoice.due_date.isoformat() if invoice.due_date else None
                    ),
                    "customer_id": invoice.customer_id,
                    "supplier_id": invoice.supplier_id,
                    "subtotal": float(invoice.subtotal) if invoice.subtotal else 0.00,
                    "tax_amount": (
                        float(invoice.tax_amount) if invoice.tax_amount else 0.00
                    ),
                    "discount_amount": (
                        float(invoice.discount_amount)
                        if invoice.discount_amount
                        else 0.00
                    ),
                    "total_amount": (
                        float(invoice.total_amount) if invoice.total_amount else 0.00
                    ),
                    "paid_amount": (
                        float(invoice.paid_amount) if invoice.paid_amount else 0.00
                    ),
                    "remaining_amount": (
                        float(invoice.remaining_amount)
                        if invoice.remaining_amount
                        else 0.00
                    ),
                    "status": (
                        invoice.status.value
                        if hasattr(invoice.status, "value")
                        else invoice.status
                    ),
                    "payment_status": (
                        invoice.payment_status.value
                        if hasattr(invoice.payment_status, "value")
                        else getattr(invoice, "payment_status", None)
                    ),
                }
            )

        return (
            success_response(
                data=data, message="تم تصدير الفواتير بنجاح", status_code=200
            ),
            200,
        )

    except Exception as e:
        logger.error(f"خطأ في تصدير الفواتير: {e}")
        return error_response(
            message="حدث خطأ في التصدير",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/<int:invoice_id>/payments", methods=["POST"])
@token_required
def add_payment(invoice_id):
    """
    إضافة دفعة للفاتورة
    Add payment to invoice
    """
    try:
        if not Invoice or not InvoicePayment:
            return error_response(
                message="نموذج الدفعات غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return error_response(
                message="الفاتورة غير موجودة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        data = request.get_json()

        # التحقق من المبلغ | Validate amount
        if not data.get("amount"):
            return error_response(
                message="المبلغ مطلوب",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        amount = Decimal(str(data["amount"]))

        if amount <= 0:
            return error_response(
                message="المبلغ يجب أن يكون أكبر من صفر",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        if amount > invoice.remaining_amount:
            return error_response(
                message="المبلغ أكبر من المتبقي",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # إنشاء الدفعة | Create payment
        payment = InvoicePayment()
        payment.invoice_id = invoice.id
        payment.amount = amount

        if data.get("payment_date"):
            try:
                payment.payment_date = datetime.strptime(
                    data["payment_date"], "%Y-%m-%d"
                ).date()
            except Exception:
                payment.payment_date = date.today()
        else:
            payment.payment_date = date.today()

        if hasattr(payment, "payment_method"):
            payment.payment_method = data.get("payment_method", "cash")
        if hasattr(payment, "reference"):
            payment.reference = data.get("reference", "")
        if hasattr(payment, "notes"):
            payment.notes = data.get("notes", "")

        db.session.add(payment)

        # تحديث الفاتورة | Update invoice
        invoice.paid_amount += amount
        invoice.remaining_amount -= amount

        # تحديث حالة الدفع | Update payment status
        if invoice.remaining_amount == 0:
            if PaymentStatus:
                invoice.payment_status = PaymentStatus.PAID
            else:
                invoice.payment_status = "paid"

            if InvoiceStatus:
                invoice.status = InvoiceStatus.PAID
            else:
                invoice.status = "paid"
        else:
            if PaymentStatus:
                invoice.payment_status = PaymentStatus.PARTIAL
            else:
                invoice.payment_status = "partial"

        db.session.commit()

        # تسجيل النشاط | Log activity
        log_activity(
            session.get("user_id", 1),
            "add_payment",
            f"إضافة دفعة للفاتورة {invoice.invoice_number}",
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "تم إضافة الدفعة بنجاح",
                    "data": {
                        "id": payment.id,
                        "amount": float(payment.amount),
                        "remaining_amount": float(invoice.remaining_amount),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إضافة الدفعة: {e}")
        return error_response(
            message="حدث خطأ في إضافة الدفعة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/<int:invoice_id>/confirm", methods=["POST"])
@token_required
def confirm_invoice(invoice_id):
    """
    تأكيد الفاتورة
    Confirm invoice
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return error_response(
                message="الفاتورة غير موجودة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # التحقق من الحالة | Check status
        if hasattr(invoice.status, "value"):
            status_value = invoice.status.value
        else:
            status_value = invoice.status

        if status_value != "draft":
            return error_response(
                message="يمكن تأكيد المسودات فقط",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # تأكيد الفاتورة | Confirm invoice
        if InvoiceStatus:
            invoice.status = InvoiceStatus.CONFIRMED
        else:
            invoice.status = "confirmed"

        db.session.commit()

        # تسجيل النشاط | Log activity
        log_activity(
            session.get("user_id", 1),
            "confirm_invoice",
            f"تأكيد فاتورة {invoice.invoice_number}",
        )

        return success_response(message="تم تأكيد الفاتورة بنجاح", status_code=200), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تأكيد الفاتورة: {e}")
        return error_response(
            message="حدث خطأ في تأكيد الفاتورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@invoices_unified_bp.route("/api/invoices/<int:invoice_id>/cancel", methods=["POST"])
@token_required
@admin_required
def cancel_invoice(invoice_id):
    """
    إلغاء الفاتورة (مدير فقط)
    Cancel invoice (admin only)
    """
    try:
        if not Invoice:
            return error_response(
                message="نموذج الفواتير غير متاح",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=501,
            )

        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return error_response(
                message="الفاتورة غير موجودة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=404,
            )

        # التحقق من الحالة | Check status
        if hasattr(invoice.status, "value"):
            status_value = invoice.status.value
        else:
            status_value = invoice.status

        if status_value == "paid":
            return error_response(
                message="لا يمكن إلغاء فاتورة مدفوعة",
                code=ErrorCodes.SYS_INTERNAL_ERROR,
                status_code=400,
            )

        # إلغاء الفاتورة | Cancel invoice
        if InvoiceStatus:
            invoice.status = InvoiceStatus.CANCELLED
        else:
            invoice.status = "cancelled"

        db.session.commit()

        # تسجيل النشاط | Log activity
        log_activity(
            session.get("user_id", 1),
            "cancel_invoice",
            f"إلغاء فاتورة {invoice.invoice_number}",
        )

        return success_response(message="تم إلغاء الفاتورة بنجاح", status_code=200), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في إلغاء الفاتورة: {e}")
        return error_response(
            message="حدث خطأ في إلغاء الفاتورة",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
