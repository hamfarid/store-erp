# Global Guidelines - Professional AI Development System

**Version**: 3.0.0  
**Status**: Production Ready  
**Last Updated**: 2025-11-18

## Overview

This is the **Global Guidelines** system - a comprehensive AI development prompt system that provides guidance for developing YOUR project. This is NOT your project; it's your instruction manual.

## Important Distinction

- **Global Guidelines** (`github/global/`): The prompts and tools that tell you HOW to work
- **Your Project**: The actual codebase you are building for the user

**NEVER confuse the two.** The `github/global/` directory is your instruction manual, not the user's application.

## System Structure

```
github/global/
├── prompts/           # Step-by-step instructions for each phase
├── roles/             # Agent role definitions
├── rules/             # Hard-coded, non-negotiable rules
├── docs/              # System documentation
├── .memory/           # AI agent's working memory
├── knowledge/         # Verified facts and solutions
├── examples/          # Working code examples
├── workflows/         # Multi-step automated workflows
├── logs/              # Structured JSON logs
├── errors/            # Error tracking and resolution
└── README.md          # This file
```

## Quick Start

### For AI Agents

1. **Read Core Prompt**: Start with `GLOBAL_PROFESSIONAL_CORE_PROMPT.md`
2. **Identify Your Role**: Read your role file from `roles/`
3. **Read Master Prompt**: Read `prompts/00_MASTER.md`
4. **Execute Workflow**: Follow the 7-phase autonomous workflow

### For Humans

1. **Understand the System**: Read this README
2. **Review Prompts**: Browse `prompts/` to see what the AI will do
3. **Check Rules**: Review `rules/` to understand constraints
4. **Give Commands**: Use commands from `USER_COMMANDS.md`

## The 7 Autonomous Phases

1. **Phase 1**: Initialization & Analysis (Existing Projects)
2. **Phase 2**: Initialization (New Projects)
3. **Phase 3**: Planning
4. **Phase 4**: Code Implementation
5. **Phase 5**: Review & Refinement
6. **Phase 6**: Testing
7. **Phase 7**: Finalization & Documentation

## Core Principles

### 1. OSF Framework (Optimal & Safe Over Easy/Fast)

```
OSF_Score = (0.35 × Security) + (0.20 × Correctness) + (0.15 × Reliability) + 
            (0.10 × Maintainability) + (0.08 × Performance) + 
            (0.07 × Usability) + (0.05 × Scalability)
```

**Always choose the option with the highest OSF_Score.**

### 2. Zero-Tolerance Constraints

1. ❌ No hardcoded secrets
2. ❌ No SQL injection
3. ❌ No XSS
4. ❌ No unhandled errors
5. ❌ No missing tests (<80% coverage)
6. ❌ No undocumented code
7. ❌ No duplicate code
8. ❌ No uncommitted changes

### 3. Mandatory Tools

- **MCP**: For research, thinking, and browser testing
- **Memory System**: For context retention
- **Structured Logging**: For all actions

## Key Features

### Autonomous Operation
- 95%+ project completion automatically
- Full 7-phase workflow execution
- Self-correction and refinement

### Quality Assurance
- Automated code reviews
- Security scanning
- Comprehensive testing (≥80% coverage)
- Performance optimization

### Documentation
- 21+ required documentation files
- Auto-generated API docs
- Decision logging with OSF analysis

### Context Retention
- 10-minute mandatory context refresh
- Memory system for long-term retention
- Structured logging for audit trail

## User Commands

### Start a New Project
```
start-new-project
```

### Analyze an Existing Project
```
analyze-existing-project
```

### Execute a Specific Task
```
execute-task <task_name>
```

See `USER_COMMANDS.md` for the full list.

## Directory Purposes

### prompts/
**Purpose**: Step-by-step instructions for each phase and task

**Key Files**:
- `00_MASTER.md` - Master blueprint
- `00_PRIORITY_ORDER.md` - Priority order for prompts
- `10_requirements.md` - Requirements gathering
- `11_analysis.md` - Project analysis
- `12_planning.md` - Detailed planning
- `20_backend.md` - Backend development
- `21_frontend.md` - Frontend development
- `30_security.md` - Security scanning
- `40_quality.md` - Code quality review
- `41_testing.md` - Testing guidelines
- `70_documentation.md` - Documentation generation
- `73_structured_logging.md` - Logging implementation

### roles/
**Purpose**: Define agent roles and responsibilities

**Key Files**:
- `lead_agent.md` - Lead software development agent
- `reviewer_agent.md` - Code review and QA agent

### rules/
**Purpose**: Hard-coded, non-negotiable rules

**Key Files**:
- `00_PRIORITY_ORDER.md` - Priority order for rules
- `security_rules.md` - Security rules (P0)
- `testing_rules.md` - Testing rules (P1)
- `code_quality.md` - Code quality rules (P1)

### .memory/
**Purpose**: AI agent's working memory

**Subdirectories**:
- `conversations/` - User interactions
- `decisions/` - OSF-analyzed decisions
- `checkpoints/` - Phase completion snapshots
- `context/` - Current task context
- `learnings/` - Lessons learned

### knowledge/
**Purpose**: Permanent knowledge base of verified solutions

**Categories**:
- Backend patterns
- Frontend patterns
- Security best practices
- Testing strategies
- DevOps techniques

### examples/
**Purpose**: Self-contained, working examples

**Categories**:
- Authentication examples
- API design examples
- Frontend component examples
- Testing examples
- Database examples

### workflows/
**Purpose**: Multi-step automated workflows

**Examples**:
- Release workflow
- Deployment workflow
- Security audit workflow
- Database migration workflow

### logs/
**Purpose**: Structured JSON logs

**Files**:
- `debug.log` - Verbose debugging
- `info.log` - General flow
- `warn.log` - Warnings
- `error.log` - Errors
- `fatal.log` - Fatal errors
- `background.log` - Background processes

### errors/
**Purpose**: Error tracking and resolution

**Subdirectories**:
- `critical/` - P0 errors
- `high/` - P1 errors
- `medium/` - P2 errors
- `low/` - P3 errors
- `resolved/` - Fixed errors

## Quality Standards

### Code Quality
- Linting: 0 errors
- Type coverage: 100%
- Cyclomatic complexity: <10
- Code duplication: <5%
- Documentation coverage: >80%

### Security
- No hardcoded secrets
- No SQL injection
- No XSS
- All inputs validated
- All errors handled

### Testing
- Unit test coverage: ≥80%
- Integration test coverage: ≥70%
- E2E test coverage: Critical paths 100%
- All tests passing

### Documentation
- All 21+ files present
- All files follow templates
- All files have proper headers
- All decisions documented

## Success Criteria

The system is successful when:
- ✅ 95%+ of tasks completed automatically
- ✅ All zero-tolerance constraints met
- ✅ All tests passing with ≥80% coverage
- ✅ All security scans clean
- ✅ All documentation complete and accurate
- ✅ Code is production-ready

## Version History

- **v1.8**: Initial release with OSF framework
- **v2.1**: Added KMS/Vault, OIDC, AWS Secrets
- **v2.3**: Added Resilience & Circuit Breakers
- **v2.6**: Expanded Frontend & Visual Design
- **v2.7**: Added Integration Guides
- **v2.8**: Added CI/CD Integration Guide
- **v3.0**: COMPLETE EDITION - Full expansion

## License

Proprietary

## Support

For issues and questions, refer to the documentation in each directory.

---

**Your Mission**: Build production-ready software with absolute precision and unwavering quality.

