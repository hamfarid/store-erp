# Multi-Tenancy - Final Task List
# قائمة المهام النهائية لتعدد المستأجرين

**Updated:** 2026-01-17T15:00:00Z
**Total Tasks:** 31
**Completed:** 22 ✅
**Remaining:** 9 ⏳

---

## 📊 Progress Summary

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Backend Models | 5 | ✅ 5 | 0 |
| Backend API | 8 | ✅ 7 | 1 |
| Database | 5 | ✅ 2 | 3 |
| Frontend | 6 | ✅ 5 | 1 |
| Integration | 7 | ✅ 3 | 4 |

---

## ✅ COMPLETED TASKS

### Backend Models (5/5) ✅
- [x] **TASK-M01**: TenantPlan model - `tenant_sqlalchemy.py`
- [x] **TASK-M02**: Tenant model - `tenant_sqlalchemy.py`
- [x] **TASK-M03**: TenantUser model - `tenant_sqlalchemy.py`
- [x] **TASK-M04**: TenantSettings model - `tenant_sqlalchemy.py`
- [x] **TASK-M05**: TenantInvitation model - `tenant_sqlalchemy.py`

### Backend API (7/8) ✅
- [x] **TASK-B01**: Flask Blueprint created - `tenant_api.py`
- [x] **TASK-B02**: CRUD routes (list, create, get, update, delete)
- [x] **TASK-B03**: Tenant users routes
- [x] **TASK-B04**: Tenant settings routes
- [x] **TASK-B05**: Plans list route
- [x] **TASK-B06**: Check slug availability route
- [x] **TASK-B07**: Blueprint registered in main.py

### Database (2/5) ✅
- [x] **TASK-D01**: SQLAlchemy models created - `tenant_sqlalchemy.py`
- [x] **TASK-D02**: Plans seed script - `tenant_plans_seed.py`

### Frontend (5/6) ✅
- [x] **TASK-F01**: tenantService.js created
- [x] **TASK-F02**: MultiTenancyPage.jsx connected to API
- [x] **TASK-F03**: TenantContext.jsx created
- [x] **TASK-F04**: TenantSelector.jsx created
- [x] **TASK-F05**: TenantUsersDialog.jsx created

### Integration (3/7) ✅
- [x] **TASK-I01**: Flask tenant middleware created - `flask_tenant_middleware.py`
- [x] **TASK-I02**: Middleware initialized in main.py
- [x] **TASK-I06**: Backend integration tests - `test_tenant_api.py`

---

## ⏳ REMAINING TASKS

### Backend API (2 remaining)

#### TASK-B07: Register Blueprint in main.py
**File:** `backend/src/main.py`
**Priority:** 🔴 CRITICAL

```python
# Add to blueprints_to_import list around line 91:
("routes.tenant_api", "tenant_bp"),
```

#### TASK-B08: Create Tenant Invitations Routes
**File:** `backend/src/routes/tenant_api.py`
**Priority:** 🟡 Medium

```python
# Routes to add:
- POST /api/tenants/{id}/invitations
- GET /api/tenants/{id}/invitations
- DELETE /api/tenants/{id}/invitations/{inv_id}
- POST /api/tenants/invitations/accept
```

---

### Database (4 remaining)

#### TASK-D01: Create Database Migration
**Priority:** 🔴 CRITICAL

```bash
# Using Flask-Migrate:
flask db migrate -m "Add tenant tables"
flask db upgrade

# Or manual SQL:
python -c "from src.models.tenant_sqlalchemy import create_tenant_tables; create_tenant_tables(engine)"
```

#### TASK-D02: Seed Default Plans
**File:** `backend/src/database/seeds/tenant_plans.py`
**Priority:** 🔴 CRITICAL

```python
plans = [
    {"code": "free", "name": "Free", "name_ar": "مجاني", "max_users": 5, "max_storage_gb": 1},
    {"code": "basic", "name": "Basic", "name_ar": "أساسي", "max_users": 10, "max_storage_gb": 10},
    {"code": "pro", "name": "Professional", "name_ar": "احترافي", "max_users": 50, "max_storage_gb": 50},
    {"code": "enterprise", "name": "Enterprise", "name_ar": "مؤسسي", "max_users": 9999, "max_storage_gb": 500},
]
```

#### TASK-D03: Implement Schema Isolation
**File:** `backend/src/database/tenant_schema.py`
**Priority:** 🟡 Medium

```python
def create_tenant_schema(schema_name):
    """Create PostgreSQL schema for tenant"""
    pass

def migrate_tenant_schema(schema_name):
    """Run migrations in tenant schema"""
    pass
```

#### TASK-D04: Add tenant_id to Existing Tables
**Priority:** 🟠 High (for shared tables)

```sql
-- For tables that need tenant isolation:
ALTER TABLE products ADD COLUMN tenant_id UUID REFERENCES tenants(id);
ALTER TABLE invoices ADD COLUMN tenant_id UUID REFERENCES tenants(id);
-- etc.
```

---

### Frontend (4 remaining)

