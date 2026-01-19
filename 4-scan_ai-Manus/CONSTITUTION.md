# 🏛️ Project Constitution: Gaara Scan AI
## نظام الكشف الذكي عن أمراض النباتات | Intelligent Plant Disease Detection System

**Version:** v4.3.1 | **Mode:** ADOPTION (Brownfield)  
**Constitutional Authority:** Global Professional Core Prompt v33.2  
**Last Ratified:** 2026-01-17

---

## 1. Vision & Mission

### 🎯 Mission Statement (Arabic)
> **Gaara Scan AI** هو نظام ذكي متكامل يجمع بين إدارة المزارع الشاملة وتشخيص أمراض النباتات باستخدام أحدث تقنيات الذكاء الاصطناعي. يوفر النظام حلاً متطوراً للمزارعين والمهندسين الزراعيين والباحثين، مع دعم كامل للغة العربية والإنجليزية.

### 🎯 Mission Statement (English)
> **Gaara Scan AI** is an integrated intelligent system that combines comprehensive farm management with plant disease diagnosis using cutting-edge AI technologies. It provides an advanced solution for farmers, agricultural engineers, and researchers, with full Arabic and English support.

### 🌟 Core Values
1. **Accuracy First (الدقة أولاً):** 95%+ disease detection accuracy
2. **Accessibility (إمكانية الوصول):** Full RTL support, bilingual interface
3. **Security (الأمان):** Enterprise-grade security with 2FA/E2E encryption
4. **Self-Learning (التعلم الذاتي):** Continuous improvement from 17 trusted sources

---

## 2. Core Principles (The Non-Negotiables)

### 🔴 PRINCIPLE 1: Security First
- **2FA/TOTP is MANDATORY** for admin accounts
- **JWT tokens** expire in 15 minutes (access), 7 days (refresh)
- **All traffic MUST be encrypted** via Cloudflare E2E
- **Rate limiting ENFORCED**: 10 req/s API, 2 req/s uploads
- **OWASP Top 10 compliance** is mandatory

### 🔴 PRINCIPLE 2: Respect Legacy (Adoption Mode)
- **DO NOT DELETE** existing files without explicit authorization
- **REGISTER ALL FILES** in `.memory/file_registry.json` before creating new ones
- **GRADUAL REFACTORING**: One module at a time
- **MAINTAIN BACKWARD COMPATIBILITY** for all API endpoints

### 🔴 PRINCIPLE 3: Bilingual Excellence
- **100% Arabic/English parity** for all UI strings
- **RTL layout support** is mandatory for all components
- **i18n keys MUST exist** for both languages before merge

### 🔴 PRINCIPLE 4: AI/ML Quality Standards
- **Model accuracy ≥ 95%** for disease detection
- **Response time ≤ 2 seconds** for diagnosis
- **All models MUST be versioned** in `ml_service/models/`
- **Training data MUST be from trusted sources** (17 verified sources)

### 🔴 PRINCIPLE 5: Test Coverage
- **Backend: ≥ 90%** coverage (pytest)
- **Frontend: ≥ 95%** coverage (Vitest)
- **No code merge without passing tests**

---

## 3. Architectural Guidelines

### 🏗️ Tech Stack (Canonical)

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | React + Vite + Tailwind CSS | 18.x + 5.x |
| **Backend** | FastAPI + SQLAlchemy | 0.100+ |
| **Database** | PostgreSQL | 16-alpine |
| **Cache** | Redis | 7-alpine |
| **ML/AI** | YOLOv8 + PyTorch + TensorFlow | Latest |
| **Infrastructure** | Docker Compose + Nginx + Cloudflare | 2.0+ |

### 📐 Architectural Pattern
- **Pattern:** Microservices with API Gateway
- **Communication:** REST API + WebSocket
- **Data Flow:** Event-Driven (Redis Pub/Sub)

