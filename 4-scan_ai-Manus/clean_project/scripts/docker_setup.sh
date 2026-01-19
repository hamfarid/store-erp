#!/bin/bash
# File: /home/ubuntu/clean_project/scripts/docker_setup.sh
# سكريبت إعداد وتثبيت Docker لنظام Gaara Scan AI

set -e

# ألوان للمخرجات
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دوال المساعدة
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# فحص نظام التشغيل
check_os() {
    log_info "فحص نظام التشغيل..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$NAME
            VER=$VERSION_ID
            log_info "نظام التشغيل: $OS $VER"
        else
            log_error "لا يمكن تحديد نظام التشغيل"
            exit 1
        fi
    else
        log_error "هذا السكريبت يدعم Linux فقط"
        exit 1
    fi
}

# فحص المتطلبات
check_requirements() {
    log_info "فحص المتطلبات الأساسية..."
    
    # فحص الذاكرة
    MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    if [ $MEMORY_GB -lt 4 ]; then
        log_warning "الذاكرة المتاحة: ${MEMORY_GB}GB (الحد الأدنى: 4GB)"
    else
        log_success "الذاكرة المتاحة: ${MEMORY_GB}GB"
    fi
    
    # فحص مساحة القرص
    DISK_GB=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
    if [ $DISK_GB -lt 20 ]; then
        log_warning "مساحة القرص المتاحة: ${DISK_GB}GB (الحد الأدنى: 20GB)"
    else
        log_success "مساحة القرص المتاحة: ${DISK_GB}GB"
    fi
    
    # فحص المعالج
    CPU_CORES=$(nproc)
    if [ $CPU_CORES -lt 2 ]; then
        log_warning "عدد أنوية المعالج: $CPU_CORES (الحد الأدنى: 2)"
    else
        log_success "عدد أنوية المعالج: $CPU_CORES"
    fi
}

# تثبيت Docker
install_docker() {
    log_info "فحص تثبيت Docker..."
    
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        log_success "Docker مثبت بالفعل - الإصدار: $DOCKER_VERSION"
        return 0
    fi
    
    log_info "تثبيت Docker..."
    
    # تحديث النظام
    sudo apt-get update
    
    # تثبيت المتطلبات
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # إضافة مفتاح Docker GPG
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # إضافة مستودع Docker
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # تثبيت Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # إضافة المستخدم إلى مجموعة docker
    sudo usermod -aG docker $USER
    
    # تفعيل Docker
    sudo systemctl enable docker
    sudo systemctl start docker
    
    log_success "تم تثبيت Docker بنجاح"
    log_warning "يرجى إعادة تسجيل الدخول أو تشغيل: newgrp docker"
}

# إعداد ملف البيئة
setup_env_file() {
    log_info "إعداد ملف البيئة..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            log_success "تم إنشاء ملف .env من .env.example"
        else
            log_error "ملف .env.example غير موجود"
            return 1
        fi
    else
        log_info "ملف .env موجود بالفعل"
    fi
    
    # توليد كلمات مرور عشوائية
    if ! grep -q "your_secure_password_here" .env; then
        log_info "ملف .env محدث بالفعل"
        return 0
    fi
    
    log_info "توليد كلمات مرور آمنة..."
    
    # توليد كلمات مرور
    DB_PASSWORD=$(openssl rand -base64 32)
    SECRET_KEY=$(openssl rand -base64 64)
    JWT_SECRET=$(openssl rand -base64 32)
    ENCRYPTION_KEY=$(openssl rand -base64 32)
    GRAFANA_PASSWORD=$(openssl rand -base64 16)
    PORTAINER_PASSWORD=$(openssl rand -base64 16)
    
    # تحديث ملف .env
    sed -i "s/your_secure_password_here/$DB_PASSWORD/g" .env
    sed -i "s/your_secret_key_here/$SECRET_KEY/g" .env
    sed -i "s/your_jwt_secret_here/$JWT_SECRET/g" .env
    sed -i "s/your_encryption_key_here/$ENCRYPTION_KEY/g" .env
    sed -i "s/admin_password_here/$GRAFANA_PASSWORD/g" .env
    sed -i "s/portainer_password_here/$PORTAINER_PASSWORD/g" .env
    
    log_success "تم توليد كلمات مرور آمنة"
    
    # حفظ كلمات المرور في ملف منفصل
    cat > .passwords << EOF
# كلمات المرور المولدة تلقائياً لنظام Gaara Scan AI
# تاريخ الإنشاء: $(date)

قاعدة البيانات: $DB_PASSWORD
Grafana Admin: $GRAFANA_PASSWORD
Portainer Admin: $PORTAINER_PASSWORD

# احتفظ بهذا الملف في مكان آمن وقم بحذفه بعد حفظ كلمات المرور
EOF
    
    chmod 600 .passwords
    log_success "تم حفظ كلمات المرور في ملف .passwords"
}

