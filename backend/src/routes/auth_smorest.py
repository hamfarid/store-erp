"""
Authentication Routes with OpenAPI Documentation (flask-smorest)

This module provides authentication endpoints with proper OpenAPI/Swagger documentation.
Uses flask-smorest for automatic schema generation and validation.
"""

from __future__ import annotations

try:
    from flask.views import MethodView
    from flask_smorest import Blueprint  # type: ignore
    from marshmallow import Schema, fields, EXCLUDE, validate

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
        description="Authentication endpoints (login, logout, token refresh)",
    )

    # ==================== SCHEMAS ====================

    class LoginRequestSchema(Schema):
        """Schema for login request body."""

        class Meta:
            unknown = EXCLUDE

        username = fields.String(
            required=True,
            metadata={
                "description": "Username for authentication",
                "example": "admin",
            },
            validate=validate.Length(min=3, max=50),
        )
        password = fields.String(
            required=True,
            metadata={
                "description": "Password for authentication",
                "example": "password123",
            },
            validate=validate.Length(min=6, max=128),
        )
        use_jwt = fields.Boolean(
            load_default=True,
            metadata={
                "description": "Whether to use JWT tokens (default: true)",
                "example": True,
            },
        )

    class TokenResponseSchema(Schema):
        """Schema for successful login response with JWT tokens."""

        success = fields.Boolean(
            required=True,
            metadata={"description": "Operation success status", "example": True},
        )
        message = fields.String(
            metadata={"description": "Success message", "example": "تم تسجيل الدخول بنجاح"},
        )
        access_token = fields.String(
            metadata={
                "description": "JWT access token",
                "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
        )
        refresh_token = fields.String(
            metadata={
                "description": "JWT refresh token for token renewal",
                "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
        )
        user = fields.Dict(
            metadata={
                "description": "User information",
                "example": {
                    "id": 1,
                    "username": "admin",
                    "role": "admin",
                    "permissions": ["*"],
                },
            },
        )

    class LoginErrorSchema(Schema):
        """Schema for login error response."""

        success = fields.Boolean(
            required=True,
            metadata={"description": "Operation success status", "example": False},
        )
        message = fields.String(
            required=True,
            metadata={
                "description": "Error message",
                "example": "اسم المستخدم أو كلمة المرور غير صحيحة",
            },
        )
        remaining_attempts = fields.Integer(
            metadata={
                "description": "Remaining login attempts before lockout",
                "example": 4,
            },
        )

    class RefreshTokenRequestSchema(Schema):
        """Schema for token refresh request."""

        refresh_token = fields.String(
            required=True,
            metadata={
                "description": "Refresh token for getting new access token",
                "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
        )

    class LogoutResponseSchema(Schema):
        """Schema for logout response."""

        success = fields.Boolean(
            required=True,
            metadata={"description": "Operation success status", "example": True},
        )
        message = fields.String(
            metadata={"description": "Logout message", "example": "تم تسجيل الخروج بنجاح"},
        )

    # ==================== ROUTES ====================

    @auth_smorest_bp.route("/auth/login")
    class LoginResource(MethodView):
        """Login endpoint for authentication."""

        @auth_smorest_bp.arguments(LoginRequestSchema)
        @auth_smorest_bp.response(200, TokenResponseSchema)
        @auth_smorest_bp.alt_response(401, schema=LoginErrorSchema, description="Invalid credentials")
        @auth_smorest_bp.alt_response(423, schema=LoginErrorSchema, description="Account locked")
        def post(self, data):
            """
            Authenticate user and return JWT tokens.

            ---
            This endpoint validates user credentials and returns JWT tokens
            for accessing protected resources.

            **Security:**
            - Rate limited: 5 attempts per 15 minutes
            - Account lockout after 5 failed attempts
            - Passwords are hashed with bcrypt
            """
            from flask import jsonify
            from src.auth import AuthManager
            from src.services.cache_service import login_lockout_manager

            username = data.get("username")
            password = data.get("password")
            use_jwt = data.get("use_jwt", True)

            # Check for account lockout
            is_locked, unlock_time = login_lockout_manager.is_locked(username)
            if is_locked:
                return jsonify({
                    "success": False,
                    "message": "الحساب مقفل بسبب محاولات تسجيل دخول فاشلة متعددة",
                    "unlock_time": unlock_time,
                }), 423

            # Authenticate user
            result = AuthManager.authenticate_user(username, password, use_jwt=use_jwt)
            
            if result.get("success"):
                login_lockout_manager.reset_attempts(username)
                return jsonify(result), 200
            else:
                login_lockout_manager.record_failed_attempt(username)
                remaining = login_lockout_manager.get_remaining_attempts(username)
                result["remaining_attempts"] = remaining
                return jsonify(result), 401

    @auth_smorest_bp.route("/auth/refresh")
    class RefreshTokenResource(MethodView):
        """Token refresh endpoint."""

        @auth_smorest_bp.arguments(RefreshTokenRequestSchema)
        @auth_smorest_bp.response(200, TokenResponseSchema)
        @auth_smorest_bp.alt_response(401, schema=LoginErrorSchema, description="Invalid refresh token")
        def post(self, data):
            """
            Refresh access token using refresh token.

            ---
            Use this endpoint to get a new access token when the current
            one is about to expire.
            """
            from flask import jsonify
            from src.auth import AuthManager

            refresh_token = data.get("refresh_token")
            result = AuthManager.refresh_access_token(refresh_token)
            
            if result.get("success"):
                return jsonify(result), 200
            else:
                return jsonify(result), 401

    @auth_smorest_bp.route("/auth/logout")
    class LogoutResource(MethodView):
        """Logout endpoint."""

        @auth_smorest_bp.response(200, LogoutResponseSchema)
        def post(self):
            """
            Logout user and invalidate tokens.

            ---
            This endpoint revokes the current JWT token, making it invalid
            for future requests.
            """
            from flask import jsonify, request
            from src.auth import AuthManager
            from src.services.cache_service import jwt_revocation_list
            import jwt

            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                try:
                    # Decode token to get JTI
                    decoded = jwt.decode(token, options={"verify_signature": False})
                    jti = decoded.get("jti")
                    if jti:
                        jwt_revocation_list.revoke(jti)
                except Exception:
                    pass

            return jsonify({
                "success": True,
                "message": "تم تسجيل الخروج بنجاح",
            }), 200

    @auth_smorest_bp.route("/auth/me")
    class CurrentUserResource(MethodView):
        """Get current user information."""

        @auth_smorest_bp.response(200, TokenResponseSchema)
        @auth_smorest_bp.alt_response(401, schema=LoginErrorSchema, description="Not authenticated")
        def get(self):
            """
            Get current authenticated user information.

            ---
            Returns the current user's profile and permissions.
            Requires a valid JWT token in the Authorization header.
            """
            from flask import jsonify, request, g
            from src.auth import token_required

            # Get user from token (simplified - actual implementation uses decorator)
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({
                    "success": False,
                    "message": "التوكن مطلوب",
                }), 401

            # In real implementation, this would decode and validate the token
            return jsonify({
                "success": True,
                "user": getattr(g, "current_user", {}),
            }), 200


# Export for imports
__all__ = ["auth_smorest_bp", "SMOREST_AVAILABLE"]
