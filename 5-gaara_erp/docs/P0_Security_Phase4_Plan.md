# FILE: docs/P0_Security_Phase4_Plan.md | PURPOSE: Phase 4 Execution Plan | OWNER: Security Team | RELATED: P0_Security_Fix_Plan.md | LAST-AUDITED: 2025-11-19

# Phase 4: Secrets & Validation - Execution Plan

**Start Date**: 2025-11-19  
**Estimated Time**: 3 hours  
**Priority**: P0 (CRITICAL)  
**Status**: 🔄 IN PROGRESS

---

## Overview

Phase 4 focuses on removing hardcoded secrets, consolidating JWT configuration, implementing input validation, and adding secret scanning to CI/CD.

**Total Tasks**: 4  
**Estimated Time**: 3 hours  
**Files to Modify**: ~6 files  
**Files to Create**: ~2 files

---

## Task 1: Remove Hardcoded Secrets ⚠️ CRITICAL

**Priority**: P0 (HIGHEST)  
**Estimated Time**: 45 minutes  
**Risk**: CRITICAL - Exposed secrets in code

### 1.1 Files to Modify

#### A) api_gateway/main.py (2 occurrences)

**Current Issues**:
- Line 62: `jwt.decode(token, "secret_key", algorithms=["HS256"])`
- Line 162: `jwt.encode({"user_id": 1, "username": username}, "secret_key", algorithm="HS256")`

**Required Changes**:
```python
import os
from decouple import config

# At module level
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set")

# Line 62 - AFTER
payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])

# Line 162 - AFTER
token = jwt.encode({"user_id": 1, "username": username}, JWT_SECRET_KEY, algorithm="HS256")
```

#### B) gaara_erp/gaara_erp/settings/base.py

**Current Issue**:
- Line 13: `SECRET_KEY = config("SECRET_KEY", default="942ec766e095b238e40f36dfc3fe24bca61f151e394bf6d4fd1e4c4a54e4d418b01166d3762621a7eefe1b7fcf6fdc77e120")`

**Required Change**:
```python
# Line 13 - AFTER (no default - must be set in environment)
SECRET_KEY = config("SECRET_KEY")
```

### 1.2 Verification Steps

1. **Scan for hardcoded secrets**:
   ```bash
   grep -r "secret_key" gaara_erp/ --include="*.py" | grep -v ".env"
   grep -r "SECRET_KEY.*=" gaara_erp/ --include="*.py" | grep "default="
   ```

2. **Test application startup**:
   - Without `SECRET_KEY` in `.env` → should fail with clear error
   - With `SECRET_KEY` in `.env` → should start successfully

3. **Test JWT operations**:
   - Token generation should work
   - Token verification should work
   - Invalid tokens should be rejected

### 1.3 Success Criteria

✅ No hardcoded secrets in code  
✅ Application fails to start without required secrets  
✅ JWT operations work with environment variables  
✅ Security scan shows no hardcoded secrets  

---

## Task 2: Consolidate JWT Configuration ⚠️ CRITICAL

**Priority**: P0  
**Estimated Time**: 1 hour  
**Risk**: HIGH - Conflicting configurations

### 2.1 Decision: Single Source of Truth

**Use**: `gaara_erp/gaara_erp/settings/security.py` as the ONLY JWT configuration

### 2.2 Files to Modify

#### A) gaara_erp/gaara_erp/settings/security.py

**Current Configuration** (Lines 99-120):
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # ❌ Too long
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # ❌ Too short
    # ... rest of config
}
```

**Required Changes**:
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

#### B) admin_modules/custom_admin/jwt_config.py

**Action**: DELETE or DEPRECATE this file

**Reason**: Conflicts with `settings/security.py`

**Alternative** (if needed):
```python
# admin_modules/custom_admin/jwt_config.py
from gaara_erp.settings.security import SIMPLE_JWT as JWT_SETTINGS

