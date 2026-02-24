# Playwright Testing Guidelines

## Overview
Playwright is our standard for End-to-End (E2E) and Integration testing. It allows us to test across all modern rendering engines (Chromium, WebKit, Firefox).

## Testing Strategy
1.  **E2E Tests:**
    -   Test critical user flows (e.g., Signup, Checkout, Critical Business Logic).
    -   Run against a staging environment or a full local stack.
2.  **Integration Tests:**
    -   Test interactions between components or with the API.
    -   Mock external services where appropriate.
3.  **Visual Regression:**
    -   Use `expect(page).toHaveScreenshot()` to catch visual regressions.

## Best Practices
1.  **Locators:** Use user-facing locators (e.g., `getByRole`, `getByText`) instead of CSS selectors or XPaths. This ensures tests resemble how users interact with the app.
2.  **Isolation:** Each test should be independent. Use `test.beforeEach` to set up state.
3.  **Authentication:** Use `global-setup` to save authentication state and reuse it across tests to save time.
4.  **Waiting:** Avoid manual `page.waitForTimeout()`. Use auto-waiting assertions (e.g., `expect(locator).toBeVisible()`).

## Example
```typescript
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).toHaveURL('/dashboard');
});
```
