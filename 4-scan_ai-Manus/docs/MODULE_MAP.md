# Module Map

## Project: Gaara Scan AI v4.3
**Type:** Full-Stack Web Application
**Framework:** FastAPI (Backend) + React/Vite (Frontend)
**Last Updated:** 2025-12-05

## Architecture Overview

Gaara Scan AI is a smart agriculture system with AI-powered plant disease diagnosis. The architecture follows a modular monolith pattern with microservices-ready Docker infrastructure.

**Key Features:**
- AI-powered plant disease diagnosis
- Farm management system
- IoT sensor integration
- Real-time analytics
- Multi-language support (Arabic/English)

---

## Directory Structure

```
gaara_scan_ai_final_4.3/
├── backend/
│   ├── src/
│   │   ├── main.py                 # Application entry point
│   │   ├── core/                   # Core configuration
│   │   │   ├── app_factory.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── routes.py
│   │   │   └── middleware.py
│   │   ├── api/v1/                 # API routes
│   │   │   ├── auth.py
│   │   │   ├── farms.py
│   │   │   ├── diagnosis.py
│   │   │   └── reports.py
│   │   ├── models/                 # Database models
│   │   │   ├── user.py
│   │   │   ├── farm.py
│   │   │   ├── diagnosis.py
│   │   │   └── report.py
│   │   ├── modules/                # Business modules (30+)
│   │   │   ├── ai_agent/
│   │   │   ├── ai_management/
│   │   │   ├── auth/
│   │   │   ├── disease_diagnosis/
│   │   │   ├── mfa/
│   │   │   ├── notifications/
│   │   │   └── ...
│   │   ├── middleware/
│   │   │   └── csrf_middleware.py
│   │   ├── utils/
│   │   │   ├── security.py
│   │   │   ├── password_policy.py
│   │   │   └── security_audit.py
│   │   └── schemas/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── e2e/
│   │   └── performance/
│   ├── alembic/                    # Database migrations
│   ├── scripts/
│   └── requirements.txt
├── frontend/
│   ├── components/
│   │   ├── Layout/                 # Navbar, Sidebar, Footer
│   │   ├── Router/                 # AppRouter
│   │   └── UI/                     # 50+ UI components
│   ├── pages/                      # 20+ page components
│   ├── services/                   # API services
│   ├── context/                    # React contexts
│   ├── hooks/
│   ├── utils/
│   │   ├── csrf.js
│   │   └── sanitize.js
│   ├── App.jsx
│   ├── main.jsx
│   └── package.json
├── docker/                         # 25+ Docker services
├── docs/                           # 80+ documentation files
├── .memory/                        # AI memory system
├── logs/                           # Structured logging
├── prompts/                        # AI prompts
├── knowledge/                      # Knowledge base
├── examples/                       # Code examples
├── workflows/                      # Automation workflows
├── roles/                          # Agent roles
└── github/global/                  # Global Guidelines
```

---

## Frontend Modules

### Pages

