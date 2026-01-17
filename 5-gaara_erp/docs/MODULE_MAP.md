# Module Map - Gaara ERP v12

## Project: Gaara ERP v12
**Type:** Full-Stack ERP System
**Framework:** Django 4.2 (Backend) + React 19.1.0 (Frontend)
**Last Updated:** 2025-11-28

## Architecture Overview

Gaara ERP v12 follows a **modular monolithic architecture** with clear separation between:
- **Backend (Django):** 70+ modules organized by domain (core, business, agricultural, services, integration, AI)
- **Frontend (React):** Component-based architecture with shared UI library
- **Database:** SQLite (dev) / PostgreSQL (prod) with Django ORM

---

## Directory Structure

```
Gaara_erp/
├── gaara_erp/                    # Main Django project
│   ├── gaara_erp/               # Django settings and configuration
│   │   ├── settings/            # Split settings (base, development, production)
│   │   ├── urls.py              # Root URL configuration
│   │   └── wsgi.py              # WSGI application
│   │
│   ├── core_modules/            # Core system functionality (16 modules)
│   │   ├── core/                # Base models, utilities, constants
│   │   ├── users/               # User management (CANONICAL)
│   │   ├── companies/           # Multi-company management
│   │   ├── organization/        # Organization structure
│   │   ├── permissions/         # RBAC permission system
│   │   ├── rag/                 # RAG (Retrieval-Augmented Generation)
│   │   ├── security/            # Security middleware and services
│   │   └── ...                  # Other core modules
│   │
│   ├── business_modules/        # Business domain modules (10 modules)
│   │   ├── accounting/          # Accounting (invoices, payments, journal)
│   │   ├── inventory/           # Inventory management
│   │   ├── sales/               # Sales operations
│   │   ├── purchasing/          # Purchasing and procurement
│   │   ├── pos/                 # Point of Sale
│   │   ├── production/          # Manufacturing
│   │   ├── rent/                # Rental management
│   │   └── ...                  # Other business modules
│   │
│   ├── agricultural_modules/    # Agricultural domain (7 modules)
│   │   ├── farms/               # Farm management
│   │   ├── nurseries/           # Nursery management
│   │   ├── seed_production/     # Seed production tracking
│   │   ├── experiments/         # Agricultural experiments
│   │   └── ...                  # Other ag modules
│   │
│   ├── services_modules/        # Service domain (24 modules)
│   │   ├── projects/            # Project management
│   │   ├── hr/                  # Human resources
│   │   ├── crm/                 # Customer relationship
│   │   └── ...                  # Other service modules
│   │
│   ├── integration_modules/     # External integrations (7 modules)
│   │   ├── telegram_bot/        # Telegram integration
│   │   ├── ai_analytics/        # AI analytics
│   │   └── ...                  # Other integrations
│   │
│   ├── ai_modules/              # AI functionality (3 modules)
│   │   ├── assistant/           # AI assistant
│   │   ├── dashboard/           # AI-powered dashboard
│   │   └── engine/              # AI processing engine
│   │
│   ├── admin_modules/           # Admin functionality (5 modules)
│   │   ├── custom_admin/        # Custom Django admin
│   │   ├── dashboard/           # Admin dashboard
│   │   └── ...                  # Other admin modules
│   │
│   └── main-frontend/           # Embedded React components per module
│
├── gaara-erp-frontend/          # Standalone React frontend
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── contexts/            # React contexts (Auth, Theme, Notification)
│   │   ├── hooks/               # Custom hooks
│   │   └── main.jsx             # Entry point
│   └── package.json
│
├── docs/                        # Project documentation
├── logs/                        # System logs
├── .memory/                     # AI agent memory system
└── github/global/               # Global professional prompt system
```

---

## Frontend Modules

### Pages

| Page | Path | Route | Components Used | API Calls |
|------|------|-------|-----------------|-----------|
| Login | `components/LoginPage.jsx` | `/login` | Form, Button, Input | `POST /api/auth/login` |
| Dashboard | `components/Dashboard.jsx` | `/dashboard` | Header, Sidebar, Cards | `GET /api/dashboard/stats` |
| Accounting | `components/AccountingModule.jsx` | `/accounting` | Tables, Charts | `GET /api/accounting/*` |
| Inventory | `components/InventoryManagement.jsx` | `/inventory` | DataGrid, Forms | `GET /api/inventory/*` |
| Sales | `components/SalesModule.jsx` | `/sales` | Tables, Forms | `GET /api/sales/*` |
| AI Analytics | `components/AIAnalytics.jsx` | `/ai-analytics` | Charts, Cards | `GET /api/ai/analytics` |
| IoT Monitoring | `components/IoTMonitoring.jsx` | `/iot` | Gauges, Charts | `GET /api/iot/*` |

### Components

