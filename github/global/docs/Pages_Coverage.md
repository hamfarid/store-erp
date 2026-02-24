# FILE: docs/Pages_Coverage.md | PURPOSE: Page-to-route-to-button mapping | OWNER: Frontend Team | RELATED: docs/Routes_FE.md, docs/Routes_BE.md | LAST-AUDITED: 2025-10-21

# Pages Coverage — نظام إدارة المخزون العربي

**Version**: 1.0  
**Last Updated**: 2025-10-21  
**Status**: ⚠️ **Partial Coverage** (Many pages incomplete)

---

## 1. Overview

This document maps frontend pages to:
- Routes (URL paths)
- Backend API endpoints
- Interactive buttons/actions
- Required permissions
- Implementation status

**Purpose**: Ensure every page is fully wired (routes → API → buttons → permissions)

---

## 2. Coverage Matrix

| Page | Route | Component | API Endpoints | Buttons | Permissions | Status |
|------|-------|-----------|---------------|---------|-------------|--------|
| **Login** | `/login` | `Login.jsx` | `POST /api/auth/login` | Login, Forgot Password | Public | ✅ Complete |
| **Dashboard** | `/dashboard` | `Dashboard.jsx` | `GET /api/dashboard/stats` | Quick Actions (4) | Any user | ⚠️ Partial |
| **Product List** | `/products` | `ProductList.jsx` | `GET /api/products`, `DELETE /api/products/:id` | New, Edit, Delete, Export | VIEW_LIGHT, MODIFY | ⚠️ Partial |
| **Product Form** | `/products/new`, `/products/:id/edit` | `ProductForm.jsx` | `POST /api/products`, `PUT /api/products/:id` | Save, Cancel | MODIFY | ⚠️ Partial |
| **Product Detail** | `/products/:id` | `ProductDetail.jsx` | `GET /api/products/:id` | Edit, Delete, View Stock | READ | ❌ Missing |
| **Invoice List** | `/invoices` | `InvoiceList.jsx` | `GET /api/invoices` | New Sales, New Purchase, Filter | VIEW_LIGHT | ⚠️ Partial |
| **Invoice Form** | `/invoices/sales/new`, `/invoices/purchase/new` | `InvoiceForm.jsx` | `POST /api/invoices` | Add Item, Save, Print | MODIFY | ⚠️ Partial |
| **Invoice Detail** | `/invoices/:id` | `InvoiceDetail.jsx` | `GET /api/invoices/:id` | Edit, Delete, Print, Pay | READ, MODIFY | ❌ Missing |
| **Customer List** | `/customers` | `CustomerList.jsx` | `GET /api/customers` | New, Edit, Delete | VIEW_LIGHT, MODIFY | ❌ Missing |
| **Customer Form** | `/customers/new`, `/customers/:id/edit` | `CustomerForm.jsx` | `POST /api/customers`, `PUT /api/customers/:id` | Save, Cancel | MODIFY | ❌ Missing |
| **Supplier List** | `/suppliers` | `SupplierList.jsx` | `GET /api/suppliers` | New, Edit, Delete | VIEW_LIGHT, MODIFY | ❌ Missing |
| **Inventory List** | `/inventory` | `InventoryList.jsx` | `GET /api/inventory` | Adjust Stock, View Movements | VIEW_LIGHT | ❌ Missing |
| **Stock Movements** | `/inventory/movements` | `StockMovements.jsx` | `GET /api/stock-movements` | Filter, Export | READ | ❌ Missing |
| **User List** | `/users` | `UserList.jsx` | `GET /api/users` | New, Edit, Deactivate, Reset Password | ADMIN | ⚠️ Partial |
| **User Form** | `/users/new`, `/users/:id/edit` | `UserForm.jsx` | `POST /api/users`, `PUT /api/users/:id` | Save, Cancel | ADMIN | ❌ Missing |
| **Reports Dashboard** | `/reports` | `ReportsDashboard.jsx` | None (hub page) | Links to reports | READ (financial_reports) | ❌ Missing |
| **Sales Report** | `/reports/sales` | `SalesReport.jsx` | `GET /api/reports/sales` | Generate, Export, Print | READ | ❌ Missing |
| **Settings** | `/settings` | `Settings.jsx` | `GET /api/settings`, `PUT /api/settings` | Save | ADMIN | ❌ Missing |

