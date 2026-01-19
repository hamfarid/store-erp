# User Commands

This document outlines the commands you can use to interact with the autonomous AI development system.

---

## 🚀 Starting a Project

You only need to provide **one** of the following commands to initiate the entire autonomous workflow. The AI agent will take over from there and complete the project to 95%+ automatically.

### 1. Start a New Project

Use this command to build a completely new software project from scratch.

**Command:**
```
start-new-project
```

**What it does:**
1.  The AI agent will ask for the project requirements.
2.  It will then initiate the 7-phase autonomous workflow, starting with **Phase 2: Initialization**.
3.  The agent will automatically plan, code, test, and document the entire project.

### 2. Analyze an Existing Project

Use this command to analyze, improve, or add features to an existing codebase.

**Command:**
```
analyze-existing-project
```

**What it does:**
1.  The AI agent will ask for the path to the existing project.
2.  It will initiate the 7-phase autonomous workflow, starting with **Phase 1: Initialization & Analysis**.
3.  The agent will automatically analyze the code, create project maps, identify areas for improvement, and then proceed with planning, coding, and testing.

### 3. Execute a Specific Workflow

Use this command to run a predefined, complex task from the `workflows/` directory.

**Command:**
```
execute-task <workflow_name>
```

**Example:**
```
execute-task release-v2.0
```

**What it does:**
1.  The AI agent will look for a corresponding file in the `workflows/` directory (e.g., `release-v2.0.md`).
2.  It will execute the multi-step process defined in that workflow file.
3.  This is useful for standardized, repeatable tasks like creating a new release, running a full security audit, or onboarding a new developer.

---

## 🤖 What Happens Next?

After you issue one of these commands, the AI agent becomes fully autonomous. You do not need to provide any further instructions unless the agent explicitly asks for input.

The agent will:
-   **Log every action** in `system_log.md`.
-   **Follow all principles** defined in the `GLOBAL_PROFESSIONAL_CORE_PROMPT.md`.
-   **Complete all 7 phases** of the development lifecycle automatically.
-   **Aim for 95%+ completion** without human intervention.

You can monitor the agent's progress by viewing the `system_log.md` and the files being created and modified in the project directory.

