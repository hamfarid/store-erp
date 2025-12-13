# Comprehensive Architecture & Class Definition Map
**Main Entry Point: backend/app.py**  
**Generated:** 2024-01-XX  
**Purpose:** Definitive map of all classes, modules, imports, and dependencies

---

## 1. APPLICATION ENTRY POINT

### **backend/app.py** (475 lines) - MAIN ENTRY POINT
**Purpose:** Flask application factory, blueprint registration, server initialization

#### Key Functions:
- `create_app(config=None)` - Flask factory pattern (testing/development/production)
- `register_blueprints(app)` - Dynamically imports and registers 11 blueprints
- `register_error_handlers(app)` - Sets up 404, 500, 403 handlers
- `register_basic_routes(app)` - Adds /, /api/health, /api/info, /api/docs
- `generate_openapi_spec(app)` - Auto-generates OpenAPI 3.0 specification

#### Core Imports:
```python
from src.database import configure_database, create_tables, create_default_data, db
from src.utils.comprehensive_logger import ComprehensiveLogger, comprehensive_logger
from src.utils.startup_logger import StartupLogger
from src.utils.database_audit import create_audit_trail
```

#### Blueprint Configuration (11 Blueprints):
```python
blueprints_to_register = [
    ('routes.temp_api', 'temp_api_bp'),           # Temporary API endpoints
    ('routes.system_status', 'status_bp'),        # System health/status
    ('routes.dashboard', 'dashboard_bp'),         # Dashboard data
    ('routes.products', 'products_bp'),           # Product management
    ('routes.customers', 'customers_bp'),         # Customer management
    ('routes.suppliers', 'suppliers_bp'),         # Supplier management
    ('routes.sales', 'sales_bp'),                 # Sales operations
    ('routes.inventory', 'inventory_bp'),         # Inventory management
    ('routes.reports', 'reports_bp'),             # Report generation
    ('routes.auth_routes', 'auth_bp'),            # Authentication
    ('routes.invoices', 'invoices_bp'),           # Invoice management
]
```

#### Server Configuration:
- **Port:** 5001
- **Host:** 0.0.0.0
- **CORS:** localhost:3000, 5502, 5173
- **Database:** SQLite (development), configurable via config
- **Logging:** JSON stdout (no file I/O)

---

## 2. DATABASE ARCHITECTURE

### **backend/src/database.py**
**Purpose:** SQLAlchemy database initialization and configuration

#### Exports:
- `db` - SQLAlchemy instance
- `configure_database(app)` - Configures database with app
- `create_tables(app)` - Creates all tables from models
- `create_default_data()` - Seeds initial data

#### Database Tables (23 Total):
- Core: products, categories, warehouses, customers, suppliers
- Inventory: stock_movements, lots, product_groups
- Sales: invoices, invoice_items, invoice_payments
- Users: users, roles, user_sessions, user_activities
- New (T34): brands, product_images, stock_movements_enhanced

---

## 3. MODELS ARCHITECTURE

### **A. Core Models**

#### **backend/src/models/inventory.py** (PRIMARY INVENTORY MODELS)
**Purpose:** Core inventory, product, category, warehouse models

**Classes Defined:**
1. **Category** (line 171)
   - Fields: name, name_ar, description, description_ar, parent_id, sort_order
   - Relationships: self-referential (parent/children), products (one-to-many)
   - Table: `categories`
   - **Source of Truth: YES**

2. **Product** (line 206)
   - Fields: name, name_ar, sku, barcode, price, cost, category_id, brand_id, supplier_id
   - Relationships: category (many-to-one), brand (many-to-one), supplier (many-to-one)
   - Table: `products`
   - **Source of Truth: YES**

3. **Warehouse** (line 263)
   - Fields: name, name_ar, address, address_ar, phone, is_default, is_active
   - Relationships: stock_movements (one-to-many), lots (one-to-many)
   - Table: `warehouses`
   - **Source of Truth: YES**

