# FILE: templates/Dockerfile
# PURPOSE: قالب Dockerfile للمشاريع - Security Hardened Template
# OWNER: Global Team
# LAST-AUDITED: 2025-12-01
# SECURITY: Follows Docker security best practices (CIS Benchmark)

# ============================================================
# SECURITY HARDENED DOCKERFILE TEMPLATE
# ============================================================

# استخدام صورة أساسية خفيفة مع تثبيت الإصدار
# Use slim base image with pinned version
FROM ubuntu:22.04@sha256:REPLACE_WITH_ACTUAL_DIGEST

# Security labels
LABEL maintainer="Gaara ERP Team" \
      version="1.0" \
      description="Security-hardened container template" \
      org.opencontainers.image.vendor="Gaara ERP"

# تعيين متغيرات البيئة
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # Security: Disable Python bytecode cache
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# تحديث النظام وتثبيت الأدوات الأساسية
# Security: Use --no-install-recommends and clean up
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/*

# Security: Create non-root user with specific UID/GID
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home appuser

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات (سيتم تخصيصها حسب المشروع)
# COPY --chown=appuser:appgroup . /app

# Security: Set restrictive permissions
RUN chown -R appuser:appgroup /app \
    && chmod -R 550 /app

# Security: Remove unnecessary packages and files
RUN apt-get purge -y --auto-remove \
    && rm -rf /tmp/* /var/tmp/*

# التبديل إلى المستخدم غير root
USER appuser

# Security: Use HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# نقطة الدخول الافتراضية
CMD ["/bin/bash"]

# ============================================================
# SECURITY NOTES / ملاحظات الأمان:
# ============================================================
# 1. Always pin base image versions with digest
# 2. Run as non-root user (UID 1000)
# 3. Use multi-stage builds for production
# 4. Remove build dependencies in final stage
# 5. Set restrictive file permissions (550 for dirs, 440 for files)
# 6. Include HEALTHCHECK instruction
# 7. Don't store secrets in environment variables in Dockerfile
# 8. Scan images with tools like Trivy, Snyk, or Docker Scout
# 9. Use --read-only flag when running containers
# 10. Consider using distroless base images for production
#
# Example run command with security flags:
# docker run --read-only --security-opt=no-new-privileges:true \
#            --cap-drop=ALL --user 1000:1000 imagename
# ============================================================

