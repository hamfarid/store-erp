# Technology Stack

**Last Updated:** 2025-11-04  
**Owner:** DevOps/Architecture  
**Status:** ✅ Current

---

## Overview

Complete Inventory Management System (ERP) built with modern, scalable technologies.

## Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 18.x | UI library |
| **Build Tool** | Vite | 5.x | Fast build & dev server |
| **Styling** | Tailwind CSS | 3.x | Utility-first CSS |
| **State** | Context API | - | State management |
| **HTTP Client** | Fetch API | - | API communication |
| **Routing** | React Router | 6.x | Client-side routing |
| **Internationalization** | i18next | 23.x | Multi-language support (EN/AR) |
| **UI Components** | Custom + Headless UI | - | Accessible components |
| **Testing** | Vitest + React Testing Library | - | Unit & integration tests |
| **Linting** | ESLint + Prettier | - | Code quality |

### Frontend Features

- ✅ Arabic-first design (RTL support)
- ✅ Light/dark theme support
- ✅ Responsive design (mobile-first)
- ✅ Accessibility (WCAG AA)
- ✅ Progressive Web App (PWA) ready
- ✅ Environment-based API configuration (VITE_API_BASE_URL)

## Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Flask | 2.x | Web framework |
| **ORM** | SQLAlchemy | 2.x | Database ORM |
| **Migrations** | Flask-Migrate | - | Database migrations |
| **Validation** | Pydantic | 2.x | Data validation |
| **Authentication** | JWT + Sessions | - | Auth mechanism |
| **Password Hashing** | Argon2id | - | Secure password storage |
| **CORS** | Flask-CORS | - | Cross-origin requests |
| **Logging** | Python logging | - | Structured logging |
| **Testing** | pytest | 7.x | Unit & integration tests |
| **Linting** | flake8 + autopep8 | - | Code quality |
| **Type Checking** | mypy | - | Static type checking |

### Backend Features

- ✅ RESTful API with OpenAPI 3.1.0 spec
- ✅ JWT with 15m access / 7d refresh tokens
- ✅ Session-based fallback auth
- ✅ RBAC (Role-Based Access Control)
- ✅ MFA support (TOTP)
- ✅ Login lockout (5 attempts / 15 min)
- ✅ CSRF protection (double-submit cookie)
- ✅ Rate limiting (per-minute, per-hour)
- ✅ Security headers (CSP, HSTS, X-Frame-Options)
- ✅ Error envelope (unified error format)

## Database Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Dev Database** | SQLite | 3.x | Local development |
| **Prod Database** | PostgreSQL | 14+ | Production (target) |
| **Migrations** | Flask-Migrate | - | Schema versioning |
| **Connection Pool** | SQLAlchemy | - | Connection management |

### Database Features

- ✅ 39 models with relationships
- ✅ Composite indexes on high-query columns
- ✅ Foreign key constraints
- ✅ Unique constraints
- ✅ Check constraints
- ✅ Transactions support

## API Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Specification** | OpenAPI | 3.1.0 | API documentation |
| **Format** | YAML | - | Spec format |
| **Authentication** | Bearer Token (JWT) | - | API auth |
| **Validation** | Pydantic | 2.x | Request/response validation |
| **Error Handling** | Unified envelope | - | Consistent error format |

### API Features

- ✅ 50+ endpoints documented
- ✅ Request/response schemas
- ✅ Error codes standardized
- ✅ Pagination support
- ✅ Filtering & sorting
- ✅ Rate limiting per endpoint

## CI/CD Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Platform** | GitHub Actions | - | CI/CD automation |
| **Linting** | flake8, ESLint | - | Code quality |
| **Testing** | pytest, npm test | - | Automated tests |
| **Type Checking** | mypy, tsc | - | Static analysis |
| **Security Scanning** | bandit, safety, gitleaks, trufflehog | - | Vulnerability detection |
| **SBOM** | CycloneDX, Grype, Trivy | - | Supply chain security |
| **DAST** | OWASP ZAP | - | Dynamic security testing |
| **Performance** | Lighthouse CI | - | Performance budgets |
| **Artifact Storage** | GitHub Artifacts | - | Build artifacts |

### CI/CD Workflows

- ✅ 12 workflows (lint, test, typecheck, security, SBOM, DAST, Lighthouse, audit, deploy)
- ✅ Protected branches (main requires PR review)
- ✅ Status checks required before merge
- ✅ Automated deployments (dev → staging → prod)

## Infrastructure Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Server** | Nginx | 1.x | Reverse proxy |
| **Containerization** | Docker | 20.x | Container runtime |
| **Orchestration** | Docker Compose | - | Multi-container management |
| **Secrets Management** | Environment variables (dev) / KMS/Vault (prod) | - | Secret storage |

### Infrastructure Features

- ✅ Docker support (Dockerfile + docker-compose.yml)
- ✅ Environment-based configuration
- ✅ Health check endpoints
- ✅ Graceful shutdown
- ✅ Logging to stdout/stderr

## Development Tools

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **GitHub** | Repository hosting |
| **VS Code** | IDE |
| **Postman** | API testing |
| **DBeaver** | Database management |
| **npm** | Frontend package manager |
| **pip** | Backend package manager |

## Security Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Password Hashing** | Argon2id | Secure password storage |
| **JWT** | HS256 / RS256 | Token signing |
| **HTTPS** | TLS 1.2+ | Transport security |
| **CORS** | Flask-CORS | Cross-origin protection |
| **CSRF** | Double-submit cookie | CSRF protection |
| **Rate Limiting** | Custom middleware | Brute force protection |
| **Headers** | CSP, HSTS, X-Frame-Options | Security headers |
| **Secrets** | KMS/Vault (prod) | Secret management |

## Monitoring & Observability

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Logging** | Python logging + structured logs | Application logs |
| **Tracing** | TraceId in logs | Request tracing |
| **Metrics** | Custom counters | Performance metrics |
| **Alerts** | GitHub Actions | CI/CD alerts |

---

## Dependency Management

### Frontend

- **Package Manager:** npm
- **Lock File:** package-lock.json
- **Key Dependencies:** react, react-router-dom, tailwindcss, i18next

### Backend

- **Package Manager:** pip
- **Lock File:** requirements.txt / requirements_final.txt
- **Key Dependencies:** flask, sqlalchemy, pydantic, flask-cors, flask-migrate

## Version Strategy

- **Frontend:** Semantic versioning (MAJOR.MINOR.PATCH)
- **Backend:** Semantic versioning (MAJOR.MINOR.PATCH)
- **Database:** Migration-based versioning
- **API:** OpenAPI versioning (v1.7.0)

## Upgrade Path

1. **Frontend:** npm update → test → deploy
2. **Backend:** pip install --upgrade → test → deploy
3. **Database:** Flask-Migrate → test → deploy
4. **Dependencies:** Regular security updates via Dependabot

---

**Next Steps:**

- [ ] Migrate prod database to PostgreSQL (T16)
- [ ] Implement circuit breaker middleware (T8)
- [ ] Add RAG governance (T7)
- [ ] Refresh OpenAPI spec (T9)