**Legend**:
- ✅ **Complete**: Page fully implemented with all buttons wired
- ⚠️ **Partial**: Page exists but missing buttons or API calls
- ❌ **Missing**: Page not implemented or placeholder only

---

## 3. Detailed Page Analysis

### 3.1 Login Page ✅

**Route**: `/login`  
**Component**: `frontend/src/pages/Login.jsx`  
**Status**: ✅ Complete

**API Endpoints**:
- `POST /api/auth/login` — User authentication

**Buttons**:
1. **Login** — Submits credentials
   - Action: `POST /api/auth/login`
   - Success: Redirect to `/dashboard`
   - Error: Display error message
2. **Forgot Password** — Link to password reset
   - Action: Navigate to `/forgot-password`
   - Status: ⚠️ Target page not implemented

**Permissions**: Public (no auth required)

**Issues**: None

---

### 3.2 Dashboard ⚠️

**Route**: `/dashboard`  
**Component**: `frontend/src/pages/Dashboard.jsx`  
**Status**: ⚠️ Partial (missing some quick actions)

**API Endpoints**:
- `GET /api/dashboard/stats` — KPIs (sales, purchases, stock value)
- `GET /api/dashboard/recent-activity` — Recent invoices/movements

**Buttons**:
1. **New Sales Invoice** — Quick action
   - Action: Navigate to `/invoices/sales/new`
   - Status: ✅ Wired
2. **New Purchase Invoice** — Quick action
   - Action: Navigate to `/invoices/purchase/new`
   - Status: ✅ Wired
3. **Adjust Stock** — Quick action
   - Action: Navigate to `/inventory/adjust`
   - Status: ❌ Not wired
4. **View Reports** — Quick action
   - Action: Navigate to `/reports`
   - Status: ❌ Not wired

**Permissions**: Any authenticated user

**Issues**:
- Quick actions 3 & 4 not wired to routes
- Missing real-time data refresh

---

### 3.3 Product List ⚠️

**Route**: `/products`  
**Component**: `frontend/src/pages/Products/ProductList.jsx`  
**Status**: ⚠️ Partial (delete button not wired)

**API Endpoints**:
- `GET /api/products` — Fetch product list
- `DELETE /api/products/:id` — Delete product

**Buttons**:
1. **New Product** — Create new
   - Action: Navigate to `/products/new`
   - Status: ✅ Wired
2. **Edit** (per row) — Edit product
   - Action: Navigate to `/products/:id/edit`
   - Status: ✅ Wired
3. **Delete** (per row) — Delete product
   - Action: `DELETE /api/products/:id`
   - Status: ❌ Not wired (button exists but no handler)
4. **Export to Excel** — Export list
   - Action: Download Excel file
   - Status: ❌ Not implemented

**Permissions**:
- List view: `VIEW_LIGHT` on `products`
- Edit/Delete: `MODIFY` on `products`

**Issues**:
- Delete button has no onClick handler
- Export button missing
- No permission checks on Edit/Delete buttons

---

### 3.4 Product Form ⚠️

**Route**: `/products/new`, `/products/:id/edit`  
**Component**: `frontend/src/pages/Products/ProductForm.jsx`  
**Status**: ⚠️ Partial (validation incomplete)

**API Endpoints**:
- `POST /api/products` — Create product
- `PUT /api/products/:id` — Update product
- `GET /api/products/:id` — Fetch for edit

**Buttons**:
1. **Save** — Submit form
   - Action: `POST` or `PUT /api/products`
   - Status: ✅ Wired
2. **Cancel** — Discard changes
   - Action: Navigate back to `/products`
   - Status: ✅ Wired

