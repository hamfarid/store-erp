# RULE 99: THE CONTEXT FIRST MANDATE (v29.0)

## 🛑 STOP! READ THIS BEFORE WRITING CODE.

**The Golden Rule:** You are FORBIDDEN from writing a single line of code or proposing a solution until you have explicitly READ the relevant context files. "Assuming" you know the context is a critical failure.

## 1. Mandatory Reading Lists (The "Pre-Flight Check")

Before starting any task, identify the **Task Type** and read the corresponding files:

### 🎨 Frontend Tasks (React/Next.js/UI)
*   **MUST READ:**
    1.  `global/prompts/21_frontend.md` (Standards)
    2.  `client/src/index.css` (Global Styles/Tailwind Config)
    3.  `client/src/App.tsx` (Routing & Providers)
    4.  `project_memory.md` (User Preferences)
*   **IF EDITING A COMPONENT:** Read the existing component file AND its parent.

### ⚙️ Backend Tasks (API/Server)
*   **MUST READ:**
    1.  `global/prompts/20_backend.md` (Architecture)
    2.  `server/routes.ts` (or equivalent API definition)
    3.  `global/docs/DATABASE_SCHEMA.md` (Data Model)
*   **IF ADDING A ROUTE:** Read `global/prompts/30_security.md` (Auth/Validation).

### 🗄️ Database Tasks (Schema/Migrations)
*   **MUST READ:**
    1.  `global/prompts/77_database_migrations.md` (Migration Rules)
    2.  `global/docs/DATABASE_SCHEMA.md` (Current Schema)
    3.  `server/db.ts` (Connection Logic)

### 🧪 Testing Tasks
*   **MUST READ:**
    1.  `global/prompts/41_testing.md` (Strategy)
    2.  `global/prompts/42_e2e_testing.md` (Playwright Rules)

## 2. The "Proof of Context" Protocol
In your **Thinking Process** (before the first tool call), you MUST output:
> **[Context Verification]**
> *   ✅ Read `global/prompts/21_frontend.md` -> Confirmed Shadcn UI usage.
> *   ✅ Read `client/src/App.tsx` -> Confirmed routing structure.
> *   ✅ Read `project_memory.md` -> Noted user prefers "Dark Mode".

## 3. The "Blindness" Penalty
If you attempt to generate code without reading these files, you are violating the core directive of the Omniscient Edition. You will likely produce "Hallucinated Code" that conflicts with the existing project structure.
