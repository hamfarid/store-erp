# YAML Files Reference - All Projects

Generated: 2026-01-03

## Overview

All projects configured with **Egypt Localization**:

- **TIMEZONE**: Africa/Cairo
- **LANGUAGE**: ar (Arabic)
- **CURRENCY**: EGP (Egyptian Pound)

---

## 📁 1. Test Projects

**Path**: `1-test_projects/global - V1.3 -13-12-2025/test/`

| File | Type | Purpose | Status |
|------|------|---------|--------|
| `docker-compose.yml` | Main | Web dashboard backend + frontend | ✅ Configured |
| `web-dashboard/docker-compose*.yml` | Alt | Alternative configs (4 files) | ✅ Configured |

**Ports**: Backend: 1001, Frontend: 1501

---

## 📁 2. Gold Price Predictor

**Path**: `2-gold-price-predictor/`

### Main Docker Compose Files

| File | Type | Purpose | Network | Status |
|------|------|---------|---------|--------|
| `docker-compose.yml` | **Main** | Full stack (6 services) | Ai_project | ✅ Configured |
| `docker-compose.ml.yml` | ML | ML services stack | Ai_project | ✅ Configured |
| `docker-compose.postgres.yml` | DB | PostgreSQL only | Ai_project | ✅ Configured |
| `docker-compose.monitoring.yml` | Monitoring | Prometheus + Grafana | Ai_project | ✅ Configured |
| `docker-compose.production.yml` | Production | Production deployment | Ai_project | ✅ Configured |

### ML Services Directory

| File | Type | Purpose | Services |
|------|------|---------|----------|
| `ml-services/docker-compose.yml` | ML Platform | Full ML stack | postgres, timescaledb, redis, mlflow |
| `ml-services/docker-compose.gpu.yml` | GPU | GPU-enabled ML | GPU containers |

### ML Backend Directory

| File | Type | Purpose |
|------|------|---------|
| `ml_backend/docker-compose.yml` | ML Backend | ML API server |

### Monitoring Directory

| File | Type | Purpose |
|------|------|---------|
| `monitoring/docker-compose.yml` | Monitoring | Prometheus, Grafana, Alertmanager |
| `monitoring/prometheus.yml` | Config | Prometheus configuration |
| `monitoring/alertmanager.yml` | Config | Alertmanager configuration |
| `monitoring/prometheus/prometheus.yml` | Config | Prometheus scrape targets |
| `monitoring/grafana/dashboards/dashboard.yml` | Config | Grafana dashboards |
| `monitoring/grafana/datasources/prometheus.yml` | Config | Grafana datasources |

### Templates

| File | Type | Purpose |
|------|------|---------|
| `templates/docker-compose.yml` | Template | Base template |
| `templates/ci.yml` | CI | GitHub Actions template |
| `workflows_templates/ci.yml` | CI | CI workflow template |
| `workflows_templates/cd.yml` | CD | CD workflow template |
| `docs/_config.yml` | Docs | Jekyll docs config |

**Ports**: Backend: 2001, Frontend: 2501, DB: 4502, ML: 2101, AI: 2601, Redis: 6372

---

## 📁 3. Zakat System

**Path**: `3-Zakat/Zakat_Clean/`

| File | Type | Purpose | Network | Status |
|------|------|---------|---------|--------|
| `docker-compose.yml` | **Main** | Full stack (4 services) | Ai_project | ✅ Configured |

**Ports**: Backend: 3001, Frontend: 3501, DB: 6502, Redis: 6373

---

## 📁 4. Scan AI Manus

**Path**: `4-scan_ai-Manus/`

### Main Docker Compose Files

| File | Type | Purpose | Network | Status |
|------|------|---------|---------|--------|
| `docker-compose.yml` | **Main** | Full stack (6 services) | Ai_project | ✅ Configured |
| `docker-compose.unified.yml` | Unified | 2-container setup | Ai_project | ✅ Configured |

### Docker Directory

| File | Type | Purpose |
|------|------|---------|
| `docker/docker-compose.yml` | Full Stack | API, Image Processor, Load Balancer, DB, Redis, Elasticsearch |
| `docker/docker-compose.swarm.yml` | Swarm | Docker Swarm deployment |
| `docker/prometheus.yml` | Config | Prometheus configuration |
| `docker/elasticsearch/config/elasticsearch.yml` | Config | Elasticsearch settings |
| `docker/kibana/config/kibana.yml` | Config | Kibana settings |
| `docker/prometheus/config/prometheus.yml` | Config | Prometheus scrape config |

### Subprojects

| File | Type | Purpose |
|------|------|---------|
| `gaara_ai_integrated/docker-compose.yml` | Integrated | AI integration stack |
| `clean_project/docker-compose.yml` | Clean | Clean version |
| `src/modules/image_search/docker-compose.yml` | Module | Image search module |
| `src/modules/internal_diagnosis/knowledge_base.yaml` | Config | Knowledge base config |

### Other Configs

| File | Type | Purpose |
|------|------|---------|
| `.cloudflare/config.yml` | Deploy | Cloudflare Pages config |
| `config/default.yaml` | Config | App default settings |
| `docs-site/_config.yml` | Docs | Jekyll docs config |

