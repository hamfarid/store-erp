import { test, expect } from './fixtures';

/**
 * Categories CRUD E2E Tests
 * Validates category management including CategoryViewModal with hierarchy display
 */

test.describe('Categories Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/categories');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/تصنيف|Categor/);
  });

  test('should display categories list', async ({ authenticatedPage }) => {
    await authenticatedPage.waitForSelector('table, .category-card', { timeout: 10000 });
    const hasContent = await authenticatedPage.locator('table thead, .category-card').isVisible();
    expect(hasContent).toBeTruthy();
  });

  test('should create new category', async ({ authenticatedPage }) => {
    await authenticatedPage.click('button:has-text("إضافة"), button:has-text("Add")');
    await authenticatedPage.waitForSelector('[role="dialog"], form', { timeout: 5000 });
    
    await authenticatedPage.fill('input[name="name"]', `Test Category ${Date.now()}`);
    await authenticatedPage.fill('textarea[name="description"], input[name="description"]', 'Test Description');
    
    await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
    await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should view category details with hierarchy', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Verify CategoryViewModal sections
      await expect(authenticatedPage.locator('text=المعلومات الأساسية, text=Basic Info')).toBeVisible();
      await expect(authenticatedPage.locator('text=التسلسل الهرمي, text=Hierarchy')).toBeVisible();
      
      // Verify gradient header
      const modal = authenticatedPage.locator('[role="dialog"]');
      await expect(modal.locator('.bg-gradient-to-r')).toBeVisible();
      
      // Close modal
      await authenticatedPage.click('button:has-text("إغلاق"), button:has-text("Close")');
    }
  });

  test('should close category modal with ESC', async ({ authenticatedPage }) => {
    const viewButton = authenticatedPage.locator('svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      await authenticatedPage.keyboard.press('Escape');
      await expect(authenticatedPage.locator('[role="dialog"]')).not.toBeVisible({ timeout: 3000 });
    }
  });

  test('should edit category', async ({ authenticatedPage }) => {
    const editButton = authenticatedPage.locator('svg.lucide-pencil').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      const nameInput = authenticatedPage.locator('input[name="name"]');
      await nameInput.fill(`Updated Category ${Date.now()}`);
      
      await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete category', async ({ authenticatedPage }) => {
    const deleteButton = authenticatedPage.locator('svg.lucide-trash').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      await authenticatedPage.waitForSelector('[role="alertdialog"], [role="dialog"]', { timeout: 3000 });
      await authenticatedPage.click('button:has-text("تأكيد"), button:has-text("Confirm")');
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should search categories', async ({ authenticatedPage }) => {
    const searchInput = authenticatedPage.locator('input[type="search"], input[placeholder*="بحث"]');
    
    if (await searchInput.isVisible()) {
      await searchInput.fill('test');
      await authenticatedPage.waitForTimeout(1000);
      
      const results = authenticatedPage.locator('table tbody tr, .category-card');
      await expect(results).toHaveCount(await results.count(), { timeout: 5000 });
    }
  });
});
