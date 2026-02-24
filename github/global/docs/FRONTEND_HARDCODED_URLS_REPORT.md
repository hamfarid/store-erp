# Frontend Hardcoded URLs Report

**Date:** 2025-11-25  
**Status:** 🔴 Critical Issue Found  
**Priority:** 🔴 High

---

## 🚨 Problem Summary

**Issue:** Multiple components still use hardcoded API URLs instead of environment variables.

**Impact:**
- ❌ Code is not portable across environments
- ❌ Difficult to change API endpoint
- ❌ Inconsistent with project standards
- ❌ Security risk (exposes internal IPs)

---

## 📊 Hardcoded URLs Found

### **Type 1: Old IP Address (172.16.16.27:5005)**

| File | Line | Hardcoded URL | Count |
|------|------|---------------|-------|
| `AccountingSystem.jsx` | Multiple | `http://172.16.16.27:5005/accounting/*` | 4 |
| `LotManagement.jsx` | Multiple | `http://172.16.16.27:5005/lot_management/*` | 1 |
| `PaymentVouchers.jsx` | 36 | `http://172.16.16.27:5005/accounting/payment-vouchers` | 1 |
| `StockMovements.jsx` | Multiple | `http://172.16.16.27:5005/api/stock-movements` | 1 |
| `WarehousesManagement.jsx` | Multiple | `http://172.16.16.27:5005/api/warehouses` | 1 |

**Total:** 8 occurrences

### **Type 2: Localhost URLs (localhost:5005)**

| File | Line | Hardcoded URL | Count |
|------|------|---------------|-------|
| `CashBoxManagement.jsx` | Multiple | `http://localhost:5005/api/accounting/*` | 3 |
| `CurrencyManagement.jsx` | Multiple | `http://localhost:5005/api/accounting/currencies` | 2 |
| `ProfitLossReport.jsx` | Multiple | `http://localhost:5005/api/accounting/profit-loss` | 1 |
| `PurchaseInvoiceManagement.jsx` | Multiple | `http://localhost:5005/api/*` | 4 |

**Total:** 10 occurrences

---

## ✅ Correct Approach

All components should use the environment variable:

```javascript
// ❌ WRONG - Hardcoded URL
const response = await fetch('http://localhost:5005/api/products')

// ✅ CORRECT - Environment Variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const response = await fetch(`${API_BASE_URL}/products`)
```

**Note:** `VITE_API_BASE_URL` already includes `/api`, so endpoints should NOT include it.

---

## 🔧 Files to Fix

### **Priority 1: Critical (Old IP Address)**
1. ✅ `AccountingSystem.jsx` - 4 URLs
2. ✅ `LotManagement.jsx` - 1 URL
3. ✅ `PaymentVouchers.jsx` - 1 URL
4. ✅ `StockMovements.jsx` - 1 URL
5. ✅ `WarehousesManagement.jsx` - 1 URL

### **Priority 2: High (Localhost URLs)**
6. ✅ `CashBoxManagement.jsx` - 3 URLs
7. ✅ `CurrencyManagement.jsx` - 2 URLs
8. ✅ `ProfitLossReport.jsx` - 1 URL
9. ✅ `PurchaseInvoiceManagement.jsx` - 4 URLs

---

## 📋 Action Plan

### **Step 1: Create Helper Function**
Create a centralized API helper in `frontend/src/utils/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5005/api'

export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  
  return response.json()
}
```

### **Step 2: Update All Components**
Replace all hardcoded URLs with the helper function:

```javascript
// Before
const response = await fetch('http://localhost:5005/api/products')

// After
import { apiRequest } from '../utils/api'
const data = await apiRequest('/products')
```

### **Step 3: Verify Environment Variables**
Ensure `.env` file has:
```
VITE_API_BASE_URL=http://localhost:5005/api
```

---

## 🎯 Expected Outcome

After fixes:
- ✅ 0 hardcoded URLs in components
- ✅ All API calls use environment variables
- ✅ Centralized API configuration
- ✅ Easy to change API endpoint
- ✅ Consistent error handling

---

## 📊 Progress Tracker

| Task | Status | Files |
|------|--------|-------|
| Identify hardcoded URLs | ✅ Complete | 9 files |
| Create API helper | ⏳ Pending | 1 file |
| Fix Priority 1 files | ⏳ Pending | 5 files |
| Fix Priority 2 files | ⏳ Pending | 4 files |
| Test all components | ⏳ Pending | 9 files |
| Commit changes | ⏳ Pending | - |

---

## 🚀 Next Steps

1. ⏳ Create `frontend/src/utils/api.js` helper
2. ⏳ Fix all 9 components
3. ⏳ Test all API calls
4. ⏳ Commit changes
5. ⏳ Update documentation

---

**Status:** Analysis Complete | Ready to Fix

