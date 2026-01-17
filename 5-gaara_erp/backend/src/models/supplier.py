# /home/ubuntu/upload/store_v1.5/complete_inventory_system/backend/src/models/supplier.py
# -*- coding: utf-8 -*-
"""
نموذج الموردين
Supplier Model for Complete Inventory System
"""

from datetime import datetime, timezone
from src.database import db


class Supplier(db.Model):
    """نموذج الموردين"""

    __tablename__ = "suppliers"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    website = db.Column(db.String(200))

    # معلومات العنوان
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))

    # معلومات الأعمال
    company_name = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    supplier_type = db.Column(db.String(20), default="company")  # individual, company

    # معلومات الدفع والشروط
    payment_terms = db.Column(db.String(50))  # cash, credit_30, credit_60, etc.
    preferred_payment_method = db.Column(db.String(50))
    currency = db.Column(db.String(3), default="USD")
    bank_account = db.Column(db.String(100))

    # معلومات الاتصال
    contact_person = db.Column(db.String(200))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))

    # التقييم والجودة
    rating = db.Column(db.Float, default=0.0)  # تقييم من 1-5
    quality_score = db.Column(db.Float, default=0.0)
    delivery_score = db.Column(db.Float, default=0.0)

    # حالة المورد
    is_active = db.Column(db.Boolean, default=True)
    is_preferred = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    tags = db.Column(db.JSON)  # للتصنيفات والعلامات

    # تواريخ النظام
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    # العلاقات
    # purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy='dynamic')  # Disabled until PurchaseOrder model is defined
    # products = db.relationship('Product', backref='preferred_supplier',
    # lazy='dynamic')  # May cause conflicts with existing Product model

    def __repr__(self):
        return f"<Supplier {self.name}>"

    def to_dict(self):
        """تحويل النموذج إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "website": self.website,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "company_name": self.company_name,
            "tax_number": self.tax_number,
            "supplier_type": self.supplier_type,
            "payment_terms": self.payment_terms,
            "preferred_payment_method": self.preferred_payment_method,
            "currency": self.currency,
            "bank_account": self.bank_account,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "rating": self.rating,
            "quality_score": self.quality_score,
            "delivery_score": self.delivery_score,
            "is_active": self.is_active,
            "is_preferred": self.is_preferred,
            "notes": self.notes,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
        }

    @classmethod
    def create_supplier(cls, data):
        """إنشاء مورد جديد"""
        supplier = cls(**data)
        db.session.add(supplier)
        db.session.commit()
        return supplier

    def update_supplier(self, data):
        """تحديث بيانات المورد"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return self

    def get_total_purchases(self):
        """حساب إجمالي المشتريات من المورد"""
        return sum(
            po.total_amount for po in self.purchase_orders if po.status == "completed"
        )

    def get_average_rating(self):
        """حساب متوسط التقييم"""
        if self.rating and self.quality_score and self.delivery_score:
            return (self.rating + self.quality_score + self.delivery_score) / 3
        return 0.0

    def update_rating(self, new_rating, quality_score=None, delivery_score=None):
        """تحديث التقييم"""
        self.rating = new_rating
        if quality_score:
            self.quality_score = quality_score
        if delivery_score:
            self.delivery_score = delivery_score
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
