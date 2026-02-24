#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 إصلاح قاعدة البيانات وإنشاء المستخدم الإداري
Fix Database and Create Admin User Script

يقوم بإصلاح مشاكل قاعدة البيانات وإنشاء المستخدم الإداري:
- إصلاح مشكلة role_id في جدول المستخدمين
- إنشاء مستخدم إداري صحيح
- إضافة البيانات الأساسية المفقودة
"""

import sqlite3
import json
from werkzeug.security import generate_password_hash
from datetime import datetime
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def fix_database_schema():
    """إصلاح مخطط قاعدة البيانات"""
    print_step("إصلاح مخطط قاعدة البيانات...")
    
    db_path = Path("backend/instance/inventory.db")
    if not db_path.exists():
        print_error("قاعدة البيانات غير موجودة")
        return False
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # التحقق من وجود جدول الأدوار
        cursor.execute("SELECT COUNT(*) FROM roles WHERE name = 'admin'")
        admin_role_count = cursor.fetchone()[0]
        
        if admin_role_count == 0:
            # إنشاء دور الإدارة
            cursor.execute("""
                INSERT INTO roles (name, description, permissions, is_active, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                'admin',
                'System Administrator - Full system access',
                json.dumps({"all": True}),
                True,
                datetime.utcnow().isoformat()
            ))
            print_success("تم إنشاء دور الإدارة")
        
        # الحصول على معرف دور الإدارة
        cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
        admin_role_id = cursor.fetchone()[0]
        
        # التحقق من وجود مستخدم إداري
        cursor.execute("SELECT COUNT(*) FROM users WHERE role_id = ?", (admin_role_id,))
        admin_user_count = cursor.fetchone()[0]
        
        if admin_user_count == 0:
            # إنشاء مستخدم إداري
            password_hash = generate_password_hash('admin123')
            
            cursor.execute("""
                INSERT INTO users (
                    username, password_hash, email, full_name, role_id, 
                    is_active, created_at, role, permissions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'admin',
                password_hash,
                'admin@store.com',
                'مدير النظام',
                admin_role_id,
                True,
                datetime.utcnow().isoformat(),
                'admin',
                json.dumps(['read_all', 'write_all', 'delete_all', 'admin_panel'])
            ))
            print_success("تم إنشاء المستخدم الإداري")
        else:
            print_success("المستخدم الإداري موجود بالفعل")
        
        # إضافة مستودع افتراضي إذا لم يكن موجوداً
        cursor.execute("SELECT COUNT(*) FROM warehouses")
        warehouse_count = cursor.fetchone()[0]
        
        if warehouse_count == 0:
            cursor.execute("""
                INSERT INTO warehouses (name, code, address, is_active, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                'المستودع الرئيسي',
                'MAIN',
                'الموقع الرئيسي',
                True,
                datetime.utcnow().isoformat()
            ))
            print_success("تم إنشاء المستودع الافتراضي")
        
        conn.commit()
        conn.close()
        
        print_success("تم إصلاح قاعدة البيانات بنجاح")
        return True
        
    except Exception as e:
        print_error(f"خطأ في إصلاح قاعدة البيانات: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def verify_database():
    """التحقق من صحة قاعدة البيانات"""
    print_step("التحقق من صحة قاعدة البيانات...")
    
    db_path = Path("backend/instance/inventory.db")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # التحقق من المستخدم الإداري
        cursor.execute("""
            SELECT u.username, u.email, r.name as role_name 
            FROM users u 
            JOIN roles r ON u.role_id = r.id 
            WHERE r.name = 'admin'
        """)
        admin_users = cursor.fetchall()
        
        if admin_users:
            print_success(f"المستخدمون الإداريون: {len(admin_users)}")
            for user in admin_users:
                print(f"   - {user[0]} ({user[1]}) - {user[2]}")
        else:
            print_error("لا يوجد مستخدمون إداريون")
        
        # التحقق من الفئات
        cursor.execute("SELECT COUNT(*) FROM categories")
        categories_count = cursor.fetchone()[0]
        print_success(f"عدد الفئات: {categories_count}")
        
        # التحقق من المستودعات
        cursor.execute("SELECT COUNT(*) FROM warehouses")
        warehouses_count = cursor.fetchone()[0]
        print_success(f"عدد المستودعات: {warehouses_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"خطأ في التحقق من قاعدة البيانات: {e}")
        return False

def main():
    print("🔧 بدء إصلاح قاعدة البيانات وإنشاء المستخدم الإداري...")
    print("=" * 60)
    
    # إصلاح قاعدة البيانات
    if fix_database_schema():
        # التحقق من النتائج
        verify_database()
        
        print("=" * 60)
        print_success("تم إصلاح قاعدة البيانات بنجاح!")
        print("📋 بيانات تسجيل الدخول:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("   البريد الإلكتروني: admin@store.com")
        
        return True
    else:
        print_error("فشل في إصلاح قاعدة البيانات")
        return False

if __name__ == "__main__":
    main()
