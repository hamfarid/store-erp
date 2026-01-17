# PROJECT MAPS - Gaara ERP v12

**Generated**: 2025-11-18
**Purpose**: Comprehensive code maps for Backend, Frontend, and Database
**Status**: Initial Analysis

---

## 1. BACKEND ARCHITECTURE MAP

### 1.1 Module Structure (70+ Modules)

#### Core Modules (16 modules)
- **core_modules.core** - Base models, utilities, authentication
- **core_modules.companies** - Multi-company/branch management (33 incoming deps)
- **core_modules.organization** - Organization structure (25 incoming deps)
- **core_modules.permissions** - RBAC system (9 incoming deps)
- **core_modules.users** - User management
- **core_modules.rag** - RAG (Retrieval-Augmented Generation) system (10 incoming deps)
- **core_modules.settings** - System configuration
- **core_modules.audit** - Audit logging
- **core_modules.notifications** - Notification system
- **core_modules.reports** - Reporting engine
- **core_modules.search** - Search functionality
- **core_modules.workflow** - Workflow engine
- **core_modules.api** - API gateway
- **core_modules.cache** - Caching layer
- **core_modules.queue** - Task queue
- **core_modules.storage** - File storage

#### Business Modules (10 modules)
- **business_modules.accounting** - Accounting system (19 incoming deps)
- **business_modules.inventory** - Inventory management (26 incoming deps - HIGHEST)
- **business_modules.sales** - Sales management (11 incoming deps)
- **business_modules.purchasing** - Purchasing system (10 incoming deps)
- **business_modules.pos** - Point of Sale
- **business_modules.production** - Production management
- **business_modules.rental** - Rental management
- **business_modules.solar_stations** - Solar energy projects
- **business_modules.contacts** - Contact management (16 incoming deps)
- **business_modules.banking_payments** - Banking & payments

#### Agricultural Modules (7 modules)
- **agricultural_modules.farms** - Farm management (9 incoming deps)
- **agricultural_modules.nurseries** - Nursery management (7 incoming deps)
- **agricultural_modules.seed_production** - Seed production tracking
- **agricultural_modules.experiments** - Agricultural experiments
- **agricultural_modules.plant_diagnosis** - AI-powered plant disease diagnosis
- **agricultural_modules.research** - Research management
- **agricultural_modules.variety_trials** - Variety trial tracking

#### Services Modules (24 modules)
- **services_modules.projects** - Project management
- **services_modules.hr** - Human resources
- **services_modules.marketing** - Marketing campaigns
- **services_modules.legal** - Legal document management
- **services_modules.quality** - Quality assurance
- **services_modules.assets** - Asset management
- **services_modules.fleet** - Fleet management
- **services_modules.forecast** - Forecasting system (7 outgoing deps)
- **services_modules.workflows** - Workflow integration (7 outgoing deps)
- **services_modules.crm** - Customer relationship management
- **services_modules.helpdesk** - Support ticketing
- **services_modules.maintenance** - Maintenance scheduling
- **services_modules.contracts** - Contract management
- **services_modules.insurance** - Insurance tracking
- **services_modules.training** - Training management
- **services_modules.recruitment** - Recruitment system
- **services_modules.performance** - Performance evaluation
- **services_modules.payroll** - Payroll processing
- **services_modules.attendance** - Attendance tracking
- **services_modules.leave** - Leave management
- **services_modules.expenses** - Expense tracking
- **services_modules.budgeting** - Budget management
- **services_modules.procurement** - Procurement system
- **services_modules.logistics** - Logistics management

#### Integration Modules (7 modules)
- **integration_modules.telegram_bot** - Telegram integration
- **integration_modules.api_advanced** - Advanced API features
- **integration_modules.ai_analytics** - AI analytics (8 outgoing deps)
- **integration_modules.cloud_services** - Cloud service integration
- **integration_modules.payment_gateways** - Payment gateway integration
- **integration_modules.shipping** - Shipping provider integration
- **integration_modules.social_media** - Social media integration

#### AI Modules (3 modules)
- **ai_modules.assistant** - AI assistant
- **ai_modules.dashboard** - AI-powered dashboard
- **ai_modules.engine** - AI processing engine

#### Admin/Helper Modules (5 modules)
- **admin_modules.custom_admin** - Custom admin interface
- **admin_modules.dashboard** - Admin dashboard
- **admin_modules.communication** - Communication system
- **admin_modules.data_import_export** - Data import/export
- **helper_modules.utilities** - Utility functions

### 1.2 Dependency Analysis

**Total Modules**: 1570 (including sub-modules)
**Total Dependency Edges**: 501

