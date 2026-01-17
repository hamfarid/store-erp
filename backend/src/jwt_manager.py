# FILE: backend/src/jwt_manager.py | PURPOSE: JWT token management with
# rotation and revocation (P0.2) | OWNER: security | RELATED:
# backend/src/auth.py,backend/src/models/refresh_token.py | LAST-AUDITED:
# 2025-11-04

"""
JWT Token Manager
Handles JWT token generation, validation, rotation, and revocation

P0.2: JWT token rotation with 15min access + 7d refresh
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple
import logging

try:
    import jwt

    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    jwt = None

from flask import current_app, request

logger = logging.getLogger(__name__)


class JWTManager:
    """
    JWT Token Manager

    Features:
    - Access token (short-lived, 15 minutes)
    - Refresh token (long-lived, 7 days)
    - Token rotation on refresh
    - Token revocation support
    - JTI (JWT ID) for unique identification
    """

    # Token types
    TOKEN_TYPE_ACCESS = "access"
    TOKEN_TYPE_REFRESH = "refresh"

    # Default expiration times (OWASP recommendations)
    DEFAULT_ACCESS_EXPIRATION = timedelta(minutes=15)
    DEFAULT_REFRESH_EXPIRATION = timedelta(days=7)

    @staticmethod
    def get_secret_key() -> str:
        """
        Get JWT secret key from config or environment

        Returns:
            str: JWT secret key
        """
        # Try Flask config first
        if current_app:
            secret = current_app.config.get("JWT_SECRET_KEY")
            if secret:
                return secret

        # Try environment variable
        secret = os.getenv("JWT_SECRET_KEY")
        if secret:
            return secret

        # CRITICAL: No fallback in production
        if os.getenv("FLASK_ENV") == "production":
            raise ValueError("JWT_SECRET_KEY must be set in production environment")

        # Development fallback (logged as warning)
        logger.warning("⚠️ Using default JWT secret key (DEVELOPMENT ONLY)")
        return "dev-secret-key-change-in-production"

    @staticmethod
    def generate_jti() -> str:
        """
        Generate a unique JWT ID (jti)

        Returns:
            str: Unique JWT ID (UUID format)
        """
        import uuid

        return str(uuid.uuid4())

    @staticmethod
    def hash_token(token: str) -> str:
        """
        Hash a token for storage (SHA-256)

        Args:
            token: Token to hash

        Returns:
            str: SHA-256 hash of the token
        """
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @classmethod
    def create_access_token(
        cls, user_id: int, additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create an access token (short-lived)

        Args:
            user_id: User ID
            additional_claims: Optional additional claims to include

        Returns:
            str: JWT access token
        """
        if not JWT_AVAILABLE:
            raise RuntimeError("PyJWT is not available")

        now = datetime.now(timezone.utc)
        expiration = now + cls.DEFAULT_ACCESS_EXPIRATION

        payload = {
            "user_id": user_id,
            "type": cls.TOKEN_TYPE_ACCESS,
            "jti": cls.generate_jti(),
            "iat": now,
            "exp": expiration,
            "nbf": now,  # Not before
        }

        # Add additional claims
        if additional_claims:
            payload.update(additional_claims)

        secret_key = cls.get_secret_key()
        if secret_key is None:
            raise ValueError("JWT secret key is not configured")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        logger.debug(
            f"Created access token for user {user_id}, expires at {expiration}"
        )
        return token

    @classmethod
    def create_refresh_token(
        cls, user_id: int, additional_claims: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str, datetime]:
        """
        Create a refresh token (long-lived)

        Args:
            user_id: User ID
            additional_claims: Optional additional claims to include

        Returns:
            tuple: (token, jti, expiration_datetime)
        """
        if not JWT_AVAILABLE:
            raise RuntimeError("PyJWT is not available")

        now = datetime.now(timezone.utc)
        expiration = now + cls.DEFAULT_REFRESH_EXPIRATION
        jti = cls.generate_jti()

        payload = {
            "user_id": user_id,
            "type": cls.TOKEN_TYPE_REFRESH,
            "jti": jti,
            "iat": now,
            "exp": expiration,
            "nbf": now,
        }

        # Add additional claims
        if additional_claims:
            payload.update(additional_claims)

        secret_key = cls.get_secret_key()
        if secret_key is None:
            raise ValueError("JWT secret key is not configured")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        logger.debug(
            f"Created refresh token for user {user_id}, jti={jti}, expires at {expiration}"
        )
        return token, jti, expiration

    @classmethod
    def decode_token(cls, token: str, verify: bool = True) -> Optional[Dict[str, Any]]:
        """
        Decode and verify a JWT token

        Args:
            token: JWT token to decode
            verify: Whether to verify signature and expiration

        Returns:
            dict: Decoded payload or None if invalid
        """
        if not JWT_AVAILABLE:
            raise RuntimeError("PyJWT is not available")

        try:
            payload = jwt.decode(
                token,
                cls.get_secret_key(),
                algorithms=["HS256"],
                options={"verify_signature": verify, "verify_exp": verify},
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    @classmethod
    def verify_access_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify an access token

        Args:
            token: Access token to verify

        Returns:
            dict: Decoded payload or None if invalid
        """
        payload = cls.decode_token(token)
        if not payload:
            return None

        # Verify token type
        if payload.get("type") != cls.TOKEN_TYPE_ACCESS:
            logger.warning(f"Invalid token type: {payload.get('type')}")
            return None

        return payload

    @classmethod
    def verify_refresh_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a refresh token

        Args:
            token: Refresh token to verify

        Returns:
            dict: Decoded payload or None if invalid
        """
        payload = cls.decode_token(token)
        if not payload:
            return None

        # Verify token type
        if payload.get("type") != cls.TOKEN_TYPE_REFRESH:
            logger.warning(f"Invalid token type: {payload.get('type')}")
            return None

        # Check if token is revoked (requires database check)
        from models.refresh_token import RefreshToken

        jti = payload.get("jti")
        if jti:
            db_token = RefreshToken.find_by_jti(jti)
            if db_token:
                if not db_token.is_valid():
                    logger.warning(f"Refresh token {jti} is revoked or expired")
                    return None
                # Update last used timestamp
                db_token.update_last_used()
                from models.user import db

                db.session.commit()

        return payload

    @classmethod
    def get_client_info(cls) -> Dict[str, Optional[str]]:
        """
        Get client information from request

        Returns:
            dict: Client IP, user agent, and device fingerprint
        """
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get("User-Agent") if request else None

        # Simple device fingerprint (can be enhanced)
        device_fingerprint = None
        if user_agent:
            device_fingerprint = hashlib.md5(user_agent.encode("utf-8")).hexdigest()

        return {
            "ip_address": ip_address,
            "user_agent": user_agent,
            "device_fingerprint": device_fingerprint,
        }


# Convenience functions
def create_token_pair(
    user_id: int, additional_claims: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create both access and refresh tokens

    Args:
        user_id: User ID
        additional_claims: Optional additional claims

    Returns:
        dict: {access_token, refresh_token, expires_in, refresh_expires_in}
    """
    access_token = JWTManager.create_access_token(user_id, additional_claims)
    refresh_token, jti, refresh_expiration = JWTManager.create_refresh_token(
        user_id, additional_claims
    )

    # Store refresh token in database
    from models.refresh_token import RefreshToken
    from models.user import db

    client_info = JWTManager.get_client_info()
    token_hash = JWTManager.hash_token(refresh_token)

    RefreshToken.create_token(
        user_id=user_id,
        jti=jti,
        token_hash=token_hash,
        expires_at=refresh_expiration,
        **client_info,
    )
    db.session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": int(JWTManager.DEFAULT_ACCESS_EXPIRATION.total_seconds()),
        "refresh_expires_in": int(
            JWTManager.DEFAULT_REFRESH_EXPIRATION.total_seconds()
        ),
    }
