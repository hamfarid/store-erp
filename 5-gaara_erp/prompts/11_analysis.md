=================================================================================
PROJECT ANALYSIS - Existing Project Analysis
=================================================================================

Version: Latest
Type: Core - Analysis

This prompt guides analysis of existing projects.
Based on Section 65 and project_analyzer.py tool.

=================================================================================
OVERVIEW
=================================================================================

When a user provides an existing project, this prompt helps you:
1. Detect the project structure
2. Identify technologies used
3. Analyze code quality
4. Generate project-specific configuration
5. Create custom prompts for this project

=================================================================================
ANALYSIS WORKFLOW
=================================================================================

## Step 1: Initial Scan

```bash
# Run the project analyzer
python3 tools/project_analyzer.py /path/to/project
```

The analyzer will detect:
- Frontend framework (React, Vue, Angular, etc.)
- Backend framework (Django, Flask, FastAPI, Express, etc.)
- Database type (PostgreSQL, MySQL, MongoDB, etc.)
- Project structure
- Dependencies
- Configuration files

## Step 2: Technology Detection

### Frontend Detection

**React:**
- Look for: `package.json` with `"react"` dependency
- Look for: `src/App.js` or `src/App.tsx`
- Look for: JSX/TSX files
- Indicators: `create-react-app`, `next.js`, `gatsby`

**Vue:**
- Look for: `package.json` with `"vue"` dependency
- Look for: `src/App.vue`
- Look for: `.vue` files
- Indicators: `@vue/cli`, `nuxt`

**Angular:**
- Look for: `package.json` with `"@angular/core"`
- Look for: `angular.json`
- Look for: `src/app/app.component.ts`
- Indicators: `@angular/cli`

**Plain HTML/CSS/JS:**
- Look for: `index.html` in root
- No framework dependencies
- Simple file structure

### Backend Detection

**Django:**
- Look for: `manage.py`
- Look for: `settings.py`
- Look for: `requirements.txt` or `Pipfile` with `Django`
- Look for: `urls.py`, `models.py`, `views.py`

**FastAPI:**
- Look for: `main.py` with `from fastapi import FastAPI`
- Look for: `requirements.txt` with `fastapi`
- Look for: `uvicorn` in dependencies

**Flask:**
- Look for: `app.py` or `application.py`
- Look for: `requirements.txt` with `Flask`
- Look for: `from flask import Flask`

**Express (Node.js):**
- Look for: `package.json` with `"express"`
- Look for: `server.js` or `app.js`
- Look for: `const express = require('express')`

### Database Detection

**PostgreSQL:**
- Look for: `psycopg2` in Python requirements
- Look for: `pg` in Node.js dependencies
- Look for: Connection strings with `postgresql://`
- Look for: `DATABASE_URL` with postgres

**MySQL:**
- Look for: `mysqlclient` or `PyMySQL` in Python
- Look for: `mysql2` in Node.js
- Look for: Connection strings with `mysql://`

**MongoDB:**
- Look for: `pymongo` in Python
- Look for: `mongoose` in Node.js
- Look for: Connection strings with `mongodb://`

**SQLite:**
- Look for: `sqlite3` in Python
- Look for: `.db` or `.sqlite` files
- Look for: Django with `ENGINE: 'django.db.backends.sqlite3'`

## Step 3: Structure Analysis

### Directory Structure Patterns

**Monolithic:**
```
project/
├── frontend/
├── backend/
└── database/
```

**Microservices:**
```
project/
├── service-a/
├── service-b/
├── service-c/
└── gateway/
```

**Full-stack (Django):**
```
project/
├── apps/
│   ├── users/
│   ├── products/
│   └── orders/
├── static/
├── templates/
└── manage.py
```

**Full-stack (MERN):**
```
project/
├── client/          # React
├── server/          # Express
└── package.json
```

## Step 4: Dependency Analysis

### Python Projects

```bash
# Check requirements.txt
cat requirements.txt

# Check Pipfile
cat Pipfile

# Check pyproject.toml
cat pyproject.toml
```

Common dependencies and their purposes:
- `django` → Web framework
- `djangorestframework` → API framework
- `celery` → Background tasks
- `redis` → Caching
- `gunicorn` → WSGI server
- `pytest` → Testing
- `black` → Code formatting
- `flake8` → Linting

### Node.js Projects

```bash
# Check package.json
cat package.json
```

Common dependencies:
- `express` → Web framework
- `react` → Frontend library
- `next` → React framework
- `mongoose` → MongoDB ORM
- `sequelize` → SQL ORM
- `jest` → Testing
- `eslint` → Linting
- `prettier` → Formatting

## Step 5: Configuration Detection

### Environment Variables

Look for:
- `.env` file
- `.env.example` file
- `config.py` or `settings.py`
- `config.js` or `config.json`

Common variables:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000
```

### Docker Configuration

Look for:
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

Analyze Docker setup:
- Which services are defined?
- What ports are exposed?
- What volumes are mounted?
- What networks are used?

## Step 6: Code Quality Analysis

### Python Code Quality

```bash
# Run flake8
flake8 . --count --statistics

