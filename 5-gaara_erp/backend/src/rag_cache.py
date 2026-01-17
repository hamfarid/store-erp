#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.39: RAG Caching System with TTL Support

Provides caching for RAG query results to improve performance and reduce
embedding computation costs. Supports both in-memory and Redis backends.

Features:
- Configurable TTL (Time To Live)
- Cache key normalization
- Cache statistics
- Redis support for distributed caching
"""

import os
import json
import time
import hashlib
import logging
from typing import Optional, Dict, Any, Callable
from functools import wraps
from threading import Lock

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

RAG_CACHE_TTL = int(os.environ.get("RAG_CACHE_TTL", 3600))  # 1 hour default
RAG_CACHE_MAX_SIZE = int(os.environ.get("RAG_CACHE_MAX_SIZE", 1000))  # Max entries
RAG_CACHE_ENABLED = os.environ.get("RAG_CACHE_ENABLED", "true").lower() == "true"


# =============================================================================
# Cache Key Generation
# =============================================================================


def generate_cache_key(query: str, top_k: int, **kwargs) -> str:
    """
    Generate a unique cache key for a RAG query.

    Args:
        query: The search query
        top_k: Number of results requested
        **kwargs: Additional parameters that affect results

    Returns:
        SHA256 hash of the normalized query parameters
    """
    # Normalize query (lowercase, strip whitespace)
    normalized_query = query.lower().strip()

    # Create key components
    key_parts = {"q": normalized_query, "k": top_k, **kwargs}

    # Sort and serialize
    key_string = json.dumps(key_parts, sort_keys=True)

    # Hash for fixed-length key
    return hashlib.sha256(key_string.encode("utf-8")).hexdigest()[:32]


# =============================================================================
# In-Memory Cache Implementation
# =============================================================================


class InMemoryRAGCache:
    """
    P1.39: Thread-safe in-memory cache with TTL support.

    Uses LRU eviction when max size is reached.
    """

    def __init__(self, ttl: int = RAG_CACHE_TTL, max_size: int = RAG_CACHE_MAX_SIZE):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl
        self._max_size = max_size
        self._lock = Lock()
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get a value from cache if it exists and hasn't expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                self._stats["misses"] += 1
                return None

            entry = self._cache[key]

            # Check expiration
            if time.time() > entry["expires_at"]:
                del self._cache[key]
                self._stats["misses"] += 1
                return None

            # Update access time for LRU
            entry["last_access"] = time.time()
            self._stats["hits"] += 1

            return entry["value"]

    def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """
        Set a value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional custom TTL (uses default if not provided)
        """
        effective_ttl = ttl if ttl is not None else self._ttl

        with self._lock:
            # Evict if at max size
            if len(self._cache) >= self._max_size and key not in self._cache:
                self._evict_oldest()

            self._cache[key] = {
                "value": value,
                "created_at": time.time(),
                "expires_at": time.time() + effective_ttl,
                "last_access": time.time(),
            }

    def delete(self, key: str) -> bool:
        """
        Delete a key from cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of entries cleared
        """
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    def _evict_oldest(self) -> None:
        """Evict the least recently used entry."""
        if not self._cache:
            return

        # Find oldest entry by last_access
        oldest_key = min(
            self._cache.keys(), key=lambda k: self._cache[k]["last_access"]
        )
        del self._cache[oldest_key]
        self._stats["evictions"] += 1

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns:
            Number of entries removed
        """
        with self._lock:
            now = time.time()
            expired_keys = [k for k, v in self._cache.items() if now > v["expires_at"]]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total = self._stats["hits"] + self._stats["misses"]
            hit_rate = self._stats["hits"] / total if total > 0 else 0

            return {
                "hits": self._stats["hits"],
                "misses": self._stats["misses"],
                "evictions": self._stats["evictions"],
                "hit_rate": round(hit_rate, 4),
                "size": len(self._cache),
                "max_size": self._max_size,
                "ttl": self._ttl,
            }


# =============================================================================
# Redis Cache Implementation
# =============================================================================


