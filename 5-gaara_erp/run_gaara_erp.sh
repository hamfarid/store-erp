#!/bin/bash

# =============================================================================
# Gaara ERP v12 - Enhanced Startup Script
# =============================================================================
# تاريخ الإنشاء: 05 أكتوبر 2025
# الإصدار: v12.0.0
# الحالة: 77 وحدة مفعلة ومستقرة
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/ubuntu/gaara_erp_v12/gaara_erp"
VENV_DIR="/home/ubuntu/gaara_erp_v12/venv"
LOG_DIR="/home/ubuntu/gaara_erp_v12/logs"
BACKUP_DIR="/home/ubuntu/gaara_erp_v12/backups"
PORT=5001
HOST="0.0.0.0"

# Create necessary directories
mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Banner
print_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 Gaara ERP v12 🚀                      ║"
    echo "║              نظام تخطيط موارد المؤسسات المتقدم              ║"
    echo "║                                                              ║"
    echo "║  📊 77 وحدة مفعلة | 🤖 ذكاء اصطناعي | 🌾 نظام زراعي      ║"
    echo "║  🔐 أمان متقدم | 🌐 تكامل خارجي | 📱 واجهات متجاوبة       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# System check
check_system() {
    log "🔍 فحص متطلبات النظام..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 غير مثبت"
        exit 1
    fi
    
    # Check if project directory exists
    if [ ! -d "$PROJECT_DIR" ]; then
        error "مجلد المشروع غير موجود: $PROJECT_DIR"
        exit 1
    fi
    
    # Check if manage.py exists
    if [ ! -f "$PROJECT_DIR/manage.py" ]; then
        error "ملف manage.py غير موجود"
        exit 1
    fi
    
    info "✅ فحص النظام مكتمل"
}

# Setup virtual environment
setup_venv() {
    log "🐍 إعداد البيئة الافتراضية..."
    
    if [ ! -d "$VENV_DIR" ]; then
        info "إنشاء بيئة افتراضية جديدة..."
        python3 -m venv "$VENV_DIR"
    fi
    
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        info "تثبيت المتطلبات الأساسية..."
        pip install -r "$PROJECT_DIR/requirements.txt"
    fi
    
    if [ -f "$PROJECT_DIR/requirements-dev.txt" ] && [ "$1" = "dev" ]; then
        info "تثبيت متطلبات التطوير..."
        pip install -r "$PROJECT_DIR/requirements-dev.txt"
    fi
    
    info "✅ البيئة الافتراضية جاهزة"
}

# Database operations
setup_database() {
    log "🗄️ إعداد قاعدة البيانات..."
    
    cd "$PROJECT_DIR"
    
    # Check for migrations
    info "فحص الترحيلات..."
    python manage.py showmigrations --plan > /dev/null 2>&1 || {
        warning "مشكلة في الترحيلات، محاولة إصلاح..."
    }
    
    # Make migrations
    info "إنشاء ترحيلات جديدة..."
    python manage.py makemigrations --noinput || warning "فشل في إنشاء بعض الترحيلات"
    
    # Apply migrations
    info "تطبيق الترحيلات..."
    python manage.py migrate --noinput || warning "فشل في تطبيق بعض الترحيلات"
    
    # Collect static files
    info "جمع الملفات الثابتة..."
    python manage.py collectstatic --noinput --clear || warning "فشل في جمع الملفات الثابتة"
    
    info "✅ قاعدة البيانات جاهزة"
}

# Create superuser
create_superuser() {
    log "👤 إنشاء مستخدم إداري..."
    
    cd "$PROJECT_DIR"
    
    # Check if superuser exists
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@gaara-erp.com', 'Admin@123456')
    print('تم إنشاء المستخدم الإداري: admin / Admin@123456')
else:
    print('المستخدم الإداري موجود بالفعل')
" 2>/dev/null || warning "فشل في إنشاء المستخدم الإداري"
    
    info "✅ المستخدم الإداري جاهز"
}

