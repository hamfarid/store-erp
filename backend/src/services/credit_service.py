#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.91: Customer Credit Management

Service for managing customer credit limits and transactions.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from src.database import db
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CreditTransactionType(str, Enum):
    """Credit transaction types."""

    CREDIT_GIVEN = "credit_given"  # منح ائتمان
    CREDIT_PAYMENT = "credit_payment"  # سداد ائتمان
    CREDIT_ADJUSTMENT = "credit_adjustment"  # تعديل ائتمان
    INVOICE_CREDIT = "invoice_credit"  # فاتورة آجلة
    CREDIT_RETURN = "credit_return"  # مرتجع ائتماني


class CustomerCredit(db.Model):
    """
    P2.91: Customer credit account.
    """

    __tablename__ = "customer_credits"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), unique=True, nullable=False
    )

    # Credit limits
    credit_limit = db.Column(db.Float, default=0)
    available_credit = db.Column(db.Float, default=0)
    used_credit = db.Column(db.Float, default=0)

    # Balance
    total_outstanding = db.Column(db.Float, default=0)  # المبلغ المستحق

    # Payment terms
    payment_terms_days = db.Column(db.Integer, default=30)  # أيام السداد

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, default=False)
    blocked_reason = db.Column(db.String(200))

    # Risk assessment
    risk_level = db.Column(db.String(20), default="low")  # low, medium, high
    last_payment_date = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    customer = db.relationship("Customer", backref="credit_account")
    transactions = db.relationship(
        "CreditTransaction",
        back_populates="credit_account",
        cascade="all, delete-orphan",
    )

    @property
    def utilization_percent(self) -> float:
        """Calculate credit utilization percentage."""
        if self.credit_limit <= 0:
            return 0
        return round((self.used_credit / self.credit_limit) * 100, 2)

    @property
    def is_overdue(self) -> bool:
        """Check if customer has overdue payments."""
        overdue = CreditTransaction.query.filter(
            CreditTransaction.credit_account_id == self.id,
            CreditTransaction.due_date < datetime.utcnow(),
            CreditTransaction.is_settled == False,
        ).first()
        return overdue is not None

    @property
    def oldest_overdue_days(self) -> int:
        """Get days of oldest overdue amount."""
        oldest = (
            CreditTransaction.query.filter(
                CreditTransaction.credit_account_id == self.id,
                CreditTransaction.due_date < datetime.utcnow(),
                CreditTransaction.is_settled == False,
            )
            .order_by(CreditTransaction.due_date.asc())
            .first()
        )

        if oldest and oldest.due_date:
            return (datetime.utcnow() - oldest.due_date).days
        return 0

    def can_use_credit(self, amount: float) -> tuple:
        """Check if customer can use specified credit amount."""
        if not self.is_active:
            return False, "حساب الائتمان غير نشط"

        if self.is_blocked:
            return False, f"حساب الائتمان محظور: {self.blocked_reason}"

        if amount > self.available_credit:
            return (
                False,
                f"المبلغ المطلوب ({amount}) يتجاوز الائتمان المتاح ({self.available_credit})",
            )

        return True, None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else None,
            "credit_limit": self.credit_limit,
            "available_credit": self.available_credit,
            "used_credit": self.used_credit,
            "utilization_percent": self.utilization_percent,
            "total_outstanding": self.total_outstanding,
            "payment_terms_days": self.payment_terms_days,
            "is_active": self.is_active,
            "is_blocked": self.is_blocked,
            "blocked_reason": self.blocked_reason,
            "risk_level": self.risk_level,
            "is_overdue": self.is_overdue,
            "oldest_overdue_days": self.oldest_overdue_days,
            "last_payment_date": (
                self.last_payment_date.isoformat() if self.last_payment_date else None
            ),
        }