class RedisRAGCache:
    """
    P1.39: Redis-backed cache for distributed RAG caching.
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        ttl: int = RAG_CACHE_TTL,
        prefix: str = "rag:cache:",
    ):
        self._ttl = ttl
        self._prefix = prefix
        self._redis = None
        self._stats = {"hits": 0, "misses": 0}

        # Try to initialize Redis connection
        redis_url = redis_url or os.environ.get("REDIS_URL")
        if redis_url:
            try:
                import redis

                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()  # Test connection
                logger.info("P1.39: Redis RAG cache initialized")
            except Exception as e:
                logger.warning(
                    f"P1.39: Redis connection failed, using memory cache: {e}"
                )
                self._redis = None

    def _key(self, key: str) -> str:
        """Generate prefixed Redis key."""
        return f"{self._prefix}{key}"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a value from Redis cache."""
        if not self._redis:
            return None

        try:
            data = self._redis.get(self._key(key))
            if data:
                self._stats["hits"] += 1
                return json.loads(data)
            self._stats["misses"] += 1
            return None
        except Exception as e:
            logger.error(f"P1.39: Redis get error: {e}")
            return None

    def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set a value in Redis cache with TTL."""
        if not self._redis:
            return

        effective_ttl = ttl if ttl is not None else self._ttl

        try:
            self._redis.setex(self._key(key), effective_ttl, json.dumps(value))
        except Exception as e:
            logger.error(f"P1.39: Redis set error: {e}")

    def delete(self, key: str) -> bool:
        """Delete a key from Redis cache."""
        if not self._redis:
            return False

        try:
            return self._redis.delete(self._key(key)) > 0
        except Exception as e:
            logger.error(f"P1.39: Redis delete error: {e}")
            return False

    def clear(self) -> int:
        """Clear all RAG cache entries from Redis."""
        if not self._redis:
            return 0

        try:
            pattern = f"{self._prefix}*"
            keys = self._redis.keys(pattern)
            if keys:
                return self._redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"P1.39: Redis clear error: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0

        size = 0
        if self._redis:
            try:
                size = len(self._redis.keys(f"{self._prefix}*"))
            except Exception:
                pass

        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": round(hit_rate, 4),
            "size": size,
            "ttl": self._ttl,
            "backend": "redis" if self._redis else "none",
        }


# =============================================================================
# Cache Factory and Global Instance
# =============================================================================


def create_rag_cache() -> InMemoryRAGCache:
    """
    Create the appropriate RAG cache based on configuration.

    Returns:
        Cache instance (Redis if available, otherwise in-memory)
    """
    redis_url = os.environ.get("REDIS_URL")

    if redis_url:
        redis_cache = RedisRAGCache(redis_url)
        if redis_cache._redis:
            # Wrap Redis cache with in-memory fallback
            return _HybridCache(redis_cache, InMemoryRAGCache())

    return InMemoryRAGCache()


class _HybridCache:
    """Hybrid cache that uses Redis with in-memory fallback."""

    def __init__(self, primary: RedisRAGCache, fallback: InMemoryRAGCache):
        self._primary = primary
        self._fallback = fallback

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        result = self._primary.get(key)
        if result is None:
            result = self._fallback.get(key)
        return result

    def set(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None) -> None:
        self._primary.set(key, value, ttl)
        self._fallback.set(key, value, ttl)

    def delete(self, key: str) -> bool:
        r1 = self._primary.delete(key)
        r2 = self._fallback.delete(key)
        return r1 or r2

    def clear(self) -> int:
        c1 = self._primary.clear()
        c2 = self._fallback.clear()
        return c1 + c2

    def get_stats(self) -> Dict[str, Any]:
        return {
            "primary": self._primary.get_stats(),
            "fallback": self._fallback.get_stats(),
        }


# Global cache instance
rag_cache = create_rag_cache() if RAG_CACHE_ENABLED else None


# =============================================================================
# Cache Decorator
# =============================================================================


def cache_rag_query(ttl: Optional[int] = None):
    """
    P1.39: Decorator to cache RAG query results.

    Usage:
        @cache_rag_query(ttl=3600)
        def query(text: str, top_k: int = 5) -> Dict:
            ...

    Args:
        ttl: Cache TTL in seconds (uses default if not provided)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(text: str, top_k: int = 5, **kwargs) -> Dict[str, Any]:
            # Skip cache if disabled
            if not RAG_CACHE_ENABLED or rag_cache is None:
                return func(text, top_k, **kwargs)

            # Generate cache key
            cache_key = generate_cache_key(text, top_k, **kwargs)

            # Try to get from cache
            cached = rag_cache.get(cache_key)
            if cached is not None:
                logger.debug(f"P1.39: RAG cache hit for key {cache_key[:8]}...")
                cached["_cached"] = True
                return cached

            # Execute function and cache result
            result = func(text, top_k, **kwargs)

            # Only cache successful results
            if result.get("success", False):
                rag_cache.set(cache_key, result, ttl)
                logger.debug(f"P1.39: RAG result cached with key {cache_key[:8]}...")

            result["_cached"] = False
            return result

        return wrapper

    return decorator


# =============================================================================
# Cache Management Functions
# =============================================================================


def invalidate_rag_cache(
    query: Optional[str] = None, top_k: Optional[int] = None
) -> int:
    """
    Invalidate RAG cache entries.

    Args:
        query: Specific query to invalidate (clears all if None)
        top_k: Top K value for the query

    Returns:
        Number of entries invalidated
    """
    if not rag_cache:
        return 0

    if query is None:
        return rag_cache.clear()

    cache_key = generate_cache_key(query, top_k or 5)
    return 1 if rag_cache.delete(cache_key) else 0


def get_rag_cache_stats() -> Dict[str, Any]:
    """
    Get RAG cache statistics.

    Returns:
        Dictionary with cache statistics
    """
    if not rag_cache:
        return {"enabled": False}

    stats = rag_cache.get_stats()
    stats["enabled"] = True
    return stats


__all__ = [
    "generate_cache_key",
    "InMemoryRAGCache",
    "RedisRAGCache",
    "create_rag_cache",
    "rag_cache",
    "cache_rag_query",
    "invalidate_rag_cache",
    "get_rag_cache_stats",
    "RAG_CACHE_TTL",
    "RAG_CACHE_ENABLED",
]
