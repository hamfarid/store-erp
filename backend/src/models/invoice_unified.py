#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج الفواتير الموحد والمحسّن
Unified and Enhanced Invoice Model

يدمج invoice.py, invoices.py, unified_invoice.py مع تحسينات
"""

import enum
from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from src.database import db
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.user import User
from src.models.inventory import Warehouse

# Import Product for InvoiceItem relationship
try:
    from src.models.product_unified import Product
except ImportError:
    Product = None  # type: ignore

# Touch registry to avoid removal by formatter and ensure mapper sees classes
_REG_IMPORTS = (Customer, Supplier, Warehouse, User, Product)


class InvoiceType(enum.Enum):
    """أنواع الفواتير"""

    SALES = "sales"  # فاتورة مبيعات
    PURCHASE = "purchase"  # فاتورة مشتريات
    SALES_RETURN = "sales_return"  # مرتجع مبيعات
    PURCHASE_RETURN = "purchase_return"  # مرتجع مشتريات


class InvoiceStatus(enum.Enum):
    """حالات الفاتورة"""

    DRAFT = "draft"  # مسودة
    CONFIRMED = "confirmed"  # مؤكدة
    PAID = "paid"  # مدفوعة
    PARTIAL = "partial"  # مدفوعة جزئياً
    CANCELLED = "cancelled"  # ملغاة
    OVERDUE = "overdue"  # متأخرة


class PaymentStatus(enum.Enum):
    """حالات الدفع"""

    UNPAID = "unpaid"  # غير مدفوعة
    PARTIAL = "partial"  # مدفوعة جزئياً
    PAID = "paid"  # مدفوعة بالكامل


class Invoice(db.Model):
    """نموذج الفواتير الموحد"""

    __tablename__ = "invoices"
    __table_args__ = (
        Index("idx_invoice_number", "invoice_number"),
        Index("idx_invoice_type", "invoice_type"),
        Index("idx_invoice_status", "status"),
        Index("idx_invoice_date", "invoice_date"),
        Index("idx_invoice_customer", "customer_id"),
        Index("idx_invoice_supplier", "supplier_id"),
        Index("idx_invoice_warehouse", "warehouse_id"),
        {"extend_existing": True},
    )

    # المعلومات الأساسية
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    invoice_type = Column(
        Enum(
            InvoiceType,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            native_enum=False,
        ),
        nullable=False,
        default=InvoiceType.SALES,
    )

    # التواريخ
    invoice_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date)
    delivery_date = Column(Date)  # تاريخ التسليم

    # الأطراف
    customer_id = Column(Integer, ForeignKey("customers.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # المبالغ
    subtotal = Column(Numeric(15, 2), default=0.00)  # المجموع الفرعي
    tax_amount = Column(Numeric(15, 2), default=0.00)  # الضريبة
    discount_amount = Column(Numeric(15, 2), default=0.00)  # الخصم
    shipping_cost = Column(Numeric(15, 2), default=0.00)  # تكلفة الشحن
    other_charges = Column(Numeric(15, 2), default=0.00)  # رسوم أخرى
    total_amount = Column(Numeric(15, 2), default=0.00)  # الإجمالي
    paid_amount = Column(Numeric(15, 2), default=0.00)  # المدفوع
    remaining_amount = Column(Numeric(15, 2), default=0.00)  # المتبقي

    # معلومات الخصم
    discount_type = Column(String(20), default="fixed")  # fixed, percentage
    discount_value = Column(Numeric(10, 2), default=0.00)

    # معلومات الضريبة
    tax_rate = Column(Numeric(5, 2), default=0.00)  # نسبة الضريبة
    is_tax_inclusive = Column(Boolean, default=False)  # الضريبة شاملة

    # العملة
    currency = Column(String(3), default="USD")
    exchange_rate = Column(Numeric(10, 4), default=1.0000)

    # الحالة
    status = Column(
        Enum(
            InvoiceStatus,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            native_enum=False,
        ),
        default=InvoiceStatus.DRAFT,
    )
    payment_status = Column(
        Enum(
            PaymentStatus,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            native_enum=False,
        ),
        default=PaymentStatus.UNPAID,
    )

    # معلومات الدفع
    payment_method = Column(String(50))  # cash, card, bank_transfer, etc.
    payment_terms = Column(String(100))  # شروط الدفع

    # معلومات الشحن
    shipping_address = Column(Text)
    shipping_method = Column(String(50))
    tracking_number = Column(String(100))

    # الملاحظات
    notes = Column(Text)  # ملاحظات عامة
    internal_notes = Column(Text)  # ملاحظات داخلية
    terms_conditions = Column(Text)  # الشروط والأحكام

    # معلومات إضافية
    reference_number = Column(String(50))  # رقم مرجعي
    po_number = Column(String(50))  # رقم أمر الشراء

    # التواريخ النظامية
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    confirmed_at = Column(DateTime)  # تاريخ التأكيد
    paid_at = Column(DateTime)  # تاريخ الدفع الكامل
    cancelled_at = Column(DateTime)  # تاريخ الإلغاء

    # العلاقات
    customer = db.relationship("src.models.customer.Customer")
    supplier = db.relationship("src.models.supplier.Supplier")
    warehouse = db.relationship("src.models.inventory.Warehouse")

    items = db.relationship(
        "src.models.invoice_unified.InvoiceItem", cascade="all, delete-orphan"
    )
    payments = db.relationship(
        "src.models.invoice_unified.InvoicePayment",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def calculate_totals(self):
        """حساب إجماليات الفاتورة"""
        # حساب المجموع الفرعي من الأصناف
        subtotal = sum(item.line_total for item in self.items)
        self.subtotal = subtotal

        # حساب الخصم - استخدام getattr لتجنب مشاكل SQLAlchemy
        discount_type = getattr(self, "discount_type", "fixed") or "fixed"
        discount_value = getattr(self, "discount_value", 0) or 0

        if discount_type == "percentage":
            discount_amount = (subtotal * float(discount_value)) / 100
        else:
            discount_amount = float(discount_value)
        self.discount_amount = discount_amount

        # المجموع بعد الخصم
        amount_after_discount = subtotal - discount_amount

        # حساب الضريبة
        tax_rate = getattr(self, "tax_rate", 0) or 0
        is_tax_inclusive = getattr(self, "is_tax_inclusive", False) or False

        if is_tax_inclusive:
            # الضريبة شاملة
            tax_amount = (amount_after_discount * float(tax_rate)) / (
                100 + float(tax_rate)
            )
        else:
            # الضريبة غير شاملة
            tax_amount = (amount_after_discount * float(tax_rate)) / 100
        self.tax_amount = tax_amount

        # الإجمالي النهائي
        shipping_cost = getattr(self, "shipping_cost", 0) or 0
        other_charges = getattr(self, "other_charges", 0) or 0

        if is_tax_inclusive:
            total_amount = (
                amount_after_discount + float(shipping_cost) + float(other_charges)
            )
        else:
            total_amount = (
                amount_after_discount
                + tax_amount
                + float(shipping_cost)
                + float(other_charges)
            )
        self.total_amount = total_amount

        # المتبقي
        paid_amount = getattr(self, "paid_amount", 0) or 0
        self.remaining_amount = total_amount - float(paid_amount)

        # تحديث حالة الدفع
        self.update_payment_status()

    def update_payment_status(self):
        """تحديث حالة الدفع"""
        paid_amount = getattr(self, "paid_amount", 0) or 0
        total_amount = getattr(self, "total_amount", 0) or 0

        if float(paid_amount) == 0:
            self.payment_status = PaymentStatus.UNPAID
        elif float(paid_amount) >= float(total_amount):
            self.payment_status = PaymentStatus.PAID
            paid_at = getattr(self, "paid_at", None)
            if not paid_at:
                self.paid_at = datetime.now(timezone.utc)
        else:
            self.payment_status = PaymentStatus.PARTIAL

    def add_payment(self, amount, payment_method="cash", notes=None):
        """إضافة دفعة"""
        self.paid_amount += amount
        self.update_payment_status()

        # إنشاء سجل الدفعة
        from src.models.supporting_models import Payment

        payment = Payment(
            invoice_id=self.id,
            amount=amount,
            payment_method=payment_method,
            payment_date=date.today(),
            notes=notes,
        )
        db.session.add(payment)

    def confirm(self):
        """تأكيد الفاتورة"""
        if self.status == InvoiceStatus.DRAFT:  # type: ignore[comparison-overlap]
            self.status = InvoiceStatus.CONFIRMED
            self.confirmed_at = datetime.now(timezone.utc)

            # تحديث المخزون
            self.update_inventory()

    def cancel(self):
        """إلغاء الفاتورة"""
        if self.status != InvoiceStatus.CANCELLED:  # type: ignore[comparison-overlap]
            self.status = InvoiceStatus.CANCELLED
            self.cancelled_at = datetime.now(timezone.utc)

            # إرجاع المخزون
            self.reverse_inventory()

    def update_inventory(self):
        """تحديث المخزون بناءً على الفاتورة"""
        for item in self.items:
            if self.invoice_type == InvoiceType.SALES:  # type: ignore[comparison-overlap]
                # خصم من المخزون
                item.product.update_stock(item.quantity, "subtract")
            elif self.invoice_type == InvoiceType.PURCHASE:  # type: ignore[comparison-overlap]
                # إضافة للمخزون
                item.product.update_stock(item.quantity, "add")
            elif self.invoice_type == InvoiceType.SALES_RETURN:  # type: ignore[comparison-overlap]
                # إرجاع للمخزون
                item.product.update_stock(item.quantity, "add")
            # type: ignore[comparison-overlap]
            elif self.invoice_type == InvoiceType.PURCHASE_RETURN:
                # خصم من المخزون
                item.product.update_stock(item.quantity, "subtract")

    def reverse_inventory(self):
        """عكس تأثير الفاتورة على المخزون"""
        for item in self.items:
            if self.invoice_type == InvoiceType.SALES:  # type: ignore[comparison-overlap]
                # إرجاع للمخزون
                item.product.update_stock(item.quantity, "add")
            elif self.invoice_type == InvoiceType.PURCHASE:  # type: ignore[comparison-overlap]
                # خصم من المخزون
                item.product.update_stock(item.quantity, "subtract")
            elif self.invoice_type == InvoiceType.SALES_RETURN:  # type: ignore[comparison-overlap]
                # خصم من المخزون
                item.product.update_stock(item.quantity, "subtract")
            # type: ignore[comparison-overlap]
            elif self.invoice_type == InvoiceType.PURCHASE_RETURN:
                # إرجاع للمخزون
                item.product.update_stock(item.quantity, "add")

    def to_dict(self, include_items=True):
        """تحويل إلى قاموس"""
        data = {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "invoice_type": (
                getattr(self.invoice_type, "value", self.invoice_type)
                if self.invoice_type is not None
                else None
            ),
            # type: ignore[union-attr]
            "invoice_date": (
                self.invoice_date.isoformat() if self.invoice_date else None
            ),
            # type: ignore[union-attr]
            "due_date": self.due_date.isoformat() if self.due_date else None,
            # type: ignore[union-attr]
            "delivery_date": (
                self.delivery_date.isoformat() if self.delivery_date else None
            ),
            "customer_id": self.customer_id,
            "supplier_id": self.supplier_id,
            "warehouse_id": self.warehouse_id,
            "created_by": self.created_by,
            # type: ignore[arg-type,redundant-expr]
            "subtotal": float(self.subtotal) if self.subtotal else 0.00,
            # type: ignore[arg-type,redundant-expr]
            "tax_amount": float(self.tax_amount) if self.tax_amount else 0.00,
            # type: ignore[arg-type,redundant-expr]
            "discount_amount": (
                float(self.discount_amount) if self.discount_amount else 0.00
            ),
            # type: ignore[arg-type,redundant-expr]
            "shipping_cost": float(self.shipping_cost) if self.shipping_cost else 0.00,
            # type: ignore[arg-type,redundant-expr]
            "other_charges": float(self.other_charges) if self.other_charges else 0.00,
            # type: ignore[arg-type,redundant-expr]
            "total_amount": float(self.total_amount) if self.total_amount else 0.00,
            # type: ignore[arg-type,redundant-expr]
            "paid_amount": float(self.paid_amount) if self.paid_amount else 0.00,
            # type: ignore[arg-type,redundant-expr]
            "remaining_amount": (
                float(self.remaining_amount) if self.remaining_amount else 0.00
            ),
            "discount_type": self.discount_type,
            "discount_value": (
                float(self.discount_value) if self.discount_value else 0.00
            ),
            "tax_rate": float(self.tax_rate) if self.tax_rate else 0.00,
            "is_tax_inclusive": self.is_tax_inclusive,
            "currency": self.currency,
            "exchange_rate": (
                float(self.exchange_rate) if self.exchange_rate else 1.0000
            ),
            "status": (
                getattr(self.status, "value", self.status) if self.status else None
            ),
            "payment_status": (
                getattr(self.payment_status, "value", self.payment_status)
                if self.payment_status
                else None
            ),
            "payment_method": self.payment_method,
            "payment_terms": self.payment_terms,
            "notes": self.notes,
            "internal_notes": self.internal_notes,
            "reference_number": self.reference_number,
            "po_number": self.po_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "confirmed_at": (
                self.confirmed_at.isoformat() if self.confirmed_at else None
            ),
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
        }

        if include_items:
            data["items"] = [item.to_dict() for item in self.items]
            data["payments"] = [payment.to_dict() for payment in self.payments]

        return data

    def __repr__(self):
        inv_type = self.invoice_type.value if self.invoice_type else "unknown"
        return f"<Invoice {self.invoice_number} ({inv_type})>"


class InvoiceItem(db.Model):
    """عناصر الفاتورة"""

    __tablename__ = "invoice_items"
    __table_args__ = (
        Index("idx_invoice_item_invoice", "invoice_id"),
        Index("idx_invoice_item_product", "product_id"),
        {"extend_existing": True},
    )

    # المعرفات | IDs
    id = Column(Integer, primary_key=True)
    invoice_id = Column(
        Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    # معلومات المنتج | Product info
    product_name = Column(String(200))  # نسخة من اسم المنتج
    product_sku = Column(String(100))  # نسخة من SKU

    # الكميات والأسعار | Quantities and prices
    quantity = Column(Numeric(15, 3), nullable=False, default=0)
    price = Column(Numeric(15, 2), nullable=False, default=0.00)
    discount = Column(Numeric(15, 2), default=0.00)
    tax = Column(Numeric(15, 2), default=0.00)
    total = Column(Numeric(15, 2), nullable=False, default=0.00)

    # معلومات إضافية | Additional info
    notes = Column(Text)

    # التواريخ | Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # العلاقات | Relationships
    invoice = db.relationship("src.models.invoice_unified.Invoice")
    product = db.relationship("src.models.inventory.Product")

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_sku": self.product_sku,
            "quantity": float(self.quantity) if self.quantity else 0,
            "price": float(self.price) if self.price else 0.00,
            "discount": float(self.discount) if self.discount else 0.00,
            "tax": float(self.tax) if self.tax else 0.00,
            "total": float(self.total) if self.total else 0.00,
            "notes": self.notes,
        }

    def __repr__(self):
        return f"<InvoiceItem {self.id} - Invoice {self.invoice_id}>"


class InvoicePayment(db.Model):
    """دفعات الفاتورة"""

    __tablename__ = "invoice_payments"
    __table_args__ = (
        Index("idx_invoice_payment_invoice", "invoice_id"),
        Index("idx_invoice_payment_date", "payment_date"),
        {"extend_existing": True},
    )

    # المعرفات | IDs
    id = Column(Integer, primary_key=True)
    invoice_id = Column(
        Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False
    )

    # معلومات الدفع | Payment info
    amount = Column(Numeric(15, 2), nullable=False)
    payment_date = Column(Date, nullable=False, default=date.today)
    payment_method = Column(
        String(50), default="cash"
    )  # cash, card, bank_transfer, etc.
    reference = Column(String(100))  # رقم مرجعي للدفعة

    # معلومات إضافية | Additional info
    notes = Column(Text)

    # التواريخ | Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("users.id"))

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "amount": float(self.amount) if self.amount else 0.00,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "payment_method": self.payment_method,
            "reference": self.reference,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<InvoicePayment {self.id} - Invoice {self.invoice_id} - Amount {self.amount}>"
