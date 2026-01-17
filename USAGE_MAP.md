# Usage Map - Global Guidelines v10.0

> **Your complete guide to using the knowledge system**

---

## Quick Start

### For ANY New Task

```
1. Read: CORE_PROMPT_v10.md (this is YOU!)
2. Initialize: Memory + MCP (MANDATORY!)
3. Read: This usage map (you are here)
4. Follow: Scenario-specific path below
```

---

## How to Use This Map

**This map shows:**
- Which knowledge items to use when
- In what order to read them
- How they connect
- Decision points

**Format:**
```
📖 = Read this knowledge item
🔧 = Use this tool
⚡ = Critical step
🎯 = Decision point
```

---

## Universal Workflow (Every Task)

```
START
  ↓
📖 CORE_PROMPT_v10.md
  ↓
⚡ Initialize
  ├─ 🔧 Memory System (knowledge/core/memory.md)
  └─ 🔧 MCP System (knowledge/core/mcp.md)
  ↓
⚡ Verify Environment Separation
  └─ 📖 knowledge/core/environment.md
  ↓
🎯 What type of task?
  ├─ API Development → [Path A]
  ├─ Bug Fix → [Path B]
  ├─ Database Design → [Path C]
  ├─ Frontend Development → [Path D]
  ├─ Security Implementation → [Path E]
  ├─ Testing → [Path F]
  └─ Deployment → [Path G]
```

---

## Path A: API Development

**Use this path when:**
- Building REST API
- Creating GraphQL API
- Adding API endpoints
- Integrating third-party APIs

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()

2. Understand Requirements
   📖 knowledge/development/requirements.md
   🔧 Save requirements to memory

3. Design API
   📖 knowledge/development/api.md
   🎯 REST or GraphQL?
      ├─ REST → knowledge/technical/rest.md
      └─ GraphQL → knowledge/technical/graphql.md
   ⚡ Choose BEST, not easiest!

4. Choose Framework
   📖 knowledge/technical/backend.md
   🎯 Which framework?
      ├─ FastAPI → For modern Python APIs
      ├─ Django REST → For full-featured apps
      └─ Flask → For lightweight APIs
   ⚡ Choose based on requirements!

5. Design Database
   📖 knowledge/development/database.md
   🔧 Design schema
   ⚡ Verify: ~/user-project/database/ (NOT ~/.global/!)

6. Implement Security
   📖 knowledge/development/security.md
   📖 knowledge/development/authentication.md
   🔧 Add auth, validation, CORS

7. Write Tests
   📖 knowledge/development/testing.md
   🔧 Unit + Integration tests
   ⚡ Target: 95%+ coverage

8. Document API
   📖 knowledge/operations/documentation.md
   🔧 OpenAPI/Swagger docs

9. Review & Deliver
   ⚡ Quality gates passed?
   🔧 Save completion to memory
   ✅ Deliver!
```

### Knowledge Items for API Development

**Must Read:**
- `knowledge/core/memory.md`
- `knowledge/core/mcp.md`
- `knowledge/core/environment.md`
- `knowledge/development/api.md`
- `knowledge/development/security.md`

**Should Read:**
- `knowledge/technical/backend.md`
- `knowledge/development/database.md`
- `knowledge/development/testing.md`

**Optional:**
- `knowledge/technical/rest.md`
- `knowledge/technical/graphql.md`
- `knowledge/operations/monitoring.md`

---

## Path B: Bug Fix

**Use this path when:**
- User reports a bug
- Tests are failing
- Unexpected behavior
- Performance issues

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()

2. Extract Error Information
   📖 knowledge/operations/troubleshooting.md
   🔧 Extract:
      - Error messages
      - Stack traces
      - Imports/Exports
      - Classes/Functions
   🔧 Save to memory

3. Analyze Root Cause
   📖 knowledge/core/thinking.md
   🔧 Deep analysis
   🔧 Check memory for similar errors

4. Plan Fix
   🎯 Decision: Best solution?
      - Quick patch? ❌ NO!
      - Proper fix? ✅ YES!
   📖 knowledge/development/debugging.md

5. Implement Fix
   🔧 Write fix
   🔧 Add test to prevent regression
   ⚡ Verify environment separation

6. Handle Errors (if fix fails)
   📖 knowledge/operations/error_handling.md
   Attempt 1: Known solutions
   Attempt 2: Deep analysis
   Attempt 3: Internet search
   Attempt 4+: Ask user

7. Verify Fix
   📖 knowledge/development/testing.md
   🔧 Run all tests
   🔧 Manual verification

8. Document Solution
   🔧 Save to memory
   📖 knowledge/operations/documentation.md

9. Deliver
   ✅ Explain fix
   ✅ Provide prevention tips
```

