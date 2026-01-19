# 📋 Gaara Scan AI - Detailed Task Breakdown
## قائمة المهام التفصيلية | Atomic Task List with Subtasks

**Generated:** 2026-01-17  
**Persona:** The Project Manager  
**Mode:** ADOPTION (Brownfield)  
**Total Tasks:** 127 tasks across 5 phases

---

## 🏷️ Tag Legend

| Tag | Meaning |
|-----|---------|
| `[Scaffold]` | Create new file/directory |
| `[Code]` | Write implementation code |
| `[Modify]` | Change existing file |
| `[Test]` | Write/fix tests |
| `[Doc]` | Documentation update |
| `[Config]` | Configuration change |
| `[Migration]` | Database migration |
| `[Security]` | Security-related task |
| `[Librarian]` | Update file registry |
| `[CI/CD]` | Pipeline task |
| `[Cleanup]` | Remove/archive files |

---

## Phase 1: Code Stabilization (Days 1-3)

### 1.1 Legacy Code Archival 🔴 CRITICAL

#### Task 1.1.1: Archive Legacy Directory
- [ ] `[Scaffold]` Create `scripts/archive_legacy.py`
  - [ ] Import shutil, os, datetime modules
  - [ ] Define archive_legacy() function
  - [ ] Add timestamp to archive filename
  - [ ] Create ZIP archive of `gaara_ai_integrated/`
  - [ ] Remove original directory after archival
  - [ ] Add logging for audit trail
- [ ] `[Code]` Implement archive verification
  - [ ] Verify ZIP file integrity
  - [ ] List archived files count
  - [ ] Calculate archive size
- [ ] `[Test]` Test archive script
  - [ ] Test on small test directory first
  - [ ] Verify no imports from archived directory
- [ ] `[Librarian]` Update `.memory/file_registry.json`
  - [ ] Mark `gaara_ai_integrated/` as archived
  - [ ] Add archive path to registry

#### Task 1.1.2: Clean SQLite Artifacts
- [ ] `[Cleanup]` Delete `backend/data/gaara_scan_ai.db`
- [ ] `[Cleanup]` Delete `backend/data/gaara_scan.db`
- [ ] `[Cleanup]` Delete `backend/gaara_scan_ai.db`
- [ ] `[Cleanup]` Delete `backend/test.db`
- [ ] `[Cleanup]` Delete root `gaara_scan_ai.db`
- [ ] `[Config]` Verify `DATABASE_URL` points to PostgreSQL
- [ ] `[Doc]` Document that SQLite is only for testing

#### Task 1.1.3: Update .gitignore
- [ ] `[Config]` Add `*.db` to `.gitignore`
- [ ] `[Config]` Add `*.db-journal` to `.gitignore`
- [ ] `[Config]` Add `legacy_archive_*.zip` to `.gitignore`
- [ ] `[Config]` Verify `__pycache__/` is ignored
- [ ] `[Config]` Verify `node_modules/` is ignored

---

### 1.2 Test Suite Repair 🔴 CRITICAL

#### Task 1.2.1: Identify Failing Tests
- [ ] `[Test]` Run `pytest tests/ -v --tb=short`
- [ ] `[Doc]` Document each failing test
  - [ ] Test name and file
  - [ ] Error message
  - [ ] Root cause analysis
- [ ] `[Librarian]` Create `.memory/test_failures.json`

#### Task 1.2.2: Fix Backend Tests
- [ ] `[Test]` Fix test 1: `test_auth_login_invalid`
  - [ ] Check expected error response
  - [ ] Update test assertions
- [ ] `[Test]` Fix test 2: `test_diagnosis_create`
  - [ ] Mock ML service response
  - [ ] Fix file upload handling
- [ ] `[Test]` Fix test 3: `test_user_update_profile`
  - [ ] Check schema validation
  - [ ] Update test data
