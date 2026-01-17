# FILE: docs/P0_Security_Phase3_Plan.md | PURPOSE: Phase 3 Execution Plan | OWNER: Security Team | RELATED: P0_Security_Fix_Plan.md | LAST-AUDITED: 2025-11-19

# Phase 3: HTTPS & Security Headers - Execution Plan

**Start Date**: 2025-11-19  
**Estimated Time**: 2 hours  
**Priority**: P0 (CRITICAL)  
**Status**: ⏳ IN PROGRESS

---

## Overview

Phase 3 focuses on enforcing HTTPS in production and configuring comprehensive security headers to protect against common web vulnerabilities.

**Total Tasks**: 3  
**Estimated Time**: 2 hours  
**OSF Priority**: Security (35%)

---

## Task 1: Enforce HTTPS in Production ⚠️ HIGH

**Priority**: P0  
**Estimated Time**: 45 minutes  
**Risk**: MEDIUM - Insecure connections possible without HTTPS

### Objectives

1. ✅ Force HTTPS redirect in production (HTTP → HTTPS)
2. ✅ Configure secure proxy headers
3. ✅ Enable HSTS (HTTP Strict Transport Security)
4. ✅ Secure all cookies (SESSION, CSRF)

### Files to Modify

#### 1.1 `gaara_erp/gaara_erp/settings/prod.py`

**Changes Required**:

```python
# HTTPS Enforcement
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # For reverse proxy

# Secure Cookies
SESSION_COOKIE_SECURE = True  # Only send session cookie over HTTPS
CSRF_COOKIE_SECURE = True     # Only send CSRF cookie over HTTPS

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year (recommended)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow browser preload list inclusion
```

### Testing Strategy

1. ✅ Test HTTP request redirects to HTTPS (301/302)
2. ✅ Verify HSTS header present in response
3. ✅ Verify cookies have `Secure` flag set
4. ✅ Test in staging environment first
5. ✅ Verify no mixed content warnings

### Verification Commands

```bash
# Test HTTPS redirect
curl -I http://your-domain.com

# Verify HSTS header
curl -I https://your-domain.com | grep -i "strict-transport-security"

# Check cookie flags
# Use browser DevTools → Application → Cookies
```

### Success Criteria

- ✅ All HTTP requests redirect to HTTPS
- ✅ HSTS header present with 1-year max-age
- ✅ All cookies have Secure flag
- ✅ No mixed content errors

---

## Task 2: Configure Security Headers ⚠️ HIGH

**Priority**: P0  
**Estimated Time**: 45 minutes  
**Risk**: HIGH - Missing headers expose to XSS, clickjacking, MIME sniffing

### Objectives

1. ✅ Configure Content Security Policy (CSP)
2. ✅ Enable X-Frame-Options (clickjacking protection)
3. ✅ Enable X-Content-Type-Options (MIME sniffing protection)
4. ✅ Configure Referrer-Policy
5. ✅ Configure Permissions-Policy

### Files to Modify

#### 2.1 `gaara_erp/gaara_erp/settings/security.py`

**Add/Modify Security Headers**:

```python
# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # TODO: Remove unsafe-inline, use nonces
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")   # TODO: Remove unsafe-inline, use nonces
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # Prevent clickjacking
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)

# X-Frame-Options (Clickjacking Protection)
X_FRAME_OPTIONS = 'DENY'  # Prevent embedding in iframes

# X-Content-Type-Options (MIME Sniffing Protection)
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer Policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Permissions Policy (formerly Feature Policy)
PERMISSIONS_POLICY = {
    'geolocation': [],
    'microphone': [],
    'camera': [],
    'payment': [],
    'usb': [],
}
```

#### 2.2 Verify `gaara_erp/middleware/security_headers.py` exists

**Check if SecurityHeadersMiddleware is implemented**:

```python
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # CSP header
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        return response
```

### Testing Strategy

1. ✅ Verify all headers present in HTTP response
2. ✅ Test CSP blocks unauthorized scripts
3. ✅ Test X-Frame-Options prevents iframe embedding
4. ✅ Use security header scanner (securityheaders.com)

### Verification Commands

```bash
# Check all security headers
curl -I https://your-domain.com

# Expected headers:
# Content-Security-Policy: ...
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# Referrer-Policy: strict-origin-when-cross-origin
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### Success Criteria

- ✅ CSP header present and configured
- ✅ X-Frame-Options: DENY
- ✅ X-Content-Type-Options: nosniff
- ✅ Referrer-Policy configured
- ✅ Security headers score A+ on securityheaders.com

---

## Task 3: Update CORS Settings ⚠️ MEDIUM

**Priority**: P0  
**Estimated Time**: 30 minutes  
**Risk**: MEDIUM - Overly permissive CORS allows unauthorized access

### Objectives

1. ✅ Whitelist only trusted origins
2. ✅ Disable CORS_ALLOW_ALL_ORIGINS
3. ✅ Configure allowed methods and headers
4. ✅ Enable credentials support

### Files to Modify

#### 3.1 `gaara_erp/gaara_erp/settings/base.py` or `security.py`

**Current (Insecure)**:
```python
CORS_ALLOW_ALL_ORIGINS = True  # ❌ INSECURE - Allows any origin
```

**Updated (Secure)**:
```python
# CORS Configuration - Whitelist Only
CORS_ALLOW_ALL_ORIGINS = False  # ✅ Disable wildcard

# Whitelist trusted origins
CORS_ALLOWED_ORIGINS = [
    "https://app.gaara-erp.com",
    "https://admin.gaara-erp.com",
    # Add staging/dev origins from environment
]

