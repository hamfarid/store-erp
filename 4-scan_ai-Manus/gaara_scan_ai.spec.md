# 📋 Gaara Scan AI - Technical Specification
## نظام الكشف الذكي عن أمراض النباتات | Intelligent Plant Disease Detection System

**Spec Version:** 1.0.0  
**Project Version:** 4.3.1  
**Status:** ADOPTION MODE (Existing Production System)  
**Last Updated:** 2026-01-17

---

## 1. Executive Summary

### 1.1 Project Overview
Gaara Scan AI is a comprehensive agricultural technology platform that combines:
- **AI-powered plant disease detection** using YOLOv8 and CNN models
- **Farm management system** for complete agricultural operations
- **Self-learning crawler** that continuously improves from trusted sources
- **Bilingual interface** with full Arabic and English support

### 1.2 Key Metrics (Current State)
| Metric | Value | Target |
|--------|-------|--------|
| Disease Detection Accuracy | 95%+ | ≥95% |
| API Response Time | <2s | <2s |
| Backend Test Coverage | 89% | ≥90% |
| Frontend Test Coverage | 100% | ≥95% |
| Production Readiness | 95% | 98% |
| Pages | 22 | 22 |
| API Endpoints | 13+ | 15+ |
| Functional Buttons | 136 | 136 |

---

## 2. System Architecture

### 2.1 Service Topology
```
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL LAYER                            │
│  Cloudflare CDN → WAF → DDoS Protection → E2E Encryption    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   GATEWAY LAYER                             │
│           Nginx Reverse Proxy (SSL/TLS, Load Balancing)     │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│   PRESENTATION    │ │   APPLICATION     │ │   AI/ML LAYER     │
│   Frontend        │ │   Backend API     │ │   ML Service      │
│   React + Vite    │ │   FastAPI         │ │   YOLO + PyTorch  │
│   Port: 4501      │ │   Port: 4001      │ │   Port: 4101      │
└───────────────────┘ └───────────────────┘ └───────────────────┘
                              │                       │
                              ▼                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│  PostgreSQL (8502)  │  Redis (6379)  │  AI Service (4601)   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Service Definitions

#### 2.2.1 Frontend Service
- **Technology:** React 18 + Vite + Tailwind CSS
- **Port:** 4501
- **Features:**
  - 22 responsive pages
  - Full RTL (Arabic) support
  - Dark mode
  - 136 functional UI elements
- **Container:** `scan_ai-Manus-frontend`

#### 2.2.2 Backend API Service
- **Technology:** FastAPI + SQLAlchemy + Alembic
- **Port:** 4001
- **Features:**
  - RESTful API with OpenAPI 3.0 documentation
  - JWT authentication with refresh tokens
  - 2FA (TOTP) support
  - Rate limiting and CORS protection
- **Container:** `scan_ai-Manus-backend`

#### 2.2.3 ML Service
- **Technology:** FastAPI + PyTorch + YOLO v8
- **Port:** 4101
- **Features:**
  - Real-time disease detection (<2s)
  - Model versioning
  - Batch processing support
- **Container:** `scan_ai-Manus-ml`

#### 2.2.4 AI/Crawler Service
- **Technology:** FastAPI + BeautifulSoup + OpenAI Vision
- **Port:** 4601
- **Features:**
  - Automated image crawling from 17 sources
  - AI-powered image analysis
  - Knowledge base management
  - Auto-training pipeline
- **Container:** `scan_ai-Manus-ai`

#### 2.2.5 Database Service
- **Technology:** PostgreSQL 16 Alpine
- **Port:** 8502
- **Features:**
  - 12 data models
  - Automatic migrations (Alembic)
  - Backup automation
- **Container:** `scan_ai-Manus-database`

#### 2.2.6 Cache Service
- **Technology:** Redis 7 Alpine
- **Port:** 6379
- **Features:**
  - Session management
  - Rate limiting storage
  - Pub/Sub messaging
- **Container:** `scan_ai-Manus-redis`

---

## 3. Database Schema

### 3.1 Core Models

#### 3.1.1 User Model
```python
class User(Base):
    id: UUID (PK)
    email: String (unique, indexed)
    username: String (unique)
    password_hash: String
    full_name: String
    role: Enum [admin, user, agronomist, researcher]
    is_active: Boolean
    is_verified: Boolean
    totp_secret: String (nullable)
    totp_enabled: Boolean
    failed_login_attempts: Integer
    locked_until: DateTime (nullable)
    created_at: DateTime
    updated_at: DateTime
```

#### 3.1.2 Farm Model
```python
class Farm(Base):
    id: UUID (PK)
    name: String
    location: String
    area_hectares: Float
    owner_id: UUID (FK → User)
    coordinates: JSON (nullable)
    soil_type: String (nullable)
    irrigation_type: Enum
    created_at: DateTime
    updated_at: DateTime
