# Monitoring & Observability Setup Guide

This guide describes how to set up monitoring for Gaara ERP v12 using Prometheus and Grafana.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Gaara ERP     │────▶│   Prometheus    │────▶│    Grafana      │
│   (Django)      │     │   (Metrics)     │     │  (Dashboards)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Redis/Celery  │     │   AlertManager  │
└─────────────────┘     └─────────────────┘
```

## Prerequisites

- Docker and Docker Compose
- Gaara ERP running
- Network access to monitoring ports

## Quick Start with Docker Compose

Add to your `docker-compose.yml`:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: gaara_prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    networks:
      - app-network
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: gaara_grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
      - GF_USERS_ALLOW_SIGN_UP=false
    networks:
      - app-network
    depends_on:
      - prometheus
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    container_name: gaara_alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    networks:
      - app-network
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

## Prometheus Configuration

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - "alerts/*.yml"

scrape_configs:
  # Django application
  - job_name: 'gaara-erp'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  # Redis
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  # PostgreSQL (with postgres_exporter)
  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgres_exporter:9187']

  # Celery (with flower)
  - job_name: 'celery'
    static_configs:
      - targets: ['flower:5555']
```

## Django Metrics Integration

Install django-prometheus:

```bash
pip install django-prometheus
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    ...  # Other middleware
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# Database monitoring
DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        ...
    }
}
```

Add to `urls.py`:

```python
urlpatterns = [
    ...
    path('', include('django_prometheus.urls')),
]
```

## Key Metrics to Monitor

### Application Metrics
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (5xx, 4xx)
- Active connections

### Database Metrics
- Query count and duration
- Connection pool usage
- Table sizes and growth

### Celery Metrics
- Task success/failure rate
- Queue depth
- Worker utilization
- Task duration

### System Metrics
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

## Grafana Dashboards

### Recommended Dashboards

1. **Django Application Dashboard**
   - Request rate and latency
   - Error rates by endpoint
   - Database query performance

2. **Infrastructure Dashboard**
   - Container resource usage
   - Redis memory and connections
   - PostgreSQL performance

3. **Celery Dashboard**
   - Task throughput
   - Queue sizes
   - Worker status

### Import Dashboard IDs

| Dashboard | Grafana ID |
|-----------|------------|
| Django Prometheus | 9528 |
| PostgreSQL | 9628 |
| Redis | 763 |
| Celery | 5984 |

## Alerting Rules

Create `monitoring/alerts/gaara.yml`:

```yaml
groups:
  - name: gaara-erp
    rules:
      - alert: HighErrorRate
        expr: rate(django_http_responses_total_by_status_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: Error rate is {{ $value }} errors/second

      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(django_http_requests_latency_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: Slow response time
          description: 95th percentile response time is {{ $value }} seconds

      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High memory usage
          description: Memory usage is above 90%

      - alert: CeleryQueueBacklog
        expr: celery_task_received_total - celery_task_succeeded_total - celery_task_failed_total > 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: Celery queue backlog
          description: More than 100 tasks pending
```

## AlertManager Configuration

Create `monitoring/alertmanager.yml`:

```yaml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@gaara-erp.com'
  smtp_auth_username: 'alertmanager'
  smtp_auth_password: 'password'

route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'email-notifications'

receivers:
  - name: 'email-notifications'
    email_configs:
      - to: 'team@gaara-erp.com'
        send_resolved: true
```

## Health Check Endpoints

Gaara ERP provides these health endpoints:

| Endpoint | Description |
|----------|-------------|
| `/health/` | Basic health check |
| `/health/ready/` | Readiness probe |
| `/health/live/` | Liveness probe |
| `/metrics/` | Prometheus metrics |

## Best Practices

1. **Retention**: Keep metrics for 15-30 days
2. **Alerting**: Start with critical alerts only
3. **Dashboards**: Create role-based dashboards
4. **Labels**: Use consistent labeling
5. **Documentation**: Document all alerts and dashboards