- [ ] `[Test]` Fix test 4: `test_farm_delete_cascade`
  - [ ] Verify cascade relationships
  - [ ] Update test fixtures
- [ ] `[Test]` Fix test 5: `test_crawler_rate_limit`
  - [ ] Mock Redis connection
  - [ ] Fix rate limit assertions

#### Task 1.2.3: Improve Test Coverage
- [ ] `[Test]` Run `pytest --cov=src --cov-report=html`
- [ ] `[Test]` Identify modules below 90% coverage
- [ ] `[Test]` Add tests for `backend/src/api/v1/auth.py`
  - [ ] Test successful login
  - [ ] Test failed login
  - [ ] Test token refresh
  - [ ] Test logout
- [ ] `[Test]` Add tests for `backend/src/api/v1/diagnosis.py`
  - [ ] Test image upload
  - [ ] Test diagnosis retrieval
  - [ ] Test pagination
- [ ] `[Doc]` Generate coverage report

---

### 1.3 Code Quality Fixes 🟠 HIGH

#### Task 1.3.1: Fix Import Errors
- [ ] `[Code]` Scan for circular imports
- [ ] `[Code]` Fix any broken imports from legacy code
- [ ] `[Code]` Verify all `__init__.py` files are correct
- [ ] `[Test]` Run `python -c "from backend.src.main import app"`

#### Task 1.3.2: Lint Compliance
- [ ] `[Code]` Run `black backend/src/` --check
- [ ] `[Code]` Run `isort backend/src/` --check
- [ ] `[Code]` Fix any formatting issues
- [ ] `[Code]` Run `flake8 backend/src/`
- [ ] `[Doc]` Document any ignored lint rules

---

## Phase 2: Security Hardening (Days 4-7)

### 2.1 Secret Management 🔴 CRITICAL

#### Task 2.1.1: Remove Default Secrets from Docker Compose
- [ ] `[Security]` Open `docker-compose.yml`
- [ ] `[Modify]` Remove default for `POSTGRES_PASSWORD`
  - [ ] Change `${POSTGRES_PASSWORD:-gaara_secure_2024}` to `${POSTGRES_PASSWORD}`
- [ ] `[Modify]` Remove default for `REDIS_PASSWORD`
  - [ ] Change `${REDIS_PASSWORD:-redis_secure_2024}` to `${REDIS_PASSWORD}`
- [ ] `[Modify]` Remove default for `SECRET_KEY`
- [ ] `[Modify]` Remove default for `JWT_SECRET`
- [ ] `[Config]` Update `docker-compose.unified.yml` similarly
- [ ] `[Test]` Verify compose fails without secrets

#### Task 2.1.2: Update Environment Example
- [ ] `[Doc]` Open `env.example`
- [ ] `[Doc]` Add comment: "REQUIRED - Must be set"
- [ ] `[Doc]` Add secure password generation example
- [ ] `[Doc]` Add `openssl rand -hex 32` command for secrets
- [ ] `[Security]` Add minimum length requirements

#### Task 2.1.3: Create Secret Validation
- [ ] `[Scaffold]` Create `backend/src/core/secret_validator.py`
- [ ] `[Code]` Implement `validate_secrets()` function
  - [ ] Check SECRET_KEY length >= 32
  - [ ] Check JWT_SECRET length >= 32
  - [ ] Check POSTGRES_PASSWORD is not default
  - [ ] Raise error on validation failure
- [ ] `[Modify]` Call validator in `backend/src/main.py` startup
- [ ] `[Test]` Test validation with weak secrets

---

### 2.2 Account Lockout 🔴 CRITICAL

#### Task 2.2.1: Add User Model Fields
- [ ] `[Migration]` Create Alembic migration file
  - [ ] `alembic revision -m "add_security_fields"`
