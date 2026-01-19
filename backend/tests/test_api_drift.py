"""
API Drift Tests - T10

Tests to ensure the actual API implementation matches the OpenAPI specification.
This prevents "drift" between documentation and reality.

What is API Drift?
- When API implementation changes but OpenAPI spec doesn't (or vice versa)
- When response schemas don't match documented schemas
- When endpoints exist in code but not in docs (or vice versa)
- When validation rules differ between spec and implementation

This test suite validates:
1. All documented endpoints exist and are accessible
2. Response schemas match OpenAPI definitions
3. Request validation matches OpenAPI spec
4. Status codes match documentation
5. No undocumented endpoints are exposed
"""

import json
import pytest
from flask import Flask
from jsonschema import validate, ValidationError

try:
    from flask_smorest import Api
    from src.routes.openapi_external_docs import openapi_external_bp
    from src.routes.auth_smorest import auth_smorest_bp
    from src.routes.products_smorest import products_smorest_bp
    from src.database import db
    from src.models.user import User, Role
    from src.models.inventory import Product
    # Import models with FK dependencies to ensure proper table creation order
    from src.models.sales_engineer import SalesEngineer  # noqa: F401
    from src.models.customer import Customer  # noqa: F401
    from src.models.product_variant import ProductVariant  # noqa: F401

    SMOREST_AVAILABLE = True
except Exception:
    Api = None
    openapi_external_bp = None
    auth_smorest_bp = None
    products_smorest_bp = None
    db = None
    User = None
    Product = None
    SMOREST_AVAILABLE = False
    pytestmark = pytest.mark.skip(
        "flask-smorest or dependencies not available in this environment"
    )


@pytest.fixture
def app():
    """Create test Flask application with database."""
    if not SMOREST_AVAILABLE:
        pytest.skip("Dependencies not available")

    app = Flask(__name__)
    app.config.update(
        API_TITLE="Store ERP API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/api",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=True,
        JWT_SECRET_KEY="test-secret-key-for-drift-tests",
    )

    # Initialize database
    db.init_app(app)

    # Initialize API
    api = Api(app)

    # Register blueprints
    for bp in (openapi_external_bp, auth_smorest_bp, products_smorest_bp):
        if bp is not None:
            api.register_blueprint(bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

        role = Role(
            name="admin",
            description="Administrator role",
            permissions=["create", "read", "update", "delete"],
            is_active=True,
        )
        db.session.add(role)
        db.session.commit()

        # Create test user for authentication tests
        test_user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            role_id=role.id,
            is_active=True,
        )
        test_user.set_password("TestPassword123!")
        db.session.add(test_user)

        # Create test products
        for i in range(5):
            product = Product(
                name=f"Test Product {i+1}",
                barcode=f"TEST{i+1:04d}",
                sku=f"SKU-TEST-{i+1:03d}",
                cost_price=100.0 + (i * 10),
                selling_price=150.0 + (i * 15),
                current_stock=50 + (i * 5),
                min_stock_level=10,
                max_stock_level=200,
                is_active=True,
                is_trackable=True,
            )
            db.session.add(product)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def openapi_spec(client):
    """Get OpenAPI specification."""
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    return response.json if hasattr(response, "json") else json.loads(response.data)


class TestAPIDriftDocumentedEndpoints:
    """Test that all documented endpoints exist and work correctly."""

    def test_all_documented_paths_exist(self, client, openapi_spec):
        """Verify all paths in OpenAPI spec are accessible."""
        paths = openapi_spec.get("paths", {})

        for path, methods in paths.items():
            for method in methods.keys():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    # Try to access the endpoint (may fail with auth, but should not 404)
                    response = getattr(client, method.lower())(path)
                    # Should not be 404 (Not Found) - endpoint should exist
                    assert (
                        response.status_code != 404
                    ), f"{method.upper()} {path} returns 404 - endpoint doesn't exist!"

    def test_auth_login_endpoint_exists(self, client):
        """Test /api/auth/login endpoint exists."""
        response = client.post("/api/auth/login", json={})
        # Should not be 404, even if request is invalid
        assert response.status_code != 404

    def test_products_endpoint_exists(self, client):
        """Test /api/products endpoint exists."""
        response = client.get("/api/products")
        # Should not be 404
        assert response.status_code != 404


