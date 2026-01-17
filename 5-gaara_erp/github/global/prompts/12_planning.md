# PLANNING PROMPT

**FILE**: github/global/prompts/12_planning.md | **PURPOSE**: Create detailed execution plan | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 3: Planning

This prompt guides you through creating a comprehensive, actionable plan for the project.

## Pre-Execution Checklist

- [ ] Requirements documented (new projects) OR analysis completed (existing projects)
- [ ] Memory system is active
- [ ] Logging is configured
- [ ] `docs/Task_List.md` exists (may be initial version)

## Step 1: Review Input

### For New Projects
- Read `docs/REQUIREMENTS.md`
- Identify all must-have features
- Identify all non-functional requirements

### For Existing Projects
- Read `docs/PROJECT_MAPS.md`
- Identify all issues and recommendations
- Identify all missing features

## Step 2: Break Down Work

Decompose the work into the 7 phases:

### Phase 1: Setup & Infrastructure
- Project initialization
- Version control setup
- Development environment configuration
- CI/CD pipeline setup
- Docker/Kubernetes configuration

### Phase 2: Database Design
- Schema design
- Migration scripts
- Seed data
- Indexes and constraints

### Phase 3: Backend Development
- Models/Entities
- Services/Business logic
- API endpoints
- Authentication/Authorization
- Validation
- Error handling

### Phase 4: Frontend Development
- Component library setup
- Page layouts
- Forms and validation
- State management
- API integration
- Routing

### Phase 5: Testing
- Unit tests (backend)
- Unit tests (frontend)
- Integration tests
- E2E tests
- Performance tests
- Security tests

### Phase 6: Documentation
- API documentation
- User documentation
- Deployment guide
- Architecture documentation

### Phase 7: Deployment
- Production configuration
- Database migration
- Deployment scripts
- Monitoring setup
- Backup configuration

## Step 3: Create Detailed Task List

Update `docs/Task_List.md` with granular, actionable tasks:

### Template

