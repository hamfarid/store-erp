#!/bin/bash

# 🏪 نظام إدارة المخزون الكامل - سكريبت إنشاء الأرشيف
# Complete Inventory Management System - Archive Creation Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="complete_inventory_system"
VERSION="v1.0.0"
DATE=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="${PROJECT_NAME}_${VERSION}_${DATE}"

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

# Function to create archive
create_archive() {
    print_status "🗜️ بدء إنشاء الأرشيف المضغوط..."
    print_status "🗜️ Starting archive creation..."
    
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "يرجى تشغيل هذا السكريبت من المجلد الجذر للمشروع"
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Create temporary directory for clean copy
    TEMP_DIR="/tmp/${ARCHIVE_NAME}"
    print_status "إنشاء مجلد مؤقت: $TEMP_DIR"
    print_status "Creating temporary directory: $TEMP_DIR"
    
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR"
    
    # Copy project files (excluding unnecessary files)
    print_status "نسخ ملفات المشروع..."
    print_status "Copying project files..."
    
    # Copy main directories and files
    cp -r backend "$TEMP_DIR/"
    cp -r frontend "$TEMP_DIR/"
    cp -r scripts "$TEMP_DIR/"
    cp -r docs "$TEMP_DIR/"
    
    # Copy root files
    cp README.md "$TEMP_DIR/"
    cp PROJECT_SUMMARY.md "$TEMP_DIR/"
    
    # Copy git files if they exist
    if [ -f ".gitignore" ]; then
        cp .gitignore "$TEMP_DIR/"
    fi
    
    if [ -f ".gitattributes" ]; then
        cp .gitattributes "$TEMP_DIR/"
    fi
    
    # Clean up unnecessary files from the copy
    print_status "تنظيف الملفات غير الضرورية..."
    print_status "Cleaning unnecessary files..."
    
    # Remove Python cache
    find "$TEMP_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$TEMP_DIR" -name "*.pyc" -delete 2>/dev/null || true
    find "$TEMP_DIR" -name "*.pyo" -delete 2>/dev/null || true
    
    # Remove Node.js dependencies (will be installed by user)
    rm -rf "$TEMP_DIR/frontend/node_modules" 2>/dev/null || true
    rm -rf "$TEMP_DIR/frontend/dist" 2>/dev/null || true
    rm -rf "$TEMP_DIR/frontend/.next" 2>/dev/null || true
    
    # Remove Python virtual environment
    rm -rf "$TEMP_DIR/backend/venv" 2>/dev/null || true
    rm -rf "$TEMP_DIR/backend/env" 2>/dev/null || true
    
    # Remove database files (will be created fresh)
    rm -rf "$TEMP_DIR/backend/instance" 2>/dev/null || true
    
    # Remove log files
    rm -rf "$TEMP_DIR/backend/logs" 2>/dev/null || true
    rm -rf "$TEMP_DIR/logs" 2>/dev/null || true
    
    # Remove IDE files
    rm -rf "$TEMP_DIR/.vscode" 2>/dev/null || true
    rm -rf "$TEMP_DIR/.idea" 2>/dev/null || true
    find "$TEMP_DIR" -name ".DS_Store" -delete 2>/dev/null || true
    
    # Remove temporary files
    find "$TEMP_DIR" -name "*.tmp" -delete 2>/dev/null || true
    find "$TEMP_DIR" -name "*.temp" -delete 2>/dev/null || true
    find "$TEMP_DIR" -name "*~" -delete 2>/dev/null || true
    
    # Create archive info file
    print_status "إنشاء ملف معلومات الأرشيف..."
    print_status "Creating archive info file..."
    
    cat > "$TEMP_DIR/ARCHIVE_INFO.txt" << EOF
# 🏪 نظام إدارة المخزون الكامل - معلومات الأرشيف
# Complete Inventory Management System - Archive Information

Archive Name: ${ARCHIVE_NAME}
Version: ${VERSION}
Creation Date: $(date)
Created By: Automated Archive Script

## 📋 محتويات الأرشيف / Archive Contents:

### 📂 المجلدات الرئيسية / Main Directories:
- backend/          # الخادم الخلفي (Flask + Python)
- frontend/         # الواجهة الأمامية (React + Vite)
- scripts/          # سكريبتات التشغيل والنشر
- docs/             # الوثائق والتوثيق

### 📄 الملفات الرئيسية / Main Files:
- README.md         # دليل المشروع
- PROJECT_SUMMARY.md # ملخص المشروع
- ARCHIVE_INFO.txt  # هذا الملف

## 🚀 خطوات التثبيت السريع / Quick Installation:

1. استخراج الأرشيف / Extract archive:
   unzip ${ARCHIVE_NAME}.zip
   cd ${ARCHIVE_NAME}

2. تشغيل سكريبت التثبيت / Run installation script:
   chmod +x scripts/*.sh
   ./scripts/install.sh

3. تشغيل النظام / Start system:
   ./scripts/start.sh

4. الوصول للنظام / Access system:
   Frontend: http://localhost:5173
   Backend: http://localhost:8000

## 📋 المتطلبات / Requirements:
- Python 3.9+
- Node.js 18.0.0+
- npm 9.0.0+
- 4GB RAM (8GB recommended)
- 2GB free disk space

## 📞 الدعم / Support:
راجع ملف README.md للحصول على تعليمات مفصلة
See README.md for detailed instructions

تاريخ الإنشاء: $(date)
Creation Date: $(date)
EOF
    
    # Create checksums file
    print_status "إنشاء ملف المجاميع التحققية..."
    print_status "Creating checksums file..."
    
    cd "$TEMP_DIR"
    find . -type f -exec sha256sum {} \; > CHECKSUMS.sha256
    cd - > /dev/null
    
    # Create the archive
    print_status "إنشاء الملف المضغوط..."
    print_status "Creating compressed archive..."
    
    # Create ZIP archive
    cd "$(dirname "$TEMP_DIR")"
    zip -r "${ARCHIVE_NAME}.zip" "$(basename "$TEMP_DIR")" -x "*.git*" > /dev/null
    
    # Move archive to current directory
    mv "${ARCHIVE_NAME}.zip" "$OLDPWD/"
    
    # Create TAR.GZ archive as alternative
    tar -czf "${ARCHIVE_NAME}.tar.gz" "$(basename "$TEMP_DIR")" --exclude="*.git*"
    mv "${ARCHIVE_NAME}.tar.gz" "$OLDPWD/"
    
    cd "$OLDPWD"
    
    # Clean up temporary directory
    rm -rf "$TEMP_DIR"
    
    # Get file sizes
    ZIP_SIZE=$(du -h "${ARCHIVE_NAME}.zip" | cut -f1)
    TAR_SIZE=$(du -h "${ARCHIVE_NAME}.tar.gz" | cut -f1)
    
    print_success "🎉 تم إنشاء الأرشيف بنجاح!"
    print_success "🎉 Archive created successfully!"
    
    echo ""
    print_status "الملفات المنشأة:"
    print_status "Created files:"
    print_status "  📦 ${ARCHIVE_NAME}.zip (${ZIP_SIZE})"
    print_status "  📦 ${ARCHIVE_NAME}.tar.gz (${TAR_SIZE})"
    
    echo ""
    print_status "معلومات الأرشيف:"
    print_status "Archive information:"
    print_status "  الاسم / Name: ${ARCHIVE_NAME}"
    print_status "  الإصدار / Version: ${VERSION}"
    print_status "  التاريخ / Date: ${DATE}"
    
    echo ""
    print_status "للاستخدام:"
    print_status "To use:"
    print_status "  unzip ${ARCHIVE_NAME}.zip"
    print_status "  cd ${ARCHIVE_NAME}"
    print_status "  ./scripts/install.sh"
    
    # Verify archives
    print_status "التحقق من سلامة الأرشيف..."
    print_status "Verifying archive integrity..."
    
    if zip -T "${ARCHIVE_NAME}.zip" > /dev/null 2>&1; then
        print_success "✓ ملف ZIP سليم"
        print_success "✓ ZIP file is valid"
    else
        print_error "✗ ملف ZIP تالف"
        print_error "✗ ZIP file is corrupted"
    fi
    
    if tar -tzf "${ARCHIVE_NAME}.tar.gz" > /dev/null 2>&1; then
        print_success "✓ ملف TAR.GZ سليم"
        print_success "✓ TAR.GZ file is valid"
    else
        print_error "✗ ملف TAR.GZ تالف"
        print_error "✗ TAR.GZ file is corrupted"
    fi
}

# Function to create source-only archive (without dependencies)
create_source_archive() {
    print_status "إنشاء أرشيف الكود المصدري فقط..."
    print_status "Creating source-only archive..."
    
    SOURCE_ARCHIVE_NAME="${PROJECT_NAME}_source_${VERSION}_${DATE}"
    
    # Create source archive with git if available
    if [ -d ".git" ]; then
        git archive --format=zip --prefix="${SOURCE_ARCHIVE_NAME}/" HEAD > "${SOURCE_ARCHIVE_NAME}.zip"
        print_success "تم إنشاء أرشيف Git: ${SOURCE_ARCHIVE_NAME}.zip"
        print_success "Git archive created: ${SOURCE_ARCHIVE_NAME}.zip"
    else
        print_warning "مستودع Git غير موجود، سيتم إنشاء أرشيف عادي"
        print_warning "Git repository not found, creating regular archive"
        
        # Create regular source archive
        zip -r "${SOURCE_ARCHIVE_NAME}.zip" . \
            -x "*/node_modules/*" \
            -x "*/venv/*" \
            -x "*/env/*" \
            -x "*/__pycache__/*" \
            -x "*/dist/*" \
            -x "*/build/*" \
            -x "*/.next/*" \
            -x "*/instance/*" \
            -x "*/logs/*" \
            -x "*/.git/*" \
            -x "*/.vscode/*" \
            -x "*/.idea/*" \
            -x "*.pyc" \
            -x "*.pyo" \
            -x "*.tmp" \
            -x "*.temp" \
            -x "*~" \
            -x ".DS_Store"
        
        print_success "تم إنشاء أرشيف الكود المصدري: ${SOURCE_ARCHIVE_NAME}.zip"
        print_success "Source archive created: ${SOURCE_ARCHIVE_NAME}.zip"
    fi
}

# Main function
main() {
    print_status "🗜️ بدء إنشاء أرشيف نظام إدارة المخزون..."
    print_status "🗜️ Starting inventory system archive creation..."
    
    case "${1:-full}" in
        "full")
            create_archive
            ;;
        "source")
            create_source_archive
            ;;
        "both")
            create_archive
            create_source_archive
            ;;
        *)
            echo "Usage: $0 {full|source|both}"
            echo "الاستخدام: $0 {full|source|both}"
            echo ""
            echo "  full   - أرشيف كامل (افتراضي)"
            echo "  source - أرشيف الكود المصدري فقط"
            echo "  both   - كلا النوعين"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
