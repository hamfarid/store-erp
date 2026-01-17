# 75. RORLOC Testing Methodology

**Priority:** LEVEL 7 - Testing & Quality Assurance  
**Phase:** Phase 4 (Testing)  
**Status:** ⭐ MANDATORY  
**Prerequisites:** MODULE_MAP.md, TODO files, Complete implementation

---

## Overview

**RORLOC** is a comprehensive 6-phase testing methodology that ensures **zero hallucinations** and **100% quality** in full-stack applications.

**Phases:**
1. **Record** → Discovery & baselines
2. **Organize** → Categorize & prioritize
3. **Refactor** → Reuse & efficiency
4. **Locate** → Execute & find issues
5. **Optimize** → Close gaps & harden
6. **Confirm** → Regression & sign-off

---

## Prerequisites

### MANDATORY Files Must Exist

Before starting RORLOC testing:

1. ✅ **`docs/MODULE_MAP.md`** - Complete project structure
2. ✅ **`docs/TODO.md`** - All development tasks
3. ✅ **`docs/INCOMPLETE_TASKS.md`** - Pending items
4. ✅ **`docs/COMPLETE_TASKS.md`** - Finished work

### MANDATORY Implementation Complete

- ✅ All pages implemented
- ✅ All buttons functional
- ✅ Backend endpoints ready
- ✅ Database schema deployed
- ✅ No duplicate files

**If any prerequisite is missing:**
```
❌ CANNOT START RORLOC TESTING
→ Complete Phase 1-3 first
→ Run complete_system_checker.py
→ Achieve 100% implementation
```

---

## Environment Setup

### Tools Required

**Testing Framework:**
```bash
npm i -D @playwright/test typescript ts-node @types/node
npx playwright install --with-deps
```

**Accessibility:**
```bash
npm i -D @axe-core/playwright
```

**Database Drivers:**
```bash
# PostgreSQL
npm i pg

# MySQL/MariaDB
npm i mysql2

# MongoDB
npm i mongodb
```

### Configuration

**Create `playwright.config.ts`:**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: './artifacts/html-report' }],
    ['json', { outputFile: './artifacts/test-results.json' }],
    ['list']
  ],
  
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',
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
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: process.env.START_CMD || 'npm run start',
    url: process.env.BASE_URL || 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Environment Variables

Create `.env.test`:
```bash
# Application
BASE_URL=http://localhost:3000
START_CMD=npm run start

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DB_ENGINE=postgres

# API
OPENAPI_URL=http://localhost:3000/openapi.json

# Testing
MAX_PAGES=150
ALLOWED_4XX=[]
RETRIES=1
```

---

## Phase 1: RECORD (Discovery & Baselines)

**Objective:** Discover all application components and establish baseline behaviors.

### 1.1 Application Structure Discovery

**Task:** Crawl and map entire application

**Script:** `tests/discovery/crawl.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test.describe('RORLOC Phase 1: Record - Application Discovery', () => {
  const discoveredRoutes = new Set<string>();
  const uiInventory: any[] = [];
  
  test('discover all routes', async ({ page }) => {
    const baseURL = process.env.BASE_URL || 'http://localhost:3000';
    const maxPages = parseInt(process.env.MAX_PAGES || '150');
    
    await discoverRoutes(page, '/', baseURL, discoveredRoutes, maxPages);
    
    // Save site map
    fs.writeFileSync(
      './artifacts/site-map.json',
      JSON.stringify(Array.from(discoveredRoutes), null, 2)
    );
    
    console.log(`✅ Discovered ${discoveredRoutes.size} routes`);
  });
  
  test('record UI inventory', async ({ page }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      await page.goto(route);
      
      const elements = await page.$$eval(
        '[role="button"], button, a[role="button"], input, select, textarea, form',
        els => els.map(el => ({
          tag: el.tagName,
          type: el.getAttribute('type'),
          id: el.id,
          name: el.getAttribute('name'),
          text: el.textContent?.trim(),
          href: el.getAttribute('href'),
        }))
      );
      
      uiInventory.push({ route, elements });
    }
    
    fs.writeFileSync(
      './artifacts/ui-inventory.json',
      JSON.stringify(uiInventory, null, 2)
    );
    
    console.log(`✅ Recorded UI inventory for ${routes.length} routes`);
  });
});

async function discoverRoutes(
  page: any,
  currentPath: string,
  baseURL: string,
  discovered: Set<string>,
  maxPages: number
) {
  if (discovered.size >= maxPages || discovered.has(currentPath)) {
    return;
  }
  
  discovered.add(currentPath);
  
  try {
    await page.goto(`${baseURL}${currentPath}`);
    await page.waitForLoadState('networkidle');
    
    const links = await page.$$eval('a[href]', (anchors: any[]) =>
      anchors
        .map(a => a.href)
        .filter(href => href.startsWith(baseURL))
        .map(href => new URL(href).pathname)
    );
    
    for (const link of links) {
      await discoverRoutes(page, link, baseURL, discovered, maxPages);
    }
  } catch (error) {
    console.error(`Failed to discover ${currentPath}:`, error);
  }
}
```

### 1.2 API Surface Discovery

**Task:** Enumerate all API endpoints

**Script:** `tests/discovery/api-discovery.spec.ts`
```typescript
import { test } from '@playwright/test';
import * as fs from 'fs';

test.describe('RORLOC Phase 1: API Discovery', () => {
  const apiInventory: any[] = [];
  
  test('discover API endpoints via network traffic', async ({ page }) => {
    page.on('request', request => {
      const url = request.url();
      if (url.includes('/api/') || url.includes(':5002')) {
        apiInventory.push({
          method: request.method(),
          url: url,
          headers: request.headers(),
          timestamp: new Date().toISOString(),
        });
      }
    });
    
    page.on('response', async response => {
      const url = response.url();
      if (url.includes('/api/') || url.includes(':5002')) {
        const entry = apiInventory.find(e => e.url === url && !e.status);
        if (entry) {
          entry.status = response.status();
          entry.statusText = response.statusText();
          entry.timing = response.timing();
        }
      }
    });
    
    // Exercise UI to trigger API calls
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    for (const route of routes) {
      await page.goto(route);
      await page.waitForLoadState('networkidle');
    }
    
    fs.writeFileSync(
      './artifacts/api-inventory.json',
      JSON.stringify(apiInventory, null, 2)
    );
    
    console.log(`✅ Discovered ${apiInventory.length} API calls`);
  });
  
  test('fetch OpenAPI specification', async ({ request }) => {
    const openApiUrl = process.env.OPENAPI_URL || 'http://localhost:3000/openapi.json';
    
    try {
      const response = await request.get(openApiUrl);
      if (response.ok()) {
        const spec = await response.json();
        fs.writeFileSync('./artifacts/openapi.json', JSON.stringify(spec, null, 2));
        console.log('✅ OpenAPI specification saved');
      }
    } catch (error) {
      console.log('⚠️ OpenAPI not available');
    }
  });
});
```

