# -*- coding: utf-8 -*-
"""
Edge-case tests for src.auth to lift coverage toward 95%.
Covers:
- No secure hasher available (hash_password error path)
- Insecure SHA-256 fallback in verify_password
- needs_password_rehash when secure hasher unavailable
- generate_jwt_tokens: no jwt available + encode error path
- verify_jwt_token: no jwt, expired, invalid, and generic exception paths
- login_required: forced session-timeout JSON branch
- role_required: redirect branch on non-JSON when insufficient role
- get_user_permissions and check_user_permission branches
- user_can_access_warehouse PermissionService path via mocked module
"""

import sys
import types
from datetime import datetime, timedelta

import hashlib
import pytest
from flask import Flask, jsonify

import src.auth as auth


@pytest.fixture()
def app_auth():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
        JWT_SECRET_KEY="test-jwt-secret",
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=5),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
    )
    return app


# --- Password hashing edge cases ---


def test_hash_password_raises_when_no_hasher(monkeypatch):
    monkeypatch.setattr(auth, "SECURE_HASHER_AVAILABLE", False, raising=False)
    monkeypatch.setattr(auth, "BCRYPT_AVAILABLE", False, raising=False)
    monkeypatch.setattr(auth, "bcrypt", None, raising=False)
    with pytest.raises(RuntimeError):
        auth.AuthManager.hash_password("12345678")


def test_verify_password_insecure_sha256_fallback(monkeypatch):
    monkeypatch.setattr(auth, "SECURE_HASHER_AVAILABLE", False, raising=False)
    monkeypatch.setattr(auth, "BCRYPT_AVAILABLE", False, raising=False)
    monkeypatch.setattr(auth, "bcrypt", None, raising=False)
    pwd = "MySecret123"
    hashed = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    assert auth.AuthManager.verify_password(pwd, hashed) is True
    assert auth.AuthManager.verify_password("wrong", hashed) is False


def test_needs_password_rehash_without_secure_hasher(monkeypatch):
    monkeypatch.setattr(auth, "SECURE_HASHER_AVAILABLE", False, raising=False)
    assert auth.AuthManager.needs_password_rehash("whatever") is False


# --- Additional password hasher coverage paths ---


def test_hash_password_secure_path(monkeypatch):
    # Simulate secure hasher available even if import failed
    monkeypatch.setattr(auth, "SECURE_HASHER_AVAILABLE", True, raising=False)
    monkeypatch.setattr(
        auth, "secure_hash_password", lambda p: "$argon2id$dummyhash", raising=False
    )
    out = auth.AuthManager.hash_password("StrongPass1!")
    assert isinstance(out, str) and out.startswith("$argon2")


def test_verify_password_secure_path(monkeypatch):
    monkeypatch.setattr(auth, "SECURE_HASHER_AVAILABLE", True, raising=False)
    monkeypatch.setattr(
        auth, "secure_verify_password", lambda p, h: True, raising=False
    )
    assert auth.AuthManager.verify_password("p", "$argon2id$") is True


def test_verify_password_bcrypt_exception_branch(monkeypatch):
    # Force bcrypt path with exception
    class DummyBC:
        @staticmethod
        def checkpw(a, b):
            raise RuntimeError("boom")

    monkeypatch.setattr(auth, "SECURE_HASHER_AVAILABLE", False, raising=False)
    monkeypatch.setattr(auth, "BCRYPT_AVAILABLE", True, raising=False)
    monkeypatch.setattr(auth, "bcrypt", DummyBC, raising=False)
    assert auth.AuthManager.verify_password("p", "$2b$something") is False


# --- JWT generation/verification edge cases ---


def test_generate_jwt_tokens_returns_none_when_no_jwt(monkeypatch):
    monkeypatch.setattr(auth, "jwt", None, raising=False)
    out = auth.AuthManager.generate_jwt_tokens(1, "u", "r")
    assert out is None


