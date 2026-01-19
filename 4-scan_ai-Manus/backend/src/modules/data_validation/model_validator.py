# /home/ubuntu/ai_web_organized/src/modules/data_validation/model_validator.py

"""
from flask import g
وحدة محقق النموذج (Model Validator)

هذه الوحدة مسؤولة عن التحقق من صحة البيانات المدخلة وفقًا لنماذج البيانات المحددة.
تقوم بالتحقق من أن البيانات تتوافق مع القواعد والقيود المحددة في النماذج.
"""

import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('model_validator')


class ModelValidator:
    """
    فئة محقق النموذج المسؤولة عن التحقق من صحة البيانات وفقًا للنماذج المحددة.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        تهيئة محقق النموذج.

        Args:
            config_path (str, optional): مسار ملف التكوين. إذا لم يتم تحديده، يتم استخدام الإعدادات الافتراضية.
        """
        self.config = self._load_config(config_path)
        self.models = self._load_models()
        self.validation_rules = self._load_validation_rules()
        logger.info("تم تهيئة محقق النموذج بنجاح")

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        تحميل ملف التكوين.

        Args:
            config_path (str, optional): مسار ملف التكوين.

        Returns:
            Dict[str, Any]: بيانات التكوين.
        """
        default_config = {
            "models_path": "/home/ubuntu/ai_web_organized/src/modules/data_validation/models",
            "rules_path": "/home/ubuntu/ai_web_organized/src/modules/data_validation/rules",
            "strict_mode": True,
            "log_level": "INFO"}

        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                logger.error("خطأ في تحميل ملف التكوين: %s", str(e))
                return default_config
        return default_config

    def _load_models(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل نماذج البيانات.

        Returns:
            Dict[str, Dict[str, Any]]: نماذج البيانات المحملة.
        """
        models = {}
        try:
            # في الإنتاج، يمكن تحميل النماذج من ملفات JSON أو قاعدة بيانات
            # هنا نستخدم نماذج افتراضية للتوضيح
            models = {
                "user": {
                    "fields": {
                        "id": {"type": "integer", "required": True},
                        "username": {"type": "string", "required": True, "min_length": 3, "max_length": 50},
                        "email": {"type": "email", "required": True},
                        "password": {"type": "string", "required": True, "min_length": 8},
                        "role": {"type": "string", "required": True, "enum": ["admin", "user", "guest"]},
                        "created_at": {"type": "datetime", "required": False}
                    }
                },
                "product": {
                    "fields": {
                        "id": {"type": "integer", "required": True},
                        "name": {"type": "string", "required": True, "min_length": 2, "max_length": 100},
                        "price": {"type": "float", "required": True, "min": 0},
                        "category": {"type": "string", "required": True},
                        "in_stock": {"type": "boolean", "required": True},
                        "created_at": {"type": "datetime", "required": False}
                    }
                },
                "order": {
                    "fields": {
                        "id": {"type": "integer", "required": True},
                        "user_id": {"type": "integer", "required": True},
                        "products": {"type": "array", "required": True, "item_type": "integer"},
                        "total": {"type": "float", "required": True, "min": 0},
                        "status": {"type": "string", "required": True, "enum": ["pending", "processing", "shipped", "delivered", "cancelled"]},
                        "created_at": {"type": "datetime", "required": False}
                    }
                }
            }
            logger.info("تم تحميل %d نموذج بنجاح", len(models))
        except Exception as e:
            logger.error("خطأ في تحميل النماذج: %s", str(e))
        return models

    def _load_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قواعد التحقق.

        Returns:
            Dict[str, Dict[str, Any]]: قواعد التحقق المحملة.
        """
        rules = {}
        try:
            # في الإنتاج، يمكن تحميل القواعد من ملفات JSON أو قاعدة بيانات
            # هنا نستخدم قواعد افتراضية للتوضيح
            rules = {
                "string": {
                    "validate": lambda value, params: isinstance(value, str)
                    and (params.get("min_length", 0) <= len(value) <= params.get("max_length", float('inf')))
                },
                "integer": {
                    "validate": lambda value, params: isinstance(value, int)
                    and (params.get("min", float('-inf')) <= value <= params.get("max", float('inf')))
                },
                "float": {
                    "validate": lambda value, params: isinstance(value, (int, float))
                    and (params.get("min", float('-inf')) <= value <= params.get("max", float('inf')))
                },
                "boolean": {
                    "validate": lambda value, params: isinstance(value, bool)
                },
                "email": {
                    "validate": lambda value, params: isinstance(value, str)
                    and bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value))
                },
                "datetime": {
                    "validate": lambda value, params: isinstance(value, (str, datetime))
                    and (isinstance(value, datetime) or self._is_valid_datetime(value))
                },
                "array": {
                    "validate": lambda value, params: isinstance(value, list)
                    and (not params.get("item_type") or all(self._validate_type(item, params.get("item_type"), {}) for item in value))
                }
            }
            logger.info("تم تحميل %d قاعدة تحقق بنجاح", len(rules))
        except Exception as e:
            logger.error("خطأ في تحميل قواعد التحقق: %s", str(e))
        return rules

    def _is_valid_datetime(self, value: str) -> bool:
        """
        التحقق من صحة تنسيق التاريخ والوقت.

        Args:
            value (str): قيمة التاريخ والوقت.

        Returns:
            bool: True إذا كان التنسيق صحيحًا، False خلاف ذلك.
        """
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
            return True
        except (ValueError, AttributeError):
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                return True
            except (ValueError, AttributeError):
                return False

    def validate_data(
            self, data: Dict[str, Any], model_name: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        التحقق من صحة البيانات وفقًا لنموذج محدد.

        Args:
            data (Dict[str, Any]): البيانات المراد التحقق منها.
            model_name (str): اسم النموذج.

        Returns:
            Tuple[bool, List[Dict[str, Any]]]: زوج من القيمة المنطقية (صحيح/خطأ) وقائمة بالأخطاء.
        """
        if model_name not in self.models:
            logger.error("النموذج '%s' غير موجود", model_name)
            return False, [
                {"field": "model", "error": f"النموذج '{model_name}' غير موجود"}]

        model = self.models[model_name]
        validation_errors = []

        # التحقق من الحقول المطلوبة
        for field_name, field_config in model["fields"].items():
            if field_config.get("required", False) and field_name not in data:
                validation_errors.append({
                    "field": field_name,
                    "error": f"الحقل '{field_name}' مطلوب"
                })

        # التحقق من صحة البيانات
        for field_name, field_value in data.items():
            if field_name in model["fields"]:
                field_config = model["fields"][field_name]
                field_type = field_config.get("type")

                if field_value is None and field_config.get("required", False):
                    validation_errors.append({
                        "field": field_name,
                        "error": f"الحقل '{field_name}' لا يمكن أن يكون فارغًا"
                    })
                    continue

                if field_value is not None:
                    field_is_valid = self._validate_type(
                        field_value, field_type, field_config)
                    if not field_is_valid:
                        validation_errors.append({
                            "field": field_name,
                            "error": f"قيمة الحقل '{field_name}' غير صالحة"
                        })

                    # التحقق من القيم المحددة (enum)
                    if "enum" in field_config and field_value not in field_config["enum"]:
                        validation_errors.append({
                            "field": field_name,
                            "error": f"قيمة الحقل '{field_name}' يجب أن تكون واحدة من: {', '.join(field_config['enum'])}"
                        })
            elif self.config.get("strict_mode", True):
                validation_errors.append({
                    "field": field_name,
                    "error": f"الحقل '{field_name}' غير موجود في النموذج"
                })

        data_is_valid = len(validation_errors) == 0
        return data_is_valid, validation_errors

    def _validate_type(self, value: Any, type_name: str,
                       params: Dict[str, Any]) -> bool:
        """
        التحقق من صحة نوع البيانات.

        Args:
            value (Any): القيمة المراد التحقق منها.
            type_name (str): اسم النوع.
            params (Dict[str, Any]): معلمات التحقق.

        Returns:
            bool: True إذا كان النوع صحيحًا، False خلاف ذلك.
        """
        if type_name not in self.validation_rules:
            logger.warning("نوع التحقق '%s' غير معرف", type_name)
            return True

        rule = self.validation_rules[type_name]
        return rule["validate"](value, params)

    def add_model(self, model_name: str,
                  model_definition: Dict[str, Any]) -> bool:
        """
        إضافة نموذج جديد.

        Args:
            model_name (str): اسم النموذج.
            model_definition (Dict[str, Any]): تعريف النموذج.

        Returns:
            bool: True إذا تمت الإضافة بنجاح، False خلاف ذلك.
        """
        try:
            if "fields" not in model_definition:
                logger.error("تعريف النموذج يجب أن يحتوي على حقل 'fields'")
                return False

            self.models[model_name] = model_definition
            logger.info("تمت إضافة النموذج '%s' بنجاح", model_name)
            return True
        except Exception as e:
            logger.error("خطأ في إضافة النموذج: %s", str(e))
            return False

    def update_model(self, model_name: str,
                     model_definition: Dict[str, Any]) -> bool:
        """
        تحديث نموذج موجود.

        Args:
            model_name (str): اسم النموذج.
            model_definition (Dict[str, Any]): تعريف النموذج الجديد.

        Returns:
            bool: True إذا تم التحديث بنجاح، False خلاف ذلك.
        """
        if model_name not in self.models:
            logger.error("النموذج '%s' غير موجود", model_name)
            return False

        try:
            if "fields" not in model_definition:
                logger.error("تعريف النموذج يجب أن يحتوي على حقل 'fields'")
                return False

            self.models[model_name] = model_definition
            logger.info("تم تحديث النموذج '%s' بنجاح", model_name)
            return True
        except Exception as e:
            logger.error("خطأ في تحديث النموذج: %s", str(e))
            return False

    def delete_model(self, model_name: str) -> bool:
        """
        حذف نموذج.

        Args:
            model_name (str): اسم النموذج.

        Returns:
            bool: True إذا تم الحذف بنجاح، False خلاف ذلك.
        """
        if model_name not in self.models:
            logger.error("النموذج '%s' غير موجود", model_name)
            return False

        try:
            del self.models[model_name]
            logger.info("تم حذف النموذج '%s' بنجاح", model_name)
            return True
        except Exception as e:
            logger.error("خطأ في حذف النموذج: %s", str(e))
            return False

    def get_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على نموذج.

        Args:
            model_name (str): اسم النموذج.

        Returns:
            Optional[Dict[str, Any]]: تعريف النموذج إذا كان موجودًا، None خلاف ذلك.
        """
        if model_name not in self.models:
            logger.warning("النموذج '%s' غير موجود", model_name)
            return None

        return self.models[model_name]

    def get_all_models(self) -> Dict[str, Dict[str, Any]]:
        """
        الحصول على جميع النماذج.

        Returns:
            Dict[str, Dict[str, Any]]: جميع النماذج المحملة.
        """
        return self.models

    def validate_batch(self, data_list: List[Dict[str, Any]],
                       model_name: str) -> List[Tuple[bool, List[Dict[str, Any]]]]:
        """
        التحقق من صحة مجموعة من البيانات.

        Args:
            data_list (List[Dict[str, Any]]): قائمة البيانات المراد التحقق منها.
            model_name (str): اسم النموذج.

        Returns:
            List[Tuple[bool, List[Dict[str, Any]]]]: قائمة بنتائج التحقق لكل عنصر.
        """
        results = []
        for data in data_list:
            result = self.validate_data(data, model_name)
            results.append(result)
        return results