### Knowledge Items for Bug Fixes

**Must Read:**
- `knowledge/core/memory.md`
- `knowledge/operations/troubleshooting.md`
- `knowledge/operations/error_handling.md`

**Should Read:**
- `knowledge/core/thinking.md`
- `knowledge/development/debugging.md`
- `knowledge/development/testing.md`

---

## Path C: Database Design

**Use this path when:**
- Designing new database
- Modifying schema
- Optimizing queries
- Data modeling

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()

2. Analyze Data Requirements
   📖 knowledge/development/requirements.md
   🔧 Identify:
      - Entities
      - Relationships
      - Constraints
      - Access patterns

3. Choose Database Type
   📖 knowledge/development/database.md
   🎯 SQL or NoSQL?
      ├─ SQL → Structured data, ACID
      └─ NoSQL → Flexible schema, scale
   ⚡ Choose BEST for data model!

4. Design Schema
   📖 knowledge/technical/database_design.md
   🔧 Normalize (to appropriate level)
   🔧 Define relationships
   🔧 Add constraints
   ⚡ Verify: ~/user-project/database/ (NOT ~/.global/!)

5. Plan Indexes
   📖 knowledge/technical/database_optimization.md
   🔧 Identify slow queries
   🔧 Add strategic indexes
   ⚡ Balance read/write performance

6. Create Migrations
   📖 knowledge/technical/migrations.md
   🔧 Version control schema
   🔧 Rollback plan

7. Implement & Test
   🔧 Create database
   🔧 Run migrations
   🔧 Test queries
   📖 knowledge/development/testing.md

8. Optimize
   📖 knowledge/technical/database_optimization.md
   🔧 Query optimization
   🔧 Index tuning
   🔧 Connection pooling

9. Document
   📖 knowledge/operations/documentation.md
   🔧 Schema diagrams
   🔧 Query examples

10. Deliver
    ✅ Schema ready
    ✅ Migrations tested
    ✅ Documentation complete
```

### Knowledge Items for Database Design

**Must Read:**
- `knowledge/core/environment.md` (Critical for DB location!)
- `knowledge/development/database.md`
- `knowledge/technical/database_design.md`

**Should Read:**
- `knowledge/technical/database_optimization.md`
- `knowledge/technical/migrations.md`
- `knowledge/development/testing.md`

---

## Path D: Frontend Development

**Use this path when:**
- Building user interface
- Creating components
- Implementing responsive design
- Adding interactivity

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()
   ⚡ Check: playwright MCP for testing!

2. Understand Requirements
   📖 knowledge/development/requirements.md
   🔧 UI/UX requirements
   🔧 Responsive needs
   🔧 Accessibility requirements

3. Choose Framework
   📖 knowledge/technical/frontend.md
   🎯 Which framework?
      ├─ React → Component-based, large ecosystem
      ├─ Vue → Progressive, easy learning curve
      └─ Svelte → Compile-time, minimal runtime
   ⚡ Choose BEST for project!

4. Design Components
   📖 knowledge/technical/component_design.md
   🔧 Component hierarchy
   🔧 State management
   🔧 Props flow

5. Implement UI
   📖 knowledge/technical/ui_development.md
   🔧 Build components
   🔧 Add styling
   🔧 Ensure responsiveness
   ⚡ Verify: ~/user-project/src/frontend/ (NOT ~/.global/!)

6. Add Interactivity
   📖 knowledge/technical/javascript.md
   🔧 Event handlers
   🔧 API integration
   🔧 State updates

7. Ensure Accessibility
   📖 knowledge/development/accessibility.md
   🔧 ARIA labels
   🔧 Keyboard navigation
   🔧 Screen reader support

8. Test
   📖 knowledge/development/testing.md
   🔧 Component tests
   🔧 E2E tests (use playwright MCP!)
   🔧 Visual regression tests

9. Optimize
   📖 knowledge/technical/frontend_optimization.md
   🔧 Bundle size
   🔧 Load time
   🔧 Runtime performance

10. Deliver
    ✅ UI complete
    ✅ Tests passing
    ✅ Accessible
    ✅ Performant
```

