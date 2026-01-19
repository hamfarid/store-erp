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

## �️ Management Tools

| Tool | Port | URL | Description |
|------|------|-----|-------------|
| Portainer | 9000, 9443 | <http://localhost:9000> | Docker Container Management |
| Nginx Gateway | 80, 443 | <http://localhost> | Unified Entry Point |

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

---

## 🐳 Container Names Convention

| # | Project | Backend | Frontend | Database | ML | AI/RAG | Redis |
|---|---------|---------|----------|----------|----|----|-------|
| 1 | test_projects | test-backend | test-frontend | - | - | - | - |
| 2 | gold-price-predictor | gold-price-predictor-backend | gold-price-predictor-frontend | gold-price-predictor-database | gold-price-predictor-ml | gold-price-predictor-ai | gold-price-predictor-redis |
| 3 | Zakat | zakat_backend | zakat_frontend | zakat_db | - | - | zakat_redis |
| 4 | scan_ai-Manus | scan_ai-Manus-backend | scan_ai-Manus-frontend | scan_ai-Manus-database | scan_ai-Manus-ml | scan_ai-Manus-ai | scan_ai-Manus-redis |
| 5 | gaara_erp | gaara_backend | gaara_frontend | gaara_db | - | - | gaara_redis |
| 6 | store | store_backend | store_frontend | store_database | - | - | store_redis |

---

## 📁 Environment Files Status

| # | Project | .env Path | Status |
|---|---------|-----------|--------|
| 1 | test_projects | N/A | ⬜ No env needed |
| 2 | gold-price-predictor | `.env` | ✅ Configured |
| 3 | Zakat | `Zakat_Clean/.env` | ✅ Created |
| 4 | scan_ai-Manus | `.env` | ✅ Configured |
| 5 | gaara_erp | `.env` | ✅ Configured |
| 6 | store | `.env`, `backend/.env` | ✅ Configured |

---

## 📋 Project Analysis Summary

### Project 1: test_projects

**Path:** `E:\Ai_Project\1-test_projects\global - V1.3 -13-12-2025\test`
**Status:** ✅ Configured for Ai_project network
**Services:**

- ✅ Backend (port 1001)
- ✅ Frontend (port 1501)
- ⬜ Database (not needed)
- ⬜ ML (not needed)
- ⬜ AI
- ⬜ Redis

---

### Project 2: gold-price-predictor ✅ CONFIGURED

**Path:** `E:\Ai_Project\2-gold-price-predictor`
**Tech Stack:** FastAPI Backend, React+Vite Frontend, PostgreSQL, Redis, ML (TensorFlow), AI/RAG
**Status:** Docker Compose configured, needs network update
**Services:**

- ✅ Backend (FastAPI) - Port 2001
- ✅ Frontend (React+Vite+Nginx) - Port 2501
- ✅ Database (PostgreSQL) - Port 4502
- ✅ ML Service (TensorFlow) - Port 2101
- ✅ AI/RAG Service - Port 2601
- ✅ Redis - Port 6379 → Should be 6372

---

### Project 3: Zakat

**Path:** `E:\Ai_Project\3-Zakat\Zakat_Clean`
**Tech Stack:** Flask Backend, React Frontend, PostgreSQL, Redis
**Current Ports:** Backend 3005, Frontend 3505, DB 5432, Redis 6379
**Services Needed:**

- ✅ Backend (Flask) - Change to 3001
- ✅ Frontend - Change to 3501
- ✅ Database - Change to 6502
- ⬜ ML Service - Add 3101
- ⬜ AI Service - Add 3601
- ✅ Redis - Change to 6373

---

### Project 4: scan_ai-Manus ✅ CONFIGURED

**Path:** `E:\Ai_Project\4-scan_ai-Manus`
**Tech Stack:** FastAPI Backend, React+Vite Frontend, PostgreSQL, Redis, ML (Disease Diagnosis), AI (Image Crawler)
**Status:** Already configured with Ai_project network
**Services:**

- ✅ Backend (FastAPI) - Port 4001
- ✅ Frontend (React+Vite) - Port 4501
- ✅ Database (PostgreSQL) - Port 8502 (internal)
- ✅ ML Service - Port 4101
- ✅ AI Service - Port 4601
- ✅ Redis - Exposed internally

---

### Project 5: gaara_erp

**Path:** `E:\Ai_Project\5-gaara_erp`
**Tech Stack:** Django Backend, React Frontend, PostgreSQL, Redis, Celery, Nginx
**Current Ports:** Backend 8000, Frontend 3000, Nginx 80/443
**Services Needed:**

- ✅ Backend (Django) - Change to 5001
- ✅ Frontend (React) - Change to 5501
- ✅ Database - Change to 10502
- ⬜ ML Service - Add 5101
- ⬜ AI Service - Add 5601
- ✅ Redis - Change to 6375
- ✅ Celery Worker
- ⬜ Celery Beat

---

### Project 6: store

**Path:** `E:\Ai_Project\6-store`
**Tech Stack:** Flask Backend, React Frontend, PostgreSQL, Redis, Nginx
**Current Ports:** Backend 5002, Frontend 5502, DB 5432, Nginx 80/443
**Services Needed:**

- ✅ Backend (Flask) - Change to 6001
- ✅ Frontend - Change to 6501
- ✅ Database - Change to 12502
- ⬜ ML Service - Add 6101
- ⬜ AI Service - Add 6601
- ✅ Redis - Change to 6376

