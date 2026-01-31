# Implementation Plan: Gaara ERP v12 - Master System

**Branch**: `gaara-erp` | **Date**: 2026-01-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/gaara-erp/spec.md`

**Note**: This plan covers the comprehensive ERP system with focus on Phase 0 Critical Stability priorities: Multi-Tenancy, MFA Security, HR Module, Projects Module.

## Summary

Gaara ERP v12 is a comprehensive enterprise resource planning system targeting **top 5 global ERP systems** within two years. The system comprises 94 modules (41 complete, 13 partial, 21 missing) with specialized agricultural (10 modules) and AI capabilities (13 modules). This plan prioritizes the critical Phase 0 requirements: complete Multi-Tenancy implementation, MFA security hardening, and creation of HR/Projects/Contacts modules.

**Primary technical approach**: Django 4.x backend with PostgreSQL multi-schema isolation for tenant separation, React 18 frontend, Redis caching, Celery task queue, and external AI integrations (OpenAI API).

## Technical Context

**Language/Version**: Python 3.11+ (Backend), JavaScript/TypeScript (Frontend React 18)  
**Primary Dependencies**: Django 4.x, Django REST Framework 3.14+, React 18, Redux, Material-UI/Ant Design, Celery 5.x  
**Storage**: PostgreSQL 15.x (Multi-Schema per tenant), Redis 7.x (Cache + Sessions + Queue)  
**Testing**: pytest, Jest, Playwright (E2E)  
**Target Platform**: Linux server (Docker/Kubernetes), Web browsers, Mobile-responsive  
**Project Type**: Web application (Frontend + Backend + AI Service layers)  
**Performance Goals**: API response < 200ms, Page load < 2 seconds, Redis cache hit > 80%, 1000 concurrent users  
**Constraints**: JWT access 1h / refresh 24h, Rate limiting 100 req/min, 80%+ test coverage mandatory  
**Scale/Scope**: Multi-tenant SaaS, 94 modules, ~500,000+ LOC, 963 React components, 10 Agricultural + 13 AI modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles from Constitution (CONSTITUTION.md)

| Gate | Principle | Status | Notes |
|------|-----------|--------|-------|
| ✅ | **OSF Framework** - Security 35%, Correctness 20%, Reliability 15%, Performance 10%, Maintainability 10%, Scalability 10% | PASS | All designs must prioritize security |
| ✅ | **Zero-Tolerance Rules** - No hardcoded secrets, No SQL Injection, No XSS, No unhandled errors, 80%+ test coverage, No undocumented code, DRY, No uncommitted changes | PASS | Plan adheres to all 10 rules |
| ✅ | **MFA Mandatory** - SMS OTP, TOTP (Google Auth), Email OTP | PASS | Phase 0 priority SEC-03 to SEC-05 |
| ✅ | **Encryption Standards** - AES-256 for sensitive data, bcrypt/Argon2 for passwords, TLS 1.3 | PASS | Following constitution requirements |
| ✅ | **Multi-Tenancy Schema Isolation** - Each tenant in separate PostgreSQL schema | PASS | Phase 0 priority MT-01 to MT-06 |
| ✅ | **JWT Policy** - 1h access token, 24h refresh token | PASS | SEC-01, SEC-02 already exist |
| ✅ | **Rate Limiting** - All API endpoints protected | PASS | SEC-07 already exists |
| ✅ | **Verification Oath** - Check file_registry.json, read specs, verify imports, no hallucinations | PASS | Following Librarian Protocol |
| ✅ | **Speckit SDD** - No code without spec | PASS | This plan follows speckit workflow |

### Pre-Design Gate: **PASSED** ✅

All constitution principles are accounted for. No violations require justification.

## Project Structure

### Documentation (this feature)

```text
specs/gaara-erp/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Master system specification (copied from 5-gaara_erp/specs/)
├── research.md          # Phase 0 output - Technical research and decisions
├── data-model.md        # Phase 1 output - Entity relationships and schemas
├── quickstart.md        # Phase 1 output - Developer onboarding guide
├── contracts/           # Phase 1 output - API contracts (OpenAPI)
│   ├── auth-api.yaml    # Authentication & MFA endpoints
│   ├── tenant-api.yaml  # Multi-tenancy endpoints
│   ├── hr-api.yaml      # HR module endpoints
│   └── projects-api.yaml # Projects module endpoints
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root: D:\Ai_Project\5-gaara_erp)

