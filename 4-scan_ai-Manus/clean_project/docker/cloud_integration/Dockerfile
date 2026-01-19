# حاوية التكامل السحابي
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ متطلبات Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY src/ ./src/
COPY config/ ./config/

# إنشاء مجلدات البيانات
RUN mkdir -p /app/data/{cloud_sync,backups,uploads,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV CLOUD_PORT=8015
ENV SYNC_INTERVAL_MINUTES=30
ENV MAX_UPLOAD_SIZE_MB=100

# تعريض المنفذ
EXPOSE 8015

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8015/health || exit 1

# أمر التشغيل
CMD ["python", "src/cloud_integration_service.py"]

