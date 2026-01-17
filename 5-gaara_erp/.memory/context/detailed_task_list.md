# 📋 قائمة المهام التفصيلية - Gaara ERP
# Hierarchical Task List with Subtasks

> **Last Updated**: Session Active  
> **Total Tasks**: 92 Main Tasks + 276 Subtasks  
> **Target**: 100% Production Ready

---

## 🔴 P0 - CRITICAL (ALL COMPLETE ✅)

### ✅ Task 1: KMS/Vault Secrets Migration
**Status**: ✅ COMPLETE  
**File**: `gaara_erp/core_modules/security/secrets_manager.py`

Subtasks:
- [x] 1.1: Create SecretsManager class
- [x] 1.2: Implement get_secret() method
- [x] 1.3: Add Azure Key Vault integration
- [x] 1.4: Add HashiCorp Vault integration
- [x] 1.5: Add environment variable fallback
- [x] 1.6: Implement secret rotation
- [x] 1.7: Add audit logging

### ✅ Task 2: JWT Token Rotation & Blacklist
**Status**: ✅ COMPLETE  
**File**: `gaara_erp/core_modules/security/jwt_manager.py`

Subtasks:
- [x] 2.1: Create JWTManager class
- [x] 2.2: Implement token generation (15min TTL)
- [x] 2.3: Add refresh token support (7 days)
- [x] 2.4: Implement token blacklist
- [x] 2.5: Add token validation
- [x] 2.6: Implement automatic rotation

### ✅ Task 3: CSRF Protection
**Status**: ✅ COMPLETE (Already in Django)

Subtasks:
- [x] 3.1: Verify CsrfViewMiddleware in MIDDLEWARE
- [x] 3.2: Confirm CSRF cookie settings
- [x] 3.3: Test CSRF token in forms

### ✅ Task 4: Rate Limiting
**Status**: ✅ COMPLETE  
**File**: `gaara_erp/core_modules/security/rate_limiter.py`

Subtasks:
- [x] 4.1: Create RateLimiter class
- [x] 4.2: Implement sliding window algorithm
- [x] 4.3: Add Redis backend
- [x] 4.4: Configure limits per endpoint
- [x] 4.5: Add decorator for views

### ✅ Task 5: Docker Security Hardening
**Status**: ✅ COMPLETE  
**Files**: `Dockerfile`, `docker-compose.wsgi.yml`

Subtasks:
- [x] 5.1: Multi-stage builds
- [x] 5.2: Non-root user
- [x] 5.3: Minimal base images
- [x] 5.4: Health checks
- [x] 5.5: Security scanning

### ✅ Task 6: Secret Scanning CI
**Status**: ✅ COMPLETE  
**File**: `.github/workflows/secret-scan.yml`

### ✅ Task 7: Hardcoded Password Fix
**Status**: ✅ COMPLETE

### ✅ Task 8: SBOM Generation
**Status**: ✅ COMPLETE  
**File**: `.github/workflows/sbom.yml`

---

## 🟠 P1 - HIGH PRIORITY (35/47 remaining)

### Task 9: OpenAPI 3.0 Specification ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 8h  
**Dependencies**: None

Subtasks:
- [ ] 9.1: Install drf-spectacular (Django REST Swagger)
- [ ] 9.2: Configure schema settings in settings.py
- [ ] 9.3: Add @extend_schema decorators to all views
- [ ] 9.4: Generate OpenAPI schema file
- [ ] 9.5: Add Swagger UI endpoint (/api/docs/)
- [ ] 9.6: Add ReDoc endpoint (/api/redoc/)
- [ ] 9.7: Validate schema with OpenAPI linter
- [ ] 9.8: Document all response codes

**Implementation**:
```python
# settings.py
SPECTACULAR_SETTINGS = {
    'TITLE': 'Gaara ERP API',
    'VERSION': '12.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
```

---

### Task 10: Typed Frontend API Client ⬜
**Priority**: P1  
**Owner**: FE  
**Estimate**: 6h  
**Dependencies**: Task 9

Subtasks:
- [ ] 10.1: Install openapi-typescript-codegen
- [ ] 10.2: Configure code generation script
- [ ] 10.3: Generate TypeScript client from OpenAPI
- [ ] 10.4: Create API service wrapper
- [ ] 10.5: Add request/response types
- [ ] 10.6: Update frontend to use typed client
- [ ] 10.7: Add runtime validation with Zod

