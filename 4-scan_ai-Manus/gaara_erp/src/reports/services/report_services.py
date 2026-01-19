"""
خدمات وحدة التقارير
يحتوي هذا الملف على خدمات وحدة التقارير
"""

import os
import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import jinja2
import pdfkit
import xlsxwriter
import csv
from uuid import uuid4
import re
from io import BytesIO

from ..models.report_models import (
    ReportTemplate, Report, ScheduledReport, ReportDashboard,
    ReportType, ReportFormat, ReportFrequency, ReportStatus
)


class ReportService:
    """خدمة التقارير"""
    
    def __init__(self, db_manager, config=None):
        """تهيئة خدمة التقارير"""
        self.db_manager = db_manager
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # مسار حفظ التقارير
        self.reports_dir = self.config.get("reports_dir", "/tmp/reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # مسار قوالب التقارير
        self.templates_dir = self.config.get("templates_dir", "/tmp/report_templates")
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # تهيئة محرك القوالب
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    
    def create_report_template(self, template_data: Dict[str, Any]) -> ReportTemplate:
        """إنشاء قالب تقرير جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["name", "description", "report_type", "query_template", "parameters", "created_by"]
        for field in required_fields:
            if field not in template_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من نوع التقرير
        if isinstance(template_data["report_type"], str):
            try:
                template_data["report_type"] = ReportType(template_data["report_type"])
            except ValueError:
                raise ValueError(f"نوع التقرير غير صالح: {template_data['report_type']}")
        
        # إنشاء قالب تقرير جديد
        report_template = ReportTemplate(
            name=template_data["name"],
            description=template_data["description"],
            report_type=template_data["report_type"],
            query_template=template_data["query_template"],
            parameters=template_data["parameters"],
            created_by=template_data["created_by"],
            is_system=template_data.get("is_system", False),
            is_active=template_data.get("is_active", True)
        )
        
        # حفظ قالب التقرير في قاعدة البيانات
        self._save_report_template(report_template)
        
        return report_template
    
    def _save_report_template(self, report_template: ReportTemplate) -> None:
        """حفظ قالب تقرير في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            template_dict = report_template.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO report_templates (
                    template_id, name, description, report_type, query_template,
                    parameters, created_by, is_system, is_active, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                template_dict["template_id"],
                template_dict["name"],
                template_dict["description"],
                template_dict["report_type"],
                template_dict["query_template"],
                json.dumps(template_dict["parameters"]),
                template_dict["created_by"],
                template_dict["is_system"],
                template_dict["is_active"],
                template_dict["created_at"],
                template_dict["updated_at"]
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ قالب التقرير: {str(e)}")
            raise
    
    def get_report_template(self, template_id: str) -> Optional[ReportTemplate]:
        """الحصول على قالب تقرير بواسطة المعرف"""
        try:
            query = """
                SELECT template_id, name, description, report_type, query_template,
                       parameters, created_by, is_system, is_active, created_at, updated_at
                FROM report_templates
                WHERE template_id = %s
            """
            
            result = self.db_manager.execute_query(query, (template_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            template_dict = {
                "template_id": result[0],
                "name": result[1],
                "description": result[2],
                "report_type": result[3],
                "query_template": result[4],
                "parameters": json.loads(result[5]) if result[5] else {},
                "created_by": result[6],
                "is_system": result[7],
                "is_active": result[8],
                "created_at": result[9],
                "updated_at": result[10]
            }
            
            return ReportTemplate.from_dict(template_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قالب التقرير: {str(e)}")
            return None
    
    def get_all_report_templates(
        self,
        report_type: Optional[ReportType] = None,
        is_system: Optional[bool] = None,
        is_active: Optional[bool] = None,
        created_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ReportTemplate], int]:
        """الحصول على جميع قوالب التقارير"""
        try:
            # بناء الاستعلام
            query = """
                SELECT template_id, name, description, report_type, query_template,
                       parameters, created_by, is_system, is_active, created_at, updated_at
                FROM report_templates
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM report_templates
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if report_type:
                query += " AND report_type = %s"
                count_query += " AND report_type = %s"
                params.append(report_type.value)
            
            if is_system is not None:
                query += " AND is_system = %s"
                count_query += " AND is_system = %s"
                params.append(is_system)
            
            if is_active is not None:
                query += " AND is_active = %s"
                count_query += " AND is_active = %s"
                params.append(is_active)
            
            if created_by:
                query += " AND created_by = %s"
                count_query += " AND created_by = %s"
                params.append(created_by)
            
            # إضافة الترتيب والحد
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # تنفيذ استعلام العدد
            count_result = self.db_manager.execute_query(count_query, params[:-2], fetch_one=True)
            total = count_result[0] if count_result else 0
            
            # تنفيذ استعلام البيانات
            results = self.db_manager.execute_query(query, params)
            
            # تحويل النتائج إلى كائنات
            templates = []
            for result in results:
                template_dict = {
                    "template_id": result[0],
                    "name": result[1],
                    "description": result[2],
                    "report_type": result[3],
                    "query_template": result[4],
                    "parameters": json.loads(result[5]) if result[5] else {},
                    "created_by": result[6],
                    "is_system": result[7],
                    "is_active": result[8],
                    "created_at": result[9],
                    "updated_at": result[10]
                }
                
                templates.append(ReportTemplate.from_dict(template_dict))
            
            return templates, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قوالب التقارير: {str(e)}")
            return [], 0
    
    def update_report_template(self, template_id: str, template_data: Dict[str, Any]) -> Optional[ReportTemplate]:
        """تحديث قالب تقرير"""
        try:
            # الحصول على قالب التقرير الحالي
            current_template = self.get_report_template(template_id)
            if not current_template:
                return None
            
            # تحديث البيانات
            if "name" in template_data:
                current_template.name = template_data["name"]
            
            if "description" in template_data:
                current_template.description = template_data["description"]
            
            if "report_type" in template_data:
                if isinstance(template_data["report_type"], str):
                    try:
                        current_template.report_type = ReportType(template_data["report_type"])
                    except ValueError:
                        raise ValueError(f"نوع التقرير غير صالح: {template_data['report_type']}")
                else:
                    current_template.report_type = template_data["report_type"]
            
            if "query_template" in template_data:
                current_template.query_template = template_data["query_template"]
            
            if "parameters" in template_data:
                current_template.parameters = template_data["parameters"]
            
            if "is_active" in template_data:
                current_template.is_active = template_data["is_active"]
            
            # تحديث وقت التحديث
            current_template.updated_at = datetime.now()
            
            # حفظ التغييرات في قاعدة البيانات
            query = """
                UPDATE report_templates
                SET name = %s, description = %s, report_type = %s, query_template = %s,
                    parameters = %s, is_active = %s, updated_at = %s
                WHERE template_id = %s
            """
            
            params = (
                current_template.name,
                current_template.description,
                current_template.report_type.value,
                current_template.query_template,
                json.dumps(current_template.parameters),
                current_template.is_active,
                current_template.updated_at,
                template_id
            )
            
            self.db_manager.execute_query(query, params)
            
            return current_template
        except Exception as e:
            self.logger.error(f"خطأ في تحديث قالب التقرير: {str(e)}")
            raise
    
    def delete_report_template(self, template_id: str) -> bool:
        """حذف قالب تقرير"""
        try:
            # التحقق من وجود قالب التقرير
            current_template = self.get_report_template(template_id)
            if not current_template:
                return False
            
            # التحقق من أن القالب ليس قالبًا نظاميًا
            if current_template.is_system:
                raise ValueError("لا يمكن حذف قوالب التقارير النظامية")
            
            # حذف قالب التقرير
            query = """
                DELETE FROM report_templates
                WHERE template_id = %s
            """
            
            self.db_manager.execute_query(query, (template_id,))
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف قالب التقرير: {str(e)}")
            raise
    
    def create_report(self, report_data: Dict[str, Any]) -> Report:
        """إنشاء تقرير جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["template_id", "parameters", "created_by"]
        for field in required_fields:
            if field not in report_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من وجود قالب التقرير
        template = self.get_report_template(report_data["template_id"])
        if not template:
            raise ValueError(f"قالب التقرير غير موجود: {report_data['template_id']}")
        
        # التحقق من أن قالب التقرير نشط
        if not template.is_active:
            raise ValueError(f"قالب التقرير غير نشط: {report_data['template_id']}")
        
        # التحقق من صيغة التقرير
        report_format = report_data.get("report_format")
        if report_format:
            if isinstance(report_format, str):
                try:
                    report_format = ReportFormat(report_format)
                except ValueError:
                    raise ValueError(f"صيغة التقرير غير صالحة: {report_format}")
        else:
            report_format = ReportFormat.PDF
        
        # إنشاء تقرير جديد
        report = Report(
            template_id=report_data["template_id"],
            parameters=report_data["parameters"],
            created_by=report_data["created_by"],
            report_format=report_format
        )
        
        # حفظ التقرير في قاعدة البيانات
        self._save_report(report)
        
        return report
    
    def _save_report(self, report: Report) -> None:
        """حفظ تقرير في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            report_dict = report.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO reports (
                    report_id, template_id, parameters, created_by, report_format,
                    status, file_path, error_message, created_at, updated_at, completed_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                report_dict["report_id"],
                report_dict["template_id"],
                json.dumps(report_dict["parameters"]),
                report_dict["created_by"],
                report_dict["report_format"],
                report_dict["status"],
                report_dict["file_path"],
                report_dict["error_message"],
                report_dict["created_at"],
                report_dict["updated_at"],
                report_dict.get("completed_at")
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ التقرير: {str(e)}")
            raise
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """الحصول على تقرير بواسطة المعرف"""
        try:
            query = """
                SELECT report_id, template_id, parameters, created_by, report_format,
                       status, file_path, error_message, created_at, updated_at, completed_at
                FROM reports
                WHERE report_id = %s
            """
            
            result = self.db_manager.execute_query(query, (report_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            report_dict = {
                "report_id": result[0],
                "template_id": result[1],
                "parameters": json.loads(result[2]) if result[2] else {},
                "created_by": result[3],
                "report_format": result[4],
                "status": result[5],
                "file_path": result[6],
                "error_message": result[7],
                "created_at": result[8],
                "updated_at": result[9],
                "completed_at": result[10]
            }
            
            return Report.from_dict(report_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على التقرير: {str(e)}")
            return None
    
    def get_all_reports(
        self,
        template_id: Optional[str] = None,
        created_by: Optional[str] = None,
        status: Optional[ReportStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[Report], int]:
        """الحصول على جميع التقارير"""
        try:
            # بناء الاستعلام
            query = """
                SELECT report_id, template_id, parameters, created_by, report_format,
                       status, file_path, error_message, created_at, updated_at, completed_at
                FROM reports
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM reports
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if template_id:
                query += " AND template_id = %s"
                count_query += " AND template_id = %s"
                params.append(template_id)
            
            if created_by:
                query += " AND created_by = %s"
                count_query += " AND created_by = %s"
                params.append(created_by)
            
            if status:
                query += " AND status = %s"
                count_query += " AND status = %s"
                params.append(status.value)
            
            # إضافة الترتيب والحد
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # تنفيذ استعلام العدد
            count_result = self.db_manager.execute_query(count_query, params[:-2], fetch_one=True)
            total = count_result[0] if count_result else 0
            
            # تنفيذ استعلام البيانات
            results = self.db_manager.execute_query(query, params)
            
            # تحويل النتائج إلى كائنات
            reports = []
            for result in results:
                report_dict = {
                    "report_id": result[0],
                    "template_id": result[1],
                    "parameters": json.loads(result[2]) if result[2] else {},
                    "created_by": result[3],
                    "report_format": result[4],
                    "status": result[5],
                    "file_path": result[6],
                    "error_message": result[7],
                    "created_at": result[8],
                    "updated_at": result[9],
                    "completed_at": result[10]
                }
                
                reports.append(Report.from_dict(report_dict))
            
            return reports, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على التقارير: {str(e)}")
            return [], 0
    
    def generate_report(self, report_id: str) -> bool:
        """توليد تقرير"""
        try:
            # الحصول على التقرير
            report = self.get_report(report_id)
            if not report:
                self.logger.error(f"لم يتم العثور على التقرير بالمعرف {report_id}")
                return False
            
            # التحقق من أن التقرير في حالة قيد الانتظار
            if report.status != ReportStatus.PENDING:
                self.logger.error(f"لا يمكن توليد التقرير لأنه في حالة {report.status.value}")
                return False
            
            # تحديث حالة التقرير إلى قيد الإنشاء
            self._update_report_status(report_id, ReportStatus.GENERATING)
            
            # الحصول على قالب التقرير
            template = self.get_report_template(report.template_id)
            if not template:
                self.logger.error(f"لم يتم العثور على قالب التقرير بالمعرف {report.template_id}")
                self._update_report_status(report_id, ReportStatus.FAILED, "قالب التقرير غير موجود")
                return False
            
            # تنفيذ استعلام التقرير
            try:
                data = self._execute_report_query(template.query_template, report.parameters)
            except Exception as e:
                self.logger.error(f"خطأ في تنفيذ استعلام التقرير: {str(e)}")
                self._update_report_status(report_id, ReportStatus.FAILED, f"خطأ في تنفيذ استعلام التقرير: {str(e)}")
                return False
            
            # توليد التقرير بالصيغة المطلوبة
            try:
                file_path = self._generate_report_file(report, template, data)
            except Exception as e:
                self.logger.error(f"خطأ في توليد ملف التقرير: {str(e)}")
                self._update_report_status(report_id, ReportStatus.FAILED, f"خطأ في توليد ملف التقرير: {str(e)}")
                return False
            
            # تحديث حالة التقرير إلى مكتمل
            self._update_report_status(report_id, ReportStatus.COMPLETED, file_path=file_path)
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في توليد التقرير: {str(e)}")
            self._update_report_status(report_id, ReportStatus.FAILED, str(e))
            return False
    
    def _update_report_status(
        self,
        report_id: str,
        status: ReportStatus,
        error_message: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> None:
        """تحديث حالة تقرير"""
        try:
            # بناء الاستعلام
            query = """
                UPDATE reports
                SET status = %s, updated_at = %s
            """
            
            params = [status.value, datetime.now()]
            
            # إضافة رسالة الخطأ إذا تم توفيرها
            if error_message is not None:
                query += ", error_message = %s"
                params.append(error_message)
            
            # إضافة مسار الملف إذا تم توفيره
            if file_path is not None:
                query += ", file_path = %s"
                params.append(file_path)
            
            # إضافة وقت الاكتمال إذا كانت الحالة مكتملة
            if status == ReportStatus.COMPLETED:
                query += ", completed_at = %s"
                params.append(datetime.now())
            
            # إضافة شرط المعرف
            query += " WHERE report_id = %s"
            params.append(report_id)
            
            # تنفيذ الاستعلام
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة التقرير: {str(e)}")
            raise
    
    def _execute_report_query(self, query_template: str, parameters: Dict[str, Any]) -> pd.DataFrame:
        """تنفيذ استعلام التقرير"""
        try:
            # استبدال المعلمات في قالب الاستعلام
            query = self._replace_query_parameters(query_template, parameters)
            
            # تنفيذ الاستعلام
            results = self.db_manager.execute_query(query)
            
            # الحصول على أسماء الأعمدة
            cursor_description = self.db_manager.get_cursor_description()
            columns = [desc[0] for desc in cursor_description]
            
            # إنشاء DataFrame
            df = pd.DataFrame(results, columns=columns)
            
            return df
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ استعلام التقرير: {str(e)}")
            raise
    
    def _replace_query_parameters(self, query_template: str, parameters: Dict[str, Any]) -> str:
        """استبدال المعلمات في قالب الاستعلام"""
        query = query_template
        
        # استبدال المعلمات
        for key, value in parameters.items():
            placeholder = f":{key}"
            
            # التعامل مع أنواع البيانات المختلفة
            if isinstance(value, str):
                # تهرب من الاقتباسات في النصوص
                value = value.replace("'", "''")
                # إضافة اقتباسات للنصوص
                value = f"'{value}'"
            elif isinstance(value, bool):
                value = "TRUE" if value else "FALSE"
            elif isinstance(value, (list, tuple)):
                # تحويل القائمة إلى سلسلة مفصولة بفواصل
                value_str = ", ".join([f"'{item}'" if isinstance(item, str) else str(item) for item in value])
                value = f"({value_str})"
            elif value is None:
                value = "NULL"
            else:
                value = str(value)
            
            # استبدال المعلمة في الاستعلام
            query = query.replace(placeholder, value)
        
        return query
    
    def _generate_report_file(self, report: Report, template: ReportTemplate, data: pd.DataFrame) -> str:
        """توليد ملف التقرير"""
        # إنشاء اسم الملف
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{template.name.replace(' ', '_')}_{timestamp}"
        
        # توليد الملف حسب الصيغة
        if report.report_format == ReportFormat.PDF:
            file_path = self._generate_pdf_report(report, template, data, file_name)
        elif report.report_format == ReportFormat.EXCEL:
            file_path = self._generate_excel_report(report, template, data, file_name)
        elif report.report_format == ReportFormat.CSV:
            file_path = self._generate_csv_report(report, template, data, file_name)
        elif report.report_format == ReportFormat.HTML:
            file_path = self._generate_html_report(report, template, data, file_name)
        elif report.report_format == ReportFormat.JSON:
            file_path = self._generate_json_report(report, template, data, file_name)
        else:
            raise ValueError(f"صيغة التقرير غير مدعومة: {report.report_format}")
        
        return file_path
    
    def _generate_pdf_report(self, report: Report, template: ReportTemplate, data: pd.DataFrame, file_name: str) -> str:
        """توليد تقرير PDF"""
        # إنشاء مسار الملف
        file_path = os.path.join(self.reports_dir, f"{file_name}.pdf")
        
        # إنشاء قالب HTML
        html_content = self._generate_html_content(report, template, data)
        
        # تحويل HTML إلى PDF
        pdfkit.from_string(html_content, file_path)
        
        return file_path
    
    def _generate_excel_report(self, report: Report, template: ReportTemplate, data: pd.DataFrame, file_name: str) -> str:
        """توليد تقرير Excel"""
        # إنشاء مسار الملف
        file_path = os.path.join(self.reports_dir, f"{file_name}.xlsx")
        
        # إنشاء ملف Excel
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='Report', index=False)
            
            # الحصول على ورقة العمل
            workbook = writer.book
            worksheet = writer.sheets['Report']
            
            # إضافة تنسيق للعناوين
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # تطبيق التنسيق على العناوين
            for col_num, value in enumerate(data.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # ضبط عرض الأعمدة
            for i, col in enumerate(data.columns):
                column_width = max(data[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)
        
        return file_path
    
    def _generate_csv_report(self, report: Report, template: ReportTemplate, data: pd.DataFrame, file_name: str) -> str:
        """توليد تقرير CSV"""
        # إنشاء مسار الملف
        file_path = os.path.join(self.reports_dir, f"{file_name}.csv")
        
        # إنشاء ملف CSV
        data.to_csv(file_path, index=False, encoding='utf-8-sig')
        
        return file_path
    
    def _generate_html_report(self, report: Report, template: ReportTemplate, data: pd.DataFrame, file_name: str) -> str:
        """توليد تقرير HTML"""
        # إنشاء مسار الملف
        file_path = os.path.join(self.reports_dir, f"{file_name}.html")
        
        # إنشاء محتوى HTML
        html_content = self._generate_html_content(report, template, data)
        
        # حفظ الملف
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return file_path
    
    def _generate_json_report(self, report: Report, template: ReportTemplate, data: pd.DataFrame, file_name: str) -> str:
        """توليد تقرير JSON"""
        # إنشاء مسار الملف
        file_path = os.path.join(self.reports_dir, f"{file_name}.json")
        
        # تحويل DataFrame إلى JSON
        json_data = data.to_json(orient='records', force_ascii=False, indent=4)
        
        # حفظ الملف
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_data)
        
        return file_path
    
    def _generate_html_content(self, report: Report, template: ReportTemplate, data: pd.DataFrame) -> str:
        """توليد محتوى HTML للتقرير"""
        # تحويل DataFrame إلى HTML
        table_html = data.to_html(index=False, classes='table table-striped table-bordered')
        
        # إنشاء قالب HTML
        html_template = """
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    direction: rtl;
                }
                h1 {
                    color: #2c3e50;
                    text-align: center;
                }
                .report-info {
                    margin-bottom: 20px;
                    padding: 10px;
                    background-color: #f8f9fa;
                    border-radius: 5px;
                }
                .table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                .table th, .table td {
                    padding: 8px;
                    text-align: right;
                    border: 1px solid #ddd;
                }
                .table th {
                    background-color: #f2f2f2;
                    font-weight: bold;
                }
                .table tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .footer {
                    margin-top: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            
            <div class="report-info">
                <p><strong>الوصف:</strong> {{ description }}</p>
                <p><strong>تاريخ التقرير:</strong> {{ report_date }}</p>
                <p><strong>نوع التقرير:</strong> {{ report_type }}</p>
            </div>
            
            {{ table_html|safe }}
            
            <div class="footer">
                <p>تم إنشاء هذا التقرير بواسطة نظام Gaara ERP</p>
                <p>{{ current_date }}</p>
            </div>
        </body>
        </html>
        """
        
        # إنشاء قالب Jinja2
        template_obj = jinja2.Template(html_template)
        
        # تحضير بيانات القالب
        template_data = {
            'title': template.name,
            'description': template.description,
            'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'report_type': template.report_type.value,
            'table_html': table_html,
            'current_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # توليد HTML
        html_content = template_obj.render(**template_data)
        
        return html_content
    
    def create_scheduled_report(self, schedule_data: Dict[str, Any]) -> ScheduledReport:
        """إنشاء تقرير مجدول جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["template_id", "parameters", "frequency", "created_by"]
        for field in required_fields:
            if field not in schedule_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # التحقق من وجود قالب التقرير
        template = self.get_report_template(schedule_data["template_id"])
        if not template:
            raise ValueError(f"قالب التقرير غير موجود: {schedule_data['template_id']}")
        
        # التحقق من أن قالب التقرير نشط
        if not template.is_active:
            raise ValueError(f"قالب التقرير غير نشط: {schedule_data['template_id']}")
        
        # التحقق من تكرار التقرير
        if isinstance(schedule_data["frequency"], str):
            try:
                schedule_data["frequency"] = ReportFrequency(schedule_data["frequency"])
            except ValueError:
                raise ValueError(f"تكرار التقرير غير صالح: {schedule_data['frequency']}")
        
        # التحقق من صيغة التقرير
        report_format = schedule_data.get("report_format")
        if report_format:
            if isinstance(report_format, str):
                try:
                    report_format = ReportFormat(report_format)
                except ValueError:
                    raise ValueError(f"صيغة التقرير غير صالحة: {report_format}")
        else:
            report_format = ReportFormat.PDF
        
        # حساب وقت التشغيل التالي
        next_run = self._calculate_next_run(schedule_data["frequency"])
        
        # إنشاء تقرير مجدول جديد
        scheduled_report = ScheduledReport(
            template_id=schedule_data["template_id"],
            parameters=schedule_data["parameters"],
            frequency=schedule_data["frequency"],
            created_by=schedule_data["created_by"],
            report_format=report_format,
            is_active=schedule_data.get("is_active", True),
            next_run=next_run
        )
        
        # حفظ التقرير المجدول في قاعدة البيانات
        self._save_scheduled_report(scheduled_report)
        
        return scheduled_report
    
    def _save_scheduled_report(self, scheduled_report: ScheduledReport) -> None:
        """حفظ تقرير مجدول في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            schedule_dict = scheduled_report.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO scheduled_reports (
                    schedule_id, template_id, parameters, frequency, created_by,
                    report_format, is_active, next_run, last_run, last_report_id,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                schedule_dict["schedule_id"],
                schedule_dict["template_id"],
                json.dumps(schedule_dict["parameters"]),
                schedule_dict["frequency"],
                schedule_dict["created_by"],
                schedule_dict["report_format"],
                schedule_dict["is_active"],
                schedule_dict.get("next_run"),
                schedule_dict.get("last_run"),
                schedule_dict["last_report_id"],
                schedule_dict["created_at"],
                schedule_dict["updated_at"]
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ التقرير المجدول: {str(e)}")
            raise
    
    def _calculate_next_run(self, frequency: ReportFrequency) -> datetime:
        """حساب وقت التشغيل التالي"""
        now = datetime.now()
        
        if frequency == ReportFrequency.ONCE:
            # للتقارير التي تشغل مرة واحدة، نستخدم الوقت الحالي
            return now
        elif frequency == ReportFrequency.DAILY:
            # للتقارير اليومية، نستخدم اليوم التالي في نفس الوقت
            return now + timedelta(days=1)
        elif frequency == ReportFrequency.WEEKLY:
            # للتقارير الأسبوعية، نستخدم الأسبوع التالي في نفس اليوم والوقت
            return now + timedelta(weeks=1)
        elif frequency == ReportFrequency.MONTHLY:
            # للتقارير الشهرية، نستخدم الشهر التالي في نفس اليوم والوقت
            if now.month == 12:
                next_month = 1
                next_year = now.year + 1
            else:
                next_month = now.month + 1
                next_year = now.year
            
            # التعامل مع أيام الشهر المختلفة
            day = min(now.day, self._get_days_in_month(next_year, next_month))
            
            return datetime(next_year, next_month, day, now.hour, now.minute, now.second)
        elif frequency == ReportFrequency.QUARTERLY:
            # للتقارير الربع سنوية، نستخدم الربع التالي في نفس اليوم والوقت
            if now.month <= 3:
                next_month = 4
                next_year = now.year
            elif now.month <= 6:
                next_month = 7
                next_year = now.year
            elif now.month <= 9:
                next_month = 10
                next_year = now.year
            else:
                next_month = 1
                next_year = now.year + 1
            
            # التعامل مع أيام الشهر المختلفة
            day = min(now.day, self._get_days_in_month(next_year, next_month))
            
            return datetime(next_year, next_month, day, now.hour, now.minute, now.second)
        elif frequency == ReportFrequency.YEARLY:
            # للتقارير السنوية، نستخدم السنة التالية في نفس اليوم والوقت
            next_year = now.year + 1
            
            # التعامل مع السنوات الكبيسة
            if now.month == 2 and now.day == 29:
                if self._is_leap_year(next_year):
                    day = 29
                else:
                    day = 28
            else:
                day = now.day
            
            return datetime(next_year, now.month, day, now.hour, now.minute, now.second)
        else:
            raise ValueError(f"تكرار التقرير غير صالح: {frequency}")
    
    def _get_days_in_month(self, year: int, month: int) -> int:
        """الحصول على عدد أيام الشهر"""
        if month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            if self._is_leap_year(year):
                return 29
            else:
                return 28
        else:
            return 31
    
    def _is_leap_year(self, year: int) -> bool:
        """التحقق مما إذا كانت السنة كبيسة"""
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        if year % 4 == 0:
            return True
        return False
    
    def get_scheduled_report(self, schedule_id: str) -> Optional[ScheduledReport]:
        """الحصول على تقرير مجدول بواسطة المعرف"""
        try:
            query = """
                SELECT schedule_id, template_id, parameters, frequency, created_by,
                       report_format, is_active, next_run, last_run, last_report_id,
                       created_at, updated_at
                FROM scheduled_reports
                WHERE schedule_id = %s
            """
            
            result = self.db_manager.execute_query(query, (schedule_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            schedule_dict = {
                "schedule_id": result[0],
                "template_id": result[1],
                "parameters": json.loads(result[2]) if result[2] else {},
                "frequency": result[3],
                "created_by": result[4],
                "report_format": result[5],
                "is_active": result[6],
                "next_run": result[7],
                "last_run": result[8],
                "last_report_id": result[9],
                "created_at": result[10],
                "updated_at": result[11]
            }
            
            return ScheduledReport.from_dict(schedule_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على التقرير المجدول: {str(e)}")
            return None
    
    def get_all_scheduled_reports(
        self,
        template_id: Optional[str] = None,
        created_by: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ScheduledReport], int]:
        """الحصول على جميع التقارير المجدولة"""
        try:
            # بناء الاستعلام
            query = """
                SELECT schedule_id, template_id, parameters, frequency, created_by,
                       report_format, is_active, next_run, last_run, last_report_id,
                       created_at, updated_at
                FROM scheduled_reports
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM scheduled_reports
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if template_id:
                query += " AND template_id = %s"
                count_query += " AND template_id = %s"
                params.append(template_id)
            
            if created_by:
                query += " AND created_by = %s"
                count_query += " AND created_by = %s"
                params.append(created_by)
            
            if is_active is not None:
                query += " AND is_active = %s"
                count_query += " AND is_active = %s"
                params.append(is_active)
            
            # إضافة الترتيب والحد
            query += " ORDER BY next_run ASC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # تنفيذ استعلام العدد
            count_result = self.db_manager.execute_query(count_query, params[:-2], fetch_one=True)
            total = count_result[0] if count_result else 0
            
            # تنفيذ استعلام البيانات
            results = self.db_manager.execute_query(query, params)
            
            # تحويل النتائج إلى كائنات
            schedules = []
            for result in results:
                schedule_dict = {
                    "schedule_id": result[0],
                    "template_id": result[1],
                    "parameters": json.loads(result[2]) if result[2] else {},
                    "frequency": result[3],
                    "created_by": result[4],
                    "report_format": result[5],
                    "is_active": result[6],
                    "next_run": result[7],
                    "last_run": result[8],
                    "last_report_id": result[9],
                    "created_at": result[10],
                    "updated_at": result[11]
                }
                
                schedules.append(ScheduledReport.from_dict(schedule_dict))
            
            return schedules, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على التقارير المجدولة: {str(e)}")
            return [], 0
    
    def update_scheduled_report(self, schedule_id: str, schedule_data: Dict[str, Any]) -> Optional[ScheduledReport]:
        """تحديث تقرير مجدول"""
        try:
            # الحصول على التقرير المجدول الحالي
            current_schedule = self.get_scheduled_report(schedule_id)
            if not current_schedule:
                return None
            
            # تحديث البيانات
            if "parameters" in schedule_data:
                current_schedule.parameters = schedule_data["parameters"]
            
            if "frequency" in schedule_data:
                if isinstance(schedule_data["frequency"], str):
                    try:
                        current_schedule.frequency = ReportFrequency(schedule_data["frequency"])
                    except ValueError:
                        raise ValueError(f"تكرار التقرير غير صالح: {schedule_data['frequency']}")
                else:
                    current_schedule.frequency = schedule_data["frequency"]
                
                # إعادة حساب وقت التشغيل التالي
                current_schedule.next_run = self._calculate_next_run(current_schedule.frequency)
            
            if "report_format" in schedule_data:
                if isinstance(schedule_data["report_format"], str):
                    try:
                        current_schedule.report_format = ReportFormat(schedule_data["report_format"])
                    except ValueError:
                        raise ValueError(f"صيغة التقرير غير صالحة: {schedule_data['report_format']}")
                else:
                    current_schedule.report_format = schedule_data["report_format"]
            
            if "is_active" in schedule_data:
                current_schedule.is_active = schedule_data["is_active"]
            
            # تحديث وقت التحديث
            current_schedule.updated_at = datetime.now()
            
            # حفظ التغييرات في قاعدة البيانات
            query = """
                UPDATE scheduled_reports
                SET parameters = %s, frequency = %s, report_format = %s,
                    is_active = %s, next_run = %s, updated_at = %s
                WHERE schedule_id = %s
            """
            
            params = (
                json.dumps(current_schedule.parameters),
                current_schedule.frequency.value,
                current_schedule.report_format.value,
                current_schedule.is_active,
                current_schedule.next_run,
                current_schedule.updated_at,
                schedule_id
            )
            
            self.db_manager.execute_query(query, params)
            
            return current_schedule
        except Exception as e:
            self.logger.error(f"خطأ في تحديث التقرير المجدول: {str(e)}")
            raise
    
    def delete_scheduled_report(self, schedule_id: str) -> bool:
        """حذف تقرير مجدول"""
        try:
            # التحقق من وجود التقرير المجدول
            current_schedule = self.get_scheduled_report(schedule_id)
            if not current_schedule:
                return False
            
            # حذف التقرير المجدول
            query = """
                DELETE FROM scheduled_reports
                WHERE schedule_id = %s
            """
            
            self.db_manager.execute_query(query, (schedule_id,))
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف التقرير المجدول: {str(e)}")
            raise
    
    def run_scheduled_reports(self) -> List[str]:
        """تشغيل التقارير المجدولة المستحقة"""
        try:
            # الحصول على التقارير المجدولة المستحقة
            query = """
                SELECT schedule_id
                FROM scheduled_reports
                WHERE is_active = TRUE AND next_run <= %s
            """
            
            results = self.db_manager.execute_query(query, (datetime.now(),))
            
            # تشغيل التقارير المجدولة
            report_ids = []
            for result in results:
                schedule_id = result[0]
                report_id = self.run_scheduled_report(schedule_id)
                if report_id:
                    report_ids.append(report_id)
            
            return report_ids
        except Exception as e:
            self.logger.error(f"خطأ في تشغيل التقارير المجدولة: {str(e)}")
            return []
    
    def run_scheduled_report(self, schedule_id: str) -> Optional[str]:
        """تشغيل تقرير مجدول"""
        try:
            # الحصول على التقرير المجدول
            scheduled_report = self.get_scheduled_report(schedule_id)
            if not scheduled_report:
                self.logger.error(f"لم يتم العثور على التقرير المجدول بالمعرف {schedule_id}")
                return None
            
            # التحقق من أن التقرير المجدول نشط
            if not scheduled_report.is_active:
                self.logger.error(f"التقرير المجدول غير نشط: {schedule_id}")
                return None
            
            # إنشاء تقرير جديد
            report_data = {
                "template_id": scheduled_report.template_id,
                "parameters": scheduled_report.parameters,
                "created_by": scheduled_report.created_by,
                "report_format": scheduled_report.report_format
            }
            
            report = self.create_report(report_data)
            
            # توليد التقرير
            success = self.generate_report(report.report_id)
            
            if not success:
                self.logger.error(f"فشل في توليد التقرير المجدول: {schedule_id}")
                return None
            
            # تحديث التقرير المجدول
            now = datetime.now()
            next_run = self._calculate_next_run_from_last(scheduled_report.frequency, now)
            
            # إذا كان التقرير يشغل مرة واحدة، نقوم بتعطيله
            is_active = True
            if scheduled_report.frequency == ReportFrequency.ONCE:
                is_active = False
            
            query = """
                UPDATE scheduled_reports
                SET last_run = %s, next_run = %s, last_report_id = %s, is_active = %s, updated_at = %s
                WHERE schedule_id = %s
            """
            
            params = (now, next_run, report.report_id, is_active, now, schedule_id)
            
            self.db_manager.execute_query(query, params)
            
            return report.report_id
        except Exception as e:
            self.logger.error(f"خطأ في تشغيل التقرير المجدول: {str(e)}")
            return None
    
    def _calculate_next_run_from_last(self, frequency: ReportFrequency, last_run: datetime) -> Optional[datetime]:
        """حساب وقت التشغيل التالي من وقت التشغيل الأخير"""
        if frequency == ReportFrequency.ONCE:
            # للتقارير التي تشغل مرة واحدة، لا يوجد وقت تشغيل تالي
            return None
        elif frequency == ReportFrequency.DAILY:
            # للتقارير اليومية، نستخدم اليوم التالي في نفس الوقت
            return last_run + timedelta(days=1)
        elif frequency == ReportFrequency.WEEKLY:
            # للتقارير الأسبوعية، نستخدم الأسبوع التالي في نفس اليوم والوقت
            return last_run + timedelta(weeks=1)
        elif frequency == ReportFrequency.MONTHLY:
            # للتقارير الشهرية، نستخدم الشهر التالي في نفس اليوم والوقت
            if last_run.month == 12:
                next_month = 1
                next_year = last_run.year + 1
            else:
                next_month = last_run.month + 1
                next_year = last_run.year
            
            # التعامل مع أيام الشهر المختلفة
            day = min(last_run.day, self._get_days_in_month(next_year, next_month))
            
            return datetime(next_year, next_month, day, last_run.hour, last_run.minute, last_run.second)
        elif frequency == ReportFrequency.QUARTERLY:
            # للتقارير الربع سنوية، نستخدم الربع التالي في نفس اليوم والوقت
            if last_run.month <= 3:
                next_month = 4
                next_year = last_run.year
            elif last_run.month <= 6:
                next_month = 7
                next_year = last_run.year
            elif last_run.month <= 9:
                next_month = 10
                next_year = last_run.year
            else:
                next_month = 1
                next_year = last_run.year + 1
            
            # التعامل مع أيام الشهر المختلفة
            day = min(last_run.day, self._get_days_in_month(next_year, next_month))
            
            return datetime(next_year, next_month, day, last_run.hour, last_run.minute, last_run.second)
        elif frequency == ReportFrequency.YEARLY:
            # للتقارير السنوية، نستخدم السنة التالية في نفس اليوم والوقت
            next_year = last_run.year + 1
            
            # التعامل مع السنوات الكبيسة
            if last_run.month == 2 and last_run.day == 29:
                if self._is_leap_year(next_year):
                    day = 29
                else:
                    day = 28
            else:
                day = last_run.day
            
            return datetime(next_year, last_run.month, day, last_run.hour, last_run.minute, last_run.second)
        else:
            raise ValueError(f"تكرار التقرير غير صالح: {frequency}")
    
    def create_report_dashboard(self, dashboard_data: Dict[str, Any]) -> ReportDashboard:
        """إنشاء لوحة تحكم تقارير جديدة"""
        # التحقق من البيانات المطلوبة
        required_fields = ["name", "description", "layout", "created_by"]
        for field in required_fields:
            if field not in dashboard_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # إنشاء لوحة تحكم تقارير جديدة
        dashboard = ReportDashboard(
            name=dashboard_data["name"],
            description=dashboard_data["description"],
            layout=dashboard_data["layout"],
            created_by=dashboard_data["created_by"],
            is_public=dashboard_data.get("is_public", False),
            is_active=dashboard_data.get("is_active", True)
        )
        
        # حفظ لوحة تحكم التقارير في قاعدة البيانات
        self._save_report_dashboard(dashboard)
        
        return dashboard
    
    def _save_report_dashboard(self, dashboard: ReportDashboard) -> None:
        """حفظ لوحة تحكم تقارير في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            dashboard_dict = dashboard.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO report_dashboards (
                    dashboard_id, name, description, layout, created_by,
                    is_public, is_active, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                dashboard_dict["dashboard_id"],
                dashboard_dict["name"],
                dashboard_dict["description"],
                json.dumps(dashboard_dict["layout"]),
                dashboard_dict["created_by"],
                dashboard_dict["is_public"],
                dashboard_dict["is_active"],
                dashboard_dict["created_at"],
                dashboard_dict["updated_at"]
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ لوحة تحكم التقارير: {str(e)}")
            raise
    
    def get_report_dashboard(self, dashboard_id: str) -> Optional[ReportDashboard]:
        """الحصول على لوحة تحكم تقارير بواسطة المعرف"""
        try:
            query = """
                SELECT dashboard_id, name, description, layout, created_by,
                       is_public, is_active, created_at, updated_at
                FROM report_dashboards
                WHERE dashboard_id = %s
            """
            
            result = self.db_manager.execute_query(query, (dashboard_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            dashboard_dict = {
                "dashboard_id": result[0],
                "name": result[1],
                "description": result[2],
                "layout": json.loads(result[3]) if result[3] else {},
                "created_by": result[4],
                "is_public": result[5],
                "is_active": result[6],
                "created_at": result[7],
                "updated_at": result[8]
            }
            
            return ReportDashboard.from_dict(dashboard_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على لوحة تحكم التقارير: {str(e)}")
            return None
    
    def get_all_report_dashboards(
        self,
        created_by: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ReportDashboard], int]:
        """الحصول على جميع لوحات تحكم التقارير"""
        try:
            # بناء الاستعلام
            query = """
                SELECT dashboard_id, name, description, layout, created_by,
                       is_public, is_active, created_at, updated_at
                FROM report_dashboards
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM report_dashboards
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if created_by:
                query += " AND created_by = %s"
                count_query += " AND created_by = %s"
                params.append(created_by)
            
            if is_public is not None:
                query += " AND is_public = %s"
                count_query += " AND is_public = %s"
                params.append(is_public)
            
            if is_active is not None:
                query += " AND is_active = %s"
                count_query += " AND is_active = %s"
                params.append(is_active)
            
            # إضافة الترتيب والحد
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # تنفيذ استعلام العدد
            count_result = self.db_manager.execute_query(count_query, params[:-2], fetch_one=True)
            total = count_result[0] if count_result else 0
            
            # تنفيذ استعلام البيانات
            results = self.db_manager.execute_query(query, params)
            
            # تحويل النتائج إلى كائنات
            dashboards = []
            for result in results:
                dashboard_dict = {
                    "dashboard_id": result[0],
                    "name": result[1],
                    "description": result[2],
                    "layout": json.loads(result[3]) if result[3] else {},
                    "created_by": result[4],
                    "is_public": result[5],
                    "is_active": result[6],
                    "created_at": result[7],
                    "updated_at": result[8]
                }
                
                dashboards.append(ReportDashboard.from_dict(dashboard_dict))
            
            return dashboards, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على لوحات تحكم التقارير: {str(e)}")
            return [], 0
    
    def update_report_dashboard(self, dashboard_id: str, dashboard_data: Dict[str, Any]) -> Optional[ReportDashboard]:
        """تحديث لوحة تحكم تقارير"""
        try:
            # الحصول على لوحة تحكم التقارير الحالية
            current_dashboard = self.get_report_dashboard(dashboard_id)
            if not current_dashboard:
                return None
            
            # تحديث البيانات
            if "name" in dashboard_data:
                current_dashboard.name = dashboard_data["name"]
            
            if "description" in dashboard_data:
                current_dashboard.description = dashboard_data["description"]
            
            if "layout" in dashboard_data:
                current_dashboard.layout = dashboard_data["layout"]
            
            if "is_public" in dashboard_data:
                current_dashboard.is_public = dashboard_data["is_public"]
            
            if "is_active" in dashboard_data:
                current_dashboard.is_active = dashboard_data["is_active"]
            
            # تحديث وقت التحديث
            current_dashboard.updated_at = datetime.now()
            
            # حفظ التغييرات في قاعدة البيانات
            query = """
                UPDATE report_dashboards
                SET name = %s, description = %s, layout = %s,
                    is_public = %s, is_active = %s, updated_at = %s
                WHERE dashboard_id = %s
            """
            
            params = (
                current_dashboard.name,
                current_dashboard.description,
                json.dumps(current_dashboard.layout),
                current_dashboard.is_public,
                current_dashboard.is_active,
                current_dashboard.updated_at,
                dashboard_id
            )
            
            self.db_manager.execute_query(query, params)
            
            return current_dashboard
        except Exception as e:
            self.logger.error(f"خطأ في تحديث لوحة تحكم التقارير: {str(e)}")
            raise
    
    def delete_report_dashboard(self, dashboard_id: str) -> bool:
        """حذف لوحة تحكم تقارير"""
        try:
            # التحقق من وجود لوحة تحكم التقارير
            current_dashboard = self.get_report_dashboard(dashboard_id)
            if not current_dashboard:
                return False
            
            # حذف لوحة تحكم التقارير
            query = """
                DELETE FROM report_dashboards
                WHERE dashboard_id = %s
            """
            
            self.db_manager.execute_query(query, (dashboard_id,))
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف لوحة تحكم التقارير: {str(e)}")
            raise
