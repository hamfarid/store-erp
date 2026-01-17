# Workflows

**FILE**: github/global/workflows/README.md | **PURPOSE**: Workflows documentation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

The `workflows/` directory contains multi-step workflows for repeatable processes.

## Purpose

Workflows are **automated sequences** of tasks that:
- Execute multiple steps in order
- Handle dependencies between steps
- Provide rollback capabilities
- Log all actions
- Can be triggered by commands

## Structure

```
workflows/
├── release_workflow.md
├── deployment_workflow.md
├── security_audit_workflow.md
├── database_migration_workflow.md
└── README.md
```

## Workflow Format

Each workflow file should follow this format:

```markdown
# [Workflow Name]

**FILE**: workflows/[name].md | **PURPOSE**: [Description] | **OWNER**: [Team] | **LAST-AUDITED**: [Date]

## Overview

[Brief description of what this workflow does]

## Trigger

**Command**: `execute-task [workflow-name]`

**When to use**: [Scenarios when this workflow should be run]

## Prerequisites

- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Steps

### Step 1: [Name]

**Purpose**: [What this step does]

**Actions**:
1. [Action 1]
2. [Action 2]

**Verification**:
- [ ] [Check 1]
- [ ] [Check 2]

**Rollback** (if step fails):
1. [Rollback action 1]
2. [Rollback action 2]

### Step 2: [Name]

[Same format]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Rollback Procedure

If the workflow fails at any step:
1. [Rollback step 1]
2. [Rollback step 2]

## Logging

All actions are logged to:
- `logs/info.log`
- `.memory/checkpoints/workflow_[name]_[date].md`

## Example

```bash
# Execute the workflow
execute-task release-workflow

# Expected output
[Description of expected output]
```
```

## Example Workflows

### 1. Release Workflow

**Purpose**: Prepare and publish a new release

**Steps**:
1. Run all tests
2. Update version numbers
3. Generate changelog
4. Create Git tag
5. Build artifacts
6. Publish to registry

### 2. Deployment Workflow

**Purpose**: Deploy to production

**Steps**:
1. Backup database
2. Run migrations
3. Build Docker images
4. Deploy to Kubernetes
5. Run smoke tests
6. Monitor for errors

### 3. Security Audit Workflow

**Purpose**: Comprehensive security audit

**Steps**:
1. Run SAST tools
2. Run DAST tools
3. Scan dependencies
4. Check for secrets
5. Generate report
6. Create remediation tasks

### 4. Database Migration Workflow

**Purpose**: Safely migrate database schema

**Steps**:
1. Backup database
2. Test migration in staging
3. Run migration in production
4. Verify data integrity
5. Update documentation

## Usage

### Execute a Workflow

```bash
# From the AI agent
execute-task release-workflow
```

### Create a New Workflow

1. Copy the template above
2. Fill in all sections
3. Test the workflow
4. Document in this README

## Best Practices

1. **Idempotent**: Workflows should be safe to run multiple times
2. **Atomic**: Each step should be atomic (all or nothing)
3. **Reversible**: Provide rollback for each step
4. **Logged**: Log all actions and outcomes
5. **Verified**: Include verification checks
6. **Documented**: Clear documentation for each step

## Monitoring

All workflows are monitored:
- Start time logged
- Each step logged
- End time logged
- Success/failure logged
- Errors logged with stack traces

## Error Handling

If a workflow fails:
1. Log the error
2. Execute rollback procedure
3. Notify user
4. Create error report in `errors/`
5. Update `docs/fix_this_error.md`

---

**This directory should never be empty. Define workflows for all repeatable processes.**

