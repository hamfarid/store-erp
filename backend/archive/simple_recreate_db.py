#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعادة إنشاء قاعدة البيانات - نسخة مبسطة
Simple Database Recreation Script
"""

import os
import sys
import shutil
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة من .env
load_dotenv()

def backup_old_database():
    """نسخ احتياطي لقاعدة البيانات القديمة"""
    db_path = 'instance/inventory.db'
    
    if not os.path.exists(db_path):
        print("⚠️ لا توجد قاعدة بيانات قديمة")
        return None
    
    backup_dir = f'database_archive/backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_path = os.path.join(backup_dir, 'inventory.db')
    shutil.copy2(db_path, backup_path)
    print(f"✅ تم نسخ قاعدة البيانات إلى {backup_path}")
    
    return backup_dir

def delete_old_databases():
    """حذف قواعد البيانات القديمة"""
    db_paths = [
        'instance/inventory.db',
        'instance/inventory.db-shm',
        'instance/inventory.db-wal',
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ تم حذف {db_path}")

def create_new_database():
    """إنشاء قاعدة بيانات جديدة باستخدام SQL مباشرة"""
    try:
        # إنشاء مجلد instance
        os.makedirs('instance', exist_ok=True)
        
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()
        
        # تفعيل Foreign Keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("📊 إنشاء الجداول...")
        
        # 1. جدول الأدوار (roles)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                permissions TEXT,
                is_system BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ تم إنشاء جدول roles")
        
        # 2. جدول المستخدمين (users)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                phone VARCHAR(20),
                avatar VARCHAR(255),
                department VARCHAR(100),
                position VARCHAR(100),
                role_id INTEGER,
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                is_superuser BOOLEAN DEFAULT 0,
                permissions TEXT,
                failed_login_attempts INTEGER DEFAULT 0,
                account_locked_until DATETIME,
                password_changed_at DATETIME,
                must_change_password BOOLEAN DEFAULT 0,
                last_login DATETIME,
                last_activity DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                settings TEXT,
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL
            )
        """)
        print("✅ تم إنشاء جدول users")
        
        # 3. جدول الفئات (categories)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                parent_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)
        print("✅ تم إنشاء جدول categories")
        
        # 4. جدول العملاء (customers)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                company VARCHAR(200),
                email VARCHAR(120),
                phone VARCHAR(20),
                address TEXT,
                city VARCHAR(100),
                country VARCHAR(100) DEFAULT 'مصر',
                tax_number VARCHAR(50),
                credit_limit DECIMAL(10, 2) DEFAULT 0.00,
                current_balance DECIMAL(10, 2) DEFAULT 0.00,
                payment_terms INTEGER DEFAULT 30,
                is_active BOOLEAN DEFAULT 1,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ تم إنشاء جدول customers")
        
        # 5. جدول الموردين (suppliers)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                company VARCHAR(200),
                email VARCHAR(120),
                phone VARCHAR(20),
                address TEXT,
                city VARCHAR(100),
                country VARCHAR(100) DEFAULT 'مصر',
                tax_number VARCHAR(50),
                payment_terms INTEGER DEFAULT 30,
                is_active BOOLEAN DEFAULT 1,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ تم إنشاء جدول suppliers")
        
        # 6. جدول المخازن (warehouses)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS warehouses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(50) UNIQUE,
                location VARCHAR(200),
                manager_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        print("✅ تم إنشاء جدول warehouses")
        
        # 7. جدول المنتجات (products)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                name_en VARCHAR(200),
                sku VARCHAR(100) UNIQUE NOT NULL,
                barcode VARCHAR(100) UNIQUE,
                category_id INTEGER,
                supplier_id INTEGER,
                brand VARCHAR(100),
                product_type VARCHAR(20) DEFAULT 'storable',
                tracking_type VARCHAR(20) DEFAULT 'none',
                cost_price DECIMAL(10, 2) DEFAULT 0.00,
                sale_price DECIMAL(10, 2) DEFAULT 0.00,
                wholesale_price DECIMAL(10, 2) DEFAULT 0.00,
                min_price DECIMAL(10, 2) DEFAULT 0.00,
                current_stock DECIMAL(10, 3) DEFAULT 0.000,
                min_quantity DECIMAL(10, 3) DEFAULT 0.000,
                max_quantity DECIMAL(10, 3) DEFAULT 1000.000,
                reorder_point DECIMAL(10, 3) DEFAULT 0.000,
                reorder_quantity DECIMAL(10, 3) DEFAULT 0.000,
                unit VARCHAR(20) DEFAULT 'قطعة',
                unit_en VARCHAR(20) DEFAULT 'piece',
                weight DECIMAL(10, 3),
                weight_unit VARCHAR(10) DEFAULT 'kg',
                length DECIMAL(10, 2),
                width DECIMAL(10, 2),
                height DECIMAL(10, 2),
                dimension_unit VARCHAR(10) DEFAULT 'cm',
                tax_rate DECIMAL(5, 2) DEFAULT 0.00,
                is_taxable BOOLEAN DEFAULT 1,
                discount_rate DECIMAL(5, 2) DEFAULT 0.00,
                description TEXT,
                description_en TEXT,
                image VARCHAR(255),
                images TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_featured BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
            )
        """)
        print("✅ تم إنشاء جدول products")
        
        conn.commit()
        print("✅ تم حفظ جميع الجداول")
        
        # إنشاء البيانات الأساسية
        print("\n👤 إنشاء البيانات الأساسية...")

        # قراءة الإعدادات من .env
        admin_username = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@system.com')
        admin_fullname = os.getenv('DEFAULT_ADMIN_FULLNAME', 'مدير النظام')
        admin_password = os.getenv('ADMIN_PASSWORD', 'u-fZEk2jsOQN3bwvFrj93A')
        admin_role = os.getenv('DEFAULT_ADMIN_ROLE', 'admin')

        # إنشاء الأدوار
        roles = [
            ('admin', 'مدير النظام', '*', 1),
            ('manager', 'مدير', 'read,write,update', 1),
            ('user', 'مستخدم', 'read', 1),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO roles (name, description, permissions, is_system) VALUES (?, ?, ?, ?)",
            roles
        )
        print("✅ تم إنشاء الأدوار")

        # إنشاء مستخدم admin
        import bcrypt
        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(
            """INSERT OR IGNORE INTO users
            (username, email, password_hash, full_name, role, is_active, is_superuser, permissions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (admin_username, admin_email, password_hash, admin_fullname, admin_role, 1, 1, '*')
        )
        print("✅ تم إنشاء مستخدم admin")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🔄 إعادة إنشاء قاعدة البيانات (نسخة مبسطة)")
    print("=" * 60)
    
    # 1. نسخ احتياطي
    print("\n📦 الخطوة 1: نسخ احتياطي...")
    backup_dir = backup_old_database()
    if backup_dir:
        print(f"✅ تم حفظ النسخة الاحتياطية في: {backup_dir}")
    
    # 2. حذف القديم
    print("\n🗑️  الخطوة 2: حذف قواعد البيانات القديمة...")
    delete_old_databases()
    print("✅ تم حذف قواعد البيانات القديمة")
    
    # 3. إنشاء جديد
    print("\n🆕 الخطوة 3: إنشاء قاعدة بيانات جديدة...")
    success = create_new_database()

    if success:
        # قراءة الإعدادات من .env
        admin_username = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@system.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'u-fZEk2jsOQN3bwvFrj93A')
        frontend_port = os.getenv('FRONTEND_PORT', '5502')
        backend_port = os.getenv('PORT', '5002')

        print("\n" + "=" * 60)
        print("✅ تم إعادة إنشاء قاعدة البيانات بنجاح!")
        print("=" * 60)
        print("\n📝 بيانات الدخول:")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        print("\n🚀 الخطوات التالية:")
        print("   1. شغّل Backend:")
        print("      python app.py")
        print("\n   2. شغّل Frontend (Terminal جديد):")
        print("      cd ../frontend")
        print("      npm run dev")
        print("\n   3. افتح المتصفح:")
        print(f"      http://localhost:{frontend_port}")
        print("\n   4. Backend API:")
        print(f"      http://localhost:{backend_port}")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ فشل في إعادة إنشاء قاعدة البيانات!")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())

