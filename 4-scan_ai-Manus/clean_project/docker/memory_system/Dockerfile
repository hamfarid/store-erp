# File: /home/ubuntu/clean_project/docker/memory_system/Dockerfile
# حاوية أنظمة الذاكرة القصيرة والطويلة

# مرحلة البناء - تحضير البيئة المتقدمة
FROM python:3.11-slim as builder

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء بيئة Python معزولة
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت المكتبات المتقدمة للذاكرة
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# تحميل النماذج المطلوبة للذاكرة الدلالية
RUN python -c "
from sentence_transformers import SentenceTransformer
import nltk

# تحميل نموذج التضمين الدلالي
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('/opt/venv/sentence_transformer_model')

# تحميل بيانات NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

print('Memory models downloaded successfully')
"

# مرحلة التشغيل - بيئة محسنة للإنتاج
FROM python:3.11-slim as runtime

# تثبيت متطلبات التشغيل
RUN apt-get update && apt-get install -y \
    libpq5 \
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

# إنشاء مجلدات البيانات
RUN mkdir -p /app/data/short_term /app/data/long_term /app/data/vector_store

# إنشاء مستخدم غير جذر
RUN useradd --create-home --shell /bin/bash memory_user && \
    chown -R memory_user:memory_user /app
USER memory_user

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV SENTENCE_TRANSFORMER_MODEL=/opt/venv/sentence_transformer_model
ENV SHORT_TERM_MEMORY_TTL=3600
ENV LONG_TERM_MEMORY_RETENTION=2592000
ENV VECTOR_DIMENSION=384
ENV MAX_MEMORY_SIZE=1GB

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8005/health')" || exit 1

# تعريض المنفذ
EXPOSE 8005

# أمر التشغيل
CMD ["python", "-m", "uvicorn", "src.memory_service:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "1"]

