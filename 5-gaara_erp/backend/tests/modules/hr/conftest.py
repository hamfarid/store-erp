"""
Pytest configuration for HR module tests.

These tests are pure unit tests that don't require database setup.
The parent conftest.py (tests/conftest.py) automatically skips database
setup for tests in the 'tests/modules/hr' directory.
"""
import pytest


# Register custom markers
def pytest_configure(config):
    """Configure pytest for HR tests."""
    config.addinivalue_line(
        "markers", "unit: mark test as a pure unit test without database"
    )


# Mark all tests in this module as unit tests
def pytest_collection_modifyitems(session, config, items):
    """Add unit marker to all tests in HR module."""
    for item in items:
        if 'modules/hr' in str(item.fspath) or 'modules\\hr' in str(item.fspath):
            item.add_marker(pytest.mark.unit)


# Provide mock fixtures for unit tests (optional - tests don't use these)
@pytest.fixture
def db():
    """Mock database fixture - not used in HR unit tests."""
    yield None


@pytest.fixture
def app():
    """Mock app fixture - not used in HR unit tests."""
    yield None


@pytest.fixture
def client():
    """Mock client fixture - not used in HR unit tests."""
    yield None
