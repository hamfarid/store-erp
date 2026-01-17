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
    from src.main import app  # noqa: E402
except ImportError:
    # Fallback to create a minimal test app
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "test-secret-key"

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

    # Advanced models must load BEFORE purchase models (FK dependencies)
    try:
        from src.models.product_advanced import ProductAdvanced  # noqa: F401
        from src.models.lot_advanced import LotAdvanced  # noqa: F401
    except ImportError:
        pass

    try:
        from src.models.purchase_order import PurchaseOrder  # noqa: F401
        from src.models.purchase_order_item import PurchaseOrderItem  # noqa: F401
        from src.models.purchase_receipt import PurchaseReceipt  # noqa: F401
    except ImportError:
        pass


# Session setup hook
def pytest_configure(config):
    """Setup for entire test session"""
    pass  # Can add logging, env setup here


# Pre-test cleanup hook
def pytest_runtest_setup(item):
    """Run before EACH test - ensure fresh database"""
    # Skip database setup for pure unit tests (e.g., HR module tests)
    # These tests are marked by being in specific directories
    test_path = str(item.fspath)
    
    # Skip database setup for these test directories
    skip_db_paths = [
        'tests/modules/hr',
        'tests\\modules\\hr',  # Windows path
    ]
    
    should_skip_db = any(skip_path in test_path for skip_path in skip_db_paths)
    
    if should_skip_db:
        # Skip database setup for pure unit tests
        return
    
    try:
        with app.app_context():
            _preload_models()
            db.session.remove()
            db.drop_all()
            db.create_all()  # Fresh database!
    except RuntimeError:
        # App context might not be available yet
        pass


# Post-test cleanup hook
def pytest_runtest_teardown(item):
    """Run after EACH test - cleanup"""
    # Skip teardown for pure unit tests
    test_path = str(item.fspath)
    
    skip_db_paths = [
        'tests/modules/hr',
        'tests\\modules\\hr',  # Windows path
    ]
    
    should_skip_db = any(skip_path in test_path for skip_path in skip_db_paths)
    
    if should_skip_db:
        return
    
    try:
        with app.app_context():
            db.session.remove()
    except RuntimeError:
        pass


# Moved fixture from test_api_integration.py
@pytest.fixture(scope="function")  # Changed from 'module'
def test_app():
    """Create test application with function scope (fresh per test)"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        yield app


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
