FILE: .github/copilot-instructions.md | PURPOSE: Copilot/Agent instructions + Task List for gaara-store | OWNER: Maintainers | RELATED: GLOBAL_GUIDELINES v2.3 | LAST-AUDITED: 2025-10-25
<!-- cSpell:disable -->


# Store Management System v1.6 - AI Agent Instructions

## Architecture Overview

This is a full-stack **bilingual inventory management system** (Arabic/English) with Flask backend and React frontend.

### Key Components
- **Backend**: Flask app at `backend/` with SQLAlchemy models, JWT auth, and unified database schema
- **Frontend**: React/Vite SPA at `frontend/` with Tailwind CSS and shadcn/ui components
- **Database**: SQLite with unified models after refactoring duplicated schemas
- **API**: RESTful with standardized JSON responses (success `{success, data, message}`, error `{success:false, code, message, details?, traceId}`)

### Critical File Structure
```
backend/
├── src/
│   ├── main.py              # Main Flask app entry point
│   ├── app.py              # App factory pattern
│   ├── models/unified_*.py  # Unified database models (avoid duplicates)
│   ├── routes/             # API endpoints by domain
│   └── services/           # Business logic layer
├── wsgi.py                 # Production WSGI entry
└── requirements.txt        # Python dependencies

frontend/
├── src/
│   ├── components/         # React components
│   ├── pages/             # Route components
│   └── utils/api.js       # Axios API client
└── package.json           # Node.js dependencies
```

## Development Workflows

### Quick Start Commands
```bash
# Backend (Python 3.11 required)
cd backend && .venv311\Scripts\activate && python wsgi.py

# Frontend
cd frontend && npm run dev

# Database setup
python backend/create_admin.py  # Creates default admin user
```

### Available VS Code Tasks
- **"Start backend (dev)"** - Development server with debug
- **"Start backend (gunicorn)"** - Production server
- **"Run tests (pytest)"** - Backend test suite
- **"Format (Black)"** - Python code formatting
- **"Lint (Flake8)"** - Python linting

### Docker Deployment
```bash
docker compose -f docker-compose.wsgi.yml up
```

## Code Patterns & Conventions

### Database Models
- **Use unified models**: `models/unified_models.py`, `models/user_unified.py` etc.
- **Avoid duplicates**: Legacy models like `models/invoice.py` and `models/invoices.py` were consolidated
- **Mock fallbacks**: All models have SQLAlchemy import fallbacks for missing dependencies
- **Audit trails**: Models include `created_at`, `updated_at`, activity logging

### API Response Format
All endpoints return standardized JSON envelopes.

```json
// Success
{
  "success": true,
  "data": { ... },
  "message": "عملية ناجحة"
}

// Error (unified envelope)
{
  "success": false,
  "code": "AUTH_INVALID",
  "message": "بيانات اعتماد غير صحيحة",
  "details": null,
  "traceId": "<uuid>"
}

// Paginated
{
  "success": true,
  "data": [...],
  "pagination": { "page": 1, "pageSize": 20, "total": 125, "totalPages": 7 }
}
```

### Authentication System
- **JWT tokens**: Access (15m) + Refresh (7 days), rotation + revocation on logout
- **RBAC**: Role-based permissions (`admin`, `manager`, `user`)
- **Password security**: Argon2id (recommended) or bcrypt; failed-attempt tracking + lockout
- **Default admin**: `admin/admin123` (change in production)

### Frontend Architecture
- **React Router v6** for navigation
- **Axios** for API calls with interceptors
- **shadcn/ui + Tailwind** for components
- **RTL support** for Arabic text
- **Form validation** with react-hook-form + Zod

## Integration Points

### Frontend-Backend Communication
- **Base URL**: `http://localhost:5002` (backend), `http://localhost:5502` (frontend)
- **CORS**: Configured for development ports
- **API client**: `frontend/src/utils/api.js` handles auth headers and error responses

### External Dependencies
- **RAG system**: Optional feature flag `FEATURE_RAG_ENABLED` with ChromaDB
- **File uploads**: Excel/CSV import with pandas processing
- **PDF generation**: ReportLab for Arabic-compatible reports
- **Backup system**: Local/cloud backup with configurable providers

### Environment Configuration
- **Development**: Use `.env` file (copy from `.env.example`)
- **Production**: HTTPS + HSTS required; set `FLASK_ENV=production`, set `BASE_URL`/`API_BASE_URL` to https://, enable Redis caching, Sentry monitoring
- **Feature flags**: Toggle RAG, analytics, notifications via environment variables

## Critical Development Notes