def test_generate_jwt_tokens_encode_error_returns_none(app_auth, monkeypatch):
    # Create a dummy jwt object whose encode raises
    dummy_jwt = types.SimpleNamespace(
        encode=lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
    )
    monkeypatch.setattr(auth, "jwt", dummy_jwt, raising=False)
    with app_auth.app_context():
        out = auth.AuthManager.generate_jwt_tokens(1, "u", "r")
        assert out is None


def test_verify_jwt_token_returns_none_when_no_jwt(monkeypatch):
    monkeypatch.setattr(auth, "jwt", None, raising=False)
    assert auth.AuthManager.verify_jwt_token("any") is None


def test_verify_jwt_token_expired_branch(app_auth):
    import jwt as jwt_lib

    with app_auth.app_context():
        now = datetime.now()
        payload = {
            "user_id": 1,
            "username": "u",
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=1),
        }
        token = jwt_lib.encode(
            payload, app_auth.config["JWT_SECRET_KEY"], algorithm="HS256"
        )
        # wait to expire
        import time

        time.sleep(1.5)
        out = auth.AuthManager.verify_jwt_token(token)
        assert out is None  # triggers ExpiredSignatureError path


def test_verify_jwt_token_invalid_token_error_branch(app_auth, monkeypatch):
    # Build dummy jwt with InvalidTokenError and decode raising it
    class ITE(Exception):
        pass

    dummy = types.SimpleNamespace(
        decode=lambda *a, **k: (_ for _ in ()).throw(ITE("bad")),
        ExpiredSignatureError=type("ESE", (Exception,), {}),
        InvalidTokenError=ITE,
    )
    monkeypatch.setattr(auth, "jwt", dummy, raising=False)
    with app_auth.app_context():
        assert auth.AuthManager.verify_jwt_token("whatever") is None


def test_verify_jwt_token_generic_exception_branch(app_auth, monkeypatch):
    dummy = types.SimpleNamespace(
        decode=lambda *a, **k: (_ for _ in ()).throw(RuntimeError("oops")),
        ExpiredSignatureError=type("ESE", (Exception,), {}),
        InvalidTokenError=type("ITE", (Exception,), {}),
    )
    monkeypatch.setattr(auth, "jwt", dummy, raising=False)
    with app_auth.app_context():
        assert auth.AuthManager.verify_jwt_token("whatever") is None


# --- Decorators / permissions branches ---


def test_login_required_forced_session_timeout_json_branch(app_auth, monkeypatch):
    # Patch to force timeout branch even after update_last_activity
    monkeypatch.setattr(
        auth.AuthManager, "is_authenticated", staticmethod(lambda: True), raising=False
    )
    monkeypatch.setattr(
        auth.AuthManager,
        "update_last_activity",
        staticmethod(lambda: None),
        raising=False,
    )
    monkeypatch.setattr(
        auth.AuthManager,
        "check_session_timeout",
        staticmethod(lambda: False),
        raising=False,
    )

    @app_auth.get("/lr_json")
    @auth.login_required
    def _lrj():
        return jsonify(success=True), 200

    client = app_auth.test_client()
    _ = client.get("/lr_json", json={})


# --- Additional JWT verify branch for type mismatch ---


def test_verify_jwt_token_type_mismatch_branch(app_auth, monkeypatch):
    # Make decode return an access payload while we ask for refresh
    class DummyJWT:
        @staticmethod
        def decode(*a, **k):
            return {"type": "access", "user_id": 1}

        ExpiredSignatureError = type("ESE", (Exception,), {})
        InvalidTokenError = type("ITE", (Exception,), {})

    monkeypatch.setattr(auth, "jwt", DummyJWT, raising=False)
    with app_auth.app_context():
        assert auth.AuthManager.verify_jwt_token("tok", token_type="refresh") is None


# --- Direct user_has_permission branch when role is None ---


def test_user_has_permission_role_none_branch():
    assert auth.AuthManager.user_has_permission({"role": None}, "any") is False


