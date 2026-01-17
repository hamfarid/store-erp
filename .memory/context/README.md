# 🎯 Context Memory

This directory stores the current working context, enabling seamless continuation across sessions and maintaining focus on active tasks.

## Purpose

The Context Memory system preserves the immediate working state, enabling:
- **Session Continuity** - Resume work exactly where you left off
- **Focus Maintenance** - Keep track of current task and subtasks
- **Context Switching** - Easily switch between multiple contexts
- **Progress Tracking** - Monitor real-time progress on current work
- **Collaboration** - Share current context with team members

## Structure

```
context/
├── README.md                    # This file
├── current_task.md              # Current active task
├── current_phase.md             # Current phase details
├── current_session.md           # Current session information
├── active_files.md              # Files currently being worked on
├── pending_actions.md           # Actions waiting to be completed
├── blockers.md                  # Current blockers and issues
└── notes.md                     # Temporary notes and reminders
```

## Context Files

### 1. current_task.md
**Purpose:** Track the immediate task being worked on

**Format:**
```markdown
# Current Task

**Task ID:** [From Task_List.md]  
**Task Name:** [Task name]  
**Phase:** [Phase number and name]  
**Status:** [Not Started/In Progress/Blocked/Complete]  
**Started:** YYYY-MM-DD HH:MM:SS  
**Estimated Completion:** YYYY-MM-DD HH:MM:SS

## Description
[What needs to be done]

## Subtasks
- [ ] Subtask 1
- [ ] Subtask 2
- [ ] Subtask 3

## Progress
[Current progress description]

## Next Steps
1. [Next step 1]
2. [Next step 2]

## Related
- **Previous Task:** [Link]
- **Next Task:** [Link]
- **Decisions:** [Links]
- **Files:** [Links]
```

---

### 2. current_phase.md
**Purpose:** Track the current phase and its progress

**Format:**
```markdown
# Current Phase

**Phase:** [Number] - [Name]  
**Status:** [In Progress]  
**Started:** YYYY-MM-DD  
**Target Completion:** YYYY-MM-DD  
**Progress:** [X%]

## Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Completed Tasks
- [x] Task 1
- [x] Task 2

## In Progress
- [ ] Task 3 (50%)
- [ ] Task 4 (20%)

## Pending
- [ ] Task 5
- [ ] Task 6

## Blockers
- [Blocker 1]
- [Blocker 2]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Related
- **Previous Phase:** [Link]
- **Next Phase:** [Link]
- **Checkpoint:** [Link]
```

---

### 3. current_session.md
**Purpose:** Track the current working session

**Format:**
```markdown
# Current Session

**Session ID:** sess_YYYYMMDD_HHMMSS  
**Started:** YYYY-MM-DD HH:MM:SS  
**Duration:** [X hours Y minutes]  
**User:** [User identifier]  
**Agent:** [Agent identifier]

## Session Goals
1. [Goal 1]
2. [Goal 2]

## Work Done
- [x] Action 1
- [x] Action 2
- [ ] Action 3 (in progress)

## Files Modified
- `path/to/file1.ext` (created)
- `path/to/file2.ext` (modified)

## Decisions Made
- [Decision 1]
- [Decision 2]

## Next Session
- [ ] Action to continue
- [ ] Action to start

## Notes
[Any notes for next session]
```

---

### 4. active_files.md
**Purpose:** Track files currently being worked on

**Format:**
```markdown
# Active Files

**Last Updated:** YYYY-MM-DD HH:MM:SS

## Files Being Modified

### File 1: path/to/file1.ext
**Status:** In Progress  
**Purpose:** [Why this file is being modified]  
**Changes:** [What changes are being made]  
**Progress:** [X%]

### File 2: path/to/file2.ext
**Status:** In Progress  
**Purpose:** [Why this file is being modified]  
**Changes:** [What changes are being made]  
**Progress:** [X%]

## Files Recently Completed

### File 3: path/to/file3.ext
**Status:** Complete  
**Completed:** YYYY-MM-DD HH:MM:SS  
**Changes:** [What was changed]

## Files Pending

### File 4: path/to/file4.ext
**Status:** Pending  
**Purpose:** [Why this file needs to be modified]  
**Planned Changes:** [What will be changed]
```

