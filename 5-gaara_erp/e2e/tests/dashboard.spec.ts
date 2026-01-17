/**
 * Dashboard E2E Tests for Gaara ERP v12
 */

import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display main dashboard', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Gaara ERP|لوحة التحكم/);
    
    // Check main navigation is visible
    await expect(page.locator('nav, [data-testid="main-nav"]')).toBeVisible();
  });

  test('should display statistics cards', async ({ page }) => {
    // Dashboard should show summary cards
    const statsSection = page.locator('[data-testid="stats-section"], .stats-cards, .dashboard-stats');
    await expect(statsSection).toBeVisible();
  });

  test('should navigate to inventory module', async ({ page }) => {
    // Click inventory link
    await page.click('a[href*="inventory"], [data-testid="nav-inventory"]');
    
    // Verify navigation
    await expect(page).toHaveURL(/\/inventory/);
  });

  test('should navigate to sales module', async ({ page }) => {
    // Click sales link
    await page.click('a[href*="sales"], [data-testid="nav-sales"]');
    
    // Verify navigation
    await expect(page).toHaveURL(/\/sales/);
  });

  test('should navigate to accounting module', async ({ page }) => {
    // Click accounting link
    await page.click('a[href*="accounting"], [data-testid="nav-accounting"]');
    
    // Verify navigation
    await expect(page).toHaveURL(/\/accounting/);
  });

  test('should support Arabic language', async ({ page }) => {
    // Check for Arabic text or RTL layout
    const htmlElement = page.locator('html');
    const dir = await htmlElement.getAttribute('dir');
    const lang = await htmlElement.getAttribute('lang');
    
    // Should be RTL for Arabic
    expect(dir === 'rtl' || lang?.startsWith('ar')).toBeTruthy();
  });

  test('should display user profile menu', async ({ page }) => {
    // User menu should be accessible
    const userMenu = page.locator('[data-testid="user-menu"], .user-menu, .profile-dropdown');
    await expect(userMenu).toBeVisible();
    
    // Click to open dropdown
    await userMenu.click();
    
    // Should show logout option
    await expect(page.locator('[data-testid="logout-btn"], a:has-text("تسجيل الخروج"), button:has-text("خروج")')).toBeVisible();
  });
});

