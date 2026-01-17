import { test, expect } from './fixtures';

/**
 * Suppliers CRUD E2E Tests
 * Validates supplier management including SupplierViewModal with rating display
 */

test.describe('Suppliers Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/suppliers');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/مورد|Supplier/);
  });

  test('should display suppliers list', async ({ authenticatedPage }) => {
    await authenticatedPage.waitForSelector('table, .supplier-card', { timeout: 10000 });
    const hasContent = await authenticatedPage.locator('table thead, .supplier-card').isVisible();
    expect(hasContent).toBeTruthy();
  });

  test('should create new supplier', async ({ authenticatedPage }) => {
    await authenticatedPage.click('button:has-text("إضافة"), button:has-text("Add")');
    await authenticatedPage.waitForSelector('[role="dialog"], form', { timeout: 5000 });
    
    await authenticatedPage.fill('input[name="name"]', `Test Supplier ${Date.now()}`);
    await authenticatedPage.fill('input[name="phone"]', '01234567890');
    await authenticatedPage.fill('input[name="email"]', `supplier${Date.now()}@test.com`);
    
    await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
    await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should view supplier details with rating section', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Verify SupplierViewModal specific sections
      await expect(authenticatedPage.locator('text=التقييم والأداء, text=Rating')).toBeVisible();
      await expect(authenticatedPage.locator('text=المعلومات الأساسية, text=Basic')).toBeVisible();
      
      // Close with ESC
      await authenticatedPage.keyboard.press('Escape');
      await expect(authenticatedPage.locator('[role="dialog"]')).not.toBeVisible({ timeout: 3000 });
    }
  });

  test('should edit supplier', async ({ authenticatedPage }) => {
    const editButton = authenticatedPage.locator('svg.lucide-pencil').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      const nameInput = authenticatedPage.locator('input[name="name"]');
      await nameInput.fill(`Updated Supplier ${Date.now()}`);
      
      await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete supplier', async ({ authenticatedPage }) => {
    const deleteButton = authenticatedPage.locator('svg.lucide-trash').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      await authenticatedPage.waitForSelector('[role="alertdialog"], [role="dialog"]', { timeout: 3000 });
      await authenticatedPage.click('button:has-text("تأكيد"), button:has-text("Confirm")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });
});
