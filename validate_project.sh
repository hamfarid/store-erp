#!/bin/bash
# FILE: validate_project.sh
# PURPOSE: التحقق من صحة واكتمال هيكل المشروع المُنشأ
# OWNER: Global Team
# LAST-AUDITED: 2025-10-21

set -e

PROJECT_PATH="${1:-.}"

echo "=========================================="
echo "🔍 التحقق من صحة هيكل المشروع"
echo "المسار: $PROJECT_PATH"
echo "=========================================="
echo ""

cd "$PROJECT_PATH"

# عداد الأخطاء
ERRORS=0
WARNINGS=0

# التحقق من المجلدات الأساسية
echo "📁 التحقق من المجلدات الأساسية..."

REQUIRED_DIRS=(
    "docs"
    "src"
    "src/frontend"
    "src/backend"
    "src/shared"
    "tests"
    "tests/unit"
    "tests/integration"
    "tests/e2e"
    "todo"
    "todo/errors"
    "todo/fixes"
    "todo/development"
    "todo/integration"
    "todo/inspection"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir - مفقود"
        ((ERRORS++))
    fi
done

echo ""

# التحقق من الملفات الأساسية
echo "📝 التحقق من الملفات الأساسية..."

REQUIRED_FILES=(
    "README.md"
    ".gitignore"
    "function_reference.md"
    "docs/TODO.md"
    "docs/DONT_DO_THIS_AGAIN.md"
    "docs/TechStack.md"
    "docs/Inventory.md"
    "docs/API_Contracts.md"
    "docs/DB_Schema.md"
    "docs/Security.md"
    "docs/Permissions_Model.md"
    "docs/Routes_FE.md"
    "docs/Routes_BE.md"
    "docs/Solution_Tradeoff_Log.md"
    "docs/fix_this_error.md"
    "docs/To_ReActivated_again.md"
    "docs/Class_Registry.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - مفقود"
        ((ERRORS++))
    fi
done

echo ""

# التحقق من محتوى الملفات
echo "🔎 التحقق من محتوى الملفات..."

# التحقق من أن TODO.md يحتوي على الأقسام الأساسية
if [ -f "docs/TODO.md" ]; then
    if grep -q "High Priority" "docs/TODO.md" && grep -q "Medium Priority" "docs/TODO.md"; then
        echo "  ✅ docs/TODO.md - يحتوي على الأقسام الأساسية"
    else
        echo "  ⚠️  docs/TODO.md - قد يكون ناقصاً"
        ((WARNINGS++))
    fi
fi

# التحقق من أن .gitignore يحتوي على استبعادات أساسية
if [ -f ".gitignore" ]; then
    if grep -q ".env" ".gitignore" && grep -q "node_modules" ".gitignore"; then
        echo "  ✅ .gitignore - يحتوي على الاستبعادات الأساسية"
    else
        echo "  ⚠️  .gitignore - قد يكون ناقصاً"
        ((WARNINGS++))
    fi
fi

# التحقق من أن Solution_Tradeoff_Log.md يحتوي على القالب
if [ -f "docs/Solution_Tradeoff_Log.md" ]; then
    if grep -q "OSF_Score" "docs/Solution_Tradeoff_Log.md"; then
        echo "  ✅ docs/Solution_Tradeoff_Log.md - يحتوي على قالب OSF_Score"
    else
        echo "  ⚠️  docs/Solution_Tradeoff_Log.md - قد يكون ناقصاً"
        ((WARNINGS++))
    fi
fi

echo ""

# التحقق من الأذونات
echo "🔐 التحقق من الأذونات..."

if [ -f "setup_project_structure.sh" ]; then
    if [ -x "setup_project_structure.sh" ]; then
        echo "  ✅ السكريبتات قابلة للتنفيذ"
    else
        echo "  ⚠️  السكريبتات قد لا تكون قابلة للتنفيذ"
        ((WARNINGS++))
    fi
fi

echo ""

# النتيجة النهائية
echo "=========================================="
echo "📊 ملخص النتائج"
echo "=========================================="
echo "الأخطاء: $ERRORS"
echo "التحذيرات: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ المشروع صحيح ومكتمل!"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  المشروع صحيح مع بعض التحذيرات"
    exit 0
else
    echo "❌ المشروع يحتوي على أخطاء يجب إصلاحها"
    exit 1
fi

