# Full Project Workflow

> **Complete workflow for building entire projects from scratch**

---

## Use This When

**Use this workflow when:**
- ✅ Starting a complete new project
- ✅ Building a full application (not just a feature)
- ✅ Need to set up everything from scratch
- ✅ Project will take days/weeks (not hours)
- ✅ Multiple components and integrations

**Don't use this when:**
- ❌ Adding a single feature to existing project
- ❌ Quick prototype or POC
- ❌ Simple script or tool
- ❌ Bug fix or maintenance task

---

## Purpose

Build complete, production-ready projects with:
- Proper planning and architecture
- Clean code structure
- Comprehensive testing
- Complete documentation
- Deployment readiness

---

## Decision Rule

```
If project scope is:
  - Single feature → Use feature workflow
  - Bug fix → Use troubleshooting workflow
  - Full application → Use THIS workflow
  - Prototype → Use rapid prototyping workflow
```

---

## Workflow Overview

```
Phase 1: Initialize
  ├─ Set up project tracking
  ├─ Initialize memory context
  └─ Create project structure

Phase 2: Plan
  ├─ Understand requirements
  ├─ Design architecture
  ├─ Create detailed plan
  └─ Review and approve

Phase 3: Build
  ├─ Implement in phases
  ├─ Test continuously
  ├─ Document as you go
  └─ Review quality gates

Phase 4: Finalize
  ├─ Complete testing
  ├─ Finalize documentation
  ├─ Prepare deployment
  └─ Handoff

Phase 5: Deliver
  ├─ Deploy to production
  ├─ Verify functionality
  ├─ Create handoff document
  └─ Archive project context
```

---

## Phase 1: Initialize

### Step 1.1: Set Up Project Tracking

**Create project tracking files in user's project:**

```bash
# In user's project root
mkdir -p .ai

# Create tracking files
touch .ai/PROJECT_PLAN.md
touch .ai/PROGRESS_TRACKER.md
touch .ai/DECISIONS_LOG.md
touch .ai/ARCHITECTURE.md
touch .ai/MEMORY_CONTEXT.md
```

**Location:** `~/user-project/.ai/` (NOT ~/.global/!)

**Templates:** See `knowledge/templates/`

### Step 1.2: Initialize Memory

```python
# Save project initialization to memory
memory.save({
    "type": "project_start",
    "project_name": "user-project-name",
    "date": "2025-11-04",
    "location": "~/user-project/",
    "tracking_files": "~/user-project/.ai/"
})
```

**Location:** `~/.global/memory/` (YOUR tool!)

### Step 1.3: Initialize MCP

```python
# Check available tools
servers = mcp.list_servers()
tools = mcp.list_all_tools()

# Save to memory
memory.save({
    "type": "mcp_initialization",
    "available_servers": servers,
    "available_tools": len(tools)
})
```

### Step 1.4: Create Project Structure

**Based on project type:**

```
Web Application:
  ~/user-project/
  ├── .ai/              # AI tracking files
  ├── src/              # Source code
  ├── tests/            # Tests
  ├── docs/             # Documentation
  ├── config/           # Configuration
  └── deploy/           # Deployment files

API Service:
  ~/user-project/
  ├── .ai/
  ├── api/
  ├── models/
  ├── services/
  ├── tests/
  └── docs/

Full-Stack:
  ~/user-project/
  ├── .ai/
  ├── backend/
  ├── frontend/
  ├── database/
  ├── tests/
  └── docs/
```

---

## Phase 2: Plan

### Step 2.1: Understand Requirements

**Read and analyze:**
- User's requirements
- Constraints
- Priorities
- Success criteria

**Document in:** `.ai/PROJECT_PLAN.md`

**Save to memory:**
```python
memory.save({
    "type": "requirements",
    "summary": "...",
    "key_features": [...],
    "constraints": [...],
    "priorities": [...]
})
```

### Step 2.2: Design Architecture

**Create architecture document:**
- System components
- Data flow
- Technology choices (with rationale!)
- Integration points
- Security considerations

**Document in:** `.ai/ARCHITECTURE.md`

**Decision Rule:**
```
For each technology choice:
  ❌ Don't choose: Most familiar
  ✅ Choose: Best fit for requirements
  
  Document:
  - What you chose
  - Why you chose it
  - What alternatives you considered
  - Trade-offs
```

