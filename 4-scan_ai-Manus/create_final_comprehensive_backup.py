import os
import tarfile
import time
from datetime import datetime

# --- الإعدادات ---
SOURCE_DIR = '/home/ubuntu/gaara-ai-system'
BACKUP_DIR = '/home/ubuntu/'
PROJECT_NAME = 'gaara_ai_FINAL_COMPREHENSIVE_SYSTEM'

# --- قائمة الاستبعاد ---
EXCLUDE_PATTERNS = [
    # --- Python ---
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.Python',
    'build/',
    'develop-eggs/',
    'dist/',
    'downloads/',
    'eggs/',
    '.eggs/',
    'lib/',
    'lib64/',
    'parts/',
    'sdist/',
    'var/',
    'wheels/',
    'share/python-wheels/',
    '*.egg-info/',
    '.installed.cfg',
    '*.egg',
    'MANIFEST',

    # --- Node.js ---
    'node_modules/',
    'npm-debug.log',
    'yarn-debug.log',
    'yarn-error.log',
    'lerna-debug.log',
    '.pnpm-debug.log',

    # --- البيئة ---
    '.env',
    '.env.local',
    '.env.development.local',
    '.env.test.local',
    '.env.production.local',

    # --- Git ---
    '.git',
    '.gitignore',
    '.gitattributes',
    '.gitmodules',

    # --- IDEs ---
    '.idea/',
    '.vscode/',
    '*.suo',
    '*.ntvs*',
    '*.njsproj',
    '*.sln',
    '*.swp',

    # --- ملفات النظام والنسخ الاحتياطي ---
    '*.log',
    '*.log.*',
    '*.gz',
    '*.zip',
    '*.tar',
    '*.bak',
    '*.tmp',
    'temp/',
    'tmp/',

    # --- ملفات خاصة بالمشروع ---
    'performance_report.md',
    'code_quality_issues.txt',
    'create_final_backup.py',
    'create_final_comprehensive_backup.py'
]

def filter_function(tarinfo):
    """دالة لتحديد الملفات التي يجب استبعادها"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern.endswith('/') and tarinfo.name.startswith(pattern):
            print(f'استبعاد المجلد: {tarinfo.name}')
            return None
        elif not pattern.endswith('/') and pattern in tarinfo.name:
            print(f'استبعاد الملف: {tarinfo.name}')
            return None
    print(f'إضافة: {tarinfo.name}')
    return tarinfo

def main():
    """الدالة الرئيسية لإنشاء النسخة الاحتياطية"""
    print('🚀 بدء إنشاء النسخة الاحتياطية النهائية الشاملة...')

    # إنشاء اسم الملف مع طابع زمني
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'{PROJECT_NAME}_{timestamp}.tar.gz'
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        with tarfile.open(backup_path, 'w:gz') as tar:
            tar.add(SOURCE_DIR, arcname=os.path.basename(SOURCE_DIR), filter=filter_function)

        # حساب حجم الملف
        file_size_mb = os.path.getsize(backup_path) / (1024 * 1024)

        print('\n' + '='*60)
        print('🎉 اكتمل إنشاء النسخة الاحتياطية بنجاح!')
        print(f'📁 اسم الملف: {backup_filename}')
        print(f'💾 الحجم: {file_size_mb:.2f} MB')
        print(f'📍 المسار: {backup_path}')
        print('='*60)

    except Exception as e:
        print(f'❌ حدث خطأ أثناء إنشاء النسخة الاحتياطية: {e}')

if __name__ == '__main__':
    main()

