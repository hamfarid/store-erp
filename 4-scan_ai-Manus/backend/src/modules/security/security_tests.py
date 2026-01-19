"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/security/security_tests.py
الوصف: اختبارات أمان النظام للتحقق من فعالية طبقات الحماية
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import time
import unittest
from datetime import datetime, timedelta, timezone

import jwt
import requests

# عنوان الخادم المحلي للاختبار
BASE_URL = "http://localhost:8000"
SECRET_KEY = "test_secret_key"  # مفتاح الاختبار فقط


class SecurityTests(unittest.TestCase):
    """
    اختبارات شاملة لطبقات الحماية الأمنية في النظام

    تتضمن هذه الاختبارات:
    - اختبار الحماية من هجمات XSS
    - اختبار الحماية من هجمات CSRF
    - اختبار الحماية من هجمات حقن SQL
    - اختبار تحديد معدل الطلبات
    - اختبار التحقق من الصلاحيات
    - اختبار حظر المستخدم بعد محاولات فاشلة
    """

    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "SecurityTestAgent"
        }

    def test_xss_protection(self):
        """
        اختبار الحماية من هجمات XSS
        """
        # محاولة إرسال نص يحتوي على سكريبت
        xss_payload = "<script>alert('XSS')</script>"
        data = {
            "username": "test_user",
            "comment": xss_payload
        }

        response = self.session.post(
            f"{BASE_URL}/api/comments",
            headers=self.headers,
            json=data
        )

        # التحقق من وجود رؤوس الحماية من XSS
        self.assertEqual(
            response.headers.get("X-XSS-Protection"),
            "1; mode=block")
        self.assertEqual(response.headers.get(
            "X-Content-Type-Options"), "nosniff")
        self.assertIsNotNone(response.headers.get("Content-Security-Policy"))

        # التحقق من تنظيف المحتوى
        if response.status_code == 200:
            result = response.json()
            self.assertNotIn("<script>", result.get("comment", ""))

    def test_csrf_protection(self):
        """
        اختبار الحماية من هجمات CSRF
        """
        # الحصول على رمز CSRF من طلب GET
        response = self.session.get(f"{BASE_URL}/api/user/profile")
        csrf_token = response.headers.get("X-CSRF-Token")

        # محاولة إرسال طلب POST بدون رمز CSRF
        data = {"name": "Test User", "email": "test@example.com"}
        response_without_token = self.session.post(
            f"{BASE_URL}/api/user/profile",
            headers=self.headers,
            json=data
        )

        # يجب أن يفشل الطلب بدون رمز CSRF
        self.assertEqual(response_without_token.status_code, 403)

        # إرسال طلب POST مع رمز CSRF
        headers_with_token = self.headers.copy()
        headers_with_token["X-CSRF-Token"] = csrf_token

        response_with_token = self.session.post(
            f"{BASE_URL}/api/user/profile",
            headers=headers_with_token,
            json=data
        )

        # يجب أن ينجح الطلب مع رمز CSRF
        self.assertNotEqual(response_with_token.status_code, 403)

    def test_sql_injection_protection(self):
        """
        اختبار الحماية من هجمات حقن SQL
        """
        # قائمة بمحاولات حقن SQL
        sql_injection_attempts = [
            "1' OR '1'='1",
            "1; DROP TABLE users;",
            "1' UNION SELECT username, password FROM users;",
            "1' OR 1=1 --",
            "admin'--",
            "admin' #",
            "admin'/*",
            "' OR 1=1 /*",
            "'; exec xp_cmdshell('dir') --",
            "1' waitfor delay '0:0:10'--"
        ]

        for attempt in sql_injection_attempts:
            # محاولة تسجيل الدخول باستخدام حقن SQL
            data = {
                "username": attempt,
                "password": "password"
            }

            response = self.session.post(
                f"{BASE_URL}/api/auth/login",
                headers=self.headers,
                json=data
            )

            # يجب أن يفشل الطلب مع رمز 400 أو 401
            self.assertIn(response.status_code, [400, 401, 403])

            # محاولة استخدام حقن SQL في معلمات URL
            response = self.session.get(
                f"{BASE_URL}/api/users?id={attempt}"
            )

            # يجب أن يفشل الطلب مع رمز 400 أو 403
            self.assertIn(response.status_code, [400, 403])

    def test_rate_limiting(self):
        """
        اختبار تحديد معدل الطلبات
        """
        # إرسال عدد كبير من الطلبات في وقت قصير
        for i in range(100):
            response = self.session.get(
                f"{BASE_URL}/api/health?iteration={i}",
                headers=self.headers
            )

            # إذا تم تجاوز الحد، يجب أن يعود رمز 429
            if response.status_code == 429:
                break

        # يجب أن يتم تطبيق تحديد معدل الطلبات
        self.assertEqual(response.status_code, 429)

        # الانتظار لفترة قصيرة
        time.sleep(5)

        # محاولة إرسال طلب جديد
        response = self.session.get(
            f"{BASE_URL}/api/health",
            headers=self.headers
        )

        # يجب أن ينجح الطلب بعد الانتظار
        self.assertNotEqual(response.status_code, 429)

    def test_permission_validation(self):
        """
        اختبار التحقق من الصلاحيات
        """
        # إنشاء رمز JWT للمستخدم العادي
        user_payload = {
            "sub": "user123",
            "roles": ["user"],
            "permissions": ["read"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        user_token = jwt.encode(user_payload, SECRET_KEY, algorithm="HS256")

        # إنشاء رمز JWT للمسؤول
        admin_payload = {
            "sub": "admin123",
            "roles": ["admin"],
            "permissions": ["read", "write", "admin"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        admin_token = jwt.encode(admin_payload, SECRET_KEY, algorithm="HS256")

        # محاولة الوصول إلى مسار المسؤول بدون رمز
        response_no_token = self.session.get(
            f"{BASE_URL}/api/admin/users",
            headers=self.headers
        )

        # يجب أن يفشل الطلب بدون رمز
        self.assertEqual(response_no_token.status_code, 401)

        # محاولة الوصول إلى مسار المسؤول برمز المستخدم العادي
        headers_user = self.headers.copy()
        headers_user["Authorization"] = f"Bearer {user_token}"

        response_user = self.session.get(
            f"{BASE_URL}/api/admin/users",
            headers=headers_user
        )

        # يجب أن يفشل الطلب مع صلاحيات المستخدم العادي
        self.assertEqual(response_user.status_code, 403)

        # محاولة الوصول إلى مسار المسؤول برمز المسؤول
        headers_admin = self.headers.copy()
        headers_admin["Authorization"] = f"Bearer {admin_token}"

        response_admin = self.session.get(
            f"{BASE_URL}/api/admin/users",
            headers=headers_admin
        )

        # يجب أن ينجح الطلب مع صلاحيات المسؤول
        self.assertNotEqual(response_admin.status_code, 403)

    def test_user_blocking_after_failed_attempts(self):
        """
        اختبار حظر المستخدم بعد محاولات فاشلة
        """
        # محاولة تسجيل الدخول بكلمة مرور خاطئة عدة مرات
        for i in range(6):  # أكثر من الحد المسموح (5 محاولات)
            data = {
                "username": "test_user",
                "password": "wrong_password"
            }

            response = self.session.post(
                f"{BASE_URL}/api/auth/login",
                headers=self.headers,
                json=data
            )

            # يجب أن تفشل المحاولات
            self.assertIn(response.status_code, [400, 401])

        # محاولة تسجيل الدخول بكلمة المرور الصحيحة
        data = {
            "username": "test_user",
            "password": "correct_password"
        }

        response = self.session.post(
            f"{BASE_URL}/api/auth/login",
            headers=self.headers,
            json=data
        )

        # يجب أن يفشل الطلب بسبب الحظر
        self.assertEqual(response.status_code, 423)  # Locked

    def test_admin_notification_for_blocked_user(self):
        """
        اختبار إشعار المسؤول عند حظر مستخدم
        """
        # إنشاء رمز JWT للمسؤول
        admin_payload = {
            "sub": "admin123",
            "roles": ["admin"],
            "permissions": ["read", "write", "admin"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        admin_token = jwt.encode(admin_payload, SECRET_KEY, algorithm="HS256")

        # الحصول على قائمة الإشعارات للمسؤول
        headers_admin = self.headers.copy()
        headers_admin["Authorization"] = f"Bearer {admin_token}"

        response = self.session.get(
            f"{BASE_URL}/api/admin/notifications",
            headers=headers_admin
        )

        # التحقق من وجود إشعار حظر المستخدم
        if response.status_code == 200:
            notifications = response.json()
            blocked_notifications = [
                n for n in notifications
                if "blocked" in n.get("message", "").lower()
            ]
            self.assertGreater(len(blocked_notifications), 0)

    def test_unblock_user(self):
        """
        اختبار إلغاء حظر المستخدم
        """
        # إنشاء رمز JWT للمسؤول
        admin_payload = {
            "sub": "admin123",
            "roles": ["admin"],
            "permissions": ["read", "write", "admin"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        admin_token = jwt.encode(admin_payload, SECRET_KEY, algorithm="HS256")

        # إلغاء حظر المستخدم
        headers_admin = self.headers.copy()
        headers_admin["Authorization"] = f"Bearer {admin_token}"

        data = {"username": "test_user"}

        response = self.session.post(
            f"{BASE_URL}/api/admin/unblock-user",
            headers=headers_admin,
            json=data
        )

        # يجب أن ينجح إلغاء الحظر
        self.assertEqual(response.status_code, 200)

        # محاولة تسجيل الدخول مرة أخرى
        data = {
            "username": "test_user",
            "password": "correct_password"
        }

        response = self.session.post(
            f"{BASE_URL}/api/auth/login",
            headers=self.headers,
            json=data
        )

        # يجب أن ينجح تسجيل الدخول بعد إلغاء الحظر
        self.assertNotEqual(response.status_code, 423)

    def test_ssl_headers(self):
        """
        اختبار رؤوس SSL والأمان
        """
        response = self.session.get(f"{BASE_URL}/api/health")

        # التحقق من وجود رؤوس الأمان
        self.assertIsNotNone(response.headers.get("Strict-Transport-Security"))
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(response.headers.get(
            "X-Content-Type-Options"), "nosniff")

    def tearDown(self):
        """
        تنظيف بيئة الاختبار
        """
        self.session.close()


if __name__ == "__main__":
    unittest.main()