class CreditTransaction(db.Model):
    """Credit transaction record."""

    __tablename__ = "credit_transactions"

    id = db.Column(db.Integer, primary_key=True)
    credit_account_id = db.Column(
        db.Integer, db.ForeignKey("customer_credits.id"), nullable=False
    )

    # Transaction details
    transaction_type = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Balance tracking
    balance_before = db.Column(db.Float)
    balance_after = db.Column(db.Float)

    # Reference
    reference_type = db.Column(db.String(50))  # invoice, payment, adjustment
    reference_id = db.Column(db.Integer)
    reference_number = db.Column(db.String(50))

    # Due date (for credit given)
    due_date = db.Column(db.DateTime)
    is_settled = db.Column(db.Boolean, default=False)
    settled_date = db.Column(db.DateTime)

    # Notes
    notes = db.Column(db.Text)

    # User and timestamps
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    credit_account = db.relationship("CustomerCredit", back_populates="transactions")

    @property
    def type_ar(self) -> str:
        """Get Arabic transaction type."""
        translations = {
            CreditTransactionType.CREDIT_GIVEN.value: "منح ائتمان",
            CreditTransactionType.CREDIT_PAYMENT.value: "سداد ائتمان",
            CreditTransactionType.CREDIT_ADJUSTMENT.value: "تعديل ائتمان",
            CreditTransactionType.INVOICE_CREDIT.value: "فاتورة آجلة",
            CreditTransactionType.CREDIT_RETURN.value: "مرتجع ائتماني",
        }
        return translations.get(self.transaction_type, self.transaction_type)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "credit_account_id": self.credit_account_id,
            "transaction_type": self.transaction_type,
            "type_ar": self.type_ar,
            "amount": self.amount,
            "balance_before": self.balance_before,
            "balance_after": self.balance_after,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "reference_number": self.reference_number,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_settled": self.is_settled,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class CreditService:
    """Service for managing customer credit."""

    @staticmethod
    def get_or_create_credit_account(customer_id: int) -> CustomerCredit:
        """Get or create credit account for customer."""
        credit = CustomerCredit.query.filter_by(customer_id=customer_id).first()

        if not credit:
            credit = CustomerCredit(customer_id=customer_id)
            db.session.add(credit)
            db.session.commit()

        return credit

    @staticmethod
    def set_credit_limit(
        customer_id: int,
        credit_limit: float,
        payment_terms_days: int = 30,
        user_id: int = None,
    ) -> CustomerCredit:
        """Set credit limit for a customer."""
        credit = CreditService.get_or_create_credit_account(customer_id)

        old_limit = credit.credit_limit
        credit.credit_limit = credit_limit
        credit.available_credit = credit_limit - credit.used_credit
        credit.payment_terms_days = payment_terms_days

        # Log the change
        if old_limit != credit_limit:
            transaction = CreditTransaction(
                credit_account_id=credit.id,
                transaction_type=CreditTransactionType.CREDIT_ADJUSTMENT.value,
                amount=credit_limit - old_limit,
                balance_before=old_limit,
                balance_after=credit_limit,
                notes=f"تعديل حد الائتمان من {old_limit} إلى {credit_limit}",
                created_by=user_id,
            )
            db.session.add(transaction)

        db.session.commit()
        return credit

    @staticmethod
    def use_credit(
        customer_id: int,
        amount: float,
        reference_type: str = None,
        reference_id: int = None,
        reference_number: str = None,
        notes: str = None,
        user_id: int = None,
    ) -> CreditTransaction:
        """Record credit usage (increase outstanding)."""
        credit = CreditService.get_or_create_credit_account(customer_id)

        can_use, error = credit.can_use_credit(amount)
        if not can_use:
            raise ValueError(error)

        balance_before = credit.used_credit
        credit.used_credit += amount
        credit.available_credit -= amount
        credit.total_outstanding += amount

        # Calculate due date
        due_date = datetime.utcnow() + timedelta(days=credit.payment_terms_days)

        transaction = CreditTransaction(
            credit_account_id=credit.id,
            transaction_type=CreditTransactionType.INVOICE_CREDIT.value,
            amount=amount,
            balance_before=balance_before,
            balance_after=credit.used_credit,
            reference_type=reference_type,
            reference_id=reference_id,
            reference_number=reference_number,
            due_date=due_date,
            notes=notes,
            created_by=user_id,
        )

        db.session.add(transaction)
        db.session.commit()

        return transaction

    @staticmethod
    def receive_payment(
        customer_id: int,
        amount: float,
        reference_type: str = "payment",
        reference_id: int = None,
        reference_number: str = None,
        notes: str = None,
        user_id: int = None,
    ) -> CreditTransaction:
        """Record credit payment (reduce outstanding)."""
        credit = CreditService.get_or_create_credit_account(customer_id)

        balance_before = credit.used_credit
        credit.used_credit = max(0, credit.used_credit - amount)
        credit.available_credit = credit.credit_limit - credit.used_credit
        credit.total_outstanding = max(0, credit.total_outstanding - amount)
        credit.last_payment_date = datetime.utcnow()

        transaction = CreditTransaction(
            credit_account_id=credit.id,
            transaction_type=CreditTransactionType.CREDIT_PAYMENT.value,
            amount=-amount,
            balance_before=balance_before,
            balance_after=credit.used_credit,
            reference_type=reference_type,
            reference_id=reference_id,
            reference_number=reference_number,
            is_settled=True,
            settled_date=datetime.utcnow(),
            notes=notes,
            created_by=user_id,
        )

        db.session.add(transaction)

        # Mark old transactions as settled
        CreditService._settle_transactions(credit.id, amount)

        db.session.commit()
        return transaction

    @staticmethod
    def _settle_transactions(credit_account_id: int, amount: float):
        """Mark oldest transactions as settled up to the amount."""
        unsettled = (
            CreditTransaction.query.filter(
                CreditTransaction.credit_account_id == credit_account_id,
                CreditTransaction.is_settled == False,
                CreditTransaction.amount > 0,
            )
            .order_by(CreditTransaction.due_date.asc())
            .all()
        )

        remaining = amount
        for txn in unsettled:
            if remaining <= 0:
                break
            if txn.amount <= remaining:
                txn.is_settled = True
                txn.settled_date = datetime.utcnow()
                remaining -= txn.amount
            else:
                break

    @staticmethod
    def block_credit(
        customer_id: int, reason: str, user_id: int = None
    ) -> CustomerCredit:
        """Block customer credit account."""
        credit = CreditService.get_or_create_credit_account(customer_id)
        credit.is_blocked = True
        credit.blocked_reason = reason

        db.session.commit()
        logger.info(f"Credit blocked for customer {customer_id}: {reason}")

        return credit

    @staticmethod
    def unblock_credit(customer_id: int, user_id: int = None) -> CustomerCredit:
        """Unblock customer credit account."""
        credit = CreditService.get_or_create_credit_account(customer_id)
        credit.is_blocked = False
        credit.blocked_reason = None

        db.session.commit()
        return credit

    @staticmethod
    def get_statement(
        customer_id: int, start_date: datetime = None, end_date: datetime = None
    ) -> Dict[str, Any]:
        """Get customer credit statement."""
        credit = CustomerCredit.query.filter_by(customer_id=customer_id).first()

        if not credit:
            return {
                "customer_id": customer_id,
                "transactions": [],
                "summary": {"opening_balance": 0, "closing_balance": 0},
            }

        query = CreditTransaction.query.filter_by(credit_account_id=credit.id)

        if start_date:
            query = query.filter(CreditTransaction.created_at >= start_date)
        if end_date:
            query = query.filter(CreditTransaction.created_at <= end_date)

        transactions = query.order_by(CreditTransaction.created_at.asc()).all()

        return {
            "customer_id": customer_id,
            "customer_name": credit.customer.name if credit.customer else None,
            "account": credit.to_dict(),
            "transactions": [t.to_dict() for t in transactions],
            "summary": {
                "total_credit_used": sum(
                    t.amount for t in transactions if t.amount > 0
                ),
                "total_payments": abs(
                    sum(t.amount for t in transactions if t.amount < 0)
                ),
                "current_balance": credit.total_outstanding,
            },
        }

    @staticmethod
    def get_overdue_customers(days_overdue: int = 0) -> List[Dict[str, Any]]:
        """Get list of customers with overdue credit."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_overdue)

        overdue = (
            db.session.query(CustomerCredit)
            .join(
                CreditTransaction,
                CreditTransaction.credit_account_id == CustomerCredit.id,
            )
            .filter(
                CreditTransaction.due_date < cutoff_date,
                CreditTransaction.is_settled == False,
                CreditTransaction.amount > 0,
            )
            .distinct()
            .all()
        )

        return [
            {
                **c.to_dict(),
                "overdue_amount": sum(
                    t.amount
                    for t in c.transactions
                    if not t.is_settled
                    and t.due_date
                    and t.due_date < cutoff_date
                    and t.amount > 0
                ),
            }
            for c in overdue
        ]


__all__ = [
    "CustomerCredit",
    "CreditTransaction",
    "CreditTransactionType",
    "CreditService",
]
