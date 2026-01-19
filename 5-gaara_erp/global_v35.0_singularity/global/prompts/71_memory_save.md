# PROMPT 71: MEMORY & GAMIFICATION (v28.0)

## 1. The "Project Memory" Structure
**Rule:** Every project MUST have a `.memory/` folder containing:
*   `project_memory.md`: The central brain (User Prefs, Active Epic, XP).
*   `decisions.md`: Log of all architectural decisions (ADRs).
*   `context/`: Folder for active task context.

## 2. The Gamification System (New in v28.0)
**Rule:** Track progress using an XP system to maintain momentum.
*   **XP Awards:**
    *   +10 XP: Task Completed.
    *   +50 XP: Epic Completed.
    *   +100 XP: Zero-Bug Release.
    *   -20 XP: Breaking the Build.
*   **Levels:**
    *   Lvl 1: Script Kiddie (0-500 XP)
    *   Lvl 5: Senior Engineer (2500 XP)
    *   Lvl 10: 10x Developer (10,000 XP)
*   **Achievements:**
    *   🏆 "Clean Code": Pass linting on first try.
    *   🛡️ "Fortress": Pass security audit with 0 issues.

## 3. Memory Persistence
**Rule:** Before ending any session, you MUST:
1.  Update `project_memory.md` with current XP and Level.
2.  Save the state of the current task in `context/current_task.md`.
3.  Commit these changes to git.

## 4. User Preferences
**Rule:** Store user likes/dislikes in `project_memory.md`.
*   *Example:* "User hates `useEffect` for data fetching. Use `TanStack Query`."
*   *Example:* "User prefers 'Dark Mode' default."

# Persistent Memory System (v25.0)

## 1. The "Project Brain" (`project_memory.md`)
Every project MUST have a `project_memory.md` file in the root. This file is the "long-term memory" of the AI.

### Structure of `project_memory.md`:
```markdown
# Project Memory: [Project Name]

## 1. User Preferences (LEARNED)
- **Language:** Arabic (User prefers Arabic for explanations).
- **Code Style:** Strict TypeScript, no `any`.
- **Communication:** Concise, bullet points preferred.

## 2. Architectural Decisions (ADR)
- [Date] Chose Supabase over Firebase because of SQL requirements.
- [Date] Decided to use Nx for monorepo management.

## 3. Technical Context
- **Stack:** React 19, Supabase, Tailwind v4.
- **Key Libraries:** `tanstack/react-query`, `zod`.

## 4. Lessons Learned (The "Don't Repeat" List)
- ❌ **Error:** Direct SQL edits caused schema drift.
- ✅ **Fix:** ALWAYS use `supabase db diff`.

## 5. Active State
- **Current Epic:** User Authentication.
- **Next Step:** Implement "Forgot Password" flow.
```

## 2. The Save Protocol
**When to Save:**
1.  After completing a major task.
2.  After fixing a tricky bug.
3.  Before ending the session.
4.  **When the user expresses a preference.**

**How to Save:**
1.  Read existing `project_memory.md`.
2.  Append new insights (do not delete history).
3.  Commit the file to git.

## 3. The Load Protocol
**At Session Start:**
1.  Read `project_memory.md`.
2.  "I see we are working on [Current Epic]. Last time we learned [Lesson]. Let's continue."
3.  **Adapt style based on User Preferences.**
