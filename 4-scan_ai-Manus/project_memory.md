# 🧠 Project Memory: Gaara Scan AI
## ذاكرة المشروع | Persistent Context for AI Assistants

**Version:** 1.0.0  
**Created:** 2026-01-17  
**Mode:** ADOPTION (Brownfield)

---

## 1. Project Identity

### Basic Information
- **Name:** Gaara Scan AI
- **Arabic Name:** نظام قاارا للكشف الذكي عن أمراض النباتات
- **Version:** 4.3.1
- **Status:** Production Ready (95%)
- **License:** Proprietary (Gaara Group & Manus AI)

### Mission Statement
> An integrated intelligent system that combines comprehensive farm management with plant disease diagnosis using cutting-edge AI technologies, providing solutions for farmers, agricultural engineers, and researchers with full Arabic and English support.

---

## 2. Technical Context

### Tech Stack (Canonical)
```
Frontend:    React 18 + Vite + Tailwind CSS
Backend:     FastAPI + SQLAlchemy + Alembic
Database:    PostgreSQL 16 + Redis 7
ML/AI:       YOLOv8 + PyTorch + TensorFlow + OpenCV
Infra:       Docker Compose + Nginx + Cloudflare
```

### Service Ports
| Service | Internal Port | External Port |
|---------|--------------|---------------|
| Frontend | 4501 | 4501 |
| Backend | 4001 | 4001 |
| ML Service | 4101 | 4101 |
| AI/Crawler | 4601 | 4601 |
| PostgreSQL | 8502 | - |
| Redis | 6379 | - |

### Container Names
```
scan_ai-Manus-frontend
scan_ai-Manus-backend
scan_ai-Manus-ml
scan_ai-Manus-ai
scan_ai-Manus-database
scan_ai-Manus-redis
```

---

## 3. User Preferences

### Language
- **Primary:** Arabic (RTL)
- **Secondary:** English (LTR)
- **Code Comments:** Both Arabic and English accepted

### UI Preferences
- **Theme:** Support both Light and Dark modes
- **Layout:** RTL-first design
- **Icons:** Lucide React library

### Code Style
- **Python:** PEP 8, Black formatter, isort imports
- **JavaScript:** ESLint with Airbnb config
- **Commits:** Conventional Commits format

---

## 4. Domain Knowledge

### Plant Diseases (40+)
The system detects and diagnoses over 40 plant diseases including:
- Early Blight (اللفحة المبكرة)
- Late Blight (اللفحة المتأخرة)
- Powdery Mildew (البياض الدقيقي)
- Downy Mildew (البياض الزغبي)
- Rust (الصدأ)
- Leaf Spot (تبقع الأوراق)
- Bacterial Wilt (الذبول البكتيري)
- And 33+ more...

### Trusted Data Sources (17)
**Academic:** PlantVillage, CABI, Cornell, UC IPM, ISC  
**Government:** EPPO, FAO, USDA, PaDIL  
**Arabic:** AOAD, ICARDA  
**Images:** Google, Bing, Unsplash, Flickr, Bugwood, iNaturalist

---

## 5. Known Issues & Warnings

### ⚠️ Legacy Code Warning
```
Directory: gaara_ai_integrated/
Status: DEPRECATED - Contains 150+ syntax errors
Action: DO NOT IMPORT from this directory
Recommendation: Archive and remove
```

### ⚠️ Database Files
```
SQLite files found (should be using PostgreSQL only):
- backend/data/gaara_scan_ai.db
- backend/data/gaara_scan.db
- backend/gaara_scan_ai.db
- backend/test.db
- gaara_scan_ai.db (root)

Action: These are likely development artifacts - ignore
```

### ⚠️ Test Failures
```
5 backend tests currently failing
Location: backend/tests/
Status: Needs investigation
```

---

## 6. Architectural Decisions

### ADR-001: Microservices over Monolith
**Date:** 2025-11  
**Decision:** Use microservices with Docker Compose  
**Rationale:** Separate ML inference from API for scalability  
**Consequences:** More complex deployment, but better resource isolation

### ADR-002: PostgreSQL over SQLite
**Date:** 2025-11  
**Decision:** Use PostgreSQL as primary database  
**Rationale:** Production-ready, better concurrency  
**Consequences:** Requires more setup, but handles scale

### ADR-003: React Context over Redux
**Date:** 2025-11  
**Decision:** Use React Context for state management  
**Rationale:** Simpler for current scale  
**Consequences:** May need to revisit at larger scale

### ADR-004: YOLOv8 for Detection
**Date:** 2025-12  
**Decision:** Use YOLOv8 for disease detection  
**Rationale:** Best accuracy/speed tradeoff  
**Consequences:** Requires GPU for production performance

---

## 7. Critical Paths

### Authentication Flow
```
User → Login → JWT Token → (Optional 2FA) → Access
               ↓
          Refresh Token → New Access Token
```

### Diagnosis Flow
```
Image Upload → ML Service (YOLO) → Disease Detection
                                        ↓
                              Knowledge Base Lookup
                                        ↓
                              Treatment Recommendations
```

### Crawler Flow
```
Scheduler → Source Selection → Web Crawl → Image Download
                                              ↓
                                    AI Analysis (OpenAI Vision)
                                              ↓
                                    Knowledge Base Update
```

---

## 8. Security Requirements

### Authentication
- JWT tokens (15 min access, 7 day refresh)
- 2FA (TOTP) mandatory for admins
- Account lockout after 5 failed attempts
- Password: 8+ chars, mixed case, number, special

### Authorization
- RBAC with roles: admin, user, agronomist, researcher
- Resource-level permissions
- API key authentication for services

### Infrastructure
- Cloudflare WAF + DDoS protection
- TLS 1.3 for all connections
- Rate limiting on all endpoints

---

## 9. Naming Conventions

### Files
```
Python:     snake_case.py
JavaScript: camelCase.js / PascalCase.jsx (components)
CSS:        kebab-case.css
```

### Database
```
Tables:     snake_case (plural: users, farms, crops)
Columns:    snake_case (user_id, created_at)
```

### API
```
Endpoints:  kebab-case (/api/v1/disease-detection)
Query:      snake_case (?page_size=20)
Body:       camelCase (JSON)
```

---

## 10. Quick Reference

### Start Development
```bash
cd D:\Ai_Project\4-scan_ai-Manus
docker-compose up -d --build
```

### Run Tests
```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd frontend && npm test
```

### Access Services
```
Frontend:   http://localhost:4501
Backend:    http://localhost:4001/docs
ML Service: http://localhost:4101/docs
Crawler:    http://localhost:4601/docs
```

### Key Files
```
Entry Points:
- backend/src/main.py
- frontend/main.jsx
- ml_service/main.py
- image_crawler/main.py

Configuration:
- docker-compose.yml
- backend/src/core/config.py
- frontend/vite.config.js

Documentation:
- CONSTITUTION.md
- gaara_scan_ai.spec.md
- todo.md
```

---

## 11. Contact & Ownership

### Repository
```
GitHub: github.com/hamfarid/gaara-Scan-system
```

### Team
- **Lead Developer:** @hamfarid
- **Organization:** Gaara Group & Manus AI

### Support
- **Issues:** GitHub Issues
- **Email:** support@gaara-scan-ai.com

---

**Last Updated:** 2026-01-17  
**Memory Version:** 1.0.0

*"This memory persists across sessions. Update it when context changes."*
