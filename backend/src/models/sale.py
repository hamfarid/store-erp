"""
نموذج Sale - عمليات البيع
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from src.database import db

class Sale(db.Model):
    """نموذج عملية البيع"""
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    
    # معلومات العميل
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    customer_name = Column(String(200), nullable=True)
    
    # معلومات الوردية والفرع
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=True)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # المبالغ
    subtotal = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    discount_percentage = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, nullable=False, default=0.0)
    tax_percentage = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    
    # الدفع
    payment_method = Column(String(20), nullable=False, default='cash')  # cash, card, mixed
    paid_amount = Column(Float, nullable=False, default=0.0)
    change_amount = Column(Float, nullable=False, default=0.0)
    
    # الحالة
    status = Column(String(20), nullable=False, default='completed')  # completed, refunded, partial_refund
    is_refund = Column(Boolean, default=False)
    refund_of_sale_id = Column(Integer, ForeignKey('sales.id'), nullable=True)
    
    # ملاحظات
    notes = Column(Text, nullable=True)
    
    # التواريخ
    sale_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات - disabled user relationship to avoid mapper conflicts
    customer = relationship('Customer', backref='sales')
    shift = relationship('Shift', back_populates='sales')
    # user = relationship('User', backref='sales')  # Disabled to avoid mapper conflicts
    items = relationship('SaleItem', back_populates='sale', cascade='all, delete-orphan')
    
    @property
    def user(self):
        """Get the sale's user - lazy query to avoid mapper conflicts"""
        if self.user_id:
            from src.models.user import User
            return User.query.get(self.user_id)
        return None
    refunds = relationship('Sale', backref='original_sale', remote_side=[id])
    
    def __repr__(self):
        return f'<Sale {self.invoice_number}>'
    
    def calculate_totals(self):
        """حساب الإجماليات"""
        # حساب المجموع الفرعي من العناصر
        self.subtotal = sum(item.total for item in self.items)
        
        # حساب الخصم
        if self.discount_percentage > 0:
            self.discount_amount = self.subtotal * (self.discount_percentage / 100)
        
        # حساب الضريبة
        taxable_amount = self.subtotal - self.discount_amount
        if self.tax_percentage > 0:
            self.tax_amount = taxable_amount * (self.tax_percentage / 100)
        
        # حساب الإجمالي
        self.total = taxable_amount + self.tax_amount
        
        # حساب الباقي
        self.change_amount = self.paid_amount - self.total
        
        return self
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'shift_id': self.shift_id,
            'branch_id': self.branch_id,
            'user_id': self.user_id,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'discount_percentage': self.discount_percentage,
            'tax_amount': self.tax_amount,
            'tax_percentage': self.tax_percentage,
            'total': self.total,
            'payment_method': self.payment_method,
            'paid_amount': self.paid_amount,
            'change_amount': self.change_amount,
            'status': self.status,
            'is_refund': self.is_refund,
            'refund_of_sale_id': self.refund_of_sale_id,
            'notes': self.notes,
            'sale_date': self.sale_date.isoformat() if self.sale_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items] if self.items else []
        }


class SaleItem(db.Model):
    """نموذج عنصر البيع"""
    __tablename__ = 'sale_items'
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    batch_id = Column(Integer, ForeignKey('batches_advanced.id'), nullable=True)
    
    # معلومات المنتج
    product_name = Column(String(200), nullable=False)
    product_code = Column(String(100), nullable=True)
    
    # الكميات والأسعار
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount_amount = Column(Float, nullable=False, default=0.0)
    discount_percentage = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False)
    
    # معلومات اللوط
    lot_number = Column(String(100), nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    
    # التواريخ
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    sale = relationship('Sale', back_populates='items')
    product = relationship('Product', backref='sale_items')
    # batch = relationship('LotAdvanced', backref='sale_items')  # Disabled to avoid import order issues
    batch_id_ref = None  # Use lot_advanced.LotAdvanced.query.get(batch_id) instead
    
    def __repr__(self):
        return f'<SaleItem {self.product_name} x{self.quantity}>'
    
    def calculate_total(self):
        """حساب الإجمالي"""
        # حساب السعر بعد الخصم
        if self.discount_percentage > 0:
            self.discount_amount = self.unit_price * self.quantity * (self.discount_percentage / 100)
        
        self.total = (self.unit_price * self.quantity) - self.discount_amount
        return self
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'batch_id': self.batch_id,
            'product_name': self.product_name,
            'product_code': self.product_code,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'discount_amount': self.discount_amount,
            'discount_percentage': self.discount_percentage,
            'total': self.total,
            'lot_number': self.lot_number,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
