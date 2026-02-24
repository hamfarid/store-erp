# Knowledge Solutions Registry (v26.0)
# Scope: Reusable Solutions for Recurring Problems
# Audience: All Agents

## Purpose
This directory stores proven solutions to problems encountered during development and deployment. When an agent encounters a problem, they should search here FIRST before attempting a new solution. Every solution must be verified, documented, and linked to its originating error or incident.

## Solution Entry Format
Each solution file in this directory should follow this structure: Problem Description (what went wrong), Root Cause (why it happened), Solution (step-by-step fix), Verification (how to confirm the fix worked), Prevention (how to avoid recurrence), and Related Errors (link to error catalog entries).

## How to Add a New Solution
When a novel problem is solved, the responsible agent creates a new file named `{date}_{short_description}.md` in this directory. The solution must be reviewed by the Reviewer Agent before being considered authoritative. Solutions that address errors in the ML pipeline should also update `errors/ml/` catalogs.

## Naming Convention
Files follow the pattern: `YYYY-MM-DD_problem_short_name.md`. Example: `2026-02-15_gpu_oom_multi_crop.md`.

## Cross-References
Solutions should reference: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` for error codes, `memory-bank/knowledge/lessons_learned/` for broader lessons, and `memory-bank/knowledge/best_practices/` for patterns that emerged from solutions.
