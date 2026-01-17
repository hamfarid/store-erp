# P0 SECURITY FIX PLAN - Gaara ERP v12

**Created**: 2025-11-18 09:21
**Priority**: CRITICAL (P0)
**Timeline**: 24-48 hours
**Owner**: Autonomous AI Agent

---

## OVERVIEW

**Total P0 Fixes**: 5 critical security issues
**Estimated Time**: 8-12 hours
**Risk Level**: HIGH (production deployment blocked until complete)

---

## FIX #1: REMOVE HARDCODED SECRETS ⚠️ CRITICAL

**Priority**: P0 (HIGHEST)
**Estimated Time**: 1 hour
**Risk**: CRITICAL - Exposed secrets in code

### Files to Modify

#### 1.1 api_gateway/main.py (2 occurrences)

**Line 62** - BEFORE:
```python
payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
```

**Line 62** - AFTER:
```python
import os
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")
payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
```

**Line 162** - BEFORE:
```python
token = jwt.encode({"user_id": 1, "username": username}, "secret_key", algorithm="HS256")
```

**Line 162** - AFTER:
```python
token = jwt.encode({"user_id": 1, "username": username}, JWT_SECRET_KEY, algorithm="HS256")
```

#### 1.2 gaara_erp/gaara_erp/settings/base.py

**Line 13** - BEFORE:
```python
SECRET_KEY = config("SECRET_KEY", default="942ec766e095b238e40f36dfc3fe24bca61f151e394bf6d4fd1e4c4a54e4d418b01166d3762621a7eefe1b7fcf6fdc77e120")
```

**Line 13** - AFTER:
```python
SECRET_KEY = config("SECRET_KEY")  # No default - must be set in environment
```

### Testing Strategy
1. Set `JWT_SECRET_KEY` in `.env.example`
2. Verify application fails to start without `SECRET_KEY`
3. Test JWT token generation/verification with env var
4. Run security scan to verify no hardcoded secrets remain

### Verification
```bash
# Scan for hardcoded secrets
grep -r "secret_key" gaara_erp/ --include="*.py" | grep -v ".env"
grep -r "SECRET_KEY.*=" gaara_erp/ --include="*.py" | grep "default="
```

---

## FIX #2: CONSOLIDATE JWT CONFIGURATION ⚠️ CRITICAL

**Priority**: P0
**Estimated Time**: 2 hours
**Risk**: HIGH - Conflicting configurations

### Decision: Use settings/security.py as Single Source of Truth

#### 2.1 gaara_erp/gaara_erp/settings/security.py

**Lines 99-120** - MODIFY:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # ✅ Changed from 30 to 15
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # ✅ Changed from 1 to 7
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': 'gaara-erp',
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
```

#### 2.2 admin_modules/custom_admin/jwt_config.py

**Action**: DELETE THIS FILE or mark as deprecated
**Reason**: Conflicts with settings/security.py

**Alternative**: If needed, import from settings:
```python
from gaara_erp.settings.security import SIMPLE_JWT as JWT_SETTINGS
```

#### 2.3 gaara_erp/gaara_erp/settings/security_enhanced.py

**Lines 197-198** - DELETE or COMMENT OUT:
```python
# DEPRECATED - Use SIMPLE_JWT in settings/security.py instead
# 'JWT_EXPIRATION_DELTA': int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', '3600')),
```

### Testing Strategy
1. Verify only one JWT configuration is active
2. Test token generation with 15-minute expiry
3. Test refresh token rotation
4. Verify old tokens are blacklisted after rotation
5. Test token expiry (wait 16 minutes, verify 401)

### Verification
```bash
# Find all JWT configurations
grep -r "ACCESS_TOKEN_LIFETIME" gaara_erp/ --include="*.py"
grep -r "JWT_EXPIRATION_DELTA" gaara_erp/ --include="*.py"
```

---

## FIX #3: IMPLEMENT ACCOUNT LOCKOUT LOGIC ⚠️ HIGH

**Priority**: P0
**Estimated Time**: 3 hours
**Risk**: HIGH - Brute force vulnerability

### File to Modify: core_modules/users/services.py

**Add to authentication function** (around line 40):

```python
from django.utils import timezone
from datetime import timedelta

