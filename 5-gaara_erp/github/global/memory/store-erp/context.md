# Store ERP - Project Context

**Project Name:** Store ERP  
**Type:** Enterprise Resource Planning System  
**Status:** Active Development  
**Version:** Using GLOBAL_GUIDELINES v10.2.0  
**Initialized:** November 5, 2025

---

## Project Overview

Store ERP is an existing Enterprise Resource Planning system designed for comprehensive business management.

### Technology Stack

**Backend:**
- Framework: Flask (Python)
- Database (Production): PostgreSQL
- Database (Development): SQLite
- ORM: SQLAlchemy
- Migrations: Alembic

**Architecture:**
- RESTful API
- Microservices-ready
- AI-First approach

---

## Current Status

### Phase Progress

**Phase 0 (Preparation):** ✅ Complete  
**Phase 1 (Requirements & Analysis):** 🔄 In Progress  
**Phase 2 (Planning & Design):** ✅ Complete

**Documentation Coverage:** 67%

### Completed Tasks

- ✅ **T7:** RAG Governance implementation complete

### In Progress

**Phase 1 Tasks:**
- 🔄 Requirements gathering
- 🔄 System analysis
- 🔄 Documentation updates

### Next Tasks

**Phase 1 Remaining:**
- ⏳ **T8:** Circuit Breaker pattern implementation
- ⏳ **T9:** OpenAPI specification
- ⏳ **T10:** API drift tests

---

## Environment Separation

### Helper Tools (AI Assistant)
```
Location: C:\Users\hadym\.global\
├── memory\store-erp\      # Project-specific memory
└── mcp\store-erp\         # Project-specific MCP
```

### User Project
```
Location: D:\APPS_AI\store\Store\
├── backend\               # Flask application
├── database\              # Database files
├── migrations\            # Alembic migrations
└── tests\                 # Test suite
```

**CRITICAL:** Never mix helper tools with user project!

---

## AI-First Modules

The following modules from GLOBAL_GUIDELINES are loaded and active:

1. **Module 01:** Memory Management (Prompt 60)
2. **Module 02:** MCP (Prompt 15)
3. **Module 03:** MCP Integration (Prompt 16)
4. **Module 04:** Thinking Framework (Prompt 17)
5. **Module 05:** Context Engineering (Prompt 19)
6. **Module 06:** Task AI (Prompt 18)

**Total Prompts Available:** 21 (from global/prompts)

---

## MCP Integration

### Active MCP Servers

**Sentry MCP:**
- Organization: gaara-group
- Status: Active
- Purpose: Error monitoring and performance tracking

### Available MCP Tools
- Cloudflare (D1, R2, KV, Workers)
- Playwright (Browser automation)
- Sentry (Error monitoring)
- Serena (Semantic code retrieval)

---

## Guidelines & Standards

### Core Principles

**Philosophy:**
> "Always choose the BEST solution, not the easiest."

**Quality Standards:**
- Code: Clean, readable, well-documented
- Testing: 80%+ coverage (100% for critical paths)
- Documentation: Complete and accurate
- Architecture: Scalable and maintainable

### Workflow

1. **Initialize:** Memory + MCP for project
2. **Understand:** Read requirements fully
3. **Plan:** Design before coding
4. **Build:** Implement with quality
5. **Test:** Verify thoroughly (80%+ coverage)
6. **Document:** Explain clearly
7. **Deliver:** High-quality results

---

## Project History

### Version History

- **v8.0.0:** Using GLOBAL_GUIDELINES_UNIFIED_v8.0.0
- **v10.2.0:** Migrated to project-specific Memory/MCP structure

### Key Decisions

See `decisions.md` for architectural decisions and rationale.

---

## Next Steps

### Immediate (Phase 1)

1. Complete T8 (Circuit Breaker)
2. Complete T9 (OpenAPI)
3. Complete T10 (API drift tests)
4. Increase documentation to 80%+

### Upcoming (Phase 3+)

- Implementation of remaining features
- Integration testing
- Performance optimization
- Deployment preparation

---

## Notes

- This is an **existing** ERP system (not a new project)
- Separate from any e-commerce platform requests
- Using Flask (not Node.js/Express)
- Production database is PostgreSQL

---

**Last Updated:** November 5, 2025  
**Memory Location:** `C:\Users\hadym\.global\memory\store-erp\context.md`

