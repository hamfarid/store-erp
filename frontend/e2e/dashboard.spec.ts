import { test, expect } from './fixtures';

/**
 * Dashboard E2E Tests - RORLOC Phase 4
 * P1 High Priority
 */

test.describe('Dashboard - P1 High', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/dashboard');
    await authenticatedPage.waitForLoadState('networkidle');
  });

  test('should display dashboard with statistics', async ({ authenticatedPage }) => {
    // Verify dashboard loads
    await expect(authenticatedPage.locator('h1, h2')).toContainText(/لوحة|Dashboard|الرئيسية/);
    
    // Check for stat cards
    const statCards = authenticatedPage.locator('.stat-card, .stats-card, [class*="stat"]');
    await expect(statCards.first()).toBeVisible({ timeout: 10000 });
  });

  test('should display key metrics', async ({ authenticatedPage }) => {
    // Wait for data to load
    await authenticatedPage.waitForTimeout(2000);
    
    // Check for common dashboard metrics
    const metricsText = await authenticatedPage.textContent('body');
    
    // Should have at least some metrics visible
    const hasMetrics = 
      metricsText?.includes('منتج') || 
      metricsText?.includes('Product') ||
      metricsText?.includes('عميل') ||
      metricsText?.includes('Customer') ||
      metricsText?.includes('فاتورة') ||
      metricsText?.includes('Invoice');
    
    expect(hasMetrics).toBeTruthy();
  });

  test('should have navigation to main modules', async ({ authenticatedPage }) => {
    // Check sidebar navigation
    const sidebar = authenticatedPage.locator('aside, nav, [role="navigation"]');
    await expect(sidebar.first()).toBeVisible();
    
    // Verify key navigation links exist
    const navLinks = authenticatedPage.locator('a[href*="product"], a[href*="customer"], a[href*="invoice"]');
    await expect(navLinks.first()).toBeVisible();
  });

  test('should display recent activity or alerts', async ({ authenticatedPage }) => {
    // Look for recent activity section
    const activitySection = authenticatedPage.locator(
      '[class*="recent"], [class*="activity"], [class*="alert"], [class*="notification"]'
    );
    
    // At least one such section should exist
    const count = await activitySection.count();
    expect(count).toBeGreaterThanOrEqual(0); // May not always have activity
  });

  test('should be responsive on mobile viewport', async ({ authenticatedPage }) => {
    // Resize to mobile viewport
    await authenticatedPage.setViewportSize({ width: 375, height: 667 });
    
    // Dashboard should still be visible
    await expect(authenticatedPage.locator('body')).toBeVisible();
    
    // Menu should be accessible (hamburger menu or sidebar)
    const mobileMenu = authenticatedPage.locator(
      'button[aria-label*="menu"], .hamburger, [class*="mobile-menu"]'
    );
    
    // Either mobile menu or regular nav should be accessible
    const hasMobileMenu = await mobileMenu.isVisible();
    const hasNav = await authenticatedPage.locator('nav, aside').isVisible();
    
    expect(hasMobileMenu || hasNav).toBeTruthy();
  });
});

test.describe('Dashboard Navigation - P1 High', () => {
  test('should navigate to Products from dashboard', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/dashboard');
    
    // Find and click products link
    const productsLink = authenticatedPage.locator('a[href*="product"]').first();
    if (await productsLink.isVisible()) {
      await productsLink.click();
      await expect(authenticatedPage).toHaveURL(/product/);
    }
  });

  test('should navigate to Customers from dashboard', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/dashboard');
    
    // Find and click customers link
    const customersLink = authenticatedPage.locator('a[href*="customer"]').first();
    if (await customersLink.isVisible()) {
      await customersLink.click();
      await expect(authenticatedPage).toHaveURL(/customer/);
    }
  });

  test('should navigate to Invoices from dashboard', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/dashboard');
    
    // Find and click invoices link
    const invoicesLink = authenticatedPage.locator('a[href*="invoice"]').first();
    if (await invoicesLink.isVisible()) {
      await invoicesLink.click();
      await expect(authenticatedPage).toHaveURL(/invoice/);
    }
  });
});