**Permissions**: `MODIFY` on `products`

**Issues**:
- Client-side validation incomplete (missing required field checks)
- No image upload functionality
- Category dropdown not populated

---

### 3.5 Invoice List ⚠️

**Route**: `/invoices`  
**Component**: `frontend/src/pages/Invoices/InvoiceList.jsx`  
**Status**: ⚠️ Partial (filters not working)

**API Endpoints**:
- `GET /api/invoices` — Fetch invoice list

**Buttons**:
1. **New Sales Invoice**
   - Action: Navigate to `/invoices/sales/new`
   - Status: ✅ Wired
2. **New Purchase Invoice**
   - Action: Navigate to `/invoices/purchase/new`
   - Status: ✅ Wired
3. **Filter** (dropdown) — Filter by type/status
   - Action: Update query params and refetch
   - Status: ❌ Not wired (UI exists but no handler)

**Permissions**: `VIEW_LIGHT` on `invoices`

**Issues**:
- Filter dropdowns not functional
- No date range picker
- Missing pagination

---

### 3.6 Invoice Form ⚠️

**Route**: `/invoices/sales/new`, `/invoices/purchase/new`, `/invoices/:id/edit`  
**Component**: `frontend/src/pages/Invoices/InvoiceForm.jsx`  
**Status**: ⚠️ Partial (calculations incorrect)

**API Endpoints**:
- `POST /api/invoices` — Create invoice
- `PUT /api/invoices/:id` — Update invoice
- `GET /api/products` — Product search for line items

**Buttons**:
1. **Add Item** — Add line item
   - Action: Add row to items array
   - Status: ✅ Wired
2. **Remove Item** (per row)
   - Action: Remove row from items array
   - Status: ✅ Wired
3. **Save as Draft**
   - Action: `POST /api/invoices` with `status=DRAFT`
   - Status: ✅ Wired
4. **Confirm Invoice**
   - Action: `POST /api/invoices` with `status=CONFIRMED`
   - Status: ✅ Wired
5. **Print**
   - Action: Open print dialog
   - Status: ❌ Not implemented

**Permissions**: `MODIFY` on `invoices`

**Issues**:
- Tax calculation incorrect (not applying tax_rate from product)
- Discount not being subtracted from subtotal
- Total amount formula: `total = subtotal + tax - discount` (currently wrong)

---

### 3.7 User List ⚠️

**Route**: `/users`  
**Component**: `frontend/src/pages/Admin/UserList.jsx`  
**Status**: ⚠️ Partial (reset password not wired)

**API Endpoints**:
- `GET /api/users` — Fetch user list
- `PUT /api/users/:id` — Update user (activate/deactivate)

**Buttons**:
1. **New User**
   - Action: Navigate to `/users/new`
   - Status: ✅ Wired
2. **Edit** (per row)
   - Action: Navigate to `/users/:id/edit`
   - Status: ✅ Wired
3. **Deactivate** (per row)
   - Action: `PUT /api/users/:id` with `is_active=false`
   - Status: ✅ Wired
4. **Reset Password** (per row)
   - Action: `POST /api/users/:id/reset-password`
   - Status: ❌ Not wired

**Permissions**: `ADMIN` on `users`

**Issues**:
- Reset Password button has no handler
- No confirmation dialog for deactivate action

---

## 4. Missing Pages (Not Implemented)

| Page | Priority | Estimated Effort |
|------|----------|------------------|
| Product Detail (`/products/:id`) | P1 | 4 hours |
| Invoice Detail (`/invoices/:id`) | P1 | 6 hours |
| Customer List & Form | P1 | 8 hours |
| Supplier List & Form | P2 | 8 hours |
| Inventory List | P1 | 6 hours |
| Stock Movements | P2 | 4 hours |
| User Form (`/users/new`, `/users/:id/edit`) | P1 | 4 hours |
| Reports Dashboard | P2 | 3 hours |
| Sales Report | P2 | 6 hours |
| Settings | P2 | 5 hours |
| Warehouse Management | P3 | 8 hours |
| Category Management | P3 | 4 hours |

