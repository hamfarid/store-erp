# DOCUMENTATION GENERATION PROMPT

**FILE**: github/global/prompts/70_documentation.md | **PURPOSE**: Generate all project documentation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 7: Finalization & Documentation

This prompt guides you through creating all required documentation files.

## Required Documentation Files (21+)

1. README.md
2. docs/ARCHITECTURE.md
3. docs/API_DOCUMENTATION.md
4. docs/DATABASE_SCHEMA.md
5. docs/DEPLOYMENT_GUIDE.md
6. docs/TESTING_STRATEGY.md
7. docs/SECURITY_GUIDELINES.md
8. CHANGELOG.md
9. CONTRIBUTING.md
10. LICENSE
11. docs/Permissions_Model.md
12. docs/Routes_FE.md
13. docs/Routes_BE.md
14. docs/Solution_Tradeoff_Log.md
15. docs/fix_this_error.md
16. docs/To_ReActivated_again.md
17. docs/Class_Registry.md
18. docs/Resilience.md
19. docs/Status_Report.md
20. docs/Task_List.md
21. docs/PROJECT_MAPS.md

## 1. README.md

```markdown
# {{PROJECT_NAME}}

**Version**: 1.0.0
**Status**: Production Ready

## Overview

[Brief description of the project]

## Features

- ✅ Feature 1
- ✅ Feature 2
- ✅ Feature 3

## Tech Stack

### Frontend
- React 18 + TypeScript
- Zustand (State Management)
- Tailwind CSS

### Backend
- FastAPI (Python 3.10+)
- PostgreSQL 14
- Redis (Caching)

### Infrastructure
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- AWS (Production)

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/{{PROJECT_SLUG}}.git
cd {{PROJECT_SLUG}}
```

2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your values
```

3. Start with Docker Compose
```bash
docker-compose up -d
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/docs

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Testing Strategy](docs/TESTING_STRATEGY.md)
- [Security Guidelines](docs/SECURITY_GUIDELINES.md)

## Testing

```bash
# Backend tests
cd backend
pytest --cov=backend --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

See [LICENSE](LICENSE)

## Support

For issues and questions, please open an issue on GitHub.

---

**Maintained by**: [Your Team]
**Last Updated**: [Date]
```

## 2. docs/ARCHITECTURE.md

```markdown
# Architecture Documentation

**FILE**: docs/ARCHITECTURE.md | **PURPOSE**: System architecture | **OWNER**: Architecture | **LAST-AUDITED**: [Date]

## System Overview

[High-level description]

## Architecture Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Frontend   │ (React + TypeScript)
│  (Port 3000)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │ (FastAPI + Python)
│  (Port 5000)│
└──────┬──────┘
       │
       ├──────────┐
       ▼          ▼
┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Redis   │
│(Port 5432│  │(Port 6379│
└──────────┘  └──────────┘
```

## Frontend Architecture

### Component Structure

```
src/
├── components/     # Reusable UI components
├── pages/          # Page-level components
├── hooks/          # Custom React hooks
├── store/          # State management (Zustand)
├── services/       # API services
├── utils/          # Utility functions
└── types/          # TypeScript types
```

### State Management

- **Global State**: Zustand stores
- **Server State**: React Query (if used)
- **Local State**: React useState/useReducer

### Routing

- React Router v6
- Protected routes with authentication guards
- Lazy loading for code splitting

## Backend Architecture

### Layered Architecture

```
Routes (API Endpoints)
    ↓
Services (Business Logic)
    ↓
Models (Data Access)
    ↓
Database
```

### Project Structure

```
backend/
├── models/         # Database models (SQLAlchemy)
├── services/       # Business logic
├── routes/         # API endpoints (FastAPI)
├── middleware/     # Request/response middleware
├── utils/          # Helper functions
└── config/         # Configuration
```

### API Design

- RESTful conventions
- JWT authentication
- RBAC authorization
- Request validation (Pydantic)
- Error handling middleware

## Database Architecture

### Schema Design

- Normalized to 3NF
- Foreign key constraints
- Indexes on frequently queried columns
- Soft deletes (deleted_at)
- Audit columns (created_at, updated_at)

