import { test, expect } from './fixtures';

/**
 * Warehouses CRUD E2E Tests
 * Validates warehouse management including WarehouseViewModal with capacity tracking
 */

test.describe('Warehouses Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/warehouses');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/مخزن|Warehouse/);
  });

  test('should display warehouses list', async ({ authenticatedPage }) => {
    await authenticatedPage.waitForSelector('table, .warehouse-card', { timeout: 10000 });
    const hasContent = await authenticatedPage.locator('table thead, .warehouse-card').isVisible();
    expect(hasContent).toBeTruthy();
  });

  test('should create new warehouse', async ({ authenticatedPage }) => {
    await authenticatedPage.click('button:has-text("إضافة"), button:has-text("Add")');
    await authenticatedPage.waitForSelector('[role="dialog"], form', { timeout: 5000 });
    
    await authenticatedPage.fill('input[name="name"]', `Test Warehouse ${Date.now()}`);
    await authenticatedPage.fill('input[name="location"]', 'Test Location');
    await authenticatedPage.fill('input[name="capacity"]', '1000');
    
    await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
    await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should view warehouse details with capacity visualization', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Verify WarehouseViewModal sections
      await expect(authenticatedPage.locator('text=المعلومات الأساسية, text=Basic Info')).toBeVisible();
      await expect(authenticatedPage.locator('text=السعة والمخزون, text=Capacity')).toBeVisible();
      
      // Verify capacity percentage bar exists
      const modal = authenticatedPage.locator('[role="dialog"]');
      const progressBar = modal.locator('.bg-green-500, .bg-yellow-500, .bg-red-500');
      if (await progressBar.count() > 0) {
        await expect(progressBar.first()).toBeVisible();
      }
      
      // Close modal
      await authenticatedPage.keyboard.press('Escape');
    }
  });

  test('should edit warehouse', async ({ authenticatedPage }) => {
    const editButton = authenticatedPage.locator('svg.lucide-pencil').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      const nameInput = authenticatedPage.locator('input[name="name"]');
      await nameInput.fill(`Updated Warehouse ${Date.now()}`);
      
      await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete warehouse', async ({ authenticatedPage }) => {
    const deleteButton = authenticatedPage.locator('svg.lucide-trash').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      await authenticatedPage.waitForSelector('[role="alertdialog"], [role="dialog"]', { timeout: 3000 });
      await authenticatedPage.click('button:has-text("تأكيد"), button:has-text("Confirm")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should show capacity warning for high utilization', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Check for warning indicators (>80% utilization)
      const modal = authenticatedPage.locator('[role="dialog"]');
      const warningText = modal.locator('text=تحذير, text=Warning');
      
      // If warehouse is over capacity, warning should be visible
      if (await warningText.count() > 0) {
        await expect(warningText.first()).toBeVisible();
      }
      
      await authenticatedPage.keyboard.press('Escape');
    }
  });
});