- [ ] `[Migration]` Add `failed_login_attempts` column (Integer, default 0)
- [ ] `[Migration]` Add `locked_until` column (DateTime, nullable)
- [ ] `[Migration]` Add `last_login` column (DateTime, nullable)
- [ ] `[Migration]` Add `password_changed_at` column (DateTime, nullable)
- [ ] `[Migration]` Apply migration: `alembic upgrade head`
- [ ] `[Test]` Verify migration applied correctly

#### Task 2.2.2: Create Lockout Service
- [ ] `[Scaffold]` Create `backend/src/services/lockout_service.py`
- [ ] `[Code]` Define `LockoutService` class
- [ ] `[Code]` Implement `MAX_ATTEMPTS = 5` constant
- [ ] `[Code]` Implement `LOCKOUT_DURATION = timedelta(minutes=15)`
- [ ] `[Code]` Implement `record_failed_attempt()` method
  - [ ] Increment `failed_login_attempts`
  - [ ] Set `locked_until` if max reached
  - [ ] Return True if now locked
- [ ] `[Code]` Implement `is_locked()` method
  - [ ] Check `locked_until` vs current time
  - [ ] Return boolean
- [ ] `[Code]` Implement `reset_attempts()` method
  - [ ] Reset counter to 0
  - [ ] Clear `locked_until`
  - [ ] Set `last_login`
- [ ] `[Test]` Write unit tests for LockoutService
  - [ ] Test successful lockout after 5 attempts
  - [ ] Test unlock after duration
  - [ ] Test reset on successful login
- [ ] `[Librarian]` Register new file

#### Task 2.2.3: Integrate Lockout with Auth
- [ ] `[Modify]` Open `backend/src/api/v1/auth.py`
- [ ] `[Code]` Import `LockoutService`
- [ ] `[Code]` Check `is_locked()` before authentication
- [ ] `[Code]` Return 423 Locked if account locked
- [ ] `[Code]` Call `record_failed_attempt()` on failure
- [ ] `[Code]` Call `reset_attempts()` on success
- [ ] `[Test]` Write integration tests
  - [ ] Test lockout response
  - [ ] Test unlock after wait

---

### 2.3 SSRF Protection 🔴 CRITICAL

#### Task 2.3.1: Create SSRF Protection Module
- [ ] `[Scaffold]` Create `image_crawler/ssrf_protection.py`
- [ ] `[Code]` Import `ipaddress`, `socket`, `urllib.parse`
- [ ] `[Code]` Define `SSRFProtection` class
- [ ] `[Code]` Define `BLOCKED_HOSTS` set
  - [ ] Add `localhost`, `127.0.0.1`, `0.0.0.0`
  - [ ] Add `metadata.google.internal`
  - [ ] Add `169.254.169.254`
- [ ] `[Code]` Define `BLOCKED_NETWORKS` list
  - [ ] Add `10.0.0.0/8`
  - [ ] Add `172.16.0.0/12`
  - [ ] Add `192.168.0.0/16`
  - [ ] Add `127.0.0.0/8`
  - [ ] Add `169.254.0.0/16`
- [ ] `[Code]` Implement `validate_url()` method
  - [ ] Parse URL
  - [ ] Check scheme (http/https only)
  - [ ] Check host not in blocked list
  - [ ] Resolve DNS
  - [ ] Check IP not in blocked networks
- [ ] `[Test]` Write unit tests
  - [ ] Test blocking localhost
  - [ ] Test blocking internal IPs
  - [ ] Test allowing valid URLs
- [ ] `[Librarian]` Register new file

#### Task 2.3.2: Integrate SSRF Protection
- [ ] `[Modify]` Open `image_crawler/crawler.py`
- [ ] `[Code]` Import `SSRFProtection`
- [ ] `[Code]` Validate all URLs before fetching
- [ ] `[Code]` Log blocked attempts
- [ ] `[Test]` Write integration tests

---

### 2.4 Rate Limiting 🟠 HIGH

