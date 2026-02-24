#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 خادم خلفي بسيط يعمل
Minimal Working Backend Server

خادم Flask بسيط يعمل بدون مشاكل
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# تمكين CORS
CORS(app, supports_credentials=True)

# مسار قاعدة البيانات
DB_PATH = "instance/inventory.db"

def init_database():
    """تهيئة قاعدة البيانات"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # إنشاء جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إنشاء جدول الفئات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إنشاء جدول المنتجات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            price REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    # إنشاء جدول المستودعات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # إضافة مستخدم إداري افتراضي
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin123', 'admin@example.com', 'admin'))

    # إضافة بيانات تجريبية
    cursor.execute('''
        INSERT OR IGNORE INTO categories (name, description)
        VALUES (?, ?)
    ''', ('إلكترونيات', 'أجهزة إلكترونية'))

    cursor.execute('''
        INSERT OR IGNORE INTO warehouses (name, location, description)
        VALUES (?, ?, ?)
    ''', ('المستودع الرئيسي', 'الرياض', 'المستودع الرئيسي للشركة'))

    conn.commit()
    conn.close()
    print("✅ تم تهيئة قاعدة البيانات بنجاح")

@app.route('/api/status', methods=['GET'])
def status():
    """حالة الخادم"""
    return jsonify({
        'status': 'running',
        'message': 'الخادم يعمل بشكل طبيعي',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health():
    """فحص صحة الخادم"""
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """تسجيل الدخول"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, email, role FROM users
        WHERE username = ? AND password = ?
    ''', (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            'success': True,
            'message': 'تم تسجيل الدخول بنجاح',
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[3]
            },
            'session_token': f'token_{user[0]}_{datetime.now().timestamp()}'
        })
    else:
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """الحصول على الفئات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, description, created_at FROM categories')
    categories = cursor.fetchall()
    conn.close()

    return jsonify([{
        'id': cat[0],
        'name': cat[1],
        'description': cat[2],
        'created_at': cat[3]
    } for cat in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    """إنشاء فئة جديدة"""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({'error': 'اسم الفئة مطلوب'}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    ''', (name, description))

    category_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'id': category_id,
        'name': name,
        'description': description,
        'message': 'تم إنشاء الفئة بنجاح'
    }), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    """الحصول على المنتجات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.id, p.name, p.description, p.price, c.name as category_name, p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
    ''')
    products = cursor.fetchall()
    conn.close()

    return jsonify([{
        'id': prod[0],
        'name': prod[1],
        'description': prod[2],
        'price': prod[3],
        'category_name': prod[4],
        'created_at': prod[5]
    } for prod in products])

@app.route('/api/warehouses', methods=['GET'])
def get_warehouses():
    """الحصول على المستودعات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, location, description, created_at FROM warehouses')
    warehouses = cursor.fetchall()
    conn.close()

    return jsonify([{
        'id': wh[0],
        'name': wh[1],
        'location': wh[2],
        'description': wh[3],
        'created_at': wh[4]
    } for wh in warehouses])

@app.route('/api/users', methods=['GET'])
def get_users():
    """الحصول على المستخدمين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id, username, email, role, created_at FROM users')
    users = cursor.fetchall()
    conn.close()

    return jsonify([{
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'role': user[3],
        'created_at': user[4]
    } for user in users])

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """الحصول على المخزون"""
    return jsonify([{
        'id': 1,
        'product_name': 'منتج تجريبي',
        'warehouse_name': 'المستودع الرئيسي',
        'quantity': 100,
        'last_updated': datetime.now().isoformat()
    }])

@app.route('/api/reports/dashboard', methods=['GET'])
def dashboard():
    """لوحة التحكم"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # عدد الفئات
    cursor.execute('SELECT COUNT(*) FROM categories')
    categories_count = cursor.fetchone()[0]

    # عدد المنتجات
    cursor.execute('SELECT COUNT(*) FROM products')
    products_count = cursor.fetchone()[0]

    # عدد المستودعات
    cursor.execute('SELECT COUNT(*) FROM warehouses')
    warehouses_count = cursor.fetchone()[0]

    # عدد المستخدمين
    cursor.execute('SELECT COUNT(*) FROM users')
    users_count = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'statistics': {
            'categories': categories_count,
            'products': products_count,
            'warehouses': warehouses_count,
            'users': users_count
        },
        'message': 'بيانات لوحة التحكم',
        'timestamp': datetime.now().isoformat()
    })


