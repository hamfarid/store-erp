# PROMPT PRIORITY ORDER

**FILE**: github/global/prompts/00_PRIORITY_ORDER.md | **PURPOSE**: Priority order for all prompts | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Critical Priority (P0) - Must Execute First

These prompts contain critical constraints that must be followed at all times:

1. **00_MASTER.md** - Master blueprint, read first
2. **01_memory_management.md** - Memory system (mandatory for context retention)
3. **73_structured_logging.md** - Logging system (mandatory for all actions)

## High Priority (P1) - Phase-Specific

Execute these based on your current phase:

### Analysis Phase
4. **11_analysis.md** - Existing project analysis
5. **13_path_and_import_tracing.md** - Path/import analysis

### Planning Phase
6. **10_requirements.md** - Requirements gathering
7. **12_planning.md** - Detailed planning

### Implementation Phase
8. **20_backend.md** - Backend development
9. **21_frontend.md** - Frontend development
10. **22_database.md** - Database design
11. **23_api.md** - API development

### Review Phase
12. **30_security.md** - Security scanning
13. **40_quality.md** - Code quality review

### Testing Phase
14. **41_testing.md** - Unit testing
15. **42_e2e_testing.md** - E2E testing
16. **43_ui_ux_testing.md** - UI/UX testing
17. **44_database_testing.md** - Database testing

### Documentation Phase
18. **70_documentation.md** - Documentation generation
19. **72_docs_folder.md** - Docs folder structure

## Medium Priority (P2) - Supporting

20. **60_templates.md** - Code templates
21. **71_memory_save.md** - Memory saving guidelines

## Execution Rules

1. **Always start with P0 prompts** - These are mandatory for every task
2. **Follow phase order** - Execute P1 prompts in the order of the 7-phase workflow
3. **Consult rules first** - Before executing any prompt, read `rules/00_PRIORITY_ORDER.md`
4. **Log everything** - Use `73_structured_logging.md` for all logging
5. **Maintain context** - Use `01_memory_management.md` for context retention

## Cross-References

- **Rules**: See `rules/00_PRIORITY_ORDER.md` for hard constraints
- **Docs**: See `docs/00_PRIORITY_ORDER.md` for documentation priorities
- **Master**: See `00_MASTER.md` for the complete workflow

## Mandatory Pre-Execution Checklist

Before executing any prompt:
- [ ] Read `rules/00_PRIORITY_ORDER.md`
- [ ] Read `docs/00_PRIORITY_ORDER.md`
- [ ] Verify compliance with OSF Framework
- [ ] Check memory system is active
- [ ] Verify logging is configured
- [ ] Proceed with execution

---

**Remember**: Priority order ensures quality, security, and completeness. Never skip P0 prompts.

