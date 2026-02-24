# 🧠 Anti-Hallucination Protocol (Active Memory + HALT + FINCH-ZK)
**Status:** Verified Feb 2026 (Based on FORGE '26 & arXiv: 2602.02888)
**Severity:** CRITICAL (Zero Tolerance)

## 1. The Problem: Context Loss & Assumptions
AI models suffer from "Context Drift" and "Hallucination" when they rely on their implicit training data or previous conversation turns instead of the **current, actual state of the file system**.

### Symptoms of Hallucination:
*   Assuming a file exists when it doesn't.
*   Assuming a file's content based on its name without reading it.
*   Forgetting recent changes (e.g., "I updated the file" when it wasn't updated).
*   Using outdated version numbers (e.g., `v15.0` instead of `v15.9.8`).

## 2. The Solution: The 5-Layer Defense Stack
This protocol defines the mandatory "Touch-First Rule" and integrates the advanced HALT and FINCH-ZK mechanisms to prevent AI hallucination, context loss, and assumption-based errors.

### Layer 1: Active Memory (The "Touch-First" Rule)
**Core Principle:** "If you haven't read it in this session, it doesn't exist."
- **Mandatory Action:** Before starting any task, the AI MUST run `tools/verify_context.py` or manually read the relevant files.
- **Prohibition:** The AI is strictly forbidden from assuming the content of a file based on its name or previous sessions.
- **Verification:** Every file read must be logged in the `activeContext.md` or system log.

### Layer 2: HALT (Heuristic Analysis of Logic & Truth)
**Source:** arXiv: 2602.02888 (Feb 2, 2026)
**Core Principle:** "Stop and think before you commit."
- **H**ypothesis: Formulate a hypothesis about the task.
- **A**nalysis: Analyze the available data and constraints.
- **L**ogic: Apply logical reasoning to validate the hypothesis.
- **T**ruth: Verify the conclusion against the "Ground Truth" (project files).
- **Mechanism:** Treat token log-probabilities as time series to detect anomalies before generation.

### Layer 3: FINCH-ZK (Fact-Checking via Zero-Knowledge Proofs)
**Source:** AWS, EMNLP 2025, arXiv: 2508.14314
**Core Principle:** "Prove it without revealing it."
- **Fact-Checking:** Every claim made by the AI must be backed by a specific line in a specific file.
- **Zero-Knowledge:** The AI must be able to prove the validity of a claim without needing to read the entire file again (using checksums or hashes).
- **Impact:** Improves hallucination detection F1 by 6–39%.

### Layer 4: Guardian Agents (The "Red Team")
**Source:** Vectara (May 2025)
**Core Principle:** "Trust, but verify."
- **Role:** Independent agents (or simulated roles) that review the AI's output for errors, hallucinations, and security vulnerabilities.
- **Action:** They run `tools/sentinel.py` and `tools/final_verify.py` to ensure compliance.
- **Pipeline:** Generate -> Detect -> Correct.

### Layer 5: External Hippocampus (RAG/MCP)
**Core Principle:** "Connect to the world, but verify the source."
- **Role:** The system's connection to external knowledge bases (RAG) and tools (MCP).
- **Action:** Ensures that external information is treated as "unverified" until cross-referenced with internal project rules.

## 3. Implementation: `verify_context.py`
We have implemented a mandatory tool `tools/verify_context.py` that enforces this protocol.

### Usage:
```bash
python3 tools/verify_context.py --target <file_or_directory> --expect <pattern>
```

### Example:
```bash
# Before updating README.md, verify it exists and check current version
python3 tools/verify_context.py --target README.md --expect "Global System Ultimate"
```

## 4. The "Checklist" Defense
Human pilots use checklists to avoid crashing planes. AI agents must use checklists to avoid crashing codebases.

*   **FILE_CHECKLIST.md:** Must be updated after *every* file creation/deletion.
*   **todo.md:** Must be the *single source of truth* for task status.
*   **INITIAL_TODO.md:** The mandatory launch checklist for every new project.

## 5. Zero Tolerance Policy
If an agent is caught:
1.  Editing a file without reading it first.
2.  Claiming a task is done without verification.
3.  Using a hardcoded version number instead of `VERSION`.

**The task will be rejected immediately.**

## 🚨 Emergency Override (Antigravity)
In rare cases where strict adherence to these protocols prevents critical system recovery, the **Antigravity** module (`tools/antigravity.py`) can be activated using a specific authorization code. This lifts constraints but logs every action as a high-risk event.
