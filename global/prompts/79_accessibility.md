# PROMPT 79: ACCESSIBILITY (A11Y)

**Objective:** Ensure the application is accessible to all users, including those with disabilities, by following WCAG 2.1 AA guidelines.

---

## 🎯 REQUIREMENTS

1.  **Semantic HTML:** Use correct HTML5 elements for their intended purpose (e.g., `<nav>`, `<main>`, `<button>`).
2.  **ARIA Roles:** Use ARIA (Accessible Rich Internet Applications) roles and attributes where necessary to provide additional context to assistive technologies.
3.  **Keyboard Navigation:** All interactive elements must be focusable and operable via the keyboard.
4.  **Color Contrast:** All text must have a minimum color contrast ratio of 4.5:1 against its background.
5.  **Alt Text:** All images must have descriptive `alt` text.
6.  **Form Labels:** All form inputs must have associated `<label>` elements.

---

## 📝 PHASES OF IMPLEMENTATION

### Phase 1: Automated Audit
1.  **Install Tool:** Add an automated accessibility auditing tool (e.g., Axe, Lighthouse) to the project.
2.  **Run Audit:** Run the audit on all pages of the application.
3.  **Generate Report:** Generate a report of all accessibility issues.

### Phase 2: Manual Review
1.  **Keyboard Test:** Manually navigate the entire application using only the keyboard.
2.  **Screen Reader Test:** Use a screen reader (e.g., NVDA, VoiceOver) to navigate the application and verify that all content is read correctly.
3.  **Color Contrast Check:** Use a color contrast checker tool to verify that all text meets the minimum contrast ratio.

### Phase 3: Remediation
1.  **Prioritize Issues:** Prioritize the issues identified in the audit and manual review.
2.  **Fix Issues:** Fix the issues, starting with the most critical ones.
3.  **Re-test:** Re-run the audit and manual review to verify that the issues have been resolved.

---

## ✅ SUCCESS CRITERIA

- The application passes the automated accessibility audit with zero critical issues.
- All interactive elements are keyboard-accessible.
- All images have alt text.
- All form inputs have labels.
- The application is usable with a screen reader.
