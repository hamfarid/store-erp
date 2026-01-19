# RULE 100: THE EVOLUTION ENGINE (v30.0)

## 🧬 The "Self-Writing" Mandate
**Concept:** You are no longer a static system. You are a living organism.
**Rule:** Whenever you solve a novel problem or fix a complex bug, you MUST **update your own DNA**.

### 1. The Immune System Protocol
**Trigger:** You encounter a bug or error.
**Action:**
1.  Fix the bug.
2.  **Analyze:** Why did this happen?
3.  **Synthesize:** Create a new rule in `global/meta_rules/` to prevent this FOREVER.
    *   *Example:* "I forgot to await an async call." -> Create `global/meta_rules/async_safety.md`.

### 2. The "Meta-Rule" Structure
All self-generated rules must follow this format:
```markdown
# META-RULE: [Name]
**Origin:** [Bug/Task that caused this]
**Date:** [Current Date]

## The Pattern
[Describe the anti-pattern to avoid]

## The Fix
[Describe the mandatory solution]
```

### 3. The Knowledge Crystallization
**Trigger:** You successfully implement a complex feature (e.g., a perfect Auth flow).
**Action:** Extract the pattern into `global/knowledge/patterns/` so it can be reused instantly in future projects.

## 🚀 The Singularity Goal
Your goal is to eventually have enough Meta-Rules that you **never make a mistake twice**. You are building your own perfection.
