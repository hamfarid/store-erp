#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لجميع APIs
Comprehensive API Testing

اختبار جميع نقاط النهاية في التطبيق
"""

import sys
import os
import json

# إضافة المسار الحالي إلى sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_all_apis():
    """اختبار شامل لجميع APIs"""

    print("=" * 80)
    print("🧪 اختبار شامل لجميع APIs")
    print("=" * 80)
    print()

    try:
        # استيراد التطبيق
        from app import app

        # إنشاء عميل اختبار
        client = app.test_client()

        # عداد الاختبارات
        total_tests = 0
        passed_tests = 0
        failed_tests = 0

        # ===== اختبار مسارات الحالة =====
        print("=" * 80)
        print("📋 اختبار مسارات الحالة (Status Routes)")
        print("=" * 80)
        print()

        # اختبار /api/status
        total_tests += 1
        try:
            response = client.get("/api/status")
            if response.status_code == 200:
                print(f"{total_tests}. ✅ GET /api/status - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ GET /api/status - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ GET /api/status - خطأ: {e}")
            failed_tests += 1

        # اختبار /api/health
        total_tests += 1
        try:
            response = client.get("/api/health")
            if response.status_code == 200:
                print(f"{total_tests}. ✅ GET /api/health - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ GET /api/health - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ GET /api/health - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار مسارات المصادقة =====
        print("=" * 80)
        print("📋 اختبار مسارات المصادقة (Auth Routes)")
        print("=" * 80)
        print()

        # اختبار تسجيل الدخول (بدون بيانات)
        total_tests += 1
        try:
            response = client.post(
                "/api/auth/login", json={}, content_type="application/json"
            )
            # يجب أن يفشل بسبب عدم وجود بيانات
            if response.status_code in [400, 401]:
                print(f"{total_tests}. ✅ POST /api/auth/login (بدون بيانات) - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ POST /api/auth/login - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ POST /api/auth/login - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار مسارات المنتجات =====
        print("=" * 80)
        print("📋 اختبار مسارات المنتجات (Products Routes)")
        print("=" * 80)
        print()

        # اختبار GET /api/products (بدون token)
        total_tests += 1
        try:
            response = client.get("/api/products")
            # يجب أن يفشل بسبب عدم وجود token
            if response.status_code in [401, 403]:
                print(f"{total_tests}. ✅ GET /api/products (بدون token) - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ GET /api/products - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ GET /api/products - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار مسارات العملاء =====
        print("=" * 80)
        print("📋 اختبار مسارات العملاء (Customers Routes)")
        print("=" * 80)
        print()

        # اختبار GET /api/customers (بدون token)
        total_tests += 1
        try:
            response = client.get("/api/customers")
            # يجب أن يفشل بسبب عدم وجود token
            if response.status_code in [401, 403]:
                print(f"{total_tests}. ✅ GET /api/customers (بدون token) - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ GET /api/customers - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ GET /api/customers - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار مسارات الموردين =====
        print("=" * 80)
        print("📋 اختبار مسارات الموردين (Suppliers Routes)")
        print("=" * 80)
        print()

        # اختبار GET /api/suppliers (بدون token)
        total_tests += 1
        try:
            response = client.get("/api/suppliers")
            # يجب أن يفشل بسبب عدم وجود token
            if response.status_code in [401, 403]:
                print(f"{total_tests}. ✅ GET /api/suppliers (بدون token) - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ GET /api/suppliers - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ GET /api/suppliers - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار مسارات الفواتير =====
        print("=" * 80)
        print("📋 اختبار مسارات الفواتير (Invoices Routes)")
        print("=" * 80)
        print()

        # اختبار GET /api/invoices (بدون token)
        total_tests += 1
        try:
            response = client.get("/api/invoices")
            # يجب أن يفشل بسبب عدم وجود token
            if response.status_code in [401, 403]:
                print(f"{total_tests}. ✅ GET /api/invoices (بدون token) - نجح")
                passed_tests += 1
            else:
                print(
                    f"{total_tests}. ❌ GET /api/invoices - فشل (Status: {response.status_code})"
                )
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ GET /api/invoices - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار معالجة الأخطاء =====
        print("=" * 80)
        print("📋 اختبار معالجة الأخطاء (Error Handling)")
        print("=" * 80)
        print()

        # اختبار 404
        total_tests += 1
        try:
            response = client.get("/api/nonexistent")
            data = response.get_json()
            if response.status_code == 404 and data.get("success") == False:
                print(f"{total_tests}. ✅ 404 Not Found - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ 404 Not Found - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ 404 Not Found - خطأ: {e}")
            failed_tests += 1

        # اختبار 405
        total_tests += 1
        try:
            response = client.post("/api/status")
            data = response.get_json()
            if response.status_code == 405 and data.get("success") == False:
                print(f"{total_tests}. ✅ 405 Method Not Allowed - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ 405 Method Not Allowed - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ 405 Method Not Allowed - خطأ: {e}")
            failed_tests += 1

        print()

        # ===== اختبار الأنظمة المساعدة =====
        print("=" * 80)
        print("📋 اختبار الأنظمة المساعدة (Helper Systems)")
        print("=" * 80)
        print()

        # اختبار نظام معالجة الأخطاء
        total_tests += 1
        try:
            from src.utils.error_handlers import APIError, ValidationError

            print(f"{total_tests}. ✅ نظام معالجة الأخطاء - متاح")
            passed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ نظام معالجة الأخطاء - خطأ: {e}")
            failed_tests += 1

        # اختبار نظام التحقق
        total_tests += 1
        try:
            from src.utils.validators import validate_email, validate_phone

            print(f"{total_tests}. ✅ نظام التحقق - متاح")
            passed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ نظام التحقق - خطأ: {e}")
            failed_tests += 1

        # اختبار نظام Logging
        total_tests += 1
        try:
            from src.utils.logging_config import setup_logging, log_user_activity

            print(f"{total_tests}. ✅ نظام Logging - متاح")
            passed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ نظام Logging - خطأ: {e}")
            failed_tests += 1

        print()
        print("=" * 80)
        print("📊 النتائج النهائية")
        print("=" * 80)
        print(f"✅ نجح: {passed_tests}/{total_tests}")
        print(f"❌ فشل: {failed_tests}/{total_tests}")
        print(f"📈 نسبة النجاح: {(passed_tests/total_tests*100):.1f}%")
        print("=" * 80)

        return passed_tests == total_tests

    except ImportError as e:
        print(f"❌ خطأ في استيراد التطبيق: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_all_apis()
    sys.exit(0 if success else 1)