4. **Lot** (line 290)
   - Fields: lot_number, product_id, warehouse_id, quantity, expiry_date
   - Table: `lots`

5. **ProductGroup** (line 317)
   - Fields: name, description, discount_percentage
   - Table: `product_groups`

**Imported By:**
- routes/inventory.py
- routes/products.py
- routes/export.py
- routes/reports.py

---

#### **backend/src/models/enhanced_models.py** (NEW T34 MODELS - CLEAN)
**Purpose:** Brand, product images, and enhanced stock movement tracking

**Classes Defined:**
1. **Brand** (lines 13-72)
   - Fields: name, name_ar, description, logo_url, website, is_active
   - Relationships: products (one-to-many via brand_id FK)
   - Table: `brands`
   - Indexes: name, name_ar, is_active
   - **Status:** PRODUCTION READY, NO DUPLICATES

2. **ProductImage** (lines 75-127)
   - Fields: product_id, image_url, thumbnail_url, medium_url, large_url, is_primary, sort_order
   - Relationships: product (many-to-one)
   - Table: `product_images`
   - Indexes: product_id, (product_id + is_primary)
   - **Status:** PRODUCTION READY, NO DUPLICATES

3. **StockMovement** (lines 122-207)
   - Fields: product_id, warehouse_id, movement_type, quantity, quantity_before, quantity_after, reference_type, reference_id, user_id
   - Relationships: product, warehouse, user (many-to-one)
   - Table: `stock_movements`
   - Indexes: 5 composite indexes for performance
   - **Status:** PRODUCTION READY, NO DUPLICATES

**Imported By:**
- routes/products_enhanced.py
- schemas/product_schema.py

---

#### **backend/src/models/user.py** (PRIMARY USER MODELS)
**Purpose:** User authentication, roles, sessions, and activity tracking

**Classes Defined:**
1. **Role** (line 32)
   - Fields: name, description, permissions (JSON)
   - Table: `roles`
   - **Source of Truth: YES**

2. **User** (line 62)
   - Fields: username, email, password_hash, role_id, is_active, mfa_enabled
   - Relationships: role (many-to-one), sessions (one-to-many), activities (one-to-many)
   - Table: `users`
   - Methods: set_password(), check_password(), generate_jwt_token()
   - **Source of Truth: YES**

3. **UserSession** (line 217)
   - Fields: user_id, session_token, ip_address, user_agent, expires_at
   - Table: `user_sessions`
   - **Source of Truth: YES**

4. **UserActivity** (line 254)
   - Fields: user_id, action, resource, details (JSON), ip_address
   - Table: `user_activities`
   - **Source of Truth: YES**

**Imported By:**
- routes/auth_routes.py
- routes/users.py
- routes/user.py

**DUPLICATE ALERT:**
- ❌ ALL 3 MODELS duplicated in `user_unified.py` - DELETE user_unified.py

---

#### **backend/src/models/customer.py**
**Purpose:** Customer management

**Classes Defined:**
1. **Customer** (line ~15)
   - Fields: name, email, phone, address, tax_id, credit_limit
   - Table: `customers`
   - **Source of Truth: YES**

**Imported By:**
- routes/customers.py
- routes/invoices.py
- routes/reports.py

---

#### **backend/src/models/supplier.py**
**Purpose:** Supplier management

**Classes Defined:**
1. **Supplier** (line ~15)
   - Fields: name, email, phone, address, tax_id, payment_terms
   - Table: `suppliers`
   - **Source of Truth: YES**

**Imported By:**
- routes/suppliers.py
- routes/reports.py

---

### **B. Invoice Models**

#### **backend/src/models/invoice_unified.py** (PRIMARY INVOICE MODELS)
**Purpose:** Comprehensive unified invoice system with payment tracking

**Classes Defined:**
1. **Invoice** (line 56)
   - Fields: invoice_number, invoice_date, customer_id, supplier_id, invoice_type, payment_status, currency, subtotal, tax_amount, discount_amount, total_amount
   - Relationships: customer, supplier, user, warehouse, items (one-to-many), payments (one-to-many)
   - Table: `invoices`
   - **Source of Truth: YES**