### 🐳 Service Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Cloudflare (CDN + WAF)                  │
│         E2E Encryption • DDoS Protection • Bot Management   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
┌───────────────────┐                     ┌──────────────────┐
│   Frontend        │                     │  Backend API     │
│   React + Vite    │◄────────────────────┤  FastAPI         │
│   Port: 4501      │                     │  Port: 4001      │
└───────────────────┘                     └──────────────────┘
                                                   ↓
                        ┌──────────────────────────┴──────────────────┐
                        ↓                          ↓                   ↓
              ┌─────────────────┐      ┌──────────────────┐  ┌────────────────┐
              │ ML Service      │      │ AI Service       │  │  PostgreSQL    │
              │ YOLO + CNN      │      │ Image Crawler    │  │  Database      │
              │ Port: 4101      │      │ Port: 4601       │  │  Port: 8502    │
              └─────────────────┘      └──────────────────┘  └────────────────┘
                                                                      ↓
                                                             ┌────────────────┐
                                                             │  Redis         │
                                                             │  Cache + Queue │
                                                             │  Port: 6379    │
                                                             └────────────────┘
```

### 📁 Project Structure (Canonical)
```
gaara_scan_ai/
├── backend/                    # FastAPI Backend
│   ├── src/
│   │   ├── api/v1/            # 15+ API endpoints
│   │   ├── models/            # 12 database models
│   │   ├── modules/           # Business logic
│   │   ├── services/          # Service layer
│   │   ├── core/              # Configuration
│   │   └── utils/             # Utilities
│   └── tests/                 # Test suites
├── frontend/                   # React Frontend
│   ├── pages/                 # 22 pages
│   ├── components/            # Reusable components
│   ├── context/               # State management
│   └── services/              # API services
├── ml_service/                 # AI/ML Service
│   ├── main.py                # FastAPI server
│   ├── yolo_detector.py       # YOLO integration
│   └── models/                # Trained models
├── image_crawler/              # Self-Learning Service
│   ├── crawler.py             # Web crawler
│   ├── analyzer.py            # AI analyzer
│   └── knowledge_base.py      # Knowledge management
├── .memory/                    # System Memory (Librarian)
│   ├── file_registry.json     # File index
│   └── code_structure.json    # Code index
└── global/                     # Global System Rules
```

---

## 4. System Integration (Global System v35.0)

### 📜 Mandatory Protocols

| Protocol | Reference | Enforcement |
|----------|-----------|-------------|
| **Librarian Protocol** | `global/rules/103_librarian_protocol.md` | MANDATORY |
| **Anti-Hallucination Oath** | `global/rules/104_anti_hallucination.md` | MANDATORY |
| **Speckit Protocol (SDD)** | `global/rules/105_speckit_protocol.md` | MANDATORY |
| **Context First** | `global/rules/99_context_first.md` | MANDATORY |
| **Shadow Architect** | `global/rules/101_shadow_architect.md` | RECOMMENDED |
| **Evolution Engine** | `global/rules/100_evolution_engine.md` | RECOMMENDED |

### ✅ Pre-Commit Checklist
Before any code commit, you MUST verify:
- [ ] `.memory/file_registry.json` checked for duplicates
- [ ] Relevant `.spec.md` file exists and is current
- [ ] Tests pass (≥90% coverage backend, ≥95% frontend)
- [ ] Security rules applied (OWASP Top 10)
- [ ] Both Arabic and English translations present
- [ ] Docker build succeeds

---

## 5. Roles & Responsibilities

### 🎭 Project Roles

| Role | Persona | Responsibility |
|------|---------|----------------|
| **Lead Architect** | The Visionary | Overall system design, tech decisions |
| **Backend Specialist** | The Engine | FastAPI, SQLAlchemy, PostgreSQL |
| **Frontend Specialist** | The Artist | React, Tailwind, RTL support |
| **ML Engineer** | The Oracle | YOLO, PyTorch, model training |
| **Security Auditor** | The Guardian | Authentication, encryption, OWASP |
| **QA Engineer** | The Skeptic | Testing, coverage, E2E |
| **DevOps Engineer** | The Deployer | Docker, CI/CD, Cloudflare |
| **Shadow Architect** | The Critic | Challenge all decisions, find weaknesses |

### 🤖 AI Agent Behavior
- **Always read context first** (Rule 99)
- **Never create duplicate files** (Rule 103)
- **Verify all imports before coding** (Rule 104)
- **Write specs before implementation** (Rule 105)
- **Swear the Verification Oath** before every import

---

## 6. API Standards

### 🔌 Endpoint Conventions
- **Base URL:** `/api/v1/`
- **Versioning:** URL-based (`/api/v1/`, `/api/v2/`)
- **Naming:** kebab-case (`/api/v1/disease-detection`)
- **Methods:** RESTful (GET, POST, PUT, PATCH, DELETE)

### 📋 Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2026-01-17T12:00:00Z"
}
```

