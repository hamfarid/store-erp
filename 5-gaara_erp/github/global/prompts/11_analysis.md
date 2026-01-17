# PROJECT ANALYSIS PROMPT

**FILE**: github/global/prompts/11_analysis.md | **PURPOSE**: Analyze existing codebase | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 1: Initialization & Analysis (Existing Projects)

This prompt guides you through analyzing an existing codebase and generating comprehensive project maps.

## Pre-Execution Checklist

- [ ] Memory system is active
- [ ] Logging is configured
- [ ] Project directory is accessible
- [ ] `docs/` folder exists

## Step 1: Initial Scan

Scan the project directory to identify:

1. **Project Type**: Web app, API, library, monorepo, etc.
2. **Tech Stack**: Languages, frameworks, libraries
3. **Structure**: Folder organization, architecture pattern
4. **Entry Points**: Main files, server files, index files
5. **Configuration**: Package files, config files, env files

### Commands to Run

```bash
# List all files
find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*"

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Find entry points
find . -name "main.*" -o -name "index.*" -o -name "app.*" -o -name "server.*"

# Find config files
find . -name "package.json" -o -name "requirements.txt" -o -name "Cargo.toml" -o -name "go.mod"
```

## Step 2: Deep Code Analysis

### Backend Analysis

For each backend file:

1. **Read the entire file** - No skipping
2. **Identify all classes and functions**
3. **Trace all imports and exports**
4. **Map all database models and relations**
5. **Document all API endpoints**

### Frontend Analysis

For each frontend file:

1. **Read the entire file** - No skipping
2. **Identify all components**
3. **Trace component hierarchy**
4. **Map state management**
5. **Document all API calls**

## Step 3: Generate Project Maps

Create `docs/PROJECT_MAPS.md` with the following sections:

### Template

```markdown
# Project Maps

**FILE**: docs/PROJECT_MAPS.md | **PURPOSE**: Comprehensive project maps | **OWNER**: System | **LAST-AUDITED**: [Date]

## 1. Technology Stack

### Frontend
- **Framework**: [React / Vue / Angular]
- **Version**: [X.X.X]
- **Language**: [TypeScript / JavaScript]
- **State Management**: [Redux / Zustand / Context]
- **Styling**: [Tailwind / MUI / CSS Modules]

### Backend
- **Framework**: [FastAPI / Django / Express]
- **Version**: [X.X.X]
- **Language**: [Python / Node.js / Go]
- **ORM**: [SQLAlchemy / Prisma / TypeORM]

### Database
- **Type**: [PostgreSQL / MySQL / MongoDB]
- **Version**: [X.X.X]

### Infrastructure
- **Containerization**: [Docker / None]
- **Orchestration**: [Kubernetes / None]
- **CI/CD**: [GitHub Actions / GitLab CI / None]

## 2. Backend Class Map

### Models

#### User
- **File**: `backend/models/user.py`
- **Purpose**: User authentication and profile
- **Fields**:
  - `id`: UUID (PK)
  - `email`: String (unique)
  - `password_hash`: String
  - `role`: Enum (admin, user)
  - `created_at`: DateTime
- **Relations**:
  - `has_many`: sessions, activity_logs
- **Methods**:
  - `verify_password(password: str) -> bool`
  - `generate_token() -> str`

[Repeat for all models]

### Services

#### AuthService
- **File**: `backend/services/auth.py`
- **Purpose**: Authentication logic
- **Methods**:
  - `login(email: str, password: str) -> Token`
  - `logout(token: str) -> bool`
  - `verify_token(token: str) -> User`
- **Dependencies**: UserModel, TokenService

[Repeat for all services]

## 3. Backend Import/Export Map

```
backend/
├── models/
│   ├── user.py
│   │   └── exports: User, UserRole
│   └── session.py
│       └── exports: Session
│       └── imports: User from models/user.py
├── services/
│   ├── auth.py
│   │   └── exports: AuthService
│   │   └── imports: User from models/user.py
│   └── user.py
│       └── exports: UserService
│       └── imports: User from models/user.py
└── routes/
    └── auth.py
        └── imports: AuthService from services/auth.py
```

## 4. Database Relation Map

```
users (1) ──< (N) sessions
users (1) ──< (N) activity_logs
users (N) ──> (1) roles
```

### Tables

#### users
- `id` (PK)
- `email` (UNIQUE)
- `password_hash`
- `role_id` (FK → roles.id)
- `created_at`
- `updated_at`

#### sessions
- `id` (PK)
- `user_id` (FK → users.id)
- `token`
- `expires_at`
- `created_at`

[Repeat for all tables]

## 5. Frontend Component Hierarchy

```
App
├── AuthProvider
│   ├── LoginPage
│   │   ├── LoginForm
│   │   └── ForgotPasswordLink
│   └── DashboardPage
│       ├── Header
│       ├── Sidebar
│       └── MainContent
│           ├── StatsCard
│           └── RecentActivity
└── ThemeProvider
```

## 6. Frontend State Flow

### Global State (Redux/Zustand)

```
store/
├── auth/
│   ├── state: { user, token, isAuthenticated }
│   └── actions: login, logout, refreshToken
├── ui/
│   ├── state: { theme, sidebarOpen }
│   └── actions: toggleTheme, toggleSidebar
└── data/
    ├── state: { items, loading, error }
    └── actions: fetchItems, createItem, updateItem, deleteItem
```

## 7. Frontend API Call Map

### Components → API Endpoints

- **LoginForm** → `POST /api/auth/login`
- **DashboardPage** → `GET /api/stats`
- **ItemsList** → `GET /api/items`
- **ItemForm** → `POST /api/items`, `PUT /api/items/:id`

## 8. API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/forgot-password` - Request password reset

### Users
- `GET /api/users` - List users (admin only)
- `GET /api/users/:id` - Get user details
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user (admin only)

[Repeat for all endpoints]

## 9. File Structure

```
project/
├── backend/
│   ├── models/
│   ├── services/
│   ├── routes/
│   ├── utils/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── hooks/
│   │   └── utils/
│   └── tests/
├── docs/
└── docker/
```

## 10. Issues & Recommendations

### Critical Issues (P0)
1. [Issue 1]
   - **Impact**: [Description]
   - **Recommendation**: [Solution]

### High Priority Issues (P1)
1. [Issue 1]
   - **Impact**: [Description]
   - **Recommendation**: [Solution]

### Medium Priority Issues (P2)
1. [Issue 1]
   - **Impact**: [Description]
   - **Recommendation**: [Solution]

---

**Analysis Completed**: [Date]
**Next Steps**: Review recommendations and create action plan
```

## Step 4: Log Actions

Log to `logs/info.log`

## Step 5: Save to Memory

Save to `.memory/checkpoints/checkpoint_phase_1_[date].md`

## Next Phase

Proceed to **Phase 3: Planning** using `12_planning.md`

---

**Completion Criteria**:
- [ ] All code files analyzed
- [ ] PROJECT_MAPS.md created
- [ ] All maps complete and accurate
- [ ] Actions logged
- [ ] Checkpoint saved

