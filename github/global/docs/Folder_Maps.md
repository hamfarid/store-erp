# Folder Maps - Project Structure

> **Purpose:** Complete map of project structure with purpose of each folder and file.

**Last Updated:** 2025-01-16
**Project:** Store Management System

---

## Project Root Structure

```
store/
├── .memory/                    # AI memory and context system
├── backend/                    # Flask backend application
├── frontend/                   # React frontend application
├── docs/                       # Project documentation
├── global/                     # Global development framework
├── helpers/                    # Helper templates
├── config/                     # Configuration files
├── database/                   # Database initialization
├── deployment/                 # Deployment configurations
├── nginx/                      # Nginx configurations
├── docker-compose.yml          # Docker services
├── Dockerfile                  # Main Dockerfile
├── .cursorrules                # Cursor IDE rules
└── README.md                   # Project overview
```

---

## /backend - Flask Backend

**Purpose:** All backend server code

```
backend/
├── src/
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py         # Models package init
│   │   ├── user.py             # User model
│   │   ├── product.py          # Product models
│   │   ├── batch.py            # Batch/Lot models
│   │   ├── invoice.py          # Invoice models
│   │   ├── sale.py             # Sale models
│   │   └── role.py             # Role & Permission models
│   ├── routes/                 # API endpoints (Blueprints)
│   │   ├── __init__.py         # Routes registration
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── users.py            # User management
│   │   ├── products.py         # Product CRUD
│   │   ├── batches.py          # Batch/Lot management
│   │   ├── invoices.py         # Invoice operations
│   │   ├── reports.py          # Reports generation
│   │   └── dashboard.py        # Dashboard data
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── user_service.py     # User operations
│   │   └── report_service.py   # Report generation
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py       # Input validation
│   │   ├── helpers.py          # Helper functions
│   │   └── file_scanner.py     # File upload scanning
│   ├── decorators/             # Custom decorators
│   │   ├── __init__.py
│   │   └── permissions.py      # Permission decorators
│   └── middleware/             # Custom middleware
│       └── security.py         # Security middleware
├── migrations/                 # Alembic migrations
│   └── versions/               # Migration files
├── tests/                      # Backend tests
│   ├── conftest.py             # Pytest configuration
│   ├── test_auth.py            # Auth tests
│   ├── test_products.py        # Product tests
│   └── test_security.py        # Security tests
├── instance/                   # Instance-specific files
│   └── store.db                # SQLite database
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Backend Dockerfile
└── pytest.ini                  # Pytest configuration
```

### Key Files:
- `app.py` - Flask application factory and configuration
- `src/models/__init__.py` - Database models and SQLAlchemy instance
- `src/routes/__init__.py` - Blueprint registration

---

## /frontend - React Frontend

**Purpose:** React single-page application

```
frontend/
├── src/
│   ├── pages/                  # Page components
│   │   ├── Dashboard.jsx       # Main dashboard
│   │   ├── Products.jsx        # Products management
│   │   ├── Batches.jsx         # Lots/Batches
│   │   ├── Invoices.jsx        # Invoices
│   │   ├── Reports.jsx         # Reports
│   │   ├── Settings.jsx        # User settings
│   │   ├── Login.jsx           # Login page
│   │   └── errors/             # Error pages
│   │       ├── NotFound.jsx    # 404 page
│   │       └── ServerError.jsx # 500 page
│   ├── components/             # Reusable components
│   │   ├── ui/                 # UI primitives (shadcn/ui)
│   │   │   ├── button.jsx
│   │   │   ├── card.jsx
│   │   │   ├── input.jsx
│   │   │   └── ...
│   │   ├── layout/             # Layout components
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Footer.jsx
│   │   ├── DataTable.jsx       # Data table component
│   │   ├── CommandPalette.jsx  # Command palette (Ctrl+K)
│   │   └── ThemeToggle.jsx     # Theme switcher
│   ├── services/               # API services
│   │   ├── api.js              # Axios configuration
│   │   └── auth.js             # Auth API methods
│   ├── contexts/               # React contexts
│   │   ├── AuthContext.jsx     # Authentication state
│   │   ├── ThemeContext.jsx    # Theme state
│   │   └── AppContext.jsx      # App-wide state
│   ├── hooks/                  # Custom hooks
│   │   ├── useAuth.js          # Auth hook
│   │   └── useApi.js           # API hook
│   ├── config/                 # Configuration
│   │   └── constants.js        # API URLs, etc.
│   ├── lib/                    # Utilities
│   │   └── utils.js            # cn() and helpers
│   ├── App.jsx                 # Application root
│   ├── AppRouter.jsx           # Route definitions
│   ├── main.jsx                # Entry point
│   └── App.css                 # Global styles
├── public/                     # Static assets
│   ├── favicon.svg
│   └── manifest.json
├── dist/                       # Build output
├── package.json                # NPM dependencies
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
└── Dockerfile                  # Frontend Dockerfile
```

