# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
warehouse_transfer - نموذج أساسي
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

# استيراد قاعدة البيانات من مصدر موحّد لتجنّب تعدد النسخ
from .user import db  # يضمن استخدام نفس الـ db.Model عبر جميع النماذج

#
# 4242 42322 24422 24 42 2434 4242 2
from .inventory import Warehouse, Product  # ensure mapper names available
from .user import User  # ensure mapper names available


# تعريف حالات التحويل
class TransferStatus(enum.Enum):
    """حالات تحويل المخزون"""

    PENDING = "pending"  # في الانتظار
    IN_TRANSIT = "in_transit"  # في الطريق
    COMPLETED = "completed"  # مكتمل
    CANCELLED = "cancelled"  # ملغي
    REJECTED = "rejected"  # مرفوض


# نماذج تحويل المخزون
class WarehouseTransfer(db.Model):
    """نموذج تحويل المخزون بين المخازن"""

    __tablename__ = "warehouse_transfers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    transfer_number = Column(String(50), unique=True, nullable=False)
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    status = Column(
        Enum(TransferStatus), default=TransferStatus.PENDING, nullable=False
    )
    transfer_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    expected_date = Column(DateTime)
    completed_date = Column(DateTime)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    received_by = Column(Integer, ForeignKey("users.id"))
    total_items = Column(Integer, default=0)
    total_value = Column(Numeric(10, 2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    if SQLALCHEMY_AVAILABLE:
        items = relationship(
            "WarehouseTransferItem",
            backref="transfer",
            lazy=True,
            cascade="all, delete-orphan",
        )
        from_warehouse = relationship(
            Warehouse, foreign_keys=[from_warehouse_id], backref="outgoing_transfers"
        )
        to_warehouse = relationship(
            Warehouse, foreign_keys=[to_warehouse_id], backref="incoming_transfers"
        )
        creator = relationship(
            User, foreign_keys=[created_by], backref="created_transfers"
        )
        approver = relationship(
            User, foreign_keys=[approved_by], backref="approved_transfers"
        )
        receiver = relationship(
            User, foreign_keys=[received_by], backref="received_transfers"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "transfer_number": self.transfer_number,
            "from_warehouse_id": self.from_warehouse_id,
            "to_warehouse_id": self.to_warehouse_id,
            "from_warehouse_name": (
                self.from_warehouse.name
                if hasattr(self, "from_warehouse") and self.from_warehouse
                else None
            ),
            "to_warehouse_name": (
                self.to_warehouse.name
                if hasattr(self, "to_warehouse") and self.to_warehouse
                else None
            ),
            "status": self.status.value if self.status else None,
            "status_display": self.get_status_display(),
            "transfer_date": (
                self.transfer_date.isoformat() if self.transfer_date else None
            ),
            "expected_date": (
                self.expected_date.isoformat() if self.expected_date else None
            ),
            "completed_date": (
                self.completed_date.isoformat() if self.completed_date else None
            ),
            "notes": self.notes,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "received_by": self.received_by,
            "creator_name": (
                self.creator.full_name
                if hasattr(self, "creator")
                and self.creator
                and hasattr(self.creator, "full_name")
                else None
            ),
            "approver_name": (
                self.approver.full_name
                if hasattr(self, "approver")
                and self.approver
                and hasattr(self.approver, "full_name")
                else None
            ),
            "receiver_name": (
                self.receiver.full_name
                if hasattr(self, "receiver")
                and self.receiver
                and hasattr(self.receiver, "full_name")
                else None
            ),
            "total_items": self.total_items,
            "total_value": float(self.total_value) if self.total_value else 0.0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "items_count": len(self.items) if self.items else 0,
        }

    def get_status_display(self):
        """الحصول على عرض حالة التحويل باللغة العربية"""
        status_map = {
            TransferStatus.PENDING: "في الانتظار",
            TransferStatus.IN_TRANSIT: "في الطريق",
            TransferStatus.COMPLETED: "مكتمل",
            TransferStatus.CANCELLED: "ملغي",
            TransferStatus.REJECTED: "مرفوض",
        }
        return status_map.get(self.status, "غير محدد")

    def can_be_approved(self):
        """التحقق من إمكانية الموافقة على التحويل"""
        return self.status == TransferStatus.PENDING

    def can_be_cancelled(self):
        """التحقق من إمكانية إلغاء التحويل"""
        return self.status in [TransferStatus.PENDING, TransferStatus.IN_TRANSIT]

    def can_be_completed(self):
        """التحقق من إمكانية إكمال التحويل"""
        return self.status == TransferStatus.IN_TRANSIT


class WarehouseTransferItem(db.Model):
    """نموذج عناصر تحويل المخزون"""

    __tablename__ = "warehouse_transfer_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    transfer_id = Column(Integer, ForeignKey("warehouse_transfers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_requested = Column(Numeric(10, 3), nullable=False)
    quantity_sent = Column(Numeric(10, 3), default=0.000)
    quantity_received = Column(Numeric(10, 3), default=0.000)
    unit_cost = Column(Numeric(10, 2), default=0.00)
    total_cost = Column(Numeric(10, 2), default=0.00)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    if SQLALCHEMY_AVAILABLE:
        product = relationship(Product, backref="warehouse_transfer_items")

    def to_dict(self):
        return {
            "id": self.id,
            "transfer_id": self.transfer_id,
            "product_id": self.product_id,
            "product_name": (
                self.product.name if hasattr(self, "product") and self.product else None
            ),
            "product_code": (
                self.product.sku
                if hasattr(self, "product")
                and self.product
                and hasattr(self.product, "sku")
                and self.product.sku
                else (
                    getattr(self.product, "barcode", None)
                    if hasattr(self, "product") and self.product
                    else None
                )
            ),
            "quantity_requested": (
                float(self.quantity_requested) if self.quantity_requested else 0.0
            ),
            "quantity_sent": float(self.quantity_sent) if self.quantity_sent else 0.0,
            "quantity_received": (
                float(self.quantity_received) if self.quantity_received else 0.0
            ),
            "unit_cost": float(self.unit_cost) if self.unit_cost else 0.0,
            "total_cost": float(self.total_cost) if self.total_cost else 0.0,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "variance": (
                float(self.quantity_received - self.quantity_sent)
                if self.quantity_received and self.quantity_sent
                else 0.0
            ),
        }

    def calculate_total_cost(self):
        """حساب التكلفة الإجمالية"""
        if self.quantity_sent and self.unit_cost:
            self.total_cost = self.quantity_sent * self.unit_cost
        return self.total_cost


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
