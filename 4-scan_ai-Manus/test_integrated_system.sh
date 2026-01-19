#!/bin/bash

# نص برمجي لاختبار النظام المتكامل

# تعيين البيئة إلى بيئة الاختبار
export ENVIRONMENT="testing"
echo "تعيين البيئة إلى: $ENVIRONMENT"

# إنشاء مجلدات البيانات إذا لم تكن موجودة
mkdir -p /home/ubuntu/agricultural_ai_system/data/primitive_features
mkdir -p /home/ubuntu/agricultural_ai_system/data/standard_features
mkdir -p /home/ubuntu/agricultural_ai_system/data/comparison_results
mkdir -p /home/ubuntu/agricultural_ai_system/data/visualizations
mkdir -p /home/ubuntu/agricultural_ai_system/models
mkdir -p /home/ubuntu/agricultural_ai_system/uploads
mkdir -p /home/ubuntu/agricultural_ai_system/temp

echo "تم إنشاء مجلدات البيانات"

# اختبار تحميل متغيرات البيئة
echo "اختبار تحميل متغيرات البيئة من ملف: ./docker/env/${ENVIRONMENT}.env"
source ./docker/env/${ENVIRONMENT}.env

# اختبار وحدة تحميل متغيرات البيئة
echo "اختبار وحدة تحميل متغيرات البيئة..."
python3 -c "
import sys
sys.path.append('/home/ubuntu/agricultural_ai_system/src/utils/config')
from env_loader import EnvLoader
loader = EnvLoader()
print('تم تحميل متغيرات البيئة بنجاح')
print(f'بيئة التشغيل: {loader.get_str(\"ENVIRONMENT\", \"غير محدد\")}')
print(f'مجلد البيانات: {loader.get_str(\"DATA_DIR\", \"غير محدد\")}')
print(f'مستوى التسجيل: {loader.get_str(\"LOG_LEVEL\", \"غير محدد\")}')
"

# اختبار وحدة تحميل التكوين
echo "اختبار وحدة تحميل التكوين..."
python3 -c "
import sys
sys.path.append('/home/ubuntu/agricultural_ai_system/src/utils/config')
from config_loader import ConfigLoader
loader = ConfigLoader()
config = loader.load_config('default')
print('تم تحميل التكوين بنجاح')
print(f'عدد المفاتيح في التكوين: {len(config.keys())}')
"

# اختبار نظام التحليل الأولي للصور
echo "اختبار نظام التحليل الأولي للصور..."
python3 -c "
import sys
import os
sys.path.append('/home/ubuntu/agricultural_ai_system/src')
from image_analysis.primitive.analyzer import PrimitiveImageAnalyzer

# إنشاء كائن المحلل
analyzer = PrimitiveImageAnalyzer()
print('تم إنشاء كائن المحلل بنجاح')
print(f'طريقة التقسيم: {analyzer.config[\"segment_method\"]}')
print(f'عدد الأجزاء: {analyzer.config[\"segment_count\"]}')
print(f'مجلد المخرجات: {analyzer.config[\"output_dir\"]}')
"

# اختبار تكامل Docker مع متغيرات البيئة
echo "اختبار تكامل Docker مع متغيرات البيئة..."
echo "التحقق من وجود ملف docker-compose.yml..."
if [ -f "./docker/docker-compose.yml" ]; then
    echo "تم العثور على ملف docker-compose.yml"
    grep "env_file" ./docker/docker-compose.yml
    grep "ENVIRONMENT" ./docker/docker-compose.yml
else
    echo "خطأ: ملف docker-compose.yml غير موجود"
fi

echo "التحقق من وجود ملفات البيئة..."
for env in development testing production; do
    if [ -f "./docker/env/${env}.env" ]; then
        echo "تم العثور على ملف البيئة: ${env}.env"
        # عرض عدد المتغيرات في الملف
        count=$(grep -v "^#" ./docker/env/${env}.env | grep -v "^$" | wc -l)
        echo "عدد المتغيرات في ${env}.env: $count"
    else
        echo "خطأ: ملف البيئة ${env}.env غير موجود"
    fi
done

# اختبار نص التشغيل
echo "اختبار نص التشغيل..."
if [ -f "./run.sh" ]; then
    echo "تم العثور على نص التشغيل run.sh"
    # التحقق من أن النص قابل للتنفيذ
    if [ -x "./run.sh" ]; then
        echo "نص التشغيل قابل للتنفيذ"
    else
        echo "تحذير: نص التشغيل غير قابل للتنفيذ"
    fi
else
    echo "خطأ: نص التشغيل run.sh غير موجود"
fi

echo "اكتمل اختبار النظام المتكامل"