**Total Estimated Effort**: ~66 hours

---

## 5. Button Wiring Checklist

For each button, verify:
- [ ] `onClick` handler defined
- [ ] API call implemented (if applicable)
- [ ] Loading state shown during API call
- [ ] Success/error handling
- [ ] Permission check (hide/disable if no permission)
- [ ] Confirmation dialog (for destructive actions)
- [ ] Optimistic UI update (if applicable)

**Example (Delete Button)**:
```jsx
const handleDelete = async (id) => {
  if (!hasPermission('products', 'MODIFY')) return;
  
  if (!confirm('Are you sure you want to delete this product?')) return;
  
  setLoading(true);
  try {
    await api.delete(`/api/products/${id}`);
    // Optimistic update: remove from local state
    setProducts(products.filter(p => p.id !== id));
    toast.success('Product deleted successfully');
  } catch (error) {
    toast.error('Failed to delete product');
  } finally {
    setLoading(false);
  }
};

// In JSX
{hasPermission('products', 'MODIFY') && (
  <button onClick={() => handleDelete(product.id)} disabled={loading}>
    Delete
  </button>
)}
```

---

## 6. API Endpoint Coverage

| Endpoint | Used By Pages | Status |
|----------|---------------|--------|
| `POST /api/auth/login` | Login | ✅ |
| `GET /api/dashboard/stats` | Dashboard | ✅ |
| `GET /api/products` | ProductList, InvoiceForm | ✅ |
| `POST /api/products` | ProductForm | ✅ |
| `PUT /api/products/:id` | ProductForm | ✅ |
| `DELETE /api/products/:id` | ProductList | ❌ Not called |
| `GET /api/invoices` | InvoiceList | ✅ |
| `POST /api/invoices` | InvoiceForm | ✅ |
| `GET /api/users` | UserList | ✅ |
| `POST /api/users/:id/reset-password` | UserList | ❌ Not called |

---

## 7. Remediation Plan

### Phase 1 (P0 - Critical) — 2 weeks
1. Fix invoice form calculations (tax, discount, total)
2. Wire delete buttons on ProductList
3. Implement permission checks on all Edit/Delete buttons
4. Add confirmation dialogs for destructive actions

### Phase 2 (P1 - High) — 3 weeks
1. Implement Product Detail page
2. Implement Invoice Detail page
3. Implement Customer List & Form
4. Implement User Form
5. Implement Inventory List
6. Wire all missing quick actions on Dashboard

### Phase 3 (P2 - Medium) — 4 weeks
1. Implement Supplier List & Form
2. Implement Stock Movements page
3. Implement Reports Dashboard
4. Implement Sales Report
5. Implement Settings page
6. Add export functionality to all list pages

### Phase 4 (P3 - Low) — 2 weeks
1. Implement Warehouse Management
2. Implement Category Management
3. Add advanced filters to all list pages
4. Implement bulk actions

---

## 8. Testing Checklist

For each page:
- [ ] All buttons have handlers
- [ ] API calls succeed with valid data
- [ ] API calls fail gracefully with invalid data
- [ ] Loading states displayed
- [ ] Error messages shown
- [ ] Success messages shown
- [ ] Permission checks enforced
- [ ] Responsive layout (mobile/tablet/desktop)
- [ ] RTL layout correct (Arabic)
- [ ] Keyboard navigation works
- [ ] Screen reader accessible

---

## 9. Maintenance

**On New Page**:
1. Add entry to this document
2. List all buttons and their actions
3. Map to API endpoints
4. Document required permissions
5. Update coverage matrix

**Quarterly Review**:
- Audit incomplete pages
- Verify button wiring
- Update status column

---

## References

- Frontend Routes: `/docs/Routes_FE.md`
- Backend Routes: `/docs/Routes_BE.md`
- API Contracts: `/docs/API_Contracts.md`
- Permissions Model: `/docs/Permissions_Model.md`

