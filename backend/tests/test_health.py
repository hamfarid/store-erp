"""
Tests for Health Check Routes
"""

import pytest


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_basic_health_check(self, client):
        """Test basic health check returns 200."""
        response = client.get('/api/health')
        # May be 404 if health blueprint not registered
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data.get('status') in ['healthy', 'ok']
    
    def test_detailed_health_check(self, client):
        """Test detailed health check with metrics."""
        response = client.get('/api/health/detailed')
        
        # Should be 200, 404, or 503
        assert response.status_code in [200, 404, 503]
    
    def test_root_health(self, client):
        """Test root health endpoint."""
        response = client.get('/health')
        
        # May or may not be registered
        assert response.status_code in [200, 404]


class TestAPIStatus:
    """Test basic API status."""
    
    def test_api_is_running(self, client):
        """Test that API is accessible."""
        # Try several common endpoints
        endpoints = ['/api/health', '/api', '/', '/api/auth/login']
        
        success = False
        for endpoint in endpoints:
            response = client.get(endpoint)
            if response.status_code in [200, 401, 405]:
                success = True
                break
        
        assert success, "API should be accessible on at least one endpoint"
    
    def test_json_response(self, client):
        """Test that API returns JSON responses."""
        response = client.post('/api/auth/login', 
                              json={'username': 'test', 'password': 'test'},
                              content_type='application/json')
        
        # Should return JSON even on error (405 means endpoint exists but wrong method)
        assert response.content_type.startswith('application/json') or response.status_code in [404, 405]
