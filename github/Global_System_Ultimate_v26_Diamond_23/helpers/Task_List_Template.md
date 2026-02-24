# Task List (Global System Ultimate)

> **Purpose:** Track all tasks with priorities, owners, and status. This is the single source of truth for what needs to be done.
> **Automation:** This file is parsed by `speckit.py` to drive the Agentic Engine.

**Last Updated:** [DATE]  
**Project:** {{PROJECT_NAME}}

---

## How to Use This File

1. **Add tasks:** When planning, add all tasks here.
2. **Update status:** Keep status current (To Do → In Progress → Done).
3. **Speckit Integration:** `speckit.py implement` reads the first "To Do" task.

---

## Priority Levels

- **P0 (Critical):** Must be done immediately, blocks everything.
- **P1 (High):** Should be done soon, important for success.
- **P2 (Medium):** Should be done eventually, nice to have.
- **P3 (Low):** Can be done later, optional enhancement.

---

## Status Values

- **To Do:** Not started yet.
- **In Progress:** Currently being worked on.
- **Blocked:** Cannot proceed due to dependency.
- **Review:** Waiting for review (Speckit Verify).
- **Done:** Completed and verified.

---

## Current Sprint / Active Tasks

### P0 - Critical (Do First!)

#### [P0][Builder][To Do] Setup Database Schema
**Description:** Create complete database schema with all tables, relationships, and constraints.

**Requirements:**
- All tables defined.
- Foreign keys configured.
- Migrations created.

**Acceptance Criteria:**
- [ ] All tables created.
- [ ] Migrations tested (up and down).
- [ ] Sentinel Check Passed (No Secrets).

**Dependencies:** None

---

#### [P0][Builder][To Do] Implement Authentication
**Description:** Implement JWT-based authentication system.

**Requirements:**
- User registration/login.
- Token generation/validation.
- Password hashing (bcrypt).

**Acceptance Criteria:**
- [ ] Registration/Login endpoints work.
- [ ] Tokens are generated correctly.
- [ ] Sentinel Check Passed (No Secrets).

**Dependencies:** Database Schema (P0)

---

### P1 - High Priority

#### [P1][Builder][To Do] Create Core API Endpoints
**Description:** Implement CRUD endpoints for main entities.

**Requirements:**
- Users/Products/Orders CRUD.
- Input validation (Pydantic).

**Acceptance Criteria:**
- [ ] All CRUD endpoints implemented.
- [ ] Tests written and passing.
- [ ] CodeRabbit Review Passed.

**Dependencies:** Database Schema (P0), Authentication (P0)

---

## Completed Tasks

#### [P0][Architect][Done] Project Initialization
**Description:** Initialize project structure and dependencies.
**Completed:** [DATE]
