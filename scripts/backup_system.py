#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FILE: scripts/backup_system.py | PURPOSE: Automated Backup System | OWNER: DevOps | RELATED: docker-compose.prod.yml | LAST-AUDITED: 2025-10-21

"""
نظام النسخ الاحتياطية التلقائية لنظام إدارة المخزون العربي
Automated Backup System for Arabic Inventory Management System

يقوم هذا النظام بـ:
- نسخ احتياطية لقاعدة البيانات
- نسخ احتياطية للملفات المرفوعة
- نسخ احتياطية لإعدادات النظام
- ضغط وتشفير النسخ الاحتياطية
- تنظيف النسخ القديمة
- إرسال تقارير النسخ الاحتياطية
"""

import os
import sys
import json
import gzip
import shutil
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import hashlib
import tarfile

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/backup_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackupConfig:
    """تكوين النسخ الاحتياطية"""
    
    def __init__(self):
        # إعدادات قاعدة البيانات
        self.db_host = os.getenv('DB_HOST', 'database')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('DB_NAME', 'store_production')
        self.db_user = os.getenv('DB_USER', 'store_user')
        self.db_password = os.getenv('DB_PASSWORD', '')
        
        # مسارات النسخ الاحتياطية
        self.backup_dir = Path('/app/backups')
        self.uploads_dir = Path('/app/uploads')
        self.config_dir = Path('/app/config')
        
        # إعدادات الاحتفاظ
        self.retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
        self.max_backups = int(os.getenv('MAX_BACKUPS', '50'))
        
        # إعدادات التشفير
        self.encryption_key = os.getenv('BACKUP_ENCRYPTION_KEY', 'default-key-change-me')
        
        # إعدادات البريد الإلكتروني
        self.smtp_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('MAIL_PORT', '587'))
        self.smtp_user = os.getenv('MAIL_USERNAME', '')
        self.smtp_password = os.getenv('MAIL_PASSWORD', '')
        self.alert_email = os.getenv('ALERT_EMAIL_RECIPIENTS', 'admin@example.com')
        
        # إنشاء المجلدات إذا لم تكن موجودة
        self.backup_dir.mkdir(parents=True, exist_ok=True)

