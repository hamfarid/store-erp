# Memory & Context Engineering Documentation (2026 Edition)

## 1. Overview
This document describes the memory and context engineering architecture for the Global System (v26 Diamond 33), based on the "2026 Engineer's Playbook for Trustworthy AI Systems".

## 2. Memory Architecture
### 2.1. Two-Tier Paradigm
*   **Tier 1 (Working Memory)**: Context window (32K–200K tokens).
*   **Tier 2 (External Storage)**: Vector DBs, Graph DBs, Relational Stores.

### 2.2. Memory Bank Pattern
Structured markdown files for persistent context:
*   `projectbrief.md`
*   `productContext.md`
*   `systemPatterns.md`
*   `techContext.md`
*   `activeContext.md`
*   `progress.md`

### 2.3. Mem0 Architecture
*   **Extraction Phase**: Identify candidate memories.
*   **Update Phase**: Reconcile new information (Add, Update, Delete).

## 3. Context Engineering
### 3.1. Four Pillars
*   **Write**: Persist information outside the context window.
*   **Select**: Pull only relevant context (RAG, Tool RAG).
*   **Compress**: Retain necessary tokens (Summarization, Compaction).
*   **Isolate**: Split context across specialized agents.

### 3.2. Context Rot
Performance degradation as input length increases.
*   **Context Poisoning**: Hallucination enters context.
*   **Context Distraction**: Over-focus on long context.
*   **Context Confusion**: Superfluous content influences response.
*   **Context Clash**: Contradictory information.

## 4. Dynamic Context Loading
*   **Just-in-Time Retrieval**: Load data at runtime using tools.
*   **Multi-Source Fusion**: Combine system prompts, history, retrieved docs, tool outputs.

## 5. Conclusion
Context engineering is an optimization problem. Use the Write-Select-Compress-Isolate framework to maximize output quality subject to length constraints.
