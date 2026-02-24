# FILE: docs/Task_List_v2.3_Comprehensive.md | PURPOSE: Complete task breakdown following GLOBAL_GUIDELINES v2.3 | OWNER: System | RELATED: .augment/rules/All Project Rolls.md, .augment/rules/fix store project.md | LAST-AUDITED: 2025-10-25

# Task List — Arabic Inventory Management System
**Generated**: 2025-10-25  
**Guidelines Version**: 2.3  
**Status**: Production-Ready with P0-P3 Improvements Needed

## Executive Summary

This task list follows GLOBAL_GUIDELINES v2.3 and the OPERATIONAL_FRAMEWORK (Phases 0-8). The system is currently production-ready with 200+ fixes completed, but requires critical security hardening (P0), API/DB improvements (P1), UI/brand enhancements (P2), and supply chain/resilience features (P3) to achieve top-5 ERP status and surpass Odoo within two years.

**Total Estimated Effort**: ~350 hours across all priorities  
**Critical Path**: P0 fixes (Login-Fix Blitz → Error Envelope → Secrets Audit) → P1 (API/DB) → P2 (UI/Brand) → P3 (SBOM/DAST/Resilience)

**OSF Score (Optimal & Safe over Easy/Fast)**: 0.854 (Hybrid Strategy)

---

## Current Status Summary

### ✅ COMPLETED (Already Implemented)
- bcrypt password hashing enforced (raises RuntimeError if unavailable)
- JWT tokens configured (Access 15m, Refresh 7d) — **JUST ADDED** in `backend/app.py` lines 238-241
- HTTPS/HSTS enforcement via HTTPSMiddleware
- Security headers with CSP nonces via SecurityHeadersMiddleware
- CSRF protection via Flask-WTF
- Rate limiting via Flask-Limiter (100 req/min global, 5 req/min for login)
- Cookie security flags (Secure, HttpOnly, SameSite=Lax)

### ❌ CRITICAL GAPS (P0 Priority)
- No JWT token rotation on logout (tokens remain valid until expiry)
- No lockout mechanism for failed login attempts (brute force vulnerability)
- No MFA option
- Inconsistent error envelope format across codebase
- Secrets in .env files (production risk)
- No CI secret scanning

### ⚠️ HIGH PRIORITY GAPS (P1)
- No request/response validators for API endpoints
- No DB constraints (FK/unique/check) or indexes
- No Alembic migrations
- No drift tests for OpenAPI spec

### 📋 MEDIUM/LOW PRIORITY (P2-P3)
- Brand tokens not derived from Gaara/MagSeeds
- No WCAG AA contrast enforcement
- No SBOM/supply chain scanning
- No circuit breakers for resilience

---

## P0: CRITICAL PRIORITY (Must Complete First)

### P0.1: Login-Fix Blitz (38 hours)

#### P0.1.1: JWT Token Rotation on Logout (4 hours)
- **Owner**: Backend Auth
- **Dependencies**: None
- **Status**: NOT_STARTED
- **Description**: Implement JWT revocation list (Redis or in-memory) to invalidate tokens on logout
- **Files**: 
  - `backend/src/routes/auth_routes.py` (lines 170-184)
  - `backend/src/auth.py` (lines 96-158)
- **Current Issue**: Logout only clears session but JWT remains valid until expiry (CRITICAL SECURITY ISSUE)
- **Implementation**:
  1. Add Redis or in-memory cache for revoked tokens
  2. Store token JTI (JWT ID) on logout with TTL = token expiry
  3. Add middleware to check revocation list before processing requests
  4. Update logout endpoint to revoke both access and refresh tokens

#### P0.1.2: Lockout Mechanism for Failed Login Attempts (6 hours)
- **Owner**: Backend Auth
- **Dependencies**: None
- **Status**: NOT_STARTED
- **Description**: Add failed login counter + lockout (5 attempts within 15 minutes)
- **Files**: 
  - `backend/src/routes/auth_routes.py` (lines 25-119)
  - `backend/src/services/cache_service.py`
- **Current Issue**: No brute force protection exists
- **Implementation**:
  1. Track failed login attempts per username/IP in cache
  2. Increment counter on failed login
  3. Lock account for 15 minutes after 5 failed attempts
  4. Return 429 (Too Many Requests) with lockout expiry time
  5. Reset counter on successful login

#### P0.1.3: Optional MFA (Multi-Factor Authentication) (12 hours)
- **Owner**: Backend Auth
- **Dependencies**: P0.1.1, P0.1.2
- **Status**: NOT_STARTED
- **Description**: Add TOTP-based MFA option for admin users
- **Files**: 
  - `backend/src/routes/auth_routes.py`
  - `backend/src/auth.py`
  - `backend/models/user.py`
- **Implementation**:
  1. Add `mfa_enabled` and `mfa_secret` fields to User model
  2. Install `pyotp` library for TOTP generation
  3. Add `/auth/mfa/setup` endpoint to generate QR code
  4. Add `/auth/mfa/verify` endpoint to validate TOTP code
  5. Modify login flow to require TOTP if MFA enabled
  6. Add `/auth/mfa/disable` endpoint with password confirmation