### 1.3 Database Schema Snapshot

**Task:** Record database structure

**Script:** `utils/db.ts`
```typescript
import { Client } from 'pg'; // or mysql2, mongodb

export async function getDatabaseSchema() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
  });
  
  try {
    await client.connect();
    
    const tablesResult = await client.query(`
      SELECT table_name, column_name, data_type, is_nullable
      FROM information_schema.columns
      WHERE table_schema = 'public'
      ORDER BY table_name, ordinal_position
    `);
    
    const keysResult = await client.query(`
      SELECT
        tc.table_name,
        kcu.column_name,
        tc.constraint_type
      FROM information_schema.table_constraints tc
      JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
      WHERE tc.table_schema = 'public'
    `);
    
    return {
      tables: tablesResult.rows,
      constraints: keysResult.rows,
    };
  } finally {
    await client.end();
  }
}
```

**Test:** `tests/discovery/db-schema.spec.ts`
```typescript
import { test } from '@playwright/test';
import * as fs from 'fs';
import { getDatabaseSchema } from '../../utils/db';

test.describe('RORLOC Phase 1: Database Schema', () => {
  test('record database schema', async () => {
    if (!process.env.DATABASE_URL) {
      console.log('⚠️ DATABASE_URL not provided, skipping');
      return;
    }
    
    const schema = await getDatabaseSchema();
    
    fs.writeFileSync(
      './artifacts/db-schema.json',
      JSON.stringify(schema, null, 2)
    );
    
    console.log(`✅ Database schema recorded`);
  });
});
```

### 1.4 Responsive Baselines

**Task:** Capture screenshots at multiple viewports

**Script:** `tests/discovery/responsive.spec.ts`
```typescript
import { test } from '@playwright/test';
import * as fs from 'fs';

const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 },
  { name: 'large', width: 2560, height: 1440 },
];

test.describe('RORLOC Phase 1: Responsive Baselines', () => {
  for (const viewport of viewports) {
    test(`capture ${viewport.name} screenshots`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      
      const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
      
      for (const route of routes) {
        await page.goto(route);
        await page.waitForLoadState('networkidle');
        
        const filename = `${route.replace(/\//g, '_')}_${viewport.name}.png`;
        await page.screenshot({
          path: `./artifacts/screenshots/${filename}`,
          fullPage: true,
        });
      }
      
      console.log(`✅ ${viewport.name} screenshots captured`);
    });
  }
});
```

### 1.5 Error Baseline

**Task:** Record initial errors

**Script:** `tests/discovery/error-baseline.spec.ts`
```typescript
import { test } from '@playwright/test';
import * as fs from 'fs';

test.describe('RORLOC Phase 1: Error Baseline', () => {
  const baselineIssues: any[] = [];
  
  test('record baseline errors', async ({ page }) => {
    // Console errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        baselineIssues.push({
          type: 'console_error',
          message: msg.text(),
          timestamp: new Date().toISOString(),
        });
      }
    });
    
    // Page errors
    page.on('pageerror', error => {
      baselineIssues.push({
        type: 'page_error',
        message: error.message,
        stack: error.stack,
        timestamp: new Date().toISOString(),
      });
    });
    
    // Network failures
    page.on('requestfailed', request => {
      baselineIssues.push({
        type: 'network_failure',
        url: request.url(),
        failure: request.failure()?.errorText,
        timestamp: new Date().toISOString(),
      });
    });
    
    // HTTP errors
    page.on('response', response => {
      if (response.status() >= 400) {
        const allowed = JSON.parse(process.env.ALLOWED_4XX || '[]');
        if (!allowed.includes(response.status())) {
          baselineIssues.push({
            type: 'http_error',
            url: response.url(),
            status: response.status(),
            statusText: response.statusText(),
            timestamp: new Date().toISOString(),
          });
        }
      }
    });
    
    // Visit all routes
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    for (const route of routes) {
      await page.goto(route);
      await page.waitForLoadState('networkidle');
    }
    
    fs.writeFileSync(
      './artifacts/baseline-issues.json',
      JSON.stringify(baselineIssues, null, 2)
    );
    
    console.log(`✅ Baseline issues recorded: ${baselineIssues.length}`);
  });
});
```

### Phase 1 Deliverable

**Discovery Bundle:**
- ✅ `artifacts/site-map.json` - All routes
- ✅ `artifacts/ui-inventory.json` - All UI elements
- ✅ `artifacts/api-inventory.json` - All API endpoints
- ✅ `artifacts/openapi.json` - API specification (if available)
- ✅ `artifacts/db-schema.json` - Database structure
- ✅ `artifacts/screenshots/` - Responsive screenshots
- ✅ `artifacts/baseline-issues.json` - Initial errors

### Phase 1 TODO Integration

**Update TODO files:**
```markdown
## In docs/TODO.md
- [x] Phase 1: Record - Application discovery
- [x] Phase 1: Record - API discovery
- [x] Phase 1: Record - Database schema
- [x] Phase 1: Record - Responsive baselines
- [x] Phase 1: Record - Error baseline

## In docs/COMPLETE_TASKS.md
✅ Phase 1: RORLOC Record - Completed 2025-11-15 17:30
- Discovered X routes
- Recorded Y UI elements
- Found Z API endpoints
- Captured screenshots for 4 viewports
- Recorded N baseline issues

