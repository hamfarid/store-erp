#!/bin/bash
echo "🛡️ بدء تقوية الأمان العسكري..."

# تأمين ملفات النظام
chmod 600 backend/.env 2>/dev/null || echo "ملف .env غير موجود"
chmod 600 admin_credentials.json 2>/dev/null || echo "ملف admin_credentials.json غير موجود"
chmod 700 backend/instance/ 2>/dev/null || echo "مجلد instance غير موجود"
chmod 755 security_monitor.py 2>/dev/null || echo "ملف security_monitor.py غير موجود"
chmod 755 intrusion_detection.py 2>/dev/null || echo "ملف intrusion_detection.py غير موجود"

# إنشاء مجلد السجلات
mkdir -p logs
chmod 755 logs

echo "✅ تم إكمال تقوية الأمان بنجاح!"
