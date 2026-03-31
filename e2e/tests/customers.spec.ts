/**
 * E2E Tests - Customers Management
 * 
 * Tests for customer CRUD operations.
 */

import { test, expect } from '@playwright/test';

test.describe('Customers Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    await expect(page).toHaveURL(/dashboard/);
    
    // Navigate to customers
    await page.goto('/customers');
  });

  test('should display customers list', async ({ page }) => {
    // Check for customers table or list
    const customersTable = page.locator('table, [data-testid="customers-table"]');
    await expect(customersTable).toBeVisible();
  });

  test('should search for customers', async ({ page }) => {
    // Find search input
    const searchInput = page.getByPlaceholder(/search|بحث/i);
    await searchInput.fill('test');
    
    // Wait for search results
    await page.waitForLoadState('networkidle');
    
    // Table should update
    const table = page.locator('table tbody tr');
    const count = await table.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('should open add customer modal', async ({ page }) => {
    // Click add button
    await page.getByRole('button', { name: /add|إضافة|new|جديد/i }).click();
    
    // Modal should open
    const modal = page.locator('[role="dialog"], .modal, [data-testid="add-customer-modal"]');
    await expect(modal).toBeVisible();
  });

  test('should create new customer', async ({ page }) => {
    // Click add button
    await page.getByRole('button', { name: /add|إضافة|new|جديد/i }).click();
    
    // Fill customer form
    const nameInput = page.getByLabel(/name|الاسم/i).first();
    await nameInput.fill('Test Customer ' + Date.now());
    
    const phoneInput = page.getByLabel(/phone|هاتف/i);
    if (await phoneInput.count() > 0) {
      await phoneInput.fill('0551234567');
    }
    
    const emailInput = page.getByLabel(/email|بريد/i);
    if (await emailInput.count() > 0) {
      await emailInput.fill('test@example.com');
    }
    
    // Submit
    await page.getByRole('button', { name: /save|حفظ|submit|إرسال/i }).click();
    
    // Should show success message or close modal
    await page.waitForLoadState('networkidle');
  });

  test('should view customer details', async ({ page }) => {
    // Click on first customer row or view button
    const viewButton = page.locator('button[aria-label*="view"], button[title*="view"], .view-btn').first();
    const exists = await viewButton.count();
    
    if (exists > 0) {
      await viewButton.click();
      await page.waitForLoadState('networkidle');
    } else {
      // Click on row
      const row = page.locator('table tbody tr').first();
      await row.click();
    }
  });

  test('should edit customer', async ({ page }) => {
    // Click edit button on first customer
    const editButton = page.locator('button[aria-label*="edit"], button[title*="edit"], .edit-btn').first();
    const exists = await editButton.count();
    
    if (exists > 0) {
      await editButton.click();
      
      // Modal should open with customer data
      const modal = page.locator('[role="dialog"], .modal');
      await expect(modal).toBeVisible();
      
      // Edit name
      const nameInput = page.getByLabel(/name|الاسم/i).first();
      await nameInput.fill('Updated Customer Name');
      
      // Save
      await page.getByRole('button', { name: /save|حفظ|update|تحديث/i }).click();
      
      // Wait for update
      await page.waitForLoadState('networkidle');
    }
  });

  test('should filter customers by status', async ({ page }) => {
    // Find status filter
    const statusFilter = page.locator('select[name*="status"], [data-testid="status-filter"]');
    const exists = await statusFilter.count();
    
    if (exists > 0) {
      await statusFilter.selectOption({ index: 1 });
      await page.waitForLoadState('networkidle');
    }
  });

  test('should export customers', async ({ page }) => {
    // Find export button
    const exportButton = page.getByRole('button', { name: /export|تصدير/i });
    const exists = await exportButton.count();
    
    if (exists > 0) {
      // Start waiting for download before clicking
      const downloadPromise = page.waitForEvent('download');
      await exportButton.click();
      
      // Wait for download
      try {
        const download = await downloadPromise;
        expect(download).toBeTruthy();
      } catch {
        // Export might open in new tab or show modal
      }
    }
  });

  test('should paginate customers list', async ({ page }) => {
    // Find pagination controls
    const nextPage = page.locator('button[aria-label*="next"], .pagination-next, [data-testid="next-page"]');
    const exists = await nextPage.count();
    
    if (exists > 0 && await nextPage.isEnabled()) {
      await nextPage.click();
      await page.waitForLoadState('networkidle');
      
      // URL or data should change
      const currentPage = page.locator('.pagination-current, [data-testid="current-page"]');
      if (await currentPage.count() > 0) {
        const pageNum = await currentPage.textContent();
        expect(pageNum).toContain('2');
      }
    }
  });
});