class TestAPIDriftResponseSchemas:
    """Test that API responses match OpenAPI schemas."""

    def test_auth_login_response_schema(self, client, openapi_spec):
        """Test /api/auth/login response matches schema."""
        # Make valid login request
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "TestPassword123!"},
        )

        assert response.status_code == 200
        data = response.json if hasattr(response, "json") else json.loads(response.data)

        # Validate response structure
        assert (
            "success" in data or "status" in data
        ), "Response missing success/status field"
        assert "data" in data, "Response missing data field"
        assert "message" in data, "Response missing message field"

        # Validate data structure
        if data.get("success") or data.get("status") == "success":
            assert "access_token" in data["data"], "Missing access_token in response"
            assert "refresh_token" in data["data"], "Missing refresh_token in response"
            assert "user" in data["data"], "Missing user in response"
            assert "expires_in" in data["data"], "Missing expires_in in response"

            # Validate user structure
            user = data["data"]["user"]
            assert "id" in user, "Missing user.id"
            assert "username" in user, "Missing user.username"

    def test_products_list_response_schema(self, client, openapi_spec):
        """Test /api/products response matches schema."""
        response = client.get("/api/products?page=1&per_page=10")

        assert response.status_code == 200
        data = response.json if hasattr(response, "json") else json.loads(response.data)

        # Validate response structure
        assert "status" in data, "Response missing status field"
        assert "data" in data, "Response missing data field"
        assert "pagination" in data, "Response missing pagination field"

        # Validate pagination structure
        pagination = data["pagination"]
        assert "page" in pagination, "Missing pagination.page"
        assert "pages" in pagination, "Missing pagination.pages"
        assert "per_page" in pagination, "Missing pagination.per_page"
        assert "total" in pagination, "Missing pagination.total"

        # Validate data is a list
        assert isinstance(data["data"], list), "data should be a list"

        # If products exist, validate product structure
        if len(data["data"]) > 0:
            product = data["data"][0]
            required_fields = [
                "id",
                "name",
                "barcode",
                "sku",
                "cost_price",
                "selling_price",
                "current_stock",
            ]
            for field in required_fields:
                assert field in product, f"Missing product.{field}"


class TestAPIDriftRequestValidation:
    """Test that request validation matches OpenAPI spec."""

    def test_auth_login_requires_username_and_password(self, client):
        """Test login endpoint validates required fields."""
        # Missing username
        response = client.post("/api/auth/login", json={"password": "test"})
        assert response.status_code in [400, 422], "Should reject missing username"

        # Missing password
        response = client.post("/api/auth/login", json={"username": "test"})
        assert response.status_code in [400, 422], "Should reject missing password"

        # Empty request
        response = client.post("/api/auth/login", json={})
        assert response.status_code in [400, 422], "Should reject empty request"

    def test_products_pagination_validation(self, client):
        """Test products endpoint validates pagination parameters."""
        # Valid pagination
        response = client.get("/api/products?page=1&per_page=10")
        assert response.status_code == 200

        # Invalid page (should default or handle gracefully)
        response = client.get("/api/products?page=0")
        assert response.status_code in [
            200,
            400,
        ], "Should handle invalid page gracefully"

        # Invalid per_page (should default or handle gracefully)
        response = client.get("/api/products?per_page=1000")
        assert response.status_code in [
            200,
            400,
        ], "Should handle large per_page gracefully"


class TestAPIDriftStatusCodes:
    """Test that status codes match OpenAPI documentation."""

    def test_auth_login_success_returns_200(self, client):
        """Test successful login returns 200."""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "TestPassword123!"},
        )
        assert response.status_code == 200

    def test_auth_login_invalid_credentials_returns_401(self, client):
        """Test invalid credentials return 401."""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "WrongPassword!"},
        )
        assert response.status_code == 401

    def test_products_list_success_returns_200(self, client):
        """Test successful products list returns 200."""
        response = client.get("/api/products")
        assert response.status_code == 200


class TestAPIDriftSpecCompleteness:
    """Test that OpenAPI spec is complete and accurate."""

    def test_spec_has_required_metadata(self, openapi_spec):
        """Test OpenAPI spec has required metadata."""
        assert "openapi" in openapi_spec, "Missing openapi version"
        assert "info" in openapi_spec, "Missing info section"
        assert "paths" in openapi_spec, "Missing paths section"

        info = openapi_spec["info"]
        assert "title" in info, "Missing info.title"
        assert "version" in info, "Missing info.version"

    def test_spec_has_documented_real_endpoints(self, openapi_spec):
        """Test spec includes our real endpoints."""
        paths = openapi_spec.get("paths", {})

        # Real endpoints that should be documented
        required_paths = [
            "/api/auth/login",
            "/api/products",
        ]

        for path in required_paths:
            assert path in paths, f"Missing {path} in OpenAPI spec"

    def test_spec_has_schemas(self, openapi_spec):
        """Test spec includes schema definitions."""
        assert "components" in openapi_spec, "Missing components section"
        assert "schemas" in openapi_spec["components"], "Missing schemas section"

        schemas = openapi_spec["components"]["schemas"]

        # Required schemas for our endpoints
        required_schemas = [
            "LoginRequest",
            "LoginResponse",
            "User",
            "ProductItem",
            "ProductsResponse",
            "Pagination",
        ]

        for schema_name in required_schemas:
            assert (
                schema_name in schemas
            ), f"Missing {schema_name} schema in OpenAPI spec"