# Run pylint
pylint **/*.py

# Check test coverage
pytest --cov=. --cov-report=html
```

### JavaScript Code Quality

```bash
# Run ESLint
eslint src/

# Run Prettier check
prettier --check src/

# Check test coverage
npm test -- --coverage
```

## Step 7: API Endpoint Discovery

### Django REST Framework

```python
# Look for urls.py patterns
from django.urls import path
from rest_framework.routers import DefaultRouter

# Common patterns:
# /api/users/
# /api/products/
# /api/orders/
```

### FastAPI

```python
# Look for @app.get, @app.post decorators
@app.get("/api/users")
@app.post("/api/users")
```

### Express

```javascript
// Look for app.get, app.post
app.get('/api/users', ...)
app.post('/api/users', ...)
```

## Step 8: Database Schema Analysis

### Django Models

```python
# Analyze models.py files
class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    ...
```

Extract:
- Model names
- Field types
- Relationships (ForeignKey, ManyToMany)
- Indexes

### SQL Migrations

Look for:
- Django: `migrations/` folders
- Alembic: `versions/` folder
- Sequelize: `migrations/` folder

Analyze migration files to understand schema evolution.

=================================================================================
ANALYSIS OUTPUT
=================================================================================

## Project Report

After analysis, generate a comprehensive report:

```markdown
# Project Analysis Report

## Overview
- **Project Name:** [detected from package.json, setup.py, etc.]
- **Project Type:** [Web App, API, Full-stack, etc.]
- **Structure:** [Monolithic, Microservices, etc.]

## Technology Stack

### Frontend
- **Framework:** React 18.2.0
- **State Management:** Redux Toolkit
- **Routing:** React Router v6
- **UI Library:** Material-UI
- **Build Tool:** Vite

### Backend
- **Framework:** Django 4.2
- **API:** Django REST Framework 3.14
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Task Queue:** Celery with Redis
- **WSGI Server:** Gunicorn

### Database
- **Type:** PostgreSQL 15
- **ORM:** Django ORM
- **Migrations:** Django migrations
- **Schema:** 12 models, 45 fields

### DevOps
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Testing:** pytest, Jest
- **Linting:** flake8, ESLint

## Project Structure

```
project/
├── frontend/           # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── store/
│   └── package.json
├── backend/            # Django application
│   ├── apps/
│   │   ├── users/
│   │   ├── products/
│   │   └── orders/
│   ├── config/
│   └── manage.py
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Users
- GET /api/users/ - List users
- POST /api/users/ - Create user
- GET /api/users/{id}/ - Get user
- PUT /api/users/{id}/ - Update user
- DELETE /api/users/{id}/ - Delete user

### Products
- GET /api/products/ - List products
- POST /api/products/ - Create product
- ...

## Database Schema

### Users Table
- id: AutoField (PK)
- username: CharField(150)
- email: EmailField
- password: CharField(128)
- created_at: DateTimeField

### Products Table
- id: AutoField (PK)
- name: CharField(200)
- price: DecimalField
- stock: IntegerField
- created_at: DateTimeField

## Code Quality

### Python
- **Lines of Code:** 5,234
- **Flake8 Issues:** 23 (mostly line length)
- **Test Coverage:** 78%
- **Pylint Score:** 8.5/10

### JavaScript
- **Lines of Code:** 3,456
- **ESLint Issues:** 12
- **Test Coverage:** 65%
- **Bundle Size:** 245 KB (gzipped)

## Configuration

### Environment Variables
- DATABASE_URL
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- FRONTEND_URL
- REDIS_URL
- CELERY_BROKER_URL

### Ports
- Frontend: 3000
- Backend: 8000
- Database: 5432
- Redis: 6379

## Recommendations

### High Priority
1. Increase test coverage to 80%+
2. Fix security issues in dependencies
3. Add API documentation (OpenAPI/Swagger)

### Medium Priority
1. Improve code quality (fix linting issues)
2. Add monitoring and logging
3. Optimize database queries

### Low Priority
1. Refactor large components
2. Update outdated dependencies
3. Improve error handling

## Next Steps

1. Load relevant prompts:
   - 10_backend.txt (Django)
   - 11_frontend.txt (React)
   - 12_database.txt (PostgreSQL)
   - 13_api.txt (REST API)

2. Generate project-specific configuration:
   - Create .global/project.json
   - Create custom prompt

3. Provide assistance based on detected tech stack
```

=================================================================================
PROJECT-SPECIFIC CONFIGURATION
=================================================================================

## Generate .global/project.json

Based on analysis, create configuration file:

```json
{
  "project_name": "MyProject",
  "project_slug": "my-project",
  "project_type": "full-stack-web-app",
  "detected": true,
  "tech_stack": {
    "backend": {
      "framework": "Django",
      "version": "4.2",
      "language": "Python",
      "language_version": "3.11"
    },
    "frontend": {
      "framework": "React",
      "version": "18.2.0",
      "language": "JavaScript",
      "build_tool": "Vite"
    },
    "database": {
      "type": "PostgreSQL",
      "version": "15",
      "orm": "Django ORM"
    }
  },
  "structure": {
    "type": "monolithic",
    "frontend_path": "frontend/",
    "backend_path": "backend/",
    "docker": true
  },
  "ports": {
    "frontend": 3000,
    "backend": 8000,
    "database": 5432
  },
  "features": {
    "authentication": true,
    "api": true,
    "celery": true,
    "docker": true,
    "ci_cd": true
  },
  "quality": {
    "test_coverage": {
      "backend": 78,
      "frontend": 65
    },
    "linting": {
      "backend": "flake8",
      "frontend": "eslint"
    }
  }
}
```

=================================================================================
CUSTOM PROMPT GENERATION
=================================================================================

## Create Project-Specific Prompt

Generate a custom prompt tailored to this project:

```
# Custom Prompt for MyProject

## Project Context
This is a full-stack web application built with:
- **Frontend:** React 18.2.0 with Redux Toolkit
- **Backend:** Django 4.2 with DRF
- **Database:** PostgreSQL 15

## Key Information
- Frontend runs on port 3000
- Backend runs on port 8000
- Uses JWT authentication
- Has Celery for background tasks
- Dockerized with docker-compose

## Common Tasks

### Start Development
```bash
docker-compose up -d
```

### Run Tests
```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

### Apply Migrations
```bash
docker-compose exec backend python manage.py migrate
```

## Relevant Prompts
When working on this project, use:
- 10_backend.txt (Django-specific guidance)
- 11_frontend.txt (React-specific guidance)
- 12_database.txt (PostgreSQL guidance)
- 21_authentication.txt (JWT authentication)

## Code Style
- Python: Follow PEP 8, use Black formatter
- JavaScript: Follow Airbnb style guide, use Prettier
- Max line length: 88 (Python), 100 (JavaScript)

## Testing
- Backend: pytest with >80% coverage
- Frontend: Jest + React Testing Library with >70% coverage

## Deployment
- Uses Docker
- CI/CD with GitHub Actions
- Deployed to [deployment target]
```

=================================================================================
INTEGRATION WITH OTHER PROMPTS
=================================================================================

After analysis, load relevant prompts based on detected technologies:

**If Django detected:**
→ Load 10_backend.txt (Django section)

**If React detected:**
→ Load 11_frontend.txt (React section)

**If PostgreSQL detected:**
→ Load 12_database.txt (PostgreSQL section)

**If API detected:**
→ Load 13_api.txt

**If authentication detected:**
→ Load 21_authentication.txt

**If Docker detected:**
→ Load 40_deployment.txt (Docker section)

=================================================================================
TROUBLESHOOTING
=================================================================================

## Common Issues

### Cannot Detect Framework

**Problem:** Analyzer cannot identify framework
**Solution:**
1. Check for package.json or requirements.txt
2. Look for framework-specific files manually
3. Ask user directly

### Multiple Frameworks Detected

**Problem:** Project uses multiple frameworks (e.g., Django + FastAPI)
**Solution:**
1. Identify primary framework (most files)
2. Note secondary frameworks
3. Load prompts for both

### Outdated Dependencies

**Problem:** Project uses old versions
**Solution:**
1. Note in analysis report
2. Recommend updates
3. Check for security vulnerabilities

=================================================================================
BEST PRACTICES
=================================================================================

1. **Be thorough:** Check all common locations
2. **Be accurate:** Verify detections
3. **Be helpful:** Provide actionable recommendations
4. **Be respectful:** Don't modify code without permission
5. **Be transparent:** Show what you detected and how

=================================================================================
NEXT STEPS
=================================================================================

After completing analysis:
1. Present analysis report to user
2. Save project configuration
3. Load relevant prompts
4. Ask user what they want to do next:
   - Add new features?
   - Fix issues?
   - Improve quality?
   - Deploy?

=================================================================================
END OF ANALYSIS PROMPT
=================================================================================



================================================================================
ADDITIONAL CONTENT FROM 
================================================================================

## 59. Comprehensive Dependency Management

--------------------------------------------------------------------------------



================================================================================
RECOVERED CONTENT FROM  (Phase 2)
================================================================================

e 2 — System & Forces
- Map agents, variables, relationships
- Dependency/call/import graphs
- Flag cycles and bottlenecks

Phase 3 — Probabilistic Behavior Modeling
- Model user/admin/API/attacker behaviors
- Justify with data/patterns
- Security threat modeling

Phase 4 — Strategy Generation (≥3 options)
- Scope, cost, risk, impact, prerequisites
- OSF_Score for each option
- No feature disabling

Phase 5 — Stress Testing & Forecasting
- Best/Worst/Most-Probable scenarios
- Triggers and rollback plans
- Load testing, chaos engineering

Phase 6 — Self-Correction Loop
- Refinement → Hybridization → Inversion
- Reward Metric (0.0–1.0)
- Choose highest-reward path

Phase 7 — Operational Principle Extraction
- Extract reusable, abstract rules
- Document in project memory
- Update guidelines

Phase 8 — Final Review
- 100% adherence check
- Document exceptions
- Sign-off

⸻

6) BACKEND & API DESIGN (Expanded in )

A) Stack Selection
- Languages: Python (FastAPI/Django), Node.js (Express
- Model selection
- Cross-validation
- Baseline comparison

C) Model Evaluation
- Metrics: accuracy, precision, recall, F1, AUC
- Confusion matrix
- Feature importance
- Bias/fairness checks
- A/B testing

D) Model Serving
- Model registry
- Versioning (semantic versioning)
- Deployment strategies (canary, blue-green)
- API endpoints
- Batch vs real-time

E) Monitoring
- Model performance metrics
- Data drift detection
- Concept drift detection
- Latency monitoring
- Error rate tracking

F) Retraining Pipeline
- Scheduled retraining (weekly, monthly)
- Trigger-based (performance degradation)
- Automated or manual approval
- Rollback capability

G) Governance
- Model cards (documentation)
- Audit trail
- Compliance (GDPR, HIPAA if applicable)
- Explainability (SHAP, LIME)

H) Tools
- Training: PyTorch, TensorFlow, scikit-learn
- Tracking: MLflow, Weights & Biases
- Serving: TorchServe, TensorFlow Serving, FastAPI
- Monitoring: Prometheus, Grafana, custom dashboards
- Orchestration: Airf
) CI ENFORCEMENT

Add to `.github/workflows/ci.yml`:
```yaml
- name: Check for duplicate files
  run: |
    python scripts/detect_duplicates.py --strict
    if [ $? -ne 0 ]; then
      echo "❌ Duplicate files detected!"
      exit 1
    fi

- name: Verify File Map is updated
  run: |
    python scripts/map_files.py --check
    git diff --exit-code docs/File_Map.md || \
      (echo "❌ File_Map.md is out of date!" && exit 1)
```

E) NAMING CONVENTIONS TO PREVENT CONFUSION

**WRONG:**
- `user.py`, `users.py`, `user_model.py`, `user_unified.py`

**CORRECT:**
- `models/user.py` (CANONICAL - the one true User model)
- All other files import from this canonical location

F) AUTOMATED FILE MAP GENERATION

Run after any file changes:
```bash
# Generate complete file map
python scripts/map_files.py

# Update imports map
python scripts/generate_imports_map.py

# Update exports map  
python scripts/generate_exports_map.py
```

G) BENEFITS

✅ No duplicate files  
✅ Clear file ownership  
✅ Easy to 
 │
│  ✅ Email configured                    │
│  ✅ Security settings applied           │
│                                         │
│  Ready to complete setup?               │
│                                         │
│  [Back] [Complete Setup]                │
└─────────────────────────────────────────┘
```

C) IMPLEMENTATION

```python
# backend/src/setup/wizard.py
from flask import Blueprint, render_template, request, redirect, session
from .validators import validate_admin_user, validate_db_config, validate_smtp

setup_bp = Blueprint('setup', __name__, url_prefix='/setup')

@setup_bp.route('/wizard', methods=['GET', 'POST'])
def wizard():
    step = request.args.get('step', '1')
    
    if request.method == 'POST':
        if step == '1':
            # Requirements check passed
            return redirect('/setup/wizard?step=2')
        
        elif step == '2':
            # Create admin user
            email = request.form['email']
            password = request.form['passw
r type definition
- `UserRole` (enum) - User roles
- `UserStatus` (enum) - User statuses

**Usage Count:** 23 imports across 12 files

---

### hooks/useAuth.tsx
**Exports:**
- `useAuth` (hook) - Authentication hook
- `AuthProvider` (component) - Auth context provider

**Usage Count:** 18 imports across 10 files

---

## Duplicate Exports Detected

❌ **User class exported from multiple locations:**
- `models/user.py` (CANONICAL)
- `models/user_unified.py` (DUPLICATE - should be removed)
- `models/users.py` (DUPLICATE - should be removed)

**Action Required:** Consolidate into single canonical export
```

C) GENERATION SCRIPT

```python
# scripts/generate_imports_map.py
import ast
import os
from pathlib import Path
from typing import Dict, List, Set

def analyze_python_imports(file_path: str) -> Dict:
    """Analyze imports in a Python file"""
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(nod
```

D) CI CHECK

```yaml
# .github/workflows/imports-check.yml
- name: Check for circular dependencies
  run: |
    python scripts/generate_imports_map.py --check-circular
    if [ $? -ne 0 ]; then
      echo "❌ Circular dependencies detected!"
      exit 1
    fi

- name: Check for duplicate exports
  run: |
    python scripts/detect_duplicate_exports.py
    if [ $? -ne 0 ]; then
      echo "❌ Duplicate exports detected!"
      exit 1
    fi
```

E) BENEFITS

✅ Clear dependency tracking  
✅ Detect circular dependencies  
✅ Identify duplicate exports  
✅ Easy refactoring  
✅ Better code organization

⸻

37) DUPLICATION DETECTION & PREVENTION (CRITICAL - NEW in )

**PURPOSE:** Prevent and eliminate duplicate code/files

A) SEMANTIC DUPLICATION DETECTION

```python
# scripts/detect_duplicates.py
import ast
import difflib
from pathlib import Path
from typing import List, Dict

class DuplicateDetector:
    def __init__(self, threshold=0.8):
        self.threshold = threshold  # Simila
      return 1  # Exit with error
    else:
        print("✅ No duplicates found!")
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
```

B) CONSOLIDATION PROCESS

When duplicates are found:

1. **Identify Canonical Version**
   - Most complete implementation
   - Best documented
   - Most recently updated
   - In the correct location

2. **Update All Imports**
   ```python
   # Before (scattered)
   from models.user import User
   from models.user_unified import User
   from models.users import User
   
   # After (consolidated)
   from models.user import User  # CANONICAL
   ```

3. **Move Duplicates to /unneeded**
   ```bash
   mkdir -p /unneeded/models
   mv models/user_unified.py /unneeded/models/user_unified.removed.py
   mv models/users.py /unneeded/models/users.removed.py
   ```

4. **Add Pointer File**
   ```python
   # /unneeded/models/user_unified.removed.py
   """
   REMOVED: 2025-10-28
   REASON: Duplicate of models/user.py
   COMMIT: abc123
def456
   CANONICAL: models/user.py
   
   This file was a duplicate and has been removed.
   All imports should use: from models.user import User
   """
   ```

5. **Document in Duplicates Log**
   ```markdown
   # /docs/Duplicates_Log.md
   
   ## 2025-10-28: User Model Consolidation
   
   **Canonical:** `models/user.py`
   
   **Removed Duplicates:**
   - `models/user_unified.py` → `/unneeded/models/user_unified.removed.py`
   - `models/users.py` → `/unneeded/models/users.removed.py`
   
   **Commit:** abc123def456
   
   **Files Updated:** 8 files
   - `services/auth_service.py`
   - `routes/user_routes.py`
   - (list all updated files)
   ```

C) CI ENFORCEMENT

```yaml
- name: Check for duplicates
  run: |
    python scripts/detect_duplicates.py --strict
    if [ $? -ne 0 ]; then
      echo "❌ Duplicates detected! Please consolidate."
      exit 1
    fi
```

D) BENEFITS

✅ No duplicate code  
✅ Single source of truth  
✅ Easier maintenance  
✅ Smaller codebase  
✅ Clear history
r functions: `grep -r "def <function_name>"`
- [ ] Run semantic search: `python scripts/detect_duplicates.py --target "<name>"`

## 4. Plan Your Changes
- [ ] Identified canonical file/class to use or extend
- [ ] No duplication of existing functionality
- [ ] Changes documented in TODO.md
- [ ] Discussed with team (if applicable)

## 5. Testing Preparation
- [ ] Identified test files to update
- [ ] Planned new tests for new functionality
- [ ] Cross-browser testing plan (if frontend)

## 6. Ready to Code
- [ ] All above items checked
- [ ] Environment is clean (no uncommitted changes)
- [ ] Created feature branch: `git checkout -b feature/<name>`

---

**Sign-off:** I have completed this checklist.

**Date:** ___________

**Developer:** ___________
```

B) AUTOMATED ENFORCEMENT

```python
# scripts/pre_dev_check.py
import sys
from validate_env import validate_env
from pathlib import Path

def pre_development_check():
    """Run all pre-development checks"""
    errors = []
    
    #

34. Production Error Handling
35. .env Validation & Management
36. Import/Export Documentation
37. Duplication Detection & Prevention
38. Pre-Development Checklist

**PROBLEMS SOLVED:**
✅ File duplication (user.py, user_unified.py, users.py)
✅ No environment detection (dev vs prod)
✅ No setup wizard for production
✅ Cross-browser compatibility issues
✅ UI assets not loading
✅ Error leaks in production
✅ .env misconfiguration
✅ No import/export tracking
✅ Duplicate code detection
✅ No pre-development checks

**NEW SCRIPTS (6):**
- `map_files.py` - Generate file map
- `validate_env.py` - Validate .env
- `detect_duplicates.py` - Find duplicates
- `generate_imports_map.py` - Track imports
- `setup_wizard.py` - Production setup
- `pre_dev_check.py` - Pre-development checks

**NEW DOCUMENTATION (7):**
- `/docs/File_Map.md`
- `/docs/Imports_Map.md`
- `/docs/Exports_Map.md`
- `/docs/Env.md`
- `/docs/Duplicates_Log.md`
- `/docs/Cross_Browser_Tests.md`
- `/docs/Setup_Guide.md`

**CI/CD CHECKS (
seModel):
    """Base for all Pydantic models"""
    class Config:
        from_attributes = True
        validate_assignment = True

class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SoftDeleteMixin(BaseModel):
    is_deleted: bool = False
    deleted_at: datetime | None = None
```

### custom.py - Project Specific
```python
"""Project-specific definitions"""

from enum import Enum

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

### __init__.py - Central Registry
```python
"""Central registry for all definitions"""

from .common import *
from .core import *
from .custom import *

__all__ = [
    # Common
    'Status', 'UserRole', 'APIResponse',
    # Core
    'BaseModel', 'Timestamp
Mixin', 'SoftDeleteMixin',
    # Custom
    'ProjectStatus', 'Priority',
]
```

### Usage
```python
# Import from central registry
from config.definitions import (
    Status,
    UserRole,
    APIResponse,
    BaseModel,
    TimestampMixin,
    ProjectStatus
)

class User(BaseModel, TimestampMixin):
    username: str
    role: UserRole
    status: Status
```

## Rules
1. ✅ ONE definition per concept
2. ✅ Import from config.definitions only
3. ✅ Document all definitions
4. ✅ Use type hints
5. ✅ Export via __all__

================================================================================
41. LINE LENGTH ENFORCEMENT (≤120)
================================================================================

## Problem
- Lines too long (>120 chars)
- Hard to read and review
- No consistent standard

## Solution: Automated Enforcement

### .flake8
```ini
[flake8]
max-line-length = 120
exclude = .git,__pycache__,venv,.venv,migrations,node_modules
ignore = E203,W503
per-file-ignores =
   
 exit 1
  }
```

### CI Check
```yaml
- name: Check Unused Code
  run: |
    pip install autoflake
    autoflake --check --recursive --exclude=venv,.venv .
```

### Manual Check
```bash
# Find unused imports
flake8 . --select=F401 --exclude=venv,.venv,migrations

# Find unused variables
flake8 . --select=F841 --exclude=venv,.venv,migrations

# Find undefined names
flake8 . --select=F821 --exclude=venv,.venv,migrations
```

## Rules
1. ✅ No unused imports
2. ✅ No unused variables
3. ✅ No dead code
4. ✅ CI enforced
5. ✅ Auto-fix available

================================================================================
44. GITHUB WORKFLOWS FIX
================================================================================

## Problem
- Workflows fail during installation
- Missing dependencies
- Incorrect setup steps

## Solution: Fixed CI/CD Pipeline

### .github/workflows/ci.yml
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main,
me: Document Imports/Exports
  run: python scripts/document_imports.py . docs/Imports_Exports.md
```

## Rules
1. ✅ Document all imports
2. ✅ Document all exports (__all__)
3. ✅ Auto-generate on CI
4. ✅ Check for circular dependencies
5. ✅ Keep up-to-date

================================================================================
 SUMMARY
================================================================================

## New Sections (39-45)

39. **Port Configuration Management** - Single source of truth for ports
40. **Organized Definitions Structure** - Three-tier definition system
41. **Line Length Enforcement** - Max 120 characters
42. **Environment-Based Error Handling** - Different errors for dev/prod
43. **Unused Code Removal** - Automated cleanup
44. **GitHub Workflows Fix** - Fixed CI/CD pipelines
45. **Import/Export Documentation** - Auto-generated docs

## Problems Solved

1. ✅ Port conflicts (8000 vs 3000)
2. ✅ Undefined classes
3. ✅ No organized definitions
4. ✅
black
    rev: 23.12.1
    hooks:
      - id: black
        args: [--line-length=120]
  
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120, --extend-ignore=E203]
  
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black, --line-length=120]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: 
    hooks:
      - id: mypy
        args: [--strict, --ignore-missing-imports]
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: [-r, ., -f, json, -o, bandit-report.json]
```

**Enforcement:**
- Runs automatically on `git commit`
- Blocks commit if checks fail
- Can be bypassed with `--no-verify` (DISCOURAGED)

### 46.2 CI/CD Quality Gates (MANDATORY)

**Pipeline Stages:**
1. **Linting** (flake8 + pylint)
2. **Type Checking** (mypy --strict)
3. **Security** (bandit + safety)
4. **Tests** (pyte
st with coverage ≥80%)
5. **Complexity** (radon, max C)
6. **Dead Code** (vulture)

**Quality Metrics:**
- Line length: ≤120 characters
- Test coverage: ≥80%
- Cyclomatic complexity: ≤C (radon scale)
- Security issues: 0 high/critical
- Type coverage: 100%

**Failure = Build Fails**

### 46.3 Verification Script

**Location:** `scripts/verify_all.sh`

```bash
#!/bin/bash
# Comprehensive verification script

set -e

echo "🔍 Running comprehensive verification..."

# 1. Code style
echo "📝 Checking code style..."
black --check --line-length=120 . || exit 1
isort --check-only --profile=black . || exit 1

# 2. Linting
echo "🔎 Linting..."
flake8 . --max-line-length=120 --extend-ignore=E203 || exit 1
pylint --max-line-length=120 --disable=C0111 . || exit 1

# 3. Type checking
echo "🔢 Type checking..."
mypy --strict --ignore-missing-imports . || exit 1

# 4. Security
echo "🔒 Security checks..."
bandit -r . -f json -o bandit-report.json || exit 1
safety check || exit 1

# 5. Complexity
echo "📊 C
omplexity analysis..."
radon cc . -a -s -n C || exit 1
radon mi . -s -n B || exit 1

# 6. Dead code
echo "💀 Dead code detection..."
vulture . --min-confidence 80 || exit 1

# 7. Tests
echo "🧪 Running tests..."
pytest --cov=. --cov-report=term --cov-report=html --cov-fail-under=80 || exit 1

# 8. Line length check
echo "📏 Checking line length..."
bash scripts/fix_line_length.sh --check || exit 1

# 9. Unused imports
echo "🗑️  Checking unused imports..."
bash scripts/remove_unused.sh --check || exit 1

echo "✅ All verification checks passed!"
```

**Usage:**
```bash
# Before every PR
./scripts/verify_all.sh

# In CI/CD
./scripts/verify_all.sh || exit 1
```

### 46.4 Testing Pyramid

**Structure:**
```
         /\
        /E2E\        10% - End-to-End Tests
       /------\
      /Integr.\     20% - Integration Tests
     /----------\
    /   Unit     \  70% - Unit Tests
   /--------------\
```

**Requirements:**
- **Unit Tests:** 70% of total tests
  - Fast (<100ms each)
  - Isolated
  - 
ests/*", "*/migrations/*", "*/__pycache__/*"]

[tool.coverage.report]
fail_under = 80
precision = 2

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

---

## 47. Function Reference System

### 47.1 Function Reference File (APPEND-ONLY)

**Location:** `docs/function_reference.md`

**Rules:**
- **APPEND-ONLY** - Never delete entries
- Document ALL shared/reusable functions
- Update when adding new shared functions
- Include examples for each function

**Template:**
```markdown
## Function: `function_name`

**File:** `path/to/file.py`
**Module:** `module_name`
**Added:** YYYY-MM-DD
**Author:** Author Name

**Description:**
Brief description of what the function does.

**Signature:**
```python
def function_name(param1: Type1, param2: Type2 = default) -> ReturnType:
    """Docstring."""
    pass
```

**Parameters:**
- `param1` (Type1): Description
- `param2` (Type2, optional): Description. Defaults to `default`.

**Returns:**
- `ReturnType`: Description


'quantity': 2}]
        >>> calculate_total(items, tax_rate=0.10)
        Decimal('22.00')
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
    return subtotal * (1 + Decimal(str(tax_rate)))
```

### 47.3 CI Enforcement

**Pre-commit Hook:**
```yaml
- repo: local
  hooks:
    - id: check-function-reference
      name: Check function reference is updated
      entry: python scripts/check_function_reference.py
      language: python
      pass_filenames: false
```

**Script:** `scripts/check_function_reference.py`
```python
#!/usr/bin/env python3
"""Check that all shared functions are documented in function_reference.md"""

import ast
import sys
from pathlib import Path

def find_shared_functions():
    """Find all functions in shared/common modules."""
    shared_dirs = ['utils', 'common', '
s
- Memory leaks
- Inefficient algorithms

**5. Security Errors**
- SQL injection
- XSS vulnerabilities
- Authentication bypass

### 48.3 Error Prevention Checklist

Before committing code:
- [ ] Read `Dont_make_this_error_again.md`
- [ ] Check for similar past errors
- [ ] Apply relevant prevention measures
- [ ] Add tests for error scenarios
- [ ] Update error log if new error type

### 48.4 CI Integration

**Pre-commit Hook:**
```yaml
- repo: local
  hooks:
    - id: check-error-patterns
      name: Check for known error patterns
      entry: python scripts/check_error_patterns.py
      language: python
```

**Script:** `scripts/check_error_patterns.py`
```python
#!/usr/bin/env python3
"""Check code for known error patterns from error log."""

import re
import sys
from pathlib import Path

def load_error_patterns():
    """Load error patterns from error log."""
    error_file = Path('docs/errors/Dont_make_this_error_again.md')
    if not error_file.exists():
        return []
    
 
()
    if check_files_for_patterns(patterns):
        print("\n❌ Known error patterns detected!")
        print("   Check docs/errors/Dont_make_this_error_again.md")
        sys.exit(1)
    
    print("✅ No known error patterns found")
```

---

## 49. Module Discovery & Reuse

### 49.1 ALWAYS Search Before Creating (MANDATORY)

**Rule:** **NEVER** create a new module without searching for existing ones first.

**Search Process:**
1. **Search by functionality**
   ```bash
   grep -r "function_name" .
   find . -name "*keyword*"
   ```

2. **Check module map**
   ```bash
   python scripts/map_files.py . docs/Module_Map.md
   cat docs/Module_Map.md
   ```

3. **Search imports**
   ```bash
   grep -r "from.*import" . | grep "keyword"
   ```

4. **Check function reference**
   ```bash
   grep "keyword" docs/function_reference.md
   ```

### 49.2 Module Map Generation

**Script:** `scripts/generate_module_map.py`
```python
#!/usr/bin/env python3
"""Generate comprehensive module map."""

imp
nt("✅ Module map generated: docs/Module_Map.md")
```

**Usage:**
```bash
# Generate module map
python scripts/generate_module_map.py

# View module map
cat docs/Module_Map.md

# Search in module map
grep "function_name" docs/Module_Map.md
```

### 49.3 Dependency Analysis

**Start with Least Dependent Modules**

**Script:** `scripts/analyze_dependencies.py`
```python
#!/usr/bin/env python3
"""Analyze module dependencies and suggest build order."""

import ast
from pathlib import Path
from collections import defaultdict

def get_dependencies(file_path):
    """Get internal dependencies of a module."""
    with open(file_path) as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return set()
    
    deps = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and not node.module.startswith(('os', 'sys', 'json')):
                # Only internal imports
                if not node.module.
ief description of file purpose

Dependencies:
- dependency1
- dependency2

Related Files:
- related_file1.py
- related_file2.py
"""
```

**TypeScript/JavaScript:**
```typescript
/**
 * File: path/to/file.ts
 * Module: module_name
 * Created: YYYY-MM-DD
 * Last Modified: YYYY-MM-DD
 * Author: author_name
 * Description: Brief description of file purpose
 * 
 * Dependencies:
 * - dependency1
 * - dependency2
 * 
 * Related Files:
 * - related_file1.ts
 * - related_file2.ts
 */
