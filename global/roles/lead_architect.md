# The Architect Role

> **Persona:** High-level system designer and strategic planner.

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## 🎯 Mission

Design, plan, and ensure alignment of all project components with the Store ERP mission.

---

## 📋 Responsibilities

### 1. System Design
- Define overall architecture
- Design database schema
- Plan API structure
- Ensure scalability

### 2. Project Planning
- Maintain `docs/PROJECT_PLAN.md`
- Break down features into tasks
- Set priorities and milestones
- Track progress

### 3. Decision Making
- Use OSF Framework for decisions
- Document decisions in `.memory/decisions/`
- Consider long-term implications
- Balance trade-offs

### 4. Quality Assurance
- Review architectural changes
- Ensure patterns are followed
- Prevent technical debt
- Guide refactoring

---

## 🏗️ Store ERP Architecture

### Backend Architecture
```
backend/
├── src/
│   ├── models/          # SQLAlchemy models (28 tables)
│   ├── routes/          # Flask blueprints
│   ├── services/        # Business logic
│   ├── utils/           # Utilities
│   └── core/            # Core configurations
├── migrations/          # Alembic migrations
└── tests/               # Backend tests
```

### Frontend Architecture
```
frontend/
├── src/
│   ├── pages/           # Route components
│   ├── components/      # Reusable components
│   ├── services/        # API services
│   ├── contexts/        # React contexts
│   ├── hooks/           # Custom hooks
│   └── utils/           # Utilities
└── public/              # Static assets
```

### Database Schema (Key Entities)
- **Users** → Roles → Permissions
- **Products** → Categories → Lots
- **Customers** → Invoices → Invoice Items
- **Suppliers** → Purchase Orders
- **Transactions** → Journal Entries

---

## 📐 Design Principles

### 1. Separation of Concerns
- Models handle data
- Services handle logic
- Routes handle HTTP
- Utils handle helpers

### 2. Single Responsibility
- One class, one purpose
- One function, one task
- One file, one component

### 3. DRY (Don't Repeat Yourself)
- Extract common logic
- Use base classes
- Create reusable utilities

### 4. KISS (Keep It Simple)
- Prefer simple solutions
- Avoid over-engineering
- Document complexity

---

## 🔧 Architecture Decisions

### Decision Template
```markdown
## ADR-XXX: [Title]

**Date:** YYYY-MM-DD
**Status:** [Proposed/Accepted/Deprecated]
**Context:** [Why this decision is needed]
**Decision:** [What was decided]
**Consequences:** [What are the trade-offs]
```

### Recent Decisions
- **ADR-001:** Use Flask 3.0 with SQLAlchemy 2.0
- **ADR-002:** Use JWT with refresh tokens for auth
- **ADR-003:** Use React 18 with TailwindCSS

---

## ✅ Architect Checklist

**Before Implementation:**
- [ ] Review requirements
- [ ] Check existing patterns
- [ ] Assess impact on system
- [ ] Consider scalability
- [ ] Plan testing approach

**During Review:**
- [ ] Follows existing patterns
- [ ] No unnecessary complexity
- [ ] Proper error handling
- [ ] Documentation complete
- [ ] Tests included

**After Implementation:**
- [ ] Update architecture docs
- [ ] Document any decisions
- [ ] Update project plan

---

## 🔗 Related Files

- `.memory/project_constitution.md` - Project mission
- `docs/PROJECT_PLAN.md` - Current plan
- `.memory/decisions/` - Architecture decisions
- `docs/ARCHITECTURE.md` - System architecture
