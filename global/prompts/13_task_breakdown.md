# Task Breakdown Prompt

## Purpose
Break down complex features into manageable tasks.

## Instructions
1. Read feature requirements
2. Identify all components (frontend, backend, database, tests)
3. Create step-by-step tasks in docs/Task_List.md
4. Estimate complexity for each task
5. Identify dependencies between tasks
6. Log breakdown to system_log.md

## Task Format
```markdown
- [ ] Task name (Complexity: Low/Medium/High)
  - Dependencies: [task_ids]
  - Components: frontend/backend/database/tests
  - Estimated time: X hours
```

## Output
- Updated Task_List.md
- Dependency graph
