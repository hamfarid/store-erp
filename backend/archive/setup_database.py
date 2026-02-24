"""
#!/usr/bin/env python3

سكريبت إعداد قاعدة البيانات الشاملة لنظام إدارة المخزون
ملف: setup_database.py
المسار: /home/ubuntu/inventory_management_system/setup_database.py

هذا السكريبت ينشئ قاعدة بيانات كاملة مع بيانات تجريبية شاملة
"""

import os
import random
import sqlite3
import sys
from datetime import datetime, timedelta

# Constants to avoid duplicate string literals
PASSWORD_HASH = 'pbkdf2:sha256:600000$salt$hash'
PESTICIDE_CABINET = 'خزانة المبيدات'
SOIL_AREA = 'منطقة التربة'
GIZA = 'الجيزة'
CAIRO = 'القاهرة'

# إضافة مسار src للوصول للنماذج
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def create_database():
    """إنشاء قاعدة البيانات والجداول"""

    # حذف قاعدة البيانات القديمة إن وجدت
    db_path = os.path.join(os.path.dirname(__file__), 'src', 'inventory.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("تم حذف قاعدة البيانات القديمة")

    # إنشاء الاتصال بقاعدة البيانات
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # إنشاء جدول المستخدمين
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL DEFAULT 'مستخدم عادي',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')

    # إنشاء جدول الفئات
    cursor.execute('''
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إنشاء جدول المنتجات
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            unit TEXT NOT NULL,
            cost_price REAL DEFAULT 0,
            selling_price REAL DEFAULT 0,
            current_stock INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 0,
            max_stock INTEGER DEFAULT 1000,
            description TEXT,
            barcode TEXT,
            location TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    # إنشاء جدول العملاء
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT DEFAULT 'مصر',
            tax_number TEXT,
            credit_limit REAL DEFAULT 0,
            current_balance REAL DEFAULT 0,
            payment_terms INTEGER DEFAULT 30,
            is_active BOOLEAN DEFAULT 1,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إنشاء جدول الموردين
    cursor.execute('''
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT DEFAULT 'مصر',
            tax_number TEXT,
            specialty TEXT,
            rating INTEGER DEFAULT 5,
            payment_terms INTEGER DEFAULT 30,
            is_active BOOLEAN DEFAULT 1,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إنشاء جدول حركات المخزون
    cursor.execute('''
        CREATE TABLE stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            movement_type TEXT NOT NULL CHECK (movement_type IN ('وارد',
                'صادر',
                'تسوية',
                'تحويل')),
            quantity INTEGER NOT NULL,
            unit_price REAL DEFAULT 0,
            total_value REAL DEFAULT 0,
            reference_type TEXT,
            reference_id INTEGER,
            reference_number TEXT,
            notes TEXT,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # إنشاء جدول المخازن
    cursor.execute('''
        CREATE TABLE warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            location TEXT,
            manager_name TEXT,
            phone TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إنشاء جدول مخزون المخازن
    cursor.execute('''
        CREATE TABLE warehouse_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            warehouse_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 0,
            reserved_quantity INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
            FOREIGN KEY (product_id) REFERENCES products (id),
            UNIQUE(warehouse_id, product_id)
        )
    ''')

    # إنشاء الفهارس لتحسين الأداء
    cursor.execute('CREATE INDEX idx_products_sku ON products(sku)')
    cursor.execute(
        'CREATE INDEX idx_products_category ON products(category_id)')
    cursor.execute(
        'CREATE INDEX idx_stock_movements_product ON stock_movements(product_id)')
    cursor.execute(
        'CREATE INDEX idx_stock_movements_date ON stock_movements(created_at)')
    cursor.execute('CREATE INDEX idx_customers_name ON customers(name)')
    cursor.execute('CREATE INDEX idx_suppliers_name ON suppliers(name)')

    conn.commit()
    print("تم إنشاء قاعدة البيانات والجداول بنجاح")
    return conn


def insert_sample_data(conn):
    """إدراج البيانات التجريبية"""
    cursor = conn.cursor()

    # إدراج المستخدمين
    users_data = [
        ('admin',
         PASSWORD_HASH,
         'مدير النظام',
         'admin@company.com',
         '01000000001',
         'مدير النظام'),
        ('manager',
         PASSWORD_HASH,
         'مدير المخزون',
         'manager@company.com',
         '01000000002',
         'مدير المخزون'),
        ('accountant',
         PASSWORD_HASH,
         'المحاسب الرئيسي',
         'accountant@company.com',
         '01000000003',
         'محاسب'),
        ('user1',
         PASSWORD_HASH,
         'أحمد محمد',
         'ahmed@company.com',
         '01000000004',
         'مستخدم عادي'),
        ('user2',
         PASSWORD_HASH,
         'فاطمة علي',
         'fatma@company.com',
         '01000000005',
         'مستخدم عادي')]

    cursor.executemany('''
        INSERT INTO users (username,
            password_hash,
            full_name,
            email,
            phone,
            role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users_data)

    # إدراج الفئات
    categories_data = [
        ('بذور وشتلات', 'بذور الخضروات والفواكه والشتلات'),
        ('أسمدة ومغذيات', 'الأسمدة الكيماوية والعضوية والمغذيات'),
        ('مبيدات ومكافحة', 'المبيدات الحشرية والفطرية ومواد المكافحة'),
        ('أدوات زراعية', 'الأدوات والمعدات الزراعية'),
        ('أنظمة الري', 'معدات وأنظمة الري والتنقيط'),
        ('مستلزمات البيوت المحمية', 'مواد وأدوات البيوت المحمية'),
        ('تربة ومواد زراعية', 'أنواع التربة والمواد الزراعية المساعدة'),
        ('معدات وآلات', 'المعدات والآلات الزراعية الكبيرة')
    ]

    cursor.executemany('''
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    ''', categories_data)

    # إدراج المخازن
    warehouses_data = [
        ('المخزن الرئيسي',
            'MAIN',
            'المقر الرئيسي - القاهرة',
            'أحمد محمود',
            '01111111111'),
        ('مخزن الإسكندرية',
            'ALEX',
            'فرع الإسكندرية',
            'محمد أحمد',
            '01222222222'),
        ('مخزن أسيوط', 'ASYT', 'فرع أسيوط', 'علي حسن', '01333333333'),
        ('مخزن المنيا', 'MNYA', 'فرع المنيا', 'سارة محمد', '01444444444')
    ]

    cursor.executemany('''
        INSERT INTO warehouses (name, code, location, manager_name, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', warehouses_data)

    # إدراج المنتجات
    products_data = [
        # بذور وشتلات
        ('بذور طماطم هجين', 'TOM-001', 1, 'جرام', 2.50, 5.00, 500, 50,
         2000, 'بذور طماطم هجين عالية الإنتاج', '1234567890001', 'رف A1'),
        ('بذور خيار هجين', 'CUC-001', 1, 'جرام', 3.00, 6.00, 300, 30,
         1500, 'بذور خيار هجين مقاوم للأمراض', '1234567890002', 'رف A2'),
        ('بذور فلفل حلو', 'PEP-001', 1, 'جرام', 4.00, 8.00, 200,
         20, 1000, 'بذور فلفل حلو ملون', '1234567890003', 'رف A3'),
        ('شتلات طماطم', 'TOM-S01', 1, 'شتلة', 0.50, 1.00, 1000, 100, 5000,
         'شتلات طماطم جاهزة للزراعة', '1234567890004', 'منطقة الشتلات'),
        ('بذور جزر', 'CAR-001', 1, 'جرام', 1.50, 3.00, 400, 40,
         2000, 'بذور جزر برتقالي', '1234567890005', 'رف A4'),

        # أسمدة ومغذيات
        ('سماد NPK 20-20-20', 'NPK-001', 2, 'كيلو', 15.00, 25.00,
         100, 10, 500, 'سماد مركب متوازن', '1234567890006', 'رف B1'),
        ('سماد يوريا 46%', 'UREA-001', 2, 'كيلو', 8.00, 12.00, 200,
         20, 1000, 'سماد نيتروجيني', '1234567890007', 'رف B2'),
        ('سماد سوبر فوسفات', 'PHOS-001', 2, 'كيلو', 10.00, 16.00,
         150, 15, 800, 'سماد فوسفاتي', '1234567890008', 'رف B3'),
        ('سماد عضوي كمبوست', 'COMP-001', 2, 'كيلو', 5.00, 8.00, 300, 30,
         1500, 'سماد عضوي طبيعي', '1234567890009', 'منطقة الأسمدة العضوية'),
        ('مغذي حديد مخلبي', 'IRON-001', 2, 'كيلو', 25.00, 40.00, 50,
         5, 200, 'مغذي حديد للنباتات', '1234567890010', 'رف B4'),

        # مبيدات ومكافحة
        ('مبيد حشري أكتارا', 'ACTA-001', 3, 'لتر', 120.00, 180.00, 20,
         2, 100, 'مبيد حشري جهازي', '1234567890011', PESTICIDE_CABINET),
        ('مبيد فطري ريدوميل', 'RIDO-001', 3, 'كيلو', 200.00, 300.00, 15, 2,
         50, 'مبيد فطري وقائي وعلاجي', '1234567890012', PESTICIDE_CABINET),
        ('مبيد عشبي راوند أب', 'ROUND-001', 3, 'لتر', 80.00, 120.00, 25,
         3, 100, 'مبيد عشبي شامل', '1234567890013', PESTICIDE_CABINET),
        ('مبيد حلم فيرتيمك', 'VERT-001', 3, 'لتر', 150.00, 220.00, 10,
         1, 50, 'مبيد حلم وتربس', '1234567890014', PESTICIDE_CABINET),

        # أدوات زراعية
        ('مجرفة يد', 'TOOL-001', 4, 'قطعة', 25.00, 40.00, 50,
         5, 200, 'مجرفة يد للحفر', '1234567890015', 'رف C1'),
        ('مقص تقليم', 'TOOL-002', 4, 'قطعة', 35.00, 55.00, 30,
         3, 150, 'مقص تقليم احترافي', '1234567890016', 'رف C1'),
        ('خرطوم ري 25 متر', 'HOSE-001', 4, 'قطعة', 80.00, 120.00, 20,
         2, 100, 'خرطوم ري مرن', '1234567890017', 'منطقة الخراطيم'),
        ('رشاش ظهر 16 لتر', 'SPRAY-001', 4, 'قطعة', 200.00, 300.00,
         15, 2, 50, 'رشاش ظهر للمبيدات', '1234567890018', 'رف C2'),

        # أنظمة الري
        ('نقاط تنقيط 4 لتر/ساعة', 'DRIP-001', 5, 'قطعة', 0.50, 1.00, 1000,
         100, 5000, 'نقاط تنقيط قابلة للتعديل', '1234567890019', 'رف D1'),
        ('خط تنقيط 16 مم', 'PIPE-001', 5, 'متر', 2.00, 3.50, 500,
         50, 2000, 'خط تنقيط مدمج', '1234567890020', 'رف D2'),
        ('فلتر شبكي 120 ميش', 'FILT-001', 5, 'قطعة', 150.00, 250.00,
         10, 1, 50, 'فلتر شبكي للري', '1234567890021', 'رف D3'),
        ('مضخة ري 1 حصان', 'PUMP-001', 5, 'قطعة', 1500.00, 2200.00, 5,
         1, 20, 'مضخة ري كهربائية', '1234567890022', 'منطقة المضخات'),

        # مستلزمات البيوت المحمية
        ('بلاستيك صوبة 200 ميكرون', 'PLAS-001', 6, 'متر', 8.00, 12.00, 200,
         20, 1000, 'بلاستيك صوبة مقاوم للأشعة', '1234567890023', 'رف E1'),
        ('شبك تظليل 50%', 'SHADE-001', 6, 'متر', 5.00, 8.00, 300,
         30, 1500, 'شبك تظليل أخضر', '1234567890024', 'رف E2'),
        ('مشابك بلاستيك', 'CLIP-001', 6, 'قطعة', 0.25, 0.50, 2000, 200,
         10000, 'مشابك تثبيت البلاستيك', '1234567890025', 'رف E3'),

        # تربة ومواد زراعية
        ('بيتموس مستورد', 'PEAT-001', 7, 'كيس', 50.00, 75.00, 100, 10,
         500, 'بيتموس عالي الجودة', '1234567890026', SOIL_AREA),
        ('فيرميكوليت', 'VERM-001', 7, 'كيس', 30.00, 45.00, 80, 8,
         400, 'فيرميكوليت للزراعة', '1234567890027', SOIL_AREA),
        ('بيرلايت', 'PERL-001', 7, 'كيس', 25.00, 40.00, 60, 6,
         300, 'بيرلايت للتهوية', '1234567890028', SOIL_AREA)
    ]

    cursor.executemany('''
        INSERT INTO products (name,
            sku,
            category_id,
            unit,
            cost_price,
            selling_price,
                            current_stock,
                                min_stock,
                                max_stock,
                                description,
                                barcode,
                                location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products_data)

    # إدراج العملاء
    customers_data = [
        ('مزرعة الأمل',
         'شركة الأمل للتنمية الزراعية',
         'amal@farm.com',
         '01111111111',
         'طريق القاهرة الإسكندرية الصحراوي',
         GIZA,
         'مصر',
         '123456789',
         50000,
         15000,
         30),
        ('مزرعة النيل',
         'مؤسسة النيل الزراعية',
         'nile@farm.com',
         '01222222222',
         'طريق مصر أسيوط الزراعي',
         'المنيا',
         'مصر',
         '987654321',
         30000,
         8000,
         15),
        ('شركة الدلتا الزراعية',
         'شركة الدلتا للاستثمار الزراعي',
         'delta@agri.com',
         '01333333333',
         'كفر الشيخ',
         'كفر الشيخ',
         'مصر',
         '456789123',
         75000,
         25000,
         45),
        ('مزرعة الصعيد',
         'مزرعة الصعيد للإنتاج الزراعي',
         'saeed@farm.com',
         '01444444444',
         'طريق أسيوط سوهاج',
         'أسيوط',
         'مصر',
         '789123456',
         40000,
         12000,
         30),
        ('الشركة المصرية للبذور',
         'الشركة المصرية لإنتاج البذور',
         'seeds@egypt.com',
         '01555555555',
         'شارع الجمهورية',
         CAIRO,
         'مصر',
         '321654987',
         60000,
         18000,
         60),
        ('مزرعة الواحات',
         'مزرعة الواحات الحديثة',
         'oasis@farm.com',
         '01666666666',
         'الوادي الجديد',
         'الخارجة',
         'مصر',
         '654987321',
         35000,
         10000,
         30),
        ('شركة الفيوم الزراعية',
         'شركة الفيوم للتنمية الزراعية',
         'fayoum@agri.com',
         '01777777777',
         'مدينة الفيوم',
         'الفيوم',
         'مصر',
         '147258369',
         45000,
         15000,
         30),
        ('مزرعة سيناء',
         'مزرعة سيناء للزراعة المتطورة',
         'sinai@farm.com',
         '01888888888',
         'شمال سيناء',
         'العريش',
         'مصر',
         '963852741',
         25000,
         5000,
         15),
        ('الشركة الحديثة للزراعة',
         'الشركة الحديثة للزراعة المحمية',
         'modern@agri.com',
         '01999999999',
         'طريق القاهرة السويس',
         CAIRO,
         'مصر',
         '852741963',
         80000,
         30000,
         45),
        ('مزرعة البحيرة',
         'مزرعة البحيرة للإنتاج المتميز',
         'beheira@farm.com',
         '01000000000',
         'محافظة البحيرة',
         'دمنهور',
         'مصر',
         '741963852',
         55000,
         20000,
         30),
        ('شركة الإسماعيلية الزراعية',
         'شركة الإسماعيلية للاستثمار الزراعي',
         'ismailia@agri.com',
         '01111111112',
         'مدينة الإسماعيلية',
         'الإسماعيلية',
         'مصر',
         '159753486',
         38000,
         12000,
         30),
        ('مزرعة قنا الحديثة',
         'مزرعة قنا للزراعة الحديثة',
         'qena@farm.com',
         '01222222223',
         'محافظة قنا',
         'قنا',
         'مصر',
         '486159753',
         42000,
         14000,
         30)]

    cursor.executemany('''
        INSERT INTO customers (name,
            company,
            email,
            phone,
            address,
            city,
            country,
                             tax_number,
                                 credit_limit,
                                 current_balance,
                                 payment_terms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', customers_data)

    # إدراج الموردين
    suppliers_data = [
        ('شركة البذور المتقدمة',
         'شركة البذور المتقدمة المحدودة',
         'seeds@advanced.com',
         '02111111111',
         'المنطقة الصناعية الأولى',
         CAIRO,
         'مصر',
         '111222333',
         'بذور وشتلات',
         9,
         30),
        ('مصنع الأسمدة الوطني',
         'المصنع الوطني للأسمدة والكيماويات',
         'fertilizer@national.com',
         '02222222222',
         'المنطقة الصناعية الثانية',
         'الإسكندرية',
         'مصر',
         '222333444',
         'أسمدة ومغذيات',
         8,
         45),
        ('شركة المبيدات الحديثة',
         'شركة المبيدات والكيماويات الحديثة',
         'pesticides@modern.com',
         '02333333333',
         'المنطقة الصناعية الثالثة',
         GIZA,
         'مصر',
         '333444555',
         'مبيدات ومكافحة',
         9,
         30),
        ('مصنع الأدوات الزراعية',
         'مصنع الأدوات والمعدات الزراعية',
         'tools@factory.com',
         '02444444444',
         'المنطقة الصناعية بالعاشر',
         CAIRO,
         'مصر',
         '444555666',
         'أدوات زراعية',
         8,
         30),
        ('شركة أنظمة الري المتطورة',
         'شركة أنظمة الري والتنقيط المتطورة',
         'irrigation@advanced.com',
         '02555555555',
         'مدينة السادات',
         'المنوفية',
         'مصر',
         '555666777',
         'أنظمة الري',
         9,
         30),
        ('مصنع البلاستيك الزراعي',
         'مصنع البلاستيك والمستلزمات الزراعية',
         'plastic@agri.com',
         '02666666666',
         'المنطقة الصناعية ببورسعيد',
         'بورسعيد',
         'مصر',
         '666777888',
         'مستلزمات البيوت المحمية',
         7,
         45),
        ('شركة التربة والمواد الزراعية',
         'شركة التربة والمواد الزراعية المتخصصة',
         'soil@materials.com',
         '02777777777',
         'طريق القاهرة الفيوم',
         GIZA,
         'مصر',
         '777888999',
         'تربة ومواد زراعية',
         8,
         30),
        ('مصنع المعدات الثقيلة',
         'مصنع المعدات والآلات الزراعية الثقيلة',
         'equipment@heavy.com',
         '02888888888',
         'المنطقة الصناعية بالسويس',
         'السويس',
         'مصر',
         '888999000',
         'معدات وآلات',
         8,
         60)]

    cursor.executemany('''
        INSERT INTO suppliers (name,
            company,
            email,
            phone,
            address,
            city,
            country,
                             tax_number, specialty, rating, payment_terms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', suppliers_data)

    # إدراج حركات المخزون (بيانات تاريخية)
    print("إدراج حركات المخزون...")

    # الحصول على معرفات المنتجات
    cursor.execute('SELECT id FROM products')
    product_ids = [row[0] for row in cursor.fetchall()]

    # إنشاء حركات وارد (شراء من الموردين)
    for i in range(100):  # 100 حركة وارد
        product_id = random.choice(product_ids)
        quantity = random.randint(10, 200)
        unit_price = random.uniform(5.0, 100.0)
        total_value = quantity * unit_price
        days_ago = random.randint(1, 90)
        created_at = datetime.now() - timedelta(days=days_ago)

        cursor.execute('''
            INSERT INTO stock_movements
            (product_id, movement_type, quantity, unit_price, total_value,
             reference_type, reference_number, notes, user_id, created_at)
            VALUES (?, 'وارد', ?, ?, ?, 'مورد', ?, 'شراء من المورد', 1, ?)
        ''',
                       (product_id,
                        quantity,
                        unit_price,
                        total_value,
                        f'PO-{1000+i}',
                        created_at))

    # إنشاء حركات صادر (مبيعات للعملاء)
    for i in range(80):  # 80 حركة صادر
        product_id = random.choice(product_ids)
        quantity = random.randint(5, 100)
        unit_price = random.uniform(10.0, 150.0)
        total_value = quantity * unit_price
        days_ago = random.randint(1, 60)
        created_at = datetime.now() - timedelta(days=days_ago)

        cursor.execute('''
            INSERT INTO stock_movements
            (product_id, movement_type, quantity, unit_price, total_value,
             reference_type, reference_number, notes, user_id, created_at)
            VALUES (?, 'صادر', ?, ?, ?, 'عميل', ?, 'بيع للعميل', 1, ?)
        ''',
                       (product_id,
                        quantity,
                        unit_price,
                        total_value,
                        f'SO-{2000+i}',
                        created_at))

    # تحديث المخزون الحالي للمنتجات بناءً على الحركات
    cursor.execute('''
        UPDATE products
        SET current_stock = (
            SELECT COALESCE(SUM(
                CASE
                    WHEN movement_type = 'وارد' THEN quantity
                    WHEN movement_type = 'صادر' THEN -quantity
                    ELSE 0
                END
            ), 0)
            FROM stock_movements
            WHERE stock_movements.product_id = products.id
        )
    ''')

    # إدراج مخزون المخازن
    cursor.execute('SELECT id FROM warehouses')
    warehouse_ids = [row[0] for row in cursor.fetchall()]

    for product_id in product_ids:
        for warehouse_id in warehouse_ids:
            # توزيع المخزون بشكل عشوائي على المخازن
            cursor.execute(
                'SELECT current_stock FROM products WHERE id = ?',
                (product_id,))
            total_stock = cursor.fetchone()[0]

            if total_stock > 0:
                # توزيع المخزون (المخزن الرئيسي يأخذ النصيب الأكبر)
                if warehouse_id == 1:  # المخزن الرئيسي
                    quantity = int(total_stock * 0.6)
                else:
                    quantity = int(total_stock * 0.4 /
                                   (len(warehouse_ids) - 1))

                if quantity > 0:
                    cursor.execute('''
                        INSERT INTO warehouse_stock (warehouse_id,
                            product_id,
                            quantity)
                        VALUES (?, ?, ?)
                    ''', (warehouse_id, product_id, quantity))

    conn.commit()
    print("تم إدراج جميع البيانات التجريبية بنجاح")


def main():
    """الدالة الرئيسية"""
    print("بدء إعداد قاعدة البيانات...")

    try:
        # إنشاء قاعدة البيانات
        conn = create_database()

        # إدراج البيانات التجريبية
        insert_sample_data(conn)

        # إغلاق الاتصال
        conn.close()

        print("\n" + "=" * 50)
        print("تم إعداد قاعدة البيانات بنجاح!")
        print("=" * 50)
        print("البيانات المدرجة:")
        print("- 5 مستخدمين (admin, manager, accountant, user1, user2)")
        print("- 8 فئات للمنتجات")
        print("- 4 مخازن")
        print("- 28 منتج متنوع")
        print("- 12 عميل")
        print("- 8 موردين")
        print("- 180 حركة مخزون (100 وارد + 80 صادر)")
        print("- توزيع المخزون على المخازن")
        print("\nبيانات تسجيل الدخول:")
        print("- admin / admin123 (مدير النظام)")
        print("- manager / manager123 (مدير المخزون)")
        print("- accountant / accountant123 (محاسب)")
        print("=" * 50)

    except Exception as e:
        print(f"خطأ في إعداد قاعدة البيانات: {e}")
        return False

    return True


if __name__ == "__main__":
    main()
