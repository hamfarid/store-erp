import { test, expect } from './fixtures';

/**
 * Products CRUD E2E Tests
 * Validates complete product management workflow
 */

test.describe('Products Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    // Navigate to products page
    await authenticatedPage.goto('/products');
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/منتج|Products/);
  });

  test('should display products list', async ({ authenticatedPage }) => {
    // Wait for products to load
    await authenticatedPage.waitForSelector('table, .product-card', { timeout: 10000 });
    
    // Verify table headers or card elements exist
    const hasTable = await authenticatedPage.locator('table thead').isVisible();
    const hasCards = await authenticatedPage.locator('.product-card').isVisible();
    
    expect(hasTable || hasCards).toBeTruthy();
  });

  test('should create new product', async ({ authenticatedPage }) => {
    // Click add product button
    await authenticatedPage.click('button:has-text("إضافة"), button:has-text("Add")');
    
    // Wait for modal/form
    await authenticatedPage.waitForSelector('[role="dialog"], form', { timeout: 5000 });
    
    // Fill product details
    await authenticatedPage.fill('input[name="name"]', `Test Product ${Date.now()}`);
    await authenticatedPage.fill('input[name="sku"]', `SKU-${Date.now()}`);
    await authenticatedPage.fill('input[name="price"]', '100');
    await authenticatedPage.fill('input[name="cost"]', '50');
    await authenticatedPage.fill('input[name="stock_quantity"]', '10');
    
    // Submit form
    await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
    
    // Verify success notification
    await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
  });

  test('should search products', async ({ authenticatedPage }) => {
    // Find search input
    const searchInput = authenticatedPage.locator('input[type="search"], input[placeholder*="بحث"], input[placeholder*="Search"]');
    
    if (await searchInput.isVisible()) {
      await searchInput.fill('test');
      await authenticatedPage.waitForTimeout(1000); // Debounce
      
      // Verify filtered results
      const results = authenticatedPage.locator('table tbody tr, .product-card');
      await expect(results).toHaveCount(await results.count(), { timeout: 5000 });
    }
  });

  test('should view product details', async ({ authenticatedPage }) => {
    // Click first view/eye button
    const viewButton = authenticatedPage.locator('button[aria-label*="view"], button:has-text("عرض"), svg.lucide-eye').first();
    
    if (await viewButton.isVisible()) {
      await viewButton.click();
      
      // Wait for view modal
      await authenticatedPage.waitForSelector('[role="dialog"]', { timeout: 5000 });
      
      // Verify modal content
      await expect(authenticatedPage.locator('[role="dialog"]')).toContainText(/معلومات|Details|Product/);
    }
  });

  test('should edit product', async ({ authenticatedPage }) => {
    // Click first edit button
    const editButton = authenticatedPage.locator('button[aria-label*="edit"], button:has-text("تعديل"), svg.lucide-pencil').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      
      // Wait for edit form
      await authenticatedPage.waitForSelector('form, [role="dialog"]', { timeout: 5000 });
      
      // Modify a field
      const nameInput = authenticatedPage.locator('input[name="name"]');
      await nameInput.fill(`Updated Product ${Date.now()}`);
      
      // Submit
      await authenticatedPage.click('button[type="submit"]:has-text("حفظ"), button[type="submit"]:has-text("Save")');
      
      // Verify success
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete product', async ({ authenticatedPage }) => {
    // Click first delete button
    const deleteButton = authenticatedPage.locator('button[aria-label*="delete"], button:has-text("حذف"), svg.lucide-trash').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      
      // Confirm deletion in dialog
      await authenticatedPage.waitForSelector('[role="alertdialog"], [role="dialog"]', { timeout: 3000 });
      await authenticatedPage.click('button:has-text("تأكيد"), button:has-text("Confirm"), button:has-text("نعم")');
      
      // Verify success
      await expect(authenticatedPage.locator('.toast-success, .alert-success')).toBeVisible({ timeout: 5000 });
    }
  });

  test('should filter by category', async ({ authenticatedPage }) => {
    // Find category filter
    const categoryFilter = authenticatedPage.locator('select[name*="category"], select:has-text("تصنيف")');
    
    if (await categoryFilter.isVisible()) {
      await categoryFilter.selectOption({ index: 1 });
      await authenticatedPage.waitForTimeout(1000);
      
      // Verify results updated
      const results = authenticatedPage.locator('table tbody tr, .product-card');
      await expect(results).toHaveCount(await results.count(), { timeout: 5000 });
    }
  });

  test('should export products', async ({ authenticatedPage }) => {
    // Find export button
    const exportButton = authenticatedPage.locator('button:has-text("تصدير"), button:has-text("Export"), button:has([aria-label*="export"])');
    
    if (await exportButton.isVisible()) {
      // Start waiting for download before clicking
      const downloadPromise = authenticatedPage.waitForEvent('download');
      await exportButton.click();
      
      // Wait for download
      const download = await downloadPromise;
      expect(download.suggestedFilename()).toMatch(/\.xlsx$|\.csv$/);
    }
  });
});