```

### 52.2 CI Enforcement

**Pre-commit Hook:**
```yaml
- repo: local
  hooks:
    - id: check-file-headers
      name: Check file headers
      entry: python scripts/check_file_headers.py
      language: python
```

**Script:** `scripts/check_file_headers.py`
```python
#!/usr/bin/env python3
"""Check that all files have proper headers."""

import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ['File:', 'Module:', 'Created:', 'Author:', 'Description:']

def check_python_header(file_path):
    """Chec
  # 70% of tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/    # 20% of tests
│   ├── test_api.py
│   └── test_database.py
└── e2e/            # 10% of tests
    └── test_workflows.py
```

**pytest Configuration:** `pytest.ini`
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --cov=.
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
    -ra
    -q
```

**Example Unit Test:**
```python
"""
File: tests/unit/test_order_service.py
Module: tests.unit.test_order_service
Created: 2025-01-15
Author: Team
Description: Unit tests for order service
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock, patch
from services.order_service import OrderService

class TestOrderService:
    """Test OrderService class."""
    
    @pytest.fixture
    def order_service(sel
   └── utils/
└── README.md
```

### 54.3 Model Example (Following 'sales' Standards)

```python
"""
File: module_name/models/main_model.py
Module: module_name.models.main_model
Created: 2025-01-15
Author: Team
Description: النموذج الرئيسي للوحدة

Dependencies:
- django.db.models
- django.contrib.auth.models
"""

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class MainModel(models.Model):
    """
    النموذج الرئيسي للوحدة.
    
    يحتوي على جميع الحقول والعلاقات الأساسية.
    """
    
    # حالات النموذج
    STATE_DRAFT = 'draft'
    STATE_CONFIRMED = 'confirmed'
    STATE_CANCELLED = 'cancelled'
    
    STATES = [
        (STATE_DRAFT, 'مسودة'),
        (STATE_CONFIRMED, 'مؤكد'),
        (STATE_CANCELLED, 'ملغي'),
    ]
    
    # الحقول الأساسية
    name = models.CharField('الاسم', max_length=255)
    code = models.CharField('الرمز', max_length=50, unique=True)
    description = models.TextField('الوصف', blank=True)
    
    
25-01-15
Author: Team
Description: Type definitions and type hints
"""

from typing import TypedDict, Literal, Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime

# State types
StateType = Literal['draft', 'confirmed', 'cancelled', 'done']
PermissionType = Literal['view', 'create', 'edit', 'delete', 'admin']

# API Response types
class APIResponse(TypedDict):
    """Standard API response structure."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]]
    errors: Optional[List[str]]

class PaginatedResponse(TypedDict):
    """Paginated API response."""
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Dict[str, Any]]

