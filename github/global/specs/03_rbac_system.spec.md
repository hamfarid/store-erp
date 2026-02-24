# 📋 Spec: نظام الصلاحيات | RBAC System

**Version:** 2.0.0
**Date:** 2026-01-16
**Role:** The Architect
**Status:** ✅ Approved
**Priority:** ⭐⭐⭐ Critical

---

## 1. نظرة عامة | Overview

نظام صلاحيات متقدم (Role-Based Access Control) مع 68 صلاحية محددة و7 أدوار افتراضية. يوفر تحكماً دقيقاً في الوصول لكل عملية في النظام.

---

## 2. المتطلبات الوظيفية | Functional Requirements

### 2.1 إدارة الأدوار | Role Management
- [ ] FR-001: إنشاء دور جديد
- [ ] FR-002: تعديل صلاحيات الدور
- [ ] FR-003: حذف دور (إذا لم يكن مستخدماً)
- [ ] FR-004: نسخ دور موجود
- [ ] FR-005: عرض الأدوار مع صلاحياتها

### 2.2 إدارة المستخدمين | User Management
- [ ] FR-006: تعيين دور للمستخدم
- [ ] FR-007: تعيين أدوار متعددة للمستخدم
- [ ] FR-008: إزالة دور من المستخدم
- [ ] FR-009: عرض صلاحيات المستخدم الفعلية

### 2.3 التحقق من الصلاحيات | Permission Check
- [ ] FR-010: التحقق من صلاحية واحدة
- [ ] FR-011: التحقق من صلاحيات متعددة (AND)
- [ ] FR-012: التحقق من صلاحيات متعددة (OR)
- [ ] FR-013: التحقق حسب الكيان (Resource-based)

### 2.4 سجل التدقيق | Audit Log
- [ ] FR-014: تسجيل جميع التغييرات في الصلاحيات
- [ ] FR-015: تسجيل محاولات الوصول المرفوضة
- [ ] FR-016: تقارير سجل التدقيق

---

## 3. الأدوار الافتراضية (7 أدوار) | Default Roles

| Role | Arabic | Total Permissions |
|------|--------|-------------------|
| admin | مدير النظام | 68 (All) |
| manager | مدير | 55 |
| accountant | محاسب | 35 |
| cashier | كاشير | 20 |
| warehouse | مستودع | 25 |
| sales | مبيعات | 30 |
| viewer | مشاهد | 10 |

### 3.1 مدير النظام (Admin)
- جميع الصلاحيات (68)
- لا يمكن حذفه
- لا يمكن تعديل صلاحياته

### 3.2 مدير (Manager)
- إدارة المستخدمين
- إدارة المنتجات
- إدارة اللوتات
- التقارير
- الإعدادات

### 3.3 محاسب (Accountant)
- عرض المبيعات
- إدارة الفواتير
- التقارير المالية
- إدارة المدفوعات

### 3.4 كاشير (Cashier)
- نقاط البيع
- إنشاء الفواتير
- عرض المنتجات
- عرض العملاء

### 3.5 مستودع (Warehouse)
- إدارة اللوتات
- إدارة المخزون
- استلام البضائع
- جرد المخزون

### 3.6 مبيعات (Sales)
- إدارة العملاء
- إنشاء عروض الأسعار
- متابعة الطلبات
- عرض المنتجات

### 3.7 مشاهد (Viewer)
- عرض فقط
- بدون تعديل
- تقارير محدودة

---

## 4. الصلاحيات (68 صلاحية) | Permissions

### 4.1 Users (6)
| Permission | Description |
|------------|-------------|
| `user.view` | عرض المستخدمين |
| `user.create` | إنشاء مستخدم |
| `user.update` | تعديل مستخدم |
| `user.delete` | حذف مستخدم |
| `user.role.assign` | تعيين الأدوار |
| `user.password.reset` | إعادة تعيين كلمة المرور |

### 4.2 Products (6)
| Permission | Description |
|------------|-------------|
| `product.view` | عرض المنتجات |
| `product.create` | إنشاء منتج |
| `product.update` | تعديل منتج |
| `product.delete` | حذف منتج |
| `product.price.update` | تعديل السعر |
| `product.import` | استيراد المنتجات |

### 4.3 Lots (8)
| Permission | Description |
|------------|-------------|
| `lot.view` | عرض اللوتات |
| `lot.create` | إنشاء لوت |
| `lot.update` | تعديل لوت |
| `lot.delete` | حذف لوت |
| `lot.block` | حظر لوت |
| `lot.quality.update` | تحديث الجودة |
| `lot.transfer` | نقل بين المستودعات |
| `lot.override_fifo` | تجاوز FIFO |

### 4.4 POS (10)
| Permission | Description |
|------------|-------------|
| `pos.shift.open` | فتح وردية |
| `pos.shift.close` | إغلاق وردية |
| `pos.sale.create` | إنشاء مبيعة |
| `pos.sale.update` | تعديل مبيعة |
| `pos.sale.cancel` | إلغاء مبيعة |
| `pos.return.create` | إنشاء مرتجع |
| `pos.return.approve` | الموافقة على مرتجع |
| `pos.discount.apply` | تطبيق خصم |
| `pos.discount.override` | تجاوز حد الخصم |
| `pos.reports.view` | عرض تقارير POS |

### 4.5 Purchases (8)
| Permission | Description |
|------------|-------------|
| `purchase.view` | عرض المشتريات |
| `purchase.create` | إنشاء طلب شراء |
| `purchase.update` | تعديل طلب شراء |
| `purchase.delete` | حذف طلب شراء |
| `purchase.approve` | الموافقة على الطلب |
| `purchase.receive` | استلام البضائع |
| `purchase.payment` | تسجيل الدفع |
| `purchase.reports` | تقارير المشتريات |

