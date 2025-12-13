#!/usr/bin/env bash
# FILE: bootstrap_linux.sh | PURPOSE: تنزيل وإعداد مستودع global بالكامل على Linux | OWNER: DevOps | LAST-AUDITED: 2025-10-21
set -euo pipefail

# ========================================
# المتغيرات الأساسية
# ========================================
REPO_OWNER="hamfarid"
REPO_NAME="global"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}.git"
REF="${1:-main}"
DEST="${2:-./${REPO_NAME}}"
TOKEN="${GITHUB_TOKEN:-}"

# ========================================
# الألوان للطباعة
# ========================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# الدوال المساعدة
# ========================================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

usage() {
    cat <<EOF
الاستخدام: $0 [branch] [destination]

الوصف:
  تنزيل وإعداد مستودع global من GitHub بالكامل

المعاملات:
  branch       : الفرع أو Tag (افتراضي: main)
  destination  : مجلد الوجهة (افتراضي: ./global)

المتغيرات البيئية:
  GITHUB_TOKEN : رمز GitHub للمستودعات الخاصة (اختياري)

أمثلة:
  $0
  $0 main ./my-global
  GITHUB_TOKEN=ghp_xxx $0 main ./my-global

EOF
    exit 1
}

# ========================================
# معالجة المعاملات
# ========================================
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
fi

# ========================================
# البداية
# ========================================
echo ""
log_info "=========================================="
log_info "تنزيل وإعداد مستودع Global"
log_info "=========================================="
echo ""
log_info "المستودع: ${REPO_OWNER}/${REPO_NAME}"
log_info "الفرع   : ${REF}"
log_info "الوجهة  : ${DEST}"
echo ""

# ========================================
# إنشاء مجلد الوجهة
# ========================================
mkdir -p "$DEST"
DEST="$(cd "$DEST" && pwd)"

# ========================================
# التحقق من وجود git
# ========================================
if command -v git >/dev/null 2>&1; then
    log_success "تم العثور على git"
    USE_GIT=true
else
    log_warning "لم يتم العثور على git - سيتم استخدام التنزيل المباشر"
    USE_GIT=false
fi

# ========================================
# التنزيل
# ========================================
tmpdir="$(mktemp -d)"
cleanup() {
    rm -rf "$tmpdir"
}
trap cleanup EXIT

log_info "جاري التنزيل..."

if [ "$USE_GIT" = true ]; then
    # استخدام git clone
    if [ -n "$TOKEN" ]; then
        CLONE_URL="https://${TOKEN}@github.com/${REPO_OWNER}/${REPO_NAME}.git"
    else
        CLONE_URL="$REPO_URL"
    fi
    
    if git clone --depth 1 --branch "$REF" "$CLONE_URL" "$DEST" 2>/dev/null; then
        log_success "تم التنزيل باستخدام git"
    else
        log_warning "فشل git clone - محاولة التنزيل المباشر..."
        USE_GIT=false
    fi
fi

if [ "$USE_GIT" = false ]; then
    # التنزيل المباشر باستخدام curl
    ZIP_URL="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/zipball/${REF}"
    
    if [ -n "$TOKEN" ]; then
        curl -sSL -H "Authorization: token ${TOKEN}" "$ZIP_URL" -o "$tmpdir/repo.zip"
    else
        curl -sSL "$ZIP_URL" -o "$tmpdir/repo.zip"
    fi
    
    if [ $? -eq 0 ]; then
        log_success "تم التنزيل"
        log_info "جاري فك الضغط..."
        unzip -q "$tmpdir/repo.zip" -d "$tmpdir"
        
        # نقل الملفات
        extracted_dir=$(find "$tmpdir" -mindepth 1 -maxdepth 1 -type d | head -n 1)
        if [ -n "$extracted_dir" ]; then
            cp -r "$extracted_dir"/* "$DEST/" 2>/dev/null || true
            cp -r "$extracted_dir"/.[!.]* "$DEST/" 2>/dev/null || true
            log_success "تم فك الضغط والنقل"
        fi
    else
        log_error "فشل التنزيل"
        exit 1
    fi
fi

# ========================================
# إنشاء المجلدات الأساسية
# ========================================
log_info "إنشاء المجلدات الأساسية..."

mkdir -p "$DEST/.github/workflows"
mkdir -p "$DEST/scripts"
mkdir -p "$DEST/templates"
mkdir -p "$DEST/docs"
mkdir -p "$DEST/contracts"
mkdir -p "$DEST/packages/shared-types"
mkdir -p "$DEST/examples"

log_success "تم إنشاء المجلدات"

# ========================================
# جعل السكريبتات قابلة للتنفيذ
# ========================================
log_info "تعيين الأذونات..."

if [ -f "$DEST/setup_project_structure.sh" ]; then
    chmod +x "$DEST/setup_project_structure.sh"
    log_success "setup_project_structure.sh قابل للتنفيذ"
fi

if [ -f "$DEST/download_and_setup.sh" ]; then
    chmod +x "$DEST/download_and_setup.sh"
    log_success "download_and_setup.sh قابل للتنفيذ"
fi

if [ -f "$DEST/validate_project.sh" ]; then
    chmod +x "$DEST/validate_project.sh"
    log_success "validate_project.sh قابل للتنفيذ"
fi

if [ -f "$DEST/scripts/backup.sh" ]; then
    chmod +x "$DEST/scripts/backup.sh"
    log_success "backup.sh قابل للتنفيذ"
fi

# ========================================
# عرض الملفات
# ========================================
log_info "الملفات المتوفرة:"
echo ""

if [ -f "$DEST/README.md" ]; then
    log_success "README.md"
fi

if [ -f "$DEST/GLOBAL_GUIDELINES.txt" ]; then
    log_success "GLOBAL_GUIDELINES.txt (v1.8)"
fi

if [ -f "$DEST/GLOBAL_GUIDELINES_v2.1.txt" ]; then
    log_success "GLOBAL_GUIDELINES_v2.1.txt (v2.1)"
fi

if [ -f "$DEST/GLOBAL_GUIDELINES_v2.2.txt" ]; then
    log_success "GLOBAL_GUIDELINES_v2.2.txt (v2.2)"
fi

if [ -f "$DEST/setup_project_structure.sh" ]; then
    log_success "setup_project_structure.sh"
fi

if [ -f "$DEST/validate_project.sh" ]; then
    log_success "validate_project.sh"
fi

if [ -f "$DEST/scripts/backup.sh" ]; then
    log_success "scripts/backup.sh"
fi

# ========================================
# الخلاصة
# ========================================
echo ""
log_info "=========================================="
log_success "اكتمل التنزيل والإعداد بنجاح!"
log_info "=========================================="
echo ""
log_info "المسار: $DEST"
echo ""
log_info "الخطوات التالية:"
echo "  1. cd $DEST"
echo "  2. اقرأ README.md للتعليمات"
echo "  3. استخدم ./setup_project_structure.sh لإنشاء مشروع جديد"
echo ""
log_info "أمثلة الاستخدام:"
echo "  # إنشاء مشروع جديد"
echo "  ./setup_project_structure.sh my_project /path/to/project"
echo ""
echo "  # التحقق من مشروع"
echo "  ./validate_project.sh /path/to/project"
echo ""
echo "  # نسخ احتياطي"
echo "  ./scripts/backup.sh /path/to/project /path/to/backups"
echo ""

