# حاوية التعلم التكيفي
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
RUN mkdir -p /app/data/{models,training,adaptation,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV ADAPTIVE_PORT=8017
ENV LEARNING_RATE=0.001
ENV ADAPTATION_THRESHOLD=0.85

# تعريض المنفذ
EXPOSE 8017

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8017/health || exit 1

# أمر التشغيل
CMD ["python", "src/adaptive_learning_service.py"]

