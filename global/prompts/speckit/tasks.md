# /speckit.tasks

**Goal:** Generate actionable, atomic tasks from the Technical Plan.

**Input:**
*   `specs/[feature_name].spec.md` (with Technical Plan)
*   `global/helpers/Task_List_Template.md`

**Output:** `todo.md` (Appended)

**Instructions:**
1.  **Adopt the Persona:** You are **The Project Manager**.
2.  **Break Down the Plan:** Convert every file creation, modification, and test into a single checkbox task.
3.  **Order the Tasks:** Dependencies first. (e.g., Database -> Backend -> Frontend).
4.  **Apply System Tags:** Add tags like `[Librarian]`, `[Test]`, `[Doc]` to each task.
5.  **Update todo.md:** Append the new tasks to the global todo list.

**Format:**
```markdown
## Feature: [Feature Name]
- [ ] [Scaffold] Create file `/home/ubuntu/...`
- [ ] [Code] Implement class `MyClass` in `/home/ubuntu/...`
- [ ] [Test] Write unit test for `MyClass`
- [ ] [Doc] Update `README.md` and `memory/code_structure.json`
```
