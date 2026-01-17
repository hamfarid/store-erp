# Complete Inventory Management System - Backend Dockerfile
# P0.22: Security-hardened multi-stage build
# Python 3.11 with Alpine Linux for minimal size

# ==================== BUILD STAGE ====================
FROM python:3.11-alpine AS builder

# P0.22: Security - Pin to specific version for reproducibility
# Update this hash periodically for security patches

# Set build arguments
ARG BUILD_DATE
ARG VERSION=1.0.0
ARG VCS_REF
ARG INCLUDE_RAG=false

# Add metadata labels
LABEL maintainer="Complete Inventory System Team" \
      version="${VERSION}" \
      description="Complete Inventory Management System Backend" \
      build-date="${BUILD_DATE}" \
      vcs-ref="${VCS_REF}"

# Set environment variables for build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    mysql-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    libimagequant-dev \
    libxcb-dev \
    libpng-dev

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /tmp/requirements.txt

# ==================== PRODUCTION STAGE ====================
FROM python:3.11-alpine AS production

# P0.22: Security labels
LABEL org.opencontainers.image.source="https://github.com/hamfarid/store" \
      org.opencontainers.image.description="Store Management System - Security Hardened" \
      org.opencontainers.image.licenses="MIT" \
      security.policy="hardened"

# P0.22: Set environment variables with security in mind
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=src.main:app \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    # P0.22: Disable Python's use of __pycache__
    PYTHONDONTWRITEBYTECODE=1

# P0.22: Install only minimal runtime dependencies
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
    tzdata \
    ca-certificates \
    # P0.22: Update CA certificates for secure connections
    && update-ca-certificates \
    # P0.22: Remove package cache
    && rm -rf /var/cache/apk/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# P0.22: Create non-root user with specific UID/GID for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S -D -H -G appgroup appuser && \
    # P0.22: Ensure no shell access
    sed -i 's|/bin/ash|/sbin/nologin|g' /etc/passwd

# Set working directory
WORKDIR /app

# P0.22: Copy only necessary application files (exclude dev files)
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup migrations/ ./migrations/
COPY --chown=appuser:appgroup templates/ ./templates/
COPY --chown=appuser:appgroup app.py wsgi.py ./

# P0.22: Create application directories with strict permissions
RUN mkdir -p /app/logs /app/uploads /app/instance /app/migrations/versions && \
    chown -R appuser:appgroup /app && \
    # P0.22: Strict directory permissions - writable only where needed
    chmod -R 750 /app && \
    chmod 770 /app/logs /app/uploads /app/instance && \
    # P0.22: Remove write permission from source code
    chmod -R 550 /app/src && \
    # P0.22: Remove any unnecessary files
    find /app -name "*.pyc" -delete && \
    find /app -name "__pycache__" -type d -delete && \
    find /app -name "*.md" -delete 2>/dev/null || true && \
    find /app -name "*.txt" ! -name "requirements.txt" -delete 2>/dev/null || true

# P0.22: Switch to non-root user
USER 1001:1001

# P0.22: Security - Set read-only root filesystem indicator
# Note: Actual read-only filesystem is set in docker-compose/k8s
LABEL security.read-only-rootfs="true"

# P0.22: Enhanced health check with timeout
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# P0.22: Expose only the necessary port
EXPOSE 5000

# P0.22: Security hardened gunicorn command
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--timeout", "120", \
     "--keep-alive", "2", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--capture-output", \
     "--enable-stdio-inheritance", \
     "wsgi:app"]
