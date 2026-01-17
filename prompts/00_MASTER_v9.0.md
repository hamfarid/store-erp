================================================================================
GLOBAL GUIDELINES - MASTER INDEX v9.0.0
================================================================================
Generated: 2025-11-07
Total Modules: 25
Version: 9.0.0 - Complete Autonomous Development with Testing & Documentation
================================================================================

⚠️ CRITICAL UPDATES IN v9.0.0:
- Added comprehensive testing modules (42-44)
- Added documentation and memory modules (70-72)
- Enhanced MCP integration with 7 servers
- Added UI/UX testing and fixes
- Added database testing and validation

================================================================================
⭐ USAGE GUIDELINES - READ THIS FIRST! ⭐
================================================================================

FOR AI SYSTEMS:
────────────────────────────────────────────────────────────────────────────
1. Read modules 01-06 FIRST before any task
2. Use memory (01) to save ALL context - MANDATORY
3. Check MCP (02-03) for available tools (7 servers)
4. Apply thinking framework (04) to EVERY problem
5. Use context engineering (05) to understand requirements
6. Manage tasks (06) systematically
7. ALWAYS test (42-44) after development
8. ALWAYS document (70) everything
9. ALWAYS save progress to memory (71)

FOR DEVELOPERS:
────────────────────────────────────────────────────────────────────────────
1. Start with AI-First modules to understand capabilities
2. Follow workflow modules for project structure
3. Reference development modules as needed
4. ALWAYS write tests (42-44) alongside code
5. ALWAYS update documentation (70)
6. Always consider security (30-31) and quality (40-41)
7. Use templates (60) for quick starts
8. Test UI/UX thoroughly (43)
9. Validate database integrity (44)

FOR PROJECTS:
────────────────────────────────────────────────────────────────────────────
- Small projects: 01-06, 10-12, relevant dev modules, 42-44, 70
- Large projects: Use ALL modules systematically
- Maintenance: Emphasize 01, 40-44, 71 (memory, quality, testing, progress)
- Bug fixes: 01, 04, 42-44, 71 (memory, thinking, testing, save progress)

MANDATORY WORKFLOW:
────────────────────────────────────────────────────────────────────────────
1. Load context from memory (01, 71)
2. Understand requirements (05, 10)
3. Think systematically (04)
4. Plan (12)
5. Develop (20-24)
6. Test (42-44) - MANDATORY
7. Document (70) - MANDATORY
8. Save to memory (71) - MANDATORY
9. Deploy (50)

================================================================================
MODULE INDEX - v9.0.0
================================================================================

AI-FIRST MODULES (01-06) - READ THESE FIRST!
────────────────────────────────────────────────────────────────────────────
01: MEMORY MANAGEMENT - AI memory and context retention (95%+ retention)
02: MCP - Model Context Protocol integration (7 servers)
03: MCP INTEGRATION - MCP integration layer and orchestration
04: THINKING FRAMEWORK - Systematic thinking and problem solving
05: CONTEXT ENGINEERING - Context awareness and learning system
06: TASK AI - Intelligent task management and automation

CORE WORKFLOW MODULES (10-12)
────────────────────────────────────────────────────────────────────────────
10: REQUIREMENTS - Requirements gathering and analysis
11: ANALYSIS - System analysis and design
12: PLANNING - Project planning and management

DEVELOPMENT MODULES (20-24)
────────────────────────────────────────────────────────────────────────────
20: BACKEND - Backend development guidelines
21: FRONTEND - Frontend development guidelines (with UI/UX fixes)
22: DATABASE - Database design and management
23: API - API design and implementation
24: BLUEPRINT - Blueprint patterns and templates

SECURITY MODULES (30-31)
────────────────────────────────────────────────────────────────────────────
30: SECURITY - Security best practices
31: AUTHENTICATION - Authentication and authorization

QUALITY MODULES (40-41)
────────────────────────────────────────────────────────────────────────────
40: QUALITY - Code quality and standards
41: TESTING - Testing strategies and practices (unit, integration)

TESTING MODULES (42-44) - NEW IN v9.0.0!
────────────────────────────────────────────────────────────────────────────
42: E2E TESTING - End-to-end testing with Playwright/Cypress
43: UI/UX TESTING - Frontend testing, icons, colors, styles
44: DATABASE TESTING - Database integrity, relationships, queries

