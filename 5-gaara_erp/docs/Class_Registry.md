# CLASS REGISTRY - Gaara ERP v12

**Generated**: 2025-11-18 09:20
**Purpose**: Canonical registry of all classes/models with duplicate detection
**Status**: APPEND-ONLY (never delete entries)

---

## 🔴 CRITICAL: DUPLICATE MODELS DETECTED

### User Model - 3 LOCATIONS ⚠️

#### 1. **CANONICAL**: core_modules.users.models.User
- **Location**: `gaara_erp/core_modules/users/models.py:89`
- **Parent**: `AbstractUser` (Django built-in)
- **App Label**: `users`
- **Purpose**: Primary user model for authentication & authorization
- **Key Fields**:
  - `email` (EmailField, unique, indexed)
  - `username` (CharField, unique)
  - `first_name`, `last_name` (CharField)
  - `phone`, `mobile` (CharField)
  - `failed_login_attempts` (PositiveIntegerField) ✅
  - `account_locked_until` (DateTimeField)
  - `email_verified`, `phone_verified` (BooleanField)
  - `language`, `timezone` (CharField)
- **Relations**:
  - `user_companies` → ManyToMany to Company
  - `user_branches` → ManyToMany to Branch
- **Methods**:
  - `__str__()`, `get_full_name()`, `get_short_name()`
  - `lock_account()`, `unlock_account()`
- **DB Table**: `users_user`
- **Status**: ✅ ACTIVE - Use this

#### 2. **PROXY**: core_modules.users_accounts.models.User
- **Location**: `gaara_erp/core_modules/users_accounts/models.py:16`
- **Parent**: `CanonicalUser` (proxy to core_modules.users.models.User)
- **App Label**: `users_accounts`
- **Purpose**: Backward compatibility proxy
- **Status**: ⚠️ DEPRECATED - Migrate imports to canonical
- **Action**: Remove after all imports updated

#### 3. **DUPLICATE**: api_server.src.models.user.User
- **Location**: `gaara_erp/api_server/src/models/user.py`
- **Status**: ❌ DUPLICATE - Needs investigation
- **Action**: Review and likely remove

---

### Company Model - 3 LOCATIONS ⚠️

#### 1. **CANONICAL**: core_modules.core.models.Company
- **Location**: `gaara_erp/core_modules/core/models.py:106`
- **Parent**: `TimestampedModel, UserTrackedModel`
- **App Label**: `core`
- **Purpose**: Primary company model
- **Key Fields**:
  - `name` (CharField, max_length=255)
  - `code` (CharField, unique, max_length=50, nullable)
  - `description` (TextField, nullable)
  - `country` (ForeignKey to Country, nullable)
  - `registration_number`, `vat_number` (CharField, nullable)
  - `logo` (ImageField)
  - `is_active` (BooleanField, default=True)
- **Mixins**:
  - `TimestampedModel`: adds `created_at`, `updated_at`
  - `UserTrackedModel`: adds `created_by`, `updated_by`
- **DB Table**: `core_company`
- **Status**: ✅ ACTIVE - Use this

#### 2. **DUPLICATE**: core_modules.organization.models.Company
- **Location**: `gaara_erp/core_modules/organization/models.py:175`
- **Parent**: `models.Model`
- **App Label**: `organization`
- **Purpose**: Duplicate company model
- **Key Fields**:
  - `name` (CharField, unique, max_length=200)
  - `legal_name` (CharField, nullable)
  - `code` (CharField, unique, max_length=20)
  - `parent_company` (ForeignKey to self)
- **Status**: ❌ DUPLICATE - Consolidate with canonical
- **DB Table**: `organization_company`
- **Action**: Migrate data, update imports, remove

#### 3. **DUPLICATE**: services_modules.core.models.company.Company
- **Location**: `gaara_erp/services_modules/core/models/company.py`
- **Status**: ❌ DUPLICATE - Needs investigation
- **Action**: Review and likely remove

---

### Invoice Models - MULTIPLE DUPLICATES ⚠️

#### SalesInvoice - 2 LOCATIONS

