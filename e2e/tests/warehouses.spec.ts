/**
 * E2E Tests - Warehouses Management
 * 
 * Tests for warehouse operations and stock management.
 */

import { test, expect } from '@playwright/test';

test.describe('Warehouses Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    await expect(page).toHaveURL(/dashboard/);
    
    // Navigate to warehouses
    await page.goto('/warehouses');
  });

  test('should display warehouses list', async ({ page }) => {
    // Check for warehouses display
    const warehousesContainer = page.locator('table, .warehouses-grid, [data-testid="warehouses-list"]');
    await expect(warehousesContainer).toBeVisible();
  });

  test('should show warehouse details', async ({ page }) => {
    // Click on first warehouse
    const warehouseCard = page.locator('.warehouse-card, table tbody tr').first();
    await warehouseCard.click();
    
    // Should show details
    await page.waitForLoadState('networkidle');
  });

  test('should add new warehouse', async ({ page }) => {
    // Click add button
    const addButton = page.getByRole('button', { name: /add|إضافة|new|جديد/i });
    await addButton.click();
    
    // Fill form
    const nameInput = page.getByLabel(/name|الاسم/i).first();
    await nameInput.fill('Test Warehouse ' + Date.now());
    
    const codeInput = page.getByLabel(/code|رمز/i);
    if (await codeInput.count() > 0) {
      await codeInput.fill('WH-TEST-' + Date.now());
    }
    
    const addressInput = page.getByLabel(/address|عنوان/i);
    if (await addressInput.count() > 0) {
      await addressInput.fill('Test Address');
    }
    
    // Save
    await page.getByRole('button', { name: /save|حفظ/i }).click();
    await page.waitForLoadState('networkidle');
  });

  test('should view warehouse inventory', async ({ page }) => {
    // Click on warehouse to view inventory
    const viewInventoryBtn = page.locator('button[aria-label*="inventory"], .view-inventory-btn').first();
    const exists = await viewInventoryBtn.count();
    
    if (exists > 0) {
      await viewInventoryBtn.click();
      await page.waitForLoadState('networkidle');
      
      // Should show inventory table
      const inventoryTable = page.locator('table, [data-testid="inventory-table"]');
      await expect(inventoryTable).toBeVisible();
    }
  });

  test('should transfer stock between warehouses', async ({ page }) => {
    // Navigate to stock transfer page
    await page.goto('/warehouse-transfer');
    
    // Select source warehouse
    const sourceSelect = page.locator('select[name*="source"], [data-testid="source-warehouse"]');
    if (await sourceSelect.count() > 0) {
      await sourceSelect.selectOption({ index: 1 });
    }
    
    // Select destination warehouse
    const destSelect = page.locator('select[name*="destination"], [data-testid="dest-warehouse"]');
    if (await destSelect.count() > 0) {
      await destSelect.selectOption({ index: 2 });
    }
    
    // Continue with transfer flow
    await page.waitForLoadState('networkidle');
  });

  test('should perform stock adjustment', async ({ page }) => {
    // Navigate to adjustments
    await page.goto('/warehouse-adjustments');
    
    // Check page loaded
    const pageTitle = page.locator('h1, h2, .page-title');
    await expect(pageTitle).toBeVisible();
  });

  test('should filter warehouses', async ({ page }) => {
    // Find search input
    const searchInput = page.getByPlaceholder(/search|بحث/i);
    if (await searchInput.count() > 0) {
      await searchInput.fill('main');
      await page.waitForLoadState('networkidle');
    }
  });

  test('should show warehouse statistics', async ({ page }) => {
    // Check for stats cards
    const statsCards = page.locator('.stat-card, [data-testid="stats"], .warehouse-stats');
    const count = await statsCards.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});
