# Import/Export Map

> **Purpose:** Track all imports and exports across the project to understand dependencies and prevent circular imports.

**Last Updated:** [DATE]  
**Project:** Store Management System

---

## How to Use This File

1. **When creating a new file:** Document its exports
2. **When importing:** Check this map to avoid circular dependencies
3. **When refactoring:** Update this map to reflect changes
4. **Before committing:** Verify this map is up to date

---

## Import Rules

### ✅ Allowed Imports

**API Layer can import:**
- Services
- Utils
- Models (for type hints only)

**Services Layer can import:**
- Models
- Database
- Utils (validators, helpers - NOT decorators)

**Models Layer can import:**
- Database only

**Utils Layer can import:**
- Services (only for decorators)
- Nothing else (validators and helpers are leaf modules)

### ❌ Forbidden Imports

**Models CANNOT import:**
- Services, API, Utils (except database)

**Services CANNOT import:**
- API, Utils/decorators

**Utils/validators CANNOT import:**
- Anything internal

---

## Core Files

### Backend Entry Point
**File:** `backend/app.py`  
**Purpose:** Main Flask application entry point

**Exports:**
- `app` (Flask) - Main Flask application instance
- `create_app()` (function) - Application factory

**Imports:**
```python
from flask import Flask
from src.config import Config
from src.database import db
from src.routes import register_blueprints
```

**Imported By:**
- run.py
- tests/conftest.py

---

## Module Template

### Example Module
**File:** `src/module/file.py`  
**Purpose:** Description

**Exports:**
- `ClassName` (class) - Description
- `function_name()` (function) - Description

**Imports:**
```python
from src.dependency import Something
```

**Dependencies:**
- src/dependency.py

**Imported By:**
- src/consumer.py

---

## Circular Dependency Risks

### ⚠️ Risk: Decorators ↔ Services
**Problem:** decorators.py imports AuthService
**Solution:** Services should NOT import decorators
**Status:** ✅ Safe (services don't import decorators)

---

## Dependency Graph

```
app.py
├── config.py (leaf)
├── database.py (leaf)
└── routes/
    └── services/
        └── models/
            └── database.py
```

---

## Import Best Practices

1. **Import from package __init__.py when possible**
2. **Use absolute imports, not relative**
3. **Import only what you need**
4. **Group imports logically** (standard, third-party, local)
5. **Check this map before adding new imports**

---

## Update Checklist

When adding a new file:
- [ ] Document its exports
- [ ] Document its imports
- [ ] Document its dependencies
- [ ] Check for circular dependencies
- [ ] Update dependency graph
