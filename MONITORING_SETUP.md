# Monitoring, Alerting & Observability Guide

## Overview

This guide covers setting up comprehensive monitoring, alerting, and observability for the Store ERP application using Prometheus, Grafana, and other tools.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Applications                              │
│         (Backend, Frontend, Database)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ (Metrics, Logs, Traces)
                       ▼
        ┌──────────────────────────────────┐
        │      Prometheus (Metrics)        │
        │      Loki (Logs)                 │
        │      Jaeger (Traces)             │
        └──────────────────┬───────────────┘
                           │
        ┌──────────────────▼───────────────┐
        │      Grafana (Visualization)     │
        │      AlertManager (Alerts)       │
        └──────────────────┬───────────────┘
                           │
        ┌──────────────────▼───────────────┐
        │    Notification Channels         │
        │    (Email, Slack, PagerDuty)    │
        └──────────────────────────────────┘
```

## 1. Prometheus Setup

### Installation via Docker Compose

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    depends_on:
      - prometheus
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  monitoring:
```

### Prometheus Configuration

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    environment: 'production'
    cluster: 'store-erp'

# Alerting configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 'alertmanager:9093'

# Rule files
rule_files:
  - '/etc/prometheus/alerts.yml'

scrape_configs:
  # Backend metrics
  - job_name: 'backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s

  # Database metrics
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']

  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # Redis (if used)
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # Docker containers
  - job_name: 'docker'
    static_configs:
      - targets: ['localhost:9323']
```

### Alert Rules

```yaml
# monitoring/alerts.yml
groups:
  - name: backend_alerts
    interval: 30s
    rules:
      # API Availability
      - alert: APIDown
        expr: up{job="backend"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Backend API is down"
          description: "Backend API has been unavailable for 2 minutes"

      # High Error Rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 5% for 5 minutes"

      # Slow Response Time
      - alert: SlowResponse
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow API response times"
          description: "95th percentile response time > 1 second"

      # High CPU Usage
      - alert: HighCPUUsage
        expr: node_cpu_seconds_total{mode="user"} > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80%"

      # High Memory Usage
      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85%"

      # Disk Space
      - alert: LowDiskSpace
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space"
          description: "Less than 10% disk space available"

  - name: database_alerts
    interval: 30s
    rules:
      # Database Down
      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database is down"
          description: "PostgreSQL database is not responding"

      # High Connection Count
      - alert: HighDatabaseConnections
        expr: pg_stat_activity_count > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High database connection count"
          description: "Database connection count > 90"

      # Slow Queries
      - alert: SlowQueries
        expr: pg_slow_queries > 10
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow queries detected"
          description: "Multiple slow running queries detected"

  - name: deployment_alerts
    interval: 30s
    rules:
      # Deployment Rollback
      - alert: DeploymentUnstable
        expr: rate(http_requests_total{status=~"5.."}[2m]) > 0.1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Deployment appears unstable"
          description: "High error rate after recent deployment"
```

## 2. Grafana Setup

### Dashboards

Key dashboards to create:

```json
{
  "dashboard": {
    "title": "Store ERP - System Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "rate(node_cpu_seconds_total{mode=\"user\"}[5m])"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100"
          }
        ]
      },
      {
        "title": "Database Connections",
        "targets": [
          {
            "expr": "pg_stat_activity_count"
          }
        ]
      }
    ]
  }
}
```

## 3. AlertManager Configuration

```yaml
# monitoring/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '${SLACK_WEBHOOK_URL}'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

  routes:
    # Critical alerts
    - match:
        severity: critical
      receiver: 'pagerduty'
      group_wait: 0s
      repeat_interval: 30m

    # Warning alerts
    - match:
        severity: warning
      receiver: 'slack-warnings'
      repeat_interval: 2h

    # Info alerts
    - match:
        severity: info
      receiver: 'slack-info'
      repeat_interval: 24h

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts-warnings'
        color: 'warning'

  - name: 'slack-info'
    slack_configs:
      - channel: '#alerts-info'

  - name: 'pagerduty'
    pagerduty_configs:
      - routing_key: '${PAGERDUTY_ROUTING_KEY}'
        description: '{{ .GroupLabels.alertname }}'
        details:
          firing: '{{ template "pagerduty.default.instances" .Alerts.Firing }}'

inhibit_rules:
  # Inhibit warning if critical is already firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']

  # Inhibit info if warning is already firing
  - source_match:
      severity: 'warning'
    target_match:
      severity: 'info'
    equal: ['alertname', 'dev', 'instance']
```

## 4. Loki Logging Setup

```yaml
# Docker compose addition for Loki
services:
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki-config.yml:/etc/loki/local-config.yml
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yml

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./monitoring/promtail-config.yml:/etc/promtail/config.yml
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock
    command: -config.file=/etc/promtail/config.yml

volumes:
  loki_data:
```

## 5. Backend Instrumentation

### Flask Prometheus Integration

```python
# backend/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
from functools import wraps

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

database_connections = Gauge(
    'database_connections',
    'Number of active database connections'
)

cache_hits = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

def track_metrics(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
            status = 200
            return result
        except Exception as e:
            status = 500
            raise
        finally:
            duration = time.time() - start_time
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.endpoint
            ).observe(duration)
            http_requests_total.labels(
                method=request.method,
                endpoint=request.endpoint,
                status=status
            ).inc()
    return decorated_function

# Flask integration
from flask import Flask, request, Response

def init_metrics(app):
    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype='text/plain')

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown'
            ).observe(duration)
        
        http_requests_total.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()
        
        return response
```

## 6. Monitoring Best Practices

### Key Metrics to Monitor

```
Backend:
- Request rate (requests/second)
- Error rate (errors/second)
- Response time (p50, p95, p99)
- Active connections
- Database query time
- Cache hit rate

Database:
- Connection count
- Query execution time
- Slow query count
- Table size
- Index usage
- Replication lag

Infrastructure:
- CPU usage
- Memory usage
- Disk usage
- Network I/O
- Container status
- Service availability
```

### Alert Thresholds

```
CRITICAL:
- API down for 2+ minutes
- Error rate > 5%
- Disk space < 5%
- Database down
- Response time > 5 seconds

WARNING:
- Error rate > 1%
- Response time > 1 second
- CPU usage > 80%
- Memory usage > 85%
- Disk space < 15%
- Database connections > 90% of max
```

## 7. Dashboard Templates

Key dashboard metrics:
1. **System Overview**: Request rate, error rate, latency
2. **Database Performance**: Query times, connection count
3. **Infrastructure**: CPU, memory, disk, network
4. **Business Metrics**: Transactions, revenue, user activity
5. **Error Tracking**: Error rate, error types, stack traces

## 8. Log Analysis Queries

```promql
# Recent errors
{job="backend"} | "error"

# Slow requests
{job="backend"} | json | latency > 1000

# Authentication failures
{job="backend"} | "auth failed"

# Database errors
{job="backend"} | "database error"
```

## Deployment

```bash
# Deploy monitoring stack
docker compose -f docker-compose.monitoring.yml up -d

# Verify services
curl http://localhost:9090/-/healthy      # Prometheus
curl http://localhost:3000/api/health     # Grafana
curl http://localhost:9093/-/healthy      # AlertManager

# View dashboards
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# AlertManager: http://localhost:9093
```

---

Last Updated: January 31, 2026
