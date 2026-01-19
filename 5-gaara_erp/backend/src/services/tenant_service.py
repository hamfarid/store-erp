"""
Tenant Service - Business Logic for Multi-Tenancy
خدمة المستأجر - منطق الأعمال لتعدد المستأجرين

This service handles all tenant-related business logic including:
- Creating tenants with schema setup
- Updating tenant information
- Managing tenant users
- Handling subscriptions

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, List, Dict, Tuple
from datetime import datetime, timedelta

from django.db import connection, transaction
from django.core.cache import cache
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from backend.src.models.tenant import Tenant, TenantUser

logger = logging.getLogger(__name__)


class TenantServiceError(Exception):
    """
    Base exception for tenant service errors.
    استثناء أساسي لأخطاء خدمة المستأجر.

    Attributes:
        code (str): Error code for API responses
        message_ar (str): Arabic error message
    """

    def __init__(
        self,
        message: str,
        code: str = 'TENANT_ERROR',
        message_ar: str = 'خطأ في المستأجر'
    ):
        """
        Initialize tenant service error.

        Args:
            message: English error message
            code: Error code
            message_ar: Arabic error message
        """
        self.code = code
        self.message_ar = message_ar
        super().__init__(message)


class TenantExistsError(TenantServiceError):
    """Raised when tenant slug or domain already exists."""

    def __init__(self, field: str, value: str):
        super().__init__(
            f"Tenant with {field}='{value}' already exists",
            code='TENANT_EXISTS',
            message_ar=f"المستأجر ب{field}='{value}' موجود مسبقاً"
        )


class TenantQuotaExceededError(TenantServiceError):
    """Raised when tenant exceeds a quota limit."""

    def __init__(self, quota_type: str, limit: int, current: int):
        super().__init__(
            f"Quota exceeded: {quota_type} (limit: {limit}, current: {current})",
            code='QUOTA_EXCEEDED',
            message_ar=f"تم تجاوز الحد: {quota_type}"
        )


class TenantService:
    """
    Service class for tenant management operations.
    فئة خدمة لعمليات إدارة المستأجر.

    This class provides methods for:
    - Creating new tenants with PostgreSQL schema
    - Updating tenant information
    - Managing tenant users and roles
    - Handling subscriptions and quotas

    Example:
        >>> service = TenantService()
        >>> tenant = service.create_tenant(
        ...     name='Acme Corp',
        ...     slug='acme-corp',
        ...     owner=user,
        ...     plan_code='pro'
        ... )
    """

    # Default modules enabled for new tenants
    DEFAULT_MODULES = [
        'core',
        'accounting',
        'inventory',
        'sales',
        'purchasing',
    ]

    # Default settings for new tenants
    DEFAULT_SETTINGS = {
        'timezone': 'Asia/Riyadh',
        'language': 'ar',
        'currency': 'SAR',
        'date_format': 'YYYY-MM-DD',
        'fiscal_year_start_month': 1,
    }

    def __init__(self):
        """Initialize tenant service."""
        pass

    @transaction.atomic
    def create_tenant(
        self,
        name: str,
        slug: str,
        owner,
        name_ar: str = '',
        plan_code: str = 'basic',
        custom_domain: Optional[str] = None,
        settings_override: Optional[Dict] = None,
        trial_days: int = 14
    ) -> 'Tenant':
        """
        Create a new tenant with database schema.

        This method:
        1. Validates the slug is unique
        2. Creates the Tenant record
        3. Creates the PostgreSQL schema
        4. Creates initial tenant settings
        5. Adds owner as TenantUser with 'owner' role

        Args:
            name: Tenant organization name
            slug: URL-safe unique identifier
            owner: User who owns the tenant
            name_ar: Arabic name (optional)
            plan_code: Subscription plan code
            custom_domain: Custom domain (optional)
            settings_override: Override default settings
            trial_days: Number of days for trial period

        Returns:
            Tenant: The created tenant

        Raises:
            TenantExistsError: If slug or domain already exists
            TenantServiceError: If creation fails

        Example:
            >>> tenant = service.create_tenant(
            ...     name='Acme Corporation',
            ...     slug='acme-corp',
            ...     owner=user
            ... )
        """
        from backend.src.models.tenant import (
            Tenant, TenantPlan, TenantUser, TenantSettings
        )

        # Validate slug uniqueness
        if Tenant.objects.filter(slug=slug).exists():
            raise TenantExistsError('slug', slug)

        # Validate custom domain uniqueness
        if custom_domain and Tenant.objects.filter(custom_domain=custom_domain).exists():
            raise TenantExistsError('custom_domain', custom_domain)

        # Get plan
        try:
            plan = TenantPlan.objects.get(code=plan_code, is_active=True)
        except TenantPlan.DoesNotExist:
            plan = None
            logger.warning(f"Plan '{plan_code}' not found, creating tenant without plan")

        # Generate schema name
        schema_name = f"tenant_{slug.replace('-', '_')}"

        # Calculate trial end date
        from django.utils import timezone
        trial_ends_at = timezone.now() + timedelta(days=trial_days)

        # Create tenant
        tenant = Tenant.objects.create(
            name=name,
            name_ar=name_ar or name,
            slug=slug,
            schema_name=schema_name,
            custom_domain=custom_domain,
            plan=plan,
            owner=owner,
            status=Tenant.TenantStatus.TRIAL,
            trial_ends_at=trial_ends_at,
            settings=self.DEFAULT_SETTINGS.copy()
        )

        logger.info(f"Created tenant: {tenant.slug} (ID: {tenant.id})")

        # Create PostgreSQL schema
        self._create_schema(schema_name)

        # Create tenant settings
        merged_settings = {**self.DEFAULT_SETTINGS}
        if settings_override:
            merged_settings.update(settings_override)

        TenantSettings.objects.create(
            tenant=tenant,
            timezone=merged_settings['timezone'],
            language=merged_settings['language'],
            currency=merged_settings['currency'],
            date_format=merged_settings['date_format'],
            fiscal_year_start_month=merged_settings['fiscal_year_start_month'],
            modules_enabled=self.DEFAULT_MODULES.copy()
        )

        # Add owner as TenantUser
        TenantUser.objects.create(
            tenant=tenant,
            user=owner,
            role=TenantUser.TenantRole.OWNER,
            is_primary=True
        )

        # Clear cache
        self._clear_tenant_cache(tenant)

        return tenant

    def _create_schema(self, schema_name: str) -> None:
        """
        Create PostgreSQL schema for tenant.

        Args:
            schema_name: Name of schema to create

        Raises:
            TenantServiceError: If schema creation fails
        """
        try:
            with connection.cursor() as cursor:
                # Create schema
                cursor.execute(
                    f"CREATE SCHEMA IF NOT EXISTS {schema_name}"
                )
                logger.info(f"Created schema: {schema_name}")

                # Grant permissions
                cursor.execute(
                    f"GRANT ALL ON SCHEMA {schema_name} TO CURRENT_USER"
                )

        except Exception as e:
            logger.error(f"Failed to create schema {schema_name}: {e}")
            raise TenantServiceError(
                f"Failed to create database schema: {e}",
                code='SCHEMA_ERROR',
                message_ar='فشل في إنشاء مخطط قاعدة البيانات'
            )

    def _run_migrations_for_schema(self, schema_name: str) -> None:
        """
        Run Django migrations in tenant schema.

        Args:
            schema_name: Name of schema to migrate

        Note:
            This is a placeholder. In production, you might use
            django-tenants or similar library for migrations.
        """
        # This would typically use django-tenants or custom migration logic
        logger.info(f"Migrations for {schema_name} should be run separately")

    @transaction.atomic
    def update_tenant(
        self,
        tenant_id: str,
        **kwargs
    ) -> 'Tenant':
        """
        Update tenant information.

        Args:
            tenant_id: UUID of tenant to update
            **kwargs: Fields to update (name, name_ar, logo, custom_domain, etc.)

        Returns:
            Tenant: Updated tenant

        Raises:
            Tenant.DoesNotExist: If tenant not found
            TenantExistsError: If custom_domain already exists

        Example:
            >>> updated = service.update_tenant(
            ...     tenant_id='uuid-here',
            ...     name='New Name',
            ...     logo='https://...'
            ... )
        """
        from backend.src.models.tenant import Tenant

        tenant = Tenant.objects.get(id=tenant_id)

        # Check custom domain uniqueness if changing
        if 'custom_domain' in kwargs and kwargs['custom_domain']:
            existing = Tenant.objects.filter(
                custom_domain=kwargs['custom_domain']
            ).exclude(id=tenant_id).first()
            if existing:
                raise TenantExistsError('custom_domain', kwargs['custom_domain'])

        # Update allowed fields
        allowed_fields = ['name', 'name_ar', 'logo', 'custom_domain', 'settings', 'metadata']
        for field in allowed_fields:
            if field in kwargs:
                setattr(tenant, field, kwargs[field])

        tenant.save()

        # Clear cache
        self._clear_tenant_cache(tenant)

        logger.info(f"Updated tenant: {tenant.slug}")
        return tenant

    @transaction.atomic
    def deactivate_tenant(
        self,
        tenant_id: str,
        reason: str = ''
    ) -> 'Tenant':
        """
        Deactivate a tenant (soft delete).

        This sets is_active=False and status to CANCELLED.
        The schema and data are preserved.

        Args:
            tenant_id: UUID of tenant to deactivate
            reason: Reason for deactivation

        Returns:
            Tenant: Deactivated tenant

        Example:
            >>> tenant = service.deactivate_tenant(
            ...     tenant_id='uuid-here',
            ...     reason='Non-payment'
            ... )
        """
        from backend.src.models.tenant import Tenant

        tenant = Tenant.objects.get(id=tenant_id)
        tenant.is_active = False
        tenant.status = Tenant.TenantStatus.CANCELLED
        tenant.metadata['deactivation_reason'] = reason
        tenant.metadata['deactivated_at'] = datetime.now().isoformat()
        tenant.save()

        # Clear cache
        self._clear_tenant_cache(tenant)

        logger.info(f"Deactivated tenant: {tenant.slug}, reason: {reason}")
        return tenant

    def reactivate_tenant(
        self,
        tenant_id: str
    ) -> 'Tenant':
        """
        Reactivate a deactivated tenant.

        Args:
            tenant_id: UUID of tenant to reactivate

        Returns:
            Tenant: Reactivated tenant
        """
        from backend.src.models.tenant import Tenant

        tenant = Tenant.objects.get(id=tenant_id)
        tenant.is_active = True
        tenant.status = Tenant.TenantStatus.ACTIVE
        tenant.metadata['reactivated_at'] = datetime.now().isoformat()
        tenant.save()

        self._clear_tenant_cache(tenant)

        logger.info(f"Reactivated tenant: {tenant.slug}")
        return tenant

    def get_tenant_by_slug(self, slug: str) -> Optional['Tenant']:
        """
        Get tenant by slug with caching.

        Args:
            slug: Tenant slug

        Returns:
            Tenant or None

        Example:
            >>> tenant = service.get_tenant_by_slug('acme-corp')
        """
        from backend.src.models.tenant import Tenant

        cache_key = f"tenant:slug:{slug}"
        tenant = cache.get(cache_key)

        if tenant is None:
            try:
                tenant = Tenant.objects.select_related('plan').get(slug=slug)
                cache.set(cache_key, tenant, 300)
            except Tenant.DoesNotExist:
                return None

        return tenant

    def get_tenant_by_domain(self, domain: str) -> Optional['Tenant']:
        """
        Get tenant by custom domain.

        Args:
            domain: Custom domain

        Returns:
            Tenant or None
        """
        from backend.src.models.tenant import Tenant

        cache_key = f"tenant:domain:{domain}"
        tenant = cache.get(cache_key)

        if tenant is None:
            try:
                tenant = Tenant.objects.select_related('plan').get(
                    custom_domain=domain
                )
                cache.set(cache_key, tenant, 300)
            except Tenant.DoesNotExist:
                return None

        return tenant

    @transaction.atomic
    def add_user_to_tenant(
        self,
        tenant_id: str,
        user,
        role: str = 'member',
        is_primary: bool = False,
        permissions: Optional[Dict] = None
    ) -> 'TenantUser':
        """
        Add a user to a tenant.

        Args:
            tenant_id: UUID of tenant
            user: User to add
            role: Role to assign (owner, admin, manager, member, viewer)
            is_primary: Is this user's primary tenant
            permissions: Additional permissions dict

        Returns:
            TenantUser: Created membership

        Raises:
            TenantQuotaExceededError: If max_users exceeded

        Example:
            >>> membership = service.add_user_to_tenant(
            ...     tenant_id='uuid',
            ...     user=user,
            ...     role='admin'
            ... )
        """
        from backend.src.models.tenant import Tenant, TenantUser

        tenant = Tenant.objects.select_related('plan').get(id=tenant_id)

        # Check user quota
        if tenant.plan:
            current_users = TenantUser.objects.filter(
                tenant=tenant,
                is_active=True
            ).count()
            if current_users >= tenant.plan.max_users:
                raise TenantQuotaExceededError(
                    'users',
                    tenant.plan.max_users,
                    current_users
                )

        # Create or update membership
        tenant_user, created = TenantUser.objects.update_or_create(
            tenant=tenant,
            user=user,
            defaults={
                'role': role,
                'is_primary': is_primary,
                'permissions': permissions or {},
                'is_active': True
            }
        )

        logger.info(f"Added user {user} to tenant {tenant.slug} with role {role}")
        return tenant_user

    def remove_user_from_tenant(
        self,
        tenant_id: str,
        user_id: str
    ) -> bool:
        """
        Remove a user from a tenant.

        Args:
            tenant_id: UUID of tenant
            user_id: UUID of user

        Returns:
            bool: True if removed

        Raises:
            ValidationError: If trying to remove owner
        """
        from backend.src.models.tenant import TenantUser

        try:
            membership = TenantUser.objects.get(
                tenant_id=tenant_id,
                user_id=user_id
            )

            if membership.role == TenantUser.TenantRole.OWNER:
                raise ValidationError("Cannot remove tenant owner")

            membership.delete()
            logger.info(f"Removed user {user_id} from tenant {tenant_id}")
            return True

        except TenantUser.DoesNotExist:
            return False

    def get_tenant_users(
        self,
        tenant_id: str,
        include_inactive: bool = False
    ) -> List['TenantUser']:
        """
        Get all users in a tenant.

        Args:
            tenant_id: UUID of tenant
            include_inactive: Include inactive users

        Returns:
            List[TenantUser]: List of memberships
        """
        from backend.src.models.tenant import TenantUser

        queryset = TenantUser.objects.filter(
            tenant_id=tenant_id
        ).select_related('user')

        if not include_inactive:
            queryset = queryset.filter(is_active=True)

        return list(queryset.order_by('role', 'joined_at'))

    def get_user_tenants(
        self,
        user_id: str
    ) -> List['Tenant']:
        """
        Get all tenants a user belongs to.

        Args:
            user_id: UUID of user

        Returns:
            List[Tenant]: List of tenants
        """
        from backend.src.models.tenant import Tenant, TenantUser

        tenant_ids = TenantUser.objects.filter(
            user_id=user_id,
            is_active=True
        ).values_list('tenant_id', flat=True)

        return list(
            Tenant.objects.filter(
                id__in=tenant_ids,
                is_active=True
            ).select_related('plan').order_by('-created_at')
        )

    @transaction.atomic
    def change_tenant_plan(
        self,
        tenant_id: str,
        new_plan_code: str
    ) -> 'Tenant':
        """
        Change tenant's subscription plan.

        Args:
            tenant_id: UUID of tenant
            new_plan_code: Code of new plan

        Returns:
            Tenant: Updated tenant

        Raises:
            TenantPlan.DoesNotExist: If plan not found
        """
        from backend.src.models.tenant import Tenant, TenantPlan

        tenant = Tenant.objects.get(id=tenant_id)
        new_plan = TenantPlan.objects.get(code=new_plan_code, is_active=True)

        old_plan = tenant.plan
        tenant.plan = new_plan
        tenant.metadata['plan_history'] = tenant.metadata.get('plan_history', [])
        tenant.metadata['plan_history'].append({
            'from': old_plan.code if old_plan else None,
            'to': new_plan.code,
            'changed_at': datetime.now().isoformat()
        })
        tenant.save()

        self._clear_tenant_cache(tenant)

        logger.info(f"Changed plan for {tenant.slug}: {old_plan.code if old_plan else 'none'} -> {new_plan.code}")
        return tenant

    def check_quota(
        self,
        tenant: 'Tenant',
        quota_type: str,
        requested: int = 1
    ) -> Tuple[bool, int, int]:
        """
        Check if a quota limit allows the requested amount.

        Args:
            tenant: The tenant to check
            quota_type: Type of quota (users, storage, api_calls, modules)
            requested: Amount being requested

        Returns:
            Tuple[bool, int, int]: (allowed, limit, current)

        Example:
            >>> allowed, limit, current = service.check_quota(
            ...     tenant, 'users', 1
            ... )
        """
        from backend.src.models.tenant import TenantUser

        if not tenant.plan:
            # No plan = unlimited (or use defaults)
            return (True, 0, 0)

        if quota_type == 'users':
            limit = tenant.plan.max_users
            current = TenantUser.objects.filter(
                tenant=tenant,
                is_active=True
            ).count()

        elif quota_type == 'storage':
            limit = tenant.plan.max_storage_gb
            # TODO: Calculate actual storage usage
            current = 0

        elif quota_type == 'api_calls':
            limit = tenant.plan.max_api_calls_per_day
            # TODO: Track API calls
            current = 0

        elif quota_type == 'modules':
            limit = tenant.plan.max_modules
            try:
                tenant_settings = tenant.extended_settings
                current = len(tenant_settings.modules_enabled)
            except Exception:
                current = 0

        else:
            return (True, 0, 0)

        allowed = (current + requested) <= limit
        return (allowed, limit, current)

    def _clear_tenant_cache(self, tenant: 'Tenant') -> None:
        """
        Clear all cached data for a tenant.

        Args:
            tenant: The tenant to clear cache for
        """
        cache_keys = [
            f"tenant:id:{tenant.id}",
            f"tenant:slug:{tenant.slug}",
        ]
        if tenant.custom_domain:
            cache_keys.append(f"tenant:domain:{tenant.custom_domain}")

        cache.delete_many(cache_keys)
        logger.debug(f"Cleared cache for tenant: {tenant.slug}")


# Singleton instance
tenant_service = TenantService()
