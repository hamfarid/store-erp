# Folder Maps - Project Structure

> **Purpose:** Complete map of project structure with purpose of each folder and file.

**Last Updated:** [DATE]  
**Project:** {{PROJECT_NAME}}

---

## Project Root Structure

```
{{PROJECT_NAME}}/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── migrations/             # Database migrations
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
├── README.md               # Project overview
├── CHANGELOG.md            # Version history
├── LICENSE                 # License file
└── docker-compose.yml      # Docker configuration
```

---

## /src - Source Code

**Purpose:** All application source code

```
src/
├── __init__.py             # Package initialization
├── app.py                  # Application entry point
├── config.py               # Configuration classes
├── database.py             # Database connection
├── api/                    # API endpoints
│   ├── __init__.py
│   ├── users.py            # User endpoints
│   ├── products.py         # Product endpoints
│   └── orders.py           # Order endpoints
├── models/                 # Database models
│   ├── __init__.py
│   ├── user.py             # User model
│   ├── product.py          # Product model
│   └── order.py            # Order model
├── services/               # Business logic
│   ├── __init__.py
│   ├── auth_service.py     # Authentication logic
│   ├── user_service.py     # User operations
│   └── order_service.py    # Order operations
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── validators.py       # Input validation
│   ├── helpers.py          # Helper functions
│   └── decorators.py       # Custom decorators
└── middleware/             # Custom middleware
    ├── __init__.py
    ├── auth.py             # Auth middleware
    └── logging.py          # Logging middleware
```

### /src/api - API Endpoints

**Purpose:** REST API endpoints organized by resource

**Naming Convention:** `{resource}s.py` (plural)

**Structure:**
- Each file is a Flask Blueprint
- Handles HTTP requests/responses
- Calls services for business logic
- Returns JSON responses

**Files:**
- `users.py` - User management endpoints
- `products.py` - Product management endpoints
- `orders.py` - Order management endpoints

### /src/models - Database Models

**Purpose:** SQLAlchemy ORM models

**Naming Convention:** `{model}.py` (singular)

**Structure:**
- Each file defines one or more related models
- Inherits from `db.Model`
- Defines table schema
- Defines relationships
- Includes basic methods (to_dict, from_dict)

**Files:**
- `user.py` - User model
- `product.py` - Product model
- `order.py` - Order and OrderItem models

### /src/services - Business Logic

**Purpose:** Business logic and operations

**Naming Convention:** `{resource}_service.py`

**Structure:**
- Each file is a service class
- Contains business logic
- Interacts with models
- Handles transactions
- No HTTP concerns

**Files:**
- `auth_service.py` - Authentication (register, login, tokens)
- `user_service.py` - User operations (CRUD, search)
- `order_service.py` - Order operations (create, update, cancel)

### /src/utils - Utilities

**Purpose:** Reusable utility functions

**Naming Convention:** `{category}.py`

**Structure:**
- Pure functions when possible
- No side effects
- Well-tested
- Documented

**Files:**
- `validators.py` - Input validation functions
- `helpers.py` - General helper functions
- `decorators.py` - Custom decorators (auth, rate limiting)

### /src/middleware - Middleware

**Purpose:** Custom Flask middleware

**Naming Convention:** `{purpose}.py`

**Structure:**
- Request/response processing
- Cross-cutting concerns
- Registered in app.py

**Files:**
- `auth.py` - Authentication middleware
- `logging.py` - Request/response logging
- `cors.py` - CORS handling

---

## /tests - Test Files

**Purpose:** All test files

```
tests/
├── __init__.py
├── conftest.py             # Pytest configuration
├── test_api/               # API tests
│   ├── __init__.py
│   ├── test_users.py       # User API tests
│   ├── test_products.py    # Product API tests
│   └── test_orders.py      # Order API tests
├── test_models/            # Model tests
│   ├── __init__.py
│   ├── test_user.py        # User model tests
│   ├── test_product.py     # Product model tests
│   └── test_order.py       # Order model tests
├── test_services/          # Service tests
│   ├── __init__.py
│   ├── test_auth_service.py
│   ├── test_user_service.py
│   └── test_order_service.py
├── test_utils/             # Utility tests
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_helpers.py
└── e2e/                    # End-to-end tests
    ├── __init__.py
    ├── test_auth_flow.py   # Authentication flow
    ├── test_order_flow.py  # Order creation flow
    └── test_admin_flow.py  # Admin operations
```

