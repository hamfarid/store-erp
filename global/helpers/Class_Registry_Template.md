# Class Registry - Complete Reference

> **Purpose:** Complete registry of all classes, functions, and their purposes across the project.

**Last Updated:** [DATE]  
**Project:** Store Management System

---

## How to Use This File

1. **When creating a class/function:** Add it to this registry
2. **When looking for functionality:** Search this file first
3. **When refactoring:** Update this registry
4. **Before implementing:** Check if functionality already exists

---

## Quick Index

- [Models](#models) - Database models
- [Services](#services) - Business logic
- [API](#api) - API endpoints
- [Utils](#utils) - Utility functions
- [Middleware](#middleware) - Custom middleware
- [Decorators](#decorators) - Custom decorators

---

## Models

### Model Template
**File:** `src/models/example.py`  
**Class:** `ExampleModel`  
**Purpose:** Description of what this model represents

**Attributes:**
- `id` (Integer) - Primary key
- `name` (String) - Name field
- `created_at` (DateTime) - Creation timestamp

**Relationships:**
- `related_items` (One-to-Many) - Related items

**Methods:**
```python
to_dict() -> dict
    """Convert to dictionary"""
    
from_dict(data: dict) -> Model
    """Create from dictionary"""
```

**Usage Example:**
```python
from src.models import ExampleModel

model = ExampleModel(name="Example")
model_dict = model.to_dict()
```

---

## Services

### Service Template
**File:** `src/services/example_service.py`  
**Class:** `ExampleService`  
**Purpose:** Business logic for example operations

**Methods:**
```python
get_all(page: int = 1, per_page: int = 20) -> dict
    """Get paginated list of items"""

get_by_id(item_id: int) -> Model
    """Get item by ID"""

create(data: dict) -> Model
    """Create new item"""

update(item_id: int, data: dict) -> Model
    """Update item"""

delete(item_id: int) -> None
    """Delete item"""
```

---

## Utils

### Validators
**File:** `src/utils/validators.py`

**Functions:**
```python
validate_data(data: dict) -> None
    """Validate input data, raise ValueError if invalid"""

validate_email(email: str) -> bool
    """Validate email format"""

validate_password(password: str) -> bool
    """Validate password strength"""
```

### Helpers
**File:** `src/utils/helpers.py`

**Functions:**
```python
format_response(data: any, message: str = "", status: int = 200) -> tuple
    """Format API response"""

handle_error(error: Exception) -> tuple
    """Handle and format error response"""

paginate(query: Query, page: int, per_page: int) -> dict
    """Paginate SQLAlchemy query"""
```

---

## Decorators

**File:** `src/utils/decorators.py`

**Decorators:**
```python
@token_required
    """Require valid JWT token"""

@admin_required
    """Require admin role"""

@rate_limit(limit=100, per=60)
    """Rate limiting decorator"""
```

---

## Statistics

**Total Classes:** [COUNT]
**Total Functions:** [COUNT]
**Total Decorators:** [COUNT]

---

## Update Checklist

When adding new class/function:
- [ ] Add to this registry
- [ ] Document purpose
- [ ] Document parameters and returns
- [ ] Add usage example
- [ ] Update statistics
