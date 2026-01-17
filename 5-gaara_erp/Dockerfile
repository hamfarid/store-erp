# =============================================================================
# Gaara ERP Backend - Multi-stage Dockerfile
# =============================================================================
# Production-ready Django backend with security best practices
# =============================================================================

# =============================================================================
# Stage 1: Builder
# =============================================================================
FROM python:3.11-slim-bookworm AS builder

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Metadata labels
LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.authors="Gaara ERP Team" \
      org.opencontainers.image.url="https://github.com/gaara-erp/gaara-erp" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Gaara ERP" \
      org.opencontainers.image.title="Gaara ERP Backend" \
      org.opencontainers.image.description="Django backend for Gaara ERP system"

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies
COPY gaara_erp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# =============================================================================
# Stage 2: Production
# =============================================================================
FROM python:3.11-slim-bookworm AS production

# Security: Create non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy application code
COPY --chown=appuser:appgroup gaara_erp/ /app/

# Copy healthcheck script
COPY --chown=appuser:appgroup docker/docker-healthcheck.sh /app/docker/docker-healthcheck.sh
RUN chmod +x /app/docker/docker-healthcheck.sh

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R appuser:appgroup /app/staticfiles /app/media /app/logs && \
    chmod -R 755 /app/staticfiles /app/media && \
    chmod -R 750 /app/logs

# Security: Set proper permissions
RUN chmod -R 550 /app && \
    find /app -type f -name "*.py" -exec chmod 440 {} \; && \
    find /app -type d -exec chmod 550 {} \;

# Security: Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD /app/docker/docker-healthcheck.sh || exit 1

# Default command
CMD ["gunicorn", "gaara_erp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]

# =============================================================================
# Stage 3: Development
# =============================================================================
FROM production AS development

# Switch back to root for development tools
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install --no-cache-dir \
    ipython \
    ipdb \
    django-debug-toolbar \
    django-extensions

# Switch back to appuser
USER appuser

# Override command for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
