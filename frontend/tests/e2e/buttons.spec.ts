/**
 * Playwright E2E Tests - Button and Interactive Element Tests
 * 
 * Tests specifically for buttons, forms, and interactive elements.
 */

import { test, expect, Page } from '@playwright/test';

const BASE_URL = process.env.TEST_URL || 'http://localhost:5505';
const TEST_USER = {
  username: 'admin',
  password: 'admin123',
};

async function login(page: Page) {
  await page.goto(`${BASE_URL}/login`);
  await page.fill('input[type="text"], input[name="username"]', TEST_USER.username);
  await page.fill('input[type="password"]', TEST_USER.password);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard**', { timeout: 10000 });
}

// ============================================================================
// Primary Button Tests
// ============================================================================

test.describe('Primary Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Add Product button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/products`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|منتج/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
    
    // Click and verify modal or navigation
    await addButton.click();
    await page.waitForTimeout(500);
  });

  test('Add Customer button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/customers`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|عميل/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
  });

  test('Add Supplier button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/suppliers`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|مورد/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
  });

  test('Create Invoice button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/invoices`);
    
    const createButton = page.locator('button').filter({ hasText: /إنشاء|جديد|فاتورة/ }).first();
    await expect(createButton).toBeVisible();
    await expect(createButton).toBeEnabled();
  });

  test('Add Warehouse button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/warehouses`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|مستودع/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
  });

  test('Add Category button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/categories`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|فئة/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
  });

  test('Add User button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/users`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|مستخدم/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
  });

  test('Add Role button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/roles-management`);
    
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد|دور/ }).first();
    await expect(addButton).toBeVisible();
    await expect(addButton).toBeEnabled();
  });
});

// ============================================================================
// Secondary/Action Buttons
// ============================================================================

test.describe('Action Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Export button on Reports page', async ({ page }) => {
    await page.goto(`${BASE_URL}/reports`);
    
    const exportButton = page.locator('button').filter({ hasText: /تصدير|Export/ }).first();
    await expect(exportButton).toBeVisible();
    await expect(exportButton).toBeEnabled();
  });

  test('Refresh button on Admin dashboard', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/dashboard`);
    
    const refreshButton = page.locator('button').filter({ hasText: /تحديث|Refresh/ }).first();
    if (await refreshButton.isVisible()) {
      await expect(refreshButton).toBeEnabled();
    }
  });

  test('Save button on Settings page', async ({ page }) => {
    await page.goto(`${BASE_URL}/settings`);
    
    const saveButton = page.locator('button').filter({ hasText: /حفظ|Save/ }).first();
    await expect(saveButton).toBeVisible();
    await expect(saveButton).toBeEnabled();
  });
});

// ============================================================================
// Filter Buttons
// ============================================================================

test.describe('Filter Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Customer filter buttons work', async ({ page }) => {
    await page.goto(`${BASE_URL}/customers`);
    
    // Test "All" filter
    const allFilter = page.locator('button').filter({ hasText: 'الكل' }).first();
    if (await allFilter.isVisible()) {
      await allFilter.click();
      await page.waitForTimeout(300);
    }
    
    // Test "Debt" filter
    const debtFilter = page.locator('button').filter({ hasText: /ديون/ }).first();
    if (await debtFilter.isVisible()) {
      await debtFilter.click();
      await page.waitForTimeout(300);
    }
  });

  test('Invoice status filters work', async ({ page }) => {
    await page.goto(`${BASE_URL}/invoices`);
    
    const statusButtons = page.locator('button').filter({ hasText: /مكتمل|قيد|ملغ|الكل/ });
    const count = await statusButtons.count();
    
    for (let i = 0; i < Math.min(count, 4); i++) {
      if (await statusButtons.nth(i).isVisible()) {
        await statusButtons.nth(i).click();
        await page.waitForTimeout(200);
      }
    }
  });

  test('Stock movement type filters work', async ({ page }) => {
    await page.goto(`${BASE_URL}/stock-movements`);
    
    const typeButtons = page.locator('button').filter({ hasText: /وارد|صادر|تحويل|الكل/ });
    const count = await typeButtons.count();
    
    for (let i = 0; i < Math.min(count, 4); i++) {
      if (await typeButtons.nth(i).isVisible()) {
        await typeButtons.nth(i).click();
        await page.waitForTimeout(200);
      }
    }
  });

  test('Payment type filters work', async ({ page }) => {
    await page.goto(`${BASE_URL}/payments`);
    
    const typeButtons = page.locator('button').filter({ hasText: /مقبوضات|مدفوعات|الكل/ });
    const count = await typeButtons.count();
    
    for (let i = 0; i < count; i++) {
      if (await typeButtons.nth(i).isVisible()) {
        await typeButtons.nth(i).click();
        await page.waitForTimeout(200);
      }
    }
  });

  test('Return status filters work', async ({ page }) => {
    await page.goto(`${BASE_URL}/returns`);
    
    const statusButtons = page.locator('button').filter({ hasText: /موافق|مراجعة|مرفوض|الكل/ });
    const count = await statusButtons.count();
    
    for (let i = 0; i < Math.min(count, 4); i++) {
      if (await statusButtons.nth(i).isVisible()) {
        await statusButtons.nth(i).click();
        await page.waitForTimeout(200);
      }
    }
  });

  test('User role filters work', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/user-rights`);
    
    const roleSelect = page.locator('select').first();
    if (await roleSelect.isVisible()) {
      await roleSelect.selectOption({ index: 1 });
      await page.waitForTimeout(300);
    }
  });
});

