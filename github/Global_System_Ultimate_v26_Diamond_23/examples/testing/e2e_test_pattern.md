# E2E Test Pattern (Global System Ultimate Synchronized Intelligence Edition)

## 1. The Planner's Intent
*   **Goal:** Verify critical user flows.
*   **Constraints:** Playwright. Headless mode. CI/CD integration.

## 2. The Executor's Implementation
```python
# tests/e2e/test_login.py
from playwright.sync_api import Page, expect

def test_login_success(page: Page):
    page.goto("http://localhost:3000/login")
    page.fill("input[name='email']", "user@example.com")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://localhost:3000/dashboard")
```

## 3. The Reviewer's Audit
*   [x] Selectors robust? Yes (`name`, `type`).
*   [x] Assertions clear? Yes (`expect`).
*   [x] Clean state? Yes (new context per test).

## 4. The Critic's Verdict
*   **Status:** APPROVED.
*   **Note:** Ensure `BASE_URL` is configurable via env.
