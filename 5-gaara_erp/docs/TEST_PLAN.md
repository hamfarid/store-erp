# Gaara ERP Test Plan

**Version**: 1.0
**Date**: 2025-12-01
**Total Test Files**: 216
**Framework**: pytest + pytest-django

---

## Test Structure Overview

```
gaara_erp/
├── core_modules/          # 33 test files, ~350 tests
│   ├── security/tests/    # Security tests (JWT, lockout, CSRF)
│   ├── permissions/tests/ # Permission & decorator tests
│   ├── users/tests/       # User management tests
│   └── ...
├── business_modules/      # 50+ test files
│   ├── accounting/tests/  # Accounting tests
│   ├── inventory/tests/   # Inventory tests
│   └── ...
├── services_modules/      # 60+ test files
│   ├── hr/tests/          # HR tests
│   ├── projects/tests/    # Project tests
│   └── ...
└── agricultural_modules/  # 30+ test files
    ├── farms/tests/       # Farm management tests
    └── ...
```

---

## Prerequisites

### 1. Install Test Dependencies
```bash
# Using pip
pip install pytest pytest-django pytest-cov factory-boy

# Or using requirements
pip install -r requirements-test.txt

# Or with pyproject.toml extras
pip install -e ".[test]"
```

### 2. Configure Environment
```bash
# Set environment variables
export DJANGO_SETTINGS_MODULE=gaara_erp.gaara_erp.settings.test
export APP_MODE=test
export SECRET_KEY=test-secret-key-for-testing-only

# Windows PowerShell
$env:DJANGO_SETTINGS_MODULE="gaara_erp.gaara_erp.settings.test"
$env:APP_MODE="test"
$env:SECRET_KEY="test-secret-key-for-testing-only"
```

---

## Running Tests

### Full Test Suite
```bash
# Run all tests
cd gaara_erp
pytest

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run with verbose output
pytest -v

# Run with parallel execution (if pytest-xdist installed)
pytest -n auto
```

### Module-Specific Tests
```bash
# Core modules
pytest core_modules/

# Security tests only
pytest core_modules/security/tests/

# Accounting tests
pytest business_modules/accounting/tests/

# HR tests
pytest services_modules/hr/tests/
```

### Category-Specific Tests
```bash
# Run only security tests
pytest -k "security or lockout or jwt or csrf"

# Run only integration tests
pytest -k "integration"

# Run only unit tests
pytest -k "not integration"

# Skip slow tests
pytest -m "not slow"
```

---

## Critical Security Tests

### Account Lockout Tests (`test_account_lockout.py`)
| Test | Description | Priority |
|------|-------------|----------|
| `test_account_locks_after_5_failed_attempts` | Verify 5 failed = lock | P0 |
| `test_account_unlocks_after_15_minutes` | Auto-unlock after timeout | P0 |
| `test_failed_login_attempts_reset_on_success` | Reset counter on success | P0 |
| `test_locked_account_prevents_authentication` | Block even with correct pw | P0 |
| `test_increment_failed_login_method` | Unit test for increment | P1 |
| `test_reset_failed_login_method` | Unit test for reset | P1 |

### JWT Security Tests (`test_jwt_security.py`)
| Test | Description | Priority |
|------|-------------|----------|
| `test_jwt_access_token_lifetime` | Access token = 15 min | P0 |
| `test_jwt_refresh_token_rotation` | Refresh rotation enabled | P0 |
| `test_jwt_uses_secret_key` | Uses Django SECRET_KEY | P0 |

### CSRF & Rate Limiting Tests (`test_csrf_and_rate_limiting.py`)
| Test | Description | Priority |
|------|-------------|----------|
| `test_csrf_protection_enabled` | CSRF middleware active | P0 |
| `test_rate_limiting_login` | 5 attempts/5min limit | P0 |

---

## Test Coverage Targets

| Module | Target | Current | Status |
|--------|--------|---------|--------|
| core_modules | 80% | TBD | ⏳ |
| security | 90% | TBD | ⏳ |
| accounting | 80% | TBD | ⏳ |
| inventory | 80% | TBD | ⏳ |
| hr | 75% | TBD | ⏳ |

---

## Test Commands Quick Reference

```bash
# Run and generate HTML coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Run specific test file
pytest core_modules/security/tests/test_account_lockout.py

# Run specific test class
pytest core_modules/security/tests/test_account_lockout.py::TestAccountLockout

# Run specific test method
pytest core_modules/security/tests/test_account_lockout.py::TestAccountLockout::test_account_locks_after_5_failed_attempts

# Run tests matching pattern
pytest -k "test_account"

# Run tests with print output visible
pytest -s

# Run tests and stop on first failure
pytest -x

# Run tests and stop after 3 failures
pytest --maxfail=3

# Run last failed tests only
pytest --lf

# Run failed tests first, then others
pytest --ff
```

---

## Django Test Runner (Alternative)

If pytest has issues, use Django's built-in test runner:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core_modules.security

# Run with verbosity
python manage.py test -v 2

# Run specific test
python manage.py test core_modules.security.tests.test_account_lockout.TestAccountLockout.test_account_locks_after_5_failed_attempts
```

---

## CI/CD Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test_gaara_erp
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e ".[test]"
      
      - name: Run tests
        env:
          DJANGO_SETTINGS_MODULE: gaara_erp.gaara_erp.settings.test
          SECRET_KEY: test-secret-key
          DATABASE_URL: postgres://postgres:postgres@localhost/test_gaara_erp
        run: |
          pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Test Fixtures

### Common Fixtures (conftest.py)
```python
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123!'
    )

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='AdminPassword123!'
    )
```

---

## Known Test Issues

1. **Circular Import**: Users ↔ Organization circular dependency
   - Workaround: DISABLE_MIGRATIONS=1 in test settings

2. **Database Migrations**: Some migrations may fail in test
   - Workaround: Use `--no-migrations` flag or disable in conftest

3. **Slow Tests**: Some integration tests are slow
   - Mark with `@pytest.mark.slow` and skip with `-m "not slow"`

---

## Post-Test Actions

After running tests:

1. **Review Coverage Report**
   ```bash
   # Open coverage report
   open htmlcov/index.html  # macOS
   start htmlcov/index.html  # Windows
   ```

2. **Fix Failing Tests**
   - Check test output for failures
   - Run specific failing tests with `-v` for details

3. **Update Documentation**
   - Update this document with actual coverage numbers
   - Document any new test patterns

---

**Last Updated**: 2025-12-01

