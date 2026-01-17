# -*- coding: utf-8 -*-
"""
Prometheus Metrics for Store ERP
=================================

Application metrics for monitoring and observability.
Part of T24: Monitoring & Logging Enhancement

Metrics Categories:
- HTTP requests (counter, histogram)
- Database queries (counter, histogram)
- Business operations (counter, gauge)
- System resources (gauge)
- Cache performance (counter)
"""

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Info,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from flask import Response
from functools import wraps
import time
from typing import Callable, Any


# ==================== HTTP Metrics ====================

http_requests_total = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0),
)

http_request_size_bytes = Histogram(
    "http_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "endpoint"],
    buckets=(100, 1000, 10000, 100000, 1000000),
)

http_response_size_bytes = Histogram(
    "http_response_size_bytes",
    "HTTP response size in bytes",
    ["method", "endpoint"],
    buckets=(100, 1000, 10000, 100000, 1000000),
)


# ==================== Database Metrics ====================

db_queries_total = Counter(
    "db_queries_total", "Total database queries", ["operation", "table"]
)

db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds",
    ["operation", "table"],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0),
)

db_connections_active = Gauge(
    "db_connections_active", "Number of active database connections"
)

db_connections_idle = Gauge(
    "db_connections_idle", "Number of idle database connections"
)


# ==================== Business Metrics ====================

products_total = Gauge("products_total", "Total number of products")

products_created_total = Counter("products_created_total", "Total products created")

products_updated_total = Counter("products_updated_total", "Total products updated")

products_deleted_total = Counter("products_deleted_total", "Total products deleted")

invoices_total = Gauge("invoices_total", "Total number of invoices")

invoices_created_total = Counter(
    "invoices_created_total",
    "Total invoices created",
    ["type"],  # 'sales' or 'purchase'
)

invoices_value_total = Counter(
    "invoices_value_total", "Total value of invoices in EGP", ["type"]
)

stock_movements_total = Counter(
    "stock_movements_total",
    "Total stock movements",
    ["type"],  # 'in', 'out', 'transfer'
)

low_stock_products = Gauge(
    "low_stock_products", "Number of products below minimum stock level"
)


# ==================== Authentication Metrics ====================

auth_login_attempts_total = Counter(
    "auth_login_attempts_total",
    "Total login attempts",
    ["status"],  # 'success' or 'failure'
)

auth_active_sessions = Gauge("auth_active_sessions", "Number of active user sessions")

auth_token_refreshes_total = Counter(
    "auth_token_refreshes_total", "Total token refresh operations"
)


# ==================== Cache Metrics ====================

cache_hits_total = Counter("cache_hits_total", "Total cache hits", ["cache_name"])

cache_misses_total = Counter("cache_misses_total", "Total cache misses", ["cache_name"])

cache_size_bytes = Gauge("cache_size_bytes", "Cache size in bytes", ["cache_name"])


# ==================== System Metrics ====================

app_info = Info("app", "Application information")

# Set app info
app_info.info({"version": "1.0.0", "name": "Store ERP", "environment": "production"})


# ==================== Decorators ====================


def track_request_metrics(f: Callable) -> Callable:
    """
    Decorator to track HTTP request metrics.

    Usage:
        @app.route('/api/products')
        @track_request_metrics
        def get_products():
            # ...
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        # Get request info
        from flask import request

        method = request.method
        endpoint = request.endpoint or "unknown"

        try:
            # Execute request
            response = f(*args, **kwargs)

            # Track metrics
            duration = time.time() - start_time
            status = getattr(response, "status_code", 200)

            http_requests_total.labels(
                method=method, endpoint=endpoint, status=status
            ).inc()

            http_request_duration_seconds.labels(
                method=method, endpoint=endpoint
            ).observe(duration)

            # Track request/response size
            if request.content_length:
                http_request_size_bytes.labels(
                    method=method, endpoint=endpoint
                ).observe(request.content_length)

            if hasattr(response, "content_length") and response.content_length:
                http_response_size_bytes.labels(
                    method=method, endpoint=endpoint
                ).observe(response.content_length)

            return response

        except Exception as e:
            # Track error
            http_requests_total.labels(
                method=method, endpoint=endpoint, status=500
            ).inc()
            raise

    return wrapper


def track_db_query(operation: str, table: str):
    """
    Decorator to track database query metrics.

    Usage:
        @track_db_query('SELECT', 'products')
        def get_product(id):
            # ...
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = f(*args, **kwargs)

                # Track metrics
                duration = time.time() - start_time

                db_queries_total.labels(operation=operation, table=table).inc()

                db_query_duration_seconds.labels(
                    operation=operation, table=table
                ).observe(duration)

                return result

            except Exception as e:
                # Still track the query even if it failed
                db_queries_total.labels(operation=operation, table=table).inc()
                raise

        return wrapper

    return decorator


# ==================== Helper Functions ====================


def track_product_created():
    """Track product creation."""
    products_created_total.inc()
    products_total.inc()


def track_product_deleted():
    """Track product deletion."""
    products_deleted_total.inc()
    products_total.dec()


def track_invoice_created(invoice_type: str, value: float):
    """
    Track invoice creation.

    Args:
        invoice_type: 'sales' or 'purchase'
        value: Invoice value in EGP
    """
    invoices_created_total.labels(type=invoice_type).inc()
    invoices_value_total.labels(type=invoice_type).inc(value)
    invoices_total.inc()


def track_stock_movement(movement_type: str):
    """
    Track stock movement.

    Args:
        movement_type: 'in', 'out', or 'transfer'
    """
    stock_movements_total.labels(type=movement_type).inc()


def track_login_attempt(success: bool):
    """
    Track login attempt.

    Args:
        success: True if login successful, False otherwise
    """
    status = "success" if success else "failure"
    auth_login_attempts_total.labels(status=status).inc()


def track_cache_access(cache_name: str, hit: bool):
    """
    Track cache access.

    Args:
        cache_name: Name of the cache
        hit: True if cache hit, False if miss
    """
    if hit:
        cache_hits_total.labels(cache_name=cache_name).inc()
    else:
        cache_misses_total.labels(cache_name=cache_name).inc()


def update_db_connections(active: int, idle: int):
    """
    Update database connection metrics.

    Args:
        active: Number of active connections
        idle: Number of idle connections
    """
    db_connections_active.set(active)
    db_connections_idle.set(idle)


# ==================== Metrics Endpoint ====================


def metrics_endpoint() -> Response:
    """
    Prometheus metrics endpoint.

    Returns:
        Response with metrics in Prometheus format
    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
