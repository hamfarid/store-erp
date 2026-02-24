# 🤖 Agent-to-Agent (A2A) Coordination Protocol
**Verified Feb 2026 Standard**

## 1. Overview
This protocol defines how autonomous agents (Architect, Developer, Reviewer) communicate and coordinate tasks without a central message bus, using **Git** as the primary coordination primitive.

## 2. The Git Coordination Primitive
*   **Task Locking:** Agents "lock" a task by creating a branch `task/<id>/<agent_name>`.
*   **Handoff:** Agents signal completion by opening a Pull Request (PR).
*   **Feedback:** Reviewer agents post comments on the PR.
*   **Merge:** Only the QA agent can merge to `main`.

## 3. Communication Standards (A2A)
*   **Format:** JSON-structured comments in PRs.
*   **Schema:**
    ```json
    {
      "agent": "Reviewer-Alpha",
      "verdict": "REQUEST_CHANGES",
      "reason": "Failed EDD check (pass^k < 0.9)",
      "required_action": "Refactor auth_service.py"
    }
    ```

## 4. Conflict Resolution
*   **Oracle Decomposition:** If multiple agents fail on the same task, the Architect (Oracle) must decompose the task into smaller sub-tasks assigned to specific agents.

## 5. Tools
*   **MCP:** For tool execution.
*   **A2A:** For agent coordination via Git.
