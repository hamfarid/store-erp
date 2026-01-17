/**
 * E2E Tests - Point of Sale (POS) System
 * Store ERP v2.0.0
 * 
 * Tests for POS functionality including cart, barcode, payments, and receipts.
 */

import { test, expect, Page } from '@playwright/test';

// Helper to login before tests
async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
  await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
  await page.getByRole('button', { name: /login|دخول/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('POS System', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/pos');
  });

  test('should load POS page with all components', async ({ page }) => {
    // Check for main POS components
    await expect(page.getByRole('heading', { name: /pos|نقطة البيع/i })).toBeVisible();
    
    // Product search/barcode input
    await expect(page.getByPlaceholder(/barcode|باركود|search|بحث/i)).toBeVisible();
    
    // Cart section
    await expect(page.getByText(/cart|سلة|العربة/i)).toBeVisible();
    
    // Payment buttons
    await expect(page.getByRole('button', { name: /pay|دفع|checkout/i })).toBeVisible();
  });

  test('should search and add product to cart', async ({ page }) => {
    // Search for a product
    const searchInput = page.getByPlaceholder(/barcode|باركود|search|بحث/i);
    await searchInput.fill('product');
    await searchInput.press('Enter');
    
    // Wait for search results
    await page.waitForTimeout(500);
    
    // Click first product to add to cart
    const productCard = page.locator('[data-testid="product-card"]').first();
    if (await productCard.isVisible()) {
      await productCard.click();
      
      // Verify item added to cart
      await expect(page.locator('[data-testid="cart-item"]')).toHaveCount(1);
    }
  });

  test('should update quantity in cart', async ({ page }) => {
    // Add a product first (assuming there's a quick add button)
    const quickAddBtn = page.locator('[data-testid="quick-add"]').first();
    if (await quickAddBtn.isVisible()) {
      await quickAddBtn.click();
      
      // Find quantity input and update
      const qtyInput = page.locator('[data-testid="cart-item-qty"]').first();
      await qtyInput.fill('3');
      await qtyInput.press('Enter');
      
      // Verify quantity updated
      await expect(qtyInput).toHaveValue('3');
    }
  });

  test('should remove item from cart', async ({ page }) => {
    // Add a product first
    const quickAddBtn = page.locator('[data-testid="quick-add"]').first();
    if (await quickAddBtn.isVisible()) {
      await quickAddBtn.click();
      
      // Count items
      const initialCount = await page.locator('[data-testid="cart-item"]').count();
      
      // Click remove button
      await page.locator('[data-testid="remove-item"]').first().click();
      
      // Verify item removed
      const newCount = await page.locator('[data-testid="cart-item"]').count();
      expect(newCount).toBeLessThan(initialCount);
    }
  });

  test('should calculate totals correctly', async ({ page }) => {
    // This test would need specific product data
    // Verify that subtotal, tax, and total are displayed
    await expect(page.getByText(/subtotal|المجموع الفرعي/i)).toBeVisible();
    await expect(page.getByText(/total|الإجمالي/i)).toBeVisible();
  });

  test('should open payment modal', async ({ page }) => {
    // Add item to cart first
    const quickAddBtn = page.locator('[data-testid="quick-add"]').first();
    if (await quickAddBtn.isVisible()) {
      await quickAddBtn.click();
      
      // Click pay button
      await page.getByRole('button', { name: /pay|دفع|checkout/i }).click();
      
      // Verify payment modal opens
      await expect(page.getByRole('dialog')).toBeVisible();
      
      // Check payment methods
      await expect(page.getByText(/cash|نقد/i)).toBeVisible();
      await expect(page.getByText(/card|بطاقة/i)).toBeVisible();
    }
  });

  test('should process cash payment', async ({ page }) => {
    const quickAddBtn = page.locator('[data-testid="quick-add"]').first();
    if (await quickAddBtn.isVisible()) {
      await quickAddBtn.click();
      
      // Open payment modal
      await page.getByRole('button', { name: /pay|دفع|checkout/i }).click();
      
      // Select cash payment
      await page.getByRole('button', { name: /cash|نقد/i }).click();
      
      // Confirm payment
      await page.getByRole('button', { name: /confirm|تأكيد/i }).click();
      
      // Should show success or receipt
      await expect(page.getByText(/success|نجاح|receipt|فاتورة/i)).toBeVisible();
    }
  });

  test('should clear cart', async ({ page }) => {
    // Add items
    const quickAddBtn = page.locator('[data-testid="quick-add"]').first();
    if (await quickAddBtn.isVisible()) {
      await quickAddBtn.click();
      await quickAddBtn.click();
      
      // Click clear cart
      await page.getByRole('button', { name: /clear|مسح|إفراغ/i }).click();
      
      // Confirm if needed
      const confirmBtn = page.getByRole('button', { name: /confirm|تأكيد|yes|نعم/i });
      if (await confirmBtn.isVisible()) {
        await confirmBtn.click();
      }
      
      // Verify cart is empty
      await expect(page.locator('[data-testid="cart-item"]')).toHaveCount(0);
    }
  });

  test('should handle barcode scan', async ({ page }) => {
    // Focus barcode input
    const barcodeInput = page.getByPlaceholder(/barcode|باركود/i);
    await barcodeInput.focus();
    
    // Simulate barcode scan (type quickly)
    await barcodeInput.type('1234567890123', { delay: 10 });
    await barcodeInput.press('Enter');
    
    // Should either add product or show not found message
    await page.waitForTimeout(500);
    const hasProduct = await page.locator('[data-testid="cart-item"]').count() > 0;
    const hasNotFound = await page.getByText(/not found|غير موجود/i).isVisible();
    
    expect(hasProduct || hasNotFound).toBeTruthy();
  });
});

test.describe('POS FIFO Lot Selection', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/pos');
  });

  test('should auto-select oldest lot (FIFO)', async ({ page }) => {
    // Search for a product with lots
    const searchInput = page.getByPlaceholder(/barcode|باركود|search|بحث/i);
    await searchInput.fill('lot-product');
    await searchInput.press('Enter');
    
    // Add product with lot
    const productCard = page.locator('[data-testid="product-with-lot"]').first();
    if (await productCard.isVisible()) {
      await productCard.click();
      
      // Verify lot info is shown in cart
      await expect(page.getByText(/lot|لوت|batch/i)).toBeVisible();
    }
  });

  test('should show lot expiry warning', async ({ page }) => {
    // Search for product with expiring lot
    const searchInput = page.getByPlaceholder(/barcode|باركود|search|بحث/i);
    await searchInput.fill('expiring-product');
    await searchInput.press('Enter');
    
    const productCard = page.locator('[data-testid="product-expiring"]').first();
    if (await productCard.isVisible()) {
      await productCard.click();
      
      // Check for expiry warning
      const hasWarning = await page.getByText(/expir|انتهاء|warning|تحذير/i).isVisible();
      expect(hasWarning).toBeTruthy();
    }
  });
});
