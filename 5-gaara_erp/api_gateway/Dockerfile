# /home/ubuntu/gaara_erp_v12/api_gateway/Dockerfile
# SECURITY HARDENING (2025-12-01): Applied Docker security best practices

# Build stage
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim-bookworm AS production

# Security labels
LABEL maintainer="Gaara ERP Team" \
      version="1.0" \
      description="Gaara ERP API Gateway" \
      org.opencontainers.image.source="https://github.com/gaara-erp/gaara-erp"

# Security: Create non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Security: Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/*

# Copy application code
COPY --chown=appuser:appgroup . .

# Security: Set proper permissions
RUN chmod -R 550 /app \
    && chmod -R 770 /app/logs 2>/dev/null || true

# Security: Remove unnecessary files
RUN rm -rf /app/.git /app/.env* /app/*.md /app/tests 2>/dev/null || true

# Security: Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Security: Read-only root filesystem compatible command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
