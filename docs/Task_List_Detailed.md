# Task List - Store Inventory System Hardening
## Generated from Global Guidelines v2.3 Analysis
## Date: 2025-10-25

---

## Priority Legend

- **P0**: Critical - Blocks production deployment
- **P1**: High - Required for compliance/security
- **P2**: Medium - Important for quality/resilience
- **P3**: Low - Nice-to-have enhancements

---

## Phase 0: Critical Security (Week 1-2)

### P0.1 - Fix SQL Injection Vulnerability
- **Priority**: P0
- **Owner**: Backend Lead
- **Estimate**: 4 hours
- **Dependencies**: None
- **Status**: Not Started

**Description**: Replace f-string SQL execution with parameterized query

**Files**:
- `backend/src/database.py` (line 172)

**Action**:
Replace:
```python
count = db.session.execute(f"SELECT COUNT(*) FROM {table_name}").scalar()
```

With:
```python
from sqlalchemy import text
count = db.session.execute(text("SELECT COUNT(*) FROM :table"), {"table": table_name}).scalar()
```

**Tests**:
- Negative test: Attempt SQL injection in table_name parameter
- Verify error handling for invalid table names

---

### P0.2 - Enforce bcrypt, Remove SHA-256 Fallback
- **Priority**: P0
- **Owner**: Backend Lead
- **Estimate**: 8 hours
- **Dependencies**: None
- **Status**: Not Started

**Description**: Eliminate weak password hashing fallback

**Files**:
- `backend/src/auth.py` (lines 76-92)
- `backend/src/models/user.py` (lines 119-120)

**Action**:
1. Remove all SHA-256 fallback code
2. Add startup check: raise exception if bcrypt unavailable
3. Update requirements.txt to pin bcrypt version
4. Add environment validation script

**Tests**:
- Unit test: Verify exception raised if bcrypt missing
- Integration test: Login with correct/incorrect passwords
- Load test: Hash 1000 passwords, verify performance

---

### P0.3 - HTTPS Enforcement + HSTS
- **Priority**: P0
- **Owner**: DevOps
- **Estimate**: 6 hours
- **Dependencies**: None
- **Status**: Not Started

**Description**: Enforce HTTPS in production with HSTS header

**Files**:
- `backend/app.py`
- `backend/.env` (add FORCE_HTTPS=true)
- `deployment/nginx.conf`

**Action**:
1. Add middleware to redirect HTTP → HTTPS
2. Set HSTS header: max-age=31536000; includeSubDomains
3. Configure Nginx to handle SSL termination
4. Update environment config

**Tests**:
- Integration test: Verify HTTP requests redirect to HTTPS
- Header test: Verify HSTS header present via curl -I
- Browser test: Check HSTS preload compatibility

---

### P0.4 - Global CSRF Middleware
- **Priority**: P0
- **Owner**: Backend Lead
- **Estimate**: 12 hours
- **Dependencies**: None
- **Status**: Not Started

**Description**: Enforce CSRF token validation on all state-changing endpoints

**Files**:
- `backend/src/middleware/csrf_middleware.py` (new)
- `backend/app.py`
- All POST/PUT/DELETE routes

**Action**:
1. Install Flask-WTF
2. Create global CSRF middleware
3. Apply to all non-GET requests
4. Update frontend to include CSRF token in headers

**Tests**:
- Integration test: POST without CSRF token → 403
- Integration test: POST with valid token → 200
- E2E test: Login flow with CSRF

---

### P0.5 - Rate Limiting (Flask-Limiter)
- **Priority**: P0
- **Owner**: Backend Lead
- **Estimate**: 8 hours
- **Dependencies**: None
- **Status**: Not Started

**Description**: Implement rate limiting to prevent brute force attacks

**Files**:
- `backend/app.py`
- `backend/src/middleware/rate_limiter.py` (new)

**Action**:
1. Install Flask-Limiter
2. Configure: 100 req/min global, 5 req/min on /auth/login
3. Use Redis for distributed rate limiting
4. Add custom error response

**Tests**:
- Load test: Send 101 requests in 1 min → verify 429
- Load test: 6 login attempts → verify lockout
- Integration test: Verify headers (X-RateLimit-*)

---

### P0.6 - Security Headers Suite
- **Priority**: P0
- **Owner**: Backend Lead
- **Estimate**: 6 hours
- **Dependencies**: None
- **Status**: Not Started

**Description**: Add comprehensive security headers

**Files**:
- `backend/src/middleware/security_headers.py` (new)

**Action**:
Add headers:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000
- Content-Security-Policy: (see P2.4)
- Referrer-Policy: strict-origin-when-cross-origin

**Tests**:
- Header scan: Verify all headers via curl -I
- Online scan: securityheaders.com → A+ rating

---

## Summary

**Total Tasks**: 23 (see full list in GLOBAL_GUIDELINES_ANALYSIS.md)
**Total Estimate**: 320 hours (8 weeks with 2 developers)

**Critical Path**: P0 tasks (Week 1-2) must complete before production deployment.

---

**Next Action**: Review with stakeholders, allocate resources, begin P0.1 immediately.
