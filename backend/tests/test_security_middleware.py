# -*- coding: utf-8 -*-
"""
Unit Tests for Security Middleware
اختبارات الوحدة لوسيط الأمان

Tests for:
- require_role() decorator
- require_admin() decorator
- require_permission() decorator
- Unauthorized access handling
- Invalid token handling
- Expired token handling

Target: >= 80% coverage
"""

import pytest
from datetime import datetime, timedelta
from flask import Flask, jsonify
import jwt as jwt_lib
import sys
import types

import time

from src.security_middleware import (
    SecurityMiddleware,
    require_admin,
    require_permission,
    require_role,
)


class TestRequireRoleDecorator:
    """Test require_role() decorator"""

    def test_require_role_valid_token_correct_role(self, app, client):
        """Test access with valid token and correct role"""
        with app.app_context():
            # Create test route
            @app.route("/admin-only")
            @require_role("مدير النظام")
            def admin_route():
                return jsonify({"message": "Admin access granted"})

            # Manually create token with past iat to avoid clock skew
            now = datetime.utcnow()
            payload = {
                "user_id": 1,
                "username": "admin",
                "role": "مدير النظام",
                "type": "access",
                "iat": now - timedelta(seconds=5),
                "exp": now + timedelta(minutes=5),
            }
            token = jwt_lib.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Make request with token
            response = client.get(
                "/admin-only", headers={"Authorization": f"Bearer {token}"}
            )

            # Should succeed
            assert response.status_code == 200
            data = response.get_json()
            assert data["message"] == "Admin access granted"

    def test_require_role_valid_token_wrong_role(self, app, client):
        """Test access with valid token but wrong role"""
        import time

        with app.app_context():
            # Create test route
            @app.route("/admin-only-2")
            @require_role("مدير النظام")
            def admin_route():
                return jsonify({"message": "Admin access granted"})

            # Small delay
            time.sleep(1.1)

            # Create manual token with past iat
            now = datetime.utcnow()
            payload = {
                "user_id": 2,
                "username": "warehouse_manager",
                "role": "مدير المخزون",
                "type": "access",
                "iat": now - timedelta(seconds=5),
                "exp": now + timedelta(minutes=5),
            }
            token = jwt_lib.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Make request with token
            response = client.get(
                "/admin-only-2", headers={"Authorization": f"Bearer {token}"}
            )

            # Should be forbidden
            assert response.status_code == 403
            data = response.get_json()
            assert "error" in data
            assert data["user_role"] == "مدير المخزون"
            assert data["required_role"] == "مدير النظام"

    def test_require_role_no_token(self, app, client):
        """Test access without token"""
        with app.app_context():
            # Create test route
            @app.route("/admin-only-3")
            @require_role("مدير النظام")
            def admin_route():
                return jsonify({"message": "Admin access granted"})

            # Make request without token
            response = client.get("/admin-only-3")

            # Should be unauthorized
            assert response.status_code == 401
            data = response.get_json()
            assert "error" in data

    def test_require_role_invalid_token_format(self, app, client):
        """Test access with invalid token format"""
        with app.app_context():
            # Create test route
            @app.route("/admin-only-4")
            @require_role("مدير النظام")
            def admin_route():
                return jsonify({"message": "Admin access granted"})

            # Make request with invalid token format
            response = client.get(
                "/admin-only-4", headers={"Authorization": "InvalidFormat token123"}
            )

            # Should be unauthorized
            assert response.status_code == 401

    def test_require_role_expired_token(self, app, client):
        """Test access with expired token"""
        import time

        with app.app_context():
            # Create test route
            @app.route("/admin-only-5")
            @require_role("مدير النظام")
            def admin_route():
                return jsonify({"message": "Admin access granted"})

            # Create expired token
            now = datetime.now()
            expired_payload = {
                "user_id": 1,
                "username": "admin",
                "role": "مدير النظام",
                "type": "access",
                "iat": now,
                "exp": now + timedelta(seconds=1),
            }

            expired_token = jwt_lib.encode(
                expired_payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Wait for token to expire
            time.sleep(2)

            # Make request with expired token
            response = client.get(
                "/admin-only-5", headers={"Authorization": f"Bearer {expired_token}"}
            )

            # Should be unauthorized
            assert response.status_code == 401
            data = response.get_json()
            assert "error" in data

    def test_require_role_malformed_token(self, app, client):
        """Test access with malformed token"""
        with app.app_context():
            # Create test route
            @app.route("/admin-only-6")
            @require_role("مدير النظام")
            def admin_route():
                return jsonify({"message": "Admin access granted"})

            # Make request with malformed token
            response = client.get(
                "/admin-only-6", headers={"Authorization": "Bearer not.a.valid.jwt"}
            )

            # Should be unauthorized
            assert response.status_code == 401


class TestRequireAdminDecorator:
    """Test require_admin() decorator"""

    def test_require_admin_with_admin_role(self, app, client):
        """Test admin access with admin role"""
        import time

        with app.app_context():
            # Create test route
            @app.route("/admin-endpoint")
            @require_admin
            def admin_endpoint():
                return jsonify({"message": "Admin endpoint"})

            # Small delay
            time.sleep(1.1)
            # Manual admin token
            now = datetime.utcnow()
            payload = {
                "user_id": 1,
                "username": "admin",
                "role": "مدير النظام",
                "type": "access",
                "iat": now - timedelta(seconds=5),
                "exp": now + timedelta(minutes=5),
            }
            token = jwt_lib.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Make request
            response = client.get(
                "/admin-endpoint", headers={"Authorization": f"Bearer {token}"}
            )

            # Should succeed
            assert response.status_code == 200

    def test_require_admin_with_non_admin_role(self, app, client):
        """Test admin access with non-admin role"""
        import time

        with app.app_context():
            # Create test route
            @app.route("/admin-endpoint-2")
            @require_admin
            def admin_endpoint():
                return jsonify({"message": "Admin endpoint"})

            # Small delay
            time.sleep(1.1)

            # Manual non-admin token
            now = datetime.utcnow()
            payload = {
                "user_id": 2,
                "username": "user",
                "role": "مستخدم",
                "type": "access",
                "iat": now - timedelta(seconds=5),
                "exp": now + timedelta(minutes=5),
            }
            token = jwt_lib.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Make request
            response = client.get(
                "/admin-endpoint-2", headers={"Authorization": f"Bearer {token}"}
            )

            # Should be forbidden
            assert response.status_code == 403


class TestRequirePermissionDecorator:
    """Test require_permission() decorator"""

    def test_require_permission_with_permission(self, app, client):
        """Test access with required permission"""
        with app.app_context():
            # Create test route
            @app.route("/inventory-edit")
            @require_permission("edit_inventory")
            def edit_inventory():
                return jsonify({"message": "Inventory edit allowed"})

            # Generate token with permissions
            now = datetime.utcnow()
            payload = {
                "user_id": 1,
                "username": "manager",
                "role": "مدير المخزون",
                "permissions": ["edit_inventory", "view_inventory"],
                "type": "access",
                "iat": now - timedelta(seconds=5),
                "exp": now + timedelta(hours=1),
            }

            token = jwt_lib.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Make request
            response = client.get(
                "/inventory-edit", headers={"Authorization": f"Bearer {token}"}
            )

            # Should succeed
            assert response.status_code == 200

    def test_require_permission_without_permission(self, app, client):
        """Test access without required permission"""
        with app.app_context():
            # Create test route
            @app.route("/inventory-delete")
            @require_permission("delete_inventory")
            def delete_inventory():
                return jsonify({"message": "Inventory delete allowed"})

            # Generate token without delete permission
            now = datetime.utcnow()
            payload = {
                "user_id": 1,
                "username": "viewer",
                "role": "مستخدم",
                "permissions": ["view_inventory"],  # No delete permission
                "type": "access",
                "iat": now - timedelta(seconds=5),
                "exp": now + timedelta(hours=1),
            }

            token = jwt_lib.encode(
                payload, app.config["JWT_SECRET_KEY"], algorithm="HS256"
            )

            # Make request
            response = client.get(
                "/inventory-delete", headers={"Authorization": f"Bearer {token}"}
            )

            # Should be forbidden
            assert response.status_code == 403


# Fixtures


@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key-for-security-middleware"
    app.config["JWT_SECRET_KEY"] = "test-jwt-secret-for-security-middleware"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


# Additional tests: middleware (before/after request) and require_auth


@pytest.fixture()
def app_sec_mw():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        JWT_SECRET_KEY="sec-secret",
        RATE_LIMIT_REQUESTS=2,
        RATE_LIMIT_WINDOW=60,
        LOCKOUT_DURATION=60,
    )
    mw = SecurityMiddleware(app)
    app.config["SEC_MW"] = mw

    @app.route("/ping")
    def ping():
        return "pong"

    from src.security_middleware import require_auth as _require_auth

    @app.route("/secure")
    @_require_auth
    def secure():
        return "ok"

    return app


