# حاوية معالجة GPU المتقدمة
FROM nvidia/cuda:11.8-devel-ubuntu20.04

# تجنب التفاعل أثناء التثبيت
ENV DEBIAN_FRONTEND=noninteractive

# تثبيت Python والمتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    gcc \
    g++ \
    curl \
    git \
    libcudnn8 \
    libcudnn8-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء رابط لـ Python
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# إنشاء مجلد العمل
WORKDIR /app

# نسخ متطلبات Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY src/ ./src/
COPY config/ ./config/

# إنشاء مجلدات البيانات
RUN mkdir -p /app/data/{gpu_cache,models,processing,results,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV GPU_PORT=8020
ENV CUDA_VISIBLE_DEVICES=0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# تعريض المنفذ
EXPOSE 8020

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8020/health || exit 1

# أمر التشغيل
CMD ["python", "src/gpu_processing_service.py"]

