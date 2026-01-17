# تعريفات الكلاسات والدوال والثوابت - Gaara ERP v12

## نظرة عامة
توثيق شامل لجميع تعريفات الكلاسات والدوال والثوابت الرئيسية في نظام Gaara ERP v12.

## 1. تعريفات الكلاسات (Class Definitions)

### 1.1 نماذج Django (Django Models)
```python
# /business_modules/accounting/models.py
class Account(models.Model):
    """نموذج الحسابات المحاسبية"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

# /business_modules/inventory/models.py
class Product(models.Model):
    """نموذج المنتجات"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey("ProductCategory", on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)

# /business_modules/sales/models.py
class SalesOrder(models.Model):
    """نموذج أوامر البيع"""
    name = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey("sales.Customer", on_delete=models.PROTECT)
    date_order = models.DateField(default=date.today)
    state = models.CharField(max_length=20, default=\"draft\")
```

### 1.2 مسلسلات DRF (DRF Serializers)
```python
# /business_modules/accounting/serializers.py
class AccountSerializer(serializers.ModelSerializer):
    """مسلسل الحسابات"""
    class Meta:
        model = Account
        fields = ["id", "code", "name", "account_type", "parent"]

# /business_modules/inventory/serializers.py
class ProductSerializer(serializers.ModelSerializer):
    """مسلسل المنتجات"""
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name", "code", "category", "category_name", "unit_price"]
```

### 1.3 عروض DRF (DRF Views)
```python
# /business_modules/accounting/views.py
class AccountViewSet(viewsets.ModelViewSet):
    """عرض الحسابات"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["account_type", "parent"]
    search_fields = ["code", "name"]

# /business_modules/inventory/views.py
class ProductViewSet(viewsets.ModelViewSet):
    """عرض المنتجات"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
```

### 1.4 كلاسات الخدمات (Service Classes)
```python
# /business_modules/accounting/services/report_service.py
class FinancialReportService:
    """خدمة التقارير المالية"""
    def get_trial_balance(self, start_date, end_date):
        # ... منطق ميزان المراجعة
        pass

    def get_balance_sheet(self, date):
        # ... منطق الميزانية العمومية
        pass

# /security/mfa.py
class MFAService:
    """خدمة المصادقة متعددة العوامل"""
    def generate_secret_key(self):
        # ... إنشاء مفتاح سري
        pass

    def verify_otp(self, secret_key, otp):
        # ... التحقق من OTP
        pass
```

## 2. تعريفات الدوال (Function Definitions)

### 2.1 دوال API (API Functions)
```python
# /business_modules/sales/views.py
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_sales_order(request, pk):
    """تأكيد أمر البيع"""
    order = get_object_or_404(SalesOrder, pk=pk)
    order.confirm()
    return Response({"status": "confirmed"}, status=status.HTTP_200_OK)

# /admin_modules/custom_admin/views/backup_restore_views.py
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_backup(request):
    """إنشاء نسخة احتياطية"""
    task = create_backup_task.delay()
    return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
```

### 2.2 دوال الخدمات (Service Functions)
```python
# /business_modules/inventory/services.py
def adjust_stock_quantity(product, location, quantity, user):
    """تعديل كمية المخزون"""
    # ... منطق تعديل المخزون
    pass

# /integration_modules/ai_agriculture/services/crop_prediction_service.py
def predict_crop_yield(field, crop, weather_data):
    """التنبؤ بإنتاجية المحصول"""
    # ... منطق التنبؤ بالذكاء الاصطناعي
    pass
```

### 2.3 دوال Celery (Celery Tasks)
```python
# /business_modules/accounting/tasks.py
@shared_task
def generate_monthly_reports(year, month):
    """إنشاء التقارير الشهرية"""
    # ... منطق إنشاء التقارير
    pass

# /integration_modules/ai/tasks.py
@shared_task
def train_ai_model(model_id):
    """تدريب نموذج الذكاء الاصطناعي"""
    # ... منطق تدريب النموذج
    pass
```

### 2.4 دوال المساعدة (Helper Functions)
```python
# /core_modules/utils/helpers.py
def format_currency(amount, currency_code):
    """تنسيق العملة"""
    # ... منطق تنسيق العملة
    pass

# /agricultural_modules/utils.py
def calculate_irrigation_needs(soil_moisture, crop_type, weather_forecast):
    """حساب احتياجات الري"""
    # ... منطق حساب الري
    pass
```

## 3. تعريفات الثوابت (Constant Definitions)

### 3.1 ثوابت النماذج (Model Constants)
```python
# /business_modules/sales/models.py
class SalesOrder(models.Model):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    STATE_CHOICES = [
        (DRAFT, _("مسودة")),
        (CONFIRMED, _("مؤكد")),
        (DELIVERED, _("تم التسليم")),
        (CANCELLED, _("ملغي")),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=DRAFT)

# /business_modules/accounting/models.py
class Account(models.Model):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    INCOME = "income"
    EXPENSE = "expense"
    ACCOUNT_TYPE_CHOICES = [
        (ASSET, _("أصل")),
        (LIABILITY, _("التزام")),
        (EQUITY, _("حقوق ملكية")),
        (INCOME, _("إيراد")),
        (EXPENSE, _("مصروف")),
    ]
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
```

### 3.2 ثوابت الإعدادات (Settings Constants)
```python
# /gaara_erp/settings/base.py
# Internationalization
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000

# Celery
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
```

### 3.3 ثوابت النظام (System Constants)
```python
# /core_modules/constants.py
DEFAULT_CURRENCY = "SAR"
DEFAULT_COUNTRY = "SA"

# /ai_modules/constants.py
DEFAULT_AI_MODEL = "gpt-4"
AI_TEMPERATURE = 0.7

# /security/constants.py
MFA_ISSUER_NAME = "Gaara ERP"
PASSWORD_RESET_TIMEOUT_HOURS = 24
```

## 4. توصيات لتوحيد التعريفات

### 4.1 استخدام ملفات الثوابت
- **إنشاء ملف `constants.py`** لكل وحدة لتجميع الثوابت المتعلقة بها.
- **إنشاء ملف `core_modules/constants.py`** للثوابت العامة على مستوى النظام.

### 4.2 توحيد أسماء الحالات
- **استخدام أسماء حالات موحدة** عبر جميع الوحدات (e.g., `draft`, `confirmed`, `cancelled`).
- **استخدام `TextChoices`** في Django لتعريف الخيارات بشكل أفضل.

### 4.3 توثيق التعريفات
- **إضافة Docstrings** لجميع الكلاسات والدوال لشرح وظيفتها.
- **إضافة تعليقات** للثوابت لشرح الغرض منها.

### 4.4 استخدام Enums
- **استخدام `Enum`** في Python لتعريف مجموعات الثوابت ذات الصلة.
- **استخدام `models.TextChoices`** في Django لتعريف خيارات الحقول.

---

**تاريخ التوثيق**: نوفمبر 2025  
**إصدار النظام**: Gaara ERP v12 Enhanced Security Edition  
**حالة التوثيق**: شامل ومحدث
