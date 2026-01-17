# -*- coding: utf-8 -*-
"""
Focused tests for src.jwt_manager

Goals:
- Cover secret key resolution paths
- Exercise access token creation and verification

These tests avoid DB-dependent refresh token flows.
"""

import os
import time
import pytest
from flask import Flask

from src.jwt_manager import JWTManager
import hashlib
from datetime import datetime, timedelta, timezone


@pytest.fixture()
def app_jwt():
    app = Flask(__name__)
    app.config.update(TESTING=True, JWT_SECRET_KEY="test-jwt-secret")
    return app


def test_get_secret_key_prefers_app_config(app_jwt, monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "env-secret-should-not-win")
    with app_jwt.app_context():
        secret = JWTManager.get_secret_key()
        assert secret == "test-jwt-secret"


def test_get_secret_key_env_no_app(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.setenv("JWT_SECRET_KEY", "env-jwt-secret")
    # No app context
    secret = JWTManager.get_secret_key()
    assert secret == "env-jwt-secret"


def test_get_secret_key_dev_fallback_no_env_no_app(monkeypatch):
    # Ensure not production, and no env set
    monkeypatch.delenv("FLASK_ENV", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    secret = JWTManager.get_secret_key()
    assert isinstance(secret, str)
    assert secret == "dev-secret-key-change-in-production"


def test_get_secret_key_prod_requires_secret(monkeypatch):
    # In production, secret must be provided
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    with pytest.raises(ValueError):
        _ = JWTManager.get_secret_key()
    # Cleanup
    monkeypatch.delenv("FLASK_ENV", raising=False)


def test_create_and_verify_access_token(app_jwt):
    with app_jwt.app_context():
        token = JWTManager.create_access_token(
            user_id=123, additional_claims={"role": "مدير النظام", "username": "admin"}
        )
        assert isinstance(token, str)
        # Allow iat/nbf clock
        time.sleep(0.05)
        payload = JWTManager.verify_access_token(token)
        assert payload is not None
        assert payload.get("type") == JWTManager.TOKEN_TYPE_ACCESS
        assert payload.get("user_id") == 123
        assert payload.get("role") == "مدير النظام"


import jwt
from flask import request


def test_decode_token_invalid_signature_returns_none(app_jwt):
    with app_jwt.app_context():
        token = JWTManager.create_access_token(
            user_id=1, additional_claims={"username": "u"}
        )
        # Change secret so signature becomes invalid at verification time
        app_jwt.config["JWT_SECRET_KEY"] = "another-secret"
        assert JWTManager.decode_token(token) is None


def test_decode_token_expired_returns_none(app_jwt):
    with app_jwt.app_context():
        now = datetime.now(timezone.utc)
        expired = now - timedelta(seconds=1)
        payload = {
            "user_id": 1,
            "type": JWTManager.TOKEN_TYPE_ACCESS,
            "iat": now,
            "nbf": now,
            "exp": expired,
        }
        token = jwt.encode(payload, app_jwt.config["JWT_SECRET_KEY"], algorithm="HS256")
        assert JWTManager.decode_token(token) is None


def test_decode_token_no_verify_returns_payload_even_if_sig_invalid(app_jwt):
    with app_jwt.app_context():
        # Create token with different secret
        payload = {"user_id": 2, "type": JWTManager.TOKEN_TYPE_ACCESS}
        token = jwt.encode(payload, "other-secret", algorithm="HS256")
        out = JWTManager.decode_token(token, verify=False)
        assert out is not None and out.get("user_id") == 2


def test_verify_access_token_wrong_type_returns_none(app_jwt):
    with app_jwt.app_context():
        refresh_token, _, _ = JWTManager.create_refresh_token(user_id=9)
        time.sleep(0.05)
        assert JWTManager.verify_access_token(refresh_token) is None


def test_verify_refresh_token_type_mismatch_returns_none(app_jwt):
    with app_jwt.app_context():
        access_token = JWTManager.create_access_token(user_id=9)
        time.sleep(0.05)
        assert JWTManager.verify_refresh_token(access_token) is None


def test_get_client_info_parses_headers(app_jwt):
    with app_jwt.test_request_context(
        "/path",
        headers={"User-Agent": "UA/1.0"},
        environ_base={"REMOTE_ADDR": "1.2.3.4"},
    ):
        info = JWTManager.get_client_info()
        assert info["ip_address"] == "1.2.3.4"
        assert info["user_agent"].startswith("UA/")
        assert isinstance(info["device_fingerprint"], str)


def test_hash_and_jti():
    t1 = JWTManager.generate_jti()
    t2 = JWTManager.generate_jti()
    assert t1 != t2
    h = JWTManager.hash_token("abc")
    # sha256('abc')
    assert h == hashlib.sha256("abc".encode("utf-8")).hexdigest()


def test_access_refresh_raise_when_pyjwt_missing(monkeypatch, app_jwt):
    import src.jwt_manager as jm

    with app_jwt.app_context():
        monkeypatch.setattr(jm, "JWT_AVAILABLE", False, raising=False)
        monkeypatch.setattr(jm, "jwt", None, raising=False)
        with pytest.raises(RuntimeError):
            jm.JWTManager.create_access_token(1)
        with pytest.raises(RuntimeError):
            jm.JWTManager.create_refresh_token(1)


def test_import_without_pyjwt_sets_flag(monkeypatch):
    import builtins, importlib, sys

    orig_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "jwt":
            raise ImportError
        return orig_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    sys.modules.pop("src.jwt_manager", None)
    jm = importlib.import_module("src.jwt_manager")
    assert jm.JWT_AVAILABLE is False
    assert jm.jwt is None


def test_verify_refresh_token_db_paths_updates_and_commits(app_jwt, monkeypatch):
    import sys, types, jwt as jwt_lib

    # Prepare dummy DB modules
    rt_store = {}

    class DummyRT:
        def __init__(self, valid=True):
            self._valid = valid
            self.updated = False

        def is_valid(self):
            return self._valid

        def update_last_used(self):
            self.updated = True

    class DummyRTModel:
        @staticmethod
        def find_by_jti(jti):
            return rt_store.get(jti)

    class DummyDB:
        class session:
            committed = False

            @staticmethod
            def commit():
                DummyDB.session.committed = True

    # Inject dummy modules
    monkeypatch.setitem(sys.modules, "models", types.ModuleType("models"))
    monkeypatch.setitem(
        sys.modules,
        "models.refresh_token",
        types.SimpleNamespace(RefreshToken=DummyRTModel),
    )
    monkeypatch.setitem(sys.modules, "models.user", types.SimpleNamespace(db=DummyDB))

    import src.jwt_manager as jm

    # Ensure jwt is available for this test (previous test may have set flag False)
    monkeypatch.setattr(jm, "JWT_AVAILABLE", True, raising=False)
    monkeypatch.setattr(jm, "jwt", jwt_lib, raising=False)
    with app_jwt.app_context():
        now = datetime.now(timezone.utc)
        jti = "jti-1"
        rt_store[jti] = DummyRT(valid=True)
        payload = {
            "user_id": 1,
            "type": jm.JWTManager.TOKEN_TYPE_REFRESH,
            "jti": jti,
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=5),
        }
        token = jwt_lib.encode(
            payload, app_jwt.config["JWT_SECRET_KEY"], algorithm="HS256"
        )
        out = jm.JWTManager.verify_refresh_token(token)
        assert out is not None and out.get("jti") == jti
        assert rt_store[jti].updated is True
        assert DummyDB.session.committed is True


def test_create_token_pair_stores_refresh_token_and_commits(app_jwt, monkeypatch):
    import sys, types

    # Dummy models
    created = {}

    class DummyRTModel:
        @staticmethod
        def create_token(**kwargs):
            created.update(kwargs)

    class DummyDB:
        class session:
            committed = False

            @staticmethod
            def commit():
                DummyDB.session.committed = True

    monkeypatch.setitem(sys.modules, "models", types.ModuleType("models"))
    monkeypatch.setitem(
        sys.modules,
        "models.refresh_token",
        types.SimpleNamespace(RefreshToken=DummyRTModel),
    )
    monkeypatch.setitem(sys.modules, "models.user", types.SimpleNamespace(db=DummyDB))

    import src.jwt_manager as jm

    # Ensure jwt is available
    monkeypatch.setattr(jm, "JWT_AVAILABLE", True, raising=False)
    import jwt as jwt_lib

    monkeypatch.setattr(jm, "jwt", jwt_lib, raising=False)
    # Ensure we have a request context so get_client_info can access request
    with app_jwt.test_request_context(
        "/x", headers={"User-Agent": "UA/1.0"}, environ_base={"REMOTE_ADDR": "2.2.2.2"}
    ):
        with app_jwt.app_context():
            res = jm.create_token_pair(42, {"role": "مدير النظام"})
            assert isinstance(res.get("access_token"), str)
            assert isinstance(res.get("refresh_token"), str)
            assert res.get("token_type") == "Bearer"
            assert created.get("user_id") == 42
            assert (
                "jti" in created and "token_hash" in created and "expires_at" in created
            )
            assert created.get("ip_address") == "2.2.2.2"
            assert DummyDB.session.committed is True
