#!/bin/bash
# سكريبت إعداد النظام المتكامل

echo "بدء إعداد نظام إدارة المخزون..."

# إعداد الواجهة الخلفية
echo "إعداد الواجهة الخلفية..."
cd backend
pip install -r requirements.txt
python setup_database.py

# إعداد الواجهة الأمامية
echo "إعداد الواجهة الأمامية..."
cd ../frontend
npm install

echo "تم إعداد النظام بنجاح!"
echo "لتشغيل النظام، استخدم: ./scripts/start_system.sh"
