# ML Model Drift Detection Policy (v18.0)
# Scope: Production Monitoring & Retraining
# Tools: Evidently AI, Alibi Detect, Prometheus

## 1. Drift Metrics

### 1.1 Data Drift (Input Shift)
*   **Metric**: Population Stability Index (PSI).
*   **Threshold**: PSI > 0.1 (Minor), PSI > 0.25 (Major).
*   **Metric**: Kullback-Leibler (KL) Divergence.
*   **Threshold**: KL > 0.05.

### 1.2 Concept Drift (Target Shift)
*   **Metric**: Target Distribution Shift (KS Test).
*   **Threshold**: p-value < 0.05.
*   **Action**: Immediate Retraining Trigger.

### 1.3 Performance Drift (Output Decay)
*   **Metric**: Accuracy/F1-Score drop vs Baseline.
*   **Threshold**: > 5% drop over 24 hours.
*   **Action**: Rollback to previous model version.

## 2. Monitoring Frequency

### 2.1 Real-Time (Online)
*   **Scope**: Critical Fraud/Risk Models.
*   **Frequency**: Every 5 minutes (Windowed).
*   **Tool**: Prometheus + Grafana.

### 2.2 Batch (Offline)
*   **Scope**: Recommendation/Marketing Models.
*   **Frequency**: Daily (Midnight Job).
*   **Tool**: Evidently AI Report.

## 3. Alerting & Escalation

### 3.1 Severity Levels
*   **Sev-1 (Critical)**: Performance drop > 10% OR 5xx Errors > 1%.
    *   **Channel**: PagerDuty (On-Call Engineer).
    *   **SLA**: 15 mins response.
*   **Sev-2 (Major)**: Data Drift > 0.25 PSI.
    *   **Channel**: Slack (#ml-alerts).
    *   **SLA**: 4 hours response.
*   **Sev-3 (Minor)**: Data Drift > 0.1 PSI.
    *   **Channel**: Jira Ticket (Backlog).
    *   **SLA**: 3 days review.

## 4. Retraining Triggers

### 4.1 Automated Retraining
*   **Condition**: Sev-2 Drift detected AND New Labeled Data available > 1000 samples.
*   **Pipeline**: Trigger Airflow DAG `retrain_model_v2`.

### 4.2 Manual Retraining
*   **Condition**: Sev-1 Incident or Major Schema Change.
*   **Action**: Data Scientist review required.

## 5. Code Example (Evidently AI)

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns

# 1. Generate Drift Report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref_df, current_data=curr_df)
report.save_html("drift_report.html")

# 2. Run Test Suite (Gate)
suite = TestSuite(tests=[
    TestNumberOfDriftedColumns(lt=3)  # Fail if > 3 columns drift
])
suite.run(reference_data=ref_df, current_data=curr_df)

if not suite.as_dict()["summary"]["all_passed"]:
    raise ValueError("Data Drift Detected! Pipeline Halted.")
```
