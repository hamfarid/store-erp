# FILE: docs/Remediation_Plan.md | PURPOSE: Prioritized fix backlog | OWNER: Engineering | RELATED: docs/Security.md, docs/Threat_Model.md, docs/Task_List.md | LAST-AUDITED: 2025-10-21

# Remediation Plan — نظام إدارة المخزون العربي

**Version**: 2.0
**Last Updated**: 2025-10-21
**Status**: 🔴 **Critical Fixes Required**

---

## 1. Executive Summary

Based on comprehensive analysis (Security.md, Threat_Model.md, Pages_Coverage.md), the system requires **289 security fixes** and **66 hours of frontend work** before production readiness.

**Overall OSF Score**: 0.12/1.0 (Critical)

- Security: 0.0/1.0 (18 critical vulnerabilities)
- Software Engineering: 0.36/1.0
- UI/UX: 0.6/1.0

**Estimated Total Effort**: 180-240 hours (4-6 weeks with 2 engineers)

---

## 2. Prioritization Framework

| Priority | Criteria | Response Time |
|----------|----------|---------------|
| **P0 (Critical)** | Security breach risk, data loss, system down | Fix within 24 hours |
| **P1 (High)** | Degraded functionality, compliance violation | Fix within 1 week |
| **P2 (Medium)** | UX issues, performance degradation | Fix within 1 month |
| **P3 (Low)** | Nice-to-have, technical debt | Backlog |

---

## 3. Phase 1: Critical Security Fixes (P0) — 2 Weeks

**Goal**: Eliminate critical vulnerabilities (CVSS ≥8.0)

### 3.1 Authentication & Authorization (40 hours)

| Task | CVSS | Effort | Owner | Status |
|------|------|--------|-------|--------|
| **SEC-001**: Implement JWT rotation with 15-min TTL | 9.1 | 6h | Backend | ❌ Not Started |
| **SEC-002**: Add HttpOnly/Secure/SameSite to cookies | 8.8 | 3h | Backend | ❌ Not Started |
| **SEC-003**: Implement CSRF protection (double-submit) | 8.2 | 4h | Backend | ❌ Not Started |
| **SEC-004**: Add account lockout (5 failed attempts) | 9.1 | 4h | Backend | ❌ Not Started |
| **SEC-005**: Implement rate limiting (100 req/hour) | 8.5 | 5h | Backend | ❌ Not Started |
| **SEC-006**: Add MFA support (TOTP) | 8.0 | 8h | Backend | ❌ Not Started |
| **SEC-007**: Fix missing authorization checks (13 endpoints) | 9.1 | 10h | Backend | ❌ Not Started |

**Acceptance Criteria**:

- [ ] JWT access token TTL ≤900 seconds
- [ ] All cookies have `HttpOnly; Secure; SameSite=Strict`
- [ ] CSRF token validated on all state-changing requests
- [ ] Account locked after 5 failed login attempts
- [ ] Rate limit enforced: 100 requests/hour per IP
- [ ] MFA optional but functional
- [ ] All endpoints check permissions via `authorize()` function

**Tests**:

```bash
pytest tests/test_auth.py::test_jwt_rotation
pytest tests/test_csrf.py::test_csrf_protection
pytest tests/test_rate_limit.py::test_rate_limit_enforced
```

---

### 3.2 SQL Injection Prevention (16 hours)

| Task | CVSS | Effort | Owner | Status |
|------|------|--------|-------|--------|
| **SEC-008**: Audit all raw SQL queries (23 found) | 9.8 | 6h | Backend | ❌ Not Started |
| **SEC-009**: Replace with parameterized queries | 9.8 | 8h | Backend | ❌ Not Started |
| **SEC-010**: Add SQLAlchemy query validation | 8.0 | 2h | Backend | ❌ Not Started |

**Acceptance Criteria**:

- [ ] Zero raw SQL queries with string interpolation
- [ ] All queries use SQLAlchemy ORM or parameterized statements
- [ ] CI gate blocks raw SQL patterns

---

### 3.3 Secrets Management (12 hours)