### Key Files:
- `main.jsx` - React entry point
- `App.jsx` - Root component with providers
- `AppRouter.jsx` - Route definitions
- `components/ui/` - shadcn/ui components

---

## /docs - Documentation

**Purpose:** All project documentation

```
docs/
├── README.md                   # Docs overview
├── ARCHITECTURE.md             # System architecture
├── API_DOCUMENTATION.md        # API reference
├── DATABASE_SCHEMA.md          # Database schema
├── SECURITY_GUIDELINES.md      # Security practices
├── TODO.md                     # Task tracking (NEVER DELETE)
├── COMPLETE_TASKS.md           # Completed tasks
├── INCOMPLETE_TASKS.md         # Remaining tasks
├── Errors_Log.md               # Error tracking
├── Import_Export_Map.md        # Dependencies
├── Folder_Maps.md              # This file
├── Class_Registry.md           # Class reference
├── DEDUPLICATION_LOG.md        # Duplicate tracking
├── CONSTITUTION.md             # Project principles
├── PROJECT_PLAN.md             # Execution plan
└── DEPLOYMENT_GUIDE.md         # Deployment steps
```

---

## /.memory - AI Memory System

**Purpose:** Context retention for AI agent

```
.memory/
├── README.md                   # Memory system docs
├── file_registry.json          # File tracking (Librarian)
├── context/
│   ├── current_task.md         # Current work context
│   └── README.md
├── checkpoints/
│   ├── index.json              # Checkpoint index
│   └── *.md                    # Phase checkpoints
├── decisions/
│   └── ui-ux/                  # UI/UX decisions
├── conversations/
│   └── daily/                  # Daily logs
└── knowledge/
    ├── patterns/
    ├── solutions/
    └── antipatterns/
```

---

## /global - Development Framework

**Purpose:** Global tools and rules from Professional Core Prompt

```
global/
├── README.md                   # Framework overview
├── tools/
│   ├── lifecycle.py            # Project lifecycle
│   ├── librarian.py            # File registry
│   ├── speckit_bridge.py       # Spec management
│   └── README.md
└── rules/
    ├── 99_context_first.md     # Context-first rule
    ├── 100_evolution_engine.md # Self-improvement
    └── README.md
```

---

## /config - Configuration

**Purpose:** Project configuration files

```
config/
└── ports.json                  # Port configuration
```

**Port Configuration:**
| Service | Port |
|---------|------|
| Backend | 6001 |
| Frontend | 6501 |
| ML | 6101 |
| AI | 6601 |

---

## /helpers - Templates

**Purpose:** Document templates

```
helpers/
├── Task_List_Template.md
├── Errors_Log_Template.md
├── Folder_Maps_Template.md
├── Class_Registry_Template.md
├── Import_Export_Map_Template.md
├── TODO_Template.md
├── COMPLETE_TASKS_Template.md
├── INCOMPLETE_TASKS_Template.md
└── RORLOC_Test_Plan_Template.md
```

---

## File Naming Conventions

**Python Files:**
- `snake_case.py`
- Models: `user.py`, `product.py`
- Routes: `auth.py`, `users.py`
- Services: `auth_service.py`

**JavaScript/JSX Files:**
- Components: `PascalCase.jsx` (`Dashboard.jsx`)
- Utilities: `camelCase.js` (`utils.js`)
- Hooks: `useCamelCase.js` (`useAuth.js`)

**Documentation:**
- `UPPER_SNAKE_CASE.md` or `Title_Case.md`

---

## Notes

- Keep this map updated when structure changes
- Use for onboarding new developers
- Review structure regularly for improvements