#### Task 2.4.1: Create Rate Limiter Middleware
- [ ] `[Scaffold]` Create `backend/src/middleware/rate_limiter.py`
- [ ] `[Code]` Import Redis client
- [ ] `[Code]` Define rate limit configurations
  - [ ] Auth endpoints: 5/minute
  - [ ] API endpoints: 60/minute
  - [ ] Upload endpoints: 2/minute
- [ ] `[Code]` Implement sliding window algorithm
- [ ] `[Code]` Return 429 Too Many Requests when exceeded
- [ ] `[Test]` Write unit tests
- [ ] `[Librarian]` Register new file

#### Task 2.4.2: Apply Rate Limiter
- [ ] `[Modify]` Open `backend/src/main.py`
- [ ] `[Code]` Import rate limiter middleware
- [ ] `[Code]` Apply to auth routes
- [ ] `[Code]` Apply to upload routes
- [ ] `[Test]` Test rate limiting works

---

## Phase 3: ML Enhancement (Days 8-14)

### 3.1 Model Versioning 🟠 HIGH

#### Task 3.1.1: Create Model Manager
- [ ] `[Scaffold]` Create `ml_service/model_manager.py`
- [ ] `[Code]` Define `ModelManager` class
- [ ] `[Code]` Implement `__init__(models_dir)`
- [ ] `[Code]` Implement `_load_manifest()` method
- [ ] `[Code]` Implement `load_model(version)` method
- [ ] `[Code]` Implement `get_active_model()` method
- [ ] `[Code]` Implement `set_active_version(version)` method
- [ ] `[Code]` Implement `list_versions()` method
- [ ] `[Test]` Write unit tests
- [ ] `[Librarian]` Register new file

#### Task 3.1.2: Create Model Manifest
- [ ] `[Scaffold]` Create `ml_service/models/manifest.json`
- [ ] `[Config]` Define schema
  ```json
  {
    "active_version": "v1.0.0",
    "versions": {
      "v1.0.0": {
        "path": "v1.0.0/model.pt",
        "created": "2025-12-01",
        "accuracy": 0.95
      }
    }
  }
  ```
- [ ] `[Doc]` Document versioning strategy

#### Task 3.1.3: Add Version Endpoints
- [ ] `[Modify]` Open `ml_service/main.py`
- [ ] `[Code]` Add `GET /models` endpoint (list versions)
- [ ] `[Code]` Add `GET /models/active` endpoint
- [ ] `[Code]` Add `POST /models/active` endpoint (set active)
- [ ] `[Test]` Write endpoint tests

---

### 3.2 Confidence Threshold 🟠 HIGH

#### Task 3.2.1: Add Configurable Threshold
- [ ] `[Modify]` Open `ml_service/yolo_detector.py`
- [ ] `[Code]` Add `DEFAULT_CONFIDENCE = 0.5` constant
- [ ] `[Code]` Add `MIN_CONFIDENCE = 0.3` constant
- [ ] `[Code]` Add `confidence_threshold` parameter to `detect()`
- [ ] `[Code]` Apply threshold validation (min/max bounds)
- [ ] `[Code]` Filter detections by threshold
- [ ] `[Test]` Test with various thresholds

#### Task 3.2.2: Per-Disease Threshold
- [ ] `[Modify]` Open `backend/src/models/disease.py`
- [ ] `[Code]` Verify `confidence_threshold` field exists
- [ ] `[Code]` Default to 0.75 if not set
- [ ] `[Modify]` Open `backend/src/api/v1/diagnosis.py`
- [ ] `[Code]` Load disease threshold before ML call
- [ ] `[Code]` Pass threshold to ML service
- [ ] `[Test]` Test disease-specific thresholds

---

### 3.3 ML Schemas 🟡 MEDIUM

