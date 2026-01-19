"""
FILE: backend/tests/integration/test_csrf_middleware.py | PURPOSE: CSRF middleware integration tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Integration Tests for CSRF Middleware

Tests for:
- CSRF token generation
- CSRF token validation
- Double-submit cookie pattern
- Token rotation
- Exempt paths

Version: 1.0.0
"""

import pytest
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add backend src to path
backend_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(backend_src))

try:
    from middleware.csrf_middleware import CSRFMiddleware
    CSRF_MIDDLEWARE_AVAILABLE = True
except ImportError:
    CSRF_MIDDLEWARE_AVAILABLE = False


# Skip if pytest-flask is conflicting with FastAPI
pytestmark = pytest.mark.skipif(
    not CSRF_MIDDLEWARE_AVAILABLE,
    reason="CSRF Middleware not available"
)


@pytest.fixture(scope="function")
def csrf_app():
    """Create test FastAPI app with CSRF middleware"""
    if not CSRF_MIDDLEWARE_AVAILABLE:
        pytest.skip("CSRF Middleware not available")

    test_app = FastAPI()

    # Add CSRF middleware
    test_app.add_middleware(
        CSRFMiddleware,
        secret_key="test-secret-key-for-csrf-protection",
        exempt_paths=["/api/auth/login", "/health"]
    )

    # Add test routes
    @test_app.get("/api/test")
    async def get_test():
        return {"message": "GET request"}

    @test_app.post("/api/test")
    async def post_test():
        return {"message": "POST request"}

    @test_app.get("/health")
    async def health():
        return {"status": "ok"}

    @test_app.post("/api/auth/login")
    async def login():
        return {"token": "test-token"}

    return test_app


@pytest.fixture(scope="function")
def csrf_client(csrf_app):
    """Create test client"""
    return TestClient(csrf_app)


class TestCSRFMiddleware:
    """Test CSRF middleware"""

    def test_get_request_sets_csrf_cookie(self, csrf_client):
        """Test that GET requests set CSRF cookie"""
        response = csrf_client.get("/api/test")

        assert response.status_code == 200
        assert "csrf_token" in response.cookies
        assert len(response.cookies["csrf_token"]) > 0

    def test_post_without_csrf_token_fails(self, csrf_client):
        """Test that POST without CSRF token fails"""
        response = csrf_client.post("/api/test")

        assert response.status_code == 403
        assert response.json()["code"] == "CSRF_TOKEN_MISSING"

    def test_post_with_valid_csrf_token_succeeds(self, csrf_client):
        """Test that POST with valid CSRF token succeeds"""
        # First, get CSRF token
        get_response = csrf_client.get("/api/test")
        csrf_token = get_response.cookies["csrf_token"]

        # Then, POST with token
        response = csrf_client.post(
            "/api/test",
            cookies={"csrf_token": csrf_token},
            headers={"X-CSRF-Token": csrf_token}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "POST request"

    def test_post_with_mismatched_tokens_fails(self, csrf_client):
        """Test that POST with mismatched tokens fails"""
        # Get CSRF token
        get_response = csrf_client.get("/api/test")
        csrf_token = get_response.cookies["csrf_token"]

        # POST with different header token
        response = csrf_client.post(
            "/api/test",
            cookies={"csrf_token": csrf_token},
            headers={"X-CSRF-Token": "different-token"}
        )

        assert response.status_code == 403
        assert response.json()["code"] == "CSRF_TOKEN_MISMATCH"

    def test_post_with_expired_token_fails(self, csrf_client):
        """Test that POST with expired token fails"""
        # Create an expired token (timestamp in the past)
        expired_token = "random.1000000000.signature"

        response = csrf_client.post(
            "/api/test",
            cookies={"csrf_token": expired_token},
            headers={"X-CSRF-Token": expired_token}
        )

        assert response.status_code == 403
        assert response.json()["code"] == "CSRF_TOKEN_INVALID"

    def test_exempt_path_does_not_require_csrf(self, csrf_client):
        """Test that exempt paths don't require CSRF token"""
        response = csrf_client.post("/api/auth/login")

        assert response.status_code == 200
        assert response.json()["token"] == "test-token"

    def test_health_endpoint_exempt(self, csrf_client):
        """Test that health endpoint is exempt"""
        response = csrf_client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_token_rotation_after_successful_request(self, csrf_client):
        """Test that token is rotated after successful request"""
        # Get initial token
        get_response = csrf_client.get("/api/test")
        initial_token = get_response.cookies["csrf_token"]

        # Make POST request
        post_response = csrf_client.post(
            "/api/test",
            cookies={"csrf_token": initial_token},
            headers={"X-CSRF-Token": initial_token}
        )

        # Check that new token is different
        new_token = post_response.cookies.get("csrf_token")
        assert new_token is not None
        assert new_token != initial_token

    def test_put_request_requires_csrf(self, csrf_client):
        """Test that PUT requests require CSRF token"""
        # Add PUT route
        response = csrf_client.put("/api/test")

        assert response.status_code == 403

    def test_delete_request_requires_csrf(self, csrf_client):
        """Test that DELETE requests require CSRF token"""
        response = csrf_client.delete("/api/test")

        assert response.status_code == 403

    def test_patch_request_requires_csrf(self, csrf_client):
        """Test that PATCH requests require CSRF token"""
        response = csrf_client.patch("/api/test")

        assert response.status_code == 403


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_all_state_changing_methods_require_csrf(csrf_client, method):
    """Parametrized test for all state-changing methods"""
    response = csrf_client.request(method, "/api/test")
    assert response.status_code == 403


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