| Page | Path | Route | Components Used | API Calls |
|------|------|-------|-----------------|-----------|
| Login | `pages/Login.jsx` | `/login` | AuthContext | `POST /api/v1/auth/login` |
| Register | `pages/Register.jsx` | `/register` | AuthContext | `POST /api/v1/auth/register` |
| ForgotPassword | `pages/ForgotPassword.jsx` | `/forgot-password` | Form | `POST /api/v1/auth/forgot-password` |
| ResetPassword | `pages/ResetPassword.jsx` | `/reset-password/:token` | Form | `POST /api/v1/auth/reset-password` |
| Dashboard | `pages/Dashboard.jsx` | `/dashboard` | Charts, Analytics | `GET /api/dashboard/stats` |
| Farms | `pages/Farms.jsx` | `/farms` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/farms` |
| Diagnosis | `pages/Diagnosis.jsx` | `/diagnosis` | ImageUpload, Results | `POST /api/v1/diagnosis/upload` |
| Diseases | `pages/Diseases.jsx` | `/diseases` | Table, Details | `GET /api/v1/diseases` |
| Crops | `pages/Crops.jsx` | `/crops` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/crops` |
| Sensors | `pages/Sensors.jsx` | `/sensors` | Charts, Table | `GET/POST/PUT/DELETE /api/v1/sensors` |
| Equipment | `pages/Equipment.jsx` | `/equipment` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/equipment` |
| Inventory | `pages/Inventory.jsx` | `/inventory` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/inventory` |
| Breeding | `pages/Breeding.jsx` | `/breeding` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/breeding` |
| Reports | `pages/Reports.jsx` | `/reports` | Table, Download | `GET/POST /api/v1/reports` |
| Analytics | `pages/Analytics.jsx` | `/analytics` | Charts, Filters | `GET /api/v1/analytics` |
| Settings | `pages/Settings.jsx` | `/settings` | Forms | `GET/PUT /api/settings` |
| Users | `pages/Users.jsx` | `/users` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/users` |
| Profile | `pages/Profile.jsx` | `/profile` | Forms | `GET/PUT /api/v1/auth/me` |
| Companies | `pages/Companies.jsx` | `/companies` | Table, Forms | `GET/POST/PUT/DELETE /api/v1/companies` |
| SetupWizard | `pages/SetupWizard.jsx` | `/setup` | Wizard, Forms | `POST /api/setup` |
| Error401 | `pages/errors/Error401.jsx` | `/401` | ErrorDisplay | - |
| Error403 | `pages/errors/Error403.jsx` | `/403` | ErrorDisplay | - |
| Error404 | `pages/errors/Error404.jsx` | `/404` | ErrorDisplay | - |
| Error500 | `pages/errors/Error500.jsx` | `/500` | ErrorDisplay | - |

### Components

| Component | Path | Used By | Props | State |
|-----------|------|---------|-------|-------|
| Navbar | `components/Layout/Navbar.jsx` | All pages | `user` | `isMenuOpen` |
| Sidebar | `components/Layout/Sidebar.jsx` | All pages | `activeMenu` | `collapsed` |
| Footer | `components/Layout/Footer.jsx` | All pages | - | - |
| AppRouter | `components/Router/AppRouter.jsx` | App.jsx | - | `routes` |
| Button | `components/UI/button.jsx` | All pages | `variant`, `size` | - |
| Card | `components/UI/card.jsx` | All pages | `children` | - |
| Table | `components/UI/table.jsx` | List pages | `data`, `columns` | - |
| Dialog | `components/UI/dialog.jsx` | Forms | `open`, `onClose` | `isOpen` |
| Input | `components/UI/input.jsx` | Forms | `type`, `value` | - |
| Select | `components/UI/select.jsx` | Forms | `options`, `value` | - |
| Charts | `components/Charts/DashboardCharts.jsx` | Dashboard | `data` | - |
| Analytics | `components/Analytics/AdvancedAnalytics.jsx` | Analytics | `data` | - |

### Services

| Service | Path | Purpose | Methods |
|---------|------|---------|---------|
| ApiService | `services/ApiService.js` | HTTP client wrapper | `get()`, `post()`, `put()`, `delete()` |
| AuthService | `services/AuthService.js` | Authentication | `login()`, `logout()`, `getToken()` |
| ApiServiceEnhanced | `services/ApiServiceEnhanced.js` | Enhanced API client | Full CRUD + error handling |

### Utils

| Util | Path | Purpose | Functions |
|------|------|---------|-----------|
| CSRF | `utils/csrf.js` | CSRF protection | `getToken()`, `setupInterceptor()` |
| Sanitize | `utils/sanitize.js` | XSS prevention | `sanitizeHtml()`, `escapeText()` |

---

## Backend Modules

### Core Modules

| Module | Path | Purpose | Files |
|--------|------|---------|-------|
| App Factory | `core/app_factory.py` | Application creation | FastAPI app setup |
| Config | `core/config.py` | Configuration | Pydantic settings |
| Database | `core/database.py` | Database connection | SQLAlchemy setup |
| Routes | `core/routes.py` | Route registration | API router setup |
| Middleware | `core/middleware.py` | Middleware stack | CORS, logging, etc. |

### API Routes

