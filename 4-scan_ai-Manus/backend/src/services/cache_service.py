"""
Caching Service
================

Purpose: Centralized caching with Redis backend and in-memory fallback.
Provides consistent caching interface across the application.

Features:
- Redis-backed caching
- In-memory fallback
- TTL support
- Key prefixing
- Cache invalidation patterns
- Statistics tracking
- Serialization handling

Usage:
    from src.services.cache_service import CacheService, get_cache
    
    cache = get_cache()
    
    # Set value
    await cache.set("user:123", user_data, ttl=3600)
    
    # Get value
    user = await cache.get("user:123")
    
    # Delete
    await cache.delete("user:123")

Author: Global System v35.0
Date: 2026-01-17
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from ..core.config import get_settings

logger = logging.getLogger(__name__)

T = TypeVar('T')


class InMemoryCache:
    """
    Simple in-memory cache for single-instance or development use.
    
    Provides same interface as Redis cache for seamless fallback.
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize in-memory cache.
        
        Args:
            max_size: Maximum number of cached items
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._hits = 0
        self._misses = 0
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            self._misses += 1
            return None
        
        entry = self._cache[key]
        
        # Check expiration
        if entry["expires_at"] and time.time() > entry["expires_at"]:
            del self._cache[key]
            self._misses += 1
            return None
        
        self._hits += 1
        return entry["value"]
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        # Evict if at max size
        if len(self._cache) >= self._max_size:
            self._evict_oldest()
        
        expires_at = time.time() + ttl if ttl else None
        
        self._cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": time.time()
        }
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        value = await self.get(key)
        return value is not None
    
    async def clear(self) -> bool:
        """Clear all cache."""
        self._cache.clear()
        return True
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern."""
        # Simple pattern matching (supports * wildcard)
        pattern = pattern.replace("*", "")
        deleted = 0
        
        keys_to_delete = [
            k for k in self._cache.keys()
            if pattern in k
        ]
        
        for key in keys_to_delete:
            del self._cache[key]
            deleted += 1
        
        return deleted
    
    def _evict_oldest(self) -> None:
        """Evict oldest entry."""
        if not self._cache:
            return
        
        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k]["created_at"]
        )
        del self._cache[oldest_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        
        return {
            "type": "memory",
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 2)
        }


class RedisCache:
    """
    Redis-backed cache implementation.
    
    Provides distributed caching for multi-instance deployments.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        db: int = 0,
        prefix: str = "gaara:"
    ):
        """
        Initialize Redis cache.
        
        Args:
            host: Redis host
            port: Redis port
            password: Redis password
            db: Redis database number
            prefix: Key prefix for namespacing
        """
        self._host = host
        self._port = port
        self._password = password
        self._db = db
        self._prefix = prefix
        self._client = None
        self._hits = 0
        self._misses = 0
    
    def _get_client(self):
        """Get or create Redis client."""
        if self._client is None:
            try:
                import redis
                
                self._client = redis.Redis(
                    host=self._host,
                    port=self._port,
                    password=self._password,
                    db=self._db,
                    decode_responses=True,
                    socket_timeout=5
                )
                # Test connection
                self._client.ping()
                logger.info(f"Redis connected: {self._host}:{self._port}")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
                raise
        
        return self._client
    
    def _make_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self._prefix}{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            client = self._get_client()
            full_key = self._make_key(key)
            
            value = client.get(full_key)
            
            if value is None:
                self._misses += 1
                return None
            
            self._hits += 1
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
                
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            self._misses += 1
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache."""
        try:
            client = self._get_client()
            full_key = self._make_key(key)
            
            # Serialize value
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            elif not isinstance(value, str):
                value = str(value)
            
            if ttl:
                client.setex(full_key, ttl, value)
            else:
                client.set(full_key, value)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            client = self._get_client()
            full_key = self._make_key(key)
            result = client.delete(full_key)
            return result > 0
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            client = self._get_client()
            full_key = self._make_key(key)
            return client.exists(full_key) > 0
        except Exception as e:
            logger.error(f"Cache exists error: {e}")
            return False
    
    async def clear(self) -> bool:
        """Clear all cache with prefix."""
        return await self.delete_pattern("*") > 0
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern."""
        try:
            client = self._get_client()
            full_pattern = self._make_key(pattern)
            
            # Find matching keys
            keys = client.keys(full_pattern)
            
            if keys:
                return client.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Cache delete_pattern error: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        
        stats = {
            "type": "redis",
            "host": self._host,
            "port": self._port,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 2)
        }
        
        try:
            client = self._get_client()
            info = client.info(section="memory")
            stats["memory_used"] = info.get("used_memory_human", "unknown")
        except Exception:
            pass
        
        return stats


