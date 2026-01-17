# Frontend Buttons Functionality Test

**Version:** 2.0  
**Last Updated:** 2025-12-13  
**Status:** Ready for Testing

---

## Overview

This document lists all buttons in the Store ERP frontend and their expected functionality. Use this as a checklist to ensure all buttons work correctly.

---

## Testing Methodology

### Manual Testing
1. Navigate to each page
2. Click each button
3. Verify expected behavior
4. Mark as ✅ (working) or ❌ (broken)
5. Document any issues

### Automated Testing
- Use Playwright or Cypress for E2E testing
- See `tests/e2e/` directory

---

## Dashboard

### Statistics Cards
- [ ] **View Details** (4 buttons - one per card)
  - Expected: Navigate to relevant detail page
  - Test: Click each card's button

### Quick Actions
- [ ] **New Sale** button
  - Expected: Navigate to POS page
  - Test: Click and verify navigation
  
- [ ] **New Product** button
  - Expected: Open new product modal/form
  - Test: Click and verify modal opens
  
- [ ] **New Purchase** button
  - Expected: Navigate to new purchase page
  - Test: Click and verify navigation
  
- [ ] **View Reports** button
  - Expected: Navigate to reports page
  - Test: Click and verify navigation

### Charts
- [ ] **Refresh** button
  - Expected: Reload chart data
  - Test: Click and verify data updates

---

## Products Management

### Main Actions
- [ ] **Add Product** button
  - Expected: Open new product form
  - Test: Click and verify form opens
  
- [ ] **Import Products** button
  - Expected: Open import dialog
  - Test: Click and verify dialog opens
  
- [ ] **Export Products** button
  - Expected: Download products CSV/Excel
  - Test: Click and verify download

### Table Actions (per row)
- [ ] **Edit** button
  - Expected: Open edit form with product data
  - Test: Click on multiple products
  
- [ ] **Delete** button
  - Expected: Show confirmation, then delete
  - Test: Click and verify confirmation dialog
  
- [ ] **View Details** button
  - Expected: Show product details modal
  - Test: Click and verify modal

### Filters
- [ ] **Apply Filters** button
  - Expected: Filter products based on criteria
  - Test: Set filters and click
  
- [ ] **Clear Filters** button
  - Expected: Reset all filters
  - Test: Click and verify filters cleared

### Search
- [ ] **Search** button
  - Expected: Search products by keyword
  - Test: Enter keyword and click

---

## POS (Point of Sale)

### Product Selection
- [ ] **Add to Cart** buttons (per product)
  - Expected: Add product to cart
  - Test: Click multiple products
  
- [ ] **Quick Add** buttons (favorites)
  - Expected: Quickly add to cart
  - Test: Click and verify cart updates

### Cart Actions
- [ ] **Increase Quantity** (+) button
  - Expected: Increase item quantity
  - Test: Click and verify quantity increases
  
- [ ] **Decrease Quantity** (-) button
  - Expected: Decrease item quantity
  - Test: Click and verify quantity decreases
  
- [ ] **Remove Item** button
  - Expected: Remove item from cart
  - Test: Click and verify item removed
  
- [ ] **Clear Cart** button
  - Expected: Remove all items
  - Test: Click and verify cart cleared

### Payment
- [ ] **Cash Payment** button
  - Expected: Process cash payment
  - Test: Click and verify payment processed
  
- [ ] **Card Payment** button
  - Expected: Process card payment
  - Test: Click and verify payment processed
  
- [ ] **Split Payment** button
  - Expected: Open split payment dialog
  - Test: Click and verify dialog opens
  
- [ ] **Complete Sale** button
  - Expected: Finalize sale and print receipt
  - Test: Click and verify sale completed

### Other
- [ ] **Hold Sale** button
  - Expected: Save current sale for later
  - Test: Click and verify sale saved
  
- [ ] **Recall Sale** button
  - Expected: Load saved sale
  - Test: Click and verify sale loaded