| Route | Path | Methods | Endpoints | Middleware |
|-------|------|---------|-----------|------------|
| Health | `api/v1/health.py` | GET | `/api/v1/health` | - |
| Auth Routes | `api/v1/auth.py` | POST, GET, PUT | `/api/v1/auth/login`, `/register`, `/me`, `/mfa/*`, `/forgot-password`, `/reset-password` | - |
| Farm Routes | `api/v1/farms.py` | GET, POST, PUT, DELETE | `/api/v1/farms`, `/api/v1/farms/:id` | auth |
| Diagnosis Routes | `api/v1/diagnosis.py` | POST, GET | `/api/v1/diagnosis/upload`, `/api/v1/diagnosis/history` | auth |
| Reports Routes | `api/v1/reports.py` | GET, POST | `/api/v1/reports`, `/api/v1/reports/generate` | auth |
| Crops Routes | `api/v1/crops.py` | GET, POST, PUT, DELETE | `/api/v1/crops`, `/api/v1/crops/:id` | auth |
| Diseases Routes | `api/v1/diseases.py` | GET, POST, PUT, DELETE | `/api/v1/diseases`, `/api/v1/diseases/:id` | auth |
| Sensors Routes | `api/v1/sensors.py` | GET, POST, PUT, DELETE | `/api/v1/sensors`, `/api/v1/sensors/:id` | auth |
| Equipment Routes | `api/v1/equipment.py` | GET, POST, PUT, DELETE | `/api/v1/equipment`, `/api/v1/equipment/:id` | auth |
| Inventory Routes | `api/v1/inventory.py` | GET, POST, PUT, DELETE | `/api/v1/inventory`, `/api/v1/inventory/:id` | auth |
| Breeding Routes | `api/v1/breeding.py` | GET, POST, PUT, DELETE | `/api/v1/breeding`, `/api/v1/breeding/:id` | auth |
| Users Routes | `api/v1/users.py` | GET, POST, PUT, DELETE | `/api/v1/users`, `/api/v1/users/:id` | auth, admin |
| Companies Routes | `api/v1/companies.py` | GET, POST, PUT, DELETE | `/api/v1/companies`, `/api/v1/companies/:id` | auth |
| Analytics Routes | `api/v1/analytics.py` | GET | `/api/v1/analytics` | auth |

### Business Modules (30+)

| Module | Path | Purpose | Key Files |
|--------|------|---------|-----------|
| AI Agent | `modules/ai_agent/` | AI agent system | service.py, api.py |
| AI Management | `modules/ai_management/` | AI model management | service.py, load_balancer.py |
| Auth | `modules/auth/` | Authentication | auth_service.py, api.py |
| Disease Diagnosis | `modules/disease_diagnosis/` | Plant disease AI | diagnosis_engine.py, service.py |
| MFA | `modules/mfa/` | Multi-factor auth | mfa_service.py |
| Notifications | `modules/notifications/` | Notification system | service.py, api.py |
| Permissions | `modules/permissions/` | Role-based access | permissions.py |
| Backup Restore | `modules/backup_restore/` | Backup management | backup_service.py |
| Image Processing | `modules/image_processing/` | Image handling | image_processor.py |
| User Management | `modules/user_management/` | User CRUD | service.py, api.py |
| Settings | `modules/settings/` | App settings | service.py |
| Performance Monitoring | `modules/performance_monitoring/` | Metrics | service.py |
| Security | `modules/security/` | Security utils | - |

### Models

| Model | Path | Table | Fields | Relationships |
|-------|------|-------|--------|---------------|
| User | `models/user.py` | `users` | id, email, password_hash, name, role, mfa_enabled, phone, avatar_url | hasMany(Farms, Diagnoses, Reports) |
| Farm | `models/farm.py` | `farms` | id, name, location, latitude, longitude, area, crop_type, user_id | belongsTo(User), hasMany(Diagnoses) |
| Diagnosis | `models/diagnosis.py` | `diagnoses` | id, image_url, disease_name, confidence, severity, farm_id, user_id | belongsTo(User, Farm) |
| Report | `models/report.py` | `reports` | id, title, type, format, file_url, user_id | belongsTo(User) |
| Crop | `models/crop.py` | `crops` | id, name, variety, description, growing_season | - |
| Disease | `models/disease.py` | `diseases` | id, name, description, symptoms, treatment | - |
| Sensor | `models/sensor.py` | `sensors` | id, name, type, location, farm_id | belongsTo(Farm) |
| Equipment | `models/equipment.py` | `equipment` | id, name, type, status, farm_id | belongsTo(Farm) |
| Inventory | `models/inventory.py` | `inventory` | id, item_name, quantity, unit, farm_id | belongsTo(Farm) |
| BreedingProgram | `models/breeding.py` | `breeding_programs` | id, name, description, start_date, farm_id | belongsTo(Farm) |
| Company | `models/company.py` | `companies` | id, name, address, phone, email | - |

