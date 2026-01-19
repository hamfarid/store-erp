"""
خدمة النسخ الاحتياطي والاستعادة المحسنة
توفر هذه الوحدة خدمات متقدمة لإنشاء وإدارة النسخ الاحتياطية واستعادة البيانات
مع دعم قواعد البيانات المتعددة ومعلومات التعلم وبيانات الحاويات
"""

import os
import json
import time
import shutil
import tarfile
import datetime
import logging
import subprocess
import threading
import queue
from pathlib import Path

# Constants
BACKUP_CONFIG_FILE = 'backup_config.json'

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


class BackupServiceEnhanced:
    """خدمة النسخ الاحتياطي والاستعادة المحسنة"""

    def __init__(self, config=None):
        """
        تهيئة خدمة النسخ الاحتياطي المحسنة

        Args:
            config (dict, optional): إعدادات النسخ الاحتياطي. Defaults to None.
        """
        # الإعدادات الافتراضية
        self.default_config = {
            'backup_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups'),
            'temp_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'),
            'max_backups': 10,
            'compression': 'gz',  # 'gz', 'bz2', 'xz'
            'exclude_patterns': [
                '.env',
                '*.pyc',
                '__pycache__',
                '*.log',
                'node_modules',
                '.git',
                '.cache',
                '*.tmp'
            ],
            'include_txt_md': True,  # تضمين جميع ملفات .txt و .md
            'backup_db': True,
            'db_configs': {
                'main': {
                    'host': 'db',
                    'port': 5432,
                    'user': 'agri_ai_user',
                    'password': 'agri_ai_password',
                    'database': 'agri_ai_db'
                },
                'test': {
                    'host': 'db_test',
                    'port': 5432,
                    'user': 'agri_ai_user',
                    'password': 'agri_ai_password',
                    'database': 'agri_ai_test_db'
                },
                'setup': {
                    'host': 'db_setup',
                    'port': 5432,
                    'user': 'agri_ai_user',
                    'password': 'agri_ai_password',
                    'database': 'agri_ai_setup_db'
                }
            },
            'data_dirs': {
                'config': '/app/config',
                'models': '/app/models',
                'media': '/app/media',
                'uploads': '/app/uploads',
                'data': '/app/data',
                'static': '/app/static'
            },
            'docker': {
                'use_volumes': True,
                'use_bind_mounts': True,
                'volumes': [
                    'postgres_data',
                    'postgres_test_data',
                    'postgres_setup_data',
                    'redis_data',
                    'rabbitmq_data',
                    'elasticsearch_data',
                    'etcd_data',
                    'minio_data'
                ],
                'bind_mounts': [
                    '/app/data',
                    '/app/logs',
                    '/app/media',
                    '/app/static',
                    '/app/uploads',
                    '/app/models',
                    '/app/backups',
                    '/app/config'
                ]
            },
            'schedule': {
                'enabled': True,
                'frequency': 'daily',  # 'hourly', 'daily', 'weekly', 'monthly'
                'time': '02:00',
                'day_of_week': 1,  # 0 = Monday, 6 = Sunday (for weekly)
                'day_of_month': 1  # 1-31 (for monthly)
            }
        }

        # دمج الإعدادات المخصصة مع الإعدادات الافتراضية
        self.config = self.default_config.copy()
        if config:
            self._deep_update(self.config, config)

        # التأكد من وجود مجلدات النسخ الاحتياطي والمؤقت
        os.makedirs(self.config['backup_dir'], exist_ok=True)
        os.makedirs(self.config['temp_dir'], exist_ok=True)

        # قائمة العمليات الجارية
        self.running_tasks = {}
        self.task_queue = queue.Queue()
        self.worker_thread = None

        # بدء خيط العمل
        self._start_worker()

    def _deep_update(self, d, u):
        """
        تحديث عميق للقواميس المتداخلة

        Args:
            d (dict): القاموس الأصلي
            u (dict): القاموس الجديد للتحديث

        Returns:
            dict: القاموس المحدث
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v
        return d

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
                    elif task_type == 'export_data':
                        result = self._export_data_internal(*args, **kwargs)
                    elif task_type == 'import_data':
                        result = self._import_data_internal(*args, **kwargs)
                    else:
                        result = {'success': False, 'error': f'Unknown task type: {task_type}'}

                    # تحديث حالة المهمة بالنتيجة
                    self.running_tasks[task_id].update({
                        'status': 'completed',
                        'completed_at': datetime.datetime.now().isoformat(),
                        'result': result
                    })
                except Exception as e:
                    logger.exception("Error processing task %s: %s", task_id, str(e))
                    # تحديث حالة المهمة بالخطأ
                    self.running_tasks[task_id].update({
                        'status': 'failed',
                        'completed_at': datetime.datetime.now().isoformat(),
                        'error': str(e)
                    })

                # إشارة إلى اكتمال المهمة
                self.task_queue.task_done()
            except Exception as e:
                logger.exception("Worker thread error: %s", str(e))
                time.sleep(1)  # تجنب استهلاك CPU في حالة الخطأ

    def create_backup(self, name=None, description=None, include_dirs=None, exclude_patterns=None,
                      backup_dbs=None, db_names=None, include_volumes=None, include_bind_mounts=None,
                      include_txt_md=None):
        """
        إنشاء نسخة احتياطية جديدة

        Args:
            name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            description (str, optional): وصف النسخة الاحتياطية. Defaults to None.
            include_dirs (list, optional): قائمة المجلدات المراد نسخها. Defaults to None.
            exclude_patterns (list, optional): قائمة أنماط الملفات المراد استبعادها. Defaults to None.
            backup_dbs (bool, optional): ما إذا كان يجب نسخ قواعد البيانات. Defaults to None.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد نسخها. Defaults to None.
            include_volumes (bool, optional): ما إذا كان يجب تضمين Docker Volumes. Defaults to None.
            include_bind_mounts (bool, optional): ما إذا كان يجب تضمين Bind Mounts. Defaults to None.
            include_txt_md (bool, optional): ما إذا كان يجب تضمين جميع ملفات .txt و .md. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # إنشاء معرف فريد للمهمة
        task_id = "backup_{}_{}".format(int(time.time.time()), os.urandom(4).hex())

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'backup',
            'name': name or "backup_{}".format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')),
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
                'backup_dbs': backup_dbs,
                'db_names': db_names,
                'include_volumes': include_volumes,
                'include_bind_mounts': include_bind_mounts,
                'include_txt_md': include_txt_md
            }
        ))

        return task_info

    def _create_backup_internal(self, name=None, description=None, include_dirs=None, exclude_patterns=None,
                                backup_dbs=None, db_names=None, include_volumes=None, include_bind_mounts=None,
                                include_txt_md=None):
        """
        التنفيذ الداخلي لإنشاء نسخة احتياطية

        Args:
            name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            description (str, optional): وصف النسخة الاحتياطية. Defaults to None.
            include_dirs (list, optional): قائمة المجلدات المراد نسخها. Defaults to None.
            exclude_patterns (list, optional): قائمة أنماط الملفات المراد استبعادها. Defaults to None.
            backup_dbs (bool, optional): ما إذا كان يجب نسخ قواعد البيانات. Defaults to None.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد نسخها. Defaults to None.
            include_volumes (bool, optional): ما إذا كان يجب تضمين Docker Volumes. Defaults to None.
            include_bind_mounts (bool, optional): ما إذا كان يجب تضمين Bind Mounts. Defaults to None.
            include_txt_md (bool, optional): ما إذا كان يجب تضمين جميع ملفات .txt و .md. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # استخدام القيم الافتراضية إذا لم يتم تحديدها
            backup_name = name or "backup_{}".format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            backup_description = description or "Automatic backup created on {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            dirs_to_include = include_dirs or list(self.config['data_dirs'].values())
            patterns_to_exclude = exclude_patterns or self.config['exclude_patterns']
            should_backup_dbs = backup_dbs if backup_dbs is not None else self.config['backup_db']
            db_list = db_names or list(self.config['db_configs'].keys())
            should_include_volumes = include_volumes if include_volumes is not None else self.config['docker']['use_volumes']
            should_include_bind_mounts = include_bind_mounts if include_bind_mounts is not None else self.config['docker']['use_bind_mounts']
            should_include_txt_md = include_txt_md if include_txt_md is not None else self.config['include_txt_md']

            # إنشاء مجلد مؤقت للنسخة الاحتياطية
            backup_temp_dir = os.path.join(self.config['temp_dir'], backup_name)
            os.makedirs(backup_temp_dir, exist_ok=True)

            # إنشاء مجلد للبيانات
            data_dir = os.path.join(backup_temp_dir, 'data')
            os.makedirs(data_dir, exist_ok=True)

            # نسخ المجلدات المحددة (Bind Mounts)
            if should_include_bind_mounts:
                for dir_path in dirs_to_include:
                    if os.path.exists(dir_path):
                        dest_dir = os.path.join(data_dir, os.path.basename(dir_path))
                        logger.info("Copying directory %s to %s", dir_path, dest_dir)
                        self._copy_directory(dir_path, dest_dir, patterns_to_exclude, include_txt_md=should_include_txt_md)
                    else:
                        logger.warning("Directory %s does not exist, skipping", dir_path)

            # نسخ قواعد البيانات إذا كان مطلوباً
            db_backup_paths = {}
            if should_backup_dbs:
                db_dir = os.path.join(backup_temp_dir, 'databases')
                os.makedirs(db_dir, exist_ok=True)

                for db_name in db_list:
                    if db_name in self.config['db_configs']:
                        db_config = self.config['db_configs'][db_name]
                        db_backup_path = os.path.join(db_dir, "{}.sql".format(db_name))
                        logger.info("Backing up database %s to %s", db_name, db_backup_path)
                        self._backup_database(db_backup_path, db_config)
                        db_backup_paths[db_name] = os.path.relpath(db_backup_path, backup_temp_dir)

            # نسخ Docker Volumes إذا كان مطلوباً
            volume_backup_paths = {}
            if should_include_volumes:
                volumes_dir = os.path.join(backup_temp_dir, 'volumes')
                os.makedirs(volumes_dir, exist_ok=True)

                for volume_name in self.config['docker']['volumes']:
                    volume_backup_path = os.path.join(volumes_dir, "{}.tar".format(volume_name))
                    logger.info("Backing up Docker volume %s to %s", volume_name, volume_backup_path)
                    success = self._backup_docker_volume(volume_name, volume_backup_path)
                    if success:
                        volume_backup_paths[volume_name] = os.path.relpath(volume_backup_path, backup_temp_dir)

            # إنشاء ملف التكوين للنسخة الاحتياطية
            backup_config = {
                'name': backup_name,
                'description': backup_description,
                'created_at': datetime.datetime.now().isoformat(),
                'include_dirs': dirs_to_include,
                'exclude_patterns': patterns_to_exclude,
                'backup_dbs': should_backup_dbs,
                'db_backup_paths': db_backup_paths,
                'include_volumes': should_include_volumes,
                'volume_backup_paths': volume_backup_paths,
                'include_bind_mounts': should_include_bind_mounts,
                'include_txt_md': should_include_txt_md
            }

            # حفظ ملف التكوين
            config_path = os.path.join(backup_temp_dir, BACKUP_CONFIG_FILE)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(backup_config, f, ensure_ascii=False, indent=2)

            # إنشاء ملف النسخة الاحتياطية المضغوط
            backup_file_path = os.path.join(self.config['backup_dir'], "{}.tar.{}".format(backup_name, self.config['compression']))
            logger.info("Creating compressed backup file %s", backup_file_path)

            # تحديد طريقة الضغط
            compression_mode = "w:{}".format(self.config['compression'])
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
                'backup_dbs': should_backup_dbs,
                'db_names': list(db_backup_paths.keys()),
                'include_volumes': should_include_volumes,
                'volume_names': list(volume_backup_paths.keys()),
                'include_bind_mounts': should_include_bind_mounts
            }

            logger.info("Backup %s created successfully", backup_name)
            return {
                'success': True,
                'backup_info': backup_info
            }
        except Exception as e:
            logger.exception("Error creating backup: %s", str(e))
            return {
                'success': False,
                'error': str(e)
            }

    def restore_backup(self, backup_name=None, backup_file=None, restore_dbs=True,
                       db_names=None, restore_volumes=True, volume_names=None,
                       restore_bind_mounts=True, dir_names=None):
        """
        استعادة نسخة احتياطية

        Args:
            backup_name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            backup_file (str, optional): مسار ملف النسخة الاحتياطية. Defaults to None.
            restore_dbs (bool, optional): ما إذا كان يجب استعادة قواعد البيانات. Defaults to True.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد استعادتها. Defaults to None.
            restore_volumes (bool, optional): ما إذا كان يجب استعادة Docker Volumes. Defaults to True.
            volume_names (list, optional): قائمة أسماء الـ Volumes المراد استعادتها. Defaults to None.
            restore_bind_mounts (bool, optional): ما إذا كان يجب استعادة Bind Mounts. Defaults to True.
            dir_names (list, optional): قائمة أسماء المجلدات المراد استعادتها. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # التحقق من توفر المعلومات المطلوبة
        if not backup_name and not backup_file:
            raise ValueError("Either backup_name or backup_file must be provided")

        # إذا تم تحديد الاسم فقط، ابحث عن الملف المناسب
        if backup_name and not backup_file:
            for ext in ['gz', 'bz2', 'xz']:
                potential_file = os.path.join(self.config['backup_dir'], "{}.tar.{}".format(backup_name, ext))
                if os.path.exists(potential_file):
                    backup_file = potential_file
                    break

            if not backup_file:
                raise FileNotFoundError("Backup file for {} not found".format(backup_name))

        # إنشاء معرف فريد للمهمة
        task_id = "restore_{}_{}".format(int(time.time.time()), os.urandom(4).hex())

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
                'backup_file': backup_file,
                'restore_dbs': restore_dbs,
                'db_names': db_names,
                'restore_volumes': restore_volumes,
                'volume_names': volume_names,
                'restore_bind_mounts': restore_bind_mounts,
                'dir_names': dir_names
            }
        ))

        return task_info

    def _restore_backup_internal(self, backup_name=None, backup_file=None, restore_dbs=True,
                                 db_names=None, restore_volumes=True, volume_names=None,
                                 restore_bind_mounts=True, dir_names=None):
        """
        التنفيذ الداخلي لاستعادة نسخة احتياطية

        Args:
            backup_name (str, optional): اسم النسخة الاحتياطية. Defaults to None.
            backup_file (str, optional): مسار ملف النسخة الاحتياطية. Defaults to None.
            restore_dbs (bool, optional): ما إذا كان يجب استعادة قواعد البيانات. Defaults to True.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد استعادتها. Defaults to None.
            restore_volumes (bool, optional): ما إذا كان يجب استعادة Docker Volumes. Defaults to True.
            volume_names (list, optional): قائمة أسماء الـ Volumes المراد استعادتها. Defaults to None.
            restore_bind_mounts (bool, optional): ما إذا كان يجب استعادة Bind Mounts. Defaults to True.
            dir_names (list, optional): قائمة أسماء المجلدات المراد استعادتها. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # التحقق من وجود ملف النسخة الاحتياطية
            if not backup_file or not isinstance(backup_file, str) or not os.path.exists(backup_file):
                raise FileNotFoundError("Backup file {} not found".format(backup_file))

            # إنشاء مجلد مؤقت لاستخراج النسخة الاحتياطية
            extract_dir = os.path.join(self.config['temp_dir'], "restore_{}".format(int(time.time())))
            os.makedirs(extract_dir, exist_ok=True)

            # استخراج النسخة الاحتياطية
            logger.info("Extracting backup file %s to %s", backup_file, extract_dir)
            with tarfile.open(backup_file, 'r:*') as tar:
                tar.extractall(path=extract_dir)

            # البحث عن مجلد النسخة الاحتياطية داخل المجلد المستخرج
            backup_dirs = [d for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
            if not backup_dirs:
                raise ValueError("No backup directory found in the extracted files")

            backup_dir = os.path.join(extract_dir, backup_dirs[0])

            # قراءة ملف التكوين
            config_path = os.path.join(backup_dir, BACKUP_CONFIG_FILE)
            if not os.path.exists(config_path):
                raise FileNotFoundError("Backup configuration file not found in {}".format(backup_dir))

            with open(config_path, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)

            # استعادة المجلدات (Bind Mounts)
            if restore_bind_mounts and backup_config.get('include_bind_mounts', False):
                data_dir = os.path.join(backup_dir, 'data')
                if os.path.exists(data_dir):
                    # تحديد المجلدات المراد استعادتها
                    dirs_to_restore = dir_names if dir_names else [os.path.basename(d) for d in backup_config.get('include_dirs', [])]

                    for dir_name in dirs_to_restore:
                        src_dir = os.path.join(data_dir, dir_name)
                        if os.path.exists(src_dir):
                            # البحث عن المجلد المقابل في الإعدادات
                            target_dir = None
                            for path in self.config['data_dirs'].values():
                                if os.path.basename(path) == dir_name:
                                    target_dir = path
                                    break

                            if target_dir:
                                logger.info("Restoring directory %s to %s", src_dir, target_dir)

                                # إنشاء نسخة احتياطية من المجلد الحالي إذا كان موجوداً
                                if os.path.exists(target_dir):
                                    backup_target_dir = "{}_backup_{}".format(target_dir, int(time.time()))
                                    logger.info("Creating backup of existing directory %s to %s", target_dir, backup_target_dir)
                                    shutil.move(target_dir, backup_target_dir)

                                # إنشاء المجلد الهدف إذا لم يكن موجوداً
                                os.makedirs(os.path.dirname(target_dir), exist_ok=True)

                                # نسخ المجلد من النسخة الاحتياطية
                                shutil.copytree(src_dir, target_dir)

            # استعادة قواعد البيانات
            if restore_dbs and backup_config.get('backup_dbs', False):
                db_backup_paths = backup_config.get('db_backup_paths', {})

                # تحديد قواعد البيانات المراد استعادتها
                dbs_to_restore = db_names if db_names else list(db_backup_paths.keys())

                for db_name in dbs_to_restore:
                    if db_name in db_backup_paths and db_name in self.config['db_configs']:
                        db_backup_path = os.path.join(backup_dir, db_backup_paths[db_name])
                        if os.path.exists(db_backup_path):
                            logger.info("Restoring database %s from %s", db_name, db_backup_path)
                            self._restore_database(db_backup_path, self.config['db_configs'][db_name])

            # استعادة Docker Volumes
            if restore_volumes and backup_config.get('include_volumes', False):
                volume_backup_paths = backup_config.get('volume_backup_paths', {})

                # تحديد الـ Volumes المراد استعادتها
                volumes_to_restore = volume_names if volume_names else list(volume_backup_paths.keys())

                for volume_name in volumes_to_restore:
                    if volume_name in volume_backup_paths:
                        volume_backup_path = os.path.join(backup_dir, volume_backup_paths[volume_name])
                        if os.path.exists(volume_backup_path):
                            logger.info("Restoring Docker volume %s from %s", volume_name, volume_backup_path)
                            self._restore_docker_volume(volume_name, volume_backup_path)

            # حذف المجلد المؤقت
            shutil.rmtree(extract_dir)

            # التحقق من وجود ملف النسخة الاحتياطية
            if not backup_file or not isinstance(backup_file, str) or not os.path.exists(backup_file):
                raise FileNotFoundError("Backup file {} not found".format(backup_file))

            # حذف الملف
            os.remove(backup_file)

            # Only call os.path.basename if backup_file is a valid str
            backup_file_name = os.path.basename(backup_file) if backup_file and isinstance(backup_file, str) else ""
            return {
                'success': True,
                'message': "Backup {} restored successfully".format(backup_name or backup_file_name)
            }
        except Exception as e:
            logger.exception("Error restoring backup: %s", str(e))
            return {
                'success': False,
                'error': str(e)
            }

    def export_data(self, target_dir, include_dbs=True, db_names=None, include_volumes=False,
                    volume_names=None, include_dirs=True, dir_names=None):
        """
        تصدير البيانات إلى مجلد خارجي

        Args:
            target_dir (str): المجلد الهدف للتصدير
            include_dbs (bool, optional): ما إذا كان يجب تصدير قواعد البيانات. Defaults to True.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد تصديرها. Defaults to None.
            include_volumes (bool, optional): ما إذا كان يجب تصدير Docker Volumes. Defaults to False.
            volume_names (list, optional): قائمة أسماء الـ Volumes المراد تصديرها. Defaults to None.
            include_dirs (bool, optional): ما إذا كان يجب تصدير المجلدات. Defaults to True.
            dir_names (list, optional): قائمة أسماء المجلدات المراد تصديرها. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # التحقق من وجود المجلد الهدف
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        # إنشاء معرف فريد للمهمة
        task_id = "export_{}_{}".format(int(time.time()), os.urandom(4).hex())

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'export',
            'target_dir': target_dir,
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
            'export_data',
            [],
            {
                'target_dir': target_dir,
                'include_dbs': include_dbs,
                'db_names': db_names,
                'include_volumes': include_volumes,
                'volume_names': volume_names,
                'include_dirs': include_dirs,
                'dir_names': dir_names
            }
        ))

        return task_info

    def _export_data_internal(self, target_dir, include_dbs=True, db_names=None, include_volumes=False,
                              volume_names=None, include_dirs=True, dir_names=None):
        """
        التنفيذ الداخلي لتصدير البيانات إلى مجلد خارجي

        Args:
            target_dir (str): المجلد الهدف للتصدير
            include_dbs (bool, optional): ما إذا كان يجب تصدير قواعد البيانات. Defaults to True.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد تصديرها. Defaults to None.
            include_volumes (bool, optional): ما إذا كان يجب تصدير Docker Volumes. Defaults to False.
            volume_names (list, optional): قائمة أسماء الـ Volumes المراد تصديرها. Defaults to None.
            include_dirs (bool, optional): ما إذا كان يجب تصدير المجلدات. Defaults to True.
            dir_names (list, optional): قائمة أسماء المجلدات المراد تصديرها. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # إنشاء مجلد للتصدير
            export_dir = os.path.join(target_dir, "export_{}".format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
            os.makedirs(export_dir, exist_ok=True)

            exported_items = {
                'databases': [],
                'volumes': [],
                'directories': []
            }

            # تصدير قواعد البيانات
            if include_dbs:
                db_export_dir = os.path.join(export_dir, 'databases')
                os.makedirs(db_export_dir, exist_ok=True)

                # تحديد قواعد البيانات المراد تصديرها
                dbs_to_export = db_names if db_names else list(self.config['db_configs'].keys())

                for db_name in dbs_to_export:
                    if db_name in self.config['db_configs']:
                        db_config = self.config['db_configs'][db_name]
                        db_export_path = os.path.join(db_export_dir, "{}.sql".format(db_name))
                        logger.info("Exporting database %s to %s", db_name, db_export_path)
                        self._backup_database(db_export_path, db_config)
                        exported_items['databases'].append(db_name)

            # تصدير Docker Volumes
            if include_volumes:
                volume_export_dir = os.path.join(export_dir, 'volumes')
                os.makedirs(volume_export_dir, exist_ok=True)

                # تحديد الـ Volumes المراد تصديرها
                volumes_to_export = volume_names if volume_names else self.config['docker']['volumes']

                for volume_name in volumes_to_export:
                    volume_export_path = os.path.join(volume_export_dir, "{}.tar".format(volume_name))
                    logger.info("Exporting Docker volume %s to %s", volume_name, volume_export_path)
                    success = self._backup_docker_volume(volume_name, volume_export_path)
                    if success:
                        exported_items['volumes'].append(volume_name)

            # تصدير المجلدات
            if include_dirs:
                dir_export_dir = os.path.join(export_dir, 'directories')
                os.makedirs(dir_export_dir, exist_ok=True)

                # تحديد المجلدات المراد تصديرها
                dirs_to_export = dir_names if dir_names else list(self.config['data_dirs'].keys())

                for dir_name in dirs_to_export:
                    if dir_name in self.config['data_dirs']:
                        dir_path = self.config['data_dirs'][dir_name]
                        if os.path.exists(dir_path):
                            dir_export_path = os.path.join(dir_export_dir, dir_name)
                            logger.info("Exporting directory %s to %s", dir_path, dir_export_path)
                            shutil.copytree(dir_path, dir_export_path)
                            exported_items['directories'].append(dir_name)

            logger.info("Data exported successfully to %s", export_dir)
            return {
                'success': True,
                'export_dir': export_dir,
                'exported_items': exported_items
            }
        except Exception as e:
            logger.exception("Error exporting data: %s", str(e))
            return {
                'success': False,
                'error': str(e)
            }

    def import_data(self, source_dir, include_dbs=True, db_names=None, include_volumes=False,
                    volume_names=None, include_dirs=True, dir_names=None):
        """
        استيراد البيانات من مجلد خارجي

        Args:
            source_dir (str): المجلد المصدر للاستيراد
            include_dbs (bool, optional): ما إذا كان يجب استيراد قواعد البيانات. Defaults to True.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد استيرادها. Defaults to None.
            include_volumes (bool, optional): ما إذا كان يجب استيراد Docker Volumes. Defaults to False.
            volume_names (list, optional): قائمة أسماء الـ Volumes المراد استيرادها. Defaults to None.
            include_dirs (bool, optional): ما إذا كان يجب استيراد المجلدات. Defaults to True.
            dir_names (list, optional): قائمة أسماء المجلدات المراد استيرادها. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # التحقق من وجود المجلد المصدر
        if not os.path.exists(source_dir):
            raise FileNotFoundError("Source directory {} not found".format(source_dir))

        # إنشاء معرف فريد للمهمة
        task_id = "import_{}_{}".format(int(time.time.time()), os.urandom(4).hex())

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'import',
            'source_dir': source_dir,
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
            'import_data',
            [],
            {
                'source_dir': source_dir,
                'include_dbs': include_dbs,
                'db_names': db_names,
                'include_volumes': include_volumes,
                'volume_names': volume_names,
                'include_dirs': include_dirs,
                'dir_names': dir_names
            }
        ))

        return task_info

    def _import_data_internal(self, source_dir, include_dbs=True, db_names=None, include_volumes=False,
                              volume_names=None, include_dirs=True, dir_names=None):
        """
        التنفيذ الداخلي لاستيراد البيانات من مجلد خارجي

        Args:
            source_dir (str): المجلد المصدر للاستيراد
            include_dbs (bool, optional): ما إذا كان يجب استيراد قواعد البيانات. Defaults to True.
            db_names (list, optional): قائمة أسماء قواعد البيانات المراد استيرادها. Defaults to None.
            include_volumes (bool, optional): ما إذا كان يجب استيراد Docker Volumes. Defaults to False.
            volume_names (list, optional): قائمة أسماء الـ Volumes المراد استيرادها. Defaults to None.
            include_dirs (bool, optional): ما إذا كان يجب استيراد المجلدات. Defaults to True.
            dir_names (list, optional): قائمة أسماء المجلدات المراد استيرادها. Defaults to None.

        Returns:
            dict: نتيجة العملية
        """
        try:
            # التحقق من وجود ملف التكوين
            config_path = os.path.join(source_dir, 'export_config.json')
            if os.path.exists(config_path):
                # Note: The config file exists but we're not using its content in this implementation
                # This could be enhanced in the future to use the config data

                imported_items = {
                    'databases': [],
                    'volumes': [],
                    'directories': []
                }

                # استيراد قواعد البيانات
                if include_dbs:
                    db_import_dir = os.path.join(source_dir, 'databases')
                    if os.path.exists(db_import_dir):
                        # تحديد قواعد البيانات المراد استيرادها
                        available_dbs = [os.path.splitext(f)[0] for f in os.listdir(db_import_dir) if f.endswith('.sql')]
                        dbs_to_import = db_names if db_names else available_dbs

                        for db_name in dbs_to_import:
                            if db_name in self.config['db_configs'] and db_name in available_dbs:
                                db_import_path = os.path.join(db_import_dir, "{}.sql".format(db_name))
                                if os.path.exists(db_import_path):
                                    logger.info("Importing database %s from %s", db_name, db_import_path)
                                    self._restore_database(db_import_path, self.config['db_configs'][db_name])
                                    imported_items['databases'].append(db_name)

                # استيراد المجلدات
                if include_dirs:
                    dir_import_dir = os.path.join(source_dir, 'directories')
                    if os.path.exists(dir_import_dir):
                        # تحديد المجلدات المراد استيرادها
                        available_dirs = [d for d in os.listdir(dir_import_dir) if os.path.isdir(os.path.join(dir_import_dir, d))]
                        dirs_to_import = dir_names if dir_names else available_dirs

                        for dir_name in dirs_to_import:
                            if dir_name in self.config['data_dirs'] and dir_name in available_dirs:
                                dir_import_path = os.path.join(dir_import_dir, dir_name)
                                target_dir = self.config['data_dirs'][dir_name]

                                if os.path.exists(dir_import_path):
                                    logger.info("Importing directory %s from %s to %s", dir_name, dir_import_path, target_dir)

                                    # إنشاء نسخة احتياطية من المجلد الحالي إذا كان موجوداً
                                    if os.path.exists(target_dir):
                                        backup_target_dir = "{}_backup_{}".format(target_dir, int(time.time()))
                                        logger.info("Creating backup of existing directory %s to %s", target_dir, backup_target_dir)
                                        shutil.move(target_dir, backup_target_dir)

                                    # إنشاء المجلد الهدف إذا لم يكن موجوداً
                                    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

                                    # نسخ المجلد من المصدر
                                    shutil.copytree(dir_import_path, target_dir)
                                    imported_items['directories'].append(dir_name)

                logger.info("Data imported successfully from %s", source_dir)
                return {
                    'success': True,
                    'imported_items': imported_items
                }
            else:
                raise FileNotFoundError(f"Export configuration file not found in {source_dir}")
        except Exception as e:
            logger.exception("Error importing data: %s", str(e))
            return {
                'success': False,
                'error': str(e)
            }

    def _copy_directory(self, src, dst, exclude_patterns=None, include_txt_md=False):
        """
        نسخ مجلد مع استبعاد أنماط محددة

        Args:
            src (str): المجلد المصدر
            dst (str): المجلد الهدف
            exclude_patterns (list, optional): قائمة أنماط الملفات المراد استبعادها. Defaults to None.
            include_txt_md (bool, optional): ما إذا كان يجب تضمين جميع ملفات .txt و .md. Defaults to False.
        """
        exclude_patterns = exclude_patterns or []
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            should_exclude = any(Path(s).match(pattern) for pattern in exclude_patterns)
            if include_txt_md and (s.endswith('.txt') or s.endswith('.md')):
                should_exclude = False
            if should_exclude:
                logger.debug("Skipping %s due to exclude pattern", s)
                continue
            if os.path.isdir(s):
                self._copy_directory(s, d, exclude_patterns, include_txt_md)
            else:
                shutil.copy2(s, d)

    def _backup_database(self, output_file, db_config):
        """
        نسخ قاعدة البيانات
        Args:
            output_file (str): مسار ملف الإخراج
            db_config (dict): إعدادات قاعدة البيانات
        Raises:
            Exception: في حالة فشل النسخ
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        env = os.environ.copy()
        if db_config.get('password'):
            env['PGPASSWORD'] = db_config['password']
        cmd = [
            'pg_dump',
            '-h', db_config.get('host', 'localhost'),
            '-p', str(db_config.get('port', 5432)),
            '-U', db_config.get('user', 'postgres'),
            '-d', db_config.get('database'),
            '-f', output_file,
            '--format=p'
        ]
        logger.info("Running command: %s", ' '.join(cmd))
        process = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if process.returncode != 0:
            error_message = process.stderr.decode('utf-8')
            raise Exception(f"Database backup failed: {error_message}")

    def _backup_docker_volume(self, volume_name, output_file):
        """
        نسخ Docker Volume
        Args:
            volume_name (str): اسم الـ Volume
            output_file (str): مسار ملف الإخراج
        Returns:
            bool: نجاح العملية
        """
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            cmd = [
                'docker', 'run', '--rm',
                '-v', f"{volume_name}:/source",
                '-v', f"{os.path.dirname(os.path.abspath(output_file))}:/backup",
                'alpine', 'tar', 'cf', f"/backup/{os.path.basename(output_file)}", '-C', '/source', '.'
            ]
            logger.info("Running command: %s", ' '.join(cmd))
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if process.returncode != 0:
                error_message = process.stderr.decode('utf-8')
                logger.error("Docker volume backup failed: %s", error_message)
                return False
            return True
        except Exception as e:
            logger.exception("Error backing up Docker volume: %s", str(e))
            return False

    def _cleanup_old_backups(self):
        """
        حذف النسخ الاحتياطية القديمة إذا تجاوز عددها الحد المسموح به
        """
        backups = self.get_backups()
        if len(backups) > self.config['max_backups']:
            backups.sort(key=lambda x: x['created_at'])
            for backup in backups[:len(backups) - self.config['max_backups']]:
                file_path = backup['file_path']
                logger.info("Removing old backup %s", file_path)
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning("Error removing old backup %s: %s", file_path, str(e))

    def _restore_database(self, input_file, db_config):
        """
        استعادة قاعدة البيانات
        Args:
            input_file (str): مسار ملف النسخة الاحتياطية
            db_config (dict): إعدادات قاعدة البيانات
        Raises:
            Exception: في حالة فشل الاستعادة
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Database backup file {input_file} not found")
        env = os.environ.copy()
        if db_config.get('password'):
            env['PGPASSWORD'] = db_config['password']
        cmd = [
            'psql',
            '-h', db_config.get('host', 'localhost'),
            '-p', str(db_config.get('port', 5432)),
            '-U', db_config.get('user', 'postgres'),
            '-d', db_config.get('database'),
            '-f', input_file
        ]
        logger.info("Running command: %s", ' '.join(cmd))
        process = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if process.returncode != 0:
            error_message = process.stderr.decode('utf-8')
            raise Exception(f"Database restore failed: {error_message}")

    def _restore_docker_volume(self, volume_name, input_file):
        """
        استعادة Docker Volume
        Args:
            volume_name (str): اسم الـ Volume
            input_file (str): مسار ملف النسخة الاحتياطية
        Returns:
            bool: نجاح العملية
        """
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Docker volume backup file {input_file} not found")
            cmd_create = ['docker', 'volume', 'create', volume_name]
            subprocess.run(cmd_create, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            cmd = [
                'docker', 'run', '--rm',
                '-v', f"{volume_name}:/target",
                '-v', f"{os.path.dirname(os.path.abspath(input_file))}:/backup",
                'alpine', 'sh', '-c', f"rm -rf /target/* && tar xf /backup/{os.path.basename(input_file)} -C /target"
            ]
            logger.info("Running command: %s", ' '.join(cmd))
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if process.returncode != 0:
                error_message = process.stderr.decode('utf-8')
                logger.error("Docker volume restore failed: %s", error_message)
                return False
            return True
        except Exception as e:
            logger.exception("Error restoring Docker volume: %s", str(e))
            return False

    def get_backups(self):
        """
        الحصول على قائمة النسخ الاحتياطية المتوفرة

        Returns:
            list: قائمة النسخ الاحتياطية
        """
        backups = []
        for file_name in os.listdir(self.config['backup_dir']):
            file_path = os.path.join(self.config['backup_dir'], file_name)
            if os.path.isfile(file_path) and any(file_name.endswith(f".tar.{ext}") for ext in ['gz', 'bz2', 'xz']):
                try:
                    backup_name = file_name.split('.tar.')[0]
                    backup_info = {
                        'name': backup_name,
                        'file_path': file_path,
                        'file_size': os.path.getsize(file_path),
                        'created_at': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                    }
                    try:
                        with tarfile.open(file_path, 'r:*') as tar:
                            config_file = None
                            for member in tar.getmembers():
                                if member.name.endswith(BACKUP_CONFIG_FILE):
                                    config_file = member
                                    break
                            if config_file:
                                extracted = tar.extractfile(config_file)
                                if extracted is not None:
                                    config_data = extracted.read().decode('utf-8')
                                    config = json.loads(config_data)
                                    backup_info.update({
                                        'description': config.get('description'),
                                        'created_at': config.get('created_at', backup_info['created_at']),
                                        'include_dirs': config.get('include_dirs', []),
                                        'backup_dbs': config.get('backup_dbs', False),
                                        'db_names': list(config.get('db_backup_paths', {}).keys()),
                                        'include_volumes': config.get('include_volumes', False),
                                        'volume_names': list(config.get('volume_backup_paths', {}).keys()),
                                        'include_bind_mounts': config.get('include_bind_mounts', False)
                                    })
                                else:
                                    logger.warning("Could not extract config file from %s: extractfile returned None", file_path)
                    except Exception as e:
                        logger.warning("Error extracting config from %s: %s", file_path, str(e))
                    backups.append(backup_info)
                except Exception as e:
                    logger.warning("Error processing backup file %s: %s", file_path, str(e))
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        return backups
