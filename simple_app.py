#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق خلفي بسيط للاختبار
Simple Backend App for Testing
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# إعداد قاعدة البيانات
DATABASE_PATH = 'instance/inventory.db'

def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """تهيئة قاعدة البيانات"""
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # إنشاء الجداول الأساسية
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            full_name TEXT,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE,
            address TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE,
            category_id INTEGER,
            price DECIMAL(10,2) DEFAULT 0,
            cost DECIMAL(10,2) DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    
    # إدراج بيانات تجريبية
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, email, full_name, password_hash, role)
            VALUES ('admin', 'admin@example.com', 'مدير النظام', 'admin123', 'admin')
        """)
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            ('إلكترونيات', 'أجهزة إلكترونية ومعدات'),
            ('ملابس', 'ملابس وأزياء'),
            ('طعام', 'مواد غذائية ومشروبات'),
            ('كتب', 'كتب ومواد تعليمية'),
            ('أدوات', 'أدوات ومعدات')
        ]
        cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)
    
    cursor.execute("SELECT COUNT(*) FROM warehouses")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO warehouses (name, code, address) VALUES ('المستودع الرئيسي', 'MAIN', 'الرياض')")
    
    conn.commit()
    conn.close()
    print("✅ تم تهيئة قاعدة البيانات")

# المسارات الأساسية
@app.route('/api/status', methods=['GET'])
def status():
    """حالة الخادم"""
    return jsonify({
        'success': True,
        'message': 'الخادم يعمل بشكل طبيعي',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """الحصول على الفئات"""
    try:
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM categories WHERE is_active = 1').fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'categories': [dict(cat) for cat in categories]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """إنشاء فئة جديدة"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'success': False, 'error': 'اسم الفئة مطلوب'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO categories (name, description) VALUES (?, ?)',
            (name, description)
        )
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء الفئة بنجاح',
            'category_id': category_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/warehouses', methods=['GET'])
def get_warehouses():
    """الحصول على المستودعات"""
    try:
        conn = get_db_connection()
        warehouses = conn.execute('SELECT * FROM warehouses WHERE is_active = 1').fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'warehouses': [dict(wh) for wh in warehouses]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """الحصول على المنتجات"""
    try:
        conn = get_db_connection()
        query = """
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE p.is_active = 1
        """
        products = conn.execute(query).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'products': [dict(prod) for prod in products]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND is_active = 1',
            (username,)
        ).fetchone()
        conn.close()
        
        if user and user['password_hash'] == password:
            return jsonify({
                'success': True,
                'message': 'تم تسجيل الدخول بنجاح',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role']
                },
                'token': 'test_token_123'
            })
        else:
            return jsonify({'success': False, 'error': 'بيانات تسجيل الدخول غير صحيحة'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """الحصول على المستخدمين"""
    try:
        conn = get_db_connection()
        users = conn.execute('SELECT id, username, email, full_name, role, is_active FROM users').fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'users': [dict(user) for user in users]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_database()
    print("🚀 بدء تشغيل الخادم الخلفي البسيط...")
    print("📍 الخادم متاح على: http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=True)
