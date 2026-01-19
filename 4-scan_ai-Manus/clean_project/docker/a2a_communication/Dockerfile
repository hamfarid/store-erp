# حاوية التواصل A2A (Agent to Agent)
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
RUN mkdir -p /app/data/{agents,communications,protocols,logs}

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV A2A_PORT=8013
ENV MAX_AGENTS=50
ENV COMMUNICATION_TIMEOUT=30

# تعريض المنفذ
EXPOSE 8013

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8013/health || exit 1

# أمر التشغيل
CMD ["python", "src/a2a_communication_service.py"]

