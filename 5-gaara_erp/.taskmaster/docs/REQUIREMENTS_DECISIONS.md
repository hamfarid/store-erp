# 📋 REQUIREMENTS DECISIONS
## Gaara ERP v12 - Finalized Requirements

**Date:** 2026-01-16
**Status:** ✅ APPROVED
**Ready For:** Implementation

---

## 🔐 Security & Authentication

| Decision | Choice | Details |
|----------|--------|---------|
| **S1: MFA Methods** | ✅ **ALL** | SMS OTP, TOTP (Google Auth), Email OTP |
| **S2: JWT Token Lifetime** | ✅ **1 Hour** | Access: 1h, Refresh: 24h |
| **S5: Password Policy** | ✅ **Strong** | 12+ chars, uppercase, lowercase, number, special |

### Implementation Notes:
```python
# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Password Policy
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

## 🏢 Multi-Tenancy

| Decision | Choice | Details |
|----------|--------|---------|
| **T1: Isolation Strategy** | ✅ **Schema-based** | Separate PostgreSQL schemas per tenant |
| **T3: Tenant Identification** | ✅ **All Methods** | Subdomain + Custom domain + Header |

### Implementation Notes:
```python
# Tenant Middleware Priority
TENANT_IDENTIFICATION_ORDER = [
    'subdomain',      # tenant.gaara-erp.com
    'custom_domain',  # erp.customer.com
    'header',         # X-Tenant-ID header
    'query_param',    # ?tenant=xxx (fallback)
]

# Schema naming
TENANT_SCHEMA_PREFIX = 'tenant_'
# Example: tenant_acme, tenant_xyz
```

---

## 💼 Business Logic

| Decision | Choice | Details |
|----------|--------|---------|
| **B1: Accounting Standards** | ✅ **Both** | IFRS and GAAP support |
| **B2: Multi-Currency** | ✅ **Yes** | Full multi-currency with exchange rates |

### Implementation Notes:
```python
# Accounting Configuration
ACCOUNTING_STANDARDS = ['IFRS', 'GAAP']
DEFAULT_ACCOUNTING_STANDARD = 'IFRS'

# Currency Settings
MULTI_CURRENCY_ENABLED = True
BASE_CURRENCY = 'SAR'  # Saudi Riyal
EXCHANGE_RATE_UPDATE_FREQUENCY = 'daily'
```

---

## 🤖 AI Integration

| Decision | Choice | Details |
|----------|--------|---------|
| **A3: External AI APIs** | ✅ **Yes** | Data can be sent to external APIs |
| **A4: Fallback Behavior** | ✅ **Graceful** | Graceful degradation when unavailable |

### Implementation Notes:
```python
# AI Configuration
AI_CONFIG = {
    'providers': ['openai', 'anthropic', 'local'],
    'primary_provider': 'openai',
    'fallback_behavior': 'graceful_degradation',
    'data_privacy': {
        'allow_external_api': True,
        'anonymize_pii': True,  # Still recommended
        'log_api_calls': True,
    },
    'fallback_responses': {
        'chat': 'AI service temporarily unavailable. Please try again later.',
        'analysis': None,  # Return null for optional features
        'predictions': 'cached',  # Use last cached prediction
    }
}
```

---

## 🚫 Resolved Blocking Issues

### 1. Agricultural Module Scope
| Decision | ✅ **CORE** |
|----------|-------------|
| **Impact** | Agricultural modules are required in all deployments |
| **Action** | Include in base schema, cannot be disabled |

### 2. AI Cost Management
| Decision | ✅ **Limit per Customer** |
|----------|--------------------------|
| **Impact** | Each tenant has API usage quota |
| **Action** | Implement usage tracking and limits |

```python
# AI Usage Limits (per tenant/month)
AI_USAGE_LIMITS = {
    'free': {'api_calls': 100, 'tokens': 10000},
    'basic': {'api_calls': 1000, 'tokens': 100000},
    'professional': {'api_calls': 10000, 'tokens': 1000000},
    'enterprise': {'api_calls': None, 'tokens': None},  # Unlimited
}
```

### 3. Deployment Target
| Decision | ✅ **BOTH** |
|----------|-------------|
| **Impact** | Support self-hosted AND Cloud SaaS |
| **Action** | Design for both deployment models |

```yaml
# Deployment Modes
deployment:
  modes:
    - self_hosted:
        docker: true
        kubernetes: true
        single_tenant: true
    - cloud_saas:
        multi_tenant: true
        auto_scaling: true
        managed: true
```

---

## 📊 Summary of All Decisions

| Area | Decision | Value |
|------|----------|-------|
| MFA Methods | S1 | All (SMS, TOTP, Email) |
| JWT Lifetime | S2 | 1 Hour |
| Password Policy | S5 | Strong (12+ chars) |
| Tenant Isolation | T1 | Schema-based |
| Tenant ID | T3 | All methods |
| Accounting | B1 | Both (IFRS + GAAP) |
| Multi-Currency | B2 | Yes |
| External AI | A3 | Yes (allowed) |
| AI Fallback | A4 | Graceful degradation |
| Agri Modules | - | Core (required) |
| AI Costs | - | Quota per customer |
| Deployment | - | Both (self-hosted + SaaS) |

---

## ✅ Ready for Implementation

All blocking issues resolved. Ready to proceed with:
- `/speckit.implement` - Start Phase 1 implementation

---

*Document approved: 2026-01-16*
