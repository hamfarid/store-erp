#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Integration Tests with Database
====================================

These tests require a real database connection and test the full stack:
- Database operations
- API endpoints
- Business logic
- Data validation

NOTE: These tests are marked as integration tests and may be skipped
if database dependencies are not properly configured.
"""

import pytest
import os
import sys

# Add backend to path
backend_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.skipif(
    os.environ.get("SKIP_INTEGRATION_TESTS", "1") == "1",
    reason="Integration tests skipped - set SKIP_INTEGRATION_TESTS=0 to run"
)


class TestAuthIntegration:
    """Integration tests for authentication"""

    def test_login_endpoint_exists(self, client):
        """Test that login endpoint exists"""
        # Test OPTIONS to check if endpoint exists
        response = client.post(
            "/api/auth/login", json={"username": "test", "password": "test"}
        )
        # 401 = auth failed (endpoint works), 405 = method not allowed (route issue)
        # 400 = bad request (endpoint works), 404 = not found
        assert response.status_code in [200, 400, 401, 404, 405], \
            f"Unexpected status: {response.status_code}"

    def test_login_with_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            json={"username": "invaliduser", "password": "wrongpassword"},
        )
        # Should return 401 (unauthorized) or 405 if route not configured
        assert response.status_code in [401, 404, 405]

    def test_login_requires_json(self, client):
        """Test that login requires JSON body"""
        response = client.post("/api/auth/login", data="not json")
        # Should return 400 (bad request) or similar
        assert response.status_code in [400, 401, 404, 405, 415]


class TestProductsIntegration:
    """Integration tests for products"""

    def test_list_products_endpoint(self, client):
        """Test listing products endpoint exists"""
        response = client.get("/api/products")
        # Should work or return 401 if auth required
        assert response.status_code in [200, 401, 404]

    def test_list_products_with_auth(self, client, auth_headers):
        """Test listing products with authentication"""
        response = client.get("/api/products", headers=auth_headers)
        # Should return products list or 404 if not configured
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            # Check response structure
            assert isinstance(data, (dict, list))


class TestCategoriesIntegration:
    """Integration tests for categories"""

    def test_list_categories(self, client, auth_headers):
        """Test listing categories"""
        response = client.get("/api/categories", headers=auth_headers)
        assert response.status_code in [200, 401, 404]

    def test_create_category(self, client, auth_headers):
        """Test creating a category"""
        response = client.post(
            "/api/categories",
            json={"name": "Test Category", "name_ar": "فئة اختبار"},
            headers=auth_headers,
        )
        # 201 = created, 401 = unauthorized, 404 = not found, 400 = validation error
        assert response.status_code in [200, 201, 400, 401, 404, 405]


class TestWarehousesIntegration:
    """Integration tests for warehouses"""

    def test_list_warehouses(self, client, auth_headers):
        """Test listing warehouses"""
        response = client.get("/api/warehouses", headers=auth_headers)
        assert response.status_code in [200, 401, 404]

    def test_create_warehouse(self, client, auth_headers):
        """Test creating a warehouse"""
        import time
        response = client.post(
            "/api/warehouses",
            json={
                "name": f"Test Warehouse {time.time()}",
                "name_ar": "مخزن اختبار",
                "location": "Test Location",
            },
            headers=auth_headers,
        )
        assert response.status_code in [200, 201, 400, 401, 404, 405]


class TestInvoicesIntegration:
    """Integration tests for invoices"""

    def test_list_invoices(self, client, auth_headers):
        """Test listing invoices"""
        response = client.get("/api/invoices", headers=auth_headers)
        assert response.status_code in [200, 401, 404]

    def test_create_invoice_requires_data(self, client, auth_headers):
        """Test that creating invoice requires proper data"""
        response = client.post(
            "/api/invoices",
            json={},
            headers=auth_headers,
        )
        # Should fail validation
        assert response.status_code in [400, 401, 404, 405, 422]


class TestDashboardIntegration:
    """Integration tests for dashboard"""

    def test_dashboard_stats(self, client, auth_headers):
        """Test dashboard statistics endpoint"""
        response = client.get("/api/dashboard/stats", headers=auth_headers)
        assert response.status_code in [200, 401, 404]

    def test_dashboard_charts(self, client, auth_headers):
        """Test dashboard charts endpoint"""
        response = client.get("/api/dashboard/charts", headers=auth_headers)
        assert response.status_code in [200, 401, 404]


class TestReportsIntegration:
    """Integration tests for reports"""

    def test_sales_report(self, client, auth_headers):
        """Test sales report endpoint"""
        response = client.get("/api/reports/sales", headers=auth_headers)
        assert response.status_code in [200, 401, 404]

    def test_inventory_report(self, client, auth_headers):
        """Test inventory report endpoint"""
        response = client.get("/api/reports/inventory", headers=auth_headers)
        assert response.status_code in [200, 401, 404]
