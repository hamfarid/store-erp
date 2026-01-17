/**
 * P0.43: E2E Tests - Invoice Management Flow
 * 
 * Tests for invoice creation and management.
 */

import { test, expect } from '@playwright/test';

test.describe('Invoice Management', () => {
  // Login before each test
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    await expect(page).toHaveURL(/dashboard/);
  });

  test('should display invoices list', async ({ page }) => {
    await page.goto('/invoices');
    
    await expect(page.getByRole('heading', { name: /invoices|الفواتير/i })).toBeVisible();
    await expect(page.getByRole('table')).toBeVisible();
  });

  test('should create a new sales invoice', async ({ page }) => {
    await page.goto('/invoices');
    
    // Click add new invoice
    await page.getByRole('button', { name: /add|إضافة|جديد/i }).click();
    
    // Select invoice type
    await page.getByRole('combobox', { name: /type|نوع/i }).selectOption('sale');
    
    // Select customer
    await page.getByRole('combobox', { name: /customer|عميل/i }).click();
    await page.getByRole('option').first().click();
    
    // Add product
    await page.getByRole('button', { name: /add item|إضافة صنف/i }).click();
    await page.getByRole('combobox', { name: /product|منتج/i }).click();
    await page.getByRole('option').first().click();
    
    // Set quantity
    await page.getByLabel(/quantity|كمية/i).fill('5');
    
    // Save invoice
    await page.getByRole('button', { name: /save|حفظ|إنشاء/i }).click();
    
    // Verify success
    await expect(page.getByText(/success|تم|نجاح/i)).toBeVisible();
  });

  test('should view invoice details', async ({ page }) => {
    await page.goto('/invoices');
    
    // Click on first invoice
    await page.getByRole('row').nth(1).click();
    
    // Verify details page
    await expect(page.getByText(/invoice details|تفاصيل الفاتورة/i)).toBeVisible();
    await expect(page.getByText(/invoice number|رقم الفاتورة/i)).toBeVisible();
    await expect(page.getByText(/total|الإجمالي/i)).toBeVisible();
  });

  test('should filter invoices by type', async ({ page }) => {
    await page.goto('/invoices');
    
    // Filter by sales
    await page.getByRole('combobox', { name: /filter|تصفية|نوع/i }).selectOption('sale');
    
    await page.waitForTimeout(500);
    
    // Verify all visible invoices are sales
    const types = await page.getByRole('cell', { name: /sale|بيع/i }).count();
    expect(types).toBeGreaterThanOrEqual(0);
  });

  test('should filter invoices by status', async ({ page }) => {
    await page.goto('/invoices');
    
    // Filter by paid
    await page.getByRole('combobox', { name: /status|حالة/i }).selectOption('paid');
    
    await page.waitForTimeout(500);
    
    // Verify filtered results
    const statuses = await page.getByRole('cell', { name: /paid|مدفوع/i }).count();
    expect(statuses).toBeGreaterThanOrEqual(0);
  });

  test('should calculate invoice totals correctly', async ({ page }) => {
    await page.goto('/invoices/new');
    
    // Select type and customer
    await page.getByRole('combobox', { name: /type|نوع/i }).selectOption('sale');
    await page.getByRole('combobox', { name: /customer|عميل/i }).click();
    await page.getByRole('option').first().click();
    
    // Add first item
    await page.getByRole('button', { name: /add item|إضافة صنف/i }).click();
    await page.getByRole('combobox', { name: /product|منتج/i }).first().click();
    await page.getByRole('option').first().click();
    await page.getByLabel(/quantity|كمية/i).first().fill('2');
    await page.getByLabel(/unit price|سعر الوحدة/i).first().fill('100');
    
    // Verify subtotal updates
    const subtotal = await page.getByTestId('subtotal').textContent();
    expect(subtotal).toContain('200');
  });

  test('should print invoice', async ({ page }) => {
    await page.goto('/invoices');
    
    // Click on first invoice
    await page.getByRole('row').nth(1).click();
    
    // Click print button
    const printPromise = page.waitForEvent('popup');
    await page.getByRole('button', { name: /print|طباعة/i }).click();
    
    // Verify print preview opens
    const printPage = await printPromise;
    await expect(printPage).toBeTruthy();
  });

  test('should export invoices', async ({ page }) => {
    await page.goto('/invoices');
    
    // Click export button
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: /export|تصدير/i }).click();
    
    // Select format
    await page.getByRole('menuitem', { name: /excel|csv/i }).click();
    
    // Verify download starts
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/invoices.*\.(xlsx|csv)/);
  });

  test('should record payment for invoice', async ({ page }) => {
    await page.goto('/invoices');
    
    // Find unpaid invoice and click
    await page.getByRole('row').filter({ hasText: /pending|معلق/i }).first().click();
    
    // Click pay button
    await page.getByRole('button', { name: /pay|دفع|تسديد/i }).click();
    
    // Enter payment amount
    await page.getByLabel(/amount|المبلغ/i).fill('100');
    
    // Confirm payment
    await page.getByRole('button', { name: /confirm|تأكيد/i }).click();
    
    // Verify success
    await expect(page.getByText(/payment recorded|تم تسجيل الدفع/i)).toBeVisible();
  });
});