def _client_env(app, ip="127.0.0.1"):
    return app.test_client(), {"REMOTE_ADDR": ip}


def test_security_headers_added(app_sec_mw):
    c, env = _client_env(app_sec_mw)
    r = c.get("/ping", environ_overrides=env)
    assert r.status_code == 200
    for k in [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "Referrer-Policy",
    ]:
        assert k in r.headers


def test_rate_limit_third_request_429(app_sec_mw):
    c, env = _client_env(app_sec_mw, ip="9.9.9.9")
    assert c.get("/ping", environ_overrides=env).status_code == 200
    assert c.get("/ping", environ_overrides=env).status_code == 200
    r3 = c.get("/ping", environ_overrides=env)
    assert r3.status_code == 429


def test_blocked_ip_returns_429(app_sec_mw):
    c, env = _client_env(app_sec_mw, ip="8.8.8.8")
    app_sec_mw.config["SEC_MW"].block_ip("8.8.8.8", duration=60)
    r = c.get("/ping", environ_overrides=env)
    assert r.status_code == 429


def test_require_auth_decorator(app_sec_mw):
    c, env = _client_env(app_sec_mw, ip="7.7.7.7")
    assert c.get("/secure", environ_overrides=env).status_code == 401
    assert (
        c.get(
            "/secure", headers={"Authorization": "Bearer t"}, environ_overrides=env
        ).status_code
        == 200
    )


