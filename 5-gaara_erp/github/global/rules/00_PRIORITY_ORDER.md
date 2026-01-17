# RULES PRIORITY ORDER

**FILE**: github/global/rules/00_PRIORITY_ORDER.md | **PURPOSE**: Priority order for all rules | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Critical Priority (P0) - Zero Tolerance

These rules are **non-negotiable**. Violation results in immediate failure.

### 1. Security Rules (security_rules.md)
- ❌ No hardcoded secrets
- ❌ No SQL injection vulnerabilities
- ❌ No XSS vulnerabilities
- ❌ No unvalidated inputs
- ❌ No unhandled errors

### 2. Code Safety Rules (code_safety.md)
- ❌ No direct database queries without parameterization
- ❌ No eval() or exec() usage
- ❌ No shell command injection
- ❌ No path traversal vulnerabilities

### 3. Data Integrity Rules (data_integrity.md)
- ❌ No data loss operations without confirmation
- ❌ No destructive operations without backups
- ❌ No schema changes without migrations

## High Priority (P1) - Must Follow

These rules must be followed for production-ready code.

### 4. Testing Rules (testing_rules.md)
- Minimum 80% test coverage
- All critical paths tested
- All tests passing
- No skipped tests without justification

### 5. Documentation Rules (documentation_rules.md)
- All functions documented
- All classes documented
- All modules documented
- All APIs documented

### 6. Code Quality Rules (code_quality.md)
- Linting errors: 0
- Type coverage: 100%
- Cyclomatic complexity: <10
- Code duplication: <5%

## Medium Priority (P2) - Should Follow

These rules improve code quality and maintainability.

### 7. Naming Conventions (naming_conventions.md)
- Consistent naming across codebase
- Descriptive variable names
- Proper function naming
- Clear class names

### 8. File Organization (file_organization.md)
- Proper folder structure
- Logical file grouping
- Clear module boundaries
- Consistent file naming

### 9. Performance Rules (performance_rules.md)
- No N+1 queries
- Proper indexing
- Efficient algorithms
- Resource cleanup

## Low Priority (P3) - Nice to Have

These rules are optional but recommended.

### 10. Style Guide (style_guide.md)
- Consistent code formatting
- Proper indentation
- Line length limits
- Comment style

## Rule Enforcement

### Automated Enforcement
- Linting tools (flake8, eslint)
- Type checkers (mypy, TypeScript)
- Security scanners (bandit, npm audit)
- Test runners (pytest, vitest)

### Manual Enforcement
- Code reviews
- Security reviews
- Architecture reviews

## Violation Handling

### P0 Violations
1. **Stop immediately**
2. Log the violation
3. Fix the issue
4. Re-run checks
5. Document in `errors/critical/`

### P1 Violations
1. Log the violation
2. Create a task to fix
3. Fix before merging
4. Document in `errors/high/`

### P2 Violations
1. Log the violation
2. Create a task to fix
3. Fix in this PR or next
4. Document in `errors/medium/`

### P3 Violations
1. Log the violation
2. Create a task (optional)
3. Fix when convenient
4. Document in `errors/low/`

## Rule Updates

Rules can be updated, but:
- P0 rules require unanimous approval
- P1 rules require majority approval
- P2 and P3 rules can be updated freely

All rule changes must be:
- Documented in CHANGELOG.md
- Announced to the team
- Reflected in CI/CD pipelines

## Cross-References

- **Prompts**: See `prompts/00_PRIORITY_ORDER.md`
- **Docs**: See `docs/00_PRIORITY_ORDER.md`
- **Examples**: See `examples/` for rule compliance examples

---

**Remember**: Rules exist to ensure quality, security, and maintainability. Follow them strictly.

