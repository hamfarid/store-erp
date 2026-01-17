import json
import pytest
from flask import Flask

try:
    from flask_smorest import Api
    from src.routes.openapi_external_docs import openapi_external_bp
    from src.routes.auth_smorest import auth_smorest_bp
    from src.routes.products_smorest import products_smorest_bp

    SMOREST_AVAILABLE = True
except Exception:
    Api = None
    openapi_external_bp = None
    auth_smorest_bp = None
    products_smorest_bp = None
    SMOREST_AVAILABLE = False
    pytestmark = pytest.mark.skip("flask-smorest not available in this environment")


def test_spec_contains_auth_products_external_docs():
    app = Flask(__name__)
    app.config.update(
        API_TITLE="Store ERP API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/api",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    )
    api = Api(app)
    for bp in (openapi_external_bp, auth_smorest_bp, products_smorest_bp):
        if bp is not None:
            api.register_blueprint(bp, url_prefix="/api")

    client = app.test_client()
    spec = client.get("/api/openapi.json")
    assert spec.status_code == 200
    data = spec.json if hasattr(spec, "json") else json.loads(spec.data)
    paths = data.get("paths", {})
    # Real endpoints with OpenAPI documentation
    assert "/api/auth/login" in paths
    assert "/api/products" in paths
    # Documentation-only endpoints
    assert "/api/docs-integration/external/health" in paths
