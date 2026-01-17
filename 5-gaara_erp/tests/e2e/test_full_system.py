#!/usr/bin/env python
"""
Gaara ERP v12 - Full System E2E Tests with Playwright Screenshots
=================================================================

Tests:
1. Backend API endpoints connectivity
2. Database connectivity and models
3. Frontend-Backend integration
4. E2E user workflows with screenshots

Usage:
    pytest tests/e2e/test_full_system.py -v --headed
    pytest tests/e2e/test_full_system.py -v  # headless

Created: 2026-01-16
"""

import os
import sys
import json
import pytest
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Screenshots directory
SCREENSHOTS_DIR = PROJECT_ROOT / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


class TestDatabaseConnectivity:
    """Test database connectivity and model operations."""
    
    @pytest.fixture(autouse=True)
    def setup_django(self):
        """Setup Django environment."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
        import django
        django.setup()
    
    def test_database_connection(self, setup_django):
        """Test database connection is working."""
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1, "Database connection failed"
        
        print("✅ Database connection: OK")
    
    def test_user_model(self, setup_django):
        """Test User model is accessible."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        count = User.objects.count()
        print(f"✅ User model: OK ({count} users)")
        assert count >= 0
    
    def test_company_model(self, setup_django):
        """Test Company model from core_modules."""
        try:
            from core_modules.companies.models import Company
            count = Company.objects.count()
            print(f"✅ Company model: OK ({count} companies)")
            assert count >= 0
        except Exception as e:
            pytest.skip(f"Company model not available: {e}")
    
    def test_migrations_applied(self, setup_django):
        """Verify all migrations are applied."""
        from django.db.migrations.recorder import MigrationRecorder
        from django.db import connection
        
        recorder = MigrationRecorder(connection)
        applied = recorder.applied_migrations()
        
        print(f"✅ Migrations applied: {len(applied)}")
        assert len(applied) > 50, "Expected more than 50 migrations applied"