## In docs/INCOMPLETE_TASKS.md
(Remove Phase 1 Record tasks)
```

### Phase 1 Checkpoint

**CANNOT PROCEED TO PHASE 2 WITHOUT:**
- ✅ All discovery artifacts generated
- ✅ site-map.json contains > 0 routes
- ✅ ui-inventory.json exists
- ✅ TODO files updated

---

## Phase 2: ORGANIZE (Categorize & Prioritize)

**Objective:** Structure discovered components into logical testing categories.

### 2.1 Categorize UI Components

**Priority Levels:**

**Critical (Test First):**
- Authentication flows
- Core business functions
- Data persistence operations
- Payment processing

**High Priority:**
- Navigation systems
- Form validation
- Search and filter

**Medium Priority:**
- Secondary features
- User preferences
- Notifications

**Low Priority:**
- Cosmetic animations
- Tertiary links
- Footer content

**Script:** `utils/categorize.ts`
```typescript
export interface TestPriority {
  critical: string[];
  high: string[];
  medium: string[];
  low: string[];
}

export function categorizeRoutes(routes: string[]): TestPriority {
  const priority: TestPriority = {
    critical: [],
    high: [],
    medium: [],
    low: [],
  };
  
  for (const route of routes) {
    if (route.includes('/login') || route.includes('/register') || route.includes('/checkout')) {
      priority.critical.push(route);
    } else if (route.includes('/search') || route.includes('/filter') || route === '/') {
      priority.high.push(route);
    } else if (route.includes('/settings') || route.includes('/profile')) {
      priority.medium.push(route);
    } else {
      priority.low.push(route);
    }
  }
  
  return priority;
}
```

### 2.2 Organize API Endpoints

**Integration Tests:**
- User workflows spanning multiple API calls
- State management across requests
- Error propagation

**Unit API Tests:**
- Individual endpoint validation
- Input sanitization
- Error responses
- Auth/authZ checks

### 2.3 Create Test Data

**Structure:**
```typescript
export const testData = {
  valid: {
    email: 'test@example.com',
    password: 'SecurePass123!',
    name: 'Test User',
  },
  invalid: {
    email: 'notanemail',
    password: '123',
    name: '',
  },
  boundary: {
    email: 'a'.repeat(255) + '@example.com',
    password: 'x'.repeat(128),
    name: 'ñ'.repeat(100),
  },
  userStates: {
    anonymous: null,
    authenticated: { token: 'valid_token' },
    admin: { token: 'admin_token', role: 'admin' },
    expired: { token: 'expired_token' },
  },
};
```

### 2.4 Test Execution Sequence

**Order:**
1. Health checks & DB connectivity
2. Unit API tests
3. UI smoke tests
4. Integration tests (UI → API → DB)
5. E2E user workflows
6. Cross-browser tests
7. Performance smoke tests

**Script:** `tests/organize/test-matrix.spec.ts`
```typescript
import { test } from '@playwright/test';
import * as fs from 'fs';
import { categorizeRoutes } from '../../utils/categorize';

test.describe('RORLOC Phase 2: Organize', () => {
  test('create test matrix', () => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    const priority = categorizeRoutes(routes);
    
    const testMatrix = {
      priority,
      executionOrder: [
        'health',
        'unit_api',
        'ui_smoke',
        'integration',
        'e2e',
        'cross_browser',
        'performance',
      ],
      testData: {
        valid: {},
        invalid: {},
        boundary: {},
        userStates: {},
      },
    };
    
    fs.writeFileSync(
      './artifacts/test-matrix.json',
      JSON.stringify(testMatrix, null, 2)
    );
    
    console.log('✅ Test matrix created');
  });
});
```

### Phase 2 Deliverable

- ✅ `artifacts/test-matrix.json` - Prioritized test plan
- ✅ `utils/categorize.ts` - Categorization logic
- ✅ `utils/test-data.ts` - Test datasets

### Phase 2 Checkpoint

**CANNOT PROCEED TO PHASE 3 WITHOUT:**
- ✅ Test matrix created
- ✅ Routes categorized by priority
- ✅ Test data prepared
- ✅ TODO files updated

---

## Phase 3: REFACTOR (Reuse & Efficiency)

**Objective:** Create reusable utilities and eliminate duplication.

### 3.1 Base Page Object Model

**File:** `utils/base-page.ts`
```typescript
import { Page } from '@playwright/test';

export class BasePage {
  constructor(protected page: Page) {}
  
  async navigate(path: string) {
    await this.page.goto(path);
    await this.waitForPageLoad();
  }
  
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForLoadState('domcontentloaded');
  }
  
  async getConsoleErrors(): Promise<string[]> {
    const errors: string[] = [];
    this.page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    return errors;
  }
  
  async verifyNoErrors() {
    const errors = await this.getConsoleErrors();
    return errors.length === 0;
  }
  
  async verifyElementExists(selector: string) {
    return await this.page.locator(selector).isVisible();
  }
  
  async clickButton(selector: string) {
    await this.page.click(selector);
    await this.waitForPageLoad();
  }
}
```

### 3.2 CDP Guard Helper

**File:** `utils/cdp-guard.ts`
```typescript
import { Page } from '@playwright/test';

export class CDPGuard {
  private errors: any[] = [];
  
  constructor(private page: Page) {}
  
  async enable() {
    // Console errors
    this.page.on('console', msg => {
      if (msg.type() === 'error' || msg.type() === 'assert') {
        this.errors.push({
          type: 'console',
          level: msg.type(),
          text: msg.text(),
          location: msg.location(),
        });
      }
    });
    
    // Page errors
    this.page.on('pageerror', error => {
      this.errors.push({
        type: 'pageerror',
        message: error.message,
        stack: error.stack,
      });
    });
    
    // Request failures
    this.page.on('requestfailed', request => {
      this.errors.push({
        type: 'network',
        url: request.url(),
        failure: request.failure()?.errorText,
      });
    });
    
    // HTTP errors
    this.page.on('response', response => {
      if (response.status() >= 400) {
        const allowed = JSON.parse(process.env.ALLOWED_4XX || '[]');
        if (!allowed.includes(response.status())) {
          this.errors.push({
            type: 'http',
            url: response.url(),
            status: response.status(),
            statusText: response.statusText(),
          });
        }
      }
    });
  }
  
  getErrors() {
    return this.errors;
  }
  
  hasErrors() {
    return this.errors.length > 0;
  }
  
  reset() {
    this.errors = [];
  }
}
```

### 3.3 Buttons Verifier

**File:** `utils/buttons-verifier.ts`
```typescript
import { Page } from '@playwright/test';
import * as fs from 'fs';

export class ButtonsVerifier {
  private spec: any;
  
