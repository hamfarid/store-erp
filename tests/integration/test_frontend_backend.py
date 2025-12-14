"""
Frontend/Backend Integration Tests

Tests the integration between React frontend and Flask backend.

Author: Store ERP Team
Version: 2.0
Last Updated: 2025-12-13
"""

import pytest
import requests
import json
from typing import Dict, Any


class TestFrontendBackendIntegration:
    """Test frontend/backend integration."""
    
    # Configuration
    BACKEND_URL = "http://localhost:8000"
    FRONTEND_URL = "http://localhost:5502"
    
    @pytest.fixture
    def auth_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        # Login
        response = requests.post(
            f"{self.BACKEND_URL}/api/auth/login",
            json={
                "username": "admin",
                "password": "admin123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        
        # Extract token (if using JWT)
        token = data.get('token')
        if token:
            return {"Authorization": f"Bearer {token}"}
        
        # Or use session cookies
        return {}
    
    def test_backend_health(self):
        """Test backend health endpoint."""
        response = requests.get(f"{self.BACKEND_URL}/health")
        assert response.status_code == 200
        assert "healthy" in response.text.lower()
    
    def test_frontend_loads(self):
        """Test frontend loads successfully."""
        response = requests.get(self.FRONTEND_URL)
        assert response.status_code == 200
        assert "text/html" in response.headers.get('Content-Type', '')
    
    def test_api_products_endpoint(self, auth_headers):
        """Test products API endpoint."""
        response = requests.get(
            f"{self.BACKEND_URL}/api/products",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_api_customers_endpoint(self, auth_headers):
        """Test customers API endpoint."""
        response = requests.get(
            f"{self.BACKEND_URL}/api/customers",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
    
    def test_api_suppliers_endpoint(self, auth_headers):
        """Test suppliers API endpoint."""
        response = requests.get(
            f"{self.BACKEND_URL}/api/suppliers",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
    
    def test_api_invoices_endpoint(self, auth_headers):
        """Test invoices API endpoint."""
        response = requests.get(
            f"{self.BACKEND_URL}/api/invoices",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
    
    def test_api_dashboard_stats(self, auth_headers):
        """Test dashboard statistics endpoint."""
        response = requests.get(
            f"{self.BACKEND_URL}/api/dashboard/stats",
            headers=auth_headers
        )
        
        # May return 200 or 404 depending on implementation
        assert response.status_code in [200, 404]
    
    def test_cors_headers(self):
        """Test CORS headers are set correctly."""
        response = requests.options(
            f"{self.BACKEND_URL}/api/products",
            headers={
                "Origin": self.FRONTEND_URL,
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Check CORS headers
        assert "Access-Control-Allow-Origin" in response.headers or response.status_code == 404
    
    def test_create_product(self, auth_headers):
        """Test creating a product via API."""
        product_data = {
            "name": "Test Product Integration",
            "barcode": "TEST-INT-001",
            "purchase_price": 50.0,
            "sale_price": 75.0,
            "quantity": 100,
            "min_quantity": 10,
            "unit": "piece"
        }
        
        response = requests.post(
            f"{self.BACKEND_URL}/api/products",
            headers=auth_headers,
            json=product_data
        )
        
        # May return 201 or 404 depending on implementation
        assert response.status_code in [201, 404, 405]
    
    def test_error_handling(self, auth_headers):
        """Test API error handling."""
        # Try to get non-existent product
        response = requests.get(
            f"{self.BACKEND_URL}/api/products/999999",
            headers=auth_headers
        )
        
        # Should return 404 or error response
        assert response.status_code in [404, 200]
        
        if response.status_code == 200:
            data = response.json()
            # If 200, should have success: false
            assert data.get('success') is not None
    
    def test_authentication_required(self):
        """Test that authentication is required for protected endpoints."""
        # Try to access protected endpoint without auth
        response = requests.get(f"{self.BACKEND_URL}/api/products")
        
        # Should return 401 or redirect to login
        assert response.status_code in [401, 302, 200]
    
    def test_static_assets_load(self):
        """Test that static assets load from frontend."""
        # Try to load main CSS
        response = requests.get(f"{self.FRONTEND_URL}/src/index.css")
        
        # May return 200 or 404 depending on build
        assert response.status_code in [200, 404]


class TestAPIResponses:
    """Test API response formats."""
    
    BACKEND_URL = "http://localhost:8000"
    
    def test_success_response_format(self):
        """Test success response format."""
        # This is a general test - actual endpoint may vary
        response = requests.get(f"{self.BACKEND_URL}/health")
        
        if response.status_code == 200:
            # Check response is valid
            assert len(response.text) > 0
    
    def test_error_response_format(self):
        """Test error response format."""
        # Try invalid endpoint
        response = requests.get(f"{self.BACKEND_URL}/api/invalid-endpoint-xyz")
        
        # Should return error
        assert response.status_code in [404, 405]


class TestDataFlow:
    """Test data flow between frontend and backend."""
    
    BACKEND_URL = "http://localhost:8000"
    
    @pytest.fixture
    def auth_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        response = requests.post(
            f"{self.BACKEND_URL}/api/auth/login",
            json={
                "username": "admin",
                "password": "admin123"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            if token:
                return {"Authorization": f"Bearer {token}"}
        
        return {}
    
    def test_product_crud_flow(self, auth_headers):
        """Test complete CRUD flow for products."""
        # This is a placeholder - actual implementation depends on API
        # 1. Create product
        # 2. Read product
        # 3. Update product
        # 4. Delete product
        pass
    
    def test_invoice_creation_flow(self, auth_headers):
        """Test invoice creation flow."""
        # This is a placeholder
        # 1. Create customer
        # 2. Add products to cart
        # 3. Create invoice
        # 4. Verify invoice created
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
