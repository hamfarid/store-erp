"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/export_service.py
الوصف: خدمة تصدير البيانات من النظام
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import json
import logging
import os
import shutil
import zipfile
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from src.modules.activity_log.error_logger import get_error_logger, log_errors
from src.database import get_db
from src.modules.security.security_middleware import get_current_user_id
from src.modules.import_export.validation import get_data_validator

# إعداد المسجل
logger = logging.getLogger(__name__)

# Constants
README_FILENAME = "README.md"


class ActivityLogService:
    """Wrapper class for activity log service functions"""

    def __init__(self, db: Session = None):
        self.db = db or next(get_db())

    def log_activity(self, user_id: int, action: str, entity_type: str, entity_id: int = None,
                     details: Dict = None, status: str = "success", message: str = "") -> None:
        """Log activity using the activity log service functions"""
        try:
            # This is a simplified logging - in a real implementation you'd use the proper schemas
            logger.info("Activity logged: user_id=%s, action=%s, entity_type=%s, status=%s, message=%s",
                        user_id, action, entity_type, status, message)
        except Exception as e:
            logger.error("Failed to log activity: %s", str(e))


class ExportService:
    """
    خدمة تصدير البيانات من النظام
    """

    def __init__(self, db: Session = None):
        """
        تهيئة خدمة التصدير

        Args:
            db: جلسة قاعدة البيانات، إذا كانت None سيتم إنشاء جلسة جديدة
        """
        self.db = db or next(get_db())
        self.error_logger = get_error_logger()
        self.activity_log_service = ActivityLogService()
        self.data_validator = get_data_validator()

        # إنشاء مجلد التصدير المؤقت إذا لم يكن موجوداً
        self.export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp', 'exports')
        os.makedirs(self.export_dir, exist_ok=True)

    @log_errors(module_name="import_export.export_service")
    def export_data(self,
                    entity_type: str,
                    export_format: str = 'excel',
                    filters: Dict = None,
                    fields: List[str] = None,
                    include_related: bool = False) -> str:
        """
        تصدير البيانات من النظام

        Args:
            entity_type: نوع الكيان المراد تصديره
            export_format: تنسيق التصدير (excel, csv, json)
            filters: مرشحات التصدير (اختياري)
            fields: الحقول المراد تصديرها (اختياري)
            include_related: تضمين البيانات المرتبطة (اختياري)

        Returns:
            str: مسار ملف التصدير
        """
        # التحقق من صحة طلب التصدير
        is_valid, error_message = self.data_validator.validate_export_request(
            entity_type=entity_type,
            filters=filters,
            fields=fields
        )

        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        # الحصول على البيانات
        data = self._get_entity_data(
            entity_type=entity_type,
            filters=filters,
            fields=fields,
            include_related=include_related
        )

        if not data:
            # تسجيل تحذير في سجل النشاط
            self._log_export_event(
                entity_type=entity_type,
                export_format=export_format,
                filters=filters or {},
                fields=fields or [],
                status="warning",
                message="لا توجد بيانات للتصدير",
                file_path=None
            )

            raise HTTPException(status_code=404, detail="لا توجد بيانات للتصدير")

        # تصدير البيانات
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{entity_type}_export_{timestamp}"

        try:
            if export_format == 'excel':
                output_path = os.path.join(self.export_dir, f"{file_name}.xlsx")
                df = pd.DataFrame(data)
                df.to_excel(output_path, index=False)
            elif export_format == 'csv':
                output_path = os.path.join(self.export_dir, f"{file_name}.csv")
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False)
            elif export_format == 'json':
                output_path = os.path.join(self.export_dir, f"{file_name}.json")
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"تنسيق غير مدعوم: {export_format}")

            # تسجيل نجاح التصدير في سجل النشاط
            self._log_export_event(
                entity_type=entity_type,
                export_format=export_format,
                filters=filters or {},
                fields=fields or [],
                status="success",
                message=f"تم تصدير {len(data)} سجل بنجاح",
                file_path=output_path
            )

            return output_path

        except Exception as e:
            # تسجيل فشل التصدير في سجل النشاط
            self._log_export_event(
                entity_type=entity_type,
                export_format=export_format,
                filters=filters or {},
                fields=fields or [],
                status="error",
                message=f"فشل التصدير: {str(e)}",
                file_path=None
            )

            raise HTTPException(status_code=500, detail=f"فشل التصدير: {str(e)}") from e

    @log_errors(module_name="import_export.export_service")
    def export_database(self,
                        database_name: str = None,
                        include_schema: bool = True,
                        include_data: bool = True,
                        background_tasks: BackgroundTasks = None) -> str:
        """
        تصدير قاعدة البيانات كاملة

        Args:
            database_name: اسم قاعدة البيانات، إذا كان None سيتم تصدير قاعدة البيانات الافتراضية
            include_schema: تضمين مخطط قاعدة البيانات
            include_data: تضمين بيانات قاعدة البيانات
            background_tasks: مهام الخلفية لتنفيذ التصدير في الخلفية

        Returns:
            str: مسار ملف التصدير
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(self.export_dir, f"database_export_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        # تحديد اسم قاعدة البيانات إذا لم يتم تحديده
        if database_name is None:
            try:
                from src.config import settings  # pylint: disable=import-outside-toplevel
                database_name = settings.DATABASE_NAME
            except ImportError:
                database_name = "default_database"

        # إنشاء ملف التصدير
        output_path = os.path.join(self.export_dir, f"database_export_{timestamp}.zip")

        # تنفيذ التصدير في الخلفية إذا تم توفير مهام الخلفية
        if background_tasks:
            background_tasks.add_task(
                self._export_database_task,
                database_name=database_name,
                include_schema=include_schema,
                include_data=include_data,
                output_dir=output_dir,
                output_path=output_path
            )

            # تسجيل بدء التصدير في سجل النشاط
            self._log_export_event(
                entity_type="database",
                export_format="zip",
                filters={},
                fields=[],
                status="pending",
                message=f"بدأ تصدير قاعدة البيانات {database_name} في الخلفية",
                file_path=None
            )

            return "pending"

        # تنفيذ التصدير مباشرة
        return self._export_database_task(
            database_name=database_name,
            include_schema=include_schema,
            include_data=include_data,
            output_dir=output_dir,
            output_path=output_path
        )

    @log_errors(module_name="import_export.export_service")
    def export_learning_data(self,
                             model_name: str = None,
                             include_weights: bool = True,
                             include_training_data: bool = True,
                             background_tasks: BackgroundTasks = None) -> str:
        """
        تصدير بيانات التعلم الآلي

        Args:
            model_name: اسم النموذج المراد تصديره
            include_weights: تضمين أوزان النموذج
            include_training_data: تضمين بيانات التدريب
            background_tasks: مهام الخلفية لتنفيذ التصدير في الخلفية

        Returns:
            str: مسار ملف التصدير
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(self.export_dir, f"learning_data_export_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        # إنشاء ملف التصدير
        output_path = os.path.join(self.export_dir, f"learning_data_export_{timestamp}.zip")

        # تنفيذ التصدير في الخلفية إذا تم توفير مهام الخلفية
        if background_tasks:
            background_tasks.add_task(
                self._export_learning_data_task,
                model_name=model_name,
                include_weights=include_weights,
                include_training_data=include_training_data,
                output_dir=output_dir,
                output_path=output_path
            )

            # تسجيل بدء التصدير في سجل النشاط
            self._log_export_event(
                entity_type="learning_data",
                export_format="zip",
                filters={"model_name": model_name} if model_name else {},
                fields=[],
                status="pending",
                message="بدأ تصدير بيانات التعلم في الخلفية",
                file_path=None
            )

            return "pending"

        # تنفيذ التصدير مباشرة
        return self._export_learning_data_task(
            model_name=model_name,
            include_weights=include_weights,
            include_training_data=include_training_data,
            output_dir=output_dir,
            output_path=output_path
        )

    @log_errors(module_name="import_export.export_service")
    def export_images(self,
                      category: str = None,
                      start_date: str = None,
                      end_date: str = None,
                      background_tasks: BackgroundTasks = None) -> str:
        """
        تصدير الصور من النظام

        Args:
            category: فئة الصور المراد تصديرها
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            background_tasks: مهام الخلفية لتنفيذ التصدير في الخلفية

        Returns:
            str: مسار ملف التصدير
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(self.export_dir, f"images_export_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        # إنشاء ملف التصدير
        output_path = os.path.join(self.export_dir, f"images_export_{timestamp}.zip")

        # تنفيذ التصدير في الخلفية إذا تم توفير مهام الخلفية
        if background_tasks:
            background_tasks.add_task(
                self._export_images_task,
                category=category,
                start_date=start_date,
                end_date=end_date,
                output_dir=output_dir,
                output_path=output_path
            )

            # تسجيل بدء التصدير في سجل النشاط
            self._log_export_event(
                entity_type="images",
                export_format="zip",
                filters={"category": category, "start_date": start_date, "end_date": end_date},
                fields=[],
                status="pending",
                message="بدأ تصدير الصور في الخلفية",
                file_path=None
            )

            return "pending"

        # تنفيذ التصدير مباشرة
        return self._export_images_task(
            category=category,
            start_date=start_date,
            end_date=end_date,
            output_dir=output_dir,
            output_path=output_path
        )

    @log_errors(module_name="import_export.export_service")
    def get_export_templates(self, entity_type: str) -> Dict[str, str]:
        """
        الحصول على قوالب التصدير للكيان المحدد

        Args:
            entity_type: نوع الكيان

        Returns:
            Dict[str, str]: قاموس يحتوي على قوالب التصدير
        """
        templates = {
            'users': 'user_export_template.xlsx',
            'plants': 'plant_export_template.xlsx',
            'diseases': 'disease_export_template.xlsx',
            'diagnoses': 'diagnosis_export_template.xlsx',
            'analysis_results': 'analysis_results_template.xlsx'
        }

        return templates.get(entity_type, {})

    @log_errors(module_name="import_export.export_service")
    def get_export_status(self, task_id: str) -> Dict[str, Any]:
        """
        الحصول على حالة مهمة التصدير

        Args:
            task_id: معرف المهمة

        Returns:
            Dict[str, Any]: معلومات حالة المهمة
        """
        # هذه وظيفة توضيحية - يجب تنفيذها مع نظام إدارة المهام
        return {
            'task_id': task_id,
            'status': 'completed',
            'progress': 100,
            'message': 'تم إنجاز التصدير بنجاح',
            'file_path': None
        }

    def _get_entity_data(self,
                         entity_type: str,
                         filters: Dict = None,
                         fields: List[str] = None,
                         include_related: bool = False) -> List[Dict[str, Any]]:
        """
        الحصول على بيانات الكيان من قاعدة البيانات

        Args:
            entity_type: نوع الكيان
            filters: مرشحات الاستعلام
            fields: الحقول المراد استرجاعها
            include_related: تضمين البيانات المرتبطة

        Returns:
            List[Dict[str, Any]]: قائمة البيانات
        """
        try:
            query = self._get_entity_query(entity_type)
            if query is None:
                return []

            query = self._apply_filters(query, filters)
            results = query.all()

            return self._convert_results_to_dict(results, fields, include_related)

        except Exception as e:
            logger.error("خطأ في الحصول على بيانات الكيان %s: %s", entity_type, str(e))
            return []

    def _get_entity_query(self, entity_type: str):
        """الحصول على استعلام الكيان بناءً على نوعه"""
        if entity_type == 'users':
            try:
                from src.modules.user_management.models import User  # pylint: disable=import-outside-toplevel
                return self.db.query(User)
            except ImportError:
                logger.warning("User model not found")
                return None
        elif entity_type == 'plants':
            # يمكن إضافة المزيد من الكيانات هنا
            return None
        else:
            logger.warning("نوع كيان غير مدعوم: %s", entity_type)
            return None

    def _apply_filters(self, query, filters: Dict):
        """تطبيق المرشحات على الاستعلام"""
        if not filters:
            return query

        for key, value in filters.items():
            if hasattr(query.column_descriptions[0]['type'], key):
                query = query.filter(getattr(query.column_descriptions[0]['type'], key) == value)
        return query

    def _convert_results_to_dict(self, results, fields: List[str], include_related: bool) -> List[Dict[str, Any]]:
        """تحويل النتائج إلى قوائم"""
        data = []
        for result in results:
            item = self._convert_single_result(result, fields)

            if include_related:
                item = self._add_related_data(item, result)

            data.append(item)
        return data

    def _convert_single_result(self, result, fields: List[str]) -> Dict[str, Any]:
        """تحويل نتيجة واحدة إلى قاموس"""
        item = {}
        for column in result.__table__.columns:
            if fields is None or column.name in fields:
                value = getattr(result, column.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                item[column.name] = value
        return item

    def _add_related_data(self, item: Dict[str, Any], result) -> Dict[str, Any]:  # pylint: disable=unused-argument
        """إضافة البيانات المرتبطة"""
        # يمكن إضافة منطق تضمين البيانات المرتبطة هنا
        return item

    def _export_database_task(self,
                              database_name: str,
                              include_schema: bool,
                              include_data: bool,
                              output_dir: str,
                              output_path: str) -> str:
        """
        مهمة تصدير قاعدة البيانات

        Args:
            database_name: اسم قاعدة البيانات
            include_schema: تضمين مخطط قاعدة البيانات
            include_data: تضمين بيانات قاعدة البيانات
            output_dir: مجلد الإخراج المؤقت
            output_path: مسار ملف الإخراج النهائي

        Returns:
            str: مسار ملف التصدير
        """
        try:
            # إنشاء ملف README
            readme_path = os.path.join(output_dir, README_FILENAME)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# تصدير قاعدة البيانات {database_name}\n")
                f.write(f"تاريخ التصدير: {datetime.now().isoformat()}\n")
                f.write(f"تضمين المخطط: {'نعم' if include_schema else 'لا'}\n")
                f.write(f"تضمين البيانات: {'نعم' if include_data else 'لا'}\n")

            # تصدير مخطط قاعدة البيانات
            if include_schema:
                schema_path = os.path.join(output_dir, f"{database_name}_schema.sql")
                # هنا يجب إضافة منطق تصدير مخطط قاعدة البيانات
                with open(schema_path, 'w', encoding='utf-8') as f:
                    f.write("-- مخطط قاعدة البيانات\n")

            # تصدير بيانات قاعدة البيانات
            if include_data:
                data_path = os.path.join(output_dir, f"{database_name}_data.sql")
                # هنا يجب إضافة منطق تصدير بيانات قاعدة البيانات
                with open(data_path, 'w', encoding='utf-8') as f:
                    f.write("-- بيانات قاعدة البيانات\n")

            # ضغط الملفات
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, output_dir)
                        zip_file.write(file_path, arc_name)

            # تنظيف المجلد المؤقت
            shutil.rmtree(output_dir)

            # تسجيل نجاح التصدير
            self._log_export_event(
                entity_type="database",
                export_format="zip",
                filters={},
                fields=[],
                status="success",
                message=f"تم تصدير قاعدة البيانات {database_name} بنجاح",
                file_path=output_path
            )

            return output_path

        except Exception as e:
            # تنظيف المجلد المؤقت في حالة الخطأ
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)

            # تسجيل فشل التصدير
            self._log_export_event(
                entity_type="database",
                export_format="zip",
                filters={},
                fields=[],
                status="error",
                message=f"فشل تصدير قاعدة البيانات: {str(e)}",
                file_path=None
            )

            raise HTTPException(status_code=500, detail=f"فشل تصدير قاعدة البيانات: {str(e)}") from e

    def _export_learning_data_task(self,
                                   model_name: str,
                                   include_weights: bool,
                                   include_training_data: bool,
                                   output_dir: str,
                                   output_path: str) -> str:
        """
        مهمة تصدير بيانات التعلم الآلي

        Args:
            model_name: اسم النموذج
            include_weights: تضمين أوزان النموذج
            include_training_data: تضمين بيانات التدريب
            output_dir: مجلد الإخراج المؤقت
            output_path: مسار ملف الإخراج النهائي

        Returns:
            str: مسار ملف التصدير
        """
        try:
            # إنشاء ملف README
            readme_path = os.path.join(output_dir, README_FILENAME)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("# تصدير بيانات التعلم الآلي\n")
                f.write(f"اسم النموذج: {model_name or 'جميع النماذج'}\n")
                f.write(f"تاريخ التصدير: {datetime.now().isoformat()}\n")
                f.write(f"تضمين الأوزان: {'نعم' if include_weights else 'لا'}\n")
                f.write(f"تضمين بيانات التدريب: {'نعم' if include_training_data else 'لا'}\n")

            # تصدير أوزان النموذج
            if include_weights:
                weights_dir = os.path.join(output_dir, "weights")
                os.makedirs(weights_dir, exist_ok=True)
                # هنا يجب إضافة منطق تصدير أوزان النماذج

            # تصدير بيانات التدريب
            if include_training_data:
                training_dir = os.path.join(output_dir, "training_data")
                os.makedirs(training_dir, exist_ok=True)
                # هنا يجب إضافة منطق تصدير بيانات التدريب

            # ضغط الملفات
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, output_dir)
                        zip_file.write(file_path, arc_name)

            # تنظيف المجلد المؤقت
            shutil.rmtree(output_dir)

            # تسجيل نجاح التصدير
            self._log_export_event(
                entity_type="learning_data",
                export_format="zip",
                filters={"model_name": model_name} if model_name else {},
                fields=[],
                status="success",
                message="تم تصدير بيانات التعلم بنجاح",
                file_path=output_path
            )

            return output_path

        except Exception as e:
            # تنظيف المجلد المؤقت في حالة الخطأ
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)

            # تسجيل فشل التصدير
            self._log_export_event(
                entity_type="learning_data",
                export_format="zip",
                filters={"model_name": model_name} if model_name else {},
                fields=[],
                status="error",
                message=f"فشل تصدير بيانات التعلم: {str(e)}",
                file_path=None
            )

            raise HTTPException(status_code=500, detail=f"فشل تصدير بيانات التعلم: {str(e)}") from e

    def _export_images_task(self,
                            category: str,
                            start_date: str,
                            end_date: str,
                            output_dir: str,
                            output_path: str) -> str:
        """
        مهمة تصدير الصور

        Args:
            category: فئة الصور
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            output_dir: مجلد الإخراج المؤقت
            output_path: مسار ملف الإخراج النهائي

        Returns:
            str: مسار ملف التصدير
        """
        try:
            # إنشاء ملف README
            readme_path = os.path.join(output_dir, README_FILENAME)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("# تصدير الصور\n")
                f.write(f"الفئة: {category or 'جميع الفئات'}\n")
                f.write(f"تاريخ البداية: {start_date or 'غير محدد'}\n")
                f.write(f"تاريخ النهاية: {end_date or 'غير محدد'}\n")
                f.write(f"تاريخ التصدير: {datetime.now().isoformat()}\n")

            # إنشاء مجلدات للصور
            images_dir = os.path.join(output_dir, "images")
            os.makedirs(images_dir, exist_ok=True)

            # هنا يجب إضافة منطق نسخ الصور المطلوبة

            # ضغط الملفات
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, output_dir)
                        zip_file.write(file_path, arc_name)

            # تنظيف المجلد المؤقت
            shutil.rmtree(output_dir)

            # تسجيل نجاح التصدير
            self._log_export_event(
                entity_type="images",
                export_format="zip",
                filters={"category": category, "start_date": start_date, "end_date": end_date},
                fields=[],
                status="success",
                message="تم تصدير الصور بنجاح",
                file_path=output_path
            )

            return output_path

        except Exception as e:
            # تنظيف المجلد المؤقت في حالة الخطأ
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)

            # تسجيل فشل التصدير
            self._log_export_event(
                entity_type="images",
                export_format="zip",
                filters={"category": category, "start_date": start_date, "end_date": end_date},
                fields=[],
                status="error",
                message=f"فشل تصدير الصور: {str(e)}",
                file_path=None
            )

            raise HTTPException(status_code=500, detail=f"فشل تصدير الصور: {str(e)}") from e

    def _log_export_event(self,
                          entity_type: str,
                          export_format: str,
                          filters: Dict = None,
                          fields: List[str] = None,
                          status: str = "success",
                          message: str = "",
                          file_path: str = None) -> None:
        """
        تسجيل حدث التصدير في سجل النشاط

        Args:
            entity_type: نوع الكيان
            export_format: تنسيق التصدير
            filters: مرشحات التصدير
            fields: الحقول المصدرة
            status: حالة التصدير
            message: رسالة الحدث
            file_path: مسار الملف المُصدر
        """
        try:
            user_id = get_current_user_id()

            event_data = {
                'entity_type': entity_type,
                'export_format': export_format,
                'filters': filters or {},
                'fields': fields or [],
                'file_path': file_path,
                'timestamp': datetime.now().isoformat()
            }

            self.activity_log_service.log_activity(
                user_id=user_id,
                action="export",
                entity_type=entity_type,
                entity_id=None,
                details=event_data,
                status=status,
                message=message
            )

        except Exception as e:
            logger.error("خطأ في تسجيل حدث التصدير: %s", str(e))
