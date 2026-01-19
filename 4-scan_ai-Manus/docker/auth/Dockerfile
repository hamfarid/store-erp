# حاوية خدمة المصادقة والأمان
FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    openssl \
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
RUN mkdir -p /app/data/{sessions,tokens,logs,certificates}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV AUTH_PORT=8010
ENV JWT_ALGORITHM=HS256
ENV TOKEN_EXPIRE_HOURS=24

# تعريض المنفذ
EXPOSE 8010

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8010/health || exit 1

# أمر التشغيل
CMD ["python", "src/auth_service.py"]

