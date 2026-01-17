# Errors

**FILE**: github/global/errors/README.md | **PURPOSE**: Error tracking documentation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

The `errors/` directory tracks all errors encountered during development, categorized by severity.

## Purpose

This directory serves as:
- **Error Registry**: All errors are logged here
- **Learning System**: Prevents repeating the same mistakes
- **Knowledge Base**: Solutions are documented for future reference
- **Quality Metric**: Track error trends over time

## Structure

```
errors/
├── critical/          # P0 - Zero tolerance violations
├── high/              # P1 - Must fix before merge
├── medium/            # P2 - Should fix soon
├── low/               # P3 - Nice to fix
├── resolved/          # Fixed errors (moved from above)
└── README.md
```

## Error Severity Levels

### Critical (P0)
**Zero-tolerance violations that must be fixed immediately**

Examples:
- Hardcoded secrets
- SQL injection vulnerabilities
- XSS vulnerabilities
- Data loss bugs
- Security breaches

**Action**: Stop all work and fix immediately

### High (P1)
**Serious issues that must be fixed before merge**

Examples:
- Failing tests
- Type errors
- Linting errors
- Missing authentication
- Broken functionality

**Action**: Fix before merging to main

### Medium (P2)
**Issues that should be fixed soon**

Examples:
- Code duplication
- Missing documentation
- Performance issues
- Minor bugs
- Code smells

**Action**: Fix in this PR or create a follow-up task

### Low (P3)
**Nice-to-fix issues**

Examples:
- Style inconsistencies
- Minor refactoring opportunities
- Optional optimizations
- Cosmetic issues

**Action**: Fix when convenient

## Error File Format

Each error should be documented in a file:

**Filename**: `error_YYYY-MM-DD_HHmmss_[brief-description].md`

**Content**:
```markdown
# Error: [Brief Description]

**Date**: 2025-11-18T14:30:00Z
**Severity**: Critical / High / Medium / Low
**Status**: Open / In Progress / Resolved
**Category**: Security / Bug / Performance / Quality

## Description

[Detailed description of the error]

## Location

- **File**: `path/to/file.py`
- **Line**: 45
- **Function**: `function_name`

## Error Message

```
[Exact error message or stack trace]
```

## Root Cause

[Analysis of why this error occurred]

## Impact

[What is affected by this error]

## Solution

[How to fix this error]

## Code Fix

```python
# Before (bad)
[Bad code]

# After (good)
[Fixed code]
```

## Prevention

[How to prevent this error in the future]

## Related

- Similar errors: [Links to related errors]
- Documentation: [Links to relevant docs]
- Rules violated: [Links to rules]

## Timeline

- **Discovered**: 2025-11-18T14:30:00Z
- **Started**: 2025-11-18T14:35:00Z
- **Resolved**: 2025-11-18T15:00:00Z
- **Verified**: 2025-11-18T15:05:00Z

---

**Resolved by**: [Name/Agent]
**Verified by**: [Name/Agent]
```

## Workflow

### 1. Error Discovered

```bash
# Create error file in appropriate severity folder
errors/critical/error_2025-11-18_143000_hardcoded_secret.md
```

### 2. Error Logged

- Document the error using the template
- Add to `docs/fix_this_error.md`
- Log to `logs/error.log`

### 3. Error Fixed

- Implement the solution
- Test the fix
- Update the error file with solution

### 4. Error Resolved

- Move file to `resolved/` folder
- Update `docs/DONT_MAKE_THESE_ERRORS_AGAIN.md`
- Add to knowledge base if applicable

## Integration with Other Systems

### Logs
All errors are also logged to `logs/error.log` in JSON format

### Memory
Critical errors are saved to `.memory/learnings/`

### Knowledge
Resolved errors with reusable solutions are added to `knowledge/`

### Documentation
All errors are tracked in `docs/fix_this_error.md`

## Metrics

Track error metrics:
- Total errors by severity
- Resolution time by severity
- Recurring errors
- Error trends over time

### Example Report

```markdown
# Error Metrics - Week of 2025-11-18

## Summary

- **Total Errors**: 25
- **Critical**: 2 (resolved)
- **High**: 8 (6 resolved, 2 open)
- **Medium**: 10 (5 resolved, 5 open)
- **Low**: 5 (1 resolved, 4 open)

## Average Resolution Time

- **Critical**: 30 minutes
- **High**: 2 hours
- **Medium**: 1 day
- **Low**: 3 days

## Top Error Categories

1. Security: 5 errors
2. Type Errors: 4 errors
3. Missing Tests: 3 errors

## Recurring Errors

- Import errors: 3 occurrences
- Missing validation: 2 occurrences

## Actions

- Add import path checking to CI
- Create validation template
```

## Best Practices

1. **Document immediately**: Don't wait to document errors
2. **Be specific**: Include exact error messages and stack traces
3. **Analyze root cause**: Don't just fix symptoms
4. **Prevent recurrence**: Update rules, tests, or CI to prevent
5. **Share knowledge**: Add solutions to knowledge base
6. **Track metrics**: Monitor error trends

## Automation

### Auto-create error files

```python
def log_error(severity, description, file, line, error_message):
    """Automatically create error file"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"errors/{severity}/error_{timestamp}_{description}.md"
    
    # Create file with template
    # ...
```

### Auto-move resolved errors

```python
def resolve_error(error_file):
    """Move error to resolved folder"""
    shutil.move(error_file, f"errors/resolved/{os.path.basename(error_file)}")
```

---

**This directory is critical for learning and improvement. Never delete error files.**

