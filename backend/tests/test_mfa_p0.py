# FILE: backend/tests/test_mfa_p0.py | PURPOSE: P0.1.3 - MFA tests | OWNER: Backend Security | RELATED: routes/mfa_routes.py, test_auth_p0.py | LAST-AUDITED: 2025-10-25

"""
P0.1.3: MFA (Multi-Factor Authentication) Tests
Tests for TOTP-based MFA setup, verification, and disable
"""

import pytest
import sys
from pathlib import Path

# Add backend/src to path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    import pyotp

    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False


# Fixtures - Must be defined before test classes
# NOTE: app and client fixtures are now in conftest.py for better test isolation


@pytest.fixture
def mock_user(app):
    """Create a mock user without MFA"""
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
        yield user
        db.session.delete(user)
        db.session.commit()


@pytest.fixture
def mock_user_with_secret(app):
    """Create a mock user with MFA secret but not enabled"""
    from src.models.user_unified import User
    from src.database import db

    with app.app_context():
        secret = pyotp.random_base32()
        user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role_id=1,
            mfa_enabled=False,
            mfa_secret=secret,
        )
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()


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
        yield user
        db.session.delete(user)
        db.session.commit()


@pytest.mark.skipif(not PYOTP_AVAILABLE, reason="pyotp not installed")
class TestMFASetup:
    """Test MFA setup endpoint"""

    def test_mfa_setup_success(self, client, mock_user):
        """Test successful MFA setup"""
        response = client.post(
            "/api/auth/mfa/setup", json={"username": "admin", "password": "admin123"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "secret" in data["data"]
        assert "qr_code" in data["data"]
        assert "provisioning_uri" in data["data"]
        assert data["data"]["qr_code"].startswith("data:image/png;base64,")

    def test_mfa_setup_missing_credentials(self, client):
        """Test MFA setup with missing credentials"""
        response = client.post("/api/auth/mfa/setup", json={"username": "admin"})

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "VAL_001"  # VAL_MISSING_FIELD

    def test_mfa_setup_invalid_credentials(self, client):
        """Test MFA setup with invalid credentials"""
        response = client.post(
            "/api/auth/mfa/setup",
            json={"username": "admin", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "AUTH_001"  # AUTH_INVALID_CREDENTIALS

    def test_mfa_setup_already_enabled(self, client, mock_user_with_mfa):
        """Test MFA setup when already enabled"""
        response = client.post(
            "/api/auth/mfa/setup", json={"username": "admin", "password": "admin123"}
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "BIZ_002"  # BIZ_INVALID_OPERATION


@pytest.mark.skipif(not PYOTP_AVAILABLE, reason="pyotp not installed")
class TestMFAVerify:
    """Test MFA verification endpoint"""

    def test_mfa_verify_success(self, client, mock_user_with_secret):
        """Test successful MFA verification"""
        # Get current TOTP code
        totp = pyotp.TOTP(mock_user_with_secret.mfa_secret)
        code = totp.now()

        response = client.post(
            "/api/auth/mfa/verify", json={"username": "admin", "code": code}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["mfa_enabled"] is True

    def test_mfa_verify_invalid_code(self, client, mock_user_with_secret):
        """Test MFA verification with invalid code"""
        response = client.post(
            "/api/auth/mfa/verify",
            json={"username": "admin", "code": "000000"},  # Invalid code
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "AUTH_009"  # AUTH_INVALID_MFA_CODE

    def test_mfa_verify_missing_code(self, client, mock_user_with_secret):
        """Test MFA verification with missing code"""
        response = client.post("/api/auth/mfa/verify", json={"username": "admin"})

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "VAL_001"  # VAL_MISSING_FIELD

    def test_mfa_verify_no_secret(self, client, mock_user):
        """Test MFA verification when no secret exists"""
        response = client.post(
            "/api/auth/mfa/verify", json={"username": "admin", "code": "123456"}
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "BIZ_002"  # BIZ_INVALID_OPERATION


@pytest.mark.skipif(not PYOTP_AVAILABLE, reason="pyotp not installed")
class TestMFADisable:
    """Test MFA disable endpoint"""

    def test_mfa_disable_success(self, client, mock_user_with_mfa):
        """Test successful MFA disable"""
        # Get current TOTP code
        totp = pyotp.TOTP(mock_user_with_mfa.mfa_secret)
        code = totp.now()

        response = client.post(
            "/api/auth/mfa/disable",
            json={"username": "admin", "password": "admin123", "code": code},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["mfa_enabled"] is False

    def test_mfa_disable_invalid_password(self, client, mock_user_with_mfa):
        """Test MFA disable with invalid password"""
        totp = pyotp.TOTP(mock_user_with_mfa.mfa_secret)
        code = totp.now()

        response = client.post(
            "/api/auth/mfa/disable",
            json={"username": "admin", "password": "wrongpassword", "code": code},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "AUTH_001"  # AUTH_INVALID_CREDENTIALS

    def test_mfa_disable_invalid_code(self, client, mock_user_with_mfa):
        """Test MFA disable with invalid code"""
        response = client.post(
            "/api/auth/mfa/disable",
            json={"username": "admin", "password": "admin123", "code": "000000"},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "AUTH_009"  # AUTH_INVALID_MFA_CODE

    def test_mfa_disable_not_enabled(self, client, mock_user):
        """Test MFA disable when not enabled"""
        response = client.post(
            "/api/auth/mfa/disable",
            json={"username": "admin", "password": "admin123", "code": "123456"},
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "BIZ_002"  # BIZ_INVALID_OPERATION


@pytest.mark.skipif(not PYOTP_AVAILABLE, reason="pyotp not installed")
class TestLoginWithMFA:
    """Test login flow with MFA enabled"""

    def test_login_with_mfa_no_code(self, client, mock_user_with_mfa):
        """Test login with MFA enabled but no code provided"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123", "use_jwt": True},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "AUTH_008"  # AUTH_MFA_REQUIRED
        assert data["details"]["mfa_required"] is True

    def test_login_with_mfa_invalid_code(self, client, mock_user_with_mfa):
        """Test login with MFA enabled and invalid code"""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "admin",
                "password": "admin123",
                "mfa_code": "000000",
                "use_jwt": True,
            },
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["code"] == "AUTH_009"  # AUTH_INVALID_MFA_CODE

    def test_login_with_mfa_valid_code(self, client, mock_user_with_mfa):
        """Test successful login with MFA"""
        # Get current TOTP code
        totp = pyotp.TOTP(mock_user_with_mfa.mfa_secret)
        code = totp.now()

        response = client.post(
            "/api/auth/login",
            json={
                "username": "admin",
                "password": "admin123",
                "mfa_code": code,
                "use_jwt": True,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "tokens" in data["data"]
        assert "access_token" in data["data"]["tokens"]
