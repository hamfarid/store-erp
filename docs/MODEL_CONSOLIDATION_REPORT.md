# Model Consolidation Report

**Task:** P1.29  
**Date:** 2025-12-01  
**Status:** In Progress

---

## Executive Summary

The `backend/src/models/` directory contains multiple model files with duplicate or overlapping definitions. This report identifies the canonical sources and recommends consolidation actions.

---

## Model File Analysis

### User & Role Models

| File | Status | Recommendation |
|------|--------|----------------|
| `user.py` | ✅ **CANONICAL** | Primary source - actively used |
| `user_unified.py` | ⚠️ Duplicate | Merge unique features into `user.py` |
| `models.py` | ⚠️ Legacy | Contains minimal User/Role - deprecate |

**Active Imports:** `from src.models.user import User, Role`

### Invoice Models

| File | Status | Recommendation |
|------|--------|----------------|
| `invoice_unified.py` | ✅ **CANONICAL** | Primary invoice model |
| `unified_invoice.py` | ⚠️ Duplicate | Check for unique features, then deprecate |
| `invoice.py` | ⚠️ Legacy | Old implementation - keep for reference |
| `invoices.py` | ⚠️ Legacy | Old implementation - deprecate |
| `invoices_clean.py` | ⚠️ Duplicate | Deprecate |

### Product Models

| File | Status | Recommendation |
|------|--------|----------------|
| `product_unified.py` | ✅ **CANONICAL** | Primary product model |
| `product_advanced.py` | ⚠️ Extensions | Merge advanced features |

### Warehouse Models

| File | Status | Recommendation |
|------|--------|----------------|
| `warehouse_unified.py` | ✅ **CANONICAL** | Primary warehouse model |
| `warehouse_advanced.py` | ⚠️ Extensions | Merge into unified |
| `warehouse_adjustments.py` | ✅ Keep | Separate adjustment logic |
| `warehouse_constraints.py` | ✅ Keep | Constraint definitions |
| `warehouse_transfer.py` | ✅ Keep | Transfer operations |

### Partner Models

| File | Status | Recommendation |
|------|--------|----------------|
| `customer.py` | ✅ **CANONICAL** | Primary customer model |
| `supplier.py` | ✅ **CANONICAL** | Primary supplier model |
| `partners.py` | ⚠️ Duplicate | Check for unique features |

### Supporting Models

| File | Status | Recommendation |
|------|--------|----------------|
| `category.py` | ✅ **CANONICAL** | Category definitions |
| `inventory.py` | ✅ **CANONICAL** | Inventory management |
| `activity_log.py` | ✅ Keep | Audit logging |
| `notifications.py` | ✅ Keep | Notification system |
| `refresh_token.py` | ✅ Keep | JWT refresh tokens |
| `security_system.py` | ✅ Keep | Security features |

### Files to Remove/Archive

| File | Reason |
|------|--------|
| `models.py` | Contains outdated minimal models |
| `enhanced_models.py` | Features merged elsewhere |
| `unified_models.py` | Duplicate of unified files |
| `supporting_models.py` | Contents moved to specific files |
| `fix_all_files.py` | One-time migration script |
| `fix_imports.py` | One-time migration script |
| `simple_fix.py` | One-time migration script |
| `test_all_files.py` | Should be in tests/ |
| `test_entire_project.py` | Should be in tests/ |
| `*.backup` files | Backup files |
| `*.unify_backup_*` files | Migration backups |

---

## Canonical Model Sources

```python
# Primary model imports for the project
from src.models.user import User, Role
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.category import Category
from src.models.inventory import Product, Warehouse, StockMovement, Inventory
from src.models.invoice_unified import UnifiedInvoice, UnifiedInvoiceItem
from src.models.refresh_token import RefreshToken
from src.models.activity_log import ActivityLog
```

---

## Consolidation Actions

### Phase 1: Identify Active Models (Completed)
- [x] Scan for duplicate class definitions
- [x] Identify import usage patterns
- [x] Create canonical source list

### Phase 2: Merge Unique Features
- [ ] Compare `user_unified.py` with `user.py`
- [ ] Compare `unified_invoice.py` with `invoice_unified.py`
- [ ] Compare `product_advanced.py` with `product_unified.py`

### Phase 3: Update Imports
- [ ] Update all imports to use canonical sources
- [ ] Run tests to verify no breaks

### Phase 4: Archive Deprecated Files
- [ ] Move deprecated files to `models/_deprecated/`
- [ ] Update `.gitignore` if needed

---

## Model Relationship Diagram

```
User ──────┬──── Role
           │
           ├──── ActivityLog
           │
           └──── RefreshToken

Product ───┬──── Category
           │
           ├──── Warehouse ──── StockMovement
           │
           └──── Inventory

Customer ──┬──── UnifiedInvoice ──── UnifiedInvoiceItem
           │
Supplier ──┘
```

---

## Next Steps

1. Create `models/_deprecated/` directory
2. Move identified deprecated files
3. Update `__init__.py` with proper imports
4. Run full test suite
5. Document final model structure

---

## Notes

- Keep backup files until migration is confirmed successful
- Test all CRUD operations after consolidation
- Update Alembic migrations if model changes affect schema

