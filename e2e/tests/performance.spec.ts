/**
 * E2E Performance Tests
 * Store ERP v2.0.0
 * 
 * Tests for application performance including load times, API response times, and resource usage.
 */

import { test, expect, Page } from '@playwright/test';

// Performance thresholds (in milliseconds)
const THRESHOLDS = {
  PAGE_LOAD: 3000,        // Max page load time
  API_RESPONSE: 1000,     // Max API response time
  INTERACTION: 500,       // Max UI interaction time
  FIRST_PAINT: 1500,      // First Contentful Paint
  LCP: 2500,              // Largest Contentful Paint
};

async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
  await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
  await page.getByRole('button', { name: /login|دخول/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('Page Load Performance', () => {
  test('login page should load quickly', async ({ page }) => {
    const start = Date.now();
    await page.goto('/login');
    await page.waitForLoadState('domcontentloaded');
    const loadTime = Date.now() - start;
    
    console.log(`Login page load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(THRESHOLDS.PAGE_LOAD);
  });

  test('dashboard should load within threshold', async ({ page }) => {
    await loginAsAdmin(page);
    
    const start = Date.now();
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - start;
    
    console.log(`Dashboard load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(THRESHOLDS.PAGE_LOAD);
  });

  test('POS page should load quickly', async ({ page }) => {
    await loginAsAdmin(page);
    
    const start = Date.now();
    await page.goto('/pos');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - start;
    
    console.log(`POS page load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(THRESHOLDS.PAGE_LOAD);
  });

  test('products list should load within threshold', async ({ page }) => {
    await loginAsAdmin(page);
    
    const start = Date.now();
    await page.goto('/products');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - start;
    
    console.log(`Products page load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(THRESHOLDS.PAGE_LOAD);
  });

  test('reports page should load within threshold', async ({ page }) => {
    await loginAsAdmin(page);
    
    const start = Date.now();
    await page.goto('/reports');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - start;
    
    console.log(`Reports page load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(THRESHOLDS.PAGE_LOAD);
  });
});

test.describe('API Response Performance', () => {
  test('login API should respond quickly', async ({ page }) => {
    await page.goto('/login');
    
    const responsePromise = page.waitForResponse(response => 
      response.url().includes('/api/auth/login') && response.status() !== 0
    );
    
    const start = Date.now();
    await page.getByLabel(/username|اسم المستخدم/i).fill('admin');
    await page.getByLabel(/password|كلمة المرور/i).fill('admin123');
    await page.getByRole('button', { name: /login|دخول/i }).click();
    
    await responsePromise;
    const responseTime = Date.now() - start;
    
    console.log(`Login API response time: ${responseTime}ms`);
    expect(responseTime).toBeLessThan(THRESHOLDS.API_RESPONSE * 2); // Allow more for auth
  });

  test('products API should respond quickly', async ({ page }) => {
    await loginAsAdmin(page);
    
    const responsePromise = page.waitForResponse(response => 
      response.url().includes('/api/products')
    );
    
    const start = Date.now();
    await page.goto('/products');
    await responsePromise;
    const responseTime = Date.now() - start;
    
    console.log(`Products API response time: ${responseTime}ms`);
    expect(responseTime).toBeLessThan(THRESHOLDS.API_RESPONSE);
  });

  test('dashboard API calls should be fast', async ({ page }) => {
    await loginAsAdmin(page);
    
    const apiCalls: number[] = [];
    
    page.on('response', response => {
      if (response.url().includes('/api/') && response.status() !== 0) {
        const timing = response.timing();
        if (timing.responseEnd > 0) {
          apiCalls.push(timing.responseEnd);
        }
      }
    });
    
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    const avgTime = apiCalls.length > 0 
      ? apiCalls.reduce((a, b) => a + b, 0) / apiCalls.length 
      : 0;
    
    console.log(`Dashboard avg API response time: ${avgTime.toFixed(0)}ms`);
    expect(avgTime).toBeLessThan(THRESHOLDS.API_RESPONSE);
  });
});

test.describe('UI Interaction Performance', () => {
  test('search should respond quickly', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    const searchInput = page.getByPlaceholder(/search|بحث/i);
    
    if (await searchInput.isVisible()) {
      const start = Date.now();
      await searchInput.fill('test');
      await page.waitForTimeout(500); // Debounce time
      const interactionTime = Date.now() - start;
      
      console.log(`Search interaction time: ${interactionTime}ms`);
      expect(interactionTime).toBeLessThan(THRESHOLDS.INTERACTION * 2); // Including debounce
    }
  });

  test('modal should open quickly', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    const addButton = page.getByRole('button', { name: /add|إضافة/i });
    
    if (await addButton.isVisible()) {
      const start = Date.now();
      await addButton.click();
      await page.waitForSelector('[role="dialog"]');
      const openTime = Date.now() - start;
      
      console.log(`Modal open time: ${openTime}ms`);
      expect(openTime).toBeLessThan(THRESHOLDS.INTERACTION);
    }
  });

  test('table pagination should be fast', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    const nextPageBtn = page.getByRole('button', { name: /next|التالي|›/i });
    
    if (await nextPageBtn.isVisible()) {
      const start = Date.now();
      await nextPageBtn.click();
      await page.waitForTimeout(300);
      const paginateTime = Date.now() - start;
      
      console.log(`Pagination time: ${paginateTime}ms`);
      expect(paginateTime).toBeLessThan(THRESHOLDS.INTERACTION * 2);
    }
  });
});

test.describe('Core Web Vitals', () => {
  test('should measure LCP on dashboard', async ({ page }) => {
    await loginAsAdmin(page);
    
    // Enable Performance API
    await page.goto('/dashboard');
    
    const lcp = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          resolve(lastEntry.startTime);
        }).observe({ type: 'largest-contentful-paint', buffered: true });
        
        // Fallback timeout
        setTimeout(() => resolve(0), 5000);
      });
    });
    
    console.log(`Dashboard LCP: ${lcp}ms`);
    if (lcp > 0) {
      expect(lcp).toBeLessThan(THRESHOLDS.LCP);
    }
  });

  test('should measure FCP', async ({ page }) => {
    await page.goto('/login');
    
    const fcp = await page.evaluate(() => {
      const paintEntries = performance.getEntriesByType('paint');
      const fcpEntry = paintEntries.find(entry => entry.name === 'first-contentful-paint');
      return fcpEntry ? fcpEntry.startTime : 0;
    });
    
    console.log(`Login FCP: ${fcp}ms`);
    if (fcp > 0) {
      expect(fcp).toBeLessThan(THRESHOLDS.FIRST_PAINT);
    }
  });
});

test.describe('Resource Usage', () => {
  test('should not have memory leaks after navigation', async ({ page }) => {
    await loginAsAdmin(page);
    
    // Navigate through multiple pages
    const pages = ['/dashboard', '/products', '/pos', '/reports', '/settings'];
    
    for (const path of pages) {
      await page.goto(path);
      await page.waitForLoadState('networkidle');
    }
    
    // Check for excessive DOM nodes
    const nodeCount = await page.evaluate(() => document.querySelectorAll('*').length);
    
    console.log(`DOM node count after navigation: ${nodeCount}`);
    expect(nodeCount).toBeLessThan(5000); // Reasonable threshold
  });

  test('should lazy load images', async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto('/products');
    
    const images = page.locator('img');
    const imageCount = await images.count();
    
    if (imageCount > 0) {
      // Check for lazy loading attribute
      const lazyImages = await images.evaluateAll(imgs => 
        imgs.filter(img => img.loading === 'lazy' || img.dataset.src).length
      );
      
      console.log(`Lazy loaded images: ${lazyImages}/${imageCount}`);
      // At least some images should be lazy loaded
      expect(lazyImages).toBeGreaterThan(0);
    }
  });
});

test.describe('Bundle Size Check', () => {
  test('should not load excessive JavaScript', async ({ page }) => {
    let totalJsSize = 0;
    
    page.on('response', async response => {
      if (response.url().endsWith('.js')) {
        const body = await response.body().catch(() => Buffer.alloc(0));
        totalJsSize += body.length;
      }
    });
    
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    
    const sizeMB = totalJsSize / (1024 * 1024);
    console.log(`Total JS bundle size: ${sizeMB.toFixed(2)} MB`);
    
    // Should be under 3MB for reasonable performance
    expect(sizeMB).toBeLessThan(3);
  });
});
