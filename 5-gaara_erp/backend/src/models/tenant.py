"""
Tenant Models for Multi-Tenancy Support
نماذج المستأجر لدعم تعدد المستأجرين

This module implements schema-based multi-tenancy for Gaara ERP.
Each tenant has isolated data in a separate PostgreSQL schema.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from django.db import models, connection
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


# Slug validator: alphanumeric and hyphens only
slug_validator = RegexValidator(
    regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
    message=_('يجب أن يحتوي المعرف على أحرف صغيرة وأرقام وشرطات فقط')
)


class TenantPlan(models.Model):
    """
    Subscription plan for tenants.
    خطة الاشتراك للمستأجرين.

    Defines quotas, features, and pricing for each subscription tier.

    Attributes:
        name (str): Plan name (e.g., 'Basic', 'Professional', 'Enterprise')
        name_ar (str): Arabic plan name
        code (str): Unique plan code
        max_users (int): Maximum number of users allowed
        max_storage_gb (int): Maximum storage in gigabytes
        max_api_calls_per_day (int): Daily API call limit
        features (dict): JSON of enabled features
        price_monthly (Decimal): Monthly subscription price
        price_yearly (Decimal): Yearly subscription price
        is_active (bool): Whether plan is available for new subscriptions
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp

    Example:
        >>> plan = TenantPlan.objects.create(
        ...     name='Professional',
        ...     code='pro',
        ...     max_users=50,
        ...     max_storage_gb=100
        ... )
    """

    class PlanType(models.TextChoices):
        """نوع الخطة"""
        FREE = 'free', _('مجاني')
        BASIC = 'basic', _('أساسي')
        PROFESSIONAL = 'pro', _('احترافي')
        ENTERPRISE = 'enterprise', _('مؤسسي')
        CUSTOM = 'custom', _('مخصص')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('المعرف')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('اسم الخطة')
    )
    name_ar = models.CharField(
        max_length=100,
        verbose_name=_('اسم الخطة بالعربية'),
        blank=True
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        validators=[slug_validator],
        verbose_name=_('رمز الخطة')
    )
    plan_type = models.CharField(
        max_length=20,
        choices=PlanType.choices,
        default=PlanType.BASIC,
        verbose_name=_('نوع الخطة')
    )
    max_users = models.PositiveIntegerField(
        default=5,
        verbose_name=_('الحد الأقصى للمستخدمين')
    )
    max_storage_gb = models.PositiveIntegerField(
        default=10,
        verbose_name=_('الحد الأقصى للتخزين (جيجابايت)')
    )
    max_api_calls_per_day = models.PositiveIntegerField(
        default=10000,
        verbose_name=_('الحد الأقصى لاستدعاءات API يومياً')
    )
    max_modules = models.PositiveIntegerField(
        default=10,
        verbose_name=_('الحد الأقصى للوحدات')
    )
    features = models.JSONField(
        default=dict,
        verbose_name=_('الميزات المتاحة'),
        help_text=_('قائمة الميزات المفعلة لهذه الخطة')
    )
    price_monthly = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('السعر الشهري')
    )
    price_yearly = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('السعر السنوي')
    )
    currency = models.CharField(
        max_length=3,
        default='SAR',
        verbose_name=_('العملة')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    class Meta:
        db_table = 'tenant_plans'
        verbose_name = _('خطة الاشتراك')
        verbose_name_plural = _('خطط الاشتراك')
        ordering = ['price_monthly']

    def __str__(self) -> str:
        """Return plan name with type."""
        return f"{self.name} ({self.get_plan_type_display()})"

    def get_feature(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled for this plan.

        Args:
            feature_name: The name of the feature to check

        Returns:
            bool: True if feature is enabled, False otherwise
        """
        return self.features.get(feature_name, False)


