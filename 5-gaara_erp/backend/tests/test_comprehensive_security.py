# -*- coding: utf-8 -*-
# FILE: backend/tests/test_comprehensive_security.py | PURPOSE: Comprehensive Security Tests | OWNER: Backend | RELATED: app.py | LAST-AUDITED: 2025-10-21

"""
اختبارات الأمان الشاملة لنظام إدارة المخزون العربي
Comprehensive Security Tests for Arabic Inventory Management System

يتضمن:
- اختبارات SQL Injection
- اختبارات CSRF Protection
- اختبارات المصادقة والترخيص
- اختبارات التحقق من المدخلات
- اختبارات رؤوس الأمان
- اختبارات Rate Limiting
"""

import pytest
import json
import time
from unittest.mock import patch, MagicMock
from flask import Flask
from werkzeug.test import Client
from werkzeug.security import generate_password_hash

# استيراد التطبيق والنماذج
from app import create_app
from src.database import db
from src.models.user import User
from src.models.product_unified import Product
from src.models.inventory import Category
from src.models.supplier import Supplier


class TestSQLInjectionPrevention:
    """اختبارات منع حقن SQL"""

    @pytest.fixture
    def app(self):
        """إنشاء تطبيق للاختبار"""
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        """عميل الاختبار"""
        return app.test_client()

    @pytest.fixture
    def auth_headers(self, client):
        """رؤوس المصادقة"""
        # إنشاء مستخدم للاختبار
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "role": "admin",
        }
        response = client.post("/api/auth/register", json=user_data)

        # تسجيل الدخول
        login_data = {"email": "test@example.com", "password": "TestPassword123!"}
        response = client.post("/api/auth/login", json=login_data)
        token = response.json["access_token"]

        return {"Authorization": f"Bearer {token}"}

    def test_product_search_sql_injection(self, client, auth_headers):
        """اختبار منع حقن SQL في البحث عن المنتجات"""
        # محاولات حقن SQL مختلفة
        malicious_queries = [
            "'; DROP TABLE products; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO products VALUES (999, 'hacked'); --",
            "' OR 1=1 UNION SELECT password FROM users --",
        ]

        for query in malicious_queries:
            response = client.get(
                f"/api/products/search?q={query}", headers=auth_headers
            )

            # يجب أن يكون الرد آمناً ولا يحتوي على بيانات حساسة
            assert response.status_code in [200, 400]

            if response.status_code == 200:
                data = response.json
                # التأكد من عدم وجود بيانات مستخدمين أو جداول أخرى
                assert "password" not in str(data).lower()
                assert "drop table" not in str(data).lower()

    def test_inventory_update_sql_injection(self, client, auth_headers):
        """اختبار منع حقن SQL في تحديث المخزون"""
        malicious_data = {
            "product_id": "1'; DROP TABLE inventory; --",
            "quantity": "100; DELETE FROM products; --",
            "warehouse_id": "' OR '1'='1",
        }

        response = client.post(
            "/api/inventory/update", json=malicious_data, headers=auth_headers
        )

        # يجب أن يفشل التحديث أو يتم التعامل معه بأمان
        assert response.status_code in [400, 422]

    def test_report_generation_sql_injection(self, client, auth_headers):
        """اختبار منع حقن SQL في إنشاء التقارير"""
        malicious_params = {
            "start_date": "2023-01-01'; DROP TABLE sales; --",
            "end_date": "2023-12-31' OR '1'='1",
            "category_id": "' UNION SELECT * FROM users --",
        }

        response = client.get(
            "/api/reports/sales", query_string=malicious_params, headers=auth_headers
        )

        assert response.status_code in [200, 400, 422]

        if response.status_code == 200:
            data = response.json
            # التأكد من عدم تسريب بيانات حساسة
            assert "password" not in str(data).lower()