| Component | Path | Used By | Props | State |
|-----------|------|---------|-------|-------|
| Header | `components/Header.jsx` | All pages | `user`, `onLogout` | `isMenuOpen` |
| Sidebar | `components/Sidebar.jsx` | Dashboard, Modules | `activeMenu` | `collapsed` |
| LoadingScreen | `components/LoadingScreen.jsx` | App.jsx | - | - |
| UI Components | `components/ui/*.jsx` | All modules | Various | Various |

### UI Library (50+ components)

| Category | Components |
|----------|------------|
| Layout | `accordion`, `card`, `collapsible`, `drawer`, `resizable`, `separator`, `sheet`, `sidebar` |
| Form | `button`, `checkbox`, `form`, `input`, `input-otp`, `label`, `radio-group`, `select`, `slider`, `switch`, `textarea`, `toggle` |
| Data Display | `avatar`, `badge`, `calendar`, `carousel`, `chart`, `pagination`, `progress`, `skeleton`, `table`, `tabs` |
| Feedback | `alert`, `alert-dialog`, `dialog`, `popover`, `sonner`, `tooltip` |
| Navigation | `breadcrumb`, `command`, `context-menu`, `dropdown-menu`, `menubar`, `navigation-menu` |

### Contexts

| Context | Path | Purpose | Exports |
|---------|------|---------|---------|
| AuthContext | `contexts/AuthContext.jsx` | Authentication state | `useAuth`, `AuthProvider`, `login`, `logout`, `user` |
| ThemeContext | `contexts/ThemeContext.jsx` | Theme management | `useTheme`, `ThemeProvider`, `theme`, `toggleTheme` |
| NotificationContext | `contexts/NotificationContext.jsx` | Notifications | `useNotification`, `notify`, `notifications` |

---

## Backend Modules

### Routes

| Route | Path | Methods | Controller | Middleware |
|-------|------|---------|------------|------------|
| Auth | `core_modules/users/urls.py` | POST /login, /register, /logout | UserViewSet | - |
| Users | `core_modules/users/urls.py` | GET, POST, PUT, DELETE /users | UserViewSet | authMiddleware |
| Companies | `core_modules/companies/urls.py` | GET, POST, PUT, DELETE /companies | CompanyViewSet | authMiddleware |
| Inventory | `business_modules/inventory/urls.py` | GET, POST, PUT, DELETE /inventory | InventoryViewSet | authMiddleware |
| Sales | `business_modules/sales/urls.py` | GET, POST, PUT, DELETE /sales | SalesViewSet | authMiddleware |
| Purchasing | `business_modules/purchasing/urls.py` | GET, POST, PUT, DELETE /purchasing | PurchasingViewSet | authMiddleware |
| Accounting | `business_modules/accounting/urls.py` | GET, POST, PUT, DELETE /accounting | AccountingViewSet | authMiddleware |

### Controllers (Views in Django)

| Controller | Path | Methods | Services Used |
|------------|------|---------|---------------|
| UserViewSet | `core_modules/users/views.py` | `list`, `create`, `retrieve`, `update`, `destroy` | UserService |
| CompanyViewSet | `core_modules/companies/views.py` | `list`, `create`, `retrieve`, `update`, `destroy` | CompanyService |
| InventoryViewSet | `business_modules/inventory/views.py` | `list`, `create`, `retrieve`, `update`, `destroy` | InventoryService |
| SalesViewSet | `business_modules/sales/views.py` | `list`, `create`, `retrieve`, `update`, `destroy` | SalesService |
| AccountingViewSet | `business_modules/accounting/views.py` | `list`, `create`, `retrieve`, `update`, `destroy` | AccountingService |

### Services

| Service | Path | Purpose | Methods |
|---------|------|---------|---------|
| UserService | `core_modules/users/services.py` | User business logic | `create_user`, `update_user`, `delete_user`, `authenticate` |
| CompanyService | `core_modules/companies/services.py` | Company management | `create_company`, `update_company`, `get_branches` |
| InventoryService | `business_modules/inventory/services.py` | Inventory operations | `add_stock`, `remove_stock`, `transfer`, `get_valuation` |
| SalesService | `business_modules/sales/services.py` | Sales operations | `create_order`, `process_payment`, `generate_invoice` |
| AccountingService | `business_modules/accounting/services.py` | Accounting operations | `create_entry`, `post_invoice`, `reconcile` |

### Models (Core)

| Model | Path | Table | Key Fields | Relationships |
|-------|------|-------|------------|---------------|
| User | `core_modules/users/models.py` | `users` | `id`, `email`, `username`, `password`, `is_active` | hasMany(Sessions), hasOne(Profile) |
| Company | `core_modules/core/models.py` | `companies` | `id`, `name`, `code`, `is_active` | hasMany(Branches), hasMany(Users) |
| Branch | `core_modules/organization/models.py` | `branches` | `id`, `name`, `company_id`, `address` | belongsTo(Company) |
| Permission | `core_modules/permissions/models.py` | `permissions` | `id`, `name`, `codename`, `module` | belongsToMany(Roles) |
| Role | `core_modules/permissions/models.py` | `roles` | `id`, `name`, `permissions` | hasMany(Users), belongsToMany(Permissions) |