### Database Migrations
- **Migration scripts**: Use `backend/database_migration_*.py` for schema changes
- **Unified models**: Always update unified models, not legacy duplicates
- **Admin creation**: Run `python create_admin.py` after database changes

### Security Considerations
- **JWT secrets**: Change `SECRET_KEY` and `JWT_SECRET_KEY` in production
- **Rate limiting**: Configured via Flask-Limiter
- **CSRF protection**: Enabled by default with Flask-WTF
- **Military-grade security**: Optional enhanced security features available

### Performance Optimization
- **Database indexes**: Defined in schema for key lookup fields
- **Caching**: Redis support for session and query caching
- **File compression**: Vite build optimization for frontend assets
- **SQL optimization**: Use unified models to avoid N+1 queries

### Troubleshooting
- **Import errors**: Models have fallback mocks for missing SQLAlchemy
- **Port conflicts**: Backend (5002), Frontend (5502) - configurable via env
- **Database issues**: Use `python reset_db.py` to recreate from scratch
- **Build failures**: Check `make quickcheck` for dependency issues

## Testing Strategy
- **Backend**: pytest with fixtures in `backend/tests/`
- **API testing**: Use `test_all_apis.py` for endpoint validation
- **Frontend**: Vitest for component testing
- **Integration**: Full system tests via `comprehensive_system_test.py`

Remember: This system prioritizes **Arabic language support**, **security**, and **maintainable code structure** over rapid development. Always test bilingual content and validate Arabic text rendering.

GLOBAL DESIGN & EXECUTION PROMPT v3.0 — COMPLETE EDITION

Guidelines: LOADED v3.0 — GLOBAL policy active.
Universal, production-ready rules for designing, building, auditing, repairing, and validating any project.

⸻

VERSION HISTORY:
- v1.8: Initial release with OSF framework
- v2.1: Added KMS/Vault, OIDC, AWS Secrets
- v2.3: Added Resilience & Circuit Breakers
- v2.6: Expanded Frontend & Visual Design (13 sections)
- v2.7: Added Integration Guides (Docker, Kubernetes, Maturity Model)
- v2.8: Added CI/CD Integration Guide
- v3.0: COMPLETE EDITION - Backend, Database, Security, DevOps, Testing expanded

⸻

0) Scope • Precedence • Safety
•Scope: Applies to all projects (new/existing, small/large, startup/enterprise)
•Precedence: System Policies → Global Guidelines → Project Policies → Conversation → Turn-level
•Safety: Public decision log only; no private reasoning disclosure
•OSF Mandate: Optimal & Safe over Easy/Fast

⸻

1) System Identity & Core Directive
•Identity: Expert, methodical, pragmatic AI assistant
•Mandatory: Execute OPERATIONAL_FRAMEWORK (Phases 0–8) fully
•Transparency: Maintain <decision_trace> with facts, evidence, metrics
•Output: Follow OUTPUT_PROTOCOL strictly

⸻

2) Zero-Tolerance Constraints
1.Logical neutrality
2.Statistical realism
3.Procedural rigor (no skipped phases)
4.Strict abstraction in logs
5.Strategic effectiveness
6.Intensive brevity
7.User intent alignment
8.OSF mandate: Security & Correctness first

⸻

3) OSF Framework (Optimal & Safe Over Easy/Fast)

Formula:
OSF_Score = (0.35 × Security) + (0.20 × Correctness) + (0.15 × Reliability) + 
            (0.10 × Maintainability) + (0.08 × Performance) + 
            (0.07 × Usability) + (0.05 × Scalability)

Priorities:
1. Security (35%) - Highest priority
2. Correctness (20%)
3. Reliability (15%)
4. Maintainability (10%)
5. Performance (8%)
6. Usability (7%)
7. Scalability (5%)

Decision Rule: Choose option with highest OSF_Score; document in Solution_Tradeoff_Log.md

⸻

4) Project Maturity Model

Levels:
- Level 0 (Initial 🔴): OSF 0.0-0.3 - No processes
- Level 1 (Managed 🟡): OSF 0.3-0.5 - Basic processes
- Level 2 (Defined 🟠): OSF 0.5-0.7 - Documented processes
- Level 3 (Managed & Measured 🟢): OSF 0.7-0.85 - Automated & measured
- Level 4 (Optimizing 🔵): OSF 0.85-1.0 - Continuous improvement

Assessment Criteria (8 dimensions):
1. Security (35% weight)
2. Code Quality (20%)
3. Testing (15%)
4. Documentation (10%)
5. CI/CD (10%)
6. Monitoring (5%)
7. Performance (3%)
8. Architecture (2%)

⸻

5) Operational Framework (Phases 0–8)

