"""
Flask Tenant Middleware
وسيط المستأجر لـ Flask

Multi-tenancy middleware for Flask applications.
Extracts tenant from request and sets up tenant context.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17

Usage:
    from src.middleware.flask_tenant_middleware import init_tenant_middleware
    init_tenant_middleware(app)
"""

from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Optional, Callable

from flask import Flask, request, g, jsonify

if TYPE_CHECKING:
    pass  # For future type imports

logger = logging.getLogger(__name__)

# Paths that don't require tenant context
EXEMPT_PATHS = [
    '/api/auth/',
    '/api/health',
    '/api/docs',
    '/api/tenants/plans',
    '/api/tenants/check-slug',
    '/static/',
    '/favicon.ico',
]

# Paths that are tenant-management only (super admin)
TENANT_ADMIN_PATHS = [
    '/api/tenants',
]


def get_tenant_from_request() -> Optional[str]:
    """
    استخراج معرف المستأجر من الطلب
    Extract tenant identifier from request.

    Priority:
    1. X-Tenant-ID header
    2. Subdomain (tenant.domain.com)
    3. Query parameter (?tenant_id=xxx)

    Returns:
        str: Tenant ID or None
    """
    # 1. Check header
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        logger.debug(f"Tenant from header: {tenant_id}")
        return tenant_id

    # 2. Check subdomain
    host = request.host.split(':')[0]  # Remove port
    parts = host.split('.')

    # Skip for localhost or IP addresses
    if host in ('localhost', '127.0.0.1') or host.replace('.', '').isdigit():
        pass
    elif len(parts) >= 3:
        # Subdomain detected (e.g., tenant.gaara-erp.com)
        subdomain = parts[0]
        if subdomain not in ('www', 'api', 'admin', 'app'):
            logger.debug(f"Tenant from subdomain: {subdomain}")
            return subdomain

    # 3. Check query parameter (for development/testing)
    tenant_id = request.args.get('tenant_id')
    if tenant_id:
        logger.debug(f"Tenant from query: {tenant_id}")
        return tenant_id

    return None


def load_tenant(tenant_identifier: str) -> Optional[dict]:
    """
    تحميل بيانات المستأجر
    Load tenant data from database.

    Args:
        tenant_identifier: Tenant ID, slug, or schema_name

    Returns:
        dict: Tenant data or None
    """
    try:
        # Import here to avoid circular imports
        from src.models.tenant_sqlalchemy import Tenant
        from src.models.user import db

        # Try to find by ID first (UUID)
        try:
            import uuid
            uuid.UUID(tenant_identifier)
            tenant = db.session.query(Tenant).filter_by(id=tenant_identifier).first()
            if tenant:
                return tenant_to_dict(tenant)
        except (ValueError, AttributeError):
            pass

        # Try by slug
        tenant = db.session.query(Tenant).filter_by(slug=tenant_identifier).first()
        if tenant:
            return tenant_to_dict(tenant)

        # Try by schema_name
        tenant = db.session.query(Tenant).filter_by(schema_name=tenant_identifier).first()
        if tenant:
            return tenant_to_dict(tenant)

        logger.warning(f"Tenant not found: {tenant_identifier}")
        return None

    except Exception as e:
        logger.error(f"Error loading tenant: {e}")
        return None


def tenant_to_dict(tenant) -> dict:
    """
    تحويل كائن المستأجر إلى قاموس
    Convert tenant object to dictionary.
    """
    return {
        'id': str(tenant.id),
        'name': tenant.name,
        'name_ar': tenant.name_ar,
        'slug': tenant.slug,
        'schema_name': tenant.schema_name,
        'status': tenant.status,
        'plan_code': tenant.plan_code,
        'is_active': tenant.is_active,
        'max_users': tenant.max_users,
        'max_storage_gb': tenant.max_storage_gb,
    }


def is_exempt_path(path: str) -> bool:
    """
    التحقق مما إذا كان المسار معفى
    Check if path is exempt from tenant requirement.
    """
    return any(path.startswith(exempt) for exempt in EXEMPT_PATHS)


def is_tenant_admin_path(path: str) -> bool:
    """
    التحقق مما إذا كان المسار لإدارة المستأجرين
    Check if path is for tenant administration.
    """
    return any(path.startswith(admin) for admin in TENANT_ADMIN_PATHS)


