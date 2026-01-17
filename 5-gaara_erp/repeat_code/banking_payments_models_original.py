import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

"""
مديول تكامل البنوك والمدفوعات(Banking & Payments Integration Module)
"""


class BankProvider(models.Model):
    """نموذج لمقدمي الخدمات المصرفية"""
    PROVIDER_TYPE_CHOICES = [
        ("bank", _("بنك")),
        ("payment_gateway", _("بوابة دفع")),
        ("digital_wallet", _("محفظة رقمية")),
        ("crypto", _("عملة مشفرة")),
        ("fintech", _("تكنولوجيا مالية")),
    ]
    class Meta:
        app_label = 'banking_payments'


    STATUS_CHOICES = [
        ("active", _("نشط")),
        ("inactive", _("غير نشط")),
        ("testing", _("قيد الاختبار")),
        ("maintenance", _("صيانة")),
    ]

    provider_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم المقدم"), max_length=255)
    provider_type = models.CharField(
        _("نوع المقدم"), max_length=20, choices=PROVIDER_TYPE_CHOICES)
    status = models.CharField(
        _("الحالة"), max_length=15, choices=STATUS_CHOICES, default="active")

    # معلومات الاتصال
    api_endpoint = models.URLField(_("نقطة API"), blank=True)
    api_version = models.CharField(_("إصدار API"), max_length=20, blank=True)
    documentation_url = models.URLField(_("رابط التوثيق"), blank=True)

    # إعدادات الأمان
    api_key = models.CharField(_("مفتاح API"), max_length=500, blank=True)
    secret_key = models.CharField(
        _("المفتاح السري"), max_length=500, blank=True)
    webhook_url = models.URLField(_("رابط Webhook"), blank=True)

    # العملات المدعومة
    supported_currencies = models.JSONField(
        _("العملات المدعومة"), default=list, blank=True)

    # الرسوم والحدود
    transaction_fee_percentage = models.DecimalField(
        _("نسبة رسوم المعاملة"), max_digits=5, decimal_places=2, default=0.00)
    fixed_fee = models.DecimalField(
        _("الرسوم الثابتة"), max_digits=10, decimal_places=2, default=0.00)
    min_transaction_amount = models.DecimalField(
        _("الحد الأدنى للمعاملة"), max_digits=15, decimal_places=2, default=0.00)
    max_transaction_amount = models.DecimalField(
        _("الحد الأقصى للمعاملة"), max_digits=15, decimal_places=2, default=999999.99)

    # إعدادات إضافية
    configuration = models.JSONField(_("الإعدادات"), default=dict, blank=True)

    # معلومات الاستخدام
    total_transactions = models.PositiveIntegerField(
        _("إجمالي المعاملات"), default=0)
    successful_transactions = models.PositiveIntegerField(
        _("المعاملات الناجحة"), default=0)
    last_used = models.DateTimeField(_("آخر استخدام"), null=True, blank=True)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    is_active = models.BooleanField(_("نشط؟"), default=True)

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

    def get_success_rate(self):
        """حساب معدل نجاح المعاملات"""
        if self.total_transactions == 0:
            return 0.0
        return (self.successful_transactions / self.total_transactions) * 100

    class Meta:
        app_label = 'banking_payments'
        verbose_name = _("مقدم الخدمة المصرفية")
        verbose_name_plural = _("مقدمو الخدمات المصرفية")


