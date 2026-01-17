# FILE: docs/P0_Security_Phase5_Plan.md | PURPOSE: Phase 5 Execution Plan | OWNER: Security Team | RELATED: P0_Security_Fix_Plan.md | LAST-AUDITED: 2025-11-19

# Phase 5: Infrastructure - Execution Plan

**Priority**: P0  
**Estimated Time**: 2 hours  
**Tasks**: 3  
**Status**: ⏳ PENDING

---

## Overview

Phase 5 focuses on verifying and configuring the infrastructure layer:
- Middleware configuration and order
- Structured logging setup
- Monitoring and alerting

**Goal**: Ensure all security infrastructure is properly configured and operational.

---

## Task 1: Verify Middleware Configuration ⚠️ CRITICAL

**Priority**: P0  
**Estimated Time**: 45 minutes  
**Risk**: HIGH - Incorrect middleware order can bypass security

### 1.1 Middleware Order Verification

**File**: `gaara_erp/gaara_erp/settings/base.py` (Lines 207-221)

**Required Order** (Security-First):
```python
MIDDLEWARE = [
    "middleware.CorsMiddleware",                                    # 1. CORS (handle preflight)
    "django.middleware.security.SecurityMiddleware",                # 2. Django Security
    "gaara_erp.middleware.security_headers.SecurityHeadersMiddleware",  # 3. Security Headers
    "middleware.WhiteNoiseMiddleware",                              # 4. Static files
    "django.contrib.sessions.middleware.SessionMiddleware",         # 5. Sessions
    "django.middleware.common.CommonMiddleware",                    # 6. Common
    "django.middleware.csrf.CsrfViewMiddleware",                    # 7. CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",      # 8. Auth
    "django.contrib.messages.middleware.MessageMiddleware",         # 9. Messages
    "django.middleware.clickjacking.XFrameOptionsMiddleware",       # 10. Clickjacking
    "core_modules.security.middleware.SecurityMiddleware",          # 11. Custom Security
    "core_modules.security.middleware.RateLimitMiddleware",         # 12. Rate Limiting
    "core_modules.security.middleware.ActivityLogMiddleware",       # 13. Activity Logging
]
```

**Verification Steps**:
1. Check middleware order matches security-first pattern
2. Verify all security middleware are present
3. Verify no middleware are disabled
4. Test middleware chain with sample request

### 1.2 Middleware Functionality Verification

**SecurityHeadersMiddleware** (`gaara_erp/middleware/security_headers.py`):
- ✅ Adds HSTS header (Strict-Transport-Security)
- ✅ Adds X-Content-Type-Options: nosniff
- ✅ Adds Referrer-Policy
- ✅ Adds Cross-Origin-Opener-Policy
- ✅ Adds Cross-Origin-Embedder-Policy
- ✅ Adds Permissions-Policy

**SecurityMiddleware** (`core_modules/security/middleware.py`):
- ✅ IP blacklist checking
- ✅ Security info injection (IP, user agent, timestamp)
- ✅ Additional security headers (X-Frame-Options, X-XSS-Protection, CSP)

**RateLimitMiddleware** (`core_modules/security/middleware.py`):
- ✅ Rate limiting per IP/user
- ✅ Configurable limits
- ✅ Redis-backed (if available)

**ActivityLogMiddleware** (`core_modules/security/middleware.py`):
- ✅ Logs all requests
- ✅ Logs user actions
- ✅ Logs security events

### 1.3 Success Criteria

- [x] Middleware order is correct (security-first)
- [x] All security middleware are present
- [x] SecurityHeadersMiddleware adds all required headers
- [x] SecurityMiddleware blocks blacklisted IPs
- [x] RateLimitMiddleware enforces limits
- [x] ActivityLogMiddleware logs requests

---

## Task 2: Configure Structured Logging ⚠️ CRITICAL

**Priority**: P0  
**Estimated Time**: 45 minutes  
**Risk**: MEDIUM - Poor logging hinders incident response

### 2.1 Logging Configuration

**File**: `gaara_erp/gaara_erp/settings/base.py` or `gaara_erp/gaara_erp/settings/logging.py` (create if needed)

**Required Configuration**:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/info.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'json',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'json',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 30,  # Keep 30 days
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
        'core_modules.security': {
            'handlers': ['file_security'],
            'level': 'INFO',
            'propagate': False,
        },
        'gaara_erp': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 2.2 Log Directories

**Create**:
- `logs/` directory in project root
- `.gitignore` entry for `logs/*.log`

### 2.3 Success Criteria

- [x] JSON logging configured
- [x] Separate log files (info, error, security)
- [x] Log rotation enabled (10MB, 10 backups)
- [x] Security events logged to security.log
- [x] logs/ directory created
- [x] logs/*.log in .gitignore

---

## Task 3: Set Up Monitoring and Alerting ⚠️ CRITICAL

**Priority**: P0
**Estimated Time**: 30 minutes
**Risk**: MEDIUM - No monitoring = blind to attacks

### 3.1 Health Check Endpoint

**File**: Create `gaara_erp/core_modules/health/views.py`

**Implementation**:
```python
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import time

def health_check(request):
    """Health check endpoint for load balancers and monitoring."""
    start_time = time.time()
    checks = {}

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'

    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            checks['cache'] = 'ok'
        else:
            checks['cache'] = 'error: cache read failed'
    except Exception as e:
        checks['cache'] = f'error: {str(e)}'

    # Response time
    response_time = (time.time() - start_time) * 1000  # ms
    checks['response_time_ms'] = round(response_time, 2)

    # Overall status
    all_ok = all(v == 'ok' or isinstance(v, (int, float)) for v in checks.values())
    status_code = 200 if all_ok else 503

    return JsonResponse({
        'status': 'healthy' if all_ok else 'unhealthy',
        'checks': checks,
        'timestamp': time.time()
    }, status=status_code)
```

### 3.2 Success Criteria

- [ ] /health/ endpoint created
- [ ] Health check tests database connectivity
- [ ] Health check tests cache connectivity
- [ ] Monitoring service verified
- [ ] Celery beat task configured

---

## Phase 5 Summary

### Tasks Overview

| Task | Description | Priority | Time | Files |
|------|-------------|----------|------|-------|
| **Task 1** | Verify middleware configuration | P0 | 45 min | 1 file (verify) |
| **Task 2** | Configure structured logging | P0 | 45 min | 1-2 files |
| **Task 3** | Set up monitoring | P0 | 30 min | 2-3 files |
| **TOTAL** | **Phase 5 Complete** | **P0** | **2 hours** | **~5 files** |

### Expected Outcomes

**Infrastructure Improvements**:
- ✅ Middleware properly ordered (security-first)
- ✅ Structured JSON logging
- ✅ Separate log files (info, error, security)
- ✅ Health check endpoint
- ✅ System monitoring active

**OSF Score Impact**:
- **Before Phase 5**: 0.95
- **After Phase 5**: 0.96 (estimated)
- **Reliability Dimension**: 0.92 → 0.95

---

**End of Phase 5 Execution Plan**