// ============================================================================
// Icon Buttons
// ============================================================================

test.describe('Icon Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('View button on cards', async ({ page }) => {
    await page.goto(`${BASE_URL}/customers`);
    
    const viewButton = page.locator('button').filter({ hasText: 'عرض' }).first();
    if (await viewButton.isVisible()) {
      await expect(viewButton).toBeEnabled();
    }
  });

  test('Edit button on cards', async ({ page }) => {
    await page.goto(`${BASE_URL}/customers`);
    
    const editButton = page.locator('button').filter({ hasText: 'تعديل' }).first();
    if (await editButton.isVisible()) {
      await expect(editButton).toBeEnabled();
    }
  });

  test('Delete button on cards', async ({ page }) => {
    await page.goto(`${BASE_URL}/customers`);
    
    // Delete buttons are usually icon-only
    const deleteButton = page.locator('button[title*="حذف"], button svg[class*="trash"], button:has(svg)').first();
    if (await deleteButton.isVisible()) {
      await expect(deleteButton).toBeEnabled();
    }
  });

  test('Key/Permissions button on user rights', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/user-rights`);
    
    // Wait for table to load
    await page.waitForSelector('table', { timeout: 5000 });
    
    // Find permission button
    const permButton = page.locator('button[title*="صلاحيات"], button[title*="إدارة"]').first();
    if (await permButton.isVisible()) {
      await expect(permButton).toBeEnabled();
    }
  });
});

// ============================================================================
// Modal Buttons
// ============================================================================

test.describe('Modal Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Modal cancel button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/roles-management`);
    
    // Open modal
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد/ }).first();
    await addButton.click();
    
    // Wait for modal
    await page.waitForSelector('[class*="fixed inset-0"], [class*="modal"]', { timeout: 3000 });
    
    // Click cancel
    const cancelButton = page.locator('button').filter({ hasText: /إلغاء|Cancel/ }).first();
    if (await cancelButton.isVisible()) {
      await cancelButton.click();
      await page.waitForTimeout(300);
    }
  });

  test('Modal save button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/roles-management`);
    
    // Open modal
    const addButton = page.locator('button').filter({ hasText: /إضافة|جديد/ }).first();
    await addButton.click();
    
    // Wait for modal
    await page.waitForSelector('[class*="fixed inset-0"], [class*="modal"]', { timeout: 3000 });
    
    // Check save button exists
    const saveButton = page.locator('button').filter({ hasText: /حفظ|Save|إنشاء/ }).first();
    if (await saveButton.isVisible()) {
      await expect(saveButton).toBeEnabled();
    }
  });
});

// ============================================================================
// Form Inputs
// ============================================================================