### Test Organization

**Unit Tests:**
- `test_models/` - Model tests
- `test_services/` - Service tests
- `test_utils/` - Utility tests

**Integration Tests:**
- `test_api/` - API endpoint tests

**E2E Tests:**
- `e2e/` - Full user flow tests

**Naming Convention:**
- Test files: `test_{module}.py`
- Test classes: `Test{ClassName}`
- Test functions: `test_{function_name}_{scenario}`

---

## /docs - Documentation

**Purpose:** Project documentation

```
docs/
├── DB_Schema.md                    # Database schema
├── API_Endpoints.md                # API documentation
├── Architecture.md                 # System architecture
├── Data_Flow.md                    # Data flow diagrams
├── Security_Model.md               # Security implementation
├── Permissions_Model.md            # RBAC details
├── Routes_FE.md                    # Frontend routes
├── Routes_BE.md                    # Backend routes
├── Solution_Tradeoff_Log.md        # Decision log
├── fix_this_error.md               # Known issues
├── To_ReActivated_again.md         # Disabled features
├── Class_Registry.md               # Class reference
├── Import_Export_Map.md            # Dependencies
├── Folder_Maps.md                  # This file
├── Errors_Log.md                   # Error history
├── Task_List.md                    # Task tracking
├── Resilience.md                   # Error handling
├── Status_Report.md                # Project status
├── Testing_Strategy.md             # Testing approach
└── Deployment_Guide.md             # Deployment steps
```

### Documentation Types

**Architecture:**
- `Architecture.md` - Overall system design
- `Data_Flow.md` - How data moves through system
- `Folder_Maps.md` - Project structure

**API:**
- `API_Endpoints.md` - All API endpoints
- `Routes_BE.md` - Backend routes
- `Routes_FE.md` - Frontend routes

**Database:**
- `DB_Schema.md` - Complete schema
- `Class_Registry.md` - Model reference

**Security:**
- `Security_Model.md` - Security implementation
- `Permissions_Model.md` - RBAC system

**Development:**
- `Solution_Tradeoff_Log.md` - Decisions made
- `fix_this_error.md` - Known issues
- `To_ReActivated_again.md` - Disabled features
- `Errors_Log.md` - Error history
- `Task_List.md` - Task tracking

**Operations:**
- `Resilience.md` - Error handling
- `Status_Report.md` - Current status
- `Deployment_Guide.md` - How to deploy

---

## /migrations - Database Migrations

**Purpose:** Database schema migrations

```
migrations/
├── versions/
│   ├── 001_initial_schema.py
│   ├── 002_add_orders.py
│   ├── 003_add_products.py
│   └── ...
├── alembic.ini             # Alembic configuration
└── env.py                  # Migration environment
```

**Naming Convention:** `{version}_{description}.py`

**Structure:**
- Sequential version numbers
- Descriptive names
- Reversible (up/down)
- Tested before production

---

## /static - Static Files

**Purpose:** Frontend static assets

```
static/
├── css/
│   ├── main.css            # Main stylesheet
│   ├── components/         # Component styles
│   │   ├── buttons.css
│   │   ├── forms.css
│   │   └── cards.css
│   └── vendor/             # Third-party CSS
│       └── bootstrap.min.css
├── js/
│   ├── main.js             # Main JavaScript
│   ├── components/         # Component scripts
│   │   ├── auth.js
│   │   ├── products.js
│   │   └── orders.js
│   └── vendor/             # Third-party JS
│       ├── jquery.min.js
│       └── bootstrap.min.js
├── images/
│   ├── logo.png
│   ├── favicon.ico
│   └── icons/              # Icon files
│       ├── user.svg
│       ├── product.svg
│       └── order.svg
└── fonts/
    └── custom-font.woff2
```

### Static File Organization

**CSS:**
- `css/main.css` - Main styles
- `css/components/` - Component-specific styles
- `css/vendor/` - Third-party libraries