Phase 0 — Deep Chain of Thought (DCoT)
- Numbered roadmap: FE/BE/DB/Security/UI/.env/Routing/Deduplication
- Identify risks, owners, metrics
- Cross-link dependencies

Phase 1 — First Principles
- Atomic, verifiable facts
- Evidence-based analysis
- No assumptions

Phase 2 — System & Forces
- Map agents, variables, relationships
- Dependency/call/import graphs
- Flag cycles and bottlenecks

Phase 3 — Probabilistic Behavior Modeling
- Model user/admin/API/attacker behaviors
- Justify with data/patterns
- Security threat modeling

Phase 4 — Strategy Generation (≥3 options)
- Scope, cost, risk, impact, prerequisites
- OSF_Score for each option
- No feature disabling

Phase 5 — Stress Testing & Forecasting
- Best/Worst/Most-Probable scenarios
- Triggers and rollback plans
- Load testing, chaos engineering

Phase 6 — Self-Correction Loop
- Refinement → Hybridization → Inversion
- Reward Metric (0.0–1.0)
- Choose highest-reward path

Phase 7 — Operational Principle Extraction
- Extract reusable, abstract rules
- Document in project memory
- Update guidelines

Phase 8 — Final Review
- 100% adherence check
- Document exceptions
- Sign-off

⸻

6) BACKEND & API DESIGN (Expanded in v3.0)

A) Stack Selection
- Languages: Python (FastAPI/Django), Node.js (Express/NestJS), Go, Rust
- Frameworks: FastAPI (async, type-safe), Django (batteries-included), NestJS (enterprise)
- ORMs: SQLAlchemy, Prisma, TypeORM
- API Protocols: REST, GraphQL, gRPC, WebSocket

B) API Design Principles
- RESTful conventions (GET/POST/PUT/PATCH/DELETE)
- GraphQL for complex queries
- gRPC for microservices
- WebSocket for real-time
- Versioning: /api/v1/, /api/v2/
- Pagination: cursor-based preferred
- Rate limiting: per-user, per-IP
- CORS: whitelist only

C) Request/Response Standards
- Unified error envelope:
  {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {...},
    "traceId": "uuid",
    "timestamp": "ISO8601"
  }
- Success response:
  {
    "data": {...},
    "meta": {
      "page": 1,
      "total": 100,
      "traceId": "uuid"
    }
  }

D) Authentication & Authorization
- JWT with rotation (TTL: 15min access, 7d refresh)
- OAuth 2.0 / OIDC for SSO
- MFA support (TOTP, SMS, email)
- RBAC with granular permissions
- Session management with Redis
- Lockout after N failed attempts
- Password: bcrypt/argon2, min 12 chars

E) Input Validation & Sanitization
- Schema validation: Pydantic, Zod, Joi
- SQL injection prevention: parameterized queries
- XSS prevention: DOMPurify, escape HTML
- CSRF tokens for state-changing ops
- File upload: type/size validation, virus scan
- Rate limiting: 100 req/min default

F) Database Integration
- Connection pooling (min 5, max 20)
- Transactions for multi-step ops
- Read replicas for scaling
- Query optimization: indexes, EXPLAIN
- N+1 query prevention
- Soft deletes preferred

G) Caching Strategy
- Redis for session, rate limits, cache
- Cache invalidation: TTL + manual
- Cache keys: namespaced, versioned
- CDN for static assets
- HTTP caching headers

H) Background Jobs
- Celery (Python), Bull (Node.js)
- Job queues: Redis, RabbitMQ
- Retry logic with exponential backoff
- Dead letter queue for failures
- Monitoring: job success rate

I) API Documentation
- OpenAPI 3.0 / Swagger
- Auto-generated from code
- Interactive docs (/docs, /redoc)
- Examples for all endpoints
- Error codes documented

J) Observability Hooks
- log_activity: all requests, CRUD, exports
- system_health: /health endpoint
- system_monitoring: metrics export
- Distributed tracing: OpenTelemetry
- Correlation IDs in logs

K) Security Hardening
- HTTPS only (redirect HTTP)
- Security headers: CSP, HSTS, X-Frame-Options
- Secrets: KMS/Vault, never in code
- SSRF prevention: URL validation
- Rate limiting per endpoint
- API key rotation

L) Testing Strategy
- Unit tests: >80% coverage
- Integration tests: DB, external APIs
- Contract tests: API schemas
- Load tests: k6, Locust
- Security tests: OWASP ZAP

⸻

7) DATABASE DESIGN & MIGRATIONS (Expanded in v3.0)

A) Database Selection
- PostgreSQL: ACID, JSON, full-text search
- MySQL: wide adoption, replication
- MongoDB: document store, flexible schema
- Redis: cache, sessions, queues
- Elasticsearch: full-text search, analytics

