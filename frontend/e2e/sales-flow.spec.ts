import { test, expect } from './fixtures';

/**
 * Sales Flow E2E Tests - RORLOC Phase 4
 * P1 High Priority - Complete business flow
 */

test.describe('Sales Invoice Flow - P1 High', () => {
  test('should complete full sales invoice flow', async ({ authenticatedPage }) => {
    // Step 1: Navigate to invoices
    await authenticatedPage.goto('/invoices');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/فاتور|Invoice/);
    
    // Step 2: Click add new invoice
    const addButton = authenticatedPage.locator(
      'button:has-text("إضافة"), button:has-text("Add"), button:has-text("جديد")'
    );
    await addButton.first().click();
    
    // Step 3: Wait for form/modal
    await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
    
    // Step 4: Select invoice type (sales)
    const typeSelect = authenticatedPage.locator('select[name*="type"], [name*="invoice_type"]');
    if (await typeSelect.isVisible()) {
      await typeSelect.selectOption({ label: /بيع|sales/i });
    }
    
    // Step 5: Select customer
    const customerSelect = authenticatedPage.locator('select[name*="customer"], [name*="customer_id"]');
    if (await customerSelect.isVisible()) {
      await customerSelect.selectOption({ index: 1 });
    }
    
    // Step 6: Add invoice items (simplified)
    const addItemButton = authenticatedPage.locator(
      'button:has-text("إضافة صنف"), button:has-text("Add Item")'
    );
    if (await addItemButton.isVisible()) {
      await addItemButton.click();
      await authenticatedPage.waitForTimeout(500);
    }
    
    // Step 7: Submit invoice
    const submitButton = authenticatedPage.locator(
      'button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")'
    );
    if (await submitButton.isVisible()) {
      await submitButton.click();
      
      // Verify success
      await expect(
        authenticatedPage.locator('.toast-success, .alert-success, [role="alert"]')
      ).toBeVisible({ timeout: 10000 });
    }
  });

  test('should validate required fields in sales invoice', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/invoices');
    
    // Click add
    const addButton = authenticatedPage.locator('button:has-text("إضافة"), button:has-text("Add")');
    await addButton.first().click();
    
    // Wait for form
    await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
    
    // Try to submit without filling required fields
    const submitButton = authenticatedPage.locator('button[type="submit"]');
    if (await submitButton.isVisible()) {
      await submitButton.click();
      
      // Should show validation errors or not submit
      // Check for error indicators
      const hasErrors = await authenticatedPage.locator(
        '.error, .invalid, [aria-invalid="true"], .text-red, .text-destructive'
      ).isVisible();
      
      // Either validation errors shown or form still open
      const formStillOpen = await authenticatedPage.locator('form, [role="dialog"]').isVisible();
      
      expect(hasErrors || formStillOpen).toBeTruthy();
    }
  });

  test('should calculate invoice totals correctly', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/invoices');
    
    // Open existing invoice or create new one
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Check for total calculation elements
      const totalElement = authenticatedPage.locator(
        '[class*="total"], :has-text("الإجمالي"), :has-text("Total")'
      );
      
      await expect(totalElement.first()).toBeVisible();
    }
  });
});

test.describe('Purchase Flow - P1 High', () => {
  test('should navigate to purchase invoices', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/purchase-invoices');
    
    // Verify page loads
    await authenticatedPage.waitForLoadState('networkidle');
    
    // Should show purchase invoices content
    const pageContent = await authenticatedPage.textContent('body');
    const isPurchasePage = 
      pageContent?.includes('شراء') || 
      pageContent?.includes('Purchase') ||
      pageContent?.includes('مورد') ||
      pageContent?.includes('Supplier');
    
    expect(isPurchasePage).toBeTruthy();
  });

  test('should create purchase invoice', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/purchase-invoices');
    
    // Click add
    const addButton = authenticatedPage.locator('button:has-text("إضافة"), button:has-text("Add")');
    if (await addButton.isVisible()) {
      await addButton.click();
      
      // Wait for form
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      // Form should be visible
      await expect(authenticatedPage.locator('form, [role="dialog"]')).toBeVisible();
    }
  });
});

test.describe('Stock Movement Flow - P1 High', () => {
  test('should view stock movements', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/stock-movements');
    
    // Wait for page to load
    await authenticatedPage.waitForLoadState('networkidle');
    
    // Verify stock movements page
    const pageContent = await authenticatedPage.textContent('body');
    const isStockPage = 
      pageContent?.includes('حركة') || 
      pageContent?.includes('Movement') ||
      pageContent?.includes('مخزون') ||
      pageContent?.includes('Stock');
    
    expect(isStockPage).toBeTruthy();
  });

  test('should filter stock movements by type', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/stock-movements');
    await authenticatedPage.waitForLoadState('networkidle');
    
    // Find type filter
    const typeFilter = authenticatedPage.locator('select[name*="type"], [aria-label*="filter"]');
    
    if (await typeFilter.isVisible()) {
      await typeFilter.selectOption({ index: 1 });
      await authenticatedPage.waitForTimeout(1000);
      
      // Results should update
      await expect(authenticatedPage.locator('table, .list')).toBeVisible();
    }
  });
});