```markdown
# Task List

**FILE**: docs/Task_List.md | **PURPOSE**: Master task list | **OWNER**: [Team] | **LAST-AUDITED**: [Date]

## Legend
- **Priority**: [P0] Critical, [P1] High, [P2] Medium, [P3] Low
- **Owner**: [Backend] [Frontend] [DevOps] [QA] [Docs]
- **Status**: [ ] Not Started, [/] In Progress, [x] Complete, [-] Cancelled

---

## Phase 1: Setup & Infrastructure

### 1.1 Project Initialization
- [ ] [P0][DevOps] Initialize Git repository
- [ ] [P0][DevOps] Create `.gitignore` file
- [ ] [P0][DevOps] Set up branch protection rules
- [ ] [P0][DevOps] Create `README.md`

### 1.2 Development Environment
- [ ] [P0][DevOps] Create `docker-compose.yml`
- [ ] [P0][DevOps] Create Dockerfile for backend
- [ ] [P0][DevOps] Create Dockerfile for frontend
- [ ] [P0][DevOps] Set up environment variables (`.env.example`)

### 1.3 CI/CD Pipeline
- [ ] [P0][DevOps] Create GitHub Actions workflow
- [ ] [P0][DevOps] Configure linting checks
- [ ] [P0][DevOps] Configure test execution
- [ ] [P0][DevOps] Configure security scanning
- [ ] [P0][DevOps] Configure deployment to staging

---

## Phase 2: Database Design

### 2.1 Schema Design
- [ ] [P0][Backend] Design `users` table
- [ ] [P0][Backend] Design `roles` table
- [ ] [P0][Backend] Design `sessions` table
- [ ] [P0][Backend] Design `activity_logs` table
- [ ] [P0][Backend] Create ER diagram

### 2.2 Migrations
- [ ] [P0][Backend] Create initial migration script
- [ ] [P0][Backend] Add indexes
- [ ] [P0][Backend] Add foreign key constraints
- [ ] [P0][Backend] Add check constraints

### 2.3 Seed Data
- [ ] [P0][Backend] Create seed script for roles
- [ ] [P0][Backend] Create seed script for admin user
- [ ] [P1][Backend] Create seed script for test data

---

## Phase 3: Backend Development

### 3.1 Models
- [ ] [P0][Backend] Create `User` model
- [ ] [P0][Backend] Create `Role` model
- [ ] [P0][Backend] Create `Session` model
- [ ] [P0][Backend] Create `ActivityLog` model

### 3.2 Services
- [ ] [P0][Backend] Create `AuthService` (login, logout, refresh)
- [ ] [P0][Backend] Create `UserService` (CRUD operations)
- [ ] [P0][Backend] Create `RoleService` (CRUD operations)
- [ ] [P0][Backend] Create `ActivityLogService` (logging)

### 3.3 API Endpoints
- [ ] [P0][Backend] `POST /api/auth/login`
- [ ] [P0][Backend] `POST /api/auth/logout`
- [ ] [P0][Backend] `POST /api/auth/refresh`
- [ ] [P0][Backend] `GET /api/users`
- [ ] [P0][Backend] `GET /api/users/:id`
- [ ] [P0][Backend] `POST /api/users`
- [ ] [P0][Backend] `PUT /api/users/:id`
- [ ] [P0][Backend] `DELETE /api/users/:id`

### 3.4 Middleware
- [ ] [P0][Backend] Authentication middleware
- [ ] [P0][Backend] Authorization middleware (RBAC)
- [ ] [P0][Backend] Request validation middleware
- [ ] [P0][Backend] Error handling middleware
- [ ] [P0][Backend] Logging middleware
- [ ] [P0][Backend] Rate limiting middleware

---

## Phase 4: Frontend Development

### 4.1 Setup
- [ ] [P0][Frontend] Initialize React/Vue/Angular project
- [ ] [P0][Frontend] Configure TypeScript
- [ ] [P0][Frontend] Set up routing
- [ ] [P0][Frontend] Set up state management
- [ ] [P0][Frontend] Configure API client (Axios/Fetch)

### 4.2 Component Library
- [ ] [P0][Frontend] Create Button component
- [ ] [P0][Frontend] Create Input component
- [ ] [P0][Frontend] Create Card component
- [ ] [P0][Frontend] Create Table component
- [ ] [P0][Frontend] Create Modal component
- [ ] [P0][Frontend] Create Toast/Alert component

### 4.3 Pages
- [ ] [P0][Frontend] Login page
- [ ] [P0][Frontend] Dashboard page
- [ ] [P0][Frontend] Users list page
- [ ] [P0][Frontend] User detail page
- [ ] [P0][Frontend] User create/edit page

### 4.4 State Management
- [ ] [P0][Frontend] Auth state (user, token, isAuthenticated)
- [ ] [P0][Frontend] UI state (theme, sidebar)
- [ ] [P0][Frontend] Data state (users, loading, error)

---

## Phase 5: Testing

### 5.1 Backend Unit Tests
- [ ] [P0][QA] Test `User` model
- [ ] [P0][QA] Test `AuthService`
- [ ] [P0][QA] Test `UserService`
- [ ] [P0][QA] Test authentication middleware
- [ ] [P0][QA] Test authorization middleware

### 5.2 Backend Integration Tests
- [ ] [P0][QA] Test `POST /api/auth/login`
- [ ] [P0][QA] Test `GET /api/users` (with auth)
- [ ] [P0][QA] Test `POST /api/users` (with validation)

### 5.3 Frontend Unit Tests
- [ ] [P0][QA] Test Button component
- [ ] [P0][QA] Test Input component
- [ ] [P0][QA] Test LoginForm component

### 5.4 E2E Tests
- [ ] [P0][QA] Test login flow
- [ ] [P0][QA] Test user creation flow
- [ ] [P0][QA] Test user update flow

### 5.5 Coverage
- [ ] [P0][QA] Achieve ≥80% backend coverage
- [ ] [P0][QA] Achieve ≥80% frontend coverage

---

## Phase 6: Documentation

- [ ] [P0][Docs] API documentation (OpenAPI/Swagger)
- [ ] [P0][Docs] Database schema documentation
- [ ] [P0][Docs] Deployment guide
- [ ] [P0][Docs] User guide
- [ ] [P0][Docs] Architecture documentation

---

## Phase 7: Deployment

- [ ] [P0][DevOps] Configure production environment
- [ ] [P0][DevOps] Set up database (production)
- [ ] [P0][DevOps] Run migrations (production)
- [ ] [P0][DevOps] Deploy backend
- [ ] [P0][DevOps] Deploy frontend
- [ ] [P0][DevOps] Configure monitoring
- [ ] [P0][DevOps] Configure backups

---

**Total Tasks**: [Count]
**Estimated Completion**: [Date]
```

## Step 4: Prioritize Tasks

Use the OSF Framework to prioritize:
1. Security-critical tasks first
2. Correctness-critical tasks second
3. All other tasks by dependency order

## Step 5: Log Actions

Log to `logs/info.log`

## Step 6: Save to Memory

Save to `.memory/checkpoints/checkpoint_phase_3_[date].md`

## Next Phase

Proceed to **Phase 4: Code Implementation** using `20_backend.md`, `21_frontend.md`, etc.

---

**Completion Criteria**:
- [ ] All tasks identified and documented
- [ ] Tasks prioritized by OSF
- [ ] Dependencies mapped
- [ ] Actions logged
- [ ] Checkpoint saved