# For development only
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
    ]

# Allowed methods
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# Allowed headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# Preflight cache (1 hour)
CORS_PREFLIGHT_MAX_AGE = 3600
```

### Testing Strategy

1. ✅ Test request from allowed origin succeeds
2. ✅ Test request from disallowed origin fails (CORS error)
3. ✅ Verify preflight OPTIONS requests work
4. ✅ Test credentials (cookies) sent with CORS requests

### Verification Commands

```bash
# Test CORS from allowed origin
curl -H "Origin: https://app.gaara-erp.com" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://api.gaara-erp.com/api/auth/login

# Expected response headers:
# Access-Control-Allow-Origin: https://app.gaara-erp.com
# Access-Control-Allow-Credentials: true
# Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS

# Test CORS from disallowed origin (should fail)
curl -H "Origin: https://evil.com" \
     -X OPTIONS \
     https://api.gaara-erp.com/api/auth/login

# Expected: No Access-Control-Allow-Origin header
```

### Success Criteria

- ✅ CORS_ALLOW_ALL_ORIGINS = False
- ✅ Only whitelisted origins allowed
- ✅ Credentials support enabled
- ✅ Preflight requests work correctly
- ✅ Unauthorized origins blocked

---

## Execution Order

**Sequential Execution**:

1. **Task 1**: Enforce HTTPS (45 min) ← START HERE
2. **Task 2**: Configure Security Headers (45 min)
3. **Task 3**: Update CORS Settings (30 min)

**Total Time**: 2 hours

---

## OSF Framework Compliance

### Target OSF Score: 0.93

| Dimension | Target Score | Weight | Contribution |
|-----------|-------------|--------|--------------|
| Security | 0.96 | 35% | 0.3360 |
| Correctness | 0.93 | 20% | 0.1860 |
| Reliability | 0.90 | 15% | 0.1350 |
| Maintainability | 0.88 | 10% | 0.0880 |
| Performance | 0.92 | 8% | 0.0736 |
| Usability | 0.90 | 7% | 0.0630 |
| Scalability | 0.93 | 5% | 0.0465 |
| **TOTAL** | **0.93** | **100%** | **0.9281** |

**Maturity Level**: Level 4 - Optimizing

---

## Post-Phase Verification Checklist

### HTTPS Enforcement
- [ ] HTTP requests redirect to HTTPS (301/302)
- [ ] HSTS header present (max-age=31536000)
- [ ] HSTS includes subdomains
- [ ] HSTS preload enabled
- [ ] All cookies have Secure flag
- [ ] No mixed content warnings

### Security Headers
- [ ] Content-Security-Policy header present
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy configured
- [ ] Permissions-Policy configured
- [ ] Security headers score A+ on securityheaders.com

### CORS Configuration
- [ ] CORS_ALLOW_ALL_ORIGINS = False
- [ ] Only whitelisted origins in CORS_ALLOWED_ORIGINS
- [ ] CORS_ALLOW_CREDENTIALS = True
- [ ] Preflight requests work
- [ ] Unauthorized origins blocked

### Testing
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Security scan clean
- [ ] Manual testing in staging

---

## Risk Mitigation

### Potential Issues

1. **HTTPS Redirect Loop**
   - **Risk**: Misconfigured proxy headers cause redirect loop
   - **Mitigation**: Test SECURE_PROXY_SSL_HEADER with actual proxy setup
   - **Rollback**: Set SECURE_SSL_REDIRECT = False temporarily

2. **CSP Blocks Legitimate Resources**
   - **Risk**: Overly strict CSP breaks frontend functionality
   - **Mitigation**: Start with report-only mode, monitor violations
   - **Rollback**: Relax CSP directives if needed

3. **CORS Blocks Legitimate Clients**
   - **Risk**: Missing origins in whitelist
   - **Mitigation**: Comprehensive testing with all client apps
   - **Rollback**: Temporarily add missing origins

### Rollback Plan

If critical issues arise:

1. **Immediate**: Revert settings file changes
2. **Restart**: Application server
3. **Verify**: Service restored
4. **Analyze**: Root cause
5. **Fix**: Address issue
6. **Redeploy**: With fix

---

## Documentation Updates

### Files to Update

1. ✅ `docs/Security.md` - Add HTTPS and security headers section
2. ✅ `docs/P0_Security_Phase3_Progress.md` - Track task progress
3. ✅ `docs/P0_Security_Phase3_COMPLETE.md` - Final report
4. ✅ `docs/P0_Security_Fixes_Status_Report.md` - Update overall status

---

## Success Metrics

### Security Improvements

**Before Phase 3**:
- ❌ HTTP allowed in production
- ❌ No HSTS
- ❌ Missing security headers
- ❌ CORS allows all origins

**After Phase 3**:
- ✅ HTTPS enforced (HTTP → HTTPS redirect)
- ✅ HSTS enabled (1-year max-age)
- ✅ All security headers configured
- ✅ CORS whitelist only

### OSF Score Progress

```
Before:  0.65 ████████░░░░░░░░░░░░ (65%)
Phase 1: 0.89 █████████████████░░░ (89%)
Phase 2: 0.92 ██████████████████░░ (92%)
Phase 3: 0.93 ██████████████████░░ (93%) ← TARGET
Target:  0.95 ███████████████████░ (95%)
```

---

**Status**: ⏳ Ready to begin Task 1
**Next Step**: Modify `gaara_erp/gaara_erp/settings/prod.py` to enforce HTTPS