class TestCSRFProtection:
    """اختبارات حماية CSRF"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        app.config["WTF_CSRF_ENABLED"] = True
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_csrf_token_required_for_forms(self, client):
        """اختبار وجوب وجود CSRF token للنماذج"""
        # محاولة إرسال نموذج بدون CSRF token
        form_data = {"name": "Test Product", "price": 100, "category_id": 1}

        response = client.post("/api/products", data=form_data)

        # يجب أن يفشل بسبب عدم وجود CSRF token
        assert response.status_code in [400, 403]

    def test_csrf_token_validation(self, client):
        """اختبار التحقق من صحة CSRF token"""
        # الحصول على CSRF token
        response = client.get("/api/csrf-token")
        csrf_token = response.json["csrf_token"]

        # إرسال نموذج مع CSRF token صحيح
        form_data = {
            "name": "Test Product",
            "price": 100,
            "category_id": 1,
            "csrf_token": csrf_token,
        }

        response = client.post("/api/products", data=form_data)

        # يجب أن ينجح مع CSRF token صحيح
        assert response.status_code in [200, 201, 401]  # 401 إذا لم يكن مصادق عليه

    def test_csrf_token_reuse_prevention(self, client):
        """اختبار منع إعادة استخدام CSRF token"""
        # الحصول على CSRF token
        response = client.get("/api/csrf-token")
        csrf_token = response.json["csrf_token"]

        form_data = {
            "name": "Test Product 1",
            "price": 100,
            "category_id": 1,
            "csrf_token": csrf_token,
        }

        # الاستخدام الأول
        response1 = client.post("/api/products", data=form_data)

        # محاولة إعادة استخدام نفس الـ token
        form_data["name"] = "Test Product 2"
        response2 = client.post("/api/products", data=form_data)

        # يجب أن يفشل الاستخدام الثاني
        assert response2.status_code in [400, 403]


class TestAuthenticationSecurity:
    """اختبارات أمان المصادقة"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_password_hashing_strength(self, app):
        """اختبار قوة تشفير كلمات المرور"""
        with app.app_context():
            password = "TestPassword123!"
            hashed = generate_password_hash(password)

            # التأكد من أن كلمة المرور مشفرة
            assert hashed != password
            assert len(hashed) > 50  # طول مناسب للتشفير القوي
            assert hashed.startswith("pbkdf2:sha256")  # خوارزمية قوية

    def test_weak_password_rejection(self, client):
        """اختبار رفض كلمات المرور الضعيفة"""
        weak_passwords = [
            "123456",
            "password",
            "qwerty",
            "abc123",
            "12345678",
            "password123",
        ]

        for weak_password in weak_passwords:
            user_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": weak_password,
            }

            response = client.post("/api/auth/register", json=user_data)

            # يجب أن يرفض كلمات المرور الضعيفة
            assert response.status_code == 400
            assert "password" in response.json.get("errors", {})

    def test_brute_force_protection(self, client):
        """اختبار الحماية من هجمات القوة الغاشمة"""
        # محاولة تسجيل دخول متكررة بكلمة مرور خاطئة
        login_data = {"email": "test@example.com", "password": "wrongpassword"}

        failed_attempts = 0
        for i in range(10):
            response = client.post("/api/auth/login", json=login_data)
            if response.status_code == 429:  # Too Many Requests
                break
            failed_attempts += 1
            time.sleep(0.1)

        # يجب أن يتم حظر المحاولات بعد عدد معين
        assert failed_attempts < 10

    def test_jwt_token_security(self, client):
        """اختبار أمان JWT tokens"""
        # إنشاء مستخدم وتسجيل الدخول
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "role": "user",
        }
        client.post("/api/auth/register", json=user_data)

        login_data = {"email": "test@example.com", "password": "TestPassword123!"}
        response = client.post("/api/auth/login", json=login_data)
        token = response.json["access_token"]

        # التأكد من أن الـ token ليس فارغاً وله طول مناسب
        assert token
        assert len(token) > 100

        # محاولة استخدام token معدل
        modified_token = token[:-5] + "HACKED"
        headers = {"Authorization": f"Bearer {modified_token}"}

        response = client.get("/api/profile", headers=headers)
        assert response.status_code == 401


