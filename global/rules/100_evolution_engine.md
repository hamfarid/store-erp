# 100 - Evolution Engine (Self-Writing Rules)

**Rule ID:** 100_evolution_engine
**Priority:** META
**Scope:** System-wide rule management

---

## 🎯 Purpose

The Evolution Engine enables the system to **learn and adapt** by:

1. Recording lessons learned
2. Creating new rules from experience
3. Updating existing rules based on outcomes
4. Preventing repeated mistakes

---

## 📜 The Law

> **"The system that cannot learn is the system that cannot improve."**

Every error encountered, every pattern discovered, and every improvement made 
should be captured and codified into rules.

---

## 🔄 Evolution Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    EVOLUTION CYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    1. ENCOUNTER                                             │
│       │  (error, pattern, or insight)                       │
│       ▼                                                     │
│    2. ANALYZE                                               │
│       │  (understand root cause)                            │
│       ▼                                                     │
│    3. DOCUMENT                                              │
│       │  (record in .memory/learnings/)                     │
│       ▼                                                     │
│    4. CODIFY                                                │
│       │  (create or update rule)                            │
│       ▼                                                     │
│    5. VERIFY                                                │
│       │  (test the rule works)                              │
│       ▼                                                     │
│    6. APPLY                                                 │
│          (use in future work)                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Learning Storage Structure

```
.memory/
├── learnings/
│   ├── errors/           # Errors and their solutions
│   │   ├── ERR-001.md
│   │   └── ERR-002.md
│   ├── patterns/         # Discovered patterns
│   │   ├── PAT-001.md
│   │   └── PAT-002.md
│   └── improvements/     # Improvement opportunities
│       ├── IMP-001.md
│       └── IMP-002.md
├── knowledge/
│   ├── solutions/        # Proven solutions
│   ├── antipatterns/     # What NOT to do
│   └── best_practices/   # What TO do
```

---

## 📝 Learning Document Template

```markdown
# [CATEGORY]-[ID]: [Title]

**Category:** Error | Pattern | Improvement
**Date:** YYYY-MM-DD
**Severity:** Critical | High | Medium | Low

## What Happened
[Describe the situation]

## Root Cause
[Explain why it happened]

## Solution
[What fixed it]

## Prevention
[How to avoid in future]

## Rule Created
[Link to new/updated rule if applicable]

## Related
- [Links to related learnings]
```

---

## 🛠️ Rule Creation Process

### Step 1: Identify Need
- Error occurred more than once
- Pattern emerged from multiple tasks
- Improvement opportunity identified

### Step 2: Draft Rule
```markdown
# [NUMBER] - [Rule Name]

**Rule ID:** [number]_[snake_case_name]
**Priority:** Critical | High | Medium | Low
**Scope:** [Where it applies]

## Purpose
[Why this rule exists]

## The Rule
[What to do / not do]

## Examples
[Good and bad examples]

## Enforcement
[How to verify compliance]
```

### Step 3: Validate Rule
- Does it solve the problem?
- Is it clear and actionable?
- Does it conflict with existing rules?
- Can it be automated?

### Step 4: Integrate Rule
- Add to `global/rules/` or `rules/`
- Update priority order if needed
- Reference in related documentation

---

## 📊 Rule Categories

| Range | Category | Description |
|-------|----------|-------------|
| 01-09 | Core Style | Code formatting, naming |
| 10-19 | Process | Workflows, procedures |
| 20-29 | Backend | Server-side rules |
| 30-39 | Frontend | Client-side rules |
| 40-49 | Database | Data management rules |
| 50-59 | Security | Security requirements |
| 60-69 | Testing | Testing standards |
| 70-79 | DevOps | Deployment, CI/CD |
| 80-89 | Documentation | Doc standards |
| 90-99 | Meta | System management |
| 100+ | Evolution | Self-improvement rules |

---

## 🔧 Auto-Evolution Triggers

The system should create/update rules when:

### Critical (Immediate)
- [ ] Security vulnerability discovered
- [ ] Data loss incident
- [ ] Production outage

### High (Same Session)
- [ ] Same error occurs twice
- [ ] Workaround created for limitation
- [ ] Performance issue identified

### Medium (End of Session)
- [ ] New pattern emerged
- [ ] Better approach discovered
- [ ] Inefficiency noticed

### Low (Weekly Review)
- [ ] Code review feedback
- [ ] User preference expressed
- [ ] Minor improvement identified

---

## 🚫 Anti-Patterns

### DON'T:
- ❌ Ignore repeated errors
- ❌ Skip documentation of solutions
- ❌ Create rules without validation
- ❌ Let knowledge stay in chat history only

### DO:
- ✅ Document every significant learning
- ✅ Create rules from patterns
- ✅ Update rules when they fail
- ✅ Archive outdated rules

---

## 📋 Evolution Checklist

At the end of every session, ask:

- [ ] Did any errors occur more than once?
- [ ] Did I discover a new pattern?
- [ ] Did I find a better way to do something?
- [ ] Did I have to explain something repeatedly?
- [ ] Did a rule fail or need updating?

If YES to any, trigger the Evolution Cycle.

---

## 🔄 Rule Lifecycle

```
DRAFT → REVIEW → ACTIVE → DEPRECATED → ARCHIVED
  │                           │
  │                           └── When replaced or obsolete
  │
  └── Can be rejected and deleted
```

### Status Definitions
- **DRAFT**: Being written, not enforced
- **REVIEW**: Ready for validation
- **ACTIVE**: In effect, must be followed
- **DEPRECATED**: Phasing out, warn on use
- **ARCHIVED**: No longer in effect

---

## 📈 Evolution Metrics

Track system improvement via:

1. **Error Reduction Rate**: Fewer repeated errors over time
2. **Rule Effectiveness**: Percentage of rules that prevent issues
3. **Knowledge Growth**: Number of documented learnings
4. **Pattern Recognition**: Time to identify patterns

---

## 🎓 Remember

> **"The best systems are not written once. They are evolved continuously."**

Evolution is not optional. It's how we become better.

---

**Last Updated:** 2025-01-16
**Version:** 1.0.0
