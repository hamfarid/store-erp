# 🏗️ Project Template: Full-Stack (Global System Ultimate 2026)

**Status:** MANDATORY BLUEPRINT
**Enforcement:** Automated by Speckit (Plan Phase)
**Version:** Global System Ultimate v15.9.8 - Verified Feb 2026

## 1. The Philosophy
Structure is destiny. A messy folder structure leads to messy code. In 2026, we prioritize **modularity**, **type safety**, and **performance**.

## 2. The Mandatory Structure (2026 Standard)
```
project/
├── apps/                   # Monorepo Structure
│   ├── web/                # React 19.2.4 + Vite/Bun
│   │   ├── src/
│   │   │   ├── features/   # Feature-based architecture
│   │   │   ├── shared/     # Shared UI/Hooks
│   │   │   └── app/        # App entry & routing
│   │   └── vite.config.ts
│   ├── api/                # FastAPI 0.129+ / Hono (Bun)
│   │   ├── src/
│   │   │   ├── modules/    # Domain-driven modules
│   │   │   ├── core/       # Core logic & config
│   │   │   └── main.py     # Server Entry
│   │   └── tests/          # Pytest / Vitest
├── packages/               # Shared Libraries
│   ├── ui/                 # Design System
│   ├── db/                 # Database Schema & Migrations
│   └── config/             # Shared Configs (ESLint, TS)
├── infra/                  # Infrastructure as Code (Terraform/Pulumi)
└── .github/                # CI/CD (AI-Ops)
```

## 3. The Stack (2026 Edition)
*   **Frontend:** React 19.2.4 (Server Components), Tailwind v4, TanStack Query v6.
*   **Backend:** FastAPI 0.129+ (Python 3.14) OR Hono (Bun/Edge).
*   **Runtime:** Bun (for JS/TS) / uv (for Python).
*   **Database:** PostgreSQL 18.2 (with Drizzle/Prisma).
*   **Auth:** Passkeys + OIDC (Stateless).
*   **AI Integration:** LangChain / LlamaIndex (Native Support).

## 4. Zero-Tolerance Rules
1.  **No Secrets:** `.env` is ignored by Git. Use Secret Managers.
2.  **Strict Typing:** TypeScript `strict: true` and Python `mypy --strict`.
3.  **Feature Slicing:** Code must be organized by feature, not type.
4.  **AI-Ready:** All APIs must have OpenAPI specs for AI consumption.
