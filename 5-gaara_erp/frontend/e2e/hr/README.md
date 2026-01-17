# HR Module E2E Tests

End-to-end tests for the HR (Human Resources) module using Playwright.

## Test Coverage

### 1. Employees Page (`employees.spec.js`)
- ✅ Page loading and navigation
- ✅ Employee listing with pagination
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Form validation
- ✅ Search and filter functionality
- ✅ Export to Excel
- ✅ Error handling
- ✅ Accessibility checks
- ✅ Responsive design

**Total Tests: 15**

### 2. Departments Page (`departments.spec.js`)
- ✅ Page loading and statistics
- ✅ Hierarchical tree view
- ✅ Expand/collapse hierarchy
- ✅ CRUD operations for departments
- ✅ Parent-child relationships
- ✅ Budget management
- ✅ Employee count tracking
- ✅ Error handling
- ✅ Accessibility checks

**Total Tests: 14**

### 3. Attendance Page (`attendance.spec.js`)
- ✅ Page loading and status display
- ✅ Check-in functionality
- ✅ Check-out functionality
- ✅ Attendance records table
- ✅ Date navigation (prev/next/today)
- ✅ Status badges (present, absent, late, on leave)
- ✅ Late minutes and overtime tracking
- ✅ Export attendance report
- ✅ Error handling
- ✅ Accessibility checks

**Total Tests: 20**

## Total E2E Test Coverage

**49 End-to-End Tests** covering the entire HR module workflow.

## Running Tests

### Prerequisites

```bash
# Install Playwright
npm install -D @playwright/test

# Install browsers
npx playwright install
```

### Run All HR Tests

```bash
# Run all HR E2E tests
npx playwright test e2e/hr/

# Run with UI mode
npx playwright test e2e/hr/ --ui

# Run in headed mode (see browser)
npx playwright test e2e/hr/ --headed

# Run specific test file
npx playwright test e2e/hr/employees.spec.js
```

### Run Tests by Module

```bash
# Employees tests only
npx playwright test e2e/hr/employees.spec.js

# Departments tests only
npx playwright test e2e/hr/departments.spec.js

# Attendance tests only
npx playwright test e2e/hr/attendance.spec.js
```

### Run with Different Browsers

```bash
# Chrome (default)
npx playwright test e2e/hr/

# Firefox
npx playwright test e2e/hr/ --project=firefox

# WebKit (Safari)
npx playwright test e2e/hr/ --project=webkit

# All browsers
npx playwright test e2e/hr/ --project=chromium --project=firefox --project=webkit
```

### Generate Test Report

```bash
# Run tests and generate HTML report
npx playwright test e2e/hr/ --reporter=html

# Show report
npx playwright show-report
```

## Environment Variables

Set these in your `.env` file or as environment variables:

```bash
BASE_URL=http://localhost:5501  # Frontend URL
API_URL=http://localhost:5001   # Backend API URL
```

## Test Structure

Each test file follows this structure:

```javascript
test.describe('Module Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Navigate to page
  });

  test('should do something', async ({ page }) => {
    // Test implementation
  });
});
```

## API Mocking

Tests use Playwright's `page.route()` to mock API responses:

```javascript
await page.route(`${API_URL}/api/hr/employees`, async route => {
  await route.fulfill({
    status: 200,
    body: JSON.stringify({ success: true, data: [...] })
  });
});
```

## Debugging Tests

### Debug Mode
```bash
# Run in debug mode
npx playwright test e2e/hr/employees.spec.js --debug
```

### Screenshot on Failure
```bash
# Capture screenshot on failure
npx playwright test e2e/hr/ --screenshot=only-on-failure
```

### Video Recording
```bash
# Record video on failure
npx playwright test e2e/hr/ --video=retain-on-failure
```

### Trace Viewer
```bash
# Record trace
npx playwright test e2e/hr/ --trace=on

# View trace
npx playwright show-trace trace.zip
```

## Best Practices

1. **Wait Strategies**: Use `waitForLoadState`, `waitForSelector` instead of hard timeouts
2. **Selectors**: Prefer `data-testid` attributes over CSS selectors
3. **API Mocking**: Mock external APIs to make tests deterministic
4. **Isolation**: Each test should be independent
5. **Arabic Support**: Tests verify RTL layout and Arabic text rendering

## Accessibility Testing

All test suites include basic accessibility checks:
- Proper heading structure
- Accessible button names
- ARIA attributes
- Keyboard navigation
- Screen reader compatibility

## Performance Testing

Tests verify:
- Page load times
- API response times
- Smooth animations
- No memory leaks

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: E2E Tests - HR Module
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test e2e/hr/
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Test Data

Tests use mock data for consistency. Real API integration tests should be run separately with a test database.

## Maintenance

- Update tests when UI changes
- Add tests for new features
- Remove tests for deprecated features
- Keep mock data synchronized with API contracts

## Support

For issues or questions:
1. Check Playwright documentation: https://playwright.dev
2. Review test logs and screenshots
3. Use trace viewer for detailed debugging
4. Contact: dev-team@company.com
