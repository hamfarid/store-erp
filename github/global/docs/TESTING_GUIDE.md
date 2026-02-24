# 🧪 Testing Guide - Store ERP v2.0.0

**Phase 5: Testing**
**Generated:** 2026-01-16
**Status:** Ready

---

## 📋 Overview

Store ERP v2.0.0 includes comprehensive testing:

| Test Type | Framework | Coverage Target |
|-----------|-----------|-----------------|
| Unit Tests | Vitest (Frontend) / Pytest (Backend) | 80%+ |
| E2E Tests | Playwright | Critical flows |
| Performance Tests | Playwright + Custom | Response times |
| Security Tests | Playwright + Custom | OWASP Top 10 |

---

## 🚀 Quick Start

### Install Dependencies

```bash
# E2E Tests
cd e2e
npm install
npx playwright install

# Frontend Unit Tests
cd frontend
npm install

# Backend Tests
cd backend
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# E2E Tests
cd e2e
npm test

# Frontend Unit Tests
cd frontend
npm test

# Backend Tests
cd backend
pytest
```

---

## 📂 Test Structure

```
store/
├── e2e/                          # E2E Tests
│   ├── playwright.config.ts      # Playwright configuration
│   ├── package.json              # Test dependencies
│   └── tests/
│       ├── auth.spec.ts          # Authentication tests
│       ├── pos.spec.ts           # POS system tests
│       ├── lots.spec.ts          # Lot management tests
│       ├── reports.spec.ts       # Reports tests
│       ├── settings.spec.ts      # Settings tests
│       ├── products.spec.ts      # Products tests
│       ├── invoices.spec.ts      # Invoices tests
│       ├── performance.spec.ts   # Performance tests
│       └── security.spec.ts      # Security tests
│
├── frontend/src/tests/           # Frontend Unit Tests
│   ├── setup.js                  # Test setup
│   ├── smoke.test.js             # Smoke tests
│   └── enhanced/                 # Component tests
│
└── backend/tests/                # Backend Tests
    ├── conftest.py               # Pytest fixtures
    ├── test_auth.py              # Auth API tests
    ├── test_products.py          # Products API tests
    └── test_security.py          # Security tests
```

---

## 🎭 E2E Testing with Playwright

### Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './tests',
  baseURL: 'http://localhost:6501',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
});
```

### Running Tests

```bash
# Run all E2E tests
npm test

# Run specific test file
npm run test:auth
npm run test:pos
npm run test:security

# Run with headed browser (visible)
npm run test:headed

# Run with debugging
npm run test:debug

# Run with UI mode
npm run test:ui

# Generate new tests
npm run codegen
```

### Test Reports

```bash
# View HTML report
npm run report

# Reports are generated in:
# - e2e/test-results/results.json
# - e2e/test-results/junit.xml
# - e2e/playwright-report/
```

---

## 🔐 Security Tests

### What's Tested

| Category | Tests |
|----------|-------|
| Authentication | Token security, session management |
| Authorization | RBAC, permission checks |
| Input Validation | XSS, SQL injection |
| CSRF | Token validation |
| Headers | Security headers |
| File Upload | Type validation |

### Running Security Tests

```bash
cd e2e
npm run test:security
```

### Sample Security Test

```typescript
test('should prevent XSS in product names', async ({ page }) => {
  await loginAsAdmin(page);
  await page.goto('/products');
  
  const xssPayload = '<script>alert("XSS")</script>';
  await page.getByLabel(/name/i).fill(xssPayload);
  await page.getByRole('button', { name: /save/i }).click();
  
  const pageContent = await page.content();
  expect(pageContent).not.toContain('<script>alert("XSS")');
});
```

---

## ⚡ Performance Tests

### Thresholds

| Metric | Target |
|--------|--------|
| Page Load | < 3000ms |
| API Response | < 1000ms |
| UI Interaction | < 500ms |
| First Contentful Paint | < 1500ms |
| Largest Contentful Paint | < 2500ms |
| Total JS Bundle | < 3MB |

### Running Performance Tests

```bash
cd e2e
npm run test:performance
```

### Sample Performance Test

```typescript
test('dashboard should load within threshold', async ({ page }) => {
  await loginAsAdmin(page);
  
  const start = Date.now();
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');
  const loadTime = Date.now() - start;
  
  console.log(`Dashboard load time: ${loadTime}ms`);
  expect(loadTime).toBeLessThan(3000);
});
```

---

## 🧩 Unit Tests

### Frontend (Vitest)

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

### Backend (Pytest)

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run with verbose output
pytest -v --tb=short
```

---

## 📊 Coverage Requirements

### Frontend Coverage

```javascript
// vitest.config.js
coverage: {
  provider: 'v8',
  reporter: ['text', 'json', 'html'],
  threshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    }
  }
}
```

### Backend Coverage

```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd e2e
          npm ci
          npx playwright install --with-deps
      
      - name: Run E2E tests
        run: |
          cd e2e
          npm test
      
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: e2e/playwright-report/
```

---

## 🛠️ Writing New Tests

### E2E Test Template

```typescript
import { test, expect, Page } from '@playwright/test';

// Helper function for login
async function loginAsAdmin(page: Page) {
  await page.goto('/login');
  await page.getByLabel(/username/i).fill('admin');
  await page.getByLabel(/password/i).fill('admin123');
  await page.getByRole('button', { name: /login/i }).click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  test('should do something', async ({ page }) => {
    await page.goto('/feature');
    await expect(page.getByText('Expected Text')).toBeVisible();
  });
});
```

### Best Practices

1. **Use semantic locators**
   ```typescript
   // Good
   page.getByRole('button', { name: /submit/i })
   page.getByLabel(/email/i)
   
   // Avoid
   page.locator('#submit-btn')
   page.locator('.email-input')
   ```

2. **Support RTL/Arabic**
   ```typescript
   // Support both English and Arabic
   page.getByRole('button', { name: /save|حفظ/i })
   ```

3. **Handle async properly**
   ```typescript
   // Wait for element
   await expect(page.getByText('Success')).toBeVisible();
   
   // Wait for navigation
   await page.waitForURL(/dashboard/);
   ```

4. **Isolate tests**
   ```typescript
   test.beforeEach(async ({ page }) => {
     await page.evaluate(() => localStorage.clear());
   });
   ```

---

## 📝 Test Checklist

### Before PR

- [ ] All E2E tests pass
- [ ] Security tests pass
- [ ] Performance within thresholds
- [ ] Unit test coverage ≥ 80%
- [ ] No console errors
- [ ] RTL layout tested

### Before Release

- [ ] Full test suite passes
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile viewport testing
- [ ] Security audit complete
- [ ] Performance benchmarks documented

---

## 📈 Test Commands Summary

| Command | Description |
|---------|-------------|
| `npm test` | Run all E2E tests |
| `npm run test:auth` | Run authentication tests |
| `npm run test:pos` | Run POS tests |
| `npm run test:security` | Run security tests |
| `npm run test:performance` | Run performance tests |
| `npm run test:headed` | Run with visible browser |
| `npm run test:debug` | Run in debug mode |
| `npm run test:ui` | Run with Playwright UI |
| `npm run report` | View HTML report |
| `npm run codegen` | Generate tests |

---

*Testing Guide - Store ERP v2.0.0*
