# MEMORY MANAGEMENT SYSTEM

**FILE**: github/global/prompts/01_memory_management.md | **PURPOSE**: Memory system usage guidelines | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

The `.memory/` directory is your working memory. It maintains context across sessions and prevents hallucination through systematic context retention.

## Memory Structure

```
.memory/
├── conversations/     # All user interactions
├── decisions/         # Significant decisions with OSF analysis
├── checkpoints/       # Project state snapshots
├── context/          # Current task context
└── learnings/        # Lessons learned
```

## Mandatory 10-Minute Context Refresh

**CRITICAL**: You must perform this refresh every 10 minutes to prevent context loss.

### Refresh Procedure

1. **Save Current State**
   ```
   Save current work to .memory/context/current_state.md
   ```

2. **Re-read Core Files**
   - `github/global/GLOBAL_PROFESSIONAL_CORE_PROMPT.md`
   - Your role file from `roles/`
   - Current task prompt from `prompts/`

3. **Consult Log**
   - Review last 20 entries in `logs/info.log`

4. **Verify Plan**
   - Check current action against `docs/Task_List.md`

5. **Resume**
   - Continue work with refreshed context

## Memory Usage Guidelines

### 1. Conversations (.memory/conversations/)

**When**: After every user interaction

**Format**: `conversation_YYYY-MM-DD_HHmmss.md`

**Content**:
```markdown
# Conversation: [Brief Title]

**Date**: 2025-11-18T14:30:00Z
**User Request**: [Original request]
**AI Response**: [Summary of response]
**Actions Taken**: [List of actions]
**Outcome**: [Result]
**Next Steps**: [What's next]
```

### 2. Decisions (.memory/decisions/)

**When**: After any significant decision requiring OSF analysis

**Format**: `decision_YYYY-MM-DD_[topic].md`

**Content**:
```markdown
# Decision: [Topic]

**Date**: 2025-11-18T14:30:00Z
**Context**: [Why this decision was needed]

## Options Analyzed

### Option 1: [Name]
- **Description**: [Details]
- **OSF Score**: 0.XX
  - Security: X.X
  - Correctness: X.X
  - Reliability: X.X
  - Maintainability: X.X
  - Performance: X.X
  - Usability: X.X
  - Scalability: X.X
- **Pros**: [List]
- **Cons**: [List]

### Option 2: [Name]
[Same structure]

## Final Decision

**Chosen**: Option X
**Rationale**: [Why this option was chosen]
**Logged In**: docs/Solution_Tradeoff_Log.md
```

### 3. Checkpoints (.memory/checkpoints/)

**When**: At the end of each phase

**Format**: `checkpoint_phase_X_YYYY-MM-DD.md`

**Content**:
```markdown
# Checkpoint: Phase X - [Phase Name]

**Date**: 2025-11-18T14:30:00Z
**Phase**: X of 7
**Status**: Complete/In Progress

## Completed Tasks
- [Task 1]
- [Task 2]

## Current State
- **Files Created**: [Count]
- **Tests Written**: [Count]
- **Coverage**: XX%
- **Issues**: [Count]

## Next Phase
- **Phase**: X+1
- **First Task**: [Description]
```

### 4. Context (.memory/context/)

**When**: Continuously updated

**File**: `current_task.md`

**Content**:
```markdown
# Current Task Context

**Last Updated**: 2025-11-18T14:30:00Z
**Phase**: X of 7
**Current Task**: [Description]

## What I'm Doing
[Current action]

## Why I'm Doing It
[Rationale]

## What I've Done So Far
- [Action 1]
- [Action 2]

## What's Next
- [Next action]

## Blockers
- [Any issues]
```

### 5. Learnings (.memory/learnings/)

**When**: After resolving errors or discovering best practices

**Format**: `learning_YYYY-MM-DD_[topic].md`

**Content**:
```markdown
# Learning: [Topic]

**Date**: 2025-11-18T14:30:00Z
**Category**: Error Resolution / Best Practice / Optimization

## Situation
[What happened]

## Problem
[What went wrong or what was discovered]

## Solution
[How it was fixed or what was learned]

## Prevention
[How to avoid this in the future]

## Related Files
- [File paths]
```

## Automation

All memory operations should be automated:

```python
# Example: Auto-save conversation
def save_conversation(user_request, ai_response, actions, outcome):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f".memory/conversations/conversation_{timestamp}.md"
    # ... save content
```

## Integration with Logging

Memory and logs work together:
- **Logs**: Detailed, structured, queryable records
- **Memory**: High-level context and decisions

Always log to both systems.

---

**Next Steps**: 
1. Create `.memory/` directory structure
2. Implement auto-save functions
3. Set up 10-minute refresh timer
4. Begin using memory system for all tasks