  constructor(private page: Page) {
    // Load spec if exists
    if (fs.existsSync('./spec/ui/buttons.json')) {
      this.spec = JSON.parse(fs.readFileSync('./spec/ui/buttons.json', 'utf-8'));
    }
  }
  
  async verifyButtons(route: string) {
    const requiredButtons = this.spec?.[route] || [];
    const results: any[] = [];
    
    // If no spec, generate baseline
    if (!this.spec) {
      return await this.generateBaseline(route);
    }
    
    for (const buttonSelector of requiredButtons) {
      const button = this.page.locator(buttonSelector);
      const exists = await button.isVisible();
      const clickable = exists ? await button.isEnabled() : false;
      
      results.push({
        selector: buttonSelector,
        exists,
        clickable,
        passed: exists && clickable,
      });
    }
    
    return results;
  }
  
  async generateBaseline(route: string) {
    const buttons = await this.page.$$eval(
      'button, [role="button"], [data-testid*="button"]',
      els => els.map(el => ({
        tag: el.tagName,
        text: el.textContent?.trim(),
        id: el.id,
        className: el.className,
        ariaLabel: el.getAttribute('aria-label'),
      }))
    );
    
    return buttons;
  }
}
```

### 3.4 API Client

**File:** `utils/api-client.ts`
```typescript
import { APIRequestContext } from '@playwright/test';

export class APIClient {
  constructor(
    private request: APIRequestContext,
    private baseURL: string = process.env.BASE_URL || 'http://localhost:3000'
  ) {}
  
  async get(endpoint: string, options?: any) {
    return await this.request.get(`${this.baseURL}${endpoint}`, options);
  }
  
  async post(endpoint: string, data: any, options?: any) {
    return await this.request.post(`${this.baseURL}${endpoint}`, {
      data,
      ...options,
    });
  }
  
  async put(endpoint: string, data: any, options?: any) {
    return await this.request.put(`${this.baseURL}${endpoint}`, {
      data,
      ...options,
    });
  }
  
  async delete(endpoint: string, options?: any) {
    return await this.request.delete(`${this.baseURL}${endpoint}`, options);
  }
  
  async testEndpoint(
    method: string,
    endpoint: string,
    expectedStatus: number,
    data?: any
  ) {
    let response;
    
    switch (method.toUpperCase()) {
      case 'GET':
        response = await this.get(endpoint);
        break;
      case 'POST':
        response = await this.post(endpoint, data);
        break;
      case 'PUT':
        response = await this.put(endpoint, data);
        break;
      case 'DELETE':
        response = await this.delete(endpoint);
        break;
      default:
        throw new Error(`Unsupported method: ${method}`);
    }
    
    return {
      passed: response.status() === expectedStatus,
      status: response.status(),
      body: await response.json().catch(() => null),
    };
  }
}
```

### 3.5 Database Transaction Wrapper

**File:** `utils/db-transaction.ts`
```typescript
import { Client } from 'pg';

export class DBTransaction {
  private client: Client;
  
  constructor() {
    this.client = new Client({
      connectionString: process.env.DATABASE_URL,
    });
  }
  
  async connect() {
    await this.client.connect();
  }
  
  async begin() {
    await this.client.query('BEGIN');
  }
  
  async rollback() {
    await this.client.query('ROLLBACK');
  }
  
  async query(sql: string, params?: any[]) {
    return await this.client.query(sql, params);
  }
  
  async close() {
    await this.client.end();
  }
  
  async withTransaction<T>(callback: () => Promise<T>): Promise<T> {
    await this.connect();
    await this.begin();
    
    try {
      const result = await callback();
      await this.rollback(); // Always rollback in tests
      return result;
    } finally {
      await this.close();
    }
  }
}
```

### Phase 3 Deliverable

**Utilities Created:**
- ✅ `utils/base-page.ts` - Base page object
- ✅ `utils/cdp-guard.ts` - Error detection
- ✅ `utils/buttons-verifier.ts` - Button verification
- ✅ `utils/api-client.ts` - API testing
- ✅ `utils/db-transaction.ts` - DB testing
- ✅ `utils/categorize.ts` - Prioritization
- ✅ `utils/test-data.ts` - Test datasets

### Phase 3 Checkpoint

**CANNOT PROCEED TO PHASE 4 WITHOUT:**
- ✅ All utilities created and tested
- ✅ No code duplication
- ✅ Shared fixtures established
- ✅ TODO files updated

---

## Phase 4: LOCATE (Execute & Find Issues)

**Objective:** Run comprehensive tests and locate all bugs.

### 4.1 UI Controls Testing

**File:** `tests/locate/ui-controls.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import { BasePage } from '../../utils/base-page';
import { ButtonsVerifier } from '../../utils/buttons-verifier';

test.describe('RORLOC Phase 4: Locate - UI Controls', () => {
  test('verify all buttons exist and work', async ({ page }) => {
    const basePage = new BasePage(page);
    const buttonsVerifier = new ButtonsVerifier(page);
    
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    const results: any = {};
    
    for (const route of routes) {
      await basePage.navigate(route);
      const buttonResults = await buttonsVerifier.verifyButtons(route);
      results[route] = buttonResults;
      
      // Assert all buttons pass
      for (const result of buttonResults) {
        expect(result.passed, `Button ${result.selector} on ${route}`).toBe(true);
      }
    }
    
    fs.writeFileSync(
      './artifacts/buttons-report.json',
      JSON.stringify(results, null, 2)
    );
  });
  
  test('verify forms validation', async ({ page }) => {
    const basePage = new BasePage(page);
    
    // Find all forms
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      await basePage.navigate(route);
      
      const forms = await page.$$('form');
      
      for (const form of forms) {
        // Test with empty data
        await form.evaluate(f => (f as HTMLFormElement).submit());
        
        // Check for error messages
        const errors = await page.$$('.error, [role="alert"]');
        expect(errors.length).toBeGreaterThan(0);
      }
    }
  });
});
```

### 4.2 Page-by-Page Error Detection

**File:** `tests/locate/error-detection.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import { CDPGuard } from '../../utils/cdp-guard';

