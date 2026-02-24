#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام معالجة الأخطاء
Test Error Handling System
"""

import os
import sys

# إضافة المسار الحالي إلى sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_error_handlers():
    """اختبار نظام معالجة الأخطاء"""

    print("=" * 80)
    print("🧪 اختبار نظام معالجة الأخطاء")
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

        print("=" * 80)
        print("📋 اختبار معالجات الأخطاء (8 اختبارات)")
        print("=" * 80)
        print()

        # ===== اختبار 1: 404 Not Found =====
        total_tests += 1
        try:
            response = client.get("/api/nonexistent-route")
            data = response.get_json()

            if response.status_code == 404 and data.get("success") == False:
                print(f"{total_tests}. ✅ اختبار 404 Not Found - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ اختبار 404 Not Found - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ اختبار 404 Not Found - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 2: 405 Method Not Allowed =====
        total_tests += 1
        try:
            response = client.post("/api/health")  # GET-only endpoint; expect 405
            data = response.get_json()

            if response.status_code == 405 and data.get("success") == False:
                print(f"{total_tests}. ✅ اختبار 405 Method Not Allowed - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ اختبار 405 Method Not Allowed - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ اختبار 405 Method Not Allowed - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 3: استيراد نظام معالجة الأخطاء =====
        total_tests += 1
        try:
            from src.utils.error_handlers import (
                APIError,
                ConflictError,
                DatabaseError,
                ForbiddenError,
                NotFoundError,
                UnauthorizedError,
                ValidationError,
                error_response,
                success_response,
            )

            print(f"{total_tests}. ✅ استيراد نظام معالجة الأخطاء - نجح")
            passed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ استيراد نظام معالجة الأخطاء - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 4: استيراد نظام التحقق =====
        total_tests += 1
        try:
            from src.utils.validators import (
                validate_date,
                validate_email,
                validate_json_schema,
                validate_number,
                validate_phone,
                validate_required_fields,
            )

            print(f"{total_tests}. ✅ استيراد نظام التحقق - نجح")
            passed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ استيراد نظام التحقق - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 5: استيراد نظام Logging =====
        total_tests += 1
        try:
            from src.utils.logging_config import (
                get_logger,
                log_request,
                log_security_event,
                log_user_activity,
                setup_logging,
            )

            print(f"{total_tests}. ✅ استيراد نظام Logging - نجح")
            passed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ استيراد نظام Logging - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 6: التحقق من البريد الإلكتروني =====
        total_tests += 1
        try:
            from src.utils.validators import validate_email

            valid_emails = ["test@example.com", "user.name@domain.co.uk"]
            invalid_emails = ["invalid", "test@", "@domain.com", "test@domain"]

            all_valid = all(validate_email(email) for email in valid_emails)
            all_invalid = all(not validate_email(email) for email in invalid_emails)

            if all_valid and all_invalid:
                print(f"{total_tests}. ✅ التحقق من البريد الإلكتروني - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ التحقق من البريد الإلكتروني - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ التحقق من البريد الإلكتروني - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 7: التحقق من رقم الهاتف =====
        total_tests += 1
        try:
            from src.utils.validators import validate_phone

            valid_phones = ["0501234567", "+966501234567", "966-50-123-4567"]
            invalid_phones = ["123", "abc", ""]

            all_valid = all(validate_phone(phone) for phone in valid_phones)
            all_invalid = all(not validate_phone(phone) for phone in invalid_phones)

            if all_valid and all_invalid:
                print(f"{total_tests}. ✅ التحقق من رقم الهاتف - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ التحقق من رقم الهاتف - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ التحقق من رقم الهاتف - خطأ: {e}")
            failed_tests += 1

        # ===== اختبار 8: التحقق من التاريخ =====
        total_tests += 1
        try:
            from src.utils.validators import validate_date

            valid_dates = ["2025-10-08", "2024-01-01", "2023-12-31"]
            invalid_dates = ["2025-13-01", "2025-10-32", "invalid", ""]

            all_valid = all(validate_date(date) for date in valid_dates)
            all_invalid = all(not validate_date(date) for date in invalid_dates)

            if all_valid and all_invalid:
                print(f"{total_tests}. ✅ التحقق من التاريخ - نجح")
                passed_tests += 1
            else:
                print(f"{total_tests}. ❌ التحقق من التاريخ - فشل")
                failed_tests += 1
        except Exception as e:
            print(f"{total_tests}. ❌ التحقق من التاريخ - خطأ: {e}")
            failed_tests += 1

        print()
        print("=" * 80)
        print("📊 النتائج النهائية")
        print("=" * 80)
        print(f"✅ نجح: {passed_tests}")
        print(f"❌ فشل: {failed_tests}")
        print(f"📈 نسبة النجاح: {(passed_tests/total_tests*100):.1f}%")
        print("=" * 80)

        return passed_tests == total_tests

    except ImportError as e:
        print(f"❌ خطأ في استيراد التطبيق: {e}")
        print("تأكد من وجود ملف app.py وتسجيل معالجات الأخطاء")
        return False
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_error_handlers()
    sys.exit(0 if success else 1)
