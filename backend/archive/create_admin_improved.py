#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت محسن لإنشاء المستخدم الإداري
Improved Admin User Creation Script
"""

import os
import sqlite3
import hashlib
from datetime import datetime

def create_admin_user():
    """إنشاء مستخدم إداري محسن"""
    
    # مسار قاعدة البيانات
    db_path = "backend/instance/inventory.db"
    
    # التأكد من وجود مجلد instance
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 فحص المستخدم الإداري الحالي...")
        
        # فحص المستخدم الإداري الحالي
        cursor.execute("SELECT username, email, role, created_at FROM users WHERE username = ?", ('admin',))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print(f"✅ المستخدم الإداري موجود بالفعل:")
            print(f"   اسم المستخدم: {existing_admin[0]}")
            print(f"   البريد الإلكتروني: {existing_admin[1]}")
            print(f"   الدور: {existing_admin[2]}")
            print(f"   تاريخ الإنشاء: {existing_admin[3]}")
            
            # اختبار كلمة المرور
            cursor.execute("SELECT password FROM users WHERE username = ?", ('admin',))
            stored_password = cursor.fetchone()[0]
            
            # فحص كلمة المرور (النظام الحالي يستخدم نص عادي)
            if stored_password == 'admin123':
                print("✅ كلمة المرور صحيحة: admin123")
            else:
                print("⚠️  كلمة المرور غير صحيحة، سيتم تحديثها...")
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", ('admin123', 'admin'))
                conn.commit()
                print("✅ تم تحديث كلمة المرور إلى: admin123")
        
        else:
            print("🆕 إنشاء مستخدم إداري جديد...")
            
            # إنشاء مستخدم إداري جديد
            cursor.execute('''
                INSERT INTO users (username, password, email, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', 'admin123', 'admin@store.com', 'admin', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
            print("✅ تم إنشاء المستخدم الإداري بنجاح!")
            print("   اسم المستخدم: admin")
            print("   كلمة المرور: admin123")
            print("   البريد الإلكتروني: admin@store.com")
        
        # فحص جميع المستخدمين
        print("\n📋 قائمة جميع المستخدمين:")
        cursor.execute("SELECT id, username, email, role, created_at FROM users")
        users = cursor.fetchall()
        
        for user in users:
            print(f"   ID: {user[0]} | المستخدم: {user[1]} | البريد: {user[2]} | الدور: {user[3]} | التاريخ: {user[4]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء المستخدم الإداري: {e}")
        return False

def test_admin_login():
    """اختبار تسجيل دخول المستخدم الإداري"""
    
    print("\n🧪 اختبار تسجيل الدخول...")
    
    import subprocess
    import json
    
    try:
        # اختبار تسجيل الدخول عبر API
        cmd = [
            'curl', '-s', '-X', 'POST', 
            'http://localhost:5002/api/auth/login',
            '-H', 'Content-Type: application/json',
            '-d', '{"username": "admin", "password": "admin123"}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if response.get('success'):
                    print("✅ تسجيل الدخول نجح!")
                    print(f"   الرسالة: {response.get('message', 'غير متوفر')}")
                    print(f"   معرف الجلسة: {response.get('session_token', 'غير متوفر')}")
                    user_info = response.get('user', {})
                    print(f"   معلومات المستخدم: {user_info.get('username')} ({user_info.get('role')})")
                else:
                    print(f"❌ فشل تسجيل الدخول: {response.get('error', 'خطأ غير معروف')}")
            except json.JSONDecodeError:
                print(f"❌ استجابة غير صالحة من الخادم: {result.stdout}")
        else:
            print(f"❌ خطأ في الاتصال بالخادم: {result.stderr}")
    
    except Exception as e:
        print(f"❌ خطأ في اختبار تسجيل الدخول: {e}")

def check_server_status():
    """فحص حالة الخادم"""
    
    print("\n🌐 فحص حالة الخادم...")
    
    import subprocess
    
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:5002/api/status'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ الخادم يعمل بشكل طبيعي")
            print(f"   الاستجابة: {result.stdout[:100]}...")
        else:
            print("❌ الخادم لا يستجيب")
            print("   تأكد من تشغيل الخادم الخلفي على المنفذ 5002")
    
    except Exception as e:
        print(f"❌ خطأ في فحص الخادم: {e}")

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🔧 سكريبت إنشاء المستخدم الإداري المحسن")
    print("=" * 60)
    
    # إنشاء المستخدم الإداري
    if create_admin_user():
        print("\n" + "=" * 60)
        print("✅ تم إنشاء/تحديث المستخدم الإداري بنجاح!")
        print("=" * 60)
        
        # فحص حالة الخادم
        check_server_status()
        
        # اختبار تسجيل الدخول
        test_admin_login()
        
        print("\n" + "=" * 60)
        print("📝 معلومات تسجيل الدخول:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")
        print("   رابط الواجهة الأمامية: http://localhost:5502")
        print("   رابط الخادم الخلفي: http://localhost:5002")
        print("=" * 60)
    
    else:
        print("\n❌ فشل في إنشاء المستخدم الإداري")

if __name__ == "__main__":
    main()
