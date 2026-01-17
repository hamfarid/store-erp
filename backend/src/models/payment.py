#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.86: Payment Tracking System

Models for tracking payments, refunds, and payment methods.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from src.database import db
from enum import Enum
from src.models.invoice import Invoice


class PaymentStatus(str, Enum):
    """Payment status."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIAL_REFUND = "partial_refund"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Payment methods."""

    CASH = "cash"
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CREDIT = "credit"
    MADA = "mada"
    APPLE_PAY = "apple_pay"
    STC_PAY = "stc_pay"
    OTHER = "other"


class Payment(db.Model):
    """
    P2.86: Payment record model.
    """

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    payment_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Reference (invoice, order, etc.)
    reference_type = db.Column(db.String(50), nullable=False)  # invoice, purchase_order
    reference_id = db.Column(db.Integer, nullable=False, index=True)
    reference_number = db.Column(db.String(50))

    # Customer/Supplier
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))

    # Payment details
    payment_method = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), default=PaymentStatus.PENDING.value, index=True)

    # Amounts
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default="EGP")
    exchange_rate = db.Column(db.Float, default=1.0)
    amount_in_base = db.Column(db.Float)

    # Transaction details
    transaction_id = db.Column(db.String(100))
    transaction_ref = db.Column(db.String(100))
    gateway = db.Column(db.String(50))

    # Card details (masked)
    card_last_four = db.Column(db.String(4))
    card_brand = db.Column(db.String(20))

    # Bank details
    bank_name = db.Column(db.String(100))
    bank_account = db.Column(db.String(50))
    check_number = db.Column(db.String(50))

    # Dates
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    cleared_date = db.Column(db.DateTime)

    # Notes
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)

    # Metadata
    metadata = db.Column(db.JSON)

    # User and timestamps
    received_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    customer = db.relationship("Customer", backref="payments")
    refunds = db.relationship(
        "PaymentRefund", back_populates="payment", cascade="all, delete-orphan"
    )

    @property
    def method_ar(self) -> str:
        """Get Arabic payment method name."""
        translations = {
            PaymentMethod.CASH.value: "نقداً",
            PaymentMethod.CARD.value: "بطاقة",
            PaymentMethod.BANK_TRANSFER.value: "تحويل بنكي",
            PaymentMethod.CHECK.value: "شيك",
            PaymentMethod.CREDIT.value: "آجل",
            PaymentMethod.MADA.value: "مدى",
            PaymentMethod.APPLE_PAY.value: "Apple Pay",
            PaymentMethod.STC_PAY.value: "STC Pay",
            PaymentMethod.OTHER.value: "أخرى",
        }
        return translations.get(self.payment_method, self.payment_method)

    @property
    def status_ar(self) -> str:
        """Get Arabic status."""
        translations = {
            PaymentStatus.PENDING.value: "معلق",
            PaymentStatus.COMPLETED.value: "مكتمل",
            PaymentStatus.FAILED.value: "فشل",
            PaymentStatus.REFUNDED.value: "مسترد",
            PaymentStatus.PARTIAL_REFUND.value: "استرداد جزئي",
            PaymentStatus.CANCELLED.value: "ملغي",
        }
        return translations.get(self.status, self.status)

    @property
    def refunded_amount(self) -> float:
        """Get total refunded amount."""
        return sum(r.amount for r in self.refunds if r.status == "completed")

    @property
    def net_amount(self) -> float:
        """Get net amount after refunds."""
        return self.amount - self.refunded_amount

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "payment_number": self.payment_number,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "reference_number": self.reference_number,
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else None,
            "supplier_id": self.supplier_id,
            "payment_method": self.payment_method,
            "method_ar": self.method_ar,
            "status": self.status,
            "status_ar": self.status_ar,
            "amount": self.amount,
            "currency": self.currency,
            "refunded_amount": self.refunded_amount,
            "net_amount": self.net_amount,
            "transaction_id": self.transaction_id,
            "card_last_four": self.card_last_four,
            "card_brand": self.card_brand,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def generate_payment_number() -> str:
        """Generate unique payment number."""
        today = datetime.utcnow()
        prefix = f"PAY{today.strftime('%Y%m%d')}"

        last = (
            Payment.query.filter(Payment.payment_number.like(f"{prefix}%"))
            .order_by(Payment.id.desc())
            .first()
        )

        if last:
            last_num = int(last.payment_number[-4:])
            new_num = last_num + 1
        else:
            new_num = 1

        return f"{prefix}{new_num:04d}"


