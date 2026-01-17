from __future__ import annotations

import argparse
import json
import os
import sys
from importlib import import_module

from flask import Flask
from flask_smorest import Api

# Ensure `import src.*` works when running from repo root
THIS_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def get_bp(mod: str, name: str):
    try:
        m = import_module(mod)
        return getattr(m, name)
    except Exception:
        return None


def build_app() -> Flask:
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

    # Doc-focused blueprints (safe, no conflict with runtime endpoints)
    bp_specs = [
        # Real endpoints with OpenAPI documentation (flask-smorest)
        ("src.routes.auth_smorest", "auth_smorest_bp"),
        ("src.routes.products_smorest", "products_smorest_bp"),
        ("src.routes.inventory_smorest", "inventory_smorest_bp"),
        ("src.routes.invoices_smorest", "invoices_smorest_bp"),
        # Documentation-only endpoints
        ("src.routes.openapi_demo", "openapi_demo_bp"),
        ("src.routes.openapi_health", "openapi_health_bp"),
        ("src.routes.openapi_external_docs", "openapi_external_bp"),
    ]

    for mod, name in bp_specs:
        bp = get_bp(mod, name)
        if bp is not None:
            # inventory_smorest_bp and invoices_smorest_bp already have url_prefix
            if name in ["inventory_smorest_bp", "invoices_smorest_bp"]:
                api.register_blueprint(bp)
            else:
                api.register_blueprint(bp, url_prefix="/api")

    return app


def main():
    parser = argparse.ArgumentParser(description="Generate OpenAPI spec JSON")
    parser.add_argument(
        "--out", required=True, help="Output file path for OpenAPI JSON"
    )
    args = parser.parse_args()

    app = build_app()
    with app.test_client() as client:
        resp = client.get("/api/openapi.json")
        if resp.status_code != 200:
            raise SystemExit(
                f"Failed to generate OpenAPI spec: HTTP {resp.status_code}"
            )
        data = resp.json

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"OpenAPI spec written to: {out_path}")


if __name__ == "__main__":
    main()
