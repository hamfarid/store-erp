# File: /home/ubuntu/clean_project/docker/diagnosis/Dockerfile
# Dockerfile لحاوية الفحص والتشخيص المنفصلة
# متخصصة في تشخيص الأمراض النباتية والفحص المتقدم

FROM python:3.11-slim as diagnosis-base

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# تثبيت المكتبات المطلوبة للذكاء الاصطناعي والتشخيص
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مستخدم غير root
RUN groupadd -r diagnosis && useradd -r -g diagnosis -d /app -s /bin/bash diagnosis

# إنشاء الدلائل
RUN mkdir -p /app /app/models /app/data /app/logs && \
    chown -R diagnosis:diagnosis /app

WORKDIR /app

# نسخ متطلبات التشخيص
COPY docker/diagnosis/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود التشخيص
COPY --chown=diagnosis:diagnosis src/modules/disease_diagnosis/ ./diagnosis/
COPY --chown=diagnosis:diagnosis src/modules/plant_disease/ ./plant_disease/
COPY --chown=diagnosis:diagnosis src/advanced_ai_system.py ./
COPY --chown=diagnosis:diagnosis src/adaptive_learning_system.py ./

# إنشاء سكريبت التشغيل
RUN cat > /app/start_diagnosis.sh << 'EOF'
#!/bin/bash
set -e

echo "🔬 بدء خدمة الفحص والتشخيص..."

# تحميل النماذج المطلوبة
python -c "
import torch
import torchvision.models as models
print('تحميل نماذج الذكاء الاصطناعي...')
model = models.resnet50(pretrained=True)
torch.save(model.state_dict(), '/app/models/resnet50.pth')
print('تم تحميل النماذج بنجاح')
"

# بدء خدمة التشخيص
exec uvicorn diagnosis.api:app --host 0.0.0.0 --port 8001
EOF

RUN chmod +x /app/start_diagnosis.sh && chown diagnosis:diagnosis /app/start_diagnosis.sh

# التبديل للمستخدم غير root
USER diagnosis

# تعريض المنفذ
EXPOSE 8001

# إعداد health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

ENTRYPOINT ["/app/start_diagnosis.sh"]