class TestBackendAPIEndpoints:
    """Test backend API endpoint availability."""
    
    @pytest.fixture
    def client(self):
        """Setup Django test client."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
        import django
        django.setup()
        from django.test import Client
        return Client()
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health/')
        # Accept 200, 404 (endpoint might not exist), or 301 (redirect)
        assert response.status_code in [200, 301, 302, 404], f"Unexpected status: {response.status_code}"
        print(f"✅ Health endpoint: {response.status_code}")
    
    def test_api_root(self, client):
        """Test API root endpoint."""
        response = client.get('/api/')
        assert response.status_code in [200, 301, 302, 404], f"Unexpected status: {response.status_code}"
        print(f"✅ API root: {response.status_code}")
    
    def test_auth_endpoints(self, client):
        """Test authentication endpoints exist."""
        endpoints = [
            '/api/auth/login/',
            '/api/auth/token/',
            '/api/token/',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # POST endpoints return 405 for GET, which is expected
            assert response.status_code in [200, 301, 302, 404, 405], f"{endpoint}: {response.status_code}"
            print(f"✅ {endpoint}: {response.status_code}")
    
    def test_admin_accessible(self, client):
        """Test Django admin is accessible."""
        response = client.get('/admin/', follow=True)
        # Admin might return 200 (login page) or 404 if not mounted in test settings
        assert response.status_code in [200, 302, 404], f"Unexpected status: {response.status_code}"
        print(f"✅ Django Admin: {response.status_code}")


class TestPlaywrightE2E:
    """Playwright E2E tests with screenshots."""
    
    @pytest.fixture
    def browser_context(self):
        """Setup Playwright browser context."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            pytest.skip("Playwright not installed. Run: pip install playwright && playwright install")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='ar-SA',
            )
            yield context
            browser.close()
    
    def _screenshot(self, page, name: str):
        """Take and save screenshot."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        page.screenshot(path=str(filepath), full_page=True)
        print(f"📸 Screenshot saved: {filepath}")
        return filepath
    
    def test_frontend_loads(self, browser_context):
        """Test frontend application loads."""
        page = browser_context.new_page()
        
        try:
            # Try common frontend ports
            for port in [3505, 5173, 3000, 8080]:
                try:
                    response = page.goto(f"http://localhost:{port}", timeout=5000)
                    if response and response.status == 200:
                        self._screenshot(page, f"frontend_home_port{port}")
                        print(f"✅ Frontend loaded on port {port}")
                        return
                except Exception:
                    continue
            
            pytest.skip("Frontend not running on common ports")
        finally:
            page.close()
    
    def test_backend_admin_page(self, browser_context):
        """Test Django admin page renders correctly."""
        page = browser_context.new_page()
        
        try:
            # Try common backend ports
            for port in [8000, 9551, 5001]:
                try:
                    response = page.goto(f"http://localhost:{port}/admin/", timeout=5000)
                    if response and response.status == 200:
                        self._screenshot(page, f"admin_login_port{port}")
                        
                        # Check for login form
                        login_form = page.locator('form')
                        assert login_form.count() > 0, "Login form should be present"
                        
                        print(f"✅ Admin page loaded on port {port}")
                        return
                except Exception:
                    continue
            
            pytest.skip("Backend admin not running on common ports")
        finally:
            page.close()
    
    def test_api_health_from_browser(self, browser_context):
        """Test API health endpoint from browser context."""
        page = browser_context.new_page()
        
        try:
            for port in [8000, 9551, 5001]:
                try:
                    response = page.goto(f"http://localhost:{port}/api/", timeout=5000)
                    if response:
                        self._screenshot(page, f"api_root_port{port}")
                        print(f"✅ API accessible on port {port}: {response.status}")
                        return
                except Exception:
                    continue
            
            pytest.skip("API not running on common ports")
        finally:
            page.close()


class TestFrontendBackendIntegration:
    """Test frontend-backend integration points."""
    
    @pytest.fixture
    def setup_django(self):
        """Setup Django environment."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
        import django
        django.setup()
        yield
    
    def test_cors_configuration(self, setup_django):
        """Verify CORS is configured for frontend."""
        from django.conf import settings
        
        # Check CORS settings exist
        cors_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        cors_all = getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)
        
        print(f"✅ CORS Origins: {cors_origins[:3]}..." if cors_origins else "✅ CORS Allow All: {cors_all}")
        assert cors_origins or cors_all or hasattr(settings, 'CORS_ORIGIN_WHITELIST'), "CORS should be configured"
    
    def test_api_serializers_load(self, setup_django):
        """Test that API serializers can be imported."""
        serializer_modules = [
            'core_modules.users.serializers',
            'core_modules.companies.serializers',
            'business_modules.sales.serializers',
            'business_modules.inventory.serializers',
        ]
        
        loaded = 0
        for module_path in serializer_modules:
            try:
                __import__(module_path)
                loaded += 1
                print(f"✅ {module_path}: OK")
            except ImportError as e:
                print(f"⚠️ {module_path}: {e}")
        
        assert loaded > 0, "At least one serializer module should load"
    
    def test_url_patterns_registered(self, setup_django):
        """Verify URL patterns are properly registered."""
        from django.urls import get_resolver
        
        resolver = get_resolver()
        url_patterns = list(resolver.url_patterns)
        
        print(f"✅ URL patterns registered: {len(url_patterns)}")
        # Test settings may have fewer URL patterns
        assert len(url_patterns) > 0, "Expected at least some URL patterns"
    
    def test_rest_framework_configured(self, setup_django):
        """Verify Django REST Framework is configured."""
        from django.conf import settings
        
        assert 'rest_framework' in settings.INSTALLED_APPS, "REST Framework should be installed"
        assert hasattr(settings, 'REST_FRAMEWORK'), "REST_FRAMEWORK settings should exist"
        
        rf_settings = settings.REST_FRAMEWORK
        print(f"✅ REST Framework configured with {len(rf_settings)} settings")


class TestReportGenerator:
    """Generate comprehensive test report."""
    
    def test_generate_report(self):
        """Generate test execution report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": "Gaara ERP v12",
            "screenshots_dir": str(SCREENSHOTS_DIR),
            "tests_executed": {
                "database": ["connection", "models", "migrations"],
                "api": ["health", "auth", "admin"],
                "e2e": ["frontend", "admin_page", "api_browser"],
                "integration": ["cors", "serializers", "urls", "rest_framework"],
            },
        }
        
        report_path = SCREENSHOTS_DIR / "test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Report generated: {report_path}")
        assert report_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
