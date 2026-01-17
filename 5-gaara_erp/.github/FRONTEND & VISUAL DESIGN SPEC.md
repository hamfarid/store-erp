Purpose: Define the UI/UX, component system, branding, SDUI, security on the client, performance budgets, testing, and governance for all frontends (web/desktop/mobile shells). Use this to design from scratch and to audit/fix existing UIs.

A) Stack Selection (mark [X])

Framework:

 React + TypeScript

 Next.js (SSR/SSG/ISR)

 Vue 3 (Composition API)

 Angular

 SvelteKit

Patterns:

 SDUI (Server-Driven UI) renderer enabled

 BFF pattern (API facade) for FE

State/Data:

 Redux Toolkit + RTK Query

 React Query / TanStack Query

 Zustand / Signals (local)

Forms & Validation:

 React Hook Form + Zod (schema validation)

Styling:

 CSS Variables (tokens) + utility CSS (Tailwind)

 Component lib: MUI / Chakra / AntD / shadcn/ui (choose one)

Charts/Maps:

 Chart.js / ECharts

 MapLibre / Leaflet / Google Maps

i18n/RTL:

 i18next + ICU

 RTL support required (mirroring, bidi)

Platform:

 PWA (offline shell, installable)

 Electron/Tauri shell (optional)

B) Brand System & Design Tokens (Gaara/MagSeeds)

Single source of truth: /ui/theme/tokens.json and /docs/Brand_Palette.json.

Tokens only in components (no hex in components).

Map brand to tokens:

color.brand.primary|secondary|accent|success|warning|danger

typography.font.family.en|ar, typography.size.scale, lineHeight, letterSpacing

radius.sm|md|lg, shadow.sm|md|lg, opacity, zIndex

spacing.xs..3xl, breakpoints.sm|md|lg|xl|2xl

Required: Light & Dark themes; high-contrast variants for AA.

Motion: duration scale (fast|base|slow) and easing tokens; subtle micro-interactions for hover/focus/press/async.

Iconography: unified set; match semantic tokens (don’t bake colors).

Seed file (example) — /ui/theme/tokens.json:

{
  "FILE": "ui/theme/tokens.json | PURPOSE: Brand tokens | OWNER: UI | LAST-AUDITED": "2025-10-28",
  "color": {
    "brand": { "primary": "#0F6CBD", "secondary": "#0A3D62", "accent": "#1ABC9C" },
    "neutral": { "50": "#F8FAFC", "900": "#0B1220" },
    "text": { "default": "{color.neutral.900}", "muted": "{color.neutral.600}" }
  },
  "typography": {
    "font": { "family": { "en": "Inter, system-ui, sans-serif", "ar": "Tajawal, system-ui, sans-serif" } },
    "size": { "xs": 12, "sm": 14, "md": 16, "lg": 18, "xl": 20, "2xl": 24 }
  },
  "radius": { "sm": 4, "md": 8, "lg": 12 },
  "spacing": { "xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "2xl": 32, "3xl": 48 },
  "breakpoints": { "sm": 640, "md": 768, "lg": 1024, "xl": 1280, "2xl": 1536 }
}

C) Layout, Navigation & Components

Layout grid: responsive 12-column; safe areas on mobile.

Navigation: AppShell (topbar + left nav), breadcrumbs, Command Palette (⌘/Ctrl-K) for power users.

Core components (all must exist & be tokenized):

Buttons (primary/secondary/tertiary/destructive/ghost)

Inputs (text/number/date/time), Selects, Autocomplete, Textarea

Toggles, Radios, Checkboxes, Chips

Tables (virtualized), Pagination, Column filters, Density switch

Cards, Tabs, Accordions, Steppers/Wizards

Modals/Drawers, Toasts/Alerts, Empty/Loading/Skeleton states

File uploader (scan + size/type guard), Image optimizer

Charts (line/bar/pie), KPI tiles, Heatmaps (optional)

Forms UX: inline validation, error summaries, autosave (where safe), optimistic UI for idempotent actions.

CRUD templates: List → View → Create/Edit (wizard if long); consistent action bars.

D) Accessibility, i18n & RTL

WCAG AA minimum; maintain color-contrast budgets in CI (Lighthouse).

Keyboard: focus order, :focus-visible, skip links, roving tabindex in menus.

ARIA roles & labels for interactive UI.

i18n: ICU messages, pluralization/gender; dynamic direction (dir=auto); number/date/locale formatting.

RTL: mirrored layouts & icons where appropriate; test both LTR/RTL in CI.

E) Security & Privacy (Client)

CSP nonces: no inline scripts/styles; hydrate with server nonces.

DOM sanitization: DOMPurify for any HTML render.

Secrets: none in FE bundle; config via env-injected public keys only (non-sensitive).

AuthN/Z in UI: route guards + button/feature guards bound to RBAC (ADMIN, MODIFY, READ, VIEW_LIGHT, APPROVE).

Anti-enumeration: generic error to users; details only in logs.

