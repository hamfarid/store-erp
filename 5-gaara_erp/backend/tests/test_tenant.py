"""
Tenant Module Tests
اختبارات وحدة المستأجر

Unit and integration tests for multi-tenancy functionality.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import JsonResponse


class TestTenantModel(TestCase):
    """
    Tests for Tenant model.
    اختبارات نموذج المستأجر.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_tenant_creation(self):
        """Test basic tenant creation."""
        from backend.src.models.tenant import Tenant

        tenant = Tenant.objects.create(
            name='Test Company',
            slug='test-company',
            owner=self.user
        )

        assert tenant.id is not None
        assert tenant.name == 'Test Company'
        assert tenant.slug == 'test-company'
        assert tenant.schema_name == 'tenant_test_company'
        assert tenant.is_active is True
        assert tenant.status == 'trial'

    def test_tenant_schema_name_auto_generation(self):
        """Test schema name is auto-generated from slug."""
        from backend.src.models.tenant import Tenant

        tenant = Tenant.objects.create(
            name='My Company',
            slug='my-company-name',
            owner=self.user
        )

        # Schema name should convert hyphens to underscores
        assert tenant.schema_name == 'tenant_my_company_name'

    def test_tenant_slug_validation(self):
        """Test slug validation rejects invalid characters."""
        from backend.src.models.tenant import Tenant
        from django.core.exceptions import ValidationError

        tenant = Tenant(
            name='Invalid',
            slug='Invalid_Slug!',  # Invalid: uppercase and special chars
            owner=self.user
        )

        with pytest.raises(ValidationError):
            tenant.full_clean()

    def test_tenant_is_subscription_active_trial(self):
        """Test subscription active check during trial."""
        from backend.src.models.tenant import Tenant
        from django.utils import timezone

        tenant = Tenant.objects.create(
            name='Trial Company',
            slug='trial-company',
            owner=self.user,
            status='trial',
            trial_ends_at=timezone.now() + timedelta(days=7)
        )

        assert tenant.is_trial is True
        assert tenant.is_subscription_active is True

    def test_tenant_is_subscription_expired(self):
        """Test subscription active check when expired."""
        from backend.src.models.tenant import Tenant
        from django.utils import timezone

        tenant = Tenant.objects.create(
            name='Expired Company',
            slug='expired-company',
            owner=self.user,
            status='active',
            subscription_ends_at=timezone.now() - timedelta(days=1)
        )

        assert tenant.is_subscription_active is False


class TestTenantPlanModel(TestCase):
    """
    Tests for TenantPlan model.
    اختبارات نموذج خطة المستأجر.
    """

    def test_plan_creation(self):
        """Test basic plan creation."""
        from backend.src.models.tenant import TenantPlan

        plan = TenantPlan.objects.create(
            name='Professional',
            code='pro',
            max_users=50,
            max_storage_gb=100,
            max_api_calls_per_day=50000,
            price_monthly=499.00
        )

        assert plan.id is not None
        assert plan.name == 'Professional'
        assert plan.max_users == 50

    def test_plan_get_feature(self):
        """Test feature checking."""
        from backend.src.models.tenant import TenantPlan

        plan = TenantPlan.objects.create(
            name='Basic',
            code='basic',
            features={
                'advanced_reports': False,
                'api_access': True
            }
        )

        assert plan.get_feature('api_access') is True
        assert plan.get_feature('advanced_reports') is False
        assert plan.get_feature('nonexistent') is False