### ❌ Error Format
```json
{
  "success": false,
  "error": {
    "code": "AUTH_001",
    "message": "Invalid credentials",
    "details": { ... }
  },
  "timestamp": "2026-01-17T12:00:00Z"
}
```

---

## 7. Security Mandates

### 🔐 Authentication & Authorization
1. **JWT-based authentication** with short-lived tokens
2. **2FA (TOTP) mandatory** for admin/superuser roles
3. **Role-Based Access Control (RBAC)** enforcement
4. **Account lockout** after 5 failed attempts

### 🛡️ Data Protection
1. **All passwords hashed** with bcrypt (cost factor ≥ 12)
2. **Sensitive data encrypted** at rest and in transit
3. **PII anonymization** in logs
4. **Secure file upload** with type and size validation

### 🚨 Infrastructure Security
1. **Cloudflare WAF** enabled
2. **DDoS protection** at edge
3. **Rate limiting** on all endpoints
4. **Security headers** (HSTS, CSP, X-Frame-Options)

---

## 8. Quality Gates

### ✅ Definition of Done
A feature is DONE when:
- [ ] Code passes all linters (ESLint, Black, isort)
- [ ] Unit tests written and passing (≥80% coverage)
- [ ] Integration tests passing
- [ ] API documentation updated (OpenAPI)
- [ ] UI components translated (AR + EN)
- [ ] Security review completed
- [ ] Code reviewed by peer
- [ ] `.spec.md` updated

### 🚫 Definition of Broken
A feature is BROKEN when:
- ❌ Tests fail on CI
- ❌ Linter errors exist
- ❌ Missing translations
- ❌ Security vulnerabilities detected
- ❌ API contract broken

---

## 9. Trusted Data Sources

The Image Crawler service ONLY fetches data from these 17 verified sources:

### Academic (5)
1. **PlantVillage** (95% reliability)
2. **CABI** (98% reliability)
3. **Cornell University** (96% reliability)
4. **UC IPM** (95% reliability)
5. **Invasive Species Compendium** (96% reliability)

### Governmental (4)
1. **EPPO** (97% reliability)
2. **FAO** (98% reliability)
3. **USDA** (97% reliability)
4. **PaDIL** (94% reliability)

### Arabic Sources (2)
1. **Arab Organization for Agricultural Development** (90% reliability)
2. **ICARDA** (92% reliability)

### Image Sources (6)
- Google Images, Bing Images, Unsplash, Flickr, Bugwood Images, iNaturalist

---

## 10. Amendment Process

This Constitution may be amended by:
1. **Proposal:** Submit change request with rationale
2. **Review:** Shadow Architect critique
3. **Approval:** Lead Architect sign-off
4. **Ratification:** Update version number and date

---

**Signed:**  
🏛️ **The Architect** | Global System v35.0  
📅 **Ratified:** 2026-01-17

---

*"This is the Law. We plan before we build, and we respect what exists."*
