import { test, expect } from '@playwright/test';
import { saveScreenshot } from '../utils/artifacts.js';

const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 720 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'mobile', width: 375, height: 667 },
];

const ROUTES = ['/', '/login', '/dashboard', '/products', '/invoices'];

test.describe('RORLOC - Responsive baseline', () => {
  test('capture responsive screenshots for key routes', async ({ page, browserName }) => {
    test.skip(browserName !== 'chromium', 'Screenshots only from chromium');

    // Login once for protected pages (robust: wait for login XHR + dashboard signal)
    await page.goto('/login');
    await page.getByTestId('username-input').fill('admin');
    await page.getByTestId('password-input').fill('admin123');

    const [loginResponse] = await Promise.all([
      page.waitForResponse((response) =>
        response.url().endsWith('/api/auth/login') &&
        response.request().method() === 'POST'
      ),
      page.getByRole('button', { name: /log in|تسجيل الدخول/i }).click(),
    ]);

    if (!loginResponse.ok()) {
      const status = loginResponse.status();
      let bodyText;
      try {
        bodyText = await loginResponse.text();
      } catch {
        bodyText = '<no body>';
      }
      throw new Error(`Login failed in responsive-baseline.spec: HTTP ${status} — ${bodyText}`);
    }

    await Promise.race([
      page.waitForURL(/\/(dashboard|)$/i, { timeout: 15000 }),
      page.waitForSelector('[data-testid="user-menu"]', { state: 'visible', timeout: 15000 })
    ]);

    for (const viewport of VIEWPORTS) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });

      for (const route of ROUTES) {
        await page.goto(route, { waitUntil: 'networkidle' });

        const name = `${viewport.name}_${route === '/' ? 'root' : route.replace(/\//g, '_')}`;

        await saveScreenshot(page, name);

        // Basic assertion that page rendered some content
        const hasBody = await page.locator('body').isVisible();
        expect(hasBody).toBeTruthy();
      }
    }
  });
});

