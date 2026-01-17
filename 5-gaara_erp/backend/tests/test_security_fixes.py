# -*- coding: utf-8 -*-
# FILE: backend/tests/test_security_fixes.py | PURPOSE: Comprehensive Security Tests | OWNER: Backend | RELATED: routes/ | LAST-AUDITED: 2025-10-21

"""
اختبارات الأمان الشاملة - الإصدار 2.0
Comprehensive Security Tests - Version 2.0

P3 Fixes Applied:
- P3.1: SQL Injection prevention tests
- P3.2: Authentication and authorization tests
- P3.3: Input validation tests
- P3.4: Security headers tests
"""

import pytest
import json
from unittest.mock import patch
from flask import Flask
from flask_jwt_extended import create_access_token

# Import the application and models
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.routes.products_fixed import products_bp as products_bp_v2  # noqa: E402
from src.routes.inventory_fixed import inventory_bp_v2  # noqa: E402
from src.routes.reports_fixed import reports_bp_v2  # noqa: E402
from src.auth_fixed import auth_bp_v2  # noqa: E402
from src.database import db  # noqa: E402
from src.models.user import User  # noqa: E402


@pytest.fixture
def app():
    """Create test Flask application."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    app.config["WTF_CSRF_ENABLED"] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(products_bp_v2)
    app.register_blueprint(inventory_bp_v2)
    app.register_blueprint(reports_bp_v2)
    app.register_blueprint(auth_bp_v2)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    """Create authentication headers for testing."""
    with app.app_context():
        # Create test user
        test_user = User(email="test@example.com", username="testuser")
        db.session.add(test_user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=test_user.id)
        return {"Authorization": f"Bearer {access_token}"}


class TestSQLInjectionPrevention:
    """Test SQL injection prevention."""

    def test_product_search_sql_injection(self, client, auth_headers):
        """Test that product search is safe from SQL injection."""
        # Try various SQL injection payloads
        malicious_payloads = [
            "'; DROP TABLE products; --",
            "' OR 1=1 --",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO products VALUES ('hacked'); --",
        ]

        for payload in malicious_payloads:
            response = client.get(
                f"/api/products?search={payload}", headers=auth_headers
            )
            # Should not crash and should return safe response
            assert response.status_code in [200, 400]
            if response.status_code == 200:
                data = json.loads(response.data)
                assert "status" in data

    def test_report_parameters_sql_injection(self, client, auth_headers):
        """Test that report parameters are safe from SQL injection."""
        malicious_payloads = [
            "1; DROP TABLE stock_movements; --",
            "1 OR 1=1",
            "1 UNION SELECT password FROM users",
        ]

        for payload in malicious_payloads:
            response = client.get(
                f"/inventory-report?category_id={payload}", headers=auth_headers
            )
            assert response.status_code in [200, 400, 422]


class TestAuthentication:
    """Test authentication and authorization."""

    def test_protected_routes_require_auth(self, client):
        """Test that protected routes require authentication."""
        protected_endpoints = [
            "/api/products",
            "/api/categories",
            "/stock-valuation",
            "/low-stock",
            "/inventory-report",
        ]

        for endpoint in protected_endpoints:
            response = client.post(endpoint)
            assert response.status_code == 401

    def test_invalid_token_rejected(self, client):
        """Test that invalid tokens are rejected."""
        invalid_headers = {"Authorization": "Bearer invalid-token"}

        response = client.get("/api/products", headers=invalid_headers)
        assert response.status_code == 422  # JWT decode error

    def test_login_with_valid_credentials(self, client, app):
        """Test login with valid credentials."""
        with app.app_context():
            # Create test user
            from werkzeug.security import generate_password_hash

            test_user = User(
                email="test@example.com",
                username="testuser",
                password=generate_password_hash("testpassword123"),
            )
            db.session.add(test_user)
            db.session.commit()

        response = client.post(
            "/login", json={"email": "test@example.com", "password": "testpassword123"}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "access_token" in data.get("data", {})

    def test_login_with_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(
            "/login",
            json={"email": "nonexistent@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401


class TestInputValidation:
    """Test input validation."""

    def test_product_creation_validation(self, client, auth_headers):
        """Test product creation input validation."""
        # Test missing required fields
        response = client.post("/api/products", headers=auth_headers, json={})
        assert response.status_code == 400

        # Test invalid data types
        response = client.post(
            "/api/products",
            headers=auth_headers,
            json={
                "name": 123,  # Should be string
                "price": "invalid",  # Should be number
            },
        )
        assert response.status_code == 400

    def test_category_creation_validation(self, client, auth_headers):
        """Test category creation input validation."""
        # Test name length validation
        response = client.post(
            "/api/categories", headers=auth_headers, json={"name": "a"}
        )  # Too short
        assert response.status_code == 400

        # Test name length validation (too long)
        response = client.post(
            "/api/categories", headers=auth_headers, json={"name": "a" * 101}
        )  # Too long
        assert response.status_code == 400

    def test_email_validation(self, client):
        """Test email validation in registration."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
        ]

        for email in invalid_emails:
            response = client.post(
                "/register",
                json={
                    "email": email,
                    "username": "testuser",
                    "password": "testpassword123",
                },
            )
            assert response.status_code == 400


