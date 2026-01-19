#!/bin/bash
# ملف: /home/ubuntu/gaara_development/scripts/start.sh
# سكريبت تشغيل نظام Gaara AI المحسن
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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# دوال مساعدة
print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}🌱 نظام Gaara AI للزراعة الذكية${NC}"
    echo -e "${PURPLE}================================${NC}"
    echo -e "${CYAN}الإصدار: 2.0.0${NC}"
    echo -e "${CYAN}التاريخ: $(date)${NC}"
    echo -e "${PURPLE}================================${NC}"
}

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

# التحقق من المتطلبات
check_requirements() {
    print_step "التحقق من المتطلبات..."
    
    # التحقق من Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 غير مثبت"
        exit 1
    fi
    print_success "Python 3 متوفر: $(python3 --version)"
    
    # التحقق من Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js غير مثبت"
        exit 1
    fi
    print_success "Node.js متوفر: $(node --version)"
    
    # التحقق من npm
    if ! command -v npm &> /dev/null; then
        print_error "npm غير مثبت"
        exit 1
    fi
    print_success "npm متوفر: $(npm --version)"
    
    # التحقق من Docker (اختياري)
    if command -v docker &> /dev/null; then
        print_success "Docker متوفر: $(docker --version)"
    else
        print_warning "Docker غير متوفر (اختياري)"
    fi
}

# إعداد البيئة
setup_environment() {
    print_step "إعداد البيئة..."
    
    # إنشاء ملف .env إذا لم يكن موجوداً
    if [ ! -f ".env" ]; then
        print_step "إنشاء ملف .env من القالب..."
        cp .env.example .env
        print_success "تم إنشاء ملف .env"
        print_warning "يرجى تحديث متغيرات البيئة في ملف .env"
    fi
    
    # إنشاء المجلدات المطلوبة
    print_step "إنشاء المجلدات المطلوبة..."
    mkdir -p data/{postgres,redis,uploads,logs,ai_models,backups}
    mkdir -p data/logs/{backend,frontend,nginx}
    mkdir -p data/{prometheus,grafana,elasticsearch}
    print_success "تم إنشاء المجلدات"
}

# تثبيت تبعيات الواجهة الخلفية
install_backend_deps() {
    print_step "تثبيت تبعيات الواجهة الخلفية..."
    
    cd gaara_ai_integrated/backend
    
    # إنشاء بيئة افتراضية إذا لم تكن موجودة
    if [ ! -d "venv" ]; then
        print_step "إنشاء بيئة افتراضية..."
        python3 -m venv venv
        print_success "تم إنشاء البيئة الافتراضية"
    fi
    
    # تفعيل البيئة الافتراضية
    source venv/bin/activate
    
    # ترقية pip
    pip install --upgrade pip
    
    # تثبيت التبعيات
    pip install -r requirements.txt
    
    print_success "تم تثبيت تبعيات الواجهة الخلفية"
    
    cd ../..
}

# تثبيت تبعيات الواجهة الأمامية
install_frontend_deps() {
    print_step "تثبيت تبعيات الواجهة الأمامية..."
    
    cd gaara_ai_integrated/frontend
    
    # تثبيت التبعيات
    npm install
    
    print_success "تم تثبيت تبعيات الواجهة الأمامية"
    
    cd ../..
}

# إعداد قاعدة البيانات
setup_database() {
    print_step "إعداد قاعدة البيانات..."
    
    cd gaara_ai_integrated/backend
    source venv/bin/activate
    
    # إنشاء قاعدة البيانات والجداول
    python3 -c "
from main_api import app, db
with app.app_context():
    db.create_all()
    print('✅ تم إنشاء قاعدة البيانات والجداول')
"
    
    print_success "تم إعداد قاعدة البيانات"
    
    cd ../..
}

# تشغيل الواجهة الخلفية
start_backend() {
    print_step "تشغيل الواجهة الخلفية..."
    
    cd gaara_ai_integrated/backend
    source venv/bin/activate
    
    # تشغيل الخادم في الخلفية
    nohup python3 main_api.py > ../../data/logs/backend/app.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../../data/backend.pid
    
    print_success "تم تشغيل الواجهة الخلفية (PID: $BACKEND_PID)"
    
    cd ../..
}

# تشغيل الواجهة الأمامية
start_frontend() {
    print_step "تشغيل الواجهة الأمامية..."
    
    cd gaara_ai_integrated/frontend
    
    # تشغيل خادم التطوير في الخلفية
    nohup npm run dev > ../../data/logs/frontend/app.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../../data/frontend.pid
    
    print_success "تم تشغيل الواجهة الأمامية (PID: $FRONTEND_PID)"
    
    cd ../..
}

# فحص حالة الخدمات
check_services() {
    print_step "فحص حالة الخدمات..."
    
    sleep 5
    
    # فحص الواجهة الخلفية
    if curl -s http://localhost:5000/api/health > /dev/null; then
        print_success "الواجهة الخلفية تعمل بنجاح"
    else
        print_error "الواجهة الخلفية لا تعمل"
    fi
    
    # فحص الواجهة الأمامية
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "الواجهة الأمامية تعمل بنجاح"
    else
        print_warning "الواجهة الأمامية قد تحتاج وقت إضافي للتشغيل"
    fi
}

# عرض معلومات التشغيل
show_info() {
    echo ""
    print_header
    echo -e "${GREEN}🎉 تم تشغيل نظام Gaara AI بنجاح!${NC}"
    echo ""
    echo -e "${CYAN}📱 الواجهة الأمامية: ${NC}http://localhost:3000"
    echo -e "${CYAN}🔧 API الواجهة الخلفية: ${NC}http://localhost:5000/api"
    echo -e "${CYAN}📊 فحص صحة النظام: ${NC}http://localhost:5000/api/health"
    echo ""
    echo -e "${YELLOW}📋 أوامر مفيدة:${NC}"
    echo -e "${CYAN}  • إيقاف النظام: ${NC}./scripts/stop.sh"
    echo -e "${CYAN}  • إعادة تشغيل: ${NC}./scripts/restart.sh"
    echo -e "${CYAN}  • عرض السجلات: ${NC}./scripts/logs.sh"
    echo -e "${CYAN}  • تشغيل بـ Docker: ${NC}docker-compose up -d"
    echo ""
    echo -e "${GREEN}✨ استمتع باستخدام نظام Gaara AI!${NC}"
    echo ""
}

# الدالة الرئيسية
main() {
    print_header
    
    # التحقق من وجود المجلد الصحيح
    if [ ! -d "gaara_ai_integrated" ]; then
        print_error "يجب تشغيل هذا السكريبت من المجلد الجذر للمشروع"
        exit 1
    fi
    
    # تنفيذ الخطوات
    check_requirements
    setup_environment
    install_backend_deps
    install_frontend_deps
    setup_database
    start_backend
    start_frontend
    check_services
    show_info
}

# معالجة الإشارات
cleanup() {
    print_step "إيقاف الخدمات..."
    
    if [ -f "data/backend.pid" ]; then
        kill $(cat data/backend.pid) 2>/dev/null || true
        rm -f data/backend.pid
    fi
    
    if [ -f "data/frontend.pid" ]; then
        kill $(cat data/frontend.pid) 2>/dev/null || true
        rm -f data/frontend.pid
    fi
    
    print_success "تم إيقاف الخدمات"
    exit 0
}

trap cleanup SIGINT SIGTERM

# تشغيل الدالة الرئيسية
main "$@"

