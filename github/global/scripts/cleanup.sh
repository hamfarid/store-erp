#!/bin/bash

# 🏪 نظام إدارة المخزون الكامل - سكريبت تنظيف الملفات
# Complete Inventory Management System - Cleanup Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to create unneeded directory if it doesn't exist
create_unneeded_dir() {
    if [ ! -d "unneeded" ]; then
        mkdir -p unneeded
        print_status "تم إنشاء مجلد unneeded"
        print_status "Created unneeded directory"
    fi
}

# Function to move files to unneeded directory
move_to_unneeded() {
    local file_path="$1"
    local reason="$2"
    
    if [ -f "$file_path" ] || [ -d "$file_path" ]; then
        # Create subdirectory structure in unneeded
        local dir_path=$(dirname "$file_path")
        mkdir -p "unneeded/$dir_path"
        
        # Move the file/directory
        mv "$file_path" "unneeded/$file_path"
        print_status "نقل $file_path إلى unneeded/ - السبب: $reason"
        print_status "Moved $file_path to unneeded/ - Reason: $reason"
    fi
}

# Main cleanup function
main() {
    print_status "🧹 بدء تنظيف الملفات غير المطلوبة..."
    print_status "🧹 Starting cleanup of unneeded files..."
    
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "يرجى تشغيل هذا السكريبت من المجلد الجذر للمشروع"
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Create unneeded directory
    create_unneeded_dir
    
    # Move old/duplicate files
    print_status "نقل الملفات المكررة والقديمة..."
    print_status "Moving duplicate and old files..."
    
    # Old server files
    move_to_unneeded "start_server.py" "Old server startup file"
    move_to_unneeded "backend/src/unified_server.py" "Old unified server"
    move_to_unneeded "backend/src/unified_server_clean.py" "Old unified server clean"
    
    # Test and development files
    move_to_unneeded "backend/src/test_*.py" "Test files"
    move_to_unneeded "backend/src/check_*.py" "Check files"
    move_to_unneeded "backend/src/final_*.py" "Final test files"
    move_to_unneeded "backend/src/run_*.py" "Run test files"
    move_to_unneeded "backend/src/backend_*.py" "Backend test files"
    
    # Log and monitoring files (keep recent ones)
    move_to_unneeded "log_monitor.py" "Old log monitor"
    move_to_unneeded "system_deployment_check.py" "Old deployment check"
    move_to_unneeded "system_integration_checker.py" "Old integration checker"
    move_to_unneeded "restructure_folders.py" "Old restructure script"
    
    # Development utilities
    move_to_unneeded "backend/src/optimize_*.py" "Optimization utilities"
    move_to_unneeded "backend/src/ssl_*.py" "SSL utilities"
    move_to_unneeded "backend/src/secure_*.py" "Security utilities"
    
    # Frontend development files
    move_to_unneeded "frontend/fix_*.js" "Frontend fix utilities"
    move_to_unneeded "frontend/src/utils/buttonChecker.js" "Button checker utility"
    
    # Backup and migration files
    move_to_unneeded "backend/src/database_migration_*.py" "Database migration files"
    move_to_unneeded "backend/src/backup_*.py" "Backup utilities"
    
    # Performance and monitoring
    move_to_unneeded "backend/src/services/performance_*.py" "Performance monitoring"
    move_to_unneeded "backend/src/middleware/rate_limiter.py" "Rate limiter middleware"
    
    # Clean up empty directories
    print_status "تنظيف المجلدات الفارغة..."
    print_status "Cleaning up empty directories..."
    
    find . -type d -empty -not -path "./unneeded/*" -delete 2>/dev/null || true
    
    # Clean up log files (keep recent ones)
    print_status "تنظيف ملفات السجلات القديمة..."
    print_status "Cleaning up old log files..."
    
    find . -name "*.log" -mtime +7 -not -path "./unneeded/*" -exec mv {} unneeded/ \; 2>/dev/null || true
    
    # Clean up cache and temporary files
    print_status "تنظيف ملفات التخزين المؤقت..."
    print_status "Cleaning up cache and temporary files..."
    
    # Python cache
    find . -type d -name "__pycache__" -not -path "./unneeded/*" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -not -path "./unneeded/*" -delete 2>/dev/null || true
    find . -name "*.pyo" -not -path "./unneeded/*" -delete 2>/dev/null || true
    
    # Node.js cache (but keep node_modules)
    rm -rf frontend/.next 2>/dev/null || true
    rm -rf frontend/dist 2>/dev/null || true
    rm -rf frontend/build 2>/dev/null || true
    
    # IDE files
    rm -rf .vscode 2>/dev/null || true
    rm -rf .idea 2>/dev/null || true
    find . -name ".DS_Store" -delete 2>/dev/null || true
    
    # Create .gitignore for unneeded directory
    cat > unneeded/.gitignore << EOF
# This directory contains files that are not needed for production
# but are kept for reference or potential future use

*
!.gitignore
EOF
    
    # Create README for unneeded directory
    cat > unneeded/README.md << EOF
# Unneeded Files Directory

This directory contains files that have been moved here during cleanup because they are:

- Duplicate files
- Old versions of files
- Development/testing utilities
- Backup files
- Log files older than 7 days
- Cache files

These files are kept for reference but are not needed for the main application to function.

## Contents

- **Test Files**: Various testing and checking utilities
- **Old Server Files**: Previous versions of server startup files
- **Development Utilities**: Tools used during development
- **Log Files**: Old log files and monitoring scripts
- **Cache Files**: Temporary and cache files

## Safety

These files can be safely deleted if disk space is needed, but they are kept here for reference.
EOF
    
    # Summary
    print_success "🎉 تم تنظيف الملفات بنجاح!"
    print_success "🎉 File cleanup completed successfully!"
    
    echo ""
    print_status "ملخص التنظيف:"
    print_status "Cleanup summary:"
    
    if [ -d "unneeded" ]; then
        local file_count=$(find unneeded -type f | wc -l)
        print_status "  تم نقل $file_count ملف إلى مجلد unneeded"
        print_status "  Moved $file_count files to unneeded directory"
    fi
    
    echo ""
    print_status "الملفات المنقولة متاحة في مجلد unneeded/ للمراجعة"
    print_status "Moved files are available in unneeded/ directory for review"
    
    echo ""
    print_warning "يمكن حذف مجلد unneeded بالكامل إذا كنت متأكداً من عدم الحاجة إليه"
    print_warning "The unneeded directory can be completely deleted if you're sure you don't need it"
}

