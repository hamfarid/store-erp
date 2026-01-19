# حاوية تشخيص أمراض النباتات المتقدمة
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    libopencv-dev \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ متطلبات Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY src/ ./src/
COPY config/ ./config/
COPY knowledge_base/ ./knowledge_base/

# إنشاء مجلدات البيانات
RUN mkdir -p /app/data/{diseases,symptoms,treatments,models,results,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV DISEASE_PORT=8021
ENV KNOWLEDGE_BASE_PATH=/app/knowledge_base
ENV MODELS_PATH=/app/data/models

# تعريض المنفذ
EXPOSE 8021

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8021/health || exit 1

# أمر التشغيل
CMD ["python", "src/plant_disease_advanced_service.py"]

