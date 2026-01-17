#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.92: Returns and Refunds System

Models for managing product returns and refunds.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from src.database import db
from enum import Enum


class ReturnStatus(str, Enum):
    """Return request statuses."""

    PENDING = "pending"  # معلق
    APPROVED = "approved"  # معتمد
    REJECTED = "rejected"  # مرفوض
    RECEIVED = "received"  # مستلم
    INSPECTING = "inspecting"  # قيد الفحص
    COMPLETED = "completed"  # مكتمل
    CANCELLED = "cancelled"  # ملغي


class ReturnReason(str, Enum):
    """Return reasons."""

    DEFECTIVE = "defective"  # معيب
    WRONG_ITEM = "wrong_item"  # منتج خاطئ
    NOT_AS_DESCRIBED = "not_as_described"  # مخالف للوصف
    DAMAGED = "damaged"  # تالف
    EXPIRED = "expired"  # منتهي الصلاحية
    CUSTOMER_CHANGE = "customer_change"  # تغيير رأي العميل
    OTHER = "other"  # أخرى


class RefundMethod(str, Enum):
    """Refund methods."""

    ORIGINAL_PAYMENT = "original_payment"  # نفس طريقة الدفع
    CASH = "cash"  # نقداً
    CREDIT = "credit"  # رصيد
    BANK_TRANSFER = "bank_transfer"  # تحويل بنكي
    STORE_CREDIT = "store_credit"  # رصيد متجر


class ReturnRequest(db.Model):
    """
    P2.92: Return request model.
    """

    __tablename__ = "return_requests"

    id = db.Column(db.Integer, primary_key=True)
    return_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Customer and invoice
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"))
    invoice_number = db.Column(db.String(50))

    # Status
    status = db.Column(db.String(20), default=ReturnStatus.PENDING.value, index=True)

    # Reason
    reason = db.Column(db.String(30), nullable=False)
    reason_detail = db.Column(db.Text)

    # Refund details
    refund_method = db.Column(db.String(30))
    refund_amount = db.Column(db.Float, default=0)
    refund_processed = db.Column(db.Boolean, default=False)
    refund_date = db.Column(db.DateTime)

    # Dates
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    received_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)

    # Notes
    customer_notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)

    # Approval
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.String(200))

    # User and timestamps
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    customer = db.relationship("Customer", backref="return_requests")
    items = db.relationship(
        "ReturnItem", back_populates="return_request", cascade="all, delete-orphan"
    )

    @property
    def status_ar(self) -> str:
        """Get Arabic status."""
        translations = {
            ReturnStatus.PENDING.value: "معلق",
            ReturnStatus.APPROVED.value: "معتمد",
            ReturnStatus.REJECTED.value: "مرفوض",
            ReturnStatus.RECEIVED.value: "مستلم",
            ReturnStatus.INSPECTING.value: "قيد الفحص",
            ReturnStatus.COMPLETED.value: "مكتمل",
            ReturnStatus.CANCELLED.value: "ملغي",
        }
        return translations.get(self.status, self.status)

    @property
    def reason_ar(self) -> str:
        """Get Arabic reason."""
        translations = {
            ReturnReason.DEFECTIVE.value: "معيب",
            ReturnReason.WRONG_ITEM.value: "منتج خاطئ",
            ReturnReason.NOT_AS_DESCRIBED.value: "مخالف للوصف",
            ReturnReason.DAMAGED.value: "تالف",
            ReturnReason.EXPIRED.value: "منتهي الصلاحية",
            ReturnReason.CUSTOMER_CHANGE.value: "تغيير رأي العميل",
            ReturnReason.OTHER.value: "أخرى",
        }
        return translations.get(self.reason, self.reason)

    @property
    def total_items(self) -> int:
        """Get total items count."""
        return sum(item.quantity for item in self.items)

    def calculate_refund(self):
        """Calculate total refund amount."""
        self.refund_amount = sum(item.refund_amount for item in self.items)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "return_number": self.return_number,
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else None,
            "invoice_id": self.invoice_id,
            "invoice_number": self.invoice_number,
            "status": self.status,
            "status_ar": self.status_ar,
            "reason": self.reason,
            "reason_ar": self.reason_ar,
            "reason_detail": self.reason_detail,
            "refund_method": self.refund_method,
            "refund_amount": self.refund_amount,
            "refund_processed": self.refund_processed,
            "request_date": (
                self.request_date.isoformat() if self.request_date else None
            ),
            "items": [item.to_dict() for item in self.items],
            "total_items": self.total_items,
            "customer_notes": self.customer_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def generate_return_number() -> str:
        """Generate unique return number."""
        today = datetime.utcnow()
        prefix = f"RET{today.strftime('%Y%m%d')}"

        last = (
            ReturnRequest.query.filter(ReturnRequest.return_number.like(f"{prefix}%"))
            .order_by(ReturnRequest.id.desc())
            .first()
        )

        if last:
            last_num = int(last.return_number[-4:])
            new_num = last_num + 1
        else:
            new_num = 1

        return f"{prefix}{new_num:04d}"