class TestTenantUserModel(TestCase):
    """
    Tests for TenantUser model.
    اختبارات نموذج مستخدم المستأجر.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.User = get_user_model()
        self.owner = self.User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass123'
        )
        self.member = self.User.objects.create_user(
            username='member',
            email='member@example.com',
            password='pass123'
        )

        from backend.src.models.tenant import Tenant
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            owner=self.owner
        )

    def test_tenant_user_creation(self):
        """Test creating tenant user membership."""
        from backend.src.models.tenant import TenantUser

        tu = TenantUser.objects.create(
            tenant=self.tenant,
            user=self.member,
            role='member'
        )

        assert tu.id is not None
        assert tu.role == 'member'
        assert tu.is_active is True

    def test_tenant_user_has_permission_admin(self):
        """Test admin has all permissions."""
        from backend.src.models.tenant import TenantUser

        tu = TenantUser.objects.create(
            tenant=self.tenant,
            user=self.member,
            role='admin'
        )

        assert tu.has_permission('any_permission') is True

    def test_tenant_user_has_permission_member(self):
        """Test member only has explicit permissions."""
        from backend.src.models.tenant import TenantUser

        tu = TenantUser.objects.create(
            tenant=self.tenant,
            user=self.member,
            role='member',
            permissions={'view_reports': True}
        )

        assert tu.has_permission('view_reports') is True
        assert tu.has_permission('edit_reports') is False


class TestTenantService(TestCase):
    """
    Tests for TenantService.
    اختبارات خدمة المستأجر.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    @patch('backend.src.services.tenant_service.connection')
    def test_create_tenant(self, mock_connection):
        """Test tenant creation via service."""
        from backend.src.services.tenant_service import TenantService

        # Mock cursor for schema creation
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_connection.cursor.return_value.__exit__ = Mock(return_value=False)

        service = TenantService()
        tenant = service.create_tenant(
            name='New Company',
            slug='new-company',
            owner=self.user
        )

        assert tenant is not None
        assert tenant.slug == 'new-company'
        assert tenant.status == 'trial'

    def test_create_tenant_duplicate_slug(self):
        """Test duplicate slug raises error."""
        from backend.src.models.tenant import Tenant
        from backend.src.services.tenant_service import TenantService, TenantExistsError

        # Create existing tenant
        Tenant.objects.create(
            name='Existing',
            slug='existing-slug',
            owner=self.user
        )

        service = TenantService()
        with pytest.raises(TenantExistsError) as exc:
            service.create_tenant(
                name='New',
                slug='existing-slug',
                owner=self.user
            )

        assert exc.value.code == 'TENANT_EXISTS'

    def test_get_tenant_by_slug(self):
        """Test getting tenant by slug."""
        from backend.src.models.tenant import Tenant
        from backend.src.services.tenant_service import TenantService

        Tenant.objects.create(
            name='Find Me',
            slug='find-me',
            owner=self.user
        )

        service = TenantService()
        tenant = service.get_tenant_by_slug('find-me')

        assert tenant is not None
        assert tenant.name == 'Find Me'

    def test_get_tenant_by_slug_not_found(self):
        """Test getting nonexistent tenant returns None."""
        from backend.src.services.tenant_service import TenantService

        service = TenantService()
        tenant = service.get_tenant_by_slug('nonexistent')

        assert tenant is None


class TestTenantMiddleware(TestCase):
    """
    Tests for TenantMiddleware.
    اختبارات وسيط المستأجر.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        from backend.src.models.tenant import Tenant
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            owner=self.user
        )

    def test_exempt_path_bypasses_middleware(self):
        """Test exempt paths don't require tenant."""
        from backend.src.middleware.tenant_middleware import TenantMiddleware

        request = self.factory.get('/api/health/')
        middleware = TenantMiddleware(lambda r: JsonResponse({'ok': True}))

        response = middleware(request)

        assert response.status_code == 200
        assert request.tenant is None

    def test_header_tenant_identification(self):
        """Test tenant identification via header."""
        from backend.src.middleware.tenant_middleware import TenantMiddleware

        request = self.factory.get(
            '/api/products/',
            HTTP_X_TENANT_ID=str(self.tenant.id)
        )

        middleware = TenantMiddleware(lambda r: JsonResponse({'ok': True}))

        with patch.object(middleware, '_activate_tenant_schema'):
            with patch.object(middleware, '_reset_schema'):
                response = middleware(request)

        assert response.status_code == 200
        assert request.tenant.id == self.tenant.id

    def test_slug_header_tenant_identification(self):
        """Test tenant identification via slug header."""
        from backend.src.middleware.tenant_middleware import TenantMiddleware

        request = self.factory.get(
            '/api/products/',
            HTTP_X_TENANT_SLUG='test-tenant'
        )

        middleware = TenantMiddleware(lambda r: JsonResponse({'ok': True}))

        with patch.object(middleware, '_activate_tenant_schema'):
            with patch.object(middleware, '_reset_schema'):
                response = middleware(request)

        assert response.status_code == 200
        assert request.tenant.slug == 'test-tenant'

    def test_missing_tenant_returns_404(self):
        """Test missing tenant returns 404."""
        from backend.src.middleware.tenant_middleware import TenantMiddleware

        request = self.factory.get(
            '/api/products/',
            HTTP_X_TENANT_ID='00000000-0000-0000-0000-000000000000'
        )

        middleware = TenantMiddleware(lambda r: JsonResponse({'ok': True}))
        response = middleware(request)

        assert response.status_code == 404

    def test_inactive_tenant_returns_403(self):
        """Test inactive tenant returns 403."""
        from backend.src.middleware.tenant_middleware import TenantMiddleware
        from backend.src.models.tenant import Tenant

        # Deactivate tenant
        self.tenant.is_active = False
        self.tenant.save()

        request = self.factory.get(
            '/api/products/',
            HTTP_X_TENANT_ID=str(self.tenant.id)
        )

        middleware = TenantMiddleware(lambda r: JsonResponse({'ok': True}))
        response = middleware(request)

        assert response.status_code == 403


