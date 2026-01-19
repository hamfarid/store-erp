# Store ERP - Monitoring Stack

## Overview

This monitoring stack provides comprehensive observability for the Store ERP system:

- **Prometheus** - Metrics collection and storage
- **Grafana** - Visualization and dashboards
- **AlertManager** - Alert routing and notifications
- **Loki** - Log aggregation
- **Promtail** - Log collection agent
- **Node Exporter** - Host metrics
- **cAdvisor** - Container metrics

## Quick Start

```bash
# Start the monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Check status
docker-compose -f docker-compose.monitoring.yml ps

# View logs
docker-compose -f docker-compose.monitoring.yml logs -f
```

## Access URLs

| Service | URL | Default Credentials |
|---------|-----|---------------------|
| Grafana | http://localhost:3000 | admin / admin123 |
| Prometheus | http://localhost:9090 | - |
| AlertManager | http://localhost:9093 | - |
| Loki | http://localhost:3100 | - |

## Configuration

### Environment Variables

Create a `.env` file with the following:

```bash
GRAFANA_PASSWORD=your-secure-password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
SMTP_PASSWORD=your-smtp-password
```

### Adding Custom Dashboards

1. Create JSON dashboard file in `grafana/dashboards/`
2. Restart Grafana or wait for auto-reload (30s)

### Alert Configuration

1. Edit alert rules in `prometheus/alerts/`
2. Configure receivers in `alertmanager/alertmanager.yml`
3. Reload configuration: `curl -X POST http://localhost:9090/-/reload`

## Metrics Available

### Application Metrics

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `auth_failed_logins_total` - Failed login attempts
- `db_query_duration_seconds` - Database query latency

### Infrastructure Metrics

- `node_cpu_seconds_total` - CPU usage
- `node_memory_MemAvailable_bytes` - Available memory
- `node_filesystem_avail_bytes` - Disk space
- `container_cpu_usage_seconds_total` - Container CPU
- `container_memory_usage_bytes` - Container memory

## Alert Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| critical | Service down, data loss risk | Immediate |
| warning | Performance degradation | < 1 hour |
| info | Informational | Next business day |

## Backup & Restore

### Backup Grafana

```bash
# Export dashboards
docker exec store_grafana grafana-cli admin export-datasources > datasources-backup.json

# Backup volume
docker run --rm -v store_grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup.tar.gz /data
```

### Backup Prometheus

```bash
# Snapshot via API
curl -X POST http://localhost:9090/api/v1/admin/tsdb/snapshot
```

## Troubleshooting

### Prometheus not scraping targets

1. Check target status: http://localhost:9090/targets
2. Verify network connectivity between containers
3. Check firewall rules

### Grafana dashboard not loading

1. Check datasource connectivity
2. Verify Prometheus is running
3. Check Grafana logs: `docker logs store_grafana`

### Alerts not firing

1. Check Prometheus rules: http://localhost:9090/rules
2. Verify AlertManager config
3. Test notification channels manually

## Maintenance

### Regular Tasks

- Weekly: Review alert history
- Monthly: Update container images
- Quarterly: Review retention policies

### Log Rotation

Loki automatically manages log retention. Default: 744 hours (31 days)

## Security Notes

1. Change default Grafana password immediately
2. Use secrets management for credentials
3. Restrict network access to monitoring endpoints
4. Enable TLS for production
