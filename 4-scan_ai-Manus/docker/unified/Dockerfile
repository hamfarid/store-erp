# ==========================================
# Unified Container - Gaara Scan AI v4.3.1
# Backend + Frontend + SQLite Database
# ==========================================

# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend-build

COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps

COPY frontend/ ./
RUN npm run build

# Stage 2: Build Backend dependencies
FROM python:3.11-slim AS backend-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ pkg-config libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Stage 3: Production
FROM python:3.11-slim AS production

ARG BUILD_DATE
ARG VERSION=4.3.1

LABEL org.opencontainers.image.title="Gaara Scan AI Unified" \
      org.opencontainers.image.description="Unified container: Backend + Frontend + SQLite" \
      org.opencontainers.image.version="${VERSION}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend \
    PATH="/opt/venv/bin:$PATH" \
    DATABASE_URL=sqlite:///./data/gaara_scan_ai.db \
    ENVIRONMENT=production \
    DEBUG=false \
    APP_PORT=1005

# Install runtime dependencies + nginx + supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi8 libssl3 curl ca-certificates nginx supervisor sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r -g 1000 gaara && \
    useradd -r -u 1000 -g gaara -d /app -s /bin/bash gaara

# Copy virtual environment
COPY --from=backend-builder /opt/venv /opt/venv

# Create directories
RUN mkdir -p /app/backend /app/frontend /app/data /app/logs /app/uploads \
    && chown -R gaara:gaara /app

WORKDIR /app

# Copy backend code
COPY --chown=gaara:gaara backend/ /app/backend/

# Copy frontend build
COPY --from=frontend-builder /frontend-build/dist /app/frontend/

# Configure nginx for frontend
RUN cat > /etc/nginx/sites-available/default << 'EOF'
server {
    listen 1505;
    root /app/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:1005/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /health {
        return 200 "healthy\n";
    }
}
EOF

# Configure supervisor
RUN cat > /etc/supervisor/conf.d/gaara.conf << 'EOF'
[supervisord]
nodaemon=true
user=root

[program:backend]
command=/opt/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 1005
directory=/app/backend
user=gaara
autostart=true
autorestart=true
stdout_logfile=/app/logs/backend.log
stderr_logfile=/app/logs/backend_error.log

[program:nginx]
command=nginx -g "daemon off;"
autostart=true
autorestart=true
stdout_logfile=/app/logs/nginx.log
stderr_logfile=/app/logs/nginx_error.log
EOF

# Create startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
set -e
echo "Starting Gaara Scan AI Unified Container..."

# Initialize SQLite database directory
mkdir -p /app/data
touch /app/data/gaara_scan_ai.db
chown -R gaara:gaara /app/data /app/logs /app/uploads

# Start supervisor
exec supervisord -c /etc/supervisor/supervisord.conf
EOF

RUN chmod +x /app/start.sh

EXPOSE 1005 1505

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:1005/api/v1/health && curl -f http://localhost:1505/health || exit 1

ENTRYPOINT ["/app/start.sh"]