**JavaScript:**
- `js/main.js` - Main scripts
- `js/components/` - Component-specific scripts
- `js/vendor/` - Third-party libraries

**Images:**
- `images/` - General images
- `images/icons/` - Icon files (SVG preferred)

**Fonts:**
- `fonts/` - Custom fonts

---

## /templates - HTML Templates

**Purpose:** Jinja2 HTML templates

```
templates/
├── base.html               # Base template
├── layout/
│   ├── header.html         # Header component
│   ├── footer.html         # Footer component
│   └── sidebar.html        # Sidebar component
├── auth/
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── forgot_password.html
├── users/
│   ├── list.html           # User list
│   ├── detail.html         # User detail
│   └── edit.html           # User edit
├── products/
│   ├── list.html
│   ├── detail.html
│   └── edit.html
└── orders/
    ├── list.html
    ├── detail.html
    └── create.html
```

### Template Organization

**Base:**
- `base.html` - Main layout template

**Layout Components:**
- `layout/header.html` - Header
- `layout/footer.html` - Footer
- `layout/sidebar.html` - Sidebar

**Feature Templates:**
- `auth/` - Authentication pages
- `users/` - User management pages
- `products/` - Product management pages
- `orders/` - Order management pages

---

## /config - Configuration Files

**Purpose:** Configuration files

```
config/
├── development.py          # Development config
├── production.py           # Production config
├── testing.py              # Testing config
├── nginx.conf              # Nginx configuration
└── gunicorn.conf.py        # Gunicorn configuration
```

---

## /scripts - Utility Scripts

**Purpose:** Helper scripts

```
scripts/
├── init_db.py              # Initialize database
├── seed_data.py            # Seed test data
├── backup_db.sh            # Backup database
├── deploy.sh               # Deployment script
└── run_tests.sh            # Run test suite
```

---

## Root Files

### Configuration Files

**`.env.example`**
- Template for environment variables
- Never commit actual `.env` file
- Document all required variables

**`.gitignore`**
- Files to ignore in Git
- Include: `.env`, `__pycache__`, `*.pyc`, etc.

**`requirements.txt`**
- Python dependencies
- Pin versions for reproducibility
- Update regularly

**`docker-compose.yml`**
- Docker services configuration
- Database, Redis, application
- Development and production profiles

### Documentation Files

**`README.md`**
- Project overview
- Setup instructions
- Quick start guide
- Links to detailed docs

**`CHANGELOG.md`**
- Version history
- Changes in each version
- Breaking changes highlighted

**`LICENSE`**
- License information
- Copyright notice

**`CONTRIBUTING.md`**
- Contribution guidelines
- Code style
- Pull request process

---

## Folder Naming Conventions

**General Rules:**
- Use lowercase
- Use underscores for spaces (`user_service.py`)
- Be descriptive but concise
- Plural for collections (`users.py`, `products/`)
- Singular for single items (`user.py`, `config/`)

**Python Packages:**
- Must have `__init__.py`
- Package name = folder name
- Use relative imports within package

**Test Files:**
- Prefix with `test_`
- Mirror source structure
- Same name as module being tested

---

## File Naming Conventions

**Python Files:**
- `snake_case.py`
- Descriptive names
- One module per file (usually)

**Test Files:**
- `test_{module}.py`
- `test_{feature}_flow.py` for E2E

**Documentation:**
- `PascalCase.md` or `Snake_Case.md`
- Descriptive names
- Consistent across project

**Configuration:**
- `{environment}.py` for Python config
- `{service}.conf` for service config
- `.{service}rc` for RC files

---

## Adding New Folders/Files

**Checklist:**
1. [ ] Choose appropriate location
2. [ ] Follow naming conventions
3. [ ] Add to this map
4. [ ] Update Import_Export_Map.md (if code file)
5. [ ] Update Class_Registry.md (if contains classes)
6. [ ] Add tests (if code file)
7. [ ] Document purpose and usage
8. [ ] Update README if significant

---

## Notes

- Keep this map updated when structure changes
- Use this map to onboard new developers
- Review structure regularly for improvements
- Maintain consistency across project
- Document any deviations from conventions