**Save to memory:**
```python
memory.save({
    "type": "architecture_decision",
    "component": "database",
    "choice": "PostgreSQL",
    "rationale": "Need JSONB support, ACID compliance",
    "alternatives": ["MongoDB", "MySQL"],
    "trade_offs": "..."
})
```

### Step 2.3: Create Detailed Plan

**Break down into phases:**
1. Phase 1: Core functionality
2. Phase 2: Additional features
3. Phase 3: Polish and optimization

**For each phase:**
- Tasks
- Dependencies
- Estimated effort
- Success criteria

**Document in:** `.ai/PROJECT_PLAN.md`

### Step 2.4: Review and Approve

**Quality gates:**
- [ ] Requirements clear and complete?
- [ ] Architecture sound and scalable?
- [ ] Plan detailed and realistic?
- [ ] All decisions documented?
- [ ] User approved?

**Save to memory:**
```python
memory.save({
    "type": "plan_approved",
    "date": "...",
    "phases": [...],
    "estimated_duration": "..."
})
```

---

## Phase 3: Build

### Step 3.1: Implement in Phases

**For each phase:**

```
1. Review phase plan
2. Set up phase tracking
3. Implement features
4. Test as you go
5. Document code
6. Update progress tracker
7. Save milestones to memory
```

**Update:** `.ai/PROGRESS_TRACKER.md`

**Example:**
```markdown
## Phase 1: Core Functionality

### Task 1: Database Setup
- Status: ✅ Complete
- Duration: 2 hours
- Notes: PostgreSQL with JSONB
- Commit: abc123

### Task 2: User Authentication
- Status: 🔄 In Progress
- Started: 2025-11-04 10:00
- Notes: Implementing JWT
```

### Step 3.2: Test Continuously

**Testing strategy:**
- Unit tests (95%+ coverage)
- Integration tests
- End-to-end tests
- Security tests

**Quality gate:**
```
Before moving to next phase:
  - [ ] All tests passing
  - [ ] Coverage >= 95%
  - [ ] No critical issues
  - [ ] Code reviewed
  - [ ] Documentation updated
```

### Step 3.3: Document As You Go

**What to document:**
- API endpoints
- Database schema
- Configuration options
- Environment variables
- Deployment steps

**Where:**
- Code comments (inline)
- README files (per module)
- API documentation (OpenAPI/Swagger)
- `.ai/ARCHITECTURE.md` (high-level)

### Step 3.4: Log Decisions

**Every important decision:**

```markdown
## Decision: Use Redis for Caching

**Date:** 2025-11-04
**Context:** Need fast session storage
**Decision:** Use Redis
**Rationale:** 
  - Sub-millisecond latency
  - Built-in expiration
  - Proven at scale
**Alternatives:** Memcached, in-memory
**Trade-offs:** Additional dependency
**Status:** Implemented
```

**Document in:** `.ai/DECISIONS_LOG.md`

**Save to memory:**
```python
memory.save({
    "type": "decision",
    "decision": "Use Redis for caching",
    "rationale": "...",
    "impact": "medium"
})
```

---

## Phase 4: Finalize

### Step 4.1: Complete Testing

**Final testing checklist:**
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] End-to-end tests passing
- [ ] Security scan clean
- [ ] Performance acceptable
- [ ] Cross-browser tested (if web)
- [ ] Mobile responsive (if web)

### Step 4.2: Finalize Documentation

**Complete documentation:**
- [ ] README.md (project overview)
- [ ] INSTALL.md (installation steps)
- [ ] API.md (API documentation)
- [ ] DEPLOYMENT.md (deployment guide)
- [ ] TROUBLESHOOTING.md (common issues)

### Step 4.3: Prepare Deployment

**Deployment checklist:**
- [ ] Environment variables documented
- [ ] Database migrations ready
- [ ] Deployment scripts tested
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Logging configured

### Step 4.4: Create Handoff Document

**Include:**
- Project overview
- Architecture summary
- Key decisions and rationale
- How to run locally
- How to deploy
- How to troubleshoot
- Future recommendations

**Document in:** `.ai/HANDOFF.md`

---