**Ports**: Backend: 4001, Frontend: 4501, DB: 8502, ML: 4101, AI: 4601, Redis: 6374

---

## 📁 5. Gaara ERP

**Path**: `5-gaara_erp/`

### Main Docker Compose Files

| File | Type | Purpose | Network | Status |
|------|------|---------|---------|--------|
| `docker-compose.yml` | **Main** | Full stack (6 services) | Ai_project | ✅ Configured |
| `docker-compose.dev.yml` | Dev | Development with hot reload | gaara_network_dev | Development |
| `docker-compose.prod.yml` | Prod | Production deployment | Separate | Production |
| `docker-compose.production.yml` | Prod | Production alt | Separate | Production |
| `docker-compose.monitoring.yml` | Monitoring | Prometheus + Grafana | Separate | Optional |
| `docker-compose.vault.yml` | Security | HashiCorp Vault | Separate | Security |
| `docker-compose.wsgi.yml` | WSGI | Gunicorn server | Separate | Production |

### Backend Directory

| File | Type | Purpose |
|------|------|---------|
| `backend/docker-compose.yml` | Backend | Backend-only stack |

### Monitoring Directory

| File | Type | Purpose |
|------|------|---------|
| `monitoring/docker-compose.monitoring.yml` | Monitoring | Full monitoring stack |
| `monitoring/prometheus.yml` | Config | Prometheus config |
| `monitoring/alertmanager.yml` | Config | Alert configuration |
| `monitoring/alert_rules.yml` | Config | Alert rules |
| `monitoring/grafana-datasources.yml` | Config | Grafana datasources |
| `monitoring/alerts/gaara-erp.yml` | Config | ERP-specific alerts |
| `monitoring/grafana/datasources/prometheus.yml` | Config | Datasource settings |

### Other Configs

| File | Type | Purpose |
|------|------|---------|
| `contracts/openapi.yaml` | API | OpenAPI specification |
| `templates/docker-compose.yml` | Template | Base template |
| `templates/ci.yml` | CI | CI workflow template |
| `scripts/dast/zap-config.yaml` | Security | OWASP ZAP config |
| `mkdocs.yml` | Docs | MkDocs documentation |

**Ports**: Backend: 5001, Frontend: 5501, DB: 10502, Redis: 6375

---

## 📁 6. Store System

**Path**: `6-store/`

### Main Docker Compose Files

| File | Type | Purpose | Network | Status |
|------|------|---------|---------|--------|
| `docker-compose.yml` | **Main** | Full stack (4 services) | Ai_project | ✅ Configured |
| `docker-compose.prod.yml` | Prod | Production deployment | Separate | Production |
| `docker-compose.production.yml` | Prod | Production alt | Separate | Production |
| `docker-compose.monitoring.yml` | Monitoring | Prometheus + Grafana | Separate | Optional |
| `docker-compose.vault.yml` | Security | HashiCorp Vault | Separate | Security |
| `docker-compose.wsgi.yml` | WSGI | Gunicorn server | Separate | Production |

### Backend Directory

| File | Type | Purpose |
|------|------|---------|
| `backend/docker-compose.yml` | Backend | Backend-only stack |

### Monitoring Directory

| File | Type | Purpose |
|------|------|---------|
| `monitoring/prometheus.yml` | Config | Prometheus config |
| `monitoring/alertmanager.yml` | Config | Alert configuration |
| `monitoring/alert_rules.yml` | Config | Alert rules |
| `monitoring/grafana-datasources.yml` | Config | Grafana datasources |
| `monitoring/grafana/datasources/prometheus.yml` | Config | Datasource settings |

### Other Configs

| File | Type | Purpose |
|------|------|---------|
| `contracts/openapi.yaml` | API | OpenAPI specification |
| `templates/docker-compose.yml` | Template | Base template |
| `templates/ci.yml` | CI | CI workflow template |
| `scripts/dast/zap-config.yaml` | Security | OWASP ZAP config |
| `mkdocs.yml` | Docs | MkDocs documentation |

**Ports**: Backend: 6001, Frontend: 6501, DB: 12502, Redis: 6376

---

## 📁 Root Nginx

