# PROMPT 100 — System Health Check (v26.0.2 Diamond 32)

## Purpose
Automated health check across all system components — database, services, APIs, containers, and AI pipelines.

## Health Check Targets
1. **Database**: Connection pool, query latency, replication lag
2. **Redis**: Memory usage, connection count, eviction rate
3. **API Endpoints**: Response time, error rate, throughput
4. **Docker Containers**: Status, CPU/memory, restart count
5. **AI Services**: Model inference latency, queue depth, GPU utilization
6. **Disk/Storage**: Available space, inode usage, backup age

## Implementation
- Endpoint: `GET /api/v1/health`
- Returns: JSON with per-component status (healthy/degraded/down)
- Frequency: Every 60 seconds via monitoring stack
- Alert on: Any component reporting `down` for > 2 checks
- Dashboard: Grafana (see `infrastructure/monitoring/`)

## Integration
- Links to `rules/ml/POLICY-alerting-escalation.yaml` for alert routing
- Links to `prompts/83_monitoring_and_alerts.md` for alert configuration
