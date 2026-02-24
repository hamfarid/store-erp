# 🎨 Frontend Development Rules (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel & CodeRabbit

## 1. The Philosophy
The frontend is the user's reality. It MUST be fast, accessible, and beautiful.

## 2. Core Principles
*   **Mobile-First:** Design for mobile first, then scale up.
*   **Accessibility:** WCAG 2.1 AA compliance is MANDATORY.
*   **Performance:** First Contentful Paint (FCP) < 1.5s.

## 3. Architecture (React/Next.js)
*   **Component Structure:** Atomic Design (Atoms, Molecules, Organisms).
*   **State Management:** Use Context API for global state, local state for UI.
*   **Hooks:** Custom hooks for logic reuse. NO logic in UI components.

## 4. Code Quality (Sentinel Enforced)
*   **No Inline Styles:** Use Tailwind CSS or CSS Modules.
*   **PropTypes/TypeScript:** Props validation is MANDATORY.
*   **Console Logs:** FORBIDDEN in production code.

## 5. User Experience
*   **Feedback:** Every action MUST have visual feedback (loading, success, error).
*   **Error Boundaries:** Wrap major sections in Error Boundaries.
*   **Empty States:** Handle empty data states gracefully.

## 6. Testing
*   **Unit Tests:** Test components in isolation (Jest/Vitest).
*   **E2E Tests:** Critical flows MUST be tested with Playwright.
