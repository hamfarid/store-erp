# حاوية RabbitMQ المتقدمة لإدارة الرسائل

# استخدام الصورة الرسمية لـ RabbitMQ مع إدارة الويب
FROM rabbitmq:3.12-management-alpine

# تثبيت الأدوات المساعدة
RUN apk add --no-cache \
    curl \
    jq \
    bash

# نسخ ملفات التكوين
COPY config/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
COPY config/definitions.json /etc/rabbitmq/definitions.json
COPY config/enabled_plugins /etc/rabbitmq/enabled_plugins

# نسخ سكريبتات التهيئة
COPY scripts/init.sh /docker-entrypoint-initdb.d/
COPY scripts/health_check.sh /usr/local/bin/

# إعداد الصلاحيات
RUN chmod +x /docker-entrypoint-initdb.d/init.sh && \
    chmod +x /usr/local/bin/health_check.sh

# إنشاء مجلدات البيانات
RUN mkdir -p /var/lib/rabbitmq/mnesia && \
    chown -R rabbitmq:rabbitmq /var/lib/rabbitmq

# إعداد متغيرات البيئة
ENV RABBITMQ_DEFAULT_USER=gaara_admin
ENV RABBITMQ_DEFAULT_PASS=gaara_rabbit_2024
ENV RABBITMQ_DEFAULT_VHOST=gaara_vhost
ENV RABBITMQ_ERLANG_COOKIE=gaara_erlang_cookie_2024
ENV RABBITMQ_NODE_TYPE=disc
ENV RABBITMQ_NODENAME=rabbit@gaara-rabbitmq
ENV RABBITMQ_USE_LONGNAME=true

# تكوين الشبكة والأمان
ENV RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbit log_levels [{connection,info}]"
ENV RABBITMQ_CTL_ERL_ARGS="-proto_dist inet_tcp"

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /usr/local/bin/health_check.sh

# تعريض المنافذ
# 5672: AMQP port
# 15672: Management UI
# 25672: Clustering port
EXPOSE 5672 15672 25672

# أمر التشغيل
CMD ["rabbitmq-server"]

