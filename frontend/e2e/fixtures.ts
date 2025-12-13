import { test as base, expect } from '@playwright/test';

/**
 * Authentication fixture for Store ERP tests
 */
export const test = base.extend({
  // Authenticated page fixture
  authenticatedPage: async ({ page }, use) => {
    // Navigate to login
    await page.goto('/login');
    
    // Wait for login page to load
    await page.waitForSelector('input[name="username"]', { timeout: 5000 });
    
    // Fill in credentials (default admin)
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    
    // Wait for API response after clicking submit
    const [response] = await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/api/auth/login') && 
        (response.status() === 200 || response.status() === 401), 
        { timeout: 10000 }
      ),
      page.click('button[type="submit"]')
    ]);
    
    // Check if login was successful
    if (response.status() !== 200) {
      throw new Error(`Login failed with status ${response.status()}`);
    }
    
    // Get response data and set authentication in localStorage
    const responseData = await response.json();
    if (responseData?.data?.access_token) {
      // Store token and user data in localStorage
      await page.evaluate((data) => {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
      }, { 
        token: responseData.data.access_token,
        user: responseData.data.user || { username: 'admin', role: 'admin', email: 'admin@store.com' }
      });
      
      // Reload page to trigger auth context initialization with new localStorage data
      await page.reload({ waitUntil: 'networkidle' });
      
      // Verify we're now authenticated (should redirect away from login)
      await page.waitForURL(url => !url.pathname.includes('/login'), { timeout: 5000 });
    } else {
      throw new Error('No access token in login response');
    }
    
    // Wait for authenticated UI to be ready
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    
    await use(page);
  },
});

export { expect };

/**
 * Helper function to get JWT token from localStorage
 */
export async function getAuthToken(page) {
  return await page.evaluate(() => {
    return localStorage.getItem('token');
  });
}

/**
 * Helper function to wait for API response
 */
export async function waitForApiResponse(page, urlPattern) {
  return await page.waitForResponse(
    response => response.url().includes(urlPattern) && response.status() === 200
  );
}

/**
 * Helper function to fill form field by label
 */
export async function fillFieldByLabel(page, label, value) {
  const field = page.locator(`label:has-text("${label}")`).locator('..').locator('input, textarea, select');
  await field.fill(value);
}

/**
 * Helper function to click button by text
 */
export async function clickButtonByText(page, text) {
  await page.locator(`button:has-text("${text}")`).click();
}

/**
 * Helper function to verify toast notification
 */
export async function verifyToast(page, message, type = 'success') {
  const toast = page.locator(`.toast-${type}:has-text("${message}")`);
  await expect(toast).toBeVisible({ timeout: 5000 });
}

/**
 * Helper function to open modal by title
 */
export async function openModalByTitle(page, title) {
  const modal = page.locator(`[role="dialog"]:has-text("${title}")`);
  await expect(modal).toBeVisible({ timeout: 5000 });
  return modal;
}

/**
 * Helper function to close modal
 */
export async function closeModal(page) {
  // Try multiple close mechanisms
  const closeButton = page.locator('button:has-text("إغلاق"), button[aria-label="Close"], button.close-button').first();
  if (await closeButton.isVisible()) {
    await closeButton.click();
  } else {
    await page.keyboard.press('Escape');
  }
}
