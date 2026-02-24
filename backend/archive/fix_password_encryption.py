#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 إصلاح مشكلة تشفير كلمة المرور
Fix Password Encryption Issue

هذا السكريبت يقوم بإصلاح مشكلة تشفير كلمة المرور في النظام
"""

import sqlite3
import hashlib
import secrets
import requests
import json

def hash_password_pbkdf2(password):
    """تشفير كلمة المرور باستخدام PBKDF2 (نفس الطريقة المستخدمة في النظام)"""
    salt = secrets.token_hex(16)  # 32 حرف hex = 16 بايت
    password_hash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)
    return salt + password_hash.hex()

def verify_password_pbkdf2(password, stored_hash):
    """التحقق من كلمة المرور باستخدام PBKDF2"""
    try:
        salt = stored_hash[:32]
        stored_password_hash = stored_hash[32:]
        password_hash = hashlib.pbkdf2_hmac('sha256',
                                          password.encode('utf-8'),
                                          salt.encode('utf-8'),
                                          100000)
        return password_hash.hex() == stored_password_hash
    except:
        return False

def fix_admin_password_encryption():
    """إصلاح تشفير كلمة مرور المستخدم الإداري"""
    print("🔐 إصلاح تشفير كلمة مرور المستخدم الإداري...")
    
    db_path = "backend/instance/inventory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # تشفير كلمة المرور الجديدة باستخدام PBKDF2
        new_password = "admin123"
        hashed_password = hash_password_pbkdf2(new_password)
        
        print(f"   كلمة المرور الجديدة المشفرة: {hashed_password[:50]}...")
        
        # تحديث كلمة مرور المستخدم الإداري
        cursor.execute("""
            UPDATE users 
            SET password_hash = ?, is_active = 1 
            WHERE username = 'admin'
        """, (hashed_password,))
        
        conn.commit()
        
        # التحقق من التحديث
        cursor.execute("SELECT username, password_hash, is_active FROM users WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            print(f"✅ تم تحديث كلمة مرور المستخدم: {result[0]}")
            print(f"   كلمة المرور المشفرة: {result[1][:50]}...")
            print(f"   حالة النشاط: {'نشط' if result[2] else 'غير نشط'}")
            
            # اختبار التحقق من كلمة المرور
            if verify_password_pbkdf2(new_password, result[1]):
                print("✅ تم التحقق من صحة تشفير كلمة المرور")
            else:
                print("❌ فشل في التحقق من تشفير كلمة المرور")
                
        else:
            print("❌ لم يتم العثور على المستخدم الإداري")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح تشفير كلمة المرور: {e}")
        return False

def test_login_with_new_encryption():
    """اختبار تسجيل الدخول مع التشفير الجديد"""
    print("\n🧪 اختبار تسجيل الدخول مع التشفير الجديد...")
    
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post('http://localhost:5002/api/auth/login', 
                               json=login_data, timeout=10)
        
        print(f"   رمز الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ تم تسجيل الدخول بنجاح!")
            print(f"   رمز الجلسة: {data.get('session_token', 'غير متوفر')[:20]}...")
            print(f"   بيانات المستخدم: {data.get('user', {}).get('username', 'غير متوفر')}")
            return True
        else:
            print(f"❌ فشل تسجيل الدخول: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار تسجيل الدخول: {e}")
        return False

def check_user_roles_table():
    """فحص وإنشاء جدول user_roles إذا لم يكن موجوداً"""
    print("\n🔍 فحص جدول user_roles...")
    
    db_path = "backend/instance/inventory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # فحص وجود الجدول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_roles'")
        if not cursor.fetchone():
            print("⚠️ جدول user_roles غير موجود، سيتم إنشاؤه...")
            
            # إنشاء جدول user_roles
            cursor.execute('''
                CREATE TABLE user_roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (role_id) REFERENCES roles (id),
                    UNIQUE(user_id, role_id)
                )
            ''')
            
            # ربط المستخدم الإداري بدور الإدارة
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            admin_user = cursor.fetchone()
            
            cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
            admin_role = cursor.fetchone()
            
            if admin_user and admin_role:
                cursor.execute('''
                    INSERT OR IGNORE INTO user_roles (user_id, role_id)
                    VALUES (?, ?)
                ''', (admin_user[0], admin_role[0]))
                print("✅ تم ربط المستخدم الإداري بدور الإدارة")
            
            conn.commit()
            print("✅ تم إنشاء جدول user_roles بنجاح")
        else:
            print("✅ جدول user_roles موجود")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص جدول user_roles: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔐 بدء إصلاح مشكلة تشفير كلمة المرور")
    print("=" * 60)
    
    # فحص وإنشاء جدول user_roles
    check_user_roles_table()
    
    # إصلاح تشفير كلمة المرور
    if fix_admin_password_encryption():
        # اختبار تسجيل الدخول
        if test_login_with_new_encryption():
            print("\n🎉 تم إصلاح مشكلة تشفير كلمة المرور بنجاح!")
        else:
            print("\n⚠️ لا تزال هناك مشكلة في تسجيل الدخول")
    else:
        print("\n❌ فشل في إصلاح تشفير كلمة المرور")

if __name__ == "__main__":
    main()
