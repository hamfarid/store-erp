"""
Purchase Receipt Model
نموذج إيصال استلام المشتريات
"""

from datetime import datetime, date
from src.database import db


class PurchaseReceipt(db.Model):
    """
    نموذج إيصال استلام المشتريات
    """
    __tablename__ = "purchase_receipts"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Receipt Info
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Foreign Keys
    po_id = db.Column(db.Integer, db.ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id", ondelete="RESTRICT"), index=True)
    received_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), index=True)

    # Dates
    receipt_date = db.Column(db.Date, default=date.today, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pending', index=True)  # pending, completed, cancelled
    
    # Notes
    notes = db.Column(db.Text)
    delivery_notes = db.Column(db.Text)
    quality_notes = db.Column(db.Text)

    # Delivery Info
    driver_name = db.Column(db.String(100))
    vehicle_number = db.Column(db.String(50))
    delivery_company = db.Column(db.String(100))

    # Audit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships
    purchase_order = db.relationship("PurchaseOrder", backref=db.backref("receipts", lazy="dynamic"))
    warehouse = db.relationship("Warehouse", backref=db.backref("purchase_receipts", lazy="dynamic"))
    receiver = db.relationship("User", foreign_keys=[received_by], backref=db.backref("received_purchases", lazy="dynamic"))
    creator = db.relationship("User", foreign_keys=[created_by], backref=db.backref("created_receipts", lazy="dynamic"))

    def __repr__(self):
        return f"<PurchaseReceipt(id={self.id}, receipt_number='{self.receipt_number}', po_id={self.po_id})>"

    def link_batches(self, items_batches):
        """
        ربط اللوطات بعناصر أمر الشراء
        
        Args:
            items_batches: قائمة من {item_id: batch_id}
        """
        from src.models.purchase_order_item import PurchaseOrderItem
        
        for item_id, batch_id in items_batches.items():
            item = PurchaseOrderItem.query.get(item_id)
            if item and item.po_id == self.po_id:
                item.batch_id = batch_id
        
        db.session.commit()
        return True

    def update_inventory(self):
        """
        تحديث المخزون بناءً على الاستلام
        """
        from src.models.purchase_order_item import PurchaseOrderItem
        from src.models.lot_advanced import LotAdvanced
        
        items = PurchaseOrderItem.query.filter_by(po_id=self.po_id).all()
        
        for item in items:
            if item.batch_id:
                # تحديث كمية اللوط
                batch = LotAdvanced.query.get(item.batch_id)
                if batch:
                    batch.quantity += item.received_quantity
                    batch.original_quantity = batch.quantity
        
        db.session.commit()
        return True

    def complete(self):
        """إتمام الاستلام"""
        self.status = 'completed'
        self.update_inventory()
        
        # تحديث حالة أمر الشراء
        from src.models.purchase_order_item import PurchaseOrderItem
        
        items = PurchaseOrderItem.query.filter_by(po_id=self.po_id).all()
        all_received = all(item.is_fully_received for item in items)
        any_received = any(item.is_partially_received or item.is_fully_received for item in items)
        
        if all_received:
            self.purchase_order.status = 'received'
        elif any_received:
            self.purchase_order.status = 'partial'
        
        db.session.commit()
        return True

    def cancel(self):
        """إلغاء الاستلام"""
        self.status = 'cancelled'
        db.session.commit()
        return True

    def to_dict(self):
        """تحويل إلى Dictionary"""
        return {
            'id': self.id,
            'receipt_number': self.receipt_number,
            'po_id': self.po_id,
            'warehouse_id': self.warehouse_id,
            'received_by': self.received_by,
            'receipt_date': self.receipt_date.isoformat() if self.receipt_date else None,
            'status': self.status,
            'notes': self.notes,
            'delivery_notes': self.delivery_notes,
            'quality_notes': self.quality_notes,
            'driver_name': self.driver_name,
            'vehicle_number': self.vehicle_number,
            'delivery_company': self.delivery_company,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
