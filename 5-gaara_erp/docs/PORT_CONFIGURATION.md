# Gaara ERP v12 - Port Configuration

## From Nginx Configuration (D:\Ai_Project\nginx)

### Gaara ERP Ports

| Service | Port | Container Name | Description |
|---------|------|----------------|-------------|
| **Backend** | 5001 | gaara_backend | Django REST API |
| **Frontend** | 5501 | gaara_frontend | React/Vite UI |
| **Database** | 10502 | gaara_db | PostgreSQL |
| **Redis** | 6375 | gaara_redis | Cache/Celery |
| **ML Service** | 5101 | gaara_erp-ml | Machine Learning |
| **AI Service** | 5601 | gaara_erp-ai | AI/RAG Service |

### Nginx Proxy Routes

| Path | Target | Description |
|------|--------|-------------|
| `/erp/` | gaara_frontend:80 | Frontend application |
| `/erp/api/` | gaara_backend:8000 | Backend API |

### Full Port Mapping (All Projects)

| Project | Backend | Frontend | Database | ML | AI/RAG | Redis |
|---------|---------|----------|----------|-----|--------|-------|
| Test | 1001 | 1501 | - | - | - | - |
| Gold | 2001 | 2501 | 4502 | 2101 | 2601 | 6372 |
| Zakat | 3001 | 3501 | 6502 | - | - | 6373 |
| Scan AI | 4001 | 4501 | 8502 | 4101 | 4601 | 6374 |
| **Gaara ERP** | **5001** | **5501** | **10502** | **5101** | **5601** | **6375** |
| Store | 6001 | 6501 | 12502 | - | - | 6376 |

### Infrastructure Ports

| Service | Port | Purpose |
|---------|------|---------|
| Nginx HTTP | 80 | Main Proxy |
| Nginx HTTPS | 443 | Secure Proxy |
| Nginx Config | 8181 | Config Dashboard |
| Portainer HTTP | 9000 | Docker UI |
| Portainer HTTPS | 9443 | Docker UI Secure |

### Development vs Production

#### Development (Current)
```bash
# Backend
cd gaara_erp && python manage.py runserver 5001

# Frontend
cd gaara-erp-frontend && pnpm dev --port 5501
```

#### Production (Docker)
```bash
docker-compose up -d
# Backend:  http://localhost:5001   (gunicorn)
# Frontend: http://localhost:5501   (nginx)
# Database: http://localhost:10502  (PostgreSQL)
# Redis:    http://localhost:6375   (Redis)
```

### Environment Variables

```env
# Backend
DJANGO_PORT=5001
DATABASE_PORT=10502
REDIS_PORT=6375
DATABASE_URL=postgresql://gaara:gaara@localhost:10502/gaara_erp

# Frontend
VITE_PORT=5501
VITE_API_URL=http://localhost:5001/api

# Docker Network
NETWORK_NAME=Ai_project
```

---
*Configuration extracted from: D:\Ai_Project\nginx\conf.d.backup\gaara_erp.conf*
*Updated: 2026-01-16*
