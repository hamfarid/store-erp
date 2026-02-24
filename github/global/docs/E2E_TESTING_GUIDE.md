# E2E Testing with Playwright - Implementation Guide

**Date:** 2025-11-08  
**Task:** T27 - E2E Testing with Playwright  
**Status:** Ready to Execute  
**Effort:** 4-5 hours

---

## Overview

This guide provides step-by-step instructions for implementing E2E testing with Playwright for the Store ERP system.

### Test Coverage
- **Authentication Tests** (10 tests) - Login, logout, session management
- **Product Management Tests** (10 tests) - CRUD operations, search, filter
- **Invoice Management Tests** (12 tests) - Create, view, print, export
- **Dashboard Navigation Tests** (14 tests) - Navigation, responsive design

**Total: 46 E2E test cases**

---

## Prerequisites

### System Requirements
- Node.js 16+ installed
- npm or yarn package manager
- Backend running on localhost:5000
- Frontend running on localhost:5001

### Verify Prerequisites
```bash
node --version  # Should be v16+
npm --version   # Should be v8+
```

---

## Step 1: Install Playwright (45 minutes)

### 1.1 Install Playwright Package
```bash
cd frontend
npm install -D @playwright/test
```

### 1.2 Install Browsers
```bash
npx playwright install
```

### 1.3 Verify Installation
```bash
npx playwright --version
```

**Expected Output:**
```
Version 1.40.0 (or higher)
```

---

## Step 2: Configure Playwright (15 minutes)

### 2.1 Create Configuration File
The `frontend/playwright.config.js` file has been created with:
- Base URL: http://localhost:5001
- Test directory: ./tests/e2e
- Browsers: Chromium, Firefox, WebKit
- Mobile viewports: Pixel 5, iPhone 12
- Screenshots on failure
- Videos on failure
- HTML reports

### 2.2 Verify Configuration
```bash
cat frontend/playwright.config.js
```

---

## Step 3: Create Test Files (Already Done!)

### 3.1 Test Files Created
1. **frontend/tests/e2e/auth.spec.js** (10 tests)
   - Login/logout flows
   - Session management
   - Password reset
   - Session timeout

2. **frontend/tests/e2e/products.spec.js** (10 tests)
   - Product CRUD operations
   - Search and filter
   - Sorting and pagination
   - Bulk actions

3. **frontend/tests/e2e/invoices.spec.js** (12 tests)
   - Invoice creation and editing
   - Print and download
   - Email sending
   - Status filtering

4. **frontend/tests/e2e/dashboard.spec.js** (14 tests)
   - Navigation
   - Responsive design
   - Theme toggle
   - Performance metrics

### 3.2 Test Structure
```
frontend/tests/e2e/
├── auth.spec.js
├── products.spec.js
├── invoices.spec.js
└── dashboard.spec.js
```

---

## Step 4: Run Tests Locally (1-2 hours)

### 4.1 Start Backend
```bash
cd backend
python app.py
```

**Wait for:** `Running on http://localhost:5000`

### 4.2 Start Frontend (in another terminal)
```bash
cd frontend
npm run dev
```

**Wait for:** `Local: http://localhost:5001`

### 4.3 Run All Tests
```bash
cd frontend
npx playwright test
```

**Expected Output:**
```
Running 46 tests using 3 workers

✓ auth.spec.js (10 tests)
✓ products.spec.js (10 tests)
✓ invoices.spec.js (12 tests)
✓ dashboard.spec.js (14 tests)

46 passed (2m 30s)
```

### 4.4 Run Specific Test File
```bash
npx playwright test tests/e2e/auth.spec.js
```

### 4.5 Run Specific Test
```bash
npx playwright test -g "should login successfully"
```

### 4.6 Run Tests in UI Mode (Interactive)
```bash
npx playwright test --ui
```

### 4.7 Run Tests in Debug Mode
```bash
npx playwright test --debug
```

### 4.8 View Test Report
```bash
npx playwright show-report
```

---

## Step 5: CI/CD Integration (1 hour)

### 5.1 Create GitHub Actions Workflow

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  pull_request:
    branches: [main, development]
  push:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Start backend
        run: |
          cd backend
          python app.py &
          sleep 10
      
      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Install Playwright
        run: |
          cd frontend
          npx playwright install --with-deps
      
      - name: Run E2E tests
        run: |
          cd frontend
          npx playwright test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
          retention-days: 30
```

### 5.2 Commit Workflow
```bash
git add .github/workflows/e2e-tests.yml
git commit -m "feat: add E2E testing workflow"
git push
```

---

## Step 6: Documentation (45 minutes)

### 6.1 Update package.json Scripts

Add to `frontend/package.json`:

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:report": "playwright show-report"
  }
}
```

### 6.2 Create Test Documentation

Create `docs/testing/E2E_TESTING.md`:

```markdown
# E2E Testing Guide

## Running Tests

### All Tests
\`\`\`bash
npm run test:e2e
\`\`\`

### UI Mode
\`\`\`bash
npm run test:e2e:ui
\`\`\`

### Debug Mode
\`\`\`bash
npm run test:e2e:debug
\`\`\`

### View Report
\`\`\`bash
npm run test:e2e:report
\`\`\`

## Test Files

- `tests/e2e/auth.spec.js` - Authentication tests
- `tests/e2e/products.spec.js` - Product management tests
- `tests/e2e/invoices.spec.js` - Invoice management tests
- `tests/e2e/dashboard.spec.js` - Dashboard navigation tests

## Coverage

- 46 E2E test cases
- 80%+ user journey coverage
- All critical flows tested
```

---

## Success Criteria

### ✅ All Tests Passing
- [ ] 46/46 tests passing
- [ ] No flaky tests
- [ ] All browsers passing (Chromium, Firefox, WebKit)

### ✅ Coverage Metrics
- [ ] 80%+ user journey coverage
- [ ] All critical flows tested
- [ ] Authentication flows covered
- [ ] CRUD operations covered

### ✅ Performance
- [ ] Test execution <5 minutes
- [ ] No timeout issues
- [ ] Stable test results

### ✅ CI/CD Integration
- [ ] GitHub Actions workflow working
- [ ] Tests run on PR creation
- [ ] Tests run on push to main
- [ ] Artifacts uploaded

### ✅ Documentation
- [ ] Test guide created
- [ ] Test cases documented
- [ ] Troubleshooting guide created

---

## Troubleshooting

### Tests Timing Out
```bash
# Increase timeout in playwright.config.js
use: {
  timeout: 30000,  // 30 seconds
}
```

### Tests Failing on CI
```bash
# Run with more verbose output
npx playwright test --reporter=verbose
```

### Browser Issues
```bash
# Reinstall browsers
npx playwright install --with-deps
```

### Port Already in Use
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

---

## Next Steps

1. ✅ Install Playwright
2. ✅ Configure Playwright
3. ✅ Create test files
4. ✅ Run tests locally
5. ✅ Set up CI/CD
6. ✅ Document tests
7. ⏳ Execute T28: DAST Enhancement
8. ⏳ Execute T29: Deployment Automation

---

**Document Version:** 1.0  
**Created:** 2025-11-08  
**Status:** Ready for Execution

