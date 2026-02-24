import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_env():
    """Mock environment variables for testing."""
    os.environ["ENV"] = "test"
    os.environ["DB_URL"] = "sqlite:///:memory:"
    yield
    del os.environ["ENV"]