### Middleware

| Middleware | Path | Purpose | Used By |
|------------|------|---------|---------|
| CSRF Middleware | `middleware/csrf_middleware.py` | CSRF protection | All state-changing routes |

### Utils

| Util | Path | Purpose | Functions |
|------|------|---------|-----------|
| Security | `utils/security.py` | XSS prevention | `sanitize_html()`, `validate_url()` |
| Password Policy | `utils/password_policy.py` | Password validation | `validate()`, `hash()`, `check_history()` |
| Security Audit | `utils/security_audit.py` | Security scanning | `run_audit()`, `generate_report()` |

---

## Database Schema

### Tables

| Table | Columns | Indexes | Foreign Keys |
|-------|---------|---------|--------------|
| users | id, email, password_hash, name, role, phone, mfa_enabled, mfa_secret, is_active, created_at, updated_at, deleted_at | email (unique) | - |
| farms | id, name, location, latitude, longitude, area, crop_type, soil_type, status, user_id, created_at, updated_at, deleted_at | user_id | user_id → users(id) |
| diagnoses | id, image_url, image_path, disease_name, confidence, severity, recommendations, farm_id, user_id, created_at | user_id, farm_id | user_id → users(id), farm_id → farms(id) |
| reports | id, title, type, format, file_url, file_path, parameters, status, user_id, created_at | user_id, status | user_id → users(id) |

### Relationships

```
users (1) ─── (N) farms
users (1) ─── (N) diagnoses
users (1) ─── (N) reports
farms (1) ─── (N) diagnoses
```

---

## Data Flow

### Example: Plant Disease Diagnosis

```
[User] → [Frontend: Diagnosis Page]
  ↓
  [Upload Image Button Click]
  ↓
  [Frontend: ApiService.uploadDiagnosis()]
  ↓
  [API Call: POST /api/v1/diagnosis/upload]
  ↓
  [Backend: diagnosis.router.py]
  ↓
  [Middleware: CSRF validation]
  ↓
  [Backend: DiagnosisController.upload()]
  ↓
  [Backend: DiagnosisService.analyze()]
  ↓
  [Backend: AI Engine (TensorFlow/PyTorch)]
  ↓
  [Backend: Diagnosis.model.py]
  ↓
  [Database: INSERT INTO diagnoses]
  ↓
  [Response: 201 Created with diagnosis results]
  ↓
  [Frontend: Update UI with results]
  ↓
  [User sees disease name, confidence, recommendations]
```

---

## Missing Files Checklist

### Frontend
- [x] All pages have corresponding routes
- [x] All components are documented
- [x] All services are implemented
- [x] All API calls are defined

### Backend
- [x] All routes have controllers
- [x] All controllers have services
- [x] All services have models
- [x] All models have migrations

### Database
- [x] All tables have migrations
- [x] All foreign keys are defined
- [x] All indexes are created

---

## Docker Services (25+)

| Service | Port | Purpose |
|---------|------|---------|
| postgres | 1605 | Database |
| redis | 1105 | Caching |
| backend | 1005 | API Server |
| frontend | 1505 | Web UI |
| nginx | 80/443 | Reverse Proxy |
| elasticsearch | 9200 | Search |
| kibana | 5601 | Log Visualization |
| prometheus | 9090 | Metrics |
| grafana | 3000 | Dashboards |
| rabbitmq | 5672 | Message Queue |
| vector_db | - | Vector Storage |
| yolo_detection | - | Object Detection |
| image_enhancement | - | Image Processing |
| ai_agents | - | AI Agents |
| websocket | - | Real-time |
| notification | - | Notifications |
| monitoring | - | Health Checks |

---

## Test Coverage

| Category | Files | Tests | Coverage |
|----------|-------|-------|----------|
| Unit Tests | 3 | 60+ | 80%+ |
| Integration Tests | 2 | 30+ | 70%+ |
| E2E Tests | 1 | 15+ | 60%+ |
| Performance Tests | 1 | 3 | - |
| **Total** | **7** | **105+** | **75%+** |

---

## Notes

- Module map last verified: 2025-12-05
- All security modules implemented
- Database migrations applied
- Admin user created
- Ready for production deployment
