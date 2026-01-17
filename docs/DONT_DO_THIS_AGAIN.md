# FILE: docs/DONT_DO_THIS_AGAIN.md | PURPOSE: Lessons learned and anti-patterns to avoid | OWNER: All Teams | RELATED: docs/Status_Report.md | LAST-AUDITED: 2025-10-25

# Don't Do This Again - Lessons Learned

**Purpose**: Document mistakes, anti-patterns, and lessons learned to prevent future issues.  
**Policy**: APPEND-ONLY - Never delete entries, only add new ones.

---

## Table of Contents

1. [SQLAlchemy & Database](#sqlalchemy--database)
2. [Testing & Test Isolation](#testing--test-isolation)
3. [Authentication & Security](#authentication--security)
4. [API Design](#api-design)
5. [Code Organization](#code-organization)
6. [CI/CD & DevOps](#cicd--devops)
7. [Import Management & Scripts](#import-management--scripts)

---

## SQLAlchemy & Database

### ❌ DON'T: Import Models Multiple Times

**Date**: 2025-10-25  
**Issue**: Multiple imports of `User`, `Role`, `Lot` models caused SQLAlchemy errors  
**Impact**: 13 errors, 24 failed tests

**What Happened**:
```python
# ❌ BAD - Multiple imports in different files
# database.py
from models.user import User, Role  # Wrong path

# user.py
from .user_unified import Role  # Duplicate import
```

**Why It's Bad**:
- SQLAlchemy maintains a single registry per declarative base
- Multiple imports register the same class multiple times
- Causes `InvalidRequestError: Multiple classes found for path "User"`

**What To Do Instead**:
```python
# ✅ GOOD - Use canonical imports only
# database.py
from src.models.user_unified import User, Role  # Canonical path

# user.py
# Don't import Role here - use fully qualified path in relationships
role = db.relationship('src.models.user_unified.Role', ...)
```

**Prevention**:
- Maintain `/docs/Class_Registry.md` with canonical locations
- Use fully qualified paths in SQLAlchemy relationships
- CI guard to detect duplicate model registrations

---

### ❌ DON'T: Use Unqualified Paths in Relationships

**Date**: 2025-10-25  
**Issue**: `Product.batches` relationship used `'Lot'` instead of fully qualified path  
**Impact**: `NoForeignKeysError` when trying to resolve relationship

**What Happened**:
```python
# ❌ BAD
class Product(db.Model):
    batches = db.relationship('Lot', foreign_keys='Lot.product_id')
```

**Why It's Bad**:
- SQLAlchemy can't resolve which `Lot` class to use if multiple exist
- Ambiguous references cause relationship resolution failures

**What To Do Instead**:
```python
# ✅ GOOD - Use fully qualified path
class Product(db.Model):
    batches = db.relationship('src.models.inventory.Lot', 
                              foreign_keys='src.models.inventory.Lot.product_id')

# ✅ BETTER - Or remove if not needed and query directly
# Query Lot model directly: Lot.query.filter_by(product_id=product.id).all()
```

**Prevention**:
- Always use fully qualified paths: `'module.path.ClassName'`
- Document all relationships in `/docs/DB_Schema.md`

---

## Testing & Test Isolation

### ❌ DON'T: Define Local `app` or `client` Fixtures in Test Files

**Date**: 2025-10-25  
**Issue**: Multiple test files defined their own `app` and `client` fixtures  
**Impact**: 24 failed tests with 404 errors when running full test suite

**What Happened**:
```python
# ❌ BAD - Local fixture in test_mfa_p0.py
@pytest.fixture
def app():
    from backend.app import create_app
    return create_app()

# ❌ BAD - Another local fixture in test_e2e_auth_p0.py
@pytest.fixture
def app():
    from backend.app import create_app
    return create_app()
```

**Why It's Bad**:
- Pytest gives precedence to local fixtures over `conftest.py` fixtures
- Each test file creates its own app with different configurations
- Causes test isolation issues and unpredictable behavior
- Routes may not be registered correctly in some app instances

**What To Do Instead**:
```python
# ✅ GOOD - Shared fixture in conftest.py
# backend/tests/conftest.py
@pytest.fixture(scope='function')
def app():
    from backend.app import create_app
    from src.database import db
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

# ✅ Test files just use the fixture
def test_something(client):  # No local fixture definition
    response = client.get('/api/endpoint')
    assert response.status_code == 200
```

**Prevention**:
- **NEVER** define `app`, `client`, or `app_context` fixtures in individual test files
- Always use shared fixtures from `conftest.py`
- Add autouse cleanup fixtures to prevent cross-test pollution

---

### ❌ DON'T: Set `SKIP_BLUEPRINTS=1` in Test Setup

**Date**: 2025-10-25  
**Issue**: `test_main.py` set `os.environ['SKIP_BLUEPRINTS'] = '1'` in setup  
**Impact**: Disabled blueprint registration, causing 404 errors in subsequent tests

**What Happened**:
```python
# ❌ BAD - test_main.py
@classmethod
def setUpClass(cls):
    os.environ['SKIP_BLUEPRINTS'] = '1'  # Disables routes!
    cls.app = create_app()
```

**Why It's Bad**:
- Environment variables persist across tests
- Disabling blueprints means no routes are registered
- Subsequent tests get 404 errors for valid endpoints

**What To Do Instead**:
```python
# ✅ GOOD - Don't disable blueprints
@classmethod
def setUpClass(cls):
    os.environ['TESTING'] = '1'  # OK
    # DON'T set SKIP_BLUEPRINTS
    cls.app = create_app()

@classmethod
def tearDownClass(cls):
    # Clean up any env vars you set
    if 'SKIP_BLUEPRINTS' in os.environ:
        del os.environ['SKIP_BLUEPRINTS']
```

**Prevention**:
- Use autouse cleanup fixtures in `conftest.py`
- Never disable core functionality in tests
- If you need minimal setup, use pytest markers instead

---

### ❌ DON'T: Expect Wrong HTTP Status Codes

**Date**: 2025-10-25  
**Issue**: `test_account_lockout` expected 401 but got 429 (correct code)  
**Impact**: 1 failed test

**What Happened**:
```python
# ❌ BAD - Wrong expectation
def test_account_lockout_after_5_failed_attempts(self, client):
    # ... 5 failed login attempts ...
    response = client.post('/api/auth/login', ...)
    assert response.status_code == 401  # Wrong! Should be 429
```

**Why It's Bad**:
- 401 = Unauthorized (wrong credentials)
- 429 = Too Many Requests (rate limited/locked out)
- Test expects wrong semantic meaning

**What To Do Instead**:
```python
# ✅ GOOD - Correct status code
def test_account_lockout_after_5_failed_attempts(self, client):
    # ... 5 failed login attempts ...
    response = client.post('/api/auth/login', ...)
    assert response.status_code == 429  # Correct - account locked
    assert 'locked' in response.get_json()['message'].lower()
```

**Prevention**:
- Use correct HTTP status codes per RFC 7231
- Document expected status codes in API contracts
- Review test assertions during code review

---

## Authentication & Security

### ❌ DON'T: Store Secrets in .env Files in Production

**Date**: 2025-10-21  
**Issue**: Production secrets stored in `.env` files  
**Impact**: Security risk, secrets in version control

**What To Do Instead**:
- ✅ Use KMS (AWS/GCP/Azure) or HashiCorp Vault
- ✅ Inject secrets at runtime via OIDC/Vault Agent
- ✅ Never commit `.env` files to git
- ✅ Use `.env.example` templates only

**Prevention**:
- Add `.env` to `.gitignore`
- Use gitleaks in CI to detect secrets
- Mandate KMS/Vault for production

---

### ❌ DON'T: Use Weak Password Hashing

**Date**: 2025-10-20  
**Issue**: Some legacy code used MD5/SHA1 for passwords  
**Impact**: Security vulnerability

**What To Do Instead**:
- ✅ Use bcrypt (current implementation)
- ✅ Use Argon2id or scrypt for new systems
- ✅ Never use MD5, SHA1, or plain SHA256 for passwords

**Prevention**:
- Code review for password hashing
- Security scan with bandit
- Document approved algorithms

---

## API Design

### ❌ DON'T: Return Inconsistent Error Formats

**Date**: 2025-10-22  
**Issue**: Different routes returned different error formats  
**Impact**: Frontend couldn't handle errors consistently

**What To Do Instead**:
- ✅ Use unified error envelope: `{success, code, message, details?, traceId}`
- ✅ Standardize error codes: `AUTH_*`, `VAL_*`, `SYS_*`
- ✅ Always include trace IDs for debugging

**Prevention**:
- Use error envelope middleware
- Document error format in API contracts
- Add E2E tests for error consistency

---

## Code Organization

### ❌ DON'T: Create Duplicate Models in Different Locations

**Date**: 2025-10-25  
**Issue**: `User` model existed in both `models/user.py` and `models/user_unified.py`  
**Impact**: SQLAlchemy registry conflicts

**What To Do Instead**:
- ✅ Maintain `/docs/Class_Registry.md` with canonical locations
- ✅ One canonical model per domain concept
- ✅ Mark legacy models clearly
- ✅ Merge duplicates into canonical version

**Prevention**:
- CI guard blocks PRs without registry delta
- Search codebase before creating new models
- Code review for duplicate classes

---

## CI/CD & DevOps

### ❌ DON'T: Skip CI Gates for "Quick Fixes"

**Date**: 2025-10-20  
**Issue**: Pushed directly to main without running tests  
**Impact**: Broke production deployment

**What To Do Instead**:
- ✅ Always run full CI pipeline
- ✅ Require PR reviews
- ✅ Use protected branches
- ✅ No direct pushes to main

**Prevention**:
- Branch protection rules
- Required status checks
- Automated deployment only after CI passes

---

## Summary of Key Lessons

1. **SQLAlchemy**: Use canonical imports only; fully qualified relationship paths
2. **Testing**: Shared fixtures in `conftest.py`; never disable blueprints
3. **Security**: KMS/Vault for secrets; bcrypt for passwords
4. **API**: Unified error envelope; consistent status codes
5. **Organization**: One canonical model per concept; maintain registry
6. **CI/CD**: Never skip gates; protect main branch

---

## Import Management & Scripts

### ❌ DON'T: Insert Imports Inside Try Blocks

**Date**: 2025-10-25
**Issue**: Automated script inserted imports inside try blocks, causing SyntaxErrors
**Impact**: 7 SyntaxErrors, 3 failed tests

**What Happened**:
```python
# ❌ BAD - Import inside try block
try:
    from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes
)
except ImportError:
    # Fallback...
```

**Why It's Bad**:
- Python expects `except` or `finally` immediately after try block
- Inserting code between `try` and `except` causes SyntaxError
- Breaks module loading and prevents tests from running

**What To Do Instead**:
```python
# ✅ GOOD - Import outside try block with its own error handling
try:
    from flask import Blueprint, jsonify, request
except ImportError:
    # Fallback...

# P0.2.4: Import error envelope helpers
try:
    from src.middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes
    )
except ImportError:
    # Fallback implementations
    def success_response(data=None, message='Success', code='SUCCESS', status_code=200):
        return {"success": True, "data": data, "message": message}, status_code

    def error_response(message, code=None, details=None, status_code=400):
        return {"success": False, "message": message, "code": code}, status_code

    class ErrorCodes:
        SYS_INTERNAL_ERROR = 'SYS_001'
```

**Prevention**:
- Always test automated scripts on a small subset first
- Add `--dry-run` mode to preview changes
- Use AST parsing instead of regex for complex code transformations
- Run linting AND tests after bulk changes

**Files Affected**:
- `backend/src/routes/dashboard.py`
- `backend/src/routes/excel_import.py`
- `backend/src/routes/excel_import_clean.py`
- `backend/src/routes/lot_management.py`
- `backend/src/routes/security_system.py`
- `backend/src/routes/batch_management.py`
- `backend/src/routes/batch_reports.py`
- `backend/src/routes/export.py`

**Resolution**: Created `scripts/fix_try_except_imports.py` to fix the pattern

---

### ❌ DON'T: Forget to Import All Required Helpers

**Date**: 2025-10-25
**Issue**: `products_unified.py` imported `error_response` and `ErrorCodes` but not `success_response`
**Impact**: 12 F821 undefined name errors

**What Happened**:
```python
# ❌ BAD - Missing success_response
from src.middleware.error_envelope_middleware import error_response, ErrorCodes

# Later in code...
return success_response(data=products)  # F821: undefined name 'success_response'
```

**Why It's Bad**:
- Code uses helper but doesn't import it
- Causes linting errors and potential runtime errors
- Inconsistent with other route files

**What To Do Instead**:
```python
# ✅ GOOD - Import all helpers used in the file
from src.middleware.error_envelope_middleware import success_response, error_response, ErrorCodes
```

**Prevention**:
- Use IDE auto-import features
- Run `flake8 --select=F821` to catch undefined names
- Review all usages of error envelope helpers in file before committing

---

### ❌ DON'T: Forget Function Parameters in Route Decorators

**Date**: 2025-10-25
**Issue**: `invoices.py` route decorator had `<int:invoice_id>` but function didn't accept parameter
**Impact**: 1 F821 undefined name error

**What Happened**:
```python
# ❌ BAD - Missing parameter
@invoices_bp.route('/api/invoices/<int:invoice_id>/payments', methods=['POST'])
def add_payment():  # Missing invoice_id parameter
    invoice = Invoice.query.get_or_404(invoice_id)  # F821: undefined name 'invoice_id'
```

**Why It's Bad**:
- Route decorator captures URL parameter but function doesn't receive it
- Causes undefined name error
- Runtime error when route is called

**What To Do Instead**:
```python
# ✅ GOOD - Include all URL parameters in function signature
@invoices_bp.route('/api/invoices/<int:invoice_id>/payments', methods=['POST'])
def add_payment(invoice_id):  # Accept invoice_id parameter
    invoice = Invoice.query.get_or_404(invoice_id)
```

**Prevention**:
- Always match function parameters to route decorator parameters
- Use type hints to make parameters explicit
- Add integration tests that call routes with URL parameters

---

**Last Updated**: 2025-10-25
**Next Review**: 2025-11-01

**Remember**: This file is APPEND-ONLY. Add new lessons, never delete old ones.

