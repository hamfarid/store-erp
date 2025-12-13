from __future__ import annotations

try:  # pragma: no cover - import guarded to avoid breaking runtime if optional dep missing
    from flask_smorest import Blueprint
    from marshmallow import Schema, fields
except Exception as _e:  # pragma: no cover
    Blueprint = None  # type: ignore
    Schema = object  # type: ignore
    fields = None  # type: ignore

# Define blueprint only if flask-smorest is available
if Blueprint is not None:
    openapi_demo_bp = Blueprint(
        "openapi_demo", __name__, description="OpenAPI demo endpoints"
    )

    class PingResponseSchema(Schema):
        message = fields.String(required=True)

    from flask.views import MethodView

    @openapi_demo_bp.route("/docs-demo/ping")
    class PingView(MethodView):
        @openapi_demo_bp.response(200, PingResponseSchema)
        def get(self):
            """Simple documented endpoint for the OpenAPI bootstrap"""
            return {"message": "pong"}

else:  # pragma: no cover
    openapi_demo_bp = None  # type: ignore
