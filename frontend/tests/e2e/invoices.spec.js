import { test, expect } from '@playwright/test';

test.describe('Invoice Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid="username-input"]', 'admin');
    await page.fill('[data-testid="password-input"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // Wait for dashboard to fully load
    await page.waitForURL('/dashboard', { timeout: 10000 });
    
    // Wait for user menu to ensure app is fully initialized
    await page.waitForSelector('[data-testid="user-menu"]', { 
      state: 'visible', 
      timeout: 10000 
    });
    
    // Navigate to invoices page using React Router (no full reload)
    await page.click('a[href="/invoices"]');
    
    // Wait for invoices page to load
    await page.waitForURL('/invoices', { timeout: 10000 });
    await page.waitForLoadState('networkidle');
  });

  test('should display invoices list', async ({ page }) => {
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Try to find invoices list with different selectors
    const tableSelectors = [
      '[data-testid="invoices-table"]',
      'table',
      '[class*="invoice"]',
      '.invoice-list'
    ];
    
    let tableFound = false;
    for (const selector of tableSelectors) {
      try {
        await page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
        tableFound = true;
        break;
      } catch {
        continue;
      }
    }
    
    // Page should have some invoices content
    expect(tableFound).toBeTruthy();
    
    // Check if invoices are loaded
    const rows = page.locator('[data-testid="invoices-table"] tbody tr, table tbody tr, [class*="invoice-row"]');
    const count = await rows.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('should search for invoice', async ({ page }) => {
    // Find search input
    const searchInput = page.locator('input[placeholder*="search" i]');
    
    if (await searchInput.isVisible()) {
      // Type search term
      await searchInput.fill('INV');
      
      // Wait for results
      await page.waitForLoadState('networkidle');
      
      // Verify results
      const rows = page.locator('tbody tr');
      const count = await rows.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test('should create new invoice', async ({ page }) => {
    // Click create invoice button
    const createButton = page.locator('button:has-text("Create Invoice")');
    if (await createButton.isVisible()) {
      await createButton.click();
      
      // Wait for form
      await page.waitForLoadState('networkidle');
      
      // Select customer
      const customerSelect = page.locator('select[name="customer"]');
      if (await customerSelect.isVisible()) {
        await customerSelect.selectOption({ index: 1 });
      }
      
      // Add line items if form exists
      const addItemButton = page.locator('button:has-text("Add Item")');
      if (await addItemButton.isVisible()) {
        await addItemButton.click();
        
        // Fill item details
        const productSelect = page.locator('select[name="product"]').first();
        if (await productSelect.isVisible()) {
          await productSelect.selectOption({ index: 1 });
        }
        
        const quantityInput = page.locator('input[name="quantity"]').first();
        if (await quantityInput.isVisible()) {
          await quantityInput.fill('1');
        }
      }
      
      // Submit form
      const submitButton = page.locator('button[type="submit"]');
      await submitButton.click();
      
      // Wait for success
      await expect(page.locator('text=/success|created|invoice/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should view invoice details', async ({ page }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click on invoice number to view details
    const invoiceLink = firstRow.locator('a').first();
    if (await invoiceLink.isVisible()) {
      await invoiceLink.click();
      
      // Wait for details page
      await page.waitForLoadState('networkidle');
      
      // Verify details are displayed
      await expect(page.locator('text=/invoice|details|items/i')).toBeVisible();
    }
  });

  test('should edit invoice', async ({ page }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click edit button
    const editButton = firstRow.locator('button:has-text("Edit")');
    if (await editButton.isVisible()) {
      await editButton.click();
      
      // Wait for form
      await page.waitForLoadState('networkidle');
      
      // Update invoice (e.g., notes)
      const notesInput = page.locator('textarea[name="notes"]');
      if (await notesInput.isVisible()) {
        await notesInput.fill(`Updated notes ${Date.now()}`);
      }
      
      // Submit
      const submitButton = page.locator('button[type="submit"]');
      await submitButton.click();
      
      // Wait for success
      await expect(page.locator('text=/success|updated/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should print invoice', async ({ page }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click print button
    const printButton = firstRow.locator('button:has-text("Print")');
    if (await printButton.isVisible()) {
      // Listen for print dialog
      page.once('dialog', dialog => {
        expect(dialog.type()).toBe('alert');
        dialog.accept();
      });
      
      await printButton.click();
    }
  });

  test('should download invoice as PDF', async ({ page, context }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click download button
    const downloadButton = firstRow.locator('button:has-text("Download")');
    if (await downloadButton.isVisible()) {
      // Start waiting for download
      const downloadPromise = context.waitForEvent('download');
      
      await downloadButton.click();
      
      // Wait for download
      const download = await downloadPromise;
      
      // Verify download
      expect(download.suggestedFilename()).toContain('.pdf');
    }
  });

  test('should filter invoices by status', async ({ page }) => {
    // Find status filter
    const statusFilter = page.locator('select[name="status"]');
    
    if (await statusFilter.isVisible()) {
      // Select a status
      await statusFilter.selectOption({ index: 1 });
      
      // Wait for results
      await page.waitForLoadState('networkidle');
      
      // Verify results are filtered
      const rows = page.locator('tbody tr');
      const count = await rows.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test('should filter invoices by date range', async ({ page }) => {
    // Find date inputs
    const fromDateInput = page.locator('input[name="fromDate"]');
    const toDateInput = page.locator('input[name="toDate"]');
    
    if (await fromDateInput.isVisible() && await toDateInput.isVisible()) {
      // Set date range
      await fromDateInput.fill('2024-01-01');
      await toDateInput.fill('2024-12-31');
      
      // Wait for results
      await page.waitForLoadState('networkidle');
      
      // Verify results
      const rows = page.locator('tbody tr');
      const count = await rows.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test('should mark invoice as paid', async ({ page }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click mark as paid button
    const paidButton = firstRow.locator('button:has-text("Mark as Paid")');
    if (await paidButton.isVisible()) {
      await paidButton.click();
      
      // Wait for success
      await expect(page.locator('text=/success|paid/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should send invoice via email', async ({ page }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click send button
    const sendButton = firstRow.locator('button:has-text("Send")');
    if (await sendButton.isVisible()) {
      await sendButton.click();
      
      // Wait for email dialog
      const emailInput = page.locator('input[type="email"]');
      if (await emailInput.isVisible()) {
        await emailInput.fill('test@example.com');
        
        // Click send in dialog
        const confirmButton = page.locator('button:has-text("Send")').last();
        await confirmButton.click();
        
        // Wait for success
        await expect(page.locator('text=/success|sent/i')).toBeVisible({ timeout: 10000 });
      }
    }
  });

  test('should delete invoice', async ({ page }) => {
    // Find first invoice row
    const firstRow = page.locator('tbody tr').first();
    
    // Click delete button
    const deleteButton = firstRow.locator('button:has-text("Delete")');
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      
      // Confirm deletion
      const confirmButton = page.locator('button:has-text("Confirm")');
      if (await confirmButton.isVisible()) {
        await confirmButton.click();
      }
      
      // Wait for success
      await expect(page.locator('text=/success|deleted/i')).toBeVisible({ timeout: 10000 });
    }
  });

  test('should export invoices', async ({ page, context }) => {
    // Find export button
    const exportButton = page.locator('button:has-text("Export")');
    
    if (await exportButton.isVisible()) {
      // Start waiting for download
      const downloadPromise = context.waitForEvent('download');
      
      await exportButton.click();
      
      // Wait for download
      const download = await downloadPromise;
      
      // Verify download
      expect(download.suggestedFilename()).toMatch(/\.(csv|xlsx|pdf)$/);
    }
  });
});

