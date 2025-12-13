#!/bin/bash
# سكريبت تثبيت نظام إدارة المخزون
# Inventory Management System Installation Script

echo "🚀 بدء تثبيت نظام إدارة المخزون..."
echo "Starting Inventory Management System Installation..."

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

# إنشاء قاعدة البيانات
echo "🗄️ تهيئة قاعدة البيانات..."
cd backend/src
python -c "
from unified_server import init_database
init_database()
print('تم تهيئة قاعدة البيانات بنجاح')
"

echo "✅ تم التثبيت بنجاح!"
echo "🌐 لتشغيل الخادم: python backend/src/unified_server.py"
echo "🌐 الرابط: http://localhost:5000"
