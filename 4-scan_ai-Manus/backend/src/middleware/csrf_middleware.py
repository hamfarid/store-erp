"""
FILE: backend/src/middleware/csrf_middleware.py
PURPOSE: CSRF protection middleware
OWNER: Security Team
LAST-AUDITED: 2025-11-18

CSRF (Cross-Site Request Forgery) Protection Middleware

This middleware implements token-based CSRF protection for all
state-changing requests. It generates and validates CSRF tokens to
prevent unauthorized requests.

Security Features:
- Token generation with cryptographic randomness
- Token validation for POST, PUT, PATCH, DELETE requests
- Configurable token expiry
- Secure token storage in HTTP-only cookies
- Double-submit cookie pattern

Version: 1.0.0
"""

import hashlib
import hmac
import secrets
import time
from typing import Callable, Optional

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class CSRFMiddleware(BaseHTTPMiddleware):
    """
    CSRF Protection Middleware

    Implements double-submit cookie pattern for CSRF protection.
    """

    def __init__(
        self,
        app,
        secret_key: str,
        cookie_name: str = "csrf_token",
        header_name: str = "X-CSRF-Token",
        token_expiry: int = 3600,  # 1 hour
        exempt_paths: Optional[list] = None,
        safe_methods: Optional[set] = None
    ):
        """
        Initialize CSRF middleware

        Args:
            app: FastAPI application
            secret_key: Secret key for token generation
            cookie_name: Name of the CSRF cookie
            header_name: Name of the CSRF header
            token_expiry: Token expiry time in seconds
            exempt_paths: List of paths exempt from CSRF protection
            safe_methods: Set of HTTP methods that don't require CSRF protection
        """
        super().__init__(app)
        self.secret_key = secret_key.encode()
        self.cookie_name = cookie_name
        self.header_name = header_name
        self.token_expiry = token_expiry
        self.exempt_paths = exempt_paths or [
            "/api/auth/login",
            "/api/auth/register",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        ]
        self.safe_methods = safe_methods or {
            "GET", "HEAD", "OPTIONS", "TRACE"
        }

    def generate_token(self) -> str:
        """
        Generate a cryptographically secure CSRF token

        Returns:
            str: CSRF token (random value + timestamp + HMAC signature)
        """
        # Generate random token
        random_value = secrets.token_urlsafe(32)

        # Add timestamp
        timestamp = str(int(time.time()))

        # Create payload
        payload = f"{random_value}.{timestamp}"

        # Generate HMAC signature
        signature = hmac.new(
            self.secret_key,
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        # Return token: random.timestamp.signature
        return f"{payload}.{signature}"

    def validate_token(self, token: str) -> bool:
        """
        Validate CSRF token

        Args:
            token: CSRF token to validate

        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            # Split token
            parts = token.split(".")
            if len(parts) != 3:
                return False

            random_value, timestamp, signature = parts

            # Check expiry
            token_time = int(timestamp)
            current_time = int(time.time())
            if current_time - token_time > self.token_expiry:
                return False

            # Verify signature
            payload = f"{random_value}.{timestamp}"
            expected_signature = hmac.new(
                self.secret_key,
                payload.encode(),
                hashlib.sha256
            ).hexdigest()

            # Use constant-time comparison to prevent timing attacks
            return hmac.compare_digest(signature, expected_signature)

        except (ValueError, AttributeError):
            return False

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Process request and validate CSRF token

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response: HTTP response
        """
        # Check if path is exempt
        if any(
            request.url.path.startswith(path)
            for path in self.exempt_paths
        ):
            response = await call_next(request)
            return response

        # Safe methods don't require CSRF protection
        if request.method in self.safe_methods:
            response = await call_next(request)

            # Generate and set CSRF token for safe requests
            csrf_token = self.generate_token()
            response.set_cookie(
                key=self.cookie_name,
                value=csrf_token,
                httponly=True,
                secure=True,  # Only send over HTTPS
                samesite="strict",
                max_age=self.token_expiry
            )

            return response

        # For state-changing methods, validate CSRF token
        # Get token from cookie
        cookie_token = request.cookies.get(self.cookie_name)

        # Get token from header
        header_token = request.headers.get(self.header_name)

        # Both tokens must be present
        if not cookie_token or not header_token:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "code": "CSRF_TOKEN_MISSING",
                    "message": (
                        "CSRF token missing. Please include CSRF token "
                        "in both cookie and header."
                    ),
                    "details": {
                        "cookie_present": bool(cookie_token),
                        "header_present": bool(header_token)
                    }
                }
            )

        # Tokens must match (double-submit pattern)
        if cookie_token != header_token:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "code": "CSRF_TOKEN_MISMATCH",
                    "message": (
                        "CSRF token mismatch. Cookie and header tokens "
                        "do not match."
                    ),
                }
            )

        # Validate token
        if not self.validate_token(cookie_token):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "code": "CSRF_TOKEN_INVALID",
                    "message": (
                        "CSRF token is invalid or expired. "
                        "Please refresh the page."
                    ),
                }
            )

        # Token is valid, proceed with request
        response = await call_next(request)

        # Rotate token after successful request
        new_token = self.generate_token()
        response.set_cookie(
            key=self.cookie_name,
            value=new_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=self.token_expiry
        )

        return response
