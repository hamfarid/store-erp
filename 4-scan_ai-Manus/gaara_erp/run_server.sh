#!/bin/bash

# ملف تشغيل سيرفر Gaara ERP
# يقوم هذا الملف بتشغيل سيرفر Gaara ERP على المنفذ 2050

# تعيين المتغيرات البيئية
export GAARA_ENV=development
export GAARA_PORT=2050
export GAARA_HOST=0.0.0.0
export GAARA_DEBUG=true

# التأكد من وجود المتطلبات
echo "التحقق من المتطلبات..."
pip3 install -r requirements.txt

# تشغيل السيرفر
echo "بدء تشغيل سيرفر Gaara ERP على المنفذ 2050..."
cd /home/ubuntu/agricultural_ai_system/gaara_erp
python3 src/main.py --port 2050 --host 0.0.0.0

echo "تم إيقاف السيرفر."
