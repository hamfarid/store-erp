# Development Workflow

**Version:** 2.0.0  
**Last Updated:** 2026-01-16

---

## Overview

This document describes the standard development workflow for Store ERP.

---

## Git Workflow

### Branch Naming

```
feature/[issue-number]-short-description
bugfix/[issue-number]-short-description
hotfix/[issue-number]-short-description
release/v[version]
```

### Commit Messages

Follow Conventional Commits:

```
feat: add lot expiry report export
fix: resolve POS cart total calculation
docs: update API documentation
style: format product form component
refactor: extract lot service logic
test: add e2e tests for settings
chore: update dependencies
```

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes
3. Run tests locally
4. Create PR with description
5. Request review
6. Address feedback
7. Merge after approval

---

## Development Cycle

### 1. Planning
- Review requirements
- Break into tasks
- Estimate effort
- Assign to sprint

### 2. Development
- Create branch
- Implement feature
- Write tests
- Document changes

### 3. Testing
- Run unit tests
- Run E2E tests
- Manual QA
- Performance check

### 4. Review
- Code review
- Security review
- UX review

### 5. Deployment
- Merge to develop
- Deploy to staging
- Smoke tests
- Deploy to production

---

## Code Standards

### Python (Backend)
- PEP 8 style guide
- Type hints required
- Docstrings for public functions
- 4 spaces indentation

### JavaScript (Frontend)
- ESLint + Prettier
- React best practices
- 2 spaces indentation
- Named exports preferred

### SQL
- Uppercase keywords
- Snake_case for identifiers
- Index frequently queried columns
- Use parameterized queries

---

## Testing Requirements

| Test Type | Coverage | Required |
|-----------|----------|----------|
| Unit Tests | 80%+ | ✅ |
| Integration Tests | Critical paths | ✅ |
| E2E Tests | User flows | ✅ |
| Performance Tests | Benchmarks | ✅ |
| Security Tests | OWASP | ✅ |

---

## Documentation

Every PR should include:
- Updated API docs (if applicable)
- Updated user docs (if applicable)
- Changelog entry
- Migration notes (if breaking)

---

## Release Process

### Semantic Versioning
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes written
- [ ] Tagged in git
- [ ] Deployed to production
