# Frontend Architecture (Global System Ultimate)

## Core Philosophy
The frontend architecture is built on **Component-Based Design**, **Separation of Concerns**, and **Type Safety**. We prioritize user experience (UX), performance, and maintainability.

## 7 Core Layers

### 1. UI Components (Atomic Design)
*   **Atoms:** Basic building blocks (Buttons, Inputs, Icons).
*   **Molecules:** Groups of atoms (Search Bar, Form Field).
*   **Organisms:** Complex sections (Header, Product Card).
*   **Templates:** Page layouts without content.
*   **Pages:** Instances of templates with real data.

### 2. State Management
*   **Local State:** `useState` / `useReducer` for component-specific data.
*   **Global State:** `Context API` / `Zustand` / `Redux Toolkit` for app-wide data (User, Theme).
*   **Server State:** `TanStack Query` (React Query) for caching and syncing API data.

### 3. API Client Layer
*   **Centralized Axios/Fetch Instance:** With interceptors for Auth and Error handling.
*   **Typed Responses:** All API calls must return typed data interfaces.
*   **Service Pattern:** `services/authService.ts`, `services/productService.ts`.

### 4. Routing
*   **File-based Routing:** (Next.js) or **Config-based Routing:** (React Router).
*   **Guards:** Protected routes for authenticated users.
*   **Lazy Loading:** Code splitting for routes to improve initial load time.

### 5. Styling System
*   **Tailwind CSS:** Utility-first framework for rapid development.
*   **CSS Modules / Styled Components:** For complex, isolated component styles.
*   **Design Tokens:** Centralized colors, typography, and spacing in `tailwind.config.js`.

### 6. Assets Management
*   **Optimization:** WebP/AVIF for images.
*   **CDN:** Serve static assets from a CDN (e.g., Cloudflare R2, AWS S3).
*   **SVGs:** Use inline SVGs or sprites for icons.

### 7. Testing & Quality
*   **Unit Tests:** Jest/Vitest for logic and utilities.
*   **Component Tests:** React Testing Library for UI interaction.
*   **E2E Tests:** Playwright for critical user flows.

## Best Practices

*   **Mobile First:** Design for small screens first, then scale up.
*   **Accessibility (a11y):** Semantic HTML, ARIA labels, keyboard navigation.
*   **Performance:** Core Web Vitals (LCP, FID, CLS) optimization.
*   **Strict TypeScript:** No `any` types allowed.
