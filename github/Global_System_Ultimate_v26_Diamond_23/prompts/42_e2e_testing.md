================================================================================
MODULE 42: END-TO-END TESTING Global System Ultimate (Synchronized Intelligence Edition)
================================================================================
Version: Dynamic
Purpose: Comprehensive E2E testing with **Camoufox**, Playwright, and the **QA Role**.
================================================================================

## OVERVIEW

End-to-End (E2E) testing validates complete user workflows.
This module integrates **Camoufox** for stealth testing and **Playwright** for standard automation.

## ROLES & RESPONSIBILITIES

*   **The QA (Primary):** Designs test cases, breaks the system, and validates fixes.
*   **Camoufox (Tool):** Executes stealth tests against protected endpoints (Cloudflare/Captcha).
*   **Playwright (Tool):** Executes standard functional tests.
*   **Speckit (Orchestrator):** Manages the test execution flow.

================================================================================
## TOOLS
================================================================================

### 1. Camoufox (Stealth Engine)
**Why:** To test production environments protected by anti-bot systems.

```python
# Usage via MCP Tool
python3 global/tools/web_scraper.py --url "https://target.com" --wait_for ".login-form"
```

**Key Features:**
*   Bypasses Cloudflare/Akamai.
*   Generates Accessibility Snapshots (low token usage).
*   Handles Captchas automatically.

### 2. Playwright (Standard Engine)
**Why:** Fast, reliable, multi-browser support for internal/staging environments.

```bash
npx playwright test
```

================================================================================
## E2E TESTING WORKFLOW
================================================================================

### Step 1: The QA Design Phase
**Role:** QA
1.  **Identify Critical Paths:** Login, Checkout, Registration.
2.  **Define Success Criteria:** What constitutes a "Pass"?
3.  **Select Engine:**
    *   Internal/Staging -> Playwright.
    *   Production/Protected -> Camoufox.

### Step 2: Test Implementation

#### A. Using Playwright (Standard)
```typescript
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.click('[data-testid="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

#### B. Using Camoufox (Stealth)
```python
# tests/e2e/stealth_login.py
from global.tools.web_scraper import CamoufoxScraper

scraper = CamoufoxScraper()
result = scraper.navigate("https://prod.site.com/login")
scraper.input("#email", "user@example.com")
scraper.click("#submit")
assert "Dashboard" in scraper.get_snapshot()
```

### Step 3: Execution & Reporting
1.  **Run Verification:**
    ```bash
    python3 global/tools/speckit.py verify
    ```
    *   This ensures no secrets are leaked in test files (Sentinel).
    *   This runs CodeRabbit to check test quality.

2.  **Log Results:**
    *   Log failures in `system_log.md`.
    *   Create tickets for the Builder Role.

================================================================================
## CHECKLIST
================================================================================
- [ ] Critical paths covered (Login, Payment, Core Feature).
- [ ] Stealth tests passing on Production.
- [ ] Standard tests passing on Staging.
- [ ] Screenshots captured for failures.
- [ ] Sentinel Check Passed (No Secrets in Test Files).
