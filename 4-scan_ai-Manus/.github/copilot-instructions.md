# Gaara Scan AI v4.3.1 - AI Agent Instructions

## Architecture Overview

This is a full-stack **bilingual agricultural management system** (Arabic/English) with FastAPI backend and React frontend, focused on plant disease diagnosis and farm management using AI.

### Key Components
- **Backend**: FastAPI app at `backend/` with SQLAlchemy models, JWT auth, and PostgreSQL database
- **Frontend**: React/Vite SPA at `frontend/` with Tailwind CSS and Radix UI components
- **Database**: PostgreSQL with 12 core models (User, Farm, Crop, Diagnosis, Sensor, etc.)
- **Cache**: Redis for session management and temporary data
- **AI**: Disease diagnosis engine with image processing and ML models
- **API**: RESTful with standardized JSON responses

### Critical File Structure
```
backend/
├── src/
│   ├── main.py              # Main FastAPI app entry point
│   ├── core/
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Database connection
│   │   └── app_factory.py   # App factory pattern
│   ├── api/v1/              # API endpoints (15 files)
│   ├── models/              # SQLAlchemy models (12 models)
│   ├── modules/             # Business logic modules (36 modules)
│   └── utils/               # Utility functions
├── tests/                   # Test suite
└── requirements.txt         # Python dependencies

frontend/
├── src/
│   ├── pages/               # 20 page components
│   ├── components/          # Reusable UI components
│   ├── context/             # React contexts (Auth, Data)
│   └── utils/               # API client and helpers
├── App.jsx                  # Main app component
└── package.json             # Node.js dependencies
```

## Development Workflows

### Quick Start Commands
```bash
# Backend (Python 3.11 required)
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.src.main:app --reload

# Frontend
cd frontend && npm install && npm run dev

# Docker (Recommended)
docker compose up --build -d
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Code Patterns & Conventions

### Database Models
- **Location**: `backend/src/models/`
- **Base**: All models inherit from `Base` (SQLAlchemy declarative base)
- **Naming**: Singular names (User, Farm, Crop, not Users, Farms, Crops)
- **Timestamps**: All models include `created_at`, `updated_at`
- **Relationships**: Use `relationship()` for ORM relationships

### API Response Format
All endpoints return standardized JSON envelopes.

```json
// Success
{
  "success": true,
  "data": { ... },
  "message": "عملية ناجحة"
}

// Error
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
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 125,
    "pages": 7
  }
}
```

### Authentication System
- **JWT tokens**: Access token (15 minutes) + Refresh token (7 days)
- **Storage**: Tokens stored in httpOnly cookies
- **Rotation**: Automatic token rotation on refresh
- **MFA**: Optional multi-factor authentication support
- **Lockout**: Account lockout after 5 failed login attempts

### API Endpoints Structure
- **Location**: `backend/src/api/v1/`
- **Pattern**: One file per resource (e.g., `farms.py`, `crops.py`)
- **Router**: Each file exports a `router` using `APIRouter()`
- **Authentication**: Use `@jwt_required()` decorator for protected routes
- **Validation**: Use Pydantic models for request/response validation

### Frontend Components
- **Pages**: Located in `frontend/pages/`, one file per route
- **Context**: Use `AuthContext` for authentication, `DataContext` for global state
- **API Calls**: Use `ApiService` from `utils/api.js`
- **Styling**: Tailwind CSS utility classes
- **UI Components**: Radix UI for accessible components

### Security Best Practices
1. **Never** store secrets in code - use environment variables
2. **Always** validate and sanitize user inputs
3. **Use** parameterized queries (SQLAlchemy ORM handles this)
4. **Implement** CSRF protection for state-changing operations
5. **Add** security headers (CSP, HSTS, X-Frame-Options)
6. **Hash** passwords with bcrypt (via `passlib`)
7. **Rate limit** authentication endpoints

### Performance Optimization
1. **Use** `joinedload()` or `selectinload()` to avoid N+1 queries
2. **Add** database indexes on frequently queried columns
3. **Implement** Redis caching for expensive operations
4. **Paginate** large result sets
5. **Use** async operations where appropriate

### Testing
- **Backend**: pytest with fixtures in `backend/tests/`
- **Frontend**: Vitest with React Testing Library in `frontend/src/test/`
- **Coverage**: Aim for >80% backend, >50% frontend
- **E2E**: Playwright tests in `backend/tests/e2e/`

### Modules (Business Logic)
- **Location**: `backend/src/modules/`
- **Structure**: Each module has its own directory with:
  - `__init__.py`: Module exports
  - `api.py`: API routes
  - `service.py`: Business logic
  - `schemas.py`: Pydantic schemas
  - `db_models.py`: Database models (if module-specific)

### Key Modules
1. **disease_diagnosis**: AI-powered plant disease detection
2. **user_management**: User CRUD and permissions
3. **authentication**: Login, logout, token management
4. **image_processing**: Image upload and processing
5. **ai_management**: AI model management and inference
6. **backup_restore**: Database backup and restore
7. **data_validation**: Input validation and sanitization

### Environment Variables
Required variables in `.env`:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/gaara_scan_ai
POSTGRES_DB=gaara_scan_ai
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=gaara_secure_2024

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# App
DEBUG=False
APP_PORT=1005
FRONTEND_URL=http://localhost:1505
```

### Docker Services
- **database**: PostgreSQL 15
- **redis**: Redis 7
- **backend**: FastAPI app (port 1005)
- **frontend**: React app (port 1505)

### Common Tasks

#### Adding a New API Endpoint
1. Create route in `backend/src/api/v1/resource.py`
2. Define Pydantic schemas for request/response
3. Implement business logic in service layer
4. Add tests in `backend/tests/`
5. Update API documentation

#### Adding a New Page
1. Create component in `frontend/pages/NewPage.jsx`
2. Add route in `frontend/App.jsx`
3. Create API service methods if needed
4. Add navigation link in sidebar/menu
5. Write tests in `frontend/src/test/`

#### Database Schema Changes
1. Modify model in `backend/src/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review migration file in `backend/alembic/versions/`
4. Apply migration: `alembic upgrade head`
5. Update tests and fixtures

### Troubleshooting

#### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check for port conflicts (1005)
- Review logs for errors

#### Frontend won't build
- Run `npm install` to update dependencies
- Check for syntax errors in JSX files
- Verify API_URL is correct
- Clear node_modules and reinstall

#### Database connection issues
- Verify PostgreSQL is running: `docker compose ps`
- Check credentials in .env
- Ensure database exists: `docker compose exec database psql -U gaara_user -d gaara_scan_ai`

### Code Quality Standards
- **Python**: Follow PEP 8, use Black formatter, max line length 120
- **JavaScript**: Use ESLint, Prettier, semicolons required
- **Commits**: Use Conventional Commits (feat:, fix:, docs:, etc.)
- **Documentation**: Add docstrings to all functions/classes
- **Types**: Use type hints in Python, PropTypes in React

### Priority Fixes (P0)
1. Complete CRUD logic in all API endpoints
2. Add comprehensive input validation
3. Implement proper error handling
4. Increase test coverage to >80%
5. Add security headers and CSRF protection
6. Optimize database queries (add indexes, fix N+1)
7. Extract reusable components in frontend
8. Add proper logging throughout the app

### Next Steps
1. Review `COMPREHENSIVE_TECHNICAL_AUDIT.md` for detailed analysis
2. Check `TODO_FIXME_REPORT.md` for pending tasks
3. Follow `DOCKER_GUIDE.md` for deployment
4. Read `ROUTES_AUDIT_REPORT.md` for frontend routing details