---

### 5. pending_actions.md
**Purpose:** Track actions waiting to be completed

**Format:**
```markdown
# Pending Actions

**Last Updated:** YYYY-MM-DD HH:MM:SS

## High Priority
- [ ] Action 1 (due: YYYY-MM-DD)
- [ ] Action 2 (due: YYYY-MM-DD)

## Medium Priority
- [ ] Action 3
- [ ] Action 4

## Low Priority
- [ ] Action 5
- [ ] Action 6

## Waiting On
- [ ] Action 7 (waiting on: user feedback)
- [ ] Action 8 (waiting on: external service)

## Completed Today
- [x] Action 9 (completed: HH:MM)
- [x] Action 10 (completed: HH:MM)
```

---

### 6. blockers.md
**Purpose:** Track current blockers and issues

**Format:**
```markdown
# Current Blockers

**Last Updated:** YYYY-MM-DD HH:MM:SS

## Critical Blockers 🔴
### Blocker 1
**Impact:** Critical  
**Description:** [What is blocked]  
**Reason:** [Why it's blocked]  
**Possible Solutions:**
1. [Solution 1]
2. [Solution 2]
**Status:** [Active/Investigating/Resolved]

## Medium Blockers 🟡
### Blocker 2
**Impact:** Medium  
**Description:** [What is blocked]  
**Reason:** [Why it's blocked]  
**Workaround:** [Temporary workaround if any]
**Status:** [Active/Investigating/Resolved]

## Resolved Blockers ✅
### Blocker 3
**Resolved:** YYYY-MM-DD HH:MM:SS  
**Solution:** [How it was resolved]
```

---

### 7. notes.md
**Purpose:** Temporary notes and reminders

**Format:**
```markdown
# Session Notes

**Date:** YYYY-MM-DD

## Quick Notes
- [Note 1]
- [Note 2]
- [Note 3]

## Reminders
- [ ] Remember to do X
- [ ] Don't forget Y

## Ideas
- [Idea 1]
- [Idea 2]

## Questions
- [Question 1]
- [Question 2]

## Links
- [Useful link 1]
- [Useful link 2]
```

---

## Usage Guidelines

### When to Update Context
- ✅ Start of each session
- ✅ When switching tasks
- ✅ When encountering blockers
- ✅ When completing tasks
- ✅ End of each session

### Context Refresh Frequency
- **current_task.md** - Every time task changes
- **current_phase.md** - Daily
- **current_session.md** - Start/end of session
- **active_files.md** - When files change
- **pending_actions.md** - Multiple times per day
- **blockers.md** - When blockers occur/resolve
- **notes.md** - As needed

### Context Cleanup
- **Daily** - Archive completed tasks
- **Weekly** - Clean up old notes
- **Monthly** - Review and update context structure

## Integration with Other Memories

Context links to:
- **Conversations** - Current conversation context
- **Decisions** - Decisions affecting current work
- **Checkpoints** - Context at checkpoint times
- **Learnings** - Learnings from current work

## Context Switching

When switching contexts (e.g., different projects):

1. **Save current context**
   ```bash
   cp context/current_task.md context/saved/task_project_a.md
   ```

2. **Load new context**
   ```bash
   cp context/saved/task_project_b.md context/current_task.md
   ```

3. **Document switch**
   ```markdown
   # Context Switch
   **From:** Project A - Task X
   **To:** Project B - Task Y
   **Reason:** [Why switching]
   **Return:** [When to return]
   ```

---

**Created:** 2025-12-13  
**Last Updated:** 2025-12-13  
**Maintained by:** AI Agent