| Task | CVSS | Effort | Owner | Status |
|------|------|--------|-------|--------|
| **SEC-011**: Migrate secrets to AWS KMS/Vault | 9.1 | 8h | DevOps | ❌ Not Started |
| **SEC-012**: Remove secrets from .env (git history) | 9.1 | 2h | DevOps | ❌ Not Started |
| **SEC-013**: Implement secret rotation (90-day TTL) | 8.0 | 2h | DevOps | ❌ Not Started |

**Acceptance Criteria**:

- [ ] All production secrets stored in KMS/Vault
- [ ] `.env` files removed from git history
- [ ] Secret rotation automated (90-day TTL)
- [ ] CI gate blocks literal secrets in code

---

### 3.4 XSS Prevention (8 hours)

| Task | CVSS | Effort | Owner | Status |
|------|------|--------|-------|--------|
| **SEC-014**: Implement CSP with nonces | 8.8 | 4h | Backend + Frontend | ❌ Not Started |
| **SEC-015**: Sanitize all user inputs (React) | 8.0 | 3h | Frontend | ❌ Not Started |
| **SEC-016**: Add Content-Type validation | 7.5 | 1h | Backend | ❌ Not Started |

---

### 3.5 HTTPS & Transport Security (6 hours)

| Task | CVSS | Effort | Owner | Status |
|------|------|--------|-------|--------|
| **SEC-017**: Enforce HTTPS in production | 8.5 | 2h | DevOps | ❌ Not Started |
| **SEC-018**: Add HSTS header (max-age=31536000) | 8.0 | 1h | Backend | ❌ Not Started |
| **SEC-019**: Disable TLS 1.0/1.1 (require TLS 1.2+) | 7.8 | 2h | DevOps | ❌ Not Started |
| **SEC-020**: Implement certificate pinning (optional) | 7.0 | 1h | Frontend | ❌ Not Started |

---

## 4. Phase 2: High-Priority Fixes (P1) — 3 Weeks

### 4.1 Frontend Pages & Buttons (66 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **FE-001**: Fix invoice form calculations (tax/discount) | P1 | 4h | Frontend | ❌ Not Started |
| **FE-002**: Wire delete buttons on ProductList | P1 | 2h | Frontend | ❌ Not Started |
| **FE-003**: Add permission checks to Edit/Delete buttons | P1 | 4h | Frontend | ❌ Not Started |
| **FE-004**: Implement Product Detail page | P1 | 4h | Frontend | ❌ Not Started |
| **FE-005**: Implement Invoice Detail page | P1 | 6h | Frontend | ❌ Not Started |
| **FE-006**: Implement Customer List & Form | P1 | 8h | Frontend | ❌ Not Started |
| **FE-007**: Implement User Form | P1 | 4h | Frontend | ❌ Not Started |
| **FE-008**: Implement Inventory List | P1 | 6h | Frontend | ❌ Not Started |
| **FE-009**: Wire Dashboard quick actions | P1 | 2h | Frontend | ❌ Not Started |
| **FE-010**: Add confirmation dialogs (destructive actions) | P1 | 3h | Frontend | ❌ Not Started |

---

### 4.2 API Alignment & Validation (24 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **API-001**: Refresh OpenAPI spec (contracts/openapi.yaml) | P1 | 4h | Backend | ❌ Not Started |
| **API-002**: Generate typed frontend client | P1 | 3h | Frontend | ❌ Not Started |
| **API-003**: Add request/response validators (Marshmallow) | P1 | 8h | Backend | ❌ Not Started |
| **API-004**: Standardize error envelope | P1 | 4h | Backend | ❌ Not Started |
| **API-005**: Add API drift tests | P1 | 5h | Backend | ❌ Not Started |

---

### 4.3 Database Relations & Integrity (16 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **DB-001**: Add foreign key constraints (12 missing) | P1 | 4h | Backend | ❌ Not Started |
| **DB-002**: Add unique constraints (5 missing) | P1 | 2h | Backend | ❌ Not Started |
| **DB-003**: Add check constraints (price ≥0, qty ≥0) | P1 | 2h | Backend | ❌ Not Started |
| **DB-004**: Add indexes (foreign keys, search columns) | P1 | 4h | Backend | ❌ Not Started |
| **DB-005**: Wrap mutations in transactions | P1 | 4h | Backend | ❌ Not Started |