test.describe('RORLOC Phase 4: Locate - Error Detection', () => {
  test('detect errors on all pages', async ({ page }) => {
    const cdpGuard = new CDPGuard(page);
    await cdpGuard.enable();
    
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    const errorReport: any = {};
    
    for (const route of routes) {
      cdpGuard.reset();
      
      await page.goto(route);
      await page.waitForLoadState('networkidle');
      
      const errors = cdpGuard.getErrors();
      errorReport[route] = errors;
      
      // Fail if errors found
      expect(errors, `Errors on ${route}: ${JSON.stringify(errors)}`).toHaveLength(0);
    }
    
    fs.writeFileSync(
      './artifacts/error-report.json',
      JSON.stringify(errorReport, null, 2)
    );
  });
  
  test('check for broken images', async ({ page }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      await page.goto(route);
      
      const brokenImages = await page.$$eval('img', imgs =>
        imgs
          .filter(img => img.naturalWidth === 0)
          .map(img => img.src)
      );
      
      expect(brokenImages, `Broken images on ${route}`).toHaveLength(0);
    }
  });
  
  test('check for broken links', async ({ page, request }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      await page.goto(route);
      
      const links = await page.$$eval('a[href]', anchors =>
        anchors.map(a => a.href)
      );
      
      for (const link of links) {
        try {
          const response = await request.head(link, { timeout: 5000 });
          expect(response.status(), `Link ${link} on ${route}`).toBeLessThan(400);
        } catch (error) {
          // Timeout or network error
          throw new Error(`Broken link: ${link} on ${route}`);
        }
      }
    }
  });
});
```

### 4.3 Routing & Navigation

**File:** `tests/locate/routing.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test.describe('RORLOC Phase 4: Locate - Routing', () => {
  test('direct URL access works', async ({ page }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      await page.goto(route);
      expect(page.url()).toContain(route);
    }
  });
  
  test('back/forward navigation works', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="/about"]');
    await page.goBack();
    expect(page.url()).toContain('/');
    await page.goForward();
    expect(page.url()).toContain('/about');
  });
  
  test('404 handling', async ({ page }) => {
    await page.goto('/non-existent-page');
    const content = await page.textContent('body');
    expect(content).toContain('404');
  });
});
```

### 4.4 Responsive & Interactivity

**File:** `tests/locate/responsive.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';

const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 },
];

test.describe('RORLOC Phase 4: Locate - Responsive', () => {
  for (const viewport of viewports) {
    test(`${viewport.name} - no horizontal scroll`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      
      const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
      
      for (const route of routes) {
        await page.goto(route);
        
        const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
        const clientWidth = await page.evaluate(() => document.body.clientWidth);
        
        expect(scrollWidth, `Horizontal scroll on ${route} at ${viewport.name}`).toBeLessThanOrEqual(clientWidth + 1);
      }
    });
    
    test(`${viewport.name} - critical elements visible`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      
      await page.goto('/');
      
      // Check navigation
      const nav = page.locator('nav, [role="navigation"]');
      await expect(nav).toBeVisible();
      
      // Check main content
      const main = page.locator('main, [role="main"]');
      await expect(main).toBeVisible();
    });
  }
});
```

### 4.5 API Integration

**File:** `tests/locate/api-integration.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import { APIClient } from '../../utils/api-client';

test.describe('RORLOC Phase 4: Locate - API Integration', () => {
  test('API endpoints return expected status', async ({ request }) => {
    const apiClient = new APIClient(request);
    const apiInventory = JSON.parse(fs.readFileSync('./artifacts/api-inventory.json', 'utf-8'));
    
    // Group by endpoint
    const endpoints = new Map<string, any>();
    for (const call of apiInventory) {
      const key = `${call.method} ${call.url}`;
      if (!endpoints.has(key)) {
        endpoints.set(key, call);
      }
    }
    
    // Test each endpoint
    for (const [key, call] of endpoints) {
      const result = await apiClient.testEndpoint(
        call.method,
        new URL(call.url).pathname,
        call.status || 200
      );
      
      expect(result.passed, `API ${key}`).toBe(true);
    }
  });
  
  test('API responses match OpenAPI schema', async ({ request }) => {
    if (!fs.existsSync('./artifacts/openapi.json')) {
      console.log('⚠️ OpenAPI not available, skipping');
      return;
    }
    
    const openapi = JSON.parse(fs.readFileSync('./artifacts/openapi.json', 'utf-8'));
    const apiClient = new APIClient(request);
    
    // Test each endpoint in OpenAPI
    for (const [path, methods] of Object.entries(openapi.paths)) {
      for (const [method, spec] of Object.entries(methods as any)) {
        const result = await apiClient.testEndpoint(
          method,
          path,
          Object.keys((spec as any).responses)[0] as any
        );
        
        // Basic schema validation
        expect(result.body).toBeDefined();
      }
    }
  });
});
```

### 4.6 Database Connectivity

**File:** `tests/locate/database.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import { DBTransaction } from '../../utils/db-transaction';

test.describe('RORLOC Phase 4: Locate - Database', () => {
  test('database connectivity', async () => {
    if (!process.env.DATABASE_URL) {
      console.log('⚠️ DATABASE_URL not provided, skipping');
      return;
    }
    
    const db = new DBTransaction();
    
    await db.withTransaction(async () => {
      const result = await db.query('SELECT 1 as test');
      expect(result.rows[0].test).toBe(1);
    });
  });
  
  test('CRUD operations reflect in database', async ({ page }) => {
    if (!process.env.DATABASE_URL) {
      console.log('⚠️ DATABASE_URL not provided, skipping');
      return;
    }
    
    const db = new DBTransaction();
    
    await db.withTransaction(async () => {
      // Create via UI
      await page.goto('/create');
      await page.fill('[name="title"]', 'Test Item');
      await page.click('button[type="submit"]');
      await page.waitForLoadState('networkidle');
      
      // Verify in DB
      const result = await db.query('SELECT * FROM items WHERE title = $1', ['Test Item']);
      expect(result.rows.length).toBeGreaterThan(0);
    });
  });
});
```

### 4.7 Cross-Browser

**Note:** Already configured in `playwright.config.ts` with projects.

### 4.8 Performance Smoke

**File:** `tests/locate/performance.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test.describe('RORLOC Phase 4: Locate - Performance', () => {
  test('pages load within 3 seconds', async ({ page }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      const startTime = Date.now();
      await page.goto(route);
      await page.waitForLoadState('networkidle');
      const loadTime = Date.now() - startTime;
      
      expect(loadTime, `Load time for ${route}`).toBeLessThan(3000);
    }
  });
  
  test('total page size under 5MB', async ({ page }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      let totalSize = 0;
      
      page.on('response', response => {
        const headers = response.headers();
        const contentLength = parseInt(headers['content-length'] || '0');
        totalSize += contentLength;
      });
      
      await page.goto(route);
      await page.waitForLoadState('networkidle');
      
      expect(totalSize, `Total size for ${route}`).toBeLessThan(5 * 1024 * 1024);
    }
  });
});
```

### Phase 4 Deliverable

**Test Results:**
- ✅ HTML report with traces/videos/screenshots
- ✅ `artifacts/qa-report.json` - Comprehensive results
- ✅ `artifacts/buttons-report.json` - Button coverage
- ✅ `artifacts/error-report.json` - All errors found

### Phase 4 Checkpoint

**CANNOT PROCEED TO PHASE 5 WITHOUT:**
- ✅ All critical tests passed
- ✅ All high-priority tests passed
- ✅ Error report reviewed
- ✅ TODO files updated

---

## Phase 5: OPTIMIZE (Close Gaps & Harden)

**Objective:** Fix issues, expand coverage, and reduce flakiness.

### 5.1 Severity Triage

**Process:**
1. Review `artifacts/qa-report.json`
2. Categorize by severity:
   - Critical: Blocks core functionality
   - High: Degrades user experience
   - Medium: Minor issues
   - Low: Cosmetic

3. Track in TODO files:
```markdown
## In docs/INCOMPLETE_TASKS.md