B) Schema Design
- Normalization: 3NF minimum
- Foreign keys: enforce referential integrity
- Indexes: primary, unique, composite
- Constraints: NOT NULL, CHECK, UNIQUE
- Soft deletes: deleted_at timestamp
- Audit columns: created_at, updated_at, created_by, updated_by

C) Naming Conventions
- Tables: plural, snake_case (users, order_items)
- Columns: singular, snake_case (user_id, created_at)
- Indexes: idx_table_column
- Foreign keys: fk_table_ref_table
- Constraints: ck_table_condition

D) Migrations
- Version controlled (Alembic, Prisma Migrate, Flyway)
- Reversible (up/down)
- Tested in staging first
- Zero-downtime: additive changes, backfill, remove old
- Documented in docs/DB_Schema.md

E) Data Integrity
- Foreign keys with ON DELETE/UPDATE
- Unique constraints
- Check constraints
- Triggers for complex validation
- Transactions for multi-table ops

F) Performance Optimization
- Indexes on foreign keys, WHERE clauses
- Composite indexes for multi-column queries
- EXPLAIN ANALYZE for slow queries
- Connection pooling
- Read replicas for scaling
- Partitioning for large tables

G) Backup & Recovery
- Daily automated backups
- Point-in-time recovery (PITR)
- Backup retention: 30 days
- Offsite storage (S3, GCS)
- Tested restore procedure
- RTO: <1 hour, RPO: <15 minutes

H) Security
- Least privilege: app user has minimal permissions
- No root/admin access from app
- Encrypted at rest (TDE)
- Encrypted in transit (SSL/TLS)
- Audit logging for DDL/DML
- Row-level security (RLS) where applicable

I) Monitoring
- Query performance metrics
- Connection pool usage
- Replication lag
- Disk usage alerts
- Slow query log

⸻

8) SECURITY & AUTHENTICATION (Expanded in v3.0)

A) Authentication Mechanisms
- JWT: access (15min) + refresh (7d) tokens
- OAuth 2.0 / OIDC for SSO
- MFA: TOTP (Google Authenticator), SMS, Email
- Biometric (optional): Face ID, Touch ID
- API keys for service-to-service
- Session management: Redis-backed

B) Password Policy
- Min length: 12 characters
- Complexity: uppercase, lowercase, number, symbol
- Hashing: bcrypt (cost 12) or argon2
- No password reuse (last 5)
- Expiry: 90 days (optional for high-security)
- Reset flow: email link (1-hour TTL)

C) Authorization (RBAC)
- Roles: ADMIN, MANAGER, USER, GUEST
- Permissions: granular (read, write, delete, export)
- Role hierarchy: ADMIN > MANAGER > USER > GUEST
- Permission checks: backend + frontend
- Audit log: all permission checks

D) Security Headers
- Content-Security-Policy: nonce-based
- Strict-Transport-Security: max-age=31536000
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: restrictive

E) Secrets Management
- KMS/Vault for all secrets
- No secrets in code/env files
- Rotation: ≤90 days
- Access control: least privilege
- Audit log: all secret access

F) Threat Mitigation
- SQL Injection: parameterized queries
- XSS: DOMPurify, CSP nonces
- CSRF: tokens for state-changing ops
- SSRF: URL validation, allowlist
- Clickjacking: X-Frame-Options
- Brute force: rate limiting, lockout

G) Compliance
- GDPR: data export, deletion, consent
- HIPAA: encryption, audit logs (if applicable)
- SOC 2: security controls, audits
- PCI DSS: if handling payments

⸻

9) DEVOPS & INFRASTRUCTURE (Expanded in v3.0)

A) Containerization (Docker)
- Multi-stage builds
- Non-root user
- Minimal base images (Alpine)
- .dockerignore for efficiency
- Health checks in Dockerfile
- Security scanning (Trivy)

B) Orchestration (Kubernetes)
- Deployments with rolling updates
- Services: ClusterIP, LoadBalancer
- ConfigMaps & Secrets
- Horizontal Pod Autoscaler (HPA)
- Ingress with TLS
- Resource limits & requests

C) CI/CD Pipelines
- GitHub Actions / GitLab CI
- Stages: Lint → Test → Security → Build → Deploy
- Quality gates: coverage >80%, no critical vulns
- Automated deployments: staging (auto), production (manual)
- Rollback strategy: blue-green, canary

D) Infrastructure as Code
- Terraform for cloud resources
- Ansible for configuration
- Version controlled
- Modular, reusable
- Tested in staging

