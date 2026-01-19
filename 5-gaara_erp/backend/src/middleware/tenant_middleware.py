"""
Tenant Middleware for Multi-Tenancy Routing
وسيط المستأجر لتوجيه تعدد المستأجرين

This middleware identifies the tenant from the request and switches
the database schema accordingly.

Identification methods (in order of priority):
1. X-Tenant-ID header
2. Subdomain (tenant.gaara-erp.com)
3. Custom domain (erp.company.com)

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, Callable

from django.db import connection
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

if TYPE_CHECKING:
    from backend.src.models.tenant import Tenant

logger = logging.getLogger(__name__)


# Cache tenant lookups for 5 minutes
TENANT_CACHE_TTL = 300


class TenantNotFoundError(Exception):
    """
    Raised when tenant cannot be identified.
    يُرفع عند عدم التمكن من تحديد المستأجر.
    """


class TenantInactiveError(Exception):
    """
    Raised when tenant is found but inactive.
    يُرفع عند العثور على مستأجر غير نشط.
    """


class TenantMiddleware(MiddlewareMixin):
    """
    Django middleware for multi-tenant request routing.
    وسيط Django لتوجيه طلبات تعدد المستأجرين.

    This middleware:
    1. Identifies the tenant from the request
    2. Validates tenant is active
    3. Switches PostgreSQL schema
    4. Attaches tenant to request object
    5. Resets schema to 'public' after response

    Attributes:
        EXEMPT_PATHS: List of paths that don't require tenant
        EXEMPT_PREFIXES: URL prefixes that bypass tenant check
        HEADER_NAME: HTTP header for explicit tenant ID

    Example:
        # In settings.py MIDDLEWARE:
        'backend.src.middleware.tenant_middleware.TenantMiddleware',
    """

    # Paths that don't require tenant identification
    EXEMPT_PATHS = frozenset([
        '/api/auth/login',
        '/api/auth/register',
        '/api/auth/forgot-password',
        '/api/auth/reset-password',
        '/api/health',
        '/api/health/',
        '/health',
        '/health/',
        '/api/public',
        '/api/tenants/create',  # Creating new tenant
        '/admin',
        '/static',
        '/media',
        '/',
    ])

    # Prefixes that bypass tenant check
    EXEMPT_PREFIXES = (
        '/admin/',
        '/static/',
        '/media/',
        '/__debug__/',
        '/api/public/',
        '/api/docs/',
        '/api/schema/',
        '/swagger/',
        '/redoc/',
    )

    # Header name for explicit tenant ID
    HEADER_NAME = 'HTTP_X_TENANT_ID'
    HEADER_SLUG = 'HTTP_X_TENANT_SLUG'

    def __init__(self, get_response: Callable) -> None:
        """
        Initialize middleware with response handler.

        Args:
            get_response: The next middleware or view
        """
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request through tenant middleware.

        Args:
            request: The incoming HTTP request

        Returns:
            HttpResponse: The response from the view or error response
        """
        # Check if path is exempt
        if self._is_exempt_path(request.path):
            request.tenant = None
            return self.get_response(request)

        try:
            # Resolve tenant
            tenant = self._resolve_tenant(request)

            if tenant is None:
                return self._tenant_not_found_response()

            if not tenant.is_active:
                return self._tenant_inactive_response(tenant)

            # Check subscription status
            if not tenant.is_subscription_active:
                return self._subscription_expired_response(tenant)

            # Attach tenant to request
            request.tenant = tenant

            # Switch to tenant schema
            self._activate_tenant_schema(tenant)

            # Process request
            response = self.get_response(request)

            # Reset to public schema
            self._reset_schema()

            # Add tenant info to response headers (for debugging)
            if settings.DEBUG:
                response['X-Tenant-ID'] = str(tenant.id)
                response['X-Tenant-Slug'] = tenant.slug

            return response

        except TenantNotFoundError:
            return self._tenant_not_found_response()
        except TenantInactiveError as e:
            return self._tenant_inactive_response(e.tenant)
        except Exception as e:
            logger.error(f"Tenant middleware error: {e}", exc_info=True)
            self._reset_schema()
            return self._error_response(str(e))

    def _is_exempt_path(self, path: str) -> bool:
        """
        Check if the path is exempt from tenant identification.

        Args:
            path: The request path

        Returns:
            bool: True if path is exempt
        """
        # Exact match
        if path in self.EXEMPT_PATHS:
            return True

        # Prefix match
        if path.startswith(self.EXEMPT_PREFIXES):
            return True

        return False

    def _resolve_tenant(self, request: HttpRequest) -> Optional['Tenant']:
        """
        Resolve tenant from request using multiple methods.

        Resolution order:
        1. X-Tenant-ID header (UUID)
        2. X-Tenant-Slug header (slug string)
        3. Subdomain
        4. Custom domain

        Args:
            request: The HTTP request

        Returns:
            Tenant or None: The resolved tenant
        """
        # Import here to avoid circular imports
        from backend.src.models.tenant import Tenant

        # Method 1: X-Tenant-ID header
        tenant_id = request.META.get(self.HEADER_NAME)
        if tenant_id:
            return self._get_tenant_by_id(tenant_id)

        # Method 2: X-Tenant-Slug header
        tenant_slug = request.META.get(self.HEADER_SLUG)
        if tenant_slug:
            return self._get_tenant_by_slug(tenant_slug)

        # Method 3: Subdomain
        host = request.get_host().lower()
        tenant = self._get_tenant_by_subdomain(host)
        if tenant:
            return tenant

        # Method 4: Custom domain
        tenant = self._get_tenant_by_custom_domain(host)
        if tenant:
            return tenant

        return None

    def _get_tenant_by_id(self, tenant_id: str) -> Optional['Tenant']:
        """
        Get tenant by UUID from header.

        Args:
            tenant_id: UUID string

        Returns:
            Tenant or None
        """
        from backend.src.models.tenant import Tenant

        cache_key = f"tenant:id:{tenant_id}"
        tenant = cache.get(cache_key)

        if tenant is None:
            try:
                tenant = Tenant.objects.select_related('plan').get(id=tenant_id)
                cache.set(cache_key, tenant, TENANT_CACHE_TTL)
            except Tenant.DoesNotExist:
                return None
            except Exception:
                logger.warning("Invalid tenant ID format: %s", tenant_id)
                return None

        return tenant

    def _get_tenant_by_slug(self, slug: str) -> Optional['Tenant']:
        """
        Get tenant by slug.

        Args:
            slug: Tenant slug string

        Returns:
            Tenant or None
        """
        from backend.src.models.tenant import Tenant

        cache_key = f"tenant:slug:{slug}"
        tenant = cache.get(cache_key)

        if tenant is None:
            try:
                tenant = Tenant.objects.select_related('plan').get(slug=slug)
                cache.set(cache_key, tenant, TENANT_CACHE_TTL)
            except Tenant.DoesNotExist:
                return None

        return tenant

    def _get_tenant_by_subdomain(self, host: str) -> Optional['Tenant']:
        """
        Extract tenant from subdomain.

        Expected format: {tenant-slug}.{domain}
        Example: acme.gaara-erp.com -> tenant 'acme'

        Args:
            host: Full hostname

        Returns:
            Tenant or None
        """
        from backend.src.models.tenant import Tenant

        # Get base domain from settings
        base_domain = getattr(settings, 'TENANT_BASE_DOMAIN', 'gaara-erp.com')

        # Remove port if present
        host = host.split(':')[0]

        # Check if host ends with base domain
        if not host.endswith(base_domain):
            return None

        # Extract subdomain
        subdomain = host[:-len(base_domain)].rstrip('.')

        if not subdomain or subdomain == 'www':
            return None

        # Look up tenant by subdomain (slug)
        return self._get_tenant_by_slug(subdomain)

    def _get_tenant_by_custom_domain(self, host: str) -> Optional['Tenant']:
        """
        Get tenant by custom domain.

        Args:
            host: Full hostname

        Returns:
            Tenant or None
        """
        from backend.src.models.tenant import Tenant

        # Remove port
        host = host.split(':')[0]

        cache_key = f"tenant:domain:{host}"
        tenant = cache.get(cache_key)

        if tenant is None:
            try:
                tenant = Tenant.objects.select_related('plan').get(
                    custom_domain=host
                )
                cache.set(cache_key, tenant, TENANT_CACHE_TTL)
            except Tenant.DoesNotExist:
                return None

        return tenant

    def _activate_tenant_schema(self, tenant: 'Tenant') -> None:
        """
        Switch database connection to tenant's schema.

        Args:
            tenant: The tenant to activate
        """
        schema_name = tenant.schema_name
        try:
            with connection.cursor() as cursor:
                # Set search path to tenant schema first, then public
                cursor.execute(
                    f"SET search_path TO {schema_name}, public"
                )
            logger.debug(f"Activated schema: {schema_name}")
        except Exception as e:
            logger.error(f"Failed to activate schema {schema_name}: {e}")
            raise

    def _reset_schema(self) -> None:
        """
        Reset database connection to public schema.
        إعادة تعيين اتصال قاعدة البيانات إلى المخطط العام.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO public")
        except Exception as e:
            logger.error(f"Failed to reset schema: {e}")

    def _tenant_not_found_response(self) -> JsonResponse:
        """
        Return JSON response for tenant not found.

        Returns:
            JsonResponse: 404 response
        """
        return JsonResponse(
            {
                'success': False,
                'error': 'TENANT_NOT_FOUND',
                'error_ar': 'لم يتم العثور على المستأجر',
                'message': 'The requested tenant could not be found.',
                'message_ar': 'لم يتم العثور على المستأجر المطلوب.'
            },
            status=404
        )

    def _tenant_inactive_response(self, tenant: 'Tenant') -> JsonResponse:
        """
        Return JSON response for inactive tenant.

        Args:
            tenant: The inactive tenant

        Returns:
            JsonResponse: 403 response
        """
        return JsonResponse(
            {
                'success': False,
                'error': 'TENANT_INACTIVE',
                'error_ar': 'المستأجر غير نشط',
                'message': f'Tenant "{tenant.name}" is currently inactive.',
                'message_ar': f'المستأجر "{tenant.name_ar or tenant.name}" غير نشط حالياً.',
                'status': tenant.status
            },
            status=403
        )

    def _subscription_expired_response(self, tenant: 'Tenant') -> JsonResponse:
        """
        Return JSON response for expired subscription.

        Args:
            tenant: The tenant with expired subscription

        Returns:
            JsonResponse: 402 Payment Required response
        """
        return JsonResponse(
            {
                'success': False,
                'error': 'SUBSCRIPTION_EXPIRED',
                'error_ar': 'انتهى الاشتراك',
                'message': 'Your subscription has expired. Please renew.',
                'message_ar': 'انتهت صلاحية اشتراكك. يرجى التجديد.',
                'tenant_id': str(tenant.id),
                'tenant_slug': tenant.slug
            },
            status=402
        )

    def _error_response(self, message: str) -> JsonResponse:
        """
        Return generic error response.

        Args:
            message: Error message

        Returns:
            JsonResponse: 500 response
        """
        return JsonResponse(
            {
                'success': False,
                'error': 'TENANT_ERROR',
                'error_ar': 'خطأ في المستأجر',
                'message': message if settings.DEBUG else 'An internal error occurred.',
                'message_ar': 'حدث خطأ داخلي.'
            },
            status=500
        )


def get_current_tenant(request: HttpRequest) -> Optional['Tenant']:
    """
    Get the current tenant from request.
    الحصول على المستأجر الحالي من الطلب.

    Utility function for views and other code.

    Args:
        request: The HTTP request

    Returns:
        Tenant or None: The current tenant

    Example:
        >>> tenant = get_current_tenant(request)
        >>> if tenant:
        ...     print(f"Current tenant: {tenant.name}")
    """
    return getattr(request, 'tenant', None)


def require_tenant(view_func: Callable) -> Callable:
    """
    Decorator to require tenant for a view.
    مزخرف لطلب مستأجر للعرض.

    Args:
        view_func: The view function to wrap

    Returns:
        Callable: Wrapped view function

    Example:
        >>> @require_tenant
        ... def my_view(request):
        ...     tenant = request.tenant
        ...     return JsonResponse({'tenant': tenant.name})
    """
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        tenant = get_current_tenant(request)
        if tenant is None:
            return JsonResponse(
                {
                    'success': False,
                    'error': 'TENANT_REQUIRED',
                    'error_ar': 'المستأجر مطلوب',
                    'message': 'This endpoint requires a valid tenant.',
                    'message_ar': 'هذه النقطة النهائية تتطلب مستأجرًا صالحًا.'
                },
                status=400
            )
        return view_func(request, *args, **kwargs)

    return wrapper


def tenant_schema_context(tenant: 'Tenant'):
    """
    Context manager for executing code in a tenant's schema.
    مدير سياق لتنفيذ الكود في مخطط المستأجر.

    Args:
        tenant: The tenant whose schema to use

    Yields:
        None

    Example:
        >>> with tenant_schema_context(tenant):
        ...     products = Product.objects.all()
        ...     print(f"Found {products.count()} products")
    """
    from contextlib import contextmanager

    @contextmanager
    def context():
        original_search_path = None
        try:
            # Save current search path
            with connection.cursor() as cursor:
                cursor.execute("SHOW search_path")
                original_search_path = cursor.fetchone()[0]

            # Switch to tenant schema
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SET search_path TO {tenant.schema_name}, public"
                )

            yield

        finally:
            # Restore original search path
            if original_search_path:
                with connection.cursor() as cursor:
                    cursor.execute(f"SET search_path TO {original_search_path}")
            else:
                with connection.cursor() as cursor:
                    cursor.execute("SET search_path TO public")

    return context()


class TenantAwareQuerySet:
    """
    Mixin for QuerySets to automatically filter by current tenant.
    مزيج لمجموعات الاستعلام للتصفية تلقائياً حسب المستأجر الحالي.

    Usage in models:
        class MyModel(models.Model):
            tenant = models.ForeignKey(Tenant, ...)

            class Meta:
                # If using with custom manager
                pass

    Note: This is optional - schema-based isolation provides
    automatic data separation. This is useful for shared tables.
    """

    def for_tenant(self, tenant: 'Tenant'):
        """
        Filter queryset by tenant.

        Args:
            tenant: The tenant to filter by

        Returns:
            QuerySet: Filtered queryset
        """
        return self.filter(tenant=tenant)

    def for_request(self, request: HttpRequest):
        """
        Filter queryset by tenant from request.

        Args:
            request: HTTP request with tenant

        Returns:
            QuerySet: Filtered queryset
        """
        tenant = get_current_tenant(request)
        if tenant:
            return self.for_tenant(tenant)
        return self.none()
