from __future__ import annotations

import json

import os
import sys
import pytest
from flask import Flask

# Optional dependency: flask-smorest
try:
    from flask_smorest import Api
except Exception:  # pragma: no cover
    Api = None  # type: ignore
    pytestmark = pytest.mark.skip("flask-smorest not available in this environment")

# Ensure backend/src is importable in PyTest context
backend_path = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
# Defer import after sys.path updated
from src.routes.openapi_demo import openapi_demo_bp


def test_openapi_ui_and_spec_available():
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
    if openapi_demo_bp is not None:
        api.register_blueprint(openapi_demo_bp, url_prefix="/api")

    client = app.test_client()

    # Swagger UI
    ui = client.get("/api/docs")
    assert ui.status_code in (200, 302)  # some setups may redirect
    assert b"Swagger UI" in ui.data or b"swagger-ui" in ui.data or ui.status_code == 302

    # OpenAPI JSON
    spec = client.get("/api/openapi.json")
    assert spec.status_code == 200
    data = spec.json if hasattr(spec, "json") else json.loads(spec.data)
    assert isinstance(data, dict)
    assert "openapi" in data

    # our demo path should be present (prefixed by /api due to registration)
    paths = data.get("paths", {})
    assert "/api/docs-demo/ping" in paths