# Additional coverage for get_client_ip and error branches


def test_get_client_ip_from_x_forwarded_for(app_sec_mw):
    mw = app_sec_mw.config["SEC_MW"]
    with app_sec_mw.test_request_context(
        "/", headers={"X-Forwarded-For": "1.1.1.1, 2.2.2.2"}
    ):
        assert mw.get_client_ip() == "1.1.1.1"


def test_get_client_ip_from_x_real_ip(app_sec_mw):
    mw = app_sec_mw.config["SEC_MW"]
    with app_sec_mw.test_request_context("/", headers={"X-Real-IP": "3.3.3.3"}):
        assert mw.get_client_ip() == "3.3.3.3"


def test_log_failed_attempt_blocks_after_max(app_sec_mw):
    mw = app_sec_mw.config["SEC_MW"]
    app_sec_mw.config["MAX_LOGIN_ATTEMPTS"] = 2
    ip = "10.0.0.9"
    with app_sec_mw.app_context():
        assert mw.log_failed_attempt(ip) is False
        assert mw.log_failed_attempt(ip) is True
        assert mw.is_ip_blocked(ip) is True


def _make_token(app, claims):
    now = datetime.utcnow()
    payload = {
        "type": "access",
        "iat": now - timedelta(seconds=5),
        "exp": now + timedelta(minutes=5),
        **claims,
    }
    return jwt_lib.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")


def test_require_role_missing_role_claim_returns_403(app, client):
    with app.app_context():

        @app.route("/role-missing")
        @require_role("مدير النظام")
        def _r():
            return "ok"

        t = _make_token(app, {"user_id": 7, "username": "u"})  # no role
        r = client.get("/role-missing", headers={"Authorization": f"Bearer {t}"})
        assert r.status_code == 403
        assert "الدور" in r.get_json().get("error")


def test_require_role_expired_token_401(app, client):
    with app.app_context():

        @app.route("/role-expired")
        @require_role("مدير النظام")
        def _rx():
            return "ok"

        now = datetime.utcnow()
        expired = now - timedelta(seconds=1)
        payload = {
            "user_id": 1,
            "username": "a",
            "role": "مدير النظام",
            "type": "access",
            "iat": now - timedelta(seconds=5),
            "exp": expired,
        }
        t = jwt_lib.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")
        r = client.get("/role-expired", headers={"Authorization": f"Bearer {t}"})
        assert r.status_code == 401


def test_require_role_generic_exception_500(app, client, monkeypatch):
    with app.app_context():

        @app.route("/role-except")
        @require_role("مدير النظام")
        def _re():
            return "ok"

        # Patch jwt to raise generic Exception
        ESE = type("ESE", (Exception,), {})
        ITE = type("ITE", (Exception,), {})
        dummy = types.SimpleNamespace(
            decode=lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")),
            ExpiredSignatureError=ESE,
            InvalidTokenError=ITE,
        )
        monkeypatch.setitem(sys.modules, "jwt", dummy)
        t = _make_token(app, {"user_id": 1, "username": "a", "role": "مدير النظام"})
        r = client.get("/role-except", headers={"Authorization": f"Bearer {t}"})
        assert r.status_code == 500