**Implementation**:
```bash
npx openapi-typescript-codegen --input ./openapi.json --output ./src/api/generated
```

---

### Task 11: Unified Error Envelope ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 11.1: Create ErrorEnvelope class
- [ ] 11.2: Define error codes enum
- [ ] 11.3: Create exception handler middleware
- [ ] 11.4: Add traceId to all responses
- [ ] 11.5: Add timestamp field
- [ ] 11.6: Implement localization for messages
- [ ] 11.7: Update all API responses

**Schema**:
```json
{
  "success": false,
  "code": "AUTH_INVALID",
  "message": "بيانات اعتماد غير صحيحة",
  "details": null,
  "traceId": "abc-123",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

---

### Task 12: Alembic Database Migrations ⬜
**Priority**: P1  
**Owner**: DBA  
**Estimate**: 8h  
**Dependencies**: None

Subtasks:
- [ ] 12.1: Install alembic
- [ ] 12.2: Initialize alembic.ini
- [ ] 12.3: Create migration environment
- [ ] 12.4: Generate initial migration
- [ ] 12.5: Test up/down migrations
- [ ] 12.6: Add pre-commit hook for migrations
- [ ] 12.7: Document migration workflow

---

### Task 13: Up/Down Migration Scripts ⬜
**Priority**: P1  
**Owner**: DBA  
**Estimate**: 6h  
**Dependencies**: Task 12

Subtasks:
- [ ] 13.1: Audit all existing Django migrations
- [ ] 13.2: Create reversible migrations
- [ ] 13.3: Add data migration scripts
- [ ] 13.4: Test rollback scenarios
- [ ] 13.5: Document rollback procedures

---

### Task 14: Database Connection Pooling ⬜
**Priority**: P1  
**Owner**: DBA  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 14.1: Install django-db-connection-pool
- [ ] 14.2: Configure pool settings (min=5, max=20)
- [ ] 14.3: Add connection timeout settings
- [ ] 14.4: Monitor pool usage
- [ ] 14.5: Add health check for pool

---

### Task 15: Activity Logging Service ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 8h  
**Dependencies**: None

Subtasks:
- [ ] 15.1: Create ActivityLog model
- [ ] 15.2: Create logging service class
- [ ] 15.3: Add middleware for auto-logging
- [ ] 15.4: Log all CRUD operations
- [ ] 15.5: Add admin UI for log viewing
- [ ] 15.6: Add log filtering/search
- [ ] 15.7: Add log retention policy

---

### Task 16: Health Check Endpoints ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 16.1: Create /health endpoint (basic)
- [ ] 16.2: Create /health/ready endpoint
- [ ] 16.3: Create /health/live endpoint
- [ ] 16.4: Add database check
- [ ] 16.5: Add Redis check
- [ ] 16.6: Add Celery check
- [ ] 16.7: Return response time metrics

**Implementation**:
```python
@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'database': check_db(),
        'redis': check_redis(),
        'version': settings.VERSION,
        'timestamp': now().isoformat()
    })
