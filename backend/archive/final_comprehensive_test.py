#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبار شامل نهائي لنظام إدارة المتجر
Final Comprehensive System Test

يقوم بإجراء اختبار شامل لجميع أجزاء النظام:
- اختبار قاعدة البيانات والمستخدم الإداري
- اختبار الخادم الخلفي ونقاط النهاية
- اختبار نظام المصادقة
- اختبار الخادم الأمامي
- تقييم الأداء العام
"""

import requests
import sqlite3
import json
import time
from pathlib import Path
from datetime import datetime

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print('='*60)

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def test_database():
    """اختبار قاعدة البيانات"""
    print_step("اختبار قاعدة البيانات...")
    
    db_path = Path("backend/instance/inventory.db")
    if not db_path.exists():
        print_error("قاعدة البيانات غير موجودة")
        return False, {}
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        results = {}
        
        # فحص الجداول الأساسية
        required_tables = ['users', 'categories', 'warehouses', 'products', 'roles']
        for table in required_tables:
            cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone()[0] > 0:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                results[f"{table}_count"] = count
                print_success(f"جدول {table}: {count} سجل")
            else:
                print_error(f"جدول {table} غير موجود")
                results[f"{table}_count"] = 0
        
        # فحص المستخدم الإداري
        cursor.execute("""
            SELECT u.username, u.email, r.name as role_name 
            FROM users u 
            JOIN roles r ON u.role_id = r.id 
            WHERE r.name = 'admin'
        """)
        admin_users = cursor.fetchall()
        
        if admin_users:
            results['admin_user'] = True
            print_success(f"المستخدم الإداري موجود: {admin_users[0][0]}")
        else:
            results['admin_user'] = False
            print_error("المستخدم الإداري غير موجود")
        
        conn.close()
        return True, results
        
    except Exception as e:
        print_error(f"خطأ في اختبار قاعدة البيانات: {e}")
        return False, {}

def test_backend_server():
    """اختبار الخادم الخلفي"""
    print_step("اختبار الخادم الخلفي...")
    
    base_url = "http://localhost:5002"
    results = {}
    
    try:
        # اختبار الاتصال الأساسي
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print_success("الخادم الخلفي يعمل")
            results['server_running'] = True
        else:
            print_error(f"الخادم الخلفي لا يستجيب: {response.status_code}")
            results['server_running'] = False
            return False, results
            
    except requests.exceptions.RequestException as e:
        print_error(f"لا يمكن الاتصال بالخادم الخلفي: {e}")
        results['server_running'] = False
        return False, results
    
    # اختبار نقاط النهاية الأساسية
    endpoints = [
        '/api/categories',
        '/api/warehouses', 
        '/api/users',
        '/api/products',
        '/api/auth/login'
    ]
    
    working_endpoints = []
    failed_endpoints = []
    
    for endpoint in endpoints:
        try:
            if endpoint == '/api/auth/login':
                # اختبار POST للمصادقة
                response = requests.post(f"{base_url}{endpoint}", 
                                       json={"username": "test", "password": "test"}, 
                                       timeout=5)
            else:
                # اختبار GET للنقاط الأخرى
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code in [200, 400, 401]:  # 400/401 مقبولة للمصادقة
                working_endpoints.append(endpoint)
                print_success(f"نقطة النهاية {endpoint} تعمل ({response.status_code})")
            else:
                failed_endpoints.append(f"{endpoint} ({response.status_code})")
                print_warning(f"نقطة النهاية {endpoint} لا تعمل: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            failed_endpoints.append(f"{endpoint} (خطأ اتصال)")
            print_error(f"خطأ في اختبار {endpoint}: {e}")
    
    results['working_endpoints'] = working_endpoints
    results['failed_endpoints'] = failed_endpoints
    results['endpoints_score'] = len(working_endpoints) / len(endpoints) * 100
    
    return True, results

def test_authentication():
    """اختبار نظام المصادقة"""
    print_step("اختبار نظام المصادقة...")
    
    base_url = "http://localhost:5002"
    results = {}
    
    try:
        # محاولة تسجيل الدخول بالمستخدم الإداري
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{base_url}/api/auth/login", 
                               json=login_data, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success("تسجيل الدخول نجح")
                results['login_success'] = True
                results['auth_token'] = data.get('token', 'development_mode')
                return True, results
            else:
                print_error(f"فشل تسجيل الدخول: {data.get('message', 'خطأ غير معروف')}")
                results['login_success'] = False
        else:
            print_error(f"خطأ في تسجيل الدخول: {response.status_code}")
            results['login_success'] = False
            
    except requests.exceptions.RequestException as e:
        print_error(f"خطأ في اختبار المصادقة: {e}")
        results['login_success'] = False
    
    return False, results

def test_frontend():
    """اختبار الخادم الأمامي"""
    print_step("اختبار الخادم الأمامي...")
    
    frontend_url = "http://localhost:5502"
    results = {}
    
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print_success("الخادم الأمامي يعمل")
            results['frontend_running'] = True
            
            # فحص المحتوى الأساسي
            content = response.text.lower()
            if 'inventory' in content or 'مخزون' in content:
                print_success("المحتوى الأساسي موجود")
                results['content_valid'] = True
            else:
                print_warning("المحتوى قد يكون غير مكتمل")
                results['content_valid'] = False
                
            return True, results
        else:
            print_error(f"الخادم الأمامي لا يستجيب: {response.status_code}")
            results['frontend_running'] = False
            
    except requests.exceptions.RequestException as e:
        print_error(f"لا يمكن الاتصال بالخادم الأمامي: {e}")
        results['frontend_running'] = False
    
    return False, results

def calculate_overall_score(test_results):
    """حساب النتيجة الإجمالية"""
    total_score = 0
    max_score = 0
    
    # نقاط قاعدة البيانات (30 نقطة)
    db_results = test_results.get('database', {})
    if db_results.get('admin_user'):
        total_score += 15
    if db_results.get('users_count', 0) > 0:
        total_score += 5
    if db_results.get('categories_count', 0) > 0:
        total_score += 5
    if db_results.get('warehouses_count', 0) > 0:
        total_score += 5
    max_score += 30
    
    # نقاط الخادم الخلفي (40 نقطة)
    backend_results = test_results.get('backend', {})
    if backend_results.get('server_running'):
        total_score += 20
    endpoints_score = backend_results.get('endpoints_score', 0)
    total_score += (endpoints_score / 100) * 20
    max_score += 40
    
    # نقاط المصادقة (20 نقطة)
    auth_results = test_results.get('authentication', {})
    if auth_results.get('login_success'):
        total_score += 20
    max_score += 20
    
    # نقاط الخادم الأمامي (10 نقاط)
    frontend_results = test_results.get('frontend', {})
    if frontend_results.get('frontend_running'):
        total_score += 7
    if frontend_results.get('content_valid'):
        total_score += 3
    max_score += 10
    
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    return percentage, total_score, max_score

def get_status_description(score):
    """وصف حالة النظام بناءً على النتيجة"""
    if score >= 95:
        return "ممتاز", "🟢"
    elif score >= 85:
        return "جيد جداً", "🟡"
    elif score >= 70:
        return "جيد", "🟠"
    elif score >= 50:
        return "مقبول", "🔴"
    else:
        return "ضعيف", "⚫"

def main():
    print_header("اختبار شامل نهائي لنظام إدارة المتجر")
    
    test_results = {}
    
    # اختبار قاعدة البيانات
    print_header("اختبار قاعدة البيانات")
    db_success, db_results = test_database()
    test_results['database'] = db_results
    
    # اختبار الخادم الخلفي
    print_header("اختبار الخادم الخلفي")
    backend_success, backend_results = test_backend_server()
    test_results['backend'] = backend_results
    
    # اختبار المصادقة
    print_header("اختبار نظام المصادقة")
    auth_success, auth_results = test_authentication()
    test_results['authentication'] = auth_results
    
    # اختبار الخادم الأمامي
    print_header("اختبار الخادم الأمامي")
    frontend_success, frontend_results = test_frontend()
    test_results['frontend'] = frontend_results
    
    # حساب النتيجة الإجمالية
    print_header("النتائج النهائية")
    
    overall_score, total_score, max_score = calculate_overall_score(test_results)
    status_desc, status_icon = get_status_description(overall_score)
    
    print(f"📊 النتيجة الإجمالية: {overall_score:.1f}/100 ({total_score}/{max_score})")
    print(f"{status_icon} حالة النظام: {status_desc}")
    
    # تفاصيل النتائج
    print(f"\n📋 تفاصيل النتائج:")
    print(f"   - قاعدة البيانات: {'✅' if db_success else '❌'}")
    print(f"   - الخادم الخلفي: {'✅' if backend_success else '❌'}")
    print(f"   - نظام المصادقة: {'✅' if auth_success else '❌'}")
    print(f"   - الخادم الأمامي: {'✅' if frontend_success else '❌'}")
    
    # حفظ التقرير
    report = {
        'timestamp': datetime.now().isoformat(),
        'overall_score': overall_score,
        'status': status_desc,
        'test_results': test_results,
        'summary': {
            'database': db_success,
            'backend': backend_success,
            'authentication': auth_success,
            'frontend': frontend_success
        }
    }
    
    with open('final_test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم حفظ التقرير في final_test_report.json")
    
    # التوصيات
    if overall_score < 100:
        print(f"\n📋 التوصيات للتحسين:")
        if not db_success:
            print("   - إصلاح مشاكل قاعدة البيانات")
        if not backend_success:
            print("   - إصلاح الخادم الخلفي ونقاط النهاية")
        if not auth_success:
            print("   - إصلاح نظام المصادقة")
        if not frontend_success:
            print("   - إصلاح الخادم الأمامي")
    
    return overall_score >= 95

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
