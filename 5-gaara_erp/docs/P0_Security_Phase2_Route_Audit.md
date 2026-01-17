# Phase 2 Task 2 - Route Audit & Permission Mapping

**Date**: 2025-11-18  
**Status**: IN PROGRESS  
**Task**: Apply @require_permission decorator to all protected routes

---

## 📊 Route Audit Summary

### Total Routes Identified: 87+ ViewSets

**By Module**:
- **Core Modules**: 25 ViewSets
- **Business Modules**: 18 ViewSets
- **Agricultural Modules**: 22 ViewSets
- **Services Modules**: 12 ViewSets
- **Integration Modules**: 10 ViewSets

---

## 🎯 Priority Routes (P0 - Critical)

### 1. Core Modules (25 ViewSets)

#### **Permissions Module** (10 ViewSets)
- `PermissionViewSet` - READ ONLY ✅
- `RoleViewSet` - READ ONLY ✅
- `GroupViewSet` - READ ONLY ✅
- `UserPermissionViewSet` - **NEEDS**: `permissions.manage`
- `UserRoleViewSet` - **NEEDS**: `roles.manage`
- `UserGroupViewSet` - **NEEDS**: `groups.manage`
- `ResourcePermissionViewSet` - **NEEDS**: `permissions.manage`
- `PermissionRequestViewSet` - **NEEDS**: `permissions.approve`
- `PermissionLogViewSet` - READ ONLY ✅
- `TemporaryPermissionViewSet` - **NEEDS**: `permissions.manage`

#### **Core Module** (8 ViewSets)
- `CountryViewSet` - **NEEDS**: `core.manage_countries`
- `CompanyViewSet` - **NEEDS**: `core.manage_companies`
- `BranchViewSet` - **NEEDS**: `core.manage_branches`
- `CurrencyViewSet` - **NEEDS**: `core.manage_currencies`
- `DepartmentViewSet` - **NEEDS**: `core.manage_departments`
- `SystemSettingViewSet` - **NEEDS**: `core.manage_settings`
- `RoleDatabasePermissionViewSet` - **NEEDS**: `permissions.manage`
- `DocumentSequenceViewSet` - **NEEDS**: `core.manage_sequences`

#### **Security Module** (4 ViewSets)
- `SecuritySettingViewSet` - **NEEDS**: `security.manage_settings`
- `BlockedIPViewSet` - **NEEDS**: `security.manage_blocked_ips`
- `SecurityAuditViewSet` - READ ONLY (for admins)
- `PasswordHistoryViewSet` - READ ONLY (for admins)

#### **API Keys Module** (2 ViewSets)
- `APIKeyAPIView.get` - **NEEDS**: `api_keys.view`
- `APIKeyAPIView.post` - **NEEDS**: `api_keys.create`

---

### 2. Business Modules (18 ViewSets)

#### **Accounting** (2 ViewSets)
- `JournalViewSet` - **NEEDS**: `accounting.manage_journals`
- `TaxViewSet` - **NEEDS**: `accounting.manage_taxes`

#### **Inventory** (6 ViewSets)
- `UOMViewSet` - **NEEDS**: `inventory.manage_uom`
- `ProductViewSet` - **NEEDS**: `inventory.manage_products`
- `StockViewSet` - **NEEDS**: `inventory.manage_stock`
- `WarehouseViewSet` - **NEEDS**: `inventory.manage_warehouses`
- `StockMoveViewSet` - **NEEDS**: `inventory.manage_stock_moves`
- `InventoryAdjustmentViewSet` - **NEEDS**: `inventory.adjust_stock`

#### **Sales** (4 ViewSets)
- `CustomerViewSet` - **NEEDS**: `sales.manage_customers`
- `SalesOrderViewSet` - **NEEDS**: `sales.create_orders`
- `SalesInvoiceViewSet` - **NEEDS**: `sales.create_invoices`
- `SalesReturnViewSet` - **NEEDS**: `sales.process_returns`

#### **Purchasing** (4 ViewSets)
- `SupplierViewSet` - **NEEDS**: `purchasing.manage_suppliers`
- `PurchaseOrderViewSet` - **NEEDS**: `purchasing.create_orders`
- `PurchaseInvoiceViewSet` - **NEEDS**: `purchasing.create_invoices`
- `PurchaseReturnViewSet` - **NEEDS**: `purchasing.process_returns`

