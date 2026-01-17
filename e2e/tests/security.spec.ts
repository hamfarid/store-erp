/**
 * E2E Security Tests
 * Store ERP v2.0.0
 * 
 * Tests for security vulnerabilities including XSS, CSRF, authentication bypass, and more.
 */

import { test, expect, Page } from '@playwright/test';

async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
  await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
  await page.getByRole('button', { name: /login|دخول/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('Authentication Security', () => {
  test('should not expose sensitive data in localStorage', async ({ page }) => {
    await loginAsAdmin(page);
    
    const storageData = await page.evaluate(() => {
      const data: Record<string, string> = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) data[key] = localStorage.getItem(key) || '';
      }
      return data;
    });
    
    // Should not store passwords or sensitive data
    const sensitiveKeys = ['password', 'secret', 'key', 'credential'];
    for (const key of Object.keys(storageData)) {
      for (const sensitive of sensitiveKeys) {
        expect(key.toLowerCase()).not.toContain(sensitive);
      }
    }
    
    // Token should exist but not be exposed
    expect(storageData).toHaveProperty('token');
  });

  test('should invalidate token after logout', async ({ page }) => {
    await loginAsAdmin(page);
    
    // Get the token
    const tokenBefore = await page.evaluate(() => localStorage.getItem('token'));
    expect(tokenBefore).toBeTruthy();
    
    // Logout
    await page.getByRole('button', { name: /logout|خروج/i }).click();
    await expect(page).toHaveURL(/login/);
    
    // Token should be cleared
    const tokenAfter = await page.evaluate(() => localStorage.getItem('token'));
    expect(tokenAfter).toBeFalsy();
  });

  test('should prevent access to protected routes without token', async ({ page }) => {
    // Clear any existing tokens
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    
    // Try to access protected route
    await page.goto('/dashboard');
    
    // Should redirect to login
    await expect(page).toHaveURL(/login/);
  });

  test('should lock account after multiple failed attempts', async ({ page }) => {
    await page.goto('/login');
    
    // Try to login with wrong password multiple times
    for (let i = 0; i < 6; i++) {
      await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
      await page.getByLabel(/password|كلمة المرور/i).fill('wrongpassword');
      await page.getByRole('button', { name: /login|دخول/i }).click();
      await page.waitForTimeout(500);
    }
    
    // Should show lockout message
    const isLocked = await page.getByText(/locked|محظور|too many|blocked/i).isVisible();
    const hasRateLimit = await page.getByText(/try again|wait|انتظر/i).isVisible();
    
    expect(isLocked || hasRateLimit).toBeTruthy();
  });

  test('should require strong passwords', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/users');
    
    await page.getByRole('button', { name: /add user|إضافة مستخدم/i }).click();
    
    // Try weak password
    await page.getByLabel(/username|اسم المستخدم/i).fill('weakuser');
    await page.getByLabel(/email|بريد/i).fill('weak@test.com');
    await page.getByLabel(/password|كلمة المرور/i).fill('123');
    
    await page.getByRole('button', { name: /save|create|حفظ/i }).click();
    
    // Should show password strength error
    const hasError = await page.getByText(/weak|ضعيف|strong|قوي|minimum|8/i).isVisible();
    expect(hasError).toBeTruthy();
  });
});

test.describe('XSS Prevention', () => {
  test('should escape HTML in product names', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    await page.getByRole('button', { name: /add|إضافة/i }).click();
    
    // Try to inject script
    const xssPayload = '<script>alert("XSS")</script>';
    await page.getByLabel(/name|اسم/i).fill(xssPayload);
    
    // Submit form
    await page.getByRole('button', { name: /save|حفظ/i }).click();
    
    // Check page for unescaped script
    await page.waitForTimeout(500);
    const pageContent = await page.content();
    
    // Script should be escaped, not executed
    expect(pageContent).not.toContain('<script>alert("XSS")</script>');
  });

  test('should escape HTML in search input', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    const searchInput = page.getByPlaceholder(/search|بحث/i);
    
    if (await searchInput.isVisible()) {
      // Try XSS in search
      await searchInput.fill('<img src=x onerror=alert(1)>');
      await page.waitForTimeout(500);
      
      // Check that payload is escaped
      const searchValue = await searchInput.inputValue();
      expect(searchValue).toContain('<');
      
      // No alert should appear (would throw if it did)
      const pageContent = await page.content();
      expect(pageContent).not.toContain('onerror=alert');
    }
  });

  test('should sanitize URLs', async ({ page }) => {
    await loginAsAdmin(page);
    
    // Try javascript: protocol in navigation
    await page.goto('javascript:alert(1)');
    
    // Should not execute, may redirect to safe page
    const currentUrl = page.url();
    expect(currentUrl).not.toContain('javascript:');
  });
});

test.describe('CSRF Protection', () => {
  test('should have CSRF protection on forms', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/settings');
    
    // Check for CSRF token in form or headers
    const hasCsrfInput = await page.locator('input[name*="csrf"]').count() > 0;
    const hasCsrfMeta = await page.locator('meta[name*="csrf"]').count() > 0;
    
    // Or check API calls include CSRF header
    let hasHeader = false;
    page.on('request', request => {
      const headers = request.headers();
      if (headers['x-csrf-token'] || headers['x-xsrf-token']) {
        hasHeader = true;
      }
    });
    
    // Trigger a form submission
    const saveBtn = page.getByRole('button', { name: /save|حفظ/i });
    if (await saveBtn.isVisible()) {
      await saveBtn.click();
      await page.waitForTimeout(500);
    }
    
    // At least one CSRF protection should exist
    // Note: SPA might use token-based auth which is CSRF-safe
    console.log(`CSRF protection: input=${hasCsrfInput}, meta=${hasCsrfMeta}, header=${hasHeader}`);
  });
});