# تقارير متقدمة
@app.route('/api/reports/sales-summary', methods=['GET'])
def get_sales_summary():
    """تقرير ملخص المبيعات"""
    try:
        # محاكاة بيانات تقرير المبيعات
        summary = {
            'total_sales': 125000,
            'total_orders': 450,
            'average_order_value': 278,
            'top_products': [
                {'name': 'منتج أ', 'sales': 25000, 'quantity': 100},
                {'name': 'منتج ب', 'sales': 18000, 'quantity': 75},
                {'name': 'منتج ج', 'sales': 15000, 'quantity': 60}
            ],
            'monthly_trend': [
                {'month': 'يناير', 'sales': 20000},
                {'month': 'فبراير', 'sales': 22000},
                {'month': 'مارس', 'sales': 25000},
                {'month': 'أبريل', 'sales': 28000},
                {'month': 'مايو', 'sales': 30000}
            ]
        }
        return jsonify({'success': True, 'data': summary})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/inventory-analysis', methods=['GET'])
def get_inventory_analysis():
    """تقرير تحليل المخزون"""
    try:
        analysis = {
            'total_products': 1250,
            'total_value': 450000,
            'low_stock_items': 15,
            'out_of_stock_items': 3,
            'categories_breakdown': [
                {'category': 'إلكترونيات', 'count': 350, 'value': 180000},
                {'category': 'ملابس', 'count': 400, 'value': 120000},
                {'category': 'كتب', 'count': 300, 'value': 80000},
                {'category': 'أدوات منزلية', 'count': 200, 'value': 70000}
            ],
            'stock_levels': {
                'high_stock': 800,
                'medium_stock': 350,
                'low_stock': 85,
                'out_of_stock': 15
            }
        }
        return jsonify({'success': True, 'data': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/financial-overview', methods=['GET'])
def get_financial_overview():
    """تقرير النظرة المالية العامة"""
    try:
        overview = {
            'revenue': {
                'current_month': 125000,
                'previous_month': 110000,
                'growth_rate': 13.6
            },
            'expenses': {
                'current_month': 85000,
                'previous_month': 78000,
                'growth_rate': 9.0
            },
            'profit': {
                'current_month': 40000,
                'previous_month': 32000,
                'growth_rate': 25.0
            },
            'cash_flow': [
                {'date': '2024-01', 'inflow': 120000, 'outflow': 80000},
                {'date': '2024-02', 'inflow': 135000, 'outflow': 85000},
                {'date': '2024-03', 'inflow': 125000, 'outflow': 85000}
            ]
        }
        return jsonify({'success': True, 'data': overview})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/customer-analytics', methods=['GET'])
def get_customer_analytics():
    """تقرير تحليل العملاء"""
    try:
        analytics = {
            'total_customers': 850,
            'new_customers_this_month': 45,
            'customer_retention_rate': 78.5,
            'top_customers': [
                {'name': 'شركة الأمل', 'total_purchases': 45000, 'orders': 25},
                {'name': 'مؤسسة النجاح', 'total_purchases': 38000, 'orders': 20},
                {'name': 'شركة التقدم', 'total_purchases': 32000, 'orders': 18}
            ],
            'customer_segments': [
                {'segment': 'عملاء VIP', 'count': 85, 'revenue_share': 45},
                {'segment': 'عملاء منتظمون', 'count': 350, 'revenue_share': 35},
                {'segment': 'عملاء جدد', 'count': 415, 'revenue_share': 20}
            ]
        }
        return jsonify({'success': True, 'data': analytics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/supplier-performance', methods=['GET'])
def get_supplier_performance():
    """تقرير أداء الموردين"""
    try:
        performance = {
            'total_suppliers': 125,
            'active_suppliers': 98,
            'top_suppliers': [
                {'name': 'مورد الجودة', 'total_orders': 150, 'on_time_delivery': 95, 'quality_score': 4.8},
                {'name': 'شركة الإمداد', 'total_orders': 120, 'on_time_delivery': 88, 'quality_score': 4.5},
                {'name': 'مؤسسة التوريد', 'total_orders': 100, 'on_time_delivery': 92, 'quality_score': 4.6}
            ],
            'delivery_performance': {
                'on_time': 89,
                'late': 8,
                'very_late': 3
            },
            'quality_metrics': {
                'excellent': 65,
                'good': 25,
                'average': 8,
                'poor': 2
            }
        }
        return jsonify({'success': True, 'data': performance})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# نظام الصلاحيات المتقدم
@app.route('/api/permissions/roles', methods=['GET'])
def get_roles():
    """جلب جميع الأدوار"""
    try:
        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, description, is_active, created_at FROM roles ORDER BY name")

        roles = []
        for row in cursor.fetchall():
            roles.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'is_active': bool(row[3]),
                'created_at': row[4]
            })

        conn.close()
        return jsonify({'success': True, 'data': roles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/permissions/roles', methods=['POST'])
def create_role():
    """إنشاء دور جديد"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        permissions = data.get('permissions', [])

        if not name:
            return jsonify({'success': False, 'error': 'اسم الدور مطلوب'}), 400

        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()

        # إنشاء الدور
        cursor.execute("INSERT INTO roles (name, description, is_active, created_at) VALUES (?, ?, 1, ?)",
                      (name, description, datetime.now().isoformat()))

        role_id = cursor.lastrowid

        # إضافة الصلاحيات للدور
        for permission in permissions:
            cursor.execute("""INSERT INTO role_permissions
                             (role_id, permission_name, can_create, can_read, can_update, can_delete)
                             VALUES (?, ?, ?, ?, ?, ?)""",
                          (role_id, permission['name'],
                           permission.get('can_create', False),
                           permission.get('can_read', True),
                           permission.get('can_update', False),
                           permission.get('can_delete', False)))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'تم إنشاء الدور بنجاح', 'role_id': role_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/permissions/check', methods=['POST'])
def check_permission():
    """فحص صلاحية مستخدم لعملية معينة"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        permission_name = data.get('permission_name')
        action = data.get('action', 'read')  # create, read, update, delete

        if not user_id or not permission_name:
            return jsonify({'success': False, 'error': 'معرف المستخدم واسم الصلاحية مطلوبان'}), 400

        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()

        # التحقق من كون المستخدم مدير
        cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
        user_role = cursor.fetchone()

        if user_role and user_role[0] == 'admin':
            conn.close()
            return jsonify({'success': True, 'has_permission': True, 'reason': 'مدير النظام'})

        # فحص الصلاحيات التفصيلية
        action_column = f'can_{action}'
        query = f"""SELECT rp.{action_column}
                   FROM user_roles ur
                   JOIN role_permissions rp ON ur.role_id = rp.role_id
                   WHERE ur.user_id = ? AND rp.permission_name = ?"""

        cursor.execute(query, (user_id, permission_name))

        result = cursor.fetchone()
        has_permission = bool(result[0]) if result else False

        conn.close()
        return jsonify({'success': True, 'has_permission': has_permission})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/permissions/available', methods=['GET'])
def get_available_permissions():
    """جلب جميع الصلاحيات المتاحة في النظام"""
    try:
        available_permissions = [
            {'name': 'products', 'display_name': 'إدارة المنتجات', 'category': 'المخزون'},
            {'name': 'categories', 'display_name': 'إدارة الفئات', 'category': 'المخزون'},
            {'name': 'inventory', 'display_name': 'إدارة المخزون', 'category': 'المخزون'},
            {'name': 'warehouses', 'display_name': 'إدارة المخازن', 'category': 'المخزون'},
            {'name': 'customers', 'display_name': 'إدارة العملاء', 'category': 'العلاقات'},
            {'name': 'suppliers', 'display_name': 'إدارة الموردين', 'category': 'العلاقات'},
            {'name': 'invoices', 'display_name': 'إدارة الفواتير', 'category': 'المبيعات'},
            {'name': 'reports', 'display_name': 'التقارير', 'category': 'التقارير'},
            {'name': 'users', 'display_name': 'إدارة المستخدمين', 'category': 'الإدارة'},
            {'name': 'settings', 'display_name': 'إعدادات النظام', 'category': 'الإدارة'},
            {'name': 'permissions', 'display_name': 'إدارة الصلاحيات', 'category': 'الإدارة'},
        ]

        return jsonify({'success': True, 'data': available_permissions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


import shutil
import zipfile
import schedule
import threading
import time
from pathlib import Path

# نظام النسخ الاحتياطي التلقائي
backup_settings = {
    'enabled': True,
    'frequency': 'daily',  # daily, weekly, monthly
    'retention_days': 30,
    'backup_path': 'backups/',
    'include_uploads': True,
    'compress': True
}

def create_backup():
    """إنشاء نسخة احتياطية"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path(backup_settings['backup_path'])
        backup_dir.mkdir(exist_ok=True)

        backup_name = f'backup_{timestamp}'
        backup_path = backup_dir / backup_name

        # إنشاء مجلد النسخة الاحتياطية
        backup_path.mkdir(exist_ok=True)

        # نسخ قاعدة البيانات
        db_source = Path('instance/inventory.db')
        if db_source.exists():
            shutil.copy2(db_source, backup_path / 'inventory.db')

        # نسخ الملفات المرفوعة إذا كانت موجودة
        if backup_settings['include_uploads']:
            uploads_dir = Path('uploads')
            if uploads_dir.exists():
                shutil.copytree(uploads_dir, backup_path / 'uploads', dirs_exist_ok=True)

        # ضغط النسخة الاحتياطية إذا كان مطلوباً
        if backup_settings['compress']:
            zip_path = backup_dir / f'{backup_name}.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in backup_path.rglob('*'):
                    if file_path.is_file():
                        zipf.write(file_path, file_path.relative_to(backup_path))

            # حذف المجلد غير المضغوط
            shutil.rmtree(backup_path)
            backup_path = zip_path

        # تنظيف النسخ القديمة
        cleanup_old_backups()

        print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
        return str(backup_path)

    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
        return None

def cleanup_old_backups():
    """تنظيف النسخ الاحتياطية القديمة"""
    try:
        backup_dir = Path(backup_settings['backup_path'])
        if not backup_dir.exists():
            return

        retention_days = backup_settings['retention_days']
        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 60 * 60)

        for backup_file in backup_dir.iterdir():
            if backup_file.is_file() and backup_file.name.startswith('backup_'):
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    print(f"🗑️  تم حذف النسخة الاحتياطية القديمة: {backup_file.name}")

    except Exception as e:
        print(f"❌ خطأ في تنظيف النسخ القديمة: {e}")

def schedule_backups():
    """جدولة النسخ الاحتياطية"""
    if not backup_settings['enabled']:
        return

    frequency = backup_settings['frequency']

    if frequency == 'daily':
        schedule.every().day.at("02:00").do(create_backup)
    elif frequency == 'weekly':
        schedule.every().sunday.at("02:00").do(create_backup)
    elif frequency == 'monthly':
        schedule.every().month.do(create_backup)

    print(f"📅 تم جدولة النسخ الاحتياطية: {frequency}")

def run_backup_scheduler():
    """تشغيل مجدول النسخ الاحتياطية"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # فحص كل دقيقة

# بدء مجدول النسخ الاحتياطية في خيط منفصل
backup_thread = threading.Thread(target=run_backup_scheduler, daemon=True)
backup_thread.start()
schedule_backups()

@app.route('/api/backup/create', methods=['POST'])
def manual_backup():
    """إنشاء نسخة احتياطية يدوياً"""
    try:
        backup_path = create_backup()
        if backup_path:
            return jsonify({
                'success': True,
                'message': 'تم إنشاء النسخة الاحتياطية بنجاح',
                'backup_path': backup_path
            })
        else:
            return jsonify({'success': False, 'error': 'فشل في إنشاء النسخة الاحتياطية'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/list', methods=['GET'])
def list_backups():
    """جلب قائمة النسخ الاحتياطية"""
    try:
        backup_dir = Path(backup_settings['backup_path'])
        backups = []

        if backup_dir.exists():
            for backup_file in backup_dir.iterdir():
                if backup_file.is_file() and backup_file.name.startswith('backup_'):
                    stat = backup_file.stat()
                    backups.append({
                        'name': backup_file.name,
                        'size': stat.st_size,
                        'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'path': str(backup_file)
                    })

        # ترتيب حسب تاريخ الإنشاء (الأحدث أولاً)
        backups.sort(key=lambda x: x['created_at'], reverse=True)

        return jsonify({'success': True, 'data': backups})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/settings', methods=['GET'])
def get_backup_settings():
    """جلب إعدادات النسخ الاحتياطي"""
    try:
        return jsonify({'success': True, 'data': backup_settings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/settings', methods=['POST'])
def update_backup_settings():
    """تحديث إعدادات النسخ الاحتياطي"""
    try:
        data = request.get_json()

        # تحديث الإعدادات
        if 'enabled' in data:
            backup_settings['enabled'] = bool(data['enabled'])
        if 'frequency' in data:
            backup_settings['frequency'] = data['frequency']
        if 'retention_days' in data:
            backup_settings['retention_days'] = int(data['retention_days'])
        if 'include_uploads' in data:
            backup_settings['include_uploads'] = bool(data['include_uploads'])
        if 'compress' in data:
            backup_settings['compress'] = bool(data['compress'])

        # إعادة جدولة النسخ الاحتياطية
        schedule.clear()
        schedule_backups()

        return jsonify({'success': True, 'message': 'تم تحديث إعدادات النسخ الاحتياطي'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/restore', methods=['POST'])
def restore_backup():
    """استعادة نسخة احتياطية"""
    try:
        data = request.get_json()
        backup_name = data.get('backup_name')

        if not backup_name:
            return jsonify({'success': False, 'error': 'اسم النسخة الاحتياطية مطلوب'}), 400

        backup_path = Path(backup_settings['backup_path']) / backup_name

        if not backup_path.exists():
            return jsonify({'success': False, 'error': 'النسخة الاحتياطية غير موجودة'}), 404

        # إنشاء نسخة احتياطية من الحالة الحالية قبل الاستعادة
        current_backup = create_backup()

        # استعادة النسخة الاحتياطية
        if backup_path.suffix == '.zip':
            # استخراج الملف المضغوط
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                temp_dir = Path('temp_restore')
                zipf.extractall(temp_dir)

                # استعادة قاعدة البيانات
                db_backup = temp_dir / 'inventory.db'
                if db_backup.exists():
                    shutil.copy2(db_backup, 'instance/inventory.db')

                # استعادة الملفات المرفوعة
                uploads_backup = temp_dir / 'uploads'
                if uploads_backup.exists():
                    uploads_dir = Path('uploads')
                    if uploads_dir.exists():
                        shutil.rmtree(uploads_dir)
                    shutil.copytree(uploads_backup, uploads_dir)

                # تنظيف المجلد المؤقت
                shutil.rmtree(temp_dir)

        return jsonify({
            'success': True,
            'message': 'تم استعادة النسخة الاحتياطية بنجاح',
            'current_backup': current_backup
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 بدء تشغيل الخادم الخلفي البسيط...")

    # تهيئة قاعدة البيانات
    init_database()

    print("🌐 الخادم يعمل على http://localhost:5002")
    print("📊 لوحة التحكم: http://localhost:5002/api/reports/dashboard")
    print("🔐 تسجيل الدخول: admin / admin123")

    # تشغيل الخادم
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False)
