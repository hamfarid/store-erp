# -*- coding: utf-8 -*-
"""
Query Optimizer with Caching
=============================

Optimize database queries with intelligent caching.
Part of T25: Database Optimization

Features:
- Query result caching
- Cache invalidation
- Query optimization hints
- Lazy loading helpers
- Batch loading utilities
"""

import hashlib
import pickle
from typing import Any, Optional, List, Callable, Dict
from functools import wraps
from datetime import datetime, timedelta
import logging
from flask import g
from sqlalchemy.orm import Query, joinedload, selectinload
from database import db

logger = logging.getLogger(__name__)


class QueryCache:
    """Simple in-memory query cache."""

    def __init__(self, ttl_seconds: int = 300):
        """
        Initialize cache.

        Args:
            ttl_seconds: Time to live in seconds (default: 5 minutes)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def _generate_key(self, query: str, params: tuple) -> str:
        """Generate cache key from query and parameters."""
        key_str = f"{query}:{params}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, query: str, params: tuple = ()) -> Optional[Any]:
        """
        Get cached result.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Cached result or None
        """
        key = self._generate_key(query, params)

        if key in self.cache:
            entry = self.cache[key]

            # Check if expired
            if datetime.utcnow() < entry["expires_at"]:
                logger.debug(f"Cache HIT: {query[:50]}...")
                return entry["result"]
            else:
                # Remove expired entry
                del self.cache[key]
                logger.debug(f"Cache EXPIRED: {query[:50]}...")

        logger.debug(f"Cache MISS: {query[:50]}...")
        return None

    def set(self, query: str, params: tuple, result: Any):
        """
        Cache query result.

        Args:
            query: SQL query string
            params: Query parameters
            result: Query result to cache
        """
        key = self._generate_key(query, params)

        self.cache[key] = {
            "result": result,
            "expires_at": datetime.utcnow() + timedelta(seconds=self.ttl_seconds),
            "created_at": datetime.utcnow(),
        }

        logger.debug(f"Cache SET: {query[:50]}...")

    def invalidate(self, pattern: Optional[str] = None):
        """
        Invalidate cache entries.

        Args:
            pattern: Pattern to match (invalidates all if None)
        """
        if pattern is None:
            # Clear all
            count = len(self.cache)
            self.cache.clear()
            logger.info(f"Cache cleared: {count} entries")
        else:
            # Clear matching pattern
            keys_to_delete = [
                key for key in self.cache.keys() if pattern in str(self.cache[key])
            ]
            for key in keys_to_delete:
                del self.cache[key]
            logger.info(
                f"Cache invalidated: {len(keys_to_delete)} entries matching '{pattern}'"
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = len(self.cache)
        expired = sum(
            1
            for entry in self.cache.values()
            if datetime.utcnow() >= entry["expires_at"]
        )

        return {
            "total_entries": total,
            "active_entries": total - expired,
            "expired_entries": expired,
            "ttl_seconds": self.ttl_seconds,
        }


# Global cache instance
query_cache = QueryCache(ttl_seconds=300)  # 5 minutes default


def cached_query(ttl_seconds: Optional[int] = None):
    """
    Decorator to cache query results.

    Args:
        ttl_seconds: Time to live (uses default if None)

    Usage:
        @cached_query(ttl_seconds=60)
        def get_active_products():
            return Product.query.filter_by(is_active=True).all()
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{args}:{sorted(kwargs.items())}"

            # Try to get from cache
            result = query_cache.get(cache_key, ())

            if result is not None:
                return result

            # Execute query
            result = func(*args, **kwargs)

            # Cache result
            if ttl_seconds:
                # Temporarily change TTL
                original_ttl = query_cache.ttl_seconds
                query_cache.ttl_seconds = ttl_seconds
                query_cache.set(cache_key, (), result)
                query_cache.ttl_seconds = original_ttl
            else:
                query_cache.set(cache_key, (), result)

            return result

        return wrapper

    return decorator


