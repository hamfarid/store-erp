# Solution Trade-off Log (APPEND-ONLY)

> Record alternatives, OSF_Score, and final decision per significant change.

## Template

```markdown
## [YYYY-MM-DD] Feature/Module: <name> | PR: <#> | Owner: <team>

**Context:**
<Describe the problem, requirement, or decision point>

**Options & OSF_Score:**

| Option | Security | Correctness | Reliability | Maintainability | Perf | Speed | OSF_Score |
|-------:|---------:|------------:|------------:|----------------:|-----:|------:|----------:|
| A      | 0.9      | 0.9         | 0.8         | 0.8             | 0.7  | 0.5   | 0.84      |
| B      | 0.7      | 0.8         | 0.7         | 0.6             | 0.9  | 0.9   | 0.74      |
| C      | 0.8      | 0.7         | 0.8         | 0.7             | 0.6  | 0.7   | 0.75      |

**Decision:** <Selected Option>

**Rationale:**
<Why this option was chosen based on OSF_Score and context>

**Rollback:**
<How and when to rollback if needed>

**Evidence:**
<Links to benchmarks, tests, threat models, documentation>

---
```

## OSF_Score Calculation Formula

```
OSF_Score = (0.40 × Security) + (0.25 × Correctness) + (0.15 × Reliability) + 
            (0.10 × Maintainability) + (0.05 × Performance) + (0.05 × Speed)
```

**Scoring Guidelines (0.0 - 1.0):**

- **Security (0.40):** Authentication, authorization, encryption, input validation, CSRF/XSS protection, secure defaults
- **Correctness (0.25):** Logic accuracy, edge case handling, data integrity, type safety
- **Reliability (0.15):** Error handling, fault tolerance, recovery mechanisms, monitoring
- **Maintainability (0.10):** Code clarity, documentation, testability, modularity
- **Performance (0.05):** Speed, resource usage, scalability
- **Speed (0.05):** Development/delivery velocity

---

## Log Entries

<!-- Add new entries below this line -->

