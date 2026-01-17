# 📚 Class Registry - Store ERP v2.0.0

**Version:** 2.0.0  
**Last Updated:** 2026-01-16  
**Total Classes:** 150+

---

## 📋 Table of Contents

1. [Backend Models](#backend-models)
2. [Backend Services](#backend-services)
3. [Backend Routes](#backend-routes)
4. [Frontend Pages](#frontend-pages)
5. [Frontend Components](#frontend-components)
6. [Frontend Services](#frontend-services)
7. [Utilities](#utilities)

---

## 🗄️ Backend Models

### User Model
**File:** `backend/src/models/user.py`  
**Purpose:** User authentication and profile management  
**Attributes:**
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password_hash` - Hashed password
- `role_id` - Foreign key to roles
- `is_active` - Account status
- `two_factor_enabled` - 2FA status
- `created_at`, `updated_at`

**Methods:**
- `set_password(password)` - Hash and set password
- `check_password(password)` - Verify password
- `generate_token()` - Generate JWT token
- `to_dict()` - Serialize to dictionary

---

### Role Model
**File:** `backend/src/models/role.py`  
**Purpose:** RBAC role management  
**Attributes:**
- `id` - Primary key
- `name` - Role name (admin, manager, cashier, etc.)
- `description` - Role description
- `permissions` - JSON field with permissions array

**Relationships:**
- `users` - One-to-Many with User

---

### Product Model
**File:** `backend/src/models/product.py`  
**Purpose:** Product catalog management  
**Attributes:**
- `id`, `sku`, `barcode`
- `name`, `name_ar` - Bilingual names
- `description`
- `category_id` - Foreign key
- `unit`, `purchase_price`, `selling_price`
- `min_stock`, `max_stock`
- `is_active`, `track_lots`

**Relationships:**
- `category` - Many-to-One with Category
- `lots` - One-to-Many with Lot
- `invoice_items` - One-to-Many

---

### Lot Model
**File:** `backend/src/models/lot.py`  
**Purpose:** Batch/Lot tracking with quality fields  
**Attributes:**
- `id`, `lot_number`
- `product_id` - Foreign key
- `quantity`, `available_quantity`
- `unit_cost`, `expiry_date`
- `supplier_id`, `warehouse_id`
- `status` - (available, reserved, sold, expired, etc.)
- **Quality Fields:**
  - `germination_rate`
  - `purity_percentage`
  - `moisture_percentage`
  - `ministry_lot_number`

**Methods:**
- `is_expired()` - Check expiry status
- `reserve(quantity)` - Reserve stock
- `release(quantity)` - Release reserved

---

### Category Model
**File:** `backend/src/models/category.py`  
**Purpose:** Product categorization  
**Attributes:**
- `id`, `name`, `name_ar`
- `description`
- `parent_id` - Self-referential FK
- `image_url`

**Relationships:**
- `parent` - Self-referential
- `children` - Self-referential
- `products` - One-to-Many

---

### Invoice Model
**File:** `backend/src/models/invoice.py`  
**Purpose:** Sales and purchase invoices  
**Attributes:**
- `id`, `invoice_number`
- `type` - (sale, purchase, return)
- `customer_id`, `supplier_id`
- `subtotal`, `discount`, `tax_amount`, `total`
- `payment_method`, `payment_status`
- `status` - (pending, completed, cancelled)
- `notes`

**Relationships:**
- `items` - One-to-Many with InvoiceItem
- `customer`, `supplier`

---

### InvoiceItem Model
**File:** `backend/src/models/invoice_item.py`  
**Purpose:** Invoice line items  
**Attributes:**
- `id`, `invoice_id`, `product_id`, `lot_id`
- `quantity`, `unit_price`, `discount`
- `subtotal`, `tax_amount`, `total`

---

### Customer Model
**File:** `backend/src/models/customer.py`  
**Purpose:** Customer management  
**Attributes:**
- `id`, `name`, `phone`, `email`
- `address`, `city`, `country`
- `tax_number`
- `credit_limit`, `balance`
- `is_active`

---

### Supplier Model
**File:** `backend/src/models/supplier.py`  
**Purpose:** Supplier management  
**Attributes:**
- `id`, `name`, `phone`, `email`
- `address`, `city`, `country`
- `tax_number`
- `payment_terms`
- `balance`

---

### Warehouse Model
**File:** `backend/src/models/warehouse.py`  
**Purpose:** Multi-warehouse support  
**Attributes:**
- `id`, `name`, `code`
- `address`
- `is_default`, `is_active`

---

### Shift Model
**File:** `backend/src/models/shift.py`  
**Purpose:** POS shift management  
**Attributes:**
- `id`, `user_id`
- `opening_cash`, `closing_cash`
- `total_sales`, `total_returns`
- `status` - (open, closed)
- `opened_at`, `closed_at`

---

### AuditLog Model
**File:** `backend/src/models/audit_log.py`  
**Purpose:** Activity logging  
**Attributes:**
- `id`, `user_id`
- `action` - (create, update, delete, login, etc.)
- `entity_type`, `entity_id`
- `old_values`, `new_values` - JSON
- `ip_address`, `user_agent`
- `created_at`

---

### Setting Model
**File:** `backend/src/models/setting.py`  
**Purpose:** System configuration  
**Attributes:**
- `id`, `key`, `value`
- `type` - (string, number, boolean, json)
- `category`
- `description`

---

## 🔧 Backend Services

### AuthService
**File:** `backend/src/services/auth_service.py`  
**Purpose:** Authentication logic  
**Methods:**
- `login(username, password)` - Authenticate user
- `logout(token)` - Invalidate token
- `refresh_token(refresh_token)` - Get new access token
- `verify_2fa(user_id, code)` - Verify TOTP code
- `enable_2fa(user_id)` - Setup 2FA

---

### ProductService
**File:** `backend/src/services/product_service.py`  
**Purpose:** Product business logic  
**Methods:**
- `create(data)`, `update(id, data)`, `delete(id)`
- `get_by_id(id)`, `get_all(filters)`
- `search(query)`, `get_by_barcode(barcode)`
- `update_stock(id, quantity)`
- `get_low_stock()`

---

### LotService
**File:** `backend/src/services/lot_service.py`  
**Purpose:** Lot management logic  
**Methods:**
- `create(data)`, `update(id, data)`
- `get_available_lots(product_id)` - FIFO sorted
- `get_expiring_lots(days)`
- `reserve_quantity(lot_id, quantity)`
- `update_status(lot_id, status)`

---

### InvoiceService
**File:** `backend/src/services/invoice_service.py`  
**Purpose:** Invoice processing  
**Methods:**
- `create_sale(data)` - Create sale invoice
- `create_purchase(data)` - Create purchase invoice
- `process_return(invoice_id, items)`
- `calculate_totals(items)`
- `generate_invoice_number(type)`

---

### POSService
**File:** `backend/src/services/pos_service.py`  
**Purpose:** Point of Sale operations  
**Methods:**
- `open_shift(user_id, opening_cash)`
- `close_shift(shift_id, closing_cash)`
- `process_sale(cart, payment)`
- `get_product_by_barcode(barcode)`
- `get_available_lot(product_id)` - FIFO selection

---

### ReportService
**File:** `backend/src/services/report_service.py`  
**Purpose:** Report generation  
**Methods:**
- `get_sales_report(from_date, to_date)`
- `get_inventory_report()`
- `get_profit_loss_report(period)`
- `get_lot_expiry_report(days)`
- `export_to_pdf(report_data)`
- `export_to_excel(report_data)`

---

### NotificationService
**File:** `backend/src/services/notification_service.py`  
**Purpose:** Notification handling  
**Methods:**
- `send_email(to, subject, body)`
- `send_sms(phone, message)`
- `create_in_app_notification(user_id, message)`
- `check_low_stock_alerts()`
- `check_expiry_alerts()`

---

### BackupService
**File:** `backend/src/services/backup_service.py`  
**Purpose:** Database backup/restore  
**Methods:**
- `create_backup()`
- `restore_backup(backup_id)`
- `list_backups()`
- `delete_backup(backup_id)`
- `schedule_auto_backup()`

---

## 🛣️ Backend Routes

### Auth Routes
**File:** `backend/src/routes/auth.py`  
**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/refresh` | Refresh token |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/2fa/setup` | Setup 2FA |
| POST | `/api/auth/2fa/verify` | Verify 2FA |

---

### Products Routes
**File:** `backend/src/routes/products.py`  
**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/products` | List products |
| GET | `/api/products/:id` | Get product |
| POST | `/api/products` | Create product |
| PUT | `/api/products/:id` | Update product |
| DELETE | `/api/products/:id` | Delete product |
| GET | `/api/products/barcode/:code` | Get by barcode |

---

### Lots Routes
**File:** `backend/src/routes/lots.py`  
**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/lots` | List lots |
| GET | `/api/lots/:id` | Get lot |
| POST | `/api/lots` | Create lot |
| PUT | `/api/lots/:id` | Update lot |
| PATCH | `/api/lots/:id/status` | Update status |
| GET | `/api/lots/expiring` | Get expiring lots |

---

### POS Routes
**File:** `backend/src/routes/pos.py`  
**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/pos/sale` | Process sale |
| POST | `/api/pos/return` | Process return |
| GET | `/api/pos/shift/current` | Get current shift |
| POST | `/api/pos/shift/open` | Open shift |
| POST | `/api/pos/shift/close` | Close shift |

---

### Reports Routes
**File:** `backend/src/routes/reports.py`  
**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/reports/sales` | Sales report |
| GET | `/api/reports/inventory` | Inventory report |
| GET | `/api/reports/profit-loss` | P&L report |
| GET | `/api/reports/lot-expiry` | Expiry report |
| GET | `/api/reports/:type/export` | Export report |

---

## 📱 Frontend Pages

### Dashboard
**File:** `frontend/src/pages/Dashboard.jsx`  
**Purpose:** Main dashboard with KPIs  
**Features:**
- Sales summary cards
- Recent transactions
- Low stock alerts
- Expiry warnings
- Charts (sales trend, category breakdown)

---

### POSSystem
**File:** `frontend/src/pages/POSSystem.jsx`  
**Purpose:** Point of Sale interface  
**Features:**
- Product search/barcode input
- Cart management
- Lot selection (FIFO)
- Payment processing
- Receipt printing

---

### ProductsPage
**File:** `frontend/src/pages/ProductsPage.jsx`  
**Purpose:** Product management  
**Features:**
- Product listing with filters
- Add/Edit/Delete products
- Import/Export functionality
- Category filtering
- Stock level indicators

---

### LotBatchManagement
**File:** `frontend/src/pages/LotBatchManagement.jsx`  
**Purpose:** Lot management  
**Features:**
- Lot listing with status filter
- Quality fields editing
- Expiry tracking
- Status transitions
- Multi-warehouse support

---

### LotExpiryReport
**File:** `frontend/src/pages/LotExpiryReport.jsx`  
**Purpose:** Expiring lots report  
**Features:**
- Days filter (7, 14, 30, 60, 90)
- Status badges
- Export to PDF/Excel/CSV
- Sorting and searching

---

### ReportsSystem
**File:** `frontend/src/pages/ReportsSystem.jsx`  
**Purpose:** Reports hub  
**Features:**
- Report type selection
- Date range filters
- Interactive charts
- Export options

---

### ProfitLossReports
**File:** `frontend/src/pages/ProfitLossReports.jsx`  
**Purpose:** Financial reports  
**Features:**
- Revenue vs Cost analysis
- Period comparison
- Profit margins
- Export functionality

---

### SettingsPage
**File:** `frontend/src/pages/SettingsPage.jsx`  
**Purpose:** General settings  
**Features:**
- Company information
- Currency/Timezone
- Theme preferences
- System configuration

---

### NotificationSettings
**File:** `frontend/src/pages/NotificationSettings.jsx`  
**Purpose:** Notification preferences  
**Features:**
- Channel toggles (Email, SMS, Push, In-App)
- Alert thresholds
- Quiet hours
- Sound settings

---

### TaxSettings
**File:** `frontend/src/pages/TaxSettings.jsx`  
**Purpose:** Tax configuration  
**Features:**
- Tax rate management
- ZATCA integration
- Tax types CRUD
- E-invoicing settings

---

### BackupRestore
**File:** `frontend/src/pages/BackupRestore.jsx`  
**Purpose:** Backup management  
**Features:**
- Backup list
- Create manual backup
- Restore from backup
- Auto-backup scheduling

---

### UsersPage / RolesPermissionsManagement
**File:** `frontend/src/pages/UsersPage.jsx`, `RolesPermissionsManagement.jsx`  
**Purpose:** User & Role management  
**Features:**
- User CRUD
- Role assignment
- Permission management
- Activity logs

---

## 🧩 Frontend Components

### UI Components
**Directory:** `frontend/src/components/ui/`  
**Components:**
- `Button` - Styled button variants
- `Input` - Form input with validation
- `Select` - Dropdown select
- `Table` - Data table with sorting/pagination
- `Card` - Content card container
- `Modal` / `Dialog` - Overlay dialogs
- `Badge` - Status badges
- `Alert` - Notification alerts
- `Tabs` - Tab navigation
- `Toast` - Toast notifications

---

### Layout Components
**Directory:** `frontend/src/components/`  
**Components:**
- `MainLayout` - App shell with sidebar
- `Sidebar` - Navigation sidebar
- `Header` - Top header bar
- `Footer` - Page footer
- `LoadingSpinner` - Loading indicator

---

### Form Components
**Directory:** `frontend/src/components/forms/`  
**Components:**
- `ProductForm` - Product create/edit
- `LotForm` - Lot create/edit
- `CustomerForm` - Customer create/edit
- `SupplierForm` - Supplier create/edit
- `UserForm` - User create/edit

---

## 🔌 Frontend Services

### apiClient
**File:** `frontend/src/services/apiClient.js`  
**Purpose:** HTTP client with auth  
**Methods:**
- `get(endpoint)`, `post(endpoint, data)`
- `put(endpoint, data)`, `delete(endpoint)`
- `uploadFile(endpoint, file)`
- Token management, refresh flow

---

### reportsService
**File:** `frontend/src/services/reportsService.js`  
**Purpose:** Reports API calls  
**Methods:**
- `getSalesReport(params)`
- `getInventoryReport(params)`
- `getProfitLossReport(params)`
- `getLotExpiryReport(params)`

---

### posService
**File:** `frontend/src/services/posService.js`  
**Purpose:** POS operations  
**Methods:**
- `processSale(cart, payment)`
- `processReturn(invoiceId, items)`
- `openShift(openingCash)`
- `closeShift(closingCash)`

---

## 🛠️ Utilities

### Export Utilities
**File:** `frontend/src/utils/export.js`  
**Functions:**
- `exportToCSV(filename, data)`
- `exportToExcel(filename, data)`

**File:** `frontend/src/utils/pdfExport.js`  
**Functions:**
- `exportToPDF(filename, title, columns, data)`
- `exportProfitReportPDF(reportData, dateRange)`
- `exportLotExpiryPDF(reportData, filterDays)`

---

### Formatting Utilities
**File:** `frontend/src/utils/formatters.js`  
**Functions:**
- `formatCurrency(amount)`
- `formatDate(date)`
- `formatNumber(number)`

---

### Validation Utilities
**File:** `frontend/src/utils/validation.js`  
**Functions:**
- `validateEmail(email)`
- `validatePhone(phone)`
- `validateRequired(value)`
- `validateMinLength(value, min)`

---

*Class Registry - Store ERP v2.0.0*
