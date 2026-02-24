# CLAUDE.md — Claude Code Entry Point (v26.0)

> **Primary Directive**: See `@AGENTS.md` for full governance framework
> **Note**: The primary directive is `AGENTS.md`. This file exists for Claude Code compatibility and provides quick-start context for any AI agent entering the project.

## Core Directives

1.  **Context First**: Always read `memory-bank/activeContext.md` and `memory-bank/systemContext.md` before acting on any task. Never ask the user for information already available in project files.
2.  **No Hallucinations**: Verify every import, file path, and API call against the actual codebase. Use `speckit analyze` to load context automatically.
3.  **Tool Usage**: Prefer MCP tools for research, database operations, and testing. Hallucinating URLs or API responses is strictly forbidden.
4.  **Version Compliance**: This project uses Global System Ultimate v26.0 (Diamond 30). All agents must follow governance rules in `rules/` and `rules/ml/`.

## Quick Start for New AI Agents

1.  Read `AGENTS.md` — the complete AI agent constitution.
2.  Read `BOOTSTRAP.md` — the bootstrap and initialization guide.
3.  Read `rules/00-iron-rules.md` — the non-negotiable rules that override everything.
4.  Run `speckit analyze` — loads project context into your working memory.
5.  Check `memory-bank/activeContext.md` — what was happening before you arrived.

## Key File Locations

-   **Governance**: `AGENTS.md`, `BOOTSTRAP.md`, `VERSION`
-   **Rules**: `rules/` (general), `rules/ml/` (ML-specific)
-   **Roles**: `roles/` (general), `roles/ml/` (ML-specific)
-   **Errors**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` (master), `errors/ml/` (ML catalogs)
-   **Context**: `memory-bank/` (project state, decisions, patterns)
-   **Workflows**: `workflows/` (general), `workflows/ml/` (ML pipelines)
-   **Knowledge**: `knowledge/` (guides, protocols, references)

## Agent Role Assignment

The standard 4-agent workflow is: Architect (01) → Developer (02) → Reviewer (03) → QA (04). See `roles/` for full role definitions. For ML tasks, additional specialized roles are in `roles/ml/`.

## Emergency Commands

-   `/compact` — Compress context window when running low on space.
-   `/refresh` — Reload all context from `memory-bank/`.
-   `/checkpoint` — Save current state to `memory-bank/activeContext.md`.
