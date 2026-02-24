# 🚦 Approval Gates Protocol (Jules-Style Escalation)

> **Purpose**: Define when an AI agent MUST stop and ask for human approval.
> **Inspiration**: Jules (Anthropic) Safety Protocol.

## 1. The Traffic Light System

### 🟢 Green Light (Autonomous Execution)
*   **Definition**: Low-risk, reversible actions.
*   **Examples**:
    *   Reading files.
    *   Running local tests.
    *   Writing to temporary directories.
    *   Generating documentation.
*   **Action**: Proceed without interruption.

### 🟡 Yellow Light (Notify & Proceed)
*   **Definition**: Medium-risk, potentially impactful actions.
*   **Examples**:
    *   Installing new dependencies.
    *   Modifying configuration files.
    *   Refactoring core logic.
    *   Creating new files in the main codebase.
*   **Action**: Log the intent clearly (`[INTENT] Installing package X...`) and proceed if no objection is raised within a short window (or proceed immediately if in async mode).

### 🔴 Red Light (Stop & Ask)
*   **Definition**: High-risk, irreversible, or sensitive actions.
*   **Examples**:
    *   **Deleting files**.
    *   **Committing to main branch**.
    *   **Deploying to production**.
    *   **Exposing ports/services to the internet**.
    *   **Accessing secrets/credentials**.
    *   **Sending emails or external messages**.
*   **Action**:
    1.  **STOP**.
    2.  Explain the risk.
    3.  Ask for explicit user confirmation (`y/n`).
    4.  Wait for approval.

## 2. Escalation Triggers

### 2.1 The "Two-Strike" Rule
*   If an autonomous task fails **twice** with the same error:
    *   **Escalate to Red Light**.
    *   Ask the user for guidance before trying a third time.

### 2.2 Ambiguity Detection
*   If a user request is vague (e.g., "Fix the code"):
    *   **Escalate to Red Light**.
    *   Ask for clarification ("Which file? What is the expected behavior?").

### 2.3 Resource Spikes
*   If a task requires > 50% of available tokens or disk space:
    *   **Escalate to Red Light**.
    *   Confirm resource usage with the user.

## 3. Implementation Guide

### For Agents (System Prompt)
```markdown
BEFORE executing any tool, classify the action:
- IF Green: Execute.
- IF Yellow: Log intent, then execute.
- IF Red: STOP. Output "⚠️ APPROVAL REQUIRED: [Reason]". Wait for user input.
```

### For Speckit (Tool)
```python
def check_gate(action_type, resource):
    if action_type in ["delete", "deploy", "publish"]:
        return "RED"
    if action_type in ["install", "modify"]:
        return "YELLOW"
    return "GREEN"
```

## 4. Override Codes
*   **User Override**: A user can explicitly authorize a Red Light action by saying "Proceed with [Action]".
*   **Emergency Override**: In case of system critical failure, specific recovery agents may bypass Yellow lights (but never Red).