# Business types
class OrderItem(TypedDict):
    """Order item structure."""
    product_id: int
    quantity: int
    price: Decimal
    subtotal: Decimal

class Order(TypedDict):
    """Order structure."""
    id: int
    code: str
    customer_id: int
    items: List[OrderItem]
    s
cal paths exist and pass
- [ ] Frontend tests exist and pass
- [ ] Coverage ≥80%

### 57.2 Gap Analysis Script

**Location:** `scripts/analyze_gaps.py`

```python
#!/usr/bin/env python3
"""
Analyze gaps between design and implementation.

File: scripts/analyze_gaps.py
Module: scripts.analyze_gaps
Created: 2025-01-15
Author: Team
Description: Compare design specs with actual implementation
"""

import ast
import json
from pathlib import Path
from typing import Dict, List, Set

def find_api_endpoints() -> Set[str]:
    """Find all defined API endpoints."""
    endpoints = set()
    
    for py_file in Path('.').rglob('*views.py'):
        with open(py_file) as f:
            content = f.read()
        
        # Find @api_view decorators
        import re
        patterns = re.findall(r'@api_view\([\'"]([A-Z]+)[\'"]\)', content)
        # Find route definitions
        routes = re.findall(r'path\([\'"]([^\'\"]+)[\'"]', content)
        
        endpoints.update(routes)
    
    return en
dpoints

def find_frontend_routes() -> Set[str]:
    """Find all frontend routes."""
    routes = set()
    
    # Check React Router
    for tsx_file in Path('.').rglob('*.tsx'):
        with open(tsx_file) as f:
            content = f.read()
        
        import re
        patterns = re.findall(r'<Route\s+path=[\'"]([^\'\"]+)[\'"]', content)
        routes.update(patterns)
    
    return routes

def find_database_models() -> Set[str]:
    """Find all database models."""
    models = set()
    
    for py_file in Path('.').rglob('models.py'):
        with open(py_file) as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                continue
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's a Django model
                for base in node.bases:
                    if isinstance(base, ast.Attribute):
                        if base.attr == 'Model':
           
istry

**🟢 Medium Priority (56-57):**
- 56. Dependency Management
- 57. Design vs Implementation Gap Analysis

### Statistics

- **Total Sections:** 57 (was 45)
- **New Sections:** 12
- **Total Lines:** ~6,600 (was ~4,271)
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
   
4. **Report**
   - List all duplicate pairs
   - Show similarity score
   - Suggest merge candidates

### 58.3 Implementation

**Tool:** `scripts/detect_code_duplication.py`

```python
# Usage
python scripts/detect_code_duplication.py <project_root>

# Output
docs/Code_Duplication_Report.md
```

**Report Format:**

```markdown
# Code Duplication Report

## Duplicate Pair 1 (Similarity: 95%)

### File 1: models/user.py
Function: `create_user()`

### File 2: models/user_unified.py  
Function: `add_user()`

### Recommendation
Merge into `models/user.py::create_user()`
Update all imports in dependent files
```

### 58.4 Workflow

**Before Creating New Function:**

1. Run duplicat
 59. Comprehensive Dependency Management
================================================================================

### 59.1 Principle

**ALWAYS** maintain a comprehensive dependency table.  
**NEVER** make changes without consulting the dependency table.

### 59.2 Dependency Table Generation

**Tool:** `scripts/analyze_dependencies.py`

```bash
# Generate dependency table
python scripts/analyze_dependencies.py <project_root>

# Output
docs/Dependency_Table.md
docs/Dependency_Graph.json
docs/Circular_Dependencies.md
docs/Orphan_Files.md
```

### 59.3 Dependency Table Format

| Module | Path | Imports From | Imported By | Dependency Level |
|--------|------|--------------|-------------|------------------|
| `base` | `/models/base.py` | - | `user`, `product` | 0 |
| `user` | `/models/user.py` | `base`, `auth` | `views.user_view` | 2 |

**Dependency Level:**
- **0:** Leaf node (no project imports)
- **1:** Imports only level-0 modules
- **2:** Imports level-0 and level-1 modules
- 
**N:** Maximum dependency level in import chain

### 59.4 Workflow

**At Project Start:**

1. Generate dependency table
2. Review dependency levels
3. Identify circular dependencies
4. Fix circular dependencies

**Before Refactoring:**

1. Consult dependency table
2. Identify all affected files
3. Plan refactoring strategy
4. Update dependency table after changes

**Module Development Order:**

1. Start with level-0 modules (least dependent)
2. Then level-1 modules
3. Continue in ascending order
4. This minimizes rework

### 59.5 Circular Dependency Detection

**Report Format:**

```markdown
# Circular Dependencies