class PaymentRefund(db.Model):
    """Payment refund record."""

    __tablename__ = "payment_refunds"

    id = db.Column(db.Integer, primary_key=True)
    refund_number = db.Column(db.String(50), unique=True, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=False)

    # Amount
    amount = db.Column(db.Float, nullable=False)

    # Status
    status = db.Column(db.String(20), default="pending")

    # Reason
    reason = db.Column(db.String(200))
    notes = db.Column(db.Text)

    # Transaction
    transaction_id = db.Column(db.String(100))

    # Dates
    refund_date = db.Column(db.DateTime, default=datetime.utcnow)

    # User
    processed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    payment = db.relationship("Payment", back_populates="refunds")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "refund_number": self.refund_number,
            "payment_id": self.payment_id,
            "amount": self.amount,
            "status": self.status,
            "reason": self.reason,
            "notes": self.notes,
            "refund_date": self.refund_date.isoformat() if self.refund_date else None,
        }


class PaymentAllocation(db.Model):
    """Allocation of payment to specific invoices."""

    __tablename__ = "payment_allocations"

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)

    # Amount allocated
    amount = db.Column(db.Float, nullable=False)

    # Dates
    allocation_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Notes
    notes = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "payment_id": self.payment_id,
            "invoice_id": self.invoice_id,
            "amount": self.amount,
            "allocation_date": (
                self.allocation_date.isoformat() if self.allocation_date else None
            ),
        }


# =============================================================================
# Payment Service
# =============================================================================


class PaymentService:
    """Service for managing payments."""

    @staticmethod
    def create_payment(
        reference_type: str,
        reference_id: int,
        amount: float,
        payment_method: str,
        customer_id: int = None,
        supplier_id: int = None,
        transaction_id: str = None,
        notes: str = None,
        user_id: int = None,
    ) -> Payment:
        """Create a new payment record."""
        payment = Payment(
            payment_number=Payment.generate_payment_number(),
            reference_type=reference_type,
            reference_id=reference_id,
            amount=amount,
            payment_method=payment_method,
            customer_id=customer_id,
            supplier_id=supplier_id,
            transaction_id=transaction_id,
            status=PaymentStatus.COMPLETED.value,
            notes=notes,
            received_by=user_id,
        )

        db.session.add(payment)
        db.session.commit()

        return payment

    @staticmethod
    def process_refund(
        payment_id: int, amount: float, reason: str, user_id: int = None
    ) -> PaymentRefund:
        """Process a payment refund."""
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        if amount > payment.net_amount:
            raise ValueError("Refund amount exceeds available balance")

        refund = PaymentRefund(
            refund_number=f"REF{payment.payment_number[3:]}",
            payment_id=payment_id,
            amount=amount,
            reason=reason,
            status="completed",
            processed_by=user_id,
        )

        # Update payment status
        if payment.refunded_amount + amount >= payment.amount:
            payment.status = PaymentStatus.REFUNDED.value
        else:
            payment.status = PaymentStatus.PARTIAL_REFUND.value

        db.session.add(refund)
        db.session.commit()

        return refund

    @staticmethod
    def get_customer_balance(customer_id: int) -> Dict[str, float]:
        """Get customer payment balance."""
        from sqlalchemy import func

        # Total invoiced
        total_invoiced = (
            db.session.query(func.sum(Invoice.total))
            .filter_by(customer_id=customer_id)
            .scalar()
            or 0
        )

        # Total paid
        total_paid = (
            db.session.query(func.sum(Payment.amount))
            .filter_by(customer_id=customer_id, status=PaymentStatus.COMPLETED.value)
            .scalar()
            or 0
        )

        # Total refunded
        total_refunded = (
            db.session.query(func.sum(PaymentRefund.amount))
            .join(Payment)
            .filter(
                Payment.customer_id == customer_id, PaymentRefund.status == "completed"
            )
            .scalar()
            or 0
        )

        from src.models.invoice import Invoice

        return {
            "total_invoiced": total_invoiced,
            "total_paid": total_paid - total_refunded,
            "balance": total_invoiced - (total_paid - total_refunded),
        }


__all__ = [
    "Payment",
    "PaymentRefund",
    "PaymentAllocation",
    "PaymentStatus",
    "PaymentMethod",
    "PaymentService",
]
