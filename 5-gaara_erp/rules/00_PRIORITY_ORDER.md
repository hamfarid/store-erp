# RULES PRIORITY ORDER

**Enforce rules in this exact order. Higher priority = more critical.**

---

## 🔴 LEVEL 1: CRITICAL (Non-Negotiable - Zero Tolerance)

**These rules MUST NEVER be violated under any circumstances.**

### System Integrity
1. `memory.md` - **MANDATORY** Memory usage (save context, load context)
2. `mcp.md` - **MANDATORY** MCP tools usage
3. `thinking.md` - **MANDATORY** Thinking framework
4. `context_engineering.md` - **MANDATORY** Context management
5. **TODO System** - **MANDATORY** Maintain TODO.md, COMPLETE_TASKS.md, INCOMPLETE_TASKS.md

### Code Quality
6. `14_no_duplicate_files.md` - **ZERO TOLERANCE** No duplicate files
7. `01_code_style.md` - Code style standards
8. `02_naming_conventions.md` - Naming conventions
9. `error_handling.md` - Error handling standards

---

## 🟠 LEVEL 2: HIGH PRIORITY (Quality & Safety)

**These ensure quality and safety. Violations cause serious issues.**

### Development Standards
10. `frontend.md` - Frontend development rules
11. `backend.md` - Backend development rules
12. `database.md` - Database rules

### Version Control
13. `03_commit_message_rules.md` - Git commit message format

---

## 🟡 LEVEL 3: MEDIUM PRIORITY (Best Practices)

**These are best practices. Follow them for maintainability.**

### Security
14. `security.md` - Security best practices

### Testing
15. `testing.md` - Testing standards
16. **RORLOC Testing** ⭐ **MANDATORY in Phase 4**
    - Must use RORLOC methodology (6 phases)
    - Must achieve 100% system verification
    - Cannot proceed to Phase 5 without passing all tests

---

## 📋 RULES BY CATEGORY

### Memory & Context Rules

**File:** `memory.md`

**MANDATORY Requirements:**
- ✅ Save context to `.memory/context/` at the end of each phase
- ✅ Load context from `.memory/context/` at the start of each task
- ✅ Save decisions to `.memory/decisions/`
- ✅ Save learnings to `.memory/learnings/`
- ✅ Create checkpoints in `.memory/checkpoints/`

**Violations:**
- ❌ Starting a task without loading context
- ❌ Completing a phase without saving context
- ❌ Making decisions without documenting them

---

### MCP Rules

**File:** `mcp.md`

**MANDATORY Requirements:**
- ✅ Check available MCP tools at task start
- ✅ Use MCP tools when available
- ✅ Document MCP tool usage
- ✅ Handle MCP errors gracefully

**Violations:**
- ❌ Not checking for MCP tools
- ❌ Ignoring available MCP tools
- ❌ Not handling MCP errors

---

### Thinking Rules

**File:** `thinking.md`

**MANDATORY Requirements:**
- ✅ Think before acting
- ✅ Break down complex problems
- ✅ Consider multiple approaches
- ✅ Validate assumptions
- ✅ Document reasoning

**Violations:**
- ❌ Acting without thinking
- ❌ Not considering alternatives
- ❌ Making assumptions without validation

---

### Context Engineering Rules

**File:** `context_engineering.md`

**MANDATORY Requirements:**
- ✅ Maintain context awareness
- ✅ Reference previous work
- ✅ Build on existing code
- ✅ Avoid context loss

**Violations:**
- ❌ Ignoring existing context
- ❌ Recreating existing solutions
- ❌ Losing track of project state

---

### No Duplicate Files Rule

**File:** `14_no_duplicate_files.md`

**ZERO TOLERANCE - This is CRITICAL**

**MANDATORY Requirements:**
- ✅ Run duplicate detection before Phase 3 completion
- ✅ Run duplicate detection after adding new files
- ✅ Run duplicate detection before final delivery
- ✅ Merge safe duplicates (>95% similarity)
- ✅ Review risky duplicates (70-95% similarity)
- ✅ Document all merges in `docs/DEDUPLICATION_LOG.md`

**Commands:**
```bash
# Detect duplicates
python .global/tools/duplicate_files_detector.py /path/to/project

# Analyze code similarity
python .global/tools/code_deduplicator.py /path/to/project --threshold 0.85

# Auto-merge safe duplicates
python .global/tools/code_deduplicator.py /path/to/project --auto-merge --threshold 0.95
```

**Safe to Merge:**
- ✅ Exact duplicates (100% identical)
- ✅ Backup files (file.bak, file_backup.js)
- ✅ Copy files (file_copy.js, file (1).js)

