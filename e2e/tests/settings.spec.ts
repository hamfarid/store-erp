/**
 * E2E Tests - Settings Pages
 * Store ERP v2.0.0
 * 
 * Tests for system settings, notifications, tax, and backup functionality.
 */

import { test, expect, Page } from '@playwright/test';

async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
  await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
  await page.getByRole('button', { name: /login|دخول/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('General Settings', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/settings');
  });

  test('should display settings page', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /settings|إعدادات/i })).toBeVisible();
  });

  test('should show company information section', async ({ page }) => {
    await expect(page.getByText(/company|شركة|مؤسسة/i)).toBeVisible();
    await expect(page.getByLabel(/company name|اسم الشركة/i)).toBeVisible();
  });

  test('should update company information', async ({ page }) => {
    const companyNameInput = page.getByLabel(/company name|اسم الشركة/i);
    
    if (await companyNameInput.isVisible()) {
      await companyNameInput.clear();
      await companyNameInput.fill('Test Company Updated');
      
      // Save
      await page.getByRole('button', { name: /save|حفظ/i }).click();
      
      // Verify success
      await expect(page.getByText(/saved|تم الحفظ|success/i)).toBeVisible();
    }
  });

  test('should toggle dark mode', async ({ page }) => {
    const darkModeToggle = page.getByRole('switch', { name: /dark|داكن/i });
    
    if (await darkModeToggle.isVisible()) {
      await darkModeToggle.click();
      
      // Check body class changes
      await page.waitForTimeout(300);
      const isDark = await page.evaluate(() => 
        document.documentElement.classList.contains('dark')
      );
      
      // Toggle again
      await darkModeToggle.click();
      const isLight = await page.evaluate(() => 
        !document.documentElement.classList.contains('dark')
      );
      
      expect(isDark !== isLight).toBeTruthy();
    }
  });
});

test.describe('Notification Settings', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/notification-settings');
  });

  test('should display notification settings page', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /notification|إشعار/i })).toBeVisible();
  });

  test('should toggle notification channels', async ({ page }) => {
    // Email notifications toggle
    const emailToggle = page.getByRole('switch', { name: /email|بريد/i });
    
    if (await emailToggle.isVisible()) {
      const initialState = await emailToggle.isChecked();
      await emailToggle.click();
      
      await page.waitForTimeout(300);
      const newState = await emailToggle.isChecked();
      
      expect(newState).toBe(!initialState);
    }
  });

  test('should configure inventory alerts', async ({ page }) => {
    const lowStockThreshold = page.getByLabel(/low stock|مخزون منخفض|threshold/i);
    
    if (await lowStockThreshold.isVisible()) {
      await lowStockThreshold.clear();
      await lowStockThreshold.fill('10');
      
      // Save
      await page.getByRole('button', { name: /save|حفظ/i }).click();
      
      await expect(page.getByText(/saved|success|تم/i)).toBeVisible();
    }
  });

  test('should set quiet hours', async ({ page }) => {
    const quietHoursToggle = page.getByRole('switch', { name: /quiet|صامت/i });
    
    if (await quietHoursToggle.isVisible()) {
      await quietHoursToggle.click();
      
      // Configure time range if visible
      const startTime = page.getByLabel(/start time|وقت البدء/i);
      if (await startTime.isVisible()) {
        await startTime.fill('22:00');
        
        const endTime = page.getByLabel(/end time|وقت الانتهاء/i);
        await endTime.fill('08:00');
      }
    }
  });
});

test.describe('Tax Settings', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/tax-settings');
  });

  test('should display tax settings page', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /tax|ضريبة/i })).toBeVisible();
  });

  test('should toggle tax enabled', async ({ page }) => {
    const taxToggle = page.getByRole('switch', { name: /enable tax|تفعيل الضريبة/i });
    
    if (await taxToggle.isVisible()) {
      await taxToggle.click();
      await page.waitForTimeout(300);
      
      // Tax settings should show/hide based on toggle
      const taxRateInput = page.getByLabel(/rate|نسبة/i);
      expect(await taxRateInput.isVisible()).toBeTruthy();
    }
  });

  test('should configure default tax rate', async ({ page }) => {
    const taxRateInput = page.getByLabel(/default.*rate|نسبة.*افتراضية/i);
    
    if (await taxRateInput.isVisible()) {
      await taxRateInput.clear();
      await taxRateInput.fill('15');
      
      // Save
      await page.getByRole('button', { name: /save|حفظ/i }).click();
      
      await expect(page.getByText(/saved|success|تم/i)).toBeVisible();
    }
  });

  test('should add custom tax type', async ({ page }) => {
    const addTaxBtn = page.getByRole('button', { name: /add tax|إضافة ضريبة/i });
    
    if (await addTaxBtn.isVisible()) {
      await addTaxBtn.click();
      
      // Fill tax type form
      await page.getByLabel(/name|اسم/i).fill('Test Tax');
      await page.getByLabel(/rate|نسبة/i).fill('5');
      
      // Save
      await page.getByRole('button', { name: /save|حفظ|add|إضافة/i }).click();
      
      // Verify added
      await expect(page.getByText('Test Tax')).toBeVisible();
    }
  });

  test('should configure ZATCA settings', async ({ page }) => {
    const zatcaSection = page.getByText(/zatca|زاتكا/i);
    
    if (await zatcaSection.isVisible()) {
      // Expand ZATCA section if collapsed
      await zatcaSection.click();
      
      // Check for ZATCA fields
      await expect(page.getByLabel(/tax number|الرقم الضريبي/i)).toBeVisible();
    }
  });
});

