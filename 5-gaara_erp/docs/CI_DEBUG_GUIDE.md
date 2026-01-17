# CI/CD Debugging Guide for Gaara ERP v12

## 🔍 Quick Reference

### Common CI Failure Points

| Job | Common Failures | Quick Fix |
|-----|-----------------|-----------|
| `backend-tests` | Import errors, Missing migrations | Run `python manage.py makemigrations` |
| `lint` | flake8 E9/F63/F7/F82 errors | Fix syntax errors first |
| `security-tests` | Missing environment variables | Check `SECRET_KEY`, `DATABASE_URL` |
| `docker-build` | Dockerfile not found | Verify paths in workflow |

---

## 🏃 Running CI Locally

### Prerequisites

```bash
# Install CI testing tools
pip install pytest pytest-django pytest-cov flake8 black isort

# Set up test database (PostgreSQL)
docker run -d --name gaara-test-db \
  -e POSTGRES_DB=gaara_erp_test \
  -e POSTGRES_USER=test_user \
  -e POSTGRES_PASSWORD=test_password \
  -p 5432:5432 \
  postgres:15-alpine

# Set up Redis
docker run -d --name gaara-test-redis -p 6379:6379 redis:7-alpine
```

### Environment Variables Required

```bash
# Create .env.test file
export SECRET_KEY="test-secret-key-for-ci-only"
export DEBUG=true
export APP_MODE=test
export DATABASE_URL=postgres://test_user:test_password@localhost:5432/gaara_erp_test
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=gaara_erp_test
export DB_USER=test_user
export DB_PASSWORD=test_password
export REDIS_HOST=localhost
export REDIS_PORT=6379
```

### Run Tests Like CI

```bash
# 1. Lint checks (same as CI)
cd gaara_erp
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# 2. Run migrations
python manage.py migrate --noinput

# 3. Run all tests
pytest --cov=. --cov-report=term-missing -v

# 4. Run security tests only
pytest core_modules/security/tests/ -v

# 5. Run integration tests
pytest -k "integration" -v
```

---

## 🐛 Common CI Failures & Solutions

### 1. Import Errors

**Symptom:**
```
ImportError: cannot import name 'X' from 'module'
ModuleNotFoundError: No module named 'X'
```

**Solutions:**
```bash
# Check for circular imports
python -c "import business_modules.accounting.models"

# Verify app is in INSTALLED_APPS
grep -r "business_modules.accounting" gaara_erp/settings/

# Check __init__.py exports
cat business_modules/accounting/__init__.py
```

### 2. Migration Errors

**Symptom:**
```
django.db.utils.ProgrammingError: relation "X" does not exist
InconsistentMigrationHistory
```

**Solutions:**
```bash
# Check migration status
python manage.py showmigrations

# Create missing migrations
python manage.py makemigrations --check --dry-run
python manage.py makemigrations

# Reset migrations (DANGEROUS - only in dev)
python manage.py migrate app_name zero
python manage.py migrate app_name
```

### 3. Database Connection Failures

**Symptom:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**
```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# Check connection manually
psql postgres://test_user:test_password@localhost:5432/gaara_erp_test

# In GitHub Actions, check service health
# The service should show "healthy" in logs
```

### 4. Flake8 Errors (E9, F63, F7, F82)

**Error Types:**
- `E9`: Syntax errors (CRITICAL - blocks execution)
- `F63`: Invalid escape sequences
- `F7`: Syntax errors in type comments
- `F82`: Undefined names

**Find & Fix:**
```bash
# Find all critical errors
flake8 . --select=E9,F63,F7,F82 --show-source

# Auto-fix some issues
autopep8 --in-place --aggressive --aggressive file.py
```

### 5. Docker Build Failures

**Symptom:**
```
COPY failed: file not found
```

**Solutions:**
```bash
# Verify Dockerfile path
ls -la Dockerfile
ls -la gaara-erp-frontend/Dockerfile

# Build locally first
docker build -t gaara-erp-test .
```

---

## 🔧 CI Workflow Files

### Main Workflows

| File | Purpose | Triggers |
|------|---------|----------|
| `ci.yml` | Main CI pipeline | push, PR to main/develop |
| `tests.yml` | Detailed test suite | push, PR |
| `security-scan.yml` | Trivy security scan | push, PR |
| `codeql.yml` | CodeQL analysis | push, PR, schedule |

### Environment Matrix

```yaml
# ci.yml uses these services
services:
  postgres:
    image: postgres:15-alpine
    # ...
  redis:
    image: redis:7-alpine
    # ...
```

---

## 🎯 Debugging Steps

### Step 1: Identify the Failing Job

```bash
# In GitHub Actions, check:
# 1. Which job failed (backend-tests, lint, etc.)
# 2. Which step in that job
# 3. The exact error message
```

### Step 2: Reproduce Locally

```bash
# Set same environment as CI
export DJANGO_SETTINGS_MODULE=gaara_erp.settings.test
export SECRET_KEY=test-secret-key
export APP_MODE=test

# Run the same commands as CI
python -m pytest tests/ -v
```

### Step 3: Check Recent Changes

```bash
# What changed in this PR?
git diff main...HEAD --name-only

# Check if any model changes need migrations
python manage.py makemigrations --check
```

### Step 4: Fix and Verify

```bash
# After fixing:
# 1. Run tests locally
pytest -v --tb=short

# 2. Run lint
flake8 . --select=E9,F63,F7,F82

# 3. Commit and push
git add .
git commit -m "fix: resolve CI failure in X"
git push
```

---

## 📊 CI Performance Optimization

### Cache Strategies

```yaml
# pip cache (already in ci.yml)
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Parallel Jobs

```yaml
# Run independent jobs in parallel
jobs:
  lint:
    # runs immediately
  test:
    needs: lint  # waits for lint
  security:
    # runs in parallel with test
```

### Skip Unnecessary Jobs

```yaml
# Skip tests for docs-only changes
on:
  push:
    paths-ignore:
      - 'docs/**'
      - '*.md'
```

---

## 🚨 Emergency: CI Completely Broken

If CI is completely broken and blocking all PRs:

```bash
# 1. Create a hotfix branch
git checkout -b hotfix/ci-fix

# 2. Disable failing checks temporarily (if needed)
# Edit .github/workflows/ci.yml to add `|| true` to failing step

# 3. Push to bypass checks (requires admin)
git push --force-with-lease

# 4. Fix the actual issue in a follow-up PR
```

---

## 📝 Checklist Before Pushing

- [ ] `python manage.py check` passes
- [ ] `python manage.py makemigrations --check` shows no changes needed
- [ ] `flake8 . --select=E9,F63,F7,F82` returns 0 errors
- [ ] `pytest -v --tb=short` passes locally
- [ ] Environment variables documented if new ones added

---

## 🔗 Related Documentation

- [Django Testing Docs](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Flake8 Error Codes](https://flake8.pycqa.org/en/latest/user/error-codes.html)

---

*Last Updated: 2026-01-16*
