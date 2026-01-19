#!/bin/bash
# ملف: /home/ubuntu/gaara_development/scripts/test.sh
# سكريبت اختبار شامل لنظام Gaara AI
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

# متغيرات الاختبار
BACKEND_URL="http://localhost:5000"
FRONTEND_URL="http://localhost:3000"
TEST_RESULTS=()
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# دوال مساعدة
print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}🧪 اختبار نظام Gaara AI${NC}"
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

# دالة تسجيل نتائج الاختبار
log_test_result() {
    local test_name="$1"
    local result="$2"
    local message="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$result" = "PASS" ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        print_success "اختبار $test_name: نجح - $message"
        TEST_RESULTS+=("✅ $test_name: نجح")
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        print_error "اختبار $test_name: فشل - $message"
        TEST_RESULTS+=("❌ $test_name: فشل")
    fi
}

# اختبار الاتصال بالخدمات
test_service_connectivity() {
    print_step "اختبار الاتصال بالخدمات..."
    
    # اختبار الواجهة الخلفية
    if curl -s -f "$BACKEND_URL/api/health" > /dev/null; then
        log_test_result "الواجهة الخلفية" "PASS" "الخدمة متاحة"
    else
        log_test_result "الواجهة الخلفية" "FAIL" "الخدمة غير متاحة"
    fi
    
    # اختبار الواجهة الأمامية
    if curl -s -f "$FRONTEND_URL" > /dev/null; then
        log_test_result "الواجهة الأمامية" "PASS" "الخدمة متاحة"
    else
        log_test_result "الواجهة الأمامية" "FAIL" "الخدمة غير متاحة"
    fi
}

# اختبار APIs الأساسية
test_basic_apis() {
    print_step "اختبار APIs الأساسية..."
    
    # اختبار API الصحة
    response=$(curl -s -w "%{http_code}" "$BACKEND_URL/api/health")
    http_code="${response: -3}"
    if [ "$http_code" = "200" ]; then
        log_test_result "API الصحة" "PASS" "HTTP 200"
    else
        log_test_result "API الصحة" "FAIL" "HTTP $http_code"
    fi
    
    # اختبار API المعلومات
    response=$(curl -s -w "%{http_code}" "$BACKEND_URL/api/info")
    http_code="${response: -3}"
    if [ "$http_code" = "200" ]; then
        log_test_result "API المعلومات" "PASS" "HTTP 200"
    else
        log_test_result "API المعلومات" "FAIL" "HTTP $http_code"
    fi
    
    # اختبار API النباتات
    response=$(curl -s -w "%{http_code}" "$BACKEND_URL/api/plants")
    http_code="${response: -3}"
    if [ "$http_code" = "200" ] || [ "$http_code" = "401" ]; then
        log_test_result "API النباتات" "PASS" "HTTP $http_code"
    else
        log_test_result "API النباتات" "FAIL" "HTTP $http_code"
    fi
    
    # اختبار API الأمراض
    response=$(curl -s -w "%{http_code}" "$BACKEND_URL/api/diseases")
    http_code="${response: -3}"
    if [ "$http_code" = "200" ] || [ "$http_code" = "401" ]; then
        log_test_result "API الأمراض" "PASS" "HTTP $http_code"
    else
        log_test_result "API الأمراض" "FAIL" "HTTP $http_code"
    fi
}

