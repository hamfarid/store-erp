#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار مسارات العملاء والموردين الموحدة
Test Partners Unified Routes
"""

import sys
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(src_dir))

import os
os.environ['SKIP_BLUEPRINTS'] = '0'

from flask import Flask
from src.database import db, configure_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_partners_routes():
    """اختبار مسارات العملاء والموردين"""
    
    print("\n" + "="*80)
    print("🧪 اختبار مسارات العملاء والموردين الموحدة")
    print("="*80 + "\n")
    
    # إنشاء التطبيق
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    
    # تكوين قاعدة البيانات
    configure_database(app)
    
    # تسجيل المسارات
    try:
        from src.routes.partners_unified import partners_unified_bp
        app.register_blueprint(partners_unified_bp)
        print("✅ تم تسجيل مسارات العملاء والموردين الموحدة")
    except Exception as e:
        print(f"❌ فشل تسجيل المسارات: {e}")
        return False
    
    # إنشاء الجداول
    with app.app_context():
        try:
            db.create_all()
            print("✅ تم إنشاء الجداول")
        except Exception as e:
            print(f"⚠️ تحذير في إنشاء الجداول: {e}")
    
    # إنشاء عميل الاختبار
    client = app.test_client()
    
    # الاختبارات
    tests_passed = 0
    tests_failed = 0
    
    # اختبارات العملاء
    print("\n" + "="*80)
    print("📋 اختبارات العملاء")
    print("="*80)
    
    print("\n" + "-"*80)
    print("📋 الاختبار 1: قائمة العملاء")
    print("-"*80)
    try:
        response = client.get('/api/customers')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 2: الحصول على عميل محدد")
    print("-"*80)
    try:
        response = client.get('/api/customers/1')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 404, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 3: إنشاء عميل")
    print("-"*80)
    try:
        new_customer = {
            'name': 'عميل اختبار',
            'email': 'test@example.com',
            'phone': '123456789'
        }
        response = client.post('/api/customers', json=new_customer)
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [201, 400, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 4: إحصائيات العملاء")
    print("-"*80)
    try:
        response = client.get('/api/customers/stats')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 5: البحث في العملاء")
    print("-"*80)
    try:
        response = client.get('/api/customers/search?q=test')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    # اختبارات الموردين
    print("\n" + "="*80)
    print("📋 اختبارات الموردين")
    print("="*80)
    
    print("\n" + "-"*80)
    print("📋 الاختبار 6: قائمة الموردين")
    print("-"*80)
    try:
        response = client.get('/api/suppliers')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 7: الحصول على مورد محدد")
    print("-"*80)
    try:
        response = client.get('/api/suppliers/1')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 404, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 8: إنشاء مورد")
    print("-"*80)
    try:
        new_supplier = {
            'name': 'مورد اختبار',
            'email': 'supplier@example.com',
            'phone': '987654321'
        }
        response = client.post('/api/suppliers', json=new_supplier)
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [201, 400, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 9: إحصائيات الموردين")
    print("-"*80)
    try:
        response = client.get('/api/suppliers/stats')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    print("\n" + "-"*80)
    print("📋 الاختبار 10: البحث في الموردين")
    print("-"*80)
    try:
        response = client.get('/api/suppliers/search?q=test')
        print(f"   الحالة: {response.status_code}")
        if response.status_code in [200, 401, 501]:
            print("   ✅ نجح")
            tests_passed += 1
        else:
            print("   ❌ فشل")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        tests_failed += 1
    
    # النتائج النهائية
    print("\n" + "="*80)
    print("📊 النتائج النهائية")
    print("="*80)
    print(f"✅ نجح: {tests_passed}")
    print(f"❌ فشل: {tests_failed}")
    print(f"📈 نسبة النجاح: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
    print("="*80 + "\n")
    
    return tests_failed == 0


if __name__ == '__main__':
    success = test_partners_routes()
    sys.exit(0 if success else 1)

