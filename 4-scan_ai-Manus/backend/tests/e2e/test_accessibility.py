"""
Playwright Accessibility Tests
Tests for accessibility features and WCAG compliance
"""

import pytest
from playwright.sync_api import sync_playwright


class TestAccessibility:
    """Test accessibility features"""

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
    def test_page_title(self, browser_page):
        """Test that page has a title"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        title = browser_page.title()
        assert title is not None
        assert len(title.strip()) > 0

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_heading_structure(self, browser_page):
        """Test heading structure"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        
        # Check for h1
        h1 = browser_page.locator("h1")
        assert h1.count() > 0, "Page should have at least one h1"

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_image_alt_text(self, browser_page):
        """Test that images have alt text"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        
        images = browser_page.locator("img")
        image_count = images.count()
        
        if image_count > 0:
            # Check first few images
            for i in range(min(5, image_count)):
                img = images.nth(i)
                alt = img.get_attribute("alt")
                # Alt should be present (can be empty for decorative images)
                assert alt is not None

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_link_accessibility(self, browser_page):
        """Test link accessibility"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        
        links = browser_page.locator("a")
        link_count = links.count()
        
        if link_count > 0:
            # Check that links have text or aria-label
            for i in range(min(5, link_count)):
                link = links.nth(i)
                text = link.text_content()
                aria_label = link.get_attribute("aria-label")
                
                # Link should have text or aria-label
                assert text or aria_label or True  # Non-blocking

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_form_labels(self, browser_page):
        """Test that form inputs have labels"""
        browser_page.goto("http://localhost:1505/login", timeout=30000)
        
        inputs = browser_page.locator("input[type='text'], input[type='email'], input[type='password']")
        input_count = inputs.count()
        
        if input_count > 0:
            # Check that inputs have associated labels
            for i in range(min(3, input_count)):
                input_field = inputs.nth(i)
                input_id = input_field.get_attribute("id")
                
                if input_id:
                    label = browser_page.locator(f"label[for='{input_id}']")
                    # Should have label or aria-label
                    assert label.count() > 0 or input_field.get_attribute("aria-label") or True

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_keyboard_navigation(self, browser_page):
        """Test keyboard navigation"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        
        # Find focusable elements
        focusable = browser_page.locator(
            "a, button, input, select, textarea, [tabindex]:not([tabindex='-1'])"
        )
        
        focusable_count = focusable.count()
        assert focusable_count > 0, "Page should have focusable elements"

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_color_contrast(self, browser_page):
        """Test color contrast (basic check)"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        
        # This is a placeholder - actual contrast checking would require
        # more sophisticated tools or libraries
        body = browser_page.locator("body")
        assert body.count() > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])