### Knowledge Items for Frontend Development

**Must Read:**
- `knowledge/core/mcp.md` (Use playwright!)
- `knowledge/technical/frontend.md`
- `knowledge/development/accessibility.md`

**Should Read:**
- `knowledge/technical/component_design.md`
- `knowledge/technical/ui_development.md`
- `knowledge/development/testing.md`

---

## Path E: Security Implementation

**Use this path when:**
- Adding authentication
- Implementing authorization
- Securing API endpoints
- Handling sensitive data
- Security audit

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()

2. Assess Security Requirements
   📖 knowledge/development/security.md
   🔧 Identify:
      - Authentication needs
      - Authorization levels
      - Data sensitivity
      - Compliance requirements

3. Implement Authentication
   📖 knowledge/development/authentication.md
   🎯 Which method?
      ├─ JWT → Stateless, scalable
      ├─ Session → Stateful, revocable
      └─ OAuth → Third-party auth
   ⚡ Choose MOST SECURE, not simplest!

4. Implement Authorization
   📖 knowledge/technical/authorization.md
   🔧 Role-based access control
   🔧 Permission system
   🔧 Resource-level permissions

5. Secure Data
   📖 knowledge/technical/data_security.md
   🔧 Encryption at rest
   🔧 Encryption in transit
   🔧 Secure key management
   ⚡ Verify: Keys NOT in code!

6. Input Validation
   📖 knowledge/technical/input_validation.md
   🔧 Sanitize inputs
   🔧 Prevent injection
   🔧 Rate limiting

7. Security Headers
   📖 knowledge/technical/security_headers.md
   🔧 CORS
   🔧 CSP
   🔧 HSTS

8. Audit & Test
   📖 knowledge/development/security_testing.md
   🔧 Penetration testing
   🔧 Vulnerability scanning
   🔧 Code review

9. Document Security
   📖 knowledge/operations/security_documentation.md
   🔧 Security policies
   🔧 Incident response plan

10. Deliver
    ✅ Authentication working
    ✅ Authorization enforced
    ✅ Data secured
    ✅ Tested & audited
```

### Knowledge Items for Security

**Must Read:**
- `knowledge/development/security.md`
- `knowledge/development/authentication.md`
- `knowledge/technical/data_security.md`

**Should Read:**
- `knowledge/technical/authorization.md`
- `knowledge/technical/input_validation.md`
- `knowledge/development/security_testing.md`

---

## Path F: Testing

**Use this path when:**
- Writing tests
- Improving coverage
- Setting up CI/CD
- Test-driven development

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()

2. Plan Testing Strategy
   📖 knowledge/development/testing.md
   🔧 Identify:
      - Unit test needs
      - Integration test needs
      - E2E test needs
      - Performance test needs

3. Write Unit Tests
   📖 knowledge/technical/unit_testing.md
   🔧 Test individual functions
   🔧 Mock dependencies
   🔧 Edge cases
   ⚡ Target: 95%+ coverage

4. Write Integration Tests
   📖 knowledge/technical/integration_testing.md
   🔧 Test component interactions
   🔧 Test API endpoints
   🔧 Test database operations

5. Write E2E Tests
   📖 knowledge/technical/e2e_testing.md
   🔧 Use playwright MCP!
   🔧 Test user workflows
   🔧 Test critical paths

6. Performance Tests
   📖 knowledge/technical/performance_testing.md
   🔧 Load testing
   🔧 Stress testing
   🔧 Benchmark

7. Set Up CI/CD
   📖 knowledge/operations/cicd.md
   🔧 Automated test runs
   🔧 Coverage reports
   🔧 Quality gates

8. Review Coverage
   🔧 Identify gaps
   🔧 Add missing tests
   ⚡ Minimum: 95%

9. Deliver
    ✅ Comprehensive test suite
    ✅ High coverage
    ✅ CI/CD configured
```

