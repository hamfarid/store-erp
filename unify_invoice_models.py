#!/usr/bin/env python3
"""
سكريبت توحيد نماذج الفواتير المختلفة
"""

import os
import shutil
from datetime import datetime

def backup_files():
    """إنشاء نسخ احتياطية من ملفات النماذج"""
    files_to_backup = [
        'src/models/invoice.py',
        'src/models/invoices.py', 
        'src/models/sales_advanced.py'
    ]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = f"{file_path}.unify_backup_{timestamp}"
            shutil.copy2(file_path, backup_path)
            print(f"✓ نسخة احتياطية: {backup_path}")

def create_unified_invoice_model():
    """إنشاء نموذج فاتورة موحد"""
    
    unified_model = '''# -*- coding: utf-8 -*-
"""
نموذج الفاتورة الموحد - يدعم جميع أنواع الفواتير
Unified Invoice Model - Supports all invoice types
"""

from datetime import datetime, timezone
import enum
from decimal import Decimal

try:
    from sqlalchemy import (
        Column, Integer, String, Float, DateTime, Boolean,
        Text, Enum, Date, ForeignKey, Numeric, JSON
    )
    from sqlalchemy.orm import relationship
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # Mock objects for when SQLAlchemy is not available
    def Column(*args, **kwargs): return None
    def Integer(): return None
    def String(length=None): return None
    def Float(): return None
    def DateTime(): return None
    def Boolean(): return None
    def Text(): return None
    def Enum(*args, **kwargs): return None
    def Date(): return None
    def ForeignKey(*args, **kwargs): return None
    def Numeric(*args, **kwargs): return None
    def JSON(): return None
    def relationship(*args, **kwargs): return None
    SQLALCHEMY_AVAILABLE = False

# استيراد قاعدة البيانات
try:
    from .user import db
except ImportError:
    try:
        from ..database import db
    except ImportError:
        class MockDB:
            class Model:
                pass
        db = MockDB()

# تعدادات الفاتورة الموحدة
class InvoiceType(enum.Enum):
    """أنواع الفواتير"""
    SALES = "sales"              # فاتورة مبيعات
    PURCHASE = "purchase"        # فاتورة مشتريات
    RETURN_SALES = "return_sales"    # مرتجع مبيعات
    RETURN_PURCHASE = "return_purchase"  # مرتجع مشتريات
    IMPORT = "import"            # فاتورة استيراد
    EXPORT = "export"            # فاتورة تصدير
    SERVICE = "service"          # فاتورة خدمة

class InvoiceStatus(enum.Enum):
    """حالات الفاتورة"""
    DRAFT = "draft"              # مسودة
    PENDING = "pending"          # في الانتظار
    CONFIRMED = "confirmed"      # مؤكدة
    PAID = "paid"               # مدفوعة
    PARTIAL_PAID = "partial_paid"    # مدفوعة جزئياً
    OVERDUE = "overdue"         # متأخرة
    CANCELLED = "cancelled"      # ملغية
    REFUNDED = "refunded"       # مستردة

class PaymentMethod(enum.Enum):
    """طرق الدفع"""
    CASH = "cash"               # نقداً
    CREDIT_CARD = "credit_card"  # بطاقة ائتمان
    BANK_TRANSFER = "bank_transfer"  # تحويل بنكي
    CHECK = "check"             # شيك
    INSTALLMENT = "installment"  # تقسيط
    CREDIT = "credit"           # آجل

class UnifiedInvoice(db.Model):
    """نموذج الفاتورة الموحد"""
    __tablename__ = 'unified_invoices'
    
    # المعرفات الأساسية
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    reference_number = Column(String(50))  # رقم مرجعي
    
    # نوع وحالة الفاتورة
    invoice_type = Column(Enum(InvoiceType), nullable=False, default=InvoiceType.SALES)
    status = Column(Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.DRAFT)
    
    # التواريخ
    invoice_date = Column(Date, nullable=False, default=datetime.utcnow)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات مع العملاء والموردين
    customer_id = Column(Integer, ForeignKey('customers.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    
    # المبالغ المالية
    subtotal = Column(Numeric(15, 3), default=0.000)  # المجموع الفرعي
    tax_amount = Column(Numeric(15, 3), default=0.000)  # قيمة الضريبة
    discount_amount = Column(Numeric(15, 3), default=0.000)  # قيمة الخصم
    shipping_cost = Column(Numeric(15, 3), default=0.000)  # تكلفة الشحن
    total_amount = Column(Numeric(15, 3), nullable=False, default=0.000)  # المجموع الكلي
    paid_amount = Column(Numeric(15, 3), default=0.000)  # المبلغ المدفوع
    remaining_amount = Column(Numeric(15, 3), default=0.000)  # المبلغ المتبقي
    
    # معلومات الدفع
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    payment_terms = Column(String(200))  # شروط الدفع
    
    # العملة والضريبة
    currency = Column(String(3), default='EGP')  # العملة
    tax_rate = Column(Float, default=15.0)  # معدل الضريبة
    
    # معلومات إضافية
    notes = Column(Text)  # ملاحظات
    internal_notes = Column(Text)  # ملاحظات داخلية
    terms_conditions = Column(Text)  # الشروط والأحكام
    
    # معلومات المستخدم والمخزن
    created_by = Column(Integer, ForeignKey('users.id'))
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    
    # معلومات متقدمة (JSON للمرونة)
    metadata = Column(JSON)  # بيانات إضافية مرنة
    
    # العلاقات
    items = relationship("UnifiedInvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<UnifiedInvoice {self.invoice_number}: {self.total_amount} {self.currency}>'
    
    @property
    def is_paid(self):
        """التحقق من دفع الفاتورة بالكامل"""
        return self.paid_amount >= self.total_amount
    
    @property
    def is_overdue(self):
        """التحقق من تأخر الفاتورة"""
        if self.due_date and not self.is_paid:
            return datetime.now().date() > self.due_date
        return False
    
    def calculate_totals(self):
        """حساب المجاميع تلقائياً"""
        self.subtotal = sum(item.total_amount for item in self.items)
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount + self.shipping_cost
        self.remaining_amount = self.total_amount - self.paid_amount
        
        # تحديث الحالة حسب الدفع
        if self.paid_amount == 0:
            self.status = InvoiceStatus.CONFIRMED
        elif self.paid_amount >= self.total_amount:
            self.status = InvoiceStatus.PAID
        else:
            self.status = InvoiceStatus.PARTIAL_PAID

class UnifiedInvoiceItem(db.Model):
    """عناصر الفاتورة الموحدة"""
    __tablename__ = 'unified_invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('unified_invoices.id'), nullable=False)
    
    # معلومات المنتج
    product_id = Column(Integer, ForeignKey('products.id'))
    product_name = Column(String(200), nullable=False)  # اسم المنتج
    product_code = Column(String(50))  # كود المنتج
    description = Column(Text)  # وصف العنصر
    
    # الكميات والأسعار
    quantity = Column(Numeric(15, 3), nullable=False, default=1.000)
    unit_price = Column(Numeric(15, 3), nullable=False, default=0.000)
    discount_percentage = Column(Float, default=0.0)  # نسبة الخصم
    discount_amount = Column(Numeric(15, 3), default=0.000)  # مبلغ الخصم
    tax_rate = Column(Float, default=15.0)  # معدل الضريبة للعنصر
    tax_amount = Column(Numeric(15, 3), default=0.000)  # مبلغ الضريبة
    total_amount = Column(Numeric(15, 3), nullable=False, default=0.000)  # المجموع
    
    # معلومات إضافية
    unit = Column(String(20), default='قطعة')  # وحدة القياس
    notes = Column(Text)  # ملاحظات العنصر
    
    # العلاقات
    invoice = relationship("UnifiedInvoice", back_populates="items")
    
    def __repr__(self):
        return f'<InvoiceItem {self.product_name}: {self.quantity} x {self.unit_price}>'
    
    def calculate_total(self):
        """حساب مجموع العنصر"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_percentage / 100) + self.discount_amount
        taxable_amount = subtotal - discount
        self.tax_amount = taxable_amount * (self.tax_rate / 100)
        self.total_amount = taxable_amount + self.tax_amount

class InvoicePayment(db.Model):
    """مدفوعات الفاتورة"""
    __tablename__ = 'invoice_payments'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('unified_invoices.id'), nullable=False)
    
    # معلومات الدفع
    payment_date = Column(Date, nullable=False, default=datetime.utcnow)
    amount = Column(Numeric(15, 3), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    
    # معلومات إضافية
    reference_number = Column(String(100))  # رقم المرجع
    notes = Column(Text)  # ملاحظات الدفع
    
    # معلومات المستخدم
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    invoice = relationship("UnifiedInvoice", back_populates="payments")
    
    def __repr__(self):
        return f'<Payment {self.amount} for Invoice {self.invoice_id}>'

# تصدير النماذج
__all__ = [
    'UnifiedInvoice', 
    'UnifiedInvoiceItem', 
    'InvoicePayment',
    'InvoiceType', 
    'InvoiceStatus', 
    'PaymentMethod'
]
'''
    
    # كتابة النموذج الموحد
    with open('src/models/unified_invoice.py', 'w', encoding='utf-8') as f:
        f.write(unified_model)
    
    print("✓ تم إنشاء نموذج الفاتورة الموحد: src/models/unified_invoice.py")

