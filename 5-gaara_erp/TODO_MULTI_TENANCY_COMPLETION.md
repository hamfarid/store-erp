# Multi-Tenancy Completion Task List
# قائمة مهام إكمال تعدد المستأجرين

**Created:** 2026-01-17
**Status:** IN PROGRESS
**Priority:** CRITICAL

---

## 📊 Progress Overview

| Category | Tasks | Completed | Remaining |
|----------|-------|-----------|-----------|
| Backend Models | 5 | ✅ 5 | 0 |
| Backend API | 8 | ⏳ 2 | 6 |
| Database | 5 | ⏳ 1 | 4 |
| Frontend | 6 | ⏳ 1 | 5 |
| Integration | 7 | 0 | 7 |
| **Total** | **31** | **9** | **22** |

---

## 🔴 Backend - API Routes (Flask Blueprint)

### TASK-B01: Convert Django Routes to Flask Blueprint ⚠️ CRITICAL
**Status:** PENDING
**Files:** `backend/src/routes/tenant_routes.py`

```python
# Current: Django REST Framework views
# Needed: Flask Blueprint with Flask-Smorest

# Changes required:
- [ ] Convert APIView to Flask Blueprint
- [ ] Use @blp.route() decorators
- [ ] Use marshmallow schemas instead of DRF serializers
- [ ] Add Flask-Smorest API documentation
```

### TASK-B02: Create Tenant Marshmallow Schemas
**Status:** PENDING
**Files to create:** `backend/src/schemas/tenant_schemas.py`

```python
# Required schemas:
- [ ] TenantSchema (full)
- [ ] TenantCreateSchema
- [ ] TenantUpdateSchema
- [ ] TenantUserSchema
- [ ] TenantSettingsSchema
- [ ] TenantPlanSchema
```

### TASK-B03: Register Tenant Blueprint in main.py
**Status:** PENDING
**File:** `backend/src/main.py`

```python
# Add to blueprints_to_import list:
("routes.tenant_routes", "tenant_bp"),

# Or register manually:
from routes.tenant_routes import tenant_bp
app.register_blueprint(tenant_bp)
```

### TASK-B04: Create Tenant Admin Routes
**Status:** PENDING
**File:** `backend/src/routes/tenant_admin_routes.py`

```python
# Admin-only endpoints:
- [ ] GET /api/admin/tenants/stats
- [ ] POST /api/admin/tenants/{id}/suspend
- [ ] POST /api/admin/tenants/{id}/activate
- [ ] GET /api/admin/tenants/{id}/audit-log
```

### TASK-B05: Create Tenant Invitation Routes
**Status:** PENDING
**File:** Add to `tenant_routes.py`

```python
- [ ] POST /api/tenants/{id}/invitations
- [ ] GET /api/tenants/{id}/invitations
- [ ] DELETE /api/tenants/{id}/invitations/{inv_id}
- [ ] POST /api/tenants/invitations/accept
```

### TASK-B06: Create Tenant Quota Tracking
**Status:** PENDING
**File:** `backend/src/services/quota_service.py`

```python
- [ ] Track storage usage per tenant
- [ ] Track API calls per day
- [ ] Track user count
- [ ] Implement quota alerts
```

---

## 🟠 Database - Models & Migrations

### TASK-D01: Convert Django Models to SQLAlchemy
**Status:** PENDING
**Files:** `backend/src/models/tenant.py`

```python
# Convert from Django ORM to SQLAlchemy:
- [ ] TenantPlan -> SQLAlchemy model
- [ ] Tenant -> SQLAlchemy model
- [ ] TenantUser -> SQLAlchemy model
- [ ] TenantSettings -> SQLAlchemy model
- [ ] TenantInvitation -> SQLAlchemy model
```

### TASK-D02: Create Database Migrations
**Status:** PENDING
**Tool:** Alembic or Flask-Migrate

```bash
# Migration files needed:
- [ ] Create tenant_plans table
- [ ] Create tenants table
- [ ] Create tenant_users table
- [ ] Create tenant_settings table
- [ ] Create tenant_invitations table
- [ ] Add indexes
```

### TASK-D03: Implement Schema-Based Isolation
**Status:** PENDING
**File:** `backend/src/database/tenant_schema.py`

```python
# Functions needed:
- [ ] create_tenant_schema(schema_name)
- [ ] drop_tenant_schema(schema_name)
- [ ] clone_schema_structure(template, target)
- [ ] migrate_tenant_schema(schema_name)
```

### TASK-D04: Create Seed Data for Plans
**Status:** PENDING
**File:** `backend/src/database/seeds/tenant_plans.py`

```python
# Default plans:
- [ ] Free plan (5 users, 1GB)
- [ ] Starter plan (10 users, 5GB)
- [ ] Professional plan (50 users, 50GB)
- [ ] Enterprise plan (unlimited)
```

### TASK-D05: Add Tenant Foreign Keys to Existing Tables
**Status:** PENDING

```sql
-- Tables to modify:
- [ ] users -> add tenant_id
- [ ] products -> add tenant_id
- [ ] invoices -> add tenant_id
- [ ] (all business tables)
```

---

## 🟡 Frontend - React Components

### TASK-F01: Connect MultiTenancyPage to Real API ⚠️ CRITICAL
**Status:** PENDING
**File:** `gaara-erp-frontend/src/pages/core/MultiTenancyPage.jsx`

```javascript
// Changes required:
- [ ] Import tenantService
- [ ] Replace mockTenants with API call
- [ ] Update loadTenants() to use tenantService.getTenants()
- [ ] Update handleSave() to use tenantService.createTenant/updateTenant
- [ ] Update handleDelete() to use tenantService.deleteTenant
- [ ] Add error handling with toast notifications
- [ ] Add loading states
```

