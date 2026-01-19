# حاوية YOLO للكشف عن الكائنات والأمراض
FROM ultralytics/ultralytics:latest

# تثبيت المتطلبات الإضافية
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ متطلبات Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود المصدري
COPY src/ ./src/
COPY config/ ./config/
COPY models/ ./models/

# إنشاء مجلدات البيانات
RUN mkdir -p /app/data/{input,output,models,weights,results,logs}

# تحميل نماذج YOLO المدربة مسبقاً
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt'); YOLO('yolov8s.pt'); YOLO('yolov8m.pt')"

# إعداد متغيرات البيئة
ENV PYTHONPATH=/app
ENV YOLO_PORT=8018
ENV MODEL_PATH=/app/models
ENV WEIGHTS_PATH=/app/data/weights

# تعريض المنفذ
EXPOSE 8018

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8018/health || exit 1

# أمر التشغيل
CMD ["python", "src/yolo_detection_service.py"]

