# Class Registry - Complete Reference (Global System v26 Diamond 32)

> **Purpose:** Complete registry of all classes, functions, and their purposes across the project.
> **Automation:** `speckit.py analyze` automatically updates this file.

**Last Updated:** [DATE]  
**Project:** {{PROJECT_NAME}}

---

## How to Use This File

1. **When creating a class/function:** Add it to this registry.
2. **When looking for functionality:** Search this file first.
3. **Speckit Integration:** The `code_indexer.py` tool generates this file.

---

## Quick Index

- [Models](#models) - Database models
- [Services](#services) - Business logic
- [API](#api) - API endpoints
- [Utils](#utils) - Utility functions

---

## Models

### User Model
**File:** `src/models/user.py`  
**Class:** `User`  
**Purpose:** User account and authentication.

**Attributes:**
- `id` (Integer) - Primary key
- `email` (String) - Unique email address
- `password_hash` (String) - Hashed password

**Methods:**
```python
set_password(password: str) -> None
    """Hash and set user password"""
    
check_password(password: str) -> bool
    """Verify password against hash"""
```

---

## Services

### AuthService
**File:** `src/services/auth_service.py`  
**Class:** `AuthService`  
**Purpose:** Authentication and token management.

**Methods:**
```python
register(email: str, password: str, name: str) -> User
    """Register new user"""

login(email: str, password: str) -> dict
    """Authenticate user and generate tokens"""
```
