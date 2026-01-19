"""
Playwright Configuration for E2E Tests
"""

from playwright.sync_api import Playwright, sync_playwright
import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments"""
    return {
        **browser_type_launch_args,
        "headless": True,  # Run in headless mode
        "slow_mo": 100,  # Slow down operations for debugging
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ar-SA",  # Arabic locale
        "timezone_id": "Asia/Riyadh",
        "ignore_https_errors": True,
        "accept_downloads": True,
    }


@pytest.fixture(scope="session")
def base_url():
    """Base URL for testing"""
    import os
    return os.getenv("TEST_BASE_URL", "http://localhost:1505")


@pytest.fixture(scope="session")
def api_base_url():
    """API base URL for testing"""
    import os
    return os.getenv("TEST_API_URL", "http://localhost:1005")


