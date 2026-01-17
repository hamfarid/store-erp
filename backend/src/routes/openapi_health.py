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
    openapi_health_bp = Blueprint(
        "openapi_health", __name__, description="System health"
    )

    class HealthResponseSchema(Schema):
        status = fields.String(required=True, metadata={"example": "ok"})
        service = fields.String(required=True, metadata={"example": "store-erp"})
        version = fields.String(required=True, metadata={"example": "v1"})

    @openapi_health_bp.route("/system/health")
    class HealthView(MethodView):
        @openapi_health_bp.response(200, HealthResponseSchema)
        def get(self):
            return {"status": "ok", "service": "store-erp", "version": "v1"}

else:  # pragma: no cover
    openapi_health_bp = None  # type: ignore