Route obfuscation: hashed labels from allowlisted map; content-hashed chunks.

SUDI (if enabled): device attestation state surfaced (read-only), graceful UI when untrusted.

F) Performance Budgets (CI-enforced)

Route-level budgets (mobile on 4x CPU throttle, Slow 4G):

First Contentful Paint (FCP) ≤ 1.8s

Largest Contentful Paint (LCP) ≤ 2.5s

Time to Interactive (TTI) ≤ 3.0s

Total Blocking Time (TBT) ≤ 200ms

Cumulative Layout Shift (CLS) ≤ 0.10

JS per route ≤ 170KB gz (initial), CSS ≤ 40KB gz

Image policy: next-gen formats (AVIF/WebP), responsive sizes, lazy-loading, placeholders.

G) SDUI (Server-Driven UI)

Contract: /contracts/sdui.schema.json (semver, append-only).

Node types: Page, Section, Grid, Card, Form, Field, Table, Chart, Action, NavItem.

Security: JWS-signed payloads + ETag; per-node RBAC; renderer allow-list (no eval/new Function).

Telemetry: client emits rendered, interacted, failed with traceId.

Minimal schema seed:

{
  "$schema": "https://example/sdui.schema.json",
  "version": "1.0.0",
  "page": {
    "id": "dashboard",
    "title": "Dashboard",
    "nodes": [
      { "type": "KPI", "props": { "label": "Active Users", "query": "kpi_active_users" }, "rbac": ["READ"] }
    ]
  }
}

H) Observability Hooks (Activity, Health, Monitoring)

log_activity (FE hooks): wrap navigations, critical button clicks, CRUD ops, export triggers; capture traceId,userId?,route,action,outcome,latency_ms.

system_health (client metrics): basic FE vitals (CLS/LCP/FID) + network downlink, rtt; surface in Ops dashboard.

system_monitoring: anomaly hints (e.g., waterfall spikes, error bursts) forwarded to BE AI monitor; no auto-action.

I) Frontend File/Folder Convention (React example)
/ui
  /theme            # tokens, global.css, theme switch
  /components       # primitive + composite components
  /modules          # feature modules (bounded contexts)
  /hooks            # reusable hooks
  /providers        # app providers (i18n, theme, query, auth)
  /pages            # route entries (Next.js) or /routes (SPA)
  /sdui             # renderer + schema types
  /icons            # central icon registry
  /tests            # unit/integration


Header in every file (line 1):
FILE: <repo-path> | PURPOSE: … | OWNER: UI | RELATED: … | LAST-AUDITED: <YYYY-MM-DD>

J) Page Blueprints (must exist)

Auth: Login (MFA optional), Forgot/Reset, Lockout states; secure error messaging.

Dashboard: KPIs, recent activity, quick actions, notifications.

Entity CRUD: List (filters, saved views) → View (audit trail) → Create/Edit (wizard support).

Search: global search + scoped filters; keyboard shortcuts; recent searches.

Reports: filters, preview, Export (Excel/PDF/CSV/PPT); long-running → async job with toast + activity log entry.

Admin: Users/Roles/Permissions (RBAC matrix), Activity Log browser, Backups panel, System Health and Monitoring tabs.

K) Testing & Visual QA

Unit: components/hooks (Jest/Vitest, React Testing Library).

Integration: forms, tables, complex flows.

E2E: Playwright (auth flows, critical business journeys).

A11y: axe-core automatic checks; manual keyboard runs.

Visual Regression: Chromatic/Playwright snapshots for core pages.

Budgets: Lighthouse CI gates (perf/a11y/SEO/PWA) must pass.

L) Acceptance Criteria (Definition of Done — Frontend)

Uses tokens only (no raw hex/px in components).

WCAG AA meets; keyboard and screen-reader verified.

Lighthouse budgets pass for target device profiles.

All critical buttons are instrumented to log_activity.

RBAC guards applied to routes, menus, actions, fields.

No inline scripts/styles; CSP nonces respected; DOM sanitized.

SDUI pages (if used) validate against schema; renderer allow-list enforced.

Exports work and run async when heavy; user gets status & link.

All pages have Empty/Loading/Error states.

i18n/RTL rendering verified (labels, numeral/date formats).

File header present in every source file.

Task list updated; docs appended (UI_Design_System.md, Brand_Palette.json, Pages_Coverage.md).

M) Call-to-Action Styling (Brand)

Bold, high-contrast palette (from brand tokens), ample white space.

Smooth animations (duration tokens) and micro-interactions on focus/press/async.

Modern, consistent iconography per module.

Keep motion subtle and accessible (reduced-motion preference respected).

Quick Start — What to do now

Tick boxes in A) Stack Selection and confirm tokens in /ui/theme/tokens.json.

Scaffold Page Blueprints and Core Components using tokens only.

Wire RBAC guards, log_activity hooks, and SDUI renderer (if selected).

Add Lighthouse CI and axe checks; set budgets in CI.

Fill Pages_Coverage.md, UI_Design_System.md, and update Brand_Palette.json.