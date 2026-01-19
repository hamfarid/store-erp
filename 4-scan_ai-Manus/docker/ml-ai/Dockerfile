# ==========================================
# ML/AI/Scraper Container - Gaara Scan AI v4.3.1
# ML Service + Image Crawler + AI Features
# ==========================================

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ libpq-dev libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build

# Combine requirements from ML service and image crawler
COPY ml_service/requirements.txt ml_requirements.txt
COPY image_crawler/requirements.txt crawler_requirements.txt

RUN cat ml_requirements.txt crawler_requirements.txt | sort -u > all_requirements.txt && \
    pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r all_requirements.txt

# ==========================================
# Production stage
# ==========================================
FROM python:3.11-slim AS production

ARG BUILD_DATE
ARG VERSION=4.3.1

LABEL org.opencontainers.image.title="Gaara Scan AI ML/AI/Scraper" \
      org.opencontainers.image.description="ML Service + Image Crawler + AI Features" \
      org.opencontainers.image.version="${VERSION}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies + supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 libffi8 libssl3 curl ca-certificates supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r -g 1001 mluser && \
    useradd -r -u 1001 -g mluser -d /app -s /bin/bash mluser

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv

# Create directories
RUN mkdir -p /app/ml_service /app/image_crawler /app/models /app/data /app/logs \
    && chown -R mluser:mluser /app

WORKDIR /app

# Copy ML service
COPY --chown=mluser:mluser ml_service/ /app/ml_service/

# Copy Image Crawler
COPY --chown=mluser:mluser image_crawler/ /app/image_crawler/

# Configure supervisor
RUN cat > /etc/supervisor/conf.d/ml-ai.conf << 'EOF'
[supervisord]
nodaemon=true
user=root

[program:ml_service]
command=/opt/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
directory=/app/ml_service
user=mluser
autostart=true
autorestart=true
stdout_logfile=/app/logs/ml_service.log
stderr_logfile=/app/logs/ml_service_error.log

[program:image_crawler]
command=/opt/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001 --workers 1
directory=/app/image_crawler
user=mluser
autostart=true
autorestart=true
stdout_logfile=/app/logs/image_crawler.log
stderr_logfile=/app/logs/image_crawler_error.log
EOF

# Create startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
set -e
echo "Starting Gaara Scan AI ML/AI/Scraper Container..."

# Ensure directories exist
mkdir -p /app/models /app/data /app/logs
chown -R mluser:mluser /app/models /app/data /app/logs

# Start supervisor
exec supervisord -c /etc/supervisor/supervisord.conf
EOF

RUN chmod +x /app/start.sh

# Expose ports: ML=8000, Crawler=8001
EXPOSE 8000 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health && curl -f http://localhost:8001/health || exit 1

ENTRYPOINT ["/app/start.sh"]

