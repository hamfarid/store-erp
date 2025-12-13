#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار سريع لنقاط النهاية (endpoints) للتحقق من توحيد عقود JSON
"""

import requests
import json
from typing import Dict, Any

# إعدادات الاتصال
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}


def print_result(
    endpoint: str, response: requests.Response, expected_key: str = "status"
):
    """طباعة نتيجة الاختبار"""
    print(f"\n{'='*60}")
    print(f"🔍 اختبار: {endpoint}")
    print(f"{'='*60}")
    print(f"📊 كود الحالة: {response.status_code}")

    try:
        data = response.json()
        print(f"📦 البيانات المستلمة:")
        print(json.dumps(data, ensure_ascii=False, indent=2))

        # التحقق من وجود المفتاح المتوقع
        if expected_key in data:
            print(f"✅ المفتاح '{expected_key}' موجود")
            if expected_key == "status":
                status_value = data.get("status")
                if status_value in ["success", "error"]:
                    print(f"✅ قيمة status صحيحة: {status_value}")
                else:
                    print(f"⚠️ قيمة status غير متوقعة: {status_value}")
        else:
            print(f"❌ المفتاح '{expected_key}' غير موجود!")
            if "success" in data:
                print(f"⚠️ تحذير: لا يزال يستخدم 'success' بدلاً من 'status'")
    except Exception as e:
        print(f"❌ خطأ في تحليل JSON: {str(e)}")
        print(f"📄 النص الخام: {response.text[:200]}")


def test_endpoints():
    """اختبار مجموعة من نقاط النهاية"""

    print("\n" + "=" * 60)
    print("🚀 بدء اختبار نقاط النهاية (Endpoints)")
    print("=" * 60)

    # قائمة نقاط النهاية للاختبار
    tests = [
        # 1. اختبار الحسابات (accounting)
        {
            "name": "الحصول على العملات",
            "method": "GET",
            "endpoint": "/api/accounting/currencies",
            "data": None,
        },
        # 2. اختبار الخزائن (cash boxes)
        {
            "name": "الحصول على الخزائن",
            "method": "GET",
            "endpoint": "/api/accounting/cash-boxes",
            "data": None,
        },
        # 3. اختبار المستخدمين (admin)
        {
            "name": "الحصول على المستخدمين",
            "method": "GET",
            "endpoint": "/api/admin/users",
            "data": None,
        },
        # 4. اختبار الأدوار (roles)
        {
            "name": "الحصول على الأدوار",
            "method": "GET",
            "endpoint": "/api/admin/roles",
            "data": None,
        },
        # 5. اختبار تعديلات المخازن
        {
            "name": "الحصول على تعديلات المخازن",
            "method": "GET",
            "endpoint": "/api/warehouse-adjustments",
            "data": None,
        },
        # 6. اختبار ملخص التعديلات
        {
            "name": "ملخص تعديلات المخازن",
            "method": "GET",
            "endpoint": "/api/warehouse-adjustments/summary",
            "data": None,
        },
        # 7. اختبار التحويلات بين المخازن
        {
            "name": "الحصول على التحويلات",
            "method": "GET",
            "endpoint": "/api/warehouse-transfers",
            "data": None,
        },
        # 8. اختبار إحصائيات التحويلات
        {
            "name": "إحصائيات التحويلات",
            "method": "GET",
            "endpoint": "/api/warehouse-transfers/stats",
            "data": None,
        },
    ]

    results = {"passed": 0, "failed": 0, "total": len(tests)}

    for test in tests:
        try:
            url = BASE_URL + test["endpoint"]

            if test["method"] == "GET":
                response = requests.get(url, headers=HEADERS, timeout=5)
            elif test["method"] == "POST":
                response = requests.post(
                    url, headers=HEADERS, json=test["data"], timeout=5
                )
            else:
                print(f"⚠️ طريقة غير مدعومة: {test['method']}")
                continue

            print_result(test["name"], response)

            # التحقق من النجاح
            if response.status_code < 500:
                try:
                    data = response.json()
                    if "status" in data:
                        results["passed"] += 1
                    else:
                        results["failed"] += 1
                except:
                    results["failed"] += 1
            else:
                results["failed"] += 1

        except requests.exceptions.ConnectionError:
            print(f"\n❌ فشل الاتصال بـ {test['name']}")
            print(f"⚠️ تأكد من تشغيل الخادم على {BASE_URL}")
            results["failed"] += 1
        except Exception as e:
            print(f"\n❌ خطأ في اختبار {test['name']}: {str(e)}")
            results["failed"] += 1

    # طباعة الملخص النهائي
    print("\n" + "=" * 60)
    print("📊 ملخص نتائج الاختبار")
    print("=" * 60)
    print(f"✅ نجح: {results['passed']}/{results['total']}")
    print(f"❌ فشل: {results['failed']}/{results['total']}")
    print(f"📈 نسبة النجاح: {(results['passed']/results['total']*100):.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    test_endpoints()
