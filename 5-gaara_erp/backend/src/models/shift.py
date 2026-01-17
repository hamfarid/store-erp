"""
نموذج Shift - إدارة ورديات نقطة البيع
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.database import db

class Shift(db.Model):
    """نموذج الوردية"""
    __tablename__ = 'shifts'
    
    id = Column(Integer, primary_key=True)
    shift_number = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=True)
    
    # معلومات الوردية
    opening_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    closing_time = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default='open')  # open, closed
    
    # النقدية
    opening_cash = Column(Float, nullable=False, default=0.0)
    closing_cash = Column(Float, nullable=True)
    expected_cash = Column(Float, nullable=True)
    cash_difference = Column(Float, nullable=True)
    
    # الإحصائيات
    total_sales = Column(Float, nullable=False, default=0.0)
    total_refunds = Column(Float, nullable=False, default=0.0)
    total_transactions = Column(Integer, nullable=False, default=0)
    
    # طرق الدفع
    cash_sales = Column(Float, nullable=False, default=0.0)
    card_sales = Column(Float, nullable=False, default=0.0)
    other_sales = Column(Float, nullable=False, default=0.0)
    
    # ملاحظات
    opening_notes = Column(Text, nullable=True)
    closing_notes = Column(Text, nullable=True)
    
    # التواريخ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    user = relationship('User', backref='shifts')
    sales = relationship('Sale', back_populates='shift')
    
    def __repr__(self):
        return f'<Shift {self.shift_number}>'
    
    def close_shift(self, closing_cash, closing_notes=None):
        """إغلاق الوردية"""
        self.closing_time = datetime.utcnow()
        self.closing_cash = closing_cash
        self.closing_notes = closing_notes
        self.status = 'closed'
        
        # حساب الفرق
        self.expected_cash = self.opening_cash + self.cash_sales - self.total_refunds
        self.cash_difference = self.closing_cash - self.expected_cash
        
        return self
    
    def add_sale(self, amount, payment_method='cash'):
        """إضافة عملية بيع للوردية"""
        self.total_sales += amount
        self.total_transactions += 1
        
        if payment_method == 'cash':
            self.cash_sales += amount
        elif payment_method == 'card':
            self.card_sales += amount
        else:
            self.other_sales += amount
        
        return self
    
    def add_refund(self, amount):
        """إضافة عملية إرجاع"""
        self.total_refunds += amount
        return self
    
    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'shift_number': self.shift_number,
            'user_id': self.user_id,
            'branch_id': self.branch_id,
            'opening_time': self.opening_time.isoformat() if self.opening_time else None,
            'closing_time': self.closing_time.isoformat() if self.closing_time else None,
            'status': self.status,
            'opening_cash': self.opening_cash,
            'closing_cash': self.closing_cash,
            'expected_cash': self.expected_cash,
            'cash_difference': self.cash_difference,
            'total_sales': self.total_sales,
            'total_refunds': self.total_refunds,
            'total_transactions': self.total_transactions,
            'cash_sales': self.cash_sales,
            'card_sales': self.card_sales,
            'other_sales': self.other_sales,
            'opening_notes': self.opening_notes,
            'closing_notes': self.closing_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