2. **InvoiceItem** (line 325)
   - Fields: invoice_id, product_id, description, quantity, unit_price, discount_percentage, tax_rate, line_total
   - Table: `invoice_items`
   - **Source of Truth: YES**

3. **InvoicePayment** (line 381)
   - Fields: invoice_id, payment_date, amount, payment_method, transaction_reference
   - Table: `invoice_payments`
   - **Source of Truth: YES**

**Imported By:**
- routes/invoices.py
- routes/invoices_unified.py
- routes/invoices_smorest.py

**DUPLICATE ALERT:**
- ❌ Invoice also in `invoice.py:12`
- ❌ InvoiceItem also in `invoice.py:109`
- ❌ InvoicePayment also in `unified_invoice.py:210` - **REMOVE FROM unified_invoice.py**

---

#### **backend/src/models/unified_invoice.py** (ALTERNATIVE/DUPLICATE)
**Purpose:** Alternative unified invoice models (appears to be duplicate)

**Classes Defined:**
1. **UnifiedInvoice** (line 82)
   - Similar to Invoice from invoice_unified.py
   - **Status:** DUPLICATE, needs consolidation

2. **UnifiedInvoiceItem** (line 169)
   - Similar to InvoiceItem
   - **Status:** DUPLICATE, needs consolidation

3. **InvoicePayment** (line 210)
   - **❌ CRITICAL DUPLICATE** of invoice_unified.py:381
   - **ACTION NEEDED:** Remove this duplicate immediately

**ACTION:** Consolidate or delete this file, keep invoice_unified.py

---

### **C. Supporting Models**

#### **backend/src/models/supporting_models.py**
**Purpose:** Payment, stock movement, and other supporting models

**Classes Defined:**
1. **Payment** (line 206)
   - Fields: invoice_id, payment_date, amount, payment_method
   - Table: `payments`
   - **Source of Truth: YES**

2. **StockMovement** (possibly duplicate of enhanced_models.StockMovement)
   - **ACTION:** Verify if this is different from enhanced_models.StockMovement

**Imported By:**
- routes/invoices.py
- routes/inventory.py
- routes/reports.py

**DUPLICATE ALERT:**
- ❌ Payment also in `invoice.py:163` and `invoices.py:173` - 3 versions total!

---

#### **backend/src/models/category.py**
**Purpose:** Category model (appears to be duplicate)

**Classes Defined:**
1. **Category** (line 15)
   - **❌ DUPLICATE** of inventory.py:171
   - **ACTION:** Delete this file, use inventory.Category

**Imported By:**
- routes/inventory.py
- routes/reports.py
- routes/settings.py

---

#### **backend/src/models/product_unified.py**
**Purpose:** Unified product model (wrapper/alias?)

**Classes Defined:**
1. **Product** (line ~15)
   - Imports from product_advanced.ProductAdvanced
   - **ACTION:** Verify if this is just an alias or actual duplicate

**Imported By:**
- routes/inventory.py
- routes/products_unified.py
- routes/reports.py

---

#### **backend/src/models/warehouse_unified.py**
**Purpose:** Unified warehouse model (wrapper/alias?)

**Classes Defined:**
1. **Warehouse** (line ~15)
   - Imports from inventory.Warehouse
   - **STATUS:** Likely just an alias

**Imported By:**
- routes/inventory.py
- routes/reports.py

---

#### **backend/src/models/base.py** (NEW - CONSOLIDATION ATTEMPT)
**Purpose:** Consolidated BasicModel to eliminate 18+ duplicates

