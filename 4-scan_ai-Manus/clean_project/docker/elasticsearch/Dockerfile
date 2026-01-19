# حاوية Elasticsearch للبحث والفهرسة المتقدمة

FROM docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# تثبيت الإضافات المطلوبة
RUN bin/elasticsearch-plugin install analysis-icu
RUN bin/elasticsearch-plugin install analysis-phonetic

# نسخ ملفات التكوين
COPY config/elasticsearch.yml /usr/share/elasticsearch/config/
COPY config/jvm.options /usr/share/elasticsearch/config/

# إنشاء مجلدات البيانات
RUN mkdir -p /usr/share/elasticsearch/data/gaara_search
RUN mkdir -p /usr/share/elasticsearch/logs

# إعداد الصلاحيات
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/logs

# إعداد متغيرات البيئة
ENV discovery.type=single-node
ENV xpack.security.enabled=true
ENV xpack.security.authc.api_key.enabled=true
ENV ELASTIC_PASSWORD=gaara_elastic_2024
ENV ES_JAVA_OPTS="-Xms2g -Xmx2g"

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f -u elastic:gaara_elastic_2024 http://localhost:9200/_cluster/health || exit 1

# تعريض المنافذ
EXPOSE 9200 9300

# أمر التشغيل
CMD ["bin/elasticsearch"]

