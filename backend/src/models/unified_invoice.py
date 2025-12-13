# -*- coding: utf-8 -*-
"""
نموذج الفاتورة الموحد - يدعم جميع أنواع الفواتير
Unified Invoice Model - Supports all invoice types
"""

from datetime import datetime
import enum

try:
    from sqlalchemy import (  # type: ignore
        Column,
        Integer,
        String,
        Float,
        DateTime,
        Boolean,
        Text,
        Enum,
        Date,
        ForeignKey,
        Numeric,
        JSON,
    )
    from sqlalchemy.orm import relationship  # type: ignore

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # Mock objects for when SQLAlchemy is not available
    def Column(*_args, **_kwargs):  # type: ignore
        return None

    def Integer():  # type: ignore
        return None

    def String(_length=None):  # type: ignore
        return None

    def Float():  # type: ignore
        return None

    def DateTime():  # type: ignore
        return None

    def Boolean():  # type: ignore
        return None

    def Text():  # type: ignore
        return None

    def Enum(*_args, **_kwargs):  # type: ignore
        return None

    def Date():  # type: ignore
        return None

    def ForeignKey(*_args, **_kwargs):  # type: ignore
        return None

    def Numeric(*_args, **_kwargs):  # type: ignore
        return None

    def JSON():  # type: ignore
        return None

    def relationship(*_args, **_kwargs):  # type: ignore
        return None

    SQLALCHEMY_AVAILABLE = False

# استيراد قاعدة البيانات
from src.database import db  # type: ignore


# تعدادات الفاتورة الموحدة
class InvoiceType(enum.Enum):
    """أنواع الفواتير"""

    SALES = "sales"  # فاتورة مبيعات
    PURCHASE = "purchase"  # فاتورة مشتريات
    RETURN_SALES = "return_sales"  # مرتجع مبيعات
    RETURN_PURCHASE = "return_purchase"  # مرتجع مشتريات
    IMPORT = "import"  # فاتورة استيراد
    EXPORT = "export"  # فاتورة تصدير
    SERVICE = "service"  # فاتورة خدمة


class InvoiceStatus(enum.Enum):
    """حالات الفاتورة"""

    DRAFT = "draft"  # مسودة
    PENDING = "pending"  # في الانتظار
    CONFIRMED = "confirmed"  # مؤكدة
    PAID = "paid"  # مدفوعة
    PARTIAL_PAID = "partial_paid"  # مدفوعة جزئياً
    OVERDUE = "overdue"  # متأخرة
    CANCELLED = "cancelled"  # ملغية
    REFUNDED = "refunded"  # مستردة


class PaymentMethod(enum.Enum):
    """طرق الدفع"""

    CASH = "cash"  # نقداً
    CREDIT_CARD = "credit_card"  # بطاقة ائتمان
    BANK_TRANSFER = "bank_transfer"  # تحويل بنكي
    CHECK = "check"  # شيك
    INSTALLMENT = "installment"  # تقسيط
    CREDIT = "credit"  # آجل


