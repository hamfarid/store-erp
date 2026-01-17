#!/usr/bin/env python3
# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
إعداد وتهيئة قاعدة البيانات - نظام إدارة المخزون الزراعي
All linting disabled due to complex imports and optional dependencies.
"""

import sqlite3
import os

# مسار قاعدة البيانات
DB_PATH = 'inventory_system.db'


def create_database():
    """إنشاء قاعدة البيانات والجداول"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🗄️ إنشاء جداول قاعدة البيانات...")

    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL,
            permissions TEXT,
            company_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول الشركات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            tax_number TEXT,
            commercial_register TEXT,
            logo_path TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول الفئات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT,
            description TEXT,
            parent_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories (id)
        )
    ''')

    # جدول الموردين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            supplier_type TEXT,
            payment_terms TEXT,
            tax_number TEXT,
            contact_person TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول العملاء
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            customer_type TEXT,
            credit_limit REAL DEFAULT 0,
            current_balance REAL DEFAULT 0,
            tax_number TEXT,
            contact_person TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول المخازن
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT,
            location TEXT,
            address TEXT,
            capacity REAL,
            current_usage REAL DEFAULT 0,
            manager_id INTEGER,
            warehouse_type TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (manager_id) REFERENCES users (id)
        )
    ''')

    # جدول المنتجات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            name_en TEXT,
            sku TEXT UNIQUE NOT NULL,
            barcode TEXT,
            category_id INTEGER,
            supplier_id INTEGER,
            product_type TEXT DEFAULT 'storable',
            tracking_type TEXT DEFAULT 'none',
            cost_price REAL DEFAULT 0,
            sale_price REAL DEFAULT 0,
            wholesale_price REAL DEFAULT 0,
            current_stock REAL DEFAULT 0,
            min_quantity REAL DEFAULT 0,
            max_quantity REAL DEFAULT 1000,
            reorder_point REAL DEFAULT 0,
            unit TEXT DEFAULT 'قطعة',
            weight REAL,
            dimensions TEXT,
            shelf_life_days INTEGER,
            quality_grade TEXT,
            origin_country TEXT,
            description TEXT,
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')

    # جدول حركات المخزون
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            warehouse_id INTEGER NOT NULL,
            movement_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit_cost REAL,
            total_cost REAL,
            reference_type TEXT,
            reference_id INTEGER,
            batch_number TEXT,
            expiry_date DATE,
            notes TEXT,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # جدول الفواتير
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            invoice_type TEXT NOT NULL,
            customer_id INTEGER,
            supplier_id INTEGER,
            warehouse_id INTEGER,
            invoice_date DATE NOT NULL,
            due_date DATE,
            subtotal REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            paid_amount REAL DEFAULT 0,
            status TEXT DEFAULT 'draft',
            currency TEXT DEFAULT 'EGP',
            exchange_rate REAL DEFAULT 1,
            payment_terms TEXT,
            notes TEXT,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
            FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # جدول تفاصيل الفواتير
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            discount_percent REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            tax_percent REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            batch_number TEXT,
            expiry_date DATE,
            notes TEXT,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # جدول اللوطات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_number TEXT UNIQUE NOT NULL,
            product_id INTEGER NOT NULL,
            warehouse_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            unit_cost REAL,
            production_date DATE,
            expiry_date DATE,
            supplier_id INTEGER,
            quality_grade TEXT,
            status TEXT DEFAULT 'active',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')

    conn.commit()
    print("✅ تم إنشاء جميع الجداول بنجاح")

    return conn


def insert_demo_data(conn):
    """إدراج البيانات التجريبية"""

    cursor = conn.cursor()

    print("📊 إدراج البيانات التجريبية...")

    # إدراج شركة تجريبية
    cursor.execute('''
        INSERT OR IGNORE INTO companies (id,
            name,
            name_en,
            address,
            phone,
            email)
        VALUES (1, 'شركة المخزون الزراعي', 'Agricultural Inventory Co.',
                'القاهرة - مصر الجديدة',
                    '02-12345678',
                    'info@agri-inventory.com')
    ''')

    # إدراج المستخدمين
    users_data = [
        (1,
         'admin',
         'admin123',
         'مدير النظام',
         'admin@system.com',
         '01234567890',
         'مدير عام',
         '["all"]',
         1),
        (2,
         'manager',
         'manager123',
         'مدير المخزون',
         'manager@system.com',
         '01234567891',
         'مدير مخزون',
         '["inventory", "reports"]',
         1),
        (3,
         'user',
         'user123',
         'موظف المبيعات',
         'user@system.com',
         '01234567892',
         'موظف',
         '["sales", "customers"]',
         1)
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO users (id,
            username,
            password,
            name,
            email,
            phone,
            role,
            permissions,
            company_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)

    # إدراج الفئات
    categories_data = [
        (1, 'بذور', 'Seeds', 'جميع أنواع البذور الزراعية'),
        (2, 'أسمدة', 'Fertilizers', 'الأسمدة الكيماوية والعضوية'),
        (3, 'مبيدات', 'Pesticides', 'المبيدات الحشرية والفطرية'),
        (4, 'أدوات زراعية', 'Farm Tools', 'الأدوات والمعدات الزراعية')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO categories (id, name, name_en, description)
        VALUES (?, ?, ?, ?)
    ''', categories_data)

    # إدراج الموردين
    suppliers_data = [
        (1,
            'شركة البذور المصرية',
            'Egyptian Seeds Co.',
            '01234567892',
            'sales@egy-seeds.com',
         'الإسكندرية - سموحة', 'مورد رئيسي', '30 يوم'),
        (2,
            'مصنع الأسمدة الحديث',
            'Modern Fertilizer Factory',
            '01234567893',
            'orders@modern-fert.com',
         'أسوان - الصناعية', 'مصنع', '45 يوم'),
        (3,
            'شركة المبيدات المتقدمة',
            'Advanced Pesticides Co.',
            '01234567894',
            'info@adv-pest.com',
         'القاهرة - مدينة نصر', 'مورد متخصص', '60 يوم')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO suppliers (id,
            name,
            name_en,
            phone,
            email,
            address,
            supplier_type,
            payment_terms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', suppliers_data)

    conn.commit()
    print("✅ تم إدراج البيانات التجريبية بنجاح")


def main():
    """الدالة الرئيسية"""
    print("🗄️ إعداد قاعدة بيانات نظام إدارة المخزون الزراعي")
    print("=" * 60)

    try:
        # إنشاء قاعدة البيانات
        conn = create_database()

        # إدراج البيانات التجريبية
        insert_demo_data(conn)

        # إغلاق الاتصال
        conn.close()

        print("\n🎉 تم إعداد قاعدة البيانات بنجاح!")
        print(f"📁 مسار قاعدة البيانات: {os.path.abspath(DB_PATH)}")
        print("📊 البيانات التجريبية متاحة للاختبار")

    except Exception as e:
        print(f"❌ خطأ في إعداد قاعدة البيانات: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
