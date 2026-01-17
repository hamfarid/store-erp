# 📋 GAARA ERP v12 - COMPLETE TASKS & SUBTASKS

**Generated:** 2026-01-16
**Total Tasks:** 40
**Total Subtasks:** 156
**Phases:** 5
**Duration:** 8 Weeks

---

## 📊 Summary by Priority

| Priority | Count | Status |
|----------|-------|--------|
| 🔴 **Critical (P0)** | 12 | Pending |
| 🟠 **High (P1)** | 16 | Pending |
| 🟡 **Medium (P2)** | 12 | Pending |
| **Total** | **40** | 0% Complete |

---

## 🔴 PHASE 1: Security & Foundation (Week 1-2)

### Task 1: JWT Configuration (1h access / 24h refresh)
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 1.1 | Update SIMPLE_JWT settings in base.py | ⬜ Pending |
| 1.2 | Implement token refresh endpoint | ⬜ Pending |
| 1.3 | Add token blacklist on rotation | ⬜ Pending |
| 1.4 | Write unit tests for JWT flow | ⬜ Pending |

**Implementation:**
```python
# gaara_erp/settings/base.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

### Task 2: MFA - SMS OTP Implementation
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** Task 1

| # | Subtask | Status |
|---|---------|--------|
| 2.1 | Create SMS provider service (Twilio) | ⬜ Pending |
| 2.2 | Implement OTP generation and storage | ⬜ Pending |
| 2.3 | Create SMS verification endpoint | ⬜ Pending |
| 2.4 | Add rate limiting for SMS requests | ⬜ Pending |

**Implementation:**
```python
# core_modules/security/services/sms_otp.py
class SMSOTPService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 5
    MAX_ATTEMPTS = 3
    
    def generate_otp(self, user):
        otp = ''.join(random.choices(string.digits, k=self.OTP_LENGTH))
        # Store with expiry
        return otp
    
    def send_sms(self, phone, otp):
        # Twilio integration
        pass
    
    def verify_otp(self, user, otp):
        # Verify and invalidate
        pass
```

---

### Task 3: MFA - TOTP Implementation (Google Authenticator)
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** Task 1

| # | Subtask | Status |
|---|---------|--------|
| 3.1 | Install and configure pyotp | ⬜ Pending |
| 3.2 | Create TOTP secret generation | ⬜ Pending |
| 3.3 | Implement QR code generation for setup | ⬜ Pending |
| 3.4 | Generate backup codes | ⬜ Pending |
| 3.5 | Create TOTP verification endpoint | ⬜ Pending |

**Implementation:**
```python
# core_modules/security/services/totp.py
import pyotp
import qrcode

class TOTPService:
    def generate_secret(self):
        return pyotp.random_base32()
    
    def generate_qr_code(self, user, secret):
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(user.email, issuer_name="Gaara ERP")
        # Generate QR code
        return qr_image
    
    def verify_totp(self, secret, code):
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    
    def generate_backup_codes(self, count=10):
        return [secrets.token_hex(4) for _ in range(count)]
```

---

### Task 4: MFA - Email OTP Implementation
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** Task 1

| # | Subtask | Status |
|---|---------|--------|
| 4.1 | Create email service for OTP delivery | ⬜ Pending |
| 4.2 | Design OTP email template (Arabic) | ⬜ Pending |
| 4.3 | Implement email verification endpoint | ⬜ Pending |
| 4.4 | Add resend with cooldown | ⬜ Pending |

**Implementation:**
```python
# core_modules/security/services/email_otp.py
class EmailOTPService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    RESEND_COOLDOWN_SECONDS = 60
    
    def send_otp_email(self, user):
        otp = self.generate_otp()
        # Send email with Arabic template
        send_mail(
            subject='رمز التحقق - Gaara ERP',
            message=f'رمز التحقق الخاص بك هو: {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
```

---

### Task 5: Password Policy (Strong - 12+ chars)
**Priority:** 🔴 Critical | **Est:** 0.5 day | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 5.1 | Update AUTH_PASSWORD_VALIDATORS | ⬜ Pending |
| 5.2 | Create custom password validator | ⬜ Pending |
| 5.3 | Add password strength indicator (frontend) | ⬜ Pending |

**Implementation:**
```python
# gaara_erp/settings/base.py
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'core_modules.security.validators.ComplexityValidator'},
]

