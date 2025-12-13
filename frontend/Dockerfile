# Dockerfile للواجهة الأمامية - نظام إدارة المخزون
# مرحلة البناء
FROM node:20-alpine AS builder

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات package
COPY package*.json ./

# تثبيت المكتبات
RUN npm ci --only=production

# نسخ الكود المصدري
COPY . .

# بناء التطبيق (if build script exists)
RUN npm run build || echo "No build script, skipping..."

# مرحلة الإنتاج
FROM nginx:alpine

# نسخ ملف تكوين nginx
COPY nginx.conf /etc/nginx/nginx.conf

# نسخ الملفات المبنية
COPY --from=builder /app/dist /usr/share/nginx/html

# إنشاء مجلد للسجلات
RUN mkdir -p /var/log/nginx

# تعيين الصلاحيات
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/log/nginx

# كشف المنفذ
EXPOSE 80

# فحص الصحة
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# أمر التشغيل
CMD ["nginx", "-g", "daemon off;"]