# DEPRECATED: Import from settings/security.py instead
# This file is kept for backward compatibility only
```

#### C) gaara_erp/gaara_erp/settings/security_enhanced.py

**Lines 197-198** - DELETE or COMMENT OUT:
```python
# DEPRECATED - Use SIMPLE_JWT in settings/security.py instead
# 'JWT_EXPIRATION_DELTA': int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', '3600')),
```

### 2.3 Verification Steps

1. **Find all JWT configurations**:
   ```bash
   grep -r "ACCESS_TOKEN_LIFETIME" gaara_erp/ --include="*.py"
   grep -r "JWT_EXPIRATION_DELTA" gaara_erp/ --include="*.py"
   ```

2. **Test token generation**:
   - Generate access token → should expire in 15 minutes
   - Generate refresh token → should expire in 7 days

3. **Test token rotation**:
   - Use refresh token → should get new access + refresh tokens
   - Old refresh token → should be blacklisted

4. **Test token expiry**:
   - Wait 16 minutes → access token should be invalid (401)
   - Use refresh token → should get new access token

### 2.4 Success Criteria

✅ Only one JWT configuration active (`settings/security.py`)  
✅ Access token expires in 15 minutes  
✅ Refresh token expires in 7 days  
✅ Token rotation works correctly  
✅ Old tokens are blacklisted after rotation

---

## Task 3: Implement Input Validation ⚠️ HIGH

**Priority**: P0
**Estimated Time**: 1 hour
**Risk**: HIGH - SQL injection, XSS vulnerabilities

### 3.1 Strategy

**Use Django REST Framework Serializers** for all API input validation.

### 3.2 Files to Create/Modify

#### A) Create: gaara_erp/core_modules/core/validators.py

**Purpose**: Centralized validation utilities

```python
# FILE: gaara_erp/core_modules/core/validators.py
"""
Centralized input validation utilities.
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_no_sql_injection(value):
    """
    Validate that input doesn't contain SQL injection patterns.

    This is a defense-in-depth measure. Primary protection is parameterized queries.
    """
    sql_patterns = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bSELECT\b.*\bFROM\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bUPDATE\b.*\bSET\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(--|\#|\/\*|\*\/)",  # SQL comments
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, str(value), re.IGNORECASE):
            raise ValidationError(
                _("Invalid input detected. Please remove special SQL characters."),
                code='sql_injection'
            )


def validate_no_xss(value):
    """
    Validate that input doesn't contain XSS patterns.

    This is a defense-in-depth measure. Primary protection is output escaping.
    """
    xss_patterns = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",  # Event handlers (onclick, onerror, etc.)
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
    ]

    for pattern in xss_patterns:
        if re.search(pattern, str(value), re.IGNORECASE):
            raise ValidationError(
                _("Invalid input detected. Please remove HTML/JavaScript code."),
                code='xss_attempt'
            )


def validate_safe_filename(value):
    """
    Validate that filename is safe (no path traversal).
    """
    if '..' in value or '/' in value or '\\' in value:
        raise ValidationError(
            _("Invalid filename. Path traversal not allowed."),
            code='path_traversal'
        )

    # Only allow alphanumeric, dash, underscore, and dot
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', value):
        raise ValidationError(
            _("Filename contains invalid characters."),
            code='invalid_filename'
        )
```

#### B) Modify: All ViewSets to use Serializer Validation

**Example Pattern** (apply to all ViewSets):

```python
from rest_framework import serializers
from .validators import validate_no_sql_injection, validate_no_xss

class UserSerializer(serializers.ModelSerializer):
    """User serializer with input validation."""

    email = serializers.EmailField(
        required=True,
        validators=[validate_no_xss]
    )

    username = serializers.CharField(
        max_length=150,
        validators=[validate_no_sql_injection, validate_no_xss]
    )

    first_name = serializers.CharField(
        max_length=150,
        validators=[validate_no_xss]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']

    def validate(self, attrs):
        """Additional validation logic."""
        # Custom validation here
        return attrs
```

### 3.3 Verification Steps

1. **Test SQL injection patterns**:
   ```python
   # Should be rejected
   POST /api/users/ {"username": "admin' OR '1'='1"}
   POST /api/users/ {"username": "admin'; DROP TABLE users;--"}
   ```

2. **Test XSS patterns**:
   ```python
   # Should be rejected
   POST /api/users/ {"first_name": "<script>alert('XSS')</script>"}
   POST /api/users/ {"first_name": "<img src=x onerror=alert('XSS')>"}
   ```

3. **Test path traversal**:
   ```python
   # Should be rejected
   POST /api/files/ {"filename": "../../../etc/passwd"}
   POST /api/files/ {"filename": "..\\..\\windows\\system32"}
   ```

### 3.4 Success Criteria

✅ Centralized validators created
✅ All serializers use validators
✅ SQL injection patterns rejected
✅ XSS patterns rejected
✅ Path traversal patterns rejected
✅ Valid input accepted

---

## Task 4: Add Secret Scanning to CI/CD ⚠️ MEDIUM

**Priority**: P0
**Estimated Time**: 15 minutes
**Risk**: MEDIUM - Prevent future secret leaks

### 4.1 Tool Selection

**Use**: `detect-secrets` (Yelp's secret scanner)

### 4.2 Files to Create

#### A) .secrets.baseline

**Purpose**: Baseline file for known false positives

```bash
# Generate baseline
detect-secrets scan > .secrets.baseline
```

#### B) .github/workflows/security-scan.yml (if using GitHub Actions)

```yaml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install detect-secrets
        run: pip install detect-secrets

      - name: Scan for secrets
        run: |
          detect-secrets scan --baseline .secrets.baseline
          if [ $? -ne 0 ]; then
            echo "❌ Secrets detected! Please remove them before committing."
            exit 1
          fi

      - name: Verify no hardcoded secrets
        run: |
          # Check for common secret patterns
          if grep -r "secret_key.*=.*['\"]" gaara_erp/ --include="*.py" | grep -v ".env"; then
            echo "❌ Hardcoded secrets found!"
            exit 1
          fi
```

### 4.3 Pre-commit Hook (Optional)

**File**: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Pre-commit hook to scan for secrets

echo "🔍 Scanning for secrets..."
detect-secrets scan --baseline .secrets.baseline

if [ $? -ne 0 ]; then
    echo "❌ Secrets detected! Commit blocked."
    echo "Please remove secrets or update .secrets.baseline if false positive."
    exit 1
fi

echo "✅ No secrets detected."
exit 0
```

### 4.4 Success Criteria

✅ `detect-secrets` installed
✅ `.secrets.baseline` created
✅ CI/CD pipeline includes secret scanning
✅ Pre-commit hook configured (optional)
✅ Test: commit with secret → blocked
✅ Test: commit without secret → allowed

---

## Phase 4 Summary

### Tasks Overview

| Task | Description | Priority | Time | Files |
|------|-------------|----------|------|-------|
| **Task 1** | Remove hardcoded secrets | P0 | 45 min | 2 files |
| **Task 2** | Consolidate JWT config | P0 | 1 hour | 3 files |
| **Task 3** | Implement input validation | P0 | 1 hour | 1 new + multiple |
| **Task 4** | Add secret scanning | P0 | 15 min | 2 files |
| **TOTAL** | **Phase 4 Complete** | **P0** | **3 hours** | **~8 files** |

### Expected Outcomes

**Security Improvements**:
- ✅ No hardcoded secrets in code
- ✅ Single JWT configuration (no conflicts)
- ✅ Input validation on all API endpoints
- ✅ Automated secret scanning in CI/CD

**OSF Score Impact**:
- **Before Phase 4**: 0.93
- **After Phase 4**: 0.94 (estimated)
- **Security Dimension**: 0.96 → 0.98

### Files to Modify/Create

**Modified**:
1. `api_gateway/main.py`
2. `gaara_erp/gaara_erp/settings/base.py`
3. `gaara_erp/gaara_erp/settings/security.py`
4. `admin_modules/custom_admin/jwt_config.py` (deprecate)
5. `gaara_erp/gaara_erp/settings/security_enhanced.py`

**Created**:
1. `gaara_erp/core_modules/core/validators.py`
2. `.secrets.baseline`
3. `.github/workflows/security-scan.yml` (optional)

---

## Next Steps

After Phase 4 completion:

**Phase 5: Infrastructure** (3 tasks, ~2 hours)
1. Verify middleware configuration
2. Configure logging
3. Set up monitoring

**Target**: Complete all 23 P0 tasks and achieve OSF Score ≥ 0.95

---

**End of Phase 4 Execution Plan**


