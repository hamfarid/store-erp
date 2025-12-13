# FILE: backend/src/routes/invoices.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# /home/ubuntu/upload/store_v1.5/complete_inventory_system/backend/src/routes/invoices.py
# -*- coding: utf-8 -*-
"""
مسارات الفواتير المحسنة
Enhanced Invoice Routes
"""

from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.models.invoice_unified import Invoice, InvoiceItem
from src.models.supporting_models import Payment
from src.models.customer import Customer
from src.database import db
from datetime import datetime, date
from sqlalchemy import desc, and_, or_

# إنشاء Blueprint
invoices_bp = Blueprint("invoices", __name__)


@invoices_bp.route("/api/invoices", methods=["GET"])
def get_invoices():
    """الحصول على قائمة الفواتير"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 50, type=int)
        search = request.args.get("search", "")
        status = request.args.get("status", "")
        customer_id = request.args.get("customer_id", type=int)

        query = Invoice.query

        # تطبيق الفلاتر
        if search:
            query = query.filter(
                or_(
                    Invoice.invoice_number.contains(search),
                    Invoice.notes.contains(search),
                )
            )

        if status:
            query = query.filter(Invoice.status == status)

        if customer_id:
            query = query.filter(Invoice.customer_id == customer_id)

        # ترتيب حسب التاريخ
        query = query.order_by(desc(Invoice.created_at))

        # تطبيق التصفح
        invoices = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "data": [invoice.to_dict() for invoice in invoices.items],
                "pagination": {
                    "page": page,
                    "pages": invoices.pages,
                    "per_page": per_page,
                    "total": invoices.total,
                },
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على الفواتير: {str(e)}"}
            ),
            500,
        )


@invoices_bp.route("/api/invoices", methods=["POST"])
def create_invoice():
    """إنشاء فاتورة جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get("customer_id"):
            return jsonify({"status": "error", "message": "معرف العميل مطلوب"}), 400

        if not data.get("items"):
            return jsonify({"status": "error", "message": "بنود الفاتورة مطلوبة"}), 400

        # التحقق من وجود العميل
        customer = Customer.query.get(data["customer_id"])
        if not customer:
            return jsonify({"status": "error", "message": "العميل غير موجود"}), 404

        # إنشاء الفاتورة
        invoice = Invoice(
            invoice_number=data.get("invoice_number") or generate_invoice_number(),
            customer_id=data["customer_id"],
            invoice_date=datetime.strptime(
                data.get("invoice_date", datetime.now().strftime("%Y-%m-%d")),
                "%Y-%m-%d",
            ).date(),
            due_date=(
                datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                if data.get("due_date")
                else None
            ),
            currency=data.get("currency", "USD"),
            exchange_rate=data.get("exchange_rate", 1.0),
            payment_terms=data.get("payment_terms"),
            notes=data.get("notes"),
            internal_notes=data.get("internal_notes"),
            status="draft",
        )

        db.session.add(invoice)
        db.session.flush()  # للحصول على معرف الفاتورة

        # إضافة بنود الفاتورة
        total_amount = 0
        for item_data in data["items"]:
            item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=item_data.get("product_id"),
                product_name=item_data["product_name"],
                product_code=item_data.get("product_code"),
                description=item_data.get("description"),
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                tax_rate=item_data.get("tax_rate", 0),
                discount_rate=item_data.get("discount_rate", 0),
                unit_of_measure=item_data.get("unit_of_measure"),
            )
            item.calculate_line_total()
            total_amount += item.line_total
            db.session.add(item)

        # تحديث إجماليات الفاتورة
        invoice.subtotal = total_amount
        invoice.tax_amount = data.get("tax_amount", 0)
        invoice.discount_amount = data.get("discount_amount", 0)
        invoice.total_amount = (
            invoice.subtotal + invoice.tax_amount - invoice.discount_amount
        )
        invoice.remaining_amount = invoice.total_amount

        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء الفاتورة بنجاح",
                    "data": invoice.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء الفاتورة: {str(e)}"}),
            500,
        )


@invoices_bp.route("/api/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    """الحصول على فاتورة محددة"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        return jsonify({"status": "success", "data": invoice.to_dict()})
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على الفاتورة: {str(e)}"}
            ),
            500,
        )


