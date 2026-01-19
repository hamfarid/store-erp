# /home/ubuntu/image_search_integration/Dockerfile
# Dockerfile للمديول البحث الذاتي الذكي في نظام Gaara ERP
# يستخدم هذا الملف لإنشاء حاوية Docker لتشغيل مديول البحث الذاتي الذكي

# استخدام صورة Python الرسمية كقاعدة
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# تعيين دليل العمل
WORKDIR /app

# نسخ ملفات المتطلبات وتثبيتها
COPY requirements.txt requirements-base.txt requirements-ml.txt  requirements-base.txt requirements-ml.txt  .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود المشروع
COPY . .

# تعريض المنفذ الذي سيستمع عليه التطبيق
EXPOSE 8000

# تشغيل التطبيق عند بدء الحاوية
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


