# FILE: templates/Dockerfile
# PURPOSE: قالب Dockerfile للمشاريع
# OWNER: Global Team
# LAST-AUDITED: 2025-10-21

# استخدام صورة أساسية خفيفة
FROM ubuntu:22.04

# تعيين متغيرات البيئة
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# تحديث النظام وتثبيت الأدوات الأساسية
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مستخدم غير root
RUN useradd -m -s /bin/bash appuser

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات (سيتم تخصيصها حسب المشروع)
# COPY . /app

# تغيير الملكية
RUN chown -R appuser:appuser /app

# التبديل إلى المستخدم غير root
USER appuser

# نقطة الدخول الافتراضية
CMD ["/bin/bash"]

# ملاحظات:
# - استبدل الصورة الأساسية حسب احتياجات المشروع (python, node, etc.)
# - أضف تثبيت التبعيات الخاصة بالمشروع
# - حدد PORT إذا كان التطبيق يحتاج لذلك
# - استخدم multi-stage builds لتقليل حجم الصورة النهائية

