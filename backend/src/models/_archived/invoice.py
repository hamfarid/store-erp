# /home/ubuntu/upload/store_v1.5/complete_inventory_system/backend/src/models/invoice.py
# -*- coding: utf-8 -*-
"""
نموذج الفواتير
Invoice Model for Complete Inventory System
"""

from datetime import datetime, timezone
from .user import db


class Invoice(db.Model):
    """نموذج الفواتير"""

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # معلومات العميل
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    # تواريخ الفاتورة
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date)

    # المبالغ
    subtotal = db.Column(db.Numeric(15, 2), default=0.00)
    tax_amount = db.Column(db.Numeric(15, 2), default=0.00)
    discount_amount = db.Column(db.Numeric(15, 2), default=0.00)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(15, 2), default=0.00)
    remaining_amount = db.Column(db.Numeric(15, 2), default=0.00)

    # معلومات إضافية
    currency = db.Column(db.String(3), default="USD")
    exchange_rate = db.Column(db.Numeric(10, 4), default=1.0000)
    payment_terms = db.Column(db.String(50))

    # حالة الفاتورة
    status = db.Column(
        db.String(20), default="draft"
    )  # draft, sent, paid, partial, overdue, cancelled

    # ملاحظات
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)

    # تواريخ النظام
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    # العلاقات
    items = db.relationship(
        "InvoiceItem", backref="invoice", lazy="dynamic", cascade="all, delete-orphan"
    )
    payments = db.relationship("Payment", backref="invoice", lazy="dynamic")

    def __repr__(self):
        return f"<Invoice {self.invoice_number}>"

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "customer_id": self.customer_id,
            "invoice_date": (
                self.invoice_date.isoformat() if self.invoice_date else None
            ),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "subtotal": float(self.subtotal) if self.subtotal else 0.00,
            "tax_amount": float(self.tax_amount) if self.tax_amount else 0.00,
            "discount_amount": (
                float(self.discount_amount) if self.discount_amount else 0.00
            ),
            "total_amount": float(self.total_amount) if self.total_amount else 0.00,
            "paid_amount": float(self.paid_amount) if self.paid_amount else 0.00,
            "remaining_amount": (
                float(self.remaining_amount) if self.remaining_amount else 0.00
            ),
            "currency": self.currency,
            "exchange_rate": float(self.exchange_rate) if self.exchange_rate else 1.0,
            "payment_terms": self.payment_terms,
            "status": self.status,
            "notes": self.notes,
            "internal_notes": self.internal_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "items": [item.to_dict() for item in self.items],
        }

    def calculate_totals(self):
        """حساب إجماليات الفاتورة"""
        self.subtotal = sum(item.line_total for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.remaining_amount = self.total_amount - self.paid_amount
        db.session.commit()

    def update_status(self):
        """تحديث حالة الفاتورة بناءً على المدفوعات"""
        if self.paid_amount == 0:
            self.status = "sent"
        elif self.paid_amount >= self.total_amount:
            self.status = "paid"
        else:
            self.status = "partial"

        # فحص التأخير
        if (
            self.due_date
            and datetime.now().date() > self.due_date
            and self.status != "paid"
        ):
            self.status = "overdue"

        db.session.commit()


class InvoiceItem(db.Model):
    """بنود الفاتورة"""

    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # معلومات المنتج
    product_name = db.Column(db.String(200), nullable=False)
    product_code = db.Column(db.String(50))
    description = db.Column(db.Text)

    # الكميات والأسعار
    quantity = db.Column(db.Numeric(10, 3), nullable=False)
    unit_price = db.Column(db.Numeric(15, 2), nullable=False)
    line_total = db.Column(db.Numeric(15, 2), nullable=False)

    # الضرائب والخصومات
    tax_rate = db.Column(db.Numeric(5, 2), default=0.00)
    discount_rate = db.Column(db.Numeric(5, 2), default=0.00)

    # وحدة القياس
    unit_of_measure = db.Column(db.String(20))

    def __repr__(self):
        return f"<InvoiceItem {self.product_name}>"

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_code": self.product_code,
            "description": self.description,
            "quantity": float(self.quantity) if self.quantity else 0.0,
            "unit_price": float(self.unit_price) if self.unit_price else 0.00,
            "line_total": float(self.line_total) if self.line_total else 0.00,
            "tax_rate": float(self.tax_rate) if self.tax_rate else 0.00,
            "discount_rate": float(self.discount_rate) if self.discount_rate else 0.00,
            "unit_of_measure": self.unit_of_measure,
        }

    def calculate_line_total(self):
        """حساب إجمالي السطر"""
        base_amount = self.quantity * self.unit_price
        discount_amount = base_amount * (self.discount_rate / 100)
        tax_amount = (base_amount - discount_amount) * (self.tax_rate / 100)
        self.line_total = base_amount - discount_amount + tax_amount
        return self.line_total


class Payment(db.Model):
    """مدفوعات الفواتير"""

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)

    # معلومات الدفع
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    payment_method = db.Column(db.String(50))  # cash, bank_transfer, credit_card, etc.
    reference_number = db.Column(db.String(100))

    # ملاحظات
    notes = db.Column(db.Text)

    # تواريخ النظام
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Payment {self.amount} for Invoice {self.invoice_id}>"

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "amount": float(self.amount) if self.amount else 0.00,
            "payment_method": self.payment_method,
            "reference_number": self.reference_number,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