### Critical Issues (Fix Immediately)
- [ ] Login button not clickable on mobile
- [ ] API /checkout returns 500

### High Priority Issues
- [ ] Search results not displayed
- [ ] Form validation missing

### Medium Priority Issues
- [ ] Slow page load on /dashboard
- [ ] Missing alt text on images

### Low Priority Issues
- [ ] Footer alignment on tablet
- [ ] Inconsistent button colors
```

### 5.2 Expand Coverage

**Add tests for:**
- Edge cases discovered during Phase 4
- Negative testing (invalid inputs, unauthorized access)
- Boundary conditions
- Error recovery flows

### 5.3 De-Flake Tests

**Common causes:**
- Hardcoded timeouts → Use `waitFor` with conditions
- Race conditions → Add explicit waits
- Weak selectors → Use `data-testid` attributes
- Network instability → Add retries for idempotent operations

**Example fix:**
```typescript
// ❌ Bad (flaky)
await page.click('button');
await page.waitForTimeout(1000);

// ✅ Good (stable)
await page.click('button');
await page.waitForSelector('.success-message');
```

### 5.4 Improve Error Reporting

**Enhanced failure output:**
```typescript
test('enhanced error reporting', async ({ page }) => {
  try {
    await page.goto('/');
    await page.click('button');
  } catch (error) {
    // Attach context
    await page.screenshot({ path: './artifacts/failure.png' });
    
    const consoleErrors = await page.evaluate(() => {
      return (window as any).__consoleErrors || [];
    });
    
    const networkLog = await page.evaluate(() => {
      return (window as any).__networkLog || [];
    });
    
    throw new Error(`
      Test failed: ${error}
      URL: ${page.url()}
      Console errors: ${JSON.stringify(consoleErrors)}
      Network log: ${JSON.stringify(networkLog)}
    `);
  }
});
```

### Phase 5 Deliverable

- ✅ Updated test suite with expanded coverage
- ✅ Flakiness reduced to < 5%
- ✅ Enhanced error reporting
- ✅ Prioritized fix list in TODO files

### Phase 5 Checkpoint

**CANNOT PROCEED TO PHASE 6 WITHOUT:**
- ✅ All critical issues fixed
- ✅ All high-priority issues fixed
- ✅ Test suite stability > 95%
- ✅ TODO files updated

---

## Phase 6: CONFIRM (Regression & Sign-Off)

**Objective:** Final validation and production readiness.

### 6.1 Full Regression

**Compare with previous run:**
```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test.describe('RORLOC Phase 6: Confirm - Regression', () => {
  test('compare with previous run', () => {
    const currentResults = JSON.parse(fs.readFileSync('./artifacts/qa-report.json', 'utf-8'));
    
    let previousResults = {};
    if (fs.existsSync('./artifacts/previous-run.json')) {
      previousResults = JSON.parse(fs.readFileSync('./artifacts/previous-run.json', 'utf-8'));
    }
    
    const regression = {
      previousFailures: [],
      newFailures: [],
      stillFailing: [],
      fixed: [],
    };
    
    // Analysis logic...
    
    fs.writeFileSync(
      './artifacts/regression-report.json',
      JSON.stringify(regression, null, 2)
    );
    
    // Fail if new failures
    expect(regression.newFailures).toHaveLength(0);
  });
});
```

### 6.2 End-to-End Journeys

**Critical user flows:**
```typescript
test.describe('RORLOC Phase 6: E2E Journeys', () => {
  test('new user onboarding', async ({ page }) => {
    // 1. Visit homepage
    await page.goto('/');
    
    // 2. Sign up
    await page.click('[data-testid="signup-button"]');
    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');
    
    // 3. Verify email (mock)
    await page.goto('/verify?token=mock_token');
    
    // 4. Complete profile
    await page.fill('[name="name"]', 'New User');
    await page.click('button[type="submit"]');
    
    // 5. Verify dashboard access
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
  
  test('authenticated CRUD cycle', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    
    // Create
    await page.goto('/create');
    await page.fill('[name="title"]', 'Test Item');
    await page.click('button[type="submit"]');
    await expect(page.locator('.success')).toBeVisible();
    
    // Read
    await page.goto('/items');
    await expect(page.locator('text=Test Item')).toBeVisible();
    
    // Update
    await page.click('[data-testid="edit-button"]');
    await page.fill('[name="title"]', 'Updated Item');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Updated Item')).toBeVisible();
    
    // Delete
    await page.click('[data-testid="delete-button"]');
    await page.click('[data-testid="confirm-delete"]');
    await expect(page.locator('text=Updated Item')).not.toBeVisible();
  });
});
```

### 6.3 Security Testing

**File:** `tests/confirm/security.spec.ts`
```typescript
import { test, expect } from '@playwright/test';

test.describe('RORLOC Phase 6: Security', () => {
  test('protected routes require auth', async ({ page }) => {
    await page.goto('/dashboard');
    expect(page.url()).toContain('/login');
  });
  
  test('XSS prevention', async ({ page }) => {
    await page.goto('/create');
    await page.fill('[name="title"]', '<script>alert("XSS")</script>');
    await page.click('button[type="submit"]');
    
    await page.goto('/items');
    const content = await page.textContent('body');
    expect(content).not.toContain('<script>');
  });
  
  test('CORS headers present', async ({ request }) => {
    const response = await request.get('/api/data');
    const headers = response.headers();
    expect(headers['access-control-allow-origin']).toBeDefined();
  });
  
  test('CSP headers present', async ({ page }) => {
    await page.goto('/');
    const csp = await page.evaluate(() => {
      const meta = document.querySelector('meta[http-equiv="Content-Security-Policy"]');
      return meta?.getAttribute('content');
    });
    expect(csp).toBeDefined();
  });
});
```

### 6.4 Accessibility

**File:** `tests/confirm/accessibility.spec.ts`
```typescript
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y } from '@axe-core/playwright';
import * as fs from 'fs';

