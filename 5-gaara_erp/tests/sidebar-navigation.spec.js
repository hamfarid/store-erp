/**
 * Sidebar Navigation Tests
 * 
 * Tests all sidebar menu items to ensure they navigate to the correct routes
 * without unnecessary redirects.
 * 
 * Date: 2025-01-25
 * Status: Testing Phase 1 routing fixes
 */

import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:5505';

// Test credentials
const TEST_USER = {
  username: 'admin',
  password: 'admin123'
};

test.describe('Sidebar Navigation Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to login page
    await page.goto(BASE_URL);
    
    // Login
    await page.fill('input[name="username"]', TEST_USER.username);
    await page.fill('input[name="password"]', TEST_USER.password);
    await page.click('button[type="submit"]');
    
    // Wait for dashboard to load
    await page.waitForURL(`${BASE_URL}/`);
  });

  test('Main Section - Dashboard', async ({ page }) => {
    // Click on Dashboard in sidebar
    await page.click('text=لوحة المعلومات');
    
    // Verify URL is correct (no redirect)
    await expect(page).toHaveURL(`${BASE_URL}/`);
    
    // Verify page loaded
    await expect(page.locator('h1, h2')).toContainText(/لوحة|Dashboard/);
  });

  test('Admin Section - User Management', async ({ page }) => {
    // Click on User Management
    await page.click('text=إدارة المستخدمين');
    
    // Verify URL is /users (not /admin/users)
    await expect(page).toHaveURL(`${BASE_URL}/users`);
    
    // Verify no redirect happened
    const navigationHistory = await page.evaluate(() => window.history.length);
    expect(navigationHistory).toBeLessThanOrEqual(3); // Login + Dashboard + Users
  });

  test('Reports Section - Comprehensive Reports', async ({ page }) => {
    // Click on Comprehensive Reports
    await page.click('text=التقارير الشاملة');
    
    // Verify URL is /reports (not /reports/comprehensive)
    await expect(page).toHaveURL(`${BASE_URL}/reports`);
    
    // Verify page loaded
    await expect(page.locator('h1, h2')).toContainText(/تقارير|Reports/);
  });

  test('Accounting Section - Payment Vouchers', async ({ page }) => {
    // Expand Accounting section
    await page.click('text=النظام المحاسبي');
    
    // Click on Payment Vouchers
    await page.click('text=قسائم الدفع');
    
    // Verify URL is /accounting/vouchers
    await expect(page).toHaveURL(`${BASE_URL}/accounting/vouchers`);
  });

  test('Accounting Section - Cash Boxes', async ({ page }) => {
    // Expand Accounting section
    await page.click('text=النظام المحاسبي');
    
    // Click on Cash Boxes
    await page.click('text=الصناديق والحسابات');
    
    // Verify URL is /accounting/cash-boxes
    await expect(page).toHaveURL(`${BASE_URL}/accounting/cash-boxes`);
  });

  test('System Section - Setup Wizard', async ({ page }) => {
    // Expand System section
    await page.click('text=النظام المتقدم');
    
    // Click on Setup Wizard
    await page.click('text=معالج الإعداد');
    
    // Verify URL is /setup-wizard (not /system/setup-wizard)
    await expect(page).toHaveURL(`${BASE_URL}/setup-wizard`);
  });

  test('System Section - Notifications', async ({ page }) => {
    // Expand System section
    await page.click('text=النظام المتقدم');
    
    // Click on Notifications
    await page.click('text=نظام الإشعارات');
    
    // Verify URL is /notifications
    await expect(page).toHaveURL(`${BASE_URL}/notifications`);
  });

  test('Advanced Section - Customer Accounts', async ({ page }) => {
    // Expand Advanced section
    await page.click('text=الميزات المتقدمة');
    
    // Click on Customer/Supplier Accounts
    await page.click('text=حسابات العملاء والموردين');
    
    // Verify URL is /customers (not /accounts/customer-supplier)
    await expect(page).toHaveURL(`${BASE_URL}/customers`);
  });

  test('Tools Section - Import/Export', async ({ page }) => {
    // Expand Tools section
    await page.click('text=الأدوات والمساعدات');
    
    // Click on Import/Export
    await page.click('text=الاستيراد والتصدير');
    
    // Verify URL is /tools/import-export
    await expect(page).toHaveURL(`${BASE_URL}/tools/import-export`);
  });

  test('All Sidebar Links - No Console Errors', async ({ page }) => {
    const consoleErrors = [];
    
    // Listen for console errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Click through all main sections
    const sections = [
      'الرئيسية',
      'إدارة المخزون',
      'المبيعات والشراء',
      'النظام المحاسبي',
      'التقارير والتحليلات',
      'الميزات المتقدمة',
      'الأدوات والمساعدات',
      'الإدارة والأمان',
      'الإعدادات',
      'النظام المتقدم'
    ];

    for (const section of sections) {
      await page.click(`text=${section}`);
      await page.waitForTimeout(500); // Wait for section to expand
    }

    // Verify no console errors
    expect(consoleErrors).toHaveLength(0);
  });

});

