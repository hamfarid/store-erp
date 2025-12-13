import json
import pytest
from flask import Flask

try:
    from flask_smorest import Api
except Exception:
    Api = None
    pytestmark = pytest.mark.skip("flask-smorest not available in this environment")

from src.routes.openapi_health import openapi_health_bp


def test_health_openapi_and_route():
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

    if openapi_health_bp is not None:
        api.register_blueprint(openapi_health_bp, url_prefix="/api")

    client = app.test_client()

    # spec JSON
    spec = client.get("/api/openapi.json")
    assert spec.status_code == 200
    data = spec.json if hasattr(spec, "json") else json.loads(spec.data)
    assert "/api/system/health" in data.get("paths", {})

    # route call
    resp = client.get("/api/system/health")
    assert resp.status_code == 200
    payload = resp.json if hasattr(resp, "json") else json.loads(resp.data)
    assert payload.get("status") == "ok"