def update_models_init():
    """تحديث ملف __init__.py لتضمين النموذج الموحد"""
    
    init_content = '''# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات - إصدار موحد ومحسن
Unified and Enhanced Database Models Package
"""

# استيراد قاعدة البيانات
try:
    from .user import db
except ImportError:
    class MockDB:
        class Model:
            pass
        def __init__(self):
            pass
    db = MockDB()

# استيراد النماذج الأساسية
try:
    from .user import User, Role
except ImportError:
    User = None
    Role = None

try:
    from .inventory import Category, Warehouse, Product, StockMovement
except ImportError:
    Category = None
    Warehouse = None
    Product = None
    StockMovement = None

try:
    from .customer import Customer
except ImportError:
    Customer = None

try:
    from .supplier import Supplier
except ImportError:
    Supplier = None

# استيراد نموذج الفاتورة الموحد الجديد
try:
    from .unified_invoice import (
        UnifiedInvoice, UnifiedInvoiceItem, InvoicePayment,
        InvoiceType, InvoiceStatus, PaymentMethod
    )
except ImportError:
    UnifiedInvoice = None
    UnifiedInvoiceItem = None
    InvoicePayment = None
    InvoiceType = None
    InvoiceStatus = None
    PaymentMethod = None

# النماذج القديمة (للتوافق المؤقت)
try:
    from .invoice import Invoice, InvoiceItem, Payment
except ImportError:
    Invoice = None
    InvoiceItem = None
    Payment = None

# التعدادات والثوابت الموحدة
class UserRole:
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"

class ProductType:
    SIMPLE = "simple"
    VARIABLE = "variable"
    SERVICE = "service"

class MovementType:
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"

# قائمة التصدير الموحدة
__all__ = [
    'db',
    'User', 'Role',
    'Category', 'Warehouse', 'Product', 'StockMovement',
    'Customer',
    'Supplier', 
    # النماذج الموحدة الجديدة
    'UnifiedInvoice', 'UnifiedInvoiceItem', 'InvoicePayment',
    'InvoiceType', 'InvoiceStatus', 'PaymentMethod',
    # النماذج القديمة (للتوافق)
    'Invoice', 'InvoiceItem', 'Payment',
    # الثوابت
    'UserRole', 'ProductType', 'MovementType'
]
'''
    
    with open('src/models/__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print("✓ تم تحديث src/models/__init__.py")

def create_migration_script():
    """إنشاء سكريبت migration لنقل البيانات"""
    
    migration_script = '''#!/usr/bin/env python3
"""
سكريبت migration لنقل البيانات من النماذج القديمة إلى النموذج الموحد
"""

from datetime import datetime
import sys
import os

# إضافة مسار src للاستيراد
sys.path.insert(0, 'src')

def migrate_invoices():
    """نقل بيانات الفواتير من النماذج القديمة"""
    print("🔄 بدء migration الفواتير...")
    
    try:
        from models.invoice import Invoice as OldInvoice, InvoiceItem as OldInvoiceItem
        from models.unified_invoice import UnifiedInvoice, UnifiedInvoiceItem
        from database import db
        
        # نقل الفواتير الأساسية
        old_invoices = OldInvoice.query.all()
        
        for old_invoice in old_invoices:
            # إنشاء فاتورة موحدة جديدة
            new_invoice = UnifiedInvoice(
                invoice_number=old_invoice.invoice_number,
                invoice_date=old_invoice.invoice_date,
                customer_id=old_invoice.customer_id,
                total_amount=old_invoice.total_amount,
                # إضافة باقي الحقول...
            )
            
            db.session.add(new_invoice)
            
            # نقل عناصر الفاتورة
            for old_item in old_invoice.items:
                new_item = UnifiedInvoiceItem(
                    invoice=new_invoice,
                    product_id=old_item.product_id,
                    quantity=old_item.quantity,
                    unit_price=old_item.unit_price,
                    total_amount=old_item.total_amount
                )
                db.session.add(new_item)
        
        db.session.commit()
        print(f"✓ تم نقل {len(old_invoices)} فاتورة")
        
    except Exception as e:
        print(f"✗ خطأ في migration: {e}")
        db.session.rollback()

if __name__ == "__main__":
    migrate_invoices()
'''
    
    with open('migrate_invoices.py', 'w', encoding='utf-8') as f:
        f.write(migration_script)
    
    print("✓ تم إنشاء سكريبت migration: migrate_invoices.py")

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء توحيد نماذج الفواتير...")
    print("="*50)
    
    # إنشاء نسخ احتياطية
    backup_files()
    
    print()
    # إنشاء النموذج الموحد
    create_unified_invoice_model()
    
    print()
    # تحديث ملف __init__.py
    update_models_init()
    
    print()
    # إنشاء سكريبت migration
    create_migration_script()
    
    print("\n" + "="*50)
    print("✅ تم الانتهاء من توحيد نماذج الفواتير!")
    print("📝 تم إنشاء:")
    print("   - src/models/unified_invoice.py (النموذج الموحد)")
    print("   - migrate_invoices.py (سكريبت النقل)")
    print("🔄 الخطوات التالية:")
    print("   1. مراجعة النموذج الموحد")
    print("   2. تشغيل سكريبت migration")
    print("   3. تحديث المسارات لاستخدام النموذج الجديد")

if __name__ == "__main__":
    main()
