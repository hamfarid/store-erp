# Playwright E2E Tests

## Overview

This directory contains End-to-End (E2E) tests using Playwright for the Gaara Scan AI application.

## Test Files

### 1. `test_playwright_direct.py`
Direct Playwright tests using `sync_playwright()` context manager. These tests work independently without pytest plugins.

**Tests:**
- Basic functionality
- Navigation
- Screenshot capability
- Network interception
- Console log capture

### 2. `test_frontend_pages.py`
Tests for frontend pages and routes.

**Tests:**
- Homepage loading
- Login page
- Register page
- Dashboard page
- Farms page
- Diagnosis page
- Page responsiveness (mobile/tablet)

### 3. `test_api_with_playwright.py`
Tests for API endpoints using Playwright's request context.

**Tests:**
- Health endpoint
- Auth login endpoint
- CORS headers
- Content type validation
- API response time

### 4. `test_user_workflows.py`
Complete user workflow tests (requires pytest-playwright plugin).

**Tests:**
- User registration
- User login
- Farm management
- Disease diagnosis
- Report generation

### 5. `conftest_playwright.py`
Playwright-specific pytest fixtures for test setup.

## Running Tests

### Option 1: Direct Python Script (Recommended)
```bash
cd backend
python run_playwright_tests.py
```

This runs basic Playwright tests without requiring pytest or server setup.

### Option 2: Using pytest
```bash
cd backend
python -m pytest tests/e2e/ -v --no-cov -m e2e
```

### Option 3: Run Specific Test File
```bash
python -m pytest tests/e2e/test_playwright_direct.py -v
```

### Option 4: Run Specific Test
```bash
python -m pytest tests/e2e/test_playwright_direct.py::TestPlaywrightDirect::test_playwright_basic_functionality -v
```

## Prerequisites

1. **Install Playwright:**
   ```bash
   pip install playwright
   ```

2. **Install Browsers:**
   ```bash
   python -m playwright install chromium
   ```

3. **For Server Tests:**
   - Start backend server on port 1005
   - Start frontend server on port 1505

## Test Configuration

### Environment Variables

Set these environment variables to customize test URLs:

```bash
export FRONTEND_URL=http://localhost:1505
export API_URL=http://localhost:1005
```

### Browser Configuration

Tests run in headless mode by default. To run with visible browser:

```python
browser = p.chromium.launch(headless=False)
```

### Viewport Configuration

Default viewport: 1920x1080

To change viewport:
```python
page.set_viewport_size({"width": 375, "height": 667})  # Mobile
```

## Test Structure

```
tests/e2e/
├── README.md                    # This file
├── conftest_playwright.py       # Playwright fixtures
├── test_playwright_direct.py   # Direct Playwright tests
├── test_frontend_pages.py      # Frontend page tests
├── test_api_with_playwright.py # API endpoint tests
└── test_user_workflows.py      # User workflow tests
```

## Writing New Tests

### Basic Test Template

```python
from playwright.sync_api import sync_playwright

def test_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        assert "Example" in page.title()
        browser.close()
```

### Using pytest Fixtures

```python
import pytest
from playwright.sync_api import Page

def test_example(page: Page):
    page.goto("http://localhost:1505")
    assert page.title() is not None
```

## Skipping Tests

Tests that require a running server are marked with `@pytest.mark.skip`:

```python
@pytest.mark.skip(reason="Requires frontend server running")
def test_login_page(page: Page):
    # Test code
```

To run skipped tests, remove the `@pytest.mark.skip` decorator and ensure servers are running.

## Debugging Tests

### Run with Visible Browser

```python
browser = p.chromium.launch(headless=False)
```

### Take Screenshots on Failure

```python
page.screenshot(path="failure.png")
```

### Slow Down Operations

```python
browser = p.chromium.launch(headless=True, slow_mo=1000)  # 1 second delay
```

### Console Logs

```python
def handle_console(msg):
    print(f"Console: {msg.text}")

page.on("console", handle_console)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Install Playwright
  run: |
    pip install playwright
    python -m playwright install chromium

- name: Run E2E Tests
  run: python run_playwright_tests.py
```

## Troubleshooting

### Issue: Tests timeout
**Solution:** Increase timeout:
```python
page.goto("https://example.com", timeout=60000)
```

### Issue: Browser not found
**Solution:** Install browsers:
```bash
python -m playwright install chromium
```

### Issue: Import errors
**Solution:** Ensure Playwright is installed:
```bash
pip install playwright
```

## Test Results

Current test status:
- ✅ Basic functionality: PASSED
- ✅ Navigation: PASSED
- ✅ Screenshot: PASSED
- ✅ API requests: PASSED
- ✅ Network interception: PASSED

## Next Steps

1. Add more E2E tests for application workflows
2. Configure test server startup/teardown
3. Add visual regression testing
4. Integrate with CI/CD pipeline
5. Add performance benchmarks

