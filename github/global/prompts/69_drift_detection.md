# Prompt 69: Drift Detection & System Monitoring

> **Scope**: Model drift monitoring and system health for GAARA-AI
> **Tools**: Evidently AI (drift) + Prometheus/Grafana (system)

## Drift Detection (Evidently AI 0.6+)

### What to Monitor
| Type | Description | Tool |
|:-----|:------------|:-----|
| Data Drift | Input data distribution changes | Evidently DataDriftPreset (PSI method) |
| Model Drift | Prediction distribution changes | Evidently custom metrics |
| Concept Drift | Relationship between input/output changes | Evidently + manual review |

### Models to Monitor
- Plant Disease (YOLOv8n) — daily drift check at 2 AM
- Nutrient Deficiency (DenseNet121) — daily drift check at 2 AM
- Embedding quality (BGE-M3) — weekly check

### Alerting Thresholds
- Data drift score > 0.3 → Warning
- Data drift score > 0.5 → Critical → trigger retraining evaluation
- Model accuracy drop > 5% → Critical

## System Monitoring (Prometheus + Grafana)

### Metrics Collected (every 60 seconds)
- Service health (all 15+ containers)
- API response times (p50, p95, p99)
- Celery queue depths and task durations
- CPU, RAM, Disk usage per server
- LLM inference latency
- Qdrant query performance

### Grafana Dashboards
- **AI Overview** — LLM usage, diagnoses count, search volume
- **System Health** — server resources, container status, network

## Rules
- Every service MUST expose `/health` endpoint
- Every service MUST expose `/metrics` endpoint (Prometheus format)
- Health checks run every 5 minutes (Celery beat)
- Drift detection runs daily at 2 AM Cairo time
- Alerts sent via email when thresholds exceeded
