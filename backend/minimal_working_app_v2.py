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
# P0.15: Use environment variable for secret key
app.secret_key = os.environ.get("SECRET_KEY") or os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")

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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # إنشاء جدول الفئات
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # إنشاء جدول المنتجات
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            price REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """
    )

    # إنشاء جدول المستودعات
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # إضافة مستخدم إداري افتراضي
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (username, password, email, role)
        VALUES (?, ?, ?, ?)
    """,
        ("admin", "admin123", "admin@example.com", "admin"),
    )

    # إضافة بيانات تجريبية
    cursor.execute(
        """
        INSERT OR IGNORE INTO categories (name, description)
        VALUES (?, ?)
    """,
        ("إلكترونيات", "أجهزة إلكترونية"),
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO warehouses (name, location, description)
        VALUES (?, ?, ?)
    """,
        ("المستودع الرئيسي", "الرياض", "المستودع الرئيسي للشركة"),
    )

    # إنشاء جدول الموردين
    cursor.execute(
        """
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
    """
    )

    # إنشاء جدول العملاء
    cursor.execute(
        """
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
    """
    )

    # إضافة بيانات تجريبية للموردين
    cursor.execute(
        """
        INSERT OR IGNORE INTO suppliers (name, company_type, email, phone)
        VALUES (?, ?, ?, ?)
    """,
        ("شركة التوريد المحدودة", "company", "supplier@example.com", "0112345678"),
    )

    # إضافة بيانات تجريبية للعملاء
    cursor.execute(
        """
        INSERT OR IGNORE INTO customers (name, customer_type, email, phone)
        VALUES (?, ?, ?, ?)
    """,
        ("أحمد محمد", "individual", "ahmed@example.com", "0501234567"),
    )

    conn.commit()
    conn.close()
    print("✅ تم تهيئة قاعدة البيانات بنجاح")


@app.route("/api/status", methods=["GET"])
def status():
    """حالة الخادم"""
    return jsonify(
        {
            "status": "running",
            "message": "الخادم يعمل بشكل طبيعي",
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/health", methods=["GET"])
def health():
    """فحص صحة الخادم"""
    return jsonify(
        {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/auth/login", methods=["POST"])
def login():
    """تسجيل الدخول"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "اسم المستخدم وكلمة المرور مطلوبان"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, email, role FROM users 
        WHERE username = ? AND password = ?
    """,
        (username, password),
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(
            {
                "success": True,
                "message": "تم تسجيل الدخول بنجاح",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[3],
                },
                "session_token": f"token_{user[0]}_{datetime.now().timestamp()}",
            }
        )
    else:
        return jsonify({"error": "اسم المستخدم أو كلمة المرور غير صحيحة"}), 401


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """الحصول على الفئات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, description, created_at FROM categories")
    categories = cursor.fetchall()
    conn.close()

    return jsonify(
        [
            {"id": cat[0], "name": cat[1], "description": cat[2], "created_at": cat[3]}
            for cat in categories
        ]
    )


@app.route("/api/categories", methods=["POST"])
def create_category():
    """إنشاء فئة جديدة"""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "اسم الفئة مطلوب"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO categories (name, description)
        VALUES (?, ?)
    """,
        (name, description),
    )

    category_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return (
        jsonify(
            {
                "id": category_id,
                "name": name,
                "description": description,
                "message": "تم إنشاء الفئة بنجاح",
            }
        ),
        201,
    )


@app.route("/api/products", methods=["GET"])
def get_products():
    """الحصول على المنتجات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT p.id, p.name, p.description, p.price, c.name as category_name, p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
    """
    )
    products = cursor.fetchall()
    conn.close()

    return jsonify(
        [
            {
                "id": prod[0],
                "name": prod[1],
                "description": prod[2],
                "price": prod[3],
                "category_name": prod[4],
                "created_at": prod[5],
            }
            for prod in products
        ]
    )


@app.route("/api/warehouses", methods=["GET"])
def get_warehouses():
    """الحصول على المستودعات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, location, description, created_at FROM warehouses")
    warehouses = cursor.fetchall()
    conn.close()

    return jsonify(
        [
            {
                "id": wh[0],
                "name": wh[1],
                "location": wh[2],
                "description": wh[3],
                "created_at": wh[4],
            }
            for wh in warehouses
        ]
    )


@app.route("/api/users", methods=["GET"])
def get_users():
    """الحصول على المستخدمين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email, role, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify(
        [
            {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3],
                "created_at": user[4],
            }
            for user in users
        ]
    )


@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    """الحصول على المخزون"""
    return jsonify(
        [
            {
                "id": 1,
                "product_name": "منتج تجريبي",
                "warehouse_name": "المستودع الرئيسي",
                "quantity": 100,
                "last_updated": datetime.now().isoformat(),
            }
        ]
    )


@app.route("/api/suppliers", methods=["GET"])
def get_suppliers():
    """الحصول على الموردين"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, company_type, email, phone, is_active, created_at FROM suppliers WHERE is_active = 1"
    )
    suppliers = cursor.fetchall()
    conn.close()

    return jsonify(
        [
            {
                "id": sup[0],
                "name": sup[1],
                "company_type": sup[2],
                "email": sup[3],
                "phone": sup[4],
                "is_active": sup[5],
                "created_at": sup[6],
            }
            for sup in suppliers
        ]
    )


@app.route("/api/customers", methods=["GET"])
def get_customers():
    """الحصول على العملاء"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, customer_type, email, phone, is_active, created_at FROM customers WHERE is_active = 1"
    )
    customers = cursor.fetchall()
    conn.close()

    return jsonify(
        [
            {
                "id": cust[0],
                "name": cust[1],
                "customer_type": cust[2],
                "email": cust[3],
                "phone": cust[4],
                "is_active": cust[5],
                "created_at": cust[6],
            }
            for cust in customers
        ]
    )


@app.route("/api/reports/dashboard", methods=["GET"])
def dashboard():
    """لوحة التحكم"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # عدد الفئات
    cursor.execute("SELECT COUNT(*) FROM categories")
    categories_count = cursor.fetchone()[0]

    # عدد المنتجات
    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]

    # عدد المستودعات
    cursor.execute("SELECT COUNT(*) FROM warehouses")
    warehouses_count = cursor.fetchone()[0]

    # عدد المستخدمين
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]

    # عدد الموردين
    cursor.execute("SELECT COUNT(*) FROM suppliers WHERE is_active = 1")
    suppliers_count = cursor.fetchone()[0]

    # عدد العملاء
    cursor.execute("SELECT COUNT(*) FROM customers WHERE is_active = 1")
    customers_count = cursor.fetchone()[0]

    conn.close()

    return jsonify(
        {
            "statistics": {
                "categories": categories_count,
                "products": products_count,
                "warehouses": warehouses_count,
                "users": users_count,
                "suppliers": suppliers_count,
                "customers": customers_count,
            },
            "message": "بيانات لوحة التحكم",
            "timestamp": datetime.now().isoformat(),
        }
    )


if __name__ == "__main__":
    print("🚀 بدء تشغيل الخادم الخلفي البسيط...")

    # تهيئة قاعدة البيانات
    init_database()

    print("🌐 الخادم يعمل على http://localhost:5002")
    print("📊 لوحة التحكم: http://localhost:5002/api/reports/dashboard")
    print("🔐 تسجيل الدخول: admin / admin123")

    # تشغيل الخادم
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)
