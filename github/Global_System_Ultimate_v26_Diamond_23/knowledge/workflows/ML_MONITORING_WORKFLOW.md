# ML Monitoring Workflow (v18.0)
# Scope: Production Observability & Alerting
# Tools: Prometheus, Grafana, Evidently AI, PagerDuty

## 1. Monitoring Architecture

### 1.1 Components
*   **Metrics Exporter**: Prometheus Client (Python) in FastAPI/Flask app.
*   **Time-Series DB**: Prometheus (Scrapes every 15s).
*   **Visualization**: Grafana Dashboards (Latency, Throughput, Errors).
*   **Drift Detection**: Evidently AI Service (Batch/Online).
*   **Alerting**: Alertmanager -> PagerDuty/Slack.

### 1.2 Data Flow
1.  **Inference Request**: API receives input.
2.  **Logging**: Input/Output logged to JSON (Structured Logging).
3.  **Metrics**: Counters/Histograms updated (e.g., `model_inference_latency_seconds`).
4.  **Scraping**: Prometheus pulls metrics.
5.  **Analysis**: Evidently analyzes logs for drift (Async).

## 2. Key Metrics (Golden Signals)

### 2.1 Latency
*   **Metric**: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`.
*   **Alert**: > 500ms for 5 mins (Sev-2).

### 2.2 Traffic
*   **Metric**: `rate(http_requests_total[5m])`.
*   **Alert**: Drop > 50% vs Last Week (Sev-1).

### 2.3 Errors
*   **Metric**: `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])`.
*   **Alert**: > 1% Error Rate (Sev-1).

### 2.4 Saturation
*   **Metric**: `container_cpu_usage_seconds_total`.
*   **Alert**: > 80% CPU for 10 mins (Sev-3).

## 3. Drift Monitoring (Evidently)

### 3.1 Setup
*   **Reference Data**: Validation set from training (v1.0).
*   **Current Data**: Last 24h of production logs.
*   **Report**: Generated daily at 00:00 UTC.

### 3.2 Dashboard
*   **Panels**:
    *   Data Drift Summary (PSI Score).
    *   Feature Drift Heatmap.
    *   Target Drift (Prediction Distribution).

## 4. Incident Response

### 4.1 Sev-1 (Critical)
1.  **Ack**: On-Call Engineer acknowledges PagerDuty (15m).
2.  **Triage**: Check Grafana (Is it Infra or Model?).
3.  **Mitigate**: Rollback to previous version (Blue/Green switch).
4.  **Analyze**: Root Cause Analysis (RCA) within 24h.

### 4.2 Sev-2 (Major)
1.  **Ack**: Team Lead acknowledges Slack (4h).
2.  **Investigate**: Check Drift Report.
3.  **Action**: Trigger Retraining Pipeline if drift confirmed.

## 5. Code Example (Prometheus Middleware)

```python
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter("http_requests_total", "Total Requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request Latency", ["endpoint"])

@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response
```