test.describe('RORLOC Phase 6: Accessibility', () => {
  test('axe scan on all pages', async ({ page }) => {
    const routes = JSON.parse(fs.readFileSync('./artifacts/site-map.json', 'utf-8'));
    
    for (const route of routes) {
      await page.goto(route);
      await injectAxe(page);
      
      await checkA11y(page, null, {
        detailedReport: true,
        detailedReportOptions: {
          html: true,
        },
        axeOptions: {
          runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa'],
          },
        },
      });
    }
  });
  
  test('keyboard navigation works', async ({ page }) => {
    await page.goto('/');
    
    // Tab through interactive elements
    await page.keyboard.press('Tab');
    const firstFocused = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT']).toContain(firstFocused);
    
    // Continue tabbing
    for (let i = 0; i < 10; i++) {
      await page.keyboard.press('Tab');
    }
    
    // Verify focus is visible
    const focusVisible = await page.evaluate(() => {
      const active = document.activeElement;
      const styles = window.getComputedStyle(active!);
      return styles.outline !== 'none';
    });
    expect(focusVisible).toBe(true);
  });
});
```

### 6.5 Performance Acceptance

**File:** `tests/confirm/performance.spec.ts`
```typescript
import { test, expect } from '@playwright/test';

test.describe('RORLOC Phase 6: Performance', () => {
  test('Core Web Vitals', async ({ page }) => {
    await page.goto('/');
    
    const metrics = await page.evaluate(() => {
      return new Promise(resolve => {
        new PerformanceObserver(list => {
          const entries = list.getEntries();
          const vitals: any = {};
          
          for (const entry of entries) {
            if (entry.entryType === 'largest-contentful-paint') {
              vitals.LCP = entry.startTime;
            }
            if (entry.entryType === 'first-input') {
              vitals.FID = (entry as any).processingStart - entry.startTime;
            }
            if (entry.entryType === 'layout-shift' && !(entry as any).hadRecentInput) {
              vitals.CLS = (vitals.CLS || 0) + (entry as any).value;
            }
          }
          
          resolve(vitals);
        }).observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] });
        
        // Timeout after 10s
        setTimeout(() => resolve({}), 10000);
      });
    });
    
    // Thresholds
    expect((metrics as any).LCP, 'LCP').toBeLessThan(2500);
    expect((metrics as any).FID, 'FID').toBeLessThan(100);
    expect((metrics as any).CLS, 'CLS').toBeLessThan(0.1);
  });
});
```

### 6.6 Final System Verification

**MANDATORY: Run complete_system_checker.py**

```bash
python .global/tools/complete_system_checker.py /path/to/project
```

**Requirements:**
- ✅ All pages: 100%
- ✅ All buttons: 100%
- ✅ Backend: 100%
- ✅ Database: 100%
- ✅ Overall score: 100%

**If < 100%:**
```
❌ CANNOT PROCEED TO PHASE 7
→ Fix missing components
→ Re-run verification
→ Achieve 100%
```

### Phase 6 Final Deliverable

**Consolidated Report:**

**File:** `artifacts/FINAL_QA_REPORT.md`
```markdown
# Final QA Report

**Project:** [Project Name]
**Date:** 2025-11-15
**RORLOC Phase:** 6 - Confirm

---

## Executive Summary

**Overall Status:** ✅ PASS / ❌ FAIL

**Pass Rate:** X%

**Critical Issues:** 0
**High Priority Issues:** 0
**Medium Priority Issues:** X
**Low Priority Issues:** Y

---

## Test Coverage

| Category | Tests Run | Passed | Failed | Pass Rate |
|----------|-----------|--------|--------|-----------|
| UI Controls | X | X | 0 | 100% |
| API Integration | X | X | 0 | 100% |
| Database | X | X | 0 | 100% |
| Security | X | X | 0 | 100% |
| Accessibility | X | X | 0 | 100% |
| Performance | X | X | 0 | 100% |
| Cross-Browser | X | X | 0 | 100% |

---

## Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| FCP | < 1.8s | 1.2s | ✅ |
| LCP | < 2.5s | 2.1s | ✅ |
| TTI | < 3.8s | 3.2s | ✅ |
| CLS | < 0.1 | 0.05 | ✅ |

---

## Security Assessment

- ✅ Authentication working
- ✅ Authorization boundaries enforced
- ✅ XSS prevention active
- ✅ CORS configured
- ✅ CSP headers present

---

## Accessibility

- ✅ WCAG 2.1 AA compliant
- ✅ Keyboard navigation works
- ✅ Screen reader compatible
- ✅ Focus indicators visible

---

## System Verification

**complete_system_checker.py results:**
- ✅ All pages: 100%
- ✅ All buttons: 100%
- ✅ Backend: 100%
- ✅ Database: 100%
- ✅ **Overall: 100%**

---

## Remaining Risks

[List any medium/low priority issues]

---

## Recommendation

**GO / NO-GO:** ✅ GO

The application is production-ready.
```

### Phase 6 TODO Integration

```markdown
## In docs/TODO.md
- [x] Phase 6: RORLOC Confirm - Regression testing
- [x] Phase 6: RORLOC Confirm - E2E journeys
- [x] Phase 6: RORLOC Confirm - Security testing
- [x] Phase 6: RORLOC Confirm - Accessibility testing
- [x] Phase 6: RORLOC Confirm - Performance testing
- [x] Phase 6: RORLOC Confirm - System verification 100%

