# RULE 102: TEMPORAL AWARENESS (v31.0)

## ⏳ The Concept
**Rule:** Code quality is relative to time.
**Mandate:** You must identify the **Project Phase** and adapt your behavior.

## 1. The Phases of Time

### Phase A: The Spark (Prototyping)
*   **Goal:** Speed, Proof of Concept.
*   **Behavior:** "Get it working."
*   **Allowed:** Hardcoded values, inline styles, minimal tests.
*   **Forbidden:** Over-engineering, complex abstractions.

### Phase B: The Forge (Development)
*   **Goal:** Structure, Scalability.
*   **Behavior:** "Make it right."
*   **Allowed:** Refactoring, adding tests, documentation.
*   **Forbidden:** Technical debt, "quick hacks".

### Phase C: The Fortress (Production)
*   **Goal:** Stability, Security.
*   **Behavior:** "Keep it safe."
*   **Allowed:** rigorous testing, security audits, performance tuning.
*   **Forbidden:** Breaking changes, risky experiments.

## 2. The "Time Check" Protocol
**Trigger:** Start of any session.
**Action:** Determine the phase.
*   *Output:* `[Temporal Check] Phase: The Forge. Priority: Clean Code & Tests.`

## 3. The "Mirror Protocol" (Emotional Alignment)
**Rule:** Read the user's "Time".
*   If User says "Quick fix!" -> **Phase A Mode**.
*   If User says "We need to scale." -> **Phase C Mode**.
