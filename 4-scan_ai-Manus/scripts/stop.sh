#!/bin/bash
# ملف: /home/ubuntu/gaara_development/scripts/stop.sh
# سكريبت إيقاف نظام Gaara AI
# الإصدار: 2.0.0
# تم الإنشاء: 2025-01-07
# المطور: Gaara Group & Manus AI

set -e

# ألوان للإخراج
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}🛑 إيقاف نظام Gaara AI${NC}"
    echo -e "${PURPLE}================================${NC}"
}

# إيقاف الواجهة الخلفية
stop_backend() {
    print_step "إيقاف الواجهة الخلفية..."
    
    if [ -f "data/backend.pid" ]; then
        PID=$(cat data/backend.pid)
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            sleep 2
            if kill -0 $PID 2>/dev/null; then
                kill -9 $PID
            fi
            print_success "تم إيقاف الواجهة الخلفية (PID: $PID)"
        else
            print_warning "الواجهة الخلفية غير قيد التشغيل"
        fi
        rm -f data/backend.pid
    else
        print_warning "لم يتم العثور على ملف PID للواجهة الخلفية"
    fi
}

# إيقاف الواجهة الأمامية
stop_frontend() {
    print_step "إيقاف الواجهة الأمامية..."
    
    if [ -f "data/frontend.pid" ]; then
        PID=$(cat data/frontend.pid)
        if kill -0 $PID 2>/dev/null; then
            kill $PID
            sleep 2
            if kill -0 $PID 2>/dev/null; then
                kill -9 $PID
            fi
            print_success "تم إيقاف الواجهة الأمامية (PID: $PID)"
        else
            print_warning "الواجهة الأمامية غير قيد التشغيل"
        fi
        rm -f data/frontend.pid
    else
        print_warning "لم يتم العثور على ملف PID للواجهة الأمامية"
    fi
}

# إيقاف العمليات المتبقية
cleanup_processes() {
    print_step "تنظيف العمليات المتبقية..."
    
    # إيقاف عمليات Python المتعلقة بـ Gaara
    pkill -f "main_api.py" 2>/dev/null || true
    
    # إيقاف عمليات Node.js المتعلقة بـ Gaara
    pkill -f "vite.*gaara" 2>/dev/null || true
    
    print_success "تم تنظيف العمليات"
}

# إيقاف Docker Compose إذا كان يعمل
stop_docker() {
    print_step "فحص Docker Compose..."
    
    if [ -f "docker-compose.yml" ] && command -v docker-compose &> /dev/null; then
        if docker-compose ps | grep -q "Up"; then
            print_step "إيقاف خدمات Docker Compose..."
            docker-compose down
            print_success "تم إيقاف خدمات Docker"
        else
            print_warning "خدمات Docker غير قيد التشغيل"
        fi
    fi
}

# الدالة الرئيسية
main() {
    print_header
    
    stop_backend
    stop_frontend
    cleanup_processes
    stop_docker
    
    echo ""
    print_success "تم إيقاف نظام Gaara AI بنجاح"
    echo ""
}

# تشغيل الدالة الرئيسية
main "$@"

