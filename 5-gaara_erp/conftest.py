"""
Gaara ERP - Root Test Configuration
====================================
Central pytest configuration with fixtures for all tests.

This file sets up:
- Django settings for tests
- Common fixtures for User, Company, Branch
- Mock fixtures for external services
- Database fixtures
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure Python can import the inner project package gaara_erp (gaara_erp/gaara_erp/...)
ROOT = Path(__file__).resolve().parent
PROJECT_DIR = ROOT / "gaara_erp"
if PROJECT_DIR.is_dir() and str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Default test env
os.environ.setdefault("APP_MODE", "test")

# Set test-specific environment variables
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only-do-not-use-in-production")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "True")
os.environ.setdefault("CELERY_TASK_EAGER_PROPAGATES", "True")


# ============================================
# User Fixtures
# ============================================

@pytest.fixture
def user_password():
    """Default test password."""
    return "TestPassword123!"


@pytest.fixture
def user_data(user_password):
    """Basic user data for creating test users."""
    return {
        "email": "testuser@gaara-erp.com",
        "username": "testuser",
        "password": user_password,
        "first_name": "Test",
        "last_name": "User",
        "is_active": True,
    }


@pytest.fixture
def admin_data(user_password):
    """Admin user data."""
    return {
        "email": "admin@gaara-erp.com",
        "username": "admin",
        "password": user_password,
        "first_name": "Admin",
        "last_name": "User",
        "is_active": True,
        "is_staff": True,
        "is_superuser": True,
    }


@pytest.fixture
def test_user(db, user_data):
    """Create a regular test user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.create_user(
        email=user_data["email"],
        username=user_data.get("username", user_data["email"]),
        password=user_data["password"],
        first_name=user_data.get("first_name", ""),
        last_name=user_data.get("last_name", ""),
    )
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def admin_user(db, admin_data):
    """Create an admin user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.create_superuser(
        email=admin_data["email"],
        username=admin_data.get("username", admin_data["email"]),
        password=admin_data["password"],
    )
    return user


@pytest.fixture
def authenticated_client(client, test_user, user_password):
    """Return a client logged in as test_user."""
    client.login(email=test_user.email, password=user_password)
    return client


@pytest.fixture
def admin_client(client, admin_user, user_password):
    """Return a client logged in as admin."""
    client.login(email=admin_user.email, password=user_password)
    return client


# ============================================
# API Client Fixtures
# ============================================

@pytest.fixture
def api_client():
    """DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, test_user):
    """DRF API client with authentication."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def admin_api_client(api_client, admin_user):
    """DRF API client with admin authentication."""
    api_client.force_authenticate(user=admin_user)
    return api_client


# ============================================
# JWT Token Fixtures
# ============================================

@pytest.fixture
def jwt_tokens(test_user):
    """Generate JWT tokens for test user."""
    from rest_framework_simplejwt.tokens import RefreshToken
    
    refresh = RefreshToken.for_user(test_user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@pytest.fixture
def jwt_authenticated_client(api_client, jwt_tokens):
    """API client with JWT authentication."""
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_tokens["access"]}')
    return api_client


# ============================================
# Mock Fixtures for External Services
# ============================================

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Mocked response"))]
        )
        yield mock


@pytest.fixture
def mock_redis():
    """Mock Redis connections."""
    with patch("redis.Redis") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_celery():
    """Mock Celery task execution."""
    with patch("celery.app.task.Task.delay") as mock:
        mock.return_value = MagicMock(id="test-task-id")
        yield mock


@pytest.fixture
def mock_pybrops():
    """Mock PyBrOpS API calls for agricultural tests."""
    with patch("pybrops.api") as mock:
        mock.return_value = MagicMock()
        yield mock


# ============================================
# Database Fixtures
# ============================================

@pytest.fixture
def company_data():
    """Company test data."""
    return {
        "name": "Test Company",
        "name_ar": "شركة الاختبار",
        "code": "TC001",
        "is_active": True,
    }


@pytest.fixture
def branch_data():
    """Branch test data."""
    return {
        "name": "Test Branch",
        "name_ar": "فرع الاختبار",
        "code": "TB001",
        "is_active": True,
    }


# ============================================
# Request Factory Fixtures
# ============================================

@pytest.fixture
def rf():
    """Django request factory."""
    from django.test import RequestFactory
    return RequestFactory()


@pytest.fixture
def authenticated_request(rf, test_user):
    """Create a request with authenticated user."""
    request = rf.get("/")
    request.user = test_user
    return request


# ============================================
# Cleanup Fixtures
# ============================================

@pytest.fixture(autouse=True)
def reset_sequences(db):
    """Reset database sequences after each test."""
    yield
    # Cleanup is handled by pytest-django


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before and after each test."""
    try:
        from django.core.cache import cache
        cache.clear()
    except (ImportError, Exception):
        pass
    yield
    try:
        from django.core.cache import cache
        cache.clear()
    except (ImportError, Exception):
        pass


# ============================================
# Test Data Factories
# ============================================

@pytest.fixture
def account_data():
    """Accounting account test data."""
    return {
        "name": "Test Account",
        "name_ar": "حساب الاختبار",
        "code": "1001",
        "account_type": "asset",
        "is_active": True,
    }


@pytest.fixture
def product_data():
    """Product test data for inventory."""
    return {
        "name": "Test Product",
        "name_ar": "منتج الاختبار",
        "sku": "PROD001",
        "price": "100.00",
        "quantity": 10,
        "is_active": True,
    }


@pytest.fixture
def contact_data():
    """Contact test data."""
    return {
        "name": "Test Contact",
        "email": "contact@test.com",
        "phone": "+966500000000",
        "contact_type": "customer",
        "is_active": True,
    }


# ============================================
# Settings Override Fixtures
# ============================================

@pytest.fixture
def override_settings():
    """Context manager for temporarily overriding settings."""
    from django.test import override_settings as django_override_settings
    return django_override_settings


@pytest.fixture
def temp_media_root(tmp_path):
    """Temporary media root for file upload tests."""
    from django.test import override_settings
    with override_settings(MEDIA_ROOT=str(tmp_path)):
        yield tmp_path
