#!/bin/bash
# سكريبت النشر الشامل
# Complete Deployment Script

set -e  # إيقاف عند أول خطأ

echo "🚀 بدء عملية النشر..."
echo "=========================="

# الألوان للرسائل
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# دالة طباعة الرسائل
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# فحص المتطلبات
check_requirements() {
    print_status "فحص المتطلبات..."
    
    # فحص Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js غير مثبت"
        exit 1
    fi
    
    # فحص Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 غير مثبت"
        exit 1
    fi
    
    # فحص npm
    if ! command -v npm &> /dev/null; then
        print_error "npm غير مثبت"
        exit 1
    fi
    
    print_status "جميع المتطلبات متوفرة"
}

# تثبيت التبعيات
install_dependencies() {
    print_status "تثبيت تبعيات الواجهة الخلفية..."
    cd backend
    pip3 install -r requirements.txt
    cd ..
    
    print_status "تثبيت تبعيات الواجهة الأمامية..."
    cd frontend
    npm install
    cd ..
}

# بناء الواجهة الأمامية
build_frontend() {
    print_status "بناء الواجهة الأمامية..."
    cd frontend
    npm run build
    
    if [ $? -eq 0 ]; then
        print_status "تم بناء الواجهة الأمامية بنجاح"
    else
        print_error "فشل في بناء الواجهة الأمامية"
        exit 1
    fi
    cd ..
}

# اختبار النظام
test_system() {
    print_status "اختبار النظام..."
    cd backend
    
    # تشغيل الاختبارات إذا كانت متوفرة
    if [ -f "tests/test_main.py" ]; then
        python3 tests/test_main.py
        if [ $? -eq 0 ]; then
            print_status "نجحت جميع الاختبارات"
        else
            print_warning "بعض الاختبارات فشلت، لكن النشر سيستمر"
        fi
    else
        print_warning "لا توجد اختبارات للتشغيل"
    fi
    cd ..
}

# إنشاء نسخة احتياطية
create_backup() {
    print_status "إنشاء نسخة احتياطية..."
    
    BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    tar --exclude='node_modules' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env*' \
        --exclude='dist' \
        --exclude='build' \
        --exclude='*.log' \
        --exclude='.cache' \
        --exclude='.git' \
        -czf "$BACKUP_NAME" .
    
    print_status "تم إنشاء النسخة الاحتياطية: $BACKUP_NAME"
}

# تحسين النظام
optimize_system() {
    print_status "تحسين النظام..."
    
    # تحسين قاعدة البيانات
    cd backend
    python3 -c "
try:
    from src.services.db_optimizer import DatabaseOptimizer
    optimizer = DatabaseOptimizer()
    results = optimizer.optimize_database()
    print('تم تحسين قاعدة البيانات:', results)
except Exception as e:
    print('تحذير: فشل في تحسين قاعدة البيانات:', e)
" 2>/dev/null || print_warning "فشل في تحسين قاعدة البيانات"
    cd ..
}

# بدء الخوادم
start_servers() {
    print_status "بدء الخوادم..."
    
    # بدء الخادم الخلفي
    cd backend
    nohup python3 app.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    cd ..
    
    # انتظار بدء الخادم
    sleep 5
    
    # فحص حالة الخادم
    if curl -s http://localhost:5001/api/health > /dev/null; then
        print_status "الخادم الخلفي يعمل (PID: $BACKEND_PID)"
    else
        print_error "فشل في بدء الخادم الخلفي"
        exit 1
    fi
    
    print_status "النشر مكتمل بنجاح! 🎉"
    echo "الخادم الخلفي: http://localhost:5001"
    echo "الواجهة الأمامية: frontend/dist/"
}

# إنشاء مجلد السجلات
mkdir -p logs

# تشغيل خطوات النشر
check_requirements
install_dependencies
build_frontend
test_system
create_backup
optimize_system
start_servers

echo "=========================="
echo "🎉 تم النشر بنجاح!"
echo "📊 لمراقبة السجلات: tail -f logs/backend.log"
echo "🛑 لإيقاف الخادم: kill \$(cat logs/backend.pid)"