# core_modules/security/validators.py
class ComplexityValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError('يجب أن تحتوي كلمة المرور على حرف كبير')
        if not re.search(r'[a-z]', password):
            raise ValidationError('يجب أن تحتوي كلمة المرور على حرف صغير')
        if not re.search(r'[0-9]', password):
            raise ValidationError('يجب أن تحتوي كلمة المرور على رقم')
        if not re.search(r'[!@#$%^&*]', password):
            raise ValidationError('يجب أن تحتوي كلمة المرور على رمز خاص')
```

---

### Task 6: Rate Limiting per Tenant
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 6.1 | Configure django-ratelimit | ⬜ Pending |
| 6.2 | Implement tenant-aware rate keys | ⬜ Pending |
| 6.3 | Add rate limit headers to responses | ⬜ Pending |

**Implementation:**
```python
# core_modules/security/middleware/rate_limit.py
from django_ratelimit.decorators import ratelimit

class TenantRateLimitMiddleware:
    def get_rate_key(self, request):
        tenant = getattr(request, 'tenant', None)
        if tenant:
            return f"tenant:{tenant.id}"
        return f"ip:{request.META.get('REMOTE_ADDR')}"

# Usage on views
@ratelimit(key='user_or_ip', rate='100/m', block=True)
def my_view(request):
    pass
```

---

### Task 7: Multi-tenant Models
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 7.1 | Create Tenant model | ⬜ Pending |
| 7.2 | Create TenantUser model | ⬜ Pending |
| 7.3 | Create TenantSettings model | ⬜ Pending |
| 7.4 | Create TenantPlan model | ⬜ Pending |
| 7.5 | Run migrations | ⬜ Pending |

**Implementation:**
```python
# core_modules/multi_tenant/models.py
class Tenant(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('اسم المستأجر'))
    slug = models.SlugField(unique=True)
    schema_name = models.CharField(max_length=63, unique=True)
    domain = models.CharField(max_length=255, blank=True)
    custom_domain = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    plan = models.ForeignKey('TenantPlan', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class TenantPlan(models.Model):
    name = models.CharField(max_length=100)
    ai_api_calls_limit = models.IntegerField(null=True)  # None = unlimited
    ai_tokens_limit = models.IntegerField(null=True)
    max_users = models.IntegerField(default=5)
    features = models.JSONField(default=dict)
```

---

### Task 8: Schema Middleware
**Priority:** 🔴 Critical | **Est:** 2 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 8.1 | Create TenantMiddleware class | ⬜ Pending |
| 8.2 | Implement schema search path setting | ⬜ Pending |
| 8.3 | Handle public schema for shared data | ⬜ Pending |
| 8.4 | Add schema creation on tenant signup | ⬜ Pending |

**Implementation:**
```python
# core_modules/multi_tenant/middleware.py
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        tenant = self.get_tenant(request)
        if tenant:
            request.tenant = tenant
            self.set_schema(tenant.schema_name)
        else:
            self.set_schema('public')
        
        response = self.get_response(request)
        return response
    
    def set_schema(self, schema_name):
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {schema_name}, public")
```

---

### Task 9: Tenant Router
**Priority:** 🔴 Critical | **Est:** 1 day | **Dependencies:** Tasks 7, 8

| # | Subtask | Status |
|---|---------|--------|
| 9.1 | Implement subdomain detection | ⬜ Pending |
| 9.2 | Implement custom domain lookup | ⬜ Pending |
| 9.3 | Implement X-Tenant-ID header support | ⬜ Pending |
| 9.4 | Add fallback chain | ⬜ Pending |

**Implementation:**
```python
# core_modules/multi_tenant/router.py
class TenantRouter:
    IDENTIFICATION_ORDER = ['subdomain', 'custom_domain', 'header', 'query_param']
    
    def get_tenant(self, request):
        for method in self.IDENTIFICATION_ORDER:
            tenant = getattr(self, f'_get_by_{method}')(request)
            if tenant:
                return tenant
        return None
    
    def _get_by_subdomain(self, request):
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]
        return Tenant.objects.filter(slug=subdomain, is_active=True).first()
    
    def _get_by_custom_domain(self, request):
        host = request.get_host().split(':')[0]
        return Tenant.objects.filter(custom_domain=host, is_active=True).first()
    
    def _get_by_header(self, request):
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_id:
            return Tenant.objects.filter(id=tenant_id, is_active=True).first()
        return None