### Knowledge Items for Testing

**Must Read:**
- `knowledge/development/testing.md`
- `knowledge/technical/unit_testing.md`
- `knowledge/technical/integration_testing.md`

**Should Read:**
- `knowledge/technical/e2e_testing.md`
- `knowledge/technical/performance_testing.md`
- `knowledge/operations/cicd.md`

---

## Path G: Deployment

**Use this path when:**
- Deploying to production
- Setting up infrastructure
- Configuring CI/CD
- Managing environments

### Step-by-Step

```
1. Initialize
   📖 knowledge/core/memory.md
   📖 knowledge/core/mcp.md
   ⚡ memory.init() + mcp.list_servers()
   ⚡ Check: cloudflare MCP for deployment!

2. Prepare for Deployment
   📖 knowledge/operations/deployment.md
   🔧 Environment variables
   🔧 Secrets management
   🔧 Configuration files
   ⚡ Verify: No secrets in code!

3. Choose Deployment Strategy
   📖 knowledge/technical/deployment_strategies.md
   🎯 Which strategy?
      ├─ Blue-Green → Zero downtime
      ├─ Rolling → Gradual rollout
      └─ Canary → Test with subset
   ⚡ Choose BEST for requirements!

4. Containerize
   📖 knowledge/technical/docker.md
   🔧 Create Dockerfile
   🔧 Docker Compose
   🔧 Optimize image size
   ⚡ Verify: ~/user-project/docker/ (NOT ~/.global/!)

5. Set Up Infrastructure
   📖 knowledge/technical/infrastructure.md
   🔧 Cloud provider setup
   🔧 Networking
   🔧 Load balancing
   🔧 Database setup

6. Configure CI/CD
   📖 knowledge/operations/cicd.md
   🔧 Build pipeline
   🔧 Test pipeline
   🔧 Deploy pipeline
   🔧 Rollback plan

7. Set Up Monitoring
   📖 knowledge/operations/monitoring.md
   🔧 Logging
   🔧 Metrics
   🔧 Alerts
   🔧 Use sentry MCP for error tracking!

8. Security Hardening
   📖 knowledge/operations/production_security.md
   🔧 Firewall rules
   🔧 SSL/TLS
   🔧 Security groups

9. Deploy
   🔧 Run deployment
   🔧 Verify health checks
   🔧 Monitor logs

10. Post-Deployment
    📖 knowledge/operations/post_deployment.md
    🔧 Smoke tests
    🔧 Monitor metrics
    🔧 Document deployment

11. Deliver
    ✅ Application deployed
    ✅ Monitoring active
    ✅ Documentation complete
```

### Knowledge Items for Deployment

**Must Read:**
- `knowledge/operations/deployment.md`
- `knowledge/technical/docker.md`
- `knowledge/operations/monitoring.md`

**Should Read:**
- `knowledge/technical/deployment_strategies.md`
- `knowledge/technical/infrastructure.md`
- `knowledge/operations/cicd.md`

---

## Decision Trees

### Tree 1: Which Database?

```
Need database?
├─ YES
│   ├─ Structured data + ACID required?
│   │   ├─ YES → PostgreSQL (best for complex queries)
│   │   └─ NO → Check scale requirements
│   │       ├─ Massive scale? → NoSQL (MongoDB, Cassandra)
│   │       └─ Moderate scale? → PostgreSQL (still best!)
│   └─ Simple key-value?
│       └─ YES → Redis (fast, simple)
└─ NO
    └─ Skip database setup
```

