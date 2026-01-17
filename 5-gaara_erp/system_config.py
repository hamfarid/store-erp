#!/usr/bin/env python3
"""
Gaara ERP System Configuration Manager
=====================================

This script provides advanced configuration management for the Gaara ERP system.
It handles environment setup, database configuration, and system optimization.

Usage:
    python system_config.py [command] [options]

Commands:
    setup       - Initial system setup
    check       - System health check
    optimize    - Performance optimization
    backup      - Create system backup
    restore     - Restore from backup
    update      - Update system components
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import argparse


class GaaraERPConfig:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.config_file = self.base_dir / 'system_config.json'
        self.backup_dir = self.base_dir / 'backups'
        
    def load_config(self):
        """Load system configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()
        
    def save_config(self, config):
        """Save system configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
    def get_default_config(self):
        """Get default system configuration"""
        return {
            "system": {
                "version": "1.0.0",
                "environment": "development",
                "debug": True,
                "language": "ar",
                "timezone": "Asia/Riyadh"
            },
            "database": {
                "engine": "sqlite3",
                "name": "db.sqlite3",
                "backup_enabled": True,
                "backup_interval": "daily"
            },
            "security": {
                "secret_key_rotation": False,
                "session_timeout": 3600,
                "password_policy": {
                    "min_length": 8,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_symbols": False
                }
            },
            "performance": {
                "cache_enabled": True,
                "cache_timeout": 300,
                "compression_enabled": True,
                "static_files_optimization": True
            },
            "features": {
                "ai_integration": True,
                "email_notifications": False,
                "sms_notifications": False,
                "file_uploads": True,
                "api_access": True
            },
            "monitoring": {
                "logging_level": "INFO",
                "performance_monitoring": False,
                "error_reporting": True,
                "usage_analytics": False
            }
        }
        
    def setup_system(self):
        """Initial system setup"""
        print("🔧 إعداد النظام الأولي...")
        
        # Create necessary directories
        directories = [
            self.backup_dir,
            self.gaara_dir / 'logs',
            self.gaara_dir / 'media',
            self.gaara_dir / 'staticfiles',
            self.base_dir / 'temp'
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"✅ تم إنشاء المجلد: {directory.name}")
            
        # Create default configuration
        config = self.get_default_config()
        self.save_config(config)
        print("✅ تم إنشاء ملف التكوين الافتراضي")
        
        # Setup environment file
        self.setup_env_file()
        
        # Setup git ignore
        self.setup_gitignore()
        
        print("🎉 تم إكمال الإعداد الأولي بنجاح!")
        
    def setup_env_file(self):
        """Setup environment file"""
        env_file = self.base_dir / '.env'
        if env_file.exists():
            print("✅ ملف .env موجود بالفعل")
            return
            
        env_content = """# Gaara ERP Environment Configuration
# Generated automatically - modify as needed

# Django Core Settings
SECRET_KEY=django-insecure-change-this-in-production-environment
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# Internationalization
LANGUAGE_CODE=ar
TIME_ZONE=Asia/Riyadh

# Company Information
COMPANY_NAME=شركة جارا للأنظمة
COMPANY_EMAIL=info@gaara-erp.com
SUPPORT_EMAIL=support@gaara-erp.com
COMPANY_PHONE=+966-XX-XXX-XXXX

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@gaara-erp.com

# AI Integration
AI_FEATURES_ENABLED=True
OPENAI_API_KEY=your-openai-api-key-here

# Cache Configuration
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
REDIS_URL=redis://127.0.0.1:6379/1

# File Upload Settings
MAX_UPLOAD_SIZE=5242880
ALLOWED_FILE_TYPES=pdf,doc,docx,xls,xlsx,jpg,jpeg,png,gif

# Security Settings
SESSION_COOKIE_AGE=3600
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False

# Performance Settings
ENABLE_COMPRESSION=True
STATIC_FILES_OPTIMIZATION=True

# Monitoring and Logging
LOGGING_LEVEL=INFO
ENABLE_PERFORMANCE_MONITORING=False
ENABLE_ERROR_REPORTING=True

# Backup Settings
BACKUP_ENABLED=True
BACKUP_RETENTION_DAYS=30
BACKUP_SCHEDULE=0 2 * * *

