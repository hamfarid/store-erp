#!/bin/bash
# سكريبت تهيئة RabbitMQ لنظام Gaara Scan AI

set -e

echo "بدء تهيئة RabbitMQ..."

# انتظار بدء تشغيل RabbitMQ
sleep 30

# التحقق من حالة RabbitMQ
rabbitmqctl wait /var/lib/rabbitmq/mnesia/rabbit@gaara-rabbitmq.pid

echo "إنشاء المستخدمين والصلاحيات..."

# إنشاء مستخدم الذكاء الاصطناعي
rabbitmqctl add_user gaara_ai_agent gaara_ai_2024 || true
rabbitmqctl set_user_tags gaara_ai_agent management || true

# إنشاء مستخدم التشخيص
rabbitmqctl add_user gaara_diagnosis gaara_diagnosis_2024 || true
rabbitmqctl set_user_tags gaara_diagnosis monitoring || true

# إنشاء مستخدم التحليلات
rabbitmqctl add_user gaara_analytics gaara_analytics_2024 || true
rabbitmqctl set_user_tags gaara_analytics monitoring || true

echo "إنشاء Virtual Hosts..."

# إنشاء Virtual Hosts
rabbitmqctl add_vhost gaara_ai_vhost || true
rabbitmqctl add_vhost gaara_diagnosis_vhost || true
rabbitmqctl add_vhost gaara_analytics_vhost || true

echo "تعيين الصلاحيات..."

# تعيين صلاحيات المستخدمين
rabbitmqctl set_permissions -p gaara_vhost gaara_admin ".*" ".*" ".*" || true
rabbitmqctl set_permissions -p gaara_ai_vhost gaara_ai_agent "ai\..*" "ai\..*" "ai\..*" || true
rabbitmqctl set_permissions -p gaara_diagnosis_vhost gaara_diagnosis "diagnosis\..*" "diagnosis\..*" "diagnosis\..*" || true
rabbitmqctl set_permissions -p gaara_analytics_vhost gaara_analytics "analytics\..*" "analytics\..*" "analytics\..*" || true

echo "إنشاء Exchanges والQueues..."

# إنشاء Exchange للذكاء الاصطناعي
rabbitmqctl eval 'rabbit_exchange:declare({resource, <<"gaara_ai_vhost">>, exchange, <<"ai_agent_exchange">>}, direct, true, false, false, []).' || true

# إنشاء Exchange للتشخيص
rabbitmqctl eval 'rabbit_exchange:declare({resource, <<"gaara_diagnosis_vhost">>, exchange, <<"diagnosis_exchange">>}, fanout, true, false, false, []).' || true

# إنشاء Exchange للتحليلات
rabbitmqctl eval 'rabbit_exchange:declare({resource, <<"gaara_analytics_vhost">>, exchange, <<"analytics_exchange">>}, topic, true, false, false, []).' || true

echo "تهيئة RabbitMQ اكتملت بنجاح!"

# تفعيل إضافة Prometheus للمراقبة
rabbitmq-plugins enable rabbitmq_prometheus || true

echo "جميع الإعدادات تمت بنجاح!"

