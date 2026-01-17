# Memory System

**FILE**: github/global/.memory/README.md | **PURPOSE**: Memory system documentation | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

The `.memory/` directory is the AI agent's working memory system. It maintains context across sessions and prevents hallucination through systematic context retention.

## Structure

```
.memory/
├── conversations/     # All user interactions
├── decisions/         # Significant decisions with OSF analysis
├── checkpoints/       # Project state snapshots
├── context/          # Current task context
└── learnings/        # Lessons learned
```

## Purpose

### conversations/
Stores all user interactions for context retention.

**Format**: `conversation_YYYY-MM-DD_HHmmss.md`

**When**: After every user interaction

### decisions/
Stores all significant decisions with OSF Framework analysis.

**Format**: `decision_YYYY-MM-DD_[topic].md`

**When**: After any decision requiring OSF analysis

### checkpoints/
Stores project state snapshots at the end of each phase.

**Format**: `checkpoint_phase_X_YYYY-MM-DD.md`

**When**: At the end of each of the 7 phases

### context/
Stores the current task context (continuously updated).

**File**: `current_task.md`

**When**: Continuously updated during work

### learnings/
Stores lessons learned from errors and discoveries.

**Format**: `learning_YYYY-MM-DD_[topic].md`

**When**: After resolving errors or discovering best practices

## Usage

See `prompts/01_memory_management.md` for detailed usage guidelines.

## Mandatory 10-Minute Context Refresh

Every 10 minutes, the AI agent must:
1. Save current state to `.memory/context/current_state.md`
2. Re-read core files
3. Review last 20 log entries
4. Verify current plan
5. Resume work

This prevents context loss and hallucination.

---

**This directory is critical for autonomous operation. Never delete or modify manually.**

