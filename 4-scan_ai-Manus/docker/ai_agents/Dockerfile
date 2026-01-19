# File: /home/ubuntu/clean_project/docker/ai_agents/Dockerfile
# حاوية وكلاء الذكاء الاصطناعي المتخصصة

# مرحلة البناء - تحضير البيئة المتقدمة
FROM python:3.11-slim as builder

# تثبيت متطلبات النظام للذكاء الاصطناعي
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

# تثبيت المكتبات المتقدمة للذكاء الاصطناعي
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# تحميل النماذج المدربة مسبقاً
RUN python -c "
import transformers
from transformers import pipeline
import nltk

# تحميل نماذج معالجة اللغة الطبيعية
sentiment_pipeline = pipeline('sentiment-analysis')
ner_pipeline = pipeline('ner', aggregation_strategy='simple')

# تحميل بيانات NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

print('AI models downloaded successfully')
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
COPY agents/ ./agents/

# إنشاء مستخدم غير جذر
RUN useradd --create-home --shell /bin/bash ai_user && \
    chown -R ai_user:ai_user /app
USER ai_user

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV TRANSFORMERS_CACHE=/app/models
ENV NLTK_DATA=/app/nltk_data
ENV AGENT_CONFIG_PATH=/app/config
ENV MAX_AGENTS=10
ENV MEMORY_LIMIT=2GB

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8004/health')" || exit 1

# تعريض المنفذ
EXPOSE 8004

# أمر التشغيل
CMD ["python", "-m", "uvicorn", "src.ai_agents_service:app", "--host", "0.0.0.0", "--port", "8004", "--workers", "1"]

