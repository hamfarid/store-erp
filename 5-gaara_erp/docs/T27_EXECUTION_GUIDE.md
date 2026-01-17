# T27: E2E Testing with Playwright - Execution Guide

**Date:** 2025-11-08  
**Task:** T27 - E2E Testing with Playwright  
**Status:** 🔄 Ready to Execute  
**Effort:** 4-5 hours  
**Priority:** P1 - High

---

## Quick Summary

**What's Done:**
- ✅ Playwright configuration created
- ✅ 46 E2E test cases created
- ✅ Test files organized
- ✅ Documentation complete

**What You Need to Do:**
1. Install Playwright
2. Run tests locally
3. Set up CI/CD integration
4. Verify all tests passing

---

## Files Created

### Configuration
- `frontend/playwright.config.js` - Playwright configuration

### Test Files (46 tests total)
- `frontend/tests/e2e/auth.spec.js` - 10 authentication tests
- `frontend/tests/e2e/products.spec.js` - 10 product tests
- `frontend/tests/e2e/invoices.spec.js` - 12 invoice tests
- `frontend/tests/e2e/dashboard.spec.js` - 14 dashboard tests

### Documentation
- `docs/E2E_TESTING_GUIDE.md` - Complete guide
- `docs/T27_EXECUTION_GUIDE.md` - This file

---

## Execution Steps

### Step 1: Install Playwright (15 minutes)

```bash
# Navigate to frontend directory
cd frontend

# Install Playwright
npm install -D @playwright/test

# Install browsers
npx playwright install

# Verify installation
npx playwright --version
```

**Expected Output:**
```
Version 1.40.0 (or higher)
```

---

### Step 2: Prepare Environment (10 minutes)

**Terminal 1: Start Backend**
```bash
cd backend
python app.py
```

**Wait for:** `Running on http://localhost:5000`

**Terminal 2: Start Frontend**
```bash
cd frontend
npm run dev
```

**Wait for:** `Local: http://localhost:5001`

---

### Step 3: Run Tests Locally (1-2 hours)

**Terminal 3: Run Tests**
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

---

### Step 4: View Test Report (10 minutes)

```bash
npx playwright show-report
```

This opens an interactive HTML report showing:
- Test results
- Screenshots on failure
- Videos on failure
- Detailed logs

---

### Step 5: Run Tests in UI Mode (Optional - 15 minutes)

For interactive debugging:

```bash
npx playwright test --ui
```

This opens Playwright Inspector where you can:
- Step through tests
- Inspect elements
- Debug failures
- Record new tests

---

### Step 6: Set Up CI/CD Integration (30 minutes)

**Create `.github/workflows/e2e-tests.yml`:**

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

**Commit and Push:**
```bash
git add .github/workflows/e2e-tests.yml
git commit -m "feat: add E2E testing workflow"
git push
```

---

### Step 7: Update package.json Scripts (10 minutes)

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

Now you can run:
```bash
npm run test:e2e          # Run all tests
npm run test:e2e:ui       # Interactive mode
npm run test:e2e:debug    # Debug mode
npm run test:e2e:report   # View report
```

---

## Test Coverage

### Authentication (10 tests)
- ✅ Display login form
- ✅ Invalid credentials error
- ✅ Successful login
- ✅ Session persistence
- ✅ Logout functionality
- ✅ Remember me
- ✅ Protected route redirect
- ✅ Password reset
- ✅ Email validation
- ✅ Session timeout

### Products (10 tests)
- ✅ Display products list
- ✅ Search products
- ✅ Create product
- ✅ Edit product
- ✅ Delete product
- ✅ Filter by category
- ✅ Sort by price
- ✅ Pagination
- ✅ View details
- ✅ Bulk actions

### Invoices (12 tests)
- ✅ Display invoices list
- ✅ Search invoices
- ✅ Create invoice
- ✅ View details
- ✅ Edit invoice
- ✅ Print invoice
- ✅ Download PDF
- ✅ Filter by status
- ✅ Filter by date
- ✅ Mark as paid
- ✅ Send via email
- ✅ Delete invoice
- ✅ Export invoices

### Dashboard (14 tests)
- ✅ Display dashboard
- ✅ Display metrics
- ✅ Navigate to products
- ✅ Navigate to invoices
- ✅ Navigate to customers
- ✅ Navigate to inventory
- ✅ Navigate to reports
- ✅ Navigate to settings
- ✅ Toggle sidebar
- ✅ Toggle theme
- ✅ User profile menu
- ✅ Notifications
- ✅ Search functionality
- ✅ Responsive layout
- ✅ Performance metrics

---

## Success Criteria

### ✅ All Tests Passing
- [ ] 46/46 tests passing
- [ ] No flaky tests
- [ ] All browsers passing

### ✅ Coverage
- [ ] 80%+ user journey coverage
- [ ] All critical flows tested
- [ ] Authentication covered
- [ ] CRUD operations covered

### ✅ Performance
- [ ] Test execution <5 minutes
- [ ] No timeout issues
- [ ] Stable results

### ✅ CI/CD
- [ ] GitHub Actions workflow working
- [ ] Tests run on PR
- [ ] Tests run on push
- [ ] Artifacts uploaded

---

## Troubleshooting

### Tests Timing Out
```bash
# Increase timeout in playwright.config.js
use: {
  timeout: 30000,  # 30 seconds
}
```

### Tests Failing on CI
```bash
# Run with verbose output
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

### Tests Flaky
```bash
# Add retry logic
test.describe.configure({ retries: 2 });
```

---

## Timeline

### Phase 1: Setup (45 min)
- [ ] Install Playwright
- [ ] Install browsers
- [ ] Verify installation

### Phase 2: Local Testing (1-2 hours)
- [ ] Start backend
- [ ] Start frontend
- [ ] Run all tests
- [ ] View report

### Phase 3: CI/CD (30 min)
- [ ] Create workflow file
- [ ] Commit and push
- [ ] Verify workflow runs

### Phase 4: Documentation (30 min)
- [ ] Update package.json
- [ ] Create documentation
- [ ] Verify everything works

**Total: 4-5 hours**

---

## Next Steps

After T27 is complete:

1. ✅ T27: E2E Testing - COMPLETE
2. ⏳ T28: DAST Scanning Enhancement (2-3h)
3. ⏳ T29: Deployment Automation (3-4h)
4. ⏳ T32: Documentation Finalization (2-3h)
5. ⏳ T33: Final Testing & Verification (2-3h)

---

## Resources

- **Playwright Docs:** https://playwright.dev/
- **Test Configuration:** `frontend/playwright.config.js`
- **Test Files:** `frontend/tests/e2e/`
- **Guide:** `docs/E2E_TESTING_GUIDE.md`

---

## Quick Commands

```bash
# Install
npm install -D @playwright/test
npx playwright install

# Run tests
npx playwright test
npx playwright test --ui
npx playwright test --debug

# View report
npx playwright show-report

# Run specific test
npx playwright test -g "should login"

# Run specific file
npx playwright test tests/e2e/auth.spec.js
```

---

**Document Version:** 1.0  
**Created:** 2025-11-08  
**Status:** Ready for Execution

