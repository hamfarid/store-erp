import { test } from '@playwright/test';
import { writeJsonArtifact, runDbSchemaSnapshot } from '../utils/artifacts.js';

const ROUTES = [
  { path: '/', type: 'public' },
  { path: '/login', type: 'public' },
  { path: '/register', type: 'public' },
  { path: '/dashboard', type: 'protected' },
  { path: '/profile', type: 'protected' },
  { path: '/settings', type: 'protected' },
  { path: '/products', type: 'protected' },
  { path: '/invoices', type: 'protected' },
  { path: '/customers', type: 'protected' },
  { path: '/inventory', type: 'protected' },
  { path: '/reports', type: 'protected' },
  { path: '/admin', type: 'admin' },
  { path: '/admin/users', type: 'admin' },
  { path: '/admin/settings', type: 'admin' },
];

const API_BASE = process.env.API_BASE_URL || 'http://localhost:5002';

test.describe('RORLOC - Record baseline', () => {
  test('record site map, UI inventory, API and baseline issues', async ({ page, browserName }) => {
    test.skip(browserName !== 'chromium', 'Record baseline only once in chromium');

    const siteMap = [];
    const uiInventory = {};
    const apiInventory = [];
    const baselineIssues = [];

    page.on('console', (msg) => {
      const type = msg.type();
      if (type === 'error' || type === 'warning') {
        baselineIssues.push({
          kind: 'console',
          level: type,
          text: msg.text(),
          location: msg.location(),
        });
      }
    });

    page.on('pageerror', (error) => {
      baselineIssues.push({
        kind: 'pageerror',
        message: error.message || String(error),
      });
    });

    page.on('response', async (response) => {
      const url = response.url();
      if (!url.startsWith(API_BASE)) {
        return;
      }
      const request = response.request();
      apiInventory.push({
        method: request.method(),
        url: new URL(url).pathname,
        status: response.status(),
        ok: response.ok(),
      });
    });

    page.on('requestfailed', (request) => {
      const url = request.url();
      if (!url.startsWith(API_BASE)) {
        return;
      }
      const failure = request.failure();
      baselineIssues.push({
        kind: 'requestfailed',
        url,
        method: request.method(),
        error: failure ? failure.errorText : 'unknown',
      });
    });

    // Login once for protected routes (robust: wait for login XHR + dashboard signal)
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
      throw new Error(`Login failed in record.spec: HTTP ${status} — ${bodyText}`);
    }

    await Promise.race([
      page.waitForURL(/\/(dashboard|)$/i, { timeout: 15000 }),
      page.waitForSelector('[data-testid="user-menu"]', { state: 'visible', timeout: 15000 })
    ]);

    for (const route of ROUTES) {
      const start = Date.now();
      const response = await page.goto(route.path, { waitUntil: 'networkidle' });
      const loadTime = Date.now() - start;
      const status = response ? response.status() : null;
      const title = await page.title();
      const url = page.url();

      siteMap.push({
        path: route.path,
        type: route.type,
        url,
        status,
        title,
        loadTimeMs: loadTime,
        browser: browserName,
      });

      const buttons = await page.locator('button, [role="button"]').count();
      const inputs = await page.locator('input, textarea, select, [role="textbox"]').count();
      const links = await page.locator('a[href]').count();
      const tables = await page.locator('table').count();

      uiInventory[route.path] = {
        buttons,
        inputs,
        links,
        tables,
      };
    }

    await writeJsonArtifact('site-map.json', { routes: siteMap });
    await writeJsonArtifact('ui-inventory.json', { pages: uiInventory });
    await writeJsonArtifact('api-inventory.json', { api: apiInventory });
    await writeJsonArtifact('baseline-issues.json', { issues: baselineIssues });

    await runDbSchemaSnapshot();
  });
});