class UnifiedInvoice(db.Model):  # type: ignore
    """نموذج الفاتورة الموحد"""

    __tablename__ = "unified_invoices"
    __table_args__ = {"extend_existing": True}

    # المعرفات الأساسية
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    reference_number = Column(String(50))  # رقم مرجعي

    # نوع وحالة الفاتورة
    invoice_type = Column(Enum(InvoiceType), nullable=False, default=InvoiceType.SALES)
    status = Column(Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.DRAFT)

    # التواريخ
    invoice_date = Column(Date, nullable=False, default=datetime.utcnow)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات مع العملاء والموردين
    customer_id = Column(Integer, ForeignKey("customers.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    # المبالغ المالية
    subtotal = Column(Numeric(15, 3), default=0.000)  # المجموع الفرعي
    tax_amount = Column(Numeric(15, 3), default=0.000)  # قيمة الضريبة
    discount_amount = Column(Numeric(15, 3), default=0.000)  # قيمة الخصم
    # تكلفة الشحن
    shipping_cost = Column(Numeric(15, 3), default=0.000)
    # المجموع الكلي
    total_amount = Column(Numeric(15, 3), nullable=False, default=0.000)
    # المبلغ المدفوع
    paid_amount = Column(Numeric(15, 3), default=0.000)
    remaining_amount = Column(Numeric(15, 3), default=0.000)  # المبلغ المتبقي

    # معلومات الدفع
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    payment_terms = Column(String(200))  # شروط الدفع

    # العملة والضريبة
    currency = Column(String(3), default="SAR")  # العملة
    tax_rate = Column(Float, default=15.0)  # معدل الضريبة

    # معلومات إضافية
    notes = Column(Text)  # ملاحظات
    internal_notes = Column(Text)  # ملاحظات داخلية
    terms_conditions = Column(Text)  # الشروط والأحكام

    # معلومات المستخدم والمخزن
    created_by = Column(Integer, ForeignKey("users.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))

    # معلومات متقدمة (JSON للمرونة)
    extra_data = Column(JSON)  # بيانات إضافية مرنة

    # العلاقات
    customer = relationship("src.models.customer.Customer")
    supplier = relationship("src.models.supplier.Supplier")
    items = relationship(
        "src.models.unified_invoice.UnifiedInvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
    )
    # NOTE: payments relationship disabled - InvoicePayment
    # references 'invoices' table,
    # but this model uses 'unified_invoices'.
    # Fix during T38 Invoice consolidation.
    # payments = relationship(
    #   "src.models.invoice_unified.InvoicePayment",
    #   back_populates="invoice",
    #   cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<UnifiedInvoice {self.invoice_number}: "
            f"{self.total_amount} {self.currency}>"
        )

    @property
    def is_paid(self):
        """التحقق من دفع الفاتورة بالكامل"""
        paid = self.paid_amount or 0
        total = self.total_amount or 0
        return paid >= total

    @property
    def is_overdue(self):
        """التحقق من تأخر الفاتورة"""
        if self.due_date is not None and not self.is_paid:
            return datetime.now().date() > self.due_date
        return False

    def calculate_totals(self):
        """حساب المجاميع تلقائياً"""
        items = self.items or []
        self.subtotal = sum((item.total_amount or 0) for item in items)
        tax_rate = self.tax_rate or 0
        self.tax_amount = (self.subtotal or 0) * (tax_rate / 100)
        self.total_amount = (
            (self.subtotal or 0)
            + (self.tax_amount or 0)
            - (self.discount_amount or 0)
            + (self.shipping_cost or 0)
        )
        self.remaining_amount = (self.total_amount or 0) - (self.paid_amount or 0)

        # تحديث الحالة حسب الدفع
        paid = self.paid_amount or 0
        total = self.total_amount or 0
        if paid == 0:
            self.status = InvoiceStatus.CONFIRMED
        elif paid >= total:
            self.status = InvoiceStatus.PAID
        else:
            self.status = InvoiceStatus.PARTIAL_PAID


class UnifiedInvoiceItem(db.Model):  # type: ignore
    """عناصر الفاتورة الموحدة"""

    __tablename__ = "unified_invoice_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("unified_invoices.id"), nullable=False)

    # معلومات المنتج
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String(200), nullable=False)  # اسم المنتج
    product_code = Column(String(50))  # كود المنتج
    description = Column(Text)  # وصف العنصر

    # الكميات والأسعار
    quantity = Column(Numeric(15, 3), nullable=False, default=1.000)
    unit_price = Column(Numeric(15, 3), nullable=False, default=0.000)
    discount_percentage = Column(Float, default=0.0)  # نسبة الخصم
    discount_amount = Column(Numeric(15, 3), default=0.000)  # مبلغ الخصم
    tax_rate = Column(Float, default=15.0)  # معدل الضريبة للعنصر
    tax_amount = Column(Numeric(15, 3), default=0.000)  # مبلغ الضريبة
    total_amount = Column(Numeric(15, 3), nullable=False, default=0.000)  # المجموع

    # معلومات إضافية
    unit = Column(String(20), default="قطعة")  # وحدة القياس
    notes = Column(Text)  # ملاحظات العنصر

    # العلاقات
    invoice = relationship(
        "src.models.unified_invoice.UnifiedInvoice", back_populates="items"
    )

    def __repr__(self):
        return (
            f"<InvoiceItem {self.product_name}: "
            f"{self.quantity} x {self.unit_price}>"
        )

    def calculate_total(self):
        """حساب مجموع العنصر"""
        subtotal = (self.quantity or 0) * (self.unit_price or 0)
        discount_pct = (self.discount_percentage or 0) / 100
        discount = subtotal * discount_pct + (self.discount_amount or 0)
        taxable_amount = subtotal - discount
        tax_rate = (self.tax_rate or 0) / 100
        self.tax_amount = taxable_amount * tax_rate
        self.total_amount = taxable_amount + self.tax_amount


# NOTE: InvoicePayment moved to invoice_unified.py to avoid duplication
# Import from there: from src.models.invoice_unified import InvoicePayment
# class InvoicePayment(db.Model):
#     """مدفوعات الفاتورة"""
#     __tablename__ = 'invoice_payments'
#     ...

# تصدير النماذج
__all__ = [
    "UnifiedInvoice",
    "UnifiedInvoiceItem",
    # 'InvoicePayment',  # Removed - use from invoice_unified.py
    "InvoiceType",
    "InvoiceStatus",
    "PaymentMethod",
]
