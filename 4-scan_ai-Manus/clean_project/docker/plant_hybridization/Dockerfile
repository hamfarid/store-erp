# حاوية تهجين النباتات المتقدمة
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    gfortran \
    liblapack-dev \
    libblas-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ متطلبات Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY src/ ./src/
COPY config/ ./config/
COPY data/ ./data/

# إنشاء مجلدات البيانات
RUN mkdir -p /app/data/{varieties,traits,objectives,simulations,results,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV HYBRIDIZATION_PORT=8022
ENV SIMULATION_WORKERS=4
ENV MAX_GENERATIONS=100

# تعريض المنفذ
EXPOSE 8022

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8022/health || exit 1

# أمر التشغيل
CMD ["python", "src/plant_hybridization_service.py"]

