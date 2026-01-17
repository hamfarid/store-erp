"""
Performance Middleware for Flask Application
Adds caching, compression, and performance monitoring
"""

from flask import request, make_response, g
from functools import wraps
import time
import gzip
import io
import hashlib
from typing import Any, Callable

# Simple in-memory cache (use Redis in production)
_cache = {}
_cache_ttl = {}


def cache_response(ttl: int = 300):
    """
    Cache decorator for Flask routes

    Args:
        ttl: Time to live in seconds (default: 5 minutes)
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any):
            # Generate cache key from request
            cache_key = _generate_cache_key(request)

            # Check if cached response exists and is valid
            if cache_key in _cache:
                cached_time = _cache_ttl.get(cache_key, 0)
                if time.time() - cached_time < ttl:
                    return _cache[cache_key]

            # Generate new response
            response = f(*args, **kwargs)

            # Cache the response
            _cache[cache_key] = response
            _cache_ttl[cache_key] = time.time()

            return response

        return decorated_function

    return decorator


def _generate_cache_key(req) -> str:
    """Generate unique cache key from request"""
    key_parts = [
        req.path,
        req.query_string.decode("utf-8"),
        req.headers.get("Accept", ""),
        (
            req.headers.get("Authorization", "")[:20]
            if req.headers.get("Authorization")
            else ""
        ),
    ]
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def clear_cache():
    """Clear all cached responses"""
    global _cache, _cache_ttl
    _cache = {}
    _cache_ttl = {}


def gzip_response(f: Callable) -> Callable:
    """
    Compress response with gzip if client supports it
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any):
        response = make_response(f(*args, **kwargs))

        # Check if client accepts gzip
        accept_encoding = request.headers.get("Accept-Encoding", "")

        if "gzip" not in accept_encoding.lower():
            return response

        # Don't compress small responses
        if len(response.get_data()) < 1024:
            return response

        # Compress response
        gzip_buffer = io.BytesIO()
        with gzip.GzipFile(
            mode="wb", fileobj=gzip_buffer, compresslevel=6
        ) as gzip_file:
            gzip_file.write(response.get_data())

        response.set_data(gzip_buffer.getvalue())
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = len(response.get_data())
        response.headers["Vary"] = "Accept-Encoding"

        return response

    return decorated_function


def add_performance_headers(response):
    """Add performance-related headers to response"""
    # Add timing header if available
    if hasattr(g, "start_time"):
        elapsed = time.time() - g.start_time
        response.headers["X-Response-Time"] = f"{elapsed:.3f}s"

    # Add cache control headers
    if request.method == "GET":
        # Cache static resources for 1 hour
        if any(ext in request.path for ext in [".js", ".css", ".png", ".jpg", ".svg"]):
            response.headers["Cache-Control"] = "public, max-age=3600"
        # Cache API responses for 5 minutes
        elif "/api/" in request.path:
            response.headers["Cache-Control"] = "private, max-age=300"

    return response


def track_request_time():
    """Track request processing time"""
    g.start_time = time.time()


def init_performance_middleware(app):
    """Initialize performance middleware for Flask app"""

    @app.before_request
    def before_request():
        track_request_time()

    @app.after_request
    def after_request(response):
        return add_performance_headers(response)

    # Add compression for all responses
    @app.after_request
    def compress_response(response):
        # Skip compression for streaming responses
        if response.is_streamed:
            return response

        # Check if client accepts gzip
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" not in accept_encoding.lower():
            return response

        # Don't compress small responses
        if response.content_length and response.content_length < 1024:
            return response

        # Don't compress already compressed content
        if response.headers.get("Content-Encoding"):
            return response

        # Compress response
        try:
            gzip_buffer = io.BytesIO()
            with gzip.GzipFile(
                mode="wb", fileobj=gzip_buffer, compresslevel=6
            ) as gzip_file:
                gzip_file.write(response.get_data())

            response.set_data(gzip_buffer.getvalue())
            response.headers["Content-Encoding"] = "gzip"
            response.headers["Content-Length"] = len(response.get_data())
            response.headers["Vary"] = "Accept-Encoding"
        except Exception:
            # If compression fails, return original response
            pass

        return response

    return app


# Database query optimization helpers
class QueryOptimizer:
    """Helper class for database query optimization"""

    @staticmethod
    def add_indexes(model, fields):
        """Add indexes to model fields"""
        # This should be done in model definitions
        pass

    @staticmethod
    def optimize_query(query):
        """Optimize SQLAlchemy query"""
        # Add eager loading for relationships
        # Use joinedload() or selectinload() as appropriate
        return query

    @staticmethod
    def batch_load(model, ids, batch_size=100):
        """Load records in batches to avoid memory issues"""
        results = []
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i : i + batch_size]
            batch_results = model.query.filter(model.id.in_(batch_ids)).all()
            results.extend(batch_results)
        return results


# Performance monitoring
class PerformanceMonitor:
    """Monitor application performance"""

    def __init__(self):
        self.metrics = {"requests": 0, "total_time": 0, "slow_requests": []}

    def record_request(self, path, duration):
        """Record request metrics"""
        self.metrics["requests"] += 1
        self.metrics["total_time"] += duration

        # Track slow requests (> 1 second)
        if duration > 1.0:
            self.metrics["slow_requests"].append(
                {"path": path, "duration": duration, "timestamp": time.time()}
            )

            # Keep only last 100 slow requests
            if len(self.metrics["slow_requests"]) > 100:
                self.metrics["slow_requests"] = self.metrics["slow_requests"][-100:]

    def get_stats(self):
        """Get performance statistics"""
        if self.metrics["requests"] == 0:
            return {"average_time": 0, "total_requests": 0}

        return {
            "total_requests": self.metrics["requests"],
            "average_time": self.metrics["total_time"] / self.metrics["requests"],
            "slow_requests_count": len(self.metrics["slow_requests"]),
            "recent_slow_requests": self.metrics["slow_requests"][-10:],
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
