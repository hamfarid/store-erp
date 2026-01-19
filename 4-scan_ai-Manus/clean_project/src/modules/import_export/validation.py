"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/validation.py
الوصف: وحدة التحقق من صحة البيانات المستوردة والمصدرة
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""
# pylint: disable=too-many-lines

import csv
import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Union

import pandas as pd

from src.modules.activity_log.error_logger import get_error_logger, log_errors
from src.modules.security.security_middleware import get_current_user_id

# إعداد المسجل
logger = logging.getLogger(__name__)

# ثوابت للنصوص المكررة
MODULE_NAME = "import_export.validation"


class ImportValidationError(Exception):
    """استثناء مخصص لأخطاء التحقق من صحة الاستيراد"""

    def __init__(self, message: str, errors: List[Dict[str, Any]] = None):
        super().__init__(message)
        self.errors = errors or []


class ExportValidationError(Exception):
    """استثناء مخصص لأخطاء التحقق من صحة التصدير"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DataValidator:
    """
    فئة للتحقق من صحة البيانات المستوردة والمصدرة
    """

    def __init__(self):
        """تهيئة مدقق البيانات"""
        self.error_logger = get_error_logger()

    @log_errors(module_name=MODULE_NAME)
    def validate_import_file(self, file_path: str, expected_format: str = None) -> Tuple[bool, Optional[str], Optional[Dict]]:  # pylint: disable=too-many-branches
        """
        التحقق من صحة ملف الاستيراد

        Args:
            file_path: مسار الملف
            expected_format: التنسيق المتوقع (csv, excel, json)، إذا كان None سيتم تحديده تلقائياً

        Returns:
            tuple: (صحيح/خطأ، رسالة الخطأ إذا وجدت، معلومات الملف)
        """
        if not os.path.exists(file_path):
            return False, "الملف غير موجود", None

        # تحديد تنسيق الملف إذا لم يتم تحديده
        if expected_format is None:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            if ext == '.csv':
                expected_format = 'csv'
            elif ext in ['.xls', '.xlsx']:
                expected_format = 'excel'
            elif ext == '.json':
                expected_format = 'json'
            else:
                return False, f"تنسيق الملف غير مدعوم: {ext}", None

        # التحقق من صحة الملف حسب التنسيق
        try:
            file_info = {
                'format': expected_format,
                'path': file_path,
                'size': os.path.getsize(file_path),
                'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            }

            if expected_format == 'csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)
                    if not headers:
                        return False, "ملف CSV فارغ أو غير صالح", file_info

                    file_info['headers'] = headers
                    file_info['row_count'] = sum(1 for _ in reader) + 1  # +1 للعناوين

            elif expected_format == 'excel':
                df = pd.read_excel(file_path)
                if df.empty:
                    return False, "ملف Excel فارغ", file_info

                file_info['headers'] = df.columns.tolist()
                file_info['row_count'] = len(df) + 1  # +1 للعناوين
                file_info['sheet_count'] = len(pd.ExcelFile(file_path).sheet_names)
                file_info['sheet_names'] = pd.ExcelFile(file_path).sheet_names

            elif expected_format == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if isinstance(data, list):
                    file_info['row_count'] = len(data)
                    if data and isinstance(data[0], dict):
                        file_info['headers'] = list(data[0].keys())
                elif isinstance(data, dict):
                    file_info['row_count'] = 1
                    file_info['headers'] = list(data.keys())
                else:
                    return False, "تنسيق JSON غير مدعوم", file_info

            return True, None, file_info

        except (OSError, ValueError, pd.errors.EmptyDataError, json.JSONDecodeError) as e:
            error_message = f"خطأ في التحقق من صحة الملف: {str(e)}"
            logger.error(error_message)

            # تسجيل الخطأ في سجل النشاط
            try:
                user_id = get_current_user_id()
            except Exception:  # pylint: disable=broad-except
                user_id = None

            self.error_logger.log_application_error(
                error=e,
                module_name=MODULE_NAME,
                function_name="validate_import_file",
                user_id=user_id,
                additional_context={
                    "file_path": file_path,
                    "expected_format": expected_format
                }
            )

            return False, error_message, None

    @log_errors(module_name=MODULE_NAME)
    def validate_import_data(self, data: Union[List, Dict], schema: Dict, entity_type: str) -> Tuple[bool, List[Dict[str, Any]]]:  # pylint: disable=too-many-branches,too-many-statements
        """
        التحقق من صحة البيانات المستوردة مقابل المخطط المتوقع

        Args:
            data: البيانات المستوردة (قائمة أو قاموس)
            schema: مخطط البيانات المتوقع
            entity_type: نوع الكيان (مثل "users", "products", "customers")

        Returns:
            tuple: (صحيح/خطأ، قائمة بالأخطاء)
        """
        errors = []

        # تحويل البيانات إلى قائمة إذا كانت قاموساً
        if isinstance(data, dict):
            data = [data]

        # التحقق من أن البيانات قائمة
        if not isinstance(data, list):
            errors.append({
                "row": 0,
                "field": None,
                "error": "البيانات يجب أن تكون قائمة أو قاموس",
                "value": str(type(data))
            })
            return False, errors

        # التحقق من كل صف في البيانات
        for row_idx, row in enumerate(data):
            if not isinstance(row, dict):
                errors.append({
                    "row": row_idx + 1,  # +1 للعناوين
                    "field": None,
                    "error": "كل صف يجب أن يكون قاموساً",
                    "value": str(type(row))
                })
                continue

            # التحقق من الحقول المطلوبة
            for field, field_schema in schema.items():
                if field_schema.get('required', False) and field not in row:
                    errors.append({
                        "row": row_idx + 1,
                        "field": field,
                        "error": "حقل مطلوب مفقود",
                        "value": None
                    })
                    continue

                # تخطي الحقول غير الموجودة وغير المطلوبة
                if field not in row:
                    continue

                value = row[field]
                field_type = field_schema.get('type')

                # التحقق من نوع البيانات
                if field_type == 'string' and not isinstance(value, str):
                    errors.append({
                        "row": row_idx + 1,
                        "field": field,
                        "error": "يجب أن يكون نص",
                        "value": value
                    })
                elif field_type == 'number' and not isinstance(value, (int, float)):
                    errors.append({
                        "row": row_idx + 1,
                        "field": field,
                        "error": "يجب أن يكون رقم",
                        "value": value
                    })
                elif field_type == 'integer' and not isinstance(value, int):
                    errors.append({
                        "row": row_idx + 1,
                        "field": field,
                        "error": "يجب أن يكون عدد صحيح",
                        "value": value
                    })
                elif field_type == 'boolean' and not isinstance(value, bool):
                    errors.append({
                        "row": row_idx + 1,
                        "field": field,
                        "error": "يجب أن يكون قيمة منطقية (صح/خطأ)",
                        "value": value
                    })
                elif field_type == 'date':
                    try:
                        if isinstance(value, str):
                            datetime.fromisoformat(value.replace('Z', '+00:00'))
                        else:
                            errors.append({
                                "row": row_idx + 1,
                                "field": field,
                                "error": "يجب أن يكون تاريخ بتنسيق ISO",
                                "value": value
                            })
                    except ValueError:
                        errors.append({
                            "row": row_idx + 1,
                            "field": field,
                            "error": "تنسيق التاريخ غير صالح",
                            "value": value
                        })

                # التحقق من القيم المسموح بها
                if 'enum' in field_schema and value not in field_schema['enum']:
                    errors.append({
                        "row": row_idx + 1,
                        "field": field,
                        "error": f"القيمة يجب أن تكون واحدة من: {', '.join(map(str, field_schema['enum']))}",
                        "value": value
                    })

                # التحقق من الحد الأدنى والأقصى للأرقام
                if field_type in ['number', 'integer']:
                    if 'minimum' in field_schema and value < field_schema['minimum']:
                        errors.append({
                            "row": row_idx + 1,
                            "field": field,
                            "error": f"القيمة يجب أن تكون أكبر من أو تساوي {field_schema['minimum']}",
                            "value": value
                        })
                    if 'maximum' in field_schema and value > field_schema['maximum']:
                        errors.append({
                            "row": row_idx + 1,
                            "field": field,
                            "error": f"القيمة يجب أن تكون أقل من أو تساوي {field_schema['maximum']}",
                            "value": value
                        })

                # التحقق من الحد الأدنى والأقصى لطول النصوص
                if field_type == 'string':
                    if 'minLength' in field_schema and len(value) < field_schema['minLength']:
                        errors.append({
                            "row": row_idx + 1,
                            "field": field,
                            "error": f"طول النص يجب أن يكون أكبر من أو يساوي {field_schema['minLength']}",
                            "value": value
                        })
                    if 'maxLength' in field_schema and len(value) > field_schema['maxLength']:
                        errors.append({
                            "row": row_idx + 1,
                            "field": field,
                            "error": f"طول النص يجب أن يكون أقل من أو يساوي {field_schema['maxLength']}",
                            "value": value
                        })
                    if 'pattern' in field_schema:
                        if not re.match(field_schema['pattern'], value):
                            errors.append({
                                "row": row_idx + 1,
                                "field": field,
                                "error": "النص لا يطابق النمط المطلوب",
                                "value": value
                            })

        # تسجيل الأخطاء في سجل النشاط إذا وجدت
        if errors:
            try:
                user_id = get_current_user_id()
            except Exception:  # pylint: disable=broad-except
                user_id = None

            self.error_logger.log_application_error(
                error=ImportValidationError("أخطاء في التحقق من صحة البيانات المستوردة", errors),
                module_name=MODULE_NAME,
                function_name="validate_import_data",
                user_id=user_id,
                additional_context={
                    "entity_type": entity_type,
                    "error_count": len(errors),
                    "data_count": len(data)
                }
            )

        return len(errors) == 0, errors

    @log_errors(module_name=MODULE_NAME)
    def generate_error_report(self, errors: List[Dict[str, Any]], report_format: str = 'excel') -> str:
        """
        إنشاء تقرير بالأخطاء

        Args:
            errors: قائمة بالأخطاء
            report_format: تنسيق التقرير (excel, csv, json)

        Returns:
            str: مسار ملف التقرير
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')
        os.makedirs(output_dir, exist_ok=True)

        if report_format == 'excel':
            output_path = os.path.join(output_dir, f'import_errors_{timestamp}.xlsx')
            df = pd.DataFrame(errors)
            df.to_excel(output_path, index=False)
        elif report_format == 'csv':
            output_path = os.path.join(output_dir, f'import_errors_{timestamp}.csv')
            df = pd.DataFrame(errors)
            df.to_csv(output_path, index=False)
        elif report_format == 'json':
            output_path = os.path.join(output_dir, f'import_errors_{timestamp}.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(errors, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"تنسيق غير مدعوم: {report_format}")

        return output_path

    @log_errors(module_name=MODULE_NAME)
    def validate_export_request(self, entity_type: str, filters: Dict = None, fields: List[str] = None) -> Tuple[bool, Optional[str]]:
        """
        التحقق من صحة طلب التصدير

        Args:
            entity_type: نوع الكيان المراد تصديره
            filters: مرشحات التصدير (اختياري)
            fields: الحقول المراد تصديرها (اختياري)

        Returns:
            tuple: (صحيح/خطأ، رسالة الخطأ إذا وجدت)
        """
        # التحقق من نوع الكيان
        valid_entity_types = [
            'users', 'customers', 'products', 'orders', 'invoices',
            'inventory', 'suppliers', 'employees', 'transactions',
            'farms', 'plants', 'seeds', 'experiments', 'diagnoses'
        ]

        if entity_type not in valid_entity_types:
            error_message = f"نوع الكيان غير صالح: {entity_type}. الأنواع الصالحة هي: {', '.join(valid_entity_types)}"

            # تسجيل الخطأ في سجل النشاط
            try:
                user_id = get_current_user_id()
            except Exception:  # pylint: disable=broad-except
                user_id = None

            self.error_logger.log_application_error(
                error=ExportValidationError(error_message),
                module_name=MODULE_NAME,
                function_name="validate_export_request",
                user_id=user_id,
                additional_context={
                    "entity_type": entity_type,
                    "filters": filters,
                    "fields": fields
                }
            )

            return False, error_message

        # يمكن إضافة المزيد من التحققات هنا حسب الحاجة

        return True, None


# إنشاء مثيل واحد من مدقق البيانات للاستخدام في جميع أنحاء التطبيق
_data_validator_instance = None


def get_data_validator() -> DataValidator:
    """
    الحصول على مثيل مدقق البيانات

    Returns:
        DataValidator: مثيل مدقق البيانات
    """
    global _data_validator_instance  # pylint: disable=global-statement
    if _data_validator_instance is None:
        _data_validator_instance = DataValidator()
    return _data_validator_instance
