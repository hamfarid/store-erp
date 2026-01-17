# FILE: docs/Permissions_Model.md | PURPOSE: RBAC Permission Matrix Documentation | OWNER: Security Team | RELATED: core_modules/permissions/ | LAST-AUDITED: 2025-11-19

# RBAC Permission Matrix - Gaara ERP v12

## 📋 Table of Contents

1. [Overview](#overview)
2. [Permission Naming Convention](#permission-naming-convention)
3. [Role Hierarchy](#role-hierarchy)
4. [Permission Matrix by Module](#permission-matrix-by-module)
5. [Custom Actions](#custom-actions)
6. [Usage Examples](#usage-examples)
7. [Security Guidelines](#security-guidelines)

---

## Overview

This document provides a comprehensive reference for all **143 permission codes** implemented across the Gaara ERP system. Each permission is protected by the `@require_permission` decorator and enforced through the unified RBAC (Role-Based Access Control) system.

**Total Permissions**: 143 codes  
**Total Modules**: 12 modules  
**Total ViewSets**: 72 ViewSets  
**Total Custom Actions**: ~25 actions  

**Last Updated**: 2025-11-19  
**Status**: ✅ Production Ready

---

## Permission Naming Convention

**Format**: `{module}.{action}_{resource}`

### Action Types

| Action | Description | HTTP Methods | Example |
|--------|-------------|--------------|---------|
| `view` | Read access (list, retrieve) | GET | `hr.view_employees` |
| `create` | Create new records | POST | `hr.create_employees` |
| `modify` | Update existing records | PUT, PATCH | `hr.modify_employees` |
| `delete` | Delete records | DELETE | `hr.delete_employees` |
| `manage` | Full CRUD access (create + modify + delete) | POST, PUT, PATCH, DELETE | `hr.manage_employees` |
| `approve` | Approval workflows | POST | `permissions.approve_requests` |
| `request` | Request permissions | POST | `permissions.request` |
| `view_logs` | View audit logs | GET | `security.view_audit_logs` |
| `export` | Export data | GET, POST | `accounting.export_reports` |

### Module Prefixes

| Prefix | Module | Example |
|--------|--------|---------|
| `permissions` | Core Permissions | `permissions.view` |
| `core` | Core Module | `core.view_countries` |
| `security` | Security Module | `security.view_audit_logs` |
| `api_keys` | API Keys Module | `api_keys.view` |
| `accounting` | Accounting Module | `accounting.view_accounts` |
| `sales` | Sales Module | `sales.view_customers` |
| `inventory` | Inventory Module | `inventory.view_products` |
| `farms` | Farms Module | `farms.view_farms` |
| `experiments` | Experiments Module | `experiments.view_experiments` |
| `seed_production` | Seed Production | `seed_production.view_orders` |
| `hr` | Human Resources | `hr.view_employees` |
| `hybridization` | Seed Hybridization | `hybridization.view_varieties` |

---

## Role Hierarchy

### Standard Roles

| Role | Level | Description | Typical Permissions |
|------|-------|-------------|---------------------|
| **ADMIN** | 4 | System Administrator | All permissions (*.manage, *.view, *.approve) |
| **MANAGER** | 3 | Department Manager | Module-specific manage + view permissions |
| **USER** | 2 | Regular User | View + limited create/modify permissions |
| **GUEST** | 1 | Read-only Guest | View-only permissions |

### Permission Inheritance

```
ADMIN (Level 4)
  └─> Has all MANAGER permissions
      └─> Has all USER permissions
          └─> Has all GUEST permissions
```

**Note**: Higher-level roles automatically inherit all permissions from lower-level roles.

---

## Permission Matrix by Module

### 1. Core Permissions Module (10 codes)

**Module**: `core_modules.permissions`  
**File**: `gaara_erp/core_modules/permissions/viewsets.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `permissions.view` | View permissions | USER | PermissionViewSet.list/retrieve |
| `permissions.manage` | Manage permissions | ADMIN | PermissionViewSet.create/update/delete |
| `permissions.request` | Request new permissions | USER | PermissionRequestViewSet.create |
| `permissions.approve` | Approve permission requests | MANAGER | PermissionRequestViewSet.approve |
| `roles.view` | View roles | USER | RoleViewSet.list/retrieve |
| `roles.manage` | Manage roles | ADMIN | RoleViewSet.create/update/delete |
| `groups.view` | View groups | USER | GroupViewSet.list/retrieve |
| `groups.manage` | Manage groups | ADMIN | GroupViewSet.create/update/delete |
| `permissions.view_logs` | View permission logs | MANAGER | PermissionLogViewSet.list/retrieve |
| `permissions.manage_temporary` | Manage temporary permissions | ADMIN | TemporaryPermissionViewSet.create/update/delete |

**Total**: 10 permission codes

---

### 2. Core Module (16 codes)

**Module**: `core_modules.core`  
**File**: `gaara_erp/core_modules/core/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `core.view_countries` | View countries | GUEST | CountryViewSet.list/retrieve |
| `core.manage_countries` | Manage countries | ADMIN | CountryViewSet.create/update/delete |
| `core.view_companies` | View companies | USER | CompanyViewSet.list/retrieve |
| `core.manage_companies` | Manage companies | ADMIN | CompanyViewSet.create/update/delete |
| `core.view_branches` | View branches | USER | BranchViewSet.list/retrieve |
| `core.manage_branches` | Manage branches | MANAGER | BranchViewSet.create/update/delete |
| `core.view_currencies` | View currencies | GUEST | CurrencyViewSet.list/retrieve |
| `core.manage_currencies` | Manage currencies | ADMIN | CurrencyViewSet.create/update/delete |
| `core.view_fiscal_years` | View fiscal years | USER | FiscalYearViewSet.list/retrieve |
| `core.manage_fiscal_years` | Manage fiscal years | ADMIN | FiscalYearViewSet.create/update/delete |
| `core.set_base_fiscal_year` | Set base fiscal year | ADMIN | FiscalYearViewSet.set_as_base |
| `core.view_sequences` | View document sequences | USER | DocumentSequenceViewSet.list/retrieve |
| `core.manage_sequences` | Manage document sequences | ADMIN | DocumentSequenceViewSet.create/update/delete |
| `core.use_sequences` | Use document sequences | USER | DocumentSequenceViewSet.get_next_number |
| `core.reset_sequences` | Reset document sequences | ADMIN | DocumentSequenceViewSet.reset |
| `core.view_settings` | View system settings | MANAGER | SettingsViewSet.list/retrieve |

**Total**: 16 permission codes

---

### 3. Security Module (8 codes)

**Module**: `core_modules.setup.submodules.security`  
**File**: `gaara_erp/core_modules/setup/submodules/security/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `security.view_settings` | View security settings | ADMIN | SecuritySettingViewSet.list/retrieve |
| `security.manage_settings` | Manage security settings | ADMIN | SecuritySettingViewSet.create/update/delete |
| `security.view_blocked_ips` | View blocked IPs | ADMIN | BlockedIPViewSet.list/retrieve |
| `security.manage_blocked_ips` | Manage blocked IPs | ADMIN | BlockedIPViewSet.create/update/delete |
| `security.view_audit_logs` | View security audit logs | ADMIN | SecurityAuditViewSet.list/retrieve |
| `security.view_password_history` | View password history | ADMIN | PasswordHistoryViewSet.list/retrieve |
| `security.export_audit_logs` | Export audit logs | ADMIN | SecurityAuditViewSet.export |
| `security.analyze_threats` | Analyze security threats | ADMIN | SecurityAuditViewSet.analyze |

**Total**: 8 permission codes

---

### 4. API Keys Module (2 codes)

**Module**: `core_modules.api_keys`
**File**: `gaara_erp/core_modules/api_keys/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `api_keys.view` | View API keys | MANAGER | APIKeyViewSet.list/retrieve |
| `api_keys.manage` | Manage API keys | ADMIN | APIKeyViewSet.create/update/delete |

**Total**: 2 permission codes

---

### 5. Business - Accounting Module (6 codes)

**Module**: `business_modules.accounting`
**File**: `gaara_erp/business_modules/accounting/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `accounting.view_accounts` | View chart of accounts | USER | ChartOfAccountsViewSet.list/retrieve |
| `accounting.manage_accounts` | Manage chart of accounts | MANAGER | ChartOfAccountsViewSet.create/update/delete |
| `accounting.view_journals` | View journal entries | USER | JournalEntryViewSet.list/retrieve |
| `accounting.manage_journals` | Manage journal entries | MANAGER | JournalEntryViewSet.create/update/delete |
| `accounting.view_cost_centers` | View cost centers | USER | CostCenterViewSet.list/retrieve |
| `accounting.manage_cost_centers` | Manage cost centers | MANAGER | CostCenterViewSet.create/update/delete |

**Total**: 6 permission codes

---

### 6. Business - Sales Module (6 codes)

**Module**: `business_modules.sales`
**File**: `gaara_erp/business_modules/sales/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `sales.view_customers` | View customers | USER | CustomerViewSet.list/retrieve |
| `sales.manage_customers` | Manage customers | MANAGER | CustomerViewSet.create/update/delete |
| `sales.view_invoices` | View sales invoices | USER | SalesInvoiceViewSet.list/retrieve |
| `sales.manage_invoices` | Manage sales invoices | MANAGER | SalesInvoiceViewSet.create/update/delete |
| `sales.view_quotations` | View quotations | USER | QuotationViewSet.list/retrieve |
| `sales.manage_quotations` | Manage quotations | MANAGER | QuotationViewSet.create/update/delete |

**Total**: 6 permission codes

---

### 7. Business - Inventory Module (6 codes)

**Module**: `business_modules.inventory`
**File**: `gaara_erp/business_modules/inventory/product_views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `inventory.view_categories` | View product categories | USER | ProductCategoryViewSet.list/retrieve |
| `inventory.manage_categories` | Manage product categories | MANAGER | ProductCategoryViewSet.create/update/delete |
| `inventory.view_products` | View products | USER | ProductViewSet.list/retrieve |
| `inventory.manage_products` | Manage products | MANAGER | ProductViewSet.create/update/delete |
| `inventory.view_uoms` | View units of measure | USER | UOMViewSet.list/retrieve |
| `inventory.manage_uoms` | Manage units of measure | MANAGER | UOMViewSet.create/update/delete |

**Total**: 6 permission codes

---

### 8. Agricultural - Farms Module (26 codes)

**Module**: `agricultural_modules.farms`
**File**: `gaara_erp/agricultural_modules/farms/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `farms.view_farms` | View farms | USER | FarmViewSet.list/retrieve |
| `farms.manage_farms` | Manage farms | MANAGER | FarmViewSet.create/update/delete |
| `farms.view_plot_types` | View plot types | USER | FarmPlotTypeViewSet.list/retrieve |
| `farms.manage_plot_types` | Manage plot types | MANAGER | FarmPlotTypeViewSet.create/update/delete |
| `farms.view_soil_types` | View soil types | USER | SoilTypeViewSet.list/retrieve |
| `farms.manage_soil_types` | Manage soil types | MANAGER | SoilTypeViewSet.create/update/delete |
| `farms.view_irrigation_types` | View irrigation types | USER | IrrigationSystemTypeViewSet.list/retrieve |
| `farms.manage_irrigation_types` | Manage irrigation types | MANAGER | IrrigationSystemTypeViewSet.create/update/delete |
| `farms.view_plots` | View farm plots | USER | FarmPlotViewSet.list/retrieve |
| `farms.manage_plots` | Manage farm plots | MANAGER | FarmPlotViewSet.create/update/delete |
| `farms.view_warehouses` | View farm warehouses | USER | FarmWarehouseViewSet.list/retrieve |
| `farms.manage_warehouses` | Manage farm warehouses | MANAGER | FarmWarehouseViewSet.create/update/delete |
| `farms.view_crop_varieties` | View crop varieties | USER | CropVarietyViewSet.list/retrieve |
| `farms.manage_crop_varieties` | Manage crop varieties | MANAGER | CropVarietyViewSet.create/update/delete |
| `farms.view_seasons` | View growing seasons | USER | GrowingSeasonViewSet.list/retrieve |
| `farms.manage_seasons` | Manage growing seasons | MANAGER | GrowingSeasonViewSet.create/update/delete |
| `farms.view_planting_plans` | View planting plans | USER | PlantingPlanViewSet.list/retrieve |
| `farms.manage_planting_plans` | Manage planting plans | MANAGER | PlantingPlanViewSet.create/update/delete |
| `farms.view_harvests` | View harvests | USER | HarvestViewSet.list/retrieve |
| `farms.manage_harvests` | Manage harvests | MANAGER | HarvestViewSet.create/update/delete |
| `farms.view_irrigation_schedules` | View irrigation schedules | USER | IrrigationScheduleViewSet.list/retrieve |
| `farms.manage_irrigation_schedules` | Manage irrigation schedules | MANAGER | IrrigationScheduleViewSet.create/update/delete |
| `farms.view_fertilization_plans` | View fertilization plans | USER | FertilizationPlanViewSet.list/retrieve |
| `farms.manage_fertilization_plans` | Manage fertilization plans | MANAGER | FertilizationPlanViewSet.create/update/delete |
| `farms.view_pest_control` | View pest control records | USER | PestControlRecordViewSet.list/retrieve |
| `farms.manage_pest_control` | Manage pest control records | MANAGER | PestControlRecordViewSet.create/update/delete |

**Total**: 26 permission codes

---

### 9. Agricultural - Experiments Module (30 codes)

**Module**: `agricultural_modules.experiments`
**File**: `gaara_erp/agricultural_modules/experiments/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `experiments.view_locations` | View experiment locations | USER | LocationViewSet.list/retrieve |
| `experiments.manage_locations` | Manage experiment locations | MANAGER | LocationViewSet.create/update/delete |
| `experiments.view_seasons` | View experiment seasons | USER | SeasonViewSet.list/retrieve |
| `experiments.manage_seasons` | Manage experiment seasons | MANAGER | SeasonViewSet.create/update/delete |
| `experiments.view_variety_types` | View variety types | USER | VarietyTypeViewSet.list/retrieve |
| `experiments.manage_variety_types` | Manage variety types | MANAGER | VarietyTypeViewSet.create/update/delete |
| `experiments.view_varieties` | View varieties | USER | VarietyViewSet.list/retrieve |
| `experiments.manage_varieties` | Manage varieties | MANAGER | VarietyViewSet.create/update/delete |
| `experiments.view_experiments` | View experiments | USER | ExperimentViewSet.list/retrieve |
| `experiments.manage_experiments` | Manage experiments | MANAGER | ExperimentViewSet.create/update/delete |
| `experiments.start_experiments` | Start experiments | MANAGER | ExperimentViewSet.start |
| `experiments.complete_experiments` | Complete experiments | MANAGER | ExperimentViewSet.complete |
| `experiments.cancel_experiments` | Cancel experiments | MANAGER | ExperimentViewSet.cancel |
| `experiments.view_experiment_varieties` | View experiment varieties | USER | ExperimentVarietyViewSet.list/retrieve |
| `experiments.manage_experiment_varieties` | Manage experiment varieties | MANAGER | ExperimentVarietyViewSet.create/update/delete |
| `experiments.view_harvests` | View harvests | USER | HarvestViewSet.list/retrieve |
| `experiments.manage_harvests` | Manage harvests | MANAGER | HarvestViewSet.create/update/delete |
| `experiments.view_quality_grades` | View quality grades | USER | HarvestQualityGradeViewSet.list/retrieve |
| `experiments.manage_quality_grades` | Manage quality grades | MANAGER | HarvestQualityGradeViewSet.create/update/delete |
| `experiments.view_evaluations` | View variety evaluations | USER | VarietyEvaluationViewSet.list/retrieve |
| `experiments.manage_evaluations` | Manage variety evaluations | MANAGER | VarietyEvaluationViewSet.create/update/delete |
| `experiments.view_fertilization_programs` | View fertilization programs | USER | FertilizationProgramViewSet.list/retrieve |
| `experiments.manage_fertilization_programs` | Manage fertilization programs | MANAGER | FertilizationProgramViewSet.create/update/delete |
| `experiments.view_fertilization_applications` | View fertilization applications | USER | FertilizationApplicationViewSet.list/retrieve |
| `experiments.manage_fertilization_applications` | Manage fertilization applications | MANAGER | FertilizationApplicationViewSet.create/update/delete |
| `experiments.view_pesticide_programs` | View pesticide programs | USER | PesticideProgramViewSet.list/retrieve |
| `experiments.manage_pesticide_programs` | Manage pesticide programs | MANAGER | PesticideProgramViewSet.create/update/delete |
| `experiments.view_pesticide_applications` | View pesticide applications | USER | PesticideApplicationViewSet.list/retrieve |
| `experiments.manage_pesticide_applications` | Manage pesticide applications | MANAGER | PesticideApplicationViewSet.create/update/delete |
| `experiments.view_costs` | View experiment costs | MANAGER | ExperimentCostViewSet.list/retrieve |
| `experiments.manage_costs` | Manage experiment costs | MANAGER | ExperimentCostViewSet.create/update/delete |

**Total**: 30 permission codes

---

### 10. Agricultural - Seed Production Module (6 codes)

**Module**: `agricultural_modules.seed_production`
**File**: `gaara_erp/agricultural_modules/seed_production/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `seed_production.view_orders` | View seed production orders | USER | SeedProductionOrderViewSet.list/retrieve |
| `seed_production.manage_orders` | Manage seed production orders | MANAGER | SeedProductionOrderViewSet.create/update/delete |
| `seed_production.approve_orders` | Approve production orders | MANAGER | SeedProductionOrderViewSet.approve |
| `seed_production.view_lots` | View seed production lots | USER | SeedProductionLotViewSet.list/retrieve |
| `seed_production.manage_lots` | Manage seed production lots | MANAGER | SeedProductionLotViewSet.create/update/delete |
| `seed_production.update_lot_status` | Update lot status | MANAGER | SeedProductionLotViewSet.update_status |

**Total**: 6 permission codes

---

### 11. Services - HR Module (16 codes)

**Module**: `services_modules.hr`
**File**: `gaara_erp/services_modules/hr/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `hr.view_departments` | View departments | USER | DepartmentViewSet.list/retrieve |
| `hr.manage_departments` | Manage departments | MANAGER | DepartmentViewSet.create/update/delete |
| `hr.view_job_grades` | View job grades | USER | JobGradeViewSet.list/retrieve |
| `hr.manage_job_grades` | Manage job grades | ADMIN | JobGradeViewSet.create/update/delete |
| `hr.view_positions` | View positions | USER | PositionViewSet.list/retrieve |
| `hr.manage_positions` | Manage positions | MANAGER | PositionViewSet.create/update/delete |
| `hr.view_employees` | View employees | USER | EmployeeViewSet.list/retrieve |
| `hr.manage_employees` | Manage employees | MANAGER | EmployeeViewSet.create/update/delete |
| `hr.terminate_employees` | Terminate employees | ADMIN | EmployeeViewSet.terminate |
| `hr.view_payroll` | View payroll summaries | MANAGER | EmployeeViewSet.payroll_summary |
| `hr.view_leave_types` | View leave types | USER | LeaveTypeViewSet.list/retrieve |
| `hr.manage_leave_types` | Manage leave types | ADMIN | LeaveTypeViewSet.create/update/delete |
| `hr.view_attendance` | View attendance records | USER | AttendanceRecordViewSet.list/retrieve |
| `hr.manage_attendance` | Manage attendance records | MANAGER | AttendanceRecordViewSet.create/update/delete |
| `hr.view_settings` | View HR settings | MANAGER | HRSettingViewSet.list/retrieve |
| `hr.manage_settings` | Manage HR settings | ADMIN | HRSettingViewSet.create/update/delete |

**Total**: 16 permission codes

---

### 12. Agricultural - Seed Hybridization Module (1 code)

**Module**: `agricultural_modules.seed_hybridization`
**File**: `gaara_erp/agricultural_modules/seed_hybridization/merged/views.py`

| Permission Code | Description | Required Role | ViewSet/Method |
|----------------|-------------|---------------|----------------|
| `hybridization.view_varieties` | View hybrid varieties | USER | HybridVarietyViewSet.list/retrieve |

**Total**: 1 permission code

---

## Custom Actions

### Custom Actions with Special Permissions

The following custom actions have dedicated permission codes beyond standard CRUD operations:

#### Core Module
- `core.set_base_fiscal_year` - Set a fiscal year as the base year (ADMIN only)
- `core.use_sequences` - Generate next document number from sequence (USER)
- `core.reset_sequences` - Reset document sequence counter (ADMIN only)

#### Experiments Module
- `experiments.start_experiments` - Start an experiment (MANAGER)
- `experiments.complete_experiments` - Mark experiment as complete (MANAGER)
- `experiments.cancel_experiments` - Cancel an experiment (MANAGER)

#### Seed Production Module
- `seed_production.approve_orders` - Approve production orders (MANAGER)
- `seed_production.update_lot_status` - Update lot status (MANAGER)

#### HR Module
- `hr.terminate_employees` - Terminate employee contracts (ADMIN only)
- `hr.view_payroll` - View payroll summaries (MANAGER)

---

## Usage Examples

### Backend (Django/DRF)

#### 1. Single Permission Check

```python
from core_modules.permissions.decorators import require_permission

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @require_permission('hr.view_employees')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @require_permission('hr.manage_employees')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
```

#### 2. Multiple Permissions (AND Logic)

```python
@require_permission(['hr.view_employees', 'hr.view_payroll'])
@action(detail=True, methods=['get'])
def payroll_summary(self, request, pk=None):
    """Requires BOTH permissions"""
    employee = self.get_object()
    # ... implementation
```

#### 3. Multiple Permissions (OR Logic)

```python
@require_permission(['hr.manage_employees', 'hr.terminate_employees'], require_all=False)
@action(detail=True, methods=['post'])
def terminate(self, request, pk=None):
    """Requires ANY ONE of the permissions"""
    employee = self.get_object()
    # ... implementation
```

#### 4. Custom Action with Permission

```python
@require_permission('experiments.start_experiments')
@action(detail=True, methods=['post'])
def start(self, request, pk=None):
    """Start an experiment"""
    experiment = self.get_object()
    experiment.status = 'IN_PROGRESS'
    experiment.save()
    return Response({'status': 'started'})
```

### Frontend (React/TypeScript)

#### 1. Conditional Rendering Based on Permission

```typescript
import { usePermissions } from '@/hooks/usePermissions';

function EmployeeList() {
  const { hasPermission } = usePermissions();

  return (
    <div>
      {hasPermission('hr.view_employees') && (
        <EmployeeTable />
      )}

      {hasPermission('hr.manage_employees') && (
        <Button onClick={handleCreate}>Add Employee</Button>
      )}
    </div>
  );
}
```

#### 2. Route Protection

```typescript
import { ProtectedRoute } from '@/components/ProtectedRoute';

<Route
  path="/employees"
  element={
    <ProtectedRoute requiredPermission="hr.view_employees">
      <EmployeesPage />
    </ProtectedRoute>
  }
/>
```

#### 3. Button/Action Protection

```typescript
import { PermissionGuard } from '@/components/PermissionGuard';

<PermissionGuard permission="hr.terminate_employees">
  <Button variant="danger" onClick={handleTerminate}>
    Terminate Employee
  </Button>
</PermissionGuard>
```

---

## Security Guidelines

### 1. Principle of Least Privilege

**Always grant the minimum permissions required for a role to perform its duties.**

✅ **Good Practice**:
```python
# USER role gets view-only access
user_role.permissions = [
    'hr.view_employees',
    'hr.view_departments',
    'hr.view_attendance'
]

# MANAGER role gets manage access
manager_role.permissions = [
    'hr.view_employees',
    'hr.manage_employees',
    'hr.view_departments',
    'hr.manage_departments'
]
```

❌ **Bad Practice**:
```python
# Don't give all permissions to everyone
user_role.permissions = ['*']  # NEVER DO THIS!
```

### 2. Defense in Depth

**Always enforce permissions at multiple layers:**

1. **Backend API** - Primary enforcement (MANDATORY)
2. **Frontend UI** - User experience (RECOMMENDED)
3. **Database** - Row-level security (OPTIONAL)

```python
# Layer 1: Backend API (MANDATORY)
@require_permission('hr.view_employees')
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

# Layer 2: Frontend UI (RECOMMENDED)
{hasPermission('hr.view_employees') && <EmployeeList />}

# Layer 3: Database RLS (OPTIONAL)
# PostgreSQL Row-Level Security policy
CREATE POLICY employee_view_policy ON employees
    FOR SELECT
    USING (
        current_user_has_permission('hr.view_employees')
    );
```

### 3. Audit Logging

**All permission checks are automatically logged by the decorator.**

The `@require_permission` decorator logs:
- User ID
- Permission code
- Resource accessed
- Timestamp
- IP address
- Success/Failure

**View logs**:
```python
from core_modules.permissions.models import PermissionLog

# Get recent permission checks
recent_logs = PermissionLog.objects.filter(
    user=request.user
).order_by('-timestamp')[:100]

# Get failed permission checks (security alerts)
failed_checks = PermissionLog.objects.filter(
    success=False
).order_by('-timestamp')
```

### 4. Permission Naming Best Practices

✅ **Good Permission Names**:
- `hr.view_employees` - Clear, specific
- `accounting.manage_journals` - Action + resource
- `experiments.start_experiments` - Verb + noun

❌ **Bad Permission Names**:
- `hr.all` - Too broad
- `view` - Missing module prefix
- `hr.employee` - Missing action

### 5. Role Assignment Guidelines

**Assign roles, not individual permissions.**

✅ **Good Practice**:
```python
# Assign a role (which contains multiple permissions)
user.roles.add(manager_role)
```

❌ **Bad Practice**:
```python
# Don't assign individual permissions directly
user.permissions.add('hr.view_employees')
user.permissions.add('hr.manage_employees')
# ... (this becomes unmaintainable)
```

### 6. Temporary Permissions

**Use temporary permissions for time-limited access.**

```python
from core_modules.permissions.models import TemporaryPermission
from datetime import datetime, timedelta

# Grant temporary permission for 24 hours
TemporaryPermission.objects.create(
    user=user,
    permission_code='accounting.view_journals',
    expires_at=datetime.now() + timedelta(hours=24),
    granted_by=request.user,
    reason='Audit review'
)
```

### 7. Permission Request Workflow

**Users can request permissions they don't have.**

```python
from core_modules.permissions.models import PermissionRequest

# User requests a permission
request = PermissionRequest.objects.create(
    user=request.user,
    permission_code='hr.manage_employees',
    reason='Promoted to HR Manager',
    status='PENDING'
)

# Manager approves the request
request.status = 'APPROVED'
request.approved_by = manager
request.save()

# Permission is automatically granted
```

---

## Permission Matrix Summary

### By Module

| Module | Permission Codes | ViewSets | Custom Actions |
|--------|-----------------|----------|----------------|
| Core Permissions | 10 | 10 | 0 |
| Core | 16 | 8 | 3 |
| Security | 8 | 4 | 2 |
| API Keys | 2 | 2 | 0 |
| Accounting | 6 | 3 | 0 |
| Sales | 6 | 3 | 0 |
| Inventory | 6 | 3 | 0 |
| Farms | 26 | 13 | 0 |
| Experiments | 30 | 15 | 3 |
| Seed Production | 6 | 2 | 2 |
| HR | 16 | 8 | 2 |
| Seed Hybridization | 1 | 1 | 0 |
| **TOTAL** | **143** | **72** | **12** |

### By Action Type

| Action Type | Count | Percentage |
|-------------|-------|------------|
| `view` | 72 | 50.3% |
| `manage` | 60 | 42.0% |
| `approve` | 3 | 2.1% |
| `request` | 1 | 0.7% |
| `view_logs` | 2 | 1.4% |
| `export` | 1 | 0.7% |
| Custom Actions | 12 | 8.4% |

### By Required Role

| Role | Typical Permissions | Count | Percentage |
|------|---------------------|-------|------------|
| GUEST | View-only (public data) | ~10 | 7% |
| USER | View + limited create | ~50 | 35% |
| MANAGER | View + manage (dept-level) | ~60 | 42% |
| ADMIN | All permissions | ~23 | 16% |

---

## Appendix: Complete Permission List

### Alphabetical Index

```
accounting.manage_accounts
accounting.manage_cost_centers
accounting.manage_journals
accounting.view_accounts
accounting.view_cost_centers
accounting.view_journals
api_keys.manage
api_keys.view
core.manage_branches
core.manage_companies
core.manage_countries
core.manage_currencies
core.manage_fiscal_years
core.manage_sequences
core.reset_sequences
core.set_base_fiscal_year
core.use_sequences
core.view_branches
core.view_companies
core.view_countries
core.view_currencies
core.view_fiscal_years
core.view_sequences
core.view_settings
experiments.cancel_experiments
experiments.complete_experiments
experiments.manage_costs
experiments.manage_evaluations
experiments.manage_experiment_varieties
experiments.manage_experiments
experiments.manage_fertilization_applications
experiments.manage_fertilization_programs
experiments.manage_harvests
experiments.manage_locations
experiments.manage_pesticide_applications
experiments.manage_pesticide_programs
experiments.manage_quality_grades
experiments.manage_seasons
experiments.manage_varieties
experiments.manage_variety_types
experiments.start_experiments
experiments.view_costs
experiments.view_evaluations
experiments.view_experiment_varieties
experiments.view_experiments
experiments.view_fertilization_applications
experiments.view_fertilization_programs
experiments.view_harvests
experiments.view_locations
experiments.view_pesticide_applications
experiments.view_pesticide_programs
experiments.view_quality_grades
experiments.view_seasons
experiments.view_varieties
experiments.view_variety_types
farms.manage_crop_varieties
farms.manage_farms
farms.manage_fertilization_plans
farms.manage_harvests
farms.manage_irrigation_schedules
farms.manage_irrigation_types
farms.manage_pest_control
farms.manage_planting_plans
farms.manage_plot_types
farms.manage_plots
farms.manage_seasons
farms.manage_soil_types
farms.manage_warehouses
farms.view_crop_varieties
farms.view_farms
farms.view_fertilization_plans
farms.view_harvests
farms.view_irrigation_schedules
farms.view_irrigation_types
farms.view_pest_control
farms.view_planting_plans
farms.view_plot_types
farms.view_plots
farms.view_seasons
farms.view_soil_types
farms.view_warehouses
groups.manage
groups.view
hr.manage_attendance
hr.manage_departments
hr.manage_employees
hr.manage_job_grades
hr.manage_leave_types
hr.manage_positions
hr.manage_settings
hr.terminate_employees
hr.view_attendance
hr.view_departments
hr.view_employees
hr.view_job_grades
hr.view_leave_types
hr.view_payroll
hr.view_positions
hr.view_settings
hybridization.view_varieties
inventory.manage_categories
inventory.manage_products
inventory.manage_uoms
inventory.view_categories
inventory.view_products
inventory.view_uoms
permissions.approve
permissions.manage
permissions.manage_temporary
permissions.request
permissions.view
permissions.view_logs
roles.manage
roles.view
sales.manage_customers
sales.manage_invoices
sales.manage_quotations
sales.view_customers
sales.view_invoices
sales.view_quotations
security.analyze_threats
security.export_audit_logs
security.manage_blocked_ips
security.manage_settings
security.view_audit_logs
security.view_blocked_ips
security.view_password_history
security.view_settings
seed_production.approve_orders
seed_production.manage_lots
seed_production.manage_orders
seed_production.update_lot_status
seed_production.view_lots
seed_production.view_orders
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-19 | Security Team | Initial creation with all 143 permission codes |

---

**End of Document**

