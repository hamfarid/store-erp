# Incident Response Workflow

## 1. Detection
*   **Sources**: Sentry, Datadog, User Report, Security Agent.
*   **Severity**:
    *   **P0 (Critical)**: Data loss, security breach, full outage.
    *   **P1 (High)**: Major feature broken, performance degradation.
    *   **P2 (Medium)**: Minor bug, UI glitch.

## 2. Triage (First 15 Minutes)
1.  **Acknowledge**: Confirm receipt of alert.
2.  **Assess**: Determine impact and scope.
3.  **Contain**: Stop the bleeding (e.g., rollback deployment, block IP).

## 3. Resolution
1.  **Investigate**: Analyze logs, reproduce issue.
2.  **Fix**: Develop patch or workaround.
3.  **Verify**: Test fix in staging.
4.  **Deploy**: Push fix to production.

## 4. Post-Mortem (Within 24 Hours)
*   **Root Cause Analysis (RCA)**: Why did it happen? (5 Whys)
*   **Action Items**: Prevent recurrence.
*   **Documentation**: Update `memory-bank/lessons.md`.

## Templates
- `templates/incident_report.md` — Post-incident report template
