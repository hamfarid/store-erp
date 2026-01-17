# 🏗️ Architecture Overview

This document describes the high-level architecture of the Store Management System.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Browser   │  │  Mobile App │  │  API Client │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
└─────────┼────────────────┼────────────────┼─────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        GATEWAY LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      Nginx / Traefik                     │   │
│  │  • SSL Termination  • Load Balancing  • Rate Limiting   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │    Frontend (React) │    │   Backend (Flask)   │            │
│  │  ├─ Components      │    │  ├─ Routes          │            │
│  │  ├─ Hooks           │    │  ├─ Services        │            │
│  │  ├─ State (Context) │    │  ├─ Models          │            │
│  │  └─ Utils           │    │  ├─ Middleware      │            │
│  └─────────────────────┘    │  └─ Utils           │            │
│                             └─────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │  PostgreSQL   │  │    Redis      │  │   ChromaDB    │       │
│  │  (Primary DB) │  │   (Cache)     │  │ (Vector Store)│       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture

### Directory Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── auth.py              # Authentication logic
│   ├── database.py          # Database configuration
│   ├── permissions.py       # RBAC system
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── invoice.py
│   │   └── ...
│   │
│   ├── routes/              # API endpoints
│   │   ├── auth_unified.py
│   │   ├── products_unified.py
│   │   ├── inventory.py
│   │   └── ...
│   │
│   ├── middleware/          # Request/Response middleware
│   │   ├── error_envelope_middleware.py
│   │   ├── route_security.py
│   │   └── csp_nonce.py
│   │
│   ├── utils/               # Utility functions
│   │   ├── validation.py
│   │   ├── file_scanner.py
│   │   └── ssrf_protection.py
│   │
│   └── config/              # Configuration
│       └── rate_limit_config.py
│
├── migrations/              # Database migrations
├── tests/                   # Test suite
└── requirements.txt
```

### Request Flow

```
Request → Middleware → Route → Service → Model → Database
                ↓
           Response ← Error Envelope ← Service Result
```

---

## Frontend Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── App.tsx              # Root component
│   ├── main.tsx             # Entry point
│   │
│   ├── api/                 # API client
│   │   ├── client.ts        # Typed API client
│   │   └── validators.ts    # Zod schemas
│   │
│   ├── components/          # UI components
│   │   ├── ui/              # Base components
│   │   ├── forms/           # Form components
│   │   └── security/        # Security components
│   │
│   ├── hooks/               # Custom hooks
│   │   └── useCsrf.ts
│   │
│   ├── pages/               # Page components
│   │   ├── Dashboard/
│   │   ├── Products/
│   │   └── ...
│   │
│   ├── utils/               # Utilities
│   │   ├── sanitize.ts
│   │   └── accessibility.ts
│   │
│   └── styles/              # Global styles
│
└── public/                  # Static assets
```

---

## Data Flow

### Authentication Flow

```
┌────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐
│ Client │────▶│  Login  │────▶│ Validate │────▶│ Generate │
└────────┘     │ Request │     │  User    │     │   JWT    │
               └─────────┘     └──────────┘     └────┬─────┘
                                                      │
┌────────┐     ┌─────────┐     ┌──────────┐          │
│ Client │◀────│  Token  │◀────│  Store   │◀─────────┘
└────────┘     │Response │     │ Session  │
               └─────────┘     └──────────┘
```

### API Request Flow

```
┌────────────┐
│ API Client │
└─────┬──────┘
      │ 1. Add Auth Header
      │ 2. Add CSRF Token
      ▼
┌────────────┐
│  Gateway   │
└─────┬──────┘
      │ 3. SSL Termination
      │ 4. Rate Limiting
      ▼
┌────────────┐
│ Middleware │
└─────┬──────┘
      │ 5. Token Validation
      │ 6. Permission Check
      │ 7. Input Sanitization
      ▼
┌────────────┐
│   Route    │
└─────┬──────┘
      │ 8. Business Logic
      │ 9. Database Operations
      ▼
┌────────────┐
│  Response  │
└────────────┘
```

---

## Security Architecture

### Defense in Depth

```
Layer 1: Network
├── TLS/SSL encryption
├── DDoS protection
└── Firewall rules

Layer 2: Application
├── Rate limiting
├── Input validation
├── CSRF protection
└── CSP headers

Layer 3: Authentication
├── JWT tokens
├── Token rotation
├── Account lockout
└── MFA (planned)

Layer 4: Authorization
├── RBAC permissions
├── Resource ownership
└── API scoping

Layer 5: Data
├── Encryption at rest
├── Parameterized queries
└── Audit logging
```

---

## Technology Stack

### Backend

| Category | Technology |
|----------|------------|
| Framework | Flask 2.x |
| ORM | SQLAlchemy 2.x |
| Auth | Flask-JWT-Extended |
| Validation | Marshmallow |
| Rate Limiting | Flask-Limiter |
| Documentation | Flask-Smorest (OpenAPI) |

### Frontend

| Category | Technology |
|----------|------------|
| Framework | React 18 |
| Language | TypeScript 5.x |
| Build Tool | Vite |
| Validation | Zod |
| Styling | Tailwind CSS |
| State | React Context |

### Infrastructure

| Category | Technology |
|----------|------------|
| Container | Docker |
| Orchestration | Docker Compose / K8s |
| CI/CD | GitHub Actions |
| Reverse Proxy | Nginx / Traefik |
| Monitoring | Prometheus + Grafana |

---

## Scalability Considerations

### Horizontal Scaling

- Stateless API servers
- Redis for session/cache
- Load balancer distribution

### Vertical Scaling

- Database optimization
- Query indexing
- Connection pooling

### Caching Strategy

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│ Browser │────▶│  CDN    │────▶│  Redis   │
│  Cache  │     │ (Static)│     │ (Dynamic)│
└─────────┘     └─────────┘     └──────────┘
                                      │
                                      ▼
                               ┌──────────┐
                               │ Database │
                               └──────────┘
```

---

*Last updated: 2025-12-01*

