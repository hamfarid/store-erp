<!-- GUIDELINES_VERSION: 2.3 -->
<!-- LAST_UPDATED: 2025-10-24 -->
<!-- AUDIT_REF: docs/COMPREHENSIVE_AUDIT_2025-10-24.md -->
<!-- ISSUES_WORKFLOW: .github/workflows/create_issues_from_task_list.yml -->

# Task List — Store Management System v1.6

## Comprehensive Security & System Hardening

**Guidelines**: GLOBAL_GUIDELINES v2.3
**Audit Date**: 2025-10-24
**Total Tasks**: 142 (23 P0, 47 P1, 54 P2, 18 P3)

Automation: Use GitHub Actions → "Create Issues from Task List" to sync these tasks into GitHub Issues (idempotent; uses hidden TL-ID markers).

Scope: repo_root="d:\APPS_AI\store\store_v1.6"
Owner Legend: [AA]=Augment Agent, [Sec]=Security Lead, [BE]=Backend Dev, [FE]=Frontend Dev, [DBA]=Database Admin, [DX]=DevEx
Status: [ ] Not Started, [/] In Progress, [x] Complete, [!] Blocked

---

## P0 — CRITICAL SECURITY (Must Fix Immediately - 0-7 Days)

### Authentication & Session Management (P0)

1. [ ] **Enable CSRF protection globally** — [P0][Sec][0.1h][None]
   - File: `backend/src/main.py:193`
   - Change: `app.config['WTF_CSRF_ENABLED'] = True`
   - Impact: Prevents all CSRF attacks; blocks production deployment
   - Tests: Add CSRF token validation to frontend forms