# Development Settings
ENABLE_DEBUG_TOOLBAR=True
ENABLE_SILK_PROFILING=False
"""
        
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("✅ تم إنشاء ملف .env")
        except Exception as e:
            print(f"❌ خطأ في إنشاء ملف .env: {e}")
            
    def setup_gitignore(self):
        """Setup .gitignore file"""
        gitignore_file = self.base_dir / '.gitignore'
        if gitignore_file.exists():
            print("✅ ملف .gitignore موجود بالفعل")
            return
            
        gitignore_content = """# Gaara ERP .gitignore
# Generated automatically

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Temporary files
temp/
tmp/
*.tmp

# Backups
backups/
*.bak
*.backup

# Node.js (for frontend)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover

# Pytest
.pytest_cache/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Celery
celerybeat-schedule
celerybeat.pid

# Redis
dump.rdb

# Local configuration
local_config.py
"""
        
        try:
            with open(gitignore_file, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("✅ تم إنشاء ملف .gitignore")
        except Exception as e:
            print(f"❌ خطأ في إنشاء ملف .gitignore: {e}")
            
    def check_system_health(self):
        """Comprehensive system health check"""
        print("🔍 فحص صحة النظام الشامل...")
        
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "overall_status": "healthy",
            "recommendations": []
        }
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 11):
            health_report["checks"].append({
                "name": "Python Version",
                "status": "pass",
                "message": f"Python {python_version.major}.{python_version.minor}.{python_version.micro}"
            })
        else:
            health_report["checks"].append({
                "name": "Python Version",
                "status": "fail",
                "message": f"Python {python_version.major}.{python_version.minor} (يتطلب 3.11+)"
            })
            health_report["overall_status"] = "critical"
            
        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            health_report["checks"].append({
                "name": "Virtual Environment",
                "status": "pass",
                "message": "البيئة الافتراضية نشطة"
            })
        else:
            health_report["checks"].append({
                "name": "Virtual Environment",
                "status": "warning",
                "message": "البيئة الافتراضية غير نشطة"
            })
            health_report["recommendations"].append("تفعيل البيئة الافتراضية")
            
        # Check disk space
        try:
            disk_usage = shutil.disk_usage(self.base_dir)
            free_gb = disk_usage.free / (1024**3)
            
            if free_gb > 5:
                health_report["checks"].append({
                    "name": "Disk Space",
                    "status": "pass",
                    "message": f"مساحة فارغة: {free_gb:.1f} GB"
                })
            elif free_gb > 1:
                health_report["checks"].append({
                    "name": "Disk Space",
                    "status": "warning",
                    "message": f"مساحة فارغة: {free_gb:.1f} GB"
                })
                health_report["recommendations"].append("تنظيف مساحة القرص")
            else:
                health_report["checks"].append({
                    "name": "Disk Space",
                    "status": "fail",
                    "message": f"مساحة فارغة: {free_gb:.1f} GB"
                })
                health_report["overall_status"] = "critical"
                
        except Exception as e:
            health_report["checks"].append({
                "name": "Disk Space",
                "status": "error",
                "message": f"خطأ في فحص المساحة: {e}"
            })
            
        # Display results
        print("\n📊 نتائج فحص الصحة:")
        for check in health_report["checks"]:
            status_icon = {
                "pass": "✅",
                "warning": "⚠️",
                "fail": "❌",
                "error": "🔥"
            }.get(check["status"], "❓")
            
            print(f"   {status_icon} {check['name']}: {check['message']}")
            
        if health_report["recommendations"]:
            print("\n💡 التوصيات:")
            for rec in health_report["recommendations"]:
                print(f"   • {rec}")
                
        # Save health report
        report_file = self.base_dir / f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(health_report, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 تم حفظ تقرير الصحة: {report_file.name}")
        
        return health_report["overall_status"] == "healthy"


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP System Configuration Manager')
    parser.add_argument('command', choices=['setup', 'check', 'optimize', 'backup', 'restore', 'update'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    config_manager = GaaraERPConfig()
    
    if args.command == 'setup':
        config_manager.setup_system()
    elif args.command == 'check':
        config_manager.check_system_health()
    else:
        print(f"الأمر '{args.command}' غير مدعوم حالياً")


if __name__ == '__main__':
    main()