class PaymentTransaction(models.Model):
    """نموذج لمعاملات الدفع"""
    TRANSACTION_TYPE_CHOICES = [
        ("payment", _("دفع")),
        ("refund", _("استرداد")),
        ("transfer", _("تحويل")),
        ("withdrawal", _("سحب")),
        ("deposit", _("إيداع")),
    ]

    STATUS_CHOICES = [
        ("pending", _("معلق")),
        ("processing", _("قيد المعالجة")),
        ("completed", _("مكتمل")),
        ("failed", _("فشل")),
        ("cancelled", _("ملغي")),
        ("refunded", _("مسترد")),
    ]

    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True)
    external_transaction_id = models.CharField(
        _("معرف المعاملة الخارجي"), max_length=255, blank=True)

    # معلومات المعاملة
    provider = models.ForeignKey(
        BankProvider, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(
        _("نوع المعاملة"), max_length=15, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(
        _("الحالة"), max_length=15, choices=STATUS_CHOICES, default="pending")

    # المبالغ
    amount = models.DecimalField(_("المبلغ"), max_digits=15, decimal_places=2)
    currency = models.CharField(_("العملة"), max_length=3, default="USD")
    fee_amount = models.DecimalField(
        _("مبلغ الرسوم"), max_digits=10, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(
        _("المبلغ الصافي"), max_digits=15, decimal_places=2)

    # معلومات الدافع والمستلم
    payer_name = models.CharField(_("اسم الدافع"), max_length=255, blank=True)
    payer_email = models.EmailField(_("بريد الدافع"), blank=True)
    payer_phone = models.CharField(_("هاتف الدافع"), max_length=20, blank=True)

    recipient_name = models.CharField(
        _("اسم المستلم"), max_length=255, blank=True)
    recipient_account = models.CharField(
        _("حساب المستلم"), max_length=255, blank=True)

    # تفاصيل إضافية
    description = models.TextField(_("الوصف"), blank=True)
    reference_number = models.CharField(
        _("الرقم المرجعي"), max_length=100, blank=True)

    # معلومات النظام المرتبط
    related_model = models.CharField(
        _("النموذج المرتبط"), max_length=100, blank=True)
    related_object_id = models.PositiveIntegerField(
        _("معرف الكائن المرتبط"), null=True, blank=True)

    # البيانات الخام
    raw_request = models.JSONField(_("الطلب الخام"), default=dict, blank=True)
    raw_response = models.JSONField(
        _("الاستجابة الخامة"), default=dict, blank=True)

    # معلومات التوقيت
    initiated_at = models.DateTimeField(_("وقت البدء"), auto_now_add=True)
    processed_at = models.DateTimeField(
        _("وقت المعالجة"), null=True, blank=True)
    completed_at = models.DateTimeField(
        _("وقت الإكمال"), null=True, blank=True)

    # معلومات الخطأ
    error_code = models.CharField(_("رمز الخطأ"), max_length=50, blank=True)
    error_message = models.TextField(_("رسالة الخطأ"), blank=True)

    # معلومات المستخدم
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_transactions"
    )

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency}"

    class Meta:
        app_label = 'banking_payments'
        verbose_name = _("معاملة الدفع")
        verbose_name_plural = _("معاملات الدفع")
        ordering = ["-initiated_at"]


class BankAccount(models.Model):
    """نموذج للحسابات المصرفية"""
    ACCOUNT_TYPE_CHOICES = [
        ("checking", _("جاري")),
        ("savings", _("توفير")),
        ("business", _("تجاري")),
        ("investment", _("استثماري")),
    ]

    account_id = models.UUIDField(default=uuid.uuid4, unique=True)
    provider = models.ForeignKey(
        BankProvider, on_delete=models.CASCADE, related_name="accounts")

    # معلومات الحساب
    account_name = models.CharField(_("اسم الحساب"), max_length=255)
    account_number = models.CharField(_("رقم الحساب"), max_length=100)
    account_type = models.CharField(
        _("نوع الحساب"), max_length=15, choices=ACCOUNT_TYPE_CHOICES)

    # معلومات البنك
    bank_name = models.CharField(_("اسم البنك"), max_length=255)
    bank_code = models.CharField(_("رمز البنك"), max_length=20, blank=True)
    branch_name = models.CharField(_("اسم الفرع"), max_length=255, blank=True)
    branch_code = models.CharField(_("رمز الفرع"), max_length=20, blank=True)

    # معلومات الرصيد
    current_balance = models.DecimalField(
        _("الرصيد الحالي"), max_digits=15, decimal_places=2, default=0.00)
    available_balance = models.DecimalField(
        _("الرصيد المتاح"), max_digits=15, decimal_places=2, default=0.00)
    currency = models.CharField(_("العملة"), max_length=3, default="USD")

    # إعدادات المزامنة
    auto_sync = models.BooleanField(_("مزامنة تلقائية؟"), default=False)
    last_sync = models.DateTimeField(_("آخر مزامنة"), null=True, blank=True)
    sync_frequency = models.PositiveIntegerField(
        _("تكرار المزامنة (دقائق)"), default=60)

    # الحالة
    is_active = models.BooleanField(_("نشط؟"), default=True)
    is_default = models.BooleanField(_("افتراضي؟"), default=False)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.account_name} - {self.account_number}"

    class Meta:
        app_label = 'banking_payments'
        verbose_name = _("الحساب المصرفي")
        verbose_name_plural = _("الحسابات المصرفية")


