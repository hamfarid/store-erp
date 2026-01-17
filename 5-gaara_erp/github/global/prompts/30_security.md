# SECURITY SCANNING PROMPT

**FILE**: github/global/prompts/30_security.md | **PURPOSE**: Security scanning and hardening | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 5: Review & Refinement - Security

This prompt guides you through comprehensive security scanning and hardening.

## Pre-Execution Checklist

- [ ] Code implementation complete
- [ ] All dependencies installed
- [ ] Environment variables configured

## Security Checklist

### 1. Secrets Management

**Check**: No hardcoded secrets in code

```bash
# Search for potential secrets
grep -r "password\s*=\s*['\"]" --include="*.py" --include="*.ts" --include="*.js"
grep -r "api_key\s*=\s*['\"]" --include="*.py" --include="*.ts" --include="*.js"
grep -r "secret\s*=\s*['\"]" --include="*.py" --include="*.ts" --include="*.js"
```

**Fix**: Move all secrets to environment variables

### 2. SQL Injection Prevention

**Check**: All database queries use parameterized queries

```python
# BAD
query = f"SELECT * FROM users WHERE email = '{email}'"

# GOOD
query = "SELECT * FROM users WHERE email = :email"
db.execute(query, {"email": email})
```

**Scan**: Use static analysis tools

```bash
# Python
bandit -r backend/

# JavaScript/TypeScript
npm audit
```

### 3. XSS Prevention

**Check**: All user input is sanitized

```typescript
// BAD
element.innerHTML = userInput;

// GOOD
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

**CSP**: Content Security Policy headers configured

```python
# FastAPI example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 4. Authentication & Authorization

**Check**: All protected routes require authentication

```python
# FastAPI example
from fastapi import Depends
from middleware.auth import verify_token

@router.get("/api/users")
async def get_users(user = Depends(verify_token)):
    # Only authenticated users can access
    pass
```

**Check**: RBAC implemented correctly

```python
def require_role(required_role: str):
    def decorator(func):
        async def wrapper(*args, user = Depends(verify_token), **kwargs):
            if user['role'] != required_role:
                raise HTTPException(status_code=403, detail="Forbidden")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@router.delete("/api/users/{id}")
@require_role("admin")
async def delete_user(id: str):
    # Only admins can delete users
    pass
```

### 5. Password Security

**Check**: Passwords are hashed with bcrypt/argon2

```python
import bcrypt

# Hash password
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

# Verify password
bcrypt.checkpw(password.encode('utf-8'), hashed)
```

**Check**: Password policy enforced

```python
import re

def validate_password(password: str) -> bool:
    """
    Password must be:
    - At least 12 characters
    - Contains uppercase, lowercase, number, and symbol
    """
    if len(password) < 12:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'[0-9]', password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True
```

### 6. HTTPS Enforcement

**Check**: All HTTP requests redirect to HTTPS

```python
# FastAPI example
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

### 7. Rate Limiting

**Check**: Rate limiting implemented

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/users")
@limiter.limit("100/minute")
async def get_users():
    pass
```

### 8. CORS Configuration

**Check**: CORS is properly configured (not `*`)

```python
# BAD
allow_origins=["*"]

# GOOD
allow_origins=["https://yourdomain.com", "https://app.yourdomain.com"]
```

### 9. Dependency Vulnerabilities

**Scan**: Check for known vulnerabilities

```bash
# Python
pip install safety
safety check

# JavaScript
npm audit
npm audit fix
```

### 10. Security Headers

**Check**: All security headers are set

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

## Automated Security Scanning

### SAST (Static Application Security Testing)

```bash
# Python
bandit -r backend/ -f json -o security_report.json

# JavaScript/TypeScript
npm install -g eslint-plugin-security
eslint --plugin security frontend/src/
```

### DAST (Dynamic Application Security Testing)

```bash
# OWASP ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:3000
```

### Dependency Scanning

```bash
# Snyk
npm install -g snyk
snyk test
snyk monitor
```

### Secret Scanning

```bash
# TruffleHog
docker run --rm -v $(pwd):/proj dxa4481/trufflehog file:///proj
```

## Security Report

Create `docs/SECURITY_REPORT.md`:

```markdown
# Security Report

**Generated**: [Date]

## Summary

- **Critical Issues**: [Count]
- **High Issues**: [Count]
- **Medium Issues**: [Count]
- **Low Issues**: [Count]

## Critical Issues (P0)

### 1. Hardcoded API Key
- **File**: `backend/config/settings.py`
- **Line**: 15
- **Issue**: API key hardcoded in source code
- **Fix**: Move to environment variable
- **Status**: Fixed

[Repeat for all critical issues]

## High Issues (P1)

[Same structure]

## Medium Issues (P2)

[Same structure]

## Low Issues (P3)

[Same structure]

## Compliance

- [ ] OWASP Top 10 addressed
- [ ] GDPR compliant (if applicable)
- [ ] HIPAA compliant (if applicable)
- [ ] SOC 2 controls implemented (if applicable)

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

---

**Next Steps**: Fix all P0 and P1 issues before deployment
```

## Log Actions

Log all security findings to `logs/info.log`

## Save to Memory

Save security report to `.memory/learnings/security_scan_[date].md`

---

**Completion Criteria**:
- [ ] All security checks performed
- [ ] All critical issues fixed
- [ ] All high issues fixed
- [ ] Security report generated
- [ ] Actions logged

