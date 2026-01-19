"""
FILE: backend/tests/test_api_quick.py | PURPOSE: Quick API endpoint tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Quick API Endpoint Tests

Verifies that all API endpoints are accessible and working.

Version: 1.0.0
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend src to path
backend_src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(backend_src))

from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test that health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data


class TestAuthenticationAPI:
    """Test authentication endpoints"""
    
    def test_register_endpoint_exists(self):
        """Test that register endpoint exists"""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "short",  # Will fail validation
            "name": "Test User"
        })
        # Should return 400 (bad request) not 404 (not found)
        assert response.status_code in [400, 422]  # 422 for validation error
    
    def test_login_endpoint_exists(self):
        """Test that login endpoint exists"""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 422]
    
    def test_me_endpoint_requires_auth(self):
        """Test that /me endpoint requires authentication"""
        response = client.get("/api/v1/auth/me")
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 403]


class TestFarmsAPI:
    """Test farms endpoints"""
    
    def test_list_farms_requires_auth(self):
        """Test that list farms requires authentication"""
        response = client.get("/api/v1/farms")
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 403]
    
    def test_create_farm_requires_auth(self):
        """Test that create farm requires authentication"""
        response = client.post("/api/v1/farms", json={
            "name": "Test Farm",
            "location": "Test Location",
            "area": 100
        })
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 403, 422]


class TestDiagnosisAPI:
    """Test diagnosis endpoints"""
    
    def test_diagnosis_history_requires_auth(self):
        """Test that diagnosis history requires authentication"""
        response = client.get("/api/v1/diagnosis/history")
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 403]
    
    def test_upload_endpoint_exists(self):
        """Test that upload endpoint exists"""
        # Try to upload without auth
        response = client.post("/api/v1/diagnosis/upload")
        # Should return 401 or 422 (validation error) not 404
        assert response.status_code in [401, 403, 422]


class TestReportsAPI:
    """Test reports endpoints"""
    
    def test_list_reports_requires_auth(self):
        """Test that list reports requires authentication"""
        response = client.get("/api/v1/reports")
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 403]
    
    def test_generate_report_requires_auth(self):
        """Test that generate report requires authentication"""
        response = client.post("/api/v1/reports/generate", json={
            "title": "Test Report",
            "report_type": "farm_summary",
            "format": "pdf"
        })
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code in [401, 403, 422]


class TestAPIDocumentation:
    """Test API documentation endpoints"""
    
    def test_openapi_json_exists(self):
        """Test that OpenAPI JSON is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_page_exists(self):
        """Test that Swagger docs page exists"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_page_exists(self):
        """Test that ReDoc page exists"""
        response = client.get("/redoc")
        assert response.status_code == 200


@pytest.mark.parametrize("endpoint,method", [
    ("/api/v1/auth/register", "POST"),
    ("/api/v1/auth/login", "POST"),
    ("/api/v1/auth/me", "GET"),
    ("/api/v1/farms", "GET"),
    ("/api/v1/farms", "POST"),
    ("/api/v1/diagnosis/history", "GET"),
    ("/api/v1/diagnosis/upload", "POST"),
    ("/api/v1/reports", "GET"),
    ("/api/v1/reports/generate", "POST"),
])
def test_endpoint_exists(endpoint, method):
    """Parametrized test to verify all endpoints exist"""
    if method == "GET":
        response = client.get(endpoint)
    elif method == "POST":
        response = client.post(endpoint, json={})
    
    # Endpoint should exist (not return 404)
    assert response.status_code != 404, f"Endpoint {method} {endpoint} not found"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