# Handle command line arguments
case "${1:-cleanup}" in
    "cleanup")
        main
        ;;
    "restore")
        if [ -d "unneeded" ]; then
            print_status "استعادة الملفات من مجلد unneeded..."
            print_status "Restoring files from unneeded directory..."
            
            # Move everything back
            find unneeded -mindepth 1 -maxdepth 1 -exec mv {} . \;
            rmdir unneeded
            
            print_success "تم استعادة جميع الملفات"
            print_success "All files restored"
        else
            print_error "مجلد unneeded غير موجود"
            print_error "unneeded directory not found"
        fi
        ;;
    "delete")
        if [ -d "unneeded" ]; then
            print_warning "حذف مجلد unneeded نهائياً..."
            print_warning "Permanently deleting unneeded directory..."
            
            rm -rf unneeded
            
            print_success "تم حذف مجلد unneeded نهائياً"
            print_success "unneeded directory permanently deleted"
        else
            print_error "مجلد unneeded غير موجود"
            print_error "unneeded directory not found"
        fi
        ;;
    *)
        echo "Usage: $0 {cleanup|restore|delete}"
        echo "الاستخدام: $0 {cleanup|restore|delete}"
        echo ""
        echo "  cleanup  - تنظيف الملفات غير المطلوبة (افتراضي)"
        echo "  restore  - استعادة الملفات من مجلد unneeded"
        echo "  delete   - حذف مجلد unneeded نهائياً"
        exit 1
        ;;
esac
