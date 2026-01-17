================================================================================
MODULE 42: END-TO-END TESTING
================================================================================
Version: Latest
Last Updated: 2025-11-07
Purpose: Comprehensive E2E testing with Playwright and Cypress
================================================================================

## OVERVIEW

End-to-End (E2E) testing validates complete user workflows from start to finish.
This module covers E2E testing strategies, tools, and best practices.

================================================================================
## WHY E2E TESTING?
================================================================================

**Benefits:**
✓ Tests real user scenarios
✓ Catches integration issues
✓ Validates complete workflows
✓ Tests across browsers
✓ Simulates production environment
✓ Builds confidence before deployment

**When to Use:**
- Critical user flows (login, checkout, etc.)
- Multi-step processes
- Cross-page interactions
- Browser-specific issues
- Production-like validation

================================================================================
## TOOLS
================================================================================

### 1. Playwright (Recommended)
**Why:** Fast, reliable, multi-browser support, great API

```bash
# Installation
npm install -D @playwright/test
npx playwright install

# Run tests
npx playwright test
npx playwright test --headed
npx playwright test --debug
```

**Features:**
✓ Auto-wait for elements
✓ Network interception
✓ Screenshots/videos
✓ Multi-browser (Chrome, Firefox, Safari)
✓ Mobile emulation
✓ Parallel execution

### 2. Cypress (Alternative)
**Why:** Developer-friendly, great debugging, time-travel

```bash
# Installation
npm install -D cypress
npx cypress open

# Run tests
npx cypress run
npx cypress run --headed
```

**Features:**
✓ Real-time reloading
✓ Time-travel debugging
✓ Automatic screenshots
✓ Network stubbing
✓ Great documentation

### 3. MCP Integration
**Use:** chrome-devtools and playwright MCP servers

```bash
# List Playwright tools
manus-mcp-cli tool list --server playwright

# Run E2E test via MCP
manus-mcp-cli tool call run_test \
  --server playwright \
  --input '{"test_file": "tests/e2e/login.spec.ts"}'
```

================================================================================
## E2E TESTING STRUCTURE
================================================================================

### Directory Structure
```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── register.spec.ts
│   │   └── logout.spec.ts
│   ├── user/
│   │   ├── profile.spec.ts
│   │   └── settings.spec.ts
│   ├── admin/
│   │   ├── dashboard.spec.ts
│   │   └── users.spec.ts
│   └── fixtures/
│       ├── users.json
│       └── data.json
├── playwright.config.ts
└── cypress.config.ts
```

### Playwright Config
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

================================================================================
## WRITING E2E TESTS
================================================================================

### 1. Basic Test Structure (Playwright)

```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    // Arrange
    const email = 'user@example.com';
    const password = 'password123';

    // Act
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    await page.click('[data-testid="login-button"]');

    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-name"]')).toContainText('User');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    // Act
    await page.fill('[data-testid="email-input"]', 'wrong@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    await page.click('[data-testid="login-button"]');

    // Assert
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-message"]')).toContainText('Invalid credentials');
  });

  test('should validate required fields', async ({ page }) => {
    // Act
    await page.click('[data-testid="login-button"]');

    // Assert
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });
});
```

### 2. Page Object Model

```typescript
// tests/e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}

// Usage in test
import { LoginPage } from './pages/LoginPage';

test('login with page object', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### 3. Fixtures and Test Data

```typescript
// tests/e2e/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type AuthFixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'user@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});

