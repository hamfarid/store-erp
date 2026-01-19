import os
import tarfile
import time

def create_final_backup(source_dir, output_filename):
    """إنشاء نسخة احتياطية نهائية للمشروع."""
    print(f"🚀 بدء إنشاء النسخة الاحتياطية النهائية...")
    start_time = time.time()

    excluded_files_and_dirs = [
        '__pycache__',
        '.git',
        '.vscode',
        'node_modules',
        'test_performance.db',
        'performance_report.md',
        'create_final_backup.py',
        'FINAL_README.md',
        '.DS_Store',
        '*.pyc',
        '*.log',
        '*.swp',
    ]

    def exclude_function(tarinfo):
        """دالة لتحديد الملفات والمجلدات المستبعدة."""
        filename = os.path.basename(tarinfo.name)
        if any(excluded in tarinfo.name for excluded in excluded_files_and_dirs):
            print(f"   - مستبعد: {tarinfo.name}")
            return None
        print(f"   + مضمن: {tarinfo.name}")
        return tarinfo

    try:
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir), filter=exclude_function)

        end_time = time.time()
        file_size = os.path.getsize(output_filename) / (1024 * 1024)

        print(f"\n✅ تم إنشاء النسخة الاحتياطية بنجاح!")
        print(f"   - الملف: {output_filename}")
        print(f"   - الحجم: {file_size:.2f} MB")
        print(f"   - المدة: {end_time - start_time:.2f} ثانية")

    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")

if __name__ == "__main__":
    source_directory = '/home/ubuntu/gaara-ai-system'
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_filename = f'/home/ubuntu/gaara_ai_FINAL_SYSTEM_{timestamp}.tar.gz'
    create_final_backup(source_directory, backup_filename)

