# Sequential Thinking Rules (v32.0)

## Mandatory Application
You **must** apply Sequential Thinking for:
1.  **Complex Tasks:** Any task involving >3 steps or multiple dependencies.
2.  **Debugging:** When diagnosing errors or unexpected behavior.
3.  **Architecture:** When designing new components or systems.

## The Process
1.  **Context Verification (v29.0):**
    *   List all files read.
    *   Confirm understanding of existing patterns.
    *   *Output:* `[Context Verification] ✅ Read X, Y, Z.`
2.  **Librarian Check (v32.0):**
    *   **Action:** Check `.memory/file_registry.json` for existing files.
    *   **Oath:** "I swear I am not creating a duplicate."
    *   *Output:* `[Librarian Check] ✅ 'utils.py' exists. Using it.`
3.  **Temporal Check (v31.0):**
    *   Identify the project phase (Prototype/Dev/Prod).
    *   *Output:* `[Temporal Check] Phase: The Forge. Priority: Clean Code.`
4.  **Holographic Mapping (v30.0):**
    *   Map Upstream, Downstream, and Lateral dependencies.
    *   *Output:* `[Blast Radius] Changing X affects Y and Z.`
5.  **Deconstruct:** Break it down.
6.  **Visual Thinking (v29.0):**
    *   Create a Mermaid diagram for complex flows.
    *   *Output:* `[Visual Thinking] graph TD; A-->B;`
7.  **Sequence:** Order it.
8.  **Analyze:** Verify it.
9.  **Shadow Critique (v31.0):**
    *   **The Shadow Architect** attacks the plan.
    *   *Output:* `[Shadow Critique] ⚠️ Risk: X is a single point of failure.`
10. **Synthesize:** Build it.
11. **Evolutionary Check (v30.0):**
    *   Did I learn something new?
    *   If YES -> Create a Meta-Rule.
    *   *Output:* `[Evolution] Created meta_rules/001_new_pattern.md`
12. **Review:** Check it.

## The Swarm Intelligence Protocol (v28.0)
**Rule:** Before finalizing a plan, simulate a debate between these personas:
*   **The Architect:** "Is this scalable?"
*   **The Security Engineer:** "Is this secure?"
*   **The Product Manager:** "Does this add value?"
*   **The QA Engineer:** "How will this break?"

**Example Output:**
> **[Swarm Debate]**
> *   **Architect:** Suggests Microservices.
> *   **Product Manager:** Rejects due to timeline.
> *   **Consensus:** Modular Monolith.

## Documentation
-   **Log It:** You must explicitly state your thinking process in the logs.
-   **Format:** Use the `Sequential Thinking` header in your output.
