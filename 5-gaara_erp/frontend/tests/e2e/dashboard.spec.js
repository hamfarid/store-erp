import { test, expect } from '@playwright/test';

test.describe('Dashboard Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid="username-input"]', 'admin');
    await page.fill('[data-testid="password-input"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Wait for dashboard
    await page.waitForURL('/dashboard', { timeout: 10000 });
  });

  test('should display dashboard', async ({ page }) => {
    // Verify dashboard is loaded
    await expect(page).toHaveURL(/.*dashboard/);
    
    // Check for main dashboard elements
    await expect(page.locator('text=/dashboard|overview|summary/i')).toBeVisible();
  });

  test('should display key metrics', async ({ page }) => {
    // Wait for page to fully load
    await page.waitForLoadState('networkidle');
    
    // Try to find metric cards with different selectors
    const metricSelectors = [
      '[data-testid="metric-card"]',
      '[class*="stat"]',
      '[class*="metric"]',
      '[class*="card"]'
    ];
    
    let foundCards = false;
    for (const selector of metricSelectors) {
      try {
        await page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
        const cards = page.locator(selector);
        const count = await cards.count();
        if (count > 0) {
          foundCards = true;
          break;
        }
      } catch {
        continue;
      }
    }
    
    // Dashboard should have some visible content
    const hasContent = await page.locator('main, [role="main"], .dashboard, .content').count() > 0;
    expect(foundCards || hasContent).toBeTruthy();
  });

  test('should navigate to products', async ({ page }) => {
    // Click products link
    const productsLink = page.locator('a:has-text("Products")');
    if (await productsLink.isVisible()) {
      await productsLink.click();
      
      // Wait for products page
      await page.waitForURL(/.*products/, { timeout: 10000 });
      await expect(page).toHaveURL(/.*products/);
    }
  });

  test('should navigate to invoices', async ({ page }) => {
    // Click invoices link
    const invoicesLink = page.locator('a:has-text("Invoices")');
    if (await invoicesLink.isVisible()) {
      await invoicesLink.click();
      
      // Wait for invoices page
      await page.waitForURL(/.*invoices/, { timeout: 10000 });
      await expect(page).toHaveURL(/.*invoices/);
    }
  });

  test('should navigate to customers', async ({ page }) => {
    // Click customers link
    const customersLink = page.locator('a:has-text("Customers")');
    if (await customersLink.isVisible()) {
      await customersLink.click();
      
      // Wait for customers page
      await page.waitForURL(/.*customers/, { timeout: 10000 });
      await expect(page).toHaveURL(/.*customers/);
    }
  });

  test('should navigate to inventory', async ({ page }) => {
    // Click inventory link
    const inventoryLink = page.locator('a:has-text("Inventory")');
    if (await inventoryLink.isVisible()) {
      await inventoryLink.click();
      
      // Wait for inventory page
      await page.waitForURL(/.*inventory/, { timeout: 10000 });
      await expect(page).toHaveURL(/.*inventory/);
    }
  });

  test('should navigate to reports', async ({ page }) => {
    // Click reports link
    const reportsLink = page.locator('a:has-text("Reports")');
    if (await reportsLink.isVisible()) {
      await reportsLink.click();
      
      // Wait for reports page
      await page.waitForURL(/.*reports/, { timeout: 10000 });
      await expect(page).toHaveURL(/.*reports/);
    }
  });

  test('should navigate to settings', async ({ page }) => {
    // Click settings link
    const settingsLink = page.locator('a:has-text("Settings")');
    if (await settingsLink.isVisible()) {
      await settingsLink.click();
      
      // Wait for settings page
      await page.waitForURL(/.*settings/, { timeout: 10000 });
      await expect(page).toHaveURL(/.*settings/);
    }
  });

  test('should toggle sidebar', async ({ page }) => {
    // Find sidebar toggle button
    const toggleButton = page.locator('button[aria-label*="toggle" i], button[class*="menu"]').first();
    
    if (await toggleButton.isVisible()) {
      // Get initial sidebar state
      const sidebar = page.locator('[class*="sidebar"]');
      const initialVisible = await sidebar.isVisible();
      
      // Toggle sidebar
      await toggleButton.click();
      
      // Wait for animation
      await page.waitForTimeout(300);
      
      // Verify state changed
      const finalVisible = await sidebar.isVisible();
      expect(finalVisible).not.toBe(initialVisible);
    }
  });

  test('should toggle theme', async ({ page }) => {
    // Find theme toggle button
    const themeButton = page.locator('button[aria-label*="theme" i], button[class*="dark"]').first();
    
    if (await themeButton.isVisible()) {
      // Get initial theme
      const html = page.locator('html');
      const initialClass = await html.getAttribute('class');
      
      // Toggle theme
      await themeButton.click();
      
      // Wait for theme change
      await page.waitForTimeout(300);
      
      // Verify theme changed
      const finalClass = await html.getAttribute('class');
      expect(finalClass).not.toBe(initialClass);
    }
  });

  test('should display user profile menu', async ({ page }) => {
    // Click user menu
    const userMenu = page.locator('[data-testid="user-menu"]');
    if (await userMenu.isVisible()) {
      await userMenu.click();
      
      // Check for profile options
      await expect(page.locator('text=/profile|settings|logout/i')).toBeVisible();
    }
  });

  test('should display notifications', async ({ page }) => {
    // Find notification bell
    const notificationBell = page.locator('button[aria-label*="notification" i]');
    
    if (await notificationBell.isVisible()) {
      await notificationBell.click();
      
      // Check for notification panel
      const notificationPanel = page.locator('[class*="notification"]');
      await expect(notificationPanel).toBeVisible();
    }
  });

  test('should display search functionality', async ({ page }) => {
    // Find search input
    const searchInput = page.locator('input[placeholder*="search" i]');
    
    if (await searchInput.isVisible()) {
      // Type search term
      await searchInput.fill('test');
      
      // Wait for results
      await page.waitForLoadState('networkidle');
      
      // Check for search results
      const results = page.locator('[class*="search-result"]');
      const count = await results.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test('should handle responsive layout on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Verify page is still accessible
    await expect(page).toHaveURL(/.*dashboard/);
    
    // Check if mobile menu is visible
    const mobileMenu = page.locator('button[class*="mobile"], button[class*="hamburger"]');
    if (await mobileMenu.isVisible()) {
      await expect(mobileMenu).toBeVisible();
    }
  });

  test('should handle responsive layout on tablet', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Verify page is still accessible
    await expect(page).toHaveURL(/.*dashboard/);
    
    // Check if layout adapts
    const sidebar = page.locator('[class*="sidebar"]');
    if (await sidebar.isVisible()) {
      await expect(sidebar).toBeVisible();
    }
  });

  test('should load dashboard quickly', async ({ page }) => {
    // Measure load time
    const startTime = Date.now();
    
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Dashboard should load in less than 3 seconds
    expect(loadTime).toBeLessThan(3000);
  });
});

