# حاوية المزامنة الفورية
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
RUN mkdir -p /app/data/{sync_queue,conflicts,logs,temp}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV SYNC_PORT=8016
ENV REAL_TIME_ENABLED=true
ENV CONFLICT_RESOLUTION=auto

# تعريض المنفذ
EXPOSE 8016

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8016/health || exit 1

# أمر التشغيل
CMD ["python", "src/real_time_sync_service.py"]

