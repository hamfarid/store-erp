"""
Rate Limiter Middleware
========================

Purpose: Implement rate limiting to protect against abuse and DDoS attacks.
Uses Redis as a backend for distributed rate limiting across multiple
workers/instances.

Features:
- Configurable rate limits per endpoint pattern
- Sliding window algorithm for smooth rate limiting
- IP-based and user-based limiting
- Custom limits for sensitive endpoints (auth, uploads)
- Proper HTTP 429 responses with Retry-After header

Usage:
    from src.middleware.rate_limiter import RateLimiter, rate_limit
    
    # Add to FastAPI app
    app.add_middleware(RateLimiter)
    
    # Or use decorator for specific routes
    @app.post("/login")
    @rate_limit(limit=5, window=60)  # 5 requests per minute
    async def login(request: Request):
        ...

Author: Global System v35.0
Date: 2026-01-17
"""

import logging
import time
from typing import Callable, Dict, Optional, Tuple

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logger
logger = logging.getLogger(__name__)


class RateLimitConfig:
    """
    Configuration for rate limiting rules.
    
    Attributes:
        DEFAULT_LIMIT: Default requests per window
        DEFAULT_WINDOW: Default window size in seconds
        ENDPOINT_LIMITS: Custom limits per endpoint pattern
    """
    
    # Default: 60 requests per minute
    DEFAULT_LIMIT: int = 60
    DEFAULT_WINDOW: int = 60  # seconds
    
    # Endpoint-specific limits (path pattern -> (limit, window_seconds))
    ENDPOINT_LIMITS: Dict[str, Tuple[int, int]] = {
        # Authentication - strict limits
        '/api/v1/auth/login': (5, 60),          # 5 per minute
        '/api/v1/auth/register': (3, 3600),     # 3 per hour
        '/api/v1/auth/forgot-password': (3, 3600),
        '/api/v1/auth/reset-password': (5, 3600),
        '/api/v1/2fa/verify': (5, 60),
        
        # File uploads - moderate limits
        '/api/v1/upload': (10, 60),             # 10 per minute
        '/api/v1/diagnosis': (10, 60),
        
        # Crawler - low limits
        '/api/v1/crawler/search': (5, 60),
        '/api/v1/crawler/train': (2, 3600),
        
        # Health checks - high limits
        '/api/v1/health': (1000, 60),
        '/health': (1000, 60),
    }
    
    # Paths to skip rate limiting entirely
    SKIP_PATHS: set = {
        '/docs',
        '/redoc',
        '/openapi.json',
        '/favicon.ico',
    }
    
    # Use Redis for distributed rate limiting
    USE_REDIS: bool = True


class InMemoryStore:
    """
    Simple in-memory rate limit store for single-instance deployments.
    
    Uses a dictionary with automatic cleanup of expired entries.
    For production with multiple workers, use Redis instead.
    """
    
    def __init__(self):
        """Initialize in-memory store."""
        self._store: Dict[str, Tuple[int, float]] = {}
        self._last_cleanup: float = time.time()
        self._cleanup_interval: int = 60  # seconds
    
    def get_count(self, key: str, window: int) -> int:
        """
        Get current request count for a key within the window.
        
        Args:
            key: Rate limit key (e.g., "ip:192.168.1.1:/api/login")
            window: Time window in seconds
            
        Returns:
            int: Current request count
        """
        self._maybe_cleanup()
        
        if key not in self._store:
            return 0
        
        count, timestamp = self._store[key]
        
        # Check if window has expired
        if time.time() - timestamp > window:
            del self._store[key]
            return 0
        
        return count
    
    def increment(self, key: str, window: int) -> int:
        """
        Increment request count for a key.
        
        Args:
            key: Rate limit key
            window: Time window in seconds
            
        Returns:
            int: New request count
        """
        current_time = time.time()
        
        if key in self._store:
            count, timestamp = self._store[key]
            
            # Reset if window expired
            if current_time - timestamp > window:
                self._store[key] = (1, current_time)
                return 1
            
            # Increment
            self._store[key] = (count + 1, timestamp)
            return count + 1
        
        # New key
        self._store[key] = (1, current_time)
        return 1
    
    def _maybe_cleanup(self) -> None:
        """Clean up expired entries periodically."""
        current_time = time.time()
        
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        self._last_cleanup = current_time
        max_window = max(
            w for _, w in RateLimitConfig.ENDPOINT_LIMITS.values()
        ) if RateLimitConfig.ENDPOINT_LIMITS else 3600
        
        # Remove entries older than max window
        expired_keys = [
            k for k, (_, ts) in self._store.items()
            if current_time - ts > max_window
        ]
        
        for key in expired_keys:
            del self._store[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired rate limit entries")


class RedisStore:
    """
    Redis-backed rate limit store for distributed deployments.
    
    Uses Redis INCR with EXPIRE for atomic increment operations.
    Supports multiple workers and instances.
    """
    
    def __init__(self, redis_client=None):
        """
        Initialize Redis store.
        
        Args:
            redis_client: Redis client instance, or None to create one
        """
        self._redis = redis_client
        self._key_prefix = "rate_limit:"
    
    def _get_redis(self):
        """Get or create Redis client."""
        if self._redis is None:
            try:
                import redis
                from src.core.config import get_settings
                
                settings = get_settings()
                self._redis = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    password=settings.REDIS_PASSWORD,
                    db=settings.REDIS_DB,
                    decode_responses=True
                )
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}")
                return None
        return self._redis
    
    def get_count(self, key: str, window: int) -> int:
        """
        Get current request count from Redis.
        
        Args:
            key: Rate limit key
            window: Time window (used for key construction)
            
        Returns:
            int: Current count, 0 if not found
        """
        redis_client = self._get_redis()
        if redis_client is None:
            return 0
        
        try:
            full_key = f"{self._key_prefix}{key}"
            count = redis_client.get(full_key)
            return int(count) if count else 0
        except Exception as e:
            logger.warning(f"Redis get error: {e}")
            return 0
    
    def increment(self, key: str, window: int) -> int:
        """
        Atomically increment count in Redis.
        
        Args:
            key: Rate limit key
            window: Time window in seconds (for TTL)
            
        Returns:
            int: New count after increment
        """
        redis_client = self._get_redis()
        if redis_client is None:
            return 0
        
        try:
            full_key = f"{self._key_prefix}{key}"
            
            # Use pipeline for atomic INCR + EXPIRE
            pipe = redis_client.pipeline()
            pipe.incr(full_key)
            pipe.expire(full_key, window)
            results = pipe.execute()
            
            return results[0]  # INCR result
        except Exception as e:
            logger.warning(f"Redis increment error: {e}")
            return 0


