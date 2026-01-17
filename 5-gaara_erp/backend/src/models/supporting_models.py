# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Supporting models for invoices and transactions
All linting disabled due to SQLAlchemy.
"""

from datetime import datetime, timezone
from database import db

# Compatibility alias for routes expecting StockMovement here
try:
    from src.models.inventory import StockMovement as StockMovement  # re-export alias
except (
    Exception
):  # pragma: no cover - inventory model may not be imported at tooling time
    pass


class PaymentMethod(db.Model):
    """طرق الدفع - Payment Methods"""

    __tablename__ = "payment_methods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_en = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, index=True)
    requires_reference = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<PaymentMethod {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "description": self.description,
            "is_active": self.is_active,
            "requires_reference": self.requires_reference,
            "icon": self.icon,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class TaxRate(db.Model):
    """معدلات الضرائب - Tax Rates"""

    __tablename__ = "tax_rates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_en = db.Column(db.String(100))
    rate = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TaxRate {self.name} ({self.rate}%)>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "rate": self.rate,
            "description": self.description,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Unit(db.Model):
    """وحدات القياس - Measurement Units"""

    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    name_en = db.Column(db.String(50))
    symbol = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Unit {self.name} ({self.symbol})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "symbol": self.symbol,
            "description": self.description,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Currency(db.Model):
    """العملات - Currencies"""

    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    code = db.Column(db.String(3), nullable=False, unique=True)  # ISO 4217 code
    symbol = db.Column(db.String(10), nullable=False)
    exchange_rate = db.Column(db.Float, default=1.0)
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Currency {self.code} ({self.symbol})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "code": self.code,
            "symbol": self.symbol,
            "exchange_rate": self.exchange_rate,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class InvoiceStatus(db.Model):
    """حالات الفواتير - Invoice Statuses"""

    __tablename__ = "invoice_statuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    name_en = db.Column(db.String(50))
    description = db.Column(db.Text)
    color = db.Column(db.String(20))
    icon = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True, index=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<InvoiceStatus {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "description": self.description,
            "color": self.color,
            "icon": self.icon,
            "is_active": self.is_active,
            "sort_order": self.sort_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class DiscountType(db.Model):
    """أنواع الخصومات - Discount Types"""

    __tablename__ = "discount_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    name_en = db.Column(db.String(50))
    type = db.Column(db.String(20), nullable=False)  # 'percentage' or 'fixed'
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<DiscountType {self.name} ({self.type})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "type": self.type,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Payment(db.Model):
    """المدفوعات - Payments"""

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, nullable=True)
    payment_method_id = db.Column(db.Integer, db.ForeignKey("payment_methods.id"))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    reference_number = db.Column(db.String(100))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default="completed")  # completed, pending, failed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    payment_method = db.relationship(
        "src.models.supporting_models.PaymentMethod", backref="payments"
    )

    def __repr__(self):
        return f"<Payment {self.id} - {self.amount}>"

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "payment_method_id": self.payment_method_id,
            "amount": self.amount,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "reference_number": self.reference_number,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