**Top Dependencies (Incoming)**:
1. core_modules.core.models - 36 dependencies
2. core_modules.companies.models - 33 dependencies
3. business_modules.inventory.models - 26 dependencies
4. core_modules.organization.models - 25 dependencies
5. business_modules.accounting.models - 19 dependencies

**Critical Integration Points**:
- All business modules depend on core_modules.core.models
- Multi-company support via core_modules.companies
- Inventory is central to business operations (26 deps)

### 1.3 Known Issues (UPDATED 2025-11-18)

**Duplicate Models** (CONFIRMED via Class Registry):
- **User**: 3 locations (canonical: core_modules.users, duplicates: users_accounts proxy, api_server)
- **Company**: 3 locations (canonical: core.models, duplicates: organization.models, services_modules)
- **SalesInvoice**: 2 locations (canonical: accounting.invoices, duplicate: sales.models)
- **PurchaseInvoice**: 3 locations (canonical: accounting.invoices, duplicates: purchasing.models x2)
- **Total**: 7 duplicate model definitions identified

**Security Status** (UPDATED after deep analysis):
- ✅ CSRF protection: ENABLED (contrary to initial report)
- ⚠️ JWT tokens: CONFLICTING configs (30min, 60min, 3600sec in 3 different files)
- ❌ Refresh token rotation: Enabled in settings but config conflicts exist
- ✅ Rate limiting: IMPLEMENTED (5 attempts/5min on auth endpoints)
- ❌ Hardcoded secrets: FOUND in 3 locations (api_gateway, settings/base.py)
- ⚠️ Account lockout: Field exists but logic NOT implemented
- ✅ Password hashing: Argon2 (EXCELLENT)
- ✅ Security headers: Middleware exists (HSTS, CSP, X-Frame-Options)

---

## 2. FRONTEND ARCHITECTURE MAP

### 2.1 Technology Stack
- **Framework**: React 19.1.0
- **Build Tool**: Vite
- **Styling**: Tailwind CSS (assumed)
- **State Management**: TBD (needs analysis)
- **API Client**: Axios (assumed)

### 2.2 Directory Structure
```
gaara-erp-frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   ├── api/            # API client
│   ├── hooks/          # Custom hooks
│   ├── utils/          # Utilities
│   ├── types/          # TypeScript types
│   └── locales/        # i18n translations (ar/en)
├── public/             # Static assets
└── vite.config.js      # Vite configuration
```

### 2.3 Required Analysis
- [ ] Component hierarchy mapping
- [ ] State flow analysis
- [ ] API call mapping
- [ ] Route structure
- [ ] Permission guards implementation

---

## 3. DATABASE SCHEMA MAP

### 3.1 Database Technology
- **Development**: SQLite
- **Production**: PostgreSQL 13+
- **ORM**: Django ORM (SQLAlchemy-like)

### 3.2 Core Tables (Estimated 100+ tables)

**Core Tables**:
- users
- companies
- branches
- permissions
- roles
- audit_logs

**Business Tables**:
- accounts
- invoices
- products
- inventory_items
- warehouses
- sales_orders
- purchase_orders

**Agricultural Tables**:
- farms
- nurseries
- seeds
- experiments
- plant_diagnoses

### 3.3 Known Issues
- Missing foreign key constraints (Task #30)
- Missing indexes on frequently queried columns (Task #31)
- No migration system (Alembic not initialized - Task #28)
- Duplicate model definitions

---

## 4. API ARCHITECTURE MAP

### 4.1 API Structure
- **Protocol**: REST
- **Authentication**: JWT (Bearer tokens)
- **Base URL**: /api/v1/ (assumed)

### 4.2 Endpoint Categories
- /api/auth/ - Authentication
- /api/users/ - User management
- /api/companies/ - Company management
- /api/inventory/ - Inventory operations
- /api/sales/ - Sales operations
- /api/accounting/ - Accounting operations
- /api/reports/ - Reporting
- /api/ai/ - AI features

### 4.3 Required Documentation
- [ ] OpenAPI 3.0 specification (Task #24)
- [ ] API contracts documentation
- [ ] Error code catalog
- [ ] Rate limiting policies

---

## 5. NEXT STEPS

1. **Immediate** (Phase 1):
   - Complete detailed backend class mapping
   - Analyze frontend component structure
   - Generate database ERD
   - Document all API endpoints

2. **Phase 2** (Planning):
   - Prioritize security fixes (P0 tasks)
   - Plan database migration strategy
   - Design API governance framework

3. **Phase 3** (Implementation):
   - Execute P0 security fixes
   - Consolidate duplicate models
   - Implement missing constraints

---

**Last Updated**: 2025-11-18 09:15
**Next Update**: After detailed code analysis

