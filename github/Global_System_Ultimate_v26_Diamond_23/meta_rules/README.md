# Meta-Rules (The Immune System Global System Ultimate)

This directory contains rules **written by the AI itself** (The Evolution Engine), now orchestrated by **Speckit**.

## How it works
1.  **Detection:** The AI encounters a bug or learns a new pattern during `speckit verify`.
2.  **Evolution:** The AI creates a new `.md` file in this directory.
3.  **Assimilation:** The AI reads this directory at the start of every session (via `AI_CONTEXT_ROUTER.md`) to "load" its immune system.

## Structure
*   `000_index.md`: A registry of all meta-rules.
*   `XXX_rule_name.md`: The specific rule.

## Integration
*   **Speckit Analyze:** Scans this directory to avoid repeating past mistakes.
*   **Sentinel:** Can be configured to enforce specific meta-rules.
