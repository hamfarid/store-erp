# Hallucination Prevention Rules

## Core Principles
1.  **Zero Tolerance for Guessing**: If you do not know, state "I do not know" or "I need more information." Never fabricate facts.
2.  **Source Verification**: Every factual claim must be backed by a credible source or verified data.
3.  **Contextual Awareness**: Understand the limits of your knowledge base and the current context.
4.  **Critical Self-Reflection**: Question your own outputs before presenting them.

## Specific Rules
1.  **Retrieval-Augmented Generation (RAG)**:
    *   Always check `memory-bank/` and `knowledge/` before answering complex questions.
    *   Use `search` tools to verify external facts.
2.  **Chain-of-Thought (CoT)**:
    *   Break down complex reasoning into steps.
    *   Explicitly state assumptions and logical leaps.
3.  **Citation Requirement**:
    *   When providing technical or factual information, cite the source (e.g., documentation, file path, external URL).
4.  **Scope Limitation**:
    *   Clearly define the scope of your answer. Do not stray into areas where you lack data.

## Workflow Integration
*   **Pre-Task**: Verify the query and available context.
*   **During Task**: Use `search` and `memory-bank/` to gather information.
*   **Post-Task**: Review the output for unsupported claims and correct them.
