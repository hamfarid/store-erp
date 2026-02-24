#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ تحديث مخطط قاعدة البيانات
Update Database Schema Script

يقوم بتحديث قاعدة البيانات لتتوافق مع النماذج الجديدة:
- إضافة الأعمدة المفقودة
- إنشاء الجداول الجديدة
- تحديث البيانات الموجودة
"""

import sqlite3
import os
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

def update_users_table(cursor):
    """تحديث جدول المستخدمين"""
    print_step("تحديث جدول المستخدمين...")
    
    # التحقق من وجود الأعمدة الجديدة
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # إضافة الأعمدة المفقودة
    new_columns = {
        'role': "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'",
        'permissions': "ALTER TABLE users ADD COLUMN permissions TEXT",
        'last_login': "ALTER TABLE users ADD COLUMN last_login DATETIME",
        'full_name': "ALTER TABLE users ADD COLUMN full_name TEXT",
        'is_active': "ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"
    }
    
    for column_name, sql in new_columns.items():
        if column_name not in columns:
            try:
                cursor.execute(sql)
                print_success(f"تم إضافة العمود: {column_name}")
            except Exception as e:
                print_warning(f"خطأ في إضافة العمود {column_name}: {e}")
    
    print_success("تم تحديث جدول المستخدمين")

def create_categories_table(cursor):
    """إنشاء جدول الفئات"""
    print_step("إنشاء جدول الفئات...")
    
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        parent_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_id) REFERENCES categories (id)
    )
    '''
    
    try:
        cursor.execute(create_table_sql)
        print_success("تم إنشاء جدول الفئات")
    except Exception as e:
        print_warning(f"خطأ في إنشاء جدول الفئات: {e}")

def create_warehouses_table(cursor):
    """إنشاء جدول المستودعات"""
    print_step("إنشاء جدول المستودعات...")
    
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS warehouses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        location TEXT,
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    '''
    
    try:
        cursor.execute(create_table_sql)
        print_success("تم إنشاء جدول المستودعات")
    except Exception as e:
        print_warning(f"خطأ في إنشاء جدول المستودعات: {e}")

def update_products_table(cursor):
    """تحديث جدول المنتجات لإضافة category_id"""
    print_step("تحديث جدول المنتجات...")
    
    # التحقق من وجود العمود category_id
    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'category_id' not in columns:
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN category_id INTEGER")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)")
            print_success("تم إضافة عمود category_id إلى جدول المنتجات")
        except Exception as e:
            print_warning(f"خطأ في تحديث جدول المنتجات: {e}")

def create_inventory_table(cursor):
    """إنشاء جدول المخزون إذا لم يكن موجوداً"""
    print_step("إنشاء جدول المخزون...")
    
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        warehouse_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0,
        reserved_quantity INTEGER DEFAULT 0,
        min_stock_level INTEGER DEFAULT 0,
        max_stock_level INTEGER DEFAULT 0,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
        UNIQUE(product_id, warehouse_id)
    )
    '''
    
    try:
        cursor.execute(create_table_sql)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_product ON inventory(product_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inventory_warehouse ON inventory(warehouse_id)")
        print_success("تم إنشاء جدول المخزون")
    except Exception as e:
        print_warning(f"خطأ في إنشاء جدول المخزون: {e}")

def insert_default_data(cursor):
    """إدراج البيانات الافتراضية"""
    print_step("إدراج البيانات الافتراضية...")
    
    # إدراج فئات افتراضية
    default_categories = [
        ('إلكترونيات', 'أجهزة إلكترونية ومعدات تقنية'),
        ('ملابس', 'ملابس وأزياء'),
        ('طعام ومشروبات', 'منتجات غذائية ومشروبات'),
        ('كتب وقرطاسية', 'كتب ومواد قرطاسية'),
        ('منزل وحديقة', 'أدوات منزلية ومعدات حديقة')
    ]
    
    for name, description in default_categories:
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
                (name, description)
            )
        except Exception as e:
            print_warning(f"خطأ في إدراج الفئة {name}: {e}")
    
    # إدراج مستودع افتراضي
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO warehouses (name, location, description) VALUES (?, ?, ?)",
            ('المستودع الرئيسي', 'الموقع الرئيسي', 'المستودع الافتراضي للنظام')
        )
    except Exception as e:
        print_warning(f"خطأ في إدراج المستودع الافتراضي: {e}")
    
    print_success("تم إدراج البيانات الافتراضية")

def create_admin_user(cursor):
    """إنشاء مستخدم إداري افتراضي"""
    print_step("إنشاء مستخدم إداري افتراضي...")
    
    from werkzeug.security import generate_password_hash
    import json
    from datetime import datetime
    
    # التحقق من وجود مستخدم إداري
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    admin_count = cursor.fetchone()[0]
    
    if admin_count == 0:
        password_hash = generate_password_hash('admin123')
        permissions = json.dumps([
            'read_all', 'write_all', 'delete_all', 'admin_panel',
            'user_management', 'system_settings', 'reports_access'
        ])
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, full_name, password_hash, role, is_active, permissions, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'admin',
                'admin@store.com',
                'مدير النظام',
                password_hash,
                'admin',
                1,
                permissions,
                datetime.utcnow().isoformat()
            ))
            print_success("تم إنشاء المستخدم الإداري")
            print("   اسم المستخدم: admin")
            print("   كلمة المرور: admin123")
        except Exception as e:
            print_warning(f"خطأ في إنشاء المستخدم الإداري: {e}")
    else:
        print_success("المستخدم الإداري موجود بالفعل")

def main():
    print("🗄️ بدء تحديث مخطط قاعدة البيانات...")
    print("=" * 50)
    
    # مسار قاعدة البيانات
    db_path = Path("backend/instance/inventory.db")
    
    # إنشاء مجلد instance إذا لم يكن موجوداً
    db_path.parent.mkdir(exist_ok=True)
    
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # تحديث جدول المستخدمين
        update_users_table(cursor)
        
        # إنشاء الجداول الجديدة
        create_categories_table(cursor)
        create_warehouses_table(cursor)
        create_inventory_table(cursor)
        
        # تحديث جدول المنتجات
        update_products_table(cursor)
        
        # إدراج البيانات الافتراضية
        insert_default_data(cursor)
        
        # إنشاء مستخدم إداري
        create_admin_user(cursor)
        
        # حفظ التغييرات
        conn.commit()
        
        print("=" * 50)
        print_success("تم تحديث مخطط قاعدة البيانات بنجاح!")
        print("📋 التحديثات المطبقة:")
        print("   - تحديث جدول المستخدمين")
        print("   - إنشاء جدول الفئات")
        print("   - إنشاء جدول المستودعات")
        print("   - إنشاء جدول المخزون")
        print("   - تحديث جدول المنتجات")
        print("   - إدراج البيانات الافتراضية")
        print("   - إنشاء مستخدم إداري")
        
    except Exception as e:
        print_error(f"خطأ في تحديث قاعدة البيانات: {e}")
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()
    
    return True

if __name__ == "__main__":
    main()
