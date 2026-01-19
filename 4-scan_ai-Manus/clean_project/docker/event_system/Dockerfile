# حاوية نظام الأحداث المتقدم
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
RUN mkdir -p /app/data/{events,handlers,logs,queue}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV EVENT_PORT=8011
ENV MAX_EVENT_QUEUE=10000
ENV EVENT_RETENTION_DAYS=30

# تعريض المنفذ
EXPOSE 8011

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8011/health || exit 1

# أمر التشغيل
CMD ["python", "src/event_system.py"]