// Usage
test('access protected page', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  await expect(authenticatedPage).toHaveURL('/profile');
});
```

================================================================================
## COMMON E2E SCENARIOS
================================================================================

### 1. Authentication Flow

```typescript
test.describe('Complete Auth Flow', () => {
  test('register -> login -> logout', async ({ page }) => {
    // Register
    await page.goto('/register');
    await page.fill('[data-testid="name-input"]', 'New User');
    await page.fill('[data-testid="email-input"]', 'newuser@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="register-button"]');
    await expect(page).toHaveURL('/dashboard');

    // Logout
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/login');

    // Login again
    await page.fill('[data-testid="email-input"]', 'newuser@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="login-button"]');
    await expect(page).toHaveURL('/dashboard');
  });
});
```

### 2. CRUD Operations

```typescript
test.describe('User CRUD', () => {
  test('create -> read -> update -> delete user', async ({ authenticatedPage }) => {
    const page = authenticatedPage;

    // Create
    await page.goto('/admin/users');
    await page.click('[data-testid="add-user-button"]');
    await page.fill('[data-testid="name-input"]', 'Test User');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.click('[data-testid="save-button"]');
    await expect(page.locator('text=Test User')).toBeVisible();

    // Read
    await page.click('text=Test User');
    await expect(page.locator('[data-testid="user-name"]')).toHaveValue('Test User');

    // Update
    await page.fill('[data-testid="name-input"]', 'Updated User');
    await page.click('[data-testid="save-button"]');
    await expect(page.locator('text=Updated User')).toBeVisible();

    // Delete
    await page.click('[data-testid="delete-button"]');
    await page.click('[data-testid="confirm-delete"]');
    await expect(page.locator('text=Updated User')).not.toBeVisible();
  });
});
```

### 3. Form Validation

```typescript
test.describe('Form Validation', () => {
  test('validates all fields', async ({ page }) => {
    await page.goto('/contact');

    // Submit empty form
    await page.click('[data-testid="submit-button"]');

    // Check all error messages
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="message-error"]')).toBeVisible();

    // Fill valid data
    await page.fill('[data-testid="name-input"]', 'John Doe');
    await page.fill('[data-testid="email-input"]', 'john@example.com');
    await page.fill('[data-testid="message-input"]', 'Test message');

    // Submit
    await page.click('[data-testid="submit-button"]');

    // Check success
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });
});
```

### 4. API Mocking

```typescript
test('mocks API responses', async ({ page }) => {
  // Mock API
  await page.route('**/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'User 1' },
        { id: 2, name: 'User 2' },
      ]),
    });
  });

  await page.goto('/users');
  await expect(page.locator('text=User 1')).toBeVisible();
  await expect(page.locator('text=User 2')).toBeVisible();
});
```

### 5. File Upload

```typescript
test('uploads file', async ({ page }) => {
  await page.goto('/upload');

  // Set file input
  const fileInput = page.locator('[data-testid="file-input"]');
  await fileInput.setInputFiles('path/to/file.pdf');

  // Submit
  await page.click('[data-testid="upload-button"]');

  // Check success
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  await expect(page.locator('text=file.pdf')).toBeVisible();
});
```

================================================================================
## BEST PRACTICES
================================================================================

### 1. Use data-testid Attributes

```html
<!-- Good -->
<button data-testid="login-button">Login</button>

<!-- Avoid -->
<button class="btn btn-primary">Login</button>
```

**Why:** data-testid is stable and doesn't change with styling.

### 2. Wait for Elements Properly

```typescript
// Good - Playwright auto-waits
await page.click('[data-testid="button"]');

// Good - Explicit wait
await page.waitForSelector('[data-testid="button"]');

// Avoid - Hard-coded delays
await page.waitForTimeout(3000); // ❌
```

### 3. Use Assertions

```typescript
// Good - Multiple assertions
await expect(page).toHaveURL('/dashboard');
await expect(page.locator('[data-testid="title"]')).toBeVisible();
await expect(page.locator('[data-testid="title"]')).toContainText('Dashboard');

// Avoid - No assertions
await page.goto('/dashboard'); // ❌ No verification
```

### 4. Clean Up After Tests

```typescript
test.afterEach(async ({ page }, testInfo) => {
  // Take screenshot on failure
  if (testInfo.status !== 'passed') {
    await page.screenshot({ path: `screenshots/${testInfo.title}.png` });
  }

  // Clean up test data
  await page.request.delete('/api/test-data');
});
```

### 5. Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: 4, // Run 4 tests in parallel
});

// Disable parallel for specific test
test.describe.configure({ mode: 'serial' });
```

================================================================================
## DEBUGGING
================================================================================

### 1. Headed Mode

```bash
# Run with browser visible
npx playwright test --headed

# Run with slow motion
npx playwright test --headed --slow-mo=1000
```

### 2. Debug Mode

```bash
# Open Playwright Inspector
npx playwright test --debug

# Debug specific test
npx playwright test login.spec.ts --debug
```

### 3. Screenshots and Videos

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on-first-retry',
  },
});
```

### 4. Console Logs

```typescript
// Listen to console
page.on('console', msg => console.log('Browser:', msg.text()));

// Listen to errors
page.on('pageerror', error => console.error('Error:', error));
```

================================================================================
## CI/CD INTEGRATION
================================================================================

### GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npx playwright test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

================================================================================
## CHECKLIST
================================================================================

BEFORE WRITING TESTS:
────────────────────────────────────────────────────────────────────────────
☐ Install Playwright/Cypress
☐ Configure test environment
☐ Add data-testid to elements
☐ Set up test database
☐ Create test fixtures

WRITING TESTS:
────────────────────────────────────────────────────────────────────────────
☐ Test critical user flows
☐ Test error scenarios
☐ Test form validation
☐ Test authentication
☐ Test CRUD operations
☐ Use Page Object Model
☐ Add proper assertions
☐ Mock external APIs

AFTER WRITING TESTS:
────────────────────────────────────────────────────────────────────────────
☐ Run tests locally
☐ Run tests in CI/CD
☐ Check test coverage
☐ Review test reports
☐ Fix flaky tests
☐ Document test scenarios

================================================================================
## REMEMBER
================================================================================

✓ Test real user scenarios
✓ Use stable selectors (data-testid)
✓ Wait for elements properly
✓ Add meaningful assertions
✓ Clean up test data
✓ Run tests in CI/CD
✓ Debug failures thoroughly
✓ Keep tests maintainable

E2E tests are your safety net - invest in them!
================================================================================

