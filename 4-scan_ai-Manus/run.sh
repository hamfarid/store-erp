#!/bin/bash

# نص برمجي لتشغيل النظام الزراعي باستخدام متغيرات البيئة

# تعيين البيئة الافتراضية إذا لم يتم تحديدها
if [ -z "$ENVIRONMENT" ]; then
    export ENVIRONMENT="development"
    echo "لم يتم تحديد البيئة. استخدام البيئة الافتراضية: $ENVIRONMENT"
fi

# التحقق من صحة البيئة
if [ "$ENVIRONMENT" != "development" ] && [ "$ENVIRONMENT" != "testing" ] && [ "$ENVIRONMENT" != "production" ]; then
    echo "خطأ: البيئة غير صالحة: $ENVIRONMENT"
    echo "البيئات المدعومة: development, testing, production"
    exit 1
fi

echo "تشغيل النظام الزراعي في بيئة: $ENVIRONMENT"

# تعيين عدد النسخ المتكررة لخادم API
if [ -z "$API_REPLICAS" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export API_REPLICAS=4
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export API_REPLICAS=1
    else
        export API_REPLICAS=2
    fi
    echo "تعيين عدد النسخ المتكررة لخادم API: $API_REPLICAS"
fi

# تعيين حدود موارد وحدة المعالجة المركزية لخادم API
if [ -z "$API_CPU_LIMIT" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export API_CPU_LIMIT=2
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export API_CPU_LIMIT=0.5
    else
        export API_CPU_LIMIT=1
    fi
    echo "تعيين حد وحدة المعالجة المركزية لخادم API: $API_CPU_LIMIT"
fi

# تعيين حدود الذاكرة لخادم API
if [ -z "$API_MEMORY_LIMIT" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export API_MEMORY_LIMIT="2G"
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export API_MEMORY_LIMIT="512M"
    else
        export API_MEMORY_LIMIT="1G"
    fi
    echo "تعيين حد الذاكرة لخادم API: $API_MEMORY_LIMIT"
fi

# تعيين حدود موارد وحدة المعالجة المركزية لمعالج الصور
if [ -z "$PROCESSOR_CPU_LIMIT" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export PROCESSOR_CPU_LIMIT=4
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export PROCESSOR_CPU_LIMIT=1
    else
        export PROCESSOR_CPU_LIMIT=2
    fi
    echo "تعيين حد وحدة المعالجة المركزية لمعالج الصور: $PROCESSOR_CPU_LIMIT"
fi

# تعيين حدود الذاكرة لمعالج الصور
if [ -z "$PROCESSOR_MEMORY_LIMIT" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export PROCESSOR_MEMORY_LIMIT="8G"
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export PROCESSOR_MEMORY_LIMIT="2G"
    else
        export PROCESSOR_MEMORY_LIMIT="4G"
    fi
    echo "تعيين حد الذاكرة لمعالج الصور: $PROCESSOR_MEMORY_LIMIT"
fi

# تعيين حدود موارد وحدة المعالجة المركزية لموازن الحمل
if [ -z "$NGINX_CPU_LIMIT" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export NGINX_CPU_LIMIT=1
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export NGINX_CPU_LIMIT=0.2
    else
        export NGINX_CPU_LIMIT=0.5
    fi
    echo "تعيين حد وحدة المعالجة المركزية لموازن الحمل: $NGINX_CPU_LIMIT"
fi

# تعيين حدود الذاكرة لموازن الحمل
if [ -z "$NGINX_MEMORY_LIMIT" ]; then
    if [ "$ENVIRONMENT" == "production" ]; then
        export NGINX_MEMORY_LIMIT="512M"
    elif [ "$ENVIRONMENT" == "testing" ]; then
        export NGINX_MEMORY_LIMIT="128M"
    else
        export NGINX_MEMORY_LIMIT="256M"
    fi
    echo "تعيين حد الذاكرة لموازن الحمل: $NGINX_MEMORY_LIMIT"
fi

# التحقق من وجود ملف البيئة
ENV_FILE="./docker/env/${ENVIRONMENT}.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "خطأ: ملف البيئة غير موجود: $ENV_FILE"
    exit 1
fi

echo "استخدام ملف البيئة: $ENV_FILE"

# تشغيل النظام باستخدام Docker Compose
docker-compose -f ./docker/docker-compose.yml up -d

echo "تم تشغيل النظام الزراعي بنجاح في بيئة: $ENVIRONMENT"