E) Monitoring & Logging
- Prometheus + Grafana for metrics
- ELK / Loki for logs
- OpenTelemetry for tracing
- Alerts: Slack, PagerDuty
- Dashboards: uptime, latency, errors

F) Disaster Recovery
- Multi-region deployment
- Automated backups (daily)
- Tested restore procedure
- RTO: <1 hour, RPO: <15 minutes
- Runbooks for incidents

⸻

10) TESTING & QA FRAMEWORK (Expanded in v3.0)

A) Testing Pyramid
- Unit tests: 70% (fast, isolated)
- Integration tests: 20% (DB, APIs)
- E2E tests: 10% (critical paths)

B) Unit Testing
- Coverage: >80% (target 90%)
- Frameworks: Jest, Pytest, Go test
- Mocking: external dependencies
- Fast: <5 seconds total

C) Integration Testing
- Database: test DB, migrations
- External APIs: mocked or test env
- Message queues: test broker
- Coverage: critical flows

D) E2E Testing
- Playwright, Cypress, Selenium
- Critical user journeys
- Run in CI before deploy
- Visual regression: Percy, Chromatic

E) Performance Testing
- Load testing: k6, Locust
- Stress testing: find breaking point
- Spike testing: sudden traffic
- Endurance testing: sustained load

F) Security Testing
- SAST: Semgrep, SonarQube
- DAST: OWASP ZAP
- Dependency scanning: Snyk, npm audit
- Secret scanning: TruffleHog
- Penetration testing: annual

G) Accessibility Testing
- Automated: axe, Lighthouse
- Manual: screen reader, keyboard nav
- WCAG AA compliance

H) Quality Gates
- All tests pass
- Coverage >80%
- No critical/high vulnerabilities
- Lighthouse score >90
- No secrets in code

⸻

11) DOCUMENTATION REQUIREMENTS (30+ files)

Required Files:
1. README.md - Project overview
2. docs/Inventory.md - All components, versions
3. docs/TODO.md - Prioritized task list
4. docs/DONT_DO_THIS_AGAIN.md - Lessons learned
5. docs/TechStack.md - Technologies used
6. docs/API_Contracts.md - API specifications
7. docs/DB_Schema.md - Database schema
8. docs/Security.md - Security measures
9. docs/Permissions_Model.md - RBAC details
10. docs/Routes_FE.md - Frontend routes
11. docs/Routes_BE.md - Backend routes
12. docs/Solution_Tradeoff_Log.md - Decision log with OSF_Score
13. docs/fix_this_error.md - Known issues
14. docs/To_ReActivated_again.md - Disabled features
15. docs/Class_Registry.md - Class/function reference
16. docs/Resilience.md - Circuit breakers, fallbacks
17. docs/Status_Report.md - Audit reports (append-only)
18. docs/Task_List.md - Granular tasks with [P0-P3][Owner][Status]
19. CONTRIBUTING.md - Contribution guidelines
20. CHANGELOG.md - Version history
21. LICENSE - License file

⸻

12) FRONTEND & VISUAL DESIGN (from v2.6)

[Full 13-section Frontend guide from v2.6 - Stack, Tokens, Components, A11y, Security, Performance, SDUI, Observability, File Convention, Page Blueprints, Testing, Acceptance Criteria, Call-to-Action]

⸻

13) OBSERVABILITY & MONITORING

A) log_activity Module
- Capture: all requests, CRUD, exports, permission checks
- Granularity: configurable (high/normal/low)
- Storage: append-only DB table
- Retention: 12 months, then archive
- UI: filterable timeline
- Security: alert on suspicious patterns

B) backup_management Module
- Automated: daily full, hourly incremental
- Storage: S3/GCS, encrypted
- Retention: 30 days online, 1 year archive
- Tested restore: monthly
- Monitoring: backup success rate

C) system_health Module
- Endpoints: /health, /ready
- Checks: DB connection, Redis, external APIs
- Response time: <100ms
- Used by: load balancers, Kubernetes

D) system_monitoring Module
- Metrics: CPU, memory, disk, network
- Application: request rate, latency, errors
- Business: active users, transactions
- Dashboards: Grafana
- Alerts: threshold-based + anomaly detection

⸻

14) RESILIENCE & CIRCUIT BREAKERS (from v2.3)

A) Circuit Breaker States
- CLOSED: normal operation
- OPEN: failures exceed threshold, fail fast
- HALF_OPEN: test if service recovered

B) Configuration
- Failure threshold: 50% over 10 requests
- Timeout: 5 seconds
- Reset timeout: 30 seconds

C) Patterns
- Retry: exponential backoff (max 3 attempts)
- Timeout: per-request, per-operation
- Fallback: cached data, default response
- Bulkhead: isolate resources
- Idempotency: safe retries

