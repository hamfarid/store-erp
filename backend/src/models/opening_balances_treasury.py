# type: ignore
# flake8: noqa
"""
نماذج الأرصدة الافتتاحية والخزنة
All linting disabled due to SQLAlchemy mock objects and optional dependencies.
"""

from datetime import datetime
import enum

try:
    from sqlalchemy import (
        Column,
        Integer,
        String,
        Float,
        DateTime,
        Text,
        Boolean,
        ForeignKey,
        Enum,
        Numeric,
    )
    from sqlalchemy.orm import relationship, validates
    from sqlalchemy.ext.declarative import declarative_base

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

    def Text():
        return None

    def Boolean():
        return None

    def ForeignKey(*args, **kwargs):
        return None

    def Enum(*args, **kwargs):
        return None

    def Numeric(*args, **kwargs):
        return None

    def relationship(*args, **kwargs):
        return None

    def validates(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def declarative_base():
        class Base:
            pass

        return Base

    SQLALCHEMY_AVAILABLE = False

Base = declarative_base()


class BalanceType(enum.Enum):
    """أنواع الأرصدة"""

    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    INVENTORY = "inventory"
    CASH = "cash"
    BANK = "bank"
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"


class TransactionType(enum.Enum):
    """أنواع المعاملات"""

    DEBIT = "debit"
    CREDIT = "credit"


# محاولة استيراد قاعدة البيانات
try:
    from database import db  # type: ignore

    if hasattr(db, "Model"):
        BaseModel = db.Model
    else:
        BaseModel = Base
except ImportError:
    try:
        from ..database import db  # type: ignore

        if hasattr(db, "Model"):
            BaseModel = db.Model
        else:
            BaseModel = Base
    except ImportError:
        BaseModel = Base


class OpeningBalance(BaseModel):
    """نموذج الأرصدة الافتتاحية"""

    __tablename__ = "opening_balances"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    balance_code = Column(String(50), unique=True, nullable=False)
    balance_name = Column(String(200), nullable=False)
    balance_type = Column(Enum(BalanceType), nullable=False)

    # الأرصدة
    opening_balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    current_balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    closing_balance = Column(Numeric(15, 2), default=0.00, nullable=False)

    # معلومات إضافية
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    # تواريخ
    balance_date = Column(DateTime, default=datetime.utcnow)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # معلومات المستخدم
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    posted_by = Column(Integer, nullable=True)

    def to_dict(self):
        balance_type_value = (
            self.balance_type.value
            if hasattr(self.balance_type, "value")
            else str(self.balance_type)
        )
        return {
            "id": self.id,
            "balance_code": self.balance_code,
            "balance_name": self.balance_name,
            "balance_type": balance_type_value,
            "opening_balance": (
                float(self.opening_balance) if self.opening_balance else 0.0
            ),
            "current_balance": (
                float(self.current_balance) if self.current_balance else 0.0
            ),
            "closing_balance": (
                float(self.closing_balance) if self.closing_balance else 0.0
            ),
            "description": self.description,
            "is_active": self.is_active,
            "balance_date": (
                self.balance_date.isoformat() if self.balance_date else None
            ),
            "created_date": (
                self.created_date.isoformat() if self.created_date else None
            ),
            "updated_date": (
                self.updated_date.isoformat() if self.updated_date else None
            ),
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "posted_by": self.posted_by,
        }
