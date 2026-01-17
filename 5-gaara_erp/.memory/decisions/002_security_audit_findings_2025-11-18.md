# Decision 002: Critical Security Audit Findings

**Date**: 2025-11-18 09:17
**Phase**: Phase 1 - Deep Code Analysis
**Decision Type**: Security Assessment
**Severity**: CRITICAL (P0)

---

## Executive Summary

Deep code analysis reveals **MIXED security posture**:
- ✅ **GOOD**: Argon2 password hashing, security middleware exists, JWT infrastructure present
- ❌ **CRITICAL**: Multiple configuration files with conflicting settings, potential security bypasses

---

## CRITICAL FINDINGS

### 1. JWT Configuration - CONFLICTING SETTINGS ⚠️

**Location 1**: `gaara_erp/gaara_erp/settings/security.py:100`
```python
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # ✅ GOOD (30 min)
```

**Location 2**: `gaara_erp/admin_modules/custom_admin/jwt_config.py:13`
```python
"ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # ❌ BAD (60 min - 4x guideline)
```

**Location 3**: `gaara_erp/gaara_erp/settings/security_enhanced.py:197`
```python
'JWT_EXPIRATION_DELTA': int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', '3600')),  # ❌ BAD (3600 sec = 1 hour)
```

**Issue**: Multiple JWT configurations exist. Unclear which is active.
**Risk**: HIGH - Token lifetime may be 1 hour instead of 15 minutes
**Action Required**: Consolidate to single configuration, enforce 15-minute TTL

### 2. Password Hashing - GOOD ✅

**Location**: `gaara_erp/gaara_erp/settings/security.py:64-70`
```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # ✅ EXCELLENT
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    ...
]
```

**Status**: ✅ Using Argon2 (best practice)
**Action**: None required

### 3. CSRF Protection - ENABLED ✅

**Location**: `gaara_erp/gaara_erp/settings/security.py:45-47`
```python
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
```

**Status**: ✅ CSRF protection enabled
**Issue**: `CSRF_COOKIE_SECURE` defaults to False (should be True in production)
**Action**: Set to True in production environment

### 4. Rate Limiting - IMPLEMENTED ✅

**Location**: `gaara_erp/core_modules/security/middleware.py:110-118`
```python
if request.path.startswith('/api/auth/') and request.method == 'POST':
    if self.is_rate_limited(ip_address, 'login', 5, 300):  # 5 attempts in 5 minutes
        # Return 429
```

**Status**: ✅ Rate limiting exists for auth endpoints
**Coverage**: Login endpoints protected (5 attempts / 5 minutes)
**Action**: Verify it's enabled in production settings

### 5. Account Lockout - PARTIALLY IMPLEMENTED ⚠️

**Location**: `gaara_erp/core_modules/users/models.py:237-241`
```python
failed_login_attempts = models.PositiveIntegerField(
    _('محاولات تسجيل الدخول الفاشلة'),
    default=0,
    help_text=_('عدد محاولات تسجيل الدخول الفاشلة المتتالية')
)
```

**Status**: ⚠️ Field exists but lockout logic not found in authentication service
**Action**: Implement lockout logic in `core_modules/users/services.py`

### 6. Security Headers - IMPLEMENTED ✅

**Location**: `gaara_erp/gaara_erp/middleware/security_headers.py:16-28`
```python
response["Strict-Transport-Security"] = hsts
# X-Content-Type-Options, Referrer-Policy, etc.
```

**Status**: ✅ Security headers middleware exists
**Action**: Verify it's in MIDDLEWARE list

### 7. Hardcoded Secrets - FOUND ❌

**Location 1**: `api_gateway/main.py:62`
```python
payload = jwt.decode(token, "secret_key", algorithms=["HS256"])  # ❌ HARDCODED
```

**Location 2**: `api_gateway/main.py:162`
```python
token = jwt.encode({"user_id": 1, "username": username}, "secret_key", algorithm="HS256")  # ❌ HARDCODED
```

**Location 3**: `gaara_erp/gaara_erp/settings/base.py:13`
```python
SECRET_KEY = config("SECRET_KEY", default="942ec766e095b238e40f36dfc3fe24bca61f151e394bf6d4fd1e4c4a54e4d418b01166d3762621a7eefe1b7fcf6fdc77e120")  # ❌ LONG DEFAULT
```

**Risk**: CRITICAL - Hardcoded secrets in code
**Action**: Remove all hardcoded secrets, use environment variables only

### 8. HTTPS Enforcement - CONFIGURABLE ⚠️

**Location**: `gaara_erp/gaara_erp/settings/base.py:21`
```python
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
```

**Status**: ⚠️ Defaults to True (good) but can be disabled via env var
**Action**: Force True in production, no override

---

## POSITIVE FINDINGS

1. ✅ **Argon2 Password Hashing**: Best-in-class password security
2. ✅ **CSRF Protection**: Enabled with proper cookie settings
3. ✅ **Rate Limiting**: Implemented for auth endpoints
4. ✅ **Security Headers**: Middleware exists for HSTS, CSP, etc.
5. ✅ **JWT Infrastructure**: rest_framework_simplejwt installed
6. ✅ **Security Middleware**: Multiple security layers implemented
7. ✅ **User Model**: Has `failed_login_attempts` field

---

## CRITICAL ACTIONS REQUIRED (P0)

### Immediate (Next 24 Hours)

1. **Consolidate JWT Configuration**
   - Remove duplicate JWT configs
   - Set ACCESS_TOKEN_LIFETIME to 15 minutes globally
   - Set REFRESH_TOKEN_LIFETIME to 7 days
   - Enable ROTATE_REFRESH_TOKENS

2. **Remove Hardcoded Secrets**
   - Fix `api_gateway/main.py` (lines 62, 162)
   - Remove default SECRET_KEY from `settings/base.py`
   - Scan entire codebase for "secret_key", "SECRET_KEY"

3. **Implement Account Lockout Logic**
   - Add lockout logic to `core_modules/users/services.py`
   - Lock account after 5 failed attempts
   - Auto-unlock after 15 minutes

4. **Force HTTPS in Production**
   - Remove ability to disable SECURE_SSL_REDIRECT in production
   - Set CSRF_COOKIE_SECURE = True (no override)
   - Set SESSION_COOKIE_SECURE = True (no override)

5. **Verify Middleware Order**
   - Ensure SecurityHeadersMiddleware is in MIDDLEWARE list
   - Ensure RateLimitMiddleware is active
   - Verify CSRF middleware is enabled

---

## DECISION

**APPROVED**: Proceed with P0 security fixes immediately
**Priority Order**:
1. Remove hardcoded secrets (CRITICAL)
2. Consolidate JWT configuration (CRITICAL)
3. Implement account lockout (HIGH)
4. Force HTTPS in production (HIGH)
5. Verify middleware configuration (MEDIUM)

**Timeline**: 24-48 hours for P0 fixes

---

**Next Steps**: Create detailed fix plan for each issue