class Tenant(models.Model):
    """
    Main tenant model representing an organization/company.
    نموذج المستأجر الرئيسي يمثل منظمة/شركة.

    Each tenant has:
    - A unique slug for URL identification
    - A dedicated PostgreSQL schema for data isolation
    - Optional custom domain support
    - Subscription plan with quotas

    Attributes:
        id (UUID): Primary key
        name (str): Organization name
        name_ar (str): Arabic organization name
        slug (str): URL-safe unique identifier
        schema_name (str): PostgreSQL schema name
        custom_domain (str): Optional custom domain
        logo (str): URL to organization logo
        plan (TenantPlan): Subscription plan
        owner (User): Primary account owner
        is_active (bool): Whether tenant is active
        subscription_ends_at (datetime): Subscription expiry date
        settings (dict): Tenant-specific settings
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp

    Example:
        >>> tenant = Tenant.objects.create(
        ...     name='Acme Corp',
        ...     slug='acme-corp',
        ...     owner=user
        ... )
    """

    class TenantStatus(models.TextChoices):
        """حالة المستأجر"""
        ACTIVE = 'active', _('نشط')
        SUSPENDED = 'suspended', _('معلق')
        TRIAL = 'trial', _('تجريبي')
        EXPIRED = 'expired', _('منتهي')
        CANCELLED = 'cancelled', _('ملغي')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('المعرف')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('اسم المؤسسة')
    )
    name_ar = models.CharField(
        max_length=255,
        verbose_name=_('اسم المؤسسة بالعربية'),
        blank=True
    )
    slug = models.SlugField(
        max_length=63,
        unique=True,
        validators=[slug_validator, MinLengthValidator(3)],
        verbose_name=_('المعرف الفريد'),
        help_text=_('يستخدم في الرابط: your-slug.gaara-erp.com')
    )
    schema_name = models.CharField(
        max_length=63,
        unique=True,
        verbose_name=_('اسم المخطط'),
        help_text=_('اسم schema في PostgreSQL')
    )
    custom_domain = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('النطاق المخصص'),
        help_text=_('نطاق مخصص مثل: erp.your-company.com')
    )
    logo = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('الشعار')
    )
    plan = models.ForeignKey(
        TenantPlan,
        on_delete=models.PROTECT,
        related_name='tenants',
        null=True,
        blank=True,
        verbose_name=_('خطة الاشتراك')
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_tenants',
        verbose_name=_('المالك')
    )
    status = models.CharField(
        max_length=20,
        choices=TenantStatus.choices,
        default=TenantStatus.TRIAL,
        verbose_name=_('الحالة')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )
    trial_ends_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('انتهاء الفترة التجريبية')
    )
    subscription_ends_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('انتهاء الاشتراك')
    )
    settings = models.JSONField(
        default=dict,
        verbose_name=_('الإعدادات'),
        help_text=_('إعدادات خاصة بالمستأجر')
    )
    metadata = models.JSONField(
        default=dict,
        verbose_name=_('البيانات الوصفية')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    class Meta:
        db_table = 'tenants'
        verbose_name = _('المستأجر')
        verbose_name_plural = _('المستأجرون')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['custom_domain']),
            models.Index(fields=['schema_name']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self) -> str:
        """Return tenant name with slug."""
        return f"{self.name} ({self.slug})"

    def save(self, *args, **kwargs) -> None:
        """
        Save tenant and auto-generate schema_name if not set.

        The schema name is derived from the slug with 'tenant_' prefix.
        """
        if not self.schema_name:
            # Convert slug to valid schema name
            self.schema_name = f"tenant_{self.slug.replace('-', '_')}"
        super().save(*args, **kwargs)

    @property
    def is_trial(self) -> bool:
        """Check if tenant is in trial period."""
        return self.status == self.TenantStatus.TRIAL

    @property
    def is_subscription_active(self) -> bool:
        """
        Check if subscription is currently active.

        Returns:
            bool: True if subscription hasn't expired
        """
        if self.status == self.TenantStatus.TRIAL:
            return self.trial_ends_at is None or self.trial_ends_at > datetime.now()
        if self.subscription_ends_at is None:
            return False
        return self.subscription_ends_at > datetime.now()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a tenant-specific setting.

        Args:
            key: Setting key to retrieve
            default: Default value if key not found

        Returns:
            The setting value or default
        """
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """
        Set a tenant-specific setting.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        self.save(update_fields=['settings', 'updated_at'])

    def activate_schema(self) -> None:
        """
        Switch database connection to this tenant's schema.

        This sets the PostgreSQL search_path to the tenant's schema.
        """
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.schema_name}, public")

    def create_schema(self) -> bool:
        """
        Create the PostgreSQL schema for this tenant.

        Returns:
            bool: True if schema was created successfully

        Raises:
            Exception: If schema creation fails
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"
                )
            return True
        except Exception as e:
            raise Exception(f"فشل إنشاء المخطط: {e}")


class TenantUser(models.Model):
    """
    Mapping between users and tenants with roles.
    ربط المستخدمين بالمستأجرين مع الأدوار.

    A user can belong to multiple tenants with different roles.

    Attributes:
        id (UUID): Primary key
        tenant (Tenant): The tenant
        user (User): The user
        role (str): User's role in this tenant
        is_primary (bool): Is this user's primary tenant
        permissions (dict): Additional permissions
        joined_at (datetime): When user joined tenant
        last_accessed_at (datetime): Last access timestamp

    Example:
        >>> tenant_user = TenantUser.objects.create(
        ...     tenant=tenant,
        ...     user=user,
        ...     role='admin'
        ... )
    """

    class TenantRole(models.TextChoices):
        """أدوار المستخدم في المستأجر"""
        OWNER = 'owner', _('مالك')
        ADMIN = 'admin', _('مدير')
        MANAGER = 'manager', _('مشرف')
        MEMBER = 'member', _('عضو')
        VIEWER = 'viewer', _('مشاهد')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('المعرف')
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='tenant_users',
        verbose_name=_('المستأجر')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_memberships',
        verbose_name=_('المستخدم')
    )
    role = models.CharField(
        max_length=20,
        choices=TenantRole.choices,
        default=TenantRole.MEMBER,
        verbose_name=_('الدور')
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_('المستأجر الأساسي'),
        help_text=_('هل هذا هو المستأجر الأساسي للمستخدم؟')
    )
    permissions = models.JSONField(
        default=dict,
        verbose_name=_('الصلاحيات'),
        help_text=_('صلاحيات إضافية للمستخدم')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الانضمام')
    )
    last_accessed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('آخر وصول')
    )

    class Meta:
        db_table = 'tenant_users'
        verbose_name = _('مستخدم المستأجر')
        verbose_name_plural = _('مستخدمو المستأجر')
        unique_together = ['tenant', 'user']
        ordering = ['-joined_at']
        indexes = [
            models.Index(fields=['tenant', 'user']),
            models.Index(fields=['user', 'is_primary']),
        ]

    def __str__(self) -> str:
        """Return user email with tenant and role."""
        return f"{self.user} @ {self.tenant.slug} ({self.get_role_display()})"

    def has_permission(self, permission: str) -> bool:
        """
        Check if user has a specific permission.

        Args:
            permission: Permission name to check

        Returns:
            bool: True if user has the permission
        """
        # Owner and admin have all permissions
        if self.role in [self.TenantRole.OWNER, self.TenantRole.ADMIN]:
            return True
        return self.permissions.get(permission, False)

    def update_last_access(self) -> None:
        """Update the last_accessed_at timestamp."""
        from django.utils import timezone
        self.last_accessed_at = timezone.now()
        self.save(update_fields=['last_accessed_at'])


class TenantSettings(models.Model):
    """
    Extended settings for a tenant.
    إعدادات موسعة للمستأجر.

    Stores configuration like timezone, language, currency preferences.

    Attributes:
        tenant (Tenant): One-to-one relation with Tenant
        timezone (str): Tenant's timezone
        language (str): Primary language
        date_format (str): Preferred date format
        currency (str): Primary currency
        fiscal_year_start (int): Month fiscal year starts
        modules_enabled (list): List of enabled module codes

    Example:
        >>> settings = TenantSettings.objects.create(
        ...     tenant=tenant,
        ...     timezone='Asia/Riyadh',
        ...     language='ar'
        ... )
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('المعرف')
    )
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name='extended_settings',
        verbose_name=_('المستأجر')
    )
    timezone = models.CharField(
        max_length=50,
        default='Asia/Riyadh',
        verbose_name=_('المنطقة الزمنية')
    )
    language = models.CharField(
        max_length=10,
        default='ar',
        verbose_name=_('اللغة الأساسية')
    )
    secondary_language = models.CharField(
        max_length=10,
        default='en',
        blank=True,
        verbose_name=_('اللغة الثانوية')
    )
    date_format = models.CharField(
        max_length=20,
        default='YYYY-MM-DD',
        verbose_name=_('صيغة التاريخ')
    )
    time_format = models.CharField(
        max_length=10,
        default='24h',
        choices=[('12h', '12 ساعة'), ('24h', '24 ساعة')],
        verbose_name=_('صيغة الوقت')
    )
    currency = models.CharField(
        max_length=3,
        default='SAR',
        verbose_name=_('العملة الأساسية')
    )
    currency_symbol = models.CharField(
        max_length=5,
        default='ر.س',
        verbose_name=_('رمز العملة')
    )
    fiscal_year_start_month = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('شهر بداية السنة المالية')
    )
    modules_enabled = models.JSONField(
        default=list,
        verbose_name=_('الوحدات المفعلة'),
        help_text=_('قائمة أكواد الوحدات المفعلة')
    )
    theme_settings = models.JSONField(
        default=dict,
        verbose_name=_('إعدادات المظهر')
    )
    notification_settings = models.JSONField(
        default=dict,
        verbose_name=_('إعدادات الإشعارات')
    )
    security_settings = models.JSONField(
        default=dict,
        verbose_name=_('إعدادات الأمان'),
        help_text=_('إعدادات مثل MFA الإلزامي، انتهاء الجلسة')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )

    class Meta:
        db_table = 'tenant_settings'
        verbose_name = _('إعدادات المستأجر')
        verbose_name_plural = _('إعدادات المستأجرين')

    def __str__(self) -> str:
        """Return tenant name with settings."""
        return f"Settings for {self.tenant.name}"

    def is_module_enabled(self, module_code: str) -> bool:
        """
        Check if a module is enabled for this tenant.

        Args:
            module_code: The module code to check

        Returns:
            bool: True if module is enabled
        """
        return module_code in self.modules_enabled

    def enable_module(self, module_code: str) -> None:
        """
        Enable a module for this tenant.

        Args:
            module_code: The module code to enable
        """
        if module_code not in self.modules_enabled:
            self.modules_enabled.append(module_code)
            self.save(update_fields=['modules_enabled', 'updated_at'])

    def disable_module(self, module_code: str) -> None:
        """
        Disable a module for this tenant.

        Args:
            module_code: The module code to disable
        """
        if module_code in self.modules_enabled:
            self.modules_enabled.remove(module_code)
            self.save(update_fields=['modules_enabled', 'updated_at'])