### TASK-F02: Create Tenant Users Management Component
**Status:** PENDING
**File:** `gaara-erp-frontend/src/components/tenants/TenantUsersDialog.jsx`

```javascript
// Features:
- [ ] List tenant users
- [ ] Add user to tenant
- [ ] Change user role
- [ ] Remove user from tenant
- [ ] Send invitation
```

### TASK-F03: Create Tenant Settings Component
**Status:** PENDING
**File:** `gaara-erp-frontend/src/components/tenants/TenantSettingsDialog.jsx`

```javascript
// Settings sections:
- [ ] General settings (timezone, language)
- [ ] Security settings (MFA requirement)
- [ ] Notification settings
- [ ] Module configuration
```

### TASK-F04: Create Tenant Selector Component
**Status:** PENDING
**File:** `gaara-erp-frontend/src/components/layout/TenantSelector.jsx`

```javascript
// Features:
- [ ] Dropdown to switch between tenants
- [ ] Show current tenant name/logo
- [ ] Quick tenant search
- [ ] Create new tenant link
```

### TASK-F05: Create Invitation Management Component
**Status:** PENDING
**File:** `gaara-erp-frontend/src/components/tenants/TenantInvitations.jsx`

```javascript
// Features:
- [ ] List pending invitations
- [ ] Send new invitation form
- [ ] Resend invitation
- [ ] Cancel invitation
```

### TASK-F06: Add Tenant Context Provider
**Status:** PENDING
**File:** `gaara-erp-frontend/src/contexts/TenantContext.jsx`

```javascript
// Context provides:
- [ ] currentTenant
- [ ] setCurrentTenant
- [ ] tenants list
- [ ] refreshTenants
- [ ] tenant permissions
```

---

## 🟢 Integration & Connections

### TASK-I01: Add Tenant Middleware to Flask App
**Status:** PENDING
**File:** `backend/src/main.py`

```python
# Add middleware:
- [ ] Import TenantMiddleware
- [ ] Register as Flask middleware
- [ ] Configure exempt paths
```

### TASK-I02: Update Auth to Include Tenant
**Status:** PENDING
**File:** `backend/src/auth.py`

```python
# Changes:
- [ ] Include tenant_id in JWT token
- [ ] Validate user belongs to tenant
- [ ] Add tenant permission checks
```

### TASK-I03: Create API Response Wrapper
**Status:** PENDING
**File:** `backend/src/utils/response.py`

```python
# Standardized responses:
- [ ] success_response(data, message)
- [ ] error_response(error, message, message_ar)
- [ ] paginated_response(data, total, page)
```

### TASK-I04: Add Tenant Headers to Frontend Requests
**Status:** PENDING
**File:** `gaara-erp-frontend/src/services/api.js`

```javascript
// Axios interceptor:
- [ ] Add X-Tenant-ID header to all requests
- [ ] Read from localStorage or context
- [ ] Handle tenant switching
```

### TASK-I05: Create E2E Tests for Multi-Tenancy
**Status:** PENDING
**File:** `e2e/multi-tenancy.spec.ts`

```typescript
// Test scenarios:
- [ ] Create tenant
- [ ] Switch tenant
- [ ] Tenant data isolation
- [ ] User permissions per tenant
- [ ] Quota enforcement
```

### TASK-I06: Create Backend Integration Tests
**Status:** PENDING
**File:** `backend/tests/test_tenant_integration.py`

```python
# Test scenarios:
- [ ] Schema creation
- [ ] Data isolation
- [ ] Middleware routing
- [ ] API authentication
```

### TASK-I07: Add Caching for Tenant Lookups
**Status:** PENDING
**File:** `backend/src/services/tenant_cache.py`

```python
# Caching strategy:
- [ ] Cache tenant by ID (5 min)
- [ ] Cache tenant by slug (5 min)
- [ ] Cache tenant by domain (5 min)
- [ ] Invalidate on update
```

---

## 📋 Implementation Order (Recommended)

### Phase 1: Database Foundation (Day 1-2)
1. TASK-D01: Convert Models to SQLAlchemy
2. TASK-D02: Create Migrations
3. TASK-D04: Seed Plans Data

### Phase 2: Backend API (Day 3-4)
4. TASK-B01: Convert to Flask Blueprint
5. TASK-B02: Create Schemas
6. TASK-B03: Register Blueprint

### Phase 3: Frontend Connection (Day 5-6)
7. TASK-F01: Connect MultiTenancyPage
8. TASK-F06: Create TenantContext
9. TASK-I04: Add Tenant Headers

### Phase 4: Integration (Day 7-8)
10. TASK-I01: Add Middleware
11. TASK-I02: Update Auth
12. TASK-I03: Response Wrapper

### Phase 5: Advanced Features (Day 9-10)
13. TASK-F02: User Management
14. TASK-F03: Settings Component
15. TASK-F04: Tenant Selector

### Phase 6: Testing & Polish (Day 11-12)
16. TASK-I05: E2E Tests
17. TASK-I06: Integration Tests
18. TASK-D03: Schema Isolation

---

## ⚡ Quick Start - First 3 Tasks

To start immediately, complete these in order:

```bash
# 1. Convert models (TASK-D01)
# Edit: backend/src/models/tenant.py

# 2. Create Flask Blueprint (TASK-B01)
# Edit: backend/src/routes/tenant_routes.py

# 3. Connect Frontend (TASK-F01)
# Edit: gaara-erp-frontend/src/pages/core/MultiTenancyPage.jsx
```

---

**Next Action:** Start with TASK-D01 (Convert Models to SQLAlchemy)
