# حاوية تحسين الصور المتقدمة
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libopencv-dev \
    python3-opencv \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
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
RUN mkdir -p /app/data/{input,output,processed,enhanced,filters,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV ENHANCEMENT_PORT=8019
ENV MAX_IMAGE_SIZE=4096
ENV QUALITY_LEVEL=95

# تعريض المنفذ
EXPOSE 8019

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8019/health || exit 1

# أمر التشغيل
CMD ["python", "src/image_enhancement_service.py"]

