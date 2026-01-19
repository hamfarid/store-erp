# MASTER PROMPT v24.0 (The "Project OS")

## 1. System Initialization & IDE Awareness
**First Action:** Detect the environment and configure the workspace.

### IDE Detection Logic
1.  **Check Environment:**
    *   If `.cursorrules` exists -> Mode: **Cursor AI**.
    *   If `.windsurfrules` exists -> Mode: **Windsurf**.
    *   If `.vscode/` exists -> Mode: **VS Code**.
2.  **Action:**
    *   **Copy Rules:** Automatically copy the relevant rule file from `global/rules/ide_configs/` to the project root.
    *   *Example:* `cp global/rules/ide_configs/cursor.md .cursorrules`

---

## 2. Project Analysis (The "Doctor" Phase)
Before writing code, diagnose the patient.
1.  **Scan:** `ls -R`, `cat package.json`, `cat requirements.txt`.
2.  **Classify:**
    *   **Greenfield:** New project -> Use **Modern Stack** (Nx, Supabase, Playwright).
    *   **Brownfield:** Existing project -> Use **Legacy Support** (Respect existing choices).
3.  **Memory Check:** Load `project_memory.md` to recall past decisions.

---

## 3. Execution Loop (The "Agent" Phase)
1.  **Plan:** Use **Speckit** to generate a hierarchical plan (Epics -> Stories -> Tasks).
2.  **Context:** Use **Context7** (Exa) to fetch external docs if needed.
3.  **Code:** Implement the task.
4.  **Test:** Run Playwright/Vitest.
5.  **Reflect:** Update `project_memory.md` with lessons learned.

---

## 4. The "Supabase First" Mandate
*   **Database:** Postgres via Supabase.
*   **Auth:** Supabase Auth.
*   **Migrations:** `supabase db diff` & `supabase db push`.
*   **No Manual SQL:** All schema changes must be versioned migrations.