def authenticate_user(email, password):
    """Authenticate user with account lockout protection."""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal if user exists
        return None
    
    # Check if account is locked
    if user.account_locked_until:
        if user.account_locked_until > timezone.now():
            # Account still locked
            raise AccountLockedException(
                f"Account locked until {user.account_locked_until}. "
                f"Please try again later or contact support."
            )
        else:
            # Lock period expired, reset
            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.save(update_fields=['failed_login_attempts', 'account_locked_until'])
    
    # Verify password
    if not user.check_password(password):
        # Increment failed attempts
        user.failed_login_attempts += 1
        user.last_failed_login = timezone.now()
        
        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.account_locked_until = timezone.now() + timedelta(minutes=15)
            user.save(update_fields=['failed_login_attempts', 'last_failed_login', 'account_locked_until'])
            raise AccountLockedException(
                "Account locked due to too many failed login attempts. "
                "Please try again in 15 minutes or contact support."
            )
        
        user.save(update_fields=['failed_login_attempts', 'last_failed_login'])
        return None
    
    # Successful login - reset failed attempts
    if user.failed_login_attempts > 0:
        user.failed_login_attempts = 0
        user.last_failed_login = None
        user.account_locked_until = None
        user.save(update_fields=['failed_login_attempts', 'last_failed_login', 'account_locked_until'])
    
    return user


class AccountLockedException(Exception):
    """Raised when account is locked due to failed login attempts."""
    pass
```

### Testing Strategy
1. Test 4 failed logins (should not lock)
2. Test 5 failed logins (should lock for 15 minutes)
3. Test login during lock period (should fail)
4. Test login after 15 minutes (should succeed and reset)
5. Test successful login resets counter

### Verification
```python
# Test script
from core_modules.users.services import authenticate_user
from core_modules.users.models import User

user = User.objects.get(email='test@example.com')
print(f"Failed attempts: {user.failed_login_attempts}")
print(f"Locked until: {user.account_locked_until}")
```

---

## FIX #4: FORCE HTTPS IN PRODUCTION ⚠️ HIGH

**Priority**: P0
**Estimated Time**: 1 hour
**Risk**: MEDIUM - Insecure connections possible

### File to Modify: gaara_erp/gaara_erp/settings/prod.py

**Add/Modify**:
```python
# Force HTTPS in production - NO OVERRIDE
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secure cookies - NO OVERRIDE
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Testing Strategy
1. Test HTTP request redirects to HTTPS
2. Verify HSTS header present
3. Verify cookies have Secure flag
4. Test in staging environment first

---

## FIX #5: VERIFY MIDDLEWARE CONFIGURATION ⚠️ MEDIUM

**Priority**: P0
**Estimated Time**: 1 hour
**Risk**: MEDIUM - Security features may not be active

### File to Check: gaara_erp/gaara_erp/settings/base.py

**Verify MIDDLEWARE includes**:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'gaara_erp.middleware.security_headers.SecurityHeadersMiddleware',  # ✅ Verify present
    'core_modules.security.middleware.RateLimitMiddleware',             # ✅ Verify present
    'django.middleware.csrf.CsrfViewMiddleware',                        # ✅ Verify present
    # ... other middleware
]
```

### Testing Strategy
1. Verify middleware order
2. Test rate limiting (5 login attempts)
3. Test CSRF protection
4. Test security headers (HSTS, CSP, X-Frame-Options)

---

## EXECUTION ORDER

1. **FIX #1**: Remove hardcoded secrets (1 hour) ← START HERE
2. **FIX #2**: Consolidate JWT config (2 hours)
3. **FIX #3**: Implement account lockout (3 hours)
4. **FIX #4**: Force HTTPS (1 hour)
5. **FIX #5**: Verify middleware (1 hour)

**Total Time**: 8 hours (sequential)

---

## POST-FIX VERIFICATION CHECKLIST

- [ ] No hardcoded secrets in codebase
- [ ] JWT tokens expire in 15 minutes
- [ ] Refresh tokens expire in 7 days
- [ ] Refresh tokens rotate on use
- [ ] Account locks after 5 failed attempts
- [ ] Account auto-unlocks after 15 minutes
- [ ] HTTPS enforced in production
- [ ] All security middleware active
- [ ] All tests pass
- [ ] Security scan clean

---

**Next Steps**: Begin execution of Fix #1

