#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/system_backup_clean/store_v1.5_folder/add_modules_gradually.py
سكريبت إضافة الوحدات تدريجياً
Add Modules Gradually Script

سكريبت لإضافة وحدات جديدة للنظام بشكل تدريجي وآمن
"""

import os
import shutil
from datetime import datetime

def add_suppliers_module():
    """إضافة وحدة الموردين"""
    print("🏭 إضافة وحدة الموردين...")
    
    # إنشاء نموذج الموردين
    suppliers_model = '''# -*- coding: utf-8 -*-
"""
نموذج الموردين - Suppliers Model
/backend/src/models/supplier.py

نموذج قاعدة البيانات لإدارة الموردين
"""

from datetime import datetime
from src.database import db


class Supplier(db.Model):
    """نموذج الموردين"""
    __tablename__ = 'suppliers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company_type = db.Column(db.String(50), default='company')  # company, individual
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    website = db.Column(db.String(200))
    address = db.Column(db.Text)
    tax_number = db.Column(db.String(50))
    payment_terms = db.Column(db.String(100))
    preferred_payment_method = db.Column(db.String(50))
    currency = db.Column(db.String(10), default='SAR')
    language = db.Column(db.String(10), default='ar')
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy=True)

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'company_type': self.company_type,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'website': self.website,
            'address': self.address,
            'tax_number': self.tax_number,
            'payment_terms': self.payment_terms,
            'preferred_payment_method': self.preferred_payment_method,
            'currency': self.currency,
            'language': self.language,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Supplier {self.name}>'
'''
    
    # إنشاء مسارات الموردين
    suppliers_routes = '''# -*- coding: utf-8 -*-
"""
مسارات الموردين - Suppliers Routes
/backend/src/routes/suppliers.py