```

#### 3.1.3 Crop Model
```python
class Crop(Base):
    id: UUID (PK)
    name: String
    scientific_name: String
    farm_id: UUID (FK → Farm)
    planting_date: Date
    expected_harvest_date: Date
    status: Enum [planted, growing, harvesting, harvested]
    area_hectares: Float
    created_at: DateTime
    updated_at: DateTime
```

#### 3.1.4 Disease Model
```python
class Disease(Base):
    id: UUID (PK)
    name: String (indexed)
    name_ar: String
    scientific_name: String
    description: Text
    description_ar: Text
    symptoms: JSON
    symptoms_ar: JSON
    treatments: JSON
    treatments_ar: JSON
    prevention: JSON
    severity: Enum [low, medium, high, critical]
    affected_crops: JSON
    images: JSON (URLs)
    source: String
    confidence_threshold: Float
    created_at: DateTime
    updated_at: DateTime
```

#### 3.1.5 Diagnosis Model
```python
class Diagnosis(Base):
    id: UUID (PK)
    user_id: UUID (FK → User)
    crop_id: UUID (FK → Crop, nullable)
    disease_id: UUID (FK → Disease, nullable)
    image_path: String
    confidence_score: Float
    detection_boxes: JSON (YOLO output)
    status: Enum [pending, completed, reviewed]
    notes: Text (nullable)
    treatment_applied: Boolean
    created_at: DateTime
    reviewed_at: DateTime (nullable)
```

### 3.2 Relationships
```
User ─────┬─── has_many ───► Farm
          │
          └─── has_many ───► Diagnosis

Farm ─────────── has_many ───► Crop

Crop ─────────── has_many ───► Diagnosis

Disease ──────── has_many ───► Diagnosis
```

---

## 4. API Specification

### 4.1 Authentication Endpoints

#### POST `/api/v1/auth/register`
Register a new user account.
```json
Request:
{
  "email": "string",
  "username": "string",
  "password": "string",
  "full_name": "string"
}

Response (201):
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "string",
    "username": "string"
  }
}
```

#### POST `/api/v1/auth/login`
Authenticate user and return tokens.
```json
Request:
{
  "email": "string",
  "password": "string",
  "totp_code": "string" // Optional, required if 2FA enabled
}