DEPLOYMENT MODULE (50)
────────────────────────────────────────────────────────────────────────────
50: DEPLOYMENT - Deployment and DevOps

TEMPLATES MODULE (60)
────────────────────────────────────────────────────────────────────────────
60: TEMPLATES - Project templates and boilerplates

DOCUMENTATION MODULES (70-72) - NEW IN v9.0.0!
────────────────────────────────────────────────────────────────────────────
70: DOCUMENTATION - Code documentation, API docs, user guides
71: MEMORY SAVE - Save progress, decisions, learnings to memory
72: DOCS FOLDER - /docs folder structure and maintenance

================================================================================
WHY THIS ORDER?
================================================================================

The v9.0.0 order ensures complete development lifecycle:

1. MEMORY (01) - AI learns to remember from the start
2. MCP (02-03) - AI knows available tools immediately (7 servers)
3. THINKING (04-06) - AI learns how to think systematically
4. WORKFLOW (10-12) - AI applies thinking to requirements
5. DEVELOPMENT (20-24) - AI builds with full context
6. SECURITY (30-31) - AI ensures security throughout
7. QUALITY (40-41) - AI maintains high standards
8. TESTING (42-44) - AI tests everything thoroughly
9. DEPLOYMENT (50) - AI deploys correctly
10. TEMPLATES (60) - AI uses proven patterns
11. DOCUMENTATION (70-72) - AI documents and saves everything

================================================================================
MCP SERVERS AVAILABLE (7 SERVERS)
================================================================================

1. autonomous-builder - Multi-agent project builder
2. sequential-thinking - Logical reasoning and problem solving
3. chrome-devtools - Browser debugging and testing
4. sentry - Error monitoring and tracking
5. cloudflare - D1, R2, KV storage
6. playwright - Browser automation and E2E testing
7. serena - Semantic code search and refactoring

USAGE:
────────────────────────────────────────────────────────────────────────────
manus-mcp-cli tool list --server <server_name>
manus-mcp-cli tool call <tool_name> --server <server_name> --input '<json>'

================================================================================
TESTING REQUIREMENTS (MANDATORY)
================================================================================

AFTER EVERY DEVELOPMENT PHASE:
────────────────────────────────────────────────────────────────────────────
1. Unit Tests (41) - Test individual functions
2. Integration Tests (41) - Test component interactions
3. E2E Tests (42) - Test complete user flows
4. UI/UX Tests (43) - Test frontend rendering, icons, colors
5. Database Tests (44) - Test schema, relationships, queries

COMMON UI/UX ISSUES TO FIX:
────────────────────────────────────────────────────────────────────────────
✗ Icons not displaying
✗ Colors not applying
✗ CSS not loading
✗ Images not showing
✗ Fonts not rendering
✗ Responsive issues
✗ Import errors

ALWAYS CHECK:
────────────────────────────────────────────────────────────────────────────
✓ All imports are correct
✓ Static files are served properly
✓ CSS/JS files are linked correctly
✓ Icon libraries are loaded
✓ Color variables are defined
✓ Images paths are correct
✓ Fonts are loaded

================================================================================
DOCUMENTATION REQUIREMENTS (MANDATORY)
================================================================================

AFTER EVERY DEVELOPMENT PHASE:
────────────────────────────────────────────────────────────────────────────
1. Code Documentation (70) - Docstrings, comments
2. API Documentation (70) - Endpoints, parameters, responses
3. User Guide (70) - How to use the system
4. /docs Folder (72) - Architecture, design decisions
5. README.md - Project overview, setup, usage

ALWAYS DOCUMENT:
────────────────────────────────────────────────────────────────────────────
✓ What the code does
✓ Why decisions were made
✓ How to use it
✓ Examples
✓ Edge cases
✓ Known issues
✓ Future improvements

================================================================================
MEMORY SAVE REQUIREMENTS (MANDATORY)
================================================================================

AFTER EVERY SIGNIFICANT ACTION:
────────────────────────────────────────────────────────────────────────────
1. Save context (01, 71)
2. Save decisions and rationale (71)
3. Save learnings from errors (71)
4. Save progress checkpoints (71)
5. Update session information (71)

WHAT TO SAVE:
────────────────────────────────────────────────────────────────────────────
✓ Requirements understood
✓ Design decisions made
✓ Code written
✓ Tests created
✓ Bugs fixed
✓ Documentation updated
✓ Lessons learned