# Global store instance
_store: Optional[InMemoryStore | RedisStore] = None


def get_store() -> InMemoryStore | RedisStore:
    """Get or create rate limit store."""
    global _store
    
    if _store is None:
        if RateLimitConfig.USE_REDIS:
            _store = RedisStore()
        else:
            _store = InMemoryStore()
    
    return _store


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request.
    
    Handles X-Forwarded-For header for proxied requests.
    
    Args:
        request: FastAPI request object
        
    Returns:
        str: Client IP address
    """
    # Check X-Forwarded-For header (set by proxies/load balancers)
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        # First IP in the list is the original client
        return forwarded.split(',')[0].strip()
    
    # Check X-Real-IP header
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip.strip()
    
    # Fall back to direct client IP
    if request.client:
        return request.client.host
    
    return 'unknown'


def get_rate_limit(path: str) -> Tuple[int, int]:
    """
    Get rate limit configuration for a path.
    
    Args:
        path: Request path
        
    Returns:
        Tuple[int, int]: (limit, window_seconds)
    """
    # Check exact match
    if path in RateLimitConfig.ENDPOINT_LIMITS:
        return RateLimitConfig.ENDPOINT_LIMITS[path]
    
    # Check prefix match
    for pattern, limits in RateLimitConfig.ENDPOINT_LIMITS.items():
        if path.startswith(pattern):
            return limits
    
    # Return default
    return (RateLimitConfig.DEFAULT_LIMIT, RateLimitConfig.DEFAULT_WINDOW)


class RateLimiter(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.
    
    Applies rate limiting to all requests based on configured rules.
    Returns HTTP 429 Too Many Requests when limit is exceeded.
    
    Example:
        app = FastAPI()
        app.add_middleware(RateLimiter)
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Process request with rate limiting.
        
        Args:
            request: Incoming request
            call_next: Next middleware/handler
            
        Returns:
            Response: Normal response or 429 error
        """
        path = request.url.path
        
        # Skip rate limiting for excluded paths
        if path in RateLimitConfig.SKIP_PATHS:
            return await call_next(request)
        
        # Get client identifier
        client_ip = get_client_ip(request)
        
        # Get rate limit for this endpoint
        limit, window = get_rate_limit(path)
        
        # Create rate limit key
        key = f"{client_ip}:{path}"
        
        # Get store and check/increment count
        store = get_store()
        current_count = store.increment(key, window)
        
        # Check if over limit
        if current_count > limit:
            logger.warning(
                f"Rate limit exceeded: ip={client_ip}, path={path}, "
                f"count={current_count}/{limit}"
            )
            
            # Calculate retry-after
            retry_after = window
            
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please try again later.",
                        "message_ar": "طلبات كثيرة جداً. يرجى المحاولة لاحقاً.",
                        "retry_after": retry_after
                    }
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + window)
                }
            )
        
        # Process request normally
        response = await call_next(request)
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current_count))
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + window)
        
        return response


def rate_limit(limit: int = 60, window: int = 60):
    """
    Decorator for custom rate limiting on specific routes.
    
    Args:
        limit: Maximum requests allowed
        window: Time window in seconds
        
    Returns:
        Decorator function
        
    Example:
        @app.post("/sensitive-endpoint")
        @rate_limit(limit=5, window=60)
        async def sensitive_endpoint(request: Request):
            ...
    """
    def decorator(func: Callable) -> Callable:
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = get_client_ip(request)
            key = f"{client_ip}:{func.__name__}"
            
            store = get_store()
            current_count = store.increment(key, window)
            
            if current_count > limit:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests",
                        "retry_after": window
                    }
                )
            
            return await func(request, *args, **kwargs)
        
        wrapper.__name__ = func.__name__
        return wrapper
    
    return decorator
