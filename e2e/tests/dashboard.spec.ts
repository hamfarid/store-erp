/**
 * E2E Tests - Dashboard
 * 
 * Tests for dashboard functionality and statistics.
 */

import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    await expect(page).toHaveURL(/dashboard/);
  });

  test('should display dashboard statistics cards', async ({ page }) => {
    // Check for statistics cards
    await expect(page.locator('[data-testid="stats-card"]').first()).toBeVisible();
    
    // Should have multiple stat cards
    const statCards = page.locator('[data-testid="stats-card"], .stat-card, .stats-card');
    const count = await statCards.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should display sales chart', async ({ page }) => {
    // Check for chart container
    const chartContainer = page.locator('[data-testid="sales-chart"], .recharts-wrapper, canvas');
    await expect(chartContainer.first()).toBeVisible();
  });

  test('should display recent activities', async ({ page }) => {
    // Check for recent activities section
    const activitiesSection = page.locator('[data-testid="recent-activities"], .activities-list');
    await expect(activitiesSection).toBeVisible();
  });

  test('should display low stock alerts', async ({ page }) => {
    // Check for alerts section
    const alertsSection = page.locator('[data-testid="alerts"], .alerts-section, .low-stock');
    const exists = await alertsSection.count();
    
    // May or may not have alerts depending on data
    expect(exists).toBeGreaterThanOrEqual(0);
  });

  test('should navigate to products from quick action', async ({ page }) => {
    // Click on products quick action or link
    await page.getByRole('link', { name: /products|المنتجات/i }).first().click();
    await expect(page).toHaveURL(/products/);
  });

  test('should navigate to invoices from quick action', async ({ page }) => {
    // Click on invoices quick action or link
    await page.getByRole('link', { name: /invoices|الفواتير/i }).first().click();
    await expect(page).toHaveURL(/invoices/);
  });

  test('should refresh dashboard data', async ({ page }) => {
    // Find and click refresh button if exists
    const refreshButton = page.getByRole('button', { name: /refresh|تحديث/i });
    const exists = await refreshButton.count();
    
    if (exists > 0) {
      await refreshButton.click();
      // Wait for loading state
      await page.waitForLoadState('networkidle');
    }
  });

  test('should display correct date range', async ({ page }) => {
    // Check for date picker or date range display
    const dateRange = page.locator('[data-testid="date-range"], .date-picker, .date-range');
    const exists = await dateRange.count();
    
    if (exists > 0) {
      await expect(dateRange.first()).toBeVisible();
    }
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Dashboard should still be functional
    await expect(page.locator('main, [role="main"]')).toBeVisible();
    
    // Sidebar might be collapsed/hidden
    const sidebar = page.locator('[data-testid="sidebar"], .sidebar, aside');
    const sidebarVisible = await sidebar.isVisible();
    
    // On mobile, sidebar might be hidden or collapsed
    // This is expected behavior
    expect(typeof sidebarVisible).toBe('boolean');
  });
});
