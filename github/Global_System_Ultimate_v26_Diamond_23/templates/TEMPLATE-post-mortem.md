# Post-Mortem Template (v26.0)

> **Usage**: Copy and fill after any ML model failure, drift event, or production incident
> **Reference**: `errors/ml/ERROR-drift-detection-catalog.md`
> **Version**: v26.0.0 (Diamond 8)

## Incident Summary

| Field | Value |
| :--- | :--- |
| **Incident ID** | [e.g., PM-2026-001] |
| **Date Detected** | [YYYY-MM-DD HH:MM] |
| **Date Resolved** | [YYYY-MM-DD HH:MM] |
| **Severity** | [Critical / High / Medium] |
| **Status** | [Open / Resolved / Monitoring] |

**One-Line Summary**: [e.g., “Model accuracy dropped 15% on tomato early blight due to seasonal distribution shift”]

## Timeline

| Time | Event |
| :--- | :--- |
| [datetime] | First indication of issue (alert, user report, monitoring) |
| [datetime] | Investigation started |
| [datetime] | Root cause identified |
| [datetime] | Fix deployed |
| [datetime] | Verification complete |

## Impact

- **Affected Systems**: [Model name/version, API endpoints, user-facing features]
- **Affected Users/Volume**: [Number of predictions affected, duration of degraded service]
- **Business Impact**: [e.g., “Approximately 500 misclassifications over 3 days”]
- **Data Impact**: [Were any embeddings, labels, or stored results affected?]

## Root Cause Analysis

### What Happened
[Detailed narrative of the failure — what broke and how it manifested]

### Why It Happened (5 Whys)
1.  **Why did the model accuracy drop?** → [answer]
2.  **Why did [answer above] occur?** → [answer]
3.  **Why did [answer above] occur?** → [answer]
4.  **Why did [answer above] occur?** → [answer]
5.  **Why did [answer above] occur?** → [root cause]

### Contributing Factors
[List factors that made this worse or harder to detect]

## Resolution

### Immediate Actions Taken
[What was done to stop the bleeding — rollback, hotfix, manual intervention]

### Permanent Fix
[What was done to resolve the root cause — retraining, pipeline fix, threshold adjustment]

### Verification
[How was the fix verified — metrics, test results, monitoring period]

## Prevention: What We Will Change

### Detection Improvements
[How will we catch this faster next time? — new alerts, monitoring, quality gates]

### Process Improvements
[What process changes prevent recurrence? — new checks, automation, reviews]

### Documentation Updates
[Which docs/rules/error catalogs need updating?]

### Error Catalog Entry
- **Error Code**: [e.g., ERR-DRIFT-002]
- **Added to**: `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md`? [Yes/No]
- **Added to**: `errors/ml/ERROR-drift-detection-catalog.md`? [Yes/No]

## Metrics Before/After

| Metric | Before Incident | During Incident | After Fix |
| :--- | :--- | :--- | :--- |
| **Overall Accuracy** | [Value] | [Value] | [Value] |
| **Affected Class F1** | [Value] | [Value] | [Value] |
| **Centroid Shift** | [Value] | [Value] | [Value] |
| **Inference Latency** | [Value] | [Value] | [Value] |

## Lessons Learned

### What Went Well
[Detection speed, response time, communication, etc.]

### What Went Poorly
[Gaps in monitoring, slow response, missing documentation, etc.]

### Action Items

| Action | Owner | Due Date | Status |
| :--- | :--- | :--- | :--- |
| [Action 1] | [Name] | [Date] | [Status] |
| [Action 2] | [Name] | [Date] | [Status] |

## Approvals

| Role | Name | Date |
| :--- | :--- | :--- |
| **Written by** | [Author] | [Date] |
| **Reviewed by** | [Reviewer] | [Date] |
| **Approved by** | [Project Lead] | [Date] |

## Cross-References
- **Model Card**: `templates/ml/MODEL_CARD.md` (for the affected model)
- **Governance Guide**: `knowledge/ml/GUIDE-model-governance.md`
- **Error Catalogs**: `errors/ml/` (relevant catalog)
