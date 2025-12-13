# type: ignore
# flake8: noqa
"""
نماذج الفواتير
All linting disabled due to SQLAlchemy mock objects and optional dependencies.
"""

from datetime import datetime, timezone

try:
    from sqlalchemy import (
        Column,
        Integer,
        String,
        Text,
        DateTime,
        Boolean,
        Float,
        Date,
        ForeignKey,
        JSON,
        Numeric,
    )
    from sqlalchemy.orm import relationship
    from flask_sqlalchemy import SQLAlchemy
    from database import db  # type: ignore

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # SQLAlchemy not available - create mock objects
    def Column(*args, **kwargs):
        return None

    def Integer():
        return None

    def String(length=None):
        return None

    def Text():
        return None

    def DateTime():
        return None

    def Boolean():
        return None

    def Float():
        return None

    def Date():
        return None

    def ForeignKey(*args, **kwargs):
        return None

    def JSON():
        return None

    def Numeric(*args, **kwargs):
        return None

    def relationship(*args, **kwargs):
        return None

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
        Text = Text
        DateTime = DateTime
        Boolean = Boolean
        Float = Float
        Date = Date
        ForeignKey = ForeignKey
        JSON = JSON
        Numeric = Numeric
        relationship = relationship

    db = MockDB()
    SQLALCHEMY_AVAILABLE = False


class InvoiceCurrency(db.Model):
    """نموذج عملات الفواتير"""

    __tablename__ = "invoice_currencies"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    symbol = Column(String(10))
    exchange_rate = Column(Float, default=1.0)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "symbol": self.symbol,
            "exchange_rate": self.exchange_rate,
            "is_default": self.is_default,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class ImportInvoice(db.Model):
    """نموذج فواتير الاستيراد"""

    __tablename__ = "import_invoices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), nullable=False)
    year = Column(Integer)
    financial_year = Column(String(20))
    invoice_date = Column(Date)
    shipping_date = Column(Date)
    due_date = Column(Date)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    invoice_value_eur = Column(Numeric(15, 2))
    payment_status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "year": self.year,
            "financial_year": self.financial_year,
            "invoice_date": (
                self.invoice_date.isoformat() if self.invoice_date else None
            ),
            "shipping_date": (
                self.shipping_date.isoformat() if self.shipping_date else None
            ),
            "due_date": (self.due_date.isoformat() if self.due_date else None),
            "supplier_id": self.supplier_id,
            "invoice_value_eur": (
                float(self.invoice_value_eur) if self.invoice_value_eur else 0
            ),
            "payment_status": self.payment_status,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class InvoiceDetail(db.Model):
    """نموذج تفاصيل الفواتير"""

    __tablename__ = "invoice_details"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("import_invoices.id"))
    product_name = Column(String(200))
    quantity = Column(Numeric(10, 2))
    unit_price = Column(Numeric(10, 2))
    total_price = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "product_name": self.product_name,
            "quantity": float(self.quantity) if self.quantity else 0,
            "unit_price": float(self.unit_price) if self.unit_price else 0,
            "total_price": float(self.total_price) if self.total_price else 0,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class Payment(db.Model):
    """نموذج المدفوعات"""

    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("import_invoices.id"))
    amount = Column(Numeric(15, 2))
    payment_date = Column(Date)
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "amount": float(self.amount) if self.amount else 0,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "payment_method": self.payment_method,
            "notes": self.notes,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class InvoiceSummary(db.Model):
    """نموذج ملخص الفواتير"""

    __tablename__ = "invoice_summaries"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    total_invoices = Column(Integer, default=0)
    total_value = Column(Numeric(15, 2), default=0)
    paid_value = Column(Numeric(15, 2), default=0)
    pending_value = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "total_invoices": self.total_invoices,
            "total_value": float(self.total_value) if self.total_value else 0,
            "paid_value": float(self.paid_value) if self.paid_value else 0,
            "pending_value": float(self.pending_value) if self.pending_value else 0,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class ExchangeRate(db.Model):
    """نموذج أسعار الصرف"""

    __tablename__ = "exchange_rates"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    from_currency = Column(String(3))
    to_currency = Column(String(3))
    rate = Column(Numeric(10, 4))
    date = Column(Date)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "rate": float(self.rate) if self.rate else 0,
            "date": (self.date.isoformat() if self.date else None),
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class Bank(db.Model):
    """نموذج البنوك"""

    __tablename__ = "banks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20))
    swift_code = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "swift_code": self.swift_code,
            "address": self.address,
            "is_active": self.is_active,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }
