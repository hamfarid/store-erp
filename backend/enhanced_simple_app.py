#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 الخادم الخلفي المحسن مع نظام المصادقة المتقدم
Enhanced Simple Backend Server with Advanced Authentication

خادم Flask محسن يدعم:
- نظام مصادقة متقدم
- إدارة المستخدمين والأدوار
- حماية نقاط النهاية
- واجهات برمجة تطبيقات شاملة
"""

import os
import sys
import sqlite3
from src.routes.categories import categories_bp
from src.routes.warehouses import warehouses_bp
from src.routes.users import users_bp
from src.routes.inventory import inventory_bp
from src.routes.reports import reports_bp
from datetime import datetime
from flask import Flask, request, jsonify, g
from flask_cors import CORS

# إضافة المسار الجذر للمشروع
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استيراد نظام المصادقة المتقدم
from advanced_auth_system import (
    auth_system,
    require_auth,
    require_admin,
    require_manager,
)

app = Flask(__name__)
# P0.15: Use environment variable for secret key
app.secret_key = os.environ.get("SECRET_KEY") or os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")

# تمكين CORS
CORS(app, supports_credentials=True)

# مسار قاعدة البيانات
DB_PATH = "instance/inventory.db"


def init_database():
    """تهيئة قاعدة البيانات مع البيانات الأساسية"""
    print("✅ تم تهيئة قاعدة البيانات")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # إنشاء الجداول الأساسية
    tables = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "categories": """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """,
        "warehouses": """
            CREATE TABLE IF NOT EXISTS warehouses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                location TEXT,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """,
        "products": """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT UNIQUE,
                description TEXT,
                category_id INTEGER,
                price DECIMAL(10,2) DEFAULT 0,
                cost DECIMAL(10,2) DEFAULT 0,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """,
    }

    for table_name, table_sql in tables.items():
        cursor.execute(table_sql)

    # P0.16: إنشاء المستخدم الإداري الافتراضي باستخدام متغير بيئي
    import secrets

    default_admin_password = os.environ.get("DEFAULT_ADMIN_PASSWORD")
    if not default_admin_password:
        # Generate secure random password for development
        default_admin_password = secrets.token_urlsafe(16)

    admin_result = auth_system.create_user(
        username="admin",
        password=default_admin_password,
        email="admin@inventory.com",
        full_name="مدير النظام",
        role="admin",
    )

    if admin_result["success"]:
        print(f"👤 تم إنشاء المستخدم الإداري: admin / {default_admin_password}")
        print("⚠️  SECURITY: Change this password immediately in production!")

    # إضافة بيانات تجريبية
    sample_data = [
        # الفئات
        (
            "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
            [
                ("إلكترونيات", "أجهزة إلكترونية ومعدات"),
                ("مكتبية", "لوازم مكتبية وقرطاسية"),
                ("منظفات", "مواد تنظيف ومطهرات"),
                ("غذائية", "مواد غذائية ومشروبات"),
                ("طبية", "مستلزمات طبية وأدوية"),
            ],
        ),
        # المستودعات
        (
            "INSERT OR IGNORE INTO warehouses (name, location, description) VALUES (?, ?, ?)",
            [
                ("المستودع الرئيسي", "الرياض - حي الصناعية", "المستودع الرئيسي للشركة"),
                ("مستودع جدة", "جدة - حي الحمراء", "فرع جدة"),
                ("مستودع الدمام", "الدمام - الكورنيش", "فرع المنطقة الشرقية"),
            ],
        ),
    ]

    for query, data_list in sample_data:
        for data in data_list:
            cursor.execute(query, data)

    conn.commit()
    conn.close()


# تهيئة قاعدة البيانات عند بدء التطبيق
init_database()

# ===== نقاط النهاية العامة =====


@app.route("/api/status", methods=["GET"])
def get_status():
    """حالة الخادم"""
    return jsonify(
        {
            "success": True,
            "message": "الخادم يعمل بشكل طبيعي",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
        }
    )


# ===== نقاط نهاية المصادقة =====


@app.route("/api/auth/login", methods=["POST"])
def login():
    """تسجيل الدخول"""
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return (
            jsonify({"success": False, "error": "اسم المستخدم وكلمة المرور مطلوبان"}),
            400,
        )

    result = auth_system.authenticate_user(data["username"], data["password"])

    if result["success"]:
        # إعداد الكوكي للجلسة
        response = jsonify(result)
        response.set_cookie(
            "session_token",
            result["session_token"],
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        return response
    else:
        return jsonify(result), 401


@app.route("/api/auth/logout", methods=["POST"])
@require_auth()
def logout():
    """تسجيل الخروج"""
    session_token = request.cookies.get("session_token")
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header[7:]

    result = auth_system.logout_user(session_token)

    if result["success"]:
        response = jsonify(result)
        response.set_cookie("session_token", "", expires=0)
        return response
    else:
        return jsonify(result), 400


@app.route("/api/auth/me", methods=["GET"])
@require_auth()
def get_current_user():
    """الحصول على بيانات المستخدم الحالي"""
    return jsonify({"success": True, "user": g.current_user})


# ===== نقاط نهاية إدارة المستخدمين =====


@app.route("/api/users", methods=["GET"])
@require_auth("read")
def get_users():
    """الحصول على قائمة المستخدمين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT u.id, u.username, u.email, u.full_name, u.is_active, u.created_at,
               GROUP_CONCAT(r.name) as roles
        FROM users u
        LEFT JOIN user_roles ur ON u.id = ur.user_id
        LEFT JOIN roles r ON ur.role_id = r.id
        GROUP BY u.id
        ORDER BY u.created_at DESC
    """
    )

    users = []
    for row in cursor.fetchall():
        users.append(
            {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "full_name": row[3],
                "is_active": bool(row[4]),
                "created_at": row[5],
                "roles": row[6].split(",") if row[6] else [],
            }
        )

    conn.close()

    return jsonify({"success": True, "users": users})


@app.route("/api/users", methods=["POST"])
@require_admin()
def create_user():
    """إنشاء مستخدم جديد"""
    data = request.get_json()

    required_fields = ["username", "password", "email", "full_name"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "error": f"الحقل {field} مطلوب"}), 400

    result = auth_system.create_user(
        username=data["username"],
        password=data["password"],
        email=data["email"],
        full_name=data["full_name"],
        role=data.get("role", "employee"),
    )

    if result["success"]:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


# ===== نقاط نهاية الفئات =====


@app.route("/api/categories", methods=["GET"])
@require_auth("read")
def get_categories():
    """الحصول على الفئات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.id, c.name, c.description, c.created_at, u.full_name as created_by_name
        FROM categories c
        LEFT JOIN users u ON c.created_by = u.id
        ORDER BY c.name
    """
    )

    categories = []
    for row in cursor.fetchall():
        categories.append(
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_at": row[3],
                "created_by_name": row[4],
            }
        )

    conn.close()

    return jsonify({"success": True, "categories": categories})


@app.route("/api/categories", methods=["POST"])
@require_auth("write")
def create_category():
    """إنشاء فئة جديدة"""
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"success": False, "error": "اسم الفئة مطلوب"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO categories (name, description, created_by)
            VALUES (?, ?, ?)
        """,
            (data["name"], data.get("description", ""), g.current_user["id"]),
        )

        category_id = cursor.lastrowid
        conn.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "تم إنشاء الفئة بنجاح",
                    "category_id": category_id,
                }
            ),
            201,
        )

    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "اسم الفئة موجود بالفعل"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


# ===== نقاط نهاية المستودعات =====


@app.route("/api/warehouses", methods=["GET"])
@require_auth("read")
def get_warehouses():
    """الحصول على المستودعات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT w.id, w.name, w.location, w.description, w.is_active, w.created_at,
               u.full_name as created_by_name
        FROM warehouses w
        LEFT JOIN users u ON w.created_by = u.id
        ORDER BY w.name
    """
    )

    warehouses = []
    for row in cursor.fetchall():
        warehouses.append(
            {
                "id": row[0],
                "name": row[1],
                "location": row[2],
                "description": row[3],
                "is_active": bool(row[4]),
                "created_at": row[5],
                "created_by_name": row[6],
            }
        )

    conn.close()

    return jsonify({"success": True, "warehouses": warehouses})


@app.route("/api/warehouses", methods=["POST"])
@require_auth("write")
def create_warehouse():
    """إنشاء مستودع جديد"""
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"success": False, "error": "اسم المستودع مطلوب"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO warehouses (name, location, description, created_by)
            VALUES (?, ?, ?, ?)
        """,
            (
                data["name"],
                data.get("location", ""),
                data.get("description", ""),
                g.current_user["id"],
            ),
        )

        warehouse_id = cursor.lastrowid
        conn.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "تم إنشاء المستودع بنجاح",
                    "warehouse_id": warehouse_id,
                }
            ),
            201,
        )

    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "اسم المستودع موجود بالفعل"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


# ===== نقاط نهاية المنتجات =====


@app.route("/api/products", methods=["GET"])
@require_auth("read")
def get_products():
    """الحصول على المنتجات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT p.id, p.name, p.sku, p.description, p.price, p.cost, p.quantity,
               p.min_quantity, p.is_active, p.created_at,
               c.name as category_name, u.full_name as created_by_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN users u ON p.created_by = u.id
        ORDER BY p.name
    """
    )

    products = []
    for row in cursor.fetchall():
        products.append(
            {
                "id": row[0],
                "name": row[1],
                "sku": row[2],
                "description": row[3],
                "price": float(row[4]) if row[4] else 0,
                "cost": float(row[5]) if row[5] else 0,
                "quantity": row[6],
                "min_quantity": row[7],
                "is_active": bool(row[8]),
                "created_at": row[9],
                "category_name": row[10],
                "created_by_name": row[11],
            }
        )

    conn.close()

    return jsonify({"success": True, "products": products})


@app.route("/api/products", methods=["POST"])
@require_auth("write")
def create_product():
    """إنشاء منتج جديد"""
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"success": False, "error": "اسم المنتج مطلوب"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO products (name, sku, description, category_id, price, cost,
                                quantity, min_quantity, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                data["name"],
                data.get("sku"),
                data.get("description", ""),
                data.get("category_id"),
                data.get("price", 0),
                data.get("cost", 0),
                data.get("quantity", 0),
                data.get("min_quantity", 0),
                g.current_user["id"],
            ),
        )

        product_id = cursor.lastrowid
        conn.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "تم إنشاء المنتج بنجاح",
                    "product_id": product_id,
                }
            ),
            201,
        )

    except sqlite3.IntegrityError:
        return (
            jsonify({"success": False, "error": "رمز المنتج (SKU) موجود بالفعل"}),
            400,
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


# ===== نقاط نهاية التقارير =====


@app.route("/api/reports/dashboard", methods=["GET"])
@require_auth("read")
def get_dashboard_stats():
    """إحصائيات لوحة التحكم"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # إحصائيات عامة
    stats = {}

    # عدد المنتجات
    cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
    stats["total_products"] = cursor.fetchone()[0]

    # عدد الفئات
    cursor.execute("SELECT COUNT(*) FROM categories")
    stats["total_categories"] = cursor.fetchone()[0]

    # عدد المستودعات
    cursor.execute("SELECT COUNT(*) FROM warehouses WHERE is_active = 1")
    stats["total_warehouses"] = cursor.fetchone()[0]

    # عدد المستخدمين
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
    stats["total_users"] = cursor.fetchone()[0]

    # المنتجات منخفضة المخزون
    cursor.execute(
        "SELECT COUNT(*) FROM products WHERE quantity <= min_quantity AND is_active = 1"
    )
    stats["low_stock_products"] = cursor.fetchone()[0]

    # إجمالي قيمة المخزون
    cursor.execute("SELECT SUM(quantity * cost) FROM products WHERE is_active = 1")
    result = cursor.fetchone()[0]
    stats["total_inventory_value"] = float(result) if result else 0

    conn.close()

    return jsonify(
        {"success": True, "stats": stats, "timestamp": datetime.now().isoformat()}
    )


# نقطة نهاية لوحة التحكم
@app.route("/api/reports/dashboard", methods=["GET"])
def get_dashboard():
    """الحصول على بيانات لوحة التحكم"""
    try:
        conn = sqlite3.connect("instance/inventory.db")
        cursor = conn.cursor()

        # إحصائيات أساسية
        stats = {}

        # عدد المنتجات
        cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
        stats["total_products"] = cursor.fetchone()[0]

        # عدد الفئات
        cursor.execute("SELECT COUNT(*) FROM categories")
        stats["total_categories"] = cursor.fetchone()[0]

        # عدد المستودعات
        cursor.execute("SELECT COUNT(*) FROM warehouses")
        stats["total_warehouses"] = cursor.fetchone()[0]

        # عدد المستخدمين النشطين
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        stats["active_users"] = cursor.fetchone()[0]

        # المنتجات منخفضة المخزون
        cursor.execute(
            "SELECT COUNT(*) FROM products WHERE quantity <= min_quantity AND is_active = 1"
        )
        stats["low_stock_products"] = cursor.fetchone()[0]

        # إجمالي قيمة المخزون
        cursor.execute("SELECT SUM(quantity * cost) FROM products WHERE is_active = 1")
        total_value = cursor.fetchone()[0]
        stats["total_inventory_value"] = total_value if total_value else 0

        # أحدث المنتجات المضافة
        cursor.execute(
            """
            SELECT name, sku, quantity, created_at 
            FROM products 
            WHERE is_active = 1 
            ORDER BY created_at DESC 
            LIMIT 5
        """
        )
        recent_products = []
        for row in cursor.fetchall():
            recent_products.append(
                {
                    "name": row[0],
                    "sku": row[1],
                    "quantity": row[2],
                    "created_at": row[3],
                }
            )

        # المنتجات منخفضة المخزون (تفصيلي)
        cursor.execute(
            """
            SELECT name, sku, quantity, min_quantity 
            FROM products 
            WHERE quantity <= min_quantity AND is_active = 1 
            ORDER BY quantity ASC 
            LIMIT 10
        """
        )
        low_stock_details = []
        for row in cursor.fetchall():
            low_stock_details.append(
                {
                    "name": row[0],
                    "sku": row[1],
                    "current_quantity": row[2],
                    "min_quantity": row[3],
                }
            )

        conn.close()

        dashboard_data = {
            "success": True,
            "data": {
                "statistics": stats,
                "recent_products": recent_products,
                "low_stock_products": low_stock_details,
                "timestamp": datetime.now().isoformat(),
            },
        }

        return jsonify(dashboard_data)

    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"خطأ في الحصول على بيانات لوحة التحكم: {str(e)}",
                }
            ),
            500,
        )


app.register_blueprint(categories_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(users_bp)
app.register_blueprint(warehouses_bp)

if __name__ == "__main__":
    print("✅ تم تهيئة قاعدة البيانات")
    print("🚀 بدء تشغيل الخادم الخلفي المحسن...")
    print("📍 الخادم متاح على: http://localhost:5002")
    print("👤 المستخدم الإداري: admin / admin123")

    app.run(host="0.0.0.0", port=5002, debug=True)
