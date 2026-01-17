# Code Review Prompt

## Purpose
Perform comprehensive code review before merging.

## Instructions
1. Check all files against rules/
2. Verify test coverage >= 80%
3. Run linting and style checks
4. Check for security vulnerabilities
5. Verify documentation completeness
6. Log review results to system_log.md

## Review Checklist
- [ ] All tests pass
- [ ] No linting errors
- [ ] Security scan clean
- [ ] Documentation complete
- [ ] No TODO comments

## Output
- Review report in docs/
- List of required fixes
- Approval/rejection decision
