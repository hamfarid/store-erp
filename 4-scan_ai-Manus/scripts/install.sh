#!/bin/bash

# =============================================================================
# سكريبت الإعداد والتثبيت الشامل لنظام Gaara Scan AI
# Gaara Scan AI Complete Setup and Installation Script
# =============================================================================

set -e  # إيقاف السكريبت عند حدوث خطأ

# الألوان للعرض
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# متغيرات النظام
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$PROJECT_ROOT/logs/setup_${TIMESTAMP}.log"

# إنشاء مجلد السجلات
mkdir -p "$PROJECT_ROOT/logs"

# =============================================================================
# دوال المساعدة
# =============================================================================

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "${PURPLE}"
    echo "============================================================================="
    echo "$1"
    echo "============================================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}>>> $1${NC}"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "الأمر $1 غير موجود. يرجى تثبيته أولاً."
        exit 1
    fi
}

# =============================================================================
# فحص المتطلبات الأساسية
# =============================================================================

check_requirements() {
    print_header "فحص المتطلبات الأساسية"
    
    print_step "فحص Docker..."
    check_command "docker"
    
    print_step "فحص Docker Compose..."
    check_command "docker-compose"
    
    print_step "فحص Git..."
    check_command "git"
    
    print_step "فحص curl..."
    check_command "curl"
    
    # فحص إصدار Docker
    DOCKER_VERSION=$(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    log_info "إصدار Docker: $DOCKER_VERSION"
    
    # فحص إصدار Docker Compose
    COMPOSE_VERSION=$(docker-compose --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    log_info "إصدار Docker Compose: $COMPOSE_VERSION"
    
    # فحص وجود GPU (اختياري)
    if command -v nvidia-smi &> /dev/null; then
        log_info "تم العثور على GPU NVIDIA"
        nvidia-smi --query-gpu=name --format=csv,noheader | head -1 | tee -a "$LOG_FILE"
    else
        log_warning "لم يتم العثور على GPU NVIDIA - ستعمل الخدمات بدون تسريع GPU"
    fi
    
    log "✅ تم فحص جميع المتطلبات بنجاح"
}

# =============================================================================
# إنشاء هيكل المجلدات
# =============================================================================

create_directory_structure() {
    print_header "إنشاء هيكل المجلدات"
    
    # مجلدات البيانات الرئيسية
    local data_dirs=(
        "data"
        "config"
        "logs"
        "backups"
        "uploads"
        "downloads"
        "temp"
        "knowledge_base"
    )
    
    # مجلدات البيانات للخدمات
    local service_data_dirs=(
        # قواعد البيانات
        "data/postgres/data"
        "data/postgres/backups"
        "data/redis/data"
        "data/elasticsearch/data"
        "data/elasticsearch/logs"
        "data/vector_db/data"
        "data/vector_db/indexes"
        
        # خدمات الذكاء الاصطناعي
        "data/yolo/input"
        "data/yolo/output"
        "data/yolo/models"
        "data/yolo/weights"
        "data/yolo/results"
        "data/yolo/logs"
        
        "data/image_enhancement/input"
        "data/image_enhancement/output"
        "data/image_enhancement/processed"
        "data/image_enhancement/enhanced"
        "data/image_enhancement/filters"
        "data/image_enhancement/logs"
        
        "data/gpu/processing"
        "data/gpu/results"
        "data/gpu/models"
        "data/gpu/logs"
        
        "data/plant_disease/diseases"
        "data/plant_disease/symptoms"
        "data/plant_disease/treatments"
        "data/plant_disease/models"
        "data/plant_disease/results"
        "data/plant_disease/logs"
        
        "data/plant_hybridization/varieties"
        "data/plant_hybridization/traits"
        "data/plant_hybridization/objectives"
        "data/plant_hybridization/simulations"
        "data/plant_hybridization/results"
        "data/plant_hybridization/logs"
        
        # خدمات الذاكرة والتعلم
        "data/memory_system/short_term"
        "data/memory_system/long_term"
        "data/memory_system/cache"
        "data/memory_system/logs"
        
        "data/resnet50/models"
        "data/resnet50/cache"
        "data/resnet50/results"
        "data/resnet50/logs"
        
        "data/ai_agents/conversations"
        "data/ai_agents/models"
        "data/ai_agents/logs"
        
        # خدمات الاتصالات
        "data/rabbitmq/data"
        "data/rabbitmq/logs"
        
        "data/websocket/sessions"
        "data/websocket/logs"
        
        "data/notification/queue"
        "data/notification/logs"
        
        # خدمات المراقبة
        "data/prometheus/data"
        "data/prometheus/config"
        
        "data/grafana/data"
        "data/grafana/logs"
        "data/grafana/dashboards"
        
        "data/kibana/data"
        "data/kibana/logs"
        
        # خدمات النظام
        "data/monitoring/metrics"
        "data/monitoring/alerts"
        "data/monitoring/logs"
        
        "data/auth/sessions"
        "data/auth/tokens"
        "data/auth/logs"
        
        "data/event_system/events"
        "data/event_system/logs"
        
        "data/auto_learning/models"
        "data/auto_learning/training"
        "data/auto_learning/logs"
        
        "data/cloud_integration/sync"
        "data/cloud_integration/logs"
        
        "data/real_time_sync/data"
        "data/real_time_sync/logs"
        
        "data/adaptive_learning/models"
        "data/adaptive_learning/logs"
    )
    
    # مجلدات التكوين
    local config_dirs=(
        "config/postgres"
        "config/redis"
        "config/elasticsearch"
        "config/kibana"
        "config/prometheus"
        "config/grafana"
        "config/nginx"
        "config/rabbitmq"
        "config/vector_db"
        "config/yolo"
        "config/image_enhancement"
        "config/gpu"
        "config/plant_disease"
        "config/plant_hybridization"
        "config/memory_system"
        "config/resnet50"
        "config/ai_agents"
        "config/websocket"
        "config/notification"
        "config/monitoring"
        "config/auth"
        "config/event_system"
        "config/auto_learning"
        "config/cloud_integration"
        "config/real_time_sync"
        "config/adaptive_learning"
    )
    
    print_step "إنشاء المجلدات الرئيسية..."
    for dir in "${data_dirs[@]}"; do
        mkdir -p "$PROJECT_ROOT/$dir"
        log_info "تم إنشاء: $dir"
    done
    
    print_step "إنشاء مجلدات بيانات الخدمات..."
    for dir in "${service_data_dirs[@]}"; do
        mkdir -p "$PROJECT_ROOT/$dir"
        log_info "تم إنشاء: $dir"
    done
    
    print_step "إنشاء مجلدات التكوين..."
    for dir in "${config_dirs[@]}"; do
        mkdir -p "$PROJECT_ROOT/$dir"
        log_info "تم إنشاء: $dir"
    done
    
    # تعيين الصلاحيات المناسبة
    print_step "تعيين الصلاحيات..."
    chmod -R 755 "$PROJECT_ROOT/data"
    chmod -R 755 "$PROJECT_ROOT/config"
    chmod -R 755 "$PROJECT_ROOT/logs"
    
    # إنشاء ملفات .gitkeep للمجلدات الفارغة
    find "$PROJECT_ROOT/data" -type d -empty -exec touch {}/.gitkeep \;
    find "$PROJECT_ROOT/config" -type d -empty -exec touch {}/.gitkeep \;
    
    log "✅ تم إنشاء هيكل المجلدات بنجاح"
}

# =============================================================================
# إعداد ملفات التكوين
# =============================================================================

setup_configuration_files() {
    print_header "إعداد ملفات التكوين"
    
    print_step "إنشاء ملف .env..."
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        
        # توليد كلمات مرور عشوائية آمنة
        DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        REDIS_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        JWT_SECRET=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-50)
        ENCRYPTION_KEY=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
        
        # تحديث ملف .env
        sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" "$PROJECT_ROOT/.env"
        sed -i "s/REDIS_PASSWORD=.*/REDIS_PASSWORD=$REDIS_PASSWORD/" "$PROJECT_ROOT/.env"
        sed -i "s/JWT_SECRET=.*/JWT_SECRET=$JWT_SECRET/" "$PROJECT_ROOT/.env"
        sed -i "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$ENCRYPTION_KEY/" "$PROJECT_ROOT/.env"
        
        log_info "تم إنشاء ملف .env مع كلمات مرور آمنة"
    else
        log_info "ملف .env موجود مسبقاً"
    fi
    
    print_step "نسخ ملفات التكوين..."
    
    # نسخ ملفات تكوين PostgreSQL
    if [ -f "$PROJECT_ROOT/docker/postgres/postgresql.conf" ]; then
        cp "$PROJECT_ROOT/docker/postgres/postgresql.conf" "$PROJECT_ROOT/config/postgres/"
        cp "$PROJECT_ROOT/docker/postgres/pg_hba.conf" "$PROJECT_ROOT/config/postgres/"
        log_info "تم نسخ تكوين PostgreSQL"
    fi
    
    # نسخ ملفات تكوين Nginx
    if [ -f "$PROJECT_ROOT/docker/nginx/nginx.conf" ]; then
        cp "$PROJECT_ROOT/docker/nginx/nginx.conf" "$PROJECT_ROOT/config/nginx/"
        log_info "تم نسخ تكوين Nginx"
    fi
    
    # نسخ ملفات تكوين RabbitMQ
    if [ -d "$PROJECT_ROOT/docker/rabbitmq/config" ]; then
        cp -r "$PROJECT_ROOT/docker/rabbitmq/config/"* "$PROJECT_ROOT/config/rabbitmq/"
        log_info "تم نسخ تكوين RabbitMQ"
    fi
    
    # نسخ ملفات تكوين Prometheus
    if [ -f "$PROJECT_ROOT/docker/prometheus/config/prometheus.yml" ]; then
        cp "$PROJECT_ROOT/docker/prometheus/config/prometheus.yml" "$PROJECT_ROOT/config/prometheus/"
        log_info "تم نسخ تكوين Prometheus"
    fi
    
    # نسخ ملفات تكوين Grafana
    if [ -d "$PROJECT_ROOT/docker/grafana" ]; then
        cp -r "$PROJECT_ROOT/docker/grafana/"* "$PROJECT_ROOT/config/grafana/"
        log_info "تم نسخ تكوين Grafana"
    fi
    
    log "✅ تم إعداد ملفات التكوين بنجاح"
}

# =============================================================================
# تحضير Docker Images
# =============================================================================

prepare_docker_images() {
    print_header "تحضير Docker Images"
    
    print_step "سحب الصور الأساسية..."
    
    # الصور الأساسية المطلوبة
    local base_images=(
        "postgres:15-alpine"
        "redis:7-alpine"
        "elasticsearch:8.11.0"
        "kibana:8.11.0"
        "rabbitmq:3.12-management"
        "nginx:alpine"
        "prom/prometheus:v2.47.0"
        "grafana/grafana:10.2.0"
        "portainer/portainer-ce:latest"
        "containrrr/watchtower:latest"
        "python:3.11-slim"
        "node:20-alpine"
        "ultralytics/ultralytics:latest"
    )
    
    for image in "${base_images[@]}"; do
        print_step "سحب $image..."
        if docker pull "$image"; then
            log_info "تم سحب $image بنجاح"
        else
            log_warning "فشل في سحب $image"
        fi
    done
    
    # سحب صور GPU إذا كانت متوفرة
    if command -v nvidia-smi &> /dev/null; then
        print_step "سحب صور GPU..."
        docker pull nvidia/cuda:11.8-devel-ubuntu20.04 || log_warning "فشل في سحب صورة CUDA"
    fi
    
    log "✅ تم تحضير Docker Images بنجاح"
}

# =============================================================================
# بناء الخدمات المخصصة
# =============================================================================

build_custom_services() {
    print_header "بناء الخدمات المخصصة"
    
    cd "$PROJECT_ROOT"
    
    print_step "بناء الخدمات الأساسية..."
    
    # بناء الخدمات بالترتيب الصحيح
    local services_to_build=(
        "gaara-postgres"
        "gaara-redis"
        "gaara-elasticsearch"
        "gaara-vector-db"
        "gaara-rabbitmq"
        "gaara-memory-system"
        "gaara-resnet50"
        "gaara-ai-agents"
        "gaara-yolo-detection"
        "gaara-image-enhancement"
        "gaara-gpu-processing"
        "gaara-plant-disease-advanced"
        "gaara-plant-hybridization"
        "gaara-monitoring"
        "gaara-auth"
        "gaara-event-system"
        "gaara-auto-learning"
        "gaara-websocket"
        "gaara-notification"
        "gaara-cloud-integration"
        "gaara-real-time-sync"
        "gaara-adaptive-learning"
        "gaara-prometheus"
        "gaara-grafana"
        "gaara-kibana"
        "gaara-nginx"
    )
    
    for service in "${services_to_build[@]}"; do
        print_step "بناء $service..."
        if docker-compose build "$service" --no-cache; then
            log_info "تم بناء $service بنجاح"
        else
            log_error "فشل في بناء $service"
        fi
    done
    
    log "✅ تم بناء الخدمات المخصصة بنجاح"
}

# =============================================================================
# إعداد قواعد البيانات
# =============================================================================

setup_databases() {
    print_header "إعداد قواعد البيانات"
    
    cd "$PROJECT_ROOT"
    
    print_step "بدء خدمات قواعد البيانات..."
    
    # بدء PostgreSQL
    docker-compose up -d gaara-postgres
    log_info "تم بدء PostgreSQL"
    
    # انتظار حتى تصبح قاعدة البيانات جاهزة
    print_step "انتظار جاهزية PostgreSQL..."
    sleep 30
    
    # فحص حالة PostgreSQL
    for i in {1..30}; do
        if docker-compose exec -T gaara-postgres pg_isready -U gaara_user; then
            log_info "PostgreSQL جاهزة"
            break
        fi
        sleep 2
    done
    
    # بدء Redis
    docker-compose up -d gaara-redis
    log_info "تم بدء Redis"
    
    # بدء Elasticsearch
    docker-compose up -d gaara-elasticsearch
    log_info "تم بدء Elasticsearch"
    
    # انتظار حتى تصبح Elasticsearch جاهزة
    print_step "انتظار جاهزية Elasticsearch..."
    sleep 60
    
    # بدء Vector Database
    docker-compose up -d gaara-vector-db
    log_info "تم بدء Vector Database"
    
    log "✅ تم إعداد قواعد البيانات بنجاح"
}

# =============================================================================
# بدء الخدمات بالترتيب الصحيح
# =============================================================================

start_services() {
    print_header "بدء الخدمات بالترتيب الصحيح"
    
    cd "$PROJECT_ROOT"
    
    # المرحلة 1: البنية التحتية
    print_step "المرحلة 1: بدء البنية التحتية..."
    local infrastructure_services=(
        "gaara-postgres"
        "gaara-redis"
        "gaara-elasticsearch"
        "gaara-vector-db"
        "gaara-rabbitmq"
    )
    
    for service in "${infrastructure_services[@]}"; do
        docker-compose up -d "$service"
        log_info "تم بدء $service"
        sleep 5
    done
    
    # انتظار جاهزية البنية التحتية
    print_step "انتظار جاهزية البنية التحتية..."
    sleep 60
    
    # المرحلة 2: خدمات الذكاء الاصطناعي
    print_step "المرحلة 2: بدء خدمات الذكاء الاصطناعي..."
    local ai_services=(
        "gaara-memory-system"
        "gaara-resnet50"
        "gaara-ai-agents"
        "gaara-yolo-detection"
        "gaara-image-enhancement"
        "gaara-gpu-processing"
        "gaara-plant-disease-advanced"
        "gaara-plant-hybridization"
    )
    
    for service in "${ai_services[@]}"; do
        docker-compose up -d "$service"
        log_info "تم بدء $service"
        sleep 10
    done
    
    # المرحلة 3: خدمات النظام
    print_step "المرحلة 3: بدء خدمات النظام..."
    local system_services=(
        "gaara-monitoring"
        "gaara-auth"
        "gaara-event-system"
        "gaara-auto-learning"
        "gaara-websocket"
        "gaara-notification"
        "gaara-cloud-integration"
        "gaara-real-time-sync"
        "gaara-adaptive-learning"
    )
    
    for service in "${system_services[@]}"; do
        docker-compose up -d "$service"
        log_info "تم بدء $service"
        sleep 5
    done
    
    # المرحلة 4: خدمات المراقبة
    print_step "المرحلة 4: بدء خدمات المراقبة..."
    local monitoring_services=(
        "gaara-prometheus"
        "gaara-grafana"
        "gaara-kibana"
    )
    
    for service in "${monitoring_services[@]}"; do
        docker-compose up -d "$service"
        log_info "تم بدء $service"
        sleep 10
    done
    
    # المرحلة 5: خدمات الإدارة
    print_step "المرحلة 5: بدء خدمات الإدارة..."
    docker-compose up -d gaara-portainer
    docker-compose up -d gaara-watchtower
    log_info "تم بدء خدمات الإدارة"
    
    # المرحلة 6: Nginx (آخر خدمة)
    print_step "المرحلة 6: بدء Nginx..."
    docker-compose up -d gaara-nginx
    log_info "تم بدء Nginx"
    
    # المرحلة 7: التطبيق الرئيسي (آخر حاوية)
    print_step "المرحلة 7: بدء التطبيق الرئيسي..."
    docker-compose up -d gaara-main-app
    log_info "تم بدء التطبيق الرئيسي"
    
    log "✅ تم بدء جميع الخدمات بنجاح"
}

# =============================================================================
# فحص صحة النظام
# =============================================================================

health_check() {
    print_header "فحص صحة النظام"
    
    print_step "فحص حالة الحاويات..."
    docker-compose ps
    
    print_step "فحص صحة الخدمات..."
    
    # قائمة الخدمات للفحص
    local services_to_check=(
        "http://localhost:5432"  # PostgreSQL
        "http://localhost:6379"  # Redis
        "http://localhost:9200"  # Elasticsearch
        "http://localhost:5672"  # RabbitMQ
        "http://localhost:8001"  # Memory System
        "http://localhost:8002"  # ResNet-50
        "http://localhost:8003"  # AI Agents
        "http://localhost:8018"  # YOLO Detection
        "http://localhost:8019"  # Image Enhancement
        "http://localhost:8020"  # GPU Processing
        "http://localhost:8021"  # Plant Disease Advanced
        "http://localhost:8022"  # Plant Hybridization
        "http://localhost:9090"  # Prometheus
        "http://localhost:3000"  # Grafana
        "http://localhost:5601"  # Kibana
        "http://localhost:9000"  # Portainer
        "http://localhost:80"    # Nginx
        "http://localhost:8000"  # Main App
    )
    
    local healthy_services=0
    local total_services=${#services_to_check[@]}
    
    for service_url in "${services_to_check[@]}"; do
        if curl -f -s "$service_url/health" > /dev/null 2>&1 || curl -f -s "$service_url" > /dev/null 2>&1; then
            log_info "✅ $service_url - صحي"
            ((healthy_services++))
        else
            log_warning "❌ $service_url - غير متاح"
        fi
    done
    
    log_info "الخدمات الصحية: $healthy_services/$total_services"
    
    if [ $healthy_services -eq $total_services ]; then
        log "🎉 جميع الخدمات تعمل بشكل صحيح!"
    else
        log_warning "بعض الخدمات قد تحتاج وقت إضافي للبدء"
    fi
}

# =============================================================================
# إعداد صفحة الإعدادات الأولية
# =============================================================================

setup_initial_configuration_page() {
    print_header "إعداد صفحة الإعدادات الأولية"
    
    print_step "إنشاء ملف إعدادات النظام..."
    
    cat > "$PROJECT_ROOT/config/system_setup.json" << EOF
{
  "setup_completed": false,
  "setup_timestamp": null,
  "admin_configured": false,
  "database_initialized": false,
  "services_configured": false,
  "first_run": true,
  "setup_wizard_enabled": true,
  "default_language": "ar",
  "timezone": "Asia/Riyadh",
  "setup_steps": {
    "welcome": false,
    "admin_account": false,
    "database_config": false,
    "services_config": false,
    "security_config": false,
    "completion": false
  }
}
EOF
    
    log_info "تم إنشاء ملف إعدادات النظام"
    
    # إنشاء ملف تكوين معالج الإعداد
    cat > "$PROJECT_ROOT/src/setup_wizard_config.py" << EOF
"""
تكوين معالج الإعداد الأولي
Initial Setup Wizard Configuration
"""

SETUP_CONFIG = {
    "wizard_enabled": True,
    "force_setup_on_first_run": True,
    "setup_url": "/setup",
    "redirect_after_setup": "/dashboard",
    "required_steps": [
        "welcome",
        "admin_account", 
        "database_config",
        "services_config",
        "security_config",
        "completion"
    ],
    "optional_steps": [
        "email_config",
        "backup_config",
        "monitoring_config"
    ],
    "setup_timeout_minutes": 30,
    "auto_save_progress": True
}

SETUP_VALIDATION = {
    "admin_password_min_length": 8,
    "require_strong_password": True,
    "require_email_verification": False,
    "database_connection_timeout": 30,
    "service_health_check_timeout": 60
}
EOF
    
    log_info "تم إنشاء تكوين معالج الإعداد"
    
    log "✅ تم إعداد صفحة الإعدادات الأولية"
}

# =============================================================================
# إنشاء ملفات المساعدة
# =============================================================================

create_helper_scripts() {
    print_header "إنشاء ملفات المساعدة"
    
    # سكريبت بدء النظام
    cat > "$PROJECT_ROOT/start.sh" << 'EOF'
#!/bin/bash
echo "🚀 بدء نظام Gaara Scan AI..."
cd "$(dirname "$0")"
docker-compose up -d
echo "✅ تم بدء النظام بنجاح"
echo "🌐 يمكنك الوصول للنظام عبر: http://localhost"
EOF
    
    # سكريبت إيقاف النظام
    cat > "$PROJECT_ROOT/stop.sh" << 'EOF'
#!/bin/bash
echo "⏹️ إيقاف نظام Gaara Scan AI..."
cd "$(dirname "$0")"
docker-compose down
echo "✅ تم إيقاف النظام بنجاح"
EOF
    
    # سكريبت إعادة تشغيل النظام
    cat > "$PROJECT_ROOT/restart.sh" << 'EOF'
#!/bin/bash
echo "🔄 إعادة تشغيل نظام Gaara Scan AI..."
cd "$(dirname "$0")"
docker-compose down
sleep 5
docker-compose up -d
echo "✅ تم إعادة تشغيل النظام بنجاح"
EOF
    
    # سكريبت فحص الحالة
    cat > "$PROJECT_ROOT/status.sh" << 'EOF'
#!/bin/bash
echo "📊 حالة نظام Gaara Scan AI:"
cd "$(dirname "$0")"
docker-compose ps
echo ""
echo "🔍 فحص صحة الخدمات:"
curl -s http://localhost/api/services/health-check | jq '.' 2>/dev/null || echo "API غير متاح"
EOF
    
    # سكريبت النسخ الاحتياطي
    cat > "$PROJECT_ROOT/backup.sh" << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/backup_$TIMESTAMP"
echo "💾 إنشاء نسخة احتياطية..."
mkdir -p "$BACKUP_DIR"
docker-compose exec -T gaara-postgres pg_dump -U gaara_user gaara_scan_ai > "$BACKUP_DIR/database.sql"
cp -r ./data "$BACKUP_DIR/"
cp -r ./config "$BACKUP_DIR/"
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"
echo "✅ تم إنشاء النسخة الاحتياطية: $BACKUP_DIR.tar.gz"
EOF
    
    # سكريبت التحديث
    cat > "$PROJECT_ROOT/update.sh" << 'EOF'
#!/bin/bash
echo "🔄 تحديث نظام Gaara Scan AI..."
cd "$(dirname "$0")"
git pull origin main
docker-compose pull
docker-compose build --no-cache
docker-compose up -d
echo "✅ تم تحديث النظام بنجاح"
EOF
    
    # إعطاء صلاحيات التنفيذ
    chmod +x "$PROJECT_ROOT"/*.sh
    
    log "✅ تم إنشاء ملفات المساعدة"
}

# =============================================================================
# الدالة الرئيسية
# =============================================================================

main() {
    print_header "🚀 بدء تثبيت نظام Gaara Scan AI المتقدم"
    
    log "بدء عملية التثبيت في: $(date)"
    log "مجلد المشروع: $PROJECT_ROOT"
    log "ملف السجل: $LOG_FILE"
    
    # تنفيذ خطوات التثبيت
    check_requirements
    create_directory_structure
    setup_configuration_files
    prepare_docker_images
    build_custom_services
    setup_databases
    start_services
    setup_initial_configuration_page
    create_helper_scripts
    
    # انتظار قبل فحص الصحة
    print_step "انتظار استقرار النظام..."
    sleep 60
    
    health_check
    
    # رسالة الإكمال
    print_header "🎉 تم إكمال التثبيت بنجاح!"
    
    echo -e "${GREEN}"
    echo "============================================================================="
    echo "                    🌟 نظام Gaara Scan AI جاهز للاستخدام! 🌟"
    echo "============================================================================="
    echo ""
    echo "🌐 الروابط المهمة:"
    echo "   • الصفحة الرئيسية: http://localhost"
    echo "   • صفحة الإعدادات: http://localhost/setup"
    echo "   • لوحة التحكم: http://localhost/dashboard"
    echo "   • Grafana: http://localhost:3000"
    echo "   • Portainer: http://localhost:9000"
    echo ""
    echo "📋 الأوامر المفيدة:"
    echo "   • بدء النظام: ./start.sh"
    echo "   • إيقاف النظام: ./stop.sh"
    echo "   • إعادة التشغيل: ./restart.sh"
    echo "   • فحص الحالة: ./status.sh"
    echo "   • نسخة احتياطية: ./backup.sh"
    echo ""
    echo "📁 الملفات المهمة:"
    echo "   • السجلات: $LOG_FILE"
    echo "   • التكوين: .env"
    echo "   • البيانات: ./data/"
    echo ""
    echo "⚠️  ملاحظة مهمة:"
    echo "   يرجى زيارة صفحة الإعدادات أولاً لإكمال التكوين الأولي"
    echo "   http://localhost/setup"
    echo ""
    echo "============================================================================="
    echo -e "${NC}"
    
    log "تم إكمال التثبيت بنجاح في: $(date)"
}

# تنفيذ السكريبت
main "$@"