@invoices_bp.route("/api/invoices/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    """تحديث فاتورة"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()

        # التحقق من إمكانية التعديل
        if invoice.status in ["paid", "cancelled"]:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "لا يمكن تعديل فاتورة مدفوعة أو ملغاة",
                    }
                ),
                400,
            )

        # تحديث البيانات الأساسية
        if "invoice_date" in data:
            invoice.invoice_date = datetime.strptime(
                data["invoice_date"], "%Y-%m-%d"
            ).date()
        if "due_date" in data:
            invoice.due_date = (
                datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                if data["due_date"]
                else None
            )
        if "notes" in data:
            invoice.notes = data["notes"]
        if "internal_notes" in data:
            invoice.internal_notes = data["internal_notes"]

        # تحديث البنود إذا تم تمريرها
        if "items" in data:
            # حذف البنود الحالية
            InvoiceItem.query.filter_by(invoice_id=invoice_id).delete()

            # إضافة البنود الجديدة
            total_amount = 0
            for item_data in data["items"]:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=item_data.get("product_id"),
                    product_name=item_data["product_name"],
                    product_code=item_data.get("product_code"),
                    description=item_data.get("description"),
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    tax_rate=item_data.get("tax_rate", 0),
                    discount_rate=item_data.get("discount_rate", 0),
                    unit_of_measure=item_data.get("unit_of_measure"),
                )
                item.calculate_line_total()
                total_amount += item.line_total
                db.session.add(item)

            # إعادة حساب الإجماليات
            invoice.calculate_totals()

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث الفاتورة بنجاح",
                "data": invoice.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث الفاتورة: {str(e)}"}),
            500,
        )


@invoices_bp.route("/api/invoices/<int:invoice_id>/payments", methods=["POST"])
def add_payment(invoice_id):
    """إضافة دفعة للفاتورة"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        if not data.get("amount"):
            return jsonify({"status": "error", "message": "مبلغ الدفعة مطلوب"}), 400

        amount = float(data["amount"])

        # التحقق من صحة المبلغ
        if amount <= 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "مبلغ الدفعة يجب أن يكون أكبر من صفر",
                    }
                ),
                400,
            )

        if amount > invoice.remaining_amount:
            return (
                jsonify(
                    {"status": "error", "message": "مبلغ الدفعة أكبر من المبلغ المستحق"}
                ),
                400,
            )

        # إنشاء الدفعة
        payment = Payment(
            invoice_id=invoice.id,
            payment_date=datetime.strptime(
                data.get("payment_date", datetime.now().strftime("%Y-%m-%d")),
                "%Y-%m-%d",
            ).date(),
            amount=amount,
            payment_method=data.get("payment_method"),
            reference_number=data.get("reference_number"),
            notes=data.get("notes"),
        )

        db.session.add(payment)

        # تحديث مبلغ المدفوع في الفاتورة
        invoice.paid_amount += amount
        invoice.remaining_amount = invoice.total_amount - invoice.paid_amount

        # تحديث حالة الفاتورة
        invoice.update_status()

        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة الدفعة بنجاح",
                    "data": {
                        "payment": payment.to_dict(),
                        "invoice": invoice.to_dict(),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في إضافة الدفعة: {str(e)}"}),
            500,
        )


@invoices_bp.route("/api/invoices/<int:invoice_id>/status", methods=["PUT"])
def update_invoice_status(invoice_id):
    """تحديث حالة الفاتورة"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()

        new_status = data.get("status")
        if not new_status:
            return jsonify({"status": "error", "message": "الحالة الجديدة مطلوبة"}), 400

        # التحقق من صحة الحالة
        valid_statuses = ["draft", "sent", "paid", "partial", "overdue", "cancelled"]
        if new_status not in valid_statuses:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f'حالة غير صحيحة. الحالات المتاحة: {", ".join(valid_statuses)}',
                    }
                ),
                400,
            )

        invoice.status = new_status
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث حالة الفاتورة بنجاح",
                "data": invoice.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في تحديث حالة الفاتورة: {str(e)}"}
            ),
            500,
        )


def generate_invoice_number():
    """توليد رقم فاتورة تلقائي"""
    today = datetime.now()
    prefix = f"INV-{today.year}{today.month:02d}"

    # البحث عن آخر فاتورة في الشهر الحالي
    last_invoice = (
        Invoice.query.filter(Invoice.invoice_number.like(f"{prefix}%"))
        .order_by(desc(Invoice.invoice_number))
        .first()
    )

    if last_invoice:
        # استخراج الرقم التسلسلي وزيادته
        try:
            last_number = int(last_invoice.invoice_number.split("-")[-1])
            new_number = last_number + 1
        except (ValueError, IndexError):
            new_number = 1
    else:
        new_number = 1

    return f"{prefix}-{new_number:04d}"