مسارات API لإدارة الموردين
"""

from flask import Blueprint, request, jsonify
from src.models.supplier import Supplier
from src.database import db

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """الحصول على قائمة الموردين"""
    try:
        suppliers = Supplier.query.filter_by(is_active=True).all()
        return jsonify([supplier.to_dict() for supplier in suppliers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@suppliers_bp.route('/api/suppliers', methods=['POST'])
def create_supplier():
    """إنشاء مورد جديد"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        if not data.get('name'):
            return jsonify({'error': 'اسم المورد مطلوب'}), 400
        
        # إنشاء المورد الجديد
        supplier = Supplier(
            name=data['name'],
            company_type=data.get('company_type', 'company'),
            email=data.get('email'),
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            website=data.get('website'),
            address=data.get('address'),
            tax_number=data.get('tax_number'),
            payment_terms=data.get('payment_terms'),
            preferred_payment_method=data.get('preferred_payment_method'),
            currency=data.get('currency', 'SAR'),
            language=data.get('language', 'ar'),
            notes=data.get('notes')
        )
        
        db.session.add(supplier)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء المورد بنجاح',
            'supplier': supplier.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@suppliers_bp.route('/api/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    """الحصول على مورد محدد"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        return jsonify(supplier.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@suppliers_bp.route('/api/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    """تحديث مورد"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        data = request.get_json()
        
        # تحديث البيانات
        for field in ['name', 'company_type', 'email', 'phone', 'mobile', 
                     'website', 'address', 'tax_number', 'payment_terms',
                     'preferred_payment_method', 'currency', 'language', 'notes']:
            if field in data:
                setattr(supplier, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث المورد بنجاح',
            'supplier': supplier.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@suppliers_bp.route('/api/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    """حذف مورد (إلغاء تفعيل)"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        supplier.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'تم حذف المورد بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
'''
    
    # كتابة الملفات
    with open('system_backup_clean/store_v1.5_folder/backend/src/models/supplier.py', 'w', encoding='utf-8') as f:
        f.write(suppliers_model)
    
    with open('system_backup_clean/store_v1.5_folder/backend/src/routes/suppliers.py', 'w', encoding='utf-8') as f:
        f.write(suppliers_routes)
    
    print("   ✅ تم إنشاء وحدة الموردين")

def add_customers_module():
    """إضافة وحدة العملاء"""
    print("👥 إضافة وحدة العملاء...")
    
    # إنشاء مسارات العملاء
    customers_routes = '''# -*- coding: utf-8 -*-
"""
مسارات العملاء - Customers Routes
/backend/src/routes/customers.py

مسارات API لإدارة العملاء
"""

from flask import Blueprint, request, jsonify
from src.models.customer import Customer
from src.database import db

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/api/customers', methods=['GET'])
def get_customers():
    """الحصول على قائمة العملاء"""
    try:
        customers = Customer.query.filter_by(is_active=True).all()
        return jsonify([customer.to_dict() for customer in customers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/api/customers', methods=['POST'])
def create_customer():
    """إنشاء عميل جديد"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        if not data.get('name'):
            return jsonify({'error': 'اسم العميل مطلوب'}), 400
        
        # إنشاء العميل الجديد
        customer = Customer(
            name=data['name'],
            customer_type=data.get('customer_type', 'individual'),
            email=data.get('email'),
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            tax_number=data.get('tax_number'),
            payment_terms=data.get('payment_terms'),
            credit_limit=data.get('credit_limit', 0.0),
            currency=data.get('currency', 'SAR'),
            language=data.get('language', 'ar'),
            notes=data.get('notes')
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء العميل بنجاح',
            'customer': customer.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """الحصول على عميل محدد"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify(customer.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """تحديث عميل"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        
        # تحديث البيانات
        for field in ['name', 'customer_type', 'email', 'phone', 'mobile', 
                     'address', 'tax_number', 'payment_terms', 'credit_limit',
                     'currency', 'language', 'notes']:
            if field in data:
                setattr(customer, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث العميل بنجاح',
            'customer': customer.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """حذف عميل (إلغاء تفعيل)"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        customer.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'تم حذف العميل بنجاح'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
'''
    
    # كتابة ملف المسارات
    with open('system_backup_clean/store_v1.5_folder/backend/src/routes/customers.py', 'w', encoding='utf-8') as f:
        f.write(customers_routes)
    
    print("   ✅ تم إنشاء وحدة العملاء")

def add_purchase_orders_module():
    """إضافة وحدة أوامر الشراء"""
    print("🛒 إضافة وحدة أوامر الشراء...")
    
    # إنشاء نموذج أوامر الشراء
    purchase_order_model = '''# -*- coding: utf-8 -*-
"""
نموذج أوامر الشراء - Purchase Orders Model
/backend/src/models/purchase_order.py

نموذج قاعدة البيانات لإدارة أوامر الشراء
"""

from datetime import datetime
from src.database import db


class PurchaseOrder(db.Model):
    """نموذج أوامر الشراء"""
    __tablename__ = 'purchase_orders'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    order_date = db.Column(db.Date, default=datetime.utcnow().date)
    expected_delivery_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, received, cancelled
    total_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    order_items = db.relationship('PurchaseOrderItem', backref='purchase_order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'supplier_id': self.supplier_id,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'expected_delivery_date': self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
            'status': self.status,
            'total_amount': self.total_amount,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.order_items] if self.order_items else []
        }

    def __repr__(self):
        return f'<PurchaseOrder {self.order_number}>'


class PurchaseOrderItem(db.Model):
    """نموذج بنود أوامر الشراء"""
    __tablename__ = 'purchase_order_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    received_quantity = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            'id': self.id,
            'purchase_order_id': self.purchase_order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'received_quantity': self.received_quantity,
            'notes': self.notes
        }

    def __repr__(self):
        return f'<PurchaseOrderItem {self.id}>'
'''
    
    # كتابة ملف النموذج
    with open('system_backup_clean/store_v1.5_folder/backend/src/models/purchase_order.py', 'w', encoding='utf-8') as f:
        f.write(purchase_order_model)
    
    print("   ✅ تم إنشاء وحدة أوامر الشراء")

def update_minimal_app():
    """تحديث التطبيق البسيط لدعم الوحدات الجديدة"""
    print("🔄 تحديث التطبيق البسيط...")
    
    # قراءة التطبيق الحالي
    with open('system_backup_clean/store_v1.5_folder/backend/minimal_working_app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة جداول جديدة لقاعدة البيانات
    new_tables = """
    # إنشاء جدول الموردين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company_type TEXT DEFAULT 'company',
            email TEXT,
            phone TEXT,
            mobile TEXT,
            website TEXT,
            address TEXT,
            tax_number TEXT,
            payment_terms TEXT,
            preferred_payment_method TEXT,
            currency TEXT DEFAULT 'SAR',
            language TEXT DEFAULT 'ar',
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إنشاء جدول العملاء
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            customer_type TEXT DEFAULT 'individual',
            email TEXT,
            phone TEXT,
            mobile TEXT,
            address TEXT,
            tax_number TEXT,
            payment_terms TEXT,
            credit_limit REAL DEFAULT 0.0,
            currency TEXT DEFAULT 'SAR',
            language TEXT DEFAULT 'ar',
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إنشاء جدول أوامر الشراء
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            supplier_id INTEGER,
            order_date DATE DEFAULT CURRENT_DATE,
            expected_delivery_date DATE,
            status TEXT DEFAULT 'draft',
            total_amount REAL DEFAULT 0.0,
            tax_amount REAL DEFAULT 0.0,
            discount_amount REAL DEFAULT 0.0,
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # إضافة بيانات تجريبية
    cursor.execute('''
        INSERT OR IGNORE INTO suppliers (name, company_type, email, phone)
        VALUES (?, ?, ?, ?)
    ''', ('شركة التوريد المحدودة', 'company', 'supplier@example.com', '0112345678'))
    
    cursor.execute('''
        INSERT OR IGNORE INTO customers (name, customer_type, email, phone)
        VALUES (?, ?, ?, ?)
    ''', ('أحمد محمد', 'individual', 'ahmed@example.com', '0501234567'))
"""
    
    # إضافة نقاط النهاية الجديدة
    new_endpoints = """
@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    '''الحصول على الموردين'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, company_type, email, phone, is_active, created_at FROM suppliers WHERE is_active = 1')
    suppliers = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': sup[0],
        'name': sup[1],
        'company_type': sup[2],
        'email': sup[3],
        'phone': sup[4],
        'is_active': sup[5],
        'created_at': sup[6]
    } for sup in suppliers])

@app.route('/api/customers', methods=['GET'])
def get_customers():
    '''الحصول على العملاء'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, customer_type, email, phone, is_active, created_at FROM customers WHERE is_active = 1')
    customers = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': cust[0],
        'name': cust[1],
        'customer_type': cust[2],
        'email': cust[3],
        'phone': cust[4],
        'is_active': cust[5],
        'created_at': cust[6]
    } for cust in customers])

