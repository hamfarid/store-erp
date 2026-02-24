# GUIDE-drift-detection-tools.md
# Governance: ML/AI Application Framework (Feb 2026)

## 1. Evidently AI (Recommended)
*   **Version:** 0.7.17
*   **Pros:** Comprehensive reports (HTML/JSON), integrates with MLflow/Airflow, supports text/image drift.
*   **Cons:** Can be slow on very large datasets (requires sampling).
*   **Use Case:** General-purpose drift detection, dashboarding, reporting.

## 2. NannyML
*   **Version:** 0.10.3
*   **Pros:** Estimates performance *without* ground truth (CBPE algorithm), handles delayed feedback well.
*   **Cons:** More complex setup than Evidently.
*   **Use Case:** Production monitoring where ground truth is delayed (e.g., credit default).

## 3. Alibi Detect
*   **Version:** 0.11.4
*   **Pros:** Advanced algorithms (ks-test, mm-discrepancy), supports outlier/adversarial detection.
*   **Cons:** License change (Apache 2.0 -> Elastic License 2.0) - check compliance!
*   **Use Case:** Deep learning models, image/text outlier detection.

## 4. Deepchecks
*   **Version:** 0.18.0
*   **Pros:** Extensive suite of checks (integrity, distribution, performance), CI/CD integration.
*   **Cons:** Can be verbose.
*   **Use Case:** Pre-deployment validation, CI/CD pipelines.

## 5. Why Not Custom Scripts?
*   **Risk:** Reinventing the wheel leads to bugs and maintenance burden.
*   **Standardization:** Tools provide consistent metrics (PSI, KL Divergence) across teams.
*   **Visualization:** Built-in dashboards save development time.