```

---

### Task 13: Session Security Hardening
**Priority:** 🟠 High | **Est:** 1 day | **Dependencies:** Task 1

| # | Subtask | Status |
|---|---------|--------|
| 13.1 | Implement IP binding | ⬜ Pending |
| 13.2 | Add user agent validation | ⬜ Pending |
| 13.3 | Limit concurrent sessions (max 5) | ⬜ Pending |
| 13.4 | Add session revocation on logout | ⬜ Pending |

---

### Task 14: Tenant Admin UI
**Priority:** 🟠 High | **Est:** 1 day | **Dependencies:** Tasks 7, 8, 9

| # | Subtask | Status |
|---|---------|--------|
| 14.1 | Create TenantAdmin class | ⬜ Pending |
| 14.2 | Add inline TenantSettings | ⬜ Pending |
| 14.3 | Add tenant user management | ⬜ Pending |

---

## 🟠 PHASE 2: Business Logic (Week 3-4)

### Task 10: Accounting IFRS/GAAP Setup
**Priority:** 🔴 Critical | **Est:** 2 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 10.1 | Create IFRS chart of accounts template | ⬜ Pending |
| 10.2 | Create GAAP chart of accounts template | ⬜ Pending |
| 10.3 | Add accounting standard field to TenantSettings | ⬜ Pending |
| 10.4 | Implement account initialization on tenant creation | ⬜ Pending |

**Implementation:**
```python
# business_modules/accounting/templates/ifrs_coa.py
IFRS_CHART_OF_ACCOUNTS = [
    {'code': '1000', 'name': 'الأصول', 'name_en': 'Assets', 'type': 'asset'},
    {'code': '1100', 'name': 'الأصول المتداولة', 'name_en': 'Current Assets', 'type': 'asset'},
    {'code': '1110', 'name': 'النقد والنقد المعادل', 'name_en': 'Cash and Cash Equivalents', 'type': 'asset'},
    # ... more accounts
]

GAAP_CHART_OF_ACCOUNTS = [
    # Similar structure with GAAP-specific accounts
]
```

---

### Task 11: Multi-currency Support
**Priority:** 🔴 Critical | **Est:** 2 days | **Dependencies:** Task 10

| # | Subtask | Status |
|---|---------|--------|
| 11.1 | Create Currency model | ⬜ Pending |
| 11.2 | Create ExchangeRate model with history | ⬜ Pending |
| 11.3 | Implement exchange rate API integration | ⬜ Pending |
| 11.4 | Add currency conversion utilities | ⬜ Pending |
| 11.5 | Update journal entries for multi-currency | ⬜ Pending |

**Implementation:**
```python
# business_modules/accounting/models/currency.py
class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # SAR, USD, EUR
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    decimal_places = models.IntegerField(default=2)
    is_active = models.BooleanField(default=True)

class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_to')
    rate = models.DecimalField(max_digits=18, decimal_places=8)
    effective_date = models.DateField()
    source = models.CharField(max_length=50)  # 'manual', 'api', 'bank'

class CurrencyService:
    BASE_CURRENCY = 'SAR'
    
    def convert(self, amount, from_currency, to_currency, date=None):
        rate = self.get_rate(from_currency, to_currency, date)
        return amount * rate
