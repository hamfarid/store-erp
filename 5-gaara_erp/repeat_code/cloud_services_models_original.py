import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
مديول تكامل الخدمات السحابية(Cloud Services Integration Module)
"""


class CloudProvider(models.Model):
    """نموذج لمقدمي الخدمات السحابية"""
    PROVIDER_TYPE_CHOICES = [
        ("aws", _("Amazon Web Services")),
        ("azure", _("Microsoft Azure")),
        ("gcp", _("Google Cloud Platform")),
        ("digitalocean", _("DigitalOcean")),
        ("dropbox", _("Dropbox")),
        ("googledrive", _("Google Drive")),
        ("onedrive", _("OneDrive")),
        ("icloud", _("iCloud")),
    ]
    class Meta:
        app_label = 'cloud_services'


    provider_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم المقدم"), max_length=255)
    provider_type = models.CharField(
        _("نوع المقدم"), max_length=20, choices=PROVIDER_TYPE_CHOICES)

    # إعدادات الاتصال
    api_endpoint = models.URLField(_("نقطة API"), blank=True)
    access_key = models.CharField(
        _("مفتاح الوصول"), max_length=500, blank=True)
    secret_key = models.CharField(
        _("المفتاح السري"), max_length=500, blank=True)
    region = models.CharField(_("المنطقة"), max_length=100, blank=True)

    # إعدادات التخزين
    bucket_name = models.CharField(
        _("اسم الحاوية"), max_length=255, blank=True)
    storage_quota = models.BigIntegerField(_("حصة التخزين (بايت)"), default=0)
    used_storage = models.BigIntegerField(
        _("التخزين المستخدم (بايت)"), default=0)

    # إحصائيات
    total_files = models.PositiveIntegerField(_("إجمالي الملفات"), default=0)
    total_uploads = models.PositiveIntegerField(_("إجمالي الرفع"), default=0)
    total_downloads = models.PositiveIntegerField(
        _("إجمالي التحميل"), default=0)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)
    is_default = models.BooleanField(_("افتراضي؟"), default=False)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

    class Meta:
        app_label = 'cloud_services'
        verbose_name = _("مقدم الخدمة السحابية")
        verbose_name_plural = _("مقدمو الخدمات السحابية")


class CloudFile(models.Model):
    """نموذج للملفات السحابية"""
    FILE_TYPE_CHOICES = [
        ("document", _("مستند")),
        ("image", _("صورة")),
        ("video", _("فيديو")),
        ("audio", _("صوت")),
        ("archive", _("أرشيف")),
        ("other", _("أخرى")),
    ]

    file_id = models.UUIDField(default=uuid.uuid4, unique=True)
    provider = models.ForeignKey(
        CloudProvider, on_delete=models.CASCADE, related_name="files")

    # معلومات الملف
    filename = models.CharField(_("اسم الملف"), max_length=255)
    file_path = models.CharField(_("مسار الملف"), max_length=1000)
    file_type = models.CharField(
        _("نوع الملف"), max_length=15, choices=FILE_TYPE_CHOICES)
    file_size = models.BigIntegerField(_("حجم الملف (بايت)"))
    mime_type = models.CharField(_("نوع MIME"), max_length=100, blank=True)

    # معلومات الوصول
    public_url = models.URLField(_("الرابط العام"), blank=True)
    download_url = models.URLField(_("رابط التحميل"), blank=True)
    is_public = models.BooleanField(_("عام؟"), default=False)

    # معلومات التحميل
    upload_progress = models.PositiveIntegerField(_("تقدم الرفع"), default=100)
    checksum = models.CharField(
        _("المجموع الاختباري"), max_length=64, blank=True)

    # إحصائيات
    download_count = models.PositiveIntegerField(_("عدد التحميلات"), default=0)
    last_accessed = models.DateTimeField(_("آخر وصول"), null=True, blank=True)

    # معلومات المالك
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cloud_files"
    )

    # الطوابع الزمنية
    uploaded_at = models.DateTimeField(_("تاريخ الرفع"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.filename} ({self.provider.name})"

    class Meta:
        app_label = 'cloud_services'
        verbose_name = _("الملف السحابي")
        verbose_name_plural = _("الملفات السحابية")


class CloudBackup(models.Model):
    """نموذج للنسخ الاحتياطية السحابية"""
    BACKUP_TYPE_CHOICES = [
        ("full", _("كامل")),
        ("incremental", _("تدريجي")),
        ("differential", _("تفاضلي")),
    ]

    class Meta:
        app_label = "cloud_services"

    STATUS_CHOICES = [
        ("pending", _("معلق")),
        ("running", _("قيد التشغيل")),
        ("completed", _("مكتمل")),
        ("failed", _("فشل")),
    ]

    backup_id = models.UUIDField(default=uuid.uuid4, unique=True)
    provider = models.ForeignKey(
        CloudProvider, on_delete=models.CASCADE, related_name="backups")

    # معلومات النسخة الاحتياطية
    name = models.CharField(_("اسم النسخة الاحتياطية"), max_length=255)
    backup_type = models.CharField(
        _("نوع النسخة"), max_length=15, choices=BACKUP_TYPE_CHOICES)
    status = models.CharField(
        _("الحالة"), max_length=15, choices=STATUS_CHOICES, default="pending")

    # معلومات البيانات
    source_path = models.CharField(_("مسار المصدر"), max_length=1000)
    backup_path = models.CharField(
        _("مسار النسخة الاحتياطية"), max_length=1000, blank=True)
    backup_size = models.BigIntegerField(_("حجم النسخة الاحتياطية"), default=0)

    # التوقيت
    started_at = models.DateTimeField(_("وقت البدء"), null=True, blank=True)
    completed_at = models.DateTimeField(
        _("وقت الانتهاء"), null=True, blank=True)

    # معلومات الخطأ
    error_message = models.TextField(_("رسالة الخطأ"), blank=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)

    def __str__(self):
        return f"نسخة احتياطية {self.name}"

    class Meta:
        app_label = 'cloud_services'
        verbose_name = _("النسخة الاحتياطية السحابية")
        verbose_name_plural = _("النسخ الاحتياطية السحابية")