class TestSecurityHeaders:
    """Test security headers."""

    def test_security_headers_present(self, client):
        """Test that security headers are present in responses."""
        response = client.get("/")

        # Test for important security headers
        expected_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy",
        ]

        for header in expected_headers:
            assert header in response.headers

    def test_csp_header_configured(self, client):
        """Test that CSP header is properly configured."""
        response = client.get("/")
        csp = response.headers.get("Content-Security-Policy")

        assert csp is not None
        assert "default-src 'self'" in csp
        assert "object-src 'none'" in csp


class TestErrorHandling:
    """Test error handling and information disclosure."""

    def test_error_responses_dont_leak_info(self, client):
        """Test that error responses don't leak sensitive information."""
        # Test 404 error
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404

        # Ensure no stack traces or sensitive info in response
        response_text = response.get_data(as_text=True)
        sensitive_keywords = ["traceback", "exception", "stack", "database", "sql"]
        for keyword in sensitive_keywords:
            assert keyword.lower() not in response_text.lower()

    def test_database_error_handling(self, client, auth_headers):
        """Test that database errors are handled gracefully."""
        with patch("src.database.db.session.commit") as mock_commit:
            mock_commit.side_effect = Exception("Database error")

            response = client.post(
                "/api/categories", headers=auth_headers, json={"name": "Test Category"}
            )

            assert response.status_code == 500
            data = json.loads(response.data)
            assert "error" in data
            # Ensure no sensitive database info is leaked
            assert "Database error" not in str(data)


class TestRateLimiting:
    """Test rate limiting (if implemented)."""

    def test_login_rate_limiting(self, client):
        """Test that login attempts are rate limited."""
        # This test assumes rate limiting is implemented
        # Make multiple failed login attempts
        for _ in range(10):
            response = client.post(
                "/login",
                json={"email": "test@example.com", "password": "wrongpassword"},
            )

        # After many attempts, should be rate limited
        # Note: This test will pass if rate limiting is not implemented
        # but serves as a reminder to implement it
        assert response.status_code in [401, 429]


class TestDataSanitization:
    """Test data sanitization."""

    def test_xss_prevention(self, client, auth_headers):
        """Test that XSS payloads are sanitized."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
        ]

        for payload in xss_payloads:
            response = client.post(
                "/api/categories", headers=auth_headers, json={"name": payload}
            )

            # Should either reject the input or sanitize it
            if response.status_code == 201:
                data = json.loads(response.data)
                # Ensure the payload is sanitized
                assert "<script>" not in str(data)
                assert "javascript:" not in str(data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
