/**
 * Authentication Setup for E2E Tests
 * 
 * This runs before all tests to authenticate and save session state.
 */

import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '../playwright/.auth/user.json');

setup('authenticate', async ({ page }) => {
  // Navigate to login page
  await page.goto('/login');
  
  // Fill login form
  await page.fill('[data-testid="email-input"], input[name="email"], input[type="email"]', 
    process.env.E2E_USER_EMAIL || 'test@gaara-erp.com');
  
  await page.fill('[data-testid="password-input"], input[name="password"], input[type="password"]', 
    process.env.E2E_USER_PASSWORD || 'testpassword123');
  
  // Submit login
  await page.click('[data-testid="login-button"], button[type="submit"]');
  
  // Wait for successful login - redirect to dashboard
  await expect(page).toHaveURL(/\/(dashboard|home)?$/);
  
  // Verify authentication
  await expect(page.locator('[data-testid="user-menu"], .user-menu')).toBeVisible();
  
  // Save authentication state
  await page.context().storageState({ path: authFile });
});

