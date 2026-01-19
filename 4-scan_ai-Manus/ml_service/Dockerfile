# ==========================================
# ML Service Dockerfile - Gaara Scan AI v4.3.1
# AI/ML service for disease diagnosis
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
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build

# Copy requirements
COPY requirements.txt .

# Install ML dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Production stage
# ==========================================
FROM python:3.11-slim as production

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION=4.3.1

LABEL org.opencontainers.image.title="Gaara Scan AI ML Service" \
      org.opencontainers.image.description="ML Service for Disease Diagnosis" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Gaara Group & Manus AI" \
      org.opencontainers.image.source="https://github.com/hamfarid/gaara-Scan-system"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libffi8 \
    libssl3 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r -g 1001 mluser && \
    useradd -r -u 1001 -g mluser -d /app -s /bin/bash mluser

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv

# Create directories
RUN mkdir -p \
    /app \
    /app/models \
    /app/data \
    /app/logs \
    && chown -R mluser:mluser /app

WORKDIR /app

# Copy application code
COPY --chown=mluser:mluser . .

# Switch to non-root user
USER mluser

# Expose port
EXPOSE 4101

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:4101/health || exit 1

# Start service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4101", "--workers", "2"]
