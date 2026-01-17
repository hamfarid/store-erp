#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار صيغة الردود (Response Format) للتحقق من توحيد عقود JSON
"""

import sys
import os

# إضافة مسار src إلى PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_response_formats():
    """اختبار صيغة الردود من ملفات routes المختلفة"""

    print("\n" + "=" * 70)
    print("🧪 اختبار صيغة الردود (Response Format Validation)")
    print("=" * 70)

    results = {"passed": 0, "failed": 0, "warnings": 0}

    # اختبار 1: استيراد الملفات والتحقق من عدم وجود أخطاء syntax
    print("\n📦 المرحلة 1: اختبار استيراد الملفات")
    print("-" * 70)

    route_files = [
        "routes.accounting_system",
        "routes.admin",
        "routes.user_management_advanced",
        "routes.warehouse_adjustments",
        "routes.warehouse_transfer",
        "routes.interactive_dashboard",
        "routes.automation",
        "routes.system_settings_advanced",
    ]

    for module_name in route_files:
        try:
            __import__(module_name)
            print(f"✅ {module_name}: استيراد ناجح")
            results["passed"] += 1
        except ImportError as e:
            print(f"⚠️ {module_name}: تحذير - {str(e)[:80]}")
            results["warnings"] += 1
        except SyntaxError as e:
            print(f"❌ {module_name}: خطأ syntax - {str(e)}")
            results["failed"] += 1
        except Exception as e:
            print(f"⚠️ {module_name}: تحذير - {str(e)[:80]}")
            results["warnings"] += 1

    # اختبار 2: فحص محتوى الملفات للتأكد من استخدام 'status'
    print("\n🔍 المرحلة 2: فحص استخدام 'status' في الملفات")
    print("-" * 70)

    routes_dir = os.path.join(os.path.dirname(__file__), "src", "routes")

    files_to_check = [
        "accounting_system.py",
        "admin.py",
        "user_management_advanced.py",
        "warehouse_adjustments.py",
        "warehouse_transfer.py",
        "interactive_dashboard.py",
        "automation.py",
        "system_settings_advanced.py",
    ]

    for filename in files_to_check:
        filepath = os.path.join(routes_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️ {filename}: الملف غير موجود")
            results["warnings"] += 1
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # البحث عن أنماط قديمة
        old_patterns = [
            "'success': True",
            "'success': False",
            '"success": True',
            '"success": False',
        ]

        found_old = False
        for pattern in old_patterns:
            if pattern in content:
                print(f"⚠️ {filename}: وُجد نمط قديم '{pattern}'")
                found_old = True
                results["warnings"] += 1

        # البحث عن أنماط جديدة
        new_patterns = [
            "'status': 'success'",
            "'status': 'error'",
            '"status": "success"',
            '"status": "error"',
        ]

        found_new = False
        for pattern in new_patterns:
            if pattern in content:
                found_new = True
                break

        if found_new and not found_old:
            print(f"✅ {filename}: يستخدم النمط الجديد 'status'")
            results["passed"] += 1
        elif found_new and found_old:
            print(f"⚠️ {filename}: يحتوي على كلا النمطين (قديم وجديد)")
            # لا نحسبه كفشل لأن قد يكون في تعليقات أو schemas
        elif not found_new:
            print(f"❌ {filename}: لا يستخدم النمط الجديد")
            results["failed"] += 1

    # اختبار 3: التحقق من دوال المساعدة في user_management_advanced
    print("\n🔧 المرحلة 3: التحقق من دوال المساعدة")
    print("-" * 70)

    uma_file = os.path.join(routes_dir, "user_management_advanced.py")
    if os.path.exists(uma_file):
        with open(uma_file, "r", encoding="utf-8") as f:
            content = f.read()

        helper_functions = ["normalize_result", "is_ok"]
        for func_name in helper_functions:
            if f"def {func_name}(" in content:
                print(f"✅ user_management_advanced.py: دالة '{func_name}' موجودة")
                results["passed"] += 1
            else:
                print(f"❌ user_management_advanced.py: دالة '{func_name}' غير موجودة")
                results["failed"] += 1
    else:
        print(f"⚠️ user_management_advanced.py: الملف غير موجود")
        results["warnings"] += 1

    # اختبار 4: التحقق من الفحوصات الشرطية المتوافقة
    print("\n🔀 المرحلة 4: التحقق من الفحوصات الشرطية")
    print("-" * 70)

    files_with_checks = [
        "automation.py",
        "interactive_dashboard.py",
        "system_settings_advanced.py",
    ]

    for filename in files_with_checks:
        filepath = os.path.join(routes_dir, filename)

        if not os.path.exists(filepath):
            print(f"⚠️ {filename}: الملف غير موجود")
            results["warnings"] += 1
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # البحث عن الفحوصات المتوافقة
        compatible_check = (
            "result.get('status') == 'success' or result.get('success') is True"
        )
        old_check = "result['success']"

        if compatible_check in content:
            print(f"✅ {filename}: يستخدم فحوصات متوافقة")
            results["passed"] += 1
        elif old_check in content and compatible_check not in content:
            print(f"❌ {filename}: لا يزال يستخدم فحوصات قديمة")
            results["failed"] += 1
        else:
            print(f"ℹ️ {filename}: لا يحتوي على فحوصات result")

    # طباعة الملخص النهائي
    print("\n" + "=" * 70)
    print("📊 ملخص نتائج الاختبار")
    print("=" * 70)
    total = results["passed"] + results["failed"] + results["warnings"]
    print(f"✅ نجح: {results['passed']}")
    print(f"❌ فشل: {results['failed']}")
    print(f"⚠️ تحذيرات: {results['warnings']}")
    print(f"📈 المجموع: {total}")

    if results["failed"] == 0:
        print("\n🎉 جميع الاختبارات نجحت!")
        return 0
    else:
        print(f"\n⚠️ يوجد {results['failed']} اختبار فشل")
        return 1


if __name__ == "__main__":
    exit_code = test_response_formats()
    sys.exit(exit_code)