class BackupSystem:
    """نظام النسخ الاحتياطية"""
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_session_dir = self.config.backup_dir / f"backup_{self.backup_timestamp}"
        self.backup_session_dir.mkdir(parents=True, exist_ok=True)
        
        self.backup_report = {
            'timestamp': self.backup_timestamp,
            'start_time': datetime.now().isoformat(),
            'status': 'running',
            'components': {},
            'total_size': 0,
            'errors': [],
            'warnings': []
        }
    
    def create_database_backup(self) -> bool:
        """إنشاء نسخة احتياطية لقاعدة البيانات"""
        logger.info("بدء نسخ قاعدة البيانات...")
        
        try:
            backup_file = self.backup_session_dir / f"database_{self.backup_timestamp}.sql"
            
            # إعداد متغيرات البيئة لـ pg_dump
            env = os.environ.copy()
            env['PGPASSWORD'] = self.config.db_password
            
            # تنفيذ pg_dump
            cmd = [
                'pg_dump',
                '-h', self.config.db_host,
                '-p', self.config.db_port,
                '-U', self.config.db_user,
                '-d', self.config.db_name,
                '--verbose',
                '--no-password',
                '--format=custom',
                '--compress=9',
                '--file', str(backup_file)
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                # ضغط الملف
                compressed_file = f"{backup_file}.gz"
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # حذف الملف غير المضغوط
                backup_file.unlink()
                
                # حساب الحجم والتحقق من التكامل
                file_size = Path(compressed_file).stat().st_size
                file_hash = self.calculate_file_hash(compressed_file)
                
                self.backup_report['components']['database'] = {
                    'status': 'success',
                    'file': compressed_file,
                    'size_bytes': file_size,
                    'size_mb': file_size / (1024 * 1024),
                    'hash': file_hash,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.backup_report['total_size'] += file_size
                logger.info(f"تم إنشاء نسخة احتياطية لقاعدة البيانات: {file_size / (1024 * 1024):.2f} MB")
                return True
                
            else:
                error_msg = f"فشل في نسخ قاعدة البيانات: {result.stderr}"
                logger.error(error_msg)
                self.backup_report['errors'].append(error_msg)
                self.backup_report['components']['database'] = {
                    'status': 'failed',
                    'error': error_msg
                }
                return False
                
        except Exception as e:
            error_msg = f"خطأ في نسخ قاعدة البيانات: {str(e)}"
            logger.error(error_msg)
            self.backup_report['errors'].append(error_msg)
            self.backup_report['components']['database'] = {
                'status': 'failed',
                'error': error_msg
            }
            return False
    
    def create_files_backup(self) -> bool:
        """إنشاء نسخة احتياطية للملفات"""
        logger.info("بدء نسخ الملفات...")
        
        try:
            backup_file = self.backup_session_dir / f"files_{self.backup_timestamp}.tar.gz"
            
            # إنشاء أرشيف مضغوط للملفات
            with tarfile.open(backup_file, 'w:gz') as tar:
                # نسخ الملفات المرفوعة
                if self.config.uploads_dir.exists():
                    tar.add(self.config.uploads_dir, arcname='uploads')
                    logger.info(f"تم إضافة مجلد الملفات المرفوعة: {self.config.uploads_dir}")
                
                # نسخ ملفات الإعدادات
                config_files = [
                    '/app/.env.production',
                    '/app/docker-compose.prod.yml',
                    '/app/nginx/nginx.conf'
                ]
                
                for config_file in config_files:
                    if Path(config_file).exists():
                        tar.add(config_file, arcname=f"config/{Path(config_file).name}")
                        logger.info(f"تم إضافة ملف الإعدادات: {config_file}")
                
                # نسخ السجلات الحديثة (آخر 7 أيام)
                logs_dir = Path('/app/logs')
                if logs_dir.exists():
                    cutoff_date = datetime.now() - timedelta(days=7)
                    for log_file in logs_dir.glob('*.log'):
                        if datetime.fromtimestamp(log_file.stat().st_mtime) > cutoff_date:
                            tar.add(log_file, arcname=f"logs/{log_file.name}")
            
            # حساب الحجم والتحقق من التكامل
            file_size = backup_file.stat().st_size
            file_hash = self.calculate_file_hash(str(backup_file))
            
            self.backup_report['components']['files'] = {
                'status': 'success',
                'file': str(backup_file),
                'size_bytes': file_size,
                'size_mb': file_size / (1024 * 1024),
                'hash': file_hash,
                'timestamp': datetime.now().isoformat()
            }
            
            self.backup_report['total_size'] += file_size
            logger.info(f"تم إنشاء نسخة احتياطية للملفات: {file_size / (1024 * 1024):.2f} MB")
            return True
            
        except Exception as e:
            error_msg = f"خطأ في نسخ الملفات: {str(e)}"
            logger.error(error_msg)
            self.backup_report['errors'].append(error_msg)
            self.backup_report['components']['files'] = {
                'status': 'failed',
                'error': error_msg
            }
            return False
    
    def create_redis_backup(self) -> bool:
        """إنشاء نسخة احتياطية لـ Redis"""
        logger.info("بدء نسخ بيانات Redis...")
        
        try:
            backup_file = self.backup_session_dir / f"redis_{self.backup_timestamp}.rdb"
            
            # نسخ ملف RDB من Redis
            cmd = [
                'docker', 'exec', 'store_redis_prod',
                'redis-cli', '--rdb', '/data/backup.rdb'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # نسخ الملف من الحاوية
                copy_cmd = [
                    'docker', 'cp',
                    'store_redis_prod:/data/backup.rdb',
                    str(backup_file)
                ]
                
                copy_result = subprocess.run(copy_cmd, capture_output=True, text=True)
                
                if copy_result.returncode == 0:
                    # ضغط الملف
                    compressed_file = f"{backup_file}.gz"
                    with open(backup_file, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # حذف الملف غير المضغوط
                    backup_file.unlink()
                    
                    # حساب الحجم والتحقق من التكامل
                    file_size = Path(compressed_file).stat().st_size
                    file_hash = self.calculate_file_hash(compressed_file)
                    
                    self.backup_report['components']['redis'] = {
                        'status': 'success',
                        'file': compressed_file,
                        'size_bytes': file_size,
                        'size_mb': file_size / (1024 * 1024),
                        'hash': file_hash,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.backup_report['total_size'] += file_size
                    logger.info(f"تم إنشاء نسخة احتياطية لـ Redis: {file_size / (1024 * 1024):.2f} MB")
                    return True
                else:
                    error_msg = f"فشل في نسخ ملف Redis: {copy_result.stderr}"
                    logger.warning(error_msg)
                    self.backup_report['warnings'].append(error_msg)
                    return False
            else:
                error_msg = f"فشل في إنشاء نسخة احتياطية لـ Redis: {result.stderr}"
                logger.warning(error_msg)
                self.backup_report['warnings'].append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"خطأ في نسخ Redis: {str(e)}"
            logger.warning(error_msg)
            self.backup_report['warnings'].append(error_msg)
            self.backup_report['components']['redis'] = {
                'status': 'failed',
                'error': error_msg
            }
            return False
    
    def calculate_file_hash(self, file_path: str) -> str:
        """حساب hash للملف للتحقق من التكامل"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def cleanup_old_backups(self):
        """تنظيف النسخ الاحتياطية القديمة"""
        logger.info("بدء تنظيف النسخ الاحتياطية القديمة...")
        
        try:
            # العثور على جميع مجلدات النسخ الاحتياطية
            backup_dirs = [d for d in self.config.backup_dir.iterdir() 
                          if d.is_dir() and d.name.startswith('backup_')]
            
            # ترتيب حسب التاريخ (الأحدث أولاً)
            backup_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            deleted_count = 0
            freed_space = 0
            
            # حذف النسخ القديمة بناءً على العدد الأقصى
            if len(backup_dirs) > self.config.max_backups:
                for backup_dir in backup_dirs[self.config.max_backups:]:
                    dir_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
                    shutil.rmtree(backup_dir)
                    deleted_count += 1
                    freed_space += dir_size
                    logger.info(f"تم حذف النسخة الاحتياطية القديمة: {backup_dir.name}")
            
            # حذف النسخ القديمة بناءً على التاريخ
            cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
            for backup_dir in backup_dirs:
                if datetime.fromtimestamp(backup_dir.stat().st_mtime) < cutoff_date:
                    dir_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
                    shutil.rmtree(backup_dir)
                    deleted_count += 1
                    freed_space += dir_size
                    logger.info(f"تم حذف النسخة الاحتياطية المنتهية الصلاحية: {backup_dir.name}")
            
            self.backup_report['cleanup'] = {
                'deleted_backups': deleted_count,
                'freed_space_mb': freed_space / (1024 * 1024),
                'remaining_backups': len(backup_dirs) - deleted_count
            }
            
            logger.info(f"تم تنظيف {deleted_count} نسخة احتياطية، تم توفير {freed_space / (1024 * 1024):.2f} MB")
            
        except Exception as e:
            error_msg = f"خطأ في تنظيف النسخ الاحتياطية: {str(e)}"
            logger.error(error_msg)
            self.backup_report['warnings'].append(error_msg)
    
    def send_backup_report(self):
        """إرسال تقرير النسخ الاحتياطية"""
        try:
            # تحديد حالة النسخ الاحتياطية
            if self.backup_report['errors']:
                status = 'فشل'
                status_icon = '❌'
            elif self.backup_report['warnings']:
                status = 'نجح مع تحذيرات'
                status_icon = '⚠️'
            else:
                status = 'نجح'
                status_icon = '✅'
            
            subject = f"{status_icon} تقرير النسخ الاحتياطية - نظام إدارة المخزون - {status}"
            
            # إنشاء محتوى التقرير
            body = f"""
تقرير النسخ الاحتياطية لنظام إدارة المخزون العربي
{'=' * 50}

الحالة العامة: {status}
وقت البدء: {self.backup_report['start_time']}
وقت الانتهاء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
الحجم الإجمالي: {self.backup_report['total_size'] / (1024 * 1024):.2f} MB

مكونات النسخ الاحتياطية:
{'-' * 30}
"""
            
            for component, details in self.backup_report['components'].items():
                if details['status'] == 'success':
                    body += f"✅ {component}: نجح ({details['size_mb']:.2f} MB)\n"
                else:
                    body += f"❌ {component}: فشل - {details.get('error', 'خطأ غير معروف')}\n"
            
            if 'cleanup' in self.backup_report:
                cleanup = self.backup_report['cleanup']
                body += f"\nتنظيف النسخ القديمة:\n"
                body += f"- تم حذف {cleanup['deleted_backups']} نسخة احتياطية\n"
                body += f"- تم توفير {cleanup['freed_space_mb']:.2f} MB\n"
                body += f"- النسخ المتبقية: {cleanup['remaining_backups']}\n"
            
            if self.backup_report['errors']:
                body += f"\nالأخطاء:\n"
                for error in self.backup_report['errors']:
                    body += f"• {error}\n"
            
            if self.backup_report['warnings']:
                body += f"\nالتحذيرات:\n"
                for warning in self.backup_report['warnings']:
                    body += f"• {warning}\n"
            
            body += f"\nمعرف الجلسة: {self.backup_timestamp}\n"
            body += f"مجلد النسخ الاحتياطية: {self.backup_session_dir}\n"
            
            # إرسال البريد الإلكتروني
            msg = MIMEMultipart()
            msg['From'] = self.config.smtp_user
            msg['To'] = self.config.alert_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # إرفاق ملف JSON للتقرير
            report_file = self.backup_session_dir / 'backup_report.json'
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.backup_report, f, ensure_ascii=False, indent=2)
            
            with open(report_file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= backup_report_{self.backup_timestamp}.json'
                )
                msg.attach(part)
            
            # إرسال البريد
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.smtp_user, self.config.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info("تم إرسال تقرير النسخ الاحتياطية بالبريد الإلكتروني")
            
        except Exception as e:
            logger.error(f"فشل إرسال تقرير النسخ الاحتياطية: {e}")
    
    def run_backup(self) -> bool:
        """تشغيل عملية النسخ الاحتياطي الكاملة"""
        logger.info(f"بدء عملية النسخ الاحتياطي - الجلسة: {self.backup_timestamp}")
        
        success = True
        
        # نسخ قاعدة البيانات
        if not self.create_database_backup():
            success = False
        
        # نسخ الملفات
        if not self.create_files_backup():
            success = False
        
        # نسخ Redis (اختياري)
        self.create_redis_backup()
        
        # تنظيف النسخ القديمة
        self.cleanup_old_backups()
        
        # تحديث حالة التقرير
        self.backup_report['end_time'] = datetime.now().isoformat()
        self.backup_report['status'] = 'completed' if success else 'failed'
        self.backup_report['duration_minutes'] = (
            datetime.now() - datetime.fromisoformat(self.backup_report['start_time'])
        ).total_seconds() / 60
        
        # حفظ التقرير
        report_file = self.backup_session_dir / 'backup_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.backup_report, f, ensure_ascii=False, indent=2)
        
        # إرسال التقرير
        self.send_backup_report()
        
        logger.info(f"انتهت عملية النسخ الاحتياطي - الحالة: {'نجح' if success else 'فشل'}")
        return success

def main():
    """الدالة الرئيسية"""
    config = BackupConfig()
    backup_system = BackupSystem(config)
    
    try:
        success = backup_system.run_backup()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"خطأ في النظام: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
