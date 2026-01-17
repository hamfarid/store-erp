# 99 - Context First

**Rule ID:** 99_context_first
**Priority:** CRITICAL
**Scope:** All development work

---

## 🎯 Purpose

This rule ensures that **context is gathered and understood BEFORE any code is written**. 
Context-first development prevents wasted effort, misunderstandings, and incorrect implementations.

---

## 📜 The Law

> **"No code without context. No implementation without understanding."**

Before writing ANY code, you MUST:

1. **READ** all relevant documentation
2. **UNDERSTAND** the requirements fully
3. **VERIFY** your understanding
4. **PLAN** your approach
5. **THEN** implement

---

## ✅ Context Checklist

Before starting ANY task, verify you have:

### 1. Project Context
- [ ] Read `docs/ARCHITECTURE.md`
- [ ] Read `docs/TODO.md` for current status
- [ ] Read `.memory/context/current_task.md`
- [ ] Checked `.memory/file_registry.json` for existing files

### 2. Task Context
- [ ] Understood what the user is asking
- [ ] Identified the specific requirements
- [ ] Determined success criteria
- [ ] Identified dependencies

### 3. Code Context
- [ ] Read existing code in the area you're modifying
- [ ] Understood the coding conventions
- [ ] Identified related files and functions
- [ ] Checked for existing implementations

### 4. Technical Context
- [ ] Understood the technology stack
- [ ] Identified API contracts
- [ ] Checked database schema
- [ ] Verified integration points

---

## 🚫 Anti-Patterns

### DON'T:
- ❌ Start coding immediately
- ❌ Assume you know what the user wants
- ❌ Skip reading existing code
- ❌ Ignore documentation
- ❌ Make assumptions about file paths
- ❌ Hallucinate imports or APIs

### DO:
- ✅ Ask clarifying questions
- ✅ Read before writing
- ✅ Verify before assuming
- ✅ Plan before implementing
- ✅ Check file registry before creating files

---

## 📋 Context-First Workflow

```
1. RECEIVE TASK
      ↓
2. READ RELEVANT DOCS
      ↓
3. SCAN EXISTING CODE
      ↓
4. VERIFY UNDERSTANDING
      ↓
5. CREATE PLAN
      ↓
6. VALIDATE PLAN
      ↓
7. IMPLEMENT
      ↓
8. VERIFY IMPLEMENTATION
```

---

## 🔍 Context Sources

### Primary Sources (Must Read)
1. `docs/TODO.md` - Current task status
2. `docs/ARCHITECTURE.md` - System design
3. `.memory/file_registry.json` - File index
4. `.memory/context/current_task.md` - Current context

### Secondary Sources (Read as Needed)
1. `docs/API_DOCUMENTATION.md` - API reference
2. `docs/DATABASE_SCHEMA.md` - Data model
3. `backend/src/` - Backend code
4. `frontend/src/` - Frontend code

### Historical Sources (For Understanding)
1. `docs/COMPLETE_TASKS.md` - What's been done
2. `.memory/decisions/` - Past decisions
3. `CHANGELOG.md` - Version history

---

## 💡 Examples

### Good Context-First Approach

```
User: "Add a new endpoint for product search"

AI Response:
1. Let me check the existing API structure...
2. Reading backend/src/routes/ to understand the pattern...
3. Checking docs/API_DOCUMENTATION.md for conventions...
4. Found that we use /api/products/ prefix
5. Existing search pattern in customers endpoint: GET /api/customers/search
6. Plan: Create GET /api/products/search with similar pattern
7. Implementation: [code with proper context]
```

### Bad Approach (No Context)

```
User: "Add a new endpoint for product search"

AI Response:
Here's the code: [generates code without checking existing patterns]
```

---

## ⚠️ Violation Consequences

Skipping context-first steps leads to:

1. **Duplicate code** - Because you didn't check what exists
2. **Inconsistent patterns** - Because you didn't read conventions
3. **Broken integrations** - Because you didn't verify APIs
4. **Wasted time** - Because you have to redo work
5. **User frustration** - Because the solution doesn't fit

---

## 📝 Implementation Note

This rule is automatically enforced by:

1. The Librarian Protocol (`global/tools/librarian.py`)
2. The Lifecycle Maestro (`global/tools/lifecycle.py`)
3. The Verification Oath (sworn before every import)

---

## 🎓 Remember

> **"A minute of context saves an hour of debugging."**

Context is not overhead. Context is the foundation of good code.

---

**Last Updated:** 2025-01-16
**Version:** 1.0.0
