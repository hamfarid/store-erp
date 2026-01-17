import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
مديول تكامل أنظمة CRM الخارجية (External CRM Integration Module)
"""


class ExternalCRMSystem(models.Model):
    """نموذج لأنظمة CRM الخارجية"""
    SYSTEM_TYPE_CHOICES = [
        ("salesforce", _("Salesforce")),
        ("hubspot", _("HubSpot")),
        ("pipedrive", _("Pipedrive")),
        ("zoho", _("Zoho CRM")),
        ("freshsales", _("Freshsales")),
        ("monday", _("Monday.com")),
        ("custom", _("مخصص")),
    ]
    class Meta:
        app_label = 'external_crm'


    system_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم النظام"), max_length=255)
    system_type = models.CharField(
        _("نوع النظام"), max_length=20, choices=SYSTEM_TYPE_CHOICES)

    # معلومات الاتصال
    base_url = models.URLField(_("الرابط الأساسي"))
    api_endpoint = models.URLField(_("نقطة API"), blank=True)

    # إعدادات الأمان
    api_key = models.CharField(_("مفتاح API"), max_length=500, blank=True)
    access_token = models.TextField(_("رمز الوصول"), blank=True)
    refresh_token = models.TextField(_("رمز التحديث"), blank=True)

    # إعدادات المزامنة
    sync_contacts = models.BooleanField(_("مزامنة جهات الاتصال"), default=True)
    sync_leads = models.BooleanField(
        _("مزامنة العملاء المحتملين"), default=True)
    sync_opportunities = models.BooleanField(_("مزامنة الفرص"), default=True)
    sync_activities = models.BooleanField(_("مزامنة الأنشطة"), default=True)

    # إحصائيات
    total_contacts = models.PositiveIntegerField(
        _("إجمالي جهات الاتصال"), default=0)
    total_leads = models.PositiveIntegerField(
        _("إجمالي العملاء المحتملين"), default=0)
    last_sync = models.DateTimeField(_("آخر مزامنة"), null=True, blank=True)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_system_type_display()})"

    class Meta:
        app_label = 'external_crm'
        verbose_name = _("نظام CRM خارجي")
        verbose_name_plural = _("أنظمة CRM خارجية")


"""
مديول تكامل خدمات الخرائط والموقع (Maps & Location Integration Module)
"""


class LocationService(models.Model):
    """نموذج لخدمات الموقع"""
    SERVICE_TYPE_CHOICES = [
        ("google_maps", _("خرائط جوجل")),
        ("mapbox", _("Mapbox")),
        ("openstreetmap", _("OpenStreetMap")),
        ("here", _("HERE Maps")),
        ("bing", _("Bing Maps")),
    ]

    class Meta:
        app_label = 'external_crm'

    service_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم الخدمة"), max_length=255)
    service_type = models.CharField(
        _("نوع الخدمة"), max_length=20, choices=SERVICE_TYPE_CHOICES)

    # إعدادات API
    api_key = models.CharField(_("مفتاح API"), max_length=500)
    api_endpoint = models.URLField(_("نقطة API"), blank=True)

    # الحدود والاستخدام
    daily_quota = models.PositiveIntegerField(_("الحصة اليومية"), default=1000)
    used_today = models.PositiveIntegerField(_("المستخدم اليوم"), default=0)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)
    is_default = models.BooleanField(_("افتراضي؟"), default=False)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"

    class Meta:
        app_label = 'maps_location'
        verbose_name = _("خدمة الموقع")
        verbose_name_plural = _("خدمات الموقع")


"""
مديول تكامل خدمات الترجمة (Translation Services Integration Module)
"""


class TranslationService(models.Model):
    """نموذج لخدمات الترجمة"""
    SERVICE_TYPE_CHOICES = [
        ("google_translate", _("ترجمة جوجل")),
        ("microsoft_translator", _("مترجم مايكروسوفت")),
        ("aws_translate", _("ترجمة أمازون")),
        ("deepl", _("DeepL")),
        ("yandex", _("Yandex Translate")),
    ]

    class Meta:
        app_label = 'external_crm'

    service_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم الخدمة"), max_length=255)
    service_type = models.CharField(
        _("نوع الخدمة"), max_length=25, choices=SERVICE_TYPE_CHOICES)

    # إعدادات API
    api_key = models.CharField(_("مفتاح API"), max_length=500)
    api_endpoint = models.URLField(_("نقطة API"), blank=True)

    # اللغات المدعومة
    supported_languages = models.JSONField(_("اللغات المدعومة"), default=list)

    # إحصائيات
    characters_translated = models.BigIntegerField(
        _("الأحرف المترجمة"), default=0)
    translation_requests = models.PositiveIntegerField(
        _("طلبات الترجمة"), default=0)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"

    class Meta:
        app_label = 'translation'
        verbose_name = _("خدمة الترجمة")
        verbose_name_plural = _("خدمات الترجمة")


"""
مديول تكامل خدمات التحليلات (Analytics Services Integration Module)
"""


class AnalyticsService(models.Model):
    """نموذج لخدمات التحليلات"""
    SERVICE_TYPE_CHOICES = [
        ("google_analytics", _("Google Analytics")),
        ("adobe_analytics", _("Adobe Analytics")),
        ("mixpanel", _("Mixpanel")),
        ("hotjar", _("Hotjar")),
        ("segment", _("Segment")),
    ]

    class Meta:
        app_label = 'external_crm'

    service_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم الخدمة"), max_length=255)
    service_type = models.CharField(
        _("نوع الخدمة"), max_length=20, choices=SERVICE_TYPE_CHOICES)

    # إعدادات الاتصال
    tracking_id = models.CharField(_("معرف التتبع"), max_length=255)
    api_key = models.CharField(_("مفتاح API"), max_length=500, blank=True)

    # إعدادات التتبع
    track_pageviews = models.BooleanField(
        _("تتبع مشاهدات الصفحة"), default=True)
    track_events = models.BooleanField(_("تتبع الأحداث"), default=True)
    track_conversions = models.BooleanField(_("تتبع التحويلات"), default=True)

    # إحصائيات
    total_events = models.PositiveIntegerField(_("إجمالي الأحداث"), default=0)
    total_pageviews = models.PositiveIntegerField(
        _("إجمالي مشاهدات الصفحة"), default=0)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"

    class Meta:
        app_label = 'analytics'
        verbose_name = _("خدمة التحليلات")
        verbose_name_plural = _("خدمات التحليلات")


"""
مديول تكامل APIs الخارجية (External APIs Integration Module)
"""


class ExternalAPI(models.Model):
    """نموذج لـ APIs الخارجية"""

    class Meta:
        app_label = 'external_crm'
    API_TYPE_CHOICES = [
        ("rest", _("REST API")),
        ("graphql", _("GraphQL")),
        ("soap", _("SOAP")),
        ("webhook", _("Webhook")),
        ("rpc", _("RPC")),
    ]

    AUTH_TYPE_CHOICES = [
        ("none", _("بدون")),
        ("api_key", _("مفتاح API")),
        ("bearer", _("Bearer Token")),
        ("basic", _("Basic Auth")),
        ("oauth", _("OAuth")),
    ]

    api_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم API"), max_length=255)
    description = models.TextField(_("الوصف"), blank=True)
    api_type = models.CharField(
        _("نوع API"), max_length=15, choices=API_TYPE_CHOICES)

    # معلومات الاتصال
    base_url = models.URLField(_("الرابط الأساسي"))
    version = models.CharField(_("الإصدار"), max_length=20, blank=True)

    # إعدادات الأمان
    auth_type = models.CharField(
        _("نوع المصادقة"), max_length=15, choices=AUTH_TYPE_CHOICES, default="none")
    api_key = models.CharField(_("مفتاح API"), max_length=500, blank=True)
    username = models.CharField(_("اسم المستخدم"), max_length=255, blank=True)
    password = models.CharField(_("كلمة المرور"), max_length=255, blank=True)

    # إعدادات الطلبات
    timeout = models.PositiveIntegerField(
        _("مهلة الانتظار (ثانية)"), default=30)
    retry_attempts = models.PositiveIntegerField(
        _("محاولات الإعادة"), default=3)
    rate_limit = models.PositiveIntegerField(
        _("حد المعدل (طلبات/دقيقة)"), default=60)

    # إحصائيات
    total_requests = models.PositiveIntegerField(
        _("إجمالي الطلبات"), default=0)
    successful_requests = models.PositiveIntegerField(
        _("الطلبات الناجحة"), default=0)
    failed_requests = models.PositiveIntegerField(
        _("الطلبات الفاشلة"), default=0)
    average_response_time = models.FloatField(
        _("متوسط وقت الاستجابة"), default=0.0)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_api_type_display()})"

    class Meta:
        app_label = "external_apis"
        verbose_name = _("API خارجي")
        verbose_name_plural = _("APIs خارجية")
