# Monitoring Dashboard Template
# Tooling: Grafana, Prometheus, Evidently AI

## Dashboard Overview
*   **Title:** [Model Name] Production Monitoring
*   **Description:** Real-time monitoring of model health, data drift, and system performance.
*   **Owner:** [MLOps Team]
*   **Refresh Rate:** [e.g., 1m]

## Panel 1: System Health (Top Row)
*   **Metric:** `container_cpu_usage_seconds_total` (Rate)
    *   **Alert:** > 80% for 5m (Warning)
*   **Metric:** `container_memory_usage_bytes`
    *   **Alert:** > 90% (Critical)
*   **Metric:** `http_request_duration_seconds` (p95, p99)
    *   **Alert:** p95 > 100ms (Warning)
*   **Metric:** `http_requests_total` (Rate, by status code)
    *   **Alert:** 5xx rate > 1% (Critical)

## Panel 2: Data Drift (Middle Row)
*   **Metric:** `evidently_data_drift_score` (PSI/KL Divergence)
    *   **Alert:** PSI > 0.1 (Warning), PSI > 0.25 (Critical)
*   **Metric:** `evidently_feature_drift_score` (Top 5 features)
    *   **Visualization:** Bar chart of drift scores per feature.
*   **Metric:** `evidently_target_drift_score` (Prediction distribution)
    *   **Visualization:** Histogram overlay (Reference vs. Current).

## Panel 3: Model Performance (Bottom Row)
*   **Metric:** `model_accuracy` (If ground truth available)
    *   **Alert:** < 90% (Warning)
*   **Metric:** `model_prediction_count` (By class/value)
    *   **Visualization:** Time series of prediction volume.
*   **Metric:** `model_confidence_score` (Mean/Median)
    *   **Alert:** Drop > 10% (Warning)

## Alerting Rules
*   **Channel:** Slack (#ml-alerts), PagerDuty (Critical only).
*   **Escalation:** On-call MLOps -> Model Owner -> Data Scientist.