class CacheService:
    """
    Unified caching service with Redis and memory fallback.
    
    Automatically falls back to in-memory cache if Redis is unavailable.
    
    Example:
        >>> cache = CacheService()
        >>> await cache.set("key", {"data": "value"}, ttl=3600)
        >>> data = await cache.get("key")
    """
    
    def __init__(self, use_redis: bool = True):
        """
        Initialize cache service.
        
        Args:
            use_redis: Whether to try Redis first
        """
        self.settings = get_settings()
        self._redis_cache: Optional[RedisCache] = None
        self._memory_cache = InMemoryCache()
        self._use_redis = use_redis
        
        if use_redis:
            self._init_redis()
    
    def _init_redis(self) -> None:
        """Initialize Redis cache."""
        try:
            self._redis_cache = RedisCache(
                host=getattr(self.settings, 'REDIS_HOST', 'localhost'),
                port=getattr(self.settings, 'REDIS_PORT', 6379),
                password=getattr(self.settings, 'REDIS_PASSWORD', None),
                db=getattr(self.settings, 'REDIS_DB', 0),
                prefix="gaara:"
            )
            # Test connection
            self._redis_cache._get_client()
            logger.info("Cache service using Redis backend")
        except Exception as e:
            logger.warning(f"Redis unavailable, using memory cache: {e}")
            self._redis_cache = None
    
    @property
    def _cache(self):
        """Get active cache backend."""
        if self._redis_cache:
            return self._redis_cache
        return self._memory_cache
    
    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            default: Default value if not found
            
        Returns:
            Cached value or default
        """
        value = await self._cache.get(key)
        return value if value is not None else default
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            bool: Success status
        """
        return await self._cache.set(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        return await self._cache.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self._cache.exists(key)
    
    async def clear(self) -> bool:
        """Clear all cache."""
        return await self._cache.clear()
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern."""
        return await self._cache.delete_pattern(pattern)
    
    async def get_or_set(
        self,
        key: str,
        factory: Callable[[], T],
        ttl: Optional[int] = None
    ) -> T:
        """
        Get from cache or set using factory function.
        
        Args:
            key: Cache key
            factory: Function to generate value if not cached
            ttl: Time to live in seconds
            
        Returns:
            Cached or generated value
        """
        value = await self.get(key)
        
        if value is None:
            value = factory()
            if asyncio.iscoroutine(value):
                value = await value
            await self.set(key, value, ttl)
        
        return value
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self._cache.get_stats()
    
    # Convenience methods for common patterns
    
    async def cache_user(self, user_id: int, data: Dict) -> bool:
        """Cache user data."""
        return await self.set(f"user:{user_id}", data, ttl=3600)
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get cached user data."""
        return await self.get(f"user:{user_id}")
    
    async def invalidate_user(self, user_id: int) -> bool:
        """Invalidate user cache."""
        return await self.delete(f"user:{user_id}")
    
    async def cache_diagnosis(self, diagnosis_id: int, data: Dict) -> bool:
        """Cache diagnosis result."""
        return await self.set(f"diagnosis:{diagnosis_id}", data, ttl=86400)
    
    async def get_diagnosis(self, diagnosis_id: int) -> Optional[Dict]:
        """Get cached diagnosis."""
        return await self.get(f"diagnosis:{diagnosis_id}")


def cached(
    ttl: int = 3600,
    key_prefix: str = "",
    key_builder: Optional[Callable] = None
):
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
        key_builder: Custom function to build cache key
        
    Example:
        @cached(ttl=3600, key_prefix="user")
        async def get_user(user_id: int):
            return await db.get_user(user_id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = get_cache()
            
            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                key_parts = [key_prefix, func.__name__]
                key_parts.extend(str(a) for a in args)
                key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key = ":".join(filter(None, key_parts))
            
            # Try to get from cache
            result = await cache.get(cache_key)
            
            if result is not None:
                return result
            
            # Call function
            result = await func(*args, **kwargs)
            
            # Cache result
            if result is not None:
                await cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


# Singleton instance
_cache_service: Optional[CacheService] = None


def get_cache() -> CacheService:
    """Get or create cache service singleton."""
    global _cache_service
    
    if _cache_service is None:
        _cache_service = CacheService()
    
    return _cache_service