MEMORY LOCATION:
────────────────────────────────────────────────────────────────────────────
~/.global/memory/<project_name>/

FILES TO CREATE:
────────────────────────────────────────────────────────────────────────────
- project_summary.json
- development_log.md
- decisions.md
- learnings.md
- checkpoints/checkpoint_<timestamp>.json
- sessions/session_<timestamp>.json

================================================================================
QUALITY GATES (MUST PASS)
================================================================================

BEFORE COMMITTING CODE:
────────────────────────────────────────────────────────────────────────────
✓ All unit tests pass (41)
✓ All integration tests pass (41)
✓ All E2E tests pass (42)
✓ UI/UX renders correctly (43)
✓ Database integrity validated (44)
✓ Code quality checks pass (40)
✓ Security scan passes (30)
✓ Documentation updated (70)
✓ Progress saved to memory (71)

BEFORE DEPLOYING:
────────────────────────────────────────────────────────────────────────────
✓ All quality gates passed
✓ Performance tests pass
✓ Load tests pass
✓ Security audit complete
✓ Documentation complete
✓ Rollback plan ready

================================================================================
COMMON ISSUES AND FIXES
================================================================================

ISSUE: Icons not displaying
FIX: Check icon library import, verify CDN links, check CSS classes

ISSUE: Colors not applying
FIX: Check CSS variables, verify color definitions, check specificity

ISSUE: CSS not loading
FIX: Check file paths, verify static file serving, check link tags

ISSUE: Import errors
FIX: Check file paths, verify module names, check __init__.py

ISSUE: Database relationships broken
FIX: Check foreign keys, verify cascade rules, test queries

ISSUE: Tests failing
FIX: Check test data, verify mocks, check async handling

================================================================================
BEST PRACTICES
================================================================================

DEVELOPMENT:
────────────────────────────────────────────────────────────────────────────
✓ Write tests BEFORE code (TDD)
✓ Document WHILE coding
✓ Save to memory AFTER each phase
✓ Use MCP tools when available
✓ Think systematically (module 04)
✓ Follow security best practices (30-31)
✓ Maintain code quality (40)

TESTING:
────────────────────────────────────────────────────────────────────────────
✓ Test early, test often
✓ Test all user flows (E2E)
✓ Test edge cases
✓ Test error handling
✓ Test UI/UX thoroughly
✓ Test database integrity
✓ Automate everything

DOCUMENTATION:
────────────────────────────────────────────────────────────────────────────
✓ Write for humans, not machines
✓ Include examples
✓ Keep it updated
✓ Explain WHY, not just WHAT
✓ Document decisions
✓ Document known issues

================================================================================
VERSION HISTORY
================================================================================

v9.0.0 (2025-11-07):
- Added comprehensive testing modules (42-44)
- Added documentation and memory modules (70-72)
- Enhanced MCP integration (7 servers)
- Added UI/UX testing and fixes
- Added database testing and validation
- Made testing, documentation, and memory save MANDATORY

v8.0.0 (2025-11-04):
- Reordered modules to prioritize AI capabilities
- Added AI-First modules (01-06)
- Enhanced memory management
- Added MCP integration

v7.0.0 and earlier:
- Legacy versions with traditional ordering

================================================================================
QUICK REFERENCE
================================================================================

START NEW PROJECT:
────────────────────────────────────────────────────────────────────────────
1. Read modules 01-06
2. Gather requirements (10)
3. Analyze (11)
4. Plan (12)
5. Develop (20-24)
6. Test (42-44)
7. Document (70)
8. Save (71)
9. Deploy (50)

FIX BUG:
────────────────────────────────────────────────────────────────────────────
1. Load context (01, 71)
2. Understand issue (04, 05)
3. Write failing test (42-44)
4. Fix code
5. Verify test passes
6. Document fix (70)
7. Save learning (71)

ADD FEATURE:
────────────────────────────────────────────────────────────────────────────
1. Load context (01, 71)
2. Understand requirement (10)
3. Design (11)
4. Write tests (42-44)
5. Implement (20-24)
6. Verify tests pass
7. Document (70)
8. Save progress (71)

================================================================================
REMEMBER: Test, Document, Save - ALWAYS!
================================================================================

