# حاوية Kibana للتصور والتحليل

FROM docker.elastic.co/kibana/kibana:8.11.0

# نسخ ملفات التكوين
COPY config/kibana.yml /usr/share/kibana/config/

# إنشاء مجلدات البيانات
RUN mkdir -p /usr/share/kibana/data
RUN mkdir -p /usr/share/kibana/logs

# إعداد الصلاحيات
RUN chown -R kibana:kibana /usr/share/kibana/data
RUN chown -R kibana:kibana /usr/share/kibana/logs

# إعداد متغيرات البيئة
ENV ELASTICSEARCH_HOSTS=http://gaara-elasticsearch:9200
ENV ELASTICSEARCH_USERNAME=elastic
ENV ELASTICSEARCH_PASSWORD=gaara_elastic_2024
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=5601

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5601/api/status || exit 1

# تعريض المنفذ
EXPOSE 5601

# أمر التشغيل
CMD ["bin/kibana"]

