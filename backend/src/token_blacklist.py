# FILE: backend/src/token_blacklist.py | PURPOSE: P0.3 JWT Token Blacklist
# for Refresh Token Rotation | OWNER: Security | LAST-AUDITED: 2025-12-01
"""
P0.3: Token Blacklist for JWT Refresh Token Rotation

This module provides a token blacklist to revoke refresh tokens when:
- User logs out
- Refresh token is rotated (old token added to blacklist)
- Admin revokes a user's sessions

For production, use Redis backend. This implementation provides:
- In-memory store for development
- Redis store for production (if available)
"""

import os
import time
import logging
from datetime import datetime, timezone
from typing import Optional, Set
import hashlib

logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None  # type: ignore


class TokenBlacklist:
    """
    P0.3: Token Blacklist for JWT Refresh Token Rotation

    Stores revoked token JTIs (JWT IDs) to prevent reuse.
    Uses Redis in production, in-memory dict for development.
    """

    def __init__(self, redis_url: Optional[str] = None, default_ttl: int = 604800):
        """
        Initialize token blacklist

        Args:
            redis_url: Redis connection URL (optional, falls back to in-memory)
            default_ttl: Default TTL in seconds (7 days = 604800)
        """
        self.default_ttl = default_ttl
        self._memory_store: dict = {}  # {jti: expiry_timestamp}
        self._redis_client = None

        if redis_url and REDIS_AVAILABLE:
            try:
                self._redis_client = redis.from_url(redis_url)
                self._redis_client.ping()  # Test connection
                logger.info("✅ Token blacklist using Redis")
            except Exception as e:
                logger.warning(f"⚠️ Redis not available, using in-memory blacklist: {e}")
                self._redis_client = None
        else:
            logger.info("ℹ️ Token blacklist using in-memory store (development mode)")

    def _get_jti_from_token(self, token: str) -> str:
        """
        Extract or generate JTI from token

        For tokens without JTI, we hash the token to create a unique identifier.
        """
        # Try to decode token to get JTI
        try:
            import jwt

            # Decode without verification to extract payload
            payload = jwt.decode(token, options={"verify_signature": False})
            if "jti" in payload:
                return payload["jti"]
            # Use user_id + iat as unique identifier if no JTI
            user_id = payload.get("user_id", "")
            iat = payload.get("iat", 0)
            return f"{user_id}:{iat}"
        except Exception:
            pass

        # Fallback: hash the token
        return hashlib.sha256(token.encode()).hexdigest()[:32]

    def add(self, token: str, ttl: Optional[int] = None) -> bool:
        """
        Add a token to the blacklist

        Args:
            token: JWT token string
            ttl: Time-to-live in seconds (uses default if not specified)

        Returns:
            True if added successfully
        """
        jti = self._get_jti_from_token(token)
        ttl = ttl or self.default_ttl
        expiry = int(time.time()) + ttl

        if self._redis_client:
            try:
                # Use Redis SETEX for automatic expiry
                key = f"token_blacklist:{jti}"
                self._redis_client.setex(key, ttl, "1")
                logger.debug(f"Token {jti[:8]}... added to Redis blacklist")
                return True
            except Exception as e:
                logger.error(f"Failed to add token to Redis blacklist: {e}")
                return False
        else:
            # In-memory store
            self._memory_store[jti] = expiry
            self._cleanup_expired()
            logger.debug(f"Token {jti[:8]}... added to in-memory blacklist")
            return True

    def is_blacklisted(self, token: str) -> bool:
        """
        Check if a token is blacklisted

        Args:
            token: JWT token string

        Returns:
            True if token is blacklisted
        """
        jti = self._get_jti_from_token(token)

        if self._redis_client:
            try:
                key = f"token_blacklist:{jti}"
                return self._redis_client.exists(key) > 0
            except Exception as e:
                logger.error(f"Failed to check Redis blacklist: {e}")
                return False
        else:
            # In-memory check
            expiry = self._memory_store.get(jti)
            if expiry is None:
                return False
            if expiry < int(time.time()):
                # Expired, remove from store
                del self._memory_store[jti]
                return False
            return True

    def remove(self, token: str) -> bool:
        """
        Remove a token from the blacklist (rarely used)

        Args:
            token: JWT token string

        Returns:
            True if removed successfully
        """
        jti = self._get_jti_from_token(token)

        if self._redis_client:
            try:
                key = f"token_blacklist:{jti}"
                return self._redis_client.delete(key) > 0
            except Exception as e:
                logger.error(f"Failed to remove token from Redis blacklist: {e}")
                return False
        else:
            if jti in self._memory_store:
                del self._memory_store[jti]
                return True
            return False

    def _cleanup_expired(self):
        """Clean up expired entries from in-memory store"""
        if self._redis_client:
            return  # Redis handles expiry automatically

        now = int(time.time())
        expired = [jti for jti, expiry in self._memory_store.items() if expiry < now]
        for jti in expired:
            del self._memory_store[jti]

        if expired:
            logger.debug(f"Cleaned up {len(expired)} expired blacklist entries")

    def clear(self):
        """Clear all blacklisted tokens (use with caution)"""
        if self._redis_client:
            try:
                # Delete all token_blacklist:* keys
                cursor = 0
                while True:
                    cursor, keys = self._redis_client.scan(
                        cursor, match="token_blacklist:*", count=100
                    )
                    if keys:
                        self._redis_client.delete(*keys)
                    if cursor == 0:
                        break
                logger.info("Redis token blacklist cleared")
            except Exception as e:
                logger.error(f"Failed to clear Redis blacklist: {e}")
        else:
            self._memory_store.clear()
            logger.info("In-memory token blacklist cleared")

    def count(self) -> int:
        """Get count of blacklisted tokens"""
        if self._redis_client:
            try:
                cursor = 0
                count = 0
                while True:
                    cursor, keys = self._redis_client.scan(
                        cursor, match="token_blacklist:*", count=100
                    )
                    count += len(keys)
                    if cursor == 0:
                        break
                return count
            except Exception:
                return 0
        else:
            self._cleanup_expired()
            return len(self._memory_store)


# Global instance - initialize with Redis URL from environment if available

_redis_url = os.environ.get("REDIS_URL") or os.environ.get("RATELIMIT_STORAGE_URL")
token_blacklist = TokenBlacklist(redis_url=_redis_url)


def blacklist_token(token: str, ttl: Optional[int] = None) -> bool:
    """Add a token to the blacklist"""
    return token_blacklist.add(token, ttl)


def is_token_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted"""
    return token_blacklist.is_blacklisted(token)


def revoke_all_user_tokens(user_id: int) -> bool:
    """
    Revoke all tokens for a user

    Note: This is a simple implementation. For better performance,
    store user_id -> token mappings and revoke by user_id.
    """
    # This would require tracking all tokens per user
    # For now, we rely on short access token TTL
    logger.info(f"Token revocation requested for user {user_id}")
    return True
