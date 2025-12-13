# RBAC Permission Matrix

**Version:** 1.0  
**Created:** 2025-12-01  
**Last Updated:** 2025-12-01  
**Task:** P0.10 - Document RBAC Permission Matrix

---

## Overview

This document defines the Role-Based Access Control (RBAC) permission matrix for the Store Management System.

---

## Roles

| Role ID | Role Name (EN) | Role Name (AR) | Description |
|---------|----------------|----------------|-------------|
| admin | Admin | مدير النظام | Full system access |
| manager | Manager | مدير | Most operations except security settings |
| warehouse_manager | Warehouse Manager | مدير المخزون | Inventory and warehouse operations |
| sales | Sales | موظف المبيعات | Sales and customer operations |
| purchase | Purchase | موظف المشتريات | Purchase and supplier operations |
| accountant | Accountant | محاسب | Financial viewing and reports |
| viewer | Viewer | مشاهد | Read-only access |
| user | User | مستخدم | Basic access |

---

## Permission Categories

### System Administration

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| admin_full | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| user_management | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| role_management | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| system_settings | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| manage_security | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| view_security | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| view_audit_log | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### User Profile

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| profile_view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| profile_edit | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

### Inventory / Products

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| inventory_view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| inventory_add | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| inventory_edit | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| inventory_delete | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| inventory_export | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

### Categories

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| category_view | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| category_add | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| category_edit | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| category_delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Warehouses

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| warehouse_view | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| warehouse_add | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| warehouse_edit | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| warehouse_delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| warehouse_transfer | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

### Sales

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| sales_view | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| sales_add | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| sales_edit | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| sales_delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| sales_approve | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Purchases

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| purchases_view | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| purchases_add | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| purchases_edit | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| purchases_delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| purchases_approve | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Customers

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| customer_view | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| customer_add | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| customer_edit | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| customer_delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Suppliers

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| supplier_view | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| supplier_add | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| supplier_edit | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| supplier_delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Invoices

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| invoice_view | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| invoice_add | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| invoice_edit | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| invoice_delete | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| invoice_approve | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| invoice_void | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Reports

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| reports_view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| reports_export | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| reports_advanced | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| reports_financial | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |

### Dashboard

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| dashboard_view | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| dashboard_admin | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Treasury

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| treasury_view | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| treasury_add | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| treasury_edit | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| treasury_delete | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| treasury_transfer | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Excel Operations

| Permission | Admin | Manager | Warehouse | Sales | Purchase | Accountant | Viewer |
|------------|:-----:|:-------:|:---------:|:-----:|:--------:|:----------:|:------:|
| excel_import | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| excel_export | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## Implementation

### Backend Permission Decorator

```python
from src.permissions import require_permission, Permissions

@app.route('/api/products', methods=['POST'])
@token_required
@require_permission(Permissions.INVENTORY_ADD)
def create_product():
    ...
```

### Multiple Permissions (AND)

```python
@require_permission(Permissions.INVENTORY_EDIT, Permissions.WAREHOUSE_TRANSFER)
def transfer_stock():
    # Requires BOTH permissions
    ...
```

### Multiple Permissions (OR)

```python
@require_permission(Permissions.INVENTORY_ADD, Permissions.PURCHASES_ADD, any_of=True)
def add_item():
    # Requires ANY of the permissions
    ...
```

---

## API Response on Permission Denied

```json
{
    "success": false,
    "error": "permission_denied",
    "message": "ليس لديك صلاحية للوصول إلى هذه الوظيفة",
    "missing_permissions": ["inventory_delete"],
    "code": "INSUFFICIENT_PERMISSIONS"
}
```

HTTP Status: `403 Forbidden`

---

## Security Notes

1. **Admin Bypass**: Users with `admin_full` permission bypass all permission checks
2. **Arabic Role Names**: System supports both English and Arabic role names
3. **JWT Integration**: Permissions are checked after JWT token validation
4. **Audit Logging**: All permission denials are logged with user ID and requested resource

---

## Related Files

- `backend/src/permissions.py` - Permission constants and decorators
- `backend/src/routes/auth_unified.py` - Authentication decorators
- `backend/src/models/user.py` - User and Role models