Response (200):
{
  "success": true,
  "data": {
    "access_token": "jwt",
    "refresh_token": "jwt",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

#### POST `/api/v1/auth/refresh`
Refresh access token.
```json
Request:
{
  "refresh_token": "jwt"
}

Response (200):
{
  "success": true,
  "data": {
    "access_token": "jwt",
    "expires_in": 900
  }
}
```

### 4.2 2FA Endpoints

#### POST `/api/v1/2fa/setup`
Initialize 2FA setup for user.
```json
Response (200):
{
  "success": true,
  "data": {
    "secret": "base32_secret",
    "qr_code": "base64_image",
    "manual_entry_key": "formatted_secret"
  }
}
```

#### POST `/api/v1/2fa/verify`
Verify TOTP code and enable 2FA.
```json
Request:
{
  "totp_code": "string"
}

Response (200):
{
  "success": true,
  "message": "2FA enabled successfully"
}
```

### 4.3 Diagnosis Endpoints

#### POST `/api/v1/diagnosis`
Create new disease diagnosis from image.
```
Content-Type: multipart/form-data

Request:
- image: File (required, JPEG/PNG/WebP, max 50MB)
- crop_id: UUID (optional)
- notes: string (optional)

Response (201):
{
  "success": true,
  "data": {
    "id": "uuid",
    "disease": {
      "name": "Early Blight",
      "name_ar": "اللفحة المبكرة",
      "confidence": 0.97,
      "severity": "high"
    },
    "detection_boxes": [...],
    "treatments": [...],
    "processing_time_ms": 1200
  }
}
```

#### GET `/api/v1/diagnosis/{id}`
Get diagnosis details by ID.

#### GET `/api/v1/diagnosis`
List all diagnoses for current user with pagination.
```
Query Parameters:
- page: int (default: 1)
- limit: int (default: 20, max: 100)
- crop_id: UUID (optional filter)
- status: string (optional filter)
```

### 4.4 ML Service Endpoints

#### POST `/api/v1/ml/detect`
Direct YOLO detection endpoint.
```json
Request (multipart/form-data):
- image: File

Response (200):
{
  "success": true,
  "data": {
    "detections": [
      {
        "class": "early_blight",
        "confidence": 0.97,
        "bbox": [x1, y1, x2, y2]
      }
    ],
    "inference_time_ms": 150
  }
}
```

### 4.5 Crawler Endpoints

#### POST `/api/v1/crawler/search`
Initiate disease image search from trusted sources.
```json
Request:
{
  "disease_name": "string",
  "max_images": 100,
  "sources": ["plantvillage", "cabi", "fao"]
}

Response (202):
{
  "success": true,
  "data": {
    "job_id": "uuid",
    "status": "queued"
  }
}
```

#### GET `/api/v1/crawler/status/{job_id}`
Get crawler job status.

#### GET `/api/v1/crawler/stats`
Get knowledge base statistics.
```json
Response (200):
{
  "success": true,
  "data": {
    "total_diseases": 40,
    "total_images": 15000,
    "sources_active": 17,
    "last_crawl": "2026-01-17T10:00:00Z"
  }
}
```

### 4.6 Farm Management Endpoints

#### CRUD for Farms: `/api/v1/farms`
#### CRUD for Crops: `/api/v1/crops`
#### CRUD for Equipment: `/api/v1/equipment`
#### CRUD for Inventory: `/api/v1/inventory`
#### CRUD for Workers: `/api/v1/workers`

---

## 5. Frontend Specification

### 5.1 Page Inventory (22 Pages)

| # | Page | Route | Description |
|---|------|-------|-------------|
| 1 | Dashboard | `/` | Main dashboard with analytics |
| 2 | Login | `/login` | User authentication |
| 3 | Register | `/register` | User registration |
| 4 | Forgot Password | `/forgot-password` | Password recovery |
| 5 | Reset Password | `/reset-password` | Password reset |
| 6 | Diagnosis | `/diagnosis` | Upload and diagnose plant images |
| 7 | Diseases | `/diseases` | Disease catalog and information |
| 8 | Farms | `/farms` | Farm management |
| 9 | Crops | `/crops` | Crop tracking |
| 10 | Equipment | `/equipment` | Equipment management |
| 11 | Inventory | `/inventory` | Inventory tracking |
| 12 | Workers | `/workers` | Worker management |
| 13 | Sensors | `/sensors` | IoT sensor monitoring |
| 14 | Reports | `/reports` | Generate reports |
| 15 | Analytics | `/analytics` | Advanced analytics |
| 16 | Learning Dashboard | `/learning` | ML model performance |
| 17 | Image Crawler | `/crawler` | Crawler control panel |
| 18 | Users | `/users` | User management (admin) |
| 19 | Companies | `/companies` | Company management |
| 20 | Breeding | `/breeding` | Plant breeding module |
| 21 | Profile | `/profile` | User profile settings |
| 22 | Settings | `/settings` | System settings |

### 5.2 Component Architecture
```
frontend/
├── components/
│   ├── Layout/
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Footer.jsx
│   │   └── MainLayout.jsx
│   ├── UI/
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Modal.jsx
│   │   ├── Table.jsx
│   │   ├── Form/
│   │   └── ...50+ components
│   ├── Charts/
│   │   ├── LineChart.jsx
│   │   └── BarChart.jsx
│   └── Router/
│       ├── PrivateRoute.jsx
│       └── PublicRoute.jsx
├── context/
│   ├── AuthContext.jsx
│   └── DataContext.jsx
├── services/
│   ├── ApiService.js
│   └── AuthService.js
└── pages/
    └── [22 pages]
```

### 5.3 State Management
- **Authentication:** React Context (AuthContext)
- **Data:** React Context (DataContext)
- **Local State:** useState hooks
- **API Cache:** In-memory with invalidation

### 5.4 Styling
- **Framework:** Tailwind CSS
- **RTL Support:** Tailwind RTL plugin
- **Dark Mode:** Class-based switching
- **Responsive:** Mobile-first design

---

## 6. Security Specification

### 6.1 Authentication Flow
```
┌─────────┐       ┌─────────┐       ┌─────────┐
│  User   │──────►│ Login   │──────►│  JWT    │
│         │       │ Request │       │ Issued  │
└─────────┘       └─────────┘       └────┬────┘
                                         │
                       ┌─────────────────┘
                       ▼
              ┌────────────────┐
              │ 2FA Required?  │
              └───────┬────────┘
                 YES  │  NO
           ┌─────────┴─────────┐
           ▼                   ▼
    ┌────────────┐      ┌────────────┐
    │ TOTP Check │      │  Success   │
    └────────────┘      └────────────┘
```

### 6.2 Security Headers
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### 6.3 Rate Limiting
| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/v1/auth/*` | 5 requests | 1 minute |
| `/api/v1/*` | 60 requests | 1 minute |
| `/api/v1/diagnosis` | 10 requests | 1 minute |
| File uploads | 2 requests | 1 minute |

### 6.4 Password Policy
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character
- No dictionary words
- No user info (name, email)

---

## 7. Deployment Specification

### 7.1 Docker Compose Services
```yaml
services:
  - database     (PostgreSQL 16)
  - redis        (Redis 7)
  - backend      (FastAPI)
  - ml_service   (YOLO + PyTorch)
  - ai_service   (Image Crawler)
  - frontend     (React + Nginx)
```

### 7.2 Network Configuration
```
Network: Ai_project (external)

Internal Communication:
- backend ←→ database (5432)
- backend ←→ redis (6379)
- backend ←→ ml_service (4101)
- backend ←→ ai_service (4601)

External Access (via Nginx):
- frontend: 4501
- backend API: 4001
```

### 7.3 Volume Mounts
```yaml
volumes:
  - postgres_data      (Database persistence)
  - redis_data         (Cache persistence)
  - backend_uploads    (User uploads)
  - backend_results    (Processing results)
  - ai_models          (ML models)
  - ml_data            (Training data)
  - crawler_data       (Crawled images)
```

### 7.4 Health Checks
| Service | Endpoint | Interval |
|---------|----------|----------|
| Backend | `/api/v1/health` | 30s |
| ML Service | `/health` | 30s |
| AI Service | `/health` | 30s |
| Frontend | `/health` | 30s |
| Database | `pg_isready` | 10s |
| Redis | `redis-cli ping` | 10s |

---

## 8. Testing Specification

### 8.1 Test Categories
```
tests/
├── unit/           # Unit tests (isolated)
├── integration/    # Integration tests (with DB)
├── e2e/            # End-to-end tests (Playwright)
└── performance/    # Load tests (Locust)
```

### 8.2 Coverage Targets
| Component | Current | Target |
|-----------|---------|--------|
| Backend Unit | 89% | ≥90% |
| Backend Integration | 85% | ≥85% |
| Frontend Unit | 100% | ≥95% |
| E2E Critical Paths | 90% | 100% |

### 8.3 Test Commands
```bash
# Backend
cd backend && pytest tests/ -v --cov=src

# Frontend
cd frontend && npm run test:coverage

# E2E
cd backend && python -m pytest tests/e2e/ --browser chromium
```

---

## 9. Trusted Data Sources

### 9.1 Academic Sources
| Source | URL | Reliability |
|--------|-----|-------------|
| PlantVillage | plantvillage.psu.edu | 95% |
| CABI | cabi.org | 98% |
| Cornell | cornell.edu | 96% |
| UC IPM | ipm.ucanr.edu | 95% |
| ISC | cabi.org/isc | 96% |

### 9.2 Government Sources
| Source | URL | Reliability |
|--------|-----|-------------|
| EPPO | eppo.int | 97% |
| FAO | fao.org | 98% |
| USDA | usda.gov | 97% |
| PaDIL | padil.gov.au | 94% |

### 9.3 Arabic Sources
| Source | URL | Reliability |
|--------|-----|-------------|
| AOAD | aoad.org | 90% |
| ICARDA | icarda.org | 92% |

### 9.4 Image Sources
- Google Images (with license filter)
- Bing Images (with license filter)
- Unsplash (free license)
- Flickr (Creative Commons)
- Bugwood Images (agricultural focus)
- iNaturalist (citizen science)

---

## 10. Appendix

### 10.1 Environment Variables
```env
# Application
ENVIRONMENT=production
DEBUG=false
APP_PORT=4001
LOG_LEVEL=info

# Database
POSTGRES_DB=gaara_scan_ai
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=<secure>
DATABASE_URL=postgresql://...

# Redis
REDIS_HOST=scan_ai-Manus-redis
REDIS_PORT=6379
REDIS_PASSWORD=<secure>

# Security
SECRET_KEY=<secure>
JWT_SECRET=<secure>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# External APIs
OPENAI_API_KEY=<optional>

# Frontend
VITE_API_URL=http://localhost:4001/api/v1
```

### 10.2 Error Codes
| Code | Description |
|------|-------------|
| AUTH_001 | Invalid credentials |
| AUTH_002 | Account locked |
| AUTH_003 | 2FA required |
| AUTH_004 | Invalid TOTP code |
| DIAG_001 | Invalid image format |
| DIAG_002 | Image too large |
| DIAG_003 | Detection failed |
| ML_001 | Model not loaded |
| ML_002 | Inference timeout |

### 10.3 API Versioning Strategy
- Current: `/api/v1/`
- Next: `/api/v2/` (when breaking changes needed)
- Deprecation: 6-month notice
- Sunset: 12-month from deprecation

---

**Document Status:** APPROVED  
**Architect:** Global System v35.0  
**Date:** 2026-01-17

*"No Code Without Spec. This is the Law."*
