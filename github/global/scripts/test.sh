#!/bin/bash

# 🏪 نظام إدارة المخزون الكامل - سكريبت الاختبار الشامل
# Complete Inventory Management System - Comprehensive Test Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    print_status "اختبار: $test_name"
    print_status "Testing: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        print_success "✓ نجح الاختبار: $test_name"
        print_success "✓ Test passed: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        print_error "✗ فشل الاختبار: $test_name"
        print_error "✗ Test failed: $test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Function to test file existence
test_file_exists() {
    local file_path="$1"
    local description="$2"
    
    run_test "$description" "[ -f '$file_path' ]"
}

# Function to test directory existence
test_dir_exists() {
    local dir_path="$1"
    local description="$2"
    
    run_test "$description" "[ -d '$dir_path' ]"
}

# Function to test script execution
test_script_executable() {
    local script_path="$1"
    local description="$2"
    
    run_test "$description" "[ -x '$script_path' ]"
}

# Function to test Python syntax
test_python_syntax() {
    local file_path="$1"
    local description="$2"
    
    run_test "$description" "python3 -m py_compile '$file_path'"
}

# Function to test JavaScript syntax
test_js_syntax() {
    local file_path="$1"
    local description="$2"
    
    run_test "$description" "node -c '$file_path'"
}

