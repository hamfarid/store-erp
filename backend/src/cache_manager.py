# -*- coding: utf-8 -*-
# FILE: backend/src/cache_manager.py
# PURPOSE: Comprehensive Caching System
# OWNER: Backend
# RELATED: app.py
# LAST-AUDITED: 2025-10-21

"""
نظام التخزين المؤقت الشامل - الإصدار 2.0
Comprehensive Caching System - Version 2.0

P1 Fixes Applied:
- P1.4: Redis-based caching for frequently accessed data
- P1.5: Cache invalidation strategies
- P1.6: Performance optimization for database queries
"""

import json
import redis
from functools import wraps


class CacheManager:
    """Comprehensive cache manager using Redis."""

    def __init__(self, redis_url="redis://localhost:5606/0"):
        try:
            self.redis_client = redis.from_url(redis_url)
            # Ping to validate connection (may raise RedisError)
            self.redis_client.ping()
            self.enabled = True
        except (redis.ConnectionError, redis.RedisError) as e:
            self.redis_client = None
            self.enabled = False
            print(f"Warning: Redis not available ({e}), caching disabled")

    def get(self, key):
        """Get value from cache."""
        if not self.enabled:
            return None
        try:
            if self.redis_client is None:
                return None
            value = self.redis_client.get(key)
            # redis returns bytes; decode via json if present
            return json.loads(value) if value else None
        except (redis.RedisError, json.JSONDecodeError, TypeError):
            return None

    def set(self, key, value, timeout=300):
        """Set value in cache with timeout in seconds."""
        if not self.enabled:
            return False
        try:
            if self.redis_client is None:
                return False
            payload = json.dumps(value, default=str)
            return self.redis_client.setex(key, timeout, payload)
        except (redis.RedisError, TypeError):
            return False

    def delete(self, key):
        """Delete key from cache."""
        if not self.enabled:
            return False
        try:
            if self.redis_client is None:
                return False
            return self.redis_client.delete(key)
        except redis.RedisError:
            return False

    def delete_pattern(self, pattern):
        """Delete all keys matching pattern."""
        if not self.enabled:
            return False
        try:
            if self.redis_client is None:
                return False
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except redis.RedisError:
            return False


# Global cache instance

cache_manager = CacheManager()


def cached(timeout=300, key_prefix=""):
    """Decorator for caching function results."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            fname = f.__name__
            args_repr = str(args) + str(sorted(kwargs.items()))
            cache_key = f"{key_prefix}:{fname}:{hash(args_repr)}"

            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = f(*args, **kwargs)
            cache_manager.set(cache_key, result, timeout)
            return result

        return decorated_function

    return decorator


def invalidate_cache_pattern(pattern):
    """Invalidate all cache keys matching pattern."""

    return cache_manager.delete_pattern(pattern)


# Specific cache functions for common operations


@cached(timeout=3600, key_prefix="categories")
def get_cached_categories():
    """Get cached categories list."""

    from .models.inventory import Category

    categories = Category.query.all()
    cats = []
    for c in categories:
        cats.append({"id": c.id, "name": c.name, "description": c.description})
    return cats


@cached(timeout=1800, key_prefix="products")
def get_cached_products_page(page=1, per_page=20, search=""):
    """Get cached products page."""

    from .models.product_unified import Product
    from sqlalchemy import or_

    query = Product.query.filter(Product.is_active.is_(True))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.like(search_term),
                Product.sku.like(search_term),
                Product.barcode.like(search_term),
            )
        )

    products = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "products": [p.to_dict() for p in products.items],
        "pagination": {
            "page": products.page,
            "pages": products.pages,
            "per_page": products.per_page,
            "total": products.total,
        },
    }


@cached(timeout=600, key_prefix="stock")
def get_cached_stock_levels():
    """Get cached stock levels for all products."""

    from .models.product_unified import Product

    products = Product.query.filter(Product.is_active.is_(True)).all()
    return {p.id: p.get_current_stock() for p in products}


def invalidate_product_cache(product_id=None):
    """Invalidate product-related cache."""

    patterns = ["products:*", "stock:*"]
    if product_id:
        patterns.append(f"product:{product_id}:*")

    for pattern in patterns:
        invalidate_cache_pattern(pattern)


def invalidate_category_cache():
    """Invalidate category-related cache."""

    invalidate_cache_pattern("categories:*")


def invalidate_all_cache():
    """Invalidate all application cache."""

    invalidate_cache_pattern("*")


# Cache warming functions


# pylint: disable=broad-exception-caught
def warm_cache():
    """Warm up frequently accessed cache entries."""
    try:
        # Warm categories cache
        get_cached_categories()

        # Warm first page of products
        get_cached_products_page(page=1)

        # Warm stock levels
        get_cached_stock_levels()

        print("Cache warmed successfully!")
        return True
    except Exception as e:
        print(f"Cache warming failed: {e}")
        return False


# Flask integration


def init_cache(app):
    """Initialize cache with Flask app and return manager instance."""

    redis_url = app.config.get("REDIS_URL", "redis://localhost:5606/0")
    manager = CacheManager(redis_url)

    # Store in app extensions for access throughout app
    app.extensions = getattr(app, "extensions", {})
    app.extensions["cache_manager"] = manager

    # Add cache warming on startup
    with app.app_context():
        warm_cache()

    return manager