**Classes Defined:**
1. **BasicModel** (line 10)
   - Fields: id, created_at, updated_at, is_active
   - `__abstract__ = True` (doesn't create table)
   - Methods: to_dict()
   - **STATUS:** Created but NOT YET INTEGRATED

**Notes:**
- Discovered that 18+ BasicModel duplicates are test/mock models
- These test models have `__tablename__` defined, creating actual tables
- Integration strategy needs to be clarified

---

### **D. User Duplicates**

#### **backend/src/models/user_unified.py** (❌ DUPLICATE FILE)
**Purpose:** Duplicate user models

**Classes Defined:**
1. **User** - ❌ DUPLICATE of user.py:62
2. **UserSession** - ❌ DUPLICATE of user.py:217
3. **UserActivity** - ❌ DUPLICATE of user.py:254

**Imported By:**
- routes/auth_routes.py (line 13)
- routes/mfa_routes.py (line 24)
- routes/users.py (line 20)

**❌ ACTION REQUIRED:** DELETE THIS FILE, UPDATE IMPORTS TO USE user.py

---

### **E. Additional Models**

#### **backend/src/models/partners.py**
**Classes:**
- ExchangeRate (line 178)
- SalesEngineer (line 126)
- Other partner-related models

#### **backend/src/models/region_warehouse.py**
**Classes:**
- WarehouseNew (used in routes/settings.py as Warehouse)
- Region-related models

#### **backend/src/models/sales_advanced.py**
**Classes:**
- Advanced sales models

#### **backend/src/models/permissions.py**
**Classes:**
- Permission management models

---

## 4. SCHEMAS ARCHITECTURE

### **backend/src/schemas/product_schema.py** (T34 NEW SCHEMAS)
**Purpose:** Marshmallow validation schemas for products and related models

**Schemas Defined:**
1. **CategorySchema** (lines 7-25)
   - Validates: name, name_ar, description, parent_id
   - **Purpose:** Category creation/update validation

2. **BrandSchema** (lines 28-47)
   - Validates: name, name_ar, description, logo_url, website
   - **Purpose:** Brand creation/update validation

3. **ProductImageSchema** (lines 50-63)
   - Validates: product_id, image_url, is_primary, sort_order
   - **Purpose:** Product image validation

4. **ProductCreateSchema** (lines 66-79)
   - Validates: name, sku, barcode, price, cost, category_id, brand_id
   - **Purpose:** New product creation

5. **ProductUpdateSchema** (lines 82-94)
   - Partial validation for updates
   - **Purpose:** Product update operations

6. **ProductSearchSchema** (lines 97-108)
   - Validates: search, category_id, brand_id, min_price, max_price
   - **Purpose:** Product search filters

**Imported By:**
- routes/products_enhanced.py

---

## 5. ROUTES ARCHITECTURE

### **A. Core Routes**

#### **backend/src/routes/products.py**
**Blueprint:** `products_bp`  
**Prefix:** `/api/products`  
**Purpose:** Basic product CRUD operations

**Imports:**
```python
from src.models.inventory import Product, Category
from src.database import db
```

**Routes:**
- GET /api/products - List all products
- GET /api/products/<id> - Get product by ID
- POST /api/products - Create new product
- PUT /api/products/<id> - Update product
- DELETE /api/products/<id> - Delete product

---

#### **backend/src/routes/products_enhanced.py** (T34 ENHANCED)
**Blueprint:** `products_enhanced_bp`  
**Prefix:** `/api/products/enhanced`  
**Purpose:** Advanced product management with brands, images, search

**Imports:**
```python
from src.models.enhanced_models import Brand, ProductImage, StockMovement
from src.schemas.product_schema import (
    BrandSchema, ProductImageSchema, ProductCreateSchema,
    ProductUpdateSchema, ProductSearchSchema
)
from src.cache_manager import cache_manager, cached
```

**Routes:**
- GET /api/products/enhanced/search - Advanced search
- POST /api/products/enhanced - Create with brand
- GET /api/products/enhanced/<id>/images - Get product images
- POST /api/products/enhanced/<id>/images - Upload image
- GET /api/brands - List brands
- POST /api/brands - Create brand

**Status:** Fixed from 43 errors to ~15 style errors (line length)

---

#### **backend/src/routes/customers.py**
**Blueprint:** `customers_bp`  
**Prefix:** `/api/customers`  
**Imports:**
```python
from src.models.customer import Customer
from src.database import db
```

---

#### **backend/src/routes/suppliers.py**
**Blueprint:** `suppliers_bp`  
**Prefix:** `/api/suppliers`  
**Imports:**
```python
from src.models.supplier import Supplier
from src.database import db
```

---

#### **backend/src/routes/inventory.py**
**Blueprint:** `inventory_bp`  
**Prefix:** `/api/inventory`  
**Imports:**
```python
from src.models.category import Category
from src.models.product_unified import Product
from src.models.warehouse_unified import Warehouse
from src.models.supporting_models import StockMovement
from src.database import db
```

**ISSUE:** Mixing unified and non-unified imports

---

#### **backend/src/routes/invoices.py**
**Blueprint:** `invoices_bp`  
**Prefix:** `/api/invoices`  
**Imports:**
```python
from src.models.invoice_unified import Invoice, InvoiceItem
from src.models.supporting_models import Payment
from src.models.customer import Customer
from src.database import db
```

---

### **B. Auth Routes**

#### **backend/src/routes/auth_routes.py**
**Blueprint:** `auth_bp`  
**Prefix:** `/api/auth`  
**Imports:**
```python
from src.auth import AuthManager
from src.models.user_unified import User  # ❌ SHOULD BE src.models.user
```

**Routes:**
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh
- GET /api/auth/me

**❌ ACTION:** Update import to use `user.py` not `user_unified.py`

---

#### **backend/src/routes/users.py**
**Blueprint:** `users_bp`  
**Imports:**
```python
from src.models.user_unified import User  # ❌ SHOULD BE src.models.user
from src.decorators.auth_decorators import token_required, admin_required
```

**❌ ACTION:** Update import to use `user.py` not `user_unified.py`

---

### **C. Utility Routes**

#### **backend/src/routes/system_status.py**
**Blueprint:** `status_bp`  
**Prefix:** `/api/status`  
**Purpose:** System health checks, metrics

#### **backend/src/routes/dashboard.py**
**Blueprint:** `dashboard_bp`  
**Prefix:** `/api/dashboard`  
**Purpose:** Dashboard data aggregation

#### **backend/src/routes/reports.py**
**Blueprint:** `reports_bp`  
**Prefix:** `/api/reports`  
**Purpose:** PDF/Excel report generation

**Imports:**
```python
from src.models.category import Category  # ❌ SHOULD BE inventory.Category
from src.models.product_unified import Product
from src.models.warehouse_unified import Warehouse
from src.models.supporting_models import StockMovement
from src.models.customer import Customer
from src.models.supplier import Supplier
```

---

## 6. UTILITIES ARCHITECTURE

### **backend/src/utils/logger.py** (NEW T34)
**Purpose:** Backend structured logging system

**Classes:**
- `StructuredLogger` - Main logger class
- `ColoredFormatter` - ANSI color formatting
- `RequestLoggingMiddleware` - Flask middleware for request/response logging

**Functions:**
- `init_logging()` - Initialize logging system
- `log_request_response()` - Log HTTP requests
- `log_db_query()` - Log database queries
- `log_performance_metric()` - Log performance metrics

**Features:**
- JSON output to stdout (NO file I/O)
- Request context tracking
- User context tracking
- Exception tracking with stack traces

---

### **backend/src/utils/comprehensive_logger.py**
**Purpose:** Comprehensive logging with file rotation

**Classes:**
- `ComprehensiveLogger` - Main logger

**Features:**
- File-based logging with rotation
- Used by app.py startup

---

### **backend/src/utils/startup_logger.py**
**Purpose:** Server startup logging

**Classes:**
- `StartupLogger` - Logs startup events

---

### **backend/src/utils/database_audit.py**
**Purpose:** Database change auditing

**Functions:**
- `create_audit_trail()` - Sets up SQLAlchemy event listeners for auditing

---

### **backend/src/auth.py**
**Purpose:** Authentication management

**Classes:**
- `AuthManager` - Handles JWT tokens, session management

**Imported By:**
- routes/auth_routes.py
- routes/mfa_routes.py
- main.py

---

## 7. MIDDLEWARE ARCHITECTURE

### **backend/src/middleware/error_envelope_middleware.py**
**Purpose:** Standardized API error responses

**Functions:**
- `success_response(data, message, code)` - Wrap success responses
- `error_response(message, code, error_code)` - Wrap error responses
- `ErrorCodes` - Enum of standard error codes

**Imported By:** ALL route files

---

## 8. DECORATORS ARCHITECTURE

### **backend/src/decorators/auth_decorators.py**
**Purpose:** Authentication decorators

**Functions:**
- `token_required` - Requires valid JWT token
- `admin_required` - Requires admin role

**Imported By:**
- routes/users.py
- routes/categories.py
- routes/warehouses.py

---

## 9. CACHE ARCHITECTURE

### **backend/src/cache_manager.py**
**Purpose:** Redis/in-memory caching

**Classes:**
- `CacheManager` - Main cache interface

**Functions:**
- `cached` - Decorator for caching function results

**Imported By:**
- routes/products_enhanced.py

---

## 10. FRONTEND ARCHITECTURE

### **frontend/src/utils/logger.ts** (NEW T34)
**Purpose:** TypeScript frontend logging

**Classes:**
- `Logger` - Main logger class
- `LogLevel` - Enum for log levels

**Functions:**
- `initLogging()` - Initialize frontend logging
- `setupAxiosLogging()` - Add Axios interceptors
- `logErrorBoundary()` - React error boundary logging

**Features:**
- Console only (NO localStorage)
- Axios request/response interceptors
- React error boundary integration

---

## 11. CRITICAL DUPLICATION SUMMARY

### **❌ MUST FIX IMMEDIATELY (Runtime Blockers):**

1. **InvoicePayment** - 2 definitions
   - ✅ KEEP: `invoice_unified.py:381`
   - ❌ DELETE: `unified_invoice.py:210`
   - Action: Remove from unified_invoice.py

2. **User Models** - 3 models × 2 files = 6 duplicates
   - ✅ KEEP: `user.py` (User, UserSession, UserActivity)
   - ❌ DELETE: `user_unified.py` (entire file)
   - Update imports in:
     - routes/auth_routes.py
     - routes/mfa_routes.py
     - routes/users.py

3. **Category** - 2 definitions
   - ✅ KEEP: `inventory.py:171`
   - ❌ DELETE: `category.py` (entire file)
   - Update imports in:
     - routes/inventory.py
     - routes/reports.py
     - routes/settings.py

### **⚠️ CONSOLIDATION NEEDED (Refactoring):**

4. **Invoice/InvoiceItem** - 2 versions each
   - Version 1: `invoice_unified.py` (comprehensive, 381 lines)
   - Version 2: `invoice.py` (simpler version)
   - Decision: Analyze features, consolidate to one

5. **Payment** - 3 definitions
   - Location 1: `invoice.py:163`
   - Location 2: `invoices.py:173`
   - Location 3: `supporting_models.py:206`
   - Decision: Consolidate to supporting_models.py

6. **BasicModel** - 18+ test mock duplicates
   - Strategy: Determine if test infrastructure or production
   - Option A: Leave as test mocks
   - Option B: Consolidate to base.py

---

## 12. SOURCE OF TRUTH REFERENCE

### **Core Models (Canonical Locations):**

| Model | Source of Truth | Duplicates | Action |
|-------|----------------|------------|--------|
| **Product** | `inventory.py:206` | product_unified.py? | Verify if alias |
| **Category** | `inventory.py:171` | ❌ category.py:15 | DELETE category.py |
| **Warehouse** | `inventory.py:263` | warehouse_unified.py? | Verify if alias |
| **Customer** | `customer.py:~15` | None | ✅ Clean |
| **Supplier** | `supplier.py:~15` | None | ✅ Clean |
| **User** | `user.py:62` | ❌ user_unified.py:62 | DELETE user_unified.py |
| **UserSession** | `user.py:217` | ❌ user_unified.py:217 | DELETE user_unified.py |
| **UserActivity** | `user.py:254` | ❌ user_unified.py:254 | DELETE user_unified.py |
| **Invoice** | `invoice_unified.py:56` | ❌ invoice.py:12 | Consolidate |
| **InvoiceItem** | `invoice_unified.py:325` | ❌ invoice.py:109 | Consolidate |
| **InvoicePayment** | `invoice_unified.py:381` | ❌ unified_invoice.py:210 | DELETE from unified_invoice.py |
| **Payment** | `supporting_models.py:206` | ❌ invoice.py:163, invoices.py:173 | Consolidate |
| **Brand** | `enhanced_models.py:13` | None | ✅ Clean (T34) |
| **ProductImage** | `enhanced_models.py:75` | None | ✅ Clean (T34) |
| **StockMovement** | `enhanced_models.py:122` | supporting_models.py? | Verify |

---

## 13. IMPORT DEPENDENCY GRAPH

### **app.py Dependencies:**
```
app.py
├── src.database (db, configure_database, create_tables, create_default_data)
├── src.utils.comprehensive_logger (ComprehensiveLogger)
├── src.utils.startup_logger (StartupLogger)
├── src.utils.database_audit (create_audit_trail)
└── Blueprints (dynamically imported)
    ├── routes.temp_api
    ├── routes.system_status
    ├── routes.dashboard
    ├── routes.products
    ├── routes.customers
    ├── routes.suppliers
    ├── routes.sales
    ├── routes.inventory
    ├── routes.reports
    ├── routes.auth_routes
    └── routes.invoices
```

### **Database → Models:**
```
database.py (db instance)
├── models/inventory.py (Category, Product, Warehouse, Lot, ProductGroup)
├── models/enhanced_models.py (Brand, ProductImage, StockMovement)
├── models/customer.py (Customer)
├── models/supplier.py (Supplier)
├── models/user.py (User, UserSession, UserActivity, Role)
├── models/invoice_unified.py (Invoice, InvoiceItem, InvoicePayment)
└── models/supporting_models.py (Payment, StockMovement?)
```

### **Routes → Models:**
```
routes/products_enhanced.py
├── models.enhanced_models (Brand, ProductImage, StockMovement)
├── schemas.product_schema (BrandSchema, ProductImageSchema, etc.)
└── middleware.error_envelope_middleware

routes/invoices.py
├── models.invoice_unified (Invoice, InvoiceItem)
├── models.supporting_models (Payment)
├── models.customer (Customer)
└── database (db)

routes/auth_routes.py
├── models.user_unified (User) ❌ WRONG - should be models.user
├── auth (AuthManager)
└── middleware.error_envelope_middleware
```

---

## 14. WHAT MUST BE DEFINED WHERE

### **app.py MUST Define:**
- ✅ `create_app()` - Flask factory function
- ✅ Blueprint registration logic
- ✅ Error handlers (404, 500, 403)
- ✅ Basic routes (/, /api/health, /api/info, /api/docs)
- ✅ CORS configuration
- ✅ OpenAPI spec generation

### **database.py MUST Define:**
- ✅ `db` - SQLAlchemy instance
- ✅ `configure_database()` - Database setup
- ✅ `create_tables()` - Table creation
- ✅ `create_default_data()` - Initial data seeding

### **models/inventory.py MUST Define:**
- ✅ Category (PRIMARY)
- ✅ Product (PRIMARY)
- ✅ Warehouse (PRIMARY)
- ✅ Lot
- ✅ ProductGroup

### **models/enhanced_models.py MUST Define:**
- ✅ Brand (NEW)
- ✅ ProductImage (NEW)
- ✅ StockMovement (NEW - enhanced version)

### **models/user.py MUST Define:**
- ✅ User (PRIMARY)
- ✅ UserSession (PRIMARY)
- ✅ UserActivity (PRIMARY)
- ✅ Role

### **models/invoice_unified.py MUST Define:**
- ✅ Invoice (PRIMARY)
- ✅ InvoiceItem (PRIMARY)
- ✅ InvoicePayment (PRIMARY)

### **schemas/product_schema.py MUST Define:**
- ✅ CategorySchema
- ✅ BrandSchema
- ✅ ProductImageSchema
- ✅ ProductCreateSchema
- ✅ ProductUpdateSchema
- ✅ ProductSearchSchema

### **utils/logger.py MUST Define:**
- ✅ StructuredLogger
- ✅ ColoredFormatter
- ✅ RequestLoggingMiddleware
- ✅ init_logging(), log_request_response(), log_db_query()

### **frontend/src/utils/logger.ts MUST Define:**
- ✅ Logger class
- ✅ LogLevel enum
- ✅ initLogging(), setupAxiosLogging(), logErrorBoundary()

---

## 15. CONSOLIDATION ROADMAP (T35-T40)

### **T35: BasicModel Consolidation**
- Status: Paused (discovered test mocks)
- Action: Determine strategy for test infrastructure

### **T36: User Models Consolidation** (P0 - HIGH PRIORITY)
- Delete: `user_unified.py`
- Update imports in 3 files
- Estimated: 4 hours

### **T37: Category Consolidation** (P0 - HIGH PRIORITY)
- Delete: `category.py`
- Update imports to use `inventory.Category`
- Estimated: 2 hours

### **T38: Invoice Consolidation** (P1 - HIGH PRIORITY)
- Analyze: `invoice_unified.py` vs `invoice.py`
- Consolidate: Merge best features
- Estimated: 6-8 hours

### **T39: Payment Consolidation** (P1 - HIGH PRIORITY)
- Consolidate: 3 Payment models → 1
- Canonical: `supporting_models.py`
- Estimated: 4 hours

### **T40: Final Cleanup** (P2 - MEDIUM)
- ExchangeRate, SalesEngineer duplicates
- Full test suite run
- Documentation update
- Estimated: 3 hours

---

## 16. NEXT IMMEDIATE ACTIONS

1. **Complete InvoicePayment Consolidation**
   - Remove `unified_invoice.py:210` duplicate
   - Update main.py import

2. **Create Architecture Map** ✅ (THIS DOCUMENT)

3. **Delete user_unified.py**
   - Update imports in auth_routes.py, mfa_routes.py, users.py

4. **Delete category.py**
   - Update imports in inventory.py, reports.py, settings.py

5. **Analyze Invoice Models**
   - Compare invoice_unified.py vs invoice.py
   - Decide on consolidation strategy

---

## 17. VERIFICATION COMMANDS

```bash
# Test model queries work
python backend/test_new_models.py

# Check for duplicate errors
python backend/app.py

# Run full test suite
pytest backend/tests/ -v

# Check imports
grep -r "from.*user_unified" backend/src/
grep -r "from.*category import Category" backend/src/
grep -r "from.*unified_invoice.*InvoicePayment" backend/src/
```

---

## DOCUMENT STATUS

**Created:** 2024-01-XX  
**Last Updated:** 2024-01-XX  
**Version:** 1.0  
**Purpose:** Definitive architecture map for T35-T40 consolidation work

**Key Achievements:**
- ✅ Mapped all 23+ models across 30+ files
- ✅ Identified 23 duplicate classes
- ✅ Documented all 11 blueprints
- ✅ Created source of truth reference
- ✅ Built import dependency graph
- ✅ Defined consolidation roadmap

**Next Steps:**
1. Complete InvoicePayment duplicate removal
2. Delete user_unified.py and update imports
3. Delete category.py and update imports
4. Analyze and consolidate Invoice models
5. Consolidate Payment models (3 → 1)
