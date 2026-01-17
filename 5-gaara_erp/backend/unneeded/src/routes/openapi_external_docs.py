from __future__ import annotations

try:  # pragma: no cover
    from flask_smorest import Blueprint
    from marshmallow import Schema, fields
    from flask.views import MethodView
except Exception:  # pragma: no cover
    Blueprint = None  # type: ignore
    Schema = object  # type: ignore
    fields = None  # type: ignore
    MethodView = object  # type: ignore

if Blueprint is not None:
    openapi_external_bp = Blueprint(
        "openapi_external_docs",
        __name__,
        description="External integration endpoints (documentation slice)",
    )

    class ExternalHealthResponse(Schema):
        service = fields.String(required=True, example="httpbin")
        url = fields.String(required=True, example="https://httpbin.org/status/200")
        ok = fields.Boolean(required=True, example=True)
        status_code = fields.Integer(required=True, example=200)
        elapsed_ms = fields.Integer(required=True, example=42)

    @openapi_external_bp.route("/docs-integration/external/health")
    class ExternalHealthView(MethodView):
        @openapi_external_bp.response(200, ExternalHealthResponse)
        def get(self):  # pragma: no cover - sample response only
            """Documented external health (sample response for spec)."""
            return {
                "service": "httpbin",
                "url": "https://httpbin.org/status/200",
                "ok": True,
                "status_code": 200,
                "elapsed_ms": 10,
            }

else:  # pragma: no cover
    openapi_external_bp = None  # type: ignore
