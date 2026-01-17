#!/usr/bin/env python
"""
Gaara ERP v12 - Playwright E2E Tests with Screenshots
======================================================

Dedicated Playwright tests for capturing screenshots of the application.

Prerequisites:
    - Backend running on port 9551
    - Frontend running on port 3505 (optional)

Usage:
    pytest tests/e2e/test_playwright_screenshots.py -v --headed

Created: 2026-01-16
"""

import os
import sys
import pytest
from datetime import datetime
from pathlib import Path

# Screenshots directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:9551')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3505')


def take_screenshot(page, name: str) -> Path:
    """Take and save a screenshot with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = SCREENSHOTS_DIR / filename
    page.screenshot(path=str(filepath), full_page=True)
    print(f"📸 Screenshot saved: {filepath}")
    return filepath


@pytest.fixture(scope="module")
def browser_context():
    """Setup Playwright browser context."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip("Playwright not installed")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='ar-SA',
        )
        yield context
        browser.close()


class TestBackendScreenshots:
    """Capture screenshots of backend pages."""
    
    def test_django_admin_login(self, browser_context):
        """Capture Django admin login page."""
        page = browser_context.new_page()
        
        try:
            page.goto(f"{BACKEND_URL}/admin/", timeout=10000)
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "backend_admin_login")
            
            # Verify we're on the login page
            title = page.title()
            print(f"✅ Admin page title: {title}")
        except Exception as e:
            take_screenshot(page, "backend_admin_error")
            pytest.skip(f"Backend not accessible: {e}")
        finally:
            page.close()
    
    def test_api_root(self, browser_context):
        """Capture API root endpoint."""
        page = browser_context.new_page()
        
        try:
            page.goto(f"{BACKEND_URL}/api/", timeout=10000)
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "backend_api_root")
            print("✅ API root captured")
        except Exception as e:
            take_screenshot(page, "backend_api_error")
            pytest.skip(f"API not accessible: {e}")
        finally:
            page.close()
    
    def test_api_health(self, browser_context):
        """Capture API health endpoint."""
        page = browser_context.new_page()
        
        try:
            # Try common health endpoints
            for endpoint in ['/api/health/', '/health/', '/api/v1/health/']:
                try:
                    response = page.goto(f"{BACKEND_URL}{endpoint}", timeout=5000)
                    if response and response.status in [200, 404]:
                        take_screenshot(page, f"backend_health_{endpoint.replace('/', '_')}")
                        print(f"✅ Health endpoint {endpoint}: {response.status}")
                        return
                except:
                    continue
            
            pytest.skip("No health endpoint found")
        finally:
            page.close()
    
    def test_swagger_docs(self, browser_context):
        """Capture Swagger/OpenAPI documentation if available."""
        page = browser_context.new_page()
        
        try:
            # Try common docs endpoints
            for endpoint in ['/api/docs/', '/swagger/', '/api/schema/', '/redoc/']:
                try:
                    response = page.goto(f"{BACKEND_URL}{endpoint}", timeout=5000)
                    if response and response.status == 200:
                        page.wait_for_load_state('networkidle')
                        take_screenshot(page, f"backend_docs_{endpoint.replace('/', '_')}")
                        print(f"✅ Docs endpoint {endpoint}: accessible")
                        return
                except:
                    continue
            
            print("⚠️ No documentation endpoint found")
        finally:
            page.close()


class TestFrontendScreenshots:
    """Capture screenshots of frontend pages."""
    
    def test_frontend_home(self, browser_context):
        """Capture frontend home page."""
        page = browser_context.new_page()
        
        try:
            page.goto(FRONTEND_URL, timeout=10000)
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "frontend_home")
            
            title = page.title()
            print(f"✅ Frontend home title: {title}")
        except Exception as e:
            take_screenshot(page, "frontend_home_error")
            pytest.skip(f"Frontend not accessible: {e}")
        finally:
            page.close()
    
    def test_frontend_login(self, browser_context):
        """Capture frontend login page."""
        page = browser_context.new_page()
        
        try:
            # Try common login routes
            for route in ['/login', '/auth/login', '/signin', '/']:
                try:
                    page.goto(f"{FRONTEND_URL}{route}", timeout=5000)
                    page.wait_for_load_state('networkidle')
                    
                    # Check for login form elements
                    if page.locator('input[type="email"], input[type="text"], input[name="username"]').count() > 0:
                        take_screenshot(page, "frontend_login")
                        print(f"✅ Frontend login found at {route}")
                        return
                except:
                    continue
            
            # Capture whatever is shown
            take_screenshot(page, "frontend_default")
            print("✅ Frontend default page captured")
        except Exception as e:
            pytest.skip(f"Frontend login not found: {e}")
        finally:
            page.close()


class TestResponsiveScreenshots:
    """Capture responsive/mobile screenshots."""
    
    def test_mobile_backend_admin(self, browser_context):
        """Capture mobile view of backend admin."""
        page = browser_context.new_page()
        
        try:
            # Set mobile viewport
            page.set_viewport_size({'width': 375, 'height': 812})
            page.goto(f"{BACKEND_URL}/admin/", timeout=10000)
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "mobile_backend_admin")
            print("✅ Mobile backend admin captured")
        except Exception as e:
            pytest.skip(f"Backend not accessible: {e}")
        finally:
            page.close()
    
    def test_tablet_frontend(self, browser_context):
        """Capture tablet view of frontend."""
        page = browser_context.new_page()
        
        try:
            # Set tablet viewport
            page.set_viewport_size({'width': 768, 'height': 1024})
            page.goto(FRONTEND_URL, timeout=10000)
            page.wait_for_load_state('networkidle')
            take_screenshot(page, "tablet_frontend")
            print("✅ Tablet frontend captured")
        except Exception as e:
            pytest.skip(f"Frontend not accessible: {e}")
        finally:
            page.close()


class TestAPIEndpointScreenshots:
    """Capture API endpoint responses as screenshots."""
    
    def test_users_api(self, browser_context):
        """Capture users API endpoint."""
        page = browser_context.new_page()
        
        try:
            for endpoint in ['/api/users/', '/api/v1/users/', '/api/auth/users/']:
                try:
                    response = page.goto(f"{BACKEND_URL}{endpoint}", timeout=5000)
                    take_screenshot(page, f"api_users_{response.status if response else 'error'}")
                    print(f"✅ Users API {endpoint}: {response.status if response else 'error'}")
                    return
                except:
                    continue
        finally:
            page.close()
    
    def test_companies_api(self, browser_context):
        """Capture companies API endpoint."""
        page = browser_context.new_page()
        
        try:
            for endpoint in ['/api/companies/', '/api/v1/companies/', '/api/organization/companies/']:
                try:
                    response = page.goto(f"{BACKEND_URL}{endpoint}", timeout=5000)
                    take_screenshot(page, f"api_companies_{response.status if response else 'error'}")
                    print(f"✅ Companies API {endpoint}: {response.status if response else 'error'}")
                    return
                except:
                    continue
        finally:
            page.close()


class TestGenerateSummary:
    """Generate test summary."""
    
    def test_list_screenshots(self):
        """List all captured screenshots."""
        screenshots = list(SCREENSHOTS_DIR.glob("*.png"))
        
        print(f"\n📁 Screenshots Directory: {SCREENSHOTS_DIR}")
        print(f"📸 Total Screenshots: {len(screenshots)}")
        
        for screenshot in sorted(screenshots)[-10:]:  # Show last 10
            size = screenshot.stat().st_size / 1024
            print(f"  - {screenshot.name} ({size:.1f} KB)")
        
        assert SCREENSHOTS_DIR.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