2. [ ] **Set JWT access token TTL to 15 minutes** — [P0][Sec][0.2h][None]
   - File: `backend/src/auth.py:55`
   - Change: `JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)`
   - Current: 1 hour (4x guideline limit)
   - Dependency: Refresh token rotation (task #3)

3. [ ] **Implement JWT refresh token rotation** — [P0][Sec][2h][Task #2]
   - File: `backend/src/auth.py` + new `routes/auth_refresh.py`
   - Logic: Issue new access+refresh pair, revoke old refresh token
   - Requirements: Token blacklist (Redis), rotation endpoint
   - Tests: Verify old refresh fails after rotation

4. [ ] **Set refresh token TTL to 7 days** — [P0][Sec][0.1h][None]
   - File: `backend/src/auth.py:56`
   - Change: `JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)`
   - Current: 30 days (4x guideline limit)

5. [ ] **Implement account lockout after failed login attempts** — [P0][Sec][3h][None]
   - Files: `backend/src/auth.py`, `models/user_unified.py`
   - Logic: Track failed attempts in DB, lock after 5 failures for 15 min
   - Fields: `failed_login_count`, `locked_until` in User model
   - Tests: Verify lockout triggers, auto-unlock after timeout

6. [ ] **Add rate limiting to /api/auth/login** — [P0][Sec][1h][None]
   - File: `backend/src/routes/auth.py`
   - Config: Flask-Limiter `@limiter.limit("5 per minute")` decorator
   - Dependencies: Task #32 (Redis backend for limiter)
   - Tests: Verify 429 response after 5 attempts

7. [ ] **Migrate secrets to KMS/Vault** — [P0][Sec][8h][None]
   - Files: `.env.example`, `backend/src/config.py`
   - Change: Remove plaintext SECRET_KEY, JWT_SECRET_KEY, ADMIN_PASSWORD
   - Implement: KMS client (AWS/GCP/Azure) or HashiCorp Vault integration
   - Config: Store Key IDs/Secret Paths only; inject at runtime
   - Documentation: Record in `docs/Env.md` and `docs/Security.md`
   - Tests: Verify production startup without .env secrets

8. [ ] **Configure secure cookie flags** — [P0][Sec][0.5h][None]
   - File: `backend/src/main.py`
   - Flags: `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`
   - Flags: `SESSION_COOKIE_SAMESITE='Lax'` (or 'Strict')
   - Condition: Only if switching from Authorization headers to cookies
   - Tests: Verify flags in Set-Cookie response headers

### Authorization & RBAC (P0)

9. [ ] **Add @require_permission decorator to all protected routes** — [P0][Sec][12h][None]
   - Files: `backend/src/routes/**/*.py` (50+ route handlers)
   - Pattern: Stack `@jwt_required()` + `@require_permission('MODULE_READ')`
   - Modules: users, products, invoices, warehouses, reports, settings
   - Tests: Negative tests for each route (401 without token, 403 without permission)

10. [ ] **Document RBAC permission matrix** — [P0][Sec][4h][Task #9]
    - File: `docs/Permissions_Model.md` (expand existing)
    - Table: Role × Module × Permission (ADMIN, MODIFY, READ, VIEW_LIGHT, APPROVE)
    - Format: Markdown table with all roles (admin, manager, user) × all modules
    - Tests: Automated matrix validation against route decorators

11. [ ] **Frontend route guards with permission checks** — [P0][FE][6h][Task #9]
    - File: `frontend/src/components/ProtectedRoute.jsx` (create)
    - Logic: Check user.permissions before rendering <Outlet />
    - Integration: Wrap all routes in App.jsx with <ProtectedRoute>
    - UX: Redirect to /403 or show permission-denied modal
    - Tests: E2E tests for route access control

### HTTPS & Transport Security (P0)

12. [ ] **Enforce HTTPS in production environment** — [P0][Sec][2h][None]
    - Files: `backend/src/config.py`, `.env.example`
    - Logic: HTTP→HTTPS redirect middleware when `APP_ENV=production`
    - Headers: Add HSTS header `Strict-Transport-Security: max-age=31536000`
    - Config: `FORCE_HTTPS=true` (prod), `BASE_URL=https://...`
    - Tests: Verify redirect, HSTS header presence

13. [ ] **Configure CSP with nonces** — [P0][Sec][3h][None]
    - Files: `backend/src/middleware/security.py`, templates
    - Policy: `script-src 'nonce-{random}'; style-src 'nonce-{random}'`
    - Implementation: Generate nonce per request, inject into templates
    - Document: `docs/CSP.md` with policy rationale
    - Tests: CSP report-uri endpoint, violation monitoring

14. [ ] **Configure security headers** — [P0][Sec][1h][None]
    - File: `backend/src/middleware/security.py`
    - Headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy
    - Headers: Permissions-Policy (camera, microphone, geolocation)
    - Tests: Verify headers in response with security headers scanner

### Secrets Management (P0)

15. [ ] **Scan repository for leaked secrets** — [P0][Sec][1h][None]
    - Tools: gitleaks, trufflehog
    - Scope: Full git history scan
    - Action: Revoke any found secrets immediately
    - CI: Add secret scanning to GitHub Actions (block on findings)

16. [ ] **Remove hardcoded passwords from scripts** — [P0][Sec][2h][None]
    - Files: `simple_recreate_db.py:240,307`, `setup_database.py`, etc.
    - Change: Accept password via env var or KMS/Vault
    - Clean: Remove all `password="admin123"` literals
    - Tests: Verify scripts work with injected secrets

### Database Security (P0)

17. [ ] **Upgrade password hashing to Argon2id/scrypt** — [P0][Sec][2h][None]
    - File: `backend/src/auth.py:70-91`
    - Change: Replace bcrypt with argon2-cffi
    - Migration: Hash existing passwords on first login
    - Fallback: Remove SHA-256 fallback (security risk)
    - Tests: Verify new hashes validate correctly

18. [ ] **Add SQL injection protection audit** — [P0][Sec][4h][None]
    - Scope: All SQLAlchemy queries, especially dynamic filters
    - Pattern: Ensure parameterized queries (no string concatenation)
    - Tools: semgrep with SQLi rules
    - Tests: Fuzzing tests with malicious input

### Input Validation (P0)

19. [ ] **Add input validation to all API endpoints** — [P0][BE][8h][None]
    - Pattern: Use Marshmallow or Pydantic schemas for request validation
    - Scope: 50+ endpoints across all blueprints
    - Response: 400 Bad Request with validation errors in unified envelope
    - Tests: Negative tests with invalid payloads (missing fields, wrong types, etc.)

20. [ ] **RAG input schema validation** — [P0][BE][2h][None]
    - File: `backend/src/rag_service.py:83-85`
    - Schema: Max length 1000 chars, alphanumeric + punctuation only
    - Guards: Prompt injection detection (regex for common patterns)
    - Allowlist: Source domains for retrieval
    - Tests: Verify rejection of oversized/malicious inputs

### Deployment Security (P0)

21. [ ] **Configure production .env with KMS references** — [P0][DX][2h][Task #7]
    - File: `.env.production` (create, gitignored)
    - Content: Only Key IDs/Vault Paths (no secret values)
    - Example: `JWT_SECRET_KEY=kms://aws/secretsmanager/prod/jwt-secret`
    - CI: Inject secrets at deploy time via OIDC/Vault Agent

22. [ ] **Docker image security hardening** — [P0][DX][3h][None]
    - File: `Dockerfile`
    - Changes: Run as non-root user, remove unnecessary packages
    - Scan: Trivy/Grype scan in CI (fail on critical CVEs)
    - Multi-stage: Ensure build artifacts not in final image

23. [ ] **Enable SBOM generation on every PR** — [P0][DX][2h][None]
    - Tool: Syft or CycloneDX
    - CI: `.github/workflows/sbom.yml`
    - Artifact: Store SBOM as build artifact, diff on PRs
    - Alert: Notify on new high-severity dependencies

---

## P1 — HIGH PRIORITY (Complete in 7-30 Days)

### API Governance (P1)

24. [ ] **Generate complete OpenAPI 3.0 specification** — [P1][BE][8h][None]
    - File: `/contracts/openapi.yaml`
    - Tool: Flask-RESTX auto-generation or manual documentation
    - Scope: All 50+ endpoints (auth, users, products, invoices, warehouses, reports)
    - Validation: Spectral linting of OpenAPI spec
    - Tests: Contract tests verifying API matches spec

25. [ ] **Generate typed frontend API client** — [P1][FE][4h][Task #24]
    - Tool: openapi-generator-cli
    - Output: `frontend/src/api/generated/` (TypeScript)
    - Integration: Replace manual Axios calls with typed client
    - Tests: Type checking catches API contract drift

26. [ ] **Implement unified error envelope** — [P1][BE][6h][None]
    - Pattern: `{success: false, code: "AUTH_INVALID", message: "...", details: null, traceId: "uuid"}`
    - Files: Update all error responses in `backend/src/routes/**/*.py`
    - Catalog: Document error codes in `docs/Error_Catalog.md`
    - Tests: Verify all error responses match schema

27. [ ] **Add API request/response validators** — [P1][BE][6h][Task #24]
    - Pattern: Marshmallow schemas for every endpoint
    - Auto-validation: Decorator to validate against schema
    - Response: 400 with validation errors if schema fails
    - Tests: Negative tests for every endpoint

### Database (P1)

28. [ ] **Initialize Alembic for migrations** — [P1][DBA][4h][None]
    - Commands: `flask db init`, `flask db migrate -m "initial"`
    - Config: `migrations/` directory, env.py with auto-detection
    - Baseline: Generate migration for current schema
    - Tests: Test migration up/down, rollback scenarios

29. [ ] **Consolidate duplicate models** — [P1][DBA][8h][None]
    - Duplicates: invoice.py + invoices.py + invoice_unified.py + unified_invoice.py
    - Canonical: Keep `unified_invoice.py`, delete others
    - Refactor: Update all imports to canonical model
    - Move: Legacy models to `/backend/unneeded/` with breadcrumbs
    - Tests: Verify no broken imports, all tests pass

30. [ ] **Add missing foreign key constraints** — [P1][DBA][6h][Task #28]
    - Scope: Review all relationships in unified models
    - Missing: Likely missing in invoice→product, warehouse→product
    - Migration: Alembic migration adding FK constraints
    - Tests: Verify FK violations raise IntegrityError

31. [ ] **Add database indexes** — [P1][DBA][4h][None]
    - Analysis: EXPLAIN ANALYZE on slow queries
    - Candidates: user.email, invoice.created_at, product.barcode
    - Migration: Alembic migration adding indexes
    - Tests: Verify query performance improvement

### Security Hardening (P1)

32. [ ] **Configure Flask-Limiter with Redis backend** — [P1][BE][3h][None]
    - File: `backend/src/main.py`
    - Config: `RATELIMIT_STORAGE_URL=redis://localhost:6379/0`
    - Limits: Per-endpoint limits (login 5/min, API 60/min)
    - Tests: Verify 429 response, rate limit headers

33. [ ] **Add upload file scanning** — [P1][Sec][6h][None]
    - File: `backend/src/middleware/upload_scanner.py` (create)
    - Checks: File type validation, virus scan (ClamAV), size limits
    - Integration: Middleware for all upload endpoints
    - Tests: Negative tests with malicious files (EICAR test file)

34. [ ] **Add SSRF defenses** — [P1][Sec][4h][None]
    - Scope: Any endpoint fetching external URLs
    - Checks: Allowlist of permitted domains, block private IPs
    - Library: Use SSRF protection library or custom validator
    - Tests: Attempt SSRF to localhost, internal IPs (should fail)

35. [ ] **Implement route obfuscation** — [P1][Sec][6h][None]
    - Pattern: HMAC-signed hashed route labels with short TTL
    - Example: `/api/users/123` → `/api/r/{hmac-hash}`
    - Config: HMAC secret from KMS, TTL 5 minutes
    - Documentation: `docs/Route_Obfuscation.md`
    - Tests: Verify expired signatures rejected

### Frontend Security (P1)

36. [ ] **Add CSRF tokens to all frontend forms** — [P1][FE][6h][Task #1]
    - Pattern: Fetch CSRF token from `/api/csrf-token`, include in headers
    - Forms: All forms with POST/PUT/DELETE requests
    - Integration: Axios interceptor to auto-inject CSRF header
    - Tests: Verify requests fail without valid CSRF token

37. [ ] **Implement frontend input sanitization** — [P1][FE][4h][None]
    - Library: DOMPurify for XSS prevention
    - Scope: All user-generated content display (especially Arabic text)
    - Pattern: Sanitize before rendering to DOM
    - Tests: Attempt XSS with script tags (should be sanitized)

38. [ ] **Add Content Security Policy meta tags** — [P1][FE][2h][Task #13]
    - Pattern: `<meta http-equiv="Content-Security-Policy" content="...">`
    - Nonces: Inject nonce from backend into script/style tags
    - Tests: Verify inline scripts blocked without nonce

### RAG Middleware (P1)

39. [ ] **Implement RAG caching with TTLs** — [P1][BE][4h][None]
    - File: `backend/src/rag_service.py`
    - Strategy: Redis cache for query results, TTL 1 hour
    - Key: `rag:query:{hash(text)}:{top_k}`
    - Invalidation: Clear cache on data refresh
    - Tests: Verify cache hits, TTL expiration

40. [ ] **Add RAG reranker optimization** — [P1][BE][6h][None]
    - Library: sentence-transformers cross-encoder for reranking
    - Flow: ChromaDB retrieval → rerank top 20 → return top 5
    - Metrics: Measure P@5, MRR, nDCG improvement
    - Tests: Compare with baseline (no reranking)

41. [ ] **Implement RAG evaluation metrics** — [P1][BE][8h][None]
    - Metrics: Precision@k, Mean Reciprocal Rank, nDCG
    - Dataset: Create test set with queries and expected results
    - CI: Run evaluation on every RAG code change
    - Documentation: Record in `docs/RAG_Metrics.md`

### Testing (P1)

42. [ ] **Add comprehensive negative tests** — [P1][BE][12h][None]
    - Scope: Every API endpoint
    - Cases: Missing auth, missing permissions, invalid input, SQL injection
    - Coverage: Target 80% line coverage minimum
    - CI: Block PRs if coverage drops below 80%

43. [ ] **Add E2E tests for critical flows** — [P1][FE][16h][None]
    - Tool: Playwright or Cypress
    - Flows: Login, create invoice, product search, warehouse transfer
    - CI: Run on every PR
    - Tests: Should cover 50% of user journeys

44. [ ] **Implement DAST scanning** — [P1][DX][4h][None]
    - Tool: OWASP ZAP baseline scan
    - Trigger: On every PR (ephemeral environment)
    - Threshold: Fail on high-severity findings
    - CI: `.github/workflows/dast.yml`

### Documentation (P1)

45. [ ] **Expand API_Contracts.md** — [P1][BE][6h][Task #24]
    - Content: Document all endpoints with request/response examples
    - Format: Mirror OpenAPI spec in human-readable format
    - Scope: Auth, users, products, invoices, warehouses, reports, settings
    - Tests: Verify examples match actual API behavior

46. [ ] **Create comprehensive Security.md** — [P1][Sec][8h][None]
    - Content: Threat model, security controls, incident response
    - Sections: Auth, authz, data protection, transport, monitoring
    - Status: Expand existing 367-line doc with remediation progress
    - Tests: Security audit checklist derived from doc

47. [ ] **Document database schema with ERD** — [P1][DBA][4h][None]
    - File: `docs/DB_Schema.md` (expand existing)
    - Diagram: Mermaid ERD showing all tables and relationships
    - Documentation: Document all columns, constraints, indexes
    - Tests: Auto-generate ERD from Alembic migrations

### CI/CD (P1)

48. [ ] **Implement CI security gates** — [P1][DX][8h][None]
    - Gates: Build, lint, test, typecheck, security scan, SBOM, DAST, Lighthouse
    - Tools: flake8, autopep8, pytest, gitleaks, Syft, ZAP, Lighthouse CI
    - Policy: Block merge if any gate fails (configurable allowlist)
    - CI: `.github/workflows/ci.yml`

49. [ ] **Add Lighthouse performance budgets** — [P1][FE][4h][None]
    - Budgets: Performance >90, Accessibility >90, SEO >90, PWA >80
    - CI: Lighthouse CI on every PR
    - Fail: Block merge if budgets not met
    - CI: `.github/workflows/lighthouse.yml`

50. [ ] **Implement WCAG AA contrast checks** — [P1][FE][2h][None]
    - Tool: axe-core or pa11y in CI
    - Threshold: 0 violations for WCAG AA
    - CI: Block merge on violations
    - Tests: Manual accessibility testing with screen reader

### GitHub Integration (P1)

51. [ ] **Auto-generate GitHub Issues from this task list** — [P1][DX][2h][None]
    - Script: Parse this markdown, create issues via GitHub API
    - Labels: P0-P3, area:FE/BE/DB/Security/UI/RAG/Docs
    - Assignment: Link to GitHub Project board
    - Automation: Run on task list updates

52. [ ] **Configure GitHub Actions auto-deploy** — [P1][DX][6h][None]
    - Workflow: `.github/workflows/deploy.yml`
    - Environments: dev→staging→prod with required reviewers
    - Secrets: Via KMS/Vault (OIDC authentication)
    - Strategy: Canary or blue-green (optional, ADD-ON F)

53. [ ] **Set up GitHub Wiki** — [P1][DX][4h][None]
    - Content: Mirror key docs from `/docs` (no secrets)
    - Pages: Architecture, API, Database, Security, Runbook
    - Sync: Automated sync from repo to wiki

54. [ ] **Configure GitHub Pages for docs** — [P1][DX][6h][None]
    - Tool: MkDocs or Docusaurus
    - Source: `/docs` directory
    - URL: `https://{org}.github.io/{repo}`
    - CI: Auto-deploy on main branch changes

### Observability (P1)

55. [ ] **Implement structured logging** — [P1][BE][6h][None]
    - Format: `{traceId, userId, tenantId, route, action, severity, timed_ms, outcome}`
    - Library: Python structlog
    - Output: JSON logs to stdout (for log aggregation)
    - Tests: Verify log format, no stack traces to clients

56. [ ] **Add distributed tracing** — [P1][BE][8h][None]
    - Tool: OpenTelemetry + Jaeger or Zipkin
    - Scope: Trace requests across backend → database → RAG
    - Headers: Propagate trace context in HTTP headers
    - UI: Jaeger UI for trace visualization

57. [ ] **Define SLOs and error budgets** — [P1][DX][4h][None]
    - SLOs: Availability 99.9%, P95 latency <500ms
    - Error budgets: Track budget consumption weekly
    - Policy: Block risky merges when budget exhausted
    - Documentation: `docs/SLOs.md`

### UI/Brand (P1)

58. [ ] **Generate design tokens from Gaara/MagSeeds** — [P1][FE][6h][None]
    - Sources: <www.gaaragroup.com>, <www.magseeds.com>
    - Output: `/ui/theme/tokens.json` and `/docs/Brand_Palette.json`
    - Tokens: Colors, typography, spacing, shadows, radii
    - Integration: Replace hardcoded colors with token references

59. [ ] **Create UI Design System documentation** — [P1][FE][8h][Task #58]
    - File: `docs/UI_Design_System.md`
    - Content: Component library, usage guidelines, accessibility
    - Examples: Interactive Storybook or similar
    - Tests: Visual regression tests (Percy or Chromatic)

60. [ ] **Implement light/dark theme toggle** — [P1][FE][6h][Task #58]
    - State: User preference in localStorage
    - Tokens: Separate light/dark token sets
    - UI: Toggle in settings page
    - Tests: Verify theme persistence across sessions

### Data Quality (P1)

61. [ ] **Implement input validation at all layers** — [P1][BE+FE][8h][None]
    - Layers: Frontend (immediate feedback), backend (security), database (constraints)
    - Pattern: Same validation rules across all layers
    - Documentation: Validation rules in `docs/Data_Quality.md`
    - Tests: Verify validation at each layer

62. [ ] **Add data integrity constraints** — [P1][DBA][6h][Task #30]
    - Constraints: NOT NULL, UNIQUE, CHECK, FK
    - Migration: Alembic migration adding constraints
    - Tests: Attempt to violate constraints (should fail)

### Backup & DR (P1)

63. [ ] **Implement automated backup system** — [P1][DBA][8h][None]
    - Schedule: Daily full, hourly incremental
    - Retention: 30 days online, 1 year cold storage
    - Scope: Database, config files, uploaded files
    - Exclusions: .venv, node_modules, caches, secrets
    - Tests: Restore from backup, verify data integrity

64. [ ] **Document disaster recovery runbook** — [P1][DX][4h][None]
    - File: `docs/Runbook.md` (expand existing)
    - Sections: Incident response, rollback procedures, recovery steps
    - Contacts: On-call rotation, escalation paths
    - Tests: Quarterly DR drill

### Resilience (P1)

65. [ ] **Implement circuit breakers for external dependencies** — [P1][BE][8h][None]
    - Pattern: CLOSED → OPEN (fail-fast) → HALF_OPEN (recovery probe)
    - Scope: External APIs, database, RAG, third-party services
    - Config: Failure thresholds, timeouts, retries per dependency
    - Documentation: `docs/Resilience.md` (expand existing)
    - Tests: Chaos tests simulating failures

66. [ ] **Add fallback strategies for degraded service** — [P1][BE][6h][Task #65]
    - Strategies: Cached response, stale-while-revalidate, alternate provider
    - Scope: Gold price API, market data, geocoding, etc.
    - UX: Show "using cached data" notice to users
    - Tests: Verify fallbacks activate on failures

67. [ ] **Configure timeouts and retries** — [P1][BE][4h][Task #65]
    - Pattern: Bounded retries (≤2) with exponential backoff + jitter
    - Timeouts: Client-side timeouts ≤ p95 latency × 1.5
    - Idempotency: Use idempotency keys for retried mutating calls
    - Tests: Verify retry logic, timeout enforcement

### Multi-Tenancy (P1 - If Applicable)

68. [ ] **Implement tenant isolation** — [P1][BE][16h][None]
    - Pattern: Add `tenant_id` to all tables
    - Filters: Auto-filter queries by tenant_id
    - Auth: Extract tenant from JWT token
    - Tests: Verify cross-tenant data leakage prevention

69. [ ] **Add tenant-level configuration** — [P1][BE][8h][Task #68]
    - Pattern: Settings table with tenant_id FK
    - Scope: Customizable features per tenant
    - UI: Tenant admin settings page
    - Tests: Verify tenant-specific settings isolation

70. [ ] **Implement tenant-aware rate limiting** — [P1][BE][4h][Task #32,68]
    - Pattern: Rate limits per tenant (not global)
    - Config: Different limits per tenant tier (free/pro/enterprise)
    - Tests: Verify tenant A can't exhaust tenant B's quota

---

## P2 — MEDIUM PRIORITY (Complete in 30-90 Days)

### Performance Optimization (P2)

71. [ ] **Add database query optimization** — [P2][DBA][8h][Task #31]
    - Analysis: Enable SQLAlchemy query logging, find N+1 queries
    - Optimization: Eager loading, subquery optimization
    - Caching: Redis cache for expensive queries (TTL 5 min)
    - Tests: Benchmark queries before/after optimization

72. [ ] **Implement multi-layer caching** — [P2][BE][12h][None]
    - Layers: In-memory (LRU), Redis (distributed), CDN (static assets)
    - Strategy: Cache-aside pattern, stale-while-revalidate
    - Invalidation: Explicit invalidation on data updates
    - Tests: Verify cache hits, invalidation logic

73. [ ] **Add CDN integration for static assets** — [P2][DX][6h][None]
    - Provider: CloudFront, Cloudflare, or Fastly
    - Assets: JS/CSS bundles, images, fonts
    - Config: CDN origin pointing to frontend build
    - Tests: Verify assets served from CDN, cache headers

74. [ ] **Implement lazy loading for frontend components** — [P2][FE][8h][None]
    - Pattern: React.lazy() + Suspense for route components
    - Scope: Split large pages into async chunks
    - Lighthouse: Improve performance score via code splitting
    - Tests: Verify chunks load on demand

75. [ ] **Add performance budgets** — [P2][FE][4h][Task #49]
    - Budgets: Bundle size <250KB gzipped, FCP <1.5s, TTI <3s
    - CI: webpack-bundle-analyzer, size-limit
    - Fail: Block merge if budgets exceeded
    - Tests: Lighthouse CI performance metrics

### Developer Experience (P2)

76. [ ] **Set up monorepo tooling** — [P2][DX][12h][None]
    - Tool: Nx or Turborepo
    - Structure: /packages/backend, /packages/frontend, /packages/shared-types
    - Benefits: Shared types, unified build/test commands
    - Migration: Gradual migration from current structure

77. [ ] **Add pre-commit hooks** — [P2][DX][2h][None]
    - Tool: pre-commit or husky
    - Hooks: lint, format, type-check, secret-scan
    - Config: `.pre-commit-config.yaml`
    - Tests: Verify hooks block bad commits

78. [ ] **Implement hot module replacement (HMR)** — [P2][FE][4h][None]
    - Config: Vite HMR already enabled (verify)
    - Scope: Backend Flask hot reload (already enabled)
    - Tests: Verify changes reflected without full reload

79. [ ] **Add developer documentation** — [P2][DX][8h][None]
    - File: `docs/Developer_Guide.md`
    - Sections: Setup, architecture, workflows, troubleshooting
    - Examples: Common tasks (add endpoint, add model, add page)
    - Tests: Onboarding new developer with guide

### Feature Enhancements (P2)

80. [ ] **Implement PWA features** — [P2][FE][12h][None]
    - Manifest: `/public/manifest.json` with icons
    - Service worker: Cache-first strategy for offline support
    - Install: Add to home screen prompt
    - Tests: Lighthouse PWA score >80

81. [ ] **Add Command Palette (Ctrl+K)** — [P2][FE][8h][None]
    - Library: cmdk or kbar
    - Actions: Navigate, search, create, settings
    - UI: Keyboard shortcuts overlay
    - Tests: Verify keyboard navigation works

82. [ ] **Implement advanced search** — [P2][BE+FE][16h][None]
    - Backend: Full-text search with Elasticsearch or PostgreSQL FTS
    - Frontend: Search UI with filters, facets, autocomplete
    - Scope: Products, invoices, customers
    - Tests: Search quality metrics (precision, recall)

83. [ ] **Add export functionality** — [P2][BE][8h][None]
    - Formats: Excel, CSV, PDF
    - Scope: Invoices, products, reports
    - Library: openpyxl (Excel), ReportLab (PDF)
    - Tests: Verify exports match database data

84. [ ] **Implement bulk operations** — [P2][BE+FE][12h][None]
    - Operations: Bulk create, update, delete
    - UI: Checkbox selection, bulk action dropdown
    - Backend: Batch processing with transactions
    - Tests: Verify atomicity (all or nothing)

### Analytics & Reporting (P2)

85. [ ] **Add analytics dashboard** — [P2][BE+FE][16h][None]
    - Metrics: Sales, inventory, top products, low stock alerts
    - Visualization: Chart.js or Recharts
    - Backend: Aggregation queries with caching
    - Tests: Verify metric calculations

86. [ ] **Implement user activity tracking** — [P2][BE][8h][None]
    - Events: Login, logout, create, update, delete
    - Storage: Activity log table with user_id, action, timestamp
    - Privacy: No PII in logs (only IDs)
    - Tests: Verify events logged correctly

87. [ ] **Add custom report builder** — [P2][BE+FE][20h][None]
    - UI: Drag-drop report builder (filters, grouping, sorting)
    - Backend: Dynamic query generation from UI config
    - Export: Save report configs, schedule email reports
    - Tests: Verify query generation correctness

### Internationalization (P2)

88. [ ] **Expand Arabic/English translations** — [P2][FE][8h][None]
    - Files: `frontend/src/locales/ar.json`, `en.json`
    - Coverage: 100% of UI strings
    - Tool: i18next for translation management
    - Tests: Verify no missing translation keys

89. [ ] **Add RTL layout testing** — [P2][FE][4h][None]
    - Scope: All pages and components
    - Issues: Icon placement, text alignment, margins
    - Tests: Visual regression tests for RTL

90. [ ] **Implement locale-based formatting** — [P2][FE][4h][None]
    - Scope: Dates, numbers, currency
    - Library: date-fns or Intl API
    - Locales: ar-SA, en-US
    - Tests: Verify formatting per locale

### Compliance & Privacy (P2)

91. [ ] **Add GDPR compliance features** — [P2][BE+FE][16h][None]
    - Features: Data export, deletion, consent management
    - UI: Privacy settings page, cookie consent banner
    - Backend: Data retention policies, anonymization
    - Documentation: `docs/Privacy_Policy.md`

92. [ ] **Implement audit logging** — [P2][BE][8h][None]
    - Scope: All data changes (who, what, when)
    - Storage: Immutable audit log table
    - UI: Audit log viewer for admins
    - Tests: Verify log completeness

93. [ ] **Add data anonymization for testing** — [P2][DBA][6h][None]
    - Tool: Faker for generating test data
    - Scope: Anonymize production data for staging/dev
    - Script: `scripts/anonymize_db.py`
    - Tests: Verify no real PII in anonymized data

### Infrastructure as Code (P2)

94. [ ] **Migrate to IaC (Terraform/Helm)** — [P2][DX][20h][None]
    - Tool: Terraform (cloud resources) + Helm (K8s)
    - Scope: Database, Redis, app containers, networking
    - Scanning: tfsec/checkov for security issues
    - Tests: Plan/apply in staging before production

95. [ ] **Implement GitOps workflow** — [P2][DX][12h][Task #94]
    - Tool: ArgoCD or FluxCD
    - Pattern: Git as single source of truth for infra
    - Automation: Auto-sync on git push
    - Tests: Drift detection, rollback scenarios

96. [ ] **Add Kubernetes security policies** — [P2][DX][8h][Task #94]
    - Policies: No privileged containers, runAsNonRoot
    - NetworkPolicies: Restrict pod-to-pod communication
    - Secrets: Via Vault sidecar or sealed secrets
    - Tests: kube-linter, policy enforcement tests

### Monitoring & Alerting (P2)

97. [ ] **Set up Prometheus + Grafana** — [P2][DX][12h][None]
    - Metrics: Request rate, latency, error rate, saturation
    - Dashboards: Grafana dashboards for backend, frontend, database
    - Alerting: Alert rules for SLO violations
    - Tests: Verify metrics collection, alert firing

98. [ ] **Implement log aggregation** — [P2][DX][8h][None]
    - Tool: ELK stack or Loki
    - Scope: Application logs, access logs, error logs
    - Retention: 30 days online, 1 year cold storage
    - Tests: Verify log search, dashboard creation

99. [ ] **Add uptime monitoring** — [P2][DX][4h][None]
    - Tool: Pingdom, UptimeRobot, or Datadog Synthetics
    - Checks: HTTP health check every 1 minute
    - Alerts: Notify on-call on downtime
    - Tests: Verify alerts received

### Code Quality (P2)

100. [ ] **Add mutation testing** — [P2][DX][8h][None]
     - Tool: mutpy (Python) or Stryker (JS)
     - Scope: Critical business logic
     - Threshold: 80% mutation score
     - Tests: Verify test suite catches mutations

101. [ ] **Implement static code analysis** — [P2][DX][4h][None]
     - Tool: SonarQube or CodeClimate
     - Metrics: Code smells, complexity, duplication
     - CI: Block merge on quality gate failure
     - Tests: Verify analysis runs on every PR

102. [ ] **Add dependency vulnerability scanning** — [P2][DX][2h][None]
     - Tool: Snyk, Dependabot, or Safety (Python)
     - Frequency: Daily scans
     - Alerts: Notify on high-severity CVEs
     - Tests: Verify alerts for known vulnerable packages

### Multi-Region (P2 - If Applicable)

103. [ ] **Implement multi-region deployment** — [P2][DX][24h][None]
     - Regions: US-East, EU-West (example)
     - Routing: GeoDNS for lowest latency
     - Database: Master-replica replication
     - Tests: Verify region failover

104. [ ] **Add data replication strategy** — [P2][DBA][16h][Task #103]
     - Pattern: Master-replica with async replication
     - Conflict resolution: Last-write-wins or CRDT
     - Lag: Monitor replication lag (alert >5s)
     - Tests: Verify data consistency across regions

---

## P3 — LOW PRIORITY (Nice-to-Have, 90+ Days)

### Advanced Features (P3)

105. [ ] **Implement webhooks** — [P3][BE][12h][None]
     - Events: Invoice created, product updated, etc.
     - Config: Webhook URLs in settings
     - Retry: Exponential backoff on failures
     - Tests: Verify webhook delivery

106. [ ] **Add GraphQL API** — [P3][BE][20h][None]
     - Library: Graphene (Python)
     - Schema: Mirror REST API in GraphQL
     - Benefits: Flexible querying, reduced over-fetching
     - Tests: GraphQL query tests

107. [ ] **Implement real-time notifications** — [P3][BE+FE][16h][None]
     - Protocol: WebSockets or Server-Sent Events
     - Events: Low stock alerts, new invoice, etc.
     - UI: Toast notifications
     - Tests: Verify real-time delivery

108. [ ] **Add collaborative editing** — [P3][FE][24h][None]
     - Library: Yjs or automerge for CRDT
     - Scope: Simultaneous invoice editing
     - Conflict resolution: Operational transforms
     - Tests: Verify conflict resolution

### Machine Learning (P3)

109. [ ] **Implement demand forecasting** — [P3][BE][32h][None]
     - Model: ARIMA or Prophet for time series
     - Data: Historical sales data
     - Output: Predicted demand per product
     - Tests: Evaluate forecast accuracy (MAPE)

110. [ ] **Add anomaly detection** — [P3][BE][24h][None]
     - Model: Isolation Forest or autoencoder
     - Scope: Unusual transactions, inventory discrepancies
     - Alerts: Notify on anomalies
     - Tests: Verify detection of synthetic anomalies

111. [ ] **Implement recommendation engine** — [P3][BE][28h][None]
     - Model: Collaborative filtering or content-based
     - Scope: Recommend products to customers
     - UI: Recommendations widget
     - Tests: Evaluate recommendation quality

### Advanced UI (P3)

112. [ ] **Add data visualization library** — [P3][FE][12h][None]
     - Library: D3.js or Apache ECharts
     - Scope: Custom charts for reports
     - Examples: Sankey diagrams, heatmaps
     - Tests: Visual regression tests

113. [ ] **Implement drag-and-drop dashboard** — [P3][FE][16h][None]
     - Library: react-grid-layout
     - Scope: Customizable dashboard widgets
     - Persistence: Save layout per user
     - Tests: Verify layout persistence

114. [ ] **Add animations and micro-interactions** — [P3][FE][12h][None]
     - Library: Framer Motion or react-spring
     - Scope: Page transitions, button states, loading
     - Performance: Use CSS transforms, avoid layout thrashing
     - Tests: Performance impact measurement

### Infrastructure Enhancements (P3)

115. [ ] **Implement auto-scaling** — [P3][DX][16h][None]
     - Metrics: CPU, memory, request rate
     - Scaling: Horizontal pod autoscaling (K8s)
     - Limits: Min 2, max 10 replicas
     - Tests: Load test triggering scale-up

116. [ ] **Add blue-green deployment** — [P3][DX][12h][None]
     - Pattern: Two identical environments (blue=live, green=staging)
     - Cutover: Instant traffic switch via load balancer
     - Rollback: Switch back to blue if issues
     - Tests: Zero-downtime deployment test

117. [ ] **Implement canary releases** — [P3][DX][16h][None]
     - Pattern: Route 10% traffic to new version
     - Monitoring: Compare error rates, latency
     - Auto-rollback: Revert if metrics degrade
     - Tests: Verify gradual rollout

### Documentation & Knowledge Management (P3)

118. [ ] **Add interactive API documentation** — [P3][BE][8h][Task #24]
     - Tool: Swagger UI or Redoc
     - Features: Try-it-out, code samples
     - URL: `/api/docs`
     - Tests: Verify all endpoints documented

119. [ ] **Implement docs-as-code** — [P3][DX][8h][None]
     - Tool: MkDocs with Material theme
     - Source: Markdown files in `/docs`
     - Versioning: Version docs alongside code
     - Tests: Build docs on every PR

120. [ ] **Add ADR (Architecture Decision Records)** — [P3][DX][4h][None]
     - Location: `/docs/adr/`
     - Template: MADR (Markdown ADR)
     - Process: Document all significant decisions
     - Tests: Review ADRs in design meetings

### Security Enhancements (P3)

121. [ ] **Implement SSO (Single Sign-On)** — [P3][BE+FE][20h][None]
     - Protocol: SAML 2.0 or OAuth2/OIDC
     - Providers: Okta, Auth0, Azure AD
     - UI: SSO login button
     - Tests: End-to-end SSO flow

122. [ ] **Add SCIM provisioning** — [P3][BE][16h][Task #121]
     - Protocol: SCIM 2.0
     - Scope: Auto-provision users from IdP
     - Endpoints: /scim/v2/Users, /scim/v2/Groups
     - Tests: Verify user sync from IdP

123. [ ] **Implement SIEM integration** — [P3][BE][12h][None]
     - Tool: Splunk, ELK, or QRadar
     - Data: Security logs, audit logs
     - Alerts: Suspicious activity detection
     - Tests: Verify log ingestion

### Performance & Optimization (P3)

124. [ ] **Add HTTP/2 support** — [P3][DX][4h][None]
     - Server: Gunicorn with HTTP/2 (or nginx proxy)
     - Benefits: Multiplexing, header compression
     - Tests: Verify HTTP/2 enabled

125. [ ] **Implement database connection pooling** — [P3][BE][4h][None]
     - Library: SQLAlchemy pool (already enabled, tune)
     - Config: Max pool size 20, overflow 10
     - Tests: Verify connection reuse

126. [ ] **Add compression middleware** — [P3][BE][2h][None]
     - Library: Flask-Compress
     - Scope: Gzip/Brotli for responses >1KB
     - Tests: Verify response compression

### Testing Enhancements (P3)

127. [ ] **Add contract testing** — [P3][BE+FE][12h][None]
     - Tool: Pact
     - Scope: Frontend-backend API contracts
     - Tests: Verify consumer-provider contract compatibility

128. [ ] **Implement chaos engineering** — [P3][DX][16h][None]
     - Tool: Chaos Monkey or Litmus Chaos
     - Tests: Random pod kills, network latency, CPU stress
     - Observability: Verify system resilience
     - Schedule: Monthly chaos days

129. [ ] **Add property-based testing** — [P3][BE][8h][None]
     - Tool: Hypothesis (Python)
     - Scope: Business logic with invariants
     - Tests: Generate random inputs, verify properties

### Accessibility (P3)

130. [ ] **Add screen reader testing** — [P3][FE][8h][None]
     - Tools: NVDA, JAWS, VoiceOver
     - Scope: All pages and components
     - Tests: Manual testing with screen readers

131. [ ] **Implement keyboard navigation** — [P3][FE][8h][None]
     - Scope: All interactive elements
     - Pattern: Tab order, focus traps, skip links
     - Tests: Verify full keyboard navigation

132. [ ] **Add high-contrast mode** — [P3][FE][6h][None]
     - Pattern: Detect prefers-contrast media query
     - Tokens: High-contrast color palette
     - Tests: Verify contrast ratios WCAG AAA

### Localization (P3)

133. [ ] **Add third language support** — [P3][FE][12h][None]
     - Language: French/German/Spanish (TBD)
     - Files: `frontend/src/locales/{locale}.json`
     - Tests: Verify translations complete

134. [ ] **Implement currency localization** — [P3][BE+FE][8h][None]
     - Scope: Multi-currency support
     - Conversion: Real-time exchange rates API
     - UI: Currency selector
     - Tests: Verify currency calculations

### DevEx & Tooling (P3)

135. [ ] **Add Storybook for component library** — [P3][FE][12h][None]
     - Tool: Storybook
     - Scope: All reusable components
     - Benefits: Isolated component development
     - Tests: Visual regression with Chromatic

136. [ ] **Implement hot code reloading** — [P3][BE][8h][None]
     - Tool: Watchdog or similar
     - Scope: Flask auto-reload (already enabled, optimize)
     - Tests: Verify changes reflected instantly

137. [ ] **Add code generation templates** — [P3][DX][8h][None]
     - Tool: Plop or custom scripts
     - Templates: New model, new endpoint, new page
     - Tests: Verify generated code compiles

### Business Intelligence (P3)

138. [ ] **Add BI dashboard integration** — [P3][BE][16h][None]
     - Tool: Metabase, Superset, or Tableau
     - Data: Read-replica database connection
     - UI: Embedded BI iframes
     - Tests: Verify dashboard load

139. [ ] **Implement data warehouse** — [P3][DBA][32h][None]
     - Tool: Snowflake or BigQuery
     - ETL: Daily data pipeline from production DB
     - Purpose: Analytics, reporting, ML training
     - Tests: Verify data freshness

### Legacy Cleanup (P3)

140. [ ] **Remove all duplicate models** — [P3][DBA][8h][Task #29]
     - Action: Delete invoice.py, invoices.py (keep unified_invoice.py)
     - Action: Delete product_advanced.py (keep product_unified.py)
     - Clean: Move to `/backend/unneeded/` with pointers
     - Tests: Verify no broken imports

141. [ ] **Archive unused scripts** — [P3][DX][4h][None]
     - Scope: Root-level test/migration scripts
     - Action: Move to `/scripts/archive/` with README
     - Clean: Keep only actively used scripts in root
     - Tests: Verify no CI dependencies on archived scripts

142. [ ] **Refactor monolithic files** — [P3][BE][16h][None]
     - Targets: Files >1000 lines
     - Action: Split into smaller modules
     - Pattern: Single responsibility principle
     - Tests: Verify behavior unchanged after refactor

---

## COMPLETION CRITERIA

### P0 Tasks (Critical - 23 tasks)

- **Deadline**: 7 days from audit date (2025-10-31)
- **Blocking**: Production deployment MUST NOT proceed until P0 complete
- **Owner**: Security Lead + Backend Team
- **Verification**: All P0 security tests passing, no critical vulnerabilities

### P1 Tasks (High Priority - 47 tasks)

- **Deadline**: 30 days from audit date (2025-11-23)
- **Impact**: Major security/functionality gaps addressed
- **Owner**: Full team (BE/FE/DBA/DX)
- **Verification**: 80% test coverage, API contracts complete, CI gates passing

### P2 Tasks (Medium Priority - 54 tasks)

- **Deadline**: 90 days from audit date (2026-01-22)
- **Impact**: Performance, UX, monitoring improvements
- **Owner**: Full team + specialized roles
- **Verification**: Lighthouse budgets met, observability dashboards live

### P3 Tasks (Low Priority - 18 tasks)

- **Deadline**: 180+ days (ongoing)
- **Impact**: Nice-to-have features, advanced capabilities
- **Owner**: As capacity allows
- **Verification**: Feature-specific acceptance criteria

---

## REFERENCES

- **Audit Report**: `docs/COMPREHENSIVE_AUDIT_2025-10-24.md`
- **Global Guidelines**: `GLOBAL_GUIDELINES_v2.3.txt`
- **Security Documentation**: `docs/Security.md`
- **API Contracts**: `docs/API_Contracts.md`
- **Database Schema**: `docs/DB_Schema.md`
- **Resilience Guide**: `docs/Resilience.md`

---

**Last Updated**: 2025-10-24
**Next Review**: 2025-10-31 (after P0 completion)
**Status Tracking**: GitHub Project Board (to be created per task #51)
