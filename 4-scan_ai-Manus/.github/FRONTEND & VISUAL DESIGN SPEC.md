# Gaara Scan AI - Frontend & Visual Design Specification

**Version:** 2.0  
**Last Updated:** December 13, 2025  
**Scope:** Defines the technical specifications, component architecture, and visual design guidelines for the Gaara Scan AI frontend.

---

## I. CORE PRINCIPLES

1.  **Performance**: The application must be fast and responsive. Target a Lighthouse Performance score of 90+.
2.  **Accessibility (A11y)**: The application must be usable by everyone. Comply with WCAG 2.1 AA standards.
3.  **Consistency**: The UI must be consistent across all pages and components.
4.  **Maintainability**: The codebase must be clean, well-documented, and easy to modify.

---

## II. TECHNICAL STACK

| Category | Technology | Rationale |
|---|---|---|
| **Framework** | React 18+ | Industry standard, large ecosystem, hooks for stateful logic. |
| **Build Tool** | Vite | Extremely fast development server and optimized production builds. |
| **Styling** | Tailwind CSS | Utility-first CSS for rapid, consistent, and maintainable styling. |
| **UI Components** | Radix UI | Headless, accessible, and unstyled components for building a custom design system. |
| **State Management** | React Context API | Sufficient for global state (e.g., auth) without adding a heavy library. |
| **Forms** | React Hook Form | Performant, flexible, and easy-to-use form validation. |
| **Routing** | React Router | Standard for routing in React applications. |
| **Testing** | Vitest + React Testing Library | Fast, modern testing framework with a focus on user-centric testing. |

---

## III. VISUAL DESIGN & BRANDING

### Color Palette

| Role | Light Mode | Dark Mode | Usage |
|---|---|---|---|
| **Primary** | `#2E7D32` (Green) | `#66BB6A` (Light Green) | Buttons, links, active states, key actions |
| **Secondary** | `#FFA000` (Amber) | `#FFCA28` (Lighter Amber) | Highlights, notifications, secondary actions |
| **Background** | `#FFFFFF` (White) | `#121212` (Near Black) | Main page background |
| **Surface** | `#F5F5F5` (Light Gray) | `#1E1E1E` (Dark Gray) | Cards, modals, sidebars |
| **Text** | `#212121` (Near Black) | `#E0E0E0` (Light Gray) | Body text, headings |
| **Subtle Text** | `#757575` (Gray) | `#BDBDBD` (Lighter Gray) | Placeholders, disabled text, metadata |
| **Error** | `#D32F2F` (Red) | `#E57373` (Light Red) | Error messages, destructive actions |

### Typography

- **Font Family**: `Inter` (or a similar sans-serif system font) for all text.
- **Base Font Size**: `16px`.
- **Scale**: Use a modular scale for headings (e.g., 1.25x).
    -   `h1`: 2.44rem
    -   `h2`: 1.95rem
    -   `h3`: 1.56rem
    -   `h4`: 1.25rem

### Spacing & Layout

- **Base Unit**: `4px`. All spacing (padding, margin, gaps) should be a multiple of the base unit.
- **Layout**: Use a responsive grid system (e.g., CSS Grid or Flexbox) for page layouts.
- **Max Width**: Main content should have a max-width of `1280px` and be centered on larger screens.

---

## IV. COMPONENT ARCHITECTURE

The frontend will be built using a component-based architecture.

### Directory Structure
```
frontend/src/
├── api/             # API client and service definitions
├── assets/          # Static assets (images, fonts)
├── components/      # Reusable, shared components
│   ├── ui/          # Generic UI elements (Button, Input, Card)
│   └── domain/      # Domain-specific components (FarmList, DiagnosisChart)
├── context/         # React Context providers (AuthContext, DataContext)
├── hooks/           # Custom React hooks (useDebounce, useApi)
├── pages/           # Top-level route components
├── styles/          # Global styles and Tailwind configuration
├── utils/           # Utility functions
└── App.jsx          # Main application component with routing
```

### Component Design

1.  **Presentational vs. Container**: Separate logic (data fetching, state management) from presentation.
    -   **Container Components** (often in `pages/`) are responsible for fetching data and managing state.
    -   **Presentational Components** (in `components/`) receive data via props and are responsible for rendering the UI.

2.  **Composition**: Build complex components by composing simpler ones. Favor composition over inheritance.

3.  **Props**: Use clear and consistent prop names. Use TypeScript or PropTypes for type checking.

---

## V. KEY UI/UX PATTERNS

### Forms
- **Validation**: Provide real-time, inline validation as the user types.
- **Labels**: All form inputs must have a corresponding `<label>`.
- **Feedback**: Provide clear success and error messages upon submission.
- **State**: Use `react-hook-form` to manage form state.

### Data Display
- **Tables**: Use tables for dense, structured data. Tables must be responsive.
- **Cards**: Use cards for less dense, more visual data.
- **Empty States**: When a list is empty, display a helpful message and a call-to-action (e.g., "No farms found. Add your first farm!").
- **Loading States**: Display skeleton loaders or spinners while data is being fetched.

### Navigation
- **Primary Navigation**: A persistent sidebar for main application routes.
- **Secondary Navigation**: Tabs or breadcrumbs for sub-sections within a page.
- **Active States**: Clearly indicate the user's current location in the navigation.

### User Feedback
- **Toasts/Notifications**: Use non-intrusive toast notifications for feedback on actions (e.g., "Farm created successfully").
- **Modals**: Use modals for critical actions that require the user's full attention (e.g., confirming a deletion).

---

## VI. ACCESSIBILITY (A11y) CHECKLIST

- [ ] **Semantic HTML**: Use correct HTML5 elements (`<nav>`, `<main>`, `<aside>`, etc.).
- [ ] **Keyboard Navigation**: All interactive elements must be focusable and operable via the keyboard.
- [ ] **Focus Management**: Ensure focus is managed correctly, especially in modals and after route changes.
- [ ] **Image `alt` Text**: All `<img>` elements must have descriptive `alt` attributes.
- [ ] **ARIA Roles**: Use ARIA attributes where necessary to provide additional context to assistive technologies.
- [ ] **Color Contrast**: Ensure all text meets WCAG AA contrast ratios.
