#!/bin/bash
# 🔧 سكريبت صيانة نظام إدارة المتجر
# Store Management System Maintenance Script

set -e

# ألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

print_header() {
    echo -e "${CYAN}================================================================================================${NC}"
    echo -e "${WHITE}                           🔧 $1 🔧${NC}"
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

# نسخ احتياطية
backup_system() {
    print_header "إنشاء نسخة احتياطية"
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    print_step "نسخ قاعدة البيانات..."
    if [ -f "backend/instance/store.db" ]; then
        cp backend/instance/store.db "$BACKUP_DIR/"
        print_success "تم نسخ قاعدة البيانات"
    fi
    
    print_step "نسخ الإعدادات..."
    cp backend/.env "$BACKUP_DIR/" 2>/dev/null || print_warning "ملف .env غير موجود"
    cp admin_credentials.json "$BACKUP_DIR/" 2>/dev/null || print_warning "ملف admin_credentials.json غير موجود"
    
    print_step "ضغط النسخة الاحتياطية..."
    tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR/"
    rm -rf "$BACKUP_DIR"
    
    print_success "تم إنشاء النسخة الاحتياطية: $BACKUP_DIR.tar.gz"
}

# تنظيف النظام
cleanup_system() {
    print_header "تنظيف النظام"
    
    print_step "تنظيف ملفات Python المؤقتة..."
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    print_success "تم تنظيف ملفات Python"
    
    print_step "تنظيف ملفات Node.js المؤقتة..."
    rm -rf frontend/.next 2>/dev/null || true
    rm -rf frontend/dist 2>/dev/null || true
    print_success "تم تنظيف ملفات Node.js"
    
    print_step "تنظيف السجلات القديمة..."
    find logs/ -name "*.log" -mtime +7 -delete 2>/dev/null || true
    print_success "تم تنظيف السجلات القديمة"
    
    print_step "تنظيف النسخ الاحتياطية القديمة..."
    find backups/ -name "*.tar.gz" -mtime +30 -delete 2>/dev/null || true
    print_success "تم تنظيف النسخ الاحتياطية القديمة"
}

# تحديث النظام
update_system() {
    print_header "تحديث النظام"
    
    print_step "تحديث متطلبات Python..."
    cd backend
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
    pip install --upgrade pip
    pip install -r requirements.txt --upgrade
    cd ..
    print_success "تم تحديث متطلبات Python"
    
    print_step "تحديث متطلبات Node.js..."
    cd frontend
    npm update
    npm audit fix --force || print_warning "بعض الثغرات تحتاج إصلاح يدوي"
    cd ..
    print_success "تم تحديث متطلبات Node.js"
}

# فحص الأمان
security_check() {
    print_header "فحص الأمان"
    
    print_step "فحص الملفات الحساسة..."
    if [ -f "backend/.env" ]; then
        PERMS=$(stat -c "%a" backend/.env)
        if [ "$PERMS" != "600" ]; then
            chmod 600 backend/.env
            print_warning "تم تصحيح صلاحيات ملف .env"
        else
            print_success "صلاحيات ملف .env صحيحة"
        fi
    fi
    
    print_step "فحص كلمات المرور المكشوفة..."
    if grep -r "password.*=" . --exclude-dir=venv --exclude-dir=node_modules --exclude="*.log" | grep -v ".env" | grep -v "admin_credentials.json"; then
        print_warning "تم العثور على كلمات مرور مكشوفة في الكود"
    else
        print_success "لا توجد كلمات مرور مكشوفة"
    fi
    
    print_step "فحص الثغرات الأمنية..."
    cd frontend
    npm audit --audit-level=high || print_warning "توجد ثغرات أمنية في Node.js"
    cd ..
}

# فحص الأداء
performance_check() {
    print_header "فحص الأداء"
    
    print_step "فحص استخدام المساحة..."
    du -sh . | awk '{print "حجم المشروع: " $1}'
    
    print_step "فحص قاعدة البيانات..."
    if [ -f "backend/instance/store.db" ]; then
        DB_SIZE=$(du -sh backend/instance/store.db | awk '{print $1}')
        echo "حجم قاعدة البيانات: $DB_SIZE"
        
        # فحص عدد الجداول
        cd backend
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
        TABLES=$(python -c "
import sqlite3
conn = sqlite3.connect('instance/store.db')
cursor = conn.cursor()
cursor.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\")
print(cursor.fetchone()[0])
conn.close()
" 2>/dev/null || echo "غير معروف")
        echo "عدد الجداول: $TABLES"
        cd ..
    fi
    
    print_step "فحص العمليات النشطة..."
    if pgrep -f "python.*app.py" > /dev/null; then
        echo "الواجهة الخلفية: نشطة ✅"
    else
        echo "الواجهة الخلفية: متوقفة ❌"
    fi
    
    if pgrep -f "npm.*run.*dev" > /dev/null; then
        echo "الواجهة الأمامية: نشطة ✅"
    else
        echo "الواجهة الأمامية: متوقفة ❌"
    fi
}

# إصلاح المشاكل الشائعة
fix_common_issues() {
    print_header "إصلاح المشاكل الشائعة"
    
    print_step "إصلاح صلاحيات الملفات..."
    chmod +x *.sh 2>/dev/null || true
    chmod 600 backend/.env 2>/dev/null || true
    chmod 600 admin_credentials.json 2>/dev/null || true
    print_success "تم إصلاح صلاحيات الملفات"
    
    print_step "إنشاء المجلدات المفقودة..."
    mkdir -p logs backups backend/instance
    print_success "تم إنشاء المجلدات المفقودة"
    
    print_step "إصلاح قاعدة البيانات..."
    cd backend
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
    python -c "
from src.database import create_app, db
try:
    app = create_app()
    with app.app_context():
        db.create_all()
    print('✅ قاعدة البيانات سليمة')
except Exception as e:
    print(f'❌ خطأ في قاعدة البيانات: {e}')
" 2>/dev/null || print_warning "تعذر فحص قاعدة البيانات"
    cd ..
}

# تقرير شامل
generate_report() {
    print_header "تقرير الصيانة الشامل"
    
    REPORT_FILE="maintenance_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "🔧 تقرير صيانة نظام إدارة المتجر"
        echo "تاريخ التقرير: $(date)"
        echo "=================================="
        echo ""
        
        echo "📊 معلومات النظام:"
        echo "- نظام التشغيل: $(uname -s)"
        echo "- إصدار Python: $(python3 --version 2>/dev/null || echo 'غير مثبت')"
        echo "- إصدار Node.js: $(node --version 2>/dev/null || echo 'غير مثبت')"
        echo ""
        
        echo "💾 استخدام المساحة:"
        du -sh . 2>/dev/null || echo "غير متاح"
        echo ""
        
        echo "🗄️ قاعدة البيانات:"
        if [ -f "backend/instance/store.db" ]; then
            echo "- الحجم: $(du -sh backend/instance/store.db | awk '{print $1}')"
            echo "- آخر تعديل: $(stat -c %y backend/instance/store.db 2>/dev/null || echo 'غير متاح')"
        else
            echo "- غير موجودة"
        fi
        echo ""
        
        echo "🔒 الأمان:"
        echo "- ملف .env: $([ -f backend/.env ] && echo 'موجود' || echo 'غير موجود')"
        echo "- صلاحيات .env: $([ -f backend/.env ] && stat -c %a backend/.env || echo 'غير متاح')"
        echo ""
        
        echo "📝 السجلات:"
        echo "- عدد ملفات السجل: $(find logs/ -name '*.log' 2>/dev/null | wc -l)"
        echo "- حجم السجلات: $(du -sh logs/ 2>/dev/null | awk '{print $1}' || echo '0')"
        echo ""
        
        echo "💿 النسخ الاحتياطية:"
        echo "- عدد النسخ: $(find backups/ -name '*.tar.gz' 2>/dev/null | wc -l)"
        echo "- حجم النسخ: $(du -sh backups/ 2>/dev/null | awk '{print $1}' || echo '0')"
        
    } > "$REPORT_FILE"
    
    print_success "تم إنشاء التقرير: $REPORT_FILE"
    cat "$REPORT_FILE"
}

# عرض المساعدة
show_help() {
    echo -e "${WHITE}🔧 سكريبت صيانة نظام إدارة المتجر${NC}"
    echo ""
    echo -e "${CYAN}الاستخدام:${NC}"
    echo "  $0 [الأمر]"
    echo ""
    echo -e "${CYAN}أوامر الصيانة:${NC}"
    echo -e "  ${GREEN}backup${NC}      - إنشاء نسخة احتياطية"
    echo -e "  ${GREEN}cleanup${NC}     - تنظيف الملفات المؤقتة"
    echo -e "  ${GREEN}update${NC}      - تحديث المتطلبات"
    echo -e "  ${GREEN}security${NC}    - فحص الأمان"
    echo -e "  ${GREEN}performance${NC} - فحص الأداء"
    echo -e "  ${GREEN}fix${NC}         - إصلاح المشاكل الشائعة"
    echo -e "  ${GREEN}report${NC}      - تقرير شامل"
    echo -e "  ${GREEN}all${NC}         - تشغيل جميع عمليات الصيانة"
    echo -e "  ${GREEN}help${NC}        - عرض هذه المساعدة"
}

# الدالة الرئيسية
main() {
    case "${1:-help}" in
        "backup")
            backup_system
            ;;
        "cleanup")
            cleanup_system
            ;;
        "update")
            update_system
            ;;
        "security")
            security_check
            ;;
        "performance")
            performance_check
            ;;
        "fix")
            fix_common_issues
            ;;
        "report")
            generate_report
            ;;
        "all")
            backup_system
            cleanup_system
            update_system
            security_check
            performance_check
            fix_common_issues
            generate_report
            print_success "🎉 تمت جميع عمليات الصيانة بنجاح!"
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
