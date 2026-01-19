#!/bin/bash
# سكريبت لتشغيل الحاويات بتسلسل محدد مع التأكد من عدم تشغيل أكثر من حاوية في نفس الوقت

# إنشاء الشبكة إذا لم تكن موجودة
echo "إنشاء شبكة agri_ai_network..."
docker network create agri_ai_network || true

# تشغيل قواعد البيانات أولاً
echo "تشغيل قواعد البيانات..."
docker-compose -f docker-compose.db.yml up -d db
echo "انتظار جاهزية قاعدة البيانات الرئيسية..."
sleep 10

# تشغيل باقي قواعد البيانات
echo "تشغيل باقي قواعد البيانات..."
docker-compose -f docker-compose.db.yml up -d redis rabbitmq etcd minio
echo "انتظار جاهزية قواعد البيانات المساعدة..."
sleep 10

# تشغيل قواعد بيانات الاختبار والإعداد
echo "تشغيل قواعد بيانات الاختبار والإعداد..."
docker-compose -f docker-compose.db.yml up -d db_test db_setup vectordb
echo "انتظار جاهزية قواعد البيانات الإضافية..."
sleep 10

# تشغيل التطبيق الرئيسي
echo "تشغيل التطبيق الرئيسي..."
docker-compose -f docker-compose.main.yml up -d app
echo "انتظار جاهزية التطبيق الرئيسي..."
sleep 15

# تشغيل خدمات الذكاء الاصطناعي ومراقبة الموارد
echo "تشغيل خدمات الذكاء الاصطناعي ومراقبة الموارد..."
docker-compose -f docker-compose.main.yml up -d ai_service resource_monitor
echo "انتظار جاهزية خدمات الذكاء الاصطناعي..."
sleep 10

# تشغيل خدمة Nginx
echo "تشغيل خدمة Nginx..."
docker-compose -f docker-compose.main.yml up -d nginx
echo "انتظار جاهزية خدمة Nginx..."
sleep 5

# تشغيل الخدمات المساعدة
echo "تشغيل خدمات النسخ الاحتياطي..."
docker-compose -f docker-compose.helpers.yml up -d backup_service
echo "انتظار جاهزية خدمات النسخ الاحتياطي..."
sleep 5

# تشغيل خدمة التهجين
echo "تشغيل خدمات التهجين..."
docker-compose -f docker-compose.hybridization.yml up -d hybridization_service
echo "انتظار جاهزية خدمة التهجين..."
sleep 10

# تشغيل خدمة التحليل الجيني
echo "تشغيل خدمة التحليل الجيني..."
docker-compose -f docker-compose.hybridization.yml up -d genetic_analysis
echo "انتظار جاهزية خدمة التحليل الجيني..."
sleep 10

# تشغيل خدمة تشخيص الأمراض
echo "تشغيل خدمة تشخيص الأمراض..."
docker-compose -f docker-compose.disease.yml up -d disease_diagnosis
echo "انتظار جاهزية خدمة تشخيص الأمراض..."
sleep 10

# تشغيل خدمة تحليل الصور
echo "تشغيل خدمة تحليل الصور..."
docker-compose -f docker-compose.disease.yml up -d image_analysis
echo "انتظار جاهزية خدمة تحليل الصور..."
sleep 10

# تشغيل Watchtower في النهاية
echo "تشغيل خدمة Watchtower للتحديث التلقائي..."
docker-compose -f docker-compose.helpers.yml up -d watchtower

echo "تم تشغيل جميع الخدمات بنجاح!"
echo "يمكنك الوصول إلى التطبيق عبر: http://localhost:80"