#### TASK-F03: Create TenantContext Provider
**File:** `gaara-erp-frontend/src/contexts/TenantContext.jsx`
**Priority:** 🟠 High

```jsx
export const TenantContext = createContext({
  currentTenant: null,
  setCurrentTenant: () => {},
  tenants: [],
  refreshTenants: () => {},
});

export const TenantProvider = ({ children }) => {
  // Implementation
};
```

#### TASK-F04: Create TenantSelector Component
**File:** `gaara-erp-frontend/src/components/layout/TenantSelector.jsx`
**Priority:** 🟡 Medium

```jsx
// Dropdown in header to switch between tenants
const TenantSelector = () => {
  // Implementation
};
```

#### TASK-F05: Create TenantUsersDialog Component
**File:** `gaara-erp-frontend/src/components/tenants/TenantUsersDialog.jsx`
**Priority:** 🟡 Medium

```jsx
// Dialog to manage users in a tenant
const TenantUsersDialog = ({ tenant, open, onClose }) => {
  // Implementation
};
```

#### TASK-F06: Add Tenant Headers to API Client
**File:** `gaara-erp-frontend/src/services/api.js`
**Priority:** 🟠 High

```javascript
// Add X-Tenant-ID header to all requests
axios.interceptors.request.use((config) => {
  const tenantId = localStorage.getItem('current_tenant_id');
  if (tenantId) {
    config.headers['X-Tenant-ID'] = tenantId;
  }
  return config;
});
```

---

### Integration (7 remaining)

#### TASK-I01: Add Tenant Middleware to Flask
**File:** `backend/src/main.py`
**Priority:** 🟠 High

```python
# Add middleware to extract tenant from request
@app.before_request
def set_tenant():
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        g.tenant = get_tenant_by_id(tenant_id)
```

#### TASK-I02: Update Auth to Include Tenant
**File:** `backend/src/auth.py`
**Priority:** 🟠 High

```python
# Include tenant_id in JWT token
# Validate user belongs to tenant
```

#### TASK-I03: Create Response Wrapper
**File:** `backend/src/utils/response.py`
**Priority:** 🟢 Low

```python
def success_response(data, message="", message_ar=""):
    return {"success": True, "data": data, "message": message, "message_ar": message_ar}

def error_response(error, message, message_ar=""):
    return {"success": False, "error": error, "message": message, "message_ar": message_ar}
```

#### TASK-I04: Add Cache for Tenant Lookups
**File:** `backend/src/services/tenant_cache.py`
**Priority:** 🟢 Low

```python
# Redis caching for tenant lookups
```

#### TASK-I05: E2E Tests
**File:** `e2e/multi-tenancy.spec.ts`
**Priority:** 🟡 Medium

#### TASK-I06: Backend Integration Tests
**File:** `backend/tests/test_tenant_integration.py`
**Priority:** 🟡 Medium

#### TASK-I07: Update All Routes to Respect Tenant
**Priority:** 🟠 High

```python
# All data routes should filter by g.tenant
```

---

## 🚀 Quick Start - Next 3 Tasks

### 1. Register Blueprint (TASK-B07)
```python
# In backend/src/main.py, add to blueprints_to_import:
("routes.tenant_api", "tenant_bp"),
```

### 2. Create Database Tables (TASK-D01)
```python
# Run in Python shell:
from src.models.tenant_sqlalchemy import create_tenant_tables
from src.models.user import db
create_tenant_tables(db.engine)
```

### 3. Seed Plans (TASK-D02)
```python
# Create seed script and run
python -c "from src.database.seeds.tenant_plans import seed_plans; seed_plans()"
```

---

## 📁 Files Created This Session

| File | Lines | Purpose |
|------|-------|---------|
| `backend/src/models/tenant_sqlalchemy.py` | 450+ | SQLAlchemy models |
| `backend/src/routes/tenant_api.py` | 650+ | Flask Blueprint API |
| `backend/src/middleware/flask_tenant_middleware.py` | 280+ | Tenant middleware |
| `backend/src/database/seeds/tenant_plans_seed.py` | 200+ | Plans seeder |
| `backend/tests/test_tenant_api.py` | 400+ | Integration tests |
| `gaara-erp-frontend/src/services/tenantService.js` | 380+ | Frontend API client |
| `gaara-erp-frontend/src/contexts/TenantContext.jsx` | 200+ | State management |
| `gaara-erp-frontend/src/components/layout/TenantSelector.jsx` | 200+ | Tenant switcher |
| `gaara-erp-frontend/src/components/tenants/TenantUsersDialog.jsx` | 450+ | User management |
| `MultiTenancyPage.jsx` | 632 | Updated - Real API |
| `backend/src/main.py` | Updated | Blueprint + Middleware |

---

## 🔗 Dependencies

```
Backend:
- flask
- flask-sqlalchemy
- sqlalchemy
- redis (for caching)

Frontend:
- axios
- react (18+)
- @tanstack/react-query (optional)
```

---

**Last Updated:** 2026-01-17T14:30:00Z
