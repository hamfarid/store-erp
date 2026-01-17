#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 إصلاح مشكلة تسجيل الدخول
Fix Login Issue

هذا السكريبت يقوم بإصلاح مشكلة تسجيل الدخول في النظام
"""

import sqlite3
import hashlib
import requests
import json

def hash_password(password):
    """تشفير كلمة المرور باستخدام SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def fix_admin_password():
    """إصلاح كلمة مرور المستخدم الإداري"""
    print("🔧 إصلاح كلمة مرور المستخدم الإداري...")
    
    db_path = "backend/instance/inventory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # تحديث كلمة مرور المستخدم الإداري
        new_password = "admin123"
        hashed_password = hash_password(new_password)
        
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
            print(f"   كلمة المرور المشفرة: {result[1][:20]}...")
            print(f"   حالة النشاط: {'نشط' if result[2] else 'غير نشط'}")
        else:
            print("❌ لم يتم العثور على المستخدم الإداري")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح كلمة المرور: {e}")
        return False

def test_login():
    """اختبار تسجيل الدخول"""
    print("\n🧪 اختبار تسجيل الدخول...")
    
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
            return True
        else:
            print(f"❌ فشل تسجيل الدخول: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار تسجيل الدخول: {e}")
        return False

def check_auth_endpoint():
    """فحص نقطة نهاية المصادقة"""
    print("\n🔍 فحص نقطة نهاية المصادقة...")
    
    try:
        # فحص حالة الخادم
        response = requests.get('http://localhost:5002/api/status', timeout=5)
        if response.status_code == 200:
            print("✅ الخادم الخلفي يعمل بشكل طبيعي")
        else:
            print(f"⚠️ مشكلة في الخادم الخلفي: {response.status_code}")
            
        # فحص نقطة نهاية تسجيل الدخول
        response = requests.options('http://localhost:5002/api/auth/login', timeout=5)
        print(f"   نقطة نهاية تسجيل الدخول متاحة: {response.status_code}")
        
    except Exception as e:
        print(f"❌ خطأ في فحص نقطة النهاية: {e}")

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء إصلاح مشكلة تسجيل الدخول")
    print("=" * 50)
    
    # فحص نقطة النهاية
    check_auth_endpoint()
    
    # إصلاح كلمة المرور
    if fix_admin_password():
        # اختبار تسجيل الدخول
        if test_login():
            print("\n🎉 تم إصلاح مشكلة تسجيل الدخول بنجاح!")
        else:
            print("\n⚠️ لا تزال هناك مشكلة في تسجيل الدخول")
    else:
        print("\n❌ فشل في إصلاح كلمة المرور")

if __name__ == "__main__":
    main()
