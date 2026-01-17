import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
مديول تكامل أنظمة ERP الخارجية(External ERP Integration Module)
"""


class ExternalERPSystem(models.Model):
    """نموذج لأنظمة ERP الخارجية"""
    SYSTEM_TYPE_CHOICES = [
        ("sap", _("SAP")),
        ("oracle", _("Oracle ERP")),
        ("microsoft", _("Microsoft Dynamics")),
        ("netsuite", _("NetSuite")),
        ("odoo", _("Odoo")),
        ("sage", _("Sage")),
        ("epicor", _("Epicor")),
        ("infor", _("Infor")),
        ("custom", _("مخصص")),
    ]
    class Meta:
        app_label = 'external_erp'


    system_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم النظام"), max_length=255)
    system_type = models.CharField(
        _("نوع النظام"), max_length=20, choices=SYSTEM_TYPE_CHOICES)

    # معلومات الاتصال
    base_url = models.URLField(_("الرابط الأساسي"))
    api_endpoint = models.URLField(_("نقطة API"), blank=True)
    api_version = models.CharField(_("إصدار API"), max_length=20, blank=True)

    # إعدادات الأمان
    username = models.CharField(_("اسم المستخدم"), max_length=255, blank=True)
    password = models.CharField(_("كلمة المرور"), max_length=255, blank=True)
    api_key = models.CharField(_("مفتاح API"), max_length=500, blank=True)
    client_id = models.CharField(_("معرف العميل"), max_length=255, blank=True)
    client_secret = models.CharField(
        _("سر العميل"), max_length=500, blank=True)

    # إعدادات المزامنة
    sync_customers = models.BooleanField(_("مزامنة العملاء"), default=True)
    sync_suppliers = models.BooleanField(_("مزامنة الموردين"), default=True)
    sync_products = models.BooleanField(_("مزامنة المنتجات"), default=True)
    sync_orders = models.BooleanField(_("مزامنة الطلبات"), default=True)
    sync_invoices = models.BooleanField(_("مزامنة الفواتير"), default=True)
    sync_inventory = models.BooleanField(_("مزامنة المخزون"), default=True)

    # تكرار المزامنة
    sync_frequency = models.PositiveIntegerField(
        _("تكرار المزامنة (دقائق)"), default=60)
    last_sync = models.DateTimeField(_("آخر مزامنة"), null=True, blank=True)

    # إحصائيات
    total_syncs = models.PositiveIntegerField(_("إجمالي المزامنات"), default=0)
    successful_syncs = models.PositiveIntegerField(
        _("المزامنات الناجحة"), default=0)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_system_type_display()})"

    class Meta:
        app_label = 'external_erp'
        verbose_name = _("نظام ERP خارجي")
        verbose_name_plural = _("أنظمة ERP خارجية")


class ERPSyncLog(models.Model):
    """نموذج لسجلات مزامنة ERP"""
    SYNC_TYPE_CHOICES = [
        ("import", _("استيراد")),
        ("export", _("تصدير")),
        ("bidirectional", _("ثنائي الاتجاه")),
    ]

    class Meta:
        app_label = "external_erp"

    STATUS_CHOICES = [
        ("pending", _("معلق")),
        ("running", _("قيد التشغيل")),
        ("completed", _("مكتمل")),
        ("failed", _("فشل")),
        ("partial", _("جزئي")),
    ]

    log_id = models.UUIDField(default=uuid.uuid4, unique=True)
    erp_system = models.ForeignKey(
        ExternalERPSystem, on_delete=models.CASCADE, related_name="sync_logs")

    # معلومات المزامنة
    sync_type = models.CharField(
        _("نوع المزامنة"), max_length=15, choices=SYNC_TYPE_CHOICES)
    data_type = models.CharField(_("نوع البيانات"), max_length=50)
    status = models.CharField(
        _("الحالة"), max_length=15, choices=STATUS_CHOICES, default="pending")

    # إحصائيات
    records_processed = models.PositiveIntegerField(
        _("السجلات المعالجة"), default=0)
    records_successful = models.PositiveIntegerField(
        _("السجلات الناجحة"), default=0)
    records_failed = models.PositiveIntegerField(
        _("السجلات الفاشلة"), default=0)

    # التوقيت
    started_at = models.DateTimeField(_("وقت البدء"), null=True, blank=True)
    completed_at = models.DateTimeField(
        _("وقت الانتهاء"), null=True, blank=True)

    # معلومات الخطأ
    error_message = models.TextField(_("رسالة الخطأ"), blank=True)
    error_details = models.JSONField(
        _("تفاصيل الخطأ"), default=dict, blank=True)

    # البيانات
    sync_data = models.JSONField(
        _("بيانات المزامنة"), default=dict, blank=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)

    def __str__(self):
        return f"مزامنة {self.data_type} - {self.erp_system.name}"

    class Meta:
        app_label = 'external_erp'
        verbose_name = _("سجل مزامنة ERP")
        verbose_name_plural = _("سجلات مزامنة ERP")


"""
مديول تكامل أنظمة CRM الخارجية(External CRM Integration Module)
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
        app_label = "external_erp"

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
