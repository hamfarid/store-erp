# File: /home/ubuntu/clean_project/docker/resnet50/Dockerfile
# حاوية ResNet-50 للرؤية الحاسوبية المتقدمة

# مرحلة البناء - تحضير البيئة
FROM python:3.11-slim as builder

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# إنشاء بيئة Python معزولة
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# تثبيت المكتبات الأساسية
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# تحميل نموذج ResNet-50 المدرب مسبقاً
RUN python -c "
import torch
import torchvision.models as models
model = models.resnet50(pretrained=True)
torch.save(model.state_dict(), '/opt/venv/resnet50_pretrained.pth')
print('ResNet-50 model downloaded successfully')
"

# مرحلة التشغيل - بيئة مُحسنة
FROM python:3.11-slim as runtime

# تثبيت متطلبات التشغيل فقط
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# نسخ البيئة المُعدة من مرحلة البناء
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات التطبيق
COPY src/ ./src/
COPY config/ ./config/

# إنشاء مستخدم غير جذر للأمان
RUN useradd --create-home --shell /bin/bash resnet_user && \
    chown -R resnet_user:resnet_user /app
USER resnet_user

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV MODEL_PATH=/opt/venv/resnet50_pretrained.pth
ENV TORCH_HOME=/app/models
ENV OMP_NUM_THREADS=4

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8003/health')" || exit 1

# تعريض المنفذ
EXPOSE 8003

# أمر التشغيل
CMD ["python", "-m", "uvicorn", "src.resnet50_service:app", "--host", "0.0.0.0", "--port", "8003", "--workers", "2"]