@app.route('/api/purchase-orders', methods=['GET'])
def get_purchase_orders():
    '''الحصول على أوامر الشراء'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT po.id, po.order_number, s.name as supplier_name, po.order_date, 
               po.status, po.total_amount, po.created_at
        FROM purchase_orders po
        LEFT JOIN suppliers s ON po.supplier_id = s.id
        ORDER BY po.created_at DESC
    ''')
    orders = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': order[0],
        'order_number': order[1],
        'supplier_name': order[2],
        'order_date': order[3],
        'status': order[4],
        'total_amount': order[5],
        'created_at': order[6]
    } for order in orders])
"""
    
    # تحديث لوحة التحكم
    dashboard_update = """
    # عدد الموردين
    cursor.execute('SELECT COUNT(*) FROM suppliers WHERE is_active = 1')
    suppliers_count = cursor.fetchone()[0]
    
    # عدد العملاء
    cursor.execute('SELECT COUNT(*) FROM customers WHERE is_active = 1')
    customers_count = cursor.fetchone()[0]
    
    # عدد أوامر الشراء
    cursor.execute('SELECT COUNT(*) FROM purchase_orders')
    purchase_orders_count = cursor.fetchone()[0]
"""
    
    # إدراج التحديثات في المحتوى
    # إضافة الجداول الجديدة بعد إنشاء جدول المستودعات
    content = content.replace(
        "conn.commit()",
        new_tables + "\n    conn.commit()"
    )
    
    # إضافة نقاط النهاية الجديدة قبل نقطة نهاية لوحة التحكم
    content = content.replace(
        "@app.route('/api/reports/dashboard', methods=['GET'])",
        new_endpoints + "\n@app.route('/api/reports/dashboard', methods=['GET'])"
    )
    
    # تحديث لوحة التحكم
    content = content.replace(
        "conn.close()\n    \n    return jsonify({",
        dashboard_update + "\n    conn.close()\n    \n    return jsonify({"
    )
    
    content = content.replace(
        "'users': users_count\n        },",
        "'users': users_count,\n            'suppliers': suppliers_count,\n            'customers': customers_count,\n            'purchase_orders': purchase_orders_count\n        },"
    )
    
    # كتابة التطبيق المحدث
    with open('system_backup_clean/store_v1.5_folder/backend/minimal_working_app_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ تم تحديث التطبيق البسيط")

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إضافة الوحدات الجديدة...")
    print("=" * 50)
    
    try:
        # إضافة الوحدات الجديدة
        add_suppliers_module()
        add_customers_module()
        add_purchase_orders_module()
        
        # تحديث التطبيق البسيط
        update_minimal_app()
        
        print("\n" + "=" * 50)
        print("✅ تم إضافة جميع الوحدات بنجاح!")
        print("\nالوحدات المضافة:")
        print("  🏭 وحدة الموردين")
        print("  👥 وحدة العملاء")
        print("  🛒 وحدة أوامر الشراء")
        print("\n📝 تم إنشاء التطبيق المحدث: minimal_working_app_v2.py")
        
    except Exception as e:
        print(f"❌ خطأ في إضافة الوحدات: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
