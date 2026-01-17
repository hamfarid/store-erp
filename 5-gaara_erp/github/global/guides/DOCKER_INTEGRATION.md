# Docker Integration Guide

دليل شامل لتكامل Docker في المشاريع مع أفضل الممارسات الأمنية.

---

## 📋 المحتويات

1. [المتطلبات الأساسية](#المتطلبات-الأساسية)
2. [Dockerfile Best Practices](#dockerfile-best-practices)
3. [Docker Compose Setup](#docker-compose-setup)
4. [Multi-Stage Builds](#multi-stage-builds)
5. [Security Hardening](#security-hardening)
6. [Performance Optimization](#performance-optimization)
7. [Development Workflow](#development-workflow)
8. [Production Deployment](#production-deployment)

---

## المتطلبات الأساسية

### التثبيت

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# إعادة تسجيل الدخول لتفعيل المجموعة
```

#### macOS
```bash
# باستخدام Homebrew
brew install --cask docker
```

#### Windows
```powershell
# تنزيل Docker Desktop من
# https://www.docker.com/products/docker-desktop
```

### التحقق من التثبيت
```bash
docker --version
docker-compose --version
```

---

## Dockerfile Best Practices

### 1. Frontend (React/Next.js)

```dockerfile
# FILE: Dockerfile.frontend | PURPOSE: Frontend production build | OWNER: DevOps | LAST-AUDITED: 2025-10-28

# ========================================
# Stage 1: Dependencies
# ========================================
FROM node:20-alpine AS deps

# تثبيت libc6-compat للتوافق
RUN apk add --no-cache libc6-compat

WORKDIR /app

# نسخ package files فقط للاستفادة من cache
COPY package.json pnpm-lock.yaml* ./

# تثبيت pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# تثبيت dependencies
RUN pnpm install --frozen-lockfile

# ========================================
# Stage 2: Builder
# ========================================
FROM node:20-alpine AS builder

WORKDIR /app

# نسخ dependencies من المرحلة السابقة
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# تعطيل telemetry
ENV NEXT_TELEMETRY_DISABLED 1

# Build
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm build

# ========================================
# Stage 3: Runner (Production)
# ========================================
FROM node:20-alpine AS runner

WORKDIR /app

# إنشاء مستخدم غير root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# نسخ الملفات الضرورية فقط
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# التبديل للمستخدم غير root
USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

### 2. Backend (Python/FastAPI)

```dockerfile
# FILE: Dockerfile.backend | PURPOSE: Backend production build | OWNER: DevOps | LAST-AUDITED: 2025-10-28

# ========================================
# Stage 1: Builder
# ========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# تثبيت build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# نسخ requirements
COPY requirements.txt .

# إنشاء virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ========================================
# Stage 2: Runner (Production)
# ========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# إنشاء مستخدم غير root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# نسخ virtual environment
COPY --from=builder /opt/venv /opt/venv

# تفعيل virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# نسخ الكود
COPY --chown=appuser:appuser . .

# التبديل للمستخدم غير root
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Database (PostgreSQL)

```dockerfile
# FILE: Dockerfile.postgres | PURPOSE: PostgreSQL with extensions | OWNER: DBA | LAST-AUDITED: 2025-10-28

FROM postgres:15-alpine

# تثبيت extensions
RUN apk add --no-cache \
    postgresql-contrib \
    postgresql-plpython3

# نسخ init scripts
COPY ./db/init/ /docker-entrypoint-initdb.d/

# إعدادات أمان
RUN chmod 0700 /docker-entrypoint-initdb.d

EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD pg_isready -U ${POSTGRES_USER:-postgres} || exit 1
```

---

## Docker Compose Setup

### docker-compose.yml (Development)

```yaml
# FILE: docker-compose.yml | PURPOSE: Development environment | OWNER: DevOps | LAST-AUDITED: 2025-10-28

version: '3.9'

services:
  # ========================================
  # Frontend
  # ========================================
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
      target: development
    container_name: app_frontend_dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    environment:
      - NODE_ENV=development
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - app_network
    restart: unless-stopped

  # ========================================
  # Backend
  # ========================================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
      target: development
    container_name: app_backend_dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - /app/__pycache__
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env.development
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app_network
    restart: unless-stopped

  # ========================================
  # PostgreSQL
  # ========================================
  postgres:
    image: postgres:15-alpine
    container_name: app_postgres_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - app_network
    restart: unless-stopped

  # ========================================
  # Redis
  # ========================================
  redis:
    image: redis:7-alpine
    container_name: app_redis_dev
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass redis_password
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - app_network
    restart: unless-stopped

  # ========================================
  # Nginx (Reverse Proxy)
  # ========================================
  nginx:
    image: nginx:alpine
    container_name: app_nginx_dev
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.dev.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app_network
    restart: unless-stopped

# ========================================
# Networks
# ========================================
networks:
  app_network:
    driver: bridge

# ========================================
# Volumes
# ========================================
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### docker-compose.prod.yml (Production)

```yaml
# FILE: docker-compose.prod.yml | PURPOSE: Production environment | OWNER: DevOps | LAST-AUDITED: 2025-10-28

version: '3.9'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: runner
    container_name: app_frontend_prod
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=${API_URL}
    env_file:
      - .env.production
    depends_on:
      - backend
    networks:
      - app_network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: runner
    container_name: app_backend_prod
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    env_file:
      - .env.production
    depends_on:
      - postgres
      - redis
    networks:
      - app_network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M

  postgres:
    image: postgres:15-alpine
    container_name: app_postgres_prod
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    networks:
      - app_network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G

  redis:
    image: redis:7-alpine
    container_name: app_redis_prod
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    networks:
      - app_network
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  nginx:
    image: nginx:alpine
    container_name: app_nginx_prod
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app_network
    restart: always

networks:
  app_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

---

## Multi-Stage Builds

### مثال متقدم (Full-Stack)

```dockerfile
# FILE: Dockerfile | PURPOSE: Full-stack multi-stage build | OWNER: DevOps | LAST-AUDITED: 2025-10-28

# ========================================
# Base Stage
# ========================================
FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat
WORKDIR /app

# ========================================
# Dependencies Stage
# ========================================
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install --frozen-lockfile

# ========================================
# Development Stage
# ========================================
FROM base AS development
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["pnpm", "dev"]

# ========================================
# Builder Stage
# ========================================
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN corepack enable && pnpm build

# ========================================
# Production Stage
# ========================================
FROM base AS production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV NODE_ENV production

HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

---

## Security Hardening

### 1. استخدام مستخدم غير root

```dockerfile
# إنشاء مستخدم
RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 appuser

# التبديل للمستخدم
USER appuser
```

### 2. Scan للثغرات الأمنية

```bash
# باستخدام Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image your-image:latest

# باستخدام Snyk
snyk container test your-image:latest
```

### 3. إعدادات Docker Daemon

```json
{
  "userns-remap": "default",
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp.json",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 4. Docker Compose Security

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp
```

---

## Performance Optimization

### 1. Layer Caching

```dockerfile
# ❌ سيء - يعيد build كل شيء عند تغيير الكود
COPY . .
RUN npm install
RUN npm build

# ✅ جيد - يستفيد من cache
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build
```

### 2. .dockerignore

```
# FILE: .dockerignore | PURPOSE: Exclude unnecessary files | OWNER: DevOps | LAST-AUDITED: 2025-10-28

node_modules
.next
.git
.gitignore
README.md
.env*
!.env.example
*.log
.DS_Store
coverage
.vscode
.idea
dist
build
tmp
temp
```

### 3. BuildKit

```bash
# تفعيل BuildKit
export DOCKER_BUILDKIT=1

# Build مع cache
docker build --cache-from=myapp:latest -t myapp:new .
```

---

## Development Workflow

### الأوامر الأساسية

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Logs
docker-compose logs -f [service]

# Stop
docker-compose down

# Clean
docker-compose down -v --remove-orphans
```

### Hot Reload Setup

```yaml
# docker-compose.dev.yml
services:
  frontend:
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    environment:
      - WATCHPACK_POLLING=true
```

---

## Production Deployment

### 1. Build Production Images

```bash
# Build
docker-compose -f docker-compose.prod.yml build

# Tag
docker tag app_frontend:latest registry.example.com/app_frontend:v1.0.0
docker tag app_backend:latest registry.example.com/app_backend:v1.0.0

# Push
docker push registry.example.com/app_frontend:v1.0.0
docker push registry.example.com/app_backend:v1.0.0
```

### 2. Deploy

```bash
# Pull
docker-compose -f docker-compose.prod.yml pull

# Up
docker-compose -f docker-compose.prod.yml up -d

# Health Check
docker-compose -f docker-compose.prod.yml ps
```

### 3. Backup

```bash
# Backup Database
docker exec app_postgres_prod pg_dump -U postgres appdb > backup_$(date +%Y%m%d).sql

# Backup Volumes
docker run --rm -v app_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz /data
```

---

## الخلاصة

### ✅ Best Practices

1. **Multi-stage builds** - تقليل حجم الصورة
2. **Non-root user** - تحسين الأمان
3. **Health checks** - مراقبة الصحة
4. **Layer caching** - تسريع البناء
5. **.dockerignore** - استبعاد الملفات غير الضرورية
6. **Security scanning** - فحص الثغرات
7. **Resource limits** - تحديد الموارد
8. **Logging** - تسجيل منظم

### 📝 Checklist

- [ ] Dockerfile مُحسّن مع multi-stage
- [ ] مستخدم غير root
- [ ] Health checks مُفعّلة
- [ ] .dockerignore موجود
- [ ] Security scan يمر
- [ ] Resource limits محددة
- [ ] Logging مُعد
- [ ] Backup strategy موجودة

---

**آخر تحديث:** 2025-10-28  
**الإصدار:** 1.0.0

