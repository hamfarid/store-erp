# Knowledge Best Practices Registry (v26.0)

> **Scope**: Proven Patterns and Standards
> **Audience**: All Agents
> **Version**: v26.0.2 (Diamond 32)

## Purpose

This directory captures best practices discovered through project experience. Unlike rules (which are mandatory), best practices are recommended patterns that have been proven to improve code quality, reduce bugs, and accelerate development. Agents should consult this directory when making implementation decisions.

## Best Practice Entry Format

Each entry should include:
-   **Context**: When does this apply.
-   **Practice**: What to do.
-   **Rationale**: Why this works.
-   **Example**: Concrete code or workflow example.
-   **Anti-Pattern**: What to avoid and why.

## Categories

Best practices are organized by domain. File naming follows the pattern: `{domain}_{practice_name}.md`.
Domains include:
-   `backend_` for server-side patterns.
-   `frontend_` for client-side patterns.
-   `ml_` for machine learning patterns.
-   `testing_` for testing strategies.
-   `security_` for security practices.
-   `infra_` for infrastructure and DevOps.

## How to Add a New Best Practice

When a pattern proves consistently beneficial across multiple tasks, any agent can propose it as a best practice by creating a file in this directory. The Reviewer Agent validates that the practice is genuinely beneficial and does not conflict with existing rules. Accepted practices may eventually be promoted to mandatory rules in the `rules/` directory if they prove critical enough.

## Relationship to Rules

Best practices complement but do not override the mandatory rules in `rules/` and `rules/ml/`. If a best practice conflicts with a rule, the rule takes precedence. Best practices that become universally adopted should be proposed for promotion to rules via the Governance Agent.

## Cross-References

-   `rules/` for mandatory standards.
-   `memory-bank/knowledge/solutions/` for specific problem fixes.
-   `memory-bank/knowledge/lessons_learned/` for retrospective insights.