##### 1. **CANONICAL**: business_modules.accounting.invoices.SalesInvoice
- **Location**: `gaara_erp/business_modules/accounting/invoices.py:23`
- **Parent**: `models.Model`
- **App Label**: `accounting`
- **Key Fields**:
  - `invoice_number` (CharField, unique)
  - `customer` (ForeignKey to Contact)
  - `invoice_date`, `due_date` (DateField)
  - `total_amount`, `tax_amount`, `net_amount`, `paid_amount` (DecimalField)
  - `status` (CharField, choices)
- **Status**: ✅ ACTIVE - Use this

##### 2. **DUPLICATE**: business_modules.sales.models.sales_invoice.SalesInvoice
- **Location**: `gaara_erp/business_modules/sales/models/sales_invoice.py`
- **Status**: ❌ DUPLICATE - Consolidate with canonical
- **Action**: Migrate data, update imports, remove

#### PurchaseInvoice - 3 LOCATIONS

##### 1. **CANONICAL**: business_modules.accounting.invoices.PurchaseInvoice
- **Location**: `gaara_erp/business_modules/accounting/invoices.py:95`
- **Parent**: `models.Model`
- **App Label**: `accounting`
- **Key Fields**: Similar to SalesInvoice but with `supplier` instead of `customer`
- **Status**: ✅ ACTIVE - Use this

##### 2. **DUPLICATE**: business_modules.purchasing.models.purchase_invoice.PurchaseInvoice
- **Location**: `gaara_erp/business_modules/purchasing/models/purchase_invoice.py`
- **Status**: ❌ DUPLICATE - Consolidate with canonical

##### 3. **DUPLICATE**: business_modules.purchasing.models.supplier_invoice.SupplierInvoice
- **Location**: `gaara_erp/business_modules/purchasing/models/supplier_invoice.py`
- **Status**: ❌ DUPLICATE - Likely same as PurchaseInvoice
- **Action**: Review and consolidate

---

## ✅ CANONICAL MODELS (No Duplicates)

### Core Models

#### Country
- **Location**: `gaara_erp/core_modules/core/models.py`
- **App Label**: `core`
- **Fields**: `name`, `code`, `region`, `is_active`
- **Status**: ✅ CANONICAL

#### Currency
- **Location**: `gaara_erp/core_modules/core/models.py`
- **App Label**: `core`
- **Fields**: `name`, `code`, `symbol`, `is_active`
- **Status**: ✅ CANONICAL

#### Branch
- **Location**: `gaara_erp/core_modules/core/models.py`
- **App Label**: `core`
- **Fields**: `name`, `code`, `company` (FK), `is_active`
- **Status**: ✅ CANONICAL

#### Department
- **Location**: `gaara_erp/core_modules/core/models.py`
- **App Label**: `core`
- **Fields**: `name`, `code`, `company` (FK), `description`, `is_active`
- **Status**: ✅ CANONICAL

---

## 📊 DUPLICATE SUMMARY

| Model | Canonical Location | Duplicate Count | Action Required |
|-------|-------------------|-----------------|-----------------|
| **User** | `core_modules.users.models` | 2 | Remove proxy + api_server duplicate |
| **Company** | `core_modules.core.models` | 2 | Consolidate organization + services duplicates |
| **SalesInvoice** | `business_modules.accounting.invoices` | 1 | Consolidate sales duplicate |
| **PurchaseInvoice** | `business_modules.accounting.invoices` | 2 | Consolidate purchasing duplicates |

**Total Duplicates**: 7 duplicate model definitions
**Total Canonical Models**: 100+ (estimated)

---

## 🔧 CONSOLIDATION PLAN

### Phase 1: User Model (Priority: HIGH)
1. Update all imports from `users_accounts.models.User` → `users.models.User`
2. Remove `core_modules/users_accounts/models.py` proxy
3. Investigate and remove `api_server/src/models/user.py`

### Phase 2: Company Model (Priority: HIGH)
1. Migrate data from `organization_company` → `core_company`
2. Update all imports from `organization.models.Company` → `core.models.Company`
3. Remove `core_modules/organization/models.py` Company class
4. Investigate and remove `services_modules/core/models/company.py`

### Phase 3: Invoice Models (Priority: MEDIUM)
1. Consolidate SalesInvoice: accounting (canonical) ← sales (duplicate)
2. Consolidate PurchaseInvoice: accounting (canonical) ← purchasing (duplicates)
3. Update all imports
4. Remove duplicate files

---

**Next Update**: After consolidation complete
**Maintained By**: Autonomous AI Agent
**Last Audit**: 2025-11-18