### Tree 2: Which Framework?

```
Need framework?
├─ Backend?
│   ├─ Python?
│   │   ├─ Full-featured? → Django
│   │   ├─ Modern API? → FastAPI
│   │   └─ Lightweight? → Flask
│   └─ JavaScript?
│       ├─ Full-featured? → NestJS
│       └─ Lightweight? → Express
└─ Frontend?
    ├─ Large app? → React
    ├─ Progressive? → Vue
    └─ Performance-critical? → Svelte
```

### Tree 3: Error Handling

```
Error occurred?
├─ YES
│   ├─ First time seeing this error?
│   │   ├─ YES
│   │   │   ├─ Attempt 1: Analyze & fix
│   │   │   ├─ Still failing?
│   │   │   │   ├─ Attempt 2: Deep dive
│   │   │   │   ├─ Still failing?
│   │   │   │   │   ├─ Attempt 3: Search internet
│   │   │   │   │   └─ Still failing? → Ask user
│   │   │   └─ Fixed? → Save solution to memory!
│   │   └─ NO → Check memory for solution
│   │       ├─ Found? → Apply solution
│   │       └─ Not found? → Attempt 1 (above)
└─ NO
    └─ Continue work
```

---

## Knowledge Item Index

### Core (ALWAYS RELEVANT)
```
knowledge/core/
├── memory.md              ⚡ MANDATORY - Use for every task
├── mcp.md                 ⚡ MANDATORY - Check at task start
├── environment.md         ⚡ CRITICAL - Maintain separation
├── thinking.md            - Decision framework
└── context.md             - Context engineering
```

### Development (BUILDING THINGS)
```
knowledge/development/
├── api.md                 - API development
├── database.md            - Database design
├── testing.md             - Testing strategies
├── security.md            - Security practices
├── authentication.md      - Auth implementation
├── requirements.md        - Requirements gathering
└── debugging.md           - Debugging techniques
```

### Technical (SPECIFIC TECHNOLOGIES)
```
knowledge/technical/
├── backend.md             - Backend frameworks
├── frontend.md            - Frontend frameworks
├── docker.md              - Containerization
├── database_design.md     - Schema design
├── database_optimization.md - Query optimization
└── ... (more specific topics)
```

### Operations (RUNNING THINGS)
```
knowledge/operations/
├── deployment.md          - Deployment strategies
├── monitoring.md          - Monitoring & logging
├── troubleshooting.md     - Problem solving
├── error_handling.md      - Error management
├── maintenance.md         - Ongoing maintenance
└── documentation.md       - Documentation practices
```

---

## Quick Reference

### Every Task Starts With:
```
1. 📖 CORE_PROMPT_v10.md
2. 🔧 memory.init()
3. 🔧 mcp.list_servers()
4. 📖 knowledge/core/environment.md
5. 🎯 Choose path (A-G above)
```

### Every Task Ends With:
```
1. ✅ Quality gates passed?
2. ✅ Environment separation verified?
3. 🔧 Save completion to memory
4. 📖 Document deliverables
5. ✅ Deliver to user
```

### Always Remember:
```
- Memory & MCP are YOUR tools (not user's project!)
- Always choose BEST solution (not easiest!)
- Maintain environment separation (CRITICAL!)
- Save important info to memory
- Document decisions and rationale
```

---

## Next Steps

1. **Read CORE_PROMPT_v10.md** if you haven't
2. **Identify your task type** (API, Bug Fix, etc.)
3. **Follow the appropriate path** (A-G above)
4. **Read knowledge items** in the order shown
5. **Execute with excellence!**

---

**Remember: You are a Senior Technical Lead. You have the knowledge. You have the tools. Now go build something amazing! 🚀**

**Version:** 10.0  
**Philosophy:** Always choose the best solution, not the easiest




---

## Path H: Full Project (Complete Application)

**Use this path when:**
- ✅ Starting a complete new project from scratch
- ✅ Building entire application (not just a feature)
- ✅ Project will take days/weeks
- ✅ Multiple components and integrations

