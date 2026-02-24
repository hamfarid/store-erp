================================================================================
MODULE 43: UI/UX TESTING & FIXES Global System Ultimate (Synchronized Intelligence Edition)
================================================================================
Version: Dynamic
Purpose: Frontend testing, visual regression, and UX validation using the **QA Role**.
================================================================================

## OVERVIEW

UI/UX testing ensures the frontend is not just functional, but **delightful** and **pixel-perfect**.
This module leverages the **QA Role** and **Speckit Global System Ultimate** to enforce strict visual standards.

## ROLES & RESPONSIBILITIES

*   **The QA (Primary):** Acts as the user's advocate. Checks for alignment, contrast, and responsiveness.
*   **The Builder:** Fixes the issues identified by the QA.
*   **Speckit (Orchestrator):** Automates the visual regression workflow.

================================================================================
## COMMON UI/UX ISSUES & FIXES
================================================================================

### 1. Visual Regression (The "Pixel" Check)
**Role:** QA
**Tool:** Playwright Visual Comparison

**Workflow:**
1.  Take a baseline screenshot of the "Golden State".
2.  Run tests on the new build.
3.  Compare screenshots.

```typescript
test('visual regression', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', { maxDiffPixels: 100 });
});
```

### 2. Responsive Design (The "Mobile" Check)
**Role:** QA
**Checklist:**
- [ ] Does the menu collapse on mobile?
- [ ] Are touch targets large enough (min 44px)?
- [ ] Is there horizontal scrolling (bad)?

**Fix (CSS):**
```css
@media (max-width: 768px) {
  .container { padding: 1rem; }
  .menu { display: none; } /* Use hamburger */
}
```

### 3. Accessibility (The "A11y" Check)
**Role:** QA
**Tool:** Axe-core / Lighthouse

**Checklist:**
- [ ] Color contrast ratio > 4.5:1.
- [ ] Images have `alt` text.
- [ ] Interactive elements are keyboard accessible.

**Fix:**
```html
<!-- Bad -->
<div onclick="submit()">Submit</div>

<!-- Good -->
<button onclick="submit()" aria-label="Submit Form">Submit</button>
```

================================================================================
## THE QA PROTOCOL
================================================================================

1.  **Visual Inspection:** Manually verify the UI against the design spec (Figma/Sketch).
2.  **Interactive Walkthrough:** Click every button, fill every form.
3.  **Cross-Browser Test:** Chrome, Firefox, Safari (via Playwright).
4.  **Verification:** Run `python3 global/tools/speckit.py verify` to ensure no regressions.
5.  **Report:** Log all UI glitches in `system_log.md` with screenshots.
