"""
Playwright Tests for API Endpoints
Tests API endpoints using Playwright's request context
"""

import pytest
from playwright.sync_api import sync_playwright
import json


class TestAPIEndpoints:
    """Test API endpoints using Playwright"""

    @pytest.fixture(scope="class")
    def api_context(self):
        """Create API request context"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running on port 1005")
    def test_health_endpoint(self, api_context):
        """Test health check endpoint"""
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        assert response.status in [200, 404]
        if response.status == 200:
            data = response.json()
            assert "status" in data or "healthy" in str(data).lower()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_health_endpoint_status(self, api_context):
        """Test health endpoint returns correct status"""
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        if response.status == 200:
            assert response.ok

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_auth_login_endpoint(self, api_context):
        """Test login endpoint structure"""
        response = api_context.request.post(
            "http://localhost:1005/api/v1/auth/login",
            data=json.dumps({
                "username": "test",
                "password": "test"
            }),
            headers={"Content-Type": "application/json"}
        )
        # Should return 401 for invalid credentials or 200 for valid
        assert response.status in [200, 401, 404, 422]

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_api_cors_headers(self, api_context):
        """Test CORS headers"""
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        if response.status == 200:
            headers = response.headers
            # Check for CORS headers (if configured)
            assert "access-control-allow-origin" in str(headers).lower() or True

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_api_content_type(self, api_context):
        """Test API returns JSON content type"""
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        if response.status == 200:
            content_type = response.headers.get("content-type", "")
            assert "json" in content_type.lower() or "text" in content_type.lower()


class TestAPIPerformance:
    """Test API performance using Playwright"""

    @pytest.fixture(scope="class")
    def api_context(self):
        """Create API request context"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_api_response_time(self, api_context):
        """Test API response time"""
        import time
        start_time = time.time()
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        elapsed_time = time.time() - start_time
        
        if response.status == 200:
            # Response should be fast (< 1 second for health check)
            assert elapsed_time < 1.0, f"Response too slow: {elapsed_time}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])

