# Anti-Hallucination Protocol (Iron Rule)

## 1. The Golden Rule
**NEVER invent information.** If you don't know, say "I don't know" or "I need to verify."

## 2. Verification Steps
Before stating a fact or writing code:
1. **Check Context:** Read `activeContext.md` and `projectBrief.md`.
2. **Check Codebase:** Use `grep` or `ls` to verify file existence and content.
3. **Check Documentation:** Refer to official docs or `knowledge/` folder.

## 3. Code Generation
- Do not import libraries that are not in `requirements.txt` or `package.json`.
- Do not call functions that do not exist in the codebase.
- Do not assume file paths; verify them first.

## 4. Self-Correction
If you realize you made a mistake:
1. Stop immediately.
2. Acknowledge the error.
3. Correct it using the `errors/` log to prevent recurrence.
