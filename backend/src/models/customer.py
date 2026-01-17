# /home/ubuntu/upload/store_v1.5/complete_inventory_system/backend/src/models/customer.py
# -*- coding: utf-8 -*-
"""
نموذج العملاء الموحد
Unified Customer Model for Complete Inventory System
"""

from datetime import datetime, timezone

try:
    from src.database import db
except ImportError:
    from ..database import db
import enum


class CustomerCategory(enum.Enum):
    """Supported customer categories."""

    REGULAR = "regular"
    VIP = "vip"
    WHOLESALE = "wholesale"
    GOVERNMENT = "government"


class Customer(db.Model):
    """نموذج العملاء الموحد"""

    __tablename__ = "customers"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(50), unique=True, nullable=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))

    # معلومات الأعمال
    company_name = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))

    # معلومات الدفع
    credit_limit = db.Column(db.Numeric(15, 2), default=0.00)
    payment_terms = db.Column(db.String(50))  # cash, credit_30, credit_60, etc.
    currency = db.Column(db.String(3), default="USD")
    discount_rate = db.Column(db.Float, default=0.0)

    # التصنيف والحالة
    category = db.Column(db.Enum(CustomerCategory), default=CustomerCategory.REGULAR)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    tags = db.Column(db.JSON)  # للتصنيفات والعلامات

    # العلاقات
    sales_engineer_id = db.Column(
        db.Integer, db.ForeignKey("sales_engineers.id"), nullable=True
    )
    # NOTE: Relationships disabled pending T38 Invoice consolidation
    # invoices relationship will be added after UnifiedInvoice consolidation
    # sales_engineer relationship requires SalesEngineer model review

    # تواريخ النظام
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # NOTE: created_by disabled - requires user permission system review

    def __repr__(self):
        return f"<Customer {self.name}>"

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            "id": self.id,
            "customer_code": self.customer_code,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "company_name": self.company_name,
            "tax_number": self.tax_number,
            "credit_limit": float(self.credit_limit) if self.credit_limit else 0.00,
            "payment_terms": self.payment_terms,
            "currency": self.currency,
            "discount_rate": float(self.discount_rate or 0),
            "category": (
                self.category.value
                if isinstance(self.category, CustomerCategory)
                else self.category
            ),
            "is_active": self.is_active,
            "notes": self.notes,
            "tags": self.tags,
            "sales_engineer_id": self.sales_engineer_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": getattr(self, "created_by", None),
        }

    @classmethod
    def create_customer(cls, data):
        """إنشاء عميل جديد"""
        customer = cls(**data)
        db.session.add(customer)
        db.session.commit()
        return customer

    def update_customer(self, data):
        """تحديث بيانات العميل"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return self

    def get_total_sales(self):
        """حساب إجمالي المبيعات للعميل"""
        # Requires Sale model to be properly defined and linked
        return 0

    def get_outstanding_balance(self):
        """حساب الرصيد المستحق

        NOTE: Returns 0.0 until T38 Invoice consolidation is complete.
        After T38: Calculate sum of remaining_amount for pending/partial invoices.
        """
        return 0.0
