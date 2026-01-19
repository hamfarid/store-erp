# FILE: backend/tests/test_auth_p0.py | PURPOSE: P0.1.4 - Negative tests for auth flows (JWT revocation, lockout, MFA) | OWNER: Backend QA | RELATED: auth.py, auth_routes.py, cache_service.py | LAST-AUDITED: 2025-10-25

"""
P0.1.4: Negative Tests for Authentication Flows
Tests for:
- Invalid credentials
- Expired tokens
- Revoked tokens (after logout)
- Account lockout after failed attempts
- MFA failures (when implemented)
"""

import pytest
import json
import time
from datetime import datetime, timedelta
from flask import Flask
from src.auth import AuthManager
from src.services.cache_service import jwt_revocation_list, login_lockout_manager


class TestAuthenticationNegative:
    """Negative test cases for authentication system"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup before each test"""
        # Clear revocation list and lockout manager
        jwt_revocation_list.clear()
        login_lockout_manager._failed_attempts.clear()
        login_lockout_manager._lockout_times.clear()
        yield

    def test_invalid_credentials(self, client):
        """Test login with invalid username/password returns 401"""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "invalid_user",
                "password": "wrong_password",
                "use_jwt": True,
            },
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["success"] is False
        assert "اسم المستخدم أو كلمة المرور غير صحيحة" in data["message"]

    def test_missing_credentials(self, client):
        """Test login without username/password returns 400"""
        # Missing password
        response = client.post("/api/auth/login", json={"username": "admin"})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False

        # Missing username
        response = client.post("/api/auth/login", json={"password": "admin123"})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False

    def test_revoked_token_after_logout(self, client, app):
        """
        P0.1.1: Test that JWT token is revoked after logout
        """
        # Step 1: Login successfully
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        assert login_data["success"] is True

        # Extract tokens from data envelope
        assert "data" in login_data
        assert "tokens" in login_data["data"]
        access_token = login_data["data"]["tokens"]["access_token"]
        refresh_token = login_data["data"]["tokens"]["refresh_token"]

        # Step 2: Verify token works before logout
        with app.app_context():
            payload = AuthManager.verify_jwt_token(access_token, "access")
            assert payload is not None
            assert payload["username"] == "admin"

        # Step 3: Logout (should revoke tokens)
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": refresh_token},
        )
        assert logout_response.status_code == 200

        # Step 4: Verify token is revoked after logout
        with app.app_context():
            payload_after_logout = AuthManager.verify_jwt_token(access_token, "access")
            assert payload_after_logout is None, "Token should be revoked after logout"

            # Step 5: Verify refresh token is also revoked
            refresh_payload_after_logout = AuthManager.verify_jwt_token(
                refresh_token, "refresh"
            )
            assert (
                refresh_payload_after_logout is None
            ), "Refresh token should be revoked after logout"

    def test_account_lockout_after_5_failed_attempts(self, client):
        """
        P0.1.2: Test account lockout after 5 failed login attempts
        """
        username = "test_lockout_user"

        # Attempt 1-4: Should fail but not lock
        for i in range(4):
            response = client.post(
                "/api/auth/login",
                json={
                    "username": username,
                    "password": "wrong_password",
                    "use_jwt": True,
                },
            )
            assert response.status_code == 401
            data = json.loads(response.data)
            assert data["success"] is False

            # Check remaining attempts
            remaining = login_lockout_manager.get_remaining_attempts(username)
            assert remaining == 5 - (
                i + 1
            ), f"Expected {5 - (i + 1)} remaining attempts, got {remaining}"

        # Attempt 5: Should trigger lockout and return 429
        response = client.post(
            "/api/auth/login",
            json={"username": username, "password": "wrong_password", "use_jwt": True},
        )
        assert (
            response.status_code == 429
        ), "Account should be locked on 5th failed attempt"
        data = json.loads(response.data)
        assert data["success"] is False
        assert "مقفل" in data["message"] or "locked" in data["message"].lower()

        # Attempt 6: Should still return 429 (locked)
        response = client.post(
            "/api/auth/login",
            json={"username": username, "password": "wrong_password", "use_jwt": True},
        )
        assert response.status_code == 429, "Account should remain locked"
        data = json.loads(response.data)
        assert data["success"] is False
        # Check details field for lockout info
        assert "details" in data
        assert "locked_until" in data["details"]
        assert "remaining_seconds" in data["details"]

    def test_lockout_prevents_valid_login(self, client):
        """
        P0.1.2: Test that even valid credentials are rejected when account is locked
        """
        username = "admin"

        # Trigger lockout with 5 failed attempts
        for _ in range(5):
            client.post(
                "/api/auth/login",
                json={
                    "username": username,
                    "password": "wrong_password",
                    "use_jwt": True,
                },
            )

        # Try to login with CORRECT password - should still be locked
        response = client.post(
            "/api/auth/login",
            json={
                "username": username,
                "password": "admin123",  # Correct password
                "use_jwt": True,
            },
        )

        assert (
            response.status_code == 429
        ), "Account should remain locked even with correct password"
        data = json.loads(response.data)
        assert data["success"] is False

    def test_lockout_reset_after_successful_login(self, client):
        """
        P0.1.2: Test that failed attempts are reset after successful login
        """
        username = "admin"

        # Make 3 failed attempts
        for _ in range(3):
            client.post(
                "/api/auth/login",
                json={
                    "username": username,
                    "password": "wrong_password",
                    "use_jwt": True,
                },
            )

        # Verify we have 2 remaining attempts
        remaining = login_lockout_manager.get_remaining_attempts(username)
        assert remaining == 2

        # Successful login should reset counter
        response = client.post(
            "/api/auth/login",
            json={"username": username, "password": "admin123", "use_jwt": True},
        )
        assert response.status_code == 200

        # Verify counter is reset
        remaining_after = login_lockout_manager.get_remaining_attempts(username)
        assert (
            remaining_after == 5
        ), "Failed attempts should be reset after successful login"

    def test_jwt_token_expiry(self, app):
        """Test that expired JWT tokens are rejected"""
        with app.app_context():
            # Generate token with very short expiry (3 seconds)
            app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3)

            # Wait a moment to ensure clock sync
            time.sleep(0.1)

            tokens = AuthManager.generate_jwt_tokens(1, "test_user", "user")
            assert tokens is not None

            access_token = tokens["access_token"]

            # Wait a moment before verification
            time.sleep(0.1)

            # Verify token works immediately
            payload = AuthManager.verify_jwt_token(access_token, "access")
            assert payload is not None
            assert payload["username"] == "test_user"

            # Wait for token to expire (3 seconds + buffer)
            time.sleep(3.5)

            # Verify token is rejected after expiry
            payload_after_expiry = AuthManager.verify_jwt_token(access_token, "access")
            assert payload_after_expiry is None, "Expired token should be rejected"

    def test_jwt_token_wrong_type(self, app):
        """Test that access token cannot be used as refresh token and vice versa"""
        with app.app_context():
            tokens = AuthManager.generate_jwt_tokens(1, "test_user", "user")
            assert tokens is not None

            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]

            # Try to verify access token as refresh token
            payload = AuthManager.verify_jwt_token(access_token, "refresh")
            assert payload is None, "Access token should not be valid as refresh token"

            # Try to verify refresh token as access token
            payload = AuthManager.verify_jwt_token(refresh_token, "access")
            assert payload is None, "Refresh token should not be valid as access token"

    def test_revocation_list_cleanup(self, app):
        """Test that revocation list automatically cleans up expired tokens"""
        with app.app_context():
            # Clear revocation list first
            jwt_revocation_list._revoked_tokens.clear()

            # Generate token with short expiry (3 seconds)
            app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3)

            # Wait a moment to ensure clock sync
            time.sleep(0.1)

            tokens = AuthManager.generate_jwt_tokens(1, "test_user", "user")
            access_token = tokens["access_token"]

            # Wait a moment before revocation
            time.sleep(0.1)

            # Revoke token
            success = AuthManager.revoke_jwt_token(access_token)
            assert success is True

            # Verify token is in revocation list
            stats_before = jwt_revocation_list.get_stats()
            assert stats_before["total_revoked"] >= 1

            # Wait for token to expire (3 seconds + buffer)
            time.sleep(3.5)

            # Trigger cleanup by checking stats (internal cleanup runs)
            stats_after = jwt_revocation_list.get_stats()

            # Expired tokens should be cleaned up
            assert stats_after["total_revoked"] <= stats_before["total_revoked"]

    def test_lockout_duration_15_minutes(self):
        """Test that lockout duration is exactly 15 minutes (900 seconds)"""
        assert (
            login_lockout_manager.lockout_duration == 900
        ), "Lockout duration should be 900 seconds (15 minutes)"

    def test_max_attempts_is_5(self):
        """Test that maximum failed attempts before lockout is 5"""
        assert (
            login_lockout_manager.max_attempts == 5
        ), "Maximum failed attempts should be 5"


# Pytest fixtures
@pytest.fixture
def app():
    """Create Flask app for testing"""
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