## Phase 5: Deliver

### Step 5.1: Deploy to Production

**Follow deployment workflow:**
1. Final backup
2. Run deployment script
3. Verify deployment
4. Monitor for issues
5. Document deployment

**Save to memory:**
```python
memory.save({
    "type": "deployment",
    "date": "...",
    "environment": "production",
    "version": "1.0.0",
    "status": "success"
})
```

### Step 5.2: Verify Functionality

**Post-deployment checks:**
- [ ] Application accessible
- [ ] All features working
- [ ] No errors in logs
- [ ] Performance acceptable
- [ ] Security headers present

### Step 5.3: Archive Project Context

**Save complete context to memory:**
```python
memory.save({
    "type": "project_complete",
    "project_name": "...",
    "duration": "...",
    "key_learnings": [...],
    "challenges": [...],
    "solutions": [...],
    "recommendations": [...]
})
```

### Step 5.4: Deliver to User

**Deliverables:**
1. Working application (deployed)
2. Source code (repository)
3. Documentation (complete)
4. Handoff document (.ai/HANDOFF.md)
5. Access credentials (if applicable)

---

## Quality Gates

**Throughout project:**

### Code Quality
- [ ] Follows best practices
- [ ] Clean and readable
- [ ] Well-documented
- [ ] No code smells
- [ ] Passes linting

### Testing Quality
- [ ] 95%+ coverage
- [ ] All tests passing
- [ ] Edge cases covered
- [ ] Performance tested
- [ ] Security tested

### Documentation Quality
- [ ] Complete and accurate
- [ ] Clear and concise
- [ ] Examples provided
- [ ] Up to date
- [ ] Easy to follow

### Architecture Quality
- [ ] Scalable design
- [ ] Maintainable code
- [ ] Security considered
- [ ] Performance optimized
- [ ] Best solution chosen (not easiest!)

---

## Memory Management

**Save to memory at:**
- Project start
- Each phase completion
- Important decisions
- Challenges and solutions
- Milestones reached
- Project completion

**Memory location:** `~/.global/memory/` (YOUR tool!)

---

## Related Knowledge Items

- `knowledge/workflows/project_initialization.md` - Detailed initialization
- `knowledge/templates/PROJECT_PLAN.md` - Plan template
- `knowledge/templates/PROGRESS_TRACKER.md` - Tracker template
- `knowledge/templates/DECISIONS_LOG.md` - Decisions template
- `knowledge/templates/HANDOFF.md` - Handoff template

---

## Example: Building a Blog Platform

```
Phase 1: Initialize (30 min)
  ├─ Create .ai/ folder
  ├─ Initialize memory
  ├─ Check MCP tools
  └─ Create project structure

Phase 2: Plan (2 hours)
  ├─ Requirements: Blog with auth, posts, comments
  ├─ Architecture: Flask + PostgreSQL + React
  ├─ Plan: 3 phases over 2 weeks
  └─ Approved by user

Phase 3: Build (10 days)
  ├─ Phase 1: Backend API (3 days)
  ├─ Phase 2: Frontend (4 days)
  ├─ Phase 3: Polish (3 days)
  └─ All quality gates passed

Phase 4: Finalize (1 day)
  ├─ Complete testing
  ├─ Finalize docs
  ├─ Prepare deployment
  └─ Create handoff

Phase 5: Deliver (2 hours)
  ├─ Deploy to production
  ├─ Verify functionality
  ├─ Archive context
  └─ Deliver to user

Total: 12 days
Result: Production-ready blog platform
```

---

## Best Practices

1. **Always initialize properly**
   - Set up tracking files
   - Initialize memory
   - Check MCP tools

2. **Plan before coding**
   - Understand requirements fully
   - Design architecture carefully
   - Document decisions

3. **Build incrementally**
   - Work in phases
   - Test continuously
   - Document as you go

4. **Maintain quality**
   - Pass all quality gates
   - Choose best solutions
   - No shortcuts!

5. **Document everything**
   - Code comments
   - API docs
   - Architecture docs
   - Decision logs

6. **Use memory effectively**
   - Save important decisions
   - Log challenges and solutions
   - Archive complete context

---

**Remember: You're building something to be proud of. Choose the best solution, not the easiest!**

