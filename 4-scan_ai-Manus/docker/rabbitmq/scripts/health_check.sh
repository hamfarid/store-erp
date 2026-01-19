#!/bin/bash
# سكريبت فحص صحة RabbitMQ

set -e

# التحقق من حالة RabbitMQ
if ! rabbitmqctl status > /dev/null 2>&1; then
    echo "RabbitMQ is not running"
    exit 1
fi

# التحقق من واجهة الإدارة
if ! curl -f -u gaara_admin:gaara_rabbit_2024 http://localhost:15672/api/overview > /dev/null 2>&1; then
    echo "RabbitMQ Management interface is not accessible"
    exit 1
fi

# التحقق من الاتصال بـ AMQP
if ! rabbitmqctl eval 'rabbit_networking:connections().' > /dev/null 2>&1; then
    echo "RabbitMQ AMQP port is not accessible"
    exit 1
fi

# التحقق من Virtual Hosts
VHOSTS=$(rabbitmqctl list_vhosts --quiet)
if ! echo "$VHOSTS" | grep -q "gaara_vhost"; then
    echo "Required virtual hosts are missing"
    exit 1
fi

# التحقق من استخدام الذاكرة
MEMORY_USAGE=$(rabbitmqctl status | grep -o 'memory,[^}]*' | grep -o '[0-9]*' | head -1)
if [ "$MEMORY_USAGE" -gt 1000000000 ]; then  # 1GB
    echo "Warning: High memory usage detected"
fi

echo "RabbitMQ health check passed"
exit 0

