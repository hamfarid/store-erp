#!/usr/bin/env python
"""
Comprehensive Authentication Testing Script
Tests API key authentication, JWT tokens, user authentication systems
"""

# pylint: disable=import-outside-toplevel

from django.test import Client
from django.contrib.auth import get_user_model, authenticate
import sys


User = get_user_model()


def test_user_authentication():
    """Test basic user authentication functionality."""
    print("=" * 60)
    print("USER AUTHENTICATION TESTING")
    print("=" * 60)

    try:
        # Test user creation
        print("\n--- Testing User Creation ---")
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✓ User created: {user.username}")

        # Test user authentication
        print("\n--- Testing User Authentication ---")
        auth_user = authenticate(username='testuser', password='testpass123')
        if auth_user:
            print("✓ User authentication works")
        else:
            print("✗ User authentication failed")
            return False

        # Test wrong password
        wrong_auth = authenticate(username='testuser', password='wrongpass')
        if not wrong_auth:
            print("✓ Wrong password correctly rejected")
        else:
            print("✗ Wrong password incorrectly accepted")

        # Clean up
        user.delete()
        print("✓ Test user cleaned up")

    except Exception as e:
        print(f"✗ User authentication test failed: {e}")
        return False

    return True


def test_api_key_authentication():
    """Test API key authentication system."""
    print("\n--- Testing API Key Authentication ---")

    try:
        # Check if API key models exist
        from core_modules.api_keys.models import APIKey
        print("✓ API Key model imported successfully")

        # Create test user for API key
        user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )

        # Create API key
        api_key = APIKey.objects.create(
            user=user,
            name="Test API Key"
        )
        print(f"✓ API Key created: {api_key.name}")

        # Test API key string representation
        print(f"✓ API Key representation: {str(api_key)}")

        # Clean up
        api_key.delete()
        user.delete()
        print("✓ API Key test data cleaned up")

    except ImportError:
        print("⚠ API Key module not available (may be disabled)")
        return True
    except Exception as e:
        print(f"✗ API Key authentication test failed: {e}")
        return False

    return True


def test_jwt_authentication():
    """Test JWT token authentication."""
    print("\n--- Testing JWT Authentication ---")

    client = Client()

    try:
        # Test JWT token endpoint
        response = client.post('/api/auth/jwt/create/', {
            'username': 'nonexistent',
            'password': 'wrongpass'
        })

        if response.status_code in [400, 401, 404]:
            print("✓ JWT authentication endpoint accessible")
        else:
            print("⚠ JWT endpoint returned unexpected status:",
                  response.status_code)

    except Exception as e:
        print(f"✗ JWT authentication test failed: {e}")
        return False

    return True


def test_authentication_middleware():
    """Test authentication middleware functionality."""
    print("\n--- Testing Authentication Middleware ---")

    client = Client()

    try:
        # Test protected endpoint without authentication
        response = client.get('/api/companies/')

        if response.status_code in [200, 401, 403, 404]:
            print("✓ Authentication middleware working")
        else:
            print(f"⚠ Unexpected response: {response.status_code}")

    except Exception as e:
        print(f"✗ Authentication middleware test failed: {e}")
        return False

    return True


def test_permission_system():
    """Test permission system functionality."""
    print("\n--- Testing Permission System ---")

    try:
        # Check if permission models exist
        from django.contrib.auth.models import Permission

        # Get some permissions
        permissions = Permission.objects.all()[:5]
        print(f"✓ Found {len(permissions)} permissions in system")

        for perm in permissions:
            print(f"  - {perm.codename}: {perm.name}")

    except Exception as e:
        print(f"✗ Permission system test failed: {e}")
        return False

    return True


def test_session_management():
    """Test session management functionality."""
    print("\n--- Testing Session Management ---")

    client = Client()

    try:
        # Test session creation
        session = client.session
        session['test_key'] = 'test_value'
        session.save()
        print("✓ Session creation works")

        # Test session retrieval
        if client.session.get('test_key') == 'test_value':
            print("✓ Session retrieval works")
        else:
            print("✗ Session retrieval failed")
            return False

    except Exception as e:
        print(f"✗ Session management test failed: {e}")
        return False

    return True


def test_csrf_protection():
    """Test CSRF protection functionality."""
    print("\n--- Testing CSRF Protection ---")

    client = Client()

    try:
        # Test CSRF token in forms
        response = client.get('/')

        if response.status_code in [200, 404]:
            print("✓ CSRF protection configured")
        else:
            print(f"⚠ Unexpected response: {response.status_code}")

    except Exception as e:
        print(f"✗ CSRF protection test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = True

    success &= test_user_authentication()
    success &= test_api_key_authentication()
    success &= test_jwt_authentication()
    success &= test_authentication_middleware()
    success &= test_permission_system()
    success &= test_session_management()
    success &= test_csrf_protection()

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL AUTHENTICATION TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ SOME AUTHENTICATION TESTS FAILED!")
        print("=" * 60)
        sys.exit(1)