```

---

### Task 15: Journal Entries System
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Tasks 10, 11

| # | Subtask | Status |
|---|---------|--------|
| 15.1 | Create JournalEntry model | ⬜ Pending |
| 15.2 | Create JournalLine model | ⬜ Pending |
| 15.3 | Implement balance validation | ⬜ Pending |
| 15.4 | Add posting workflow | ⬜ Pending |

---

### Task 16: Financial Reports
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 15

| # | Subtask | Status |
|---|---------|--------|
| 16.1 | Implement Trial Balance report | ⬜ Pending |
| 16.2 | Implement Income Statement (P&L) | ⬜ Pending |
| 16.3 | Implement Balance Sheet | ⬜ Pending |
| 16.4 | Add multi-currency conversion in reports | ⬜ Pending |

---

### Task 17: Inventory Management
**Priority:** 🟠 High | **Est:** 3 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 17.1 | Verify Product model completeness | ⬜ Pending |
| 17.2 | Verify Warehouse and Location models | ⬜ Pending |
| 17.3 | Implement stock movement service | ⬜ Pending |
| 17.4 | Add lot/batch tracking | ⬜ Pending |

---

### Task 18: Sales Orders
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 17

| # | Subtask | Status |
|---|---------|--------|
| 18.1 | Create SalesOrder model | ⬜ Pending |
| 18.2 | Create SalesOrderLine model | ⬜ Pending |
| 18.3 | Implement order workflow | ⬜ Pending |
| 18.4 | Add tax calculation | ⬜ Pending |

---

### Task 19: Sales Invoices
**Priority:** 🟠 High | **Est:** 1 day | **Dependencies:** Task 18

| # | Subtask | Status |
|---|---------|--------|
| 19.1 | Create SalesInvoice model | ⬜ Pending |
| 19.2 | Link invoices to journal entries | ⬜ Pending |
| 19.3 | Implement payment recording | ⬜ Pending |

---

### Task 20: Purchase Orders
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 17

| # | Subtask | Status |
|---|---------|--------|
| 20.1 | Create PurchaseOrder model | ⬜ Pending |
| 20.2 | Create GoodsReceivedNote model | ⬜ Pending |
| 20.3 | Implement three-way matching | ⬜ Pending |

---

## 🟡 PHASE 3: AI & Integration (Week 5-6)

### Task 21: AI Service Layer
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 21.1 | Create AIService base class | ⬜ Pending |
| 21.2 | Implement OpenAI provider | ⬜ Pending |
| 21.3 | Implement fallback mechanism | ⬜ Pending |
| 21.4 | Add request/response logging | ⬜ Pending |

**Implementation:**
```python
# ai_modules/core/services/ai_service.py
class AIService:
    def __init__(self, tenant):
        self.tenant = tenant
        self.provider = self._get_provider()
    
    def _get_provider(self):
        return OpenAIProvider()
    
    async def chat(self, messages, **kwargs):
        try:
            self._check_quota()
            response = await self.provider.chat(messages, **kwargs)
            self._track_usage(response)
            return response
        except AIServiceUnavailable:
            return self._fallback_response('chat')
    
    def _check_quota(self):
        usage = self.tenant.get_ai_usage()
        if usage.is_exceeded:
            raise QuotaExceeded()
    
    def _fallback_response(self, operation):
        if operation == 'chat':
            return {'message': 'خدمة الذكاء الاصطناعي غير متاحة حالياً'}
        return None
```

---

### Task 22: AI Usage Tracking
**Priority:** 🟠 High | **Est:** 1 day | **Dependencies:** Task 21

| # | Subtask | Status |
|---|---------|--------|
| 22.1 | Create AIUsage model | ⬜ Pending |
| 22.2 | Implement usage tracking middleware | ⬜ Pending |
| 22.3 | Create usage dashboard widget | ⬜ Pending |

**Implementation:**
```python
# ai_modules/core/models/usage.py
class AIUsage(models.Model):
    tenant = models.ForeignKey('multi_tenant.Tenant', on_delete=models.CASCADE)
    date = models.DateField()
    api_calls = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    class Meta:
        unique_together = ['tenant', 'date']
    
    @classmethod
    def track(cls, tenant, tokens):
        usage, _ = cls.objects.get_or_create(
            tenant=tenant,
            date=timezone.now().date()
        )
        usage.api_calls += 1
        usage.tokens_used += tokens
        usage.save()