class PaymentMethod(models.Model):
    """نموذج لطرق الدفع"""
    METHOD_TYPE_CHOICES = [
        ("credit_card", _("بطاقة ائتمان")),
        ("debit_card", _("بطاقة خصم")),
        ("bank_transfer", _("تحويل بنكي")),
        ("digital_wallet", _("محفظة رقمية")),
        ("cash", _("نقد")),
        ("check", _("شيك")),
        ("crypto", _("عملة مشفرة")),
    ]

    method_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم طريقة الدفع"), max_length=255)
    method_type = models.CharField(
        _("نوع الطريقة"), max_length=20, choices=METHOD_TYPE_CHOICES)

    # الإعدادات
    is_enabled = models.BooleanField(_("مفعل؟"), default=True)
    requires_verification = models.BooleanField(
        _("يتطلب تحقق؟"), default=False)

    # الرسوم
    fee_percentage = models.DecimalField(
        _("نسبة الرسوم"), max_digits=5, decimal_places=2, default=0.00)
    fixed_fee = models.DecimalField(
        _("الرسوم الثابتة"), max_digits=10, decimal_places=2, default=0.00)

    # الحدود
    min_amount = models.DecimalField(
        _("الحد الأدنى"), max_digits=15, decimal_places=2, default=0.00)
    max_amount = models.DecimalField(
        _("الحد الأقصى"), max_digits=15, decimal_places=2, default=999999.99)

    # الإعدادات المتقدمة
    configuration = models.JSONField(_("الإعدادات"), default=dict, blank=True)

    # إحصائيات الاستخدام
    usage_count = models.PositiveIntegerField(
        _("عدد مرات الاستخدام"), default=0)
    success_count = models.PositiveIntegerField(
        _("عدد مرات النجاح"), default=0)

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_method_type_display()})"

    def get_success_rate(self):
        """حساب معدل نجاح طريقة الدفع"""
        if self.usage_count == 0:
            return 0.0
        return (self.success_count / self.usage_count) * 100

    class Meta:
        app_label = 'banking_payments'
        verbose_name = _("طريقة الدفع")
        verbose_name_plural = _("طرق الدفع")


class RecurringPayment(models.Model):
    """نموذج للمدفوعات المتكررة"""

    class Meta:
        app_label = "banking_payments"

    FREQUENCY_CHOICES = [
        ("daily", _("يومي")),
        ("weekly", _("أسبوعي")),
        ("monthly", _("شهري")),
        ("quarterly", _("ربع سنوي")),
        ("yearly", _("سنوي")),
    ]

    STATUS_CHOICES = [
        ("active", _("نشط")),
        ("paused", _("متوقف")),
        ("cancelled", _("ملغي")),
        ("completed", _("مكتمل")),
    ]

    recurring_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(_("اسم الدفع المتكرر"), max_length=255)

    # إعدادات الدفع
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="recurring_payments")
    amount = models.DecimalField(_("المبلغ"), max_digits=15, decimal_places=2)
    currency = models.CharField(_("العملة"), max_length=3, default="USD")

    # إعدادات التكرار
    frequency = models.CharField(
        _("التكرار"), max_length=15, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(_("تاريخ البدء"))
    end_date = models.DateField(_("تاريخ الانتهاء"), null=True, blank=True)
    next_payment_date = models.DateField(_("تاريخ الدفع التالي"))

    # الحالة
    status = models.CharField(
        _("الحالة"), max_length=15, choices=STATUS_CHOICES, default="active")

    # إحصائيات
    total_payments = models.PositiveIntegerField(
        _("إجمالي المدفوعات"), default=0)
    successful_payments = models.PositiveIntegerField(
        _("المدفوعات الناجحة"), default=0)
    failed_payments = models.PositiveIntegerField(
        _("المدفوعات الفاشلة"), default=0)

    # معلومات إضافية
    description = models.TextField(_("الوصف"), blank=True)

    # معلومات المستخدم
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recurring_payments"
    )

    # الطوابع الزمنية
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"

    class Meta:
        app_label = 'banking_payments'
        verbose_name = _("الدفع المتكرر")
        verbose_name_plural = _("المدفوعات المتكررة")


class PaymentWebhook(models.Model):
    """نموذج لـ webhooks المدفوعات"""
    EVENT_TYPE_CHOICES = [
        ("payment_completed", _("دفع مكتمل")),
        ("payment_failed", _("دفع فاشل")),
        ("refund_processed", _("استرداد معالج")),
        ("chargeback", _("استرداد قسري")),
        ("subscription_created", _("اشتراك منشأ")),
        ("subscription_cancelled", _("اشتراك ملغي")),
    ]

    webhook_id = models.UUIDField(default=uuid.uuid4, unique=True)
    provider = models.ForeignKey(
        BankProvider, on_delete=models.CASCADE, related_name="webhooks")

    # معلومات الحدث
    event_type = models.CharField(
        _("نوع الحدث"), max_length=30, choices=EVENT_TYPE_CHOICES)
    event_id = models.CharField(_("معرف الحدث"), max_length=255)

    # البيانات
    payload = models.JSONField(_("البيانات"), default=dict)
    headers = models.JSONField(_("الرؤوس"), default=dict, blank=True)

    # معلومات المعالجة
    processed = models.BooleanField(_("معالج؟"), default=False)
    processed_at = models.DateTimeField(
        _("وقت المعالجة"), null=True, blank=True)

    # معلومات الخطأ
    error_message = models.TextField(_("رسالة الخطأ"), blank=True)
    retry_count = models.PositiveIntegerField(_("عدد المحاولات"), default=0)

    # الطوابع الزمنية
    received_at = models.DateTimeField(_("وقت الاستلام"), auto_now_add=True)

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.event_id}"

    class Meta:
        app_label = 'banking_payments'
        verbose_name = _("Webhook الدفع")
        verbose_name_plural = _("Webhooks المدفوعات")
        ordering = ["-received_at"]
