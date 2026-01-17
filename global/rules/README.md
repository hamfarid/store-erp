# Global Rules

**Based on:** Global Professional Core Prompt v33.2

---

## 📜 Rule Index

| ID | Name | Priority | Description |
|----|------|----------|-------------|
| 01 | Code Style | High | Formatting and style standards |
| 02 | Naming Conventions | High | Variable, function, file naming |
| 03 | Commit Messages | Medium | Git commit format |
| 14 | No Duplicate Files | Critical | Zero tolerance for duplicates |
| 99 | Context First | Critical | Read before write |
| 100 | Evolution Engine | Meta | Self-improvement rules |

---

## 🔴 Critical Rules (Non-Negotiable)

### 99 - Context First
**Always** read and understand context before writing code.
- Read existing documentation
- Check file registry
- Understand requirements
- Plan approach

### 14 - No Duplicate Files
**Zero Tolerance** for duplicate files.
- Check before creating
- Merge safe duplicates
- Document in DEDUPLICATION_LOG.md

---

## 🟠 High Priority Rules

### 01 - Code Style
- 2 spaces for JS/TS indentation
- 4 spaces for Python indentation
- Single quotes for strings
- Always use semicolons (JS)

### 02 - Naming Conventions
- camelCase for JS/TS variables
- snake_case for Python variables
- PascalCase for classes
- UPPER_SNAKE_CASE for constants

---

## 🟡 Medium Priority Rules

### 03 - Commit Messages
Follow Conventional Commits:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

---

## 🔵 Meta Rules

### 100 - Evolution Engine
The system learns and improves:
1. Record errors and solutions
2. Create rules from patterns
3. Update rules based on outcomes
4. Prevent repeated mistakes

---

## 📁 Rule Files

```
global/rules/
├── README.md                   # This file
├── 01_code_style.md           # Code formatting
├── 02_naming_conventions.md   # Naming standards
├── 03_commit_message_rules.md # Git commits
├── 14_no_duplicate_files.md   # Deduplication
├── 99_context_first.md        # Context gathering
├── 100_evolution_engine.md    # Self-improvement
├── backend.md                 # Backend rules
├── frontend.md                # Frontend rules
├── database.md                # Database rules
├── security.md                # Security rules
├── testing.md                 # Testing rules
├── mcp.md                     # MCP tools rules
├── memory.md                  # Memory management
└── thinking.md                # Thinking framework
```

---

## ⚠️ Violation Consequences

| Priority | Consequence |
|----------|-------------|
| Critical | Immediate failure state |
| High | Must fix before merge |
| Medium | Should fix in next session |
| Low | Nice to fix |

---

## 🎓 Remember

> **"Rules exist to protect quality, not to restrict creativity."**

Follow the rules. They're here to help.

---

**Last Updated:** 2025-01-16
