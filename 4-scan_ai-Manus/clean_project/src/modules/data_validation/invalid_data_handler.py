# /home/ubuntu/ai_web_organized/src/modules/data_validation/invalid_data_handler.py

"""
وحدة معالج البيانات غير الصحيحة (Invalid Data Handler)

هذه الوحدة مسؤولة عن معالجة البيانات غير الصحيحة التي تم اكتشافها بواسطة
محقق النموذج (Model Validator) ومحقق قاعدة البيانات (Database Validator).
توفر آليات للتصحيح التلقائي، والإبلاغ عن الأخطاء، وتسجيل الأحداث.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable

# استيراد وحدات التحقق
from .model_validator import ModelValidator
from .database_validator import DatabaseValidator

# Constants
DB_CONNECTION_FAILED = 'فشل الاتصال بقاعدة البيانات'
DEFAULT_EMAIL = 'default@example.com'

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('invalid_data_handler')


class InvalidDataHandler:
    """
    فئة معالج البيانات غير الصحيحة المسؤولة عن معالجة البيانات غير الصحيحة.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        تهيئة معالج البيانات غير الصحيحة.

        Args:
            config_path (str, optional): مسار ملف التكوين. إذا لم يتم تحديده، يتم استخدام الإعدادات الافتراضية.
        """
        self.config = self._load_config(config_path)
        self.model_validator = ModelValidator(config_path)
        self.database_validator = DatabaseValidator(config_path)
        self.error_handlers = self._load_error_handlers()
        self.notification_handlers = self._load_notification_handlers()
        logger.info("تم تهيئة معالج البيانات غير الصحيحة بنجاح")

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        تحميل ملف التكوين.

        Args:
            config_path (str, optional): مسار ملف التكوين.

        Returns:
            Dict[str, Any]: بيانات التكوين.
        """
        default_config = {
            "auto_fix": False,
            "log_errors": True,
            "notify_admin": True,
            "error_log_path": "/home/ubuntu/ai_web_organized/logs/data_validation_errors.log",
            "error_handlers_path": "/home/ubuntu/ai_web_organized/src/modules/data_validation/error_handlers",
            "notification_handlers_path": "/home/ubuntu/ai_web_organized/src/modules/data_validation/notification_handlers",
            "log_level": "INFO"
        }

        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                logger.error("خطأ في تحميل ملف التكوين: %s", str(e))
                return default_config
        return default_config

    def _load_error_handlers(self) -> Dict[str, Dict[str, Callable]]:
        """
        تحميل معالجات الأخطاء.

        Returns:
            Dict[str, Dict[str, Callable]]: معالجات الأخطاء المحملة.
        """
        error_handlers = {
            "model": {
                "missing_field": self._handle_missing_field,
                "invalid_type": self._handle_invalid_type,
                "invalid_value": self._handle_invalid_value,
                "unknown_field": self._handle_unknown_field
            },
            "database": {
                "schema_mismatch": self._handle_schema_mismatch,
                "null_value": self._handle_null_value,
                "invalid_value": self._handle_invalid_value,
                "foreign_key_violation": self._handle_foreign_key_violation
            }
        }
        logger.info("تم تحميل معالجات الأخطاء بنجاح")
        return error_handlers

    def _load_notification_handlers(self) -> Dict[str, Callable]:
        """
        تحميل معالجات الإشعارات.

        Returns:
            Dict[str, Callable]: معالجات الإشعارات المحملة.
        """
        notification_handlers = {
            "log": self._notify_log,
            "admin": self._notify_admin,
            "email": self._notify_email,
            "telegram": self._notify_telegram
        }
        logger.info("تم تحميل معالجات الإشعارات بنجاح")
        return notification_handlers

    def handle_invalid_model_data(self, data: Dict[str, Any], model_name: str, auto_fix: Optional[bool] = None) -> Tuple[bool, Dict[str, Any], List[Dict[str, Any]]]:
        """
        معالجة البيانات غير الصحيحة وفقًا لنموذج محدد.

        Args:
            data (Dict[str, Any]): البيانات المراد معالجتها.
            model_name (str): اسم النموذج.
            auto_fix (bool, optional): ما إذا كان يجب إصلاح البيانات تلقائيًا. إذا لم يتم تحديده، يتم استخدام الإعداد في ملف التكوين.

        Returns:
            Tuple[bool, Dict[str, Any], List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ)، البيانات المعالجة، وقائمة بالإجراءات المتخذة.
        """
        if auto_fix is None:
            auto_fix = self.config.get("auto_fix", False)

        # التحقق من صحة البيانات
        data_is_valid, errors = self.model_validator.validate_data(data, model_name)

        if data_is_valid:
            logger.info("البيانات صحيحة وفقًا للنموذج '%s'", model_name)
            return True, data, []

        # معالجة الأخطاء
        data_fixed = data.copy()
        action_list = []

        for error in errors:
            field = error.get("field")
            error_type = self._determine_error_type(error)

            if error_type in self.error_handlers["model"]:
                error_handler = self.error_handlers["model"][error_type]
                result = error_handler(data_fixed, field, model_name, auto_fix)

                if result:
                    fixed, action_taken = result
                    if fixed:
                        action_list.append(action_taken)

        # التحقق مرة أخرى بعد المعالجة
        data_is_valid, remaining_errors = self.model_validator.validate_data(data_fixed, model_name)

        # تسجيل الأخطاء والإشعارات
        if not data_is_valid and self.config.get("log_errors", True):
            self._log_errors("model", model_name, remaining_errors)

        if not data_is_valid and self.config.get("notify_admin", True):
            self._notify_errors("model", model_name, remaining_errors)

        return data_is_valid, data_fixed, action_list

    def handle_invalid_database_data(self, table_name: str, auto_fix: Optional[bool] = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        معالجة البيانات غير الصحيحة في قاعدة البيانات.

        Args:
            table_name (str): اسم الجدول.
            auto_fix (bool, optional): ما إذا كان يجب إصلاح البيانات تلقائيًا. إذا لم يتم تحديده، يتم استخدام الإعداد في ملف التكوين.

        Returns:
            Tuple[bool, List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) وقائمة بالإجراءات المتخذة.
        """
        if auto_fix is None:
            auto_fix = self.config.get("auto_fix", False)

        # التأكد من الاتصال بقاعدة البيانات
        if not self.database_validator.connection:
            connected = self.database_validator.connect()
            if not connected:
                logger.error(DB_CONNECTION_FAILED)
                return False, [{"table": table_name, "error": DB_CONNECTION_FAILED}]

        # التحقق من صحة مخطط الجدول
        schema_valid, schema_errors = self.database_validator.validate_table_schema(table_name)

        if not schema_valid:
            logger.warning("مخطط الجدول '%s' غير صحيح", table_name)

            # تسجيل الأخطاء والإشعارات
            if self.config.get("log_errors", True):
                self._log_errors("database_schema", table_name, schema_errors)

            if self.config.get("notify_admin", True):
                self._notify_errors("database_schema", table_name, schema_errors)

            # لا يمكن إصلاح مخطط الجدول تلقائيًا
            return False, [{"table": table_name, "error": "مخطط الجدول غير صحيح", "details": schema_errors}]

        # التحقق من تكامل البيانات وإصلاحها إذا لزم الأمر
        if auto_fix:
            data_is_valid, action_list = self.database_validator.repair_data_integrity(table_name, auto_fix=True)
        else:
            data_is_valid, errors = self.database_validator.validate_data_integrity(table_name)
            action_list = [{"table": table_name, "error": "تم اكتشاف أخطاء في تكامل البيانات", "details": errors}]

        # تسجيل الأخطاء والإشعارات
        if not data_is_valid and self.config.get("log_errors", True):
            self._log_errors("database_integrity", table_name, errors if 'errors' in locals() else [])

        if not data_is_valid and self.config.get("notify_admin", True):
            self._notify_errors("database_integrity", table_name, errors if 'errors' in locals() else [])

        return data_is_valid, action_list

    def handle_batch_model_data(self, data_list: List[Dict[str, Any]], model_name: str, auto_fix: Optional[bool] = None) -> Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        معالجة مجموعة من البيانات غير الصحيحة وفقًا لنموذج محدد.

        Args:
            data_list (List[Dict[str, Any]]): قائمة البيانات المراد معالجتها.
            model_name (str): اسم النموذج.
            auto_fix (bool, optional): ما إذا كان يجب إصلاح البيانات تلقائيًا. إذا لم يتم تحديده، يتم استخدام الإعداد في ملف التكوين.

        Returns:
            Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ)، قائمة البيانات المعالجة، وقائمة بالإجراءات المتخذة.
        """
        fixed_data_list = []
        all_actions = []
        all_valid = True

        for index, data in enumerate(data_list):
            data_is_valid, data_fixed, action_list = self.handle_invalid_model_data(data, model_name, auto_fix)

            fixed_data_list.append(data_fixed)

            if action_list:
                for action_taken in action_list:
                    action_taken["index"] = index
                all_actions.extend(action_list)

            if not data_is_valid:
                all_valid = False

        return all_valid, fixed_data_list, all_actions

    def handle_all_database_tables(self, auto_fix: Optional[bool] = None) -> Dict[str, Tuple[bool, List[Dict[str, Any]]]]:
        """
        معالجة البيانات غير الصحيحة في جميع جداول قاعدة البيانات.

        Args:
            auto_fix (bool, optional): ما إذا كان يجب إصلاح البيانات تلقائيًا. إذا لم يتم تحديده، يتم استخدام الإعداد في ملف التكوين.

        Returns:
            Dict[str, Tuple[bool, List[Dict[str, Any]]]]: نتائج المعالجة لكل جدول.
        """
        results = {}

        # التأكد من الاتصال بقاعدة البيانات
        if not self.database_validator.connection:
            connected = self.database_validator.connect()
            if not connected:
                logger.error(DB_CONNECTION_FAILED)
                return {"error": (False, [{"error": DB_CONNECTION_FAILED}])}

        # معالجة كل جدول
        for table_name in self.database_validator.constraints:
            data_is_valid, action_list = self.handle_invalid_database_data(table_name, auto_fix)
            results[table_name] = (data_is_valid, action_list)

        return results

    def _determine_error_type(self, error: Dict[str, Any]) -> str:
        """
        تحديد نوع الخطأ.

        Args:
            error (Dict[str, Any]): معلومات الخطأ.

        Returns:
            str: نوع الخطأ.
        """
        error_message = error.get("error", "").lower()

        if "مطلوب" in error_message or "required" in error_message:
            return "missing_field"
        elif "نوع" in error_message or "type" in error_message:
            return "invalid_type"
        elif "قيمة" in error_message or "value" in error_message:
            return "invalid_value"
        elif "غير موجود" in error_message or "not found" in error_message:
            return "unknown_field"
        else:
            return "invalid_value"  # نوع افتراضي

    def _handle_missing_field(self, data: Dict[str, Any], field: str, model_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة حقل مفقود.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            model_name (str): اسم النموذج.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        if not auto_fix:
            return None

        # الحصول على معلومات النموذج
        model = self.model_validator.get_model(model_name)
        if not model:
            return None

        # الحصول على معلومات الحقل
        field_info = model["fields"].get(field)
        if not field_info:
            return None

        # تحديد القيمة الافتراضية بناءً على نوع الحقل
        field_type = field_info.get("type")
        default_value = None

        if field_type == "string":
            default_value = ""
        elif field_type == "integer":
            default_value = 0
        elif field_type == "float":
            default_value = 0.0
        elif field_type == "boolean":
            default_value = False
        elif field_type == "email":
            default_value = DEFAULT_EMAIL
        elif field_type == "datetime":
            default_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif field_type == "array":
            default_value = []

        # إضافة القيمة الافتراضية
        if default_value is not None:
            data[field] = default_value
            return True, {
                "field": field,
                "action": "إضافة",
                "value": default_value,
                "message": f"تمت إضافة قيمة افتراضية للحقل '{field}'"
            }

        return None

    def _handle_invalid_type(self, data: Dict[str, Any], field: str, model_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة نوع غير صحيح.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            model_name (str): اسم النموذج.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        if not auto_fix or field not in data:
            return None

        # الحصول على معلومات النموذج
        model = self.model_validator.get_model(model_name)
        if not model:
            return None

        # الحصول على معلومات الحقل
        field_info = model["fields"].get(field)
        if not field_info:
            return None

        # تحويل القيمة إلى النوع الصحيح
        field_type = field_info.get("type")
        current_value = data[field]
        converted_value = None

        try:
            if field_type == "string":
                converted_value = str(current_value)
            elif field_type == "integer":
                converted_value = int(float(current_value))
            elif field_type == "float":
                converted_value = float(current_value)
            elif field_type == "boolean":
                if isinstance(current_value, str):
                    converted_value = current_value.lower() in ["true", "yes", "1", "y"]
                else:
                    converted_value = bool(current_value)
            elif field_type == "email":
                converted_value = str(current_value)
                if "@" not in converted_value:
                    converted_value = DEFAULT_EMAIL
            elif field_type == "datetime":
                if isinstance(current_value, str):
                    converted_value = current_value
                else:
                    converted_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif field_type == "array":
                if isinstance(current_value, str):
                    try:
                        converted_value = json.loads(current_value)
                    except (ValueError, TypeError, json.JSONDecodeError):
                        converted_value = []
                else:
                    converted_value = list(current_value) if hasattr(current_value, "__iter__") else [current_value]
        except (ValueError, TypeError) as e:
            logger.error("خطأ في تحويل قيمة الحقل '%s': %s", field, str(e))
            return None

        # تحديث القيمة
        if converted_value is not None:
            old_value = data[field]
            data[field] = converted_value
            return True, {
                "field": field,
                "action": "تحويل",
                "old_value": old_value,
                "new_value": converted_value,
                "message": f"تم تحويل قيمة الحقل '{field}' من '{old_value}' إلى '{converted_value}'"
            }

        return None

    def _handle_invalid_value(self, data: Dict[str, Any], field: str, model_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة قيمة غير صحيحة.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            model_name (str): اسم النموذج.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        if not auto_fix or field not in data:
            return None

        # الحصول على معلومات النموذج
        model = self.model_validator.get_model(model_name)
        if not model:
            return None

        # الحصول على معلومات الحقل
        field_info = model["fields"].get(field)
        if not field_info:
            return None

        # تصحيح القيمة
        field_type = field_info.get("type")
        current_value = data[field]
        corrected_value = None

        if field_type == "string":
            min_length = field_info.get("min_length", 0)
            max_length = field_info.get("max_length", 1000)

            if isinstance(current_value, str):
                if len(current_value) < min_length:
                    corrected_value = current_value + "x" * (min_length - len(current_value))
                elif len(current_value) > max_length:
                    corrected_value = current_value[:max_length]

        elif field_type == "integer":
            min_value = field_info.get("min_value", -2147483648)
            max_value = field_info.get("max_value", 2147483647)

            if isinstance(current_value, (int, float)):
                if current_value < min_value:
                    corrected_value = min_value
                elif current_value > max_value:
                    corrected_value = max_value

        elif field_type == "float":
            min_value = field_info.get("min_value", float('-inf'))
            max_value = field_info.get("max_value", float('inf'))

            if isinstance(current_value, (int, float)):
                if current_value < min_value:
                    corrected_value = min_value
                elif current_value > max_value:
                    corrected_value = max_value

        elif field_type == "email":
            if isinstance(current_value, str) and "@" not in current_value:
                corrected_value = DEFAULT_EMAIL

        elif field_type == "array":
            min_items = field_info.get("min_items", 0)
            max_items = field_info.get("max_items", 1000)

            if isinstance(current_value, list):
                if len(current_value) < min_items:
                    corrected_value = current_value + [None] * (min_items - len(current_value))
                elif len(current_value) > max_items:
                    corrected_value = current_value[:max_items]

        # تحديث القيمة
        if corrected_value is not None:
            old_value = data[field]
            data[field] = corrected_value
            return True, {
                "field": field,
                "action": "تصحيح",
                "old_value": old_value,
                "new_value": corrected_value,
                "message": f"تم تصحيح قيمة الحقل '{field}' من '{old_value}' إلى '{corrected_value}'"
            }

        return None

    def _handle_unknown_field(self, data: Dict[str, Any], field: str, model_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة حقل غير معروف.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            model_name (str): اسم النموذج.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        if not auto_fix or field not in data:
            return None

        # إزالة الحقل غير المعروف
        removed_value = data.pop(field)
        return True, {
            "field": field,
            "action": "إزالة",
            "value": removed_value,
            "message": f"تمت إزالة الحقل غير المعروف '{field}'"
        }

    def _handle_schema_mismatch(self, data: Dict[str, Any], field: str, table_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة عدم تطابق المخطط.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            table_name (str): اسم الجدول.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        # لا يمكن إصلاح مخطط الجدول تلقائيًا
        return None

    def _handle_null_value(self, data: Dict[str, Any], field: str, table_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة قيمة فارغة.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            table_name (str): اسم الجدول.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        # تتم معالجة القيم الفارغة في قاعدة البيانات بواسطة repair_data_integrity
        return None

    def _handle_foreign_key_violation(self, data: Dict[str, Any], field: str, table_name: str, auto_fix: bool) -> Optional[Tuple[bool, Dict[str, Any]]]:
        """
        معالجة انتهاك المفتاح الأجنبي.

        Args:
            data (Dict[str, Any]): البيانات.
            field (str): اسم الحقل.
            table_name (str): اسم الجدول.
            auto_fix (bool): ما إذا كان يجب إصلاح البيانات تلقائيًا.

        Returns:
            Optional[Tuple[bool, Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) ومعلومات الإجراء المتخذ.
        """
        # تتم معالجة انتهاكات المفتاح الأجنبي في قاعدة البيانات بواسطة repair_data_integrity
        return None

    def _log_errors(self, error_type: str, context: str, errors: List[Dict[str, Any]]) -> None:
        """
        تسجيل الأخطاء.

        Args:
            error_type (str): نوع الخطأ.
            context (str): سياق الخطأ.
            errors (List[Dict[str, Any]]): قائمة الأخطاء.
        """
        if not errors:
            return

        log_path = self.config.get("error_log_path")

        # التأكد من وجود مجلد السجلات
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {error_type} - {context}:\n")
                for error in errors:
                    f.write(f"  - {json.dumps(error, ensure_ascii=False)}\n")
                f.write("\n")

            logger.info("تم تسجيل %d خطأ في '%s'", len(errors), log_path)
        except Exception as e:
            logger.error("خطأ في تسجيل الأخطاء: %s", str(e))

    def _notify_errors(self, error_type: str, context: str, errors: List[Dict[str, Any]]) -> None:
        """
        إشعار بالأخطاء.

        Args:
            error_type (str): نوع الخطأ.
            context (str): سياق الخطأ.
            errors (List[Dict[str, Any]]): قائمة الأخطاء.
        """
        if not errors:
            return

        # استدعاء معالجات الإشعارات
        for handler_name, notification_handler in self.notification_handlers.items():
            try:
                notification_handler(error_type, context, errors)
            except Exception as e:
                logger.error("خطأ في معالج الإشعارات '%s': %s", handler_name, str(e))

    def _notify_log(self, error_type: str, context: str, errors: List[Dict[str, Any]]) -> None:
        """
        إشعار بالأخطاء في السجل.

        Args:
            error_type (str): نوع الخطأ.
            context (str): سياق الخطأ.
            errors (List[Dict[str, Any]]): قائمة الأخطاء.
        """
        logger.warning("%s - %s: %d خطأ", error_type, context, len(errors))
        for error in errors[:5]:  # تسجيل أول 5 أخطاء فقط لتجنب التضخم
            logger.warning("  - %s", json.dumps(error, ensure_ascii=False))

        if len(errors) > 5:
            logger.warning("  ... و%d خطأ آخر", len(errors) - 5)

    def _notify_admin(self, error_type: str, context: str, errors: List[Dict[str, Any]]) -> None:
        """
        إشعار المسؤول بالأخطاء.

        Args:
            error_type (str): نوع الخطأ.
            context (str): سياق الخطأ.
            errors (List[Dict[str, Any]]): قائمة الأخطاء.
        """
        # في الإنتاج، يمكن إرسال إشعار إلى لوحة تحكم المسؤول
        # هنا نقوم بتسجيل الإشعار فقط
        logger.info("تم إرسال إشعار إلى المسؤول: %s - %s: %d خطأ", error_type, context, len(errors))

    def _notify_email(self, error_type: str, context: str, errors: List[Dict[str, Any]]) -> None:
        """
        إشعار بالأخطاء عبر البريد الإلكتروني.

        Args:
            error_type (str): نوع الخطأ.
            context (str): سياق الخطأ.
            errors (List[Dict[str, Any]]): قائمة الأخطاء.
        """
        # في الإنتاج، يمكن إرسال بريد إلكتروني إلى المسؤول
        # هنا نقوم بتسجيل الإشعار فقط
        logger.info("تم إرسال إشعار عبر البريد الإلكتروني: %s - %s: %d خطأ", error_type, context, len(errors))

    def _notify_telegram(self, error_type: str, context: str, errors: List[Dict[str, Any]]) -> None:
        """
        إشعار بالأخطاء عبر تيليجرام.

        Args:
            error_type (str): نوع الخطأ.
            context (str): سياق الخطأ.
            errors (List[Dict[str, Any]]): قائمة الأخطاء.
        """
        # في الإنتاج، يمكن إرسال رسالة إلى بوت تيليجرام
        # هنا نقوم بتسجيل الإشعار فقط
        logger.info("تم إرسال إشعار عبر تيليجرام: %s - %s: %d خطأ", error_type, context, len(errors))
