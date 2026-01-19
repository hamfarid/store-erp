#!/bin/bash
# File: /home/ubuntu/clean_project/create_backup.sh
# مسار الملف: /home/ubuntu/clean_project/create_backup.sh

# سكريبت إنشاء نسخة احتياطية شاملة لمشروع WhatIsScanAI
# يستبعد الملفات غير المرغوب فيها ويحتفظ بجميع الملفات المهمة

set -e  # إيقاف السكريبت عند حدوث خطأ

# متغيرات التكوين
PROJECT_NAME="WhatIsScanAI_Complete"
BACKUP_DIR="/home/ubuntu/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="${PROJECT_NAME}_${TIMESTAMP}"
SOURCE_DIR="/home/ubuntu/clean_project"

# إنشاء مجلد النسخ الاحتياطية
mkdir -p "$BACKUP_DIR"

echo "🚀 بدء إنشاء النسخة الاحتياطية الشاملة..."
echo "📁 المصدر: $SOURCE_DIR"
echo "💾 الوجهة: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
echo "⏰ الوقت: $(date)"
echo "=" * 60

# إنشاء ملف مؤقت لقائمة الاستبعاد
EXCLUDE_FILE=$(mktemp)

# قائمة الملفات والمجلدات المستبعدة
cat > "$EXCLUDE_FILE" << EOF
.env
.venv
venv/
env/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.DS_Store
.vscode/
.idea/
*.swp
*.swo
*~
.tmp/
temp/
tmp/
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.eslintcache
.parcel-cache/
dist/
build/
*.log
logs/
*.sqlite
*.db
test_*.db
*.db-journal
.git/
.gitignore
Thumbs.db
desktop.ini
EOF

echo "📋 قائمة الملفات المستبعدة:"
cat "$EXCLUDE_FILE" | sed 's/^/  - /'
echo ""

# إنشاء النسخة الاحتياطية
echo "📦 إنشاء الأرشيف المضغوط..."
cd "$(dirname "$SOURCE_DIR")"

tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
    --exclude-from="$EXCLUDE_FILE" \
    --exclude="$BACKUP_DIR" \
    "$(basename "$SOURCE_DIR")"

# تنظيف الملف المؤقت
rm "$EXCLUDE_FILE"

# حساب حجم النسخة الاحتياطية
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -f1)

echo "✅ تم إنشاء النسخة الاحتياطية بنجاح!"
echo "📊 حجم النسخة الاحتياطية: $BACKUP_SIZE"
echo "📁 مسار النسخة الاحتياطية: $BACKUP_DIR/$BACKUP_NAME.tar.gz"

# إنشاء ملف معلومات النسخة الاحتياطية
INFO_FILE="$BACKUP_DIR/${BACKUP_NAME}_info.txt"
cat > "$INFO_FILE" << EOF
معلومات النسخة الاحتياطية - مشروع WhatIsScanAI
================================================

اسم النسخة الاحتياطية: $BACKUP_NAME.tar.gz
تاريخ الإنشاء: $(date)
حجم الملف: $BACKUP_SIZE
المسار الكامل: $BACKUP_DIR/$BACKUP_NAME.tar.gz

محتويات النسخة الاحتياطية:
- جميع ملفات المصدر (.py, .vue, .js, .html, .css)
- ملفات التكوين (requirements.txt, docker-compose.yml, etc.)
- ملفات التوثيق (.md, .txt)
- ملفات البيانات الأساسية
- ملفات الاختبار والتقارير

الملفات المستبعدة:
- ملفات البيئة الافتراضية (.venv, venv/)
- ملفات التكوين الحساسة (.env)
- ملفات الكاش (__pycache__, *.pyc)
- ملفات قواعد البيانات المؤقتة (*.db, *.sqlite)
- ملفات السجلات (*.log, logs/)
- ملفات النظام (.DS_Store, Thumbs.db)
- مجلدات التطوير (.git/, .vscode/, .idea/)

طريقة الاستعادة:
1. استخراج الملف: tar -xzf $BACKUP_NAME.tar.gz
2. الانتقال إلى المجلد: cd clean_project
3. تثبيت المتطلبات: pip install -r requirements.txt
4. تشغيل النظام: python src/main.py

ملاحظات:
- تأكد من تثبيت Python 3.8+ قبل الاستعادة
- قم بإنشاء ملف .env جديد مع المتغيرات المطلوبة
- تأكد من تثبيت قاعدة البيانات المطلوبة
EOF

echo "📄 تم إنشاء ملف المعلومات: $INFO_FILE"

# إنشاء قائمة بمحتويات النسخة الاحتياطية
CONTENTS_FILE="$BACKUP_DIR/${BACKUP_NAME}_contents.txt"
echo "📋 إنشاء قائمة المحتويات..."
tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" > "$CONTENTS_FILE"
echo "📄 تم إنشاء قائمة المحتويات: $CONTENTS_FILE"

# إحصائيات النسخة الاحتياطية
TOTAL_FILES=$(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | wc -l)
PYTHON_FILES=$(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | grep -c '\.py$' || true)
VUE_FILES=$(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | grep -c '\.vue$' || true)
JS_FILES=$(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | grep -c '\.js$' || true)
MD_FILES=$(tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | grep -c '\.md$' || true)

echo ""
echo "📊 إحصائيات النسخة الاحتياطية:"
echo "  إجمالي الملفات: $TOTAL_FILES"
echo "  ملفات Python: $PYTHON_FILES"
echo "  ملفات Vue: $VUE_FILES"
echo "  ملفات JavaScript: $JS_FILES"
echo "  ملفات Markdown: $MD_FILES"

# التحقق من سلامة النسخة الاحتياطية
echo ""
echo "🔍 التحقق من سلامة النسخة الاحتياطية..."
if tar -tzf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" > /dev/null 2>&1; then
    echo "✅ النسخة الاحتياطية سليمة ويمكن استخراجها"
else
    echo "❌ خطأ: النسخة الاحتياطية تالفة!"
    exit 1
fi

# إنشاء checksum للتحقق من التكامل
CHECKSUM=$(sha256sum "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -d' ' -f1)
echo "$CHECKSUM  $BACKUP_NAME.tar.gz" > "$BACKUP_DIR/${BACKUP_NAME}_checksum.sha256"
echo "🔐 تم إنشاء checksum: $CHECKSUM"

echo ""
echo "🎉 تمت عملية النسخ الاحتياطي بنجاح!"
echo "📁 الملفات المنشأة:"
echo "  - $BACKUP_DIR/$BACKUP_NAME.tar.gz (النسخة الاحتياطية)"
echo "  - $BACKUP_DIR/${BACKUP_NAME}_info.txt (معلومات النسخة)"
echo "  - $BACKUP_DIR/${BACKUP_NAME}_contents.txt (قائمة المحتويات)"
echo "  - $BACKUP_DIR/${BACKUP_NAME}_checksum.sha256 (التحقق من التكامل)"
echo ""
echo "💡 لاستعادة النسخة الاحتياطية:"
echo "   tar -xzf $BACKUP_DIR/$BACKUP_NAME.tar.gz"
echo ""
echo "🔐 للتحقق من التكامل:"
echo "   sha256sum -c $BACKUP_DIR/${BACKUP_NAME}_checksum.sha256"

