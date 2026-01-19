"""
Basic Playwright Tests - Test Playwright installation and basic functionality
"""

import pytest
from playwright.sync_api import Page, expect, sync_playwright


class TestPlaywrightBasic:
    """Basic Playwright functionality tests"""

    @pytest.mark.e2e
    def test_playwright_installation(self):
        """Test that Playwright is properly installed"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            expect(page).to_have_title("Example Domain")
            browser.close()

    @pytest.mark.e2e
    def test_playwright_navigation(self, page: Page):
        """Test basic navigation with Playwright"""
        page.goto("https://example.com")
        expect(page).to_have_title("Example Domain")
        expect(page.locator("h1")).to_contain_text("Example")

    @pytest.mark.e2e
    def test_playwright_screenshot(self, page: Page):
        """Test screenshot capability"""
        page.goto("https://example.com")
        screenshot = page.screenshot(path="test_screenshot.png")
        assert screenshot is not None

    @pytest.mark.e2e
    def test_playwright_network(self, page: Page):
        """Test network interception"""
        responses = []

        def handle_response(response):
            responses.append(response.url)

        page.on("response", handle_response)
        page.goto("https://example.com")

        # Wait for page to load
        page.wait_for_load_state("networkidle")

        # Verify we got responses
        assert len(responses) > 0

    @pytest.mark.e2e
    def test_playwright_console_logs(self, page: Page):
        """Test console log capture"""
        console_messages = []

        def handle_console(msg):
            console_messages.append(msg.text)

        page.on("console", handle_console)
        page.goto("https://example.com")

        # Check that page loaded (no errors)
        expect(page).to_have_title("Example Domain")


class TestLocalServer:
    """Tests for local development server"""

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires local server to be running")
    def test_backend_health_check(self, page: Page):
        """Test backend health endpoint"""
        page.goto("http://localhost:1005/api/v1/health")
        expect(page.locator("body")).to_contain_text("healthy")

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires local server to be running")
    def test_frontend_loads(self, page: Page):
        """Test frontend loads correctly"""
        page.goto("http://localhost:1505")
        expect(page).to_have_title(containing="Gaara")
        expect(page.locator("body")).to_be_visible()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])


