"""
FILE: backend/src/utils/cache.py | PURPOSE: Cache utilities for API endpoints
OWNER: Backend Team | RELATED: cache_service.py | LAST-AUDITED: 2026-01-31

Cache utilities and helpers for API endpoints.
Provides cache key builders, TTL constants, and invalidation helpers.
"""

import logging
from functools import wraps
from typing import Callable, Optional

from ..services.cache_service import get_cache, CacheService

logger = logging.getLogger(__name__)

# TTL Constants (in seconds)
TTL_SHORT = 60  # 1 minute - for frequently changing data
TTL_MEDIUM = 300  # 5 minutes - for stats and aggregations
TTL_LONG = 3600  # 1 hour - for rarely changing data
TTL_VERY_LONG = 86400  # 24 hours - for static data


# Cache key prefixes
CACHE_PREFIX_FARM = "farm"
CACHE_PREFIX_FARM_STATS = "farm_stats"
CACHE_PREFIX_SENSOR = "sensor"
CACHE_PREFIX_DIAGNOSIS = "diagnosis"
CACHE_PREFIX_USER = "user"
CACHE_PREFIX_CROP = "crop"
CACHE_PREFIX_LIST = "list"


def build_farm_stats_key(farm_id: int, user_id: int) -> str:
    """Build cache key for farm statistics."""
    return f"{CACHE_PREFIX_FARM_STATS}:{farm_id}:user:{user_id}"


def build_list_key(
    prefix: str,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    **filters
) -> str:
    """Build cache key for list endpoints with pagination."""
    filter_str = ":".join(f"{k}={v}" for k, v in sorted(filters.items()) if v)
    return f"{CACHE_PREFIX_LIST}:{prefix}:{user_id}:{skip}:{limit}:{filter_str}"


async def invalidate_farm_cache(farm_id: int) -> None:
    """Invalidate all cache entries related to a farm."""
    cache = get_cache()
    try:
        await cache.delete_pattern(f"{CACHE_PREFIX_FARM}:{farm_id}:*")
        await cache.delete_pattern(f"{CACHE_PREFIX_FARM_STATS}:{farm_id}:*")
        logger.debug(f"Invalidated cache for farm {farm_id}")
    except Exception as e:
        logger.warning(f"Failed to invalidate farm cache: {e}")


async def invalidate_user_cache(user_id: int) -> None:
    """Invalidate all cache entries for a user."""
    cache = get_cache()
    try:
        await cache.delete_pattern(f"*:user:{user_id}:*")
        await cache.delete_pattern(f"*:user:{user_id}")
        logger.debug(f"Invalidated cache for user {user_id}")
    except Exception as e:
        logger.warning(f"Failed to invalidate user cache: {e}")


async def invalidate_list_cache(prefix: str) -> None:
    """Invalidate all list cache entries for a resource type."""
    cache = get_cache()
    try:
        await cache.delete_pattern(f"{CACHE_PREFIX_LIST}:{prefix}:*")
        logger.debug(f"Invalidated list cache for {prefix}")
    except Exception as e:
        logger.warning(f"Failed to invalidate list cache: {e}")


async def get_cached_or_compute(
    key: str,
    compute_fn: Callable,
    ttl: int = TTL_MEDIUM
):
    """
    Get value from cache or compute and store it.
    
    Args:
        key: Cache key
        compute_fn: Async function to compute value if not cached
        ttl: Time to live in seconds
        
    Returns:
        Cached or computed value
    """
    cache = get_cache()
    
    # Try cache first
    cached = await cache.get(key)
    if cached is not None:
        logger.debug(f"Cache hit: {key}")
        return cached
    
    # Compute value
    logger.debug(f"Cache miss: {key}")
    value = await compute_fn()
    
    # Store in cache
    if value is not None:
        await cache.set(key, value, ttl)
    
    return value


def cache_response(
    key_builder: Callable[..., str],
    ttl: int = TTL_MEDIUM
):
    """
    Decorator to cache API response.
    
    Args:
        key_builder: Function that takes endpoint args and returns cache key
        ttl: Time to live in seconds
        
    Example:
        @cache_response(
            key_builder=lambda farm_id, **kw: f"farm:{farm_id}",
            ttl=TTL_MEDIUM
        )
        async def get_farm_stats(farm_id: int, ...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = get_cache()
            cache_key = key_builder(*args, **kwargs)
            
            # Try cache
            cached = await cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                return cached
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result (convert Pydantic model to dict if needed)
            if result is not None:
                cache_value = result
                if hasattr(result, 'model_dump'):
                    cache_value = result.model_dump()
                elif hasattr(result, 'dict'):
                    cache_value = result.dict()
                await cache.set(cache_key, cache_value, ttl)
            
            return result
        
        return wrapper
    return decorator

