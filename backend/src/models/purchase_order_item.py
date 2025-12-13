"""
Purchase Order Item Model
نموذج عناصر أمر الشراء
"""

from datetime import datetime
from src.database import db


class PurchaseOrderItem(db.Model):
    """
    نموذج عنصر أمر الشراء
    """
    __tablename__ = "purchase_order_items"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    po_id = db.Column(db.Integer, db.ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products_advanced.id", ondelete="RESTRICT"), nullable=False, index=True)
    batch_id = db.Column(db.Integer, db.ForeignKey("batches_advanced.id", ondelete="SET NULL"), index=True)

    # Quantities
    quantity = db.Column(db.Integer, nullable=False)
    received_quantity = db.Column(db.Integer, default=0)
    remaining_quantity = db.Column(db.Integer)

    # Prices
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(12, 2))
    discount_percentage = db.Column(db.Numeric(5, 2), default=0)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    tax_percentage = db.Column(db.Numeric(5, 2), default=0)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    final_price = db.Column(db.Numeric(12, 2))

    # Additional Info
    notes = db.Column(db.Text)
    expiry_date = db.Column(db.Date)
    manufacture_date = db.Column(db.Date)

    # Audit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    purchase_order = db.relationship("PurchaseOrder", backref=db.backref("items", lazy="dynamic", cascade="all, delete-orphan"))
    product = db.relationship("ProductAdvanced", backref=db.backref("purchase_items", lazy="dynamic"))
    batch = db.relationship("LotAdvanced", backref=db.backref("purchase_items", lazy="dynamic"))

    def __repr__(self):
        return f"<PurchaseOrderItem(id={self.id}, po_id={self.po_id}, product_id={self.product_id}, quantity={self.quantity})>"

    def calculate_total(self):
        """حساب الإجمالي"""
        if not self.unit_price or not self.quantity:
            return 0
        
        # السعر الأساسي
        base_total = float(self.unit_price) * self.quantity
        
        # الخصم
        discount = 0
        if self.discount_percentage:
            discount = base_total * (float(self.discount_percentage) / 100)
        elif self.discount_amount:
            discount = float(self.discount_amount)
        
        # السعر بعد الخصم
        after_discount = base_total - discount
        
        # الضريبة
        tax = 0
        if self.tax_percentage:
            tax = after_discount * (float(self.tax_percentage) / 100)
        
        # السعر النهائي
        final = after_discount + tax
        
        # تحديث الحقول
        self.total_price = base_total
        self.discount_amount = discount
        self.tax_amount = tax
        self.final_price = final
        
        return final

    def update_received(self, received_qty):
        """تحديث الكمية المستلمة"""
        if received_qty > self.quantity:
            raise ValueError(f"الكمية المستلمة ({received_qty}) أكبر من الكمية المطلوبة ({self.quantity})")
        
        self.received_quantity = (self.received_quantity or 0) + received_qty
        self.remaining_quantity = self.quantity - self.received_quantity
        
        return self.remaining_quantity

    @property
    def is_fully_received(self):
        """التحقق من استلام الكمية بالكامل"""
        return self.received_quantity >= self.quantity

    @property
    def is_partially_received(self):
        """التحقق من الاستلام الجزئي"""
        return 0 < self.received_quantity < self.quantity

    def to_dict(self):
        """تحويل إلى Dictionary"""
        return {
            'id': self.id,
            'po_id': self.po_id,
            'product_id': self.product_id,
            'batch_id': self.batch_id,
            'quantity': self.quantity,
            'received_quantity': self.received_quantity or 0,
            'remaining_quantity': self.remaining_quantity or (self.quantity - (self.received_quantity or 0)),
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0,
            'discount_percentage': float(self.discount_percentage) if self.discount_percentage else 0,
            'discount_amount': float(self.discount_amount) if self.discount_amount else 0,
            'tax_percentage': float(self.tax_percentage) if self.tax_percentage else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'final_price': float(self.final_price) if self.final_price else 0,
            'notes': self.notes,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'manufacture_date': self.manufacture_date.isoformat() if self.manufacture_date else None,
            'is_fully_received': self.is_fully_received,
            'is_partially_received': self.is_partially_received,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
