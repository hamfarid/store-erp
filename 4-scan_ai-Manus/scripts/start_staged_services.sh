#!/bin/bash

# سكريبت تشغيل الخدمات بشكل مرحلي
# يقوم بتشغيل الحاويات على مراحل لتوفير استهلاك الشبكة وتحسين الكفاءة

# تعريف الألوان للإخراج
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دالة لطباعة رسائل النجاح
success() {
  echo -e "${GREEN}[نجاح]${NC} $1"
}

# دالة لطباعة رسائل الفشل
error() {
  echo -e "${RED}[خطأ]${NC} $1"
}

# دالة لطباعة رسائل التحذير
warning() {
  echo -e "${YELLOW}[تحذير]${NC} $1"
}

# دالة لطباعة رسائل المعلومات
info() {
  echo -e "${BLUE}[معلومات]${NC} $1"
}

# دالة للتحقق من حالة الخدمات
check_services_health() {
  local compose_file=$1
  local stage_name=$2
  
  info "التحقق من حالة خدمات $stage_name..."
  
  # انتظار حتى تصبح جميع الخدمات صحية
  local max_attempts=30
  local attempt=1
  
  while [ $attempt -le $max_attempts ]; do
    if docker-compose -f $compose_file ps | grep -q "unhealthy\|starting"; then
      info "انتظار تشغيل الخدمات... المحاولة $attempt من $max_attempts"
      sleep 10
      ((attempt++))
    else
      success "جميع خدمات $stage_name تعمل بشكل صحيح"
      return 0
    fi
  done
  
  error "فشل في تشغيل بعض خدمات $stage_name خلال الوقت المحدد"
  return 1
}

# دالة لتشغيل مرحلة معينة
start_stage() {
  local stage_number=$1
  local compose_file=$2
  local stage_name=$3
  
  info "بدء تشغيل المرحلة $stage_number: $stage_name"
  
  # إنشاء الشبكة إذا لم تكن موجودة
  if [ $stage_number -eq 1 ]; then
    docker network create agri_ai_network 2>/dev/null || true
  fi
  
  # تشغيل الخدمات
  if docker-compose -f $compose_file up -d; then
    success "تم تشغيل خدمات المرحلة $stage_number بنجاح"
    
    # التحقق من حالة الخدمات
    if check_services_health $compose_file "$stage_name"; then
      success "المرحلة $stage_number جاهزة للاستخدام"
      return 0
    else
      error "فشل في التحقق من حالة خدمات المرحلة $stage_number"
      return 1
    fi
  else
    error "فشل في تشغيل خدمات المرحلة $stage_number"
    return 1
  fi
}

# دالة لإيقاف جميع المراحل
stop_all_stages() {
  info "إيقاف جميع المراحل..."
  
  docker-compose -f docker-compose.stage4-monitoring.yml down 2>/dev/null || true
  docker-compose -f docker-compose.stage3-ai-services.yml down 2>/dev/null || true
  docker-compose -f docker-compose.stage2-core-app.yml down 2>/dev/null || true
  docker-compose -f docker-compose.stage1-databases.yml down 2>/dev/null || true
  
  success "تم إيقاف جميع المراحل"
}

# دالة لعرض حالة جميع المراحل
show_status() {
  info "حالة جميع المراحل:"
  
  echo "المرحلة 1 - قواعد البيانات:"
  docker-compose -f docker-compose.stage1-databases.yml ps
  
  echo "المرحلة 2 - التطبيق الأساسي:"
  docker-compose -f docker-compose.stage2-core-app.yml ps
  
  echo "المرحلة 3 - خدمات الذكاء الاصطناعي:"
  docker-compose -f docker-compose.stage3-ai-services.yml ps
  
  echo "المرحلة 4 - المراقبة:"
  docker-compose -f docker-compose.stage4-monitoring.yml ps
}

# دالة لتشغيل مرحلة واحدة فقط
start_single_stage() {
  local stage=$1
  
  case $stage in
    1)
      start_stage 1 "docker-compose.stage1-databases.yml" "قواعد البيانات والخدمات الأساسية"
      ;;
    2)
      start_stage 2 "docker-compose.stage2-core-app.yml" "التطبيق الأساسي"
      ;;
    3)
      start_stage 3 "docker-compose.stage3-ai-services.yml" "خدمات الذكاء الاصطناعي"
      ;;
    4)
      start_stage 4 "docker-compose.stage4-monitoring.yml" "خدمات المراقبة"
      ;;
    *)
      error "رقم المرحلة غير صحيح. استخدم 1-4"
      exit 1
      ;;
  esac
}

# دالة لتشغيل جميع المراحل
start_all_stages() {
  info "بدء تشغيل جميع المراحل بالتسلسل..."
  
  # المرحلة 1: قواعد البيانات
  if start_stage 1 "docker-compose.stage1-databases.yml" "قواعد البيانات والخدمات الأساسية"; then
    
    # المرحلة 2: التطبيق الأساسي
    if start_stage 2 "docker-compose.stage2-core-app.yml" "التطبيق الأساسي"; then
      
      # المرحلة 3: خدمات الذكاء الاصطناعي
      if start_stage 3 "docker-compose.stage3-ai-services.yml" "خدمات الذكاء الاصطناعي"; then
        
        # المرحلة 4: خدمات المراقبة
        if start_stage 4 "docker-compose.stage4-monitoring.yml" "خدمات المراقبة"; then
          success "تم تشغيل جميع المراحل بنجاح!"
          info "يمكنك الوصول إلى التطبيق على: http://localhost:8031"
          info "يمكنك الوصول إلى Grafana على: http://localhost:3000"
          info "يمكنك الوصول إلى RabbitMQ Management على: http://localhost:15672"
        else
          warning "فشل في تشغيل المرحلة 4، لكن التطبيق الأساسي يعمل"
        fi
      else
        warning "فشل في تشغيل المرحلة 3، لكن التطبيق الأساسي يعمل"
      fi
    else
      error "فشل في تشغيل المرحلة 2"
      exit 1
    fi
  else
    error "فشل في تشغيل المرحلة 1"
    exit 1
  fi
}

# عرض المساعدة
show_help() {
  echo "استخدام: $0 [الخيار]"
  echo ""
  echo "الخيارات:"
  echo "  start [1-4]    تشغيل مرحلة محددة (اختياري: رقم المرحلة)"
  echo "  stop           إيقاف جميع المراحل"
  echo "  restart        إعادة تشغيل جميع المراحل"
  echo "  status         عرض حالة جميع المراحل"
  echo "  help           عرض هذه المساعدة"
  echo ""
  echo "المراحل:"
  echo "  1 - قواعد البيانات والخدمات الأساسية"
  echo "  2 - التطبيق الأساسي"
  echo "  3 - خدمات الذكاء الاصطناعي"
  echo "  4 - خدمات المراقبة"
}

# المعالج الرئيسي
case "${1:-start}" in
  start)
    if [ -n "$2" ]; then
      start_single_stage $2
    else
      start_all_stages
    fi
    ;;
  stop)
    stop_all_stages
    ;;
  restart)
    stop_all_stages
    sleep 5
    start_all_stages
    ;;
  status)
    show_status
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    error "خيار غير معروف: $1"
    show_help
    exit 1
    ;;
esac
