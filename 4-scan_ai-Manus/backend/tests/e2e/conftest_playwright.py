"""
Playwright-specific pytest fixtures
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def playwright():
    """Playwright instance"""
    p = sync_playwright().start()
    yield p
    p.stop()


@pytest.fixture(scope="session")
def browser(playwright):
    """Browser instance"""
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def browser_context(browser):
    """Browser context for each test"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ar-SA",
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """Page instance for each test"""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url():
    """Base URL for frontend"""
    import os
    return os.getenv("FRONTEND_URL", "http://localhost:1505")


@pytest.fixture(scope="session")
def api_url():
    """Base URL for API"""
    import os
    return os.getenv("API_URL", "http://localhost:1005")

