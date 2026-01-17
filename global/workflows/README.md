# Global Workflows

> **Purpose:** Define standard workflows for common development tasks.

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## 📁 Available Workflows

### Development Workflows
| Workflow | Description |
|----------|-------------|
| `feature_development.md` | Adding new features |
| `bug_fix.md` | Fixing bugs |
| `refactoring.md` | Code refactoring |

### Release Workflows
| Workflow | Description |
|----------|-------------|
| `release_workflow.md` | Release process |
| `deployment.md` | Deployment steps |
| `rollback.md` | Rollback procedures |

### Review Workflows
| Workflow | Description |
|----------|-------------|
| `code_review.md` | Code review process |
| `security_audit.md` | Security review |

---

## 🔄 Standard Feature Workflow

```
1. Spec Creation
   └─> Create .spec.md file
   
2. Planning
   └─> Break into tasks
   └─> Add to TODO.md
   
3. Implementation
   └─> Write tests first
   └─> Implement feature
   └─> Document changes
   
4. Review
   └─> Self-review
   └─> Shadow review
   └─> Code review
   
5. Testing
   └─> Unit tests pass
   └─> Integration tests pass
   └─> Coverage check
   
6. Deployment
   └─> Merge to main
   └─> Deploy to staging
   └─> Verify
   └─> Deploy to production
```

---

## 📋 Workflow Selection

| Task Type | Workflow |
|-----------|----------|
| New Feature | `feature_development.md` |
| Bug Fix | `bug_fix.md` |
| Security Issue | `security_audit.md` |
| Performance | `optimization.md` |
| Release | `release_workflow.md` |

---

## 🔗 Related Files

- `global/roles/` - Role definitions
- `docs/TODO.md` - Task tracking
- `specs/` - Specification files
