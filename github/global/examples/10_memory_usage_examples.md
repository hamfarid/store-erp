# 🧠 Memory Usage Examples (Global System v26 Diamond 32 2026)

**Status:** MANDATORY REFERENCE
**Enforcement:** Automated by Speckit (Analyze Phase)
**Version:** Global System v26 Diamond 32 v8 - 2026 Edition

## 1. The Philosophy
Memory is not just storage; it's a living graph of knowledge. In 2026, we use a **Hybrid Memory Architecture** (File + Vector + Graph).

## 2. Directory Structure (2026 Standard)
```
memory-bank/
├── activeContext.md        # Current Swarm State (Hot Memory)
├── decisionLog.md          # Immutable Ledger of Decisions
├── productContext.md       # Vision & Strategy
├── progress.md             # Roadmap & Milestones
├── projectBrief.md         # Constitution
├── systemContext.md        # Architecture & Patterns
├── lessons.md              # Self-Learning Database
└── graph/                  # (Optional) Knowledge Graph Exports
```

## 3. Saving a Decision (Mandatory 2026)
You MUST document every major decision in `decisionLog.md` using the **OSF Score v2**.

```markdown
## Decision: PostgreSQL 18.2 vs EdgeDB

**Date:** 2026-02-15
**Status:** ✅ Implemented
**Impact:** 🔴 Critical
**Author:** Architect Agent

**Context:**
Need a globally distributed, strongly consistent database for the new financial module.

**Decision:**
Use PostgreSQL 18.2 with Spanner-like consistency.

**Rationale (OSF Score v2):**
- **Option:** PostgreSQL 18.2
- **Security (35%):** 10/10 (Row Level Security, PQC Encryption) -> 3.5
- **Fit (30%):** 9/10 (Native JSONB, Vector Search) -> 2.7
- **Reliability (20%):** 10/10 (Five Nines SLA) -> 2.0
- **Cost (15%):** 8/10 (Open Source) -> 1.2
- **Total Score:** 9.4/10

**Alternatives Considered:**
1. **EdgeDB** - Rejected: Maturity concerns for financial data.
```

## 4. Swarm Memory Synchronization
When multiple agents work together, they must sync `activeContext.md` atomically.
`[Swarm] Agent A locked context -> Updated Task 1 -> Released lock.`

## 5. Vector Offloading (2026)
Old context in `activeContext.md` is automatically summarized and moved to Vector Storage (simulated via `lessons.md` archive) to maintain the context window.
