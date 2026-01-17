#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إضافة الوحدات تدريجياً - مُصحح
Add Modules Gradually Script - Fixed
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
"""

from datetime import datetime
from src.database import db

class Supplier(db.Model):
    """نموذج الموردين"""
    __tablename__ = 'suppliers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company_type = db.Column(db.String(50), default='company')
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    website = db.Column(db.String(200))
    address = db.Column(db.Text)
    tax_number = db.Column(db.String(50))
    payment_terms = db.Column(db.String(100))
    preferred_payment_method = db.Column(db.String(50))
    currency = db.Column(db.String(10), default='EGP')
    language = db.Column(db.String(10), default='ar')
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    
    # كتابة ملف النموذج
    with open('backend/src/models/supplier.py', 'w', encoding='utf-8') as f:
        f.write(suppliers_model)
    
    print("   ✅ تم إنشاء نموذج الموردين")

def update_minimal_app():
    """تحديث التطبيق البسيط لدعم الوحدات الجديدة"""
    print("🔄 تحديث التطبيق البسيط...")
    
    # قراءة التطبيق الحالي
    with open('backend/minimal_working_app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن موقع إضافة الجداول
    insert_point = content.find("conn.commit()")
    if insert_point == -1:
        print("   ❌ لم يتم العثور على نقطة الإدراج")
        return False
    
    # إضافة الجداول الجديدة
    new_tables_code = '''
    
    # إنشاء جدول الموردين
    cursor.execute(\'\'\'
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
            currency TEXT DEFAULT 'EGP',
            language TEXT DEFAULT 'ar',
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    \'\'\')
    
    # إنشاء جدول العملاء
    cursor.execute(\'\'\'
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
            currency TEXT DEFAULT 'EGP',
            language TEXT DEFAULT 'ar',
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    \'\'\')
    
    # إضافة بيانات تجريبية للموردين
    cursor.execute(\'\'\'
        INSERT OR IGNORE INTO suppliers (name, company_type, email, phone)
        VALUES (?, ?, ?, ?)
    \'\'\', ('شركة التوريد المحدودة', 'company', 'supplier@example.com', '0112345678'))
    
    # إضافة بيانات تجريبية للعملاء
    cursor.execute(\'\'\'
        INSERT OR IGNORE INTO customers (name, customer_type, email, phone)
        VALUES (?, ?, ?, ?)
    \'\'\', ('أحمد محمد', 'individual', 'ahmed@example.com', '0501234567'))
'''
    
    # إدراج الجداول الجديدة
    content = content[:insert_point] + new_tables_code + "\n    " + content[insert_point:]
    
    # إضافة نقاط النهاية الجديدة
    new_endpoints = '''
@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """الحصول على الموردين"""
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
    """الحصول على العملاء"""
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

'''
    
    # البحث عن موقع إضافة نقاط النهاية
    dashboard_point = content.find("@app.route('/api/reports/dashboard', methods=['GET'])")
    if dashboard_point != -1:
        content = content[:dashboard_point] + new_endpoints + content[dashboard_point:]
    
    # تحديث لوحة التحكم
    dashboard_stats_point = content.find("'users': users_count")
    if dashboard_stats_point != -1:
        # إضافة إحصائيات جديدة
        new_stats = '''
    # عدد الموردين
    cursor.execute('SELECT COUNT(*) FROM suppliers WHERE is_active = 1')
    suppliers_count = cursor.fetchone()[0]
    
    # عدد العملاء
    cursor.execute('SELECT COUNT(*) FROM customers WHERE is_active = 1')
    customers_count = cursor.fetchone()[0]
'''
        
        # إدراج الإحصائيات الجديدة
        stats_insert_point = content.rfind("conn.close()", 0, dashboard_stats_point)
        if stats_insert_point != -1:
            content = content[:stats_insert_point] + new_stats + "\n    " + content[stats_insert_point:]
        
        # تحديث القاموس
        content = content.replace(
            "'users': users_count",
            "'users': users_count,\n            'suppliers': suppliers_count,\n            'customers': customers_count"
        )
    
    # كتابة التطبيق المحدث
    with open('backend/minimal_working_app_v2.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ تم تحديث التطبيق البسيط")
    return True

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إضافة الوحدات الجديدة...")
    print("=" * 50)
    
    try:
        # إضافة الوحدات الجديدة
        add_suppliers_module()
        
        # تحديث التطبيق البسيط
        if update_minimal_app():
            print("\n" + "=" * 50)
            print("✅ تم إضافة الوحدات بنجاح!")
            print("\nالوحدات المضافة:")
            print("  🏭 وحدة الموردين")
            print("  👥 وحدة العملاء")
            print("\n📝 تم إنشاء التطبيق المحدث: minimal_working_app_v2.py")
            return True
        else:
            print("❌ فشل في تحديث التطبيق")
            return False
        
    except Exception as e:
        print(f"❌ خطأ في إضافة الوحدات: {e}")
        return False

if __name__ == '__main__':
    main()
