# File:
# /home/ubuntu/ai_web_organized/src/modules/data_validation/validation_service.py
"""
from flask import g
خدمة التحقق من صحة البيانات
توفر هذه الوحدة خدمات للتحقق من صحة البيانات وتنظيفها وإصلاحها
"""

import datetime
import json
import logging
import os
import queue
import re
import threading
import time

import pandas as pd

# import numpy as np  # Removed: unused import
# from pathlib import Path  # Removed: unused import
# from typing import Dict, List, Any, Union, Optional, Tuple  # Removed:
# unused imports

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_validation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ValidationService:
    """خدمة التحقق من صحة البيانات"""

    def __init__(self, config=None):
        """
        تهيئة خدمة التحقق من صحة البيانات

        Args:
            config (dict, optional): إعدادات التحقق من صحة البيانات. Defaults to None.
        """
        # الإعدادات الافتراضية
        self.default_config = {
            'validation_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'validations'),
            'temp_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp'),
            'max_validations': 50,
            'validation_rules': {},
            'auto_fix': False,
            'notification_threshold': 0.8,  # نسبة الأخطاء التي تتطلب إشعاراً
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

        # التأكد من وجود مجلدات التحقق والمؤقت
        os.makedirs(self.config['validation_dir'], exist_ok=True)
        os.makedirs(self.config['temp_dir'], exist_ok=True)

        # قائمة العمليات الجارية
        self.running_tasks = {}
        self.task_queue = queue.Queue()
        self.worker_thread = None

        # قواعد التحقق الافتراضية
        self._load_default_validation_rules()

        # بدء خيط العمل
        self._start_worker()

    def _load_default_validation_rules(self):
        """تحميل قواعد التحقق الافتراضية"""
        default_rules = {
            'general': {
                'required_fields': {
                    'description': 'التحقق من وجود الحقول المطلوبة',
                    'severity': 'error',
                    'auto_fixable': False
                },
                'data_types': {
                    'description': 'التحقق من أنواع البيانات',
                    'severity': 'error',
                    'auto_fixable': False
                },
                'value_ranges': {
                    'description': 'التحقق من نطاقات القيم',
                    'severity': 'warning',
                    'auto_fixable': True
                },
                'duplicates': {
                    'description': 'التحقق من البيانات المكررة',
                    'severity': 'warning',
                    'auto_fixable': True
                }
            },
            'users': {
                'email_format': {
                    'description': 'التحقق من صيغة البريد الإلكتروني',
                    'severity': 'error',
                    'auto_fixable': False,
                    'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                },
                'username_format': {
                    'description': 'التحقق من صيغة اسم المستخدم',
                    'severity': 'error',
                    'auto_fixable': False,
                    'pattern': r'^[a-zA-Z0-9_]{3,20}$'
                },
                'password_strength': {
                    'description': 'التحقق من قوة كلمة المرور',
                    'severity': 'warning',
                    'auto_fixable': False,
                    'min_length': 8,
                    'require_uppercase': True,
                    'require_lowercase': True,
                    'require_digit': True,
                    'require_special': True
                }
            },
            'products': {
                'sku_format': {
                    'description': 'التحقق من صيغة رمز المنتج',
                    'severity': 'error',
                    'auto_fixable': False,
                    'pattern': r'^[A-Z0-9]{6,10}$'
                },
                'price_range': {
                    'description': 'التحقق من نطاق السعر',
                    'severity': 'warning',
                    'auto_fixable': True,
                    'min': 0,
                    'max': 1000000
                },
                'stock_range': {
                    'description': 'التحقق من نطاق المخزون',
                    'severity': 'warning',
                    'auto_fixable': True,
                    'min': 0,
                    'max': 1000000
                }
            },
            'plants': {
                'scientific_name_format': {
                    'description': 'التحقق من صيغة الاسم العلمي',
                    'severity': 'warning',
                    'auto_fixable': False,
                    'pattern': r'^[A-Z][a-z]+ [a-z]+$'
                },
                'growth_days_range': {
                    'description': 'التحقق من نطاق أيام النمو',
                    'severity': 'warning',
                    'auto_fixable': True,
                    'min': 1,
                    'max': 365
                },
                'temperature_range': {
                    'description': 'التحقق من نطاق درجة الحرارة',
                    'severity': 'warning',
                    'auto_fixable': True,
                    'min': -10,
                    'max': 50
                }
            }
        }

        # دمج القواعد الافتراضية مع القواعد المخصصة
        if not self.config['validation_rules']:
            self.config['validation_rules'] = default_rules
        else:
            for category, rules in default_rules.items():
                if category not in self.config['validation_rules']:
                    self.config['validation_rules'][category] = rules
                else:
                    for rule_name, rule_config in rules.items():
                        if rule_name not in self.config['validation_rules'][category]:
                            self.config['validation_rules'][category][rule_name] = rule_config

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
                    if task_type == 'validate_data':
                        result = self._validate_data_internal(*args, **kwargs)
                    elif task_type == 'fix_data':
                        result = self._fix_data_internal(*args, **kwargs)
                    elif task_type == 'validate_database':
                        result = self._validate_database_internal(
                            *args, **kwargs)
                    else:
                        result = {'success': False,
                                  'error': f'Unknown task type: {task_type}'}

                    # تحديث حالة المهمة بالنتيجة
                    self.running_tasks[task_id].update({
                        'status': 'completed',
                        'completed_at': datetime.datetime.now().isoformat(),
                        'result': result
                    })
                except Exception as e:
                    logger.exception(
                        f"Error processing task {task_id}: {str(e)}")
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

    def validate_data(
            self,
            data=None,
            data_file=None,
            data_type=None,
            rules=None):
        """
        التحقق من صحة البيانات

        Args:
            data (dict or list, optional): البيانات المراد التحقق منها. Defaults to None.
            data_file (str, optional): مسار ملف البيانات. Defaults to None.
            data_type (str, optional): نوع البيانات. Defaults to None.
            rules (dict, optional): قواعد التحقق المخصصة. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # التحقق من توفر البيانات
        if data is None and data_file is None:
            raise ValueError("Either data or data_file must be provided")

        # إنشاء معرف فريد للمهمة
        task_id = f"validate_{int(time.time())}_{os.urandom(4).hex()}"

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'validation',
            'data_type': data_type,
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
            'validate_data',
            [],
            {
                'data': data,
                'data_file': data_file,
                'data_type': data_type,
                'rules': rules
            }
        ))

        return task_info

    def _validate_data_internal(
            self,
            data=None,
            data_file=None,
            data_type=None,
            rules=None):
        """
        التنفيذ الداخلي للتحقق من صحة البيانات

        Args:
            data (dict or list, optional): البيانات المراد التحقق منها. Defaults to None.
            data_file (str, optional): مسار ملف البيانات. Defaults to None.
            data_type (str, optional): نوع البيانات. Defaults to None.
            rules (dict, optional): قواعد التحقق المخصصة. Defaults to None.

        Returns:
            dict: نتيجة التحقق
        """
        try:
            # تحميل البيانات من الملف إذا تم تحديده
            if data is None and data_file is not None:
                data = self._load_data_from_file(data_file)

            # تحديد نوع البيانات إذا لم يتم تحديده
            if data_type is None:
                data_type = self._detect_data_type(data)

            # تحديد قواعد التحقق
            validation_rules = rules or self._get_validation_rules(data_type)

            # التحقق من صحة البيانات
            validation_results = self._validate_with_rules(
                data, validation_rules)

            # حفظ نتائج التحقق
            validation_file = os.path.join(
                self.config['validation_dir'],
                f"validation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

            with open(validation_file, 'w', encoding='utf-8') as f:
                json.dump(validation_results, f, ensure_ascii=False, indent=2)

            # إنشاء ملخص النتائج
            summary = self._create_validation_summary(validation_results)

            return {
                'success': True,
                'validation_file': validation_file,
                'summary': summary
            }
        except Exception as e:
            logger.exception(f"Error validating data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def fix_data(
            self,
            validation_id=None,
            validation_file=None,
            auto_fix=None):
        """
        إصلاح البيانات بناءً على نتائج التحقق

        Args:
            validation_id (str, optional): معرف مهمة التحقق. Defaults to None.
            validation_file (str, optional): مسار ملف نتائج التحقق. Defaults to None.
            auto_fix (bool, optional): ما إذا كان يجب إصلاح الأخطاء تلقائياً. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # التحقق من توفر معلومات التحقق
        if validation_id is None and validation_file is None:
            raise ValueError(
                "Either validation_id or validation_file must be provided")

        # إنشاء معرف فريد للمهمة
        task_id = f"fix_{int(time.time())}_{os.urandom(4).hex()}"

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'fix',
            'validation_id': validation_id,
            'validation_file': validation_file,
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
            'fix_data',
            [],
            {
                'validation_id': validation_id,
                'validation_file': validation_file,
                'auto_fix': auto_fix
            }
        ))

        return task_info

    def _fix_data_internal(
            self,
            validation_id=None,
            validation_file=None,
            auto_fix=None):
        """
        التنفيذ الداخلي لإصلاح البيانات

        Args:
            validation_id (str, optional): معرف مهمة التحقق. Defaults to None.
            validation_file (str, optional): مسار ملف نتائج التحقق. Defaults to None.
            auto_fix (bool, optional): ما إذا كان يجب إصلاح الأخطاء تلقائياً. Defaults to None.

        Returns:
            dict: نتيجة الإصلاح
        """
        try:
            # تحديد ملف نتائج التحقق
            if validation_file is None and validation_id is not None:
                validation_task = self.running_tasks.get(validation_id)
                if validation_task and validation_task['result'] and validation_task['result'].get(
                        'validation_file'):
                    validation_file = validation_task['result']['validation_file']
                else:
                    raise ValueError(
                        f"Validation file not found for task {validation_id}")

            # التحقق من وجود ملف نتائج التحقق
            if not os.path.exists(validation_file):
                raise FileNotFoundError(
                    f"Validation file {validation_file} not found")

            # تحميل نتائج التحقق
            with open(validation_file, 'r', encoding='utf-8') as f:
                validation_results = json.load(f)

            # تحديد ما إذا كان يجب إصلاح الأخطاء تلقائياً
            should_auto_fix = auto_fix if auto_fix is not None else self.config['auto_fix']

            # إصلاح البيانات
            fix_results = self._fix_data_with_results(
                validation_results, should_auto_fix)

            # حفظ نتائج الإصلاح
            fix_file = os.path.join(
                self.config['validation_dir'],
                f"fix_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            with open(fix_file, 'w', encoding='utf-8') as f:
                json.dump(fix_results, f, ensure_ascii=False, indent=2)

            # إنشاء ملخص النتائج
            summary = self._create_fix_summary(fix_results)

            return {
                'success': True,
                'fix_file': fix_file,
                'summary': summary
            }
        except Exception as e:
            logger.exception(f"Error fixing data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def validate_database(self, tables=None, rules=None):
        """
        التحقق من صحة قاعدة البيانات

        Args:
            tables (list, optional): قائمة الجداول المراد التحقق منها. Defaults to None.
            rules (dict, optional): قواعد التحقق المخصصة. Defaults to None.

        Returns:
            dict: معلومات المهمة
        """
        # إنشاء معرف فريد للمهمة
        task_id = f"validate_db_{int(time.time())}_{os.urandom(4).hex()}"

        # إنشاء معلومات المهمة
        task_info = {
            'id': task_id,
            'type': 'db_validation',
            'tables': tables,
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
            'validate_database',
            [],
            {
                'tables': tables,
                'rules': rules
            }
        ))

        return task_info

    def _validate_database_internal(self, tables=None, rules=None):
        """
        التنفيذ الداخلي للتحقق من صحة قاعدة البيانات

        Args:
            tables (list, optional): قائمة الجداول المراد التحقق منها. Defaults to None.
            rules (dict, optional): قواعد التحقق المخصصة. Defaults to None.

        Returns:
            dict: نتيجة التحقق
        """
        try:
            # تنفيذ التحقق من صحة قاعدة البيانات
            # هذه مجرد محاكاة، يجب تنفيذ الاتصال الفعلي بقاعدة البيانات

            # إنشاء نتائج التحقق
            validation_results = {
                'database': self.config['db_config']['database'],
                'tables': {},
                'timestamp': datetime.datetime.now().isoformat()
            }

            # حفظ نتائج التحقق
            validation_file = os.path.join(
                self.config['validation_dir'],
                f"db_validation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

            with open(validation_file, 'w', encoding='utf-8') as f:
                json.dump(validation_results, f, ensure_ascii=False, indent=2)

            # إنشاء ملخص النتائج
            summary = {
                'database': self.config['db_config']['database'],
                'tables_checked': 0,
                'tables_with_errors': 0,
                'total_errors': 0,
                'total_warnings': 0
            }

            return {
                'success': True,
                'validation_file': validation_file,
                'summary': summary
            }
        except Exception as e:
            logger.exception(f"Error validating database: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

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

    def get_validation_results(self, validation_id=None, validation_file=None):
        """
        الحصول على نتائج التحقق

        Args:
            validation_id (str, optional): معرف مهمة التحقق. Defaults to None.
            validation_file (str, optional): مسار ملف نتائج التحقق. Defaults to None.

        Returns:
            dict: نتائج التحقق
        """
        try:
            # تحديد ملف نتائج التحقق
            if validation_file is None and validation_id is not None:
                validation_task = self.running_tasks.get(validation_id)
                if validation_task and validation_task['result'] and validation_task['result'].get(
                        'validation_file'):
                    validation_file = validation_task['result']['validation_file']
                else:
                    raise ValueError(
                        f"Validation file not found for task {validation_id}")

            # التحقق من وجود ملف نتائج التحقق
            if not os.path.exists(validation_file):
                raise FileNotFoundError(
                    f"Validation file {validation_file} not found")

            # تحميل نتائج التحقق
            with open(validation_file, 'r', encoding='utf-8') as f:
                validation_results = json.load(f)

            return validation_results
        except Exception as e:
            logger.exception(f"Error getting validation results: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_validations(self):
        """
        الحصول على قائمة عمليات التحقق المتوفرة

        Returns:
            list: قائمة عمليات التحقق
        """
        validations = []

        # البحث عن ملفات نتائج التحقق
        for file_name in os.listdir(self.config['validation_dir']):
            file_path = os.path.join(self.config['validation_dir'], file_name)

            # التحقق من أن الملف هو ملف نتائج تحقق
            if os.path.isfile(file_path) and file_name.startswith(
                    'validation_') and file_name.endswith('.json'):
                try:
                    # تحميل ملف نتائج التحقق
                    with open(file_path, 'r', encoding='utf-8') as f:
                        validation_results = json.load(f)

                    # إنشاء معلومات التحقق
                    validation_info = {
                        'id': file_name.replace(
                            'validation_',
                            '').replace(
                            '.json',
                            ''),
                        'file_path': file_path,
                        'file_size': os.path.getsize(file_path),
                        'created_at': datetime.datetime.fromtimestamp(
                            os.path.getctime(file_path)).isoformat()}

                    # إضافة معلومات إضافية من نتائج التحقق
                    if isinstance(validation_results, dict):
                        validation_info.update({
                            'data_type': validation_results.get('data_type'),
                            'summary': validation_results.get('summary')
                        })

                    validations.append(validation_info)
                except Exception as e:
                    logger.warning(
                        f"Error processing validation file {file_path}: {str(e)}")

        # ترتيب عمليات التحقق حسب تاريخ الإنشاء (الأحدث أولاً)
        validations.sort(key=lambda x: x['created_at'], reverse=True)

        return validations

    def update_config(self, new_config):
        """
        تحديث إعدادات التحقق من صحة البيانات

        Args:
            new_config (dict): الإعدادات الجديدة

        Returns:
            dict: الإعدادات المحدثة
        """
        # تحديث الإعدادات
        self.config.update(new_config)

        # التأكد من وجود مجلدات التحقق والمؤقت
        os.makedirs(self.config['validation_dir'], exist_ok=True)
        os.makedirs(self.config['temp_dir'], exist_ok=True)

        return self.config

    def get_config(self):
        """
        الحصول على إعدادات التحقق من صحة البيانات الحالية

        Returns:
            dict: الإعدادات الحالية
        """
        return self.config

    def get_validation_rules(self, data_type=None):
        """
        الحصول على قواعد التحقق

        Args:
            data_type (str, optional): نوع البيانات. Defaults to None.

        Returns:
            dict: قواعد التحقق
        """
        if data_type:
            return self.config['validation_rules'].get(data_type, {})
        else:
            return self.config['validation_rules']

    def update_validation_rules(self, data_type, rules):
        """
        تحديث قواعد التحقق

        Args:
            data_type (str): نوع البيانات
            rules (dict): قواعد التحقق الجديدة

        Returns:
            dict: قواعد التحقق المحدثة
        """
        # تحديث قواعد التحقق
        if data_type not in self.config['validation_rules']:
            self.config['validation_rules'][data_type] = rules
        else:
            self.config['validation_rules'][data_type].update(rules)

        return self.config['validation_rules'][data_type]

    def _load_data_from_file(self, file_path):
        """
        تحميل البيانات من ملف

        Args:
            file_path (str): مسار الملف

        Returns:
            dict or list: البيانات المحملة
        """
        # التحقق من وجود الملف
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        # تحديد نوع الملف
        file_ext = os.path.splitext(file_path)[1].lower()

        # تحميل البيانات حسب نوع الملف
        if file_ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif file_ext in ['.csv', '.tsv']:
            separator = ',' if file_ext == '.csv' else '\t'
            return pd.read_csv(file_path, sep=separator).to_dict('records')
        elif file_ext in ['.xls', '.xlsx']:
            return pd.read_excel(file_path).to_dict('records')
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def _detect_data_type(self, data):
        """
        اكتشاف نوع البيانات

        Args:
            data (dict or list): البيانات

        Returns:
            str: نوع البيانات
        """
        # التحقق من نوع البيانات
        if isinstance(data, list) and len(data) > 0:
            # التحقق من الحقول الموجودة في البيانات
            sample = data[0]

            if 'email' in sample and 'username' in sample:
                return 'users'
            elif 'sku' in sample and 'price' in sample:
                return 'products'
            elif 'scientific_name' in sample and 'growth_days' in sample:
                return 'plants'

        # إرجاع النوع العام إذا لم يتم التعرف على نوع محدد
        return 'general'

    def _get_validation_rules(self, data_type):
        """
        الحصول على قواعد التحقق لنوع بيانات محدد

        Args:
            data_type (str): نوع البيانات

        Returns:
            dict: قواعد التحقق
        """
        # الحصول على قواعد التحقق لنوع البيانات المحدد
        rules = self.config['validation_rules'].get(data_type, {})

        # إضافة قواعد التحقق العامة
        general_rules = self.config['validation_rules'].get('general', {})

        # دمج القواعد
        merged_rules = general_rules.copy()
        merged_rules.update(rules)

        return merged_rules

    def _validate_with_rules(self, data, rules):
        """
        التحقق من صحة البيانات باستخدام قواعد محددة

        Args:
            data (dict or list): البيانات
            rules (dict): قواعد التحقق

        Returns:
            dict: نتائج التحقق
        """
        # إنشاء نتائج التحقق
        validation_results = {
            'data_type': self._detect_data_type(data),
            'timestamp': datetime.datetime.now().isoformat(),
            'total_records': len(data) if isinstance(data, list) else 1,
            'errors': [],
            'warnings': [],
            'summary': {}
        }

        # التحقق من صحة البيانات
        if isinstance(data, list):
            for i, record in enumerate(data):
                record_errors = []
                record_warnings = []

                # تطبيق قواعد التحقق على السجل
                for rule_name, rule_config in rules.items():
                    result = self._apply_rule(record, rule_name, rule_config)

                    if result:
                        if rule_config.get('severity') == 'error':
                            record_errors.append({
                                'rule': rule_name,
                                'message': result,
                                'auto_fixable': rule_config.get('auto_fixable', False)
                            })
                        else:
                            record_warnings.append({
                                'rule': rule_name,
                                'message': result,
                                'auto_fixable': rule_config.get('auto_fixable', False)
                            })

                # إضافة الأخطاء والتحذيرات إلى النتائج
                if record_errors:
                    validation_results['errors'].append({
                        'index': i,
                        'record': record,
                        'errors': record_errors
                    })

                if record_warnings:
                    validation_results['warnings'].append({
                        'index': i,
                        'record': record,
                        'warnings': record_warnings
                    })
        else:
            # تطبيق قواعد التحقق على البيانات
            for rule_name, rule_config in rules.items():
                result = self._apply_rule(data, rule_name, rule_config)

                if result:
                    if rule_config.get('severity') == 'error':
                        validation_results['errors'].append({
                            'rule': rule_name,
                            'message': result,
                            'auto_fixable': rule_config.get('auto_fixable', False)
                        })
                    else:
                        validation_results['warnings'].append({
                            'rule': rule_name,
                            'message': result,
                            'auto_fixable': rule_config.get('auto_fixable', False)
                        })

        # إنشاء ملخص النتائج
        validation_results['summary'] = self._create_validation_summary(
            validation_results)

        return validation_results

    def _apply_rule(self, record, rule_name, rule_config):
        """
        تطبيق قاعدة تحقق على سجل

        Args:
            record (dict): السجل
            rule_name (str): اسم القاعدة
            rule_config (dict): تكوين القاعدة

        Returns:
            str or None: رسالة الخطأ أو None إذا كان السجل صحيحاً
        """
        # تطبيق القاعدة حسب نوعها
        if rule_name == 'required_fields':
            # التحقق من وجود الحقول المطلوبة
            required_fields = rule_config.get('fields', [])
            missing_fields = [
                field for field in required_fields if field not in record]

            if missing_fields:
                return f"Missing required fields: {', '.join(missing_fields)}"

        elif rule_name == 'data_types':
            # التحقق من أنواع البيانات
            field_types = rule_config.get('field_types', {})
            type_errors = []

            for field, expected_type in field_types.items():
                if field in record:
                    value = record[field]

                    if expected_type == 'string' and not isinstance(
                            value, str):
                        type_errors.append(f"{field} should be a string")
                    elif expected_type == 'number' and not isinstance(value, (int, float)):
                        type_errors.append(f"{field} should be a number")
                    elif expected_type == 'boolean' and not isinstance(value, bool):
                        type_errors.append(f"{field} should be a boolean")
                    elif expected_type == 'array' and not isinstance(value, list):
                        type_errors.append(f"{field} should be an array")
                    elif expected_type == 'object' and not isinstance(value, dict):
                        type_errors.append(f"{field} should be an object")

            if type_errors:
                return '; '.join(type_errors)

        elif rule_name == 'value_ranges':
            # التحقق من نطاقات القيم
            field_ranges = rule_config.get('field_ranges', {})
            range_errors = []

            for field, range_config in field_ranges.items():
                if field in record:
                    value = record[field]

                    if isinstance(value, (int, float)):
                        min_value = range_config.get('min')
                        max_value = range_config.get('max')

                        if min_value is not None and value < min_value:
                            range_errors.append(
                                f"{field} should be at least {min_value}")

                        if max_value is not None and value > max_value:
                            range_errors.append(
                                f"{field} should be at most {max_value}")

            if range_errors:
                return '; '.join(range_errors)

        elif rule_name == 'duplicates':
            # التحقق من البيانات المكررة
            # هذه القاعدة تتطلب معرفة جميع السجلات، لذا يتم تنفيذها بشكل منفصل
            pass

        elif rule_name == 'email_format':
            # التحقق من صيغة البريد الإلكتروني
            if 'email' in record:
                email = record['email']
                pattern = rule_config.get(
                    'pattern', r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

                if not re.match(pattern, email):
                    return f"Invalid email format: {email}"

        elif rule_name == 'username_format':
            # التحقق من صيغة اسم المستخدم
            if 'username' in record:
                username = record['username']
                pattern = rule_config.get('pattern', r'^[a-zA-Z0-9_]{3,20}$')

                if not re.match(pattern, username):
                    return f"Invalid username format: {username}"

        elif rule_name == 'password_strength':
            # التحقق من قوة كلمة المرور
            if 'password' in record:
                password = record['password']
                min_length = rule_config.get('min_length', 8)
                require_uppercase = rule_config.get('require_uppercase', True)
                require_lowercase = rule_config.get('require_lowercase', True)
                require_digit = rule_config.get('require_digit', True)
                require_special = rule_config.get('require_special', True)

                errors = []

                if len(password) < min_length:
                    errors.append(
                        f"Password should be at least {min_length} characters long")

                if require_uppercase and not any(
                        c.isupper() for c in password):
                    errors.append(
                        "Password should contain at least one uppercase letter")

                if require_lowercase and not any(
                        c.islower() for c in password):
                    errors.append(
                        "Password should contain at least one lowercase letter")

                if require_digit and not any(c.isdigit() for c in password):
                    errors.append("Password should contain at least one digit")

                if require_special and not any(
                        c in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for c in password):
                    errors.append(
                        "Password should contain at least one special character")

                if errors:
                    return '; '.join(errors)

        elif rule_name == 'sku_format':
            # التحقق من صيغة رمز المنتج
            if 'sku' in record:
                sku = record['sku']
                pattern = rule_config.get('pattern', r'^[A-Z0-9]{6,10}$')

                if not re.match(pattern, sku):
                    return f"Invalid SKU format: {sku}"

        elif rule_name == 'price_range':
            # التحقق من نطاق السعر
            if 'price' in record:
                price = record['price']
                min_price = rule_config.get('min', 0)
                max_price = rule_config.get('max', 1000000)

                if price < min_price:
                    return f"Price should be at least {min_price}"

                if price > max_price:
                    return f"Price should be at most {max_price}"

        elif rule_name == 'stock_range':
            # التحقق من نطاق المخزون
            if 'stock' in record:
                stock = record['stock']
                min_stock = rule_config.get('min', 0)
                max_stock = rule_config.get('max', 1000000)

                if stock < min_stock:
                    return f"Stock should be at least {min_stock}"

                if stock > max_stock:
                    return f"Stock should be at most {max_stock}"

        elif rule_name == 'scientific_name_format':
            # التحقق من صيغة الاسم العلمي
            if 'scientific_name' in record:
                scientific_name = record['scientific_name']
                pattern = rule_config.get('pattern', r'^[A-Z][a-z]+ [a-z]+$')

                if not re.match(pattern, scientific_name):
                    return f"Invalid scientific name format: {scientific_name}"

        elif rule_name == 'growth_days_range':
            # التحقق من نطاق أيام النمو
            if 'growth_days' in record:
                growth_days = record['growth_days']
                min_days = rule_config.get('min', 1)
                max_days = rule_config.get('max', 365)

                if growth_days < min_days:
                    return f"Growth days should be at least {min_days}"

                if growth_days > max_days:
                    return f"Growth days should be at most {max_days}"

        elif rule_name == 'temperature_range':
            # التحقق من نطاق درجة الحرارة
            if 'temperature' in record:
                temperature = record['temperature']
                min_temp = rule_config.get('min', -10)
                max_temp = rule_config.get('max', 50)

                if temperature < min_temp:
                    return f"Temperature should be at least {min_temp}"

                if temperature > max_temp:
                    return f"Temperature should be at most {max_temp}"

        # لا توجد أخطاء
        return None

    def _create_validation_summary(self, validation_results):
        """
        إنشاء ملخص نتائج التحقق

        Args:
            validation_results (dict): نتائج التحقق

        Returns:
            dict: ملخص النتائج
        """
        # إنشاء ملخص النتائج
        summary = {
            'total_records': validation_results.get(
                'total_records', 0), 'records_with_errors': len(
                validation_results.get(
                    'errors', [])), 'records_with_warnings': len(
                    validation_results.get(
                        'warnings', [])), 'total_errors': sum(
                            len(
                                record.get(
                                    'errors', [])) for record in validation_results.get(
                                        'errors', [])), 'total_warnings': sum(
                                            len(
                                                record.get(
                                                    'warnings', [])) for record in validation_results.get(
                                                        'warnings', [])), 'error_types': {}, 'warning_types': {}}

        # حساب أنواع الأخطاء
        for record in validation_results.get('errors', []):
            for error in record.get('errors', []):
                rule = error.get('rule')
                if rule:
                    summary['error_types'][rule] = summary['error_types'].get(
                        rule, 0) + 1

        # حساب أنواع التحذيرات
        for record in validation_results.get('warnings', []):
            for warning in record.get('warnings', []):
                rule = warning.get('rule')
                if rule:
                    summary['warning_types'][rule] = summary['warning_types'].get(
                        rule, 0) + 1

        # حساب نسبة الأخطاء
        if summary['total_records'] > 0:
            summary['error_rate'] = summary['records_with_errors'] / \
                summary['total_records']
            summary['warning_rate'] = summary['records_with_warnings'] / \
                summary['total_records']
        else:
            summary['error_rate'] = 0
            summary['warning_rate'] = 0

        # تحديد ما إذا كانت النتائج تتطلب إشعاراً
        summary['requires_notification'] = summary['error_rate'] >= self.config['notification_threshold']

        return summary

    def _fix_data_with_results(self, validation_results, auto_fix=False):
        """
        إصلاح البيانات بناءً على نتائج التحقق

        Args:
            validation_results (dict): نتائج التحقق
            auto_fix (bool, optional): ما إذا كان يجب إصلاح الأخطاء تلقائياً. Defaults to False.

        Returns:
            dict: نتائج الإصلاح
        """
        # إنشاء نتائج الإصلاح
        fix_results = {
            'data_type': validation_results.get('data_type'),
            'timestamp': datetime.datetime.now().isoformat(),
            'total_records': validation_results.get('total_records', 0),
            'fixed_records': [],
            'unfixed_records': [],
            'summary': {}
        }

        # إصلاح الأخطاء
        for record in validation_results.get('errors', []):
            record_index = record.get('index')
            record_data = record.get('record')
            record_errors = record.get('errors', [])

            fixed_errors = []
            unfixed_errors = []

            for error in record_errors:
                rule = error.get('rule')
                auto_fixable = error.get('auto_fixable', False)

                if auto_fix and auto_fixable:
                    # إصلاح الخطأ
                    fixed_data = self._fix_error(record_data, rule, error)

                    if fixed_data:
                        record_data = fixed_data
                        fixed_errors.append(error)
                    else:
                        unfixed_errors.append(error)
                else:
                    unfixed_errors.append(error)

            # إضافة السجل إلى النتائج
            if fixed_errors:
                fix_results['fixed_records'].append({
                    'index': record_index,
                    'record': record_data,
                    'fixed_errors': fixed_errors,
                    'unfixed_errors': unfixed_errors
                })

            if unfixed_errors:
                fix_results['unfixed_records'].append({
                    'index': record_index,
                    'record': record_data,
                    'unfixed_errors': unfixed_errors
                })

        # إصلاح التحذيرات
        for record in validation_results.get('warnings', []):
            record_index = record.get('index')
            record_data = record.get('record')
            record_warnings = record.get('warnings', [])

            fixed_warnings = []
            unfixed_warnings = []

            for warning in record_warnings:
                rule = warning.get('rule')
                auto_fixable = warning.get('auto_fixable', False)

                if auto_fix and auto_fixable:
                    # إصلاح التحذير
                    fixed_data = self._fix_warning(record_data, rule, warning)

                    if fixed_data:
                        record_data = fixed_data
                        fixed_warnings.append(warning)
                    else:
                        unfixed_warnings.append(warning)
                else:
                    unfixed_warnings.append(warning)

            # إضافة السجل إلى النتائج
            if fixed_warnings:
                # التحقق من وجود السجل في النتائج
                existing_record = next(
                    (r for r in fix_results['fixed_records'] if r.get('index') == record_index),
                    None)

                if existing_record:
                    existing_record['fixed_warnings'] = fixed_warnings
                else:
                    fix_results['fixed_records'].append({
                        'index': record_index,
                        'record': record_data,
                        'fixed_warnings': fixed_warnings,
                        'unfixed_warnings': unfixed_warnings
                    })

            if unfixed_warnings:
                # التحقق من وجود السجل في النتائج
                existing_record = next(
                    (r for r in fix_results['unfixed_records'] if r.get('index') == record_index),
                    None)

                if existing_record:
                    existing_record['unfixed_warnings'] = unfixed_warnings
                else:
                    fix_results['unfixed_records'].append({
                        'index': record_index,
                        'record': record_data,
                        'unfixed_warnings': unfixed_warnings
                    })

        # إنشاء ملخص النتائج
        fix_results['summary'] = self._create_fix_summary(fix_results)

        return fix_results

    def _fix_error(self, record, rule, error):
        """
        إصلاح خطأ في سجل

        Args:
            record (dict): السجل
            rule (str): اسم القاعدة
            error (dict): معلومات الخطأ

        Returns:
            dict or None: السجل المصلح أو None إذا لم يتم الإصلاح
        """
        # نسخ السجل
        fixed_record = record.copy()

        # إصلاح الخطأ حسب نوع القاعدة
        if rule == 'value_ranges':
            # إصلاح نطاقات القيم
            message = error.get('message', '')

            # استخراج اسم الحقل والقيمة المطلوبة
            match = re.search(
                r'(\w+) should be at (least|most) (\d+)', message)

            if match:
                field = match.group(1)
                comparison = match.group(2)
                value = int(match.group(3))

                if field in fixed_record:
                    if comparison == 'least':
                        fixed_record[field] = max(fixed_record[field], value)
                    else:
                        fixed_record[field] = min(fixed_record[field], value)

                    return fixed_record

        elif rule == 'price_range':
            # إصلاح نطاق السعر
            if 'price' in fixed_record:
                price = fixed_record['price']
                message = error.get('message', '')

                if 'at least' in message:
                    min_price = int(
                        re.search(
                            r'at least (\d+)',
                            message).group(1))
                    fixed_record['price'] = max(price, min_price)
                    return fixed_record

                if 'at most' in message:
                    max_price = int(
                        re.search(
                            r'at most (\d+)',
                            message).group(1))
                    fixed_record['price'] = min(price, max_price)
                    return fixed_record

        elif rule == 'stock_range':
            # إصلاح نطاق المخزون
            if 'stock' in fixed_record:
                stock = fixed_record['stock']
                message = error.get('message', '')

                if 'at least' in message:
                    min_stock = int(
                        re.search(
                            r'at least (\d+)',
                            message).group(1))
                    fixed_record['stock'] = max(stock, min_stock)
                    return fixed_record

                if 'at most' in message:
                    max_stock = int(
                        re.search(
                            r'at most (\d+)',
                            message).group(1))
                    fixed_record['stock'] = min(stock, max_stock)
                    return fixed_record

        elif rule == 'growth_days_range':
            # إصلاح نطاق أيام النمو
            if 'growth_days' in fixed_record:
                growth_days = fixed_record['growth_days']
                message = error.get('message', '')

                if 'at least' in message:
                    min_days = int(
                        re.search(
                            r'at least (\d+)',
                            message).group(1))
                    fixed_record['growth_days'] = max(growth_days, min_days)
                    return fixed_record

                if 'at most' in message:
                    max_days = int(
                        re.search(
                            r'at most (\d+)',
                            message).group(1))
                    fixed_record['growth_days'] = min(growth_days, max_days)
                    return fixed_record

        elif rule == 'temperature_range':
            # إصلاح نطاق درجة الحرارة
            if 'temperature' in fixed_record:
                temperature = fixed_record['temperature']
                message = error.get('message', '')

                if 'at least' in message:
                    min_temp = int(
                        re.search(
                            r'at least (-?\d+)',
                            message).group(1))
                    fixed_record['temperature'] = max(temperature, min_temp)
                    return fixed_record

                if 'at most' in message:
                    max_temp = int(
                        re.search(
                            r'at most (-?\d+)',
                            message).group(1))
                    fixed_record['temperature'] = min(temperature, max_temp)
                    return fixed_record

        # لم يتم الإصلاح
        return None

    def _fix_warning(self, record, rule, warning):
        """
        إصلاح تحذير في سجل

        Args:
            record (dict): السجل
            rule (str): اسم القاعدة
            warning (dict): معلومات التحذير

        Returns:
            dict or None: السجل المصلح أو None إذا لم يتم الإصلاح
        """
        # استخدام نفس منطق إصلاح الأخطاء
        return self._fix_error(record, rule, warning)

    def _create_fix_summary(self, fix_results):
        """
        إنشاء ملخص نتائج الإصلاح

        Args:
            fix_results (dict): نتائج الإصلاح

        Returns:
            dict: ملخص النتائج
        """
        # إنشاء ملخص النتائج
        summary = {
            'total_records': fix_results.get('total_records', 0),
            'fixed_records': len(fix_results.get('fixed_records', [])),
            'unfixed_records': len(fix_results.get('unfixed_records', [])),
            'total_fixed_errors': sum(len(record.get('fixed_errors', [])) for record in fix_results.get('fixed_records', [])),
            'total_unfixed_errors': sum(len(record.get('unfixed_errors', [])) for record in fix_results.get('unfixed_records', [])),
            'total_fixed_warnings': sum(len(record.get('fixed_warnings', [])) for record in fix_results.get('fixed_records', [])),
            'total_unfixed_warnings': sum(len(record.get('unfixed_warnings', [])) for record in fix_results.get('unfixed_records', [])),
            'fixed_error_types': {},
            'unfixed_error_types': {},
            'fixed_warning_types': {},
            'unfixed_warning_types': {}
        }

        # حساب أنواع الأخطاء المصلحة
        for record in fix_results.get('fixed_records', []):
            for error in record.get('fixed_errors', []):
                rule = error.get('rule')
                if rule:
                    summary['fixed_error_types'][rule] = summary['fixed_error_types'].get(
                        rule, 0) + 1

        # حساب أنواع الأخطاء غير المصلحة
        for record in fix_results.get('unfixed_records', []):
            for error in record.get('unfixed_errors', []):
                rule = error.get('rule')
                if rule:
                    summary['unfixed_error_types'][rule] = summary['unfixed_error_types'].get(
                        rule, 0) + 1

        # حساب أنواع التحذيرات المصلحة
        for record in fix_results.get('fixed_records', []):
            for warning in record.get('fixed_warnings', []):
                rule = warning.get('rule')
                if rule:
                    summary['fixed_warning_types'][rule] = summary['fixed_warning_types'].get(
                        rule, 0) + 1

        # حساب أنواع التحذيرات غير المصلحة
        for record in fix_results.get('unfixed_records', []):
            for warning in record.get('unfixed_warnings', []):
                rule = warning.get('rule')
                if rule:
                    summary['unfixed_warning_types'][rule] = summary['unfixed_warning_types'].get(
                        rule, 0) + 1

        # حساب نسبة الإصلاح
        total_issues = summary['total_fixed_errors'] + summary['total_unfixed_errors'] + \
            summary['total_fixed_warnings'] + summary['total_unfixed_warnings']

        if total_issues > 0:
            summary['fix_rate'] = (
                summary['total_fixed_errors'] + summary['total_fixed_warnings']) / total_issues
        else:
            summary['fix_rate'] = 0

        return summary
