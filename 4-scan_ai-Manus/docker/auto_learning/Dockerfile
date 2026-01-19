# حاوية التعلم التلقائي والبحث الذكي
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
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
RUN mkdir -p /app/data/{models,training,search_results,keywords,sources}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV AUTO_LEARNING_PORT=8012
ENV SEARCH_ENGINE_COUNT=5
ENV LEARNING_INTERVAL_HOURS=6

# تعريض المنفذ
EXPOSE 8012

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8012/health || exit 1

# أمر التشغيل
CMD ["python", "src/auto_learning_service.py"]

