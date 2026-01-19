# File: /home/ubuntu/clean_project/Dockerfile
# Dockerfile متعدد المراحل لنظام Gaara Scan AI المتقدم
# يستخدم بناء متعدد المراحل لتحسين الأداء والأمان وتقليل حجم الصورة النهائية

# ==========================================
# المرحلة 1: مرحلة البناء (Build Stage)
# ==========================================
FROM python:3.11-slim as builder

# تعيين متغيرات البيئة للبناء
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# تثبيت أدوات البناء المطلوبة
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    pkg-config \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# إنشاء دليل العمل
WORKDIR /build

# نسخ ملفات المتطلبات
COPY requirements.txt .
COPY src/requirements.txt ./src/
COPY src/modules/*/requirements.txt ./modules/

# دمج جميع ملفات المتطلبات
RUN cat requirements.txt > all_requirements.txt && \
    find . -name "requirements.txt" -not -path "./all_requirements.txt" -exec cat {} \; >> all_requirements.txt && \
    sort all_requirements.txt | uniq > final_requirements.txt

# تثبيت المتطلبات في بيئة افتراضية
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r final_requirements.txt

# ==========================================
# المرحلة 2: مرحلة الإنتاج (Production Stage)
# ==========================================
FROM python:3.11-slim as production

# تعيين متغيرات البيئة للإنتاج
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت المكتبات المطلوبة للتشغيل فقط
RUN apt-get update && apt-get install -y \
    libpq5 \
    libffi8 \
    libssl3 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# إنشاء مستخدم غير root للأمان
RUN groupadd -r gaara && useradd -r -g gaara -d /app -s /bin/bash gaara

# إنشاء الدلائل المطلوبة
RUN mkdir -p /app /app/logs /app/uploads /app/static /app/media && \
    chown -R gaara:gaara /app

# نسخ البيئة الافتراضية من مرحلة البناء
COPY --from=builder /opt/venv /opt/venv

# تعيين دليل العمل
WORKDIR /app

# نسخ كود التطبيق
COPY --chown=gaara:gaara . .

# إنشاء ملفات التكوين الافتراضية
RUN echo "DATABASE_URL=postgresql://postgres:postgres@db:5432/gaara_scan_ai" > .env && \
    echo "REDIS_URL=redis://redis:6379/0" >> .env && \
    echo "SECRET_KEY=your-secret-key-here" >> .env && \
    echo "DEBUG=False" >> .env && \
    echo "ENVIRONMENT=production" >> .env && \
    chown gaara:gaara .env

# إنشاء سكريبت بدء التشغيل
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 بدء تشغيل نظام Gaara Scan AI..."

# انتظار قاعدة البيانات
echo "⏳ انتظار قاعدة البيانات..."
while ! curl -s db:5432 > /dev/null; do
    sleep 1
done

# تشغيل migrations إذا كانت موجودة
if [ -f "src/database.py" ]; then
    echo "🔄 تشغيل migrations قاعدة البيانات..."
    python src/database.py
fi

# بدء التطبيق
echo "✅ بدء تشغيل التطبيق..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
EOF

RUN chmod +x /app/start.sh && chown gaara:gaara /app/start.sh

# التبديل للمستخدم غير root
USER gaara

# تعريض المنافذ
EXPOSE 8000

# إعداد health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# تعيين نقطة الدخول
ENTRYPOINT ["/app/start.sh"]

# ==========================================
# المرحلة 3: مرحلة التطوير (Development Stage)
# ==========================================
FROM production as development

# التبديل لمستخدم root لتثبيت أدوات التطوير
USER root

# تثبيت أدوات التطوير
RUN apt-get update && apt-get install -y \
    git \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# تثبيت أدوات Python للتطوير
RUN /opt/venv/bin/pip install \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    jupyter

# إنشاء سكريبت تطوير
RUN cat > /app/dev.sh << 'EOF'
#!/bin/bash
set -e

echo "🔧 بدء وضع التطوير لنظام Gaara Scan AI..."

# تشغيل التطبيق في وضع التطوير
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
EOF

RUN chmod +x /app/dev.sh && chown gaara:gaara /app/dev.sh

# العودة للمستخدم غير root
USER gaara

# تعيين متغيرات التطوير
ENV DEBUG=True
ENV ENVIRONMENT=development

# ==========================================
# المرحلة 4: مرحلة الاختبار (Testing Stage)
# ==========================================
FROM development as testing

# التبديل لمستخدم root
USER root

# تثبيت أدوات الاختبار الإضافية
RUN /opt/venv/bin/pip install \
    selenium \
    requests-mock \
    factory-boy \
    faker

# إنشاء سكريبت الاختبار
RUN cat > /app/test.sh << 'EOF'
#!/bin/bash
set -e

echo "🧪 بدء تشغيل الاختبارات..."

# تشغيل اختبارات الوحدة
echo "📋 تشغيل اختبارات الوحدة..."
python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# تشغيل فحص جودة الكود
echo "🔍 فحص جودة الكود..."
flake8 src/ --max-line-length=120 --ignore=E501,W503

# تشغيل فحص الأنواع
echo "🔎 فحص الأنواع..."
mypy src/ --ignore-missing-imports

echo "✅ اكتملت جميع الاختبارات بنجاح!"
EOF

RUN chmod +x /app/test.sh && chown gaara:gaara /app/test.sh

# العودة للمستخدم غير root
USER gaara

# تعيين متغيرات الاختبار
ENV ENVIRONMENT=testing
ENV DATABASE_URL=sqlite:///test.db

# تعيين الأمر الافتراضي للاختبار
CMD ["/app/test.sh"]