def invalidate_cache(pattern: Optional[str] = None):
    """
    Invalidate query cache.

    Args:
        pattern: Pattern to match (invalidates all if None)
    """
    query_cache.invalidate(pattern)


def optimize_query(query: Query, eager_load: Optional[List[str]] = None) -> Query:
    """
    Optimize SQLAlchemy query.

    Args:
        query: SQLAlchemy query object
        eager_load: List of relationships to eager load

    Returns:
        Optimized query
    """
    if eager_load:
        for relationship in eager_load:
            # Use joinedload for one-to-one/many-to-one
            # Use selectinload for one-to-many/many-to-many
            query = query.options(selectinload(relationship))

    return query


def batch_load(
    model_class, ids: List[int], eager_load: Optional[List[str]] = None
) -> List[Any]:
    """
    Batch load multiple records by IDs.

    Args:
        model_class: SQLAlchemy model class
        ids: List of IDs to load
        eager_load: List of relationships to eager load

    Returns:
        List of model instances
    """
    query = model_class.query.filter(model_class.id.in_(ids))

    if eager_load:
        query = optimize_query(query, eager_load)

    return query.all()


def paginate_efficiently(
    query: Query, page: int, per_page: int, max_per_page: int = 100
) -> Dict[str, Any]:
    """
    Efficient pagination with count optimization.

    Args:
        query: SQLAlchemy query
        page: Page number (1-indexed)
        per_page: Items per page
        max_per_page: Maximum items per page

    Returns:
        Pagination result with items and metadata
    """
    # Limit per_page
    per_page = min(per_page, max_per_page)

    # Calculate offset
    offset = (page - 1) * per_page

    # Get items
    items = query.limit(per_page).offset(offset).all()

    # Only count if we need to know total pages
    # (Skip count for better performance if not needed)
    total = None
    if len(items) == per_page:
        # There might be more pages
        total = query.count()
    else:
        # This is the last page
        total = offset + len(items)

    return {
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page if total else page,
        "has_next": len(items) == per_page,
        "has_prev": page > 1,
    }


# Query optimization helpers


def get_or_404(model_class, id: int, eager_load: Optional[List[str]] = None):
    """
    Get record by ID or raise 404.

    Args:
        model_class: SQLAlchemy model class
        id: Record ID
        eager_load: List of relationships to eager load

    Returns:
        Model instance

    Raises:
        404 if not found
    """
    query = model_class.query.filter_by(id=id)

    if eager_load:
        query = optimize_query(query, eager_load)

    return query.first_or_404()


def exists(model_class, **filters) -> bool:
    """
    Check if record exists (optimized).

    Args:
        model_class: SQLAlchemy model class
        **filters: Filter conditions

    Returns:
        True if exists, False otherwise
    """
    return db.session.query(model_class.query.filter_by(**filters).exists()).scalar()


def count_efficiently(query: Query) -> int:
    """
    Count query results efficiently.

    Args:
        query: SQLAlchemy query

    Returns:
        Count of results
    """
    # Use subquery for complex queries
    return db.session.query(query.subquery()).count()


# Context manager for query tracking


class QueryTracker:
    """Track queries executed in a context."""

    def __init__(self):
        self.queries: List[Dict[str, Any]] = []

    def __enter__(self):
        """Start tracking."""
        g.query_tracker = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop tracking."""
        if hasattr(g, "query_tracker"):
            delattr(g, "query_tracker")

    def record_query(self, query: str, duration: float):
        """Record query execution."""
        self.queries.append(
            {"query": query, "duration": duration, "timestamp": datetime.utcnow()}
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get query summary."""
        if not self.queries:
            return {"count": 0, "total_time": 0.0, "avg_time": 0.0}

        total_time = sum(q["duration"] for q in self.queries)

        return {
            "count": len(self.queries),
            "total_time": total_time,
            "avg_time": total_time / len(self.queries),
            "queries": self.queries,
        }
