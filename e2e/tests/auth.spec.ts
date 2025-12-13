/**
 * P0.43: E2E Tests - Authentication Flow
 * 
 * Tests for login, logout, and authentication-related functionality.
 */

import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Clear storage before each test
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
  });

  test('should display login page', async ({ page }) => {
    await page.goto('/login');
    
    await expect(page.getByRole('heading', { name: /login|تسجيل الدخول/i })).toBeVisible();
    await expect(page.getByLabel(/username|اسم المستخدم/i)).toBeVisible();
    await expect(page.getByLabel(/password|كلمة المرور/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /login|دخول/i })).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.getByLabel(/username|اسم المستخدم/i).fill('invaliduser');
    await page.getByLabel(/password|كلمة المرور/i).fill('wrongpassword');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    
    await expect(page.getByText(/invalid|خطأ|incorrect/i)).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    
    // Should redirect to dashboard
    await expect(page).toHaveURL(/dashboard|الرئيسية/);
    
    // Token should be stored
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeTruthy();
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    
    await expect(page).toHaveURL(/dashboard/);
    
    // Click logout
    await page.getByRole('button', { name: /logout|خروج|تسجيل الخروج/i }).click();
    
    // Should redirect to login
    await expect(page).toHaveURL(/login/);
    
    // Token should be cleared
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBeFalsy();
  });

  test('should redirect to login when accessing protected route without auth', async ({ page }) => {
    await page.goto('/dashboard');
    
    await expect(page).toHaveURL(/login/);
  });

  test('should show access denied for unauthorized user', async ({ page }) => {
    // Login as regular user (assuming 'user' role has limited permissions)
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('user');
    await page.getByLabel(/password|كلمة المرور/i).fill('user123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    
    // Try to access admin page
    await page.goto('/admin/users');
    
    // Should show access denied
    await expect(page.getByText(/access denied|ليس لديك صلاحية/i)).toBeVisible();
  });
});

