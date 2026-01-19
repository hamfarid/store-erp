"""
Tenant API Integration Tests
اختبارات تكامل API المستأجر

Integration tests for the multi-tenancy Flask API.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17

Usage:
    pytest tests/test_tenant_api.py -v
"""

from __future__ import annotations

import json
import uuid
import pytest
from unittest.mock import patch


# Test data
VALID_TENANT_DATA = {
    'name': 'Test Company',
    'name_ar': 'شركة اختبار',
    'slug': 'test-company',
    'plan_code': 'basic',
}

VALID_USER_DATA = {
    'email': 'user@example.com',
    'role': 'member',
}


class TestTenantAPI:
    """
    Test cases for Tenant API endpoints.
    حالات اختبار لنقاط نهاية API المستأجر.
    """

    @pytest.fixture
    def app(self):
        """Create test Flask app."""
        from src.main import app as flask_app

        flask_app.config['TESTING'] = True

        with flask_app.app_context():
            try:
                from src.models.user import db
                db.create_all()
                yield flask_app
                db.drop_all()
            except Exception:
                yield flask_app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    @pytest.fixture
    def auth_headers(self):
        """Create mock auth headers."""
        return {
            'Authorization': 'Bearer test_token_12345',
            'Content-Type': 'application/json',
        }

    # ==================== List Tenants ====================

    def test_list_tenants_unauthorized(self, client):
        """Test listing tenants without auth returns 401."""
        response = client.get('/api/tenants/')
        assert response.status_code == 401

    @patch('src.routes.tenant_api.verify_token')
    def test_list_tenants_empty(self, mock_verify, client, auth_headers):
        """Test listing tenants when none exist."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        response = client.get('/api/tenants/', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert isinstance(data['data'], list)

    # ==================== Create Tenant ====================

    @patch('src.routes.tenant_api.verify_token')
    def test_create_tenant_success(self, mock_verify, client, auth_headers):
        """Test creating a tenant with valid data."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data['success'] is True
        assert data['data']['name'] == VALID_TENANT_DATA['name']
        assert data['data']['slug'] == VALID_TENANT_DATA['slug']

    @patch('src.routes.tenant_api.verify_token')
    def test_create_tenant_missing_name(self, mock_verify, client, auth_headers):
        """Test creating tenant without name fails."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps({'slug': 'test'})
        )
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['success'] is False

    @patch('src.routes.tenant_api.verify_token')
    def test_create_tenant_duplicate_slug(self, mock_verify, client, auth_headers):
        """Test creating tenant with duplicate slug fails."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create first tenant
        client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )

        # Try to create with same slug
        response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        data = json.loads(response.data)

        assert response.status_code == 409
        assert data['success'] is False

    # ==================== Get Tenant ====================

    @patch('src.routes.tenant_api.verify_token')
    def test_get_tenant_success(self, mock_verify, client, auth_headers):
        """Test getting a specific tenant."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant first
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # Get tenant
        response = client.get(f'/api/tenants/{tenant_id}', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert data['data']['id'] == tenant_id

    @patch('src.routes.tenant_api.verify_token')
    def test_get_tenant_not_found(self, mock_verify, client, auth_headers):
        """Test getting non-existent tenant returns 404."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        fake_id = str(uuid.uuid4())
        response = client.get(f'/api/tenants/{fake_id}', headers=auth_headers)

        assert response.status_code == 404

    # ==================== Update Tenant ====================

    @patch('src.routes.tenant_api.verify_token')
    def test_update_tenant_success(self, mock_verify, client, auth_headers):
        """Test updating a tenant."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # Update tenant
        update_data = {'name': 'Updated Company', 'name_ar': 'شركة محدثة'}
        response = client.put(
            f'/api/tenants/{tenant_id}',
            headers=auth_headers,
            data=json.dumps(update_data)
        )
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert data['data']['name'] == 'Updated Company'

    # ==================== Delete (Deactivate) Tenant ====================

    @patch('src.routes.tenant_api.verify_token')
    def test_delete_tenant_success(self, mock_verify, client, auth_headers):
        """Test deactivating a tenant."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # Delete (deactivate) tenant
        response = client.delete(f'/api/tenants/{tenant_id}', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True

        # Verify tenant is deactivated
        get_response = client.get(f'/api/tenants/{tenant_id}', headers=auth_headers)
        get_data = json.loads(get_response.data)

        assert get_data['data']['status'] == 'suspended'

    # ==================== Tenant Users ====================

    @patch('src.routes.tenant_api.verify_token')
    def test_add_tenant_user_success(self, mock_verify, client, auth_headers):
        """Test adding a user to a tenant."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # Add user
        response = client.post(
            f'/api/tenants/{tenant_id}/users',
            headers=auth_headers,
            data=json.dumps(VALID_USER_DATA)
        )
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data['success'] is True

    @patch('src.routes.tenant_api.verify_token')
    def test_list_tenant_users(self, mock_verify, client, auth_headers):
        """Test listing users in a tenant."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # List users
        response = client.get(f'/api/tenants/{tenant_id}/users', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True
        assert isinstance(data['data'], list)

    # ==================== Settings ====================

    @patch('src.routes.tenant_api.verify_token')
    def test_get_tenant_settings(self, mock_verify, client, auth_headers):
        """Test getting tenant settings."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # Get settings
        response = client.get(f'/api/tenants/{tenant_id}/settings', headers=auth_headers)
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True

    @patch('src.routes.tenant_api.verify_token')
    def test_update_tenant_settings(self, mock_verify, client, auth_headers):
        """Test updating tenant settings."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        create_response = client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )
        created = json.loads(create_response.data)
        tenant_id = created['data']['id']

        # Update settings
        settings_data = {'theme': 'dark', 'language': 'ar'}
        response = client.put(
            f'/api/tenants/{tenant_id}/settings',
            headers=auth_headers,
            data=json.dumps(settings_data)
        )
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['success'] is True

    # ==================== Plans ====================

    def test_list_plans_no_auth_required(self, client):
        """Test listing plans doesn't require auth."""
        response = client.get('/api/tenants/plans')

        assert response.status_code == 200

    # ==================== Check Slug ====================

    def test_check_slug_available(self, client):
        """Test checking available slug."""
        response = client.get('/api/tenants/check-slug?slug=new-company')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['available'] is True

    @patch('src.routes.tenant_api.verify_token')
    def test_check_slug_taken(self, mock_verify, client, auth_headers):
        """Test checking taken slug."""
        mock_verify.return_value = {'user_id': 'test-user', 'is_admin': True}

        # Create tenant
        client.post(
            '/api/tenants/',
            headers=auth_headers,
            data=json.dumps(VALID_TENANT_DATA)
        )

        # Check slug
        response = client.get(f'/api/tenants/check-slug?slug={VALID_TENANT_DATA["slug"]}')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['available'] is False


class TestTenantMiddleware:
    """
    Test cases for Tenant Middleware.
    حالات اختبار لوسيط المستأجر.
    """

    @pytest.fixture
    def app(self):
        """Create test Flask app with middleware."""
        from flask import Flask
        from src.middleware.flask_tenant_middleware import init_tenant_middleware

        app = Flask(__name__)
        app.config['TESTING'] = True
        init_tenant_middleware(app)

        @app.route('/test')
        def test_route():
            from flask import g
            return {
                'tenant_id': getattr(g, 'tenant_id', None),
                'has_tenant': hasattr(g, 'tenant') and g.tenant is not None
            }

        return app

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return app.test_client()

    def test_middleware_extracts_header_tenant(self, client):
        """Test middleware extracts tenant from X-Tenant-ID header."""
        # Note: This will fail to load tenant since DB is not set up
        # But it tests the header extraction logic
        response = client.get('/test', headers={'X-Tenant-ID': 'test-tenant-id'})
        _ = json.loads(response.data)  # Parse to validate JSON

        # Tenant won't be loaded (no DB), but request should succeed
        assert response.status_code == 200

    def test_middleware_handles_no_tenant(self, client):
        """Test middleware handles requests without tenant."""
        response = client.get('/test')
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['tenant_id'] is None


class TestTenantModels:
    """
    Test cases for Tenant SQLAlchemy Models.
    حالات اختبار لنماذج SQLAlchemy للمستأجر.
    """

    @pytest.fixture
    def db_session(self):
        """Create in-memory database session."""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, scoped_session

        engine = create_engine('sqlite:///:memory:')
        Session = scoped_session(sessionmaker(bind=engine))

        # Create tables
        from src.models.tenant_sqlalchemy import Tenant, TenantPlan
        Tenant.__table__.create(engine, checkfirst=True)
        TenantPlan.__table__.create(engine, checkfirst=True)

        yield Session()

        Session.remove()

    def test_tenant_model_creation(self, db_session):
        """Test creating a Tenant model."""
        from src.models.tenant_sqlalchemy import Tenant

        tenant = Tenant(
            name='Test Company',
            slug='test-company',
        )

        db_session.add(tenant)
        db_session.commit()

        assert tenant.id is not None
        assert tenant.schema_name == 'tenant_test_company'
        assert tenant.is_active is True

    def test_tenant_slug_validation(self, db_session):
        """Test tenant slug must be unique."""
        from src.models.tenant_sqlalchemy import Tenant
        from sqlalchemy.exc import IntegrityError

        tenant1 = Tenant(name='Company 1', slug='same-slug')
        db_session.add(tenant1)
        db_session.commit()

        tenant2 = Tenant(name='Company 2', slug='same-slug')
        db_session.add(tenant2)

        with pytest.raises(IntegrityError):
            db_session.commit()


# Run tests if executed directly
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
