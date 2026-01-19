# ==========================================
# Image Crawler Dockerfile - Gaara Scan AI v4.3.1
# Multi-stage build for intelligent image crawler
# ==========================================

# ==========================================
# Stage 1: Builder - Install dependencies
# ==========================================
FROM python:3.11-slim as builder

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Production - Runtime image
# ==========================================
FROM python:3.11-slim as production

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1

LABEL org.opencontainers.image.title="Gaara Scan AI Image Crawler" \
      org.opencontainers.image.description="Intelligent crawler for plant disease images" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Gaara Group & Manus AI" \
      org.opencontainers.image.source="https://github.com/hamfarid/gaara-Scan-system"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH" \
    PORT=4601

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libpq5 \
    libffi8 \
    libssl3 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user with specific UID/GID
RUN groupadd -r -g 1002 crawler && \
    useradd -r -u 1002 -g crawler -d /app -s /bin/bash crawler

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create directories with proper permissions
RUN mkdir -p \
    /app \
    /app/data/images \
    /app/data/metadata \
    /app/data/cache \
    /app/logs \
    && chown -R crawler:crawler /app

WORKDIR /app

# Copy application code
COPY --chown=crawler:crawler . .

# Create startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
set -e

echo "🕷️ Starting Gaara Scan AI Image Crawler v4.3.1..."
echo "Port: ${PORT:-4601}"

# Wait for database if configured
if [ -n "${DATABASE_HOST}" ] && [ -n "${DATABASE_PORT:-5432}" ]; then
    echo "⏳ Waiting for PostgreSQL..."
    while ! nc -z ${DATABASE_HOST} ${DATABASE_PORT:-5432}; do
        sleep 2
    done
    echo "✅ PostgreSQL is ready!"
fi

# Wait for Redis if configured
if [ -n "${REDIS_HOST}" ] && [ -n "${REDIS_PORT:-6379}" ]; then
    echo "⏳ Waiting for Redis..."
    while ! nc -z ${REDIS_HOST} ${REDIS_PORT:-6379}; do
        sleep 2
    done
    echo "✅ Redis is ready!"
fi

echo "🚀 Starting crawler service..."
exec uvicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-4601} \
    --workers ${WORKERS:-2} \
    --log-level ${LOG_LEVEL:-info}
EOF

RUN chmod +x /app/start.sh && chown crawler:crawler /app/start.sh

# Switch to non-root user
USER crawler

# Expose port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Start service
ENTRYPOINT ["/app/start.sh"]
