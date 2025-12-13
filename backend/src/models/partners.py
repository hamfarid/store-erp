# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
partners - نموذج أساسي
All linting disabled due to SQLAlchemy mock objects and optional dependencies.
"""

from datetime import datetime, timezone
import enum

try:
    from sqlalchemy import (
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
    )
    from sqlalchemy.orm import relationship

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # SQLAlchemy not available - create mock objects
    def Column(*args, **kwargs):
        return None

    def Integer():
        return None

    def String(length=None):
        return None

    def Float():
        return None

    def DateTime():
        return None

    def Boolean():
        return None

    def Text():
        return None

    def Enum(*args, **kwargs):
        return None

    def Date():
        return None

    def ForeignKey(*args, **kwargs):
        return None

    def Numeric(*args, **kwargs):
        return None

    def relationship(*args, **kwargs):
        return None

    SQLALCHEMY_AVAILABLE = False

# محاولة استيراد قاعدة البيانات – استخدم نفس الـ db الموحد من models.user أولاً
try:
    from database import db  # type: ignore
except ImportError:
    try:
        from database import db  # type: ignore
    except ImportError:
        # إنشاء mock db إذا لم تكن متوفرة
        class MockDB:
            class Model:
                def __init__(self, **kwargs):
                    for key, value in kwargs.items():
                        setattr(self, key, value)

                def to_dict(self):
                    return {}

            Column = Column
            Integer = Integer
            String = String
            Float = Float
            DateTime = DateTime
            Boolean = Boolean
            Text = Text
            Enum = Enum
            Date = Date
            ForeignKey = ForeignKey
            Numeric = Numeric
            relationship = relationship

        db = MockDB()


# ==================== Enumerations ====================


class SalesEngineerStatus(enum.Enum):
    """Available statuses for sales engineers."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class PaymentStatus(enum.Enum):
    """Shared payment status values reused across modules."""

    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


# نماذج أساسية للاختبار
class BasicModel(db.Model):
    """نموذج أساسي للاختبار"""

    __tablename__ = "basic_model"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SalesEngineer(db.Model):
    """نموذج مهندسي المبيعات"""

    __tablename__ = "sales_engineers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    email = Column(String(150))
    phone = Column(String(50))
    mobile = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    commission_rate = Column(Float, default=0.0)
    target_monthly = Column(Float, default=0.0)
    status = Column(Enum(SalesEngineerStatus), default=SalesEngineerStatus.ACTIVE)
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    if SQLALCHEMY_AVAILABLE:
        # customers = relationship('Customer', back_populates='sales_engineer', cascade='all, delete-orphan')
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "commission_rate": float(self.commission_rate or 0),
            "target_monthly": float(self.target_monthly or 0),
            "status": (
                self.status.value
                if isinstance(self.status, SalesEngineerStatus)
                else self.status
            ),
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_date": (
                self.updated_date.isoformat() if self.updated_date else None
            ),
        }


class CustomerType:
    """Mock CustomerType class for compatibility"""

    pass


class ExchangeRate(db.Model):
    """نموذج أسعار الصرف لتقارير العملات"""

    __tablename__ = "exchange_rates"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    base_currency = Column(String(3), nullable=False, default="EGP")
    target_currency = Column(String(3), nullable=False, default="USD")
    rate = Column(Float, nullable=False, default=1.0)
    date = Column(Date, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "base_currency": self.base_currency,
            "target_currency": self.target_currency,
            "rate": float(self.rate or 0),
            "date": (
                self.date.isoformat()
                if hasattr(self.date, "isoformat")
                else str(self.date) if self.date else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