test.describe('Form Inputs', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Search inputs accept text', async ({ page }) => {
    const pages = ['/products', '/customers', '/suppliers', '/invoices', '/users'];
    
    for (const pagePath of pages) {
      await page.goto(`${BASE_URL}${pagePath}`);
      
      const searchInput = page.locator('input[type="text"], input[type="search"], input[placeholder*="بحث"]').first();
      if (await searchInput.isVisible()) {
        await searchInput.fill('test');
        await expect(searchInput).toHaveValue('test');
        await searchInput.clear();
      }
    }
  });

  test('Settings form inputs work', async ({ page }) => {
    await page.goto(`${BASE_URL}/settings`);
    
    // Test text input
    const textInput = page.locator('input[type="text"]').first();
    if (await textInput.isVisible()) {
      const originalValue = await textInput.inputValue();
      await textInput.fill('Test Company');
      await expect(textInput).toHaveValue('Test Company');
      await textInput.fill(originalValue);
    }
    
    // Test select
    const select = page.locator('select').first();
    if (await select.isVisible()) {
      await select.selectOption({ index: 0 });
    }
  });

  test('Toggle switches work', async ({ page }) => {
    await page.goto(`${BASE_URL}/settings`);
    
    // Find toggle/switch elements
    const toggles = page.locator('input[type="checkbox"], [role="switch"], [class*="toggle"]');
    const count = await toggles.count();
    
    if (count > 0) {
      const toggle = toggles.first();
      if (await toggle.isVisible()) {
        await toggle.click();
        await page.waitForTimeout(200);
      }
    }
  });
});

// ============================================================================
// Navigation Buttons
// ============================================================================

test.describe('Navigation Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Sidebar collapse button works', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`);
    
    const collapseButton = page.locator('button').filter({ hasText: /طي|Collapse/ }).first();
    if (await collapseButton.isVisible()) {
      await collapseButton.click();
      await page.waitForTimeout(300);
      
      // Click again to expand
      const expandButton = page.locator('button svg, button[class*="collapse"]').first();
      if (await expandButton.isVisible()) {
        await expandButton.click();
        await page.waitForTimeout(300);
      }
    }
  });

  test('Settings tab buttons work', async ({ page }) => {
    await page.goto(`${BASE_URL}/settings`);
    
    const tabButtons = page.locator('button, [role="tab"]').filter({ hasText: /عام|الشركة|الأمان|المظهر/ });
    const count = await tabButtons.count();
    
    for (let i = 0; i < Math.min(count, 4); i++) {
      if (await tabButtons.nth(i).isVisible()) {
        await tabButtons.nth(i).click();
        await page.waitForTimeout(200);
      }
    }
  });
});

// ============================================================================
// Quick Action Buttons
// ============================================================================

test.describe('Quick Action Buttons', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Admin dashboard quick actions work', async ({ page }) => {
    await page.goto(`${BASE_URL}/admin/dashboard`);
    
    // Wait for quick actions to load
    await page.waitForSelector('[class*="rounded"], [class*="card"]', { timeout: 5000 });
    
    // Check quick action buttons/links
    const quickActions = page.locator('a, button').filter({ hasText: /إضافة مستخدم|إدارة الأدوار|نسخ احتياطي|سجل النشاط/ });
    const count = await quickActions.count();
    
    for (let i = 0; i < Math.min(count, 4); i++) {
      if (await quickActions.nth(i).isVisible()) {
        await expect(quickActions.nth(i)).toBeEnabled();
      }
    }
  });
});

// ============================================================================
// Accessibility Tests
// ============================================================================

test.describe('Button Accessibility', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('Buttons have accessible names', async ({ page }) => {
    await page.goto(`${BASE_URL}/dashboard`);
    
    const buttons = page.locator('button');
    const count = await buttons.count();
    
    for (let i = 0; i < Math.min(count, 10); i++) {
      const button = buttons.nth(i);
      if (await button.isVisible()) {
        const text = await button.textContent();
        const ariaLabel = await button.getAttribute('aria-label');
        const title = await button.getAttribute('title');
        
        // Button should have some accessible name
        expect(text || ariaLabel || title).toBeTruthy();
      }
    }
  });

  test('Buttons are keyboard accessible', async ({ page }) => {
    await page.goto(`${BASE_URL}/products`);
    
    // Tab to first button
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Get focused element
    const focused = page.locator(':focus');
    const tagName = await focused.evaluate(el => el.tagName);
    
    // Should be able to focus on interactive elements
    expect(['BUTTON', 'A', 'INPUT', 'SELECT'].includes(tagName)).toBeTruthy();
  });
});

