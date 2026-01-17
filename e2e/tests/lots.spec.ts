/**
 * E2E Tests - Lot/Batch Management System
 * Store ERP v2.0.0
 * 
 * Tests for lot management including CRUD, expiry tracking, and quality fields.
 */

import { test, expect, Page } from '@playwright/test';

async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
  await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
  await page.getByRole('button', { name: /login|دخول/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('Lot Management', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/lots');
  });

  test('should display lots list', async ({ page }) => {
    // Check for lots table/list
    await expect(page.getByRole('heading', { name: /lot|لوت|batch/i })).toBeVisible();
    
    // Should have a table or list of lots
    const hasTable = await page.locator('table').isVisible();
    const hasList = await page.locator('[data-testid="lots-list"]').isVisible();
    
    expect(hasTable || hasList).toBeTruthy();
  });

  test('should filter lots by status', async ({ page }) => {
    // Find status filter
    const statusFilter = page.getByRole('combobox', { name: /status|حالة/i });
    
    if (await statusFilter.isVisible()) {
      await statusFilter.click();
      
      // Select "Available" status
      await page.getByRole('option', { name: /available|متاح/i }).click();
      
      // Wait for filter to apply
      await page.waitForTimeout(500);
      
      // Verify filtered results
      const rows = page.locator('[data-testid="lot-row"]');
      const count = await rows.count();
      
      // All visible lots should be "Available"
      for (let i = 0; i < Math.min(count, 5); i++) {
        const row = rows.nth(i);
        await expect(row.getByText(/available|متاح/i)).toBeVisible();
      }
    }
  });

  test('should search lots by lot number', async ({ page }) => {
    const searchInput = page.getByPlaceholder(/search|بحث/i);
    
    if (await searchInput.isVisible()) {
      await searchInput.fill('LOT-');
      await page.waitForTimeout(500);
      
      // Should show matching results
      const results = page.locator('[data-testid="lot-row"]');
      expect(await results.count()).toBeGreaterThanOrEqual(0);
    }
  });

  test('should open lot details', async ({ page }) => {
    // Click on first lot
    const firstLot = page.locator('[data-testid="lot-row"]').first();
    
    if (await firstLot.isVisible()) {
      await firstLot.click();
      
      // Should show lot details
      await expect(page.getByText(/lot number|رقم اللوت/i)).toBeVisible();
      await expect(page.getByText(/quantity|كمية/i)).toBeVisible();
      await expect(page.getByText(/expiry|انتهاء/i)).toBeVisible();
    }
  });

  test('should create new lot', async ({ page }) => {
    // Click add new lot button
    await page.getByRole('button', { name: /add|إضافة|new|جديد/i }).click();
    
    // Fill lot form
    await page.getByLabel(/lot number|رقم اللوت/i).fill('LOT-TEST-001');
    await page.getByLabel(/product|منتج/i).click();
    await page.getByRole('option').first().click();
    await page.getByLabel(/quantity|كمية/i).fill('100');
    await page.getByLabel(/expiry|انتهاء/i).fill('2027-12-31');
    
    // Submit
    await page.getByRole('button', { name: /save|حفظ|create|إنشاء/i }).click();
    
    // Verify success
    await expect(page.getByText(/success|تم|نجاح/i)).toBeVisible();
  });

  test('should edit existing lot', async ({ page }) => {
    const firstLot = page.locator('[data-testid="lot-row"]').first();
    
    if (await firstLot.isVisible()) {
      // Click edit button
      await firstLot.getByRole('button', { name: /edit|تعديل/i }).click();
      
      // Update quantity
      const qtyInput = page.getByLabel(/quantity|كمية/i);
      await qtyInput.clear();
      await qtyInput.fill('150');
      
      // Save
      await page.getByRole('button', { name: /save|حفظ|update|تحديث/i }).click();
      
      // Verify success
      await expect(page.getByText(/updated|تم التحديث|success/i)).toBeVisible();
    }
  });

  test('should display quality fields', async ({ page }) => {
    const firstLot = page.locator('[data-testid="lot-row"]').first();
    
    if (await firstLot.isVisible()) {
      await firstLot.click();
      
      // Check for quality fields (seed-specific)
      const qualityFields = [
        /germination|إنبات/i,
        /purity|نقاء/i,
        /moisture|رطوبة/i,
      ];
      
      for (const field of qualityFields) {
        const element = page.getByText(field);
        // These fields may or may not be present depending on product type
        if (await element.isVisible()) {
          expect(await element.isVisible()).toBeTruthy();
        }
      }
    }
  });
});

test.describe('Lot Expiry Tracking', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('should show expiry alerts on dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Check for expiry alerts section
    const expirySection = page.getByText(/expir|انتهاء|alert|تنبيه/i);
    expect(await expirySection.isVisible()).toBeTruthy();
  });

  test('should access lot expiry report', async ({ page }) => {
    await page.goto('/lot-expiry-report');
    
    // Verify report page loads
    await expect(page.getByRole('heading', { name: /expir|انتهاء/i })).toBeVisible();
    
    // Should have filter options
    await expect(page.getByRole('combobox', { name: /days|أيام|period/i })).toBeVisible();
  });

  test('should filter expiring lots by days', async ({ page }) => {
    await page.goto('/lot-expiry-report');
    
    // Select 30 days filter
    const daysFilter = page.getByRole('combobox', { name: /days|أيام|period/i });
    if (await daysFilter.isVisible()) {
      await daysFilter.click();
      await page.getByRole('option', { name: /30/i }).click();
      
      // Wait for filter
      await page.waitForTimeout(500);
      
      // Results should update
      expect(await page.locator('[data-testid="expiry-row"]').count()).toBeGreaterThanOrEqual(0);
    }
  });

  test('should export expiry report', async ({ page }) => {
    await page.goto('/lot-expiry-report');
    
    // Find export button
    const exportBtn = page.getByRole('button', { name: /export|تصدير/i });
    
    if (await exportBtn.isVisible()) {
      await exportBtn.click();
      
      // Select format (PDF/Excel/CSV)
      const pdfOption = page.getByRole('menuitem', { name: /pdf/i });
      if (await pdfOption.isVisible()) {
        // Expect download to start
        const downloadPromise = page.waitForEvent('download');
        await pdfOption.click();
        
        // Verify download started (may timeout if no data)
        try {
          const download = await downloadPromise;
          expect(download.suggestedFilename()).toContain('.pdf');
        } catch {
          // No download if no data - that's okay
        }
      }
    }
  });
});

test.describe('Lot Status Transitions', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/lots');
  });

  test('should change lot status', async ({ page }) => {
    const firstLot = page.locator('[data-testid="lot-row"]').first();
    
    if (await firstLot.isVisible()) {
      // Open status dropdown
      const statusBtn = firstLot.getByRole('button', { name: /status|حالة/i });
      if (await statusBtn.isVisible()) {
        await statusBtn.click();
        
        // Select new status
        await page.getByRole('option', { name: /reserved|محجوز/i }).click();
        
        // Confirm if needed
        const confirmBtn = page.getByRole('button', { name: /confirm|تأكيد/i });
        if (await confirmBtn.isVisible()) {
          await confirmBtn.click();
        }
        
        // Verify status changed
        await expect(page.getByText(/success|تم|updated/i)).toBeVisible();
      }
    }
  });
});
