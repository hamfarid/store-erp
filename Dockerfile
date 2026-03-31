# =============================================================================
# Store ERP System - Root Dockerfile (builds backend from root context)
# =============================================================================
# NOTE: The preferred way to build is via docker-compose.yml which uses
# backend/Dockerfile. This root Dockerfile is for standalone backend builds.
# =============================================================================

# ==================== BUILD STAGE ====================
FROM python:3.11-alpine AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    harfbuzz-dev \
    fribidi-dev \
    libpng-dev

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install gunicorn && \
    pip install -r /tmp/requirements.txt

# ==================== PRODUCTION STAGE ====================
FROM python:3.11-alpine AS production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    FLASK_DEBUG=0

# Install runtime dependencies
RUN apk add --no-cache \
    postgresql-libs \
    jpeg \
    zlib \
    freetype \
    lcms2 \
    openjpeg \
    tiff \
    harfbuzz \
    fribidi \
    libpng \
    curl \
    wget \
    tzdata \
    ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/cache/apk/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S -D -G appgroup -h /app appuser

WORKDIR /app

# Copy backend application code
COPY --chown=appuser:appgroup backend/src/ ./src/
COPY --chown=appuser:appgroup backend/migrations/ ./migrations/
COPY --chown=appuser:appgroup backend/app.py backend/wsgi.py ./
COPY --chown=appuser:appgroup backend/docker-entrypoint.sh ./

# Create directories, fix line endings, set permissions
RUN mkdir -p /app/logs /app/uploads /app/instance /app/backups /app/flask_session /app/migrations/versions && \
    sed -i 's/\r$//' /app/docker-entrypoint.sh && \
    chown -R appuser:appgroup /app && \
    chmod -R 750 /app && \
    chmod 770 /app/logs /app/uploads /app/instance /app/backups /app/flask_session && \
    chmod +x /app/docker-entrypoint.sh

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

EXPOSE 5000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--timeout", "120", \
     "--keep-alive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--capture-output", \
     "--enable-stdio-inheritance", \
     "wsgi:app"]
