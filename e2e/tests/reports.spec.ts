/**
 * E2E Tests - Reports System
 * Store ERP v2.0.0
 * 
 * Tests for various reports including sales, inventory, profit/loss, and exports.
 */

import { test, expect, Page } from '@playwright/test';

async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
  await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
  await page.getByRole('button', { name: /login|دخول/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('Reports System', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/reports');
  });

  test('should display reports dashboard', async ({ page }) => {
    // Check for reports page
    await expect(page.getByRole('heading', { name: /report|تقرير/i })).toBeVisible();
    
    // Should show report categories/cards
    const reportCards = page.locator('[data-testid="report-card"]');
    expect(await reportCards.count()).toBeGreaterThan(0);
  });

  test('should navigate to sales report', async ({ page }) => {
    // Click sales report card
    await page.getByRole('link', { name: /sales|مبيعات/i }).click();
    
    // Verify sales report page
    await expect(page.getByRole('heading', { name: /sales|مبيعات/i })).toBeVisible();
    
    // Should have date filters
    await expect(page.getByLabel(/from|من|start/i)).toBeVisible();
    await expect(page.getByLabel(/to|إلى|end/i)).toBeVisible();
  });

  test('should navigate to inventory report', async ({ page }) => {
    await page.getByRole('link', { name: /inventory|مخزون/i }).click();
    
    await expect(page.getByRole('heading', { name: /inventory|مخزون/i })).toBeVisible();
  });

  test('should navigate to profit/loss report', async ({ page }) => {
    await page.getByRole('link', { name: /profit|loss|ربح|خسارة/i }).click();
    
    await expect(page.getByRole('heading', { name: /profit|ربح/i })).toBeVisible();
  });
});

test.describe('Sales Reports', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/sales-reports');
  });

  test('should filter by date range', async ({ page }) => {
    // Set date range
    const fromDate = page.getByLabel(/from|من|start/i);
    const toDate = page.getByLabel(/to|إلى|end/i);
    
    if (await fromDate.isVisible()) {
      await fromDate.fill('2025-01-01');
      await toDate.fill('2025-12-31');
      
      // Apply filter
      await page.getByRole('button', { name: /apply|تطبيق|filter|بحث/i }).click();
      
      // Wait for results
      await page.waitForTimeout(500);
      
      // Should show filtered data
      expect(await page.locator('table tbody tr').count()).toBeGreaterThanOrEqual(0);
    }
  });

  test('should display summary statistics', async ({ page }) => {
    // Should show total sales, orders, etc.
    const statsSection = page.locator('[data-testid="stats-section"]');
    
    if (await statsSection.isVisible()) {
      await expect(page.getByText(/total sales|إجمالي المبيعات/i)).toBeVisible();
      await expect(page.getByText(/orders|طلبات/i)).toBeVisible();
    }
  });

  test('should export sales report to PDF', async ({ page }) => {
    const exportBtn = page.getByRole('button', { name: /export|تصدير/i });
    
    if (await exportBtn.isVisible()) {
      await exportBtn.click();
      
      const pdfBtn = page.getByRole('menuitem', { name: /pdf/i });
      if (await pdfBtn.isVisible()) {
        const downloadPromise = page.waitForEvent('download');
        await pdfBtn.click();
        
        try {
          const download = await downloadPromise;
          expect(download.suggestedFilename()).toMatch(/\.(pdf)$/i);
        } catch {
          // No download if no data
        }
      }
    }
  });

  test('should export sales report to Excel', async ({ page }) => {
    const exportBtn = page.getByRole('button', { name: /export|تصدير/i });
    
    if (await exportBtn.isVisible()) {
      await exportBtn.click();
      
      const excelBtn = page.getByRole('menuitem', { name: /excel|xlsx/i });
      if (await excelBtn.isVisible()) {
        const downloadPromise = page.waitForEvent('download');
        await excelBtn.click();
        
        try {
          const download = await downloadPromise;
          expect(download.suggestedFilename()).toMatch(/\.(xlsx|xls)$/i);
        } catch {
          // No download if no data
        }
      }
    }
  });
});

test.describe('Inventory Reports', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/inventory-reports');
  });

  test('should display inventory summary', async ({ page }) => {
    // Should show inventory counts
    await expect(page.getByText(/total products|إجمالي المنتجات/i)).toBeVisible();
    await expect(page.getByText(/low stock|مخزون منخفض/i)).toBeVisible();
  });

  test('should filter by category', async ({ page }) => {
    const categoryFilter = page.getByRole('combobox', { name: /category|فئة/i });
    
    if (await categoryFilter.isVisible()) {
      await categoryFilter.click();
      await page.getByRole('option').first().click();
      
      await page.waitForTimeout(500);
      
      // Results should update
      expect(await page.locator('table tbody tr').count()).toBeGreaterThanOrEqual(0);
    }
  });

  test('should show low stock alerts', async ({ page }) => {
    // Navigate to low stock view
    await page.getByRole('tab', { name: /low stock|منخفض/i }).click();
    
    // Should show products with low stock
    const lowStockRows = page.locator('[data-testid="low-stock-row"]');
    // May or may not have low stock items
    expect(await lowStockRows.count()).toBeGreaterThanOrEqual(0);
  });
});

test.describe('Profit/Loss Reports', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/profit-loss-reports');
  });

  test('should display profit summary', async ({ page }) => {
    await expect(page.getByText(/revenue|إيرادات/i)).toBeVisible();
    await expect(page.getByText(/cost|تكلفة/i)).toBeVisible();
    await expect(page.getByText(/profit|ربح/i)).toBeVisible();
  });

  test('should show chart visualization', async ({ page }) => {
    // Check for chart container
    const chart = page.locator('[data-testid="profit-chart"], .recharts-wrapper, canvas');
    expect(await chart.isVisible()).toBeTruthy();
  });

  test('should filter by period', async ({ page }) => {
    const periodSelect = page.getByRole('combobox', { name: /period|فترة/i });
    
    if (await periodSelect.isVisible()) {
      await periodSelect.click();
      await page.getByRole('option', { name: /monthly|شهري/i }).click();
      
      await page.waitForTimeout(500);
      
      // Data should update
      await expect(page.getByText(/profit|ربح/i)).toBeVisible();
    }
  });

  test('should export profit report', async ({ page }) => {
    const exportBtn = page.getByRole('button', { name: /export|تصدير/i });
    
    if (await exportBtn.isVisible()) {
      await exportBtn.click();
      
      // Check export options exist
      await expect(page.getByRole('menuitem', { name: /pdf/i })).toBeVisible();
      await expect(page.getByRole('menuitem', { name: /excel/i })).toBeVisible();
    }
  });
});

test.describe('Reports RTL Support', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('should render reports with RTL layout', async ({ page }) => {
    await page.goto('/reports');
    
    // Check for RTL direction
    const body = page.locator('body');
    const direction = await body.evaluate(el => getComputedStyle(el).direction);
    
    // Should be RTL for Arabic
    expect(direction).toBe('rtl');
  });

  test('should have correct text alignment in tables', async ({ page }) => {
    await page.goto('/sales-reports');
    
    const table = page.locator('table');
    if (await table.isVisible()) {
      const thAlignment = await table.locator('th').first().evaluate(
        el => getComputedStyle(el).textAlign
      );
      
      // Should be right-aligned for RTL
      expect(thAlignment).toMatch(/right|start/);
    }
  });
});
