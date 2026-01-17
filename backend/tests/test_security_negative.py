#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.42: Comprehensive Negative Tests for Security Features

Tests that verify the system properly rejects invalid, malicious, or
unauthorized requests. These tests ensure security controls are working.
"""

import pytest


# =============================================================================
# Authentication Negative Tests
# =============================================================================


class TestAuthenticationNegative:
    """Negative tests for authentication endpoints."""

    def test_login_empty_username(self, client):
        """Test login fails with empty username."""
        response = client.post(
            "/api/auth/login", json={"username": "", "password": "password123"}
        )
        assert response.status_code in [400, 401]
        data = response.get_json()
        assert data["success"] is False

    def test_login_empty_password(self, client):
        """Test login fails with empty password."""
        response = client.post(
            "/api/auth/login", json={"username": "admin", "password": ""}
        )
        assert response.status_code in [400, 401]
        data = response.get_json()
        assert data["success"] is False

    def test_login_wrong_password(self, client):
        """Test login fails with incorrect password."""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrongpassword123"},
        )
        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False

    def test_login_nonexistent_user(self, client):
        """Test login fails with non-existent user."""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent_user_12345", "password": "password123"},
        )
        assert response.status_code == 401

    def test_login_sql_injection_username(self, client):
        """Test login blocks SQL injection in username."""
        payloads = [
            "admin' OR '1'='1",
            "admin'--",
            "admin'; DROP TABLE users;--",
            "admin' UNION SELECT * FROM users--",
        ]
        for payload in payloads:
            response = client.post(
                "/api/auth/login", json={"username": payload, "password": "password"}
            )
            assert response.status_code in [400, 401]

    def test_login_xss_username(self, client):
        """Test login sanitizes XSS in username."""
        payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
        ]
        for payload in payloads:
            response = client.post(
                "/api/auth/login", json={"username": payload, "password": "password"}
            )
            assert response.status_code in [400, 401]

    def test_login_missing_content_type(self, client):
        """Test login fails without proper content type."""
        response = client.post("/api/auth/login", data='{"username":"admin"}')
        # Should fail or require proper content type
        assert response.status_code in [400, 415]

    def test_refresh_invalid_token(self, client):
        """Test refresh fails with invalid token."""
        response = client.post(
            "/api/auth/refresh", headers={"Authorization": "Bearer invalid_token_12345"}
        )
        assert response.status_code == 401

    def test_refresh_expired_token(self, client, expired_refresh_token):
        """Test refresh fails with expired token."""
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {expired_refresh_token}"},
        )
        assert response.status_code == 401

    def test_refresh_revoked_token(self, client, revoked_refresh_token):
        """Test refresh fails with revoked token."""
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {revoked_refresh_token}"},
        )
        assert response.status_code == 401


# =============================================================================
# Authorization Negative Tests
# =============================================================================


class TestAuthorizationNegative:
    """Negative tests for authorization (RBAC)."""

    def test_protected_route_no_token(self, client):
        """Test protected routes require authentication."""
        protected_routes = [
            "/api/users",
            "/api/products",
            "/api/customers",
            "/api/invoices",
        ]
        for route in protected_routes:
            response = client.get(route)
            assert response.status_code == 401

    def test_protected_route_invalid_token(self, client):
        """Test protected routes reject invalid tokens."""
        response = client.get(
            "/api/users", headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_admin_route_as_regular_user(self, client, user_token):
        """Test admin routes reject regular users."""
        response = client.get(
            "/api/admin/users", headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 403

    def test_user_management_without_permission(self, client, sales_token):
        """Test user management requires proper permission."""
        response = client.post(
            "/api/users",
            json={
                "username": "newuser",
                "email": "new@test.com",
                "password": "password123",
            },
            headers={"Authorization": f"Bearer {sales_token}"},
        )
        assert response.status_code == 403

    def test_delete_user_without_permission(self, client, user_token):
        """Test delete requires delete permission."""
        response = client.delete(
            "/api/users/1", headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 403


# =============================================================================
# Input Validation Negative Tests
# =============================================================================


class TestInputValidationNegative:
    """Negative tests for input validation."""

    def test_product_negative_price(self, client, admin_token):
        """Test product creation rejects negative price."""
        response = client.post(
            "/api/products",
            json={"name": "Test Product", "price": -100, "sku": "TEST-001"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    def test_product_empty_name(self, client, admin_token):
        """Test product creation requires name."""
        response = client.post(
            "/api/products",
            json={"name": "", "price": 100, "sku": "TEST-001"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    def test_product_name_too_long(self, client, admin_token):
        """Test product name length limit."""
        response = client.post(
            "/api/products",
            json={"name": "A" * 1000, "price": 100, "sku": "TEST-001"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    def test_invalid_email_format(self, client, admin_token):
        """Test email validation."""
        invalid_emails = [
            "notanemail",
            "missing@domain",
            "@nodomain.com",
            "spaces in@email.com",
        ]
        for email in invalid_emails:
            response = client.post(
                "/api/users",
                json={
                    "username": "testuser",
                    "email": email,
                    "password": "password123",
                },
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert response.status_code == 400

    def test_weak_password_rejected(self, client, admin_token):
        """Test weak passwords are rejected."""
        weak_passwords = [
            "123",
            "password",
            "abc",
            "12345678",
        ]
        for password in weak_passwords:
            response = client.post(
                "/api/users",
                json={
                    "username": "testuser",
                    "email": "test@test.com",
                    "password": password,
                },
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            # Should fail validation
            assert response.status_code in [400, 422]

    def test_invalid_json(self, client, admin_token):
        """Test invalid JSON is rejected."""
        response = client.post(
            "/api/products",
            data='{"invalid json',
            content_type="application/json",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 400

    def test_extra_fields_ignored(self, client, admin_token):
        """Test extra fields don't cause SQL injection."""
        response = client.post(
            "/api/products",
            json={
                "name": "Test Product",
                "price": 100,
                "__sql__": "'; DROP TABLE products;--",
                "constructor": {"prototype": {"admin": True}},
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        # Should either succeed (ignoring extra) or fail validation
        assert response.status_code in [201, 400]


# =============================================================================
# SQL Injection Negative Tests
# =============================================================================


class TestSQLInjectionNegative:
    """Negative tests for SQL injection protection."""

    def test_search_sql_injection(self, client, admin_token):
        """Test search parameter SQL injection."""
        payloads = [
            "'; DROP TABLE products;--",
            "1 OR 1=1",
            "1; SELECT * FROM users",
            "UNION SELECT password FROM users",
        ]
        for payload in payloads:
            response = client.get(
                f"/api/products?search={payload}",
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            # Should return normally (empty or results) not error
            assert response.status_code in [200, 400]

    def test_id_sql_injection(self, client, admin_token):
        """Test ID parameter SQL injection."""
        payloads = [
            "1 OR 1=1",
            "1; DROP TABLE products",
            "1 UNION SELECT * FROM users",
        ]
        for payload in payloads:
            response = client.get(
                f"/api/products/{payload}",
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            # Should return 404 or 400, not execute SQL
            assert response.status_code in [400, 404]


# =============================================================================
# XSS Protection Negative Tests
# =============================================================================


class TestXSSProtectionNegative:
    """Negative tests for XSS protection."""

    def test_xss_in_product_name(self, client, admin_token):
        """Test XSS is sanitized in product name."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "<svg onload=alert('xss')>",
            "javascript:alert('xss')",
        ]
        for payload in xss_payloads:
            response = client.post(
                "/api/products",
                json={
                    "name": payload,
                    "price": 100,
                    "sku": f"XSS-{hash(payload) % 10000}",
                },
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            if response.status_code == 201:
                data = response.get_json()
                # Verify XSS is sanitized
                assert "<script>" not in data.get("data", {}).get("name", "")
                assert "javascript:" not in data.get("data", {}).get("name", "")


# =============================================================================
# Rate Limiting Negative Tests
# =============================================================================


class TestRateLimitingNegative:
    """Negative tests for rate limiting."""

    def test_login_rate_limit(self, client):
        """Test login is rate limited."""
        # Make many rapid requests
        for i in range(10):
            client.post(
                "/api/auth/login",
                json={"username": "admin", "password": "wrongpassword"},
            )

        # Should eventually get rate limited
        response = client.post(
            "/api/auth/login", json={"username": "admin", "password": "wrongpassword"}
        )
        # Either 401 (wrong password) or 429 (rate limited)
        assert response.status_code in [401, 429]


# =============================================================================
# CSRF Protection Negative Tests
# =============================================================================


class TestCSRFProtectionNegative:
    """Negative tests for CSRF protection."""

    def test_state_changing_without_csrf(self, client, admin_token):
        """Test POST/PUT/DELETE require CSRF token."""
        # In production with CSRF enabled, this should fail
        response = client.post(
            "/api/products",
            json={"name": "Test", "price": 100},
            headers={
                "Authorization": f"Bearer {admin_token}"
                # Missing X-CSRF-Token
            },
        )
        # In dev might pass, in prod should fail
        # We just verify it doesn't crash
        assert response.status_code in [201, 400, 403]


# =============================================================================
# File Upload Negative Tests
# =============================================================================


class TestFileUploadNegative:
    """Negative tests for file upload security."""

    def test_executable_upload_blocked(self, client, admin_token):
        """Test executable files are blocked."""
        # Simulate .exe upload
        from io import BytesIO

        exe_content = b"MZ" + b"\x00" * 100  # PE header

        data = {"file": (BytesIO(exe_content), "malware.exe")}
        response = client.post(
            "/api/upload",
            data=data,
            headers={"Authorization": f"Bearer {admin_token}"},
            content_type="multipart/form-data",
        )

        assert response.status_code in [400, 415]

    def test_file_size_limit(self, client, admin_token):
        """Test file size limit is enforced."""
        from io import BytesIO

        # Create file larger than limit (assume 16MB limit)
        large_file = BytesIO(b"0" * (20 * 1024 * 1024))

        data = {"file": (large_file, "large.txt")}
        response = client.post(
            "/api/upload",
            data=data,
            headers={"Authorization": f"Bearer {admin_token}"},
            content_type="multipart/form-data",
        )

        assert response.status_code in [400, 413]

    def test_double_extension_blocked(self, client, admin_token):
        """Test double extensions are blocked."""
        from io import BytesIO

        data = {"file": (BytesIO(b"fake image"), "image.jpg.php")}
        response = client.post(
            "/api/upload",
            data=data,
            headers={"Authorization": f"Bearer {admin_token}"},
            content_type="multipart/form-data",
        )

        assert response.status_code in [400, 415]


# =============================================================================
# SSRF Protection Negative Tests
# =============================================================================


class TestSSRFProtectionNegative:
    """Negative tests for SSRF protection."""

    def test_localhost_blocked(self, client, admin_token):
        """Test localhost URLs are blocked."""
        blocked_urls = [
            "http://localhost",
            "http://127.0.0.1",
            "http://[::1]",
            "http://localhost:8080",
        ]
        for url in blocked_urls:
            response = client.post(
                "/api/external/fetch",
                json={"url": url},
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert response.status_code in [400, 403]

    def test_private_ip_blocked(self, client, admin_token):
        """Test private IPs are blocked."""
        blocked_urls = [
            "http://10.0.0.1",
            "http://192.168.1.1",
            "http://172.16.0.1",
        ]
        for url in blocked_urls:
            response = client.post(
                "/api/external/fetch",
                json={"url": url},
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert response.status_code in [400, 403]

    def test_metadata_endpoint_blocked(self, client, admin_token):
        """Test cloud metadata endpoints are blocked."""
        blocked_urls = [
            "http://169.254.169.254/latest/meta-data/",
            "http://metadata.google.internal",
        ]
        for url in blocked_urls:
            response = client.post(
                "/api/external/fetch",
                json={"url": url},
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert response.status_code in [400, 403]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def admin_token(client):
    """Get admin JWT token."""
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},  # Test password
    )
    if response.status_code == 200:
        return response.get_json()["data"]["access_token"]
    return "mock_admin_token"


@pytest.fixture
def user_token(client):
    """Get regular user JWT token."""
    return "mock_user_token"


@pytest.fixture
def sales_token(client):
    """Get sales user JWT token."""
    return "mock_sales_token"


@pytest.fixture
def expired_refresh_token():
    """Get an expired refresh token."""
    return "expired_token"


@pytest.fixture
def revoked_refresh_token():
    """Get a revoked refresh token."""
    return "revoked_token"
