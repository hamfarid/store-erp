#!/bin/bash
# FILE: scripts/backup.sh
# PURPOSE: إنشاء نسخة احتياطية كاملة من المشروع
# OWNER: Global Team
# LAST-AUDITED: 2025-10-21

set -e

PROJECT_PATH="${1:-.}"
BACKUP_DIR="${2:-./backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PROJECT_NAME=$(basename "$(cd "$PROJECT_PATH" && pwd)")
BACKUP_NAME="${PROJECT_NAME}_backup_${TIMESTAMP}"

echo "=========================================="
echo "📦 إنشاء نسخة احتياطية"
echo "=========================================="
echo "المشروع: $PROJECT_NAME"
echo "المسار: $PROJECT_PATH"
echo "النسخة الاحتياطية: $BACKUP_NAME"
echo ""

# إنشاء مجلد النسخ الاحتياطية
mkdir -p "$BACKUP_DIR"

# الملفات والمجلدات المستبعدة
EXCLUDE_PATTERNS=(
    ".env"
    ".venv"
    "venv"
    "env"
    "node_modules"
    "__pycache__"
    "*.pyc"
    ".pytest_cache"
    ".mypy_cache"
    "build"
    "dist"
    "*.egg-info"
    ".git"
    "logs"
    "*.log"
    "tmp"
    "temp"
    "*.tmp"
    ".DS_Store"
    "Thumbs.db"
)

# بناء معاملات الاستبعاد
EXCLUDE_ARGS=""
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$pattern"
done

echo "📁 جمع الملفات..."

# إنشاء الأرشيف
cd "$PROJECT_PATH"
tar -czf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" \
    $EXCLUDE_ARGS \
    --exclude="$BACKUP_DIR" \
    .

echo ""
echo "✅ تم إنشاء النسخة الاحتياطية بنجاح!"
echo ""

# حساب حجم النسخة الاحتياطية
BACKUP_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -f1)
echo "📊 معلومات النسخة الاحتياطية:"
echo "   الملف: ${BACKUP_NAME}.tar.gz"
echo "   الحجم: $BACKUP_SIZE"
echo "   المسار: $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
echo ""

# التحقق من سلامة الأرشيف
echo "🔍 التحقق من سلامة الأرشيف..."
if tar -tzf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" > /dev/null 2>&1; then
    echo "✅ الأرشيف سليم"
else
    echo "❌ الأرشيف تالف!"
    exit 1
fi

echo ""

# حساب checksum
echo "🔐 حساب checksum..."
CHECKSUM=$(sha256sum "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -d' ' -f1)
echo "$CHECKSUM  ${BACKUP_NAME}.tar.gz" > "$BACKUP_DIR/${BACKUP_NAME}.sha256"
echo "   SHA256: $CHECKSUM"
echo ""

# حذف النسخ الاحتياطية القديمة (الاحتفاظ بآخر 5)
echo "🧹 تنظيف النسخ الاحتياطية القديمة..."
cd "$BACKUP_DIR"
ls -t ${PROJECT_NAME}_backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm -f
ls -t ${PROJECT_NAME}_backup_*.sha256 2>/dev/null | tail -n +6 | xargs -r rm -f
echo "✅ تم الاحتفاظ بآخر 5 نسخ احتياطية"
echo ""

echo "=========================================="
echo "✅ اكتملت عملية النسخ الاحتياطي بنجاح!"
echo "=========================================="
echo ""
echo "📝 لاستعادة النسخة الاحتياطية:"
echo "   tar -xzf $BACKUP_DIR/${BACKUP_NAME}.tar.gz -C /path/to/restore"
echo ""

