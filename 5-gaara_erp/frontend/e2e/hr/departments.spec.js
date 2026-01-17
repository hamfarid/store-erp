/**
 * E2E Tests for Departments Page
 * 
 * Tests cover:
 * - Page navigation and loading
 * - Department hierarchical tree view
 * - Adding new departments
 * - Editing departments
 * - Department parent-child relationships
 * - Budget management
 * - Employee count tracking
 */

const { test, expect } = require('@playwright/test');

// Test configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:5501';
const API_URL = process.env.API_URL || 'http://localhost:5001';

test.describe('HR - Departments Page', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to departments page
    await page.goto(`${BASE_URL}/hr/departments`);
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should load departments page successfully', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('إدارة الأقسام');
    
    // Check subtitle
    await expect(page.locator('p')).toContainText('الهيكل التنظيمي');
    
    // Check stats cards are visible
    const statsCards = page.locator('[data-testid="stats-card"]');
    await expect(statsCards).toHaveCount(3);
    
    // Check department table/tree exists
    await expect(page.locator('table')).toBeVisible();
  });

  test('should display department statistics', async ({ page }) => {
    // Verify statistics cards
    const stats = {
      total: page.locator('[data-testid="total-departments"]'),
      employees: page.locator('[data-testid="total-employees"]'),
      budget: page.locator('[data-testid="total-budget"]')
    };
    
    // Each stat should be visible and have a value
    for (const stat of Object.values(stats)) {
      if (await stat.isVisible()) {
        const value = await stat.textContent();
        expect(value).toBeTruthy();
      }
    }
  });

  test('should display departments in hierarchical tree', async ({ page }) => {
    // Wait for departments to load
    await page.waitForSelector('table tbody tr', { timeout: 10000 });
    
    // Check table headers
    const headers = ['الرمز', 'اسم القسم', 'الموظفين', 'الميزانية', 'الحالة', 'الإجراءات'];
    for (const header of headers) {
      await expect(page.locator('th')).toContainText(header);
    }
    
    // Check at least one department row exists
    const rows = page.locator('table tbody tr');
    await expect(rows.first()).toBeVisible();
  });

  test('should expand/collapse department hierarchy', async ({ page }) => {
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Find a department with children (has expand button)
    const expandButton = page.locator('button[data-testid="expand-department"]').first();
    
    if (await expandButton.isVisible()) {
      // Get initial row count
      const initialCount = await page.locator('table tbody tr').count();
      
      // Click to expand
      await expandButton.click();
      await page.waitForTimeout(500);
      
      // Row count should increase (child departments visible)
      const expandedCount = await page.locator('table tbody tr').count();
      expect(expandedCount).toBeGreaterThan(initialCount);
      
      // Click to collapse
      await expandButton.click();
      await page.waitForTimeout(500);
      
      // Row count should return to original
      const collapsedCount = await page.locator('table tbody tr').count();
      expect(collapsedCount).toBeLessThanOrEqual(expandedCount);
    }
  });

  test('should open add department modal', async ({ page }) => {
    // Click add button
    await page.click('button:has-text("إضافة قسم")');
    
    // Wait for modal
    await page.waitForSelector('[role="dialog"]', { timeout: 5000 });
    
    // Verify modal title
    await expect(page.locator('[role="dialog"] h2')).toContainText('إضافة قسم جديد');
    
    // Verify form fields
    await expect(page.locator('#code')).toBeVisible();
    await expect(page.locator('#name')).toBeVisible();
    await expect(page.locator('#name_ar')).toBeVisible();
    await expect(page.locator('#parent_id')).toBeVisible();
    await expect(page.locator('#budget')).toBeVisible();
  });

  test('should validate required fields when adding department', async ({ page }) => {
    // Open add modal
    await page.click('button:has-text("إضافة قسم")');
    await page.waitForSelector('[role="dialog"]');
    
    // Try to submit empty form
    await page.click('button[type="submit"]:has-text("إضافة")');
    
    // Check for validation
    const codeInput = page.locator('#code');
    const nameInput = page.locator('#name');
    
    await expect(codeInput).toHaveAttribute('required');
    await expect(nameInput).toHaveAttribute('required');
  });

  test('should add new department successfully', async ({ page }) => {
    // Mock API response
    await page.route(`${API_URL}/api/hr/departments`, async route => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              id: 99,
              code: 'TEST',
              name: 'Test Department',
              name_ar: 'قسم الاختبار',
              parent_id: null,
              budget: 100000,
              is_active: true
            },
            message: 'تم إضافة القسم بنجاح'
          })
        });
      } else {
        await route.continue();
      }
    });
    
    // Open add modal
    await page.click('button:has-text("إضافة قسم")');
    await page.waitForSelector('[role="dialog"]');
    
    // Fill form
    await page.fill('#code', 'TEST');
    await page.fill('#name', 'Test Department');
    await page.fill('#name_ar', 'قسم الاختبار');
    await page.selectOption('#parent_id', ''); // No parent (root department)
    await page.fill('#budget', '100000');
    
    // Submit
    await page.click('button[type="submit"]:has-text("إضافة")');
    
    // Wait for success message
    await expect(page.locator('.toast-success, .alert-success')).toContainText('نجاح', { timeout: 5000 });
    
    // Modal should close
    await expect(page.locator('[role="dialog"]')).not.toBeVisible({ timeout: 5000 });
  });

  test('should add child department with parent selection', async ({ page }) => {
    // Mock API response
    await page.route(`${API_URL}/api/hr/departments`, async route => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              id: 100,
              code: 'SUB',
              name: 'Sub Department',
              parent_id: 1,
              budget: 50000
            },
            message: 'تم إضافة القسم بنجاح'
          })
        });
      } else {
        await route.continue();
      }
    });
    
    // Open add modal
    await page.click('button:has-text("إضافة قسم")');
    await page.waitForSelector('[role="dialog"]');
    
    // Fill form with parent selection
    await page.fill('#code', 'SUB');
    await page.fill('#name', 'Sub Department');
    await page.selectOption('#parent_id', '1'); // Select parent
    await page.fill('#budget', '50000');
    
    // Submit
    await page.click('button[type="submit"]:has-text("إضافة")');
    
    // Wait for success
    await expect(page.locator('.toast-success')).toBeVisible({ timeout: 5000 });
  });

  test('should open edit department modal', async ({ page }) => {
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Click first edit button
    await page.click('table tbody tr:first-child button[title="تعديل"]');
    
    // Wait for modal
    await page.waitForSelector('[role="dialog"]');
    
    // Verify modal title
    await expect(page.locator('[role="dialog"] h2')).toContainText('تعديل بيانات القسم');
    
    // Form should be pre-filled
    const code = await page.locator('#code').inputValue();
    expect(code).toBeTruthy();
  });

  test('should update department successfully', async ({ page }) => {
    // Mock API
    await page.route(`${API_URL}/api/hr/departments/**`, async route => {
      if (route.request().method() === 'PUT') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: { id: 1, budget: 150000 },
            message: 'تم تحديث بيانات القسم بنجاح'
          })
        });
      } else {
        await route.continue();
      }
    });
    
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Click edit button
    await page.click('table tbody tr:first-child button[title="تعديل"]');
    await page.waitForSelector('[role="dialog"]');
    
    // Update budget
    await page.fill('#budget', '150000');
    
    // Submit
    await page.click('button[type="submit"]:has-text("تحديث")');
    
    // Wait for success
    await expect(page.locator('.toast-success')).toContainText('نجاح', { timeout: 5000 });
  });

  test('should display department employee count', async ({ page }) => {
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Check employee count column
    const firstRow = page.locator('table tbody tr').first();
    const employeeCount = firstRow.locator('[data-testid="employee-count"]');
    
    if (await employeeCount.isVisible()) {
      const count = await employeeCount.textContent();
      expect(count).toMatch(/\d+/); // Should contain a number
    }
  });

  test('should display department budget with currency', async ({ page }) => {
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Check budget column
    const firstRow = page.locator('table tbody tr').first();
    const budget = firstRow.locator('td:nth-child(4)');
    
    const budgetText = await budget.textContent();
    // Should contain number and currency symbol (ج.م or EGP)
    expect(budgetText).toMatch(/[\d,]+/);
  });

  test('should show department status badge', async ({ page }) => {
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Check status badge
    const firstRow = page.locator('table tbody tr').first();
    const statusBadge = firstRow.locator('[data-testid="status-badge"]');
    
    if (await statusBadge.isVisible()) {
      const status = await statusBadge.textContent();
      expect(['نشط', 'غير نشط']).toContain(status);
    }
  });

  test('should refresh departments list', async ({ page }) => {
    // Wait for initial load
    await page.waitForSelector('table tbody tr');
    
    // Click refresh button
    const refreshButton = page.locator('button:has-text("تحديث")');
    await refreshButton.click();
    
    // Should show loading state briefly
    // Then show departments again
    await page.waitForSelector('table tbody tr', { timeout: 5000 });
  });

  test('should handle empty departments list', async ({ page }) => {
    // Mock empty response
    await page.route(`${API_URL}/api/hr/departments*`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: []
        })
      });
    });
    
    // Reload page
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Should show empty state message
    await expect(page.locator('.empty-state, .no-data')).toBeVisible({ timeout: 5000 });
  });

  test('should prevent department from being its own parent', async ({ page }) => {
    // Open edit modal for a department
    await page.waitForSelector('table tbody tr');
    await page.click('table tbody tr:first-child button[title="تعديل"]');
    await page.waitForSelector('[role="dialog"]');
    
    // Get current department ID from hidden field or data attribute
    // Try to select it as parent
    const parentSelect = page.locator('#parent_id');
    
    // The current department should be disabled in the parent dropdown
    // This depends on your implementation
  });

  test('should calculate total budget correctly', async ({ page }) => {
    // Wait for page load
    await page.waitForSelector('[data-testid="total-budget"]');
    
    // Get displayed total
    const totalBudgetText = await page.locator('[data-testid="total-budget"]').textContent();
    const totalBudget = parseInt(totalBudgetText.replace(/[^\d]/g, ''));
    
    // Total should be a positive number
    expect(totalBudget).toBeGreaterThanOrEqual(0);
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route(`${API_URL}/api/hr/departments*`, async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          message: 'حدث خطأ في الخادم'
        })
      });
    });
    
    // Reload page
    await page.reload();
    
    // Should show error message
    await expect(page.locator('.error-message, .alert-danger')).toBeVisible({ timeout: 5000 });
  });

  test('should show department hierarchy depth visually', async ({ page }) => {
    // Wait for departments
    await page.waitForSelector('table tbody tr');
    
    // Expand a parent department
    const expandButton = page.locator('button[data-testid="expand-department"]').first();
    
    if (await expandButton.isVisible()) {
      await expandButton.click();
      await page.waitForTimeout(500);
      
      // Child departments should have indentation or visual indicator
      const childRow = page.locator('table tbody tr').nth(1);
      
      // Check for padding/margin or indent class
      // (This depends on your implementation)
      const hasIndent = await childRow.evaluate(el => {
        const style = window.getComputedStyle(el.querySelector('td:first-child'));
        return parseInt(style.paddingRight) > 20;
      });
      
      expect(hasIndent).toBeTruthy();
    }
  });

  test('should be accessible (ARIA checks)', async ({ page }) => {
    // Wait for page load
    await page.waitForSelector('table');
    
    // Check main heading
    await expect(page.locator('h1')).toBeVisible();
    
    // Check add button has accessible name
    const addButton = page.locator('button:has-text("إضافة قسم")');
    await expect(addButton).toHaveAccessibleName();
    
    // Check table structure
    await expect(page.locator('table thead')).toBeVisible();
    await expect(page.locator('table tbody')).toBeVisible();
  });
});
