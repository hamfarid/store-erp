from __future__ import annotations

try:
    from flask.views import MethodView
    from flask_smorest import Blueprint  # type: ignore
    from marshmallow import Schema, fields

    SMOREST_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    Blueprint = None  # type: ignore
    MethodView = None  # type: ignore
    Schema = None  # type: ignore
    fields = None  # type: ignore
    SMOREST_AVAILABLE = False


# Only define the blueprint if flask_smorest is available
auth_smorest_bp = None
if SMOREST_AVAILABLE and Blueprint is not None:
    auth_smorest_bp = Blueprint(
        "auth_smorest",
        __name__,
        description="Real Auth endpoints (migrated to flask-smorest)",
    )

    class LoginRequestSchema(Schema):
        """Login request with username and password."""

        username = fields.String(
            required=True,
            metadata={"description": "Username for authentication", "example": "admin"},
        )
        password = fields.String(
            required=True,
            load_only=True,
            metadata={
                "description": "User password (min 8 characters)",
                "example": "Secret123!",
            },
        )

    class UserSchema(Schema):
        """User information returned in login response."""

        id = fields.Integer(required=True, metadata={"example": 1})
        username = fields.String(required=True, metadata={"example": "admin"})
        email = fields.String(metadata={"example": "admin@example.com"})
        role = fields.String(metadata={"example": "admin"})
        is_active = fields.Boolean(metadata={"example": True})

    class LoginDataSchema(Schema):
        """Login response data containing tokens and user info."""

        access_token = fields.String(
            required=True,
            metadata={
                "description": "JWT access token (15 min expiry)",
                "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
        )
        refresh_token = fields.String(
            required=True,
            metadata={
                "description": "JWT refresh token (7 days expiry)",
                "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
        )
        user = fields.Nested(
            UserSchema,
            required=True,
            metadata={"description": "Authenticated user information"},
        )
        expires_in = fields.Integer(
            required=True,
            metadata={"description": "Access token expiry in seconds", "example": 900},
        )

    class LoginResponseSchema(Schema):
        """Standard API response envelope for login."""

        success = fields.Boolean(
            required=True,
            metadata={"description": "Request success status", "example": True},
        )
        data = fields.Nested(
            LoginDataSchema,
            required=True,
            metadata={"description": "Login response data"},
        )

        # Compatibility fields for integration tests expecting top-level keys
        access_token = fields.String(
            dump_only=True,
            metadata={"description": "JWT access token (top-level alias)"},
        )
        refresh_token = fields.String(
            dump_only=True,
            metadata={"description": "JWT refresh token (top-level alias)"},
        )
        user = fields.Nested(
            UserSchema,
            dump_only=True,
            metadata={"description": "Authenticated user (top-level alias)"},
        )
        expires_in = fields.Integer(
            dump_only=True,
            metadata={"description": "Access token expiry in seconds (alias)"},
        )
        message = fields.String(
            required=True,
            metadata={
                "description": "Response message (Arabic)",
                "example": "تم تسجيل الدخول بنجاح",
            },
        )

    @auth_smorest_bp.route("/auth/login")
    class LoginView(MethodView):
        @auth_smorest_bp.arguments(LoginRequestSchema)
        @auth_smorest_bp.response(200, LoginResponseSchema)
        def post(self, json_data):
            """Login using username/password and return JWT tokens (real endpoint)."""
            # Import here to avoid circular imports and missing dependencies
            from datetime import timedelta
            from src.database import db
            from src.models.user import User, AccountLockedError
            from src.jwt_manager import JWTManager
            import logging

            logger = logging.getLogger(__name__)

            username = (json_data or {}).get("username", "").strip()
            password = (json_data or {}).get("password", "")

            if not username or not password:
                # Keep response envelope consistent
                return {
                    "success": False,
                    "data": {},
                    "message": "Username and password are required",
                }, 400

            try:
                # Authenticate user (active users only)
                user = User.authenticate(username, password)
            except AccountLockedError as e:
                return {
                    "success": False,
                    "data": {"remaining_seconds": e.remaining_seconds},
                    "message": str(e.message),
                }, 423  # HTTP 423 Locked
            except Exception as e:
                logger.error(f"Authentication error: {e}")
                return {
                    "success": False,
                    "data": {},
                    "message": "Authentication error occurred",
                }, 500

            if not user:
                return {
                    "success": False,
                    "data": {},
                    "message": "Invalid username or password",
                }, 401

            # Update last login (best-effort)
            try:
                user.last_login = getattr(user, "last_login", None)
                db.session.commit()
            except Exception:  # pragma: no cover - non-critical
                db.session.rollback()

            try:
                # Issue tokens
                access_token = JWTManager.create_access_token(user.id)
                refresh_token, _jti, _exp = JWTManager.create_refresh_token(user.id)
            except Exception as e:
                logger.error(f"Token generation error: {e}")
                return {
                    "success": False,
                    "data": {},
                    "message": "Token generation failed",
                }, 500

            # Expires in seconds (aligning with prior docs 3600s)
            try:
                expires_in = int(timedelta(minutes=15).total_seconds())
            except Exception:  # pragma: no cover
                expires_in = 3600

            return {
                "success": True,
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": (
                        user.to_dict()
                        if hasattr(user, "to_dict")
                        else {"id": user.id, "username": user.username}
                    ),
                    "expires_in": expires_in,
                },
                # Duplicate keys at the top level for legacy/tests
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": (
                    user.to_dict()
                    if hasattr(user, "to_dict")
                    else {"id": user.id, "username": user.username}
                ),
                "expires_in": expires_in,
                "message": "تم تسجيل الدخول بنجاح",
            }, 200
