# File: /home/ubuntu/clean_project/docker/analytics/Dockerfile
# Dockerfile لحاوية التحليلات والبيانات الضخمة
# متخصصة في تحليل البيانات الزراعية والتنبؤات

FROM python:3.11-slim as analytics-base

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# تثبيت المكتبات المطلوبة للتحليلات
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مستخدم غير root
RUN groupadd -r analytics && useradd -r -g analytics -d /app -s /bin/bash analytics

# إنشاء الدلائل
RUN mkdir -p /app /app/data /app/reports /app/logs && \
    chown -R analytics:analytics /app

WORKDIR /app

# نسخ متطلبات التحليلات
COPY docker/analytics/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود التحليلات
COPY --chown=analytics:analytics src/advanced_analytics_system.py ./
COPY --chown=analytics:analytics src/big_data_analytics_system.py ./
COPY --chown=analytics:analytics src/modules/analytics/ ./analytics/

# إنشاء سكريبت التشغيل
RUN cat > /app/start_analytics.sh << 'EOF'
#!/bin/bash
set -e

echo "📊 بدء خدمة التحليلات والبيانات الضخمة..."

# إعداد البيانات الأولية
python -c "
import pandas as pd
import numpy as np
print('إعداد بيانات التحليل الأولية...')
# إنشاء بيانات تجريبية للتحليل
data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=365),
    'temperature': np.random.normal(25, 5, 365),
    'humidity': np.random.normal(60, 10, 365),
    'crop_yield': np.random.normal(100, 20, 365)
})
data.to_csv('/app/data/sample_data.csv', index=False)
print('تم إعداد البيانات بنجاح')
"

# بدء خدمة التحليلات
exec uvicorn analytics.api:app --host 0.0.0.0 --port 8002
EOF

RUN chmod +x /app/start_analytics.sh && chown analytics:analytics /app/start_analytics.sh

# التبديل للمستخدم غير root
USER analytics

# تعريض المنفذ
EXPOSE 8002

# إعداد health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

ENTRYPOINT ["/app/start_analytics.sh"]

