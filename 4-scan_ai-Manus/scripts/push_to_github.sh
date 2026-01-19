#!/bin/bash
# ==========================================
# سكريبت رفع المشروع إلى GitHub
# Push to GitHub Script
# ==========================================

echo "🚀 سكريبت رفع المشروع إلى GitHub"
echo "================================="
echo ""

# الانتقال إلى مجلد المشروع
cd "$(dirname "$0")/.."
PROJECT_PATH=$(pwd)

echo "📁 مجلد المشروع: $PROJECT_PATH"
echo ""

# التحقق من وجود Git
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت!"
    echo "يرجى تثبيت Git أولاً"
    exit 1
fi

# التحقق من وجود remote
REMOTE=$(git remote -v 2>/dev/null)
if [ -n "$REMOTE" ]; then
    echo "✅ تم العثور على remote:"
    echo "$REMOTE"
    echo ""
    
    read -p "هل تريد رفع الملفات الآن؟ (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        BRANCH=$(git branch --show-current)
        echo "📌 الفرع الحالي: $BRANCH"
        echo ""
        echo "⬆️  جاري رفع الملفات..."
        git push -u origin "$BRANCH"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ تم رفع الملفات بنجاح!"
        else
            echo ""
            echo "❌ فشل رفع الملفات!"
            echo "يرجى التحقق من:"
            echo "  1. اسم المستخدم وكلمة المرور/Token"
            echo "  2. صلاحيات المستودع"
            echo "  3. اتصال الإنترنت"
        fi
    fi
else
    echo "⚠️  لم يتم العثور على remote"
    echo ""
    echo "يرجى إضافة remote أولاً:"
    echo ""
    echo "git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
    echo ""
    echo "أو:"
    echo ""
    echo "git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git"
    echo ""
    
    read -p "هل تريد إضافة remote الآن؟ (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "أدخل رابط المستودع: " REPO_URL
        if [ -n "$REPO_URL" ]; then
            git remote add origin "$REPO_URL"
            echo "✅ تم إضافة remote بنجاح!"
            echo ""
            
            read -p "هل تريد رفع الملفات الآن？ (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                BRANCH=$(git branch --show-current)
                echo ""
                echo "⬆️  جاري رفع الملفات..."
                git push -u origin "$BRANCH"
            fi
        fi
    fi
fi

echo ""
echo "✨ انتهى!"