def test_require_permission_expired_and_invalid(app, client):
    with app.app_context():

        @app.route("/perm-expired")
        @require_permission("edit_inventory")
        def _pe():
            return "ok"

        @app.route("/perm-invalid")
        @require_permission("edit_inventory")
        def _pi():
            return "ok"

        now = datetime.utcnow()
        expired = now - timedelta(seconds=1)
        payload_exp = {
            "user_id": 1,
            "username": "a",
            "role": "مستخدم",
            "permissions": ["edit_inventory"],
            "type": "access",
            "iat": now - timedelta(seconds=5),
            "exp": expired,
        }
        expired_token = jwt_lib.encode(
            payload_exp, app.config["JWT_SECRET_KEY"], algorithm="HS256"
        )

        r_exp = client.get(
            "/perm-expired", headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert r_exp.status_code == 401
        data = r_exp.get_json()
        assert isinstance(data, dict)
        assert "error" in data

        r_inv = client.get(
            "/perm-invalid", headers={"Authorization": "Bearer not-a-token"}
        )
        assert r_inv.status_code == 401
        data = r_inv.get_json()
        assert isinstance(data, dict)
        assert "error" in data


def test_is_ip_blocked_removes_expired(app_sec_mw):
    mw = app_sec_mw.config["SEC_MW"]
    ip = "6.6.6.6"
    mw.blocked_ips[ip] = datetime.now() - timedelta(seconds=1)
    assert mw.is_ip_blocked(ip) is False
    assert ip not in mw.blocked_ips


def test_check_rate_limit_cleans_old_entries(app_sec_mw):
    mw = app_sec_mw.config["SEC_MW"]
    with app_sec_mw.app_context():
        app_sec_mw.config["RATE_LIMIT_WINDOW"] = 60
        ip = "5.5.5.5"
        old = time.time() - 120
        mw.rate_limits[ip].append(old)
        assert mw.check_rate_limit(ip) is True
        # after call, oldest entries older than window should be popped and new appended
        assert all(t >= time.time() - 60 for t in mw.rate_limits[ip])


def test_log_failed_attempt_cleans_old_entries(app_sec_mw):
    mw = app_sec_mw.config["SEC_MW"]
    ip = "4.4.4.4"
    mw.failed_attempts[ip].append(time.time() - 4000)
    with app_sec_mw.app_context():
        assert mw.log_failed_attempt(ip) is False
        # old entry should be removed, leaving exactly 1 recent entry
        assert len(mw.failed_attempts[ip]) == 1


def test_require_permission_missing_header_401(app_sec_mw):
    app = app_sec_mw
    with app.app_context():

        @app.route("/perm-no-auth")
        @require_permission("edit_inventory")
        def _pna():
            return "ok"

        c = app.test_client()
        r = c.get("/perm-no-auth")
        assert r.status_code == 401


def test_require_permission_admin_short_circuit(app_sec_mw):
    app = app_sec_mw
    c = app.test_client()
    with app.app_context():

        @app.route("/perm-admin")
        @require_permission("edit_inventory")
        def _pa():
            return "allowed"

        now = datetime.utcnow()
        payload = {
            "user_id": 1,
            "username": "admin",
            "role": "مدير النظام",
            "type": "access",
            "iat": now - timedelta(seconds=5),
            "exp": now + timedelta(minutes=5),
        }
        t = jwt_lib.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")
        r = c.get("/perm-admin", headers={"Authorization": f"Bearer {t}"})
        assert r.status_code == 200
        assert r.get_data(as_text=True) == "allowed"


def test_require_permission_generic_exception_500(app_sec_mw, monkeypatch):
    app = app_sec_mw
    c = app.test_client()
    with app.app_context():

        @app.route("/perm-except")
        @require_permission("edit_inventory")
        def _pe():
            return "x"

        # Patch jwt to raise generic error
        ESE = type("ESE", (Exception,), {})
        ITE = type("ITE", (Exception,), {})
        dummy = types.SimpleNamespace(
            decode=lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")),
            ExpiredSignatureError=ESE,
            InvalidTokenError=ITE,
        )
        monkeypatch.setitem(sys.modules, "jwt", dummy)
        now = datetime.utcnow()
        payload = {
            "user_id": 1,
            "username": "u",
            "role": "مستخدم",
            "permissions": ["edit_inventory"],
            "type": "access",
            "iat": now - timedelta(seconds=5),
            "exp": now + timedelta(minutes=5),
        }
        t = jwt_lib.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")
        r = c.get("/perm-except", headers={"Authorization": f"Bearer {t}"})
        assert r.status_code == 500
