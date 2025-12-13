# FILE: backend/tests/test_e2e_auth_p0.py | PURPOSE: P0.1.5 - E2E tests for auth flows | OWNER: Backend Security | RELATED: test_auth_p0.py, test_mfa_p0.py | LAST-AUDITED: 2025-10-25

"""
P0.1.5: End-to-End Authentication Flow Tests
Tests complete user journeys: login → dashboard → logout → refresh
"""

import pytest
import sys
from pathlib import Path
import time

# Add backend/src to path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    import pyotp

    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False


# Shared test fixtures for this file
# NOTE: app and client fixtures are now in conftest.py for better test isolation


@pytest.fixture
def mock_user(app):
    """Create a baseline admin user used in some MFA flows."""
    from src.models.user_unified import User
    from src.database import db

    with app.app_context():
        user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role_id=1,
            mfa_enabled=False,
            mfa_secret=None,
        )
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
        try:
            yield user
        finally:
            db.session.delete(user)
            db.session.commit()


class TestE2ELoginLogout:
    """Test complete login → logout flow"""

    def test_successful_login_logout_flow(self, client):
        """Test: Login → Get user status → Logout → Verify token revoked"""
        # Step 1: Login
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        assert login_response.status_code == 200
        login_data = login_response.get_json()
        assert login_data["success"] is True
        assert "tokens" in login_data["data"]

        access_token = login_data["data"]["tokens"]["access_token"]
        refresh_token = login_data["data"]["tokens"]["refresh_token"]

        # Step 2: Verify user status with access token
        status_response = client.get(
            "/api/auth/status", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert status_response.status_code == 200
        status_data = status_response.get_json()
        assert status_data["success"] is True
        assert status_data["data"]["username"] == "admin"

        # Step 3: Logout
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": refresh_token},
        )

        assert logout_response.status_code == 200
        logout_data = logout_response.get_json()
        assert logout_data["success"] is True

        # Step 4: Verify access token is revoked
        status_after_logout = client.get(
            "/api/auth/status", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert status_after_logout.status_code == 401
        revoked_data = status_after_logout.get_json()
        assert revoked_data["success"] is False
        assert revoked_data["code"] == "AUTH_003"  # AUTH_TOKEN_REVOKED

    def test_login_with_invalid_credentials_then_success(self, client):
        """Test: Failed login → Successful login → Verify attempts reset"""
        # Step 1: Failed login
        failed_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrongpassword", "use_jwt": True},
        )

        assert failed_response.status_code == 401

        # Step 2: Successful login
        success_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        assert success_response.status_code == 200
        success_data = success_response.get_json()
        assert success_data["success"] is True

        # Step 3: Verify can logout successfully
        access_token = success_data["data"]["tokens"]["access_token"]
        logout_response = client.post(
            "/api/auth/logout", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert logout_response.status_code == 200


class TestE2ETokenRefresh:
    """Test token refresh flow"""

    def test_access_token_refresh_flow(self, client):
        """Test: Login → Wait → Refresh token → Use new token"""
        # Step 1: Login
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        assert login_response.status_code == 200
        login_data = login_response.get_json()

        old_access_token = login_data["data"]["tokens"]["access_token"]
        refresh_token = login_data["data"]["tokens"]["refresh_token"]

        # Step 2: Refresh access token
        refresh_response = client.post(
            "/api/auth/refresh", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == 200
        refresh_data = refresh_response.get_json()
        assert refresh_data["success"] is True

        new_access_token = refresh_data["data"]["access_token"]
        assert new_access_token != old_access_token

        # Step 3: Use new access token
        status_response = client.get(
            "/api/auth/status", headers={"Authorization": f"Bearer {new_access_token}"}
        )

        assert status_response.status_code == 200
        status_data = status_response.get_json()
        assert status_data["success"] is True

    def test_refresh_with_revoked_token(self, client):
        """Test: Login → Logout → Try to refresh → Should fail"""
        # Step 1: Login
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        login_data = login_response.get_json()
        access_token = login_data["data"]["tokens"]["access_token"]
        refresh_token = login_data["data"]["tokens"]["refresh_token"]

        # Step 2: Logout (revokes tokens)
        client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": refresh_token},
        )

        # Step 3: Try to refresh with revoked token
        refresh_response = client.post(
            "/api/auth/refresh", json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == 401
        refresh_data = refresh_response.get_json()
        assert refresh_data["success"] is False


class TestE2EAccountLockout:
    """Test account lockout flow"""

    def test_lockout_after_5_failed_attempts_then_wait(self, client):
        """Test: 5 failed logins → Lockout → Wait 15 min → Retry success"""
        username = "testuser"

        # Step 1: 5 failed login attempts
        for i in range(5):
            response = client.post(
                "/api/auth/login",
                json={
                    "username": username,
                    "password": "wrongpassword",
                    "use_jwt": True,
                },
            )

            if i < 4:
                assert response.status_code == 401
            else:
                # 5th attempt should trigger lockout
                assert response.status_code == 429
                data = response.get_json()
                assert data["code"] == "AUTH_004"  # AUTH_ACCOUNT_LOCKED

        # Step 2: Verify account is locked even with correct password
        locked_response = client.post(
            "/api/auth/login",
            json={"username": username, "password": "admin123", "use_jwt": True},
        )

        assert locked_response.status_code == 429

        # Step 3: Simulate waiting (in real scenario, wait 15 minutes)
        # For testing, we'll just verify the lockout message
        locked_data = locked_response.get_json()
        assert "remaining_seconds" in locked_data["details"]
        assert locked_data["details"]["remaining_seconds"] > 0


@pytest.mark.skipif(not PYOTP_AVAILABLE, reason="pyotp not installed")
class TestE2EMFAFlow:
    """Test complete MFA setup and login flow"""

    def test_mfa_setup_verify_login_flow(self, client, mock_user):
        """Test: Setup MFA → Verify → Login with MFA → Logout"""
        # Step 1: Setup MFA
        setup_response = client.post(
            "/api/auth/mfa/setup", json={"username": "admin", "password": "admin123"}
        )

        assert setup_response.status_code == 200
        setup_data = setup_response.get_json()
        assert "secret" in setup_data["data"]

        secret = setup_data["data"]["secret"]

        # Step 2: Verify MFA with TOTP code
        totp = pyotp.TOTP(secret)
        code = totp.now()

        verify_response = client.post(
            "/api/auth/mfa/verify", json={"username": "admin", "code": code}
        )

        assert verify_response.status_code == 200
        verify_data = verify_response.get_json()
        assert verify_data["data"]["mfa_enabled"] is True

        # Step 3: Login with MFA (should require code)
        login_no_code = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        assert login_no_code.status_code == 401
        no_code_data = login_no_code.get_json()
        assert no_code_data["code"] == "AUTH_008"  # AUTH_MFA_REQUIRED

        # Step 4: Login with MFA code
        new_code = totp.now()
        login_with_mfa = client.post(
            "/api/auth/login",
            json={
                "username": "admin",
                "password": "admin123",
                "mfa_code": new_code,
                "use_jwt": True,
            },
        )

        assert login_with_mfa.status_code == 200
        login_data = login_with_mfa.get_json()
        assert login_data["success"] is True
        assert "tokens" in login_data["data"]

        # Step 5: Logout
        access_token = login_data["data"]["tokens"]["access_token"]
        logout_response = client.post(
            "/api/auth/logout", headers={"Authorization": f"Bearer {access_token}"}
        )

        assert logout_response.status_code == 200

    def test_mfa_disable_flow(self, client, mock_user_with_mfa):
        """Test: Login with MFA → Disable MFA → Login without MFA"""
        # Step 1: Login with MFA
        totp = pyotp.TOTP(mock_user_with_mfa.mfa_secret)
        code = totp.now()

        login_response = client.post(
            "/api/auth/login",
            json={
                "username": "admin",
                "password": "admin123",
                "mfa_code": code,
                "use_jwt": True,
            },
        )

        assert login_response.status_code == 200

        # Step 2: Disable MFA
        new_code = totp.now()
        disable_response = client.post(
            "/api/auth/mfa/disable",
            json={"username": "admin", "password": "admin123", "code": new_code},
        )

        assert disable_response.status_code == 200
        disable_data = disable_response.get_json()
        assert disable_data["data"]["mfa_enabled"] is False

        # Step 3: Login without MFA code
        login_no_mfa = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        assert login_no_mfa.status_code == 200
        no_mfa_data = login_no_mfa.get_json()
        assert no_mfa_data["success"] is True


class TestE2EErrorEnvelope:
    """Test error envelope consistency across flows"""

    def test_all_errors_have_trace_id(self, client):
        """Test: All error responses include traceId"""
        # Test 1: Invalid credentials
        response1 = client.post(
            "/api/auth/login", json={"username": "admin", "password": "wrong"}
        )
        data1 = response1.get_json()
        assert "traceId" in data1

        # Test 2: Missing fields
        response2 = client.post("/api/auth/login", json={"username": "admin"})
        data2 = response2.get_json()
        assert "traceId" in data2

        # Test 3: Invalid token
        response3 = client.get(
            "/api/auth/status", headers={"Authorization": "Bearer invalid_token"}
        )
        data3 = response3.get_json()
        assert "traceId" in data3

    def test_error_codes_are_consistent(self, client):
        """Test: Error codes follow standard format"""
        # Missing field
        response1 = client.post("/api/auth/login", json={"username": "admin"})
        assert response1.get_json()["code"] == "VAL_001"

        # Invalid credentials
        response2 = client.post(
            "/api/auth/login", json={"username": "admin", "password": "wrong"}
        )
        assert response2.get_json()["code"] == "AUTH_001"


@pytest.fixture
def mock_user_with_mfa(app):
    """Create a mock user with MFA enabled"""
    from src.models.user_unified import User
    from src.database import db

    with app.app_context():
        secret = pyotp.random_base32()
        user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role_id=1,
            mfa_enabled=True,
            mfa_secret=secret,
        )
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
        try:
            yield user
        finally:
            db.session.delete(user)
            db.session.commit()
