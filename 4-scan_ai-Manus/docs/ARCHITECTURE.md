# System Architecture - Gaara AI Agricultural Platform

**Version:** 2.0.0  
**Last Updated:** 2025-01-18  
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Principles](#architecture-principles)
3. [System Components](#system-components)
4. [Data Flow](#data-flow)
5. [Security Architecture](#security-architecture)
6. [Deployment Architecture](#deployment-architecture)
7. [Scalability & Performance](#scalability--performance)

---

## 1. Overview

### 1.1 Architecture Style

Gaara AI follows a **Modular Monolith** architecture with clear separation of concerns, designed for:
- **Maintainability:** Clear module boundaries and responsibilities
- **Scalability:** Ability to extract modules into microservices if needed
- **Testability:** Independent module testing
- **Security:** Defense in depth with multiple security layers

### 1.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Web Browser  │  │ Mobile App   │  │  IoT Devices │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Presentation Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         React 18 Frontend (SPA)                      │   │
│  │  - Components  - Pages  - Services  - State Mgmt    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ HTTPS/REST API
┌─────────────────────────────────────────────────────────────┐
│                   API Gateway Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI + Flask (Hybrid)                            │   │
│  │  - Authentication  - Rate Limiting  - CORS           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Business Logic Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Core   │  │ Business │  │   AI/ML  │  │  Admin   │   │
│  │ Modules  │  │ Modules  │  │ Modules  │  │ Modules  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SQLAlchemy ORM + Repository Pattern                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Persistence Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PostgreSQL   │  │  File Storage│  │  Redis Cache │      │
│  │   Database   │  │   (Images)   │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture Principles

### 2.1 OSF Framework (Optimal & Safe Over Easy/Fast)

**Priority Order:**
1. **Security (35%)** - Highest priority
2. **Correctness (20%)** - Data integrity and business logic
3. **Reliability (15%)** - System uptime and fault tolerance
4. **Maintainability (10%)** - Code quality and documentation
5. **Performance (8%)** - Response time and throughput
6. **Usability (7%)** - User experience
7. **Scalability (5%)** - Growth capacity

### 2.2 Design Principles

- **Separation of Concerns:** Each module has a single, well-defined responsibility
- **DRY (Don't Repeat Yourself):** Shared logic in utilities and services
- **SOLID Principles:** Object-oriented design best practices
- **API-First Design:** Backend exposes RESTful APIs consumed by frontend
- **Security by Design:** Security integrated at every layer
- **Fail-Safe Defaults:** Secure and safe default configurations

---

## 3. System Components

### 3.1 Frontend Architecture (React 18)

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout/          # Navbar, Sidebar, Footer
│   │   ├── UI/              # Buttons, Cards, Tables, Forms
│   │   └── Features/        # Feature-specific components
│   ├── pages/               # Route-level page components
│   │   ├── Auth/            # Login, Register, Profile
│   │   ├── Dashboard/       # Main dashboard
│   │   ├── Farms/           # Farm management pages
│   │   ├── Diagnosis/       # Disease diagnosis pages
│   │   └── Admin/           # Admin pages
│   ├── services/            # API communication layer
│   │   ├── ApiService.js    # Base HTTP client
│   │   ├── AuthService.js   # Authentication service
│   │   └── *Service.js      # Entity-specific services
│   ├── hooks/               # Custom React hooks
│   ├── context/             # React Context providers
│   ├── utils/               # Utility functions
│   └── styles/              # Global styles and themes
```

**Key Technologies:**
- **React 18:** Component-based UI with hooks
- **React Router v6:** Client-side routing
- **React Query:** Server state management and caching
- **Tailwind CSS:** Utility-first styling
- **Vite:** Fast build tool and dev server

### 3.2 Backend Architecture (FastAPI + Flask)

```
backend/
├── src/
│   ├── modules/             # Business modules (36+)
│   │   ├── ai_agent/        # AI agent system
│   │   ├── ai_diagnosis/    # Disease diagnosis
│   │   ├── farm_management/ # Farm operations
│   │   ├── user_management/ # User CRUD
│   │   └── ...              # Other modules
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API route definitions
│   ├── services/            # Business logic services
│   ├── middleware/          # Security, logging, etc.
│   ├── utils/               # Helper functions
│   └── config/              # Configuration management
```

**Key Technologies:**
- **FastAPI:** Modern async API framework
- **Flask:** Traditional web framework (legacy support)
- **SQLAlchemy:** ORM for database operations
- **Pydantic:** Data validation and serialization
- **JWT:** Token-based authentication
- **TensorFlow 2.0+:** AI/ML model serving

### 3.3 Module Categories

#### Core Modules (5)
1. `main_api` - Application entry point
2. `database` - Database connection and models
3. `security` - Authentication and authorization
4. `permissions` - RBAC system
5. `routing` - API route registration

#### Business Modules (4)
6. `inventory_management` - Stock and warehouse
7. `equipment_management` - Asset tracking
8. `hr_management` - Employee and payroll
9. `ecommerce_system` - Product sales

#### Agricultural Modules (2)
10. `farm_management` - Farm and crop management
11. `iot_sensors` - IoT integration

#### AI Modules (3)
12. `ai_diagnosis` - Disease diagnosis engine
13. `predictive_analytics` - Crop predictions
14. `ai_agents` - Decision support

#### Admin Modules (3)
15. `advanced_analytics` - Analytics dashboards
16. `advanced_reporting` - Report generation
17. `security_monitoring` - Activity logging

---

## 4. Data Flow

### 4.1 Request Flow (User Action → Database)

```
[User Action] 
    ↓
[Frontend Component]
    ↓
[Event Handler]
    ↓
[API Service Call]
    ↓ HTTP Request (JSON)
[Backend API Route]
    ↓
[Authentication Middleware] → Verify JWT
    ↓
[Authorization Middleware] → Check Permissions
    ↓
[Validation Middleware] → Validate Input (Pydantic)
    ↓
[Controller/Route Handler]
    ↓
[Business Service]
    ↓
[Repository/Data Access]
    ↓
[SQLAlchemy ORM]
    ↓
[Database (PostgreSQL)]
    ↓ Response
[JSON Response]
    ↓
[Frontend State Update]
    ↓
[UI Re-render]
```

### 4.2 Authentication Flow

```
1. User submits credentials
2. Backend validates credentials
3. Backend generates JWT (access + refresh tokens)
4. Frontend stores tokens (secure httpOnly cookies)
5. Frontend includes access token in all API requests
6. Backend validates token on each request
7. Token expires → Frontend uses refresh token
8. Refresh token expires → User must re-login
```

---

## 5. Security Architecture

### 5.1 Security Layers

**Layer 1: Network Security**
- HTTPS only (TLS 1.3)
- CORS whitelist
- Rate limiting per IP and user

**Layer 2: Authentication**
- JWT with short-lived access tokens (15 min)
- Long-lived refresh tokens (7 days)
- Password hashing (bcrypt, cost 12)
- MFA support (planned)

**Layer 3: Authorization**
- Role-Based Access Control (RBAC)
- Permission checks at route level
- Resource-level permissions

**Layer 4: Input Validation**
- Pydantic schemas for all inputs
- SQL injection prevention (parameterized queries)
- XSS prevention (DOMPurify on frontend)
- CSRF tokens for state-changing operations

**Layer 5: Data Protection**
- Encryption at rest (database)
- Encryption in transit (HTTPS)
- Secrets in environment variables
- No sensitive data in logs

### 5.2 Security Headers

```python
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

---

## 6. Deployment Architecture

### 6.1 Development Environment

```
Developer Machine
├── Backend (localhost:5000)
├── Frontend (localhost:3000)
└── Database (localhost:5432)
```

### 6.2 Production Environment (Docker)

```
Load Balancer (Nginx)
    ↓
┌─────────────────────────────────┐
│  Docker Compose Stack           │
│  ├── Frontend Container (React) │
│  ├── Backend Container (FastAPI)│
│  ├── Database Container (Postgres)│
│  └── Redis Container (Cache)    │
└─────────────────────────────────┘
```

---

## 7. Scalability & Performance

### 7.1 Current Capacity
- **Concurrent Users:** 100-500
- **API Response Time:** <200ms (avg)
- **Database Queries:** Optimized with indexes

### 7.2 Scaling Strategy
- **Horizontal Scaling:** Add more backend containers
- **Database Scaling:** Read replicas for queries
- **Caching:** Redis for frequently accessed data
- **CDN:** Static assets served via CDN

---

**Document Status:** Complete  
**Next Review:** 2025-04-18

