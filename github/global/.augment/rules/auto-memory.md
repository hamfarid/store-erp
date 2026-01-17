---
type: agent_requested
description: Memory management and context retention guidelines
---

# Memory System

## Use Memory When

- ✅ Starting a new task or project
- ✅ Making an important decision
- ✅ Switching between project phases
- ✅ Encountering an error or challenge
- ✅ Finding a solution to a problem
- ✅ Completing a milestone
- ✅ Learning something new about the codebase
- ✅ User provides important information

## Don't Use Memory When

- ❌ Performing simple calculations
- ❌ Answering one-time questions
- ❌ Handling temporary information
- ❌ Processing transient data

## Memory Location

**Project-Specific Structure:**

```
YOUR memory (helper tool):
  ~/.global/memory/[project-name]/

Example:
  ~/.global/memory/store-erp/
  ~/.global/memory/gaara-erp-v12/
  ~/.global/memory/personal-site/

NOT in user's project:
  ~/user-project/  ❌
```

**Each project has its own memory directory to prevent mixing!**

## What to Save

### Project Context
- Project name and type
- Technologies used
- Architecture decisions
- Key requirements

### Decisions
- What was decided
- Why it was decided
- Alternatives considered
- Trade-offs accepted

### Challenges & Solutions
- Problem encountered
- Solutions attempted
- What worked
- Lessons learned

### Milestones
- Phase completions
- Feature completions
- Deployment events
- Important updates

## How to Use

```
1. Initialize Memory for project:
   "Initialize Memory for project: [project-name]"

2. Identify important information

3. Save to memory:
   "Save to memory: [information]"
   → Saves to ~/.global/memory/[project-name]/

4. Recall from memory:
   "What did we decide about [topic]?"
   → Reads from ~/.global/memory/[project-name]/

5. Switch projects:
   "Switch to project: [another-project]"
   → Changes to ~/.global/memory/[another-project]/
```

## Memory Hierarchy

1. **Critical:** Always remember (project context, key decisions)
2. **Important:** Remember for current phase (current work, recent decisions)
3. **Reference:** Remember for lookup (past solutions, patterns)

## Best Practices

- Save early and often
- Use clear, descriptive titles
- Include context and rationale
- Link related memories
- Review periodically
- Update when needed

## Project-Specific Files

**Each project directory contains:**
```
~/.global/memory/[project-name]/
├── decisions.md         # Architectural decisions
├── architecture.md      # System design
├── preferences.md       # User preferences
└── context.md           # General context
```

## Critical Rules

- ❌ NEVER mix projects in the same directory
- ✅ ALWAYS use project-specific subdirectories
- ✅ ALWAYS specify project name when initializing
- ✅ Each project has completely separate memory

## Remember

Memory is YOUR helper tool. It helps YOU work better. It's not part of the user's project.

**Each project has its own memory to prevent mixing!**

