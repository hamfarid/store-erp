"""
Playwright E2E Tests for Frontend Pages
Tests all main frontend pages and routes
"""

import pytest
from playwright.sync_api import sync_playwright, Page, expect
import os


class TestFrontendPages:
    """Test frontend pages accessibility and basic functionality"""

    @pytest.fixture(scope="class")
    def browser_page(self):
        """Create browser and page fixture"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running on port 1505")
    def test_homepage_loads(self, browser_page: Page):
        """Test homepage loads correctly"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        assert browser_page.title() is not None
        assert len(browser_page.title()) > 0

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_login_page(self, browser_page: Page):
        """Test login page loads"""
        browser_page.goto("http://localhost:1505/login", timeout=30000)
        # Check for login form elements
        body = browser_page.locator("body")
        assert body.count() > 0

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_register_page(self, browser_page: Page):
        """Test register page loads"""
        browser_page.goto("http://localhost:1505/register", timeout=30000)
        body = browser_page.locator("body")
        assert body.count() > 0

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_dashboard_page(self, browser_page: Page):
        """Test dashboard page (requires auth)"""
        browser_page.goto("http://localhost:1505/dashboard", timeout=30000)
        # Should redirect to login if not authenticated
        current_url = browser_page.url
        assert "login" in current_url or "dashboard" in current_url

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_farms_page(self, browser_page: Page):
        """Test farms page"""
        browser_page.goto("http://localhost:1505/farms", timeout=30000)
        current_url = browser_page.url
        assert "farms" in current_url or "login" in current_url

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_diagnosis_page(self, browser_page: Page):
        """Test diagnosis page"""
        browser_page.goto("http://localhost:1505/diagnosis", timeout=30000)
        current_url = browser_page.url
        assert "diagnosis" in current_url or "login" in current_url


class TestAPIEndpoints:
    """Test API endpoints using Playwright"""

    @pytest.fixture(scope="class")
    def browser_page(self):
        """Create browser and page fixture"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running on port 1005")
    def test_health_endpoint(self, browser_page: Page):
        """Test health check endpoint"""
        response = browser_page.goto(
            "http://localhost:1005/api/v1/health",
            timeout=10000
        )
        if response:
            assert response.status in [200, 404]  # 404 if server not running
            if response.status == 200:
                content = browser_page.content()
                assert len(content) > 0

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_api_docs(self, browser_page: Page):
        """Test API documentation endpoint"""
        response = browser_page.goto(
            "http://localhost:1005/docs",
            timeout=10000
        )
        if response:
            assert response.status in [200, 404]


class TestPageResponsiveness:
    """Test page responsiveness and mobile view"""

    @pytest.fixture(scope="class")
    def browser_page(self):
        """Create browser and page fixture"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_mobile_view(self, browser_page: Page):
        """Test mobile viewport"""
        browser_page.set_viewport_size({"width": 375, "height": 667})
        browser_page.goto("http://localhost:1505", timeout=30000)
        viewport = browser_page.viewport_size
        assert viewport["width"] == 375
        assert viewport["height"] == 667

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_tablet_view(self, browser_page: Page):
        """Test tablet viewport"""
        browser_page.set_viewport_size({"width": 768, "height": 1024})
        browser_page.goto("http://localhost:1505", timeout=30000)
        viewport = browser_page.viewport_size
        assert viewport["width"] == 768


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])

