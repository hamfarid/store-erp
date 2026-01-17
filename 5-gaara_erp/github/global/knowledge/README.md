# Knowledge Base

**FILE**: github/global/knowledge/README.md | **PURPOSE**: Knowledge base documentation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

The `knowledge/` directory stores verified facts, code snippets, and solutions from trusted sources.

## Purpose

This is the AI agent's **permanent knowledge base**. Unlike memory (which is session-specific), knowledge is:
- **Permanent**: Never deleted
- **Verified**: Only from trusted sources
- **Reusable**: Can be referenced across projects
- **Append-only**: New knowledge is added, old knowledge is updated but not removed

## Structure

```
knowledge/
├── backend/
│   ├── authentication.md
│   ├── database.md
│   └── api_design.md
├── frontend/
│   ├── react_patterns.md
│   ├── state_management.md
│   └── performance.md
├── security/
│   ├── common_vulnerabilities.md
│   └── best_practices.md
├── testing/
│   ├── unit_testing.md
│   └── e2e_testing.md
└── devops/
    ├── docker.md
    └── ci_cd.md
```

## What to Store

### ✅ Store
- Verified solutions to common problems
- Code snippets from official documentation
- Best practices from authoritative sources
- Patterns that have been tested and work
- Performance optimization techniques
- Security guidelines

### ❌ Don't Store
- Unverified solutions
- Experimental code
- Project-specific code
- Temporary workarounds
- Deprecated patterns

## Format

Each knowledge file should follow this format:

```markdown
# [Topic]

**Source**: [Official docs / Trusted blog / etc.]
**Last Verified**: [Date]

## Problem

[Description of the problem this solves]

## Solution

[Verified solution]

## Example

```[language]
[Working code example]
```

## Notes

[Any important notes or caveats]

## References

- [Link to official docs]
- [Link to source]
```

## Usage

When the AI agent encounters a problem:
1. Search the knowledge base first
2. If found, use the verified solution
3. If not found, research and verify
4. Add the verified solution to the knowledge base

## Maintenance

- Review and update quarterly
- Remove deprecated information
- Add new verified solutions
- Keep examples up-to-date

---

**This directory should never be empty. Populate it with verified knowledge.**

