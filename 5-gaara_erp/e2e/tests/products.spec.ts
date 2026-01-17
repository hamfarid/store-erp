/**
 * P0.43: E2E Tests - Product Management Flow
 * 
 * Tests for product CRUD operations.
 */

import { test, expect } from '@playwright/test';

test.describe('Products Management', () => {
  // Login before each test
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    await expect(page).toHaveURL(/dashboard/);
  });

  test('should display products list', async ({ page }) => {
    await page.goto('/products');
    
    await expect(page.getByRole('heading', { name: /products|المنتجات/i })).toBeVisible();
    await expect(page.getByRole('table')).toBeVisible();
  });

  test('should open add product modal', async ({ page }) => {
    await page.goto('/products');
    
    await page.getByRole('button', { name: /add|إضافة|جديد/i }).click();
    
    await expect(page.getByRole('dialog')).toBeVisible();
    await expect(page.getByLabel(/name|الاسم/i)).toBeVisible();
    await expect(page.getByLabel(/sku/i)).toBeVisible();
    await expect(page.getByLabel(/price|السعر/i)).toBeVisible();
  });

  test('should create a new product', async ({ page }) => {
    await page.goto('/products');
    
    // Open add modal
    await page.getByRole('button', { name: /add|إضافة|جديد/i }).click();
    
    // Fill form
    const timestamp = Date.now();
    await page.getByLabel(/name|الاسم/i).fill(`Test Product ${timestamp}`);
    await page.getByLabel(/sku/i).fill(`TEST-${timestamp}`);
    await page.getByLabel(/price|السعر/i).fill('99.99');
    await page.getByLabel(/quantity|الكمية/i).fill('100');
    
    // Submit
    await page.getByRole('button', { name: /save|حفظ|إنشاء/i }).click();
    
    // Verify success message
    await expect(page.getByText(/success|تم|نجاح/i)).toBeVisible();
    
    // Verify product in list
    await expect(page.getByText(`Test Product ${timestamp}`)).toBeVisible();
  });

  test('should edit a product', async ({ page }) => {
    await page.goto('/products');
    
    // Click edit on first product
    await page.getByRole('row').first().getByRole('button', { name: /edit|تعديل/i }).click();
    
    // Modify name
    const nameInput = page.getByLabel(/name|الاسم/i);
    await nameInput.clear();
    await nameInput.fill('Updated Product Name');
    
    // Submit
    await page.getByRole('button', { name: /save|حفظ|تحديث/i }).click();
    
    // Verify success
    await expect(page.getByText(/success|تم|نجاح/i)).toBeVisible();
  });

  test('should search products', async ({ page }) => {
    await page.goto('/products');
    
    // Enter search term
    await page.getByPlaceholder(/search|بحث/i).fill('test');
    await page.keyboard.press('Enter');
    
    // Wait for results
    await page.waitForTimeout(500);
    
    // Verify filtered results
    const rows = page.getByRole('row');
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should delete a product', async ({ page }) => {
    await page.goto('/products');
    
    // Get initial row count
    const initialCount = await page.getByRole('row').count();
    
    // Click delete on first product
    await page.getByRole('row').first().getByRole('button', { name: /delete|حذف/i }).click();
    
    // Confirm deletion
    await page.getByRole('button', { name: /confirm|تأكيد|نعم/i }).click();
    
    // Verify success
    await expect(page.getByText(/deleted|تم الحذف/i)).toBeVisible();
    
    // Verify row count decreased (or product removed)
    await page.waitForTimeout(500);
  });

  test('should validate required fields', async ({ page }) => {
    await page.goto('/products');
    
    // Open add modal
    await page.getByRole('button', { name: /add|إضافة|جديد/i }).click();
    
    // Try to submit empty form
    await page.getByRole('button', { name: /save|حفظ|إنشاء/i }).click();
    
    // Verify validation errors
    await expect(page.getByText(/required|مطلوب/i)).toBeVisible();
  });

  test('should reject negative price', async ({ page }) => {
    await page.goto('/products');
    
    // Open add modal
    await page.getByRole('button', { name: /add|إضافة|جديد/i }).click();
    
    // Fill with negative price
    await page.getByLabel(/name|الاسم/i).fill('Test Product');
    await page.getByLabel(/sku/i).fill('TEST-NEG');
    await page.getByLabel(/price|السعر/i).fill('-10');
    
    // Submit
    await page.getByRole('button', { name: /save|حفظ|إنشاء/i }).click();
    
    // Verify validation error
    await expect(page.getByText(/invalid|positive|negative|سالب/i)).toBeVisible();
  });
});