**NEVER Merge:**
- ❌ Configuration files (.env, config.js)
- ❌ Test files (even if similar)
- ❌ Migration files
- ❌ Controllers for different entities
- ❌ Models for different entities

**Violations:**
- ❌ Completing Phase 3 without running duplicate detection
- ❌ Leaving duplicate files in the project
- ❌ Not documenting merges
- ❌ Merging files that should stay separate

---

### Code Style Rules

**File:** `01_code_style.md`

**Requirements:**
- ✅ Consistent indentation (2 or 4 spaces)
- ✅ Semicolons (JavaScript/TypeScript)
- ✅ Single quotes for strings (JavaScript/TypeScript)
- ✅ PEP 8 compliance (Python)
- ✅ Max line length: 100 characters
- ✅ No trailing whitespace
- ✅ End files with newline

**Violations:**
- ❌ Inconsistent indentation
- ❌ Mixed quotes
- ❌ Lines over 100 characters
- ❌ Trailing whitespace

---

### Naming Conventions Rules

**File:** `02_naming_conventions.md`

**Requirements:**

**Files:**
- ✅ `camelCase.js` for JavaScript/TypeScript
- ✅ `snake_case.py` for Python
- ✅ `PascalCase.jsx` for React components
- ✅ `kebab-case.css` for CSS files

**Variables:**
- ✅ `camelCase` for variables and functions
- ✅ `PascalCase` for classes and components
- ✅ `UPPER_SNAKE_CASE` for constants
- ✅ `_privateVariable` for private members

**Database:**
- ✅ `snake_case` for table names
- ✅ `snake_case` for column names
- ✅ Plural for table names (`users`, `products`)

**Violations:**
- ❌ Inconsistent naming
- ❌ Unclear abbreviations
- ❌ Single letter variables (except loops)

---

### Commit Message Rules

**File:** `03_commit_message_rules.md`

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

**Requirements:**
- ✅ Subject in present tense
- ✅ Subject max 50 characters
- ✅ Body wraps at 72 characters
- ✅ Explain what and why, not how

**Example:**
```
feat: add user authentication

Implement JWT-based authentication system with
refresh tokens and role-based access control.

Closes #123
```

**Violations:**
- ❌ Vague messages ("fix bug", "update")
- ❌ Subject over 50 characters
- ❌ Past tense ("added", "fixed")

---

### Error Handling Rules

**File:** `error_handling.md`

**Requirements:**
- ✅ Try-catch blocks for all async operations
- ✅ Specific error messages
- ✅ Log errors with context
- ✅ Return meaningful error responses
- ✅ Don't expose sensitive information
- ✅ Use error codes

**Example:**
```javascript
try {
  const user = await User.findById(id);
  if (!user) {
    throw new NotFoundError('User not found', { userId: id });
  }
  return user;
} catch (error) {
  logger.error('Failed to fetch user', { userId: id, error });
  throw error;
}
```

**Violations:**
- ❌ Silent failures
- ❌ Generic error messages
- ❌ Exposing stack traces to users
- ❌ Not logging errors

---

### Frontend Rules

**File:** `frontend.md`

**Requirements:**
- ✅ Component-based architecture
- ✅ Separate concerns (UI, logic, state)
- ✅ Reusable components
- ✅ Proper state management
- ✅ Accessibility (ARIA labels, semantic HTML)
- ✅ Responsive design
- ✅ Performance optimization (lazy loading, code splitting)

**Violations:**
- ❌ Monolithic components
- ❌ Inline styles (use CSS modules)
- ❌ Missing accessibility features
- ❌ Not responsive

---

### Backend Rules

**File:** `backend.md`

**Requirements:**
- ✅ MVC or similar architecture
- ✅ Separate routes, controllers, services, models
- ✅ Input validation on all endpoints
- ✅ Authentication & authorization
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Environment variables for config
- ✅ Proper error handling middleware

**Violations:**
- ❌ Business logic in routes
- ❌ No input validation
- ❌ Hardcoded credentials
- ❌ Missing authentication

---

### Database Rules

**File:** `database.md`

**Requirements:**
- ✅ Migrations for schema changes
- ✅ Indexes on frequently queried columns
- ✅ Foreign key constraints
- ✅ Soft deletes (deleted_at column)
- ✅ Timestamps (created_at, updated_at)
- ✅ Connection pooling
- ✅ Prepared statements (prevent SQL injection)

**Violations:**
- ❌ Direct schema changes
- ❌ Missing indexes
- ❌ No foreign keys
- ❌ Hard deletes
- ❌ SQL injection vulnerabilities