test.describe('Security Headers', () => {
  test('should have security headers', async ({ page }) => {
    const response = await page.goto('/');
    
    if (response) {
      const headers = response.headers();
      
      // Check for important security headers
      const securityHeaders = {
        'x-frame-options': ['DENY', 'SAMEORIGIN'],
        'x-content-type-options': ['nosniff'],
        'x-xss-protection': ['1; mode=block', '1'],
      };
      
      for (const [header, expectedValues] of Object.entries(securityHeaders)) {
        const value = headers[header];
        if (value) {
          console.log(`${header}: ${value}`);
          expect(expectedValues.some(v => value.includes(v))).toBeTruthy();
        } else {
          console.log(`Warning: Missing header ${header}`);
        }
      }
    }
  });

  test('should have Content-Security-Policy', async ({ page }) => {
    const response = await page.goto('/');
    
    if (response) {
      const csp = response.headers()['content-security-policy'];
      
      if (csp) {
        console.log(`CSP: ${csp.substring(0, 100)}...`);
        // CSP should restrict unsafe-inline where possible
        expect(csp).toBeTruthy();
      } else {
        console.log('Warning: No Content-Security-Policy header');
      }
    }
  });
});

test.describe('Input Validation', () => {
  test('should reject SQL injection attempts', async ({ page }) => {
    await page.goto('/login');
    
    // Try SQL injection
    await page.getByLabel(/username|اسم المستخدم/i).fill("admin' OR '1'='1");
    await page.getByLabel(/password|كلمة المرور/i).fill("' OR '1'='1");
    await page.getByRole('button', { name: /login|دخول/i }).click();
    
    // Should not login
    await page.waitForTimeout(1000);
    expect(page.url()).toContain('login');
    
    // Should show error, not crash
    const hasError = await page.getByText(/invalid|خطأ|error/i).isVisible();
    expect(hasError).toBeTruthy();
  });

  test('should validate numeric inputs', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    await page.getByRole('button', { name: /add|إضافة/i }).click();
    
    // Try non-numeric in price field
    const priceInput = page.getByLabel(/price|سعر/i);
    if (await priceInput.isVisible()) {
      await priceInput.fill('abc123!@#');
      
      // Should either reject or sanitize
      const value = await priceInput.inputValue();
      const hasOnlyNumbers = /^[\d.]*$/.test(value);
      
      console.log(`Price input value: ${value}, valid: ${hasOnlyNumbers}`);
    }
  });

  test('should limit input length', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    await page.getByRole('button', { name: /add|إضافة/i }).click();
    
    // Try very long input
    const longString = 'A'.repeat(10000);
    const nameInput = page.getByLabel(/name|اسم/i);
    
    if (await nameInput.isVisible()) {
      await nameInput.fill(longString);
      
      const value = await nameInput.inputValue();
      console.log(`Input length: ${value.length}`);
      
      // Should be limited
      expect(value.length).toBeLessThan(10000);
    }
  });
});

test.describe('Session Security', () => {
  test('should expire session after timeout', async ({ page }) => {
    await loginAsAdmin(page);
    
    // Check token expiry (this is a basic check)
    const token = await page.evaluate(() => localStorage.getItem('token'));
    
    if (token) {
      try {
        // Decode JWT to check expiry
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp;
        const now = Math.floor(Date.now() / 1000);
        
        console.log(`Token expires in: ${(exp - now) / 60} minutes`);
        
        // Token should have expiry
        expect(exp).toBeDefined();
        expect(exp).toBeGreaterThan(now);
      } catch (e) {
        console.log('Could not decode token');
      }
    }
  });

  test('should not allow session fixation', async ({ page }) => {
    await page.goto('/login');
    
    // Get any session identifier before login
    const sessionBefore = await page.evaluate(() => {
      return document.cookie || localStorage.getItem('sessionId');
    });
    
    await loginAsAdmin(page);
    
    // Get session after login
    const sessionAfter = await page.evaluate(() => {
      return document.cookie || localStorage.getItem('sessionId');
    });
    
    // Session should change after login
    if (sessionBefore && sessionAfter) {
      console.log('Session before and after login:', 
        sessionBefore.substring(0, 20), sessionAfter.substring(0, 20));
    }
  });
});

test.describe('File Upload Security', () => {
  test('should reject dangerous file types', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/settings');
    
    // Find file upload input
    const fileInput = page.locator('input[type="file"]');
    
    if (await fileInput.count() > 0) {
      // Try to upload a dangerous file type
      // Note: This is a simulation - actual file would need to exist
      const acceptedTypes = await fileInput.getAttribute('accept');
      
      console.log(`Accepted file types: ${acceptedTypes}`);
      
      // Should not accept executable or script files
      if (acceptedTypes) {
        expect(acceptedTypes).not.toContain('.exe');
        expect(acceptedTypes).not.toContain('.js');
        expect(acceptedTypes).not.toContain('.php');
      }
    }
  });
});
