# حاوية خدمة المراقبة المتقدمة لنظام Gaara Scan AI
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    procps \
    htop \
    iotop \
    net-tools \
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
RUN mkdir -p /app/data/{metrics,logs,alerts,reports}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV MONITORING_PORT=8009
ENV LOG_LEVEL=INFO

# تعريض المنفذ
EXPOSE 8009

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8009/health || exit 1

# أمر التشغيل
CMD ["python", "src/monitoring_service.py"]

