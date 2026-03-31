# /speckit.specify (Hybrid Engine v35.0)

**Goal:** Define WHAT to build with **Mathematical Precision** and **Visual Clarity**.
**Constraint:** NO Ambiguity. NO "To be determined".

**Input:**
*   `CONSTITUTION.md` (The Law)
*   `global/rules/visual_thinking.md` (Mandatory Diagrams)
*   `global/rules/context_first.md` (Context Awareness)

**Output:** `specs/[feature_name].spec.md`

**The Hybrid Protocol:**

1.  **Visual Thinking First (Mandatory):**
    *   You CANNOT write text until you have visualized the flow.
    *   **Requirement:** Include at least one **Mermaid Diagram** (Flowchart, Sequence, or State Diagram) that maps the user journey.

2.  **The "Shadow" Check (Swarm Intelligence):**
    *   Anticipate 3 potential misunderstandings a junior developer might have.
    *   Add a section: "## Anti-Patterns (What NOT to do)" to clarify these.

3.  **Context Injection:**
    *   Reference existing files from `.memory/file_registry.json`.
    *   Do not reinvent the wheel. If a helper exists, use it.

**Template (Strict Enforcement):**

```markdown
# Spec: [Feature Name]
**Version:** 1.0
**Visual Hash:** [Mermaid Diagram Hash]

## 1. The Visual Model (Mermaid)
```mermaid
[Your Diagram Here]
```

## 2. User Story (The "Why")
As a **[Role]**, I want **[Feature]**, so that **[Benefit]**.

## 3. Functional Requirements (The "What")
*   [ ] **REQ-01:** [Precise Description]
*   [ ] **REQ-02:** [Precise Description]

## 4. The Shadow Report (Anti-Patterns)
*   ⚠️ **Do NOT** use [X library]; use [Y] instead.
*   ⚠️ **Avoid** [Common Mistake].

## 5. Acceptance Criteria (The "Done")
*   [ ] Pass Rate > 99%
*   [ ] Latency < 200ms
```