# إنشاء المجلدات المطلوبة
create_directories() {
    log_info "إنشاء المجلدات المطلوبة..."
    
    mkdir -p data/postgres
    mkdir -p data/redis
    mkdir -p data/uploads
    mkdir -p data/models
    mkdir -p data/logs
    mkdir -p data/backups
    mkdir -p data/grafana
    mkdir -p data/prometheus
    mkdir -p data/portainer
    
    # تعيين الصلاحيات
    chmod 755 data
    chmod 700 data/postgres
    chmod 755 data/uploads
    chmod 755 data/models
    chmod 755 data/logs
    chmod 755 data/backups
    
    log_success "تم إنشاء المجلدات بنجاح"
}

# بناء الحاويات
build_containers() {
    log_info "بناء حاويات Docker..."
    
    # فحص وجود ملف docker-compose.yml
    if [ ! -f docker-compose.yml ]; then
        log_error "ملف docker-compose.yml غير موجود"
        return 1
    fi
    
    # بناء الحاويات
    docker compose build --parallel
    
    if [ $? -eq 0 ]; then
        log_success "تم بناء الحاويات بنجاح"
    else
        log_error "فشل في بناء الحاويات"
        return 1
    fi
}

# تشغيل النظام
start_system() {
    log_info "تشغيل نظام Gaara Scan AI..."
    
    # تشغيل الخدمات الأساسية أولاً
    docker compose up -d postgres redis
    
    # انتظار تشغيل قاعدة البيانات
    log_info "انتظار تشغيل قاعدة البيانات..."
    sleep 10
    
    # تشغيل باقي الخدمات
    docker compose up -d
    
    # انتظار تشغيل جميع الخدمات
    log_info "انتظار تشغيل جميع الخدمات..."
    sleep 30
    
    # فحص حالة الخدمات
    if docker compose ps | grep -q "Up"; then
        log_success "تم تشغيل النظام بنجاح"
        show_access_info
    else
        log_error "فشل في تشغيل بعض الخدمات"
        docker compose ps
        return 1
    fi
}

# عرض معلومات الوصول
show_access_info() {
    echo ""
    echo "=================================="
    echo "🎉 تم تثبيت نظام Gaara Scan AI بنجاح!"
    echo "=================================="
    echo ""
    echo "📱 روابط الوصول:"
    echo "  • التطبيق الرئيسي: http://localhost"
    echo "  • لوحة الإدارة: http://localhost/admin"
    echo "  • Portainer: http://localhost:9000"
    echo "  • Grafana: http://localhost:3000"
    echo "  • Prometheus: http://localhost:9090"
    echo ""
    echo "🔑 معلومات تسجيل الدخول:"
    echo "  • راجع ملف .passwords للحصول على كلمات المرور"
    echo ""
    echo "📚 الأوامر المفيدة:"
    echo "  • عرض حالة الخدمات: docker compose ps"
    echo "  • مراقبة السجلات: docker compose logs -f"
    echo "  • إيقاف النظام: docker compose down"
    echo "  • إعادة تشغيل: docker compose restart"
    echo ""
    echo "📖 للمزيد من المعلومات، راجع:"
    echo "  • docs/docker_comprehensive_guide.md"
    echo ""
}

# فحص صحة النظام
health_check() {
    log_info "فحص صحة النظام..."
    
    # فحص الخدمات
    SERVICES=("gaara-main" "gaara-admin" "postgres" "redis" "nginx")
    
    for service in "${SERVICES[@]}"; do
        if docker compose ps $service | grep -q "Up"; then
            log_success "$service: يعمل بشكل طبيعي"
        else
            log_error "$service: لا يعمل"
        fi
    done
    
    # فحص الاتصال
    if curl -s http://localhost/health > /dev/null; then
        log_success "الاتصال بالتطبيق: ناجح"
    else
        log_warning "الاتصال بالتطبيق: فشل (قد يحتاج وقت إضافي للتشغيل)"
    fi
}

# الدالة الرئيسية
main() {
    echo "🌱 مرحباً بك في مثبت نظام Gaara Scan AI"
    echo "========================================"
    echo ""
    
    # فحص إذا كان المستخدم root
    if [ "$EUID" -eq 0 ]; then
        log_error "لا تشغل هذا السكريبت كمستخدم root"
        exit 1
    fi
    
    # تنفيذ خطوات التثبيت
    check_os
    check_requirements
    install_docker
    setup_env_file
    create_directories
    build_containers
    start_system
    health_check
    
    echo ""
    echo "✅ تم الانتهاء من التثبيت!"
    echo ""
    echo "⚠️  ملاحظات مهمة:"
    echo "  • احتفظ بملف .passwords في مكان آمن"
    echo "  • قم بتغيير كلمات المرور الافتراضية"
    echo "  • فعل HTTPS في بيئة الإنتاج"
    echo "  • راجع دليل الأمان في التوثيق"
    echo ""
}

# تشغيل السكريبت
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

