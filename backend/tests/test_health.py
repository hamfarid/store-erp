"""
Tests for Health Check Routes
"""

import pytest
from flask import Flask


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_basic_health_check(self, client):
        """Test basic health check returns 200."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'version' in data
    
    def test_detailed_health_check(self, client):
        """Test detailed health check with metrics."""
        response = client.get('/api/health/detailed')
        
        # Should be 200 if database is connected
        assert response.status_code in [200, 503]
        
        data = response.get_json()
        assert 'status' in data
        assert 'timestamp' in data
        
        if response.status_code == 200:
            assert 'checks' in data
            assert 'metrics' in data
    
    def test_readiness_check(self, client):
        """Test readiness check endpoint."""
        response = client.get('/health/ready')
        
        assert response.status_code in [200, 503]
        
        data = response.get_json()
        assert 'status' in data
        assert 'timestamp' in data
    
    def test_liveness_check(self, client):
        """Test liveness check endpoint."""
        response = client.get('/health/live')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'alive'
        assert 'timestamp' in data


class TestHealthMetrics:
    """Test health metrics."""
    
    def test_health_includes_version(self, client):
        """Test health check includes version."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'version' in data
    
    def test_detailed_includes_system_metrics(self, client):
        """Test detailed health includes system metrics."""
        response = client.get('/api/health/detailed')
        
        if response.status_code == 200:
            data = response.get_json()
            
            if 'metrics' in data:
                metrics = data['metrics']
                assert 'cpu' in metrics or 'memory' in metrics


@pytest.fixture
def client():
    """Create test client."""
    from src.app import create_app
    
    app = create_app('testing')
    
    with app.test_client() as client:
        yield client