# System health check
health_check() {
    log "🏥 فحص صحة النظام..."
    
    cd "$PROJECT_DIR"
    
    # Django system check
    info "فحص Django..."
    python manage.py check --deploy > "$LOG_DIR/system_check.log" 2>&1 || {
        warning "توجد تحذيرات في النظام، راجع: $LOG_DIR/system_check.log"
    }
    
    # Count active modules
    ACTIVE_MODULES=$(python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
import django
django.setup()
from django.conf import settings
print(len(settings.INSTALLED_APPS))
" 2>/dev/null || echo "غير معروف")
    
    info "📊 عدد الوحدات المفعلة: $ACTIVE_MODULES"
    info "✅ فحص الصحة مكتمل"
}

# Start services
start_services() {
    log "🚀 بدء تشغيل الخدمات..."
    
    cd "$PROJECT_DIR"
    
    # Start Redis if available
    if command -v redis-server &> /dev/null; then
        info "بدء تشغيل Redis..."
        redis-server --daemonize yes --port 6379 || warning "فشل في تشغيل Redis"
    fi
    
    # Start Celery if configured
    if [ -f "celerybeat-schedule" ] || grep -q "CELERY" gaara_erp/settings/base.py; then
        info "بدء تشغيل Celery Worker..."
        celery -A gaara_erp.celery worker --detach --loglevel=info || warning "فشل في تشغيل Celery Worker"
        
        info "بدء تشغيل Celery Beat..."
        celery -A gaara_erp.celery beat --detach --loglevel=info || warning "فشل في تشغيل Celery Beat"
    fi
    
    info "✅ الخدمات المساعدة جاهزة"
}

# Start Django server
start_server() {
    log "🌐 بدء تشغيل خادم Django..."
    
    cd "$PROJECT_DIR"
    
    # Check if port is available
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
        warning "المنفذ $PORT مستخدم، محاولة إيقاف العملية السابقة..."
        pkill -f "runserver.*:$PORT" || true
        sleep 2
    fi
    
    # Start server
    info "🚀 تشغيل الخادم على http://$HOST:$PORT"
    info "📱 لوحة الإدارة: http://$HOST:$PORT/admin/"
    info "🤖 لوحة الذكاء الاصطناعي: http://$HOST:$PORT/ai-analytics/"
    info "📊 واجهات API: http://$HOST:$PORT/api/"
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   🎉 النظام جاهز للاستخدام! 🎉              ║"
    echo "║                                                              ║"
    echo "║  المستخدم الإداري: admin                                    ║"
    echo "║  كلمة المرور: Admin@123456                                  ║"
    echo "║                                                              ║"
    echo "║  للإيقاف: اضغط Ctrl+C                                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Start the server
    python manage.py runserver $HOST:$PORT
}

# Backup function
create_backup() {
    log "💾 إنشاء نسخة احتياطية..."
    
    BACKUP_NAME="gaara_erp_backup_$(date +%Y%m%d_%H%M%S)"
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
    
    # Create backup directory
    mkdir -p "$BACKUP_PATH"
    
    # Backup database
    cd "$PROJECT_DIR"
    python manage.py dumpdata --natural-foreign --natural-primary > "$BACKUP_PATH/database.json" || warning "فشل في نسخ قاعدة البيانات"
    
    # Backup media files
    if [ -d "media" ]; then
        cp -r media "$BACKUP_PATH/" || warning "فشل في نسخ ملفات الوسائط"
    fi
    
    # Backup configuration
    cp -r gaara_erp/settings "$BACKUP_PATH/" || warning "فشل في نسخ الإعدادات"
    cp .env "$BACKUP_PATH/" 2>/dev/null || warning "ملف .env غير موجود"
    
    # Create archive
    cd "$BACKUP_DIR"
    tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME" && rm -rf "$BACKUP_NAME"
    
    info "✅ تم إنشاء النسخة الاحتياطية: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
}

# Show system info
show_info() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    📊 معلومات النظام                        ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  الإصدار: v12.0.0                                          ║"
    echo "║  الوحدات المفعلة: 77 وحدة                                  ║"
    echo "║  قاعدة البيانات: SQLite (افتراضي)                          ║"
    echo "║  الأمان: محسن ومفعل                                        ║"
    echo "║  الذكاء الاصطناعي: متكامل                                  ║"
    echo "║  النظام الزراعي: متخصص                                     ║"
    echo "║  التكامل الخارجي: شامل                                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Main function
main() {
    print_banner
    
    case "${1:-start}" in
        "start"|"")
            check_system
            setup_venv
            setup_database
            create_superuser
            health_check
            start_services
            start_server
            ;;
        "quick")
            check_system
            source "$VENV_DIR/bin/activate" 2>/dev/null || setup_venv
            cd "$PROJECT_DIR"
            start_server
            ;;
        "dev")
            check_system
            setup_venv "dev"
            setup_database
            create_superuser
            health_check
            start_services
            start_server
            ;;
        "backup")
            create_backup
            ;;
        "info")
            show_info
            ;;
        "health")
            check_system
            source "$VENV_DIR/bin/activate"
            health_check
            ;;
        *)
            echo "الاستخدام: $0 [start|quick|dev|backup|info|health]"
            echo ""
            echo "الأوامر:"
            echo "  start  - تشغيل كامل (افتراضي)"
            echo "  quick  - تشغيل سريع"
            echo "  dev    - وضع التطوير"
            echo "  backup - إنشاء نسخة احتياطية"
            echo "  info   - عرض معلومات النظام"
            echo "  health - فحص صحة النظام"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