---

### 4.4 Logging & Observability (12 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **OBS-001**: Implement structured logging (JSON) | P1 | 4h | Backend | ❌ Not Started |
| **OBS-002**: Add traceId to all logs/errors | P1 | 3h | Backend | ❌ Not Started |
| **OBS-003**: Redact secrets from logs | P1 | 2h | Backend | ❌ Not Started |
| **OBS-004**: Add performance metrics (response time) | P1 | 3h | Backend | ❌ Not Started |

---

## 5. Phase 3: Medium-Priority Fixes (P2) — 4 Weeks

### 5.1 UI/UX Improvements (34 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **UI-001**: Implement Supplier List & Form | P2 | 8h | Frontend | ❌ Not Started |
| **UI-002**: Implement Stock Movements page | P2 | 4h | Frontend | ❌ Not Started |
| **UI-003**: Implement Reports Dashboard | P2 | 3h | Frontend | ❌ Not Started |
| **UI-004**: Implement Sales Report | P2 | 6h | Frontend | ❌ Not Started |
| **UI-005**: Implement Settings page | P2 | 5h | Frontend | ❌ Not Started |
| **UI-006**: Add export functionality (Excel) | P2 | 4h | Frontend | ❌ Not Started |
| **UI-007**: Add advanced filters (date range, status) | P2 | 4h | Frontend | ❌ Not Started |

---

### 5.2 Performance Optimization (20 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **PERF-001**: Add pagination (all list endpoints) | P2 | 6h | Backend | ❌ Not Started |
| **PERF-002**: Implement caching (Redis) | P2 | 8h | Backend | ❌ Not Started |
| **PERF-003**: Optimize N+1 queries (joinedload) | P2 | 4h | Backend | ❌ Not Started |
| **PERF-004**: Add database connection pooling | P2 | 2h | Backend | ❌ Not Started |

---

### 5.3 Testing & QA (24 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **TEST-001**: Write unit tests (target 80% coverage) | P2 | 12h | Backend | ❌ Not Started |
| **TEST-002**: Write E2E tests (Playwright) | P2 | 8h | Frontend | ❌ Not Started |
| **TEST-003**: Add negative tests (invalid inputs) | P2 | 4h | Backend | ❌ Not Started |

---

## 6. Phase 4: Low-Priority & Technical Debt (P3) — Backlog

### 6.1 Advanced Features (40 hours)

| Task | Priority | Effort | Owner | Status |
|------|----------|--------|-------|--------|
| **FEAT-001**: Implement Warehouse Management | P3 | 8h | Backend + Frontend | ❌ Not Started |
| **FEAT-002**: Implement Category Management | P3 | 4h | Backend + Frontend | ❌ Not Started |
| **FEAT-003**: Add bulk actions (bulk delete, bulk update) | P3 | 6h | Frontend | ❌ Not Started |
| **FEAT-004**: Implement advanced search (full-text) | P3 | 8h | Backend | ❌ Not Started |
| **FEAT-005**: Add email notifications | P3 | 6h | Backend | ❌ Not Started |
| **FEAT-006**: Implement audit log viewer | P3 | 4h | Frontend | ❌ Not Started |
| **FEAT-007**: Add data export (PDF reports) | P3 | 4h | Backend | ❌ Not Started |

---

## 7. Progress Tracking

**Overall Progress**: 0% (0/289 fixes completed)

| Phase | Tasks | Completed | In Progress | Not Started | % Complete |
|-------|-------|-----------|-------------|-------------|------------|
| Phase 1 (P0) | 20 | 0 | 0 | 20 | 0% |
| Phase 2 (P1) | 25 | 0 | 0 | 25 | 0% |
| Phase 3 (P2) | 15 | 0 | 0 | 15 | 0% |
| Phase 4 (P3) | 13 | 0 | 0 | 13 | 0% |
| **Total** | **73** | **0** | **0** | **73** | **0%** |

---

## References

- Security Posture: `/docs/Security.md`
- Threat Model: `/docs/Threat_Model.md`
- Pages Coverage: `/docs/Pages_Coverage.md`
- Task List: `/docs/Task_List.md`
