# Dockerfile محسن لنظام Gaara Scan AI
# Optimized Dockerfile for Gaara Scan AI System

FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Riyadh

# تثبيت التبعيات النظام
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    git \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libopencv-dev \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مستخدم غير جذر
RUN useradd --create-home --shell /bin/bash gaara

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY src/ ./src/
COPY .env.example ./.env

# إنشاء المجلدات المطلوبة
RUN mkdir -p /app/data/uploads \
             /app/data/results \
             /app/logs \
             /app/config && \
    chown -R gaara:gaara /app

# التبديل للمستخدم غير الجذر
USER gaara

# تعريض المنفذ
EXPOSE 8000

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# أمر التشغيل
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