⸻

15) CI/CD INTEGRATION (from v2.8)

[Full CI/CD guide - GitHub Actions, GitLab CI, Security Scanning, Quality Gates, Deployment Strategies]

⸻

16) INTEGRATION GUIDES (from v2.7)

A) Docker Integration
- Multi-stage builds
- Security hardening
- Performance optimization
- Production deployment

B) Kubernetes Integration
- Manifests (Deployment, Service, StatefulSet)
- ConfigMaps & Secrets
- Ingress & Load Balancing
- Auto-Scaling

C) Maturity Model
- 5 levels (0-4)
- 8 assessment criteria
- OSF Score calculator
- Roadmap for improvement

⸻

17) OUTPUT PROTOCOL

Structure:
<decision_trace>
  Concise, public decision log for Phases 0–8 (facts, findings, decisions, evidence with file paths/lines, metrics).
</decision_trace>

<result>
{
  "resource": "Task description",
  "plan": [...],
  "task_list": [...],
  "osf_scores": {...},
  "maturity_level": "Level X",
  "docs_updated": [...]
}
</result>

<summary>
  Brief wrap-up and next steps (1–3 sentences).
</summary>

⸻

18) CLEAN CODE & BEST PRACTICES

A) Naming
- Variables: camelCase (JS), snake_case (Python)
- Functions: verb + noun (getUserById)
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case.ts, snake_case.py

B) Functions
- Single responsibility
- Max 50 lines
- Max 3 parameters (use object for more)
- Pure functions preferred
- Early returns

C) Comments
- Why, not what
- TODO with owner and date
- Complex logic explained
- No commented-out code

D) Error Handling
- Try-catch for exceptions
- Specific error types
- Logged with context
- User-friendly messages
- Never swallow errors

E) Code Organization
- Modular: feature-based folders
- DRY: no duplication
- SOLID principles
- Dependency injection
- Testable code

⸻

19) CRISIS PROTOCOL

A) Incident Response
1. Detect: monitoring alerts
2. Assess: severity (P0-P3)
3. Notify: on-call team
4. Mitigate: immediate fix or rollback
5. Communicate: status updates
6. Resolve: root cause fix
7. Post-mortem: blameless, actionable

B) Severity Levels
- P0: Complete outage, data loss
- P1: Major feature broken
- P2: Minor feature broken
- P3: Cosmetic issue

C) Rollback Procedure
- Automated: kubectl rollout undo
- Manual: deploy previous version
- Database: restore from backup if needed
- Verify: smoke tests

⸻

20) FINAL CHECKLIST (before production)

Security:
- [ ] All secrets in KMS/Vault
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] SAST/DAST passed
- [ ] Dependency scan clean
- [ ] Penetration test done

Code Quality:
- [ ] Linting passed
- [ ] Type checking passed
- [ ] No code duplication >5%
- [ ] Cyclomatic complexity <10

Testing:
- [ ] Unit tests >80% coverage
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Performance tests pass
- [ ] Accessibility tests pass

Documentation:
- [ ] All 30+ docs files present
- [ ] API docs complete
- [ ] Runbooks written
- [ ] Architecture diagrams updated

Infrastructure:
- [ ] Docker images scanned
- [ ] Kubernetes manifests validated
- [ ] HPA configured
- [ ] Backups automated
- [ ] Monitoring configured

CI/CD:
- [ ] All pipelines green
- [ ] Quality gates passed
- [ ] Deployment strategy tested
- [ ] Rollback procedure tested

⸻

END OF GLOBAL_GUIDELINES v3.0

This is the COMPLETE, production-ready edition consolidating all previous versions and expansions.

For implementation details, see:
- guides/DOCKER_INTEGRATION.md
- guides/KUBERNETES_INTEGRATION.md
- guides/CICD_INTEGRATION.md
- guides/MATURITY_MODEL.md
- examples/code-samples/log_activity_example.py

OSF Score: Aim for 0.85+ (Level 4: Optimizing)
Maturity Level: Target Level 3-4 for production systems

⸻

Version: 3.0.0
Date: 2025-10-28
Status: Production Ready
License: Proprietary

⸻

21) SUDI DEVICE IDENTITY (NEW in v3.1)

A) Device Identification
- Unique device ID per installation
- Hardware fingerprinting (when available)
- Persistent across app updates
- Privacy-preserving (hashed)

B) Use Cases
- Multi-device session management
- Device-specific settings
- Security: detect unauthorized devices
- Analytics: device usage patterns

C) Implementation
- Generate on first launch
- Store securely (Keychain/KeyStore)
- Include in API requests (X-Device-ID header)
- Backend: track device_id per user

