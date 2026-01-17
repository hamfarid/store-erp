#!/usr/bin/env python3
"""
Gaara ERP Backup System
=======================

Comprehensive backup and restore system for Gaara ERP.
Supports database, media files, configuration, and full system backups.

Usage:
    python backup_system.py [command] [options]

Commands:
    backup      - Create backup
    restore     - Restore from backup
    list        - List available backups
    cleanup     - Clean old backups
    schedule    - Setup automated backups

Options:
    --type      - Backup type: full, database, media, config
    --name      - Custom backup name
    --compress  - Compress backup files
    --encrypt   - Encrypt backup files
"""

import os
import sys
import json
import shutil
import tarfile
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import hashlib


class GaaraERPBackup:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.backup_dir = self.base_dir / 'backups'
        self.backup_dir.mkdir(exist_ok=True)

        # Backup configuration
        self.config = {
            'retention_days': 30,
            'compression': True,
            'encryption': False,
            'exclude_patterns': [
                '*.pyc',
                '__pycache__',
                '*.log',
                '.git',
                'node_modules',
                '.venv',
                'venv'
            ]
        }

    def create_backup_metadata(self, backup_type, backup_path, files_included):
        """Create backup metadata file"""
        metadata = {
            'backup_id': self.generate_backup_id(),
            'timestamp': datetime.now().isoformat(),
            'type': backup_type,
            'path': str(backup_path),
            'size_bytes': backup_path.stat().st_size if backup_path.exists() else 0,
            'files_count': len(files_included),
            'files_included': files_included,
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'hostname': os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'unknown'))
            },
            'checksum': self.calculate_file_checksum(backup_path) if backup_path.exists() else None
        }

        metadata_file = backup_path.with_suffix('.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return metadata

    def generate_backup_id(self):
        """Generate unique backup ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_part = hashlib.md5(
            str(datetime.now().timestamp()).encode()).hexdigest()[:8]
        return f"gaara_backup_{timestamp}_{random_part}"

    def calculate_file_checksum(self, file_path):
        """Calculate SHA256 checksum of file"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"⚠️  تحذير: فشل في حساب checksum: {e}")
            return None

    def backup_database(self, backup_name=None):
        """Backup database"""
        print("🗄️  نسخ احتياطي لقاعدة البيانات...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = backup_name or f"database_backup_{timestamp}"

        os.chdir(self.gaara_dir)

        try:
            # Check if using SQLite or PostgreSQL
            db_file = self.gaara_dir / 'db.sqlite3'

            if db_file.exists():
                # SQLite backup
                backup_file = self.backup_dir / f"{backup_name}.sqlite3"
                shutil.copy2(db_file, backup_file)

                files_included = ['db.sqlite3']
                print(f"✅ تم نسخ قاعدة البيانات SQLite: {backup_file.name}")

            else:
                # Django dumpdata backup
                backup_file = self.backup_dir / f"{backup_name}.json"

                result = subprocess.run([
                    sys.executable, 'manage.py', 'dumpdata',
                    '--natural-foreign', '--natural-primary',
                    '--exclude', 'contenttypes',
                    '--exclude', 'auth.permission',
                    '--exclude', 'sessions.session',
                    '--output', str(backup_file)
                ], capture_output=True, text=True, timeout=300)

                if result.returncode != 0:
                    print(f"❌ خطأ في نسخ قاعدة البيانات: {result.stderr}")
                    return None

                files_included = ['django_data.json']
                print(f"✅ تم نسخ بيانات Django: {backup_file.name}")

            # Create metadata
            metadata = self.create_backup_metadata(
                'database', backup_file, files_included)

            return {
                'backup_file': backup_file,
                'metadata': metadata,
                'type': 'database'
            }

        except Exception as e:
            print(f"❌ خطأ في نسخ قاعدة البيانات: {e}")
            return None

    def backup_media_files(self, backup_name=None):
        """Backup media files"""
        print("📁 نسخ احتياطي للملفات...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = backup_name or f"media_backup_{timestamp}"

        media_dir = self.gaara_dir / 'media'
        if not media_dir.exists():
            print("⚠️  مجلد الوسائط غير موجود")
            return None

        backup_file = self.backup_dir / f"{backup_name}.tar.gz"

        try:
            files_included = []

            with tarfile.open(backup_file, 'w:gz') as tar:
                for file_path in media_dir.rglob('*'):
                    if file_path.is_file():
                        # Check exclude patterns
                        if not any(pattern in str(file_path) for pattern in self.config['exclude_patterns']):
                            arcname = file_path.relative_to(media_dir)
                            tar.add(file_path, arcname=arcname)
                            files_included.append(str(arcname))

            print(f"✅ تم نسخ {len(files_included)} ملف: {backup_file.name}")

            # Create metadata
            metadata = self.create_backup_metadata(
                'media', backup_file, files_included)

            return {
                'backup_file': backup_file,
                'metadata': metadata,
                'type': 'media'
            }

        except Exception as e:
            print(f"❌ خطأ في نسخ الملفات: {e}")
            return None

    def backup_configuration(self, backup_name=None):
        """Backup configuration files"""
        print("⚙️  نسخ احتياطي للتكوين...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = backup_name or f"config_backup_{timestamp}"

        backup_file = self.backup_dir / f"{backup_name}.zip"

        config_files = [
            '.env',
            'system_config.json',
            'gaara_erp/gaara_erp/settings.py',
            'gaara_erp/gaara_erp/production_settings.py',
            'requirements.txt',
            'package.json',
            '.gitignore'
        ]

        try:
            files_included = []

            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for config_file in config_files:
                    file_path = self.base_dir / config_file
                    if file_path.exists():
                        zipf.write(file_path, config_file)
                        files_included.append(config_file)

            print(
                f"✅ تم نسخ {len(files_included)} ملف تكوين: {backup_file.name}")

            # Create metadata
            metadata = self.create_backup_metadata(
                'configuration', backup_file, files_included)

            return {
                'backup_file': backup_file,
                'metadata': metadata,
                'type': 'configuration'
            }

        except Exception as e:
            print(f"❌ خطأ في نسخ التكوين: {e}")
            return None

    def backup_full_system(self, backup_name=None):
        """Create full system backup"""
        print("🎯 نسخ احتياطي شامل للنظام...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = backup_name or f"full_backup_{timestamp}"

        # Create individual backups
        backups = []

        # Database backup
        db_backup = self.backup_database(f"{backup_name}_database")
        if db_backup:
            backups.append(db_backup)

        # Media backup
        media_backup = self.backup_media_files(f"{backup_name}_media")
        if media_backup:
            backups.append(media_backup)

        # Configuration backup
        config_backup = self.backup_configuration(f"{backup_name}_config")
        if config_backup:
            backups.append(config_backup)

        # Create combined backup archive
        full_backup_file = self.backup_dir / f"{backup_name}_full.tar.gz"

        try:
            with tarfile.open(full_backup_file, 'w:gz') as tar:
                for backup in backups:
                    tar.add(backup['backup_file'],
                            arcname=backup['backup_file'].name)
                    # Also add metadata
                    metadata_file = backup['backup_file'].with_suffix('.json')
                    if metadata_file.exists():
                        tar.add(metadata_file, arcname=metadata_file.name)

            # Create full backup metadata
            all_files = []
            for backup in backups:
                all_files.extend(backup['metadata']['files_included'])

            full_metadata = self.create_backup_metadata(
                'full_system', full_backup_file, all_files)

            print(
                f"✅ تم إنشاء النسخة الاحتياطية الشاملة: {full_backup_file.name}")
            print(f"📊 إجمالي الملفات: {len(all_files)}")
            print(
                f"📦 حجم النسخة: {full_backup_file.stat().st_size / (1024*1024):.1f} MB")

            # Cleanup individual backup files
            for backup in backups:
                backup['backup_file'].unlink(missing_ok=True)
                backup['backup_file'].with_suffix(
                    '.json').unlink(missing_ok=True)

            return {
                'backup_file': full_backup_file,
                'metadata': full_metadata,
                'type': 'full_system',
                'components': [b['type'] for b in backups]
            }

        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الشاملة: {e}")
            return None

    def list_backups(self):
        """List available backups"""
        print("📋 النسخ الاحتياطية المتاحة:")

        backup_files = list(self.backup_dir.glob('*.tar.gz')) + \
            list(self.backup_dir.glob('*.zip')) + \
            list(self.backup_dir.glob('*.sqlite3')) + \
            list(self.backup_dir.glob('*.json'))

        if not backup_files:
            print("   لا توجد نسخ احتياطية")
            return []

        backups_info = []

        for backup_file in sorted(backup_files):
            if backup_file.suffix == '.json' and backup_file.stem.endswith('_backup'):
                continue  # Skip metadata files

            metadata_file = backup_file.with_suffix('.json')

            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)

                    size_mb = backup_file.stat().st_size / (1024*1024)
                    timestamp = datetime.fromisoformat(metadata['timestamp'])

                    print(f"\n📦 {backup_file.name}")
                    print(
                        f"   🕐 التاريخ: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   📊 النوع: {metadata['type']}")
                    print(f"   📏 الحجم: {size_mb:.1f} MB")
                    print(f"   📁 الملفات: {metadata['files_count']}")

                    if metadata.get('checksum'):
                        current_checksum = self.calculate_file_checksum(
                            backup_file)
                        if current_checksum == metadata['checksum']:
                            print("   ✅ التحقق: سليم")
                        else:
                            print("   ❌ التحقق: تالف")

                    backups_info.append({
                        'file': backup_file,
                        'metadata': metadata,
                        'size_mb': size_mb
                    })

                except Exception as e:
                    print(f"   ⚠️  خطأ في قراءة البيانات الوصفية: {e}")
            else:
                # Backup without metadata
                size_mb = backup_file.stat().st_size / (1024*1024)
                mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)

                print(f"\n📦 {backup_file.name}")
                print(f"   🕐 التاريخ: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   📏 الحجم: {size_mb:.1f} MB")
                print("   ⚠️  بدون بيانات وصفية")

                backups_info.append({
                    'file': backup_file,
                    'metadata': None,
                    'size_mb': size_mb
                })

        return backups_info

    def cleanup_old_backups(self, retention_days=None):
        """Clean up old backup files"""
        retention_days = retention_days or self.config['retention_days']
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        print(f"🧹 تنظيف النسخ الأقدم من {retention_days} يوم...")

        backup_files = list(self.backup_dir.glob('*'))
        deleted_count = 0
        freed_space = 0

        for backup_file in backup_files:
            if backup_file.is_file():
                file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)

                if file_time < cutoff_date:
                    file_size = backup_file.stat().st_size
                    backup_file.unlink()
                    deleted_count += 1
                    freed_space += file_size
                    print(f"   🗑️  حُذف: {backup_file.name}")

        if deleted_count > 0:
            print(f"✅ تم حذف {deleted_count} ملف")
            print(f"💾 تم توفير {freed_space / (1024*1024):.1f} MB")
        else:
            print("✅ لا توجد ملفات قديمة للحذف")


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP Backup System')
    parser.add_argument('command', choices=['backup', 'restore', 'list', 'cleanup'],
                        help='Command to execute')
    parser.add_argument('--type', choices=['full', 'database', 'media', 'config'],
                        default='full', help='Backup type')
    parser.add_argument('--name', help='Custom backup name')
    parser.add_argument('--retention-days', type=int, default=30,
                        help='Retention period for cleanup (days)')

    args = parser.parse_args()

    backup_system = GaaraERPBackup()

    if args.command == 'backup':
        if args.type == 'full':
            backup_system.backup_full_system(args.name)
        elif args.type == 'database':
            backup_system.backup_database(args.name)
        elif args.type == 'media':
            backup_system.backup_media_files(args.name)
        elif args.type == 'config':
            backup_system.backup_configuration(args.name)

    elif args.command == 'list':
        backup_system.list_backups()

    elif args.command == 'cleanup':
        backup_system.cleanup_old_backups(args.retention_days)

    elif args.command == 'restore':
        print("🔄 وظيفة الاستعادة قيد التطوير...")


if __name__ == '__main__':
    main()