#### Task 3.3.1: Create Pydantic Schemas
- [ ] `[Scaffold]` Create `ml_service/schemas.py`
- [ ] `[Code]` Define `Detection` model
  - [ ] `class_id: int`
  - [ ] `class_name: str`
  - [ ] `confidence: float`
  - [ ] `bbox: List[float]`
- [ ] `[Code]` Define `InferenceRequest` model
  - [ ] `image_base64: Optional[str]`
  - [ ] `image_url: Optional[str]`
  - [ ] `confidence_threshold: float = 0.5`
  - [ ] `max_detections: int = 10`
- [ ] `[Code]` Define `InferenceResponse` model
  - [ ] `success: bool`
  - [ ] `detections: List[Detection]`
  - [ ] `model_version: str`
  - [ ] `inference_time_ms: int`
- [ ] `[Test]` Test schema validation
- [ ] `[Librarian]` Register new file

---

### 3.4 Crawler Improvements 🟡 MEDIUM

#### Task 3.4.1: Add Source Rate Limiting
- [ ] `[Modify]` Open `image_crawler/crawler.py`
- [ ] `[Code]` Define per-source rate limits
- [ ] `[Code]` Implement request throttling
- [ ] `[Code]` Add retry with exponential backoff
- [ ] `[Test]` Test rate limiting

#### Task 3.4.2: Add Image Quality Validation
- [ ] `[Scaffold]` Create `image_crawler/image_validator.py`
- [ ] `[Code]` Implement `validate_image_size()` (min 256x256)
- [ ] `[Code]` Implement `validate_image_format()` (JPG, PNG)
- [ ] `[Code]` Implement `detect_watermark()` (basic heuristics)
- [ ] `[Code]` Implement `calculate_hash()` (for deduplication)
- [ ] `[Test]` Test validation functions
- [ ] `[Librarian]` Register new file

---

## Phase 4: Frontend Polish (Days 15-21)

### 4.1 RTL Audit 🟡 MEDIUM

#### Task 4.1.1: Dashboard RTL
- [ ] `[Code]` Verify `frontend/pages/Dashboard.jsx` RTL
- [ ] `[Code]` Check sidebar position (right in RTL)
- [ ] `[Code]` Check card layouts
- [ ] `[Code]` Check chart labels
- [ ] `[Test]` Visual test in Arabic

#### Task 4.1.2: Auth Pages RTL
- [ ] `[Code]` Verify `frontend/pages/Login.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Register.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/ForgotPassword.jsx` RTL
- [ ] `[Code]` Check form field alignment
- [ ] `[Code]` Check button positions
- [ ] `[Test]` Visual test all auth flows

#### Task 4.1.3: CRUD Pages RTL
- [ ] `[Code]` Verify `frontend/pages/Farms.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Crops.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Diseases.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Equipment.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Inventory.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Users.jsx` RTL
- [ ] `[Code]` Check table column order
- [ ] `[Code]` Check action button positions
- [ ] `[Test]` Visual test CRUD operations

#### Task 4.1.4: Diagnosis Pages RTL
- [ ] `[Code]` Verify `frontend/pages/Diagnosis.jsx` RTL
- [ ] `[Code]` Check image upload area
- [ ] `[Code]` Check results display
- [ ] `[Code]` Check treatment recommendations
- [ ] `[Test]` Visual test diagnosis flow

#### Task 4.1.5: Analytics Pages RTL
- [ ] `[Code]` Verify `frontend/pages/Analytics.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Reports.jsx` RTL
- [ ] `[Code]` Check chart orientations
- [ ] `[Code]` Check data labels
- [ ] `[Test]` Visual test analytics

#### Task 4.1.6: Settings Pages RTL
- [ ] `[Code]` Verify `frontend/pages/Settings.jsx` RTL
- [ ] `[Code]` Verify `frontend/pages/Profile.jsx` RTL
- [ ] `[Code]` Check form layouts
- [ ] `[Code]` Check toggle positions
- [ ] `[Test]` Visual test settings

---