```

---

### Task 17: Circuit Breaker Wrapper ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 8h  
**Dependencies**: None

Subtasks:
- [ ] 17.1: Install pybreaker library
- [ ] 17.2: Create CircuitBreaker decorator
- [ ] 17.3: Configure thresholds (50% failures)
- [ ] 17.4: Add fallback handlers
- [ ] 17.5: Add circuit state monitoring
- [ ] 17.6: Integrate with external API calls

---

### Task 18: MFA System ⬜
**Priority**: P1  
**Owner**: Sec  
**Estimate**: 12h  
**Dependencies**: Task 2

Subtasks:
- [ ] 18.1: Install django-otp and qrcode
- [ ] 18.2: Create TOTP device model
- [ ] 18.3: Add MFA setup endpoint
- [ ] 18.4: Add QR code generation
- [ ] 18.5: Add verification endpoint
- [ ] 18.6: Add backup codes generation
- [ ] 18.7: Update login flow
- [ ] 18.8: Add frontend MFA setup UI
- [ ] 18.9: Add recovery flow

---

### Task 19: Password Policy Enforcement ⬜
**Priority**: P1  
**Owner**: Sec  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 19.1: Create PasswordValidator class
- [ ] 19.2: Enforce minimum 12 characters
- [ ] 19.3: Require uppercase/lowercase/number/symbol
- [ ] 19.4: Check against common passwords
- [ ] 19.5: Prevent password reuse (last 5)
- [ ] 19.6: Add password strength indicator (FE)
- [ ] 19.7: Add password expiry (90 days optional)

---

### Task 20: CSRF Tokens in Frontend Forms ⬜
**Priority**: P1  
**Owner**: FE  
**Estimate**: 6h  
**Dependencies**: None

Subtasks:
- [ ] 20.1: Create CSRF token interceptor
- [ ] 20.2: Add token to Axios defaults
- [ ] 20.3: Handle token refresh
- [ ] 20.4: Update all form submissions
- [ ] 20.5: Add error handling for CSRF failures

---

### Task 21: Frontend Input Sanitization ⬜
**Priority**: P1  
**Owner**: FE  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 21.1: Install DOMPurify
- [ ] 21.2: Create sanitize utility function
- [ ] 21.3: Apply to all user inputs
- [ ] 21.4: Apply to rich text editors
- [ ] 21.5: Add XSS tests

---

### Task 22: CSP Meta Tags with Nonces ⬜
**Priority**: P1  
**Owner**: FE  
**Estimate**: 2h  
**Dependencies**: None

Subtasks:
- [ ] 22.1: Configure CSP in Django middleware
- [ ] 22.2: Generate nonces for scripts
- [ ] 22.3: Update templates with nonces
- [ ] 22.4: Test CSP violations in browser

---

### Task 23: RAG Caching with TTLs ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 23.1: Configure Redis for RAG cache
- [ ] 23.2: Add 1-hour TTL for queries
- [ ] 23.3: Add cache invalidation logic
- [ ] 23.4: Monitor cache hit rate

---

### Task 24: RAG Reranker Optimization ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 6h  
**Dependencies**: Task 23

Subtasks:
- [ ] 24.1: Install sentence-transformers
- [ ] 24.2: Implement cross-encoder reranking
- [ ] 24.3: Add relevance scoring
- [ ] 24.4: Optimize batch processing
- [ ] 24.5: Add A/B testing framework

---

### Task 25: Comprehensive Negative Tests ⬜
**Priority**: P1  
**Owner**: BE  
**Estimate**: 12h  
**Dependencies**: None

Subtasks:
- [ ] 25.1: Create test fixtures
- [ ] 25.2: Test invalid inputs
- [ ] 25.3: Test unauthorized access
- [ ] 25.4: Test rate limiting
- [ ] 25.5: Test error responses
- [ ] 25.6: Achieve 80% coverage

---

### Task 26: E2E Tests for Critical Flows ⬜
**Priority**: P1  
**Owner**: FE  
**Estimate**: 16h  
**Dependencies**: None

Subtasks:
- [ ] 26.1: Install Playwright
- [ ] 26.2: Configure test environment
- [ ] 26.3: Test login flow
- [ ] 26.4: Test product CRUD
- [ ] 26.5: Test invoice creation
- [ ] 26.6: Test reporting
- [ ] 26.7: Add CI integration

---

### Task 27: DAST Scanning ⬜
**Priority**: P1  
**Owner**: DX  
**Estimate**: 4h  
**Dependencies**: None

Subtasks:
- [ ] 27.1: Configure OWASP ZAP
- [ ] 27.2: Add to CI pipeline
- [ ] 27.3: Configure scan policies
- [ ] 27.4: Create vulnerability report template

---

### Tasks 28-47: (Additional P1 Tasks)
[Continued in next section...]

---

## 🟡 P2 - MEDIUM PRIORITY (12/17 remaining)

### Task 48: Database Query Optimization ⬜
**Priority**: P2  
**Owner**: DBA  
**Estimate**: 8h

Subtasks:
- [ ] 48.1: Run EXPLAIN ANALYZE on slow queries
- [ ] 48.2: Add missing indexes
- [ ] 48.3: Implement select_related/prefetch_related
- [ ] 48.4: Fix N+1 queries
- [ ] 48.5: Add query monitoring

---

### Task 49: Multi-Layer Caching ⬜
**Priority**: P2  
**Owner**: BE  
**Estimate**: 12h

Subtasks:
- [ ] 49.1: Configure LRU cache (local)
- [ ] 49.2: Configure Redis cache (distributed)
- [ ] 49.3: Add CDN for static assets
- [ ] 49.4: Implement cache invalidation
- [ ] 49.5: Add cache monitoring

---

### Tasks 50-64: (Additional P2 Tasks)
[See PRODUCTION_READINESS_TODO.md for details]

---

## ✅ VERIFICATION TASKS

### Task 68: Frontend Pages Completeness ⬜
**Priority**: Verification  
**Estimate**: 4h

Subtasks:
- [ ] 68.1: Verify all Auth pages exist
- [ ] 68.2: Verify Dashboard page
- [ ] 68.3: Verify all CRUD pages
- [ ] 68.4: Verify Error pages (404, 500)
- [ ] 68.5: Verify Settings pages

---

### Task 69: All Buttons Functional ⬜
**Priority**: Verification  
**Estimate**: 8h

Subtasks:
- [ ] 69.1: Audit all buttons in UI
- [ ] 69.2: Test each button action
- [ ] 69.3: Verify backend handlers exist
- [ ] 69.4: Fix disconnected buttons

---

### Task 70: Frontend-Backend Connection ⬜
**Priority**: Verification  
**Estimate**: 6h

Subtasks:
- [ ] 70.1: Test all API endpoints
- [ ] 70.2: Verify response handling
- [ ] 70.3: Test error scenarios
- [ ] 70.4: Validate data flow

---

### Task 71: Database Migrations Complete ⬜
**Priority**: Verification  
**Estimate**: 4h

Subtasks:
- [ ] 71.1: Run makemigrations --check
- [ ] 71.2: Verify all models have migrations
- [ ] 71.3: Test migrate/rollback

---

### Task 72: Duplicate Files Detection ⬜
**Priority**: Verification  
**Estimate**: 4h

Subtasks:
- [ ] 72.1: Scan for duplicate files
- [ ] 72.2: Compare file contents
- [ ] 72.3: Merge safe duplicates
- [ ] 72.4: Log in DEDUPLICATION_LOG.md

---

## 📚 DOCUMENTATION TASKS

### Task 84: Fix 88 ESLint Errors ⬜
**Priority**: P1  
**Estimate**: 4h

Subtasks:
- [ ] 84.1: Run eslint --fix
- [ ] 84.2: Fix remaining manual errors
- [ ] 84.3: Update ESLint config
- [ ] 84.4: Add pre-commit hook

---

### Task 85: Configure Production .env ⬜
**Priority**: P1  
**Estimate**: 2h

Subtasks:
- [ ] 85.1: Create .env.production template
- [ ] 85.2: Document all required variables
- [ ] 85.3: Add KMS references
- [ ] 85.4: Remove all hardcoded secrets

---

## 📊 PROGRESS SUMMARY

| Priority | Complete | Remaining | Progress |
|----------|----------|-----------|----------|
| P0 | 8 | 0 | ✅ 100% |
| P1 | 12 | 35 | 🟡 26% |
| P2 | 5 | 12 | 🟡 29% |
| Verification | 2 | 3 | 🔴 40% |
| Docs | 3 | 5 | 🟡 38% |
| **TOTAL** | **30** | **55** | **~33%** |

---

## 🎯 NEXT ACTIONS (Priority Order)

1. **NOW**: Task 9 - OpenAPI 3.0 Specification
2. **NEXT**: Task 10 - Typed Frontend API Client
3. **THEN**: Task 11 - Unified Error Envelope
4. **AFTER**: Task 84 - Fix ESLint Errors (88 issues)
5. **CONTINUE**: Tasks 12-27 in order

---

## 📝 NOTES

- All P0 tasks COMPLETE - Production is unblocked
- Focus on P1 API Governance for better DX
- ESLint fixes needed before E2E tests
- Database migrations should use Alembic for production

---

**Reference**: GLOBAL_PROFESSIONAL_CORE_PROMPT.md
