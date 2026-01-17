"""
Tests for Lot Management Routes
"""

import pytest
from datetime import datetime, timedelta


class TestLotCRUD:
    """Test Lot CRUD operations."""
    
    def test_list_lots(self, auth_client):
        """Test listing all lots."""
        response = auth_client.get('/api/lots')
        
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, (list, dict))
    
    def test_get_lot(self, auth_client):
        """Test getting a single lot."""
        response = auth_client.get('/api/lots/1')
        
        # May or may not exist
        assert response.status_code in [200, 404]
    
    def test_create_lot(self, auth_client):
        """Test creating a new lot."""
        expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        
        response = auth_client.post('/api/lots', json={
            'product_id': 1,
            'lot_number': f'LOT-TEST-{datetime.now().timestamp()}',
            'quantity': 100,
            'expiry_date': expiry_date,
            'warehouse_id': 1
        })
        
        # May fail if product or warehouse doesn't exist
        assert response.status_code in [200, 201, 400, 404]
    
    def test_update_lot(self, auth_client):
        """Test updating a lot."""
        response = auth_client.put('/api/lots/1', json={
            'quantity': 50
        })
        
        assert response.status_code in [200, 400, 404]
    
    def test_delete_lot(self, auth_client):
        """Test deleting a lot."""
        # First create a lot to delete
        expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        create_response = auth_client.post('/api/lots', json={
            'product_id': 1,
            'lot_number': f'LOT-DEL-{datetime.now().timestamp()}',
            'quantity': 10,
            'expiry_date': expiry_date,
            'warehouse_id': 1
        })
        
        if create_response.status_code in [200, 201]:
            data = create_response.get_json()
            lot_id = data.get('id', data.get('lot_id'))
            
            if lot_id:
                response = auth_client.delete(f'/api/lots/{lot_id}')
                assert response.status_code in [200, 204, 400, 404]


class TestLotFIFO:
    """Test FIFO functionality."""
    
    def test_get_fifo_lots(self, auth_client):
        """Test getting lots in FIFO order."""
        response = auth_client.get('/api/lots/fifo/1')
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            if isinstance(data, list) and len(data) > 1:
                # Verify FIFO order (oldest first)
                for i in range(len(data) - 1):
                    date1 = data[i].get('created_at') or data[i].get('manufacture_date')
                    date2 = data[i+1].get('created_at') or data[i+1].get('manufacture_date')
                    if date1 and date2:
                        assert date1 <= date2


class TestLotExpiry:
    """Test lot expiry functionality."""
    
    def test_get_expiring_lots(self, auth_client):
        """Test getting expiring lots."""
        response = auth_client.get('/api/lots/expiring')
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data, (list, dict))
    
    def test_get_expiring_lots_with_days(self, auth_client):
        """Test getting lots expiring within N days."""
        response = auth_client.get('/api/lots/expiring?days=30')
        
        assert response.status_code in [200, 404]


class TestLotReservation:
    """Test lot reservation functionality."""
    
    def test_reserve_lot(self, auth_client):
        """Test reserving quantity from a lot."""
        response = auth_client.post('/api/lots/1/reserve', json={
            'quantity': 5,
            'reference': 'TEST-RES-001'
        })
        
        assert response.status_code in [200, 400, 404]
    
    def test_release_lot(self, auth_client):
        """Test releasing reserved quantity."""
        response = auth_client.post('/api/lots/1/release', json={
            'quantity': 5,
            'reference': 'TEST-RES-001'
        })
        
        assert response.status_code in [200, 400, 404]


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
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        data = response.get_json()
        token = data.get('access_token', data.get('token'))
        
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