### 4.6 Customers (6)
| Permission | Description |
|------------|-------------|
| `customer.view` | عرض العملاء |
| `customer.create` | إنشاء عميل |
| `customer.update` | تعديل عميل |
| `customer.delete` | حذف عميل |
| `customer.credit.update` | تعديل حد الائتمان |
| `customer.statement` | كشف حساب العميل |

### 4.7 Suppliers (6)
| Permission | Description |
|------------|-------------|
| `supplier.view` | عرض الموردين |
| `supplier.create` | إنشاء مورد |
| `supplier.update` | تعديل مورد |
| `supplier.delete` | حذف مورد |
| `supplier.payment` | تسجيل دفعة |
| `supplier.statement` | كشف حساب المورد |

### 4.8 Reports (8)
| Permission | Description |
|------------|-------------|
| `report.sales` | تقرير المبيعات |
| `report.purchases` | تقرير المشتريات |
| `report.inventory` | تقرير المخزون |
| `report.financial` | التقرير المالي |
| `report.profit` | تقرير الأرباح |
| `report.export` | تصدير التقارير |
| `report.schedule` | جدولة التقارير |
| `report.custom` | تقارير مخصصة |

### 4.9 Settings (6)
| Permission | Description |
|------------|-------------|
| `settings.view` | عرض الإعدادات |
| `settings.general` | الإعدادات العامة |
| `settings.security` | إعدادات الأمان |
| `settings.backup` | النسخ الاحتياطي |
| `settings.restore` | الاستعادة |
| `settings.system` | إعدادات النظام |

### 4.10 Dashboard (4)
| Permission | Description |
|------------|-------------|
| `dashboard.view` | عرض لوحة التحكم |
| `dashboard.widgets` | إدارة الويدجت |
| `dashboard.export` | تصدير البيانات |
| `dashboard.customize` | تخصيص اللوحة |

---

## 5. API Endpoints

### 5.1 Roles
```
GET    /api/v1/roles                    # List all roles
GET    /api/v1/roles/{id}               # Get role details
POST   /api/v1/roles                    # Create role
PUT    /api/v1/roles/{id}               # Update role
DELETE /api/v1/roles/{id}               # Delete role
GET    /api/v1/roles/{id}/permissions   # Get role permissions
PUT    /api/v1/roles/{id}/permissions   # Update role permissions
```

### 5.2 Permissions
```
GET    /api/v1/permissions              # List all permissions
GET    /api/v1/permissions/groups       # Get permission groups
```

### 5.3 User Roles
```
GET    /api/v1/users/{id}/roles         # Get user roles
POST   /api/v1/users/{id}/roles         # Assign role to user
DELETE /api/v1/users/{id}/roles/{role}  # Remove role from user
GET    /api/v1/users/{id}/permissions   # Get effective permissions
```

---

## 6. Database Schema

### 6.1 Roles Table
```sql
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    display_name_ar VARCHAR(100),
    description TEXT,
    is_system BOOLEAN DEFAULT FALSE,  -- Cannot be deleted
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.2 Permissions Table
```sql
CREATE TABLE permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    display_name_ar VARCHAR(150),
    group_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.3 Role Permissions Table
```sql
CREATE TABLE role_permissions (
    role_id INTEGER NOT NULL REFERENCES roles(id),
    permission_id INTEGER NOT NULL REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);
```

### 6.4 User Roles Table
```sql
CREATE TABLE user_roles (
    user_id INTEGER NOT NULL REFERENCES users(id),
    role_id INTEGER NOT NULL REFERENCES roles(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)
);
```

---

## 7. Permission Checking

### 7.1 Decorator Usage
```python
from functools import wraps
from flask import g, jsonify

def require_permission(*permissions, require_all=True):
    """
    Decorator to check permissions.
    
    Usage:
        @require_permission('product.create')
        @require_permission('product.view', 'product.update', require_all=False)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user:
                return jsonify({'error': 'Unauthorized'}), 401
            
            user_permissions = get_user_permissions(g.current_user.id)
            
            if require_all:
                if not all(p in user_permissions for p in permissions):
                    return jsonify({'error': 'Forbidden'}), 403
            else:
                if not any(p in user_permissions for p in permissions):
                    return jsonify({'error': 'Forbidden'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 7.2 Service Usage
```python
def check_permission(user_id, permission):
    """Check if user has specific permission"""
    user_permissions = get_user_permissions(user_id)
    return permission in user_permissions

def get_user_permissions(user_id):
    """Get all effective permissions for user"""
    roles = get_user_roles(user_id)
    permissions = set()
    for role in roles:
        permissions.update(get_role_permissions(role.id))
    return permissions
```

---

## 8. Security Considerations

### 8.1 Admin Protection
- Admin role cannot be deleted
- Admin permissions cannot be modified
- At least one admin user must exist

### 8.2 Audit Trail
- Log all permission changes
- Log all role assignments
- Log access denied attempts

### 8.3 Session Invalidation
- Invalidate user sessions when permissions change
- Require re-login after role assignment

---

## 9. Testing Requirements

### 9.1 Unit Tests
- [ ] Test permission checking
- [ ] Test role assignment
- [ ] Test permission inheritance
- [ ] Test admin protection

### 9.2 Integration Tests
- [ ] Test API authorization
- [ ] Test frontend authorization
- [ ] Test session invalidation

---

## 10. Related Files

- `backend/src/models/role.py` - Role model
- `backend/src/models/permission.py` - Permission model
- `backend/src/utils/auth.py` - Authorization utilities
- `backend/src/routes/rbac_routes.py` - RBAC API routes
- `frontend/src/contexts/AuthContext.jsx` - Auth context

---

*Spec Status: ✅ Approved*
*Implementation: ✅ Complete*
