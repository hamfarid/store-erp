#!/bin/bash
# FILE: download_and_setup.sh
# PURPOSE: تحميل وتشغيل سكريبت إنشاء المشروع من GitHub
# OWNER: Global Team
# LAST-AUDITED: 2025-10-21

set -e

PROJECT_NAME="${1:-my_project}"
PROJECT_PATH="${2:-./$PROJECT_NAME}"

echo "=========================================="
echo "تحميل سكريبت الإعداد من GitHub..."
echo "=========================================="

# تحميل السكريبت
SCRIPT_URL="https://raw.githubusercontent.com/hamfarid/global/main/setup_project_structure.sh"
TEMP_SCRIPT="/tmp/setup_project_structure_$$.sh"

if command -v curl &> /dev/null; then
    curl -fsSL "$SCRIPT_URL" -o "$TEMP_SCRIPT"
elif command -v wget &> /dev/null; then
    wget -q "$SCRIPT_URL" -O "$TEMP_SCRIPT"
else
    echo "❌ خطأ: curl أو wget غير متوفر"
    exit 1
fi

# جعل السكريبت قابلاً للتنفيذ
chmod +x "$TEMP_SCRIPT"

echo "✅ تم تحميل السكريبت بنجاح"
echo ""

# تشغيل السكريبت
bash "$TEMP_SCRIPT" "$PROJECT_NAME" "$PROJECT_PATH"

# حذف الملف المؤقت
rm -f "$TEMP_SCRIPT"

echo ""
echo "=========================================="
echo "✅ تم الانتهاء بنجاح!"
echo "=========================================="

