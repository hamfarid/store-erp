# ==========================================
# Backend Dockerfile - Gaara Scan AI v4.3.1
# Multi-stage build for production-ready backend
# ==========================================

# ==========================================
# Stage 1: Builder - Install dependencies
# ==========================================
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    pkg-config \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /build

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with retry logic
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Production - Runtime image
# ==========================================
FROM python:3.11-slim as production

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1

# Set labels (OCI standard)
LABEL org.opencontainers.image.title="Gaara Scan AI Backend" \
      org.opencontainers.image.description="Backend API for Gaara Scan AI System" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Gaara Group & Manus AI" \
      org.opencontainers.image.source="https://github.com/hamfarid/gaara-Scan-system"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH" \
    APP_PORT=4001 \
    WORKERS=4 \
    LOG_LEVEL=info

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libffi8 \
    libssl3 \
    curl \
    ca-certificates \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user with specific UID/GID for consistency
RUN groupadd -r -g 1000 gaara && \
    useradd -r -u 1000 -g gaara -d /app -s /bin/bash gaara

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create application directories with proper permissions
RUN mkdir -p \
    /app \
    /app/logs \
    /app/uploads \
    /app/data/uploads \
    /app/data/results \
    /app/data/backups \
    /app/data/models \
    && chown -R gaara:gaara /app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=gaara:gaara . .

# Create optimized startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Starting Gaara Scan AI Backend v4.3.1..."
echo "Environment: ${ENVIRONMENT:-production}"

# Function to wait for service
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=0
    
    echo "⏳ Waiting for ${service} at ${host}:${port}..."
    
    while [ $attempt -lt $max_attempts ]; do
        if nc -z ${host} ${port} 2>/dev/null; then
            echo "✅ ${service} is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        echo "Attempt ${attempt}/${max_attempts}: ${service} is unavailable - sleeping"
        sleep 2
    done
    
    echo "❌ ${service} failed to become available"
    return 1
}

# Wait for PostgreSQL
if [ -n "${DATABASE_HOST}" ] && [ -n "${DATABASE_PORT}" ]; then
    wait_for_service ${DATABASE_HOST} ${DATABASE_PORT} "PostgreSQL"
fi

# Wait for Redis
if [ -n "${REDIS_HOST}" ] && [ -n "${REDIS_PORT}" ]; then
    wait_for_service ${REDIS_HOST} ${REDIS_PORT} "Redis"
fi

# Run database migrations
if [ -f "alembic.ini" ] && [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    echo "🔄 Running database migrations..."
    alembic upgrade head || {
        echo "⚠️ Migration failed, continuing..."
    }
fi

# Start application with proper signal handling
echo "✅ Starting application on port ${APP_PORT}..."
exec uvicorn src.main:app \
    --host 0.0.0.0 \
    --port ${APP_PORT} \
    --workers ${WORKERS} \
    --log-level ${LOG_LEVEL} \
    --access-log \
    --use-colors
EOF

RUN chmod +x /app/start.sh && chown gaara:gaara /app/start.sh

# Switch to non-root user
USER gaara

# Expose port
EXPOSE ${APP_PORT}

# Health check with proper endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:4001/api/v1/health || exit 1

# Set entrypoint
ENTRYPOINT ["/app/start.sh"]
