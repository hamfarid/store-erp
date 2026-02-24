# Context Engineering Rules (v26.0 — Global System v26 Diamond 32)

> **Status**: MANDATORY
> **Enforcement**: Automated by Speckit (Analyze Phase)
> **Version**: v26.0.2 (Diamond 32)

## 1. The Philosophy

Context is not “nice to have”; it is the prerequisite for intelligence. An AI agent without context is worse than no agent at all — it will confidently produce incorrect results. Every task must begin with context loading, and every session must end with context preservation.

## 2. The Protocol (Context First)

Before writing a single line of code, you MUST:
1.  **Read the Map**: Load `all_files_inventory.txt` or `memory-bank/file_registry.json` to understand the project structure. Know where every file is before searching for anything.
2.  **Read the Rules**: Check the `rules/` directory for any rules applicable to your current task. For ML tasks, also check `rules/ml/`.
3.  **Read the History**: Load `memory-bank/activeContext.md` (current state) and `memory-bank/lessons.md` (past mistakes). Check `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` for known error patterns.
4.  **Read the Roles**: Confirm your role and boundaries from `roles/` directory. Do not perform actions outside your role scope.
5.  **Read the Interfaces**: If your task touches multiple modules, check `docs/MODULE_INTERFACES.md` for interface contracts.

## 3. The “No Amnesia” Rule

**Forbidden**: Asking the user for information that is already available in project files. Before asking any question, search `memory-bank/`, `docs/`, and `rules/` first. If the information exists in the project, use it. Only ask the user when the information genuinely does not exist in any project file.

**Mandatory**: If you are unsure about any fact (file path, API endpoint, configuration value), SEARCH the project files first. Never guess. Never hallucinate file paths, import names, or API URLs.

## 4. Context Injection

**Speckit Integration**: The `speckit analyze` command automatically loads the “Active Context” into your working memory. This includes current task state, recent decisions, applicable rules, and known patterns. Do NOT ignore injected context — it was curated to help you succeed.

**Manual Override**: If `speckit analyze` is unavailable, manually load these files in order: `AGENTS.md` → `memory-bank/activeContext.md` → `rules/00-iron-rules.md` → task-specific rules.

## 5. Context Preservation

At the end of every task or session, you MUST:
1.  **Update `activeContext.md`**: Record what was done, what’s pending, and any decisions made.
2.  **Log Lessons**: If you encountered an unexpected issue, add it to `memory-bank/lessons.md`.
3.  **Update Error Catalog**: If you created a new error pattern, add it to the appropriate error catalog.
4.  **Checkpoint**: Leave the project in a state where the next agent can pick up seamlessly.

## 6. Context Window Management

When working in long sessions, monitor your context window usage. If nearing limits, use `/compact` to summarize and compress earlier conversation. Prioritize retaining: current task context, applicable rules, active file references, and recent decisions. Low-priority for compression: historical discussion, already-completed tasks, and verbose tool output.

## 7. Cross-References

Context loading protocol connects to: `AGENTS.md` (governance), `memory-bank/` (state), `rules/` (standards), `errors/` (known patterns), `docs/MODULE_INTERFACES.md` (boundaries).
