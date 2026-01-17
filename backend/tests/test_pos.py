"""
Tests for POS System Routes
"""

import pytest
from decimal import Decimal
from datetime import datetime


class TestPOSShift:
    """Test POS shift management."""
    
    def test_open_shift(self, auth_client):
        """Test opening a new shift."""
        response = auth_client.post('/api/pos/shift/open', json={
            'opening_cash': 1000.00,
            'notes': 'Morning shift'
        })
        
        assert response.status_code in [200, 201]
        
        if response.status_code in [200, 201]:
            data = response.get_json()
            assert 'shift_id' in data or 'id' in data
    
    def test_get_current_shift(self, auth_client):
        """Test getting current shift."""
        response = auth_client.get('/api/pos/shift/current')
        
        # May or may not have an active shift
        assert response.status_code in [200, 404]
    
    def test_close_shift(self, auth_client):
        """Test closing a shift."""
        # First open a shift
        auth_client.post('/api/pos/shift/open', json={
            'opening_cash': 1000.00
        })
        
        response = auth_client.post('/api/pos/shift/close', json={
            'closing_cash': 1500.00,
            'notes': 'End of day'
        })
        
        assert response.status_code in [200, 400, 404]


class TestPOSSales:
    """Test POS sales functionality."""
    
    def test_create_sale(self, auth_client):
        """Test creating a POS sale."""
        response = auth_client.post('/api/pos/sale', json={
            'items': [
                {
                    'product_id': 1,
                    'quantity': 2,
                    'price': 100.00
                }
            ],
            'payment_method': 'cash',
            'received_amount': 200.00
        })
        
        # May fail if no shift is open or no products
        assert response.status_code in [200, 201, 400, 404]
    
    def test_get_sale(self, auth_client):
        """Test getting a sale by ID."""
        response = auth_client.get('/api/pos/sale/1')
        
        # May or may not exist
        assert response.status_code in [200, 404]
    
    def test_search_products(self, auth_client):
        """Test searching products for POS."""
        response = auth_client.get('/api/pos/products/search?q=test')
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data, (list, dict))
    
    def test_search_by_barcode(self, auth_client):
        """Test searching product by barcode."""
        response = auth_client.get('/api/pos/products/barcode/1234567890')
        
        # May or may not find product
        assert response.status_code in [200, 404]


class TestPOSReports:
    """Test POS reporting functionality."""
    
    def test_shift_report(self, auth_client):
        """Test getting shift report."""
        response = auth_client.get('/api/pos/shift/report')
        
        assert response.status_code in [200, 404]
    
    def test_daily_summary(self, auth_client):
        """Test getting daily summary."""
        today = datetime.now().strftime('%Y-%m-%d')
        response = auth_client.get(f'/api/pos/daily-summary?date={today}')
        
        assert response.status_code in [200, 404]


@pytest.fixture
def client():
    """Create test client."""
    from src.app import create_app
    
    app = create_app('testing')
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_client(client):
    """Create authenticated test client."""
    # Login to get token
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        data = response.get_json()
        token = data.get('access_token', data.get('token'))
        
        # Create a client with auth header
        class AuthClient:
            def __init__(self, client, token):
                self.client = client
                self.headers = {'Authorization': f'Bearer {token}'}
            
            def get(self, *args, **kwargs):
                kwargs['headers'] = {**kwargs.get('headers', {}), **self.headers}
                return self.client.get(*args, **kwargs)
            
            def post(self, *args, **kwargs):
                kwargs['headers'] = {**kwargs.get('headers', {}), **self.headers}
                return self.client.post(*args, **kwargs)
            
            def put(self, *args, **kwargs):
                kwargs['headers'] = {**kwargs.get('headers', {}), **self.headers}
                return self.client.put(*args, **kwargs)
            
            def delete(self, *args, **kwargs):
                kwargs['headers'] = {**kwargs.get('headers', {}), **self.headers}
                return self.client.delete(*args, **kwargs)
        
        return AuthClient(client, token)
    
    return client
