# Knowledge Lessons Learned Registry (v26.0)
# Scope: Retrospective Insights from Project Experience
# Audience: All Agents

## Purpose
This directory captures lessons learned from incidents, failed approaches, and successful recoveries. Unlike solutions (which address specific problems) and best practices (which recommend patterns), lessons learned capture the broader insights and strategic takeaways that inform future decision-making.

## Lesson Entry Format
Each entry should include: Date (when the lesson was captured), Context (what project or task prompted this), What Happened (factual narrative), What We Learned (the insight), Impact (how this changes our approach going forward), and Action Taken (concrete changes made to prevent recurrence).

## Sources of Lessons
Lessons are derived from: post-mortem analyses (see `templates/ml/TEMPLATE-post-mortem.md`), sprint retrospectives, code review findings that revealed systemic issues, production incidents, and failed experiments that produced valuable negative results. Every post-mortem should produce at least one lesson learned entry.

## File Naming Convention
Files follow the pattern: `YYYY-MM-DD_lesson_short_name.md`. Example: `2026-02-10_embedding_version_mismatch.md`.

## How to Add a New Lesson
After any significant incident, failed approach, or retrospective finding, the responsible agent creates a lesson learned entry. The QA Engineer or Governance Agent reviews entries for accuracy and completeness. Lessons that reveal gaps in existing rules should trigger a rule update proposal to the Governance Agent.

## Promotion Path
Lessons learned that identify recurring problems may be promoted to: solutions (if a fix was found), best practices (if a prevention pattern emerged), error catalog entries (if a new error type was identified), or rule updates (if the lesson reveals a governance gap).

## Cross-References
Related directories: `memory-bank/knowledge/solutions/` for specific fixes, `memory-bank/knowledge/best_practices/` for recommended patterns, `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` for error catalog, and `templates/ml/TEMPLATE-post-mortem.md` for incident analysis template.