---

## 🎯 Master Task List

### Phase 1: Network Setup (COMPLETED)

- [x] Create shared network `Ai_project`
- [x] Create Nginx proxy container
- [x] Configure main nginx.conf

### Phase 2: Project Configuration

#### Task 2.1: gold-price-predictor (Project 2) ✅ COMPLETE

- [x] Update docker-compose.yml with correct ports
- [x] Update container names
- [x] Configure Ai_project network
- [x] Update .env file
- [x] Fix Redis port to 6372
- [x] Validate docker-compose config
- [x] Enable Nginx config

#### Task 2.2: Zakat (Project 3) ✅ COMPLETE

- [x] Create/Update docker-compose.yml
  - [x] Change backend port 3005 → 3001
  - [x] Change frontend port 3505 → 3501
  - [x] Change database port → 6502
  - [x] Change Redis port → 6373
- [x] Update container names to zakat_* convention
- [x] Add Ai_project network
- [x] Update .env file
- [x] Validate docker-compose config
- [x] Enable Nginx config

#### Task 2.3: scan_ai-Manus (Project 4) ✅ COMPLETE

- [x] Docker-compose already configured
- [x] Container names correct
- [x] Ai_project network configured
- [x] docker-compose.unified.yml validated
- [x] Validate docker-compose config
- [x] Enable Nginx config

#### Task 2.4: gaara_erp (Project 5) ✅ COMPLETE

- [x] Update docker-compose.yml
  - [x] Change backend port 8000 → 5001
  - [x] Change frontend port 3000 → 5501
  - [x] Add database port 10502
  - [x] Change Redis port → 6375
- [x] Update container names to gaara_* convention
- [x] Replace gaara_network with Ai_project
- [x] Update .env file (added ENCRYPTION_KEY)
- [x] Celery configured
- [x] Validate docker-compose config
- [x] Enable Nginx config

#### Task 2.5: store (Project 6) ✅ COMPLETE

- [x] Update docker-compose.yml
  - [x] Change backend port 5002 → 6001
  - [x] Change frontend port 5502 → 6501
  - [x] Change database port → 12502
  - [x] Change Redis port → 6376
- [x] Update container names to store_* convention
- [x] Replace inventory_network with Ai_project
- [x] Validate docker-compose config
- [x] Enable Nginx config

#### Task 2.6: test_projects (Project 1) - Optional

- [ ] Create docker-compose.yml template
- [ ] Configure for development/testing

### Phase 3: Nginx Configuration ✅ COMPLETE

- [x] Create conf.d backup folder
- [x] Update all nginx configs with correct internal ports
- [x] Add port 8181 for configuration dashboard
- [x] Test nginx configuration
- [x] All project configs enabled

### Phase 4: Environment Files ✅ COMPLETE

- [x] All projects have .env configured
- [x] DATABASE_URL with correct host:port
- [x] REDIS_URL with correct port
- [x] Added ENCRYPTION_KEY to gaara_erp

### Phase 5: Testing & Validation

- [ ] Run e2e tests for each project
- [ ] Run Playwright tests
- [ ] Take screenshots
- [ ] Fix any errors found
- [ ] Document any remaining issues

---

## 🔧 Quick Reference: Docker Commands

```bash
# Create network
docker network create Ai_project

# Start Nginx proxy
cd E:\Ai_Project
docker-compose -f docker-compose.nginx.yml up -d

# Start a project
cd E:\Ai_Project\2-gold-price-predictor
docker-compose up -d

# View logs
docker logs -f gold-price-predictor-backend

# Reload Nginx
docker exec nginx-proxy nginx -s reload

# Check container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## 📁 Files to Create/Update Per Project

```
project-folder/
├── docker-compose.yml          # Update ports, network, container names
├── .env                         # Update connection strings
├── .env.example                 # Template for environment
├── backend/
│   └── Dockerfile              # Expose correct port
├── frontend/
│   └── Dockerfile              # Expose correct port
├── NGINX_SETUP_PROMPT.md       # AI agent instructions
└── docker-compose.override.yml # Optional: development overrides
```

---

## 🌐 Network Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Ai_project Network                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    nginx-proxy (80, 443)                      │  │
│  │  Forwards to all project ports based on configuration         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│     ┌────────────────────────┼────────────────────────┐            │
│     │                        │                        │            │
│     ▼                        ▼                        ▼            │
│  ┌─────────┐           ┌─────────┐              ┌─────────┐       │
│  │Project 2│           │Project 4│              │Project 5│       │
│  │Gold Pred│           │Scan AI  │              │Gaara ERP│       │
│  ├─────────┤           ├─────────┤              ├─────────┤       │
│  │BE: 2001 │           │BE: 4001 │              │BE: 5001 │       │
│  │FE: 2501 │           │FE: 4501 │              │FE: 5501 │       │
│  │DB: 4502 │           │DB: 8502 │              │DB:10502 │       │
│  │ML: 2101 │           │ML: 4101 │              │ML: 5101 │       │
│  │AI: 2601 │           │AI: 4601 │              │AI: 5601 │       │
│  └─────────┘           └─────────┘              └─────────┘       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✅ Status Legend

- ✅ Complete/Configured
- ⬜ Not Started
- 🔄 In Progress
- ❌ Error/Blocked

---

*Last Updated: January 2, 2026*