class TestInputValidation:
    """اختبارات التحقق من صحة المدخلات"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_product_data_validation(self, client):
        """اختبار التحقق من بيانات المنتج"""
        invalid_products = [
            # اسم فارغ
            {"name": "", "price": 100, "category_id": 1},
            # سعر سالب
            {"name": "Test Product", "price": -10, "category_id": 1},
            # تصنيف غير موجود
            {"name": "Test Product", "price": 100, "category_id": 99999},
            # نوع بيانات خاطئ
            {"name": 123, "price": "invalid", "category_id": "abc"},
            # حقول مفقودة
            {"name": "Test Product"},
            # قيم كبيرة جداً
            {"name": "A" * 1000, "price": 999999999, "category_id": 1},
        ]

        for invalid_product in invalid_products:
            response = client.post("/api/products", json=invalid_product)

            # يجب أن يرفض البيانات غير الصحيحة
            assert response.status_code in [400, 422]

    def test_xss_prevention(self, client):
        """اختبار منع XSS"""
        xss_payloads = [
            '<script>alert("XSS")</script>',
            'javascript:alert("XSS")',
            '<img src="x" onerror="alert(\'XSS\')">',
            '"><script>alert("XSS")</script>',
            "<svg onload=\"alert('XSS')\">",
        ]

        for payload in xss_payloads:
            product_data = {
                "name": payload,
                "description": payload,
                "price": 100,
                "category_id": 1,
            }

            response = client.post("/api/products", json=product_data)

            if response.status_code == 201:
                # التأكد من تنظيف البيانات
                product = response.json
                assert "<script>" not in product.get("name", "")
                assert "javascript:" not in product.get("description", "")

    def test_file_upload_validation(self, client):
        """اختبار التحقق من رفع الملفات"""
        # محاولة رفع ملف خبيث
        malicious_files = [
            ("test.php", b'<?php system($_GET["cmd"]); ?>'),
            ("test.exe", b"MZ\x90\x00"),  # PE header
            ("test.js", b'<script>alert("XSS")</script>'),
        ]

        for filename, content in malicious_files:
            data = {"file": (content, filename)}

            response = client.post("/api/upload", data=data)

            # يجب أن يرفض الملفات الخبيثة
            assert response.status_code in [400, 415]


class TestSecurityHeaders:
    """اختبارات رؤوس الأمان"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_security_headers_present(self, client):
        """اختبار وجود رؤوس الأمان"""
        response = client.get("/")

        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "Referrer-Policy",
        ]

        for header in required_headers:
            assert header in response.headers

    def test_content_security_policy(self, client):
        """اختبار Content Security Policy"""
        response = client.get("/")
        csp = response.headers.get("Content-Security-Policy")

        assert csp is not None
        assert "default-src 'self'" in csp
        assert "unsafe-eval" not in csp  # يجب تجنب unsafe-eval

    def test_frame_options(self, client):
        """اختبار X-Frame-Options"""
        response = client.get("/")
        frame_options = response.headers.get("X-Frame-Options")

        assert frame_options in ["DENY", "SAMEORIGIN"]

    def test_content_type_options(self, client):
        """اختبار X-Content-Type-Options"""
        response = client.get("/")
        content_type_options = response.headers.get("X-Content-Type-Options")

        assert content_type_options == "nosniff"


class TestRateLimiting:
    """اختبارات تحديد المعدل"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        app.config["RATELIMIT_ENABLED"] = True
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_api_rate_limiting(self, client):
        """اختبار تحديد معدل API"""
        # إرسال طلبات متعددة بسرعة
        responses = []
        for i in range(100):
            response = client.get("/api/products")
            responses.append(response.status_code)

            if response.status_code == 429:
                break

        # يجب أن يتم تحديد المعدل
        assert 429 in responses

    def test_login_rate_limiting(self, client):
        """اختبار تحديد معدل تسجيل الدخول"""
        login_data = {"email": "test@example.com", "password": "wrongpassword"}

        responses = []
        for i in range(20):
            response = client.post("/api/auth/login", json=login_data)
            responses.append(response.status_code)

            if response.status_code == 429:
                break

        # يجب أن يتم تحديد معدل محاولات تسجيل الدخول
        assert 429 in responses


class TestDataLeakagePrevention:
    """اختبارات منع تسريب البيانات"""

    @pytest.fixture
    def app(self):
        app = create_app("testing")
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_error_messages_sanitization(self, client):
        """اختبار تنظيف رسائل الخطأ"""
        # محاولة الوصول لمورد غير موجود
        response = client.get("/api/products/99999")

        # التأكد من عدم تسريب معلومات النظام في رسائل الخطأ
        error_data = response.json
        assert "traceback" not in str(error_data).lower()
        assert "stack trace" not in str(error_data).lower()
        assert "database" not in str(error_data).lower()
        assert "sql" not in str(error_data).lower()

    def test_user_data_exposure(self, client):
        """اختبار عدم تعرض بيانات المستخدمين"""
        # محاولة الحصول على قائمة المستخدمين بدون صلاحية
        response = client.get("/api/users")

        if response.status_code == 200:
            users = response.json
            for user in users:
                # التأكد من عدم تعرض كلمات المرور
                assert "password" not in user
                assert "password_hash" not in user
                # التأكد من عدم تعرض معلومات حساسة أخرى
                assert "secret" not in str(user).lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
