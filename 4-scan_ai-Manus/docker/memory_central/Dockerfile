# حاوية الذاكرة المركزية المتقدمة
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
RUN mkdir -p /app/data/{memory_banks,indexes,cache,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV MEMORY_PORT=8014
ENV MEMORY_CAPACITY_GB=10
ENV CACHE_TTL_HOURS=24

# تعريض المنفذ
EXPOSE 8014

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8014/health || exit 1

# أمر التشغيل
CMD ["python", "src/memory_central_service.py"]

