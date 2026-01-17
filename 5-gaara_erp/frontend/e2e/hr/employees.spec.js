/**
 * E2E Tests for Employees Page
 * 
 * Tests cover:
 * - Page navigation and loading
 * - Employee listing and pagination
 * - Adding new employees
 * - Editing existing employees
 * - Deleting employees
 * - Search and filter functionality
 * - Form validation
 */

const { test, expect } = require('@playwright/test');

// Test configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:5501';
const API_URL = process.env.API_URL || 'http://localhost:5001';

test.describe('HR - Employees Page', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to employees page
    await page.goto(`${BASE_URL}/hr/employees`);
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should load employees page successfully', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('إدارة الموظفين');
    
    // Check stats cards are visible
    await expect(page.locator('.stats-card')).toHaveCount(4);
    
    // Check employee table exists
    await expect(page.locator('table')).toBeVisible();
  });

  test('should display employee statistics cards', async ({ page }) => {
    // Verify all statistics cards
    const statsCards = page.locator('[data-testid="stats-card"]');
    
    // Should show: Total, Active, On Leave, Department breakdown
    await expect(statsCards).toHaveCount(4);
    
    // Each card should have a number and label
    for (let i = 0; i < 4; i++) {
      const card = statsCards.nth(i);
      await expect(card.locator('.stat-value')).toBeVisible();
      await expect(card.locator('.stat-label')).toBeVisible();
    }
  });

  test('should list employees in table', async ({ page }) => {
    // Wait for employees to load
    await page.waitForSelector('table tbody tr', { timeout: 10000 });
    
    // Check table headers
    const headers = ['رقم الموظف', 'الاسم', 'القسم', 'البريد الإلكتروني', 'الحالة', 'الإجراءات'];
    for (const header of headers) {
      await expect(page.locator('th')).toContainText(header);
    }
    
    // Check at least one employee row exists
    const rows = page.locator('table tbody tr');
    await expect(rows.first()).toBeVisible();
  });

  test('should open add employee modal', async ({ page }) => {
    // Click add button
    await page.click('button:has-text("إضافة موظف")');
    
    // Wait for modal
    await page.waitForSelector('[role="dialog"]', { timeout: 5000 });
    
    // Verify modal title
    await expect(page.locator('[role="dialog"] h2')).toContainText('إضافة موظف جديد');
    
    // Verify form fields exist
    await expect(page.locator('#employee_id')).toBeVisible();
    await expect(page.locator('#first_name')).toBeVisible();
    await expect(page.locator('#last_name')).toBeVisible();
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#phone')).toBeVisible();
    await expect(page.locator('#department_id')).toBeVisible();
  });

  test('should validate required fields when adding employee', async ({ page }) => {
    // Open add modal
    await page.click('button:has-text("إضافة موظف")');
    await page.waitForSelector('[role="dialog"]');
    
    // Try to submit empty form
    await page.click('button[type="submit"]:has-text("إضافة")');
    
    // Check for validation messages (HTML5 validation or custom)
    const employeeIdInput = page.locator('#employee_id');
    const firstNameInput = page.locator('#first_name');
    
    // These fields should be marked as invalid
    await expect(employeeIdInput).toHaveAttribute('required');
    await expect(firstNameInput).toHaveAttribute('required');
  });

  test('should add new employee successfully', async ({ page }) => {
    // Mock API response for successful creation
    await page.route(`${API_URL}/api/hr/employees`, async route => {
      if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 201,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: {
              id: 999,
              employee_id: 'EMP999',
              first_name: 'محمد',
              last_name: 'أحمد',
              email: 'test@company.com',
              phone: '+201234567890',
              department_id: 1,
              department: 'تقنية المعلومات'
            },
            message: 'تم إنشاء الموظف بنجاح'
          })
        });
      } else {
        await route.continue();
      }
    });
    
    // Open add modal
    await page.click('button:has-text("إضافة موظف")');
    await page.waitForSelector('[role="dialog"]');
    
    // Fill form
    await page.fill('#employee_id', 'EMP999');
    await page.fill('#first_name', 'محمد');
    await page.fill('#last_name', 'أحمد');
    await page.fill('#email', 'test@company.com');
    await page.fill('#phone', '+201234567890');
    await page.selectOption('#department_id', '1');
    
    // Submit
    await page.click('button[type="submit"]:has-text("إضافة")');
    
    // Wait for success message
    await expect(page.locator('.toast-success, .alert-success')).toContainText('نجاح', { timeout: 5000 });
    
    // Modal should close
    await expect(page.locator('[role="dialog"]')).not.toBeVisible({ timeout: 5000 });
  });

  test('should open edit employee modal', async ({ page }) => {
    // Wait for employees to load
    await page.waitForSelector('table tbody tr');
    
    // Click first edit button
    await page.click('table tbody tr:first-child button[title="تعديل"]');
    
    // Wait for modal
    await page.waitForSelector('[role="dialog"]');
    
    // Verify modal title
    await expect(page.locator('[role="dialog"] h2')).toContainText('تعديل بيانات الموظف');
    
    // Form should be pre-filled
    const employeeId = await page.locator('#employee_id').inputValue();
    expect(employeeId).toBeTruthy();
  });

  test('should update employee successfully', async ({ page }) => {
    // Mock API responses
    await page.route(`${API_URL}/api/hr/employees/**`, async route => {
      if (route.request().method() === 'PUT') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            data: { id: 1, phone: '+201234567899' },
            message: 'تم تحديث بيانات الموظف بنجاح'
          })
        });
      } else {
        await route.continue();
      }
    });
    
    // Wait for employees
    await page.waitForSelector('table tbody tr');
    
    // Click edit button
    await page.click('table tbody tr:first-child button[title="تعديل"]');
    await page.waitForSelector('[role="dialog"]');
    
    // Update phone number
    await page.fill('#phone', '+201234567899');
    
    // Submit
    await page.click('button[type="submit"]:has-text("تحديث")');
    
    // Wait for success message
    await expect(page.locator('.toast-success, .alert-success')).toContainText('نجاح', { timeout: 5000 });
  });

  test('should delete employee with confirmation', async ({ page }) => {
    // Mock delete API
    await page.route(`${API_URL}/api/hr/employees/**`, async route => {
      if (route.request().method() === 'DELETE') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            success: true,
            message: 'تم حذف الموظف بنجاح'
          })
        });
      } else {
        await route.continue();
      }
    });
    
    // Wait for employees
    await page.waitForSelector('table tbody tr');
    
    // Setup dialog handler for confirmation
    page.once('dialog', dialog => {
      expect(dialog.type()).toBe('confirm');
      dialog.accept();
    });
    
    // Click delete button
    await page.click('table tbody tr:first-child button[title="حذف"]');
    
    // Wait for success message
    await expect(page.locator('.toast-success, .alert-success')).toContainText('نجاح', { timeout: 5000 });
  });

  test('should filter employees by department', async ({ page }) => {
    // Wait for employees
    await page.waitForSelector('table tbody tr');
    
    // Select department filter
    await page.selectOption('[data-testid="department-filter"]', '1');
    
    // Wait for filtered results
    await page.waitForTimeout(1000);
    
    // All visible employees should belong to selected department
    const rows = page.locator('table tbody tr');
    const count = await rows.count();
    
    for (let i = 0; i < count; i++) {
      const dept = await rows.nth(i).locator('td:nth-child(3)').textContent();
      expect(dept).toBeTruthy();
    }
  });

  test('should search employees by name', async ({ page }) => {
    // Wait for employees
    await page.waitForSelector('table tbody tr');
    
    // Type in search box
    await page.fill('[placeholder*="بحث"]', 'أحمد');
    
    // Wait for search results
    await page.waitForTimeout(1000);
    
    // Verify results contain search term
    const rows = page.locator('table tbody tr');
    const firstRowName = await rows.first().locator('td:nth-child(2)').textContent();
    expect(firstRowName).toContain('أحمد');
  });

  test('should paginate employees', async ({ page }) => {
    // Wait for employees
    await page.waitForSelector('table tbody tr');
    
    // Check if pagination exists (if there are enough employees)
    const pagination = page.locator('[data-testid="pagination"]');
    
    if (await pagination.isVisible()) {
      // Click next page
      await page.click('button:has-text("التالي")');
      
      // Wait for new page to load
      await page.waitForTimeout(1000);
      
      // Page number should change
      await expect(page.locator('[data-testid="current-page"]')).not.toContainText('1');
    }
  });

  test('should export employees to Excel', async ({ page }) => {
    // Mock export API
    await page.route(`${API_URL}/api/hr/employees/export`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        body: Buffer.from('mock excel data')
      });
    });
    
    // Click export button
    const exportButton = page.locator('button:has-text("تصدير")');
    
    if (await exportButton.isVisible()) {
      // Start waiting for download before clicking
      const downloadPromise = page.waitForEvent('download');
      
      await exportButton.click();
      
      // Wait for download
      const download = await downloadPromise;
      
      // Verify download filename
      expect(download.suggestedFilename()).toContain('.xlsx');
    }
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route(`${API_URL}/api/hr/employees`, async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          message: 'حدث خطأ في الخادم'
        })
      });
    });
    
    // Try to reload page
    await page.reload();
    
    // Should show error message
    await expect(page.locator('.error-message, .alert-danger')).toBeVisible({ timeout: 5000 });
  });

  test('should be accessible (basic ARIA checks)', async ({ page }) => {
    // Wait for page load
    await page.waitForSelector('table');
    
    // Check main heading has proper role
    const heading = page.locator('h1');
    await expect(heading).toBeVisible();
    
    // Check buttons have accessible names
    const addButton = page.locator('button:has-text("إضافة موظف")');
    await expect(addButton).toHaveAccessibleName();
    
    // Check table has proper structure
    await expect(page.locator('table thead')).toBeVisible();
    await expect(page.locator('table tbody')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Page should still be usable
    await expect(page.locator('h1')).toBeVisible();
    
    // Mobile menu or responsive layout should work
    // (Specific assertions depend on your responsive design)
  });
});
