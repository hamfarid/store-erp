# حاوية نظام الإشعارات المتقدم

# مرحلة البناء - تحضير البيئة
FROM python:3.11-slim as builder

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# إنشاء بيئة Python معزولة
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# مرحلة التشغيل - بيئة محسنة
FROM python:3.11-slim as runtime

# تثبيت متطلبات التشغيل
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# نسخ البيئة المُعدة
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات التطبيق
COPY src/ ./src/
COPY config/ ./config/
COPY templates/ ./templates/

# إنشاء مجلدات البيانات
RUN mkdir -p /app/logs /app/data/notifications /app/data/templates

# إنشاء مستخدم غير جذر
RUN useradd --create-home --shell /bin/bash notification_user && \
    chown -R notification_user:notification_user /app
USER notification_user

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV NOTIFICATION_QUEUE=notification_queue
ENV EMAIL_PROVIDER=smtp
ENV SMS_PROVIDER=twilio
ENV PUSH_PROVIDER=firebase
ENV TEMPLATE_ENGINE=jinja2

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8008/health')" || exit 1

# تعريض المنفذ
EXPOSE 8008

# أمر التشغيل
CMD ["python", "-m", "uvicorn", "src.notification_service:app", "--host", "0.0.0.0", "--port", "8008", "--workers", "2"]

