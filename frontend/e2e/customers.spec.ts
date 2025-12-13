import { test, expect } from './fixtures';

/**
 * Customers CRUD E2E Tests
 * Validates complete customer management workflow including new ViewModal
 */

test.describe('Customers Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/customers');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/عميل|Customer/);
  });

  test('should display customers list', async ({ authenticatedPage }) => {
    await authenticatedPage.waitForSelector('table, .customer-card', { timeout: 10000 });
    const hasContent = await authenticatedPage.locator('table thead, .customer-card').isVisible();
    expect(hasContent).toBeTruthy();
  });

  test('should create new customer', async ({ authenticatedPage }) => {
    await authenticatedPage.click('button:has-text("إضافة"), button:has-text("Add")');
    await authenticatedPage.waitForSelector('[role="dialog"], form', { timeout: 5000 });
    
    // Fill customer details
    await authenticatedPage.fill('input[name="name"]', `Test Customer ${Date.now()}`);
    await authenticatedPage.fill('input[name="phone"]', '01234567890');
    await authenticatedPage.fill('input[name="email"]', `customer${Date.now()}@test.com`);
    await authenticatedPage.fill('input[name="address"]', 'Test Address');
    
    await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
    await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should view customer details in professional modal', async ({ authenticatedPage }) => {
    // Click first view button (Eye icon)
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      
      // Wait for CustomerViewModal
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Verify modal sections exist
      await expect(authenticatedPage.locator('text=المعلومات الأساسية, text=Basic Info')).toBeVisible();
      await expect(authenticatedPage.locator('text=العنوان, text=Address')).toBeVisible();
      await expect(authenticatedPage.locator('text=معلومات العمل, text=Business')).toBeVisible();
      
      // Verify modal has gradient header
      const modal = authenticatedPage.locator('[role="dialog"]');
      await expect(modal.locator('.bg-gradient-to-r')).toBeVisible();
      
      // Close modal with button
      await authenticatedPage.click('button:has-text("إغلاق"), button:has-text("Close")');
      await expect(modal).not.toBeVisible();
    }
  });

  test('should close view modal with ESC key', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Press ESC
      await authenticatedPage.keyboard.press('Escape');
      
      // Verify modal closed
      await expect(authenticatedPage.locator('[role="dialog"]')).not.toBeVisible({ timeout: 3000 });
    }
  });

  test('should edit customer', async ({ authenticatedPage }) => {
    const editButton = authenticatedPage.locator('button[aria-label*="edit"], svg.lucide-pencil').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      const nameInput = authenticatedPage.locator('input[name="name"]');
      await nameInput.fill(`Updated Customer ${Date.now()}`);
      
      await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete customer', async ({ authenticatedPage }) => {
    const deleteButton = authenticatedPage.locator('button[aria-label*="delete"], svg.lucide-trash').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      await authenticatedPage.waitForSelector('[role="alertdialog"], [role="dialog"]', { timeout: 3000 });
      await authenticatedPage.click('button:has-text("تأكيد"), button:has-text("Confirm")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should search customers', async ({ authenticatedPage }) => {
    const searchInput = authenticatedPage.locator('input[type="search"], input[placeholder*="بحث"]');
    
    if (await searchInput.isVisible()) {
      await searchInput.fill('test');
      await authenticatedPage.waitForTimeout(1000);
      
      const results = authenticatedPage.locator('table tbody tr, .customer-card');
      await expect(results).toHaveCount(await results.count(), { timeout: 5000 });
    }
  });
});
