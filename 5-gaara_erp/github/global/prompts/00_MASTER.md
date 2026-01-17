# MASTER PROMPT INDEX

**FILE**: github/global/prompts/00_MASTER.md | **PURPOSE**: Master blueprint for all prompts | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

This is the master index for all prompts in the Global Guidelines system. Each prompt corresponds to a specific phase or task in the autonomous development workflow.

## How to Use This File

1. **Identify Your Current Phase**: Determine which phase of the 7-phase workflow you are in
2. **Select the Appropriate Prompt**: Find the prompt file that matches your current task
3. **Execute the Prompt**: Follow the instructions in the selected prompt file exactly
4. **Log Your Actions**: Record all actions in `logs/info.log` and `system_log.md`
5. **Move to Next Phase**: Upon completion, proceed to the next phase automatically

## The 7 Autonomous Phases

### Phase 1: Initialization & Analysis (Existing Projects)
- **Prompt**: `11_analysis.md`
- **Purpose**: Analyze existing codebase and generate project maps
- **Output**: `docs/PROJECT_MAPS.md`, analysis report

### Phase 2: Initialization (New Projects)
- **Prompt**: `10_requirements.md`
- **Purpose**: Define project scope and requirements
- **Output**: Requirements document, initial task list

### Phase 3: Planning
- **Prompt**: `12_planning.md`
- **Purpose**: Create detailed execution plan
- **Output**: `docs/Task_List.md` with all tasks

### Phase 4: Code Implementation
- **Prompts**: `20_backend.md`, `21_frontend.md`, `22_database.md`, `23_api.md`
- **Purpose**: Write production-ready code
- **Output**: Source code, unit tests

### Phase 5: Review & Refinement
- **Prompts**: `30_security.md`, `40_quality.md`
- **Purpose**: Automated code review and security scanning
- **Output**: Refined code, security report

### Phase 6: Testing
- **Prompts**: `41_testing.md`, `42_e2e_testing.md`, `43_ui_ux_testing.md`, `44_database_testing.md`
- **Purpose**: Comprehensive testing (unit, integration, E2E)
- **Output**: Test suites, coverage reports (≥80%)

### Phase 7: Finalization & Documentation
- **Prompts**: `70_documentation.md`, `72_docs_folder.md`
- **Purpose**: Generate and update all documentation
- **Output**: All 21 required documentation files

## Supporting Prompts

### Memory & Context
- `01_memory_management.md` - Memory system usage
- `71_memory_save.md` - Saving to memory and knowledge base

### Code Analysis
- `13_path_and_import_tracing.md` - Path and import analysis/fixing

### Logging
- `73_structured_logging.md` - Structured JSON logging

### Templates
- `60_templates.md` - Code templates and examples

## Priority Order

Always consult `00_PRIORITY_ORDER.md` before executing any task to ensure compliance with critical rules.

## Execution Flow

```
Start → Read MASTER → Identify Phase → Select Prompt → Execute → Log → Verify → Next Phase
```

## Mandatory Pre-Execution Check

Before executing any prompt:
1. Read `rules/00_PRIORITY_ORDER.md`
2. Read `docs/00_PRIORITY_ORDER.md`
3. Verify compliance with all critical rules
4. Proceed with execution

---

**Next Steps**: 
1. Identify your current phase
2. Open the corresponding prompt file
3. Execute the instructions
4. Log all actions
5. Move to the next phase upon completion