**Don't use this when:**
- ❌ Adding single feature to existing project
- ❌ Quick prototype or POC
- ❌ Bug fix or maintenance

### Complete Workflow

```
Phase 0: PREPARATION
  ↓
📖 CORE_PROMPT_v10.md (understand who you are)
  ↓
⚡ CRITICAL: Understand Environment Separation
  📖 knowledge/core/environment.md
  ⚠️  Memory/MCP = YOUR tools (in ~/.global/)
  ⚠️  Project = USER'S code (in ~/user-project/)
  ⚠️  NEVER MIX THESE!
  ↓
⚡ Initialize Helper Tools
  🔧 memory.init() → ~/.global/memory/
  🔧 mcp.list_servers() → Check available tools
  💾 Save initialization to memory
  ↓
  
Phase 1: INITIALIZE PROJECT
  ↓
📖 knowledge/workflows/project_initialization.md
  ↓
⚡ Get Project Information
  - Project name?
  - Project type?
  - Requirements?
  - Technologies?
  - Timeline?
  💾 Save all to memory
  ↓
⚡ Create Project Structure
  📂 ~/user-project/.ai/ (tracking files)
  📂 ~/user-project/src/ (code)
  📂 ~/user-project/tests/ (tests)
  📂 ~/user-project/docs/ (documentation)
  ⚠️  NOT in ~/.global/!
  ↓
⚡ Copy Templates
  📄 .ai/PROJECT_PLAN.md
  📄 .ai/PROGRESS_TRACKER.md
  📄 .ai/DECISIONS_LOG.md
  📄 .ai/ARCHITECTURE.md
  ↓
⚡ Initialize Version Control
  🔧 git init
  📄 .gitignore
  💾 Initial commit
  ↓
  
Phase 2: PLANNING
  ↓
📖 knowledge/workflows/full_project.md (Phase 2 section)
  ↓
⚡ Understand Requirements
  📖 knowledge/development/requirements.md
  🎯 What are the core features?
  🎯 What are the constraints?
  🎯 What are success criteria?
  💾 Save to memory
  📝 Document in .ai/PROJECT_PLAN.md
  ↓
⚡ Design Architecture
  📖 knowledge/development/architecture.md
  🎯 What components needed?
  🎯 What technologies to use?
  ⚠️  Choose BEST, not easiest!
  
  For each technology choice:
    1. Evaluate options
    2. Choose best fit
    3. Document rationale
    4. Log alternatives considered
    5. Note trade-offs
    💾 Save decision to memory
    📝 Log in .ai/DECISIONS_LOG.md
  ↓
⚡ Create Detailed Plan
  🎯 Break into phases (typically 3-5)
  🎯 Define tasks for each phase
  🎯 Estimate effort
  🎯 Set success criteria
  📝 Document in .ai/PROJECT_PLAN.md
  💾 Save to memory
  ↓
⚡ Review with User
  📋 Present plan
  🎯 Get approval
  📝 Update based on feedback
  💾 Save approved plan to memory
  ↓
  
Phase 3: BUILD
  ↓
📖 knowledge/workflows/full_project.md (Phase 3 section)
  ↓
For each development phase:
  ↓
  ⚡ Set Up Phase
    📝 Update .ai/PROGRESS_TRACKER.md
    💾 Save phase start to memory
    ↓
  ⚡ Implement Features
    🎯 What type of work?
       ├─ Backend → Path A (API Development)
       ├─ Frontend → Path D (Frontend Development)
       ├─ Database → Path C (Database Design)
       ├─ Security → Path E (Security)
       └─ Testing → Path F (Testing)
    ↓
    For each feature:
      1. Read relevant knowledge items
      2. Implement with best practices
      3. Test thoroughly
      4. Document code
      5. Update progress tracker
      6. Save milestone to memory
    ↓
  ⚡ Test Continuously
    📖 knowledge/quality/testing.md
    🔧 Run unit tests
    🔧 Run integration tests
    🎯 Coverage >= 95%?
       ├─ Yes → Continue
       └─ No → Add more tests
    ↓
  ⚡ Document As You Go
    📝 Code comments
    📝 API documentation
    📝 README files
    📝 Update .ai/ARCHITECTURE.md
    ↓
  ⚡ Log Decisions
    For each important decision:
      📝 Log in .ai/DECISIONS_LOG.md
      💾 Save to memory
    ↓
  ⚡ Quality Gate
    [ ] All tests passing?
    [ ] Coverage >= 95%?
    [ ] No critical issues?
    [ ] Code reviewed?
    [ ] Documentation updated?
    
    🎯 All passed?
       ├─ Yes → Next phase
       └─ No → Fix issues first
    ↓
  💾 Save phase completion to memory
  📝 Update .ai/PROGRESS_TRACKER.md
  ↓
  
Phase 4: FINALIZE
  ↓
📖 knowledge/workflows/full_project.md (Phase 4 section)
  ↓
⚡ Complete Testing
  🔧 All unit tests
  🔧 All integration tests
  🔧 End-to-end tests
  🔧 Security scan
  🔧 Performance test
  [ ] All passed?
  ↓
⚡ Finalize Documentation
  📝 README.md (complete)
  📝 INSTALL.md (installation steps)
  📝 API.md (API docs)
  📝 DEPLOYMENT.md (deployment guide)
  📝 TROUBLESHOOTING.md (common issues)
  ↓
⚡ Prepare Deployment
  📖 knowledge/operations/deployment.md
  📋 Deployment checklist
  🔧 Test deployment scripts
  📝 Document rollback plan
  ↓
⚡ Create Handoff Document
  📄 Copy template: knowledge/templates/HANDOFF.md
  📝 Fill with project details
  📝 Include all key decisions
  📝 Document how to run/deploy
  💾 Save to .ai/HANDOFF.md
  ↓
  
Phase 5: DELIVER
  ↓
📖 knowledge/workflows/full_project.md (Phase 5 section)
  ↓
⚡ Deploy to Production
  📖 knowledge/operations/deployment.md
  🔧 Run deployment
  🔧 Verify deployment
  🔧 Monitor for issues
  💾 Save deployment to memory
  ↓
⚡ Verify Functionality
  [ ] Application accessible?
  [ ] All features working?
  [ ] No errors in logs?
  [ ] Performance acceptable?
  [ ] Security headers present?
  ↓
⚡ Archive Project Context
  💾 Save complete context to memory:
     - Project summary
     - Key decisions
     - Challenges faced
     - Solutions implemented
     - Learnings
     - Recommendations
  ↓
⚡ Deliver to User
  📦 Deliverables:
     1. Working application (deployed)
     2. Source code (repository)
     3. Documentation (complete)
     4. Handoff document (.ai/HANDOFF.md)
     5. Access credentials (if applicable)
  ↓
✅ PROJECT COMPLETE!
```