---

### Security Rules

**File:** `security.md`

**Requirements:**
- ✅ HTTPS only
- ✅ JWT or session-based authentication
- ✅ Password hashing (bcrypt, argon2)
- ✅ Input validation & sanitization
- ✅ CSRF protection
- ✅ XSS prevention
- ✅ SQL injection prevention
- ✅ Rate limiting
- ✅ Audit logging

**Violations:**
- ❌ Plain text passwords
- ❌ No input validation
- ❌ Missing CSRF tokens
- ❌ Exposed sensitive data

---

### Testing Rules

**File:** `testing.md`

**Requirements:**
- ✅ Unit tests for all business logic
- ✅ Integration tests for API endpoints
- ✅ E2E tests for critical flows
- ✅ Test coverage > 80%
- ✅ Tests run in CI/CD
- ✅ Mock external dependencies

**Violations:**
- ❌ No tests
- ❌ Low coverage (<80%)
- ❌ Tests not in CI/CD
- ❌ Flaky tests

---

## 🎯 ENFORCEMENT CHECKLIST

### Before Starting (Phase 1)
- [ ] Read all LEVEL 1 rules (1-8)
- [ ] Set up memory system
- [ ] Check MCP tools
- [ ] Review thinking framework

### During Development (Phase 3)
- [ ] Follow code style rules
- [ ] Follow naming conventions
- [ ] Run duplicate detection
- [ ] Handle errors properly

### Before Committing
- [ ] Check for duplicates
- [ ] Follow commit message rules
- [ ] Run tests
- [ ] Review code style

### Before Deployment
- [ ] All security rules followed
- [ ] All testing rules followed
- [ ] No duplicate files
- [ ] Documentation complete

---

## ⚠️ VIOLATION CONSEQUENCES

### LEVEL 1 Violations (Critical)
- 🚨 **STOP IMMEDIATELY**
- 🚨 **FIX BEFORE PROCEEDING**
- 🚨 **CANNOT MARK PHASE COMPLETE**

### LEVEL 2 Violations (High)
- ⚠️ **FIX BEFORE NEXT PHASE**
- ⚠️ **DOCUMENT REASON IF UNAVOIDABLE**

### LEVEL 3 Violations (Medium)
- ⚡ **FIX WHEN POSSIBLE**
- ⚡ **ADD TO TECHNICAL DEBT**

---

## 📊 RULES SUMMARY

| Level | Rules | Enforcement | Violations |
|-------|-------|-------------|------------|
| LEVEL 1 | 1-9 | Zero Tolerance | Stop immediately |
| LEVEL 2 | 10-13 | High Priority | Fix before next phase |
| LEVEL 3 | 14-15 | Best Practice | Fix when possible |

**Total Rules:** 15  
**Critical Rules:** 9 (including TODO System)  
**High Priority Rules:** 4  
**Best Practice Rules:** 2

---

**Last Updated:** 2025-11-15  
**Enforcement:** Mandatory  
**Compliance:** Required for all phases




---

### TODO System Rules

**File:** TODO System (Integrated in GLOBAL_PROFESSIONAL_CORE_PROMPT.md)

**MANDATORY Requirements:**
- ✅ Create `docs/TODO.md` in Phase 1
- ✅ Create `docs/INCOMPLETE_TASKS.md` in Phase 1
- ✅ Create `docs/COMPLETE_TASKS.md` in Phase 1
- ✅ NEVER delete from TODO.md (only mark with [x])
- ✅ Update all three files after completing each task
- ✅ Move tasks between INCOMPLETE and COMPLETE
- ✅ Add timestamps to completed tasks

**File Structure:**

**TODO.md:**
```markdown
# TODO List
## Phase 1
- [x] Completed task
- [ ] Incomplete task
```

**COMPLETE_TASKS.md:**
```markdown
# Completed Tasks
## 2025-11-15
- [x] Task name - Completed at 14:30
```

**INCOMPLETE_TASKS.md:**
```markdown
# Incomplete Tasks
## 🔴 Critical Priority
- [ ] Task 1
## 🟠 High Priority
- [ ] Task 2
```

**Violations:**
- ❌ Not creating TODO files in Phase 1
- ❌ Deleting tasks from TODO.md
- ❌ Not updating files after completing tasks
- ❌ Files out of sync
- ❌ Missing timestamps in COMPLETE_TASKS.md

**Enforcement:**
- 🚨 Cannot complete Phase 1 without creating all three files
- 🚨 Cannot complete any phase without updating all three files
- 🚨 Cannot complete Phase 7 unless all tasks marked [x] in TODO.md

---