### Models (Business)

| Model | Path | Table | Key Fields | Relationships |
|-------|------|-------|------------|---------------|
| Product | `business_modules/inventory/models.py` | `products` | `id`, `name`, `sku`, `price`, `uom` | hasMany(StockItems), belongsTo(Category) |
| StockItem | `business_modules/inventory/models.py` | `stock_items` | `id`, `product_id`, `warehouse_id`, `quantity` | belongsTo(Product, Warehouse) |
| SalesOrder | `business_modules/sales/models.py` | `sales_orders` | `id`, `customer_id`, `total`, `status` | hasMany(OrderLines), belongsTo(Customer) |
| Invoice | `business_modules/accounting/invoices.py` | `invoices` | `id`, `number`, `type`, `total`, `status` | hasMany(Lines), belongsTo(Customer/Vendor) |
| JournalEntry | `business_modules/accounting/models.py` | `journal_entries` | `id`, `date`, `description`, `posted` | hasMany(Lines) |

### Middleware

| Middleware | Path | Purpose | Used By |
|------------|------|---------|---------|
| JWTAuth | `core_modules/security/middleware.py` | JWT token verification | All protected routes |
| PermissionCheck | `core_modules/permissions/middleware.py` | Permission verification | Protected routes |
| RateLimit | `core_modules/security/middleware.py` | API rate limiting | Auth endpoints |
| SecurityHeaders | `core_modules/security/middleware.py` | Add security headers | All responses |
| AuditLog | `core_modules/audit/middleware.py` | Log user actions | All requests |

---

## Database Schema

### Tables Summary

| Category | Table Count | Key Tables |
|----------|-------------|------------|
| Core | 15+ | users, companies, branches, permissions, roles, settings |
| Business | 40+ | products, stock_items, sales_orders, purchase_orders, invoices, journal_entries |
| Agricultural | 20+ | farms, nurseries, seeds, experiments, diagnoses |
| Services | 30+ | projects, employees, tasks, tickets, contracts |

### Key Relationships

```
users (1) ─── (N) sessions
users (1) ─── (1) profile
users (N) ─── (N) roles
roles (N) ─── (N) permissions
companies (1) ─── (N) branches
companies (1) ─── (N) users
products (1) ─── (N) stock_items
stock_items (N) ─── (1) warehouses
sales_orders (1) ─── (N) order_lines
invoices (1) ─── (N) invoice_lines
journal_entries (1) ─── (N) entry_lines
```

---

## Data Flow

### Example: Create Sales Order

```
[User] → [Frontend: SalesModule]
  ↓
  [Submit Order Button Click]
  ↓
  [Frontend: SalesService.createOrder()]
  ↓
  [API Call: POST /api/sales/orders]
  ↓
  [Backend: sales/urls.py → SalesViewSet]
  ↓
  [Middleware: JWTAuth, PermissionCheck]
  ↓
  [Backend: SalesViewSet.create()]
  ↓
  [Backend: SalesService.create_order()]
  ↓
  [Model Validation & Business Logic]
  ↓
  [Database: INSERT INTO sales_orders, order_lines]
  ↓
  [Signal: Create related invoice, update inventory]
  ↓
  [Response: 201 Created with order data]
  ↓
  [Frontend: Update UI, show success notification]
  ↓
  [User sees confirmation]
```

---

## Known Issues

### Duplicate Models (7 identified)

| Model | Canonical Location | Duplicate Locations |
|-------|-------------------|---------------------|
| User | `core_modules/users/models.py` | `users_accounts` (proxy), `api_server` |
| Company | `core_modules/core/models.py` | `organization/models.py`, `services_modules` |
| SalesInvoice | `accounting/invoices.py` | `sales/models.py` |
| PurchaseInvoice | `accounting/invoices.py` | `purchasing/models.py` (x2) |
| RestoreLog | TBD | 2 locations (TRUE DUPLICATE) |

### Security Configuration Conflicts

- JWT token TTL: Different values in 3 files (30min, 60min, 3600sec)
- Account lockout: Field exists but logic not implemented
- Hardcoded secrets: Found in 3 locations

---

## Missing Files Checklist

### Frontend
- [ ] All pages have corresponding routes
- [ ] All components are documented
- [ ] All services are implemented
- [x] API calls are defined

### Backend
- [x] All routes have controllers
- [x] All controllers have services
- [x] All services have models
- [ ] All models have complete migrations

### Database
- [ ] All tables have up-to-date migrations
- [ ] All foreign keys are properly defined
- [ ] All indexes are created
- [ ] Audit columns (created_at, updated_at) on all tables

---

**Last Updated**: 2025-11-28
**Next Update**: After model consolidation (Phase 3 Day 2)

