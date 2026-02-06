# 🎯 Monitoring Setup Guide

## Overview

Comprehensive monitoring stack for Gaara Scan AI system using:
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **AlertManager** - Alert routing
- **Loki** - Log aggregation
- **Jaeger** - Distributed tracing

## Quick Start

### 1. Start Monitoring Stack
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

### 2. Access Dashboards

| Service | URL | Default Credentials |
|---------|-----|---------------------|
| Grafana | http://localhost:3000 | admin/admin |
| Prometheus | http://localhost:9090 | - |
| AlertManager | http://localhost:9093 | - |
| Jaeger UI | http://localhost:16686 | - |

### 3. Configure Data Sources in Grafana

Data sources are auto-configured via provisioning. Verify at:
- Grafana → Configuration → Data Sources

## Components

### Prometheus (Port 9090)
- Scrapes metrics every 15 seconds
- 30-day data retention
- Alert evaluation every 15 seconds

**Targets:**
- Backend API (port 8000)
- Frontend (port 80)
- PostgreSQL (via postgres-exporter:9187)
- Redis (via redis-exporter:9121)
- Node metrics (via node-exporter:9100)
- Container metrics (via cadvisor:8080)

### Grafana (Port 3000)
**Pre-configured dashboards:**
1. System Overview
2. Application Performance
3. Database Metrics
4. Container Metrics
5. API Analytics

### AlertManager (Port 9093)
**Alert Routing:**
- Critical → Slack + Email + PagerDuty
- Warning → Slack

**Configure webhooks in:**
- `monitoring/alertmanager/alertmanager.yml`

### Loki (Port 3100)
- Log aggregation from all containers
- Integrated with Grafana for log exploration

### Jaeger (Port 16686)
- Distributed tracing
- Request flow visualization
- Performance bottleneck identification

## Key Metrics

### Application Metrics
```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Response time (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Active connections
sum(http_active_connections)
```

### Database Metrics
```promql
# Connection pool usage
pg_stat_activity_count / pg_settings_max_connections * 100

# Query duration
rate(pg_stat_statements_mean_time_seconds[5m])

# Lock waits
pg_stat_database_conflicts_total
```

### System Metrics
```promql
# CPU usage
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk usage
(node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100
```

## Alert Rules

### Critical Alerts
- Instance Down (>5 min)
- High Error Rate (>5%)
- Disk Space <10%
- Database Connection Pool >90%

### Warning Alerts
- High CPU (>80% for 10 min)
- High Memory (>85% for 10 min)
- Slow API Response (>2s p95)
- Disk Space <20%

## Custom Dashboards

### Import Dashboards
1. Go to Grafana → Dashboards → Import
2. Enter dashboard ID or upload JSON

**Recommended Dashboards:**
- Node Exporter Full: `1860`
- Docker Monitoring: `893`
- PostgreSQL: `9628`
- Redis: `11835`

## Instrumentation

### Backend (Python/FastAPI)
```python
from prometheus_client import Counter, Histogram, Gauge
from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

# Custom metrics
request_count = Counter('app_requests_total', 'Total requests')
request_duration = Histogram('app_request_duration_seconds', 'Request duration')
active_users = Gauge('app_active_users', 'Active users')
```

### Frontend (JavaScript)
```javascript
// web-vitals
import {getCLS, getFID, getFCP, getLCP, getTTFB} from 'web-vitals';

function sendToAnalytics(metric) {
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify(metric)
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

## Log Queries

### Loki Query Examples
```logql
# All logs from backend
{job="containerlogs", image_name="gaara-backend"}

# Error logs only
{job="containerlogs"} |= "ERROR"

# Slow queries
{job="containerlogs"} |~ "duration.*[5-9][0-9]{3}ms"

# Authentication failures
{job="containerlogs"} |~ "authentication.*failed"
```

## Performance Tuning

### Prometheus
```yaml
# Increase retention
--storage.tsdb.retention.time=90d

# Increase memory
--storage.tsdb.retention.size=10GB

# Enable remote write (for long-term storage)
remote_write:
  - url: https://prometheus-remote-storage/api/v1/write
```

### Grafana
- Enable caching
- Use query optimizer
- Set appropriate refresh intervals
- Use templating for reusable dashboards

## Troubleshooting

### Prometheus Not Scraping Targets
```bash
# Check targets status
curl http://localhost:9090/targets

# View scrape errors
docker logs gaara_prometheus

# Test endpoint manually
curl http://backend:8000/metrics
```

### Grafana Not Showing Data
1. Verify data source connection
2. Check Prometheus is receiving metrics
3. Verify time range in Grafana
4. Check query syntax

### High Memory Usage
```bash
# Check container stats
docker stats

# Adjust retention
# Edit prometheus.yml: storage.tsdb.retention.time
```

## Backup & Restore

### Prometheus Data
```bash
# Backup
docker cp gaara_prometheus:/prometheus ./prometheus-backup

# Restore
docker cp ./prometheus-backup/. gaara_prometheus:/prometheus
```

### Grafana Dashboards
```bash
# Export all dashboards
curl -H "Authorization: Bearer $API_KEY" \
  http://localhost:3000/api/search?query=& \
  | jq -r '.[].uid' \
  | xargs -I {} curl -H "Authorization: Bearer $API_KEY" \
    http://localhost:3000/api/dashboards/uid/{} > dashboard-{}.json

# Import dashboard
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @dashboard.json \
  http://localhost:3000/api/dashboards/db
```

## Security

### Enable Authentication
```yaml
# Prometheus
--web.enable-admin-api
--web.config.file=/etc/prometheus/web.yml

# Grafana
environment:
  - GF_AUTH_ANONYMOUS_ENABLED=false
  - GF_AUTH_BASIC_ENABLED=true
```

### SSL/TLS
```yaml
# Use reverse proxy (Nginx/Traefik)
server {
  listen 443 ssl;
  server_name grafana.example.com;
  
  location / {
    proxy_pass http://grafana:3000;
  }
}
```

## Maintenance

### Daily
- [ ] Check alert inbox
- [ ] Review error logs
- [ ] Monitor disk space

### Weekly
- [ ] Review performance metrics
- [ ] Check for metric cardinality issues
- [ ] Update alert thresholds if needed

### Monthly
- [ ] Review and optimize queries
- [ ] Clean up old dashboards
- [ ] Update exporters
- [ ] Rotate credentials

---

**Documentation:** [Prometheus](https://prometheus.io/docs/) | [Grafana](https://grafana.com/docs/) | [Loki](https://grafana.com/docs/loki/)