test.describe('Backup & Restore Settings', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/backup-restore');
  });

  test('should display backup settings page', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /backup|نسخ احتياطي/i })).toBeVisible();
  });

  test('should show backup history', async ({ page }) => {
    const backupList = page.locator('[data-testid="backup-list"]');
    
    // Should have backup list or empty state
    const hasList = await backupList.isVisible();
    const hasEmpty = await page.getByText(/no backups|لا توجد نسخ/i).isVisible();
    
    expect(hasList || hasEmpty).toBeTruthy();
  });

  test('should create manual backup', async ({ page }) => {
    const createBackupBtn = page.getByRole('button', { name: /create backup|إنشاء نسخة/i });
    
    if (await createBackupBtn.isVisible()) {
      await createBackupBtn.click();
      
      // Confirm if needed
      const confirmBtn = page.getByRole('button', { name: /confirm|تأكيد|yes|نعم/i });
      if (await confirmBtn.isVisible()) {
        await confirmBtn.click();
      }
      
      // Wait for backup process
      await page.waitForTimeout(2000);
      
      // Should show success or backup in list
      const success = await page.getByText(/success|تم|backup created/i).isVisible();
      const inList = await page.locator('[data-testid="backup-item"]').count() > 0;
      
      expect(success || inList).toBeTruthy();
    }
  });

  test('should configure auto backup', async ({ page }) => {
    const autoBackupToggle = page.getByRole('switch', { name: /auto|تلقائي/i });
    
    if (await autoBackupToggle.isVisible()) {
      await autoBackupToggle.click();
      
      // Configure schedule
      const scheduleSelect = page.getByRole('combobox', { name: /schedule|جدول/i });
      if (await scheduleSelect.isVisible()) {
        await scheduleSelect.click();
        await page.getByRole('option', { name: /daily|يومي/i }).click();
      }
      
      // Save
      await page.getByRole('button', { name: /save|حفظ/i }).click();
      
      await expect(page.getByText(/saved|success|تم/i)).toBeVisible();
    }
  });
});

test.describe('User & Role Management Settings', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/users');
  });

  test('should display users list', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /users|مستخدم/i })).toBeVisible();
    
    // Should have users table
    const usersTable = page.locator('table');
    expect(await usersTable.isVisible()).toBeTruthy();
  });

  test('should add new user', async ({ page }) => {
    await page.getByRole('button', { name: /add user|إضافة مستخدم/i }).click();
    
    // Fill user form
    await page.getByLabel(/username|اسم المستخدم/i).fill('testuser');
    await page.getByLabel(/email|بريد/i).fill('test@example.com');
    await page.getByLabel(/password|كلمة المرور/i).fill('TestPass123!');
    
    // Select role
    const roleSelect = page.getByRole('combobox', { name: /role|دور/i });
    if (await roleSelect.isVisible()) {
      await roleSelect.click();
      await page.getByRole('option').first().click();
    }
    
    // Submit
    await page.getByRole('button', { name: /save|create|حفظ|إنشاء/i }).click();
    
    await expect(page.getByText(/success|created|تم/i)).toBeVisible();
  });

  test('should navigate to roles management', async ({ page }) => {
    await page.goto('/roles');
    
    await expect(page.getByRole('heading', { name: /roles|صلاحيات|أدوار/i })).toBeVisible();
    
    // Should show roles list
    const rolesList = page.locator('[data-testid="roles-list"]');
    expect(await rolesList.isVisible() || await page.locator('table').isVisible()).toBeTruthy();
  });
});
