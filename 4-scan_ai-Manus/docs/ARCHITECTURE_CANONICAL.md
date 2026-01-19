# 🏗️ Gaara AI - Canonical Architecture

**Version:** 3.0  
**Date:** 2025-11-18  
**Status:** Phase 2 - Consolidation  
**OSF Score Target:** 0.90

---

## 📁 Canonical Project Structure

```
gaara_scan_ai_final_4.3/                    # Project root
│
├── backend/                                 # Backend application (FastAPI)
│   ├── src/
│   │   ├── main.py                         # Main entry point (from clean_project)
│   │   │
│   │   ├── core/                           # Core application modules
│   │   │   ├── __init__.py
│   │   │   ├── app_factory.py             # FastAPI app factory
│   │   │   ├── config.py                  # Configuration management
│   │   │   ├── database.py                # Database setup & session
│   │   │   ├── logging_config.py          # Logging configuration
│   │   │   └── dependencies.py            # FastAPI dependencies
│   │   │
│   │   ├── api/                            # API routes (refactored from api_router.py)
│   │   │   ├── __init__.py
│   │   │   ├── v1/                        # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py                # Authentication endpoints
│   │   │   │   ├── users.py               # User management endpoints
│   │   │   │   ├── farms.py               # Farm management endpoints
│   │   │   │   ├── diagnosis.py           # Disease diagnosis endpoints
│   │   │   │   ├── ai_management.py       # AI management endpoints
│   │   │   │   ├── backup.py              # Backup endpoints
│   │   │   │   └── notifications.py       # Notification endpoints
│   │   │   └── router.py                  # Main API router
│   │   │
│   │   ├── models/                         # Database models (from database_models.py)
│   │   │   ├── __init__.py
│   │   │   ├── user.py                    # User model
│   │   │   ├── farm.py                    # Farm model
│   │   │   ├── plant.py                   # Plant model
│   │   │   ├── disease.py                 # Disease model
│   │   │   ├── diagnosis.py               # Diagnosis model
│   │   │   ├── sensor.py                  # Sensor model
│   │   │   └── activity_log.py            # Activity log model
│   │   │
│   │   ├── schemas/                        # Pydantic schemas (DTOs)
│   │   │   ├── __init__.py
│   │   │   ├── user.py                    # User schemas
│   │   │   ├── farm.py                    # Farm schemas
│   │   │   ├── diagnosis.py               # Diagnosis schemas
│   │   │   └── common.py                  # Common schemas
│   │   │
│   │   ├── services/                       # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py            # Authentication service
│   │   │   ├── user_service.py            # User management service
│   │   │   ├── farm_service.py            # Farm management service
│   │   │   ├── diagnosis_service.py       # Diagnosis service
│   │   │   └── notification_service.py    # Notification service
│   │   │
│   │   ├── modules/                        # Feature modules (from src/modules/)
│   │   │   ├── __init__.py
│   │   │   ├── ai_management/             # AI model management
│   │   │   ├── disease_diagnosis/         # Disease diagnosis
│   │   │   ├── image_processing/          # Image processing
│   │   │   ├── user_management/           # User management
│   │   │   ├── backup_module/             # Backup & restore
│   │   │   ├── notifications/             # Notification system
│   │   │   ├── permissions/               # Permission management
│   │   │   ├── activity_log/              # Activity logging
│   │   │   └── [30+ other modules]/
│   │   │
│   │   ├── utils/                          # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── security.py                # Security utilities
│   │   │   ├── validators.py              # Input validators
│   │   │   ├── helpers.py                 # Helper functions
│   │   │   └── constants.py               # Constants
│   │   │
│   │   └── middleware/                     # Custom middleware
│   │       ├── __init__.py
│   │       ├── auth_middleware.py         # Authentication middleware
│   │       ├── cors_middleware.py         # CORS middleware
│   │       ├── logging_middleware.py      # Logging middleware
│   │       └── error_handler.py           # Error handling middleware
│   │
│   ├── tests/                              # Backend tests (from clean_project)
│   │   ├── __init__.py
│   │   ├── conftest.py                    # Pytest configuration
│   │   ├── unit/                          # Unit tests
│   │   │   ├── test_models.py
│   │   │   ├── test_services.py
│   │   │   └── test_utils.py
│   │   ├── integration/                   # Integration tests
│   │   │   ├── test_api.py
│   │   │   ├── test_database.py
│   │   │   └── test_modules.py
│   │   └── e2e/                           # End-to-end tests
│   │       └── test_workflows.py
│   │
│   ├── alembic/                            # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── requirements.txt                    # Python dependencies (merged)
│   ├── requirements-dev.txt                # Development dependencies
│   ├── Dockerfile                          # Backend Docker image
│   └── .env.example                        # Environment variables template
│
├── frontend/                               # Frontend application (React)
│   ├── src/                                # (from gaara_ai_integrated/frontend/)
│   │   ├── App.jsx                        # Main app component
│   │   ├── main.jsx                       # Entry point
│   │   │
│   │   ├── components/                    # Reusable components (47+)
│   │   │   ├── ui/                        # shadcn/ui components
│   │   │   ├── layout/                    # Layout components
│   │   │   ├── forms/                     # Form components
│   │   │   └── [other components]/
│   │   │
│   │   ├── pages/                         # Page components (30+)
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Farms.jsx
│   │   │   ├── Diagnosis.jsx
│   │   │   └── [other pages]/
│   │   │
│   │   ├── services/                      # API services
│   │   │   ├── api.js                     # Base API service
│   │   │   ├── authService.js             # Auth service
│   │   │   ├── farmService.js             # Farm service
│   │   │   └── [other services]/
│   │   │
│   │   ├── context/                       # React contexts
│   │   │   ├── AuthContext.jsx            # Authentication context
│   │   │   └── AppContext.jsx             # App context
│   │   │
│   │   ├── hooks/                         # Custom hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useApi.js
│   │   │   └── [other hooks]/
│   │   │
│   │   ├── utils/                         # Utility functions
│   │   │   ├── constants.js
│   │   │   ├── helpers.js
│   │   │   └── validators.js
│   │   │
│   │   └── styles/                        # CSS files
│   │       ├── index.css
│   │       └── tailwind.css
│   │
│   ├── public/                            # Static assets
│   ├── package.json                       # Node dependencies
│   ├── vite.config.js                     # Vite configuration
│   ├── tailwind.config.js                 # Tailwind configuration
│   ├── Dockerfile                         # Frontend Docker image
│   └── .env.example                       # Environment variables template
│
├── docker/                                 # Docker services (from clean_project)
│   ├── postgres/                          # PostgreSQL configuration
│   ├── redis/                             # Redis configuration
│   ├── nginx/                             # NGINX configuration
│   ├── elasticsearch/                     # Elasticsearch configuration
│   ├── prometheus/                        # Prometheus configuration
│   ├── grafana/                           # Grafana configuration
│   └── [20+ other services]/
│
├── docs/                                   # Documentation
│   ├── README.md                          # Project overview
│   ├── ARCHITECTURE.md                    # This file
│   ├── API_DOCUMENTATION.md               # API documentation
│   ├── DATABASE_SCHEMA.md                 # Database schema
│   ├── DEPLOYMENT_GUIDE.md                # Deployment guide
│   ├── TESTING_STRATEGY.md                # Testing strategy
│   ├── SECURITY_GUIDELINES.md             # Security guidelines
│   └── [other docs]/
│
├── scripts/                                # Utility scripts (merged from all)
│   ├── setup_and_run.sh                   # Setup and run script
│   ├── start_services.sh                  # Start services script
│   ├── backup.sh                          # Backup script
│   └── [other scripts]/
│
├── .github/                                # GitHub configuration
│   └── workflows/                         # GitHub Actions workflows
│       ├── ci.yml                         # CI pipeline
│       └── deploy.yml                     # Deployment pipeline
│
├── .env.example                            # Environment variables template
├── docker-compose.yml                      # Docker Compose configuration
├── .gitignore                              # Git ignore file
├── .flake8                                 # Flake8 configuration
├── .eslintrc.json                          # ESLint configuration
├── .prettierrc                             # Prettier configuration
├── pytest.ini                              # Pytest configuration
├── README.md                               # Project README
├── CHANGELOG.md                            # Version history
├── LICENSE                                 # License file
└── requirements.txt                        # Root requirements (for convenience)
```

---

## 🎯 Key Architectural Decisions

### 1. Modular Backend Structure
- **Core**: Essential app setup (config, database, logging)
- **API**: RESTful endpoints organized by version
- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic validation schemas
- **Services**: Business logic layer
- **Modules**: Feature-specific modules (30+)

### 2. Clean Frontend Architecture
- **Component-based**: Reusable UI components
- **Page-based routing**: Clear page structure
- **Service layer**: API abstraction
- **Context API**: State management
- **Custom hooks**: Reusable logic

### 3. Microservices-Ready
- **Docker**: Each service in separate container
- **Docker Compose**: Orchestration for 25+ services
- **NGINX**: Reverse proxy and load balancing
- **Monitoring**: Prometheus + Grafana

---

**Next:** Execute migration plan (Task 2.1.3)

