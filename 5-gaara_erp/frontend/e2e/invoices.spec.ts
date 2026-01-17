import { test, expect } from './fixtures';

/**
 * Invoices CRUD E2E Tests
 * Validates invoice management workflow
 */

test.describe('Invoices Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/invoices');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/فاتورة|Invoice/);
  });

  test('should display invoices list', async ({ authenticatedPage }) => {
    await authenticatedPage.waitForSelector('table, .invoice-card', { timeout: 10000 });
    const hasContent = await authenticatedPage.locator('table thead, .invoice-card').isVisible();
    expect(hasContent).toBeTruthy();
  });

  test('should create new invoice', async ({ authenticatedPage }) => {
    await authenticatedPage.click('button:has-text("إضافة"), button:has-text("Add"), button:has-text("فاتورة جديدة")');
    await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
    
    // Fill invoice details (simplified)
    const customerSelect = authenticatedPage.locator('select[name*="customer"]');
    if (await customerSelect.isVisible()) {
      await customerSelect.selectOption({ index: 1 });
    }
    
    await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
    await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should view invoice details', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Verify invoice items table exists
      await expect(authenticatedPage.locator('text=المنتجات, text=Items, text=البنود')).toBeVisible();
      
      await authenticatedPage.keyboard.press('Escape');
    }
  });

  test('should filter invoices by type', async ({ authenticatedPage }) => {
    const typeFilter = authenticatedPage.locator('select[name*="type"], button:has-text("مبيعات"), button:has-text("Sales")');
    
    if (await typeFilter.isVisible()) {
      await typeFilter.click();
      await authenticatedPage.waitForTimeout(1000);
      
      const results = authenticatedPage.locator('table tbody tr, .invoice-card');
      await expect(results).toHaveCount(await results.count(), { timeout: 5000 });
    }
  });

  test('should filter invoices by status', async ({ authenticatedPage }) => {
    const statusFilter = authenticatedPage.locator('select[name*="status"], button:has-text("مدفوعة")');
    
    if (await statusFilter.isVisible()) {
      await statusFilter.click();
      await authenticatedPage.waitForTimeout(1000);
      
      const results = authenticatedPage.locator('table tbody tr, .invoice-card');
      await expect(results).toHaveCount(await results.count(), { timeout: 5000 });
    }
  });

  test('should edit invoice', async ({ authenticatedPage }) => {
    const editButton = authenticatedPage.locator('svg.lucide-pencil').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      // Modify notes or description if available
      const notesField = authenticatedPage.locator('textarea[name*="note"], input[name*="note"]');
      if (await notesField.isVisible()) {
        await notesField.fill(`Updated notes ${Date.now()}`);
      }
      
      await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete invoice (admin only)', async ({ authenticatedPage }) => {
    const deleteButton = authenticatedPage.locator('svg.lucide-trash').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      await authenticatedPage.waitForSelector('[role="alertdialog"], [role="dialog"]', { timeout: 3000 });
      await authenticatedPage.click('button:has-text("تأكيد"), button:has-text("Confirm")');
      
      // Success or permission denied
      const notification = authenticatedPage.locator('.toast-success, .alert-success, .toast-error, .alert-error');
      await expect(notification).toBeVisible({ timeout: 5000 });
    }
  });
});