#### P0.1.4: Negative Tests for Auth Flows (8 hours)
- **Owner**: Backend QA
- **Dependencies**: P0.1.1, P0.1.2, P0.1.3
- **Status**: NOT_STARTED
- **Description**: Write tests for invalid credentials, expired tokens, lockout, MFA failures
- **Files**: `backend/tests/test_auth.py` (NEW FILE)
- **Test Cases**:
  1. Invalid username/password → 401
  2. Expired access token → 401
  3. Revoked token (after logout) → 401
  4. 5 failed login attempts → 429 with lockout
  5. Invalid MFA code → 401
  6. MFA required but not provided → 401
  7. Refresh token reuse after logout → 401

#### P0.1.5: E2E Coverage for Login/Logout/Refresh (8 hours)
- **Owner**: Frontend QA
- **Dependencies**: P0.1.1, P0.1.2, P0.1.3
- **Status**: NOT_STARTED
- **Description**: Playwright/Cypress tests for full auth flows
- **Files**: `frontend/tests/e2e/auth.spec.ts` (NEW FILE)
- **Test Scenarios**:
  1. Successful login → dashboard
  2. Failed login → error message
  3. Logout → redirect to login
  4. Token refresh → seamless continuation
  5. MFA setup → QR code scan → verify
  6. Lockout after 5 failed attempts → wait 15 min

---

### P0.2: Unified Error Envelope (30 hours)

#### P0.2.1: Standardize Error Envelope (6 hours)
- **Owner**: Backend API
- **Dependencies**: None
- **Status**: NOT_STARTED
- **Description**: Create middleware to wrap all responses in `{success, code, message, details?, traceId}`
- **Files**: 
  - `backend/src/middleware/error_envelope_middleware.py` (NEW FILE)
  - `backend/app.py` (lines 325-381)
- **Current Format**: `{success: False, error, message}` (inconsistent)
- **Target Format**: `{success: true/false, code: "AUTH_001", message: "...", details?: {...}, traceId: "uuid"}`
- **Implementation**:
  1. Create `ErrorEnvelopeMiddleware` class
  2. Wrap all responses in standard envelope
  3. Generate traceId per request (UUID or X-Request-Id header)
  4. Map HTTP status codes to error codes (AUTH_001, DB_002, etc.)
  5. Include details object for validation errors

#### P0.2.2: TraceId Generation and Propagation (4 hours)
- **Owner**: Backend API
- **Dependencies**: P0.2.1
- **Status**: NOT_STARTED
- **Description**: Generate traceId per request and include in all responses
- **Files**: `backend/src/middleware/error_envelope_middleware.py`
- **Implementation**:
  1. Generate UUID per request in middleware
  2. Store in `g.trace_id` for access across request lifecycle
  3. Include in all responses (success and error)
  4. Log traceId with all errors for debugging
  5. Accept X-Request-Id header from client if provided

#### P0.2.3: Unified Error Codes Catalog (4 hours)
- **Owner**: Backend API
- **Dependencies**: P0.2.1
- **Status**: NOT_STARTED
- **Description**: Create `/docs/Error_Catalog.md` with all error codes
- **Files**: `/docs/Error_Catalog.md` (UPDATE EXISTING)
- **Error Code Categories**:
  - AUTH_xxx: Authentication/authorization errors
  - DB_xxx: Database errors
  - VAL_xxx: Validation errors
  - SYS_xxx: System errors
  - BIZ_xxx: Business logic errors

#### P0.2.4: Update All Route Handlers (16 hours)
- **Owner**: Backend API
- **Dependencies**: P0.2.1, P0.2.2
- **Status**: NOT_STARTED
- **Description**: Refactor all route handlers to use new error envelope
- **Files**: `backend/src/routes/*.py` (ALL ROUTES)
- **Routes to Update**:
  - auth_routes.py
  - products.py
  - inventory.py
  - customers.py
  - suppliers.py
  - sales.py
  - purchases.py
  - reports.py
  - invoices.py
  - warehouses.py
  - categories.py
  - units.py
  - settings.py
  - users.py
  - roles.py
  - permissions.py
  - audit.py
  - dashboard.py

---

### P0.3-P0.6: Security Hardening Audit (10 hours)

#### P0.3.1: Verify HTTPS/HSTS Enforcement (2 hours)
- **Owner**: Backend Security
- **Files**: `backend/src/middleware/security_middleware.py` (lines 25-70), `backend/.env.production` (NEW FILE)
- **Verification**:
  1. Confirm FORCE_HTTPS=true in production
  2. Confirm HSTS header present with max-age=31536000
  3. Test HTTP→HTTPS redirect
  4. Document in `/docs/Security.md`

