# 🎨 Project Template: Frontend-Only (Global System Ultimate)

**Status:** MANDATORY BLUEPRINT
**Enforcement:** Automated by Speckit (Plan Phase)

## 1. The Philosophy
The frontend is the user's reality. It must be fast, accessible, and type-safe.

## 2. The Mandatory Structure
```
frontend-project/
├── src/
│   ├── components/     # Atomic Design (Atoms, Molecules, Organisms)
│   ├── features/       # Domain Logic (Auth, Dashboard)
│   ├── hooks/          # Custom Hooks
│   ├── services/       # API Clients
│   ├── store/          # State Management
│   ├── types/          # TypeScript Definitions
│   ├── utils/          # Pure Functions
│   └── App.tsx         # Root
├── tests/              # Vitest + Playwright
└── vite.config.ts      # Build Config
```

## 3. The Stack
*   **Framework:** React 18+ (TypeScript).
*   **Build:** Vite.
*   **State:** Zustand or Redux Toolkit.
*   **Styling:** Tailwind CSS.
*   **Testing:** Vitest (Unit), Playwright (E2E).

## 4. Zero-Tolerance Rules
1.  **No `any`:** TypeScript `any` is FORBIDDEN.
2.  **No Inline Styles:** Use Tailwind classes.
3.  **Accessibility:** All interactive elements MUST have `aria-label` or visible text.
4.  **Performance:** Code splitting is MANDATORY for routes.

## 5. API Integration
You MUST use a centralized Axios instance with interceptors.
```typescript
// src/services/api.ts
// Sentinel Check: Auth token injection is mandatory
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```
