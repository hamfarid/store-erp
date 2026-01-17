# Specification Files

> **Purpose:** Store all `.spec.md` files for Spec-Driven Development.

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## 📋 Spec-Driven Development

Every new feature MUST have a specification file before implementation.

### Workflow
1. Create `.spec.md` file in this directory
2. Define requirements and acceptance criteria
3. Get Shadow review
4. Implement feature
5. Verify against spec

---

## 📁 Naming Convention

```
XX_feature_name.spec.md

Examples:
- 00_project_initialization.spec.md
- 01_user_authentication.spec.md
- 02_product_management.spec.md
- 03_lot_tracking.spec.md
- 04_pos_system.spec.md
```

---

## 📝 Spec Template

```markdown
# Spec: [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Role:** The Architect
**Status:** [Draft/Approved/Implemented]

## 1. Overview
[Brief description of the feature]

## 2. Requirements

### Functional Requirements
- [ ] FR-001: [Requirement 1]
- [ ] FR-002: [Requirement 2]

### Non-Functional Requirements
- [ ] NFR-001: [Performance requirement]
- [ ] NFR-002: [Security requirement]

## 3. Acceptance Criteria
- [ ] AC-001: [Criteria 1]
- [ ] AC-002: [Criteria 2]

## 4. Technical Design
[High-level technical approach]

## 5. API Endpoints (if applicable)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/... | ... |

## 6. Database Changes (if applicable)
[Tables, columns, migrations needed]

## 7. Testing Requirements
- Unit tests for: [components]
- Integration tests for: [flows]
- E2E tests for: [scenarios]

## 8. Security Considerations
[Any security implications]

## 9. Related Files
- [File 1]
- [File 2]
```

---

## 📊 Spec Status

| Spec | Status | Implemented |
|------|--------|-------------|
| Project Initialization | ✅ Approved | ✅ Yes |
| User Authentication | ✅ Approved | ✅ Yes |
| Product Management | ✅ Approved | ✅ Yes |
| Lot Tracking | ✅ Approved | ✅ Yes |
| POS System | ✅ Approved | 🔄 Partial |
| Reports | 📋 Draft | ❌ No |

---

## 🔗 Related Files

- `.memory/project_constitution.md` - Project mission
- `.memory/project_plan.md` - Current plan
- `global/roles/lead_architect.md` - Architect role
