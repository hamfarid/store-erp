# Global Errors Directory

> **Purpose:** Track, categorize, and learn from all errors encountered in the project.

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## Directory Structure

```
errors/
├── README.md                    # This file
├── DONT_MAKE_THESE_ERRORS_AGAIN.md  # Main error log
├── critical/                    # Critical errors (system-breaking)
├── high/                        # High priority errors
├── medium/                      # Medium priority errors
├── low/                         # Low priority errors
└── resolved/                    # Archived resolved errors
```

---

## Error Severity Levels

| Level | Symbol | Description |
|-------|--------|-------------|
| Critical | 🔴 | System-breaking, blocks all work |
| High | 🟠 | Significantly impacts functionality |
| Medium | 🟡 | Affects UX but has workarounds |
| Low | 🟢 | Minor issues, cosmetic |

---

## How to Use

### When Error Occurs
1. Create file in appropriate severity folder
2. Use naming convention: `ERRXXX_short_description.md`
3. Follow the error template
4. Add to `DONT_MAKE_THESE_ERRORS_AGAIN.md`

### When Error is Resolved
1. Update status to ✅ Resolved
2. Document the solution
3. Add prevention steps
4. Move to `resolved/` folder

### Weekly Review
1. Review all open errors
2. Update solutions
3. Identify patterns
4. Archive resolved errors

---

## Error Template

```markdown
# Error ERRXXX: [Short Title]

**Date:** YYYY-MM-DD
**Severity:** [🔴/🟠/🟡/🟢]
**Category:** [Database/API/Frontend/Backend/Security]
**Status:** [🔴 Open / 🟡 In Progress / ✅ Resolved]

## Error Message
[Exact error message]

## Context
- What were you doing?
- What was expected?
- What actually happened?

## Root Cause
[Why did this happen?]

## Solution
[How was it fixed?]

## Prevention
- [ ] Prevention step 1
- [ ] Prevention step 2

## Metadata
- Files Affected: file1.py, file2.py
- Time to Fix: X hours
- Resolved By: [Name]
- Resolved Date: YYYY-MM-DD
```

---

## Related Files

- `docs/Errors_Log.md` - Project-specific error log
- `.memory/knowledge/lessons_learned/` - Lessons from errors

---

**Remember:** Every error is a learning opportunity!