# اختبار قاعدة البيانات
test_database() {
    print_step "اختبار قاعدة البيانات..."
    
    cd gaara_ai_integrated/backend
    source venv/bin/activate
    
    # اختبار الاتصال بقاعدة البيانات
    python3 -c "
import sys
sys.path.append('.')
try:
    from main_api import app, db
    with app.app_context():
        # اختبار الاتصال
        db.engine.execute('SELECT 1')
        print('PASS: الاتصال بقاعدة البيانات')
        
        # اختبار الجداول
        tables = db.engine.table_names()
        if len(tables) > 0:
            print('PASS: الجداول موجودة')
        else:
            print('FAIL: لا توجد جداول')
            
except Exception as e:
    print(f'FAIL: خطأ في قاعدة البيانات - {str(e)}')
" 2>/dev/null | while read line; do
        if [[ $line == PASS:* ]]; then
            message=${line#PASS: }
            log_test_result "قاعدة البيانات" "PASS" "$message"
        elif [[ $line == FAIL:* ]]; then
            message=${line#FAIL: }
            log_test_result "قاعدة البيانات" "FAIL" "$message"
        fi
    done
    
    cd ../..
}

# اختبار الواجهة الأمامية
test_frontend() {
    print_step "اختبار الواجهة الأمامية..."
    
    cd gaara_ai_integrated/frontend
    
    # اختبار بناء المشروع
    if npm run build > /dev/null 2>&1; then
        log_test_result "بناء الواجهة الأمامية" "PASS" "البناء نجح"
    else
        log_test_result "بناء الواجهة الأمامية" "FAIL" "البناء فشل"
    fi
    
    # اختبار الملفات الأساسية
    if [ -f "src/App.jsx" ]; then
        log_test_result "ملف App.jsx" "PASS" "الملف موجود"
    else
        log_test_result "ملف App.jsx" "FAIL" "الملف مفقود"
    fi
    
    if [ -f "package.json" ]; then
        log_test_result "ملف package.json" "PASS" "الملف موجود"
    else
        log_test_result "ملف package.json" "FAIL" "الملف مفقود"
    fi
    
    cd ../..
}

# اختبار Docker
test_docker() {
    print_step "اختبار Docker..."
    
    if command -v docker &> /dev/null; then
        log_test_result "Docker" "PASS" "Docker متوفر"
        
        # اختبار docker-compose.yml
        if [ -f "docker-compose.yml" ]; then
            log_test_result "docker-compose.yml" "PASS" "الملف موجود"
            
            # اختبار صحة التكوين
            if docker-compose config > /dev/null 2>&1; then
                log_test_result "تكوين Docker Compose" "PASS" "التكوين صحيح"
            else
                log_test_result "تكوين Docker Compose" "FAIL" "التكوين خاطئ"
            fi
        else
            log_test_result "docker-compose.yml" "FAIL" "الملف مفقود"
        fi
    else
        log_test_result "Docker" "FAIL" "Docker غير متوفر"
    fi
}

# اختبار الملفات الأساسية
test_essential_files() {
    print_step "اختبار الملفات الأساسية..."
    
    # ملفات الواجهة الخلفية
    if [ -f "gaara_ai_integrated/backend/main_api.py" ]; then
        log_test_result "main_api.py" "PASS" "الملف موجود"
    else
        log_test_result "main_api.py" "FAIL" "الملف مفقود"
    fi
    
    if [ -f "gaara_ai_integrated/backend/requirements.txt" ]; then
        log_test_result "requirements.txt" "PASS" "الملف موجود"
    else
        log_test_result "requirements.txt" "FAIL" "الملف مفقود"
    fi
    
    # ملفات الواجهة الأمامية
    if [ -f "gaara_ai_integrated/frontend/src/App.jsx" ]; then
        log_test_result "App.jsx" "PASS" "الملف موجود"
    else
        log_test_result "App.jsx" "FAIL" "الملف مفقود"
    fi
    
    if [ -f "gaara_ai_integrated/frontend/package.json" ]; then
        log_test_result "package.json" "PASS" "الملف موجود"
    else
        log_test_result "package.json" "FAIL" "الملف مفقود"
    fi
    
    # ملفات Docker
    if [ -f "gaara_ai_integrated/backend/Dockerfile" ]; then
        log_test_result "Backend Dockerfile" "PASS" "الملف موجود"
    else
        log_test_result "Backend Dockerfile" "FAIL" "الملف مفقود"
    fi
    
    if [ -f "gaara_ai_integrated/frontend/Dockerfile" ]; then
        log_test_result "Frontend Dockerfile" "PASS" "الملف موجود"
    else
        log_test_result "Frontend Dockerfile" "FAIL" "الملف مفقود"
    fi
}

# اختبار الأمان
test_security() {
    print_step "اختبار الأمان..."
    
    # التحقق من ملف .env
    if [ -f ".env" ]; then
        log_test_result "ملف .env" "PASS" "الملف موجود"
        
        # التحقق من المتغيرات الأساسية
        if grep -q "SECRET_KEY" .env; then
            log_test_result "SECRET_KEY" "PASS" "المتغير موجود"
        else
            log_test_result "SECRET_KEY" "FAIL" "المتغير مفقود"
        fi
    else
        log_test_result "ملف .env" "FAIL" "الملف مفقود"
    fi
    
    # التحقق من عدم وجود كلمات مرور في الكود
    if grep -r "password.*=" gaara_ai_integrated/ --include="*.py" --include="*.js" --include="*.jsx" | grep -v "password_hash" | grep -v "set_password" > /dev/null; then
        log_test_result "كلمات المرور المكشوفة" "FAIL" "توجد كلمات مرور في الكود"
    else
        log_test_result "كلمات المرور المكشوفة" "PASS" "لا توجد كلمات مرور مكشوفة"
    fi
}

# عرض تقرير النتائج
show_results() {
    echo ""
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}📊 تقرير نتائج الاختبار${NC}"
    echo -e "${PURPLE}================================${NC}"
    
    echo -e "${CYAN}إجمالي الاختبارات: ${NC}$TOTAL_TESTS"
    echo -e "${GREEN}الاختبارات الناجحة: ${NC}$PASSED_TESTS"
    echo -e "${RED}الاختبارات الفاشلة: ${NC}$FAILED_TESTS"
    
    if [ $TOTAL_TESTS -gt 0 ]; then
        success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
        echo -e "${CYAN}معدل النجاح: ${NC}${success_rate}%"
    fi
    
    echo ""
    echo -e "${BLUE}تفاصيل النتائج:${NC}"
    for result in "${TEST_RESULTS[@]}"; do
        echo "  $result"
    done
    
    echo ""
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام.${NC}"
    else
        echo -e "${YELLOW}⚠️  بعض الاختبارات فشلت. يرجى مراجعة المشاكل وإصلاحها.${NC}"
    fi
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
    
    # تنفيذ الاختبارات
    test_essential_files
    test_service_connectivity
    test_basic_apis
    test_database
    test_frontend
    test_docker
    test_security
    
    # عرض النتائج
    show_results
    
    # إرجاع كود الخروج المناسب
    if [ $FAILED_TESTS -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# تشغيل الدالة الرئيسية
main "$@"