```text
# Selected: Option 2 - Web application (Frontend + Backend)

backend/
├── src/
│   ├── models/                    # Database models (existing + new)
│   │   ├── tenant.py              # [NEW] Multi-tenancy model
│   │   ├── accounting_system.py   # ✅ Existing
│   │   ├── customer.py            # ✅ Existing
│   │   ├── invoice_unified.py     # ✅ Existing
│   │   └── ...
│   ├── modules/                   # Feature modules
│   │   ├── hr/                    # [NEW] HR Module
│   │   │   ├── models/
│   │   │   │   ├── employee.py
│   │   │   │   ├── attendance.py
│   │   │   │   ├── leave.py
│   │   │   │   └── payroll.py
│   │   │   └── views/
│   │   ├── projects/              # [NEW] Projects Module
│   │   │   ├── models/
│   │   │   │   ├── project.py
│   │   │   │   └── task.py
│   │   │   └── views/
│   │   ├── contacts/              # [NEW] Contacts Module
│   │   │   ├── models/
│   │   │   └── views/
│   │   └── mfa/                   # ⏳ Partial - needs completion
│   ├── middleware/
│   │   ├── tenant_middleware.py   # [NEW] Tenant context middleware
│   │   └── rate_limiter.py        # ✅ Existing
│   ├── services/
│   │   └── tenant_service.py      # [NEW] Tenant management service
│   └── routes/                    # API routes
│       ├── auth_unified.py        # ✅ Existing
│       └── ...
└── tests/
    ├── contract/                  # API contract tests
    ├── integration/               # Integration tests
    └── unit/                      # Unit tests

frontend/
├── src/
│   ├── components/               # 963 React components (existing)
│   ├── pages/                    # Page components
│   │   ├── hr/                   # [NEW] HR pages
│   │   ├── projects/             # [NEW] Projects pages
│   │   └── tenant-admin/         # [NEW] Tenant admin pages
│   └── services/                 # API service clients
└── tests/

gaara-erp-frontend/               # Unified frontend (alternate)

ai_service/                       # AI service layer
├── plant_diagnosis/              # ✅ Existing
└── ...
```

**Structure Decision**: Web application architecture with Django backend (94 modules), React frontend (963 components), and AI service layer. Multi-tenant isolation via PostgreSQL schema separation. Following existing project structure conventions.

## Complexity Tracking

> **No Constitution violations requiring justification. All designs adhere to core principles.**

| Aspect | Decision | Constitutional Alignment |
|--------|----------|-------------------------|
| Multi-Schema Tenancy | PostgreSQL schema per tenant | ✅ Constitution §2.2 MT-01 mandate |
| MFA Implementation | 3-method (SMS, TOTP, Email) | ✅ Constitution §2.3 mandatory |
| Security Weight | 35% priority in all decisions | ✅ OSF Framework compliance |
| Test Coverage | 80%+ mandatory | ✅ Zero-Tolerance Rule #5 |

---

## Phase 0: Research & Clarifications

### Research Tasks

Based on Technical Context analysis, the following research is required:

| ID | Topic | Purpose | Status |
|----|-------|---------|--------|
| R-01 | Django Multi-Tenancy Best Practices | Schema isolation patterns, middleware design | 📋 Pending |
| R-02 | MFA Implementation Patterns | TOTP libraries, SMS providers, security flows | 📋 Pending |
| R-03 | PostgreSQL Schema Management | Migration strategies, connection pooling per schema | 📋 Pending |
| R-04 | HR Module Data Models | Industry standard HR schemas (employees, payroll, leave) | 📋 Pending |
| R-05 | Project Management Patterns | Task hierarchy, Gantt chart data structures | 📋 Pending |
| R-06 | Django-Celery Integration | Background task patterns for AI/long-running operations | 📋 Pending |

### Clarifications Resolved

No NEEDS CLARIFICATION items - all technical context is specified in the Constitution and Master Spec.

---

## Phase 1: Design Artifacts

### Deliverables Checklist

- [ ] `research.md` - Consolidated research findings
- [ ] `data-model.md` - Entity definitions and relationships
- [ ] `contracts/auth-api.yaml` - Authentication + MFA OpenAPI spec
- [ ] `contracts/tenant-api.yaml` - Multi-tenancy OpenAPI spec
- [ ] `contracts/hr-api.yaml` - HR module OpenAPI spec
- [ ] `contracts/projects-api.yaml` - Projects module OpenAPI spec
- [ ] `quickstart.md` - Developer onboarding guide

---