## Cycle 1
```
models.user → models.auth → models.session → models.user
```

**Resolution:** Extract common code to `models.base`
```

**Resolution Strategies:**

1. **Extract Common Code:** Create a base module
2. **Lazy Import:** Import inside function
3. **Dependency Inversion:** Use interfaces/protocols
4. **Restructure:** Reorganize module boundaries

### 59.6 Orphan F
ile Detection

**Orphan Files:** Files not imported by any other file.

**Possible Reasons:**

1. Entry points (main.py, app.py)
2. Scripts (setup.py, manage.py)
3. Tests
4. **Dead code** ⚠️

**Action:**

- Review orphan files
- If dead code → delete
- If entry point → document
- If test → ensure it runs

### 59.7 Dependency Graph Visualization

```bash
# Generate visual graph (requires graphviz)
python scripts/visualize_dependencies.py docs/Dependency_Graph.json
```

### 59.8 CI/CD Integration

```yaml
- name: Analyze Dependencies
  run: |
    python scripts/analyze_dependencies.py .
    
- name: Check Circular Dependencies
  run: |
    if grep -q "Found.*circular" docs/Circular_Dependencies.md; then
      echo "⚠️ Circular dependencies detected!"
      cat docs/Circular_Dependencies.md
      exit 1
    fi
```

---

================================================================================
## 60. Intelligent Automatic Merging
=====================================================
`
   
   c. **Backup**
      ```
      Backing up:
      - models/user.py → backups/2025-01-15_user.py
      - models/user_unified.py → backups/2025-01-15_user_unified.py
      - All 5 dependent files
      ```
   
   d. **Merge**
      - Keep best implementation
      - Or merge features from both
      - Update docstrings
      - Update type hints
   
   e. **Update Imports**
      - Find all files importing from old location
      - Update to new location
      - Preserve import style
   
   f. **Run Tests**
      ```
      Running tests for affected modules...
      ✓ test_user.py::test_create_user
      ✓ test_api.py::test_user_endpoint
      ```
   
   g. **Commit or Rollback**
      - If tests pass → commit
      - If tests fail → rollback from backup

3. **Final Verification**
   - Run full test suite
   - Check code quality (flake8, mypy)
   - Generate new dependency table

### 60.4 Merge Strategies

**1. Keep Best Implementation**
- Choose implementation with:
  - Better docu
mentation
  - Better type hints
  - Better error handling
  - More features
  - Better tests

**2. Merge Features**
- Combine best parts from both
- Keep all functionality
- Resolve conflicts manually

**3. Deprecate Gradually**
- Keep both temporarily
- Mark old as deprecated
- Add migration guide
- Remove after grace period

### 60.5 Safety Measures

1. **Always Backup**
   - Backup all affected files
   - Keep backups for 30 days
   - Store in `backups/YYYY-MM-DD/`

2. **Always Test**
   - Run unit tests
   - Run integration tests
   - Check affected modules only (fast)
   - Then run full suite

3. **Always Rollback on Failure**
   - If any test fails → rollback
   - If syntax error → rollback
   - If import error → rollback
   - Restore from backup automatically

4. **Always Log**
   - Log all merge operations
   - Log all file changes
   - Log all test results
   - Store in `logs/merge_YYYY-MM-DD.log`

### 60.6 Post-Merge Checklist

- [ ] All tests pass
- [ ] No import errors
- [ 
] No syntax errors
- [ ] Code quality checks pass (flake8, mypy)
- [ ] Documentation updated
- [ ] Dependency table updated
- [ ] Changelog updated
- [ ] Git commit with descriptive message

### 60.7 CI/CD Integration

```yaml
- name: Smart Merge (Dry Run)
  run: |
    python scripts/smart_merge.py --dry-run --report
    
- name: Check Merge Suggestions
  run: |
    if [ -f merge_suggestions.md ]; then
      echo "📝 Merge suggestions available"
      cat merge_suggestions.md
    fi
```

---

================================================================================
## 61. Import Update Automation
================================================================================

### 61.1 Principle

**NEVER** update imports manually.  
**ALWAYS** use automated tools to update imports across all files.

### 61.2 Import Update Tool

**Tool:** `scripts/update_imports.py`

```bash
# Update imports after moving/renaming module
python scripts/update_imports.py <old_module> <new_module>

#
 Example
python scripts/update_imports.py models.user_unified models.user

# Dry-run
python scripts/update_imports.py models.user_unified models.user --dry-run
```

### 61.3 Supported Import Styles

**1. Direct Import**
```python
# Before
import models.user_unified

# After
import models.user
```

**2. From Import**
```python
# Before
from models.user_unified import create_user

# After
from models.user import create_user
```

**3. Aliased Import**
```python
# Before
import models.user_unified as user_module

# After
import models.user as user_module
```

**4. Multiple Imports**
```python
# Before
from models.user_unified import create_user, delete_user

# After
from models.user import create_user, delete_user
```

**5. Relative Imports**
```python
# Before (in models/views.py)
from .user_unified import create_user

# After
from .user import create_user
```

### 61.4 Workflow

1. **Find Affected Files**
   - Use dependency table
   - Find all files importing from old module
   
2. **Fo
r Each File:**
   
   a. **Parse Imports**
      - Use AST to parse imports
      - Identify matching imports
   
   b. **Update Imports**
      - Replace old module with new module
      - Preserve import style
      - Preserve aliases
   
   c. **Verify Syntax**
      - Parse updated file to AST
      - Check for syntax errors
   
   d. **Backup**
      - Backup original file
      - Write updated file

3. **Verify**
   - Run `python -m py_compile` on all updated files
   - Check for import errors
   - Run tests

### 61.5 Safety Measures

1. **Always Backup**
   - Backup before any change
   - Store in `backups/imports_YYYY-MM-DD/`

2. **Always Verify Syntax**
   - Parse to AST after update
   - If syntax error → rollback

3. **Always Test**
   - Run tests after update
   - If tests fail → rollback

4. **Always Log**
   - Log all file changes
   - Log all import updates
   - Store in `logs/import_update_YYYY-MM-DD.log`

### 61.6 Edge Cases

**1. Dynamic Imports**
```python
# Cannot b
Dependency table updated
- [ ] Documentation updated

---

================================================================================
## Summary of  Additions
================================================================================

### New Sections (58-61):

1. **Section 58:** AST-Based Code Duplication Detection
   - Semantic analysis instead of name-based
   - Similarity threshold ≥80%
   - CI/CD integration

2. **Section 59:** Comprehensive Dependency Management
   - Dependency table generation
   - Circular dependency detection
   - Orphan file identification
   - Module development order

3. **Section 60:** Intelligent Automatic Merging
   - Safe automated merging
   - Backup before changes
   - Update all dependent files
   - Rollback on failure

4. **Section 61:** Import Update Automation
   - Automatic import updates
   - Support all import styles
   - Syntax verification
   - Integration with smart merge

### Tools Added:

1. `scripts/analyze_dependencies.py
` - Dependency analysis
2. `scripts/detect_code_duplication.py` - AST-based duplication detection
3. `scripts/smart_merge.py` - Intelligent merging
4. `scripts/update_imports.py` - Import updates

### Benefits:

- **Eliminate Duplication:** AST-based detection finds hidden duplicates
- **Safe Refactoring:** Dependency table shows impact of changes
- **Automated Merging:** Smart merge reduces manual work
- **Zero Import Errors:** Automatic import updates prevent breakage

### Version: Latest
### Date: 2025-01-15
### Total Sections: 61
### Total Lines: ~7,700

# __init__.py Best Practices - دليل شامل لملفات __init__.py

**القسم المقترح للإضافة إلى GLOBAL_GUIDELINES**

================================================================================
## 62. __INIT__.PY PATTERNS & BEST PRACTICES
================================================================================

## Overview

ملف `__init__.py` هو القلب النابض لأي Python package. فهمه الصحيح واستخدامه بالطريقة المثلى يحدد جودة هيك
لة المشروع وسهولة استخدامه.

The `__init__.py` file is the beating heart of any Python package. Understanding and using it correctly determines the quality of project structure and ease of use.

---

## 1. الأنماط الأساسية / Basic Patterns

### Pattern 1: Empty __init__.py (Marker File)

**متى تستخدم / When to use:**
- Python 3.3+ namespace packages
- عندما لا تحتاج لتصدير أي شيء
- للحفاظ على backward compatibility

```python
# config/__init__.py
# Empty file - just marks directory as package
```

**الإيجابيات / Pros:**
✅ بسيط ونظيف
✅ لا يضيف overhead
✅ مناسب للـ namespace packages

**السلبيات / Cons:**
❌ لا يوفر واجهة واضحة للـ package
❌ المستخدمون يحتاجون معرفة البنية الداخلية

---

### Pattern 2: Explicit Imports (Recommended)

**متى تستخدم / When to use:**
- عندما تريد تحكم كامل في الصادرات
- للمشاريع المتوسطة والكبيرة
- عندما تريد تجنب namespace pollution

```python
# config/__init__.py
"""
File: config/__init__.py
Configuration package with explicit exports
"""

# Explicit import
s - clear and maintainable
from .settings import Settings, DatabaseConfig
from .constants import (
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    API_VERSION
)
from .validators import validate_config, ConfigError

