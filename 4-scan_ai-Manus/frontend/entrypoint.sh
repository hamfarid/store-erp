#!/bin/bash
# ملف: /home/ubuntu/gaara_development/gaara_ai_integrated/frontend/entrypoint.sh
# نقطة دخول محسنة للواجهة الأمامية - نظام Gaara AI
# تم الإنشاء: 2025-01-07

set -e

echo "🌐 بدء تشغيل نظام Gaara AI - الواجهة الأمامية"
echo "📅 التاريخ: $(date)"
echo "🔧 إصدار nginx: $(nginx -v 2>&1)"
echo "🌍 المنفذ: 80"

# التحقق من وجود ملفات البناء
if [ ! -f "/usr/share/nginx/html/index.html" ]; then
    echo "⚠️  تحذير: ملف index.html غير موجود، استخدام النسخة الاحتياطية"
    cp /usr/share/nginx/html/index.html.backup /usr/share/nginx/html/index.html
fi

# التحقق من تكوين nginx
echo "🔍 التحقق من تكوين nginx..."
nginx -t

# إنشاء مجلدات السجلات إذا لم تكن موجودة
mkdir -p /var/log/nginx
touch /var/log/nginx/access.log /var/log/nginx/error.log

# تعيين الصلاحيات
chown -R nginx:nginx /var/log/nginx /var/cache/nginx /var/run

echo "✅ تم إكمال التحضيرات بنجاح"
echo "🎯 بدء تشغيل nginx..."

# تشغيل nginx في المقدمة
exec nginx -g "daemon off;"

