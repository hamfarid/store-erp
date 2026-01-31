# 🏗️ Master Project Configuration - AI Projects

## 📊 Complete Port Mapping Table

### Port Formula

- **Backend** = (Project# × 1000) + 1
- **Frontend** = Backend + 500
- **Database** = Backend + Frontend (Internal 5432)
- **ML Port** = Backend + 100
- **AI Port** = Frontend + 100
- **Redis** = 6370 + Project#

---

## 🔌 Complete Port Assignment Table

| # | Project Name | Backend | Frontend | Database (Host) | Database (Internal) | ML | AI/RAG | Redis |
|---|--------------|---------|----------|-----------------|---------------------|----|----|-------|
| 1 | test_projects | 1001 | 1501 | 2502 | 5432 | 1101 | 1601 | 6371 |
| 2 | gold-price-predictor | 2001 | 2501 | 4502 | 5432 | 2101 | 2601 | 6372 |
| 3 | Zakat | 3001 | 3501 | 6502 | 5432 | 3101 | 3601 | 6373 |
| 4 | scan_ai-Manus | 4001 | 4501 | 8502 | 5432 | 4101 | 4601 | 6374 |
| 5 | gaara_erp | 5001 | 5501 | 10502 | 5432 | 5101 | 5601 | 6375 |
| 6 | store | 6001 | 6501 | 12502 | 5432 | 6101 | 6601 | 6376 |

---

## 🛠️ Management & Monitoring Tools

| Tool | Port | URL | Description |
|------|------|-----|-------------|
| Portainer | 9000, 9443 | <http://localhost:9000> | Docker Container Management |
| Nginx Gateway | 80, 443 | <http://localhost> | Unified Entry Point |
| Nginx Config | 8181 | <http://localhost:8181> | Nginx Configuration Dashboard |
| **Grafana** | 3000 | <http://localhost:3000> | Visualization & Dashboards |
| **Prometheus** | 9090 | <http://localhost:9090> | Metrics Collection |
| **Alertmanager** | 9093 | <http://localhost:9093> | Alert Handling |
| **cAdvisor** | 8088 | <http://localhost:8088> | Container Metrics |
| **Node Exporter** | 9100 | <http://localhost:9100> | Host Metrics |
| **Loki** | 3100 | <http://localhost:3100> | Log Aggregation |

---

## 🌐 Nginx Gateway Routes

All projects accessible via <http://localhost> with path-based routing:

| Route | Service | Description |
|-------|---------|-------------|
| `/test/` | Test Frontend | Test Projects Frontend |
| `/test/api/` | Test Backend | Test Projects API |
| `/gold/` | Gold Frontend | Gold Price Predictor Frontend |
| `/gold/api/` | Gold Backend | Gold Price Predictor API |
| `/gold/ml/` | Gold ML | Machine Learning Service |
| `/gold/ai/` | Gold AI/RAG | AI/RAG Service |
| `/zakat/` | Zakat Frontend | Zakat System Frontend |
| `/zakat/api/` | Zakat Backend | Zakat System API |
| `/scan/` | Scan Frontend | Scan AI Frontend |
| `/scan/api/` | Scan Backend | Scan AI API |
| `/scan/ml/` | Scan ML | Scan ML Service |
| `/scan/ai/` | Scan AI | Scan AI Service |
| `/erp/` | ERP Frontend | Gaara ERP Frontend |
| `/erp/api/` | ERP Backend | Gaara ERP API |
| `/store/` | Store Frontend | Store/Inventory Frontend |
| `/store/api/` | Store Backend | Store/Inventory API |
| `/portainer/` | Portainer | Docker Management |
| `/grafana/` | Grafana | Monitoring Dashboard |
| `/prometheus/` | Prometheus | Metrics Collection |
| `/alertmanager/` | Alertmanager | Alert Management |

---

## 🔗 Direct Access Ports

| Port | Project | Description |
|------|---------|-------------|
| 8080 | Gold Price Predictor | Direct access to Gold project |
| 8081 | Zakat | Direct access to Zakat project |
| 8082 | Scan AI | Direct access to Scan AI project |
| 8083 | Gaara ERP | Direct access to ERP project |
| 8084 | Store | Direct access to Store project |
| 8085 | Test Projects | Direct access to Test project |

---

## 🐳 Container Names Convention

| # | Project | Backend | Frontend | Database | ML | AI/RAG | Redis |
|---|---------|---------|----------|----------|----|----|-------|
| 1 | test_projects | test-backend | test-frontend | - | - | - | - |
| 2 | gold-price-predictor | gold-price-predictor-backend | gold-price-predictor-frontend | gold-price-predictor-database | gold-price-predictor-ml | gold-price-predictor-ai | gold-price-predictor-redis |
| 3 | Zakat | zakat-backend | zakat-frontend | zakat-postgres | - | - | zakat-redis |
| 4 | scan_ai-Manus | scan_ai-Manus-backend | scan_ai-Manus-frontend | scan_ai-Manus-database | scan_ai-Manus-ml | scan_ai-Manus-ai | scan_ai-Manus-redis |
| 5 | gaara_erp | gaara_backend | gaara_frontend | gaara_db | - | - | gaara_redis |
| 6 | store | store_backend | store_frontend | store_database | - | - | store_redis |

---

## 📈 Monitoring Stack Components

### Grafana (Port 3000)
- **Default Login**: admin / admin123
- **Pre-configured Dashboards**:
  - AI Projects Overview
  - Container Metrics
  - Host Metrics
- **Data Sources**:
  - Prometheus (metrics)
  - Loki (logs)
  - Alertmanager (alerts)

### Prometheus (Port 9090)
- **Scrape Interval**: 15s
- **Retention**: 30 days
- **Targets**: All project backends, frontends, ML, and AI services
- **Alert Rules**: Defined in `/monitoring/prometheus/alerts/`

### Alertmanager (Port 9093)
- **Routes**: Project-specific and severity-based
- **Receivers**: Webhook-based (configurable for email/Slack)
- **Inhibition Rules**: Prevent alert floods

### Loki (Port 3100)
- **Log Retention**: 30 days
- **Sources**: All Docker containers

### cAdvisor (Port 8088)
- **Metrics**: Container CPU, Memory, Network, Disk

### Node Exporter (Port 9100)
- **Metrics**: Host CPU, Memory, Disk, Network

---

## 📁 Environment Files Status

| # | Project | .env Path | Status |
|---|---------|-----------|--------|
| 1 | test_projects | N/A | ⬜ No env needed |
| 2 | gold-price-predictor | `.env` | ✅ Configured |
| 3 | Zakat | `Zakat_Clean/.env` | ✅ Configured |
| 4 | scan_ai-Manus | `.env` | ✅ Configured |
| 5 | gaara_erp | `.env` | ✅ Configured |
| 6 | store | `.env`, `backend/.env` | ✅ Configured |

---

## 🔧 Quick Reference: Docker Commands

```bash
# Create network (if not exists)
docker network create Ai_project

# Start Nginx proxy and monitoring stack
cd D:\Ai_Project
docker-compose -f docker-compose.nginx.yml up -d

# Start a project
cd D:\Ai_Project\2-gold-price-predictor
docker-compose up -d

# View logs
docker logs -f gold-price-predictor-backend

# Reload Nginx
docker exec nginx-proxy nginx -s reload

# Check container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# View Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check Alertmanager alerts
curl http://localhost:9093/api/v2/alerts
```

---

## 🌐 Network Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Ai_project Network                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    nginx-proxy (80, 443, 8181)                         │ │
│  │         + Direct Ports: 8080, 8081, 8082, 8083, 8084, 8085             │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│     ┌──────────────────────────────┼──────────────────────────┐             │
│     │                              │                          │             │
│     ▼                              ▼                          ▼             │
│  ┌─────────────┐            ┌─────────────┐            ┌─────────────┐     │
│  │ Project 2   │            │ Project 4   │            │ Project 5   │     │
│  │ Gold Pred   │            │ Scan AI     │            │ Gaara ERP   │     │
│  ├─────────────┤            ├─────────────┤            ├─────────────┤     │
│  │ BE: 2001    │            │ BE: 4001    │            │ BE: 5001    │     │
│  │ FE: 2501    │            │ FE: 4501    │            │ FE: 5501    │     │
│  │ DB: 4502    │            │ DB: 8502    │            │ DB: 10502   │     │
│  │ ML: 2101    │            │ ML: 4101    │            │             │     │
│  │ AI: 2601    │            │ AI: 4601    │            │             │     │
│  └─────────────┘            └─────────────┘            └─────────────┘     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     MONITORING STACK                                  │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │  Prometheus (9090) ─► Grafana (3000)                                 │   │
│  │  Alertmanager (9093)                                                 │   │
│  │  Loki (3100) ─► Promtail                                            │   │
│  │  cAdvisor (8088) | Node Exporter (9100)                             │   │
│  │  Portainer (9000, 9443)                                             │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ✅ Status Legend

- ✅ Complete/Configured
- ⬜ Not Started
- 🔄 In Progress
- ❌ Error/Blocked

---

*Last Updated: January 19, 2026*
