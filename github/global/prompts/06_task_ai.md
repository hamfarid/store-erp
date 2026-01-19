# PROMPT 06: TASK AI & PLANNING (v29.0)

## 1. The "Context First" Plan Structure
**Rule:** Every task plan MUST start with a "Context Loading" phase.
*   **Phase 0:** Read Context Files.
    *   *Action:* Read `global/rules/99_context_first.md` to identify required files.
    *   *Action:* Read `project_memory.md`.
    *   *Action:* Read specific code files (e.g., `src/App.tsx`).

## 2. The "Visual Thinking" Phase
**Rule:** For complex tasks, Phase 1 MUST be "Visual Architecture".
*   *Action:* Create a Mermaid diagram of the proposed solution.
*   *Action:* Verify the diagram against `global/docs/ARCHITECTURE.md`.

## 3. The "Atomic Execution"
**Rule:** Break tasks into atomic units that include documentation.
*   *Bad:* "Implement Auth"
*   *Good:* "Implement Login API + Update Routes.md + Add Tests"

## 4. The "Definition of Done"
**Rule:** A task is ONLY done when:
1.  Code is written.
2.  Tests pass.
3.  Documentation is updated.
4.  `project_memory.md` is updated with new XP.

# Hierarchical Task Management (v25.0)

## 1. The Visual Dashboard (`plan.md`)
The `plan.md` file MUST start with a visual status dashboard.

### Template:
```markdown
# 📊 Project Dashboard: [Project Name]

**Status:** 🟢 On Track | 🟡 At Risk | 🔴 Blocked
**Progress:** [████████░░] 80%
**Current Sprint:** Sprint 4 (Auth & Security)

---

## 🚀 Epics & Stories

### 🟢 Epic 1: User Authentication (100%)
- [x] Story: Login with Email
- [x] Story: Login with Google

### 🟡 Epic 2: Dashboard UI (50%)
- [x] Story: Sidebar Navigation
- [ ] Story: Analytics Widgets (In Progress)
```

## 2. The Hierarchy
We do not just "do tasks". We execute a strategy.

### Level 1: Epics (The "Big Picture")
*   *Example:* "User Authentication System"
*   *File:* `plan.md` (Top level)

### Level 2: Stories (The "User Value")
*   *Example:* "As a user, I want to login with Google so I don't need a password."
*   *File:* `plan.md` (Sub-sections)

### Level 3: Tasks (The "Dev Work")
*   *Example:* "Configure Google OAuth in Supabase Dashboard."
*   *File:* `todo.md` (Actionable items)

---

## 3. The Workflow
1.  **Breakdown:** AI analyzes the request -> Creates Epics -> Breaks into Stories -> Lists Tasks.
2.  **Validation:** "Does this task deliver the story? Does the story deliver the epic?"
3.  **Execution:** Pick a task from `todo.md` -> Move to "In Progress" -> Code -> Test -> Move to "Done".

---

## 4. Speckit Integration
*   Use **Speckit** to maintain the `plan.md` and `todo.md` files.
*   **Rule:** Never start a task without a corresponding Story in `plan.md`.
