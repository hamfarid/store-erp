# Knowledge Lessons Learned Registry (v26.0)

> **Scope**: Retrospective Insights from Project Experience
> **Audience**: All Agents
> **Version**: v26.0.2 (Diamond 32)

## Purpose

This directory captures lessons learned from incidents, failed approaches, and successful recoveries. Unlike solutions (which address specific problems) and best practices (which recommend patterns), lessons learned capture the broader insights and strategic takeaways that inform future decision-making.

## Lesson Entry Format

Each entry should include:
-   **Date**: When the lesson was captured.
-   **Context**: What project or task prompted this.
-   **What Happened**: Factual narrative.
-   **What We Learned**: The insight.
-   **Impact**: How this changes our approach going forward.
-   **Action Taken**: Concrete changes made to prevent recurrence.

## Sources of Lessons

Lessons are derived from:
-   Post-mortem analyses (see `templates/ml/TEMPLATE-post-mortem.md`).
-   Sprint retrospectives.
-   Code review findings that revealed systemic issues.
-   Production incidents.
-   Failed experiments that produced valuable negative results.

Every post-mortem should produce at least one lesson learned entry.

## File Naming Convention

Files follow the pattern: `YYYY-MM-DD_lesson_short_name.md`.
Example: `2026-02-10_embedding_version_mismatch.md`.

## How to Add a New Lesson

After any significant incident, failed approach, or retrospective finding, the responsible agent creates a lesson learned entry. The QA Engineer or Governance Agent reviews entries for accuracy and completeness. Lessons that reveal gaps in existing rules should trigger a rule update proposal to the Governance Agent.

## Promotion Path

Lessons learned that identify recurring problems may be promoted to:
-   **Solutions**: If a fix was found.
-   **Best Practices**: If a prevention pattern emerged.
-   **Error Catalog Entries**: If a new error type was identified.
-   **Rule Updates**: If the lesson reveals a governance gap.

## Cross-References

-   `memory-bank/knowledge/solutions/` for specific fixes.
-   `memory-bank/knowledge/best_practices/` for recommended patterns.
-   `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` for error catalog.
-   `templates/ml/TEMPLATE-post-mortem.md` for incident analysis template.
