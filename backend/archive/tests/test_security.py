"""
اختبارات نظام الأمان
Security System Tests
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.security import (
    CSRFProtection,
    RateLimiter,
    sanitize_input,
    sanitize_dict,
    PasswordPolicy,
    FileUploadSecurity,
)


def test_csrf_protection():
    """اختبار حماية CSRF"""
    print("\n" + "=" * 60)
    print("🔒 اختبار حماية CSRF")
    print("=" * 60)

    csrf = CSRFProtection()
    session_id = "test_session_123"

    # Generate token
    token = csrf.generate_token(session_id)
    print(f"✅ تم توليد Token: {token[:20]}...")

    # Validate correct token
    is_valid = csrf.validate_token(session_id, token)
    print(f"✅ التحقق من Token صحيح: {is_valid}")
    assert is_valid, "Token should be valid"

    # Validate incorrect token
    is_valid = csrf.validate_token(session_id, "wrong_token")
    print(f"✅ التحقق من Token خاطئ: {is_valid}")
    assert not is_valid, "Wrong token should be invalid"

    print("✅ اختبار CSRF نجح!")
    return True


def test_rate_limiter():
    """اختبار تحديد معدل الطلبات"""
    print("\n" + "=" * 60)
    print("⏱️ اختبار Rate Limiter")
    print("=" * 60)

    limiter = RateLimiter()
    identifier = "test_user_123"

    # Test within limit
    for i in range(5):
        allowed = limiter.is_allowed(identifier, max_requests=10, window=60)
        print(f"  طلب {i+1}: {'✅ مسموح' if allowed else '❌ محظور'}")
        assert allowed, f"Request {i+1} should be allowed"

    # Test exceeding limit
    limiter.requests[identifier]["count"] = 10
    allowed = limiter.is_allowed(identifier, max_requests=10, window=60)
    print(f"  طلب 11 (تجاوز الحد): {'✅ مسموح' if allowed else '❌ محظور'}")
    assert not allowed, "Request should be blocked"

    print("✅ اختبار Rate Limiter نجح!")
    return True


def test_input_sanitization():
    """اختبار تنظيف المدخلات"""
    print("\n" + "=" * 60)
    print("🧹 اختبار تنظيف المدخلات")
    print("=" * 60)

    # Test HTML removal
    dirty = "<script>alert('XSS')</script>Hello"
    clean = sanitize_input(dirty)
    print(f"  قبل: {dirty}")
    print(f"  بعد: {clean}")
    assert "<script>" not in clean, "Script tags should be removed"

    # Test SQL injection prevention
    dirty = "admin' OR '1'='1"
    clean = sanitize_input(dirty)
    print(f"  قبل: {dirty}")
    print(f"  بعد: {clean}")
    assert "OR" not in clean.upper(), "SQL keywords should be removed"

    # Test dict sanitization
    dirty_dict = {
        "name": "<b>Test</b>",
        "email": "test@test.com",
        "comment": "'; DROP TABLE users--",
    }
    clean_dict = sanitize_dict(dirty_dict)
    print(f"  قبل: {dirty_dict}")
    print(f"  بعد: {clean_dict}")
    assert "<b>" not in clean_dict["name"], "HTML should be removed from dict"

    print("✅ اختبار تنظيف المدخلات نجح!")
    return True


def test_password_policy():
    """اختبار سياسة كلمات المرور"""
    print("\n" + "=" * 60)
    print("🔐 اختبار سياسة كلمات المرور")
    print("=" * 60)

    # Test weak password
    is_valid, errors, strength = PasswordPolicy.validate_strength("123456")
    print(f"\n  كلمة المرور: '123456'")
    print(f"  صالحة: {is_valid}")
    print(f"  القوة: {strength}")
    print(f"  الأخطاء: {errors}")
    assert not is_valid, "Weak password should be invalid"

    # Test medium password
    is_valid, errors, strength = PasswordPolicy.validate_strength("Password123")
    print(f"\n  كلمة المرور: 'Password123'")
    print(f"  صالحة: {is_valid}")
    print(f"  القوة: {strength}")
    print(f"  الأخطاء: {errors}")

    # Test strong password
    is_valid, errors, strength = PasswordPolicy.validate_strength("MyP@ssw0rd123!")
    print(f"\n  كلمة المرور: 'MyP@ssw0rd123!'")
    print(f"  صالحة: {is_valid}")
    print(f"  القوة: {strength}")
    print(f"  الأخطاء: {errors}")
    assert is_valid, "Strong password should be valid"
    assert strength == "قوي", "Should be strong password"

    print("\n✅ اختبار سياسة كلمات المرور نجح!")
    return True


def test_file_upload_security():
    """اختبار أمان رفع الملفات"""
    print("\n" + "=" * 60)
    print("📁 اختبار أمان رفع الملفات")
    print("=" * 60)

    # Test allowed extensions
    test_files = [
        ("image.jpg", True),
        ("document.pdf", True),
        ("script.exe", False),
        ("malware.bat", False),
        ("data.xlsx", True),
    ]

    for filename, should_allow in test_files:
        allowed = FileUploadSecurity.allowed_file(filename)
        status = "✅ مسموح" if allowed else "❌ محظور"
        print(f"  {filename}: {status}")
        assert allowed == should_allow, f"File {filename} validation failed"

    # Test safe filename generation
    dangerous_names = ["../../../etc/passwd", "file<script>.jpg", "test file!@#$.pdf"]

    print("\n  توليد أسماء ملفات آمنة:")
    for name in dangerous_names:
        safe = FileUploadSecurity.generate_safe_filename(name)
        print(f"    {name} → {safe}")
        assert "../" not in safe, "Path traversal should be prevented"
        assert "<" not in safe, "Special chars should be removed"

    print("\n✅ اختبار أمان رفع الملفات نجح!")
    return True


def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("\n" + "=" * 60)
    print("🧪 بدء اختبارات نظام الأمان")
    print("=" * 60)

    tests = [
        ("CSRF Protection", test_csrf_protection),
        ("Rate Limiter", test_rate_limiter),
        ("Input Sanitization", test_input_sanitization),
        ("Password Policy", test_password_policy),
        ("File Upload Security", test_file_upload_security),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ فشل اختبار {name}: {str(e)}")
            failed += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبارات")
    print("=" * 60)
    print(f"✅ نجح: {passed}/{len(tests)}")
    print(f"❌ فشل: {failed}/{len(tests)}")
    print(f"📈 نسبة النجاح: {(passed/len(tests)*100):.1f}%")
    print("=" * 60)

    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()

    if failed == 0:
        print("\n🎉 جميع الاختبارات نجحت!")
        sys.exit(0)
    else:
        print(f"\n⚠️ فشل {failed} اختبار(ات)")
        sys.exit(1)