### Memory Management Throughout

**Save to memory at:**
- ⚡ Project initialization
- ⚡ Each major decision
- ⚡ Each phase completion
- ⚡ Challenges encountered
- ⚡ Solutions discovered
- ⚡ Milestones reached
- ⚡ Project completion

**Memory location:** `~/.global/memory/` (YOUR tool!)

### Decision Points

#### Technology Choices
```
For EACH technology decision:
  1. Evaluate options
  2. Consider requirements
  3. Choose BEST fit (not easiest!)
  4. Document rationale
  5. Log alternatives
  6. Note trade-offs
  7. Save to memory
  8. Log in .ai/DECISIONS_LOG.md
```

#### Architecture Decisions
```
For EACH architecture decision:
  1. Understand requirements
  2. Design options
  3. Evaluate trade-offs
  4. Choose best solution
  5. Document in .ai/ARCHITECTURE.md
  6. Save to memory
```

#### Problem Solving
```
When facing a problem:
  1. Try solution 1
  2. If fails, try solution 2
  3. If fails, try solution 3
  4. If 3 failures → Search internet
  5. Document solution found
  6. Save to memory
```

### Quality Gates

**Throughout project:**

#### Code Quality
- [ ] Follows best practices
- [ ] Clean and readable
- [ ] Well-documented
- [ ] No code smells
- [ ] Passes linting