### 4.2 Error Handling 🟡 MEDIUM

#### Task 4.2.1: Enhance Error Boundary
- [ ] `[Modify]` Open `frontend/components/ErrorBoundary/ErrorBoundary.jsx`
- [ ] `[Code]` Add bilingual error messages
- [ ] `[Code]` Add reload button
- [ ] `[Code]` Add "Go Home" button
- [ ] `[Code]` Style for dark mode
- [ ] `[Test]` Test error boundary triggers

#### Task 4.2.2: API Error Handling
- [ ] `[Modify]` Open `frontend/services/ApiService.js`
- [ ] `[Code]` Add consistent error response parsing
- [ ] `[Code]` Add retry logic for 5xx errors
- [ ] `[Code]` Add timeout handling
- [ ] `[Code]` Add offline detection
- [ ] `[Test]` Test error scenarios

#### Task 4.2.3: Form Validation Errors
- [ ] `[Code]` Standardize form error display
- [ ] `[Code]` Add bilingual validation messages
- [ ] `[Code]` Add inline field errors
- [ ] `[Test]` Test form validation

---

### 4.3 Performance 🟢 LOW

#### Task 4.3.1: Code Splitting
- [ ] `[Modify]` Open `frontend/App.jsx`
- [ ] `[Code]` Add `React.lazy()` for all pages
- [ ] `[Code]` Add `Suspense` with loading fallback
- [ ] `[Test]` Verify lazy loading works

#### Task 4.3.2: Image Optimization
- [ ] `[Code]` Add lazy loading to images
- [ ] `[Code]` Add placeholder/skeleton
- [ ] `[Code]` Add WebP format support
- [ ] `[Test]` Test image loading

---

## Phase 5: Deployment & CI/CD (Days 22-28)

### 5.1 CI Pipeline 🟠 HIGH

#### Task 5.1.1: Create GitHub Actions CI
- [ ] `[Scaffold]` Create `.github/workflows/ci.yml`
- [ ] `[CI/CD]` Add `backend-tests` job
  - [ ] Setup Python 3.11
  - [ ] Setup PostgreSQL service
  - [ ] Setup Redis service
  - [ ] Install dependencies
  - [ ] Run pytest with coverage
  - [ ] Fail if coverage < 90%
- [ ] `[CI/CD]` Add `frontend-tests` job
  - [ ] Setup Node 22
  - [ ] Install dependencies
  - [ ] Run Vitest with coverage
- [ ] `[CI/CD]` Add `lint` job
  - [ ] Run Black check
  - [ ] Run ESLint
- [ ] `[Test]` Test pipeline on PR
- [ ] `[Librarian]` Register new file

#### Task 5.1.2: Create Security Scan Workflow
- [ ] `[Scaffold]` Create `.github/workflows/security-scan.yml`
- [ ] `[CI/CD]` Add Trivy vulnerability scan
- [ ] `[CI/CD]` Add dependency audit
- [ ] `[CI/CD]` Add secret scanning
- [ ] `[Test]` Test security scan
- [ ] `[Librarian]` Register new file

---

### 5.2 Docker Production 🟠 HIGH

#### Task 5.2.1: Production Docker Compose
- [ ] `[Scaffold]` Create `docker-compose.prod.yml`
- [ ] `[Config]` Remove build contexts (use images)
- [ ] `[Config]` Add resource limits
- [ ] `[Config]` Add restart policies
- [ ] `[Config]` Add logging configuration
- [ ] `[Config]` Add healthcheck intervals
- [ ] `[Doc]` Document production deployment

#### Task 5.2.2: Health Check Endpoints
- [ ] `[Code]` Verify `backend/src/api/v1/health.py`
- [ ] `[Code]` Add database connectivity check
- [ ] `[Code]` Add Redis connectivity check
- [ ] `[Code]` Add ML service health proxy
- [ ] `[Test]` Test health endpoints

---

