#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared Test Configuration and Fixtures
========================================

This file provides:
- Global pytest configuration hooks
- Shared test fixtures for all test modules
- Database setup and teardown for test isolation
"""

import pytest
import os
import sys

# Add backend/src to path - must be before imports
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(backend_path, "src")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# These imports MUST come after sys.path modification
try:
    from src.main import create_app
except ImportError:
    # Fail fast if source is broken
    raise ImportError("Could not import create_app from src.main")

from src.database import db  # noqa: E402


def _preload_models():
    """Import core models so SQLAlchemy metadata includes FK targets.

    Tests call `db.drop_all()`/`db.create_all()` directly; without importing models
    first, SQLAlchemy may not have all referenced tables registered.
    """

    try:
        from src.models.user import User, Role  # noqa: F401
    except ImportError:
        try:
            from models.user import User, Role  # type: ignore  # noqa: F401  # pylint: disable=import-error
        except Exception:
            pass

    try:
        from src.models.sales_engineer import SalesEngineer  # noqa: F401
    except ImportError:
        try:
            from models.sales_engineer import SalesEngineer  # type: ignore  # noqa: F401  # pylint: disable=import-error
        except Exception:
            pass

    try:
        from src.models.customer import Customer  # noqa: F401
    except ImportError:
        try:
            from models.customer import Customer  # type: ignore  # noqa: F401  # pylint: disable=import-error
        except Exception:
            pass

    try:
        from src.models.supplier import Supplier  # noqa: F401
    except ImportError:
        try:
            from models.supplier import Supplier  # type: ignore  # noqa: F401  # pylint: disable=import-error
        except Exception:
            pass

    try:
        from src.models.inventory import Category, Product, Warehouse  # noqa: F401
    except ImportError:
        try:
            # pylint: disable=import-error
            from models.inventory import (  # type: ignore  # noqa: F401
                Category,
                Product,
                Warehouse,
            )
        except Exception:
            pass


# Session setup hook
def pytest_configure(config):
    """Setup for entire test session"""
    pass  # Can add logging, env setup here


# Post-test cleanup hook
def pytest_runtest_teardown():
    """Run after EACH test - cleanup"""
    # Clean up ANY active context
    pass


# Moved fixture from test_api_integration.py
@pytest.fixture(scope="function")
def test_app():
    """Create test application with function scope (fresh per test)"""
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests
    with app.app_context():
        _preload_models()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")  # Changed from 'module'
def client(test_app):
    """Create test client with function scope (fresh per test)"""
    return test_app.test_client()


@pytest.fixture(scope="function")
def db_session(test_app):
    """Create session with transaction rollback (fresh per test)"""
    with test_app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        yield db.session

        db.session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def test_user(test_app):
    """Create and seed a test user, return dict with user data"""
    with test_app.app_context():
        from src.models.user import User, Role
        from src.database import db
        from werkzeug.security import generate_password_hash
        
        # Ensure role exists
        role = Role.query.filter_by(name="user").first()
        if not role:
            role = Role(name="user", description="User Role")
            db.session.add(role)
            db.session.commit()
            
        user = User(
            username="testuser",
            email="testuser@example.com",
            full_name="Test User",
            role_id=role.id,
            password_hash=generate_password_hash("password123"),
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        # Return dict to avoid DetachedInstanceError
        return {"id": user.id, "username": user.username, "role": "user"}


@pytest.fixture(scope="function")
def auth_headers(test_app, test_user):
    """Generate headers with valid user token"""
    with test_app.app_context():
        from src.auth import AuthManager
        try:
            tokens = AuthManager.generate_jwt_tokens(
                user_id=test_user["id"], username=test_user["username"], role=test_user["role"]
            )
            return {"Authorization": f"Bearer {tokens['access_token']}"}
        except Exception:
            return {}

@pytest.fixture(scope="function")
def test_admin(test_app):
    """Create and seed an admin user, return dict with user data"""
    with test_app.app_context():
        from src.models.user import User, Role
        from src.database import db
        from werkzeug.security import generate_password_hash
        
        # Ensure role exists
        role = Role.query.filter_by(name="مدير النظام").first()
        if not role:
            role = Role(name="مدير النظام", description="Admin Role")
            db.session.add(role)
            db.session.commit()
            
        user = User(
            username="adminuser",
            email="admin@example.com",
            full_name="Admin User",
            role_id=role.id,
            password_hash=generate_password_hash("admin123"),
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        # Return dict to avoid DetachedInstanceError
        return {"id": user.id, "username": user.username, "role": "مدير النظام"}


@pytest.fixture(scope="function")
def admin_auth_headers(test_app, test_admin):
    """Generate headers with valid admin token"""
    with test_app.app_context():
        from src.auth import AuthManager
        try:
            tokens = AuthManager.generate_jwt_tokens(
                user_id=test_admin["id"], username=test_admin["username"], role=test_admin["role"]
            )
            return {"Authorization": f"Bearer {tokens['access_token']}"}
        except Exception:
            return {}


@pytest.fixture(scope="function")
def sample_product(test_app):
    """Seed a sample product, return dict with product data"""
    with test_app.app_context():
        from src.models.inventory import Product, Category
        from src.database import db
        
        # Create category first
        cat = Category(name="Test Category", description="Test Desc")
        db.session.add(cat)
        db.session.commit()
        
        product = Product(
            name="Seeded Product",
            sku="SEED-001",
            description="Test Desc",
            cost_price=50.0,
            selling_price=100.0,
            current_stock=10,
            category_id=cat.id,
            is_active=True
        )
        db.session.add(product)
        db.session.commit()
        
        # Refresh to get ID
        db.session.refresh(product)
        # Return dict to avoid DetachedInstanceError
        return {"id": product.id, "name": product.name, "sku": product.sku}