#### Testing Quality
- [ ] 95%+ coverage
- [ ] All tests passing
- [ ] Edge cases covered
- [ ] Performance tested
- [ ] Security tested

#### Documentation Quality
- [ ] Complete and accurate
- [ ] Clear and concise
- [ ] Examples provided
- [ ] Up to date
- [ ] Easy to follow

#### Architecture Quality
- [ ] Scalable design
- [ ] Maintainable code
- [ ] Security considered
- [ ] Performance optimized
- [ ] Best solution chosen (not easiest!)

### Example Timeline

```
Week 1:
  Day 1: Initialize + Plan (Phase 0-2)
  Day 2-5: Build Phase 1 (Core functionality)

Week 2:
  Day 1-5: Build Phase 2 (Additional features)

Week 3:
  Day 1-3: Build Phase 3 (Polish)
  Day 4: Finalize (Phase 4)
  Day 5: Deploy + Deliver (Phase 5)
```

### Related Knowledge Items

**Core (Always read):**
- `knowledge/core/memory.md` - Memory system
- `knowledge/core/mcp.md` - MCP system
- `knowledge/core/environment.md` - Environment separation

**Workflows:**
- `knowledge/workflows/full_project.md` - Complete workflow details
- `knowledge/workflows/project_initialization.md` - Initialization details

**Templates:**
- `knowledge/templates/PROJECT_PLAN.md`
- `knowledge/templates/PROGRESS_TRACKER.md`
- `knowledge/templates/DECISIONS_LOG.md`
- `knowledge/templates/ARCHITECTURE.md`
- `knowledge/templates/HANDOFF.md`

**Development:**
- `knowledge/development/requirements.md`
- `knowledge/development/architecture.md`
- `knowledge/development/api.md`
- `knowledge/development/database.md`

**Quality:**
- `knowledge/quality/testing.md`
- `knowledge/quality/security.md`

**Operations:**
- `knowledge/operations/deployment.md`

**Deep Dive (when needed):**
- `prompts/10_requirements.txt` (140KB)
- `prompts/11_analysis.txt` (96KB)
- `prompts/12_planning.txt` (25KB)
- `prompts/20_backend.txt` (63KB)
- `prompts/22_database.txt` (24KB)
- `prompts/23_api.txt` (19KB)

### Best Practices

1. **Always initialize properly**
   - Memory + MCP first
   - Understand environment separation
   - Set up tracking files

2. **Plan before coding**
   - Understand requirements fully
   - Design architecture carefully
   - Document all decisions

3. **Build incrementally**
   - Work in phases
   - Test continuously
   - Document as you go

4. **Maintain quality**
   - Pass all quality gates
   - Choose best solutions
   - No shortcuts!

5. **Use memory effectively**
   - Save important decisions
   - Log challenges and solutions
   - Archive complete context

6. **Document everything**
   - Code comments
   - API docs
   - Architecture docs
   - Decision logs
   - Handoff document

### Common Mistakes

#### ❌ Mistake 1: Mixing Environments
```
DON'T:
~/user-project/memory/  # ❌ Memory in project!

DO:
~/.global/memory/       # ✅ Memory in global
~/user-project/.ai/     # ✅ Tracking in project
```

#### ❌ Mistake 2: Skipping Planning
```
DON'T:
Start coding immediately

DO:
1. Initialize
2. Understand requirements
3. Design architecture
4. Create plan
5. Get approval
6. THEN code
```

#### ❌ Mistake 3: Not Documenting Decisions
```
DON'T:
Choose technology without documenting

DO:
1. Evaluate options
2. Choose best
3. Document rationale
4. Save to memory
5. Log in DECISIONS_LOG.md
```

#### ❌ Mistake 4: Taking Shortcuts
```
DON'T:
Choose easiest solution

DO:
Choose BEST solution
Document why
Accept trade-offs
Build it right
```

---

**Remember: You're building a complete project. Take time to do it right. Choose the best solution, not the easiest!**

