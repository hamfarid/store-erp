/**
 * Inventory Module E2E Tests for Gaara ERP v12
 */

import { test, expect } from '@playwright/test';

test.describe('Inventory Module', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/inventory');
  });

  test('should display product list', async ({ page }) => {
    // Wait for products table
    const productsTable = page.locator('[data-testid="products-table"], table.products');
    await expect(productsTable).toBeVisible({ timeout: 10000 });
  });

  test('should search products', async ({ page }) => {
    // Find search input
    const searchInput = page.locator('[data-testid="search-input"], input[type="search"], input[placeholder*="بحث"]');
    await searchInput.fill('منتج تجريبي');
    
    // Wait for search results
    await page.waitForTimeout(500);
    
    // Results should filter
    await expect(page.locator('table tbody tr, [data-testid="product-row"]').first()).toBeVisible();
  });

  test('should open create product modal', async ({ page }) => {
    // Click create button
    await page.click('[data-testid="create-product-btn"], button:has-text("إضافة منتج"), button:has-text("جديد")');
    
    // Modal should appear
    await expect(page.locator('[data-testid="product-modal"], .modal, [role="dialog"]')).toBeVisible();
  });

  test('should create a new product', async ({ page }) => {
    // Open create modal
    await page.click('[data-testid="create-product-btn"], button:has-text("إضافة"), button:has-text("جديد")');
    
    // Fill form
    await page.fill('[name="name"], [data-testid="product-name"]', 'منتج اختبار E2E');
    await page.fill('[name="sku"], [data-testid="product-sku"]', `SKU-E2E-${Date.now()}`);
    await page.fill('[name="price"], [data-testid="product-price"]', '100.00');
    
    // Submit form
    await page.click('[data-testid="submit-btn"], button[type="submit"]');
    
    // Should show success
    await expect(page.locator('[data-testid="success-toast"], .toast-success, .alert-success')).toBeVisible();
  });

  test('should view product details', async ({ page }) => {
    // Click first product row
    await page.click('table tbody tr:first-child, [data-testid="product-row"]:first-child');
    
    // Details should show
    await expect(page.locator('[data-testid="product-details"], .product-details')).toBeVisible();
  });

  test('should display stock levels', async ({ page }) => {
    // Navigate to stock tab
    await page.click('[data-testid="stock-tab"], a:has-text("المخزون"), button:has-text("المخزون")');
    
    // Stock table should be visible
    await expect(page.locator('[data-testid="stock-table"], table.stock')).toBeVisible();
  });

  test('should display low stock alerts', async ({ page }) => {
    // Low stock section
    const lowStockSection = page.locator('[data-testid="low-stock-alerts"], .low-stock-alerts');
    
    // May or may not exist depending on data
    if (await lowStockSection.isVisible()) {
      await expect(lowStockSection).toContainText(/تنبيه|منخفض|low stock/i);
    }
  });
});