**Path**: `E:\Ai_Project\`

| File | Type | Purpose | Status |
|------|------|---------|--------|
| `docker-compose.nginx.yml` | **Main** | Nginx Proxy + Portainer | ✅ Running |

**Ports**: HTTP: 80, HTTPS: 443, Config: 8181, Portainer: 9000/9443

---

## 📊 Summary Table - Main Docker Compose Files

| # | Project | Main File | Services | Network | Status |
|---|---------|-----------|----------|---------|--------|
| 0 | Nginx Proxy | `docker-compose.nginx.yml` | nginx, portainer | Ai_project | ✅ |
| 1 | Test | `1-test_projects/.../docker-compose.yml` | 2 | Ai_project | ✅ |
| 2 | Gold | `2-gold-price-predictor/docker-compose.yml` | 6 | Ai_project | ✅ |
| 3 | Zakat | `3-Zakat/Zakat_Clean/docker-compose.yml` | 4 | Ai_project | ✅ |
| 4 | Scan AI | `4-scan_ai-Manus/docker-compose.yml` | 6 | Ai_project | ✅ |
| 5 | ERP | `5-gaara_erp/docker-compose.yml` | 6 | Ai_project | ✅ |
| 6 | Store | `6-store/docker-compose.yml` | 4 | Ai_project | ✅ |

---

## 🔧 Additional YAML Files by Type

### Monitoring Stack Files (Not in main docker-compose)

| Project | File | Services |
|---------|------|----------|
| Gold | `monitoring/docker-compose.yml` | prometheus, grafana, alertmanager |
| Scan AI | `docker/docker-compose.yml` | elasticsearch, kibana, prometheus |
| ERP | `monitoring/docker-compose.monitoring.yml` | prometheus, grafana, node-exporter |

### ML/AI Stack Files (Not in main docker-compose)

| Project | File | Services |
|---------|------|----------|
| Gold | `ml-services/docker-compose.yml` | postgres, timescaledb, redis, mlflow |
| Gold | `ml-services/docker-compose.gpu.yml` | GPU-enabled services |
| Scan AI | `docker-compose.unified.yml` | gaara-main, gaara-ml-ai |

### Development Files

| Project | File | Purpose |
|---------|------|---------|
| ERP | `docker-compose.dev.yml` | Hot reload, dev DB |

### Production Files

| Project | File | Purpose |
|---------|------|---------|
| Gold | `docker-compose.production.yml` | Production config |
| ERP | `docker-compose.prod.yml` | Production config |
| ERP | `docker-compose.production.yml` | Production alt |
| Store | `docker-compose.prod.yml` | Production config |
| Store | `docker-compose.production.yml` | Production alt |

---

## 🌐 Port Assignment Reference

### Main Services

| # | Project | Backend | Frontend | Database | ML | AI/RAG | Redis |
|---|---------|---------|----------|----------|----|----|-------|
| 1 | test | 1001 | 1501 | - | - | - | - |
| 2 | gold | 2001 | 2501 | 4502 | 2101 | 2601 | 6372 |
| 3 | zakat | 3001 | 3501 | 6502 | - | - | 6373 |
| 4 | scan_ai | 4001 | 4501 | 8502 | 4101 | 4601 | 6374 |
| 5 | erp | 5001 | 5501 | 10502 | - | - | 6375 |
| 6 | store | 6001 | 6501 | 12502 | - | - | 6376 |

### Infrastructure Services

| Service | Port | Purpose |
|---------|------|---------|
| Nginx | 80 | HTTP Proxy |
| Nginx | 443 | HTTPS Proxy |
| Nginx | 8181 | Config Dashboard |
| Portainer | 9000 | Docker UI HTTP |
| Portainer | 9443 | Docker UI HTTPS |

### Monitoring Services (Optional)

| Service | Port | Project |
|---------|------|---------|
| Prometheus | 9090 | Gold, ERP |
| Grafana | 3000/3001 | Gold, ERP |
| Alertmanager | 9093 | Gold |
| Node Exporter | 9100 | ERP |

---

## 📝 .env Files Status

| Project | Path | Localization | Status |
|---------|------|--------------|--------|
| Gold | `2-gold-price-predictor/.env` | Africa/Cairo, ar, EGP | ✅ |
| Zakat | `3-Zakat/Zakat_Clean/.env` | Africa/Cairo, ar, EGP | ✅ |
| Scan AI | `4-scan_ai-Manus/.env` | Africa/Cairo, ar, EGP | ✅ |
| ERP | `5-gaara_erp/.env` | Africa/Cairo, ar, EGP | ✅ |
| Store | `6-store/.env` | Africa/Cairo, ar, EGP | ✅ |
| Store Backend | `6-store/backend/.env` | Local config | ✅ |

---

## 🚀 Quick Start Commands

```powershell
# Create network (if not exists)
docker network create Ai_project

# Start Nginx + Portainer
cd E:\Ai_Project
docker-compose -f docker-compose.nginx.yml up -d

# Start individual projects
cd "1-test_projects\global - V1.3 -13-12-2025\test"; docker-compose up -d
cd "2-gold-price-predictor"; docker-compose up -d
cd "3-Zakat\Zakat_Clean"; docker-compose up -d
cd "4-scan_ai-Manus"; docker-compose up -d
cd "5-gaara_erp"; docker-compose up -d
cd "6-store"; docker-compose up -d

# Start monitoring (optional)
cd "2-gold-price-predictor\monitoring"; docker-compose up -d
cd "5-gaara_erp\monitoring"; docker-compose -f docker-compose.monitoring.yml up -d
```

---

## ⚠️ Notes

1. **Main docker-compose.yml files** are configured for `Ai_project` network
2. **All compose files** now use `Ai_project` network (unified)
3. **Nginx Config Dashboard** available at http://localhost:8181
4. **Monitoring stacks** should be started separately if needed
5. All projects now use **Egypt localization** (Africa/Cairo, ar, EGP)