### 5.3 Monitoring 🟡 MEDIUM

#### Task 5.3.1: Add Logging Configuration
- [ ] `[Modify]` Open `backend/src/core/logging_config.py`
- [ ] `[Code]` Add JSON log format option
- [ ] `[Code]` Add request ID tracking
- [ ] `[Code]` Add user ID in logs
- [ ] `[Config]` Configure log rotation

#### Task 5.3.2: Add Metrics Endpoint
- [ ] `[Code]` Add `/metrics` endpoint
- [ ] `[Code]` Track request count
- [ ] `[Code]` Track request duration
- [ ] `[Code]` Track error count
- [ ] `[Doc]` Document metrics

---

### 5.4 Documentation 🟡 MEDIUM

#### Task 5.4.1: Update API Documentation
- [ ] `[Doc]` Verify OpenAPI spec is current
- [ ] `[Doc]` Add examples to all endpoints
- [ ] `[Doc]` Add error response documentation
- [ ] `[Doc]` Generate PDF from OpenAPI

#### Task 5.4.2: Create Deployment Runbook
- [ ] `[Doc]` Create `docs/DEPLOYMENT_RUNBOOK.md`
- [ ] `[Doc]` Document pre-deployment checklist
- [ ] `[Doc]` Document deployment steps
- [ ] `[Doc]` Document rollback procedures
- [ ] `[Doc]` Document emergency contacts

#### Task 5.4.3: Update README
- [ ] `[Doc]` Update version badges
- [ ] `[Doc]` Update installation instructions
- [ ] `[Doc]` Add troubleshooting section
- [ ] `[Doc]` Add FAQ section

---

## 📊 Task Summary

| Phase | Tasks | Subtasks | Priority |
|-------|-------|----------|----------|
| Phase 1: Code Stabilization | 12 | 47 | 🔴 CRITICAL |
| Phase 2: Security Hardening | 14 | 52 | 🔴 CRITICAL |
| Phase 3: ML Enhancement | 10 | 38 | 🟠 HIGH |
| Phase 4: Frontend Polish | 12 | 41 | 🟡 MEDIUM |
| Phase 5: Deployment | 10 | 35 | 🟠 HIGH |
| **TOTAL** | **58** | **213** | - |

---

## 🎯 Execution Order

### Week 1 (Critical Path)
```
Day 1: 1.1.1, 1.1.2, 1.1.3
Day 2: 1.2.1, 1.2.2
Day 3: 1.2.3, 1.3.1, 1.3.2
Day 4: 2.1.1, 2.1.2, 2.1.3
Day 5: 2.2.1, 2.2.2
Day 6: 2.2.3, 2.3.1
Day 7: 2.3.2, 2.4.1, 2.4.2
```

### Week 2 (ML Focus)
```
Day 8-9:   3.1.1, 3.1.2, 3.1.3
Day 10-11: 3.2.1, 3.2.2
Day 12-14: 3.3.1, 3.4.1, 3.4.2
```

### Week 3 (Polish)
```
Day 15-17: 4.1.1 - 4.1.6
Day 18-19: 4.2.1, 4.2.2, 4.2.3
Day 20-21: 4.3.1, 4.3.2
```

### Week 4 (Ship)
```
Day 22-24: 5.1.1, 5.1.2, 5.2.1, 5.2.2
Day 25-26: 5.3.1, 5.3.2
Day 27-28: 5.4.1, 5.4.2, 5.4.3
```

---

## ✅ Definition of Done

A task is DONE when:
- [ ] Code is written and passes linting
- [ ] Unit tests exist and pass
- [ ] Integration tests pass (if applicable)
- [ ] Documentation is updated
- [ ] File registry is updated
- [ ] PR is reviewed and merged

---

**Generated By:** The Project Manager (Speckit v35.0)  
**Date:** 2026-01-17

*"Every task is atomic. Every subtask is actionable. This is the Law."*