# Main test function
main() {
    print_status "🧪 بدء الاختبار الشامل لنظام إدارة المخزون..."
    print_status "🧪 Starting comprehensive test for inventory management system..."
    
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "يرجى تشغيل هذا السكريبت من المجلد الجذر للمشروع"
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    echo ""
    print_status "=== اختبار هيكل المشروع ==="
    print_status "=== Testing Project Structure ==="
    
    # Test main directories
    test_dir_exists "backend" "مجلد الخادم الخلفي"
    test_dir_exists "frontend" "مجلد الواجهة الأمامية"
    test_dir_exists "scripts" "مجلد السكريبتات"
    test_dir_exists "docs" "مجلد الوثائق"
    
    # Test main files
    test_file_exists "README.md" "ملف README الرئيسي"
    test_file_exists "backend/requirements.txt" "ملف متطلبات Python"
    test_file_exists "frontend/package.json" "ملف متطلبات Node.js"
    
    echo ""
    print_status "=== اختبار السكريبتات ==="
    print_status "=== Testing Scripts ==="
    
    # Test script files
    test_file_exists "scripts/install.sh" "سكريبت التثبيت"
    test_file_exists "scripts/start.sh" "سكريبت التشغيل"
    test_file_exists "scripts/cleanup.sh" "سكريبت التنظيف"
    test_file_exists "scripts/deploy.sh" "سكريبت النشر"
    test_file_exists "scripts/nginx.conf" "إعدادات Nginx"
    test_file_exists "scripts/ecosystem.config.js" "إعدادات PM2"
    
    # Test script permissions
    test_script_executable "scripts/install.sh" "صلاحيات سكريبت التثبيت"
    test_script_executable "scripts/start.sh" "صلاحيات سكريبت التشغيل"
    test_script_executable "scripts/cleanup.sh" "صلاحيات سكريبت التنظيف"
    test_script_executable "scripts/deploy.sh" "صلاحيات سكريبت النشر"
    
    echo ""
    print_status "=== اختبار الخادم الخلفي ==="
    print_status "=== Testing Backend ==="
    
    # Test backend structure
    test_dir_exists "backend/src" "مجلد الكود المصدري للخادم الخلفي"
    test_dir_exists "backend/src/models" "مجلد النماذج"
    test_dir_exists "backend/src/routes" "مجلد المسارات"
    test_dir_exists "backend/src/services" "مجلد الخدمات"
    
    # Test main backend files
    test_file_exists "backend/src/main.py" "ملف التشغيل الرئيسي"
    test_file_exists "backend/src/database.py" "ملف قاعدة البيانات"
    
    # Test Python syntax for main files
    if [ -f "backend/src/main.py" ]; then
        test_python_syntax "backend/src/main.py" "بناء جملة main.py"
    fi
    
    if [ -f "backend/src/database.py" ]; then
        test_python_syntax "backend/src/database.py" "بناء جملة database.py"
    fi
    
    echo ""
    print_status "=== اختبار الواجهة الأمامية ==="
    print_status "=== Testing Frontend ==="
    
    # Test frontend structure
    test_dir_exists "frontend/src" "مجلد الكود المصدري للواجهة الأمامية"
    test_dir_exists "frontend/src/components" "مجلد المكونات"
    test_dir_exists "frontend/src/pages" "مجلد الصفحات"
    test_dir_exists "frontend/src/services" "مجلد خدمات API"
    
    # Test main frontend files
    test_file_exists "frontend/src/App.jsx" "ملف التطبيق الرئيسي"
    test_file_exists "frontend/src/main.jsx" "ملف التشغيل الرئيسي"
    test_file_exists "frontend/vite.config.js" "إعدادات Vite"
    
    # Test package.json structure
    if [ -f "frontend/package.json" ]; then
        run_test "صحة ملف package.json" "node -e 'JSON.parse(require(\"fs\").readFileSync(\"frontend/package.json\"))'"
    fi
    
    echo ""
    print_status "=== اختبار الوثائق ==="
    print_status "=== Testing Documentation ==="
    
    # Test documentation files
    test_file_exists "docs/api-documentation.md" "وثائق API"
    test_file_exists "docs/frontend-components.md" "وثائق مكونات الواجهة الأمامية"
    
    echo ""
    print_status "=== اختبار التبعيات ==="
    print_status "=== Testing Dependencies ==="
    
    # Test Python availability
    run_test "توفر Python 3" "command -v python3"
    
    # Test Node.js availability
    run_test "توفر Node.js" "command -v node"
    
    # Test npm availability
    run_test "توفر npm" "command -v npm"
    
    # Test pip availability
    run_test "توفر pip" "command -v pip3 || command -v pip"
    
    echo ""
    print_status "=== اختبار إعدادات الإنتاج ==="
    print_status "=== Testing Production Settings ==="
    
    # Test Nginx configuration syntax
    if command -v nginx >/dev/null 2>&1; then
        run_test "صحة إعدادات Nginx" "nginx -t -c scripts/nginx.conf"
    else
        print_warning "Nginx غير مثبت - تم تخطي اختبار الإعدادات"
        print_warning "Nginx not installed - skipping configuration test"
    fi
    
    # Test PM2 configuration syntax
    if command -v node >/dev/null 2>&1; then
        test_js_syntax "scripts/ecosystem.config.js" "صحة إعدادات PM2"
    fi
    
    echo ""
    print_status "=== اختبار الأمان ==="
    print_status "=== Testing Security ==="
    
    # Check for sensitive files
    run_test "عدم وجود ملفات حساسة في Git" "! find . -name '*.env' -o -name '*.key' -o -name '*.pem' | grep -v node_modules | grep -q ."
    
    # Check for proper .gitignore
    test_file_exists ".gitignore" "وجود ملف .gitignore"
    
    echo ""
    print_status "=== ملخص النتائج ==="
    print_status "=== Test Summary ==="
    
    echo ""
    print_status "إجمالي الاختبارات: $TESTS_TOTAL"
    print_status "Total tests: $TESTS_TOTAL"
    print_success "الاختبارات الناجحة: $TESTS_PASSED"
    print_success "Passed tests: $TESTS_PASSED"
    
    if [ $TESTS_FAILED -gt 0 ]; then
        print_error "الاختبارات الفاشلة: $TESTS_FAILED"
        print_error "Failed tests: $TESTS_FAILED"
    fi
    
    echo ""
    
    # Calculate success rate
    if [ $TESTS_TOTAL -gt 0 ]; then
        SUCCESS_RATE=$((TESTS_PASSED * 100 / TESTS_TOTAL))
        
        if [ $SUCCESS_RATE -eq 100 ]; then
            print_success "🎉 جميع الاختبارات نجحت! معدل النجاح: 100%"
            print_success "🎉 All tests passed! Success rate: 100%"
        elif [ $SUCCESS_RATE -ge 80 ]; then
            print_warning "⚠️ معظم الاختبارات نجحت. معدل النجاح: $SUCCESS_RATE%"
            print_warning "⚠️ Most tests passed. Success rate: $SUCCESS_RATE%"
        else
            print_error "❌ العديد من الاختبارات فشلت. معدل النجاح: $SUCCESS_RATE%"
            print_error "❌ Many tests failed. Success rate: $SUCCESS_RATE%"
        fi
    fi
    
    echo ""
    print_status "التوصيات:"
    print_status "Recommendations:"
    
    if [ $TESTS_FAILED -gt 0 ]; then
        print_status "- راجع الاختبارات الفاشلة وأصلح المشاكل"
        print_status "- Review failed tests and fix issues"
        print_status "- تأكد من تثبيت جميع التبعيات"
        print_status "- Ensure all dependencies are installed"
        print_status "- تحقق من صلاحيات الملفات"
        print_status "- Check file permissions"
    else
        print_status "- النظام جاهز للنشر!"
        print_status "- System is ready for deployment!"
        print_status "- يمكنك تشغيل ./scripts/install.sh لتثبيت التبعيات"
        print_status "- You can run ./scripts/install.sh to install dependencies"
        print_status "- ثم ./scripts/start.sh لتشغيل النظام"
        print_status "- Then ./scripts/start.sh to start the system"
    fi
    
    # Exit with appropriate code
    if [ $TESTS_FAILED -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

# Handle command line arguments
case "${1:-test}" in
    "test")
        main
        ;;
    "quick")
        print_status "اختبار سريع..."
        print_status "Quick test..."
        
        # Only test essential files
        test_file_exists "README.md" "ملف README"
        test_dir_exists "backend" "مجلد الخادم الخلفي"
        test_dir_exists "frontend" "مجلد الواجهة الأمامية"
        test_file_exists "scripts/install.sh" "سكريبت التثبيت"
        test_file_exists "scripts/start.sh" "سكريبت التشغيل"
        
        print_success "الاختبار السريع مكتمل"
        print_success "Quick test completed"
        ;;
    "syntax")
        print_status "اختبار بناء الجملة..."
        print_status "Syntax test..."
        
        # Test Python files
        find backend -name "*.py" -exec python3 -m py_compile {} \; 2>/dev/null && \
            print_success "جميع ملفات Python صحيحة" || \
            print_error "بعض ملفات Python بها أخطاء"
        
        # Test JavaScript files
        if command -v node >/dev/null 2>&1; then
            find frontend -name "*.js" -o -name "*.jsx" | while read file; do
                if node -c "$file" 2>/dev/null; then
                    echo "✓ $file"
                else
                    echo "✗ $file"
                fi
            done
        fi
        ;;
    *)
        echo "Usage: $0 {test|quick|syntax}"
        echo "الاستخدام: $0 {test|quick|syntax}"
        echo ""
        echo "  test   - اختبار شامل (افتراضي)"
        echo "  quick  - اختبار سريع للملفات الأساسية"
        echo "  syntax - اختبار بناء الجملة فقط"
        exit 1
        ;;
esac