class ReturnItem(db.Model):
    """Return request line item."""

    __tablename__ = "return_items"

    id = db.Column(db.Integer, primary_key=True)
    return_request_id = db.Column(
        db.Integer, db.ForeignKey("return_requests.id"), nullable=False
    )

    # Product
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))
    invoice_item_id = db.Column(db.Integer)

    # Quantity
    quantity = db.Column(db.Integer, nullable=False)
    quantity_received = db.Column(db.Integer, default=0)
    quantity_approved = db.Column(db.Integer, default=0)

    # Pricing
    unit_price = db.Column(db.Float, nullable=False)
    refund_amount = db.Column(db.Float, default=0)

    # Condition
    condition = db.Column(db.String(50))  # new, used, damaged
    condition_notes = db.Column(db.Text)

    # Stock action
    restock = db.Column(db.Boolean, default=True)
    restocked = db.Column(db.Boolean, default=False)

    # Relationships
    return_request = db.relationship("ReturnRequest", back_populates="items")
    product = db.relationship("Product")

    def calculate_refund(self):
        """Calculate item refund amount."""
        self.refund_amount = self.quantity_approved * self.unit_price

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "variant_id": self.variant_id,
            "quantity": self.quantity,
            "quantity_received": self.quantity_received,
            "quantity_approved": self.quantity_approved,
            "unit_price": self.unit_price,
            "refund_amount": self.refund_amount,
            "condition": self.condition,
            "restock": self.restock,
            "restocked": self.restocked,
        }


class ReturnService:
    """Service for managing returns."""

    @staticmethod
    def create_return(
        customer_id: int,
        invoice_id: int,
        reason: str,
        items: List[Dict],
        reason_detail: str = None,
        customer_notes: str = None,
        user_id: int = None,
    ) -> ReturnRequest:
        """Create a new return request."""
        from src.models.invoice import Invoice

        invoice = Invoice.query.get(invoice_id)

        return_request = ReturnRequest(
            return_number=ReturnRequest.generate_return_number(),
            customer_id=customer_id,
            invoice_id=invoice_id,
            invoice_number=invoice.invoice_number if invoice else None,
            reason=reason,
            reason_detail=reason_detail,
            customer_notes=customer_notes,
            created_by=user_id,
        )

        db.session.add(return_request)
        db.session.flush()

        # Add items
        for item_data in items:
            item = ReturnItem(
                return_request_id=return_request.id,
                product_id=item_data["product_id"],
                variant_id=item_data.get("variant_id"),
                invoice_item_id=item_data.get("invoice_item_id"),
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                restock=item_data.get("restock", True),
            )
            db.session.add(item)

        db.session.commit()
        return return_request

    @staticmethod
    def approve_return(
        return_id: int,
        approved_quantities: Dict[int, int] = None,
        refund_method: str = RefundMethod.ORIGINAL_PAYMENT.value,
        notes: str = None,
        user_id: int = None,
    ) -> ReturnRequest:
        """Approve a return request."""
        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            raise ValueError("Return request not found")

        return_request.status = ReturnStatus.APPROVED.value
        return_request.approved_by = user_id
        return_request.approved_at = datetime.utcnow()
        return_request.refund_method = refund_method

        if notes:
            return_request.internal_notes = notes

        # Set approved quantities
        for item in return_request.items:
            if approved_quantities and item.id in approved_quantities:
                item.quantity_approved = approved_quantities[item.id]
            else:
                item.quantity_approved = item.quantity
            item.calculate_refund()

        return_request.calculate_refund()
        db.session.commit()

        return return_request

    @staticmethod
    def reject_return(
        return_id: int, reason: str, user_id: int = None
    ) -> ReturnRequest:
        """Reject a return request."""
        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            raise ValueError("Return request not found")

        return_request.status = ReturnStatus.REJECTED.value
        return_request.rejection_reason = reason
        return_request.approved_by = user_id
        return_request.approved_at = datetime.utcnow()

        db.session.commit()
        return return_request

    @staticmethod
    def receive_return(
        return_id: int,
        received_quantities: Dict[int, int] = None,
        conditions: Dict[int, str] = None,
        user_id: int = None,
    ) -> ReturnRequest:
        """Mark return items as received."""
        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            raise ValueError("Return request not found")

        return_request.status = ReturnStatus.RECEIVED.value
        return_request.received_date = datetime.utcnow()

        for item in return_request.items:
            if received_quantities and item.id in received_quantities:
                item.quantity_received = received_quantities[item.id]
            else:
                item.quantity_received = item.quantity

            if conditions and item.id in conditions:
                item.condition = conditions[item.id]

        db.session.commit()
        return return_request

    @staticmethod
    def complete_return(return_id: int, user_id: int = None) -> ReturnRequest:
        """Complete a return and process refund."""
        from src.models.stock_movement import StockMovementService, MovementType

        return_request = ReturnRequest.query.get(return_id)
        if not return_request:
            raise ValueError("Return request not found")

        # Restock items
        for item in return_request.items:
            if item.restock and item.quantity_approved > 0:
                StockMovementService.record_movement(
                    product_id=item.product_id,
                    movement_type=MovementType.RETURN_IN.value,
                    quantity=item.quantity_approved,
                    reference_type="return",
                    reference_id=return_request.id,
                    reference_number=return_request.return_number,
                    user_id=user_id,
                )
                item.restocked = True

        return_request.status = ReturnStatus.COMPLETED.value
        return_request.completed_date = datetime.utcnow()
        return_request.refund_processed = True
        return_request.refund_date = datetime.utcnow()

        db.session.commit()
        return return_request


__all__ = [
    "ReturnRequest",
    "ReturnItem",
    "ReturnStatus",
    "ReturnReason",
    "RefundMethod",
    "ReturnService",
]
