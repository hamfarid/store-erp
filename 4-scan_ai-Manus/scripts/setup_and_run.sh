#!/bin/bash
# سكريبت الإعداد والتشغيل الشامل المحدث لنظام Gaara Scan AI
# يتضمن جميع الحاويات والخدمات المفقودة
# الملف: /home/ubuntu/clean_project/scripts/setup_and_run.sh

set -e

# الألوان للإخراج
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دوال المساعدة
print_info() {
    echo -e "${BLUE}[معلومات]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[نجح]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[تحذير]${NC} $1"
}

print_error() {
    echo -e "${RED}[خطأ]${NC} $1"
}

# إنشاء جميع المجلدات المطلوبة للنظام الهجين
create_hybrid_directories() {
    print_info "إنشاء هيكل المجلدات الهجين (Volume + Bind Mounts)..."
    
    # المجلدات الرئيسية
    mkdir -p data/{uploads,static,logs,backups,models,temp}
    mkdir -p config/{redis,nginx,prometheus,grafana,kibana,elasticsearch}
    mkdir -p reports
    
    # مجلدات قواعد البيانات (Bind Mounts للنسخ الاحتياطية والسجلات)
    mkdir -p data/postgres/{backups,logs}
    mkdir -p data/redis/logs
    mkdir -p data/rabbitmq/logs
    mkdir -p data/elasticsearch/{logs,backups}
    
    # مجلدات الذكاء الاصطناعي
    mkdir -p data/vector_db/{vectors,models,logs}
    mkdir -p data/memory/{short_term,long_term,logs}
    mkdir -p data/resnet50/{training_data,results,logs}
    mkdir -p data/ai_agents/{agents,conversations,knowledge_base,logs}
    mkdir -p data/models/{resnet50,ai_agents,diagnosis}
    
    # مجلدات الخدمات المتقدمة
    mkdir -p data/diagnosis/{images,results,reports,logs}
    mkdir -p data/analytics/{raw_data,processed_data,reports,exports,logs}
    mkdir -p data/websocket/{logs,sessions}
    mkdir -p data/notifications/{templates,attachments,queue,logs}
    
    # مجلدات الخدمات المفقودة
    mkdir -p data/monitoring/{metrics,logs,alerts,reports}
    mkdir -p data/auth/{sessions,tokens,logs,certificates}
    mkdir -p data/events/{queue,handlers,logs}
    mkdir -p data/auto_learning/{models,training,search_results,keywords,sources,logs}
    mkdir -p data/a2a/{agents,communications,protocols,logs}
    mkdir -p data/memory_central/{memory_banks,indexes,logs}
    mkdir -p data/cloud/{sync,backups,uploads,logs}
    mkdir -p data/sync/{queue,conflicts,logs,temp}
    mkdir -p data/adaptive/{models,training,adaptation,logs}
    
    # مجلدات المراقبة
    mkdir -p data/prometheus/logs
    mkdir -p data/grafana/{dashboards,logs}
    mkdir -p data/kibana/{data,logs}
    mkdir -p data/node_exporter/logs
    mkdir -p data/cadvisor/logs
    mkdir -p data/portainer/logs
    mkdir -p data/watchtower/logs
    mkdir -p data/nginx/logs
    
    # مجلدات التكوين للخدمات الجديدة
    mkdir -p config/{vector_db,memory,resnet50,ai_agents,diagnosis,analytics}
    mkdir -p config/{websocket,notifications,monitoring,auth,events}
    mkdir -p config/{auto_learning,a2a,memory_central,cloud,sync,adaptive}
    mkdir -p config/nginx/sites
    
    # إعداد الصلاحيات
    chmod 755 data config reports
    chmod 700 data/backups data/auth data/certificates
    chmod 755 data/uploads data/static
    chmod 644 config/*/
    
    print_success "تم إنشاء هيكل المجلدات الهجين بنجاح (${GREEN}$(find data config -type d | wc -l)${NC} مجلد)"
}

# بناء الصور بالترتيب الصحيح
build_images_ordered() {
    print_info "بناء صور Docker بالترتيب المحسن..."
    
    # المرحلة 1: البنية التحتية
    print_info "المرحلة 1: بناء البنية التحتية الأساسية..."
    docker-compose build gaara-postgres
    docker-compose build gaara-rabbitmq
    
    # المرحلة 2: قواعد البيانات المتقدمة
    print_info "المرحلة 2: بناء قواعد البيانات المتقدمة..."
    docker-compose build gaara-elasticsearch
    docker-compose build gaara-kibana
    docker-compose build gaara-vector-db
    
    # المرحلة 3: خدمات الذكاء الاصطناعي
    print_info "المرحلة 3: بناء خدمات الذكاء الاصطناعي..."
    docker-compose build gaara-memory-service
    docker-compose build gaara-resnet50-service
    docker-compose build gaara-ai-agents-service
    
    # المرحلة 4: خدمات التشخيص والتحليل
    print_info "المرحلة 4: بناء خدمات التشخيص والتحليل..."
    docker-compose build gaara-diagnosis-service
    docker-compose build gaara-analytics-service
    
    # المرحلة 5: خدمات الاتصالات
    print_info "المرحلة 5: بناء خدمات الاتصالات..."
    docker-compose build gaara-websocket-service
    docker-compose build gaara-notification-service
    
    # المرحلة 6: الخدمات المتقدمة والمفقودة
    print_info "المرحلة 6: بناء الخدمات المتقدمة والمفقودة..."
    docker-compose build gaara-monitoring-service
    docker-compose build gaara-auth-service
    docker-compose build gaara-event-system
    docker-compose build gaara-auto-learning
    docker-compose build gaara-a2a-communication
    docker-compose build gaara-memory-central
    docker-compose build gaara-cloud-integration
    docker-compose build gaara-real-time-sync
    docker-compose build gaara-adaptive-learning
    
    print_success "تم بناء جميع الصور بنجاح"
}

# تشغيل الخدمات المتقدمة والمفقودة
start_advanced_services() {
    print_info "تشغيل الخدمات المتقدمة والمفقودة..."
    
    # تشغيل خدمات الأمان والمراقبة
    docker-compose up -d gaara-auth-service gaara-monitoring-service
    sleep 15
    
    # تشغيل نظام الأحداث
    docker-compose up -d gaara-event-system
    sleep 10
    
    # تشغيل خدمات التعلم المتقدمة
    docker-compose up -d gaara-auto-learning gaara-adaptive-learning
    sleep 20
    
    # تشغيل خدمات التواصل والذاكرة المركزية
    docker-compose up -d gaara-a2a-communication gaara-memory-central
    sleep 15
    
    # تشغيل خدمات السحابة والمزامنة
    docker-compose up -d gaara-cloud-integration gaara-real-time-sync
    sleep 15
    
    print_success "الخدمات المتقدمة جاهزة"
}

# فحص حالة جميع الخدمات
check_all_services_health() {
    print_info "فحص حالة جميع الخدمات..."
    
    services=(
        "gaara-postgres:5432"
        "gaara-redis:6379"
        "gaara-rabbitmq:15672"
        "gaara-elasticsearch:9200"
        "gaara-vector-db:8006"
        "gaara-memory-service:8005"
        "gaara-resnet50-service:8003"
        "gaara-ai-agents-service:8004"
        "gaara-diagnosis-service:8001"
        "gaara-analytics-service:8002"
        "gaara-websocket-service:8007"
        "gaara-notification-service:8008"
        "gaara-monitoring-service:8009"
        "gaara-auth-service:8010"
        "gaara-event-system:8011"
        "gaara-auto-learning:8012"
        "gaara-a2a-communication:8013"
        "gaara-memory-central:8014"
        "gaara-cloud-integration:8015"
        "gaara-real-time-sync:8016"
        "gaara-adaptive-learning:8017"
        "gaara-main-app:8000"
    )
    
    healthy_count=0
    total_count=${#services[@]}
    
    for service in "${services[@]}"; do
        container=$(echo $service | cut -d: -f1)
        port=$(echo $service | cut -d: -f2)
        
        if docker-compose ps $container | grep -q "Up"; then
            print_success "$container يعمل بشكل صحيح"
            ((healthy_count++))
        else
            print_error "$container لا يعمل"
        fi
    done
    
    print_info "حالة الخدمات: ${GREEN}$healthy_count${NC}/${total_count} خدمة تعمل بشكل صحيح"
    
    if [ $healthy_count -eq $total_count ]; then
        print_success "جميع الخدمات تعمل بشكل مثالي!"
    else
        print_warning "بعض الخدمات تحتاج للمراجعة"
    fi
}

# عرض معلومات الوصول المحدثة
show_comprehensive_access_info() {
    print_info "معلومات الوصول الشاملة للنظام:"
    echo ""
    echo -e "${GREEN}🌐 التطبيق الرئيسي:${NC} http://localhost"
    echo -e "${GREEN}⚙️  صفحة الإعدادات:${NC} http://localhost/setup"
    echo ""
    echo -e "${BLUE}=== خدمات الذكاء الاصطناعي ===${NC}"
    echo -e "${GREEN}🧠 ResNet-50:${NC} http://localhost:8003"
    echo -e "${GREEN}🤖 AI Agents:${NC} http://localhost:8004"
    echo -e "${GREEN}💾 Memory Service:${NC} http://localhost:8005"
    echo -e "${GREEN}🔍 Vector Database:${NC} http://localhost:8006"
    echo -e "${GREEN}📚 Auto Learning:${NC} http://localhost:8012"
    echo -e "${GREEN}🔄 A2A Communication:${NC} http://localhost:8013"
    echo -e "${GREEN}🧠 Memory Central:${NC} http://localhost:8014"
    echo -e "${GREEN}🎯 Adaptive Learning:${NC} http://localhost:8017"
    echo ""
    echo -e "${BLUE}=== خدمات التشخيص والتحليل ===${NC}"
    echo -e "${GREEN}🔬 Diagnosis Service:${NC} http://localhost:8001"
    echo -e "${GREEN}📊 Analytics Service:${NC} http://localhost:8002"
    echo ""
    echo -e "${BLUE}=== خدمات الاتصالات ===${NC}"
    echo -e "${GREEN}⚡ WebSocket:${NC} http://localhost:8007"
    echo -e "${GREEN}📢 Notifications:${NC} http://localhost:8008"
    echo ""
    echo -e "${BLUE}=== خدمات النظام ===${NC}"
    echo -e "${GREEN}📈 Monitoring:${NC} http://localhost:8009"
    echo -e "${GREEN}🔐 Auth Service:${NC} http://localhost:8010"
    echo -e "${GREEN}⚡ Event System:${NC} http://localhost:8011"
    echo -e "${GREEN}☁️  Cloud Integration:${NC} http://localhost:8015"
    echo -e "${GREEN}🔄 Real-time Sync:${NC} http://localhost:8016"
    echo ""
    echo -e "${BLUE}=== خدمات المراقبة ===${NC}"
    echo -e "${GREEN}📊 Grafana:${NC} http://localhost/grafana (admin/gaara_grafana_2024)"
    echo -e "${GREEN}🔍 Kibana:${NC} http://localhost/kibana"
    echo -e "${GREEN}📈 Prometheus:${NC} http://localhost:9090"
    echo -e "${GREEN}🐳 Portainer:${NC} http://localhost:9000"
    echo -e "${GREEN}🐰 RabbitMQ:${NC} http://localhost:15672 (gaara_admin/gaara_rabbit_2024)"
    echo ""
    echo -e "${YELLOW}📝 ملاحظة:${NC} النظام يتضمن ${GREEN}21 خدمة متقدمة${NC} مع نظام هجين Volume + Bind Mounts"
    echo -e "${YELLOW}🔧 الإعداد:${NC} اذهب إلى http://localhost/setup لإكمال الإعداد الأولي"
    echo -e "${YELLOW}📦 الحاويات:${NC} التطبيق الرئيسي هو آخر حاوية يتم إنشاؤها لسهولة التحديث"
    echo ""
}

# الدالة الرئيسية المحدثة
main() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "    نظام Gaara Scan AI - الإعداد الشامل المحدث"
    echo "    يتضمن جميع الحاويات والخدمات المفقودة"
    echo "=================================================="
    echo -e "${NC}"
    
    # فحص المتطلبات
    check_requirements
    
    # إنشاء ملف .env
    create_env_file
    
    # إنشاء المجلدات الهجينة
    create_hybrid_directories
    
    # بناء الصور بالترتيب
    build_images_ordered
    
    # تشغيل الخدمات بالترتيب
    start_infrastructure
    start_services
    start_advanced_services
    start_monitoring
    start_main_app
    
    # فحص الحالة الشاملة
    check_all_services_health
    
    # عرض معلومات الوصول الشاملة
    show_comprehensive_access_info
    
    print_success "تم إعداد وتشغيل نظام Gaara Scan AI الشامل بنجاح!"
    print_info "النظام يتضمن الآن جميع الحاويات والخدمات المطلوبة مع النظام الهجين"
}

# تشغيل السكريبت
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

