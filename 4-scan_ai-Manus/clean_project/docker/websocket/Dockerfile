# حاوية WebSocket للاتصال الفوري

# مرحلة البناء - تحضير البيئة
FROM node:20-alpine as builder

# تثبيت متطلبات النظام
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    git

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات المشروع
COPY package*.json ./
COPY src/ ./src/
COPY config/ ./config/

# تثبيت التبعيات
RUN npm ci --only=production && \
    npm cache clean --force

# مرحلة التشغيل - بيئة محسنة
FROM node:20-alpine as runtime

# تثبيت متطلبات التشغيل
RUN apk add --no-cache \
    curl \
    dumb-init

# إنشاء مستخدم غير جذر
RUN addgroup -g 1001 -S websocket && \
    adduser -S websocket -u 1001

# إعداد مجلد العمل
WORKDIR /app

# نسخ الملفات من مرحلة البناء
COPY --from=builder --chown=websocket:websocket /app .

# إنشاء مجلدات البيانات
RUN mkdir -p /app/logs /app/data && \
    chown -R websocket:websocket /app

# التبديل للمستخدم غير الجذر
USER websocket

# إعداد متغيرات البيئة
ENV NODE_ENV=production
ENV PORT=8007
ENV REDIS_URL=redis://gaara-redis:6379
ENV RABBITMQ_URL=amqp://gaara_admin:gaara_rabbit_2024@gaara-rabbitmq:5672
ENV MAX_CONNECTIONS=1000
ENV HEARTBEAT_INTERVAL=30000

# فحص صحة الحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8007/health || exit 1

# تعريض المنفذ
EXPOSE 8007

# أمر التشغيل
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "src/websocket_server.js"]