### Migrations

- Alembic for schema migrations
- Version controlled
- Reversible (up/down)

## Security Architecture

### Authentication

- JWT tokens (access + refresh)
- Access token: 15 minutes TTL
- Refresh token: 7 days TTL
- Secure HTTP-only cookies (optional)

### Authorization

- Role-Based Access Control (RBAC)
- Roles: ADMIN, MANAGER, USER, GUEST
- Permission checks at route and service level

### Data Protection

- Passwords hashed with bcrypt
- Secrets in environment variables
- HTTPS enforced
- CORS configured
- Security headers (CSP, HSTS, etc.)

## Infrastructure

### Development

- Docker Compose for local development
- Hot reload for frontend and backend
- Separate containers for each service

### Production

- Kubernetes for orchestration
- Horizontal Pod Autoscaler (HPA)
- Load balancer
- Multi-region deployment
- Automated backups

## Monitoring & Logging

### Logging

- Structured JSON logs
- Log levels: DEBUG, INFO, WARN, ERROR, FATAL
- Centralized logging (ELK stack)

### Monitoring

- Prometheus for metrics
- Grafana for dashboards
- Alerts via Slack/PagerDuty

### Tracing

- OpenTelemetry for distributed tracing
- Correlation IDs in all requests

## Performance

### Frontend

- Code splitting
- Lazy loading
- Image optimization
- CDN for static assets

### Backend

- Database connection pooling
- Redis caching
- Query optimization
- Rate limiting

## Scalability

### Horizontal Scaling

- Stateless backend services
- Session storage in Redis
- Database read replicas

### Vertical Scaling

- Resource limits in Kubernetes
- Auto-scaling based on CPU/memory

---

**Next Review**: [Date]
```

## 3. docs/API_DOCUMENTATION.md

Generate using OpenAPI/Swagger:

```python
# In FastAPI, this is automatic
# Access at http://localhost:5000/docs

# To export to file:
import json
from main import app

with open("docs/API_DOCUMENTATION.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)
```

## 4. docs/DATABASE_SCHEMA.md

```markdown
# Database Schema

**FILE**: docs/DATABASE_SCHEMA.md | **PURPOSE**: Database schema documentation | **OWNER**: Backend | **LAST-AUDITED**: [Date]

## ER Diagram

```
users (1) ──< (N) sessions
users (1) ──< (N) activity_logs
users (N) ──> (1) roles
```

## Tables

### users

**Purpose**: Store user accounts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique user ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| role | ENUM | NOT NULL | User role (admin, manager, user, guest) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account status |
| deleted_at | TIMESTAMP | NULL | Soft delete timestamp |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (email)
- INDEX (role)
- INDEX (is_active)

### sessions

**Purpose**: Store user sessions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique session ID |
| user_id | UUID | FK → users.id, NOT NULL | User reference |
| refresh_token | VARCHAR(500) | NOT NULL | JWT refresh token |
| expires_at | TIMESTAMP | NOT NULL | Expiration time |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
- INDEX (user_id)
- INDEX (expires_at)

[Repeat for all tables]

## Migrations

### Migration History

| Version | Date | Description |
|---------|------|-------------|
| 001 | 2025-11-18 | Initial schema |
| 002 | 2025-11-19 | Add activity_logs table |

---

**Last Updated**: [Date]
```

## Auto-Generation Tools

### API Documentation

```bash
# FastAPI (automatic)
# Access at /docs or /redoc

# Export to file
python -c "from main import app; import json; print(json.dumps(app.openapi(), indent=2))" > docs/API_DOCUMENTATION.json
```

### Database Schema

```bash
# Generate ER diagram
pip install eralchemy
eralchemy -i postgresql://user:pass@localhost/db -o docs/schema.png
```

## Log Actions

Log all documentation generation to `logs/info.log`

---

**Completion Criteria**:
- [ ] All 21+ documentation files created
- [ ] All files follow templates
- [ ] All files have proper headers
- [ ] API documentation auto-generated
- [ ] Database schema documented
- [ ] Actions logged

