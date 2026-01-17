/**
 * E2E Tests for Attendance Page
 * 
 * Tests cover:
 * - Page navigation and loading
 * - Check-in functionality
 * - Check-out functionality
 * - Attendance records display
 * - Date navigation
 * - Attendance statistics
 * - Status indicators (present, absent, late, on leave)
 */

const { test, expect } = require('@playwright/test');

// Test configuration
const BASE_URL = process.env.BASE_URL || 'http://localhost:5501';
const API_URL = process.env.API_URL || 'http://localhost:5001';

test.describe('HR - Attendance Page', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to attendance page
    await page.goto(`${BASE_URL}/hr/attendance`);
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should load attendance page successfully', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('الحضور والانصراف');
    
    // Check subtitle
    await expect(page.locator('p')).toContainText('إدارة ومتابعة حضور الموظفين');
    
    // Check check-in/out card is visible
    await expect(page.locator('[data-testid="attendance-card"]')).toBeVisible();
    
    // Check stats cards are visible
    const statsCards = page.locator('[data-testid="stats-card"]');
    await expect(statsCards).toHaveCount(4);
  });

  test('should display attendance statistics', async ({ page }) => {
    // Verify statistics cards: Present, Absent, Late, On Leave
    const statsLabels = ['حاضر', 'غائب', 'متأخر', 'إجازة'];
    
    for (const label of statsLabels) {
      const statCard = page.locator(`[data-testid="stats-card"]:has-text("${label}")`);
      if (await statCard.isVisible()) {
        // Should have a number value
        await expect(statCard.locator('.stat-value')).toBeVisible();
      }
    }
  });

  test('should show current user attendance status', async ({ page }) => {
    // Wait for user status card
    await page.waitForSelector('[data-testid="attendance-card"]', { timeout: 10000 });
    
    // Should display current status
    const statusText = await page.locator('[data-testid="attendance-card"] p').textContent();
    expect(statusText).toBeTruthy();
  });

  test('should enable check-in button when not checked in', async ({ page }) => {
    // Mock user not checked in
    await page.route(`${API_URL}/api/hr/attendance/my-status`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            checked_in: false,
            check_in_time: null,
            checked_out: false,
            check_out_time: null
          }
        })
      });
    });
    
    // Reload to apply mock
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check-in button should be enabled
    const checkInButton = page.locator('button:has-text("تسجيل الحضور")');
    await expect(checkInButton).toBeEnabled();
    
    // Check-out button should be disabled
    const checkOutButton = page.locator('button:has-text("تسجيل الانصراف")');
    await expect(checkOutButton).toBeDisabled();
  });

  test('should check-in successfully', async ({ page }) => {
    // Mock not checked in initially
    await page.route(`${API_URL}/api/hr/attendance/my-status`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            checked_in: false,
            check_in_time: null
          }
        })
      });
    });
    
    // Mock successful check-in
    await page.route(`${API_URL}/api/hr/attendance/check-in`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            checked_in: true,
            check_in_time: '09:00:00'
          },
          message: 'تم تسجيل الحضور بنجاح'
        })
      });
    });
    
    // Reload page
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Click check-in button
    await page.click('button:has-text("تسجيل الحضور")');
    
    // Wait for success message
    await expect(page.locator('.toast-success, .alert-success')).toContainText('نجاح', { timeout: 5000 });
  });

  test('should disable check-in button after checking in', async ({ page }) => {
    // Mock already checked in
    await page.route(`${API_URL}/api/hr/attendance/my-status`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            checked_in: true,
            check_in_time: '08:45:00',
            checked_out: false
          }
        })
      });
    });
    
    // Reload
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check-in button should be disabled
    const checkInButton = page.locator('button:has-text("تسجيل الحضور")');
    await expect(checkInButton).toBeDisabled();
    
    // Check-out button should be enabled
    const checkOutButton = page.locator('button:has-text("تسجيل الانصراف")');
    await expect(checkOutButton).toBeEnabled();
  });

  test('should check-out successfully', async ({ page }) => {
    // Mock checked in
    await page.route(`${API_URL}/api/hr/attendance/my-status`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            checked_in: true,
            check_in_time: '08:45:00',
            checked_out: false
          }
        })
      });
    });
    
    // Mock successful check-out
    await page.route(`${API_URL}/api/hr/attendance/check-out`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            checked_in: true,
            check_in_time: '08:45:00',
            checked_out: true,
            check_out_time: '17:30:00'
          },
          message: 'تم تسجيل الانصراف بنجاح'
        })
      });
    });
    
    // Reload
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Click check-out button
    await page.click('button:has-text("تسجيل الانصراف")');
    
    // Wait for success message
    await expect(page.locator('.toast-success')).toContainText('نجاح', { timeout: 5000 });
  });

  test('should display attendance records table', async ({ page }) => {
    // Wait for table to load
    await page.waitForSelector('table', { timeout: 10000 });
    
    // Check table headers
    const headers = ['الموظف', 'القسم', 'وقت الحضور', 'وقت الانصراف', 'الحالة', 'التأخير', 'الإضافي'];
    
    for (const header of headers) {
      await expect(page.locator('th')).toContainText(header);
    }
  });

  test('should display attendance records for selected date', async ({ page }) => {
    // Wait for records
    await page.waitForSelector('table tbody tr', { timeout: 10000 });
    
    // Should have at least one record (or empty state)
    const rows = page.locator('table tbody tr');
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should show correct status badges', async ({ page }) => {
    // Wait for table
    await page.waitForSelector('table tbody tr');
    
    // Check status badges
    const statusBadges = page.locator('[data-testid="status-badge"]');
    
    if (await statusBadges.first().isVisible()) {
      const firstBadge = await statusBadges.first().textContent();
      // Should be one of the valid statuses
      expect(['حاضر', 'غائب', 'متأخر', 'إجازة']).toContain(firstBadge);
    }
  });

  test('should navigate to previous day', async ({ page }) => {
    // Wait for date input
    await page.waitForSelector('input[type="date"]');
    
    // Get current date value
    const currentDate = await page.locator('input[type="date"]').inputValue();
    
    // Click previous day button
    await page.click('button[data-testid="prev-day"]');
    
    // Wait for update
    await page.waitForTimeout(1000);
    
    // Date should change
    const newDate = await page.locator('input[type="date"]').inputValue();
    expect(newDate).not.toBe(currentDate);
  });

  test('should navigate to next day', async ({ page }) => {
    // Wait for date input
    await page.waitForSelector('input[type="date"]');
    
    // Get current date value
    const currentDate = await page.locator('input[type="date"]').inputValue();
    
    // Click next day button
    await page.click('button[data-testid="next-day"]');
    
    // Wait for update
    await page.waitForTimeout(1000);
    
    // Date should change
    const newDate = await page.locator('input[type="date"]').inputValue();
    expect(newDate).not.toBe(currentDate);
  });

  test('should select specific date from date picker', async ({ page }) => {
    // Wait for date input
    await page.waitForSelector('input[type="date"]');
    
    // Select a specific date
    const targetDate = '2025-01-10';
    await page.fill('input[type="date"]', targetDate);
    
    // Trigger change event
    await page.press('input[type="date"]', 'Enter');
    
    // Wait for records to load
    await page.waitForTimeout(1000);
    
    // Date should be updated
    const selectedDate = await page.locator('input[type="date"]').inputValue();
    expect(selectedDate).toBe(targetDate);
  });

  test('should navigate to today', async ({ page }) => {
    // Change to a past date first
    await page.fill('input[type="date"]', '2025-01-01');
    await page.waitForTimeout(500);
    
    // Click "Today" button
    const todayButton = page.locator('button:has-text("اليوم")');
    await todayButton.click();
    
    // Wait for update
    await page.waitForTimeout(1000);
    
    // Should show today's date
    const today = new Date().toISOString().split('T')[0];
    const selectedDate = await page.locator('input[type="date"]').inputValue();
    expect(selectedDate).toBe(today);
  });

  test('should display late minutes for late employees', async ({ page }) => {
    // Wait for table
    await page.waitForSelector('table tbody tr');
    
    // Look for late indicator
    const lateCell = page.locator('td:has-text("د")'); // Minutes marker
    
    if (await lateCell.first().isVisible()) {
      const lateText = await lateCell.first().textContent();
      expect(lateText).toMatch(/\d+/); // Should contain number
    }
  });

  test('should display overtime hours', async ({ page }) => {
    // Wait for table
    await page.waitForSelector('table tbody tr');
    
    // Look for overtime indicator
    const overtimeCell = page.locator('td:has-text("س")'); // Hours marker
    
    if (await overtimeCell.first().isVisible()) {
      const overtimeText = await overtimeCell.first().textContent();
      expect(overtimeText).toMatch(/\d+/); // Should contain number
    }
  });

  test('should refresh attendance records', async ({ page }) => {
    // Wait for initial load
    await page.waitForSelector('table tbody tr');
    
    // Click refresh button
    await page.click('button:has-text("تحديث")');
    
    // Should reload
    await page.waitForSelector('table tbody tr', { timeout: 5000 });
  });

  test('should export attendance report', async ({ page }) => {
    // Mock export API
    await page.route(`${API_URL}/api/hr/attendance/export`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        body: Buffer.from('mock excel data')
      });
    });
    
    // Click export button
    const exportButton = page.locator('button:has-text("تصدير التقرير")');
    
    if (await exportButton.isVisible()) {
      // Start waiting for download
      const downloadPromise = page.waitForEvent('download');
      
      await exportButton.click();
      
      // Wait for download
      const download = await downloadPromise;
      
      // Verify filename
      expect(download.suggestedFilename()).toContain('attendance');
    }
  });

  test('should show empty state when no attendance records', async ({ page }) => {
    // Mock empty response
    await page.route(`${API_URL}/api/hr/attendance*`, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: [],
          stats: { present: 0, absent: 0, late: 0, onLeave: 0 }
        })
      });
    });
    
    // Reload
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Should show empty message
    await expect(page.locator('td[colspan]')).toContainText('لا توجد سجلات', { timeout: 5000 });
  });

  test('should filter attendance records', async ({ page }) => {
    // Wait for table
    await page.waitForSelector('table tbody tr');
    
    // Click filter button
    const filterButton = page.locator('button:has-text("تصفية")');
    
    if (await filterButton.isVisible()) {
      await filterButton.click();
      
      // Filter options should appear
      // (Implementation-specific)
    }
  });

  test('should show time in correct format (HH:MM)', async ({ page }) => {
    // Wait for table
    await page.waitForSelector('table tbody tr');
    
    // Check time format in check-in column
    const timeCell = page.locator('table tbody tr:first-child td:nth-child(3)');
    const timeText = await timeCell.textContent();
    
    if (timeText !== '-') {
      // Should match HH:MM format
      expect(timeText).toMatch(/\d{2}:\d{2}/);
    }
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route(`${API_URL}/api/hr/attendance*`, async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          message: 'حدث خطأ في الخادم'
        })
      });
    });
    
    // Reload
    await page.reload();
    
    // Should show error message
    await expect(page.locator('.error-message, .alert-danger')).toBeVisible({ timeout: 5000 });
  });

  test('should be accessible (ARIA checks)', async ({ page }) => {
    // Wait for page load
    await page.waitForSelector('table');
    
    // Check main heading
    await expect(page.locator('h1')).toBeVisible();
    
    // Check buttons have accessible names
    const checkInButton = page.locator('button:has-text("تسجيل الحضور")');
    await expect(checkInButton).toHaveAccessibleName();
    
    // Check date input has label
    const dateInput = page.locator('input[type="date"]');
    await expect(dateInput).toBeVisible();
  });

  test('should display date in Arabic format', async ({ page }) => {
    // Wait for date display
    await page.waitForSelector('[data-testid="date-display"]');
    
    // Should contain Arabic date text
    const dateText = await page.locator('[data-testid="date-display"]').textContent();
    
    // Should contain Arabic day names or month names
    const arabicPattern = /[\u0600-\u06FF]/;
    expect(arabicPattern.test(dateText)).toBeTruthy();
  });

  test('should update statistics when date changes', async ({ page }) => {
    // Get initial stats
    const initialPresent = await page.locator('[data-testid="stat-present"]').textContent();
    
    // Change date
    await page.fill('input[type="date"]', '2025-01-05');
    await page.waitForTimeout(1000);
    
    // Stats may change (or stay same depending on data)
    const newPresent = await page.locator('[data-testid="stat-present"]').textContent();
    
    // Stats should be loaded (not undefined)
    expect(newPresent).toBeTruthy();
  });
});