def tenant_middleware():
    """
    وسيط المستأجر
    Tenant middleware function.

    Sets g.tenant and g.tenant_id for the request.
    """
    # Skip for exempt paths
    if is_exempt_path(request.path):
        g.tenant = None
        g.tenant_id = None
        return

    # Skip tenant requirement for tenant admin paths (handled separately)
    if is_tenant_admin_path(request.path):
        g.tenant = None
        g.tenant_id = None
        return

    # Get tenant identifier
    tenant_identifier = get_tenant_from_request()

    if not tenant_identifier:
        g.tenant = None
        g.tenant_id = None
        return

    # Load tenant
    tenant = load_tenant(tenant_identifier)

    if not tenant:
        g.tenant = None
        g.tenant_id = None
        return

    # Check tenant is active
    if not tenant.get('is_active') or tenant.get('status') == 'suspended':
        g.tenant = None
        g.tenant_id = None
        logger.warning(f"Inactive tenant access attempt: {tenant_identifier}")
        return

    # Set tenant context
    g.tenant = tenant
    g.tenant_id = tenant['id']

    logger.debug(f"Tenant context set: {tenant['slug']} ({tenant['id']})")


def init_tenant_middleware(app: Flask) -> None:
    """
    تهيئة وسيط المستأجر
    Initialize tenant middleware for Flask app.

    Args:
        app: Flask application instance
    """
    @app.before_request
    def before_request_tenant():
        """Set up tenant context before each request."""
        tenant_middleware()

    @app.after_request
    def after_request_tenant(response):
        """Add tenant info to response headers (for debugging)."""
        if hasattr(g, 'tenant_id') and g.tenant_id:
            response.headers['X-Tenant-ID'] = g.tenant_id
        return response

    logger.info("Tenant middleware initialized")


def require_tenant(f: Callable) -> Callable:
    """
    مزخرف لطلب سياق المستأجر
    Decorator to require tenant context.

    Usage:
        @app.route('/api/products')
        @require_tenant
        def get_products():
            tenant = g.tenant
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'tenant') or not g.tenant:
            return jsonify({
                'success': False,
                'error': 'TENANT_REQUIRED',
                'message': 'Tenant context required',
                'message_ar': 'سياق المستأجر مطلوب'
            }), 400
        return f(*args, **kwargs)
    return decorated_function


def get_current_tenant() -> Optional[dict]:
    """
    الحصول على المستأجر الحالي
    Get current tenant from context.

    Returns:
        dict: Current tenant or None
    """
    return getattr(g, 'tenant', None)


def get_current_tenant_id() -> Optional[str]:
    """
    الحصول على معرف المستأجر الحالي
    Get current tenant ID from context.

    Returns:
        str: Current tenant ID or None
    """
    return getattr(g, 'tenant_id', None)


def filter_by_tenant(query, model):
    """
    تصفية الاستعلام حسب المستأجر
    Filter SQLAlchemy query by current tenant.

    Args:
        query: SQLAlchemy query object
        model: Model class with tenant_id column

    Returns:
        Filtered query
    """
    tenant_id = get_current_tenant_id()

    if not tenant_id:
        return query

    if hasattr(model, 'tenant_id'):
        return query.filter(model.tenant_id == tenant_id)

    return query


class TenantMixin:
    """
    مكسين المستأجر للنماذج
    Mixin for models that belong to a tenant.

    Automatically filters queries by current tenant.

    Usage:
        class Product(db.Model, TenantMixin):
            tenant_id = Column(UUID, ForeignKey('tenants.id'))
            ...
    """

    @classmethod
    def query_for_tenant(cls, session=None):
        """Get query filtered by current tenant."""
        from src.models.user import db

        session = session or db.session
        query = session.query(cls)

        tenant_id = get_current_tenant_id()
        if tenant_id and hasattr(cls, 'tenant_id'):
            query = query.filter(cls.tenant_id == tenant_id)

        return query


# Export public API
__all__ = [
    'init_tenant_middleware',
    'require_tenant',
    'get_current_tenant',
    'get_current_tenant_id',
    'filter_by_tenant',
    'TenantMixin',
]
