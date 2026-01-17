# -*- coding: utf-8 -*-
"""
نموذج مهندسي المبيعات
SalesEngineer Model for Complete Inventory System
"""

from datetime import datetime, timezone

try:
    from src.database import db
except ImportError:
    from database import db


class SalesEngineer(db.Model):
    """نموذج مهندسي المبيعات"""

    __tablename__ = "sales_engineers"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))

    # User association
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Employee info
    employee_id = db.Column(db.String(50), unique=True, nullable=True)
    department = db.Column(db.String(100))
    title = db.Column(db.String(100))

    # Commission and performance
    commission_rate = db.Column(db.Float, default=0.0)  # 0-100%
    target_amount = db.Column(db.Numeric(15, 2), default=0.00)
    current_sales = db.Column(db.Numeric(15, 2), default=0.00)

    # Status
    is_active = db.Column(db.Boolean, default=True, index=True)
    notes = db.Column(db.Text)

    # Relationships
    user = db.relationship("src.models.user.User", viewonly=True)
    customers = db.relationship("Customer", backref="sales_engineer", lazy="dynamic")

    # System timestamps
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<SalesEngineer {self.name}>"

    def to_dict(self, include_customers=False):
        """تحويل النموذج إلى قاموس"""
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "employee_id": self.employee_id,
            "department": self.department,
            "title": self.title,
            "commission_rate": float(self.commission_rate),
            "target_amount": (float(self.target_amount) if self.target_amount else 0.0),
            "current_sales": (float(self.current_sales) if self.current_sales else 0.0),
            "is_active": self.is_active,
            "notes": self.notes,
            "user_id": self.user_id,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }

        if include_customers:
            data["customers_count"] = self.customers.filter_by(is_active=True).count()

        return data

    @classmethod
    def get_active(cls):
        """الحصول على مهندسي المبيعات النشطين"""
        return cls.query.filter_by(is_active=True).order_by(cls.name).all()

    @classmethod
    def get_by_user_id(cls, user_id: int):
        """الحصول على مهندس المبيعات بواسطة معرف المستخدم"""
        return cls.query.filter_by(user_id=user_id).first()

    def update_sales(self, amount):
        """تحديث مبيعات مهندس المبيعات"""
        if self.current_sales:
            self.current_sales = float(self.current_sales) + float(amount)
        else:
            self.current_sales = float(amount)
        db.session.commit()

    def get_commission(self):
        """حساب عمولة مهندس المبيعات"""
        if self.current_sales and self.commission_rate:
            sales = float(self.current_sales)
            rate = float(self.commission_rate) / 100
            return sales * rate
        return 0.0
