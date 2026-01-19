# حاوية قاعدة البيانات الشعاعية المتقدمة (Vector Database)

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
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# إنشاء بيئة Python معزولة
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت المكتبات المتقدمة للبحث الشعاعي
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# تحميل النماذج المطلوبة للتضمين الشعاعي
RUN python -c "
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# تحميل نموذج التضمين الدلالي المتقدم
model = SentenceTransformer('all-mpnet-base-v2')
model.save('/opt/venv/vector_model')

# إنشاء فهرس FAISS تجريبي
dimension = 768
index = faiss.IndexFlatIP(dimension)
faiss.write_index(index, '/opt/venv/faiss_index.bin')

print('Vector database models downloaded successfully')
"

# مرحلة التشغيل - بيئة محسنة للإنتاج
FROM python:3.11-slim as runtime

# تثبيت متطلبات التشغيل
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    libgomp1 \
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
RUN mkdir -p /app/data/vectors /app/data/indices /app/data/metadata /app/logs

# إنشاء مستخدم غير جذر
RUN useradd --create-home --shell /bin/bash vector_user && \
    chown -R vector_user:vector_user /app
USER vector_user

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV VECTOR_MODEL_PATH=/opt/venv/vector_model
ENV FAISS_INDEX_PATH=/app/data/indices
ENV VECTOR_DIMENSION=768
ENV MAX_VECTORS=1000000
ENV SIMILARITY_THRESHOLD=0.7
ENV BATCH_SIZE=1000

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8006/health')" || exit 1

# تعريض المنفذ
EXPOSE 8006

# أمر التشغيل
CMD ["python", "-m", "uvicorn", "src.vector_db_service:app", "--host", "0.0.0.0", "--port", "8006", "--workers", "1"]