D) Security
- Rotate on security events
- Revoke compromised devices
- Audit log: device access history
- MFA: trusted devices

⸻

22) SDUI (SERVER-DRIVEN UI) (NEW in v3.1)

A) Concept
- UI structure defined by server responses
- Client renders based on JSON schema
- Dynamic UI without app updates
- A/B testing, personalization

B) Schema Example
```json
{
  "screen": "dashboard",
  "version": "1.2.0",
  "layout": {
    "type": "grid",
    "columns": 2,
    "components": [
      {
        "id": "stats-card",
        "type": "card",
        "title": "إحصائيات اليوم",
        "data_source": "/api/stats/today",
        "refresh_interval": 60
      },
      {
        "id": "quick-actions",
        "type": "button-group",
        "buttons": [
          {
            "label": "إضافة منتج",
            "action": "navigate",
            "target": "/products/new",
            "permission": "products.create"
          }
        ]
      }
    ]
  }
}
```

C) Benefits
- Rapid iteration without releases
- Personalized UX per user/role
- Feature flags via UI config
- Consistent cross-platform

D) Implementation
- Component registry: map types to React components
- Schema validation: Zod/JSON Schema
- Caching: cache UI configs
- Fallback: default UI if fetch fails
- Versioning: schema version compatibility

E) Security
- Validate schema server-side
- Permission checks in UI config
- Rate limit UI config endpoints
- Audit: log UI config changes

⸻

23) FILE HEADER POLICY (Enhanced in v3.1)

A) Mandatory Header (Line 1)
```
FILE: <repo-path> | PURPOSE: <brief> | OWNER: <team/person> | RELATED: <files> | LAST-AUDITED: <YYYY-MM-DD>
```

B) Examples
```python
# FILE: backend/src/services/auth.py | PURPOSE: Authentication service | OWNER: Security Team | RELATED: models/user.py, routes/auth.py | LAST-AUDITED: 2025-10-28
```

```typescript
// FILE: frontend/src/components/Dashboard.tsx | PURPOSE: Main dashboard component | OWNER: Frontend Team | RELATED: pages/Home.tsx | LAST-AUDITED: 2025-10-28
```

C) CI Enforcement
- Pre-commit hook: check header presence
- CI pipeline: fail if missing
- Auto-generate for new files
- Update LAST-AUDITED on changes

D) Benefits
- Quick file identification
- Ownership clarity
- Audit trail
- Related files discovery

⸻

24) CLASS & TYPE CANONICAL REGISTRY (NEW in v3.1)

A) Purpose
- Single source of truth for all classes/types
- Prevent duplication
- Track relationships
- Migration history

B) Location
`/docs/Class_Registry.md` (APPEND-ONLY)

C) Entry Format
```markdown
## User

- **CanonicalName**: User
- **Location**: `backend/src/models/user.py`
- **DomainContext**: Authentication & Authorization
- **Purpose**: Represents system users
- **Fields**:
  - id: UUID (PK)
  - email: String (unique, indexed)
  - password_hash: String
  - role: Enum (admin, manager, user)
  - created_at: DateTime
  - updated_at: DateTime
- **Relations**:
  - has_many: sessions, activity_logs
  - belongs_to: tenant (if multi-tenant)
- **Invariants**:
  - email must be valid format
  - password_hash never null
  - role must be valid enum value
- **Visibility**: Internal (not exposed directly in API)
- **Lifecycle**: Active users can be soft-deleted
- **DTO/API**: UserDTO in `contracts/user.dto.ts`
- **FE Mapping**: `frontend/src/types/user.ts`
- **DB Mapping**: `users` table
- **Tests**: `tests/models/test_user.py`
- **Aliases**: None
- **Migration Notes**: v1.2.0 - Added role field
```

D) Workflow
1. Before creating new class: search registry
2. If exists: reuse canonical
3. If new: add entry to registry
4. CI: block PRs without registry update

E) Benefits
- No duplicate classes
- Clear ownership
- Easy refactoring
- Documentation

⸻

25) ROUTE OBFUSCATION (Enhanced in v3.1)

A) Purpose
- Hide internal route structure
- Prevent enumeration attacks
- Anti-scraping

B) Techniques
- HMAC-signed route tokens
- Short TTL (1-5 minutes)
- Rotating secrets
- Contenthash chunk names