# Explicit __all__ definition
__all__ = [
    # Settings
    'Settings',
    'DatabaseConfig',
    # Constants
    'DEFAULT_TIMEOUT',
    'MAX_RETRIES',
    'API_VERSION',
    # Validators
    'validate_config',
    'ConfigError',
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Your Team'
```

**الإيجابيات / Pros:**
✅ واضح وصريح - تعرف بالضبط ما يتم تصديره
✅ سهل الصيانة والتتبع
✅ يعمل بشكل ممتاز مع IDEs وtype checkers
✅ لا توجد مفاجآت في الـ namespace

**السلبيات / Cons:**
❌ يحتاج تحديث يدوي عند إضافة exports جديدة
❌ أطول قليلاً من star imports

**التوصية:** ⭐ **هذا هو النمط الموصى به للمشاريع الاحترافية**

---

### Pattern 3: Star Imports (Use with Caution)

**متى تستخدم / When to use:**
- للـ packages الصغيرة جداً
- عندما تريد re-export كل شيء من submodule
- عندما تكون
 متأكد من عدم وجود name conflicts

```python
# config/definitions/__init__.py
"""Central registry for all definitions"""

from .common import *
from .core import *
from .custom import *

# MUST define __all__ when using star imports
__all__ = [
    # From common
    'Status',
    'UserRole',
    'Environment',
    'APIResponse',
    'ErrorResponse',
    # From core
    'BaseModel',
    'TimestampMixin',
    'SoftDeleteMixin',
    'AuditMixin',
    # From custom
    'ProjectStatus',
    'Priority',
    'TaskType',
]
```

**الإيجابيات / Pros:**
✅ مختصر
✅ مناسب للـ central registries

**السلبيات / Cons:**
❌ يمكن أن يسبب namespace pollution
❌ صعب تتبع مصدر الـ imports
❌ يسبب مشاكل مع linters (F403, F405)
❌ يمكن أن يخفي name conflicts

**التوصية:** ⚠️ **استخدم فقط مع __all__ صريح ولـ packages محددة جداً**

---

### Pattern 4: Lazy Imports (Performance)

**متى تستخدم / When to use:**
- عندما يكون import time مهم
- للـ modules الثقيلة التي لا تُستخدم دائماً
- في command-line tools

```python

# tools/__init__.py
"""
Tools package with lazy imports for better performance
"""

from typing import TYPE_CHECKING

# Always imported (lightweight)
from .utils import get_version

# Type hints only (no runtime cost)
if TYPE_CHECKING:
    from .analyzer import CodeAnalyzer
    from .formatter import CodeFormatter

__version__ = '1.0.0'

__all__ = [
    'get_version',
    'get_analyzer',  # Lazy loaded
    'get_formatter',  # Lazy loaded
]


def get_analyzer():
    """Lazy import of CodeAnalyzer"""
    from .analyzer import CodeAnalyzer
    return CodeAnalyzer


def get_formatter():
    """Lazy import of CodeFormatter"""
    from .formatter import CodeFormatter
    return CodeFormatter
```

**الإيجابيات / Pros:**
✅ يحسن startup time بشكل كبير
✅ يقلل memory footprint
✅ مناسب للـ CLI tools

**السلبيات / Cons:**
❌ أكثر تعقيداً
❌ يمكن أن يخفي import errors حتى runtime

**التوصية:** 🎯 **استخدم للـ performance-critical applications**

---

## 2. أفضل الممارسات / Best Practices

### ✅ DO: است
خدم Docstrings

```python
# mypackage/__init__.py
"""
MyPackage - A comprehensive solution for X

This package provides:
- Feature A: Description
- Feature B: Description
- Feature C: Description

Usage:
    from mypackage import FeatureA
    
    feature = FeatureA()
    feature.do_something()

See documentation at: https://docs.example.com
"""
```

### ✅ DO: حدد __all__ بوضوح

```python
# Always define __all__ explicitly
__all__ = [
    'PublicClass',
    'public_function',
    'PUBLIC_CONSTANT',
]

# Private items (not in __all__)
_private_helper = "internal use only"
```

### ✅ DO: أضف Package Metadata

```python
# Package metadata
__version__ = '1.2.3'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025, Your Company'

# Useful for debugging
__all__ = [...]

# Make version easily accessible
from .version import __version__  # If in separate file
```

### ✅ DO: استخدم Absolute Imports عند الإمكان

```python
# Good - clea
r and explicit
from mypackage.submodule import MyClass

# Avoid - can be confusing
from .submodule import MyClass  # OK in __init__.py only
```

### ❌ DON'T: تضع Logic معقد في __init__.py

```python
# ❌ BAD - complex initialization
def _initialize_database():
    # 50 lines of database setup
    pass

_initialize_database()  # Runs on import!

# ✅ GOOD - defer to explicit initialization
def initialize():
    """Call this explicitly when needed"""
    # Setup code here
    pass
```

### ❌ DON'T: تستورد كل شيء

```python
# ❌ BAD - imports everything
from .module1 import *
from .module2 import *
from .module3 import *
# No __all__ defined!

# ✅ GOOD - selective imports
from .module1 import ClassA, function_a
from .module2 import ClassB
from .module3 import CONSTANT_C

__all__ = ['ClassA', 'function_a', 'ClassB', 'CONSTANT_C']
```

---

## 3. أنماط متقدمة / Advanced Patterns

### Pattern 5: Subpackage Organization

```python
# myapp/__init__.py
"""
MyApp - Main application package

Subpack
   'TypeAlias',
    'PlatformSpecific',
]
```

### Pattern 8: Deprecation Warnings

```python
# oldpackage/__init__.py
"""
Old package - deprecated, use newpackage instead
"""

import warnings

# Deprecation warning
warnings.warn(
    "oldpackage is deprecated and will be removed in version 2.0. "
    "Use newpackage instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from newpackage import *  # noqa: F401, F403

__all__ = ['OldClass', 'old_function']
```

---

## 4. حل المشاكل الشائعة / Common Problems & Solutions

### Problem 1: Circular Imports

```python
# ❌ PROBLEM: Circular dependency
# models/__init__.py
from .user import User
from .post import Post  # Post imports User, User imports Post!

# ✅ SOLUTION 1: Import at function level
# models/user.py
def get_user_posts(user_id):
    from .post import Post  # Import here, not at module level
    return Post.query.filter_by(user_id=user_id).all()

# ✅ SOLUTION 2: Use TYPE_CHECKING
# models/user.py
fro
ersion__ = '0.1.0'
__all__ = ['run_app', 'Config', 'helper_function']
```

### Medium Project (10-50 modules)

```python
# myapp/__init__.py
"""
MyApp - Medium-sized application

Organized into logical subpackages with clear public API.
"""

# Core functionality
from .core import (
    App,
    Config,
    initialize,
)

# Models
from .models import (
    User,
    Session,
    Database,
)

# Services (most commonly used)
from .services import (
    UserService,
    AuthService,
)

# Version
from ._version import __version__, __version_info__

# Public API
__all__ = [
    # Core
    'App',
    'Config',
    'initialize',
    # Models
    'User',
    'Session',
    'Database',
    # Services
    'UserService',
    'AuthService',
    # Version
    '__version__',
    '__version_info__',
]

# Note: For other services, use:
# from myapp.services import SpecificService
```

### Large Project (50+ modules)

```python
# enterprise_app/__init__.py
"""
Enterprise Application

Large-scale applica
tion with multiple subpackages.
Import subpackages explicitly for better organization.

Usage:
    # Import main app
    from enterprise_app import App
    
    # Import specific modules
    from enterprise_app.core import Config
    from enterprise_app.models import User
    from enterprise_app.services.auth import AuthService
"""

# Only expose the absolute essentials at top level
from .core import App
from ._version import __version__

# Make subpackages easily accessible
from . import (
    core,
    models,
    services,
    api,
    utils,
    exceptions,
)

# Minimal public API at package level
__all__ = [
    'App',
    '__version__',
    # Subpackages
    'core',
    'models',
    'services',
    'api',
    'utils',
    'exceptions',
]

# Package metadata
__author__ = 'Enterprise Team'
__license__ = 'Proprietary'
__copyright__ = 'Copyright 2025, Enterprise Corp'
```

---

## 6. Testing __init__.py

```python
# tests/test_package_init.py
"""Test package __init__.py structure"""
   import sys
    import importlib
    
    # Remove module if already imported
    if 'mypackage' in sys.modules:
        del sys.modules['mypackage']
    
    # Import should not raise or print anything
    import mypackage  # noqa: F401
```

---

## 7. Checklist للمراجعة / Review Checklist

عند مراجعة ملف `__init__.py`، تأكد من:

### Structure
- [ ] يحتوي على docstring واضح
- [ ] الـ imports منظمة (stdlib → third-party → local)
- [ ] `__all__` محدد بوضوح
- [ ] Package metadata موجود (`__version__`, etc.)

### Imports
- [ ] لا توجد star imports بدون `__all__`
- [ ] لا توجد circular imports
- [ ] الـ imports ضرورية فقط (لا unused imports)
- [ ] استخدام explicit imports بدلاً من star imports

### Performance
- [ ] لا يوجد initialization code ثقيل
- [ ] استخدام lazy imports للـ modules الثقيلة
- [ ] لا يتم import modules غير ضرورية

### Maintainability
- [ ] الـ public API واضح ومحدود
- [ ] الـ private items تبدأ بـ underscore
- [ ] التعليقات توضح القرارات المهمة
- [ ] سهل إضافة exports
n code
- قلل الـ dependencies

### 🎯 Rule 5: Maintain Backwards Compatibility
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
- Ready-made templates
- Integration scripts
- Workflow documentation

**Repository URL:** https://github.com/hamfarid/global

---

## Repository Structure / بنية المستودع

```
global/
├── GLOBAL_GUIDELINES_.txt          # البرومبت الرئيسي (هذا الملف)
├── GLOBAL_GUIDELINES_FINAL.txt         # نسخة نهائية
├── VERSION                              # الإصدار الحالي
│
├── tools/                               # أدوات التطوير ⚙️
│   ├── analyze_dependencies.py          # تحليل الاعتماديات
│   ├── detect_code_duplication.py       # كشف التكرار
│   ├── smart_merge.py                   # دمج ذكي
│   ├── update_imports.py                # تحديث الاستيرادات
│   └── README.md                        # دليل الأدوات
│
├── templates/                           # القوالب 📋
│   └── config/
│       ├── ports.py                     # Ports
T_FLOW.md              # سير عمل التطوير
│   ├── INTEGRATION_FLOW.md              # سير عمل الدمج
│   ├── DEPLOYMENT_FLOW.md               # سير عمل النشر
│   └── README.md                        # دليل Flows
│
└── docs/                                # الوثائق 📖
    ├── INIT_PY_BEST_PRACTICES.md        # أفضل ممارسات __init__.py
    ├── OSF_FRAMEWORK.md                 # إطار OSF
    ├── QUICK_START.md                   # البدء السريع
    └── CHANGELOG.md                     # سجل التغييرات
```

---

## 1. Tools / الأدوات ⚙️

### 1.1 analyze_dependencies.py

**الوظيفة:** تحليل شامل للاعتماديات في المشروع

**الاستخدام:**
```bash
python tools/analyze_dependencies.py /path/to/project
```

**الميزات:**
- ✅ اكتشاف الاعتماديات المباشرة وغير المباشرة
- ✅ كشف الاعتماديات الدائرية (Circular Dependencies)
- ✅ تحليل عمق الاعتماديات
- ✅ إنشاء رسم بياني للاعتماديات
- ✅ تقرير مفصل بالمشاكل

**مثال الإخراج:**
```
=== Dependency Analysis Report ===

Total modules analyzed: 45
Direct dependencies: 123

Indirect dependencies: 67

⚠️ Circular Dependencies Found:
  - module_a → module_b → module_c → module_a
  - service_x → service_y → service_x

Recommendations:
  1. Break circular dependency between module_a and module_c
  2. Consider using dependency injection for service_x
```

**الخيارات:**
```bash
# تحليل مع رسم بياني
python tools/analyze_dependencies.py . --graph deps.png

# تحليل مع تقرير JSON
python tools/analyze_dependencies.py . --format json > report.json

# تحليل مع عمق محدد
python tools/analyze_dependencies.py . --max-depth 3
```

---

### 1.2 detect_code_duplication.py

**الوظيفة:** كشف التكرار في الكود

**الاستخدام:**
```bash
python tools/detect_code_duplication.py /path/to/project
```

**الميزات:**
- ✅ كشف الكود المكرر (>= 5 أسطر)
- ✅ حساب نسبة التشابه
- ✅ تحديد الملفات والأسطر المكررة
- ✅ اقتراحات للدمج
- ✅ تقرير مفصل

**مثال الإخراج:**
```
=== Code Duplication Report ===

Total files scanned: 45
Duplications found: 12
Average similarity: 87%

Duplication #1 (95% simi
te_imports.py

**الوظيفة:** تحديث الاستيرادات تلقائياً عند إعادة التسمية

**الاستخدام:**
```bash
python tools/update_imports.py old_module new_module /path/to/project
```

**الميزات:**
- ✅ تحديث جميع الاستيرادات تلقائياً
- ✅ دعم الاستيرادات المختلفة (from, import, as)
- ✅ تحديث docstrings
- ✅ نسخ احتياطي قبل التحديث
- ✅ تقرير مفصل بالتغييرات

**أمثلة:**
```bash
# تحديث اسم module
python tools/update_imports.py old_auth new_auth .

# تحديث اسم package
python tools/update_imports.py src.old_pkg src.new_pkg .

# تحديث مع نسخ احتياطي
python tools/update_imports.py old new . --backup
```

**مثال الإخراج:**
```
=== Import Update Report ===

Files scanned: 45
Files updated: 12
Imports updated: 34

Updated files:
  ✅ src/services/user_service.py (3 imports)
  ✅ src/api/routes.py (5 imports)
  ✅ src/models/user.py (2 imports)
  ...

Backup created at: .backup_20251102_120000/
```

**التحديثات المدعومة:**
```python
# Before
from old_module import func
import old_module
import old_module as om
fr
om old_module.sub import Class

# After
from new_module import func
import new_module
import new_module as om
from new_module.sub import Class
```

---

## 2. Templates / القوالب 📋

### 2.1 config/ports.py

**الوصف:** نمط Ports & Adapters (Hexagonal Architecture)

**الاستخدام:**
```python
from config.ports import (
    UserRepositoryPort,
    EmailServicePort,
    PaymentGatewayPort
)

# Implement adapters
class PostgresUserRepository(UserRepositoryPort):
    def get_user(self, user_id: int) -> User:
        # Implementation
        pass
```

**الميزات:**
- ✅ فصل المنطق عن التفاصيل
- ✅ سهولة الاختبار (Mocking)
- ✅ قابلية التبديل (Swappable implementations)

---

### 2.2 config/definitions/

#### common.py
**التعريفات العامة المشتركة:**
```python
from config.definitions import (
    Status,           # ACTIVE, INACTIVE, PENDING, DELETED
    UserRole,         # ADMIN, USER, GUEST, MODERATOR
    Environment,      # DEV, STAGING, PROD
    APIResponse,      # استجابة API موحدة
    ErrorResp
- ✅ استخدام config/definitions
- ✅ Ports & Adapters pattern
- ✅ Error handling موحد
- ✅ Logging شامل
- ✅ Tests كاملة

---

### 3.2 code-samples/

**الوصف:** عينات كود لأنماط شائعة

**الأمثلة المتوفرة:**
- `log_activity_example.py` - تسجيل النشاطات
- `error_handling_example.py` - معالجة الأخطاء
- `async_example.py` - البرمجة غير المتزامنة
- `database_example.py` - عمليات قاعدة البيانات

---

### 3.3 init_py_patterns/

**الوصف:** 3 أنماط كاملة لملفات `__init__.py`

#### Pattern 1: Central Registry
```python
# من 01_central_registry/__init__.py
from .status_types import Status, UserRole
from .response_types import APIResponse, ErrorResponse
from .model_mixins import TimestampMixin, AuditMixin

__all__ = [
    'Status', 'UserRole',
    'APIResponse', 'ErrorResponse',
    'TimestampMixin', 'AuditMixin'
]
```

#### Pattern 2: Lazy Loading
```python
# من 02_lazy_loading/__init__.py
def __getattr__(name):
    if name == 'Analyzer':
        from .analyzer import Analyzer
        return Analyzer
نشر
- Docker & Kubernetes
- CI/CD pipelines
- Monitoring & Rollback

---

## 6. How to Use in Augment / كيفية الاستخدام في Augment

### الطريقة الموصى بها:

```bash
# 1. نسخ البرومبت إلى Augment
cp GLOBAL_GUIDELINES_.txt /path/to/augment/prompts/

# 2. نسخ الأدوات
cp -r tools/ /path/to/augment/tools/

# 3. نسخ الأمثلة
cp -r examples/ /path/to/augment/examples/

# 4. نسخ Templates
cp -r templates/ /path/to/augment/templates/

# 5. في Augment، أشر إلى:
# - البرومبت: prompts/GLOBAL_GUIDELINES_.txt
# - الأدوات: tools/
# - الأمثلة: examples/
```

### في Augment Configuration:

```yaml
# augment.yml
prompts:
  - path: prompts/GLOBAL_GUIDELINES_.txt
    name: "Global Guidelines"
    version: "3.7.0"

tools:
  - path: tools/analyze_dependencies.py
    name: "Dependency Analyzer"
  - path: tools/detect_code_duplication.py
    name: "Duplication Detector"
  - path: tools/smart_merge.py
    name: "Smart Merge"
  - path: tools/update_imports.py
    name: "Import Updater"

examples:
  -
 path: examples/simple-api/
  - path: examples/code-samples/
  - path: examples/init_py_patterns/

templates:
  - path: templates/config/
```

---

## 7. Best Practices / أفضل الممارسات

### عند استخدام الأدوات:

1. **analyze_dependencies.py**
   - شغله دورياً (أسبوعياً)
   - راقب الاعتماديات الدائرية
   - احفظ التقارير للمقارنة

2. **detect_code_duplication.py**
   - شغله قبل كل merge
   - استهدف < 5% تكرار
   - استخدم الاقتراحات للدمج

3. **smart_merge.py**
   - استخدم dry-run أولاً
   - احفظ نسخة احتياطية دائماً
   - راجع التعارضات يدوياً

4. **update_imports.py**
   - اختبر في branch منفصل
   - راجع التغييرات قبل commit
   - احفظ نسخة احتياطية

---

### عند استخدام Templates:

1. **لا تعدل Templates مباشرة**
   - انسخها لمشروعك أولاً
   - عدل النسخة في مشروعك

2. **حافظ على التحديثات**
   - راجع templates عند التحديث
   - دمج التحسينات الجديدة

---

### عند استخدام Examples:

1. **استخدمها كمرجع**
   - لا تنسخها كما هي
   - افهم المفاهيم وطبقها

2. **تعلم من الأنماط**
   - كل مثال 
st** if no config exists
2. **Use config values** throughout the project
3. **Respect project phase** in all operations
4. **Never hardcode** project-specific values
5. **Backup before** destructive operations
6. **Verify** before production deployment
7. **Log** all important operations
8. **Notify user** of phase transitions

**For Users:**

1. **Answer questions carefully** - they affect the entire project
2. **Review config** before deployment
3. **Backup** before `start deploy`
4. **Test thoroughly** in development
5. **Use staging** if available
6. **Monitor** after deployment
7. **Keep credentials** secure

---

### 64.13 Integration with Existing Sections

**This section integrates with:**

- **Section 0-3:** Core directives and constraints
- **Section 40:** Definitions Registry (uses config)
- **Section 63:** Global Repository (tools use config)
- **All sections:** Use config values instead of hardcoded

**Example Integration:**

```python
# Section 40: Definitions Registry
# 
Before:
APP_NAME = "Gaara ERP"

# After:
from .global.project_config import load_config
config = load_config()
APP_NAME = config['project']['name']
```

---

### 64.14 Summary

**This section provides:**

✅ Interactive project setup questionnaire  
✅ Configuration file management  
✅ State management (Development/Production)  
✅ `start deploy` command workflow  
✅ Admin panel auto-open  
✅ Setup wizard integration  
✅ Phase-specific behavior  
✅ Best practices for Augment and users

**Result:**

- No more hardcoded values
- Project-specific configuration
- Smooth development-to-production transition
- Automated deployment process
- Professional setup experience

---

**End of Section 64**



================================================================================
# Section 65: Automatic Project Analysis

## Overview

When working with **existing projects**, Augment should automatically analyze the project structure, detect technologies, and generate project-specific configurati

================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```bash
# تأكد من Python version
python --version  # يجب أن يكون >= 3.8

# ثبت المتطلبات
pip install -r requirements.txt

# شغل مع verbose
python tools/analyze_dependencies.py . --verbose
```

```python
# scripts/generate_imports_map.py
import ast
import os
from pathlib import Path
from typing import Dict, List, Set

def analyze_python_imports(file_path: str) -> Dict:
    """Analyze imports in a Python file"""
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'module': alias.name,
                    'alias': alias.asname,
                    'type': 'import'
                })
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append({
                    'module': node.module,
                    'name': alias.name,
                    'alias': alias.asname,
                    'type': 'from'
                })
    
    return imports

def find_circular_dependencies(import_graph: Dict) -> List:
    """Detect circular dependencies"""
    # Implementation using DFS
    pass

def generate_imports_map(root_dir: str):
    """Generate complete imports map"""
    # Scan all Python files
    # Analyze imports
    # Detect circular dependencies
    # Generate markdown report
    pass

if __name__ == '__main__':
    generate_imports_map('./backend')
    generate_imports_map('./frontend')
```

```python
# scripts/detect_duplicates.py
import ast
import difflib
from pathlib import Path
from typing import List, Dict

class DuplicateDetector:
    def __init__(self, threshold=0.8):
        self.threshold = threshold  # Similarity threshold
    
    def get_function_signature(self, func_node: ast.FunctionDef) -> str:
        """Extract normalized function signature"""
        args = [arg.arg for arg in func_node.args.args]
        return f"{func_node.name}({', '.join(args)})"
    
    def get_class_signature(self, class_node: ast.ClassDef) -> str:
        """Extract class signature"""
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)
        return f"{class_node.name}: {', '.join(sorted(methods))}"
    
    def normalize_code(self, code: str) -> str:
        """Normalize code for comparison"""
        # Remove comments, whitespace, docstrings
        tree = ast.parse(code)
        return ast.unparse(tree)
    
    def find_similar_files(self, dir_path: str) -> List[Dict]:
    # ... (code truncated for brevity) ...
    # See full example in examples/ directory
    
    if file_duplicates or func_duplicates:
        return 1  # Exit with error
    else:
        print("✅ No duplicates found!")
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
```

```python
# scripts/pre_dev_check.py
import sys
from validate_env import validate_env
from pathlib import Path

def pre_development_check():
    """Run all pre-development checks"""
    errors = []
    
    # 1. Check .env
    print("1. Checking environment...")
    env_result = validate_env()
    if not env_result['valid']:
        errors.extend(env_result['errors'])
    
    # 2. Check documentation exists
    print("2. Checking documentation...")
    required_docs = [
        'docs/File_Map.md',
        'docs/Class_Registry.md',
        'docs/Imports_Map.md',
        'docs/TODO.md',
    ]
    for doc in required_docs:
        if not Path(doc).exists():
            errors.append(f"❌ Missing required documentation: {doc}")
    
    # 3. Check for uncommitted changes
    print("3. Checking git status...")
    import subprocess
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True)
    if result.stdout:
        errors.append("⚠️ You have uncommitted changes. Commit or stash them first.")
    
    # Summary
    if errors:
        print("\n❌ Pre-development checks failed:")
        for error in errors:
            print(f"  {error}")
        print("\nPlease fix the issues above before starting development.")
        return 1
    else:
        print("\n✅ All pre-development checks passed!")
        print("You're ready to start coding.")
        return 0

if __name__ == '__main__':
    sys.exit(pre_development_check())
```

```python
"""
File: scripts/document_imports.py
Generate import/export documentation
"""

import ast
import os
from pathlib import Path
from collections import defaultdict

def analyze_file(filepath: Path) -> dict:
    """Analyze Python file for imports and exports"""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except:
            return {}
    
    imports = []
    exports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")
        
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__all__':
                    if isinstance(node.value, ast.List):
                        exports = [
                            elt.s for elt in node.value.elts
                            if isinstance(elt, ast.Str)
                        ]
    
    return {
        'imports': imports,
        'exports': exports
    }

def generate_documentation(root_dir: str, output_file: str):
    """Generate import/export documentation"""
    
    modules = {}
    
    for filepath in Path(root_dir).rglob('*.py'):
        if 'venv' in str(filepath) or '.venv' in str(filepath):
            continue
        
        rel_path = filepath.relative_to(root_dir)
        analysis = analyze_file(filepath)
        
        if analysis:
            modules[str(rel_path)] = analysis
    
    # Write documentation
    with open(output_file, 'w') as f:
        f.write("# Import/Export Documentation\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        for module, data in sorted(modules.items()):
            f.write(f"## {module}\n\n")
            
            if data.get('exports'):
                f.write("### Exports\n")
                for exp in data['exports']:
                    f.write(f"- `{exp}`\n")
                f.write("\n")
            
            if data.get('imports'):
                f.write("### Imports\n")
                for imp in data['imports']:
                    f.write(f"- `{imp}`\n")
                f.write("\n")
            
            f.write("---\n\n")

if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "docs/Imports_Exports.md"
    
    generate_documentation(root, output)
    print(f"✅ Documentation generated: {output}")
```

```python
#!/usr/bin/env python3
"""Generate comprehensive module map."""

import ast
from pathlib import Path
from collections import defaultdict

def analyze_module(file_path):
    """Analyze a Python module."""
    with open(file_path) as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return None
    
    info = {
        'classes': [],
        'functions': [],
        'imports': [],
        'dependencies': set()
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            info['classes'].append(node.name)
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                info['functions'].append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module:
                info['dependencies'].add(node.module.split('.')[0])
    
    return info

def generate_map():
    """Generate module map."""
    modules = defaultdict(dict)
    
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' in str(py_file) or 'venv' in str(py_file):
            continue
        
        info = analyze_module(py_file)
        if info:
            modules[str(py_file)] = info
    
    # Write to markdown
    with open('docs/Module_Map.md', 'w') as f:
        f.write("# Module Map\n\n")
        f.write("**Generated:** Auto-generated\n\n")
        f.write("## Modules by Directory\n\n")
        
        # Group by directory
        by_dir = defaultdict(list)
        for path in sorted(modules.keys()):
            dir_name = str(Path(path).parent)
            by_dir[dir_name].append(path)
        
        for dir_name in sorted(by_dir.keys()):
            f.write(f"### `{dir_name}/`\n\n")
            for path in sorted(by_dir[dir_name]):
                info = modules[path]
                f.write(f"#### `{Path(path).name}`\n\n")
                
                if info['classes']:
                    f.write("**Classes:**\n")
                    for cls in info['classes']:
                        f.write(f"- `{cls}`\n")
                    f.write("\n")
                
                if info['functions']:
                    f.write("**Functions:**\n")
                    for func in info['functions']:
                        f.write(f"- `{func}()`\n")
                    f.write("\n")
                
                if info['dependencies']:
                    f.write("**Dependencies:**\n")
                    for dep in sorted(info['dependencies']):
                        f.write(f"- `{dep}`\n")
                    f.write("\n")
        
        # Dependency graph
        f.write("## Dependency Graph\n\n")
        f.write("```mermaid\n")
        f.write("graph TD\n")
        for path, info in modules.items():
            module_name = Path(path).stem
            for dep in info['dependencies']:
                f.write(f"  {module_name} --> {dep}\n")
        f.write("```\n")

if __name__ == '__main__':
    generate_map()
    print("✅ Module map generated: docs/Module_Map.md")
```

```python
#!/usr/bin/env python3
"""Suggest refactoring for large files/functions."""

import ast
from pathlib import Path

def analyze_file(file_path):
    """Analyze file for refactoring opportunities."""
    with open(file_path) as f:
        content = f.read()
        lines = content.split('\n')
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return None
    
    issues = []
    
    # Check file length
    if len(lines) > 500:
        issues.append(f"File too long: {len(lines)} lines (max 500)")
    
    # Check function lengths
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_lines = node.end_lineno - node.lineno
            if func_lines > 50:
                issues.append(
                    f"Function '{node.name}' too long: {func_lines} lines (max 50)"
                )
        
        elif isinstance(node, ast.ClassDef):
            class_lines = node.end_lineno - node.lineno
            if class_lines > 300:
                issues.append(
                    f"Class '{node.name}' too long: {class_lines} lines (max 300)"
                )
    
    return issues

def main():
    """Check all Python files."""
    all_issues = {}
    
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        issues = analyze_file(py_file)
        if issues:
            all_issues[str(py_file)] = issues
    
    if all_issues:
        print("🔧 Refactoring Suggestions:\n")
        for file_path, issues in all_issues.items():
            print(f"📄 {file_path}")
            for issue in issues:
                print(f"   ⚠️  {issue}")
            print()
        
        print(f"Total files needing refactoring: {len(all_issues)}")
    else:
        print("✅ All files are well-modularized!")

if __name__ == '__main__':
    main()
```

```python
# Good - clear and explicit
from mypackage.submodule import MyClass

# Avoid - can be confusing
from .submodule import MyClass  # OK in __init__.py only
```

```python
# plugins/__init__.py
"""
Plugin system with dynamic discovery
"""

import importlib
import pkgutil
from typing import Dict, Type

# Plugin registry
_plugins: Dict[str, Type] = {}


def discover_plugins():
    """Automatically discover and register plugins"""
    package = __package__
    for _, name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
        module = importlib.import_module(f'{package}.{name}')
        if hasattr(module, 'register_plugin'):
            plugin = module.register_plugin()
            _plugins[plugin.name] = plugin


def get_plugin(name: str):
    """Get plugin by name"""
    if not _plugins:
        discover_plugins()
    return _plugins.get(name)


__all__ = [
    'discover_plugins',
    'get_plugin',
]
```

```python
# compat/__init__.py
"""
Compatibility layer for different Python versions
"""

import sys

# Version-specific imports
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

# Platform-specific imports
if sys.platform == 'win32':
    from .windows import WindowsSpecific as PlatformSpecific
else:
    from .unix import UnixSpecific as PlatformSpecific

__all__ = [
    'TypeAlias',
    'PlatformSpecific',
]
```

```python
# mysmallapp/__init__.py
"""Small application - simple structure"""

from .main import run_app
from .config import Config
from .utils import helper_function

__version__ = '0.1.0'
__all__ = ['run_app', 'Config', 'helper_function']
```

```python
#!/usr/bin/env python3
"""
Script: check_init_py.py
Check __init__.py files for common issues
"""

import ast
import sys
from pathlib import Path


def check_init_file(filepath: Path) -> list[str]:
    """Check __init__.py for issues"""
    issues = []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [f"Syntax error: {e}"]
    
    # Check for docstring
    if not ast.get_docstring(tree):
        issues.append("Missing module docstring")
    
    # Check for __all__
    has_all = any(
        isinstance(node, ast.Assign) and
        any(isinstance(t, ast.Name) and t.id == '__all__' for t in node.targets)
        for node in tree.body
    )
    
    # Check for star imports
    has_star_import = any(
        isinstance(node, ast.ImportFrom) and
        any(isinstance(alias, ast.alias) and alias.name == '*' for alias in node.names)
        for node in tree.body
    )
    
    if has_star_import and not has_all:
        issues.append("Star import without __all__ definition")
    
    # Check for heavy initialization
    function_calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    ]
    
    if len(function_calls) > 5:
        issues.append(f"Many function calls ({len(function_calls)}) - possible heavy initialization")
    
    return issues


def main():
    """Check all __init__.py files in project"""
    project_root = Path.cwd()
    init_files = list(project_root.rglob('__init__.py'))
    
    print(f"Checking {len(init_files)} __init__.py files...\n")
    
    total_issues = 0
    for init_file in init_files:
        issues = check_init_file(init_file)
        if issues:
            print(f"❌ {init_file.relative_to(project_root)}")
            for issue in issues:
                print(f"   - {issue}")
            print()
            total_issues += len(issues)
    
    if total_issues == 0:
        print("✅ All __init__.py files look good!")
    else:
        print(f"Found {total_issues} issues in {len(init_files)} files")
        sys.exit(1)


if __name__ == '__main__':
    main()
```

```python
# Before
from old_module import func
import old_module
import old_module as om
from old_module.sub import Class

# After
from new_module import func
import new_module
import new_module as om
from new_module.sub import Class
```

```python
# من 02_lazy_loading/__init__.py
def __getattr__(name):
    if name == 'Analyzer':
        from .analyzer import Analyzer
        return Analyzer
    raise AttributeError(f"module has no attribute '{name}'")
```

```python
# Section 40: Definitions Registry
# Before:
APP_NAME = "Gaara ERP"

# After:
from .global.project_config import load_config
config = load_config()
APP_NAME = config['project']['name']
```

