# PROMPT 85: META-COGNITION & RETROSPECTIVES (v27.0)

## 1. The Retrospective Protocol (Self-Learning)
**Rule:** After completing any Epic or Major Feature, you MUST perform a "Retrospective" and save it to `.memory/retrospectives/`.

### The Retrospective Template
1.  **What went well?** (e.g., "Supabase migration was seamless.")
2.  **What went wrong?** (e.g., "Forgot to update `.env` for the new API.")
3.  **Root Cause Analysis:** (e.g., "Lack of a pre-flight check script.")
4.  **Action Item:** (e.g., "Add a `pre-commit` hook to check `.env`.")

## 2. The "Don't Repeat Yourself" (DRY) Memory
**Rule:** Before starting a new task, scan previous retrospectives.
*   If you find a similar past error, warn the user: "I recall we had issues with X last time. I will apply fix Y proactively."

## 3. Continuous Improvement
*   Every 5 retrospectives, update the `rules/` directory to codify the lessons learned into permanent laws.