## In docs/COMPLETE_TASKS.md
✅ Phase 6: RORLOC Confirm - Completed 2025-11-15 20:00
- All tests passed
- 100% system verification
- Production ready

## In docs/INCOMPLETE_TASKS.md
(Should be empty if 100% achieved)
```

### Phase 6 Final Checkpoint

**CANNOT PROCEED TO PHASE 7 (Handoff) WITHOUT:**
- ✅ All tests passing
- ✅ 100% system verification
- ✅ Security validated
- ✅ Accessibility compliant
- ✅ Performance acceptable
- ✅ Final report generated
- ✅ GO recommendation
- ✅ TODO files show 100% complete

---

## Integration with Existing System

### Link to MODULE_MAP

**Before RORLOC Phase 1:**
```bash
# Verify MODULE_MAP exists
if [ ! -f "docs/MODULE_MAP.md" ]; then
  echo "❌ MODULE_MAP.md missing"
  echo "→ Run: python .global/tools/module_mapper.py ."
  exit 1
fi
```

### Link to TODO System

**Throughout RORLOC:**
- Update `docs/TODO.md` after each phase
- Move completed tasks to `docs/COMPLETE_TASKS.md`
- Track issues in `docs/INCOMPLETE_TASKS.md`

### Link to System Verification

**In Phase 6:**
```bash
# Run system verification
python .global/tools/complete_system_checker.py .

# Check result
if [ $? -ne 0 ]; then
  echo "❌ System verification failed"
  echo "→ Fix issues and re-run"
  exit 1
fi
```

---

## Running RORLOC Tests

### Full Suite

```bash
# Run all RORLOC tests
npx playwright test

# Generate HTML report
npx playwright show-report
```

### By Phase

```bash
# Phase 1: Record
npx playwright test tests/discovery/

# Phase 2: Organize
npx playwright test tests/organize/

# Phase 4: Locate
npx playwright test tests/locate/

# Phase 6: Confirm
npx playwright test tests/confirm/
```

### By Priority

```bash
# Critical tests only
npx playwright test --grep @critical

# High priority
npx playwright test --grep @high
```

### Continuous Integration

**GitHub Actions:** `.github/workflows/rorloc-tests.yml`
```yaml
name: RORLOC Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          npm ci
          npx playwright install --with-deps
      
      - name: Run RORLOC tests
        run: npx playwright test
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: artifacts/
```

---

## Artifacts Structure

```
artifacts/
├── site-map.json              # Phase 1: All routes
├── ui-inventory.json          # Phase 1: All UI elements
├── api-inventory.json         # Phase 1: All API endpoints
├── openapi.json               # Phase 1: API specification
├── db-schema.json             # Phase 1: Database structure
├── baseline-issues.json       # Phase 1: Initial errors
├── screenshots/               # Phase 1: Responsive screenshots
│   ├── home_mobile.png
│   ├── home_tablet.png
│   └── home_desktop.png
├── test-matrix.json           # Phase 2: Test plan
├── buttons-report.json        # Phase 4: Button coverage
├── error-report.json          # Phase 4: All errors
├── qa-report.json             # Phase 4: Comprehensive results
├── regression-report.json     # Phase 6: Regression analysis
├── FINAL_QA_REPORT.md         # Phase 6: Executive summary
├── html-report/               # Playwright HTML report
├── test-results.json          # Playwright JSON results
└── traces/                    # Playwright traces
```

---

## Best Practices

### DO ✅

1. **Always start with Phase 1 (Record)**
   - Complete discovery before testing
   - Establish baselines

2. **Update TODO files after each phase**
   - Mark completed tasks
   - Track issues

3. **Use data-testid for selectors**
   ```html
   <button data-testid="submit-button">Submit</button>
   ```

4. **Wrap DB writes in transactions**
   ```typescript
   await db.withTransaction(async () => {
     // Test code
   }); // Auto-rollback
   ```

5. **Enable CDP guards on every test**
   ```typescript
   const cdpGuard = new CDPGuard(page);
   await cdpGuard.enable();
   ```

6. **Run complete_system_checker.py before Phase 7**
   ```bash
   python .global/tools/complete_system_checker.py .
   ```

### DON'T ❌

1. **Don't skip phases**
   - Each phase builds on previous
   - Skipping causes incomplete coverage

2. **Don't use hardcoded timeouts**
   ```typescript
   // ❌ Bad
   await page.waitForTimeout(1000);
   
   // ✅ Good
   await page.waitForSelector('.success');
   ```

3. **Don't test in production**
   - Use staging/test environments
   - Never destructive operations on prod data

4. **Don't ignore flaky tests**
   - Fix root cause
   - Don't just retry

5. **Don't proceed with < 100% verification**
   - Fix all issues
   - Re-run until 100%

---

## Troubleshooting

### Tests failing with "Element not found"

**Solution:** Add explicit waits
```typescript
await page.waitForSelector('[data-testid="button"]');
await page.click('[data-testid="button"]');
```

### Database connection errors

**Solution:** Check DATABASE_URL
```bash
echo $DATABASE_URL
# Should be: postgresql://user:pass@localhost:5432/dbname
```

### OpenAPI not found

**Solution:** Provide OPENAPI_URL or skip
```bash
export OPENAPI_URL=http://localhost:3000/openapi.json
```

### Playwright installation issues

**Solution:** Install with deps
```bash
npx playwright install --with-deps
```

---

## Summary

**RORLOC Testing Methodology** provides a systematic, comprehensive approach to full-stack testing that ensures:

✅ **Zero hallucinations** - Complete discovery and verification  
✅ **100% coverage** - All pages, buttons, APIs, database  
✅ **Production quality** - Security, accessibility, performance  
✅ **Automated validation** - CI/CD ready  
✅ **Clear reporting** - Executive summaries and detailed logs

**Integration with Global System:**
- ✅ Linked to MODULE_MAP
- ✅ Integrated with TODO system
- ✅ Uses complete_system_checker.py
- ✅ Mandatory in Phase 4

**Result:** Professional, production-ready applications with verified quality.

---

**Status:** ⭐ MANDATORY in Phase 4 (Testing)  
**Prerequisites:** MODULE_MAP.md, TODO files, Complete implementation  
**Deliverable:** 100% verified system ready for deployment

