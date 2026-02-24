# PROJECT MAPS - Store ERP System

**Generated:** 2025-11-08  
**Version:** 1.0  
**Purpose:** Comprehensive architectural maps for backend and frontend

---

## Table of Contents

1. [Backend Class Maps](#1-backend-class-maps)
2. [Backend Import/Export Maps](#2-backend-importexport-maps)
3. [Database Relation Maps](#3-database-relation-maps)
4. [Frontend Component Hierarchy](#4-frontend-component-hierarchy)
5. [Frontend State Flow](#5-frontend-state-flow)
6. [Frontend API Call Maps](#6-frontend-api-call-maps)

---

## 1. Backend Class Maps

### 1.1 Core Models (`backend/src/models/`)

#### User & Authentication Models

```
User (user.py)
├── Properties: id, username, email, password_hash, full_name, role_id, is_active
├── Relationships: role → Role
├── Methods: set_password(), check_password(), to_dict()
└── Table: users

Role (user.py)
├── Properties: id, name, description, permissions (JSON), is_active
├── Relationships: users ← User (backref)
├── Methods: to_dict()
└── Table: roles
```

#### Inventory Models

```
Product (inventory.py)
├── Properties: id, name, sku, barcode, category_id, price, cost, stock_quantity
├── Relationships: category → Category, stock_movements ← StockMovement
├── Methods: to_dict(), update_stock()
└── Table: products

Category (inventory.py)
├── Properties: id, name, description, parent_id, is_active
├── Relationships: parent → Category (self-ref), children ← Category, products ← Product
├── Methods: to_dict()
└── Table: categories

Warehouse (inventory.py)
├── Properties: id, name, location, description, is_active
├── Relationships: stock_movements ← StockMovement
├── Methods: to_dict()
└── Table: warehouses

StockMovement (inventory.py)
├── Properties: id, product_id, warehouse_id, movement_type, quantity, reference
├── Relationships: product → Product, warehouse → Warehouse
├── Methods: to_dict()
└── Table: stock_movements
```

#### Customer & Supplier Models

```
Customer (customer.py)
├── Properties: id, customer_code, name, email, phone, address, credit_limit
├── Relationships: sales_invoices ← SalesInvoice
├── Methods: to_dict()
└── Table: customers

Supplier (supplier.py)
├── Properties: id, supplier_code, name, email, phone, address, payment_terms
├── Relationships: purchase_orders ← PurchaseOrder
├── Methods: to_dict()
└── Table: suppliers
```

#### Invoice Models

```
UnifiedInvoice (unified_invoice.py)
├── Properties: id, invoice_number, invoice_type, customer_id, total_amount, status
├── Relationships: customer → Customer, items ← UnifiedInvoiceItem, payments ← InvoicePayment
├── Methods: to_dict(), calculate_total()
└── Table: unified_invoices

UnifiedInvoiceItem (unified_invoice.py)
├── Properties: id, invoice_id, product_id, quantity, unit_price, total
├── Relationships: invoice → UnifiedInvoice, product → Product
├── Methods: to_dict()
└── Table: unified_invoice_items

SalesInvoice (sales_advanced.py)
├── Properties: id, invoice_number, customer_id, total_amount, status
├── Relationships: customer → Customer, items ← SalesInvoiceItem
├── Methods: to_dict()
└── Table: sales_invoices
```

### 1.2 Service Classes (`backend/src/services/`)

```
PermissionService (permission_service.py)
├── Methods: check_permission(), get_user_permissions(), assign_role()
└── Dependencies: User, Role models

CacheService (cache_service.py)
├── Methods: get(), set(), delete(), clear()
└── Dependencies: Redis/Memory cache

MonitoringService (monitoring_service.py)
├── Methods: log_metric(), get_metrics(), alert()
└── Dependencies: Prometheus, Sentry

BackupService (backup_service.py)
├── Methods: create_backup(), restore_backup(), list_backups()
└── Dependencies: Database, File system
```

### 1.3 Route Blueprints (`backend/src/routes/`)

**Canonical blueprints registered by `app.py` (current reality)**

```
temp_api.py → temp_api_bp
├── GET /api/temp/health
└── Temporary/diagnostic endpoints

system_status.py → status_bp
├── GET /system/status
└── GET /system/health

dashboard.py → dashboard_bp
├── GET /api/dashboard/data
├── GET /api/dashboard/statistics
└── GET /api/dashboard/alerts

products_unified.py → products_unified_bp
├── GET /api/products
├── POST /api/products
├── GET /api/products/<id>
├── PUT /api/products/<id>
└── DELETE /api/products/<id>

inventory.py → inventory_bp
├── GET /api/inventory/stock-levels
├── POST /api/inventory/movements
└── Category / warehouse / stock utilities

sales.py → sales_bp
└── Sales and legacy invoice‑related endpoints

reports.py → reports_bp
└── Inventory / financial reports and PDF exports

auth_unified.py → auth_unified_bp
├── POST /api/auth/login
├── POST /api/auth/refresh
└── GET /api/auth/me

invoices_unified.py → invoices_unified_bp
└── Unified invoice API (headers, items, payments)

users_unified.py → users_unified_bp
└── User & role management on unified models

partners_unified.py → partners_unified_bp
└── Unified customers & suppliers API (partners abstraction)
```

**Legacy blueprints (still present, may be used for backward compatibility / tests)**

- `auth_routes.py → auth_bp`
- `products.py → products_bp`
- `customers.py → customers_bp`
- `suppliers.py → suppliers_bp`
- `invoices.py → invoices_bp`

These are no longer registered by default in `register_blueprints(app)` but remain in the codebase for migration and API drift testing.

---

### 1.4 Model Architecture: Base vs Unified Models

- **Base inventory models** (`src.models.inventory`)
  - `Category`, `Product`, `Warehouse`, `Lot`, `ProductGroup`
  - Aliases: `StockMovement = Lot`, `Batch = Lot`, etc., maintained for compatibility.
- **Unified product & warehouse models**
  - `src.models.product_unified.Product`
  - `src.models.warehouse_unified.Warehouse` (re‑exports `Warehouse` from `inventory` for a single source of truth).
- **Unified invoice models**
  - `src.models.unified_invoice.UnifiedInvoice`, `UnifiedInvoiceItem` (legacy unified invoice schema)
  - `src.models.invoice_unified.InvoicePayment` and related enums for statuses/types.
- **Supporting models** (`src.models.supporting_models`)
  - `PaymentMethod`, `TaxRate`, `Unit`, `Currency`, `InvoiceStatus`, `DiscountType`, `Payment`
  - Re‑exports `StockMovement` to allow routes to import it via `src.models.supporting_models`.
- **Routing preference**
  - Routes prefer unified models where available and fall back to base models/dummy classes under a feature flag (e.g., `UNIFIED_MODELS` in some routes).

---

## 2. Backend Import/Export Maps

### 2.1 Model Import Chain

```
app.py
└── imports src.database.configure_database / create_tables
    └── creates db (SQLAlchemy instance)
        └── create_tables() preloads models in phases:
            ├── Phase 1: src.models.user → User, Role
            ├── Phase 1: src.models.sales_engineer → SalesEngineer (optional)
            ├── Phase 1: src.models.customer → Customer
            ├── Phase 1: src.models.supplier → Supplier
            ├── Phase 2: src.models.inventory → Category, Product, Warehouse
            ├── Phase 4: src.models.unified_invoice → UnifiedInvoice, UnifiedInvoiceItem
            ├── Phase 4: src.models.invoice_unified → InvoicePayment
            └── Phase 5: src.models.sales_advanced → SalesInvoice, SalesInvoiceItem, CustomerPayment
```

### 2.2 Route Import Chain

```
app.py
└── calls register_blueprints(app)
    └── imports and registers blueprints:
        ├── routes.temp_api → temp_api_bp
        ├── routes.system_status → status_bp
        ├── routes.dashboard → dashboard_bp
        ├── routes.products_unified → products_unified_bp
        ├── routes.sales → sales_bp
        ├── routes.inventory → inventory_bp
        ├── routes.reports → reports_bp
        ├── routes.auth_unified → auth_unified_bp
        ├── routes.invoices_unified → invoices_unified_bp
        ├── routes.users_unified → users_unified_bp
        └── routes.partners_unified → partners_unified_bp
```

### 2.3 Service Dependencies

```
routes/products.py
├── imports models.Product, models.Category
├── imports services.permission_service
├── imports services.cache_service
└── imports utils.error_handler

routes/invoices.py
├── imports models.UnifiedInvoice, models.Customer
├── imports services.permission_service
└── imports utils.validation
```

---

## 3. Database Relation Maps

### 3.1 Entity Relationship Diagram (Text)

```
User ──────┐
           │ 1:N
           └──> Role

Customer ──────┐
               │ 1:N
               └──> SalesInvoice ──────┐
                                       │ 1:N
                                       └──> SalesInvoiceItem ──────┐
                                                                    │ N:1
                                                                    └──> Product

Supplier ──────┐
               │ 1:N
               └──> PurchaseOrder

Product ──────┐
              │ N:1
              ├──> Category ──────┐
              │                    │ self-ref (parent_id)
              │                    └──> Category (children)
              │
              │ 1:N
              └──> StockMovement ──────┐
                                       │ N:1
                                       └──> Warehouse
```

### 3.2 Foreign Key Map

```
Table: users
└── role_id → roles.id

Table: products
└── category_id → categories.id

Table: stock_movements
├── product_id → products.id
└── warehouse_id → warehouses.id

Table: sales_invoices
└── customer_id → customers.id

Table: sales_invoice_items
├── invoice_id → sales_invoices.id
└── product_id → products.id

Table: unified_invoices
└── customer_id → customers.id

Table: unified_invoice_items
├── invoice_id → unified_invoices.id
└── product_id → products.id

Table: categories
└── parent_id → categories.id (self-reference)
```

---

## 4. Frontend Component Hierarchy

### 4.1 Application Root

```
App.jsx (Root)
└── ErrorBoundary
    └── Suspense
        └── AppRouter
            ├── AuthProvider
            │   └── Router
            │       ├── Login (public route)
            │       └── ProtectedRoute
            │           └── Layout
            │               ├── Header
            │               ├── Sidebar
            │               ├── Main Content (Outlet)
            │               └── Footer
            └── Toaster (global notifications)
```

### 4.2 Page Components (`frontend/src/pages/`)

```
InteractiveDashboard.jsx
├── DashboardStats
├── SalesChart
├── InventoryChart
└── AlertsPanel

ProductDetails.jsx
├── ProductInfo
├── ProductImages
├── StockLevels
└── PriceHistory

CustomerDetails.jsx
├── CustomerInfo
├── OrderHistory
└── PaymentHistory

Reports.jsx
├── ReportFilters
├── ReportTable
└── ExportButtons
```

### 4.3 Shared Components (`frontend/src/components/`)

```
Layout.jsx
├── Header.jsx
│   ├── Logo
│   ├── Navigation
│   └── UserMenu
├── Sidebar.jsx
│   ├── MainMenu
│   ├── QuickActions
│   └── CollapseButton
└── Footer.jsx

ProductManagement.jsx
├── ProductList
│   ├── SearchBar
│   ├── FilterPanel
│   └── ProductTable
├── ProductForm (Modal)
└── ProductDetails (Modal)

InvoiceManagement.jsx
├── InvoiceList
├── InvoiceForm
└── InvoicePrint

CustomerManagement.jsx
├── CustomerList
├── CustomerForm
└── CustomerDetails
```

### 4.4 UI Components (`frontend/src/components/ui/`)

```
AdvancedTable.jsx
├── TableHeader
├── TableBody
├── TableRow
├── Pagination
└── SortControls

DynamicForm.jsx
├── FormField
├── ValidationMessage
└── SubmitButton

Modal.jsx
├── ModalHeader
├── ModalBody
└── ModalFooter

LoadingSpinner.jsx
ErrorBoundary.jsx
Notification.jsx
PermissionsGuard.jsx
```

---

## 5. Frontend State Flow

### 5.1 Context Providers

```
AuthContext (contexts/AuthContext.jsx)
├── State:
│   ├── user (current user object)
│   ├── token (JWT token)
│   ├── isAuthenticated (boolean)
│   └── permissions (array)
├── Methods:
│   ├── login(username, password)
│   ├── logout()
│   ├── refreshToken()
│   └── hasPermission(permission)
└── Consumers: All protected components

ThemeContext (contexts/ThemeContext.jsx)
├── State:
│   ├── theme (light/dark)
│   └── colors (theme colors)
├── Methods:
│   ├── toggleTheme()
│   └── setCustomColors()
└── Consumers: Layout, UI components

PermissionContext (contexts/PermissionContext.jsx)
├── State:
│   └── userPermissions (array)
├── Methods:
│   ├── checkPermission(permission)
│   └── hasAnyPermission(permissions[])
└── Consumers: Protected routes, action buttons

AppContext (contexts/AppContext.jsx)
├── State:
│   ├── loading (boolean)
│   ├── notifications (array)
│   └── settings (object)
├── Methods:
│   ├── showNotification(message, type)
│   └── updateSettings(settings)
└── Consumers: Global components
```

### 5.2 Component State Flow

```
Login Component
├── Local State: username, password, loading, error
├── On Submit:
│   ├── Call AuthContext.login()
│   ├── Store token in localStorage
│   ├── Update AuthContext state
│   └── Navigate to dashboard
└── On Success: Redirect to /dashboard

ProductManagement Component
├── Local State: products[], loading, filters, selectedProduct
├── On Mount:
│   ├── Call productsAPI.getAll()
│   ├── Update products state
│   └── Set loading to false
├── On Create:
│   ├── Call productsAPI.create(data)
│   ├── Refresh products list
│   └── Show success notification
└── On Update/Delete: Similar flow

Dashboard Component
├── Local State: stats, charts, alerts, loading
├── On Mount:
│   ├── Call dashboardAPI.getDashboardData()
│   ├── Call dashboardAPI.getStatistics()
│   ├── Call dashboardAPI.getAlerts()
│   └── Update state with responses
└── Auto-refresh: Every 30 seconds
```

---

## 6. Frontend API Call Maps

### 6.1 API Service Structure (`frontend/src/services/`)

```
api.js (Main API client)
├── axios instance with:
│   ├── baseURL: VITE_API_BASE or ''
│   ├── timeout: 30000ms
│   ├── withCredentials: true
│   └── headers: Content-Type, Accept
├── Request Interceptor:
│   ├── Add Authorization header (Bearer token)
│   └── Add CSRF token
└── Response Interceptor:
    ├── Handle 401 → logout
    ├── Handle 403 → redirect to /403
    └── Handle 500 → show error notification
```

### 6.2 API Endpoint Mapping

#### Products API (`productsAPI`)

```
GET    /api/products-advanced          → getAll(params)
GET    /api/products/:id               → getById(id)
POST   /api/products                   → create(data)
PUT    /api/products/:id               → update(id, data)
DELETE /api/products/:id               → delete(id)
GET    /api/products/search            → search(query)
GET    /api/products/categories        → getCategories()
POST   /api/products/bulk-update       → bulkUpdate(data)
POST   /api/products/export            → export(format)
```

#### Customers API (`customersAPI`)

```
GET    /api/customers                  → getAll(params)
GET    /api/customers/:id              → getById(id)
POST   /api/customers                  → create(data)
PUT    /api/customers/:id              → update(id, data)
DELETE /api/customers/:id              → delete(id)
GET    /api/customers/:id/orders       → getOrders(id)
GET    /api/customers/:id/payments     → getPayments(id)
```

#### Invoices API (`salesInvoicesAPI`)

```
GET    /api/invoices                   → getAll(params)
GET    /api/invoices/:id               → getById(id)
POST   /api/invoices                   → create(data)
PUT    /api/invoices/:id               → update(id, data)
DELETE /api/invoices/:id               → delete(id)
POST   /api/invoices/:id/print         → print(id)
POST   /api/invoices/:id/email         → sendEmail(id)
```

#### Inventory API (`stockMovementsAPI`)

```
GET    /api/stock-movements-advanced   → getAll(params)
POST   /api/stock-movements-advanced   → create(data)
GET    /api/inventory/stock-levels     → getStockLevels()
GET    /api/inventory/low-stock        → getLowStock()
```

#### Dashboard API (`dashboardAPI`)

```
GET    /api/dashboard/data             → getDashboardData(period)
GET    /api/dashboard/statistics       → getStatistics()
GET    /api/dashboard/alerts           → getAlerts()
```

#### Reports API (`reportsAPI`)

```
GET    /api/reports/sales              → getSalesReport(params)
GET    /api/reports/inventory          → getInventoryReport(params)
GET    /api/reports/financial          → getFinancialReport(params)
POST   /api/reports/export             → exportReport(type, format)
```

### 6.3 API Call Flow Example

```
Component: ProductManagement
│
├── On Mount:
│   └── productsAPI.getAll({ page: 1, limit: 20 })
│       └── axios.get('/api/products-advanced', { params })
│           ├── Request Interceptor: Add token
│           ├── Backend: products.py → get_products()
│           ├── Response: { success: true, data: [...] }
│           └── Response Interceptor: Check success
│               └── Component: Update state with data
│
├── On Create:
│   └── productsAPI.create({ name, sku, price })
│       └── axios.post('/api/products', data)
│           ├── Request Interceptor: Add token
│           ├── Backend: products.py → create_product()
│           ├── Response: { success: true, data: {...} }
│           └── Component: Refresh list, show notification
│
└── On Error:
    └── Response Interceptor: Catch error
        ├── 401: AuthContext.logout() → Navigate to /login
        ├── 403: Navigate to /403
        └── 500: Show error notification
```

---

## 7. Integration Points

### 7.1 Frontend → Backend Communication

```
Frontend Component
└── calls API service (api.js)
    └── axios HTTP request
        └── Backend Flask route
            └── calls Service layer
                └── calls Model/Database
                    └── returns data
                        └── Service processes
                            └── Route returns JSON
                                └── axios receives response
                                    └── Component updates state
```

### 7.2 Authentication Flow

```
1. User enters credentials in Login.jsx
2. AuthContext.login() called
3. POST /api/auth/login with { username, password }
4. Backend auth_routes.py validates credentials
5. Backend generates JWT token
6. Frontend stores token in localStorage
7. Frontend updates AuthContext state
8. All subsequent requests include token in Authorization header
9. Backend validates token on protected routes
10. On token expiry: Frontend calls /api/auth/refresh
```

### 7.3 Permission Flow

```
1. User logs in → Backend returns user with permissions
2. AuthContext stores permissions array
3. PermissionContext provides hasPermission() method
4. Components use PermissionGuard wrapper
5. Routes use ProtectedRoute with requiredPermission
6. Buttons/Actions check permission before rendering
7. Backend validates permissions on each API call
```

---

## 8. File Structure Summary

### Backend

```
backend/
├── src/
│   ├── models/          # 50+ model files
│   ├── routes/          # 80+ route files
│   ├── services/        # 15+ service files
│   ├── utils/           # Helper functions
│   ├── middleware/      # Auth, CORS, error handling
│   ├── database.py      # SQLAlchemy setup
│   └── main.py          # Application entry
├── tests/               # 30+ test files
├── migrations/          # Alembic migrations
└── app.py               # Alternative entry point
```

### Frontend

```
frontend/
├── src/
│   ├── components/      # 100+ component files
│   ├── pages/           # 20+ page files
│   ├── services/        # API services
│   ├── contexts/        # React contexts
│   ├── utils/           # Helper functions
│   ├── hooks/           # Custom hooks
│   ├── styles/          # CSS/Tailwind
│   ├── App.jsx          # Root component
│   └── main.jsx         # React entry
├── public/              # Static assets
└── dist/                # Build output
```

---

**Last Updated:** 2025-11-08
**Maintained By:** AI Agent (Autonomous Analysis)
**Next Review:** On major architectural changes