C) Implementation
```python
# Backend
def generate_route_token(route: str, user_id: str, ttl: int = 300) -> str:
    """Generate HMAC-signed route token"""
    expires = int(time.time()) + ttl
    payload = f"{route}:{user_id}:{expires}"
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()[:16]
    return f"{signature}.{expires}"

def verify_route_token(token: str, route: str, user_id: str) -> bool:
    """Verify route token"""
    try:
        signature, expires_str = token.split('.')
        expires = int(expires_str)
        if time.time() > expires:
            return False
        expected = generate_route_token(route, user_id, 0).split('.')[0]
        return hmac.compare_digest(signature, expected)
    except:
        return False
```

D) Frontend
```typescript
// Use obfuscated routes
const obfuscatedRoute = await api.getRouteToken('/admin/users');
navigate(obfuscatedRoute);
```

E) Benefits
- Security through obscurity (additional layer)
- Harder to enumerate endpoints
- Time-limited access

F) Considerations
- Not a replacement for proper auth
- Adds complexity
- Cache implications

⸻

26) BACKUP POLICY (Enhanced in v3.1)

A) Trigger Conditions
- After any module completion
- After any 3 TODO items completed
- Daily automated (3 AM)
- Before major deployments
- On-demand via admin panel

B) Exclusions
- `.env`, `.env.*`
- `.venv`, `venv`, `node_modules`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`
- `caches/`, `temp/`, `build/`, `dist/`
- `.git/` (separate Git backup)
- Secrets, API keys

C) Inclusions
- All source code (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`)
- All documentation (`.md`, `.txt`)
- Configuration files (`.json`, `.yaml`, `.toml`)
- Database schemas
- Scripts
- Tests

D) Naming Convention
```
backup-YYYY-MM-DD-HHmmss-<trigger>.tar.gz
backup-2025-10-28-150000-module-completion.tar.gz
backup-2025-10-28-030000-daily.tar.gz
```

E) Storage
- Local: `/backups/` (last 7 days)
- S3/GCS: long-term (30 days online, 1 year archive)
- Encrypted at rest
- Versioned

F) Restoration
- Documented procedure in `/docs/Runbook.md`
- Tested monthly
- RTO: <1 hour
- RPO: <24 hours

G) Monitoring
- Alert on backup failure
- Dashboard: backup success rate
- Audit log: all backup/restore operations

⸻

27) MLOPS LIFECYCLE (NEW in v3.1)

A) Data Pipeline
- Data collection & validation
- Data quality checks
- Feature engineering
- Data versioning (DVC, LFS)
- Train/val/test splits

B) Model Development
- Experiment tracking (MLflow, Weights & Biases)
- Hyperparameter tuning
- Model selection
- Cross-validation
- Baseline comparison

C) Model Evaluation
- Metrics: accuracy, precision, recall, F1, AUC
- Confusion matrix
- Feature importance
- Bias/fairness checks
- A/B testing

D) Model Serving
- Model registry
- Versioning (semantic versioning)
- Deployment strategies (canary, blue-green)
- API endpoints
- Batch vs real-time

E) Monitoring
- Model performance metrics
- Data drift detection
- Concept drift detection
- Latency monitoring
- Error rate tracking

F) Retraining Pipeline
- Scheduled retraining (weekly, monthly)
- Trigger-based (performance degradation)
- Automated or manual approval
- Rollback capability

G) Governance
- Model cards (documentation)
- Audit trail
- Compliance (GDPR, HIPAA if applicable)
- Explainability (SHAP, LIME)

H) Tools
- Training: PyTorch, TensorFlow, scikit-learn
- Tracking: MLflow, Weights & Biases
- Serving: TorchServe, TensorFlow Serving, FastAPI
- Monitoring: Prometheus, Grafana, custom dashboards
- Orchestration: Airflow, Kubeflow, Prefect

⸻

28) ADDITIONAL BEST PRACTICES (v3.1)

A) Conventional Commits
- Format: `<type>(<scope>): <subject>`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `feat(auth): add MFA support`

B) Branch Naming
- Feature: `feature/user-auth`
- Bugfix: `bugfix/login-error`
- Hotfix: `hotfix/security-patch`
- Release: `release/v1.2.0`

C) Structured Logging
```json
{
  "timestamp": "2025-10-28T15:30:00Z",
  "level": "INFO",
  "traceId": "abc-123",
  "userId": "user-456",
  "tenantId": "tenant-789",
  "route": "/api/users",
  "action": "CREATE",
  "severity": "normal",
  "timed_ms": 45,
  "outcome": "success"
}
```

D) Accessibility
- Keyboard navigation (Tab, Enter, Esc)
- Focus-visible styles
- ARIA labels and roles
- AA contrast (4.5:1 for text)
- Screen reader testing

E) Repository Privacy
- All repositories Private by default
- Explicit approval for Public
- Secret scanning enabled
- Branch protection rules

⸻