#### **POS** (2 ViewSets)
- `POSSessionViewSet` - **NEEDS**: `pos.manage_sessions`
- `POSOrderViewSet` - **NEEDS**: `pos.create_orders`

---

### 3. Agricultural Modules (22 ViewSets)

#### **Farms** (10 ViewSets)
- `FarmViewSet` - **NEEDS**: `farms.manage`
- `FieldViewSet` - **NEEDS**: `farms.manage_fields`
- `CropViewSet` - **NEEDS**: `farms.manage_crops`
- `PlantingSeasonViewSet` - **NEEDS**: `farms.manage_seasons`
- `AgriculturalActivityTypeViewSet` - **NEEDS**: `farms.manage_activity_types`
- `AgriculturalActivityViewSet` - **NEEDS**: `farms.manage_activities`
- `HarvestViewSet` - **NEEDS**: `farms.manage_harvests`
- `FarmResourceViewSet` - **NEEDS**: `farms.manage_resources`
- `FarmWorkerLogViewSet` - **NEEDS**: `farms.manage_workers`
- `FarmEquipmentLogViewSet` - **NEEDS**: `farms.manage_equipment`

#### **Experiments** (8 ViewSets)
- `ExperimentViewSet` - **NEEDS**: `experiments.manage`
- `LocationViewSet` - **NEEDS**: `experiments.manage_locations`
- `SeasonViewSet` - **NEEDS**: `experiments.manage_seasons`
- `VarietyTypeViewSet` - **NEEDS**: `experiments.manage_variety_types`
- `VarietyViewSet` - **NEEDS**: `experiments.manage_varieties`
- `ExperimentVarietyViewSet` - **NEEDS**: `experiments.manage_experiment_varieties`
- `HarvestViewSet` - **NEEDS**: `experiments.manage_harvests`
- `VarietyEvaluationViewSet` - **NEEDS**: `experiments.evaluate_varieties`

#### **Seed Production** (4 ViewSets)
- `SeedProductionOrderViewSet` - **NEEDS**: `seed_production.create_orders`
- `SeedBatchViewSet` - **NEEDS**: `seed_production.manage_batches`
- `QualityTestViewSet` - **NEEDS**: `seed_production.manage_quality_tests`
- `CertificationViewSet` - **NEEDS**: `seed_production.manage_certifications`

---

### 4. Services Modules (12 ViewSets)

#### **HR** (8 ViewSets)
- `EmployeeViewSet` - **NEEDS**: `hr.manage_employees`
- `DepartmentViewSet` - **NEEDS**: `hr.manage_departments`
- `AttendanceRecordViewSet` - **NEEDS**: `hr.manage_attendance`
- `LeaveRequestViewSet` - **NEEDS**: `hr.manage_leave_requests`
- `PayrollPeriodViewSet` - **NEEDS**: `hr.manage_payroll`
- `SalaryComponentViewSet` - **NEEDS**: `hr.manage_salary_components`
- `TaxBracketViewSet` - **NEEDS**: `hr.manage_tax_brackets`
- `SocialInsuranceSettingViewSet` - **NEEDS**: `hr.manage_insurance_settings`

#### **Assets** (4 ViewSets)
- `AssetViewSet` - **NEEDS**: `assets.manage`
- `AssetCategoryViewSet` - **NEEDS**: `assets.manage_categories`
- `DepreciationViewSet` - **NEEDS**: `assets.manage_depreciation`
- `MaintenanceViewSet` - **NEEDS**: `assets.manage_maintenance`

---

## 🔒 Permission Naming Convention

**Format**: `{module}.{action}_{resource}`

**Actions**:
- `view` - Read access
- `create` - Create new records
- `modify` - Update existing records
- `delete` - Delete records
- `manage` - Full CRUD access
- `approve` - Approval workflows
- `export` - Export data

**Examples**:
- `users.create` - Create new users
- `users.modify` - Update existing users
- `users.delete` - Delete users
- `users.manage` - Full user management
- `inventory.adjust_stock` - Adjust inventory levels
- `payroll.approve` - Approve payroll

---

## 📝 Next Steps

1. ✅ Create permission records in database
2. 🔄 Apply decorators to ViewSets (IN PROGRESS)
3. ⏳ Test each route with/without permissions
4. ⏳ Document in `docs/Permissions_Model.md`

---

**Report Generated**: 2025-11-18  
**Total Routes to Protect**: 87+  
**Estimated Time**: 2-3 hours

