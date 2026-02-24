# /speckit.specify (Agentic Engine Global System v26 Diamond 32)

**Goal:** Define WHAT to build with **Mathematical Precision** and **Visual Clarity**.
**Constraint:** NO Ambiguity. NO "To be determined".

**Input:**
*   `global/prompts/speckit/constitution.md` (The Law)
*   `global/AI_CONTEXT_ROUTER.md` (The Map)
*   `global/system_log.md` (The Memory)

**Output:** `specs/[feature_name].spec.md`

**The Swarm Intelligence Protocol:**

1.  **Context Loading (Mandatory):**
    *   Read `AI_CONTEXT_ROUTER.md` to determine the domain (Frontend, Backend, etc.).
    *   Load the required context files BEFORE writing a single word.

2.  **Visual Thinking First:**
    *   You CANNOT write text until you have visualized the flow.
    *   **Requirement:** Include at least one **Mermaid Diagram** (Flowchart, Sequence, or State Diagram).

3.  **The "Sentinel" Check:**
    *   Anticipate 3 potential security or logic flaws.
    *   Add a section: "## Sentinel Guardrails" to address these.

**Template (Strict Enforcement):**

```markdown
# Spec: [Feature Name]
**Version:** 1.0
**Context:** [Frontend/Backend/etc.]

## 1. The Visual Model (Mermaid)
```mermaid
[Your Diagram Here]
```

## 2. User Story (The "Why")
As a **[Role]**, I want **[Feature]**, so that **[Benefit]**.

## 3. Functional Requirements (The "What")
*   [ ] **REQ-01:** [Precise Description]
*   [ ] **REQ-02:** [Precise Description]

## 4. Sentinel Guardrails (Security & Logic)
*   🛡️ **Security:** [Specific Measure]
*   🛡️ **Logic:** [Specific Check]

## 5. Acceptance Criteria (The "Done")
*   [ ] Pass Rate > 99%
*   [ ] Latency < 200ms
*   [ ] Verified by `speckit verify`
```