class TestTenantInvitation(TestCase):
    """
    Tests for TenantInvitation model.
    اختبارات نموذج دعوة المستأجر.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.User = get_user_model()
        self.owner = self.User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass123'
        )
        self.invitee = self.User.objects.create_user(
            username='invitee',
            email='invitee@example.com',
            password='pass123'
        )

        from backend.src.models.tenant import Tenant
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            owner=self.owner
        )

    def test_create_invitation(self):
        """Test creating invitation."""
        from backend.src.models.tenant import TenantInvitation

        invitation = TenantInvitation.create_invitation(
            tenant=self.tenant,
            email='new@example.com',
            role='member',
            invited_by=self.owner
        )

        assert invitation.id is not None
        assert invitation.token is not None
        assert len(invitation.token) == 64
        assert invitation.is_expired is False

    def test_invitation_expiry(self):
        """Test invitation expiry check."""
        from backend.src.models.tenant import TenantInvitation
        from django.utils import timezone

        invitation = TenantInvitation.objects.create(
            tenant=self.tenant,
            email='expired@example.com',
            role='member',
            token='test-token',
            invited_by=self.owner,
            expires_at=timezone.now() - timedelta(days=1)
        )

        assert invitation.is_expired is True

    def test_accept_invitation(self):
        """Test accepting invitation."""
        from backend.src.models.tenant import TenantInvitation, TenantUser

        invitation = TenantInvitation.create_invitation(
            tenant=self.tenant,
            email='invitee@example.com',
            role='member',
            invited_by=self.owner
        )

        tenant_user = invitation.accept(self.invitee)

        assert tenant_user is not None
        assert tenant_user.role == 'member'
        assert invitation.is_accepted is True

    def test_accept_expired_invitation_fails(self):
        """Test accepting expired invitation raises error."""
        from backend.src.models.tenant import TenantInvitation
        from django.utils import timezone

        invitation = TenantInvitation.objects.create(
            tenant=self.tenant,
            email='expired@example.com',
            role='member',
            token='test-token',
            invited_by=self.owner,
            expires_at=timezone.now() - timedelta(days=1)
        )

        with pytest.raises(ValueError) as exc:
            invitation.accept(self.invitee)

        assert 'انتهت' in str(exc.value) or 'expired' in str(exc.value).lower()


# Pytest fixtures for use in other tests
@pytest.fixture
def test_user(db):
    """Create a test user."""
    User = get_user_model()
    return User.objects.create_user(
        username='pytest_user',
        email='pytest@example.com',
        password='testpass123'
    )


@pytest.fixture
def test_tenant(db, test_user):
    """Create a test tenant."""
    from backend.src.models.tenant import Tenant
    return Tenant.objects.create(
        name='Pytest Tenant',
        slug='pytest-tenant',
        owner=test_user
    )


@pytest.fixture
def test_plan(db):
    """Create a test plan."""
    from backend.src.models.tenant import TenantPlan
    return TenantPlan.objects.create(
        name='Test Plan',
        code='test-plan',
        max_users=10,
        max_storage_gb=50
    )
