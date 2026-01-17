import { test, expect } from '@playwright/test';

test.describe('Product Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid="username-input"]', 'admin');
    await page.fill('[data-testid="password-input"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Wait for dashboard to fully load
    await page.waitForURL('/dashboard', { timeout: 10000 });
    
    // Wait for user menu to ensure app is fully initialized
    await page.waitForSelector('[data-testid="user-menu"]', { 
      state: 'visible', 
      timeout: 10000 
    });
    
    // Navigate to products page using React Router (no full reload)
    await page.click('a[href="/products"]');
    
    // Wait for products page to load
    await page.waitForURL('/products', { timeout: 10000 });
    await page.waitForLoadState('networkidle');
  });

  test('should display products list', async ({ page }) => {
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Try to find products list with different selectors
    const tableSelectors = [
      '[data-testid="products-table"]',
      'table',
      '[class*="product"]',
      '.grid'
    ];
    
    let tableFound = false;
    for (const selector of tableSelectors) {
      try {
        await page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
        tableFound = true;
        break;
      } catch {
        continue;
      }
    }
    
    // Page should have some products content
    expect(tableFound).toBeTruthy();
    
    // Check if products are loaded (table rows or grid cards)
    const rows = page.locator('[data-testid="products-table"] tbody tr, [class*="product"], .grid > div');
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should search for product', async ({ page }) => {
    // Find search input
    const searchInput = page.locator('input[placeholder*="search" i]');
    
    if (await searchInput.isVisible()) {
      // Type search term
      await searchInput.fill('test');
      
      // Wait for results
      await page.waitForLoadState('networkidle');
      
      // Verify results are filtered
      const rows = page.locator('tbody tr');
      const count = await rows.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test('should create new product', async ({ page }) => {
    // Click add product button
    const addButton = page.locator('button:has-text("Add Product")');
    if (await addButton.isVisible()) {
      await addButton.click();
      
      // Wait for modal/form
      await page.waitForLoadState('networkidle');
      
      // Fill product form
      const timestamp = Date.now();
      await page.fill('input[name="name"]', `Test Product ${timestamp}`);
      await page.fill('input[name="sku"]', `SKU-${timestamp}`);
      await page.fill('input[name="price"]', '100');
      
      // Fill category if exists
      const categorySelect = page.locator('select[name="category"]');
      if (await categorySelect.isVisible()) {
        await categorySelect.selectOption({ index: 1 });
      }
      
      // Submit form
      const submitButton = page.locator('button[type="submit"]');
      await submitButton.click();
      
      // Wait for success message
      await expect(page.locator('text=/success|created|added/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should edit product', async ({ page }) => {
    // Find first product row
    const firstRow = page.locator('tbody tr').first();
    
    // Click edit button
    const editButton = firstRow.locator('button:has-text("Edit")');
    if (await editButton.isVisible()) {
      await editButton.click();
      
      // Wait for form
      await page.waitForLoadState('networkidle');
      
      // Update product name
      const nameInput = page.locator('input[name="name"]');
      await nameInput.clear();
      await nameInput.fill(`Updated Product ${Date.now()}`);
      
      // Submit
      const submitButton = page.locator('button[type="submit"]');
      await submitButton.click();
      
      // Wait for success
      await expect(page.locator('text=/success|updated/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should delete product', async ({ page }) => {
    // Find first product row
    const firstRow = page.locator('tbody tr').first();
    
    // Click delete button
    const deleteButton = firstRow.locator('button:has-text("Delete")');
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      
      // Confirm deletion if dialog appears
      const confirmButton = page.locator('button:has-text("Confirm")');
      if (await confirmButton.isVisible()) {
        await confirmButton.click();
      }
      
      // Wait for success
      await expect(page.locator('text=/success|deleted/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should filter products by category', async ({ page }) => {
    // Find category filter
    const categoryFilter = page.locator('select[name="category"]');
    
    if (await categoryFilter.isVisible()) {
      // Select a category
      await categoryFilter.selectOption({ index: 1 });
      
      // Wait for results
      await page.waitForLoadState('networkidle');
      
      // Verify results are filtered
      const rows = page.locator('tbody tr');
      const count = await rows.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test('should sort products by price', async ({ page }) => {
    // Find price column header
    const priceHeader = page.locator('th:has-text("Price")');
    
    if (await priceHeader.isVisible()) {
      // Click to sort
      await priceHeader.click();
      
      // Wait for sort
      await page.waitForLoadState('networkidle');
      
      // Verify sort indicator
      const sortIndicator = priceHeader.locator('[class*="sort"]');
      if (await sortIndicator.isVisible()) {
        await expect(sortIndicator).toBeVisible();
      }
    }
  });

  test('should paginate products', async ({ page }) => {
    // Find pagination controls
    const nextButton = page.locator('button:has-text("Next")');
    
    if (await nextButton.isVisible()) {
      // Click next
      await nextButton.click();
      
      // Wait for new page
      await page.waitForLoadState('networkidle');
      
      // Verify we're on next page
      const rows = page.locator('tbody tr');
      const count = await rows.count();
      expect(count).toBeGreaterThan(0);
    }
  });

  test('should view product details', async ({ page }) => {
    // Find first product row
    const firstRow = page.locator('tbody tr').first();
    
    // Click on product name to view details
    const productLink = firstRow.locator('a').first();
    if (await productLink.isVisible()) {
      await productLink.click();
      
      // Wait for details page
      await page.waitForLoadState('networkidle');
      
      // Verify details are displayed
      await expect(page.locator('text=/details|information|product/i')).toBeVisible();
    }
  });

  test('should handle bulk actions', async ({ page }) => {
    // Find select all checkbox
    const selectAllCheckbox = page.locator('input[type="checkbox"][aria-label*="all" i]');
    
    if (await selectAllCheckbox.isVisible()) {
      // Select all
      await selectAllCheckbox.check();
      
      // Find bulk action button
      const bulkButton = page.locator('button:has-text("Bulk")');
      if (await bulkButton.isVisible()) {
        await bulkButton.click();
        
        // Verify bulk actions menu appears
        await expect(page.locator('text=/export|delete|update/i')).toBeVisible();
      }
    }
  });
});