#### P0.4.1: Verify CSRF Protection (2 hours)
- **Owner**: Backend Security
- **Files**: `backend/src/middleware/security_middleware.py` (lines 144-167)
- **Verification**:
  1. Confirm Flask-WTF CSRF enabled
  2. Confirm tokens validated on POST/PUT/PATCH/DELETE
  3. Test CSRF token missing → 403
  4. Document in `/docs/Security.md`

#### P0.5.1: Verify Rate Limiting (2 hours)
- **Owner**: Backend Security
- **Files**: `backend/src/middleware/security_middleware.py` (lines 170-200), `backend/src/routes/auth_routes.py` (lines 247-265)
- **Verification**:
  1. Confirm Flask-Limiter enabled
  2. Confirm 100 req/min global limit
  3. Confirm 5 req/min for login endpoint
  4. Test rate limit exceeded → 429
  5. Document in `/docs/Security.md`

#### P0.6.1: Verify CSP Nonces (2 hours)
- **Owner**: Backend Security
- **Files**: `backend/src/middleware/security_middleware.py` (lines 90-95), `backend/app.py` (lines 476-494)
- **Verification**:
  1. Confirm CSP nonces generated per-request
  2. Confirm nonces used in inline scripts
  3. Test CSP violation → blocked
  4. Document in `/docs/CSP.md`

#### P0.6.2: Verify Cookie Security Flags (1 hour)
- **Owner**: Backend Security
- **Files**: `backend/app.py` (lines 226-237)
- **Verification**:
  1. Confirm Secure flag set on all cookies
  2. Confirm HttpOnly flag set on all cookies
  3. Confirm SameSite=Lax flag set
  4. Document in `/docs/Security.md`

#### P0.6.3: Verify JWT TTLs (1 hour)
- **Owner**: Backend Security
- **Files**: `backend/app.py` (lines 238-241), `backend/src/auth.py` (lines 54-55)
- **Verification**:
  1. Confirm Access TTL ≤15m
  2. Confirm Refresh TTL ≤7d
  3. Test token expiry → 401
  4. Document in `/docs/Security.md`

---

### P0.7: Secrets Management Audit (14 hours)

#### P0.7.1: Identify All Secrets (2 hours)
- **Owner**: Backend Security
- **Files**: `backend/.env`, `backend/.env.example`
- **Secrets to Identify**:
  - SECRET_KEY
  - JWT_SECRET_KEY
  - DATABASE_URL
  - REDIS_URL (if applicable)
  - SMTP credentials (if applicable)
  - Third-party API keys (if applicable)

#### P0.7.2: Document Migration to KMS/Vault (4 hours)
- **Owner**: Backend Security
- **Files**: `/docs/Secrets_Migration_Plan.md` (NEW FILE)
- **Migration Options**:
  1. AWS KMS + Secrets Manager
  2. GCP Secret Manager
  3. Azure Key Vault
  4. HashiCorp Vault
- **Migration Steps**:
  1. Choose KMS/Vault provider
  2. Create secrets in KMS/Vault
  3. Update app to fetch secrets at runtime
  4. Remove secrets from .env files
  5. Update CI/CD to inject secrets
  6. Document rotation schedule (≤90 days)

#### P0.7.3: Update /docs/Env.md (2 hours)
- **Owner**: Backend Security
- **Files**: `/docs/Env.md` (UPDATE EXISTING)
- **Document**: Key IDs/Secret Paths (not values) for all secrets

#### P0.7.4: Update /docs/Security.md (2 hours)
- **Owner**: Backend Security
- **Files**: `/docs/Security.md` (UPDATE EXISTING)
- **Document**: Secrets lifecycle (create→access→rotate→revoke)

#### P0.7.5: CI Secret Scanning (4 hours)
- **Owner**: DevOps
- **Files**: `.github/workflows/security.yml` (NEW FILE)
- **Implementation**:
  1. Add gitleaks to CI pipeline
  2. Add trufflehog to CI pipeline
  3. Block PRs with literal secrets
  4. Configure allowlist for false positives
  5. Alert on secret detection

---

## Summary of P0 Tasks

**Total P0 Effort**: 112 hours (3 weeks at 40 hours/week)

**Critical Path**:
1. Week 1: Login-Fix Blitz (P0.1.1-P0.1.3) + Error Envelope (P0.2.1-P0.2.2)
2. Week 2: Error Envelope (P0.2.3-P0.2.4) + Security Audit (P0.3-P0.6)
3. Week 3: Secrets Management (P0.7.1-P0.7.5) + Testing (P0.1.4-P0.1.5)

**Success Criteria**:
- ✅ JWT tokens revoked on logout
- ✅ Lockout after 5 failed login attempts
- ✅ MFA option available for admin users
- ✅ All API responses use standard error envelope with traceId
- ✅ All secrets migrated to KMS/Vault for production
- ✅ CI secret scanning blocks literal secrets
- ✅ 100% negative test coverage for auth flows
- ✅ 100% E2E test coverage for auth flows

---

**Next**: See `/docs/Task_List_P1_P2_P3.md` for P1-P3 task details (API/DB, UI/Brand, SBOM/DAST/Resilience)

