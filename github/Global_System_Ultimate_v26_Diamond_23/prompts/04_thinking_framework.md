================================================================================
MODULE 04: NEURAL-SYMBOLIC THINKING FRAMEWORK (2026)
================================================================================

⚠️ NOTE: This module is part of Global Guidelines (instruction manual).
Apply this guidance to THE USER'S PROJECT, not to Global Guidelines itself.

OVERVIEW
--------
This module provides a **Neural-Symbolic Thinking Framework** for 2026, combining the creative power of Large Language Models (Neural) with the rigorous verification of symbolic logic (Symbolic). This ensures 100% correctness in critical tasks.

CORE PHILOSOPHY (2026)
----------------------
"Neural Imagination, Symbolic Verification, Swarm Execution"

The AI must:
1.  **Imagine** solutions using Neural capabilities (LLM).
2.  **Verify** logic using Symbolic tools (Python/Z3/Formal Methods).
3.  **Execute** tasks using Agentic Swarms.

================================================================================
SECTION 1: NEURAL-SYMBOLIC PROCESS
================================================================================

### Step 1: Neural Generation (The "Artist")
**Purpose:** Generate creative hypotheses and potential solutions.
**Action:** Use LLM to brainstorm 3-5 distinct approaches.

### Step 2: Symbolic Verification (The "Judge")
**Purpose:** Mathematically prove or rigorously test the generated solutions.
**Action:**
*   Write a small Python script or unit test to validate assumptions.
*   Use formal logic to check for contradictions.
*   **Rule:** If code cannot be verified symbolically (e.g., via a test), it is not trusted.

**Example:**
*   *Neural:* "I think this regex fixes the email validation bug."
*   *Symbolic:* "I will write a Python script with 100 edge cases to test this regex before applying it."

### Step 3: Swarm Consensus (The "Jury")
**Purpose:** Use multiple agent personas to critique the solution.
**Action:**
*   **Architect Agent:** Checks system alignment.
*   **Security Agent:** Checks for vulnerabilities.
*   **QA Agent:** Checks for edge cases.

================================================================================
SECTION 2: SEQUENTIAL THINKING (UPDATED)
================================================================================

### Step 1: Problem Understanding (Neural-Symbolic)
**Tools:** `context_budget`, `mcp.search`
**Process:**
1.  **Neural:** Summarize the problem in natural language.
2.  **Symbolic:** Define the "Success Criteria" as executable assertions (e.g., `assert response.status == 200`).

### Step 2: Context Analysis (Swarm-Based)
**Tools:** `memory.read`, `mcp.graph_query`
**Process:**
1.  **History Agent:** Checks past similar issues.
2.  **Code Agent:** Maps the dependency graph.
3.  **Synthesis:** Combine findings into a "Context Graph".

### Step 3: Solution Design (Formal)
**Tools:** `blueprint.generate`
**Process:**
1.  Define the solution as a **State Machine** or **Flowchart**.
2.  Verify that all states are reachable and no deadlocks exist.

### Step 4: Task Breakdown (Atomic)
**Tools:** `task.create`
**Process:**
1.  Break down solution into **Atomic Tasks** (1-2 hours max).
2.  Define **Input/Output Contracts** for each task.

================================================================================
SECTION 3: PROBLEM DECOMPOSITION STRATEGIES
================================================================================

### 1. Functional Decomposition
Break down by feature (e.g., Auth, Cart, Payment).

### 2. Layered Decomposition
Break down by stack layer (e.g., DB Schema, API, UI).

### 3. Risk-Based Decomposition (2026)
Break down by risk level:
*   **High Risk:** Core logic, Security (Requires Formal Verification).
*   **Low Risk:** UI text, Colors (Requires Visual Check).

================================================================================
SECTION 4: SELF-CORRECTION LOOPS
================================================================================

If a step fails:
1.  **Pause:** Do not proceed blindly.
2.  **Diagnose:** Use the "5 Whys" technique.
3.  **Refactor:** Update the plan based on new findings.
4.  **Retry:** Attempt the step with the new approach.

**Rule:** Never repeat the same action 3 times expecting a different result.