---

## Purchases Management

### Main Actions
- [ ] **New Purchase** button
  - Expected: Open new purchase form
  - Test: Click and verify form opens
  
- [ ] **Import Purchases** button
  - Expected: Open import dialog
  - Test: Click and verify dialog opens

### Purchase Form
- [ ] **Add Item** button
  - Expected: Add new item to purchase
  - Test: Click and verify item added
  
- [ ] **Remove Item** button (per item)
  - Expected: Remove item from purchase
  - Test: Click and verify item removed
  
- [ ] **Save Draft** button
  - Expected: Save purchase as draft
  - Test: Click and verify draft saved
  
- [ ] **Submit Purchase** button
  - Expected: Submit purchase for approval
  - Test: Click and verify submission
  
- [ ] **Cancel** button
  - Expected: Discard changes and close
  - Test: Click and verify cancellation

---

## Customers Management

### Main Actions
- [ ] **Add Customer** button
  - Expected: Open new customer form
  - Test: Click and verify form opens
  
- [ ] **Import Customers** button
  - Expected: Open import dialog
  - Test: Click and verify dialog opens
  
- [ ] **Export Customers** button
  - Expected: Download customers list
  - Test: Click and verify download

### Table Actions
- [ ] **Edit** button (per customer)
  - Expected: Open edit form
  - Test: Click and verify form opens
  
- [ ] **Delete** button (per customer)
  - Expected: Show confirmation, then delete
  - Test: Click and verify confirmation
  
- [ ] **View History** button (per customer)
  - Expected: Show customer purchase history
  - Test: Click and verify history displayed

---

## Suppliers Management

### Main Actions
- [ ] **Add Supplier** button
  - Expected: Open new supplier form
  - Test: Click and verify form opens
  
- [ ] **Import Suppliers** button
  - Expected: Open import dialog
  - Test: Click and verify dialog opens

### Table Actions
- [ ] **Edit** button (per supplier)
  - Expected: Open edit form
  - Test: Click and verify form opens
  
- [ ] **Delete** button (per supplier)
  - Expected: Show confirmation, then delete
  - Test: Click and verify confirmation
  
- [ ] **View Purchases** button (per supplier)
  - Expected: Show supplier purchase history
  - Test: Click and verify history displayed

---

## Reports

### Report Generation
- [ ] **Generate Report** button (per report type)
  - Expected: Generate selected report
  - Test: Click and verify report generated
  
- [ ] **Export PDF** button
  - Expected: Download report as PDF
  - Test: Click and verify download
  
- [ ] **Export Excel** button
  - Expected: Download report as Excel
  - Test: Click and verify download
  
- [ ] **Print** button
  - Expected: Open print dialog
  - Test: Click and verify print dialog

### Filters
- [ ] **Apply Date Range** button
  - Expected: Filter report by date range
  - Test: Set dates and click
  
- [ ] **Reset Filters** button
  - Expected: Clear all report filters
  - Test: Click and verify filters cleared

---

## Settings

### General Settings
- [ ] **Save Settings** button
  - Expected: Save all settings changes
  - Test: Make changes and click
  
- [ ] **Reset to Default** button
  - Expected: Reset settings to default values
  - Test: Click and verify confirmation

### User Management
- [ ] **Add User** button
  - Expected: Open new user form
  - Test: Click and verify form opens
  
- [ ] **Edit User** button (per user)
  - Expected: Open edit user form
  - Test: Click and verify form opens
  
- [ ] **Delete User** button (per user)
  - Expected: Show confirmation, then delete
  - Test: Click and verify confirmation
  
- [ ] **Reset Password** button (per user)
  - Expected: Send password reset email
  - Test: Click and verify email sent

### Roles & Permissions
- [ ] **Add Role** button
  - Expected: Open new role form
  - Test: Click and verify form opens
  
