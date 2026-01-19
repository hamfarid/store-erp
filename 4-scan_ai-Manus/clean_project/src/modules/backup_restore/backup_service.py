# File: /home/ubuntu/ai_web_organized/src/modules/backup_restore/backup_service.py
"""
from flask import g
خدمة النسخ الاحتياطي والاستعادة
توفر هذه الوحدة خدمات لإنشاء وإدارة النسخ الاحتياطية واستعادة البيانات
"""

import os
import json
import time
import shutil
import tarfile
import datetime
import logging
from pathlib import Path
import subprocess
import threading
import queue

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backup_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BackupService:
    """خدمة النسخ الاحتياطي والاستعادة"""

    def __init__(self, config=None):
        """
        تهيئة خدمة النسخ الاحتياطي

        Args:
            config (dict, optional): إعدادات النسخ الاحتياطي. Defaults to None.
        """
        # الإعدادات الافتراضية
        self.default_config = {
            'backup_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups'),
            'temp_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'),
            'max_backups': 10,
            'compression': 'gz',  # 'gz', 'bz2', 'xz'
            'include_dirs': [],
            'exclude_patterns': ['.env', '*.pyc', '__pycache__', '*.log', 'node_modules', '.git'],
            'backup_db': True,
            'db_config': {
                'host': 'localhost',
                'port': 5432,
                'user': 'postgres',
                'password': 'postgres',
                'database': 'gaara_erp'
            }
        }

        # دمج الإعدادات المخصصة مع الإعدادات الافتراضية
        self.config = self.default_config.copy()
        if config:
            self.config.update(config)

        # التأكد من وجود مجلدات النسخ الاحتياطي والمؤقت
        os.makedirs(self.config['backup_dir'], exist_ok=True)
        os.makedirs(self.config['temp_dir'], exist_ok=True)

        # قائمة العمليات الجارية
        self.running_tasks = {}
        self.task_queue = queue.Queue()
        self.worker_thread = None

        # بدء خيط العمل
        self._start_worker()

    def _start_worker(self):
        """بدء خيط العمل لمعالجة المهام في الخلفية"""
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self._process_tasks)
            self.worker_thread.daemon = True
            self.worker_thread.start()

    def _process_tasks(self):
        """معالجة المهام في الخلفية"""
        while True:
            try:
                task_id, task_type, args, kwargs = self.task_queue.get()

                # تحديث حالة المهمة
                self.running_tasks[task_id]['status'] = 'running'

                try:
                    # تنفيذ المهمة المناسبة
                    if task_type == 'create_backup':
                        result = self._create_backup_internal(*args, **kwargs)
                    elif task_type == 'restore_backup':
                        result = self._restore_backup_internal(*args, **kwargs)
                    else:
                        result = {'success': False, 'error': f'Unknown task type: {task_type}'}

                    # تحديث حالة المهمة بالنتيجة
                    self.running_tasks[task_id].update({
                        'status': 'completed',
                        'completed_at': datetime.datetime.now().isoformat(),
                        'result': result
                    })
                except Exception as e:
                    logger.exception(f"Error processing task {task_id}: {str(e)}")
                    # تحديث حالة المهمة بالخطأ
                    self.running_tasks[task_id].update({
                        'status': 'failed',
                        'completed_at': datetime.datetime.now().isoformat(),
                        'error': str(e)
                    })

                # إشارة إلى اكتمال المهمة
                self.task_queue.task_done()
            except Exception as e:
                logger.exception(f"Worker thread error: {str(e)}")
                time.sleep(1)  # تجنب استهلاك CPU في حالة الخطأ

    def create_backup(self, name=None, description=None, include_dirs=None, exclude_patterns=None, backup_db=None):
        """
        إنشاء نسخة احتياطية جديدة

        Args:
            name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            description (str, optional): وصف النسخة الاحتياطية. Defaults to None.
            include_dirs (list, optional): قائمة المجلدات المراد نسخها. Defaults to None.
            exclude_patterns (list, optional): قائمة أنماط الملفات المراد استبعادها. Defaults to None.
            backup_db (bool, optional): ما إذا كان يجب نسخ قاعدة البيانات. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # إنشاء معرف فريد للمهمة
        task_id = f"backup_{int(time.time())}_{os.urandom(4).hex()}"

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'backup',
            'name': name or f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'description': description,
            'status': 'pending',
            'created_at': datetime.datetime.now().isoformat(),
            'completed_at': None,
            'result': None,
            'error': None
        }

        # إضافة المهمة إلى قائمة المهام الجارية
        self.running_tasks[task_id] = task_info

        # إضافة المهمة إلى قائمة الانتظار
        self.task_queue.put((
            task_id,
            'create_backup',
            [],
            {
                'name': name,
                'description': description,
                'include_dirs': include_dirs,
                'exclude_patterns': exclude_patterns,
                'backup_db': backup_db
            }
        ))

        return task_info

    def _create_backup_internal(self, name=None, description=None, include_dirs=None, exclude_patterns=None, backup_db=None):
        """
        التنفيذ الداخلي لإنشاء نسخة احتياطية

        Args:
            name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            description (str, optional): وصف النسخة الاحتياطية. Defaults to None.
            include_dirs (list, optional): قائمة المجلدات المراد نسخها. Defaults to None.
            exclude_patterns (list, optional): قائمة أنماط الملفات المراد استبعادها. Defaults to None.
            backup_db (bool, optional): ما إذا كان يجب نسخ قاعدة البيانات. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # استخدام القيم الافتراضية إذا لم يتم تحديدها
            backup_name = name or f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_description = description or f"Automatic backup created on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            dirs_to_include = include_dirs or self.config['include_dirs']
            patterns_to_exclude = exclude_patterns or self.config['exclude_patterns']
            should_backup_db = backup_db if backup_db is not None else self.config['backup_db']

            # إنشاء مجلد مؤقت للنسخة الاحتياطية
            backup_temp_dir = os.path.join(self.config['temp_dir'], backup_name)
            os.makedirs(backup_temp_dir, exist_ok=True)

            # نسخ المجلدات المحددة
            for dir_path in dirs_to_include:
                if os.path.exists(dir_path):
                    dest_dir = os.path.join(backup_temp_dir, os.path.basename(dir_path))
                    logger.info(f"Copying directory {dir_path} to {dest_dir}")
                    self._copy_directory(dir_path, dest_dir, patterns_to_exclude)
                else:
                    logger.warning(f"Directory {dir_path} does not exist, skipping")

            # نسخ قاعدة البيانات إذا كان مطلوباً
            db_backup_path = None
            if should_backup_db:
                db_backup_path = os.path.join(backup_temp_dir, 'database.sql')
                logger.info(f"Backing up database to {db_backup_path}")
                self._backup_database(db_backup_path)

            # إنشاء ملف التكوين للنسخة الاحتياطية
            backup_config = {
                'name': backup_name,
                'description': backup_description,
                'created_at': datetime.datetime.now().isoformat(),
                'include_dirs': dirs_to_include,
                'exclude_patterns': patterns_to_exclude,
                'backup_db': should_backup_db,
                'db_backup_path': db_backup_path and os.path.basename(db_backup_path)
            }

            # حفظ ملف التكوين
            config_path = os.path.join(backup_temp_dir, 'backup_config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(backup_config, f, ensure_ascii=False, indent=2)

            # إنشاء ملف النسخة الاحتياطية المضغوط
            backup_file_path = os.path.join(self.config['backup_dir'], f"{backup_name}.tar.{self.config['compression']}")
            logger.info(f"Creating compressed backup file {backup_file_path}")

            # تحديد طريقة الضغط
            compression_mode = f"w:{self.config['compression']}"
            with tarfile.open(backup_file_path, compression_mode) as tar:
                tar.add(backup_temp_dir, arcname=os.path.basename(backup_temp_dir))

            # حذف المجلد المؤقت
            shutil.rmtree(backup_temp_dir)

            # التحقق من عدد النسخ الاحتياطية وحذف الأقدم إذا تجاوز الحد
            self._cleanup_old_backups()

            # إنشاء معلومات النسخة الاحتياطية
            backup_info = {
                'name': backup_name,
                'description': backup_description,
                'created_at': backup_config['created_at'],
                'file_path': backup_file_path,
                'file_size': os.path.getsize(backup_file_path),
                'include_dirs': dirs_to_include,
                'backup_db': should_backup_db
            }

            logger.info(f"Backup {backup_name} created successfully")
            return {
                'success': True,
                'backup_info': backup_info
            }
        except Exception as e:
            logger.exception(f"Error creating backup: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def restore_backup(self, backup_name=None, backup_file=None):
        """
        استعادة نسخة احتياطية

        Args:
            backup_name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            backup_file (str, optional): مسار ملف النسخة الاحتياطية. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # التحقق من توفر المعلومات المطلوبة
        if not backup_name and not backup_file:
            raise ValueError("Either backup_name or backup_file must be provided")

        # إذا تم تحديد الاسم فقط، ابحث عن الملف المناسب
        if backup_name and not backup_file:
            for ext in ['gz', 'bz2', 'xz']:
                potential_file = os.path.join(self.config['backup_dir'], f"{backup_name}.tar.{ext}")
                if os.path.exists(potential_file):
                    backup_file = potential_file
                    break

            if not backup_file:
                raise FileNotFoundError(f"Backup file for {backup_name} not found")

        # إنشاء معرف فريد للمهمة
        task_id = f"restore_{int(time.time())}_{os.urandom(4).hex()}"

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'restore',
            'backup_name': backup_name,
            'backup_file': backup_file,
            'status': 'pending',
            'created_at': datetime.datetime.now().isoformat(),
            'completed_at': None,
            'result': None,
            'error': None
        }

        # إضافة المهمة إلى قائمة المهام الجارية
        self.running_tasks[task_id] = task_info

        # إضافة المهمة إلى قائمة الانتظار
        self.task_queue.put((
            task_id,
            'restore_backup',
            [],
            {
                'backup_name': backup_name,
                'backup_file': backup_file
            }
        ))

        return task_info

    def _restore_backup_internal(self, backup_name=None, backup_file=None):
        """
        التنفيذ الداخلي لاستعادة نسخة احتياطية

        Args:
            backup_name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            backup_file (str, optional): مسار ملف النسخة الاحتياطية. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # التحقق من وجود ملف النسخة الاحتياطية
            if not os.path.exists(backup_file):
                raise FileNotFoundError(f"Backup file {backup_file} not found")

            # إنشاء مجلد مؤقت لاستخراج النسخة الاحتياطية
            extract_dir = os.path.join(self.config['temp_dir'], f"restore_{int(time.time())}")
            os.makedirs(extract_dir, exist_ok=True)

            # استخراج النسخة الاحتياطية
            logger.info(f"Extracting backup file {backup_file} to {extract_dir}")
            with tarfile.open(backup_file, 'r:*') as tar:
                tar.extractall(path=extract_dir)

            # البحث عن مجلد النسخة الاحتياطية داخل المجلد المستخرج
            backup_dirs = [d for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
            if not backup_dirs:
                raise ValueError("No backup directory found in the extracted files")

            backup_dir = os.path.join(extract_dir, backup_dirs[0])

            # قراءة ملف التكوين
            config_path = os.path.join(backup_dir, 'backup_config.json')
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Backup configuration file not found in {backup_dir}")

            with open(config_path, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)

            # استعادة المجلدات
            for dir_name in os.listdir(backup_dir):
                dir_path = os.path.join(backup_dir, dir_name)
                if os.path.isdir(dir_path) and dir_name != 'database':
                    # البحث عن المجلد المقابل في الإعدادات
                    for include_dir in backup_config['include_dirs']:
                        if os.path.basename(include_dir) == dir_name:
                            target_dir = include_dir
                            logger.info(f"Restoring directory {dir_path} to {target_dir}")

                            # إنشاء نسخة احتياطية من المجلد الحالي إذا كان موجوداً
                            if os.path.exists(target_dir):
                                backup_target_dir = f"{target_dir}_backup_{int(time.time())}"
                                logger.info(f"Creating backup of existing directory {target_dir} to {backup_target_dir}")
                                shutil.move(target_dir, backup_target_dir)

                            # نسخ المجلد من النسخة الاحتياطية
                            shutil.copytree(dir_path, target_dir)
                            break

            # استعادة قاعدة البيانات إذا كانت موجودة
            if backup_config.get('backup_db') and backup_config.get('db_backup_path'):
                db_backup_path = os.path.join(backup_dir, backup_config['db_backup_path'])
                if os.path.exists(db_backup_path):
                    logger.info(f"Restoring database from {db_backup_path}")
                    self._restore_database(db_backup_path)

            # حذف المجلد المؤقت
            shutil.rmtree(extract_dir)

            logger.info(f"Backup {backup_name or os.path.basename(backup_file)} restored successfully")
            return {
                'success': True,
                'message': f"Backup {backup_name or os.path.basename(backup_file)} restored successfully"
            }
        except Exception as e:
            logger.exception(f"Error restoring backup: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_backups(self):
        """
        الحصول على قائمة النسخ الاحتياطية المتوفرة

        Returns:
            list: قائمة النسخ الاحتياطية
        """
        backups = []

        # البحث عن ملفات النسخ الاحتياطية
        for file_name in os.listdir(self.config['backup_dir']):
            file_path = os.path.join(self.config['backup_dir'], file_name)

            # التحقق من أن الملف هو نسخة احتياطية
            if os.path.isfile(file_path) and any(file_name.endswith(f".tar.{ext}") for ext in ['gz', 'bz2', 'xz']):
                try:
                    # استخراج اسم النسخة الاحتياطية من اسم الملف
                    backup_name = file_name.split('.tar.')[0]

                    # محاولة استخراج ملف التكوين للحصول على معلومات إضافية
                    backup_info = {
                        'name': backup_name,
                        'file_path': file_path,
                        'file_size': os.path.getsize(file_path),
                        'created_at': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                    }

                    # محاولة استخراج معلومات إضافية من ملف التكوين
                    try:
                        with tarfile.open(file_path, 'r:*') as tar:
                            config_file = None
                            for member in tar.getmembers():
                                if member.name.endswith('backup_config.json'):
                                    config_file = member
                                    break

                            if config_file:
                                config_data = tar.extractfile(config_file).read().decode('utf-8')
                                config = json.loads(config_data)

                                # تحديث معلومات النسخة الاحتياطية
                                backup_info.update({
                                    'description': config.get('description'),
                                    'created_at': config.get('created_at', backup_info['created_at']),
                                    'include_dirs': config.get('include_dirs', []),
                                    'backup_db': config.get('backup_db', False)
                                })
                    except Exception as e:
                        logger.warning(f"Error extracting config from {file_path}: {str(e)}")

                    backups.append(backup_info)
                except Exception as e:
                    logger.warning(f"Error processing backup file {file_path}: {str(e)}")

        # ترتيب النسخ الاحتياطية حسب تاريخ الإنشاء (الأحدث أولاً)
        backups.sort(key=lambda x: x['created_at'], reverse=True)

        return backups

    def get_task_status(self, task_id):
        """
        الحصول على حالة مهمة

        Args:
            task_id (str): معرف المهمة

        Returns:
            dict: معلومات المهمة
        """
        return self.running_tasks.get(task_id)

    def get_all_tasks(self):
        """
        الحصول على جميع المهام

        Returns:
            list: قائمة المهام
        """
        return list(self.running_tasks.values())

    def _copy_directory(self, src, dst, exclude_patterns=None):
        """
        نسخ مجلد مع استبعاد أنماط محددة

        Args:
            src (str): المجلد المصدر
            dst (str): المجلد الهدف
            exclude_patterns (list, optional): قائمة أنماط الملفات المراد استبعادها. Defaults to None.
        """
        exclude_patterns = exclude_patterns or []

        # إنشاء المجلد الهدف إذا لم يكن موجوداً
        os.makedirs(dst, exist_ok=True)

        # نسخ الملفات والمجلدات
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            # التحقق من أنماط الاستبعاد
            if any(Path(s).match(pattern) for pattern in exclude_patterns):
                logger.debug(f"Skipping {s} due to exclude pattern")
                continue

            if os.path.isdir(s):
                self._copy_directory(s, d, exclude_patterns)
            else:
                shutil.copy2(s, d)

    def _backup_database(self, output_file):
        """
        نسخ قاعدة البيانات

        Args:
            output_file (str): مسار ملف الإخراج

        Raises:
            Exception: في حالة فشل النسخ
        """
        db_config = self.config['db_config']

        # إنشاء مجلد الإخراج إذا لم يكن موجوداً
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # إعداد متغيرات البيئة لـ pg_dump
        env = os.environ.copy()
        if db_config.get('password'):
            env['PGPASSWORD'] = db_config['password']

        # إعداد أمر pg_dump
        cmd = [
            'pg_dump',
            '-h', db_config.get('host', 'localhost'),
            '-p', str(db_config.get('port', 5432)),
            '-U', db_config.get('user', 'postgres'),
            '-d', db_config.get('database'),
            '-f', output_file,
            '--format=p'  # نص عادي
        ]

        # تنفيذ الأمر
        logger.info(f"Running command: {' '.join(cmd)}")
        process = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # التحقق من نجاح العملية
        if process.returncode != 0:
            error_message = process.stderr.decode('utf-8')
            raise Exception(f"Database backup failed: {error_message}")

    def _restore_database(self, input_file):
        """
        استعادة قاعدة البيانات

        Args:
            input_file (str): مسار ملف النسخة الاحتياطية

        Raises:
            Exception: في حالة فشل الاستعادة
        """
        db_config = self.config['db_config']

        # التحقق من وجود ملف النسخة الاحتياطية
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Database backup file {input_file} not found")

        # إعداد متغيرات البيئة لـ psql
        env = os.environ.copy()
        if db_config.get('password'):
            env['PGPASSWORD'] = db_config['password']

        # إعداد أمر psql
        cmd = [
            'psql',
            '-h', db_config.get('host', 'localhost'),
            '-p', str(db_config.get('port', 5432)),
            '-U', db_config.get('user', 'postgres'),
            '-d', db_config.get('database'),
            '-f', input_file
        ]

        # تنفيذ الأمر
        logger.info(f"Running command: {' '.join(cmd)}")
        process = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # التحقق من نجاح العملية
        if process.returncode != 0:
            error_message = process.stderr.decode('utf-8')
            raise Exception(f"Database restore failed: {error_message}")

    def _cleanup_old_backups(self):
        """
        حذف النسخ الاحتياطية القديمة إذا تجاوز عددها الحد المسموح به
        """
        backups = self.get_backups()

        # التحقق من عدد النسخ الاحتياطية
        if len(backups) > self.config['max_backups']:
            # ترتيب النسخ الاحتياطية حسب تاريخ الإنشاء (الأقدم أولاً)
            backups.sort(key=lambda x: x['created_at'])

            # حذف النسخ الاحتياطية القديمة
            for backup in backups[:len(backups) - self.config['max_backups']]:
                file_path = backup['file_path']
                logger.info(f"Removing old backup {file_path}")
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Error removing old backup {file_path}: {str(e)}")

    def delete_backup(self, backup_name=None, backup_file=None):
        """
        حذف نسخة احتياطية

        Args:
            backup_name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            backup_file (str, optional): مسار ملف النسخة الاحتياطية. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # التحقق من توفر المعلومات المطلوبة
            if not backup_name and not backup_file:
                raise ValueError("Either backup_name or backup_file must be provided")

            # إذا تم تحديد الاسم فقط، ابحث عن الملف المناسب
            if backup_name and not backup_file:
                for ext in ['gz', 'bz2', 'xz']:
                    potential_file = os.path.join(self.config['backup_dir'], f"{backup_name}.tar.{ext}")
                    if os.path.exists(potential_file):
                        backup_file = potential_file
                        break

                if not backup_file:
                    raise FileNotFoundError(f"Backup file for {backup_name} not found")

            # التحقق من وجود الملف
            if not os.path.exists(backup_file):
                raise FileNotFoundError(f"Backup file {backup_file} not found")

            # حذف الملف
            os.remove(backup_file)

            return {
                'success': True,
                'message': f"Backup {backup_name or os.path.basename(backup_file)} deleted successfully"
            }
        except Exception as e:
            logger.exception(f"Error deleting backup: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def update_config(self, new_config):
        """
        تحديث إعدادات النسخ الاحتياطي

        Args:
            new_config (dict): الإعدادات الجديدة

        Returns:
            dict: الإعدادات المحدثة
        """
        # تحديث الإعدادات
        self.config.update(new_config)

        # التأكد من وجود مجلدات النسخ الاحتياطي والمؤقت
        os.makedirs(self.config['backup_dir'], exist_ok=True)
        os.makedirs(self.config['temp_dir'], exist_ok=True)

        return self.config

    def get_config(self):
        """
        الحصول على إعدادات النسخ الاحتياطي الحالية

        Returns:
            dict: الإعدادات الحالية
        """
        return self.config
