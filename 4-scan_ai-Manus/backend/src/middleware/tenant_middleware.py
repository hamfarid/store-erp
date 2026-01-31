"""
FILE: backend/src/middleware/tenant_middleware.py | PURPOSE: Multi-tenant middleware
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

Tenant Middleware - Multi-tenant Data Isolation

Provides automatic tenant context extraction and query filtering.

Version: 1.0.0
"""

import logging
from contextvars import ContextVar
from typing import Optional

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Context variable for current tenant
_current_tenant_id: ContextVar[Optional[int]] = ContextVar(
    'current_tenant_id', default=None
)


def get_current_tenant_id() -> Optional[int]:
    """Get the current tenant ID from context"""
    return _current_tenant_id.get()


def set_current_tenant_id(tenant_id: Optional[int]) -> None:
    """Set the current tenant ID in context"""
    _current_tenant_id.set(tenant_id)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract and set tenant context from JWT token.
    
    The tenant_id is extracted from the JWT payload and stored in
    request.state and context variable for use in queries.
    """

    # Paths that don't require tenant context
    EXEMPT_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/api/v1/health",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/forgot-password",
        "/api/v1/auth/reset-password",
    ]

    async def dispatch(self, request: Request, call_next):
        # Skip tenant check for exempt paths
        path = request.url.path
        if any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS):
            return await call_next(request)

        # Extract tenant_id from request state (set by auth middleware)
        tenant_id = getattr(request.state, 'tenant_id', None)

        # Also check for X-Tenant-ID header (for system admins)
        if not tenant_id:
            tenant_header = request.headers.get('X-Tenant-ID')
            if tenant_header:
                try:
                    tenant_id = int(tenant_header)
                except ValueError:
                    pass

        # Set tenant context
        set_current_tenant_id(tenant_id)
        request.state.tenant_id = tenant_id

        try:
            response = await call_next(request)
            return response
        finally:
            # Clear tenant context after request
            set_current_tenant_id(None)


def tenant_filter(query, model, tenant_id: Optional[int] = None):
    """
    Apply tenant filter to a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        model: Model class with tenant_id column
        tenant_id: Optional tenant ID (uses context if not provided)
    
    Returns:
        Filtered query
    """
    if tenant_id is None:
        tenant_id = get_current_tenant_id()

    if tenant_id is not None and hasattr(model, 'tenant_id'):
        return query.filter(model.tenant_id == tenant_id)

    return query


def require_tenant(func):
    """
    Decorator to require tenant context for an endpoint.
    Raises 403 if no tenant context is available.
    """
    from functools import wraps

    @wraps(func)
    async def wrapper(*args, **kwargs):
        tenant_id = get_current_tenant_id()
        if tenant_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant context required"
            )
        return await func(*args, **kwargs)

    return wrapper


def require_same_tenant(resource_tenant_id: int) -> bool:
    """
    Check if the current tenant matches the resource's tenant.
    
    Args:
        resource_tenant_id: The tenant_id of the resource being accessed
    
    Returns:
        True if access is allowed, raises HTTPException otherwise
    """
    current_tenant = get_current_tenant_id()

    # System admins (no tenant) can access all
    if current_tenant is None:
        return True

    if current_tenant != resource_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: resource belongs to different tenant"
        )

    return True