- [ ] **Edit Role** button (per role)
  - Expected: Open edit role form
  - Test: Click and verify form opens
  
- [ ] **Delete Role** button (per role)
  - Expected: Show confirmation, then delete
  - Test: Click and verify confirmation

### Backup & Restore
- [ ] **Create Backup** button
  - Expected: Create database backup
  - Test: Click and verify backup created
  
- [ ] **Restore Backup** button
  - Expected: Open restore dialog
  - Test: Click and verify dialog opens
  
- [ ] **Download Backup** button
  - Expected: Download backup file
  - Test: Click and verify download

---

## Authentication

### Login Page
- [ ] **Login** button
  - Expected: Authenticate user and redirect
  - Test: Enter credentials and click
  
- [ ] **Forgot Password** button
  - Expected: Open password reset form
  - Test: Click and verify form opens

### 2FA Page
- [ ] **Verify Code** button
  - Expected: Verify 2FA code
  - Test: Enter code and click
  
- [ ] **Use Backup Code** button
  - Expected: Switch to backup code input
  - Test: Click and verify input changes
  
- [ ] **Resend Code** button
  - Expected: Resend 2FA code
  - Test: Click and verify code sent

### Profile
- [ ] **Update Profile** button
  - Expected: Save profile changes
  - Test: Make changes and click
  
- [ ] **Change Password** button
  - Expected: Open change password form
  - Test: Click and verify form opens
  
- [ ] **Enable 2FA** button
  - Expected: Start 2FA setup process
  - Test: Click and verify QR code displayed
  
- [ ] **Disable 2FA** button
  - Expected: Disable 2FA after confirmation
  - Test: Click and verify confirmation
  
- [ ] **Logout** button
  - Expected: Log out user and redirect to login
  - Test: Click and verify logout

---

## Common Buttons (across all pages)

### Navigation
- [ ] **Back** button
  - Expected: Navigate to previous page
  - Test: Click and verify navigation
  
- [ ] **Home** button
  - Expected: Navigate to dashboard
  - Test: Click and verify navigation

### Forms
- [ ] **Submit** button
  - Expected: Submit form data
  - Test: Fill form and click
  
- [ ] **Cancel** button
  - Expected: Close form without saving
  - Test: Click and verify form closes
  
- [ ] **Reset** button
  - Expected: Clear form fields
  - Test: Fill form and click

### Modals/Dialogs
- [ ] **Confirm** button
  - Expected: Confirm action and close
  - Test: Click and verify action
  
- [ ] **Close** (X) button
  - Expected: Close modal without action
  - Test: Click and verify modal closes

---

## Testing Checklist Summary

### Total Buttons to Test
- Dashboard: 10 buttons
- Products: 15 buttons
- POS: 20 buttons
- Purchases: 10 buttons
- Customers: 10 buttons
- Suppliers: 8 buttons
- Reports: 8 buttons
- Settings: 15 buttons
- Authentication: 12 buttons
- Common: 8 buttons

**Total: ~116 buttons**

---

## Issue Tracking

### Found Issues
| Button | Page | Issue | Priority | Status |
|--------|------|-------|----------|--------|
| Example | Products | Not responding | High | Open |

---

## Automated Testing Script

```javascript
// Playwright example
const { test, expect } = require('@playwright/test');

test('Dashboard - New Sale button works', async ({ page }) => {
  await page.goto('http://localhost:5502');
  await page.click('text=New Sale');
  await expect(page).toHaveURL(/.*pos/);
});

// Add more tests...
```

---

## Notes

- Test on different browsers (Chrome, Firefox, Safari)
- Test on different screen sizes (Mobile, Tablet, Desktop)
- Test with different user roles (Admin, Manager, Cashier)
- Test with slow network connection
- Test with disabled JavaScript (should show fallback)

---

**Status:** Ready for Testing  
**Last Updated:** 2025-12-13  
**Tester:** [Your Name]
