"""
Direct Playwright Tests - Using Playwright directly without pytest-playwright plugin
"""

import pytest
from playwright.sync_api import sync_playwright


class TestPlaywrightDirect:
    """Direct Playwright tests"""

    def test_playwright_basic_functionality(self):
        """Test basic Playwright functionality"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            assert "Example Domain" in page.title()
            browser.close()

    def test_playwright_navigation(self):
        """Test navigation"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            h1 = page.locator("h1")
            assert h1.text_content() == "Example Domain"
            browser.close()

    def test_playwright_screenshot(self):
        """Test screenshot capability"""
        import os
        screenshot_path = "test_screenshot_playwright.png"
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("https://example.com")
                page.screenshot(path=screenshot_path)
                assert os.path.exists(screenshot_path)
                browser.close()
        finally:
            # Cleanup
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)

    def test_playwright_network(self):
        """Test network interception"""
        responses = []

        def handle_response(response):
            responses.append(response.url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("response", handle_response)
            page.goto("https://example.com")
            page.wait_for_load_state("networkidle")
            browser.close()

        # Verify we got responses
        assert len(responses) > 0

    def test_playwright_console_logs(self):
        """Test console log capture"""
        console_messages = []

        def handle_console(msg):
            console_messages.append(msg.text)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.on("console", handle_console)
            page.goto("https://example.com")
            assert "Example Domain" in page.title()
            browser.close()

    @pytest.mark.skip(reason="Requires local server")
    def test_backend_health_check(self):
        """Test backend health endpoint"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:1005/api/v1/health")
            content = page.content()
            assert "healthy" in content.lower() or "status" in content.lower()
            browser.close()

    @pytest.mark.skip(reason="Requires local server")
    def test_frontend_loads(self):
        """Test frontend loads correctly"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:1505")
            assert "Gaara" in page.title() or "gaara" in page.title().lower()
            browser.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