```

---

### Task 23: AI Quota Limits
**Priority:** 🟠 High | **Est:** 1 day | **Dependencies:** Task 22

| # | Subtask | Status |
|---|---------|--------|
| 23.1 | Add quota fields to TenantPlan | ⬜ Pending |
| 23.2 | Implement quota checking service | ⬜ Pending |
| 23.3 | Add quota exceeded notifications | ⬜ Pending |

**Quota Tiers:**
```python
AI_USAGE_LIMITS = {
    'free': {'api_calls': 100, 'tokens': 10000},
    'basic': {'api_calls': 1000, 'tokens': 100000},
    'professional': {'api_calls': 10000, 'tokens': 1000000},
    'enterprise': {'api_calls': None, 'tokens': None},  # Unlimited
}
```

---

### Task 24: Farm Management
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 24.1 | Verify Farm model completeness | ⬜ Pending |
| 24.2 | Verify Plot model completeness | ⬜ Pending |
| 24.3 | Implement activity logging | ⬜ Pending |
| 24.4 | Add crop tracking | ⬜ Pending |

---

### Task 25: Plant Diagnosis
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Tasks 21, 24

| # | Subtask | Status |
|---|---------|--------|
| 25.1 | Create diagnosis upload endpoint | ⬜ Pending |
| 25.2 | Integrate AI vision model | ⬜ Pending |
| 25.3 | Implement treatment database | ⬜ Pending |
| 25.4 | Create diagnosis history | ⬜ Pending |

---

### Task 29: AI Fallback Implementation
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** Task 21

| # | Subtask | Status |
|---|---------|--------|
| 29.1 | Implement response caching | ⬜ Pending |
| 29.2 | Create fallback responses | ⬜ Pending |
| 29.3 | Add circuit breaker | ⬜ Pending |

---

### Task 30: Agricultural Experiments
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** Task 24

| # | Subtask | Status |
|---|---------|--------|
| 30.1 | Create Experiment model | ⬜ Pending |
| 30.2 | Create ExperimentResult model | ⬜ Pending |
| 30.3 | Implement experiment reports | ⬜ Pending |

---

## 🟢 PHASE 4: Services & Admin (Week 7)

### Task 26: HR Module
**Priority:** 🟠 High | **Est:** 3 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 26.1 | Verify Employee model | ⬜ Pending |
| 26.2 | Verify Department model | ⬜ Pending |
| 26.3 | Implement attendance tracking | ⬜ Pending |
| 26.4 | Implement leave management | ⬜ Pending |

---

### Task 27: Project Management
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 27.1 | Create Project model | ⬜ Pending |
| 27.2 | Create Task model | ⬜ Pending |
| 27.3 | Implement Gantt chart data | ⬜ Pending |
| 27.4 | Add resource allocation | ⬜ Pending |

---

### Task 31: Quality Control
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** Task 17

| # | Subtask | Status |
|---|---------|--------|
| 31.1 | Create Inspection model | ⬜ Pending |
| 31.2 | Create NCR model | ⬜ Pending |
| 31.3 | Implement quality reports | ⬜ Pending |

---

### Task 32: Dashboard Module
**Priority:** 🟡 Medium | **Est:** 2 days | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 32.1 | Create dashboard API endpoints | ⬜ Pending |
| 32.2 | Implement widget system | ⬜ Pending |
| 32.3 | Add chart data providers | ⬜ Pending |

---

### Task 33: Backup System
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** Task 7

| # | Subtask | Status |
|---|---------|--------|
| 33.1 | Implement backup service | ⬜ Pending |
| 33.2 | Add backup scheduling | ⬜ Pending |
| 33.3 | Implement restore functionality | ⬜ Pending |

---

### Task 34: Health Monitoring
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 34.1 | Create health check endpoints | ⬜ Pending |
| 34.2 | Implement alert system | ⬜ Pending |
| 34.3 | Add performance metrics | ⬜ Pending |

---

## 🔵 PHASE 5: Testing & Deployment (Week 8)

### Task 12: Unit Test Suite
**Priority:** 🔴 Critical | **Est:** 3 days | **Dependencies:** All P0 tasks

| # | Subtask | Status |
|---|---------|--------|
| 12.1 | Security module tests | ⬜ Pending |
| 12.2 | Multi-tenant tests | ⬜ Pending |
| 12.3 | Accounting tests | ⬜ Pending |
| 12.4 | MFA tests | ⬜ Pending |

---

### Task 28: Integration Tests
**Priority:** 🟠 High | **Est:** 2 days | **Dependencies:** Task 12

| # | Subtask | Status |
|---|---------|--------|
| 28.1 | Auth API tests | ⬜ Pending |
| 28.2 | Tenant API tests | ⬜ Pending |
| 28.3 | Business module API tests | ⬜ Pending |
| 28.4 | AI API tests | ⬜ Pending |

---

### Task 35: E2E Test Suite
**Priority:** 🟡 Medium | **Est:** 2 days | **Dependencies:** Task 28

| # | Subtask | Status |
|---|---------|--------|
| 35.1 | Login/logout flow tests | ⬜ Pending |
| 35.2 | MFA flow tests | ⬜ Pending |
| 35.3 | Business operation tests | ⬜ Pending |
| 35.4 | Multi-tenant switching tests | ⬜ Pending |

---

### Task 36: Docker Configuration
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 36.1 | Create production Dockerfile | ⬜ Pending |
| 36.2 | Create docker-compose.prod.yml | ⬜ Pending |
| 36.3 | Add health checks | ⬜ Pending |

---

### Task 37: Kubernetes Configuration
**Priority:** 🟡 Medium | **Est:** 2 days | **Dependencies:** Task 36

| # | Subtask | Status |
|---|---------|--------|
| 37.1 | Create deployment manifests | ⬜ Pending |
| 37.2 | Create service manifests | ⬜ Pending |
| 37.3 | Create ingress configuration | ⬜ Pending |
| 37.4 | Add horizontal pod autoscaler | ⬜ Pending |

---

### Task 38: CI/CD Pipeline
**Priority:** 🟡 Medium | **Est:** 1 day | **Dependencies:** Task 36

| # | Subtask | Status |
|---|---------|--------|
| 38.1 | Create CI workflow | ⬜ Pending |
| 38.2 | Create CD workflow | ⬜ Pending |
| 38.3 | Add security scanning | ⬜ Pending |

---

### Task 39: API Documentation
**Priority:** 🟡 Medium | **Est:** 2 days | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 39.1 | Generate OpenAPI schema | ⬜ Pending |
| 39.2 | Add Arabic descriptions | ⬜ Pending |
| 39.3 | Create usage examples | ⬜ Pending |

---

### Task 40: User Documentation
**Priority:** 🟡 Medium | **Est:** 2 days | **Dependencies:** None

| # | Subtask | Status |
|---|---------|--------|
| 40.1 | Create user guide | ⬜ Pending |
| 40.2 | Create admin guide | ⬜ Pending |
| 40.3 | Add Arabic translations | ⬜ Pending |

---

## 📊 Quick Reference

### By Phase
| Phase | Tasks | Subtasks | Duration |
|-------|-------|----------|----------|
| Phase 1 | 11 | 43 | Week 1-2 |
| Phase 2 | 9 | 36 | Week 3-4 |
| Phase 3 | 8 | 28 | Week 5-6 |
| Phase 4 | 5 | 18 | Week 7 |
| Phase 5 | 7 | 31 | Week 8 |
| **Total** | **40** | **156** | **8 Weeks** |

### By Priority
| Priority | Tasks | First Task |
|----------|-------|------------|
| 🔴 Critical | 12 | Task 1: JWT Config |
| 🟠 High | 16 | Task 13: Session Security |
| 🟡 Medium | 12 | Task 29: AI Fallback |

### Dependencies Summary
```
Task 1 (JWT) ──────┬──► Task 2 (SMS MFA)
                   ├──► Task 3 (TOTP MFA)
                   ├──► Task 4 (Email MFA)
                   └──► Task 13 (Session Security)

Task 7 (Tenant) ───┬──► Task 6 (Rate Limit)
                   ├──► Task 8 (Schema) ──► Task 9 (Router) ──► Task 14 (Admin)
                   └──► Task 10 (Accounting) ──► Task 11 (Currency) ──► Task 15 (Journal)
```

---

## 🚀 Start Implementation

**Command:** `/speckit.implement`

**First Task:** Task 1 - JWT Configuration

---

*Generated: 2026-01-16*
*Status: Ready for Implementation*