class TenantInvitation(models.Model):
    """
    Invitation to join a tenant.
    دعوة للانضمام إلى مستأجر.

    Allows tenant admins to invite users via email.

    Attributes:
        tenant (Tenant): The tenant inviting
        email (str): Email of invitee
        role (str): Role to assign on join
        token (str): Unique invitation token
        expires_at (datetime): Invitation expiry
        accepted_at (datetime): When invitation was accepted

    Example:
        >>> invitation = TenantInvitation.create_invitation(
        ...     tenant=tenant,
        ...     email='user@example.com',
        ...     role='member'
        ... )
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('المعرف')
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='invitations',
        verbose_name=_('المستأجر')
    )
    email = models.EmailField(
        verbose_name=_('البريد الإلكتروني')
    )
    role = models.CharField(
        max_length=20,
        choices=TenantUser.TenantRole.choices,
        default=TenantUser.TenantRole.MEMBER,
        verbose_name=_('الدور')
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('رمز الدعوة')
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_invitations',
        verbose_name=_('الداعي')
    )
    message = models.TextField(
        blank=True,
        verbose_name=_('رسالة الدعوة')
    )
    expires_at = models.DateTimeField(
        verbose_name=_('تنتهي في')
    )
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('تم القبول في')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )

    class Meta:
        db_table = 'tenant_invitations'
        verbose_name = _('دعوة المستأجر')
        verbose_name_plural = _('دعوات المستأجر')
        unique_together = ['tenant', 'email']
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Return invitation email with tenant."""
        return f"Invitation to {self.email} for {self.tenant.slug}"

    @property
    def is_expired(self) -> bool:
        """Check if invitation has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at

    @property
    def is_accepted(self) -> bool:
        """Check if invitation was accepted."""
        return self.accepted_at is not None

    @classmethod
    def create_invitation(
        cls,
        tenant: Tenant,
        email: str,
        role: str,
        invited_by,
        message: str = '',
        days_valid: int = 7
    ) -> 'TenantInvitation':
        """
        Create a new invitation with auto-generated token.

        Args:
            tenant: The tenant to invite to
            email: Email address to invite
            role: Role to assign
            invited_by: User sending the invitation
            message: Optional invitation message
            days_valid: Number of days invitation is valid

        Returns:
            TenantInvitation: The created invitation
        """
        import secrets
        from django.utils import timezone

        token = secrets.token_urlsafe(48)
        expires_at = timezone.now() + timedelta(days=days_valid)

        return cls.objects.create(
            tenant=tenant,
            email=email,
            role=role,
            token=token,
            invited_by=invited_by,
            message=message,
            expires_at=expires_at
        )

    def accept(self, user) -> TenantUser:
        """
        Accept the invitation and create TenantUser.

        Args:
            user: The user accepting the invitation

        Returns:
            TenantUser: The created tenant user record

        Raises:
            ValueError: If invitation is expired or already accepted
        """
        from django.utils import timezone

        if self.is_expired:
            raise ValueError(_('انتهت صلاحية الدعوة'))
        if self.is_accepted:
            raise ValueError(_('تم قبول الدعوة مسبقاً'))

        # Create TenantUser
        tenant_user = TenantUser.objects.create(
            tenant=self.tenant,
            user=user,
            role=self.role
        )

        # Mark as accepted
        self.accepted_at = timezone.now()
        self.save(update_fields=['accepted_at'])

        return tenant_user