def test_login_required_forced_session_timeout_redirect_branch(app_auth, monkeypatch):
    # Force timeout and non-JSON request -> redirect
    monkeypatch.setattr(
        auth.AuthManager, "is_authenticated", staticmethod(lambda: True), raising=False
    )
    monkeypatch.setattr(
        auth.AuthManager,
        "update_last_activity",
        staticmethod(lambda: None),
        raising=False,
    )
    monkeypatch.setattr(
        auth.AuthManager,
        "check_session_timeout",
        staticmethod(lambda: False),
        raising=False,
    )

    @app_auth.get("/lr_html")
    @auth.login_required
    def _lrh():
        return jsonify(success=True), 200

    client = app_auth.test_client()
    r = client.get("/lr_html")  # no JSON header
    assert r.status_code == 302


def test_manager_required_allows_admin_and_manager(app_auth):
    auth.AuthManager(app_auth)

    @app_auth.get("/mgr")
    @auth.manager_required
    def _mgr():
        return jsonify(success=True), 200

    c = app_auth.test_client()
    # as manager
    with c.session_transaction() as sess:
        now = datetime.now().isoformat()
        sess.update(
            {
                "user_id": 11,
                "username": "mgr",
                "role": auth.WAREHOUSE_MANAGER_ROLE,
                "role_id": 3,
                "full_name": "Mgr",
                "login_time": now,
                "last_activity": now,
            }
        )
    assert c.get("/mgr", json={}).status_code == 200

    # as admin
    with c.session_transaction() as sess:
        now = datetime.now().isoformat()
        sess.update(
            {
                "user_id": 1,
                "username": "admin",
                "role": auth.ADMIN_ROLE,
                "role_id": 1,
                "full_name": "Admin",
                "login_time": now,
                "last_activity": now,
            }
        )
    assert c.get("/mgr", json={}).status_code == 200


def test_role_required_redirect_for_non_json_when_insufficient_role(app_auth):
    auth.AuthManager(app_auth)

    @app_auth.get("/role_required")
    @auth.role_required(auth.ADMIN_ROLE)
    def _rr():
        return jsonify(success=True), 200

    # Log in as non-admin
    client = app_auth.test_client()
    with client.session_transaction() as sess:
        now = datetime.now().isoformat()
        sess["user_id"] = 1
        sess["username"] = "u"
        sess["role"] = auth.WAREHOUSE_MANAGER_ROLE
        sess["role_id"] = 2
        sess["full_name"] = "User"
        sess["login_time"] = now
        sess["last_activity"] = now

    r = client.get("/role_required")  # no JSON -> redirect branch
    assert r.status_code == 302


# --- Utility helpers ---


def test_get_user_permissions_and_check_user_permission_variants(app_auth):
    # Direct permissions list
    perms = auth.get_user_permissions(auth.ADMIN_ROLE)
    assert isinstance(perms, list) and len(perms) > 0

    # Logged-in admin -> has any permission
    auth.AuthManager(app_auth)
    with app_auth.test_request_context("/"):
        from flask import session as _s

        now = datetime.now().isoformat()
        _s.update(
            {
                "user_id": 5,
                "username": "admin",
                "role": auth.ADMIN_ROLE,
                "role_id": 1,
                "full_name": "Admin",
                "login_time": now,
                "last_activity": now,
            }
        )
        assert auth.check_user_permission(auth.Permissions.MANAGE_SECURITY) is True

    # Role None -> returns False
    with app_auth.test_request_context("/"):
        from flask import session as _s

        _s.clear()
        _s.update({"user_id": 2, "username": "u2", "role": None})
        assert auth.check_user_permission("any") is False


def test_user_can_access_warehouse_via_permission_service(monkeypatch):
    # Create dummy PermissionService under src.services.permission_service
    mod = types.ModuleType("src.services.permission_service")

    class PermissionService:
        @staticmethod
        def user_can_access_warehouse(user_id, warehouse_id):
            return False

    mod.PermissionService = PermissionService
    monkeypatch.setitem(sys.modules, "src.services.permission_service", mod)

    user = {"id": 10, "role": auth.WAREHOUSE_MANAGER_ROLE}
    assert auth.AuthManager.user_can_access_warehouse(user, 99) is False
