#!/bin/bash
# 🚀 سكريبت تشغيل نظام إدارة المتجر الشامل
# Complete Store Management System Launcher v1.5

set -e  # إيقاف عند أول خطأ

# ألوان للعرض
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# متغيرات النظام
SYSTEM_NAME="نظام إدارة المتجر v1.5"
BACKEND_PORT=5002
FRONTEND_PORT=5502
PYTHON_VERSION="3.8"
NODE_VERSION="18"

# دوال مساعدة
print_header() {
    echo -e "${CYAN}================================================================================================${NC}"
    echo -e "${WHITE}                           🚀 $1 🚀${NC}"
    echo -e "${CYAN}================================================================================================${NC}"
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

print_info() {
    echo -e "${PURPLE}ℹ️  $1${NC}"
}

# فحص متطلبات النظام
check_system_requirements() {
    print_header "فحص متطلبات النظام"
    
    # فحص نظام التشغيل
    print_step "فحص نظام التشغيل..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_success "نظام Linux مدعوم"
        OS_TYPE="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_success "نظام macOS مدعوم"
        OS_TYPE="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        print_success "نظام Windows مدعوم"
        OS_TYPE="windows"
    else
        print_error "نظام التشغيل غير مدعوم: $OSTYPE"
        exit 1
    fi
    
    # فحص Python
    print_step "فحص Python..."
    if command -v python3 &> /dev/null; then
        PYTHON_CURRENT=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        print_success "Python $PYTHON_CURRENT موجود"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CURRENT=$(python --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        print_success "Python $PYTHON_CURRENT موجود"
        PYTHON_CMD="python"
    else
        print_error "Python غير مثبت"
        install_python
    fi
    
    # فحص pip
    print_step "فحص pip..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 موجود"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip موجود"
        PIP_CMD="pip"
    else
        print_error "pip غير مثبت"
        install_pip
    fi
    
    # فحص Node.js
    print_step "فحص Node.js..."
    if command -v node &> /dev/null; then
        NODE_CURRENT=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_CURRENT" -ge "$NODE_VERSION" ]; then
            print_success "Node.js v$(node --version) موجود"
        else
            print_warning "Node.js قديم (v$(node --version)). يُنصح بالترقية إلى v$NODE_VERSION+"
        fi
    else
        print_error "Node.js غير مثبت"
        install_nodejs
    fi
    
    # فحص npm
    print_step "فحص npm..."
    if command -v npm &> /dev/null; then
        print_success "npm v$(npm --version) موجود"
    else
        print_error "npm غير مثبت"
        install_npm
    fi
    
    # فحص Git
    print_step "فحص Git..."
    if command -v git &> /dev/null; then
        print_success "Git v$(git --version | cut -d' ' -f3) موجود"
    else
        print_warning "Git غير مثبت - سيتم تثبيته"
        install_git
    fi
    
    # فحص المساحة المتاحة
    print_step "فحص المساحة المتاحة..."
    if [[ "$OS_TYPE" == "linux" ]] || [[ "$OS_TYPE" == "macos" ]]; then
        AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}' | sed 's/G//')
        if [ "${AVAILABLE_SPACE%.*}" -ge 2 ]; then
            print_success "مساحة كافية متاحة: ${AVAILABLE_SPACE}GB"
        else
            print_warning "مساحة قليلة متاحة: ${AVAILABLE_SPACE}GB"
        fi
    fi
    
    # فحص الذاكرة
    print_step "فحص الذاكرة..."
    if [[ "$OS_TYPE" == "linux" ]]; then
        TOTAL_RAM=$(free -h | awk 'NR==2{print $2}' | sed 's/Gi//')
        if [ "${TOTAL_RAM%.*}" -ge 2 ]; then
            print_success "ذاكرة كافية: ${TOTAL_RAM}GB"
        else
            print_warning "ذاكرة قليلة: ${TOTAL_RAM}GB"
        fi
    fi
}

# تثبيت Python
install_python() {
    print_step "تثبيت Python..."
    if [[ "$OS_TYPE" == "linux" ]]; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif [[ "$OS_TYPE" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install python3
        else
            print_error "يرجى تثبيت Homebrew أولاً أو تثبيت Python يدوياً"
            exit 1
        fi
    else
        print_error "يرجى تثبيت Python يدوياً من https://python.org"
        exit 1
    fi
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
}

# تثبيت pip
install_pip() {
    print_step "تثبيت pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $PYTHON_CMD get-pip.py
    rm get-pip.py
    PIP_CMD="pip3"
}

# تثبيت Node.js
install_nodejs() {
    print_step "تثبيت Node.js..."
    if [[ "$OS_TYPE" == "linux" ]]; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif [[ "$OS_TYPE" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install node
        else
            print_error "يرجى تثبيت Homebrew أولاً أو تثبيت Node.js يدوياً"
            exit 1
        fi
    else
        print_error "يرجى تثبيت Node.js يدوياً من https://nodejs.org"
        exit 1
    fi
}

# تثبيت npm
install_npm() {
    print_step "تثبيت npm..."
    if [[ "$OS_TYPE" == "linux" ]] || [[ "$OS_TYPE" == "macos" ]]; then
        sudo npm install -g npm@latest
    else
        npm install -g npm@latest
    fi
}

# تثبيت Git
install_git() {
    print_step "تثبيت Git..."
    if [[ "$OS_TYPE" == "linux" ]]; then
        sudo apt-get update
        sudo apt-get install -y git
    elif [[ "$OS_TYPE" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install git
        else
            print_error "يرجى تثبيت Git يدوياً"
        fi
    else
        print_error "يرجى تثبيت Git يدوياً من https://git-scm.com"
    fi
}

# إعداد البيئة الافتراضية
setup_virtual_environment() {
    print_header "إعداد البيئة الافتراضية"
    
    cd backend
    
    # إنشاء البيئة الافتراضية
    if [ ! -d "venv" ]; then
        print_step "إنشاء البيئة الافتراضية..."
        $PYTHON_CMD -m venv venv
        print_success "تم إنشاء البيئة الافتراضية"
    else
        print_info "البيئة الافتراضية موجودة مسبقاً"
    fi
    
    # تفعيل البيئة الافتراضية
    print_step "تفعيل البيئة الافتراضية..."
    if [[ "$OS_TYPE" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    print_success "تم تفعيل البيئة الافتراضية"
    
    # ترقية pip
    print_step "ترقية pip..."
    pip install --upgrade pip
    print_success "تم ترقية pip"
    
    cd ..
}

# تثبيت متطلبات Python
install_python_requirements() {
    print_header "تثبيت متطلبات Python"
    
    cd backend
    
    # تفعيل البيئة الافتراضية
    if [[ "$OS_TYPE" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # تثبيت المتطلبات الأساسية
    print_step "تثبيت المتطلبات الأساسية..."
    
    # تثبيت المكتبات واحدة تلو الأخرى لتجنب تعارضات الإصدارات
    print_info "تثبيت Flask Framework..."
    pip install Flask==3.0.0 Flask-CORS==4.0.1 Flask-SQLAlchemy==3.1.1
    
    print_info "تثبيت مكتبات الأمان..."
    pip install Flask-JWT-Extended==4.6.0 Flask-Login==0.6.3 bcrypt==4.1.2 PyJWT==2.8.0 cryptography==41.0.8
    
    print_info "تثبيت مكتبات قاعدة البيانات..."
    pip install SQLAlchemy==2.0.23
    
    print_info "تثبيت مكتبات معالجة البيانات..."
    pip install pandas==2.1.4 numpy==1.25.2 openpyxl==3.1.2 xlsxwriter==3.1.9
    
    print_info "تثبيت مكتبات PDF..."
    pip install reportlab==4.0.7 weasyprint==60.2
    
    print_info "تثبيت مكتبات إضافية..."
    pip install Pillow==10.1.0 requests==2.31.0 python-dotenv==1.0.0 psutil==5.9.6
    
    print_info "تثبيت مكتبات الخادم..."
    pip install gunicorn==21.2.0 Flask-Limiter==3.5.0
    
    # تثبيت باقي المتطلبات
    if [ -f "requirements.txt" ]; then
        print_step "تثبيت باقي المتطلبات من requirements.txt..."
        pip install -r requirements.txt --no-deps || print_warning "بعض المكتبات قد تكون مثبتة مسبقاً"
    fi
    
    print_success "تم تثبيت جميع متطلبات Python"
    
    cd ..
}

# تثبيت متطلبات Node.js
install_nodejs_requirements() {
    print_header "تثبيت متطلبات Node.js"
    
    cd frontend
    
    # تنظيف التثبيت السابق
    if [ -d "node_modules" ]; then
        print_step "تنظيف التثبيت السابق..."
        rm -rf node_modules package-lock.json
    fi
    
    # تثبيت المتطلبات
    print_step "تثبيت متطلبات الواجهة الأمامية..."
    npm install
    
    # فحص الثغرات الأمنية وإصلاحها
    print_step "فحص وإصلاح الثغرات الأمنية..."
    npm audit fix --force || print_warning "بعض الثغرات قد تحتاج إصلاح يدوي"
    
    print_success "تم تثبيت جميع متطلبات Node.js"
    
    cd ..
}

# إعداد قاعدة البيانات
setup_database() {
    print_header "إعداد قاعدة البيانات"
    
    cd backend
    
    # تفعيل البيئة الافتراضية
    if [[ "$OS_TYPE" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # إنشاء مجلد instance إذا لم يكن موجوداً
    if [ ! -d "instance" ]; then
        print_step "إنشاء مجلد قاعدة البيانات..."
        mkdir -p instance
        chmod 700 instance
    fi
    
    # إنشاء قاعدة البيانات
    print_step "إنشاء قاعدة البيانات..."
    $PYTHON_CMD -c "
from src.database import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ تم إنشاء قاعدة البيانات بنجاح')
" || print_warning "قاعدة البيانات موجودة مسبقاً أو حدث خطأ"
    
    print_success "تم إعداد قاعدة البيانات"
    
    cd ..
}

# إنشاء مستخدم admin
create_admin_user() {
    print_header "إنشاء مستخدم Admin"
    
    cd backend
    
    # تفعيل البيئة الافتراضية
    if [[ "$OS_TYPE" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # تشغيل سكريبت إنشاء admin
    if [ -f "../create_admin_user.py" ]; then
        print_step "إنشاء مستخدم admin..."
        $PYTHON_CMD ../create_admin_user.py
    else
        print_warning "ملف إنشاء admin غير موجود"
    fi
    
    cd ..
}

# بناء الواجهة الأمامية
build_frontend() {
    print_header "بناء الواجهة الأمامية"
    
    cd frontend
    
    print_step "بناء الواجهة الأمامية للإنتاج..."
    npm run build
    
    print_success "تم بناء الواجهة الأمامية بنجاح"
    
    cd ..
}

# تطبيق الأمان
apply_security() {
    print_header "تطبيق الأمان العسكري"
    
    # تشغيل الأمان العسكري
    if [ -f "military_grade_security.py" ]; then
        print_step "تطبيق الأمان العسكري..."
        $PYTHON_CMD military_grade_security.py
    fi
    
    # تشغيل تقوية الأمان
    if [ -f "security_hardening.sh" ]; then
        print_step "تطبيق تقوية الأمان..."
        chmod +x security_hardening.sh
        ./security_hardening.sh
    fi
    
    print_success "تم تطبيق الأمان بنجاح"
}

# تشغيل النظام
start_system() {
    print_header "تشغيل النظام"
    
    # إنشاء ملفات السجلات
    mkdir -p logs
    
    # تشغيل الواجهة الخلفية
    print_step "تشغيل الواجهة الخلفية على المنفذ $BACKEND_PORT..."
    cd backend
    
    # تفعيل البيئة الافتراضية
    if [[ "$OS_TYPE" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # تشغيل الخادم في الخلفية
    nohup $PYTHON_CMD app.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    
    cd ..
    
    # انتظار تشغيل الواجهة الخلفية
    print_step "انتظار تشغيل الواجهة الخلفية..."
    sleep 5
    
    # فحص حالة الواجهة الخلفية
    if curl -s http://localhost:$BACKEND_PORT/api/health > /dev/null; then
        print_success "الواجهة الخلفية تعمل على http://localhost:$BACKEND_PORT"
    else
        print_warning "قد تحتاج الواجهة الخلفية وقت إضافي للتشغيل"
    fi
    
    # تشغيل الواجهة الأمامية
    print_step "تشغيل الواجهة الأمامية على المنفذ $FRONTEND_PORT..."
    cd frontend
    
    # تشغيل الخادم في الخلفية
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    
    cd ..
    
    # انتظار تشغيل الواجهة الأمامية
    print_step "انتظار تشغيل الواجهة الأمامية..."
    sleep 10
    
    print_success "تم تشغيل النظام بنجاح!"
    
    # عرض معلومات النظام
    print_info "🌐 الواجهة الأمامية: http://localhost:$FRONTEND_PORT"
    print_info "🔧 الواجهة الخلفية: http://localhost:$BACKEND_PORT"
    print_info "📊 API الصحة: http://localhost:$BACKEND_PORT/api/health"
    print_info "📝 سجلات النظام: logs/"
    
    # عرض معلومات admin
    if [ -f "admin_credentials.json" ]; then
        print_info "👑 معلومات Admin:"
        cat admin_credentials.json | grep -E "(username|email)" | sed 's/^/     /'
    fi
}

# إيقاف النظام
stop_system() {
    print_header "إيقاف النظام"
    
    # إيقاف الواجهة الخلفية
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            print_step "إيقاف الواجهة الخلفية..."
            kill $BACKEND_PID
            rm logs/backend.pid
            print_success "تم إيقاف الواجهة الخلفية"
        fi
    fi
    
    # إيقاف الواجهة الأمامية
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            print_step "إيقاف الواجهة الأمامية..."
            kill $FRONTEND_PID
            rm logs/frontend.pid
            print_success "تم إيقاف الواجهة الأمامية"
        fi
    fi
    
    # إيقاف العمليات المتبقية
    pkill -f "python.*app.py" 2>/dev/null || true
    pkill -f "npm.*run.*dev" 2>/dev/null || true
    
    print_success "تم إيقاف النظام بالكامل"
}

# فحص حالة النظام
check_system_status() {
    print_header "فحص حالة النظام"
    
    # فحص الواجهة الخلفية
    if curl -s http://localhost:$BACKEND_PORT/api/health > /dev/null; then
        print_success "الواجهة الخلفية تعمل ✅"
    else
        print_error "الواجهة الخلفية لا تعمل ❌"
    fi
    
    # فحص الواجهة الأمامية
    if curl -s http://localhost:$FRONTEND_PORT > /dev/null; then
        print_success "الواجهة الأمامية تعمل ✅"
    else
        print_error "الواجهة الأمامية لا تعمل ❌"
    fi
    
    # فحص العمليات
    if pgrep -f "python.*app.py" > /dev/null; then
        print_info "عملية Python Backend: $(pgrep -f 'python.*app.py')"
    fi
    
    if pgrep -f "npm.*run.*dev" > /dev/null; then
        print_info "عملية NPM Frontend: $(pgrep -f 'npm.*run.*dev')"
    fi
}

# عرض المساعدة
show_help() {
    echo -e "${WHITE}🚀 سكريبت تشغيل نظام إدارة المتجر الشامل v1.5${NC}"
    echo ""
    echo -e "${CYAN}الاستخدام:${NC}"
    echo "  $0 [الأمر]"
    echo ""
    echo -e "${CYAN}الأوامر المتاحة:${NC}"
    echo -e "  ${GREEN}install${NC}     - تثبيت جميع المتطلبات والإعدادات"
    echo -e "  ${GREEN}start${NC}       - تشغيل النظام (الواجهة الأمامية والخلفية)"
    echo -e "  ${GREEN}stop${NC}        - إيقاف النظام"
    echo -e "  ${GREEN}restart${NC}     - إعادة تشغيل النظام"
    echo -e "  ${GREEN}status${NC}      - فحص حالة النظام"
    echo -e "  ${GREEN}build${NC}       - بناء الواجهة الأمامية فقط"
    echo -e "  ${GREEN}setup${NC}       - إعداد قاعدة البيانات ومستخدم admin"
    echo -e "  ${GREEN}security${NC}    - تطبيق الأمان العسكري"
    echo -e "  ${GREEN}check${NC}       - فحص متطلبات النظام"
    echo -e "  ${GREEN}help${NC}        - عرض هذه المساعدة"
    echo ""
    echo -e "${CYAN}أمثلة:${NC}"
    echo "  $0 install    # تثبيت كامل للنظام"
    echo "  $0 start      # تشغيل النظام"
    echo "  $0 status     # فحص حالة النظام"
    echo ""
    echo -e "${YELLOW}ملاحظة: يُنصح بتشغيل 'install' أولاً قبل 'start'${NC}"
}

# الدالة الرئيسية
main() {
    case "${1:-help}" in
        "install")
            check_system_requirements
            setup_virtual_environment
            install_python_requirements
            install_nodejs_requirements
            setup_database
            create_admin_user
            apply_security
            print_success "🎉 تم تثبيت النظام بالكامل بنجاح!"
            ;;
        "start")
            start_system
            ;;
        "stop")
            stop_system
            ;;
        "restart")
            stop_system
            sleep 2
            start_system
            ;;
        "status")
            check_system_status
            ;;
        "build")
            build_frontend
            ;;
        "setup")
            setup_database
            create_admin_user
            ;;
        "security")
            apply_security
            ;;
        "check")
            check_system_requirements
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "أمر غير معروف: $1"
            show_help
            exit 1
            ;;
    esac
}

# تشغيل الدالة الرئيسية
main "$@"
