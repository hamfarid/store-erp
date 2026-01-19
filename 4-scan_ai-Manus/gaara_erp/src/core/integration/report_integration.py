"""
وحدة تكامل التقارير بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي

هذه الوحدة مسؤولة عن:
1. إنشاء تقارير موحدة تجمع بيانات من كلا النظامين
2. توفير قوالب تقارير مخصصة للتحليلات الزراعية
3. جدولة وتوزيع التقارير
4. تصدير التقارير بصيغ مختلفة
"""

import os
import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import threading
import schedule
import time

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("report_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("report_integration")

class ReportIntegration:
    """فئة تكامل التقارير بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي"""
    
    def __init__(self, config_path=None, db_integration=None, ui_integration=None):
        """
        تهيئة وحدة تكامل التقارير
        
        المعلمات:
            config_path (str): مسار ملف التكوين (اختياري)
            db_integration: كائن تكامل قواعد البيانات (اختياري)
            ui_integration: كائن تكامل واجهات المستخدم (اختياري)
        """
        self.config = self._load_config(config_path)
        self.db_integration = db_integration
        self.ui_integration = ui_integration
        self.reports_dir = self.config.get('reports_dir', '/tmp/reports')
        self.templates_dir = self.config.get('templates_dir', 'templates/reports')
        
        # إنشاء مجلد التقارير إذا لم يكن موجوداً
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # إعداد محرك قوالب Jinja2
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # قائمة المهام المجدولة
        self.scheduled_tasks = []
        
        logger.info("تم تهيئة وحدة تكامل التقارير بنجاح")
    
    def _load_config(self, config_path):
        """
        تحميل ملف التكوين
        
        المعلمات:
            config_path (str): مسار ملف التكوين
            
        العوائد:
            dict: بيانات التكوين
        """
        default_config = {
            'reports_dir': '/tmp/reports',
            'templates_dir': 'templates/reports',
            'default_format': 'pdf',
            'email': {
                'smtp_server': 'smtp.example.com',
                'smtp_port': 587,
                'username': 'reports@example.com',
                'password': 'your_password',
                'from_email': 'reports@example.com',
                'subject_prefix': '[تقرير] '
            },
            'report_templates': {
                'disease_summary': {
                    'name': 'ملخص الأمراض',
                    'template': 'disease_summary.html',
                    'description': 'تقرير يلخص حالات الأمراض المكتشفة وتوزيعها حسب المحصول والمنطقة',
                    'data_sources': ['disease_detections', 'plants', 'diseases'],
                    'charts': ['disease_distribution', 'detection_timeline'],
                    'available_formats': ['pdf', 'html', 'xlsx']
                },
                'breeding_results': {
                    'name': 'نتائج التهجين',
                    'template': 'breeding_results.html',
                    'description': 'تقرير يعرض نتائج عمليات التهجين والصفات المتوقعة للأصناف الجديدة',
                    'data_sources': ['breeding_requests', 'breeding_results', 'varieties'],
                    'charts': ['trait_comparison', 'success_rate'],
                    'available_formats': ['pdf', 'html', 'xlsx']
                },
                'nursery_status': {
                    'name': 'حالة المشاتل',
                    'template': 'nursery_status.html',
                    'description': 'تقرير يعرض حالة المشاتل والإشغال والأصناف المزروعة',
                    'data_sources': ['nurseries', 'plants', 'varieties'],
                    'charts': ['occupancy_rate', 'variety_distribution'],
                    'available_formats': ['pdf', 'html', 'xlsx']
                },
                'yield_forecast': {
                    'name': 'توقعات الإنتاج',
                    'template': 'yield_forecast.html',
                    'description': 'تقرير يعرض توقعات الإنتاج للمحاصيل المختلفة',
                    'data_sources': ['yield_predictions', 'farms', 'crops'],
                    'charts': ['yield_comparison', 'prediction_accuracy'],
                    'available_formats': ['pdf', 'html', 'xlsx']
                },
                'soil_analysis': {
                    'name': 'تحليل التربة',
                    'template': 'soil_analysis.html',
                    'description': 'تقرير يعرض نتائج تحليل التربة والتوصيات',
                    'data_sources': ['soil_analyses', 'farms', 'soil_types'],
                    'charts': ['nutrient_levels', 'ph_distribution'],
                    'available_formats': ['pdf', 'html', 'xlsx']
                },
                'system_integration': {
                    'name': 'تكامل النظام',
                    'template': 'system_integration.html',
                    'description': 'تقرير يعرض حالة تكامل النظامين وسلامة البيانات',
                    'data_sources': ['integration_status', 'data_integrity'],
                    'charts': ['sync_status', 'integrity_score'],
                    'available_formats': ['pdf', 'html', 'xlsx']
                }
            },
            'scheduled_reports': [
                {
                    'report_template': 'disease_summary',
                    'schedule': 'daily',
                    'time': '18:00',
                    'format': 'pdf',
                    'recipients': ['farm_manager@example.com', 'plant_pathologist@example.com'],
                    'parameters': {
                        'days': 1
                    }
                },
                {
                    'report_template': 'nursery_status',
                    'schedule': 'weekly',
                    'day': 'monday',
                    'time': '08:00',
                    'format': 'pdf',
                    'recipients': ['nursery_manager@example.com'],
                    'parameters': {}
                },
                {
                    'report_template': 'system_integration',
                    'schedule': 'monthly',
                    'day': 1,
                    'time': '00:00',
                    'format': 'pdf',
                    'recipients': ['system_admin@example.com'],
                    'parameters': {}
                }
            ]
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # دمج التكوين المخصص مع التكوين الافتراضي
                    for key, value in config.items():
                        if isinstance(value, dict) and key in default_config and isinstance(default_config[key], dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
                logger.info(f"تم تحميل ملف التكوين من {config_path}")
            except Exception as e:
                logger.error(f"خطأ في تحميل ملف التكوين: {str(e)}")
        else:
            logger.warning("لم يتم تحديد ملف تكوين، استخدام الإعدادات الافتراضية")
        
        return default_config
    
    def generate_report(self, template_id, parameters=None, output_format=None):
        """
        إنشاء تقرير
        
        المعلمات:
            template_id (str): معرف قالب التقرير
            parameters (dict): معلمات التقرير (اختياري)
            output_format (str): صيغة الإخراج (اختياري)
            
        العوائد:
            str: مسار ملف التقرير
        """
        if template_id not in self.config.get('report_templates', {}):
            raise ValueError(f"قالب التقرير غير موجود: {template_id}")
        
        template_config = self.config['report_templates'][template_id]
        
        # تحديد صيغة الإخراج
        if output_format is None:
            output_format = self.config.get('default_format', 'pdf')
        
        if output_format not in template_config.get('available_formats', []):
            raise ValueError(f"صيغة الإخراج غير مدعومة لهذا القالب: {output_format}")
        
        # تهيئة معلمات التقرير
        if parameters is None:
            parameters = {}
        
        # جمع البيانات للتقرير
        report_data = self._collect_report_data(template_id, parameters)
        
        # إنشاء الرسوم البيانية
        charts = self._generate_charts(template_id, report_data)
        
        # إعداد سياق القالب
        context = {
            'report_title': template_config.get('name', template_id),
            'report_description': template_config.get('description', ''),
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': report_data,
            'charts': charts,
            'parameters': parameters
        }
        
        # توليد محتوى التقرير
        template_name = template_config.get('template')
        html_content = self._render_template(template_name, context)
        
        # إنشاء ملف التقرير
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"{template_id}_{timestamp}"
        
        if output_format == 'pdf':
            report_path = self._generate_pdf(report_filename, html_content)
        elif output_format == 'html':
            report_path = self._generate_html(report_filename, html_content)
        elif output_format == 'xlsx':
            report_path = self._generate_excel(report_filename, report_data)
        else:
            raise ValueError(f"صيغة الإخراج غير مدعومة: {output_format}")
        
        logger.info(f"تم إنشاء تقرير {template_id} بصيغة {output_format}: {report_path}")
        
        return report_path
    
    def _collect_report_data(self, template_id, parameters):
        """
        جمع البيانات للتقرير
        
        المعلمات:
            template_id (str): معرف قالب التقرير
            parameters (dict): معلمات التقرير
            
        العوائد:
            dict: بيانات التقرير
        """
        template_config = self.config['report_templates'][template_id]
        data_sources = template_config.get('data_sources', [])
        
        report_data = {}
        
        for source in data_sources:
            try:
                # جلب البيانات حسب نوع المصدر
                if source == 'disease_detections':
                    report_data[source] = self._get_disease_detections_data(parameters)
                elif source == 'plants':
                    report_data[source] = self._get_plants_data(parameters)
                elif source == 'diseases':
                    report_data[source] = self._get_diseases_data(parameters)
                elif source == 'breeding_requests':
                    report_data[source] = self._get_breeding_requests_data(parameters)
                elif source == 'breeding_results':
                    report_data[source] = self._get_breeding_results_data(parameters)
                elif source == 'varieties':
                    report_data[source] = self._get_varieties_data(parameters)
                elif source == 'nurseries':
                    report_data[source] = self._get_nurseries_data(parameters)
                elif source == 'yield_predictions':
                    report_data[source] = self._get_yield_predictions_data(parameters)
                elif source == 'farms':
                    report_data[source] = self._get_farms_data(parameters)
                elif source == 'crops':
                    report_data[source] = self._get_crops_data(parameters)
                elif source == 'soil_analyses':
                    report_data[source] = self._get_soil_analyses_data(parameters)
                elif source == 'soil_types':
                    report_data[source] = self._get_soil_types_data(parameters)
                elif source == 'integration_status':
                    report_data[source] = self._get_integration_status_data(parameters)
                elif source == 'data_integrity':
                    report_data[source] = self._get_data_integrity_data(parameters)
                else:
                    logger.warning(f"مصدر بيانات غير معروف: {source}")
            except Exception as e:
                logger.error(f"خطأ في جمع بيانات {source}: {str(e)}")
                report_data[source] = {'error': str(e)}
        
        return report_data
    
    def _generate_charts(self, template_id, report_data):
        """
        إنشاء الرسوم البيانية للتقرير
        
        المعلمات:
            template_id (str): معرف قالب التقرير
            report_data (dict): بيانات التقرير
            
        العوائد:
            dict: مسارات ملفات الرسوم البيانية
        """
        template_config = self.config['report_templates'][template_id]
        chart_types = template_config.get('charts', [])
        
        charts = {}
        
        for chart_type in chart_types:
            try:
                # إنشاء الرسم البياني حسب النوع
                if chart_type == 'disease_distribution':
                    charts[chart_type] = self._create_disease_distribution_chart(report_data)
                elif chart_type == 'detection_timeline':
                    charts[chart_type] = self._create_detection_timeline_chart(report_data)
                elif chart_type == 'trait_comparison':
                    charts[chart_type] = self._create_trait_comparison_chart(report_data)
                elif chart_type == 'success_rate':
                    charts[chart_type] = self._create_success_rate_chart(report_data)
                elif chart_type == 'occupancy_rate':
                    charts[chart_type] = self._create_occupancy_rate_chart(report_data)
                elif chart_type == 'variety_distribution':
                    charts[chart_type] = self._create_variety_distribution_chart(report_data)
                elif chart_type == 'yield_comparison':
                    charts[chart_type] = self._create_yield_comparison_chart(report_data)
                elif chart_type == 'prediction_accuracy':
                    charts[chart_type] = self._create_prediction_accuracy_chart(report_data)
                elif chart_type == 'nutrient_levels':
                    charts[chart_type] = self._create_nutrient_levels_chart(report_data)
                elif chart_type == 'ph_distribution':
                    charts[chart_type] = self._create_ph_distribution_chart(report_data)
                elif chart_type == 'sync_status':
                    charts[chart_type] = self._create_sync_status_chart(report_data)
                elif chart_type == 'integrity_score':
                    charts[chart_type] = self._create_integrity_score_chart(report_data)
                else:
                    logger.warning(f"نوع رسم بياني غير معروف: {chart_type}")
            except Exception as e:
                logger.error(f"خطأ في إنشاء الرسم البياني {chart_type}: {str(e)}")
                charts[chart_type] = None
        
        return charts
    
    def _render_template(self, template_name, context):
        """
        توليد محتوى HTML من قالب
        
        المعلمات:
            template_name (str): اسم ملف القالب
            context (dict): سياق القالب
            
        العوائد:
            str: محتوى HTML
        """
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"خطأ في توليد محتوى HTML من قالب {template_name}: {str(e)}")
            raise
    
    def _generate_pdf(self, filename, html_content):
        """
        إنشاء ملف PDF
        
        المعلمات:
            filename (str): اسم الملف
            html_content (str): محتوى HTML
            
        العوائد:
            str: مسار ملف PDF
        """
        output_path = os.path.join(self.reports_dir, f"{filename}.pdf")
        
        try:
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملف PDF: {str(e)}")
            raise
    
    def _generate_html(self, filename, html_content):
        """
        إنشاء ملف HTML
        
        المعلمات:
            filename (str): اسم الملف
            html_content (str): محتوى HTML
            
        العوائد:
            str: مسار ملف HTML
        """
        output_path = os.path.join(self.reports_dir, f"{filename}.html")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_path
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملف HTML: {str(e)}")
            raise
    
    def _generate_excel(self, filename, report_data):
        """
        إنشاء ملف Excel
        
        المعلمات:
            filename (str): اسم الملف
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف Excel
        """
        output_path = os.path.join(self.reports_dir, f"{filename}.xlsx")
        
        try:
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                for source, data in report_data.items():
                    if isinstance(data, list) and data and isinstance(data[0], dict):
                        # تحويل قائمة القواميس إلى DataFrame
                        df = pd.DataFrame(data)
                        df.to_excel(writer, sheet_name=source, index=False)
                    elif isinstance(data, dict) and 'error' not in data:
                        # تحويل القاموس إلى DataFrame
                        df = pd.DataFrame([data])
                        df.to_excel(writer, sheet_name=source, index=False)
            
            return output_path
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملف Excel: {str(e)}")
            raise
    
    def send_report_by_email(self, report_path, recipients, subject=None, message=None):
        """
        إرسال التقرير بالبريد الإلكتروني
        
        المعلمات:
            report_path (str): مسار ملف التقرير
            recipients (list): قائمة عناوين البريد الإلكتروني للمستلمين
            subject (str): عنوان الرسالة (اختياري)
            message (str): نص الرسالة (اختياري)
            
        العوائد:
            bool: نجاح الإرسال
        """
        if not os.path.exists(report_path):
            raise ValueError(f"ملف التقرير غير موجود: {report_path}")
        
        email_config = self.config.get('email', {})
        
        # إعداد عنوان الرسالة
        if subject is None:
            report_filename = os.path.basename(report_path)
            subject = f"{email_config.get('subject_prefix', '')}تقرير: {report_filename}"
        
        # إعداد نص الرسالة
        if message is None:
            message = f"مرفق تقرير تم إنشاؤه في {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        
        try:
            # إنشاء رسالة البريد الإلكتروني
            msg = MIMEMultipart()
            msg['From'] = email_config.get('from_email')
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # إضافة نص الرسالة
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            # إضافة ملف التقرير كمرفق
            with open(report_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), Name=os.path.basename(report_path))
            
            attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_path)}"'
            msg.attach(attachment)
            
            # إرسال البريد الإلكتروني
            with smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port')) as server:
                server.starttls()
                server.login(email_config.get('username'), email_config.get('password'))
                server.send_message(msg)
            
            logger.info(f"تم إرسال التقرير {report_path} إلى {len(recipients)} مستلم")
            
            return True
        
        except Exception as e:
            logger.error(f"خطأ في إرسال التقرير بالبريد الإلكتروني: {str(e)}")
            return False
    
    def schedule_reports(self):
        """
        جدولة التقارير
        
        العوائد:
            bool: نجاح الجدولة
        """
        scheduled_reports = self.config.get('scheduled_reports', [])
        
        if not scheduled_reports:
            logger.warning("لا توجد تقارير مجدولة")
            return False
        
        try:
            # إلغاء جميع المهام المجدولة السابقة
            schedule.clear()
            
            for report_config in scheduled_reports:
                template_id = report_config.get('report_template')
                output_format = report_config.get('format')
                recipients = report_config.get('recipients', [])
                parameters = report_config.get('parameters', {})
                
                # إنشاء دالة لإنشاء وإرسال التقرير
                def send_scheduled_report():
                    try:
                        report_path = self.generate_report(template_id, parameters, output_format)
                        self.send_report_by_email(report_path, recipients)
                    except Exception as e:
                        logger.error(f"خطأ في إنشاء وإرسال التقرير المجدول {template_id}: {str(e)}")
                
                # جدولة التقرير حسب التكرار
                schedule_type = report_config.get('schedule')
                
                if schedule_type == 'daily':
                    time_str = report_config.get('time', '00:00')
                    schedule.every().day.at(time_str).do(send_scheduled_report)
                    logger.info(f"تمت جدولة التقرير {template_id} يومياً في الساعة {time_str}")
                
                elif schedule_type == 'weekly':
                    day = report_config.get('day', 'monday').lower()
                    time_str = report_config.get('time', '00:00')
                    
                    if day == 'monday':
                        schedule.every().monday.at(time_str).do(send_scheduled_report)
                    elif day == 'tuesday':
                        schedule.every().tuesday.at(time_str).do(send_scheduled_report)
                    elif day == 'wednesday':
                        schedule.every().wednesday.at(time_str).do(send_scheduled_report)
                    elif day == 'thursday':
                        schedule.every().thursday.at(time_str).do(send_scheduled_report)
                    elif day == 'friday':
                        schedule.every().friday.at(time_str).do(send_scheduled_report)
                    elif day == 'saturday':
                        schedule.every().saturday.at(time_str).do(send_scheduled_report)
                    elif day == 'sunday':
                        schedule.every().sunday.at(time_str).do(send_scheduled_report)
                    
                    logger.info(f"تمت جدولة التقرير {template_id} أسبوعياً يوم {day} في الساعة {time_str}")
                
                elif schedule_type == 'monthly':
                    day = report_config.get('day', 1)
                    time_str = report_config.get('time', '00:00')
                    
                    # جدولة شهرية (يتم التحقق من اليوم في كل تشغيل)
                    def monthly_job():
                        if datetime.now().day == day:
                            send_scheduled_report()
                    
                    schedule.every().day.at(time_str).do(monthly_job)
                    logger.info(f"تمت جدولة التقرير {template_id} شهرياً في اليوم {day} الساعة {time_str}")
            
            # تشغيل خيط منفصل لتنفيذ المهام المجدولة
            def run_scheduler():
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
            
            # حفظ مرجع للخيط
            self.scheduler_thread = scheduler_thread
            
            logger.info("تم بدء جدولة التقارير")
            
            return True
        
        except Exception as e:
            logger.error(f"خطأ في جدولة التقارير: {str(e)}")
            return False
    
    def get_available_report_templates(self):
        """
        الحصول على قائمة قوالب التقارير المتاحة
        
        العوائد:
            list: قائمة قوالب التقارير المتاحة
        """
        templates = []
        
        for template_id, template_config in self.config.get('report_templates', {}).items():
            templates.append({
                'id': template_id,
                'name': template_config.get('name', template_id),
                'description': template_config.get('description', ''),
                'available_formats': template_config.get('available_formats', [])
            })
        
        return templates
    
    def get_scheduled_reports(self):
        """
        الحصول على قائمة التقارير المجدولة
        
        العوائد:
            list: قائمة التقارير المجدولة
        """
        return self.config.get('scheduled_reports', [])
    
    # دوال مساعدة لجمع البيانات
    
    def _get_disease_detections_data(self, parameters):
        """
        جلب بيانات تشخيص الأمراض
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات تشخيص الأمراض
        """
        # تحديد الفترة الزمنية
        days = parameters.get('days', 30)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = f"""
            SELECT dd.*, d.name as disease_name, p.name as plant_name, p.variety as plant_variety
            FROM disease_detection dd
            JOIN disease d ON dd.disease_id = d.id
            JOIN plant p ON dd.plant_id = p.id
            WHERE dd.detection_date >= '{start_date.strftime('%Y-%m-%d')}'
            AND dd.detection_date <= '{end_date.strftime('%Y-%m-%d')}'
            ORDER BY dd.detection_date DESC
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    detections = [dict(row) for row in result]
                    return detections
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات تشخيص الأمراض: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 1,
                    'plant_id': 101,
                    'disease_id': 201,
                    'detection_date': '2023-01-15',
                    'confidence': 0.95,
                    'status': 'confirmed',
                    'disease_name': 'اللفحة المتأخرة',
                    'plant_name': 'طماطم',
                    'plant_variety': 'مونيميكر'
                },
                {
                    'id': 2,
                    'plant_id': 102,
                    'disease_id': 202,
                    'detection_date': '2023-01-16',
                    'confidence': 0.87,
                    'status': 'confirmed',
                    'disease_name': 'البياض الدقيقي',
                    'plant_name': 'خيار',
                    'plant_variety': 'بيت ألفا'
                }
            ]
    
    def _get_plants_data(self, parameters):
        """
        جلب بيانات النباتات
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات النباتات
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT p.*, n.name as nursery_name
            FROM plant p
            JOIN nursery n ON p.nursery_id = n.id
            ORDER BY p.planting_date DESC
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    plants = [dict(row) for row in result]
                    return plants
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات النباتات: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 101,
                    'name': 'طماطم',
                    'variety': 'مونيميكر',
                    'planting_date': '2023-01-01',
                    'nursery_id': 1,
                    'nursery_name': 'مشتل الوادي'
                },
                {
                    'id': 102,
                    'name': 'خيار',
                    'variety': 'بيت ألفا',
                    'planting_date': '2023-01-05',
                    'nursery_id': 2,
                    'nursery_name': 'مشتل الخضراء'
                }
            ]
    
    def _get_diseases_data(self, parameters):
        """
        جلب بيانات الأمراض
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات الأمراض
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT *
            FROM disease
            ORDER BY name
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    diseases = [dict(row) for row in result]
                    return diseases
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات الأمراض: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 201,
                    'name': 'اللفحة المتأخرة',
                    'description': 'مرض فطري يصيب الطماطم والبطاطس',
                    'symptoms': 'بقع بنية على الأوراق والثمار',
                    'treatment': 'رش مبيدات فطرية'
                },
                {
                    'id': 202,
                    'name': 'البياض الدقيقي',
                    'description': 'مرض فطري يصيب العديد من النباتات',
                    'symptoms': 'طبقة بيضاء على الأوراق',
                    'treatment': 'رش مبيدات فطرية وتحسين التهوية'
                }
            ]
    
    def _get_breeding_requests_data(self, parameters):
        """
        جلب بيانات طلبات التهجين
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات طلبات التهجين
        """
        # تحديد الفترة الزمنية
        days = parameters.get('days', 90)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = f"""
            SELECT br.*, p1.name as parent1_name, p1.variety as parent1_variety,
                   p2.name as parent2_name, p2.variety as parent2_variety
            FROM breeding_request br
            JOIN plant p1 ON br.parent1_id = p1.id
            JOIN plant p2 ON br.parent2_id = p2.id
            WHERE br.request_date >= '{start_date.strftime('%Y-%m-%d')}'
            AND br.request_date <= '{end_date.strftime('%Y-%m-%d')}'
            ORDER BY br.request_date DESC
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    requests = [dict(row) for row in result]
                    return requests
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات طلبات التهجين: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 301,
                    'parent1_id': 101,
                    'parent2_id': 103,
                    'target_traits': 'مقاومة الجفاف، إنتاجية عالية',
                    'request_date': '2023-01-10',
                    'status': 'completed',
                    'parent1_name': 'طماطم',
                    'parent1_variety': 'مونيميكر',
                    'parent2_name': 'طماطم',
                    'parent2_variety': 'ريو جراندي'
                },
                {
                    'id': 302,
                    'parent1_id': 102,
                    'parent2_id': 104,
                    'target_traits': 'مقاومة الأمراض، حجم كبير',
                    'request_date': '2023-01-15',
                    'status': 'in_progress',
                    'parent1_name': 'خيار',
                    'parent1_variety': 'بيت ألفا',
                    'parent2_name': 'خيار',
                    'parent2_variety': 'سوبر ستار'
                }
            ]
    
    def _get_breeding_results_data(self, parameters):
        """
        جلب بيانات نتائج التهجين
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات نتائج التهجين
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT br.*, req.parent1_id, req.parent2_id, req.target_traits,
                   p1.name as parent1_name, p1.variety as parent1_variety,
                   p2.name as parent2_name, p2.variety as parent2_variety
            FROM breeding_result br
            JOIN breeding_request req ON br.request_id = req.id
            JOIN plant p1 ON req.parent1_id = p1.id
            JOIN plant p2 ON req.parent2_id = p2.id
            ORDER BY br.result_date DESC
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    results = [dict(row) for row in result]
                    return results
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات نتائج التهجين: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 401,
                    'request_id': 301,
                    'result_date': '2023-01-20',
                    'predicted_traits': 'مقاومة الجفاف: عالية، إنتاجية: متوسطة',
                    'success_probability': 0.85,
                    'recommendations': 'يوصى بزراعة في مناطق قليلة المياه',
                    'parent1_id': 101,
                    'parent2_id': 103,
                    'target_traits': 'مقاومة الجفاف، إنتاجية عالية',
                    'parent1_name': 'طماطم',
                    'parent1_variety': 'مونيميكر',
                    'parent2_name': 'طماطم',
                    'parent2_variety': 'ريو جراندي'
                }
            ]
    
    def _get_varieties_data(self, parameters):
        """
        جلب بيانات الأصناف
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات الأصناف
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT DISTINCT name, variety, COUNT(*) as count
            FROM plant
            GROUP BY name, variety
            ORDER BY name, variety
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    varieties = [dict(row) for row in result]
                    return varieties
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات الأصناف: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'name': 'طماطم',
                    'variety': 'مونيميكر',
                    'count': 50
                },
                {
                    'name': 'طماطم',
                    'variety': 'ريو جراندي',
                    'count': 30
                },
                {
                    'name': 'خيار',
                    'variety': 'بيت ألفا',
                    'count': 40
                },
                {
                    'name': 'خيار',
                    'variety': 'سوبر ستار',
                    'count': 25
                }
            ]
    
    def _get_nurseries_data(self, parameters):
        """
        جلب بيانات المشاتل
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات المشاتل
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT n.*, COUNT(p.id) as plant_count
            FROM nursery n
            LEFT JOIN plant p ON n.id = p.nursery_id
            GROUP BY n.id
            ORDER BY n.name
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    nurseries = [dict(row) for row in result]
                    
                    # حساب نسبة الإشغال
                    for nursery in nurseries:
                        nursery['occupancy_rate'] = (nursery['plant_count'] / nursery['capacity']) * 100 if nursery['capacity'] > 0 else 0
                    
                    return nurseries
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات المشاتل: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 1,
                    'name': 'مشتل الوادي',
                    'location': 'المنطقة الشرقية',
                    'capacity': 1000,
                    'status': 'active',
                    'plant_count': 750,
                    'occupancy_rate': 75.0
                },
                {
                    'id': 2,
                    'name': 'مشتل الخضراء',
                    'location': 'المنطقة الغربية',
                    'capacity': 800,
                    'status': 'active',
                    'plant_count': 600,
                    'occupancy_rate': 75.0
                }
            ]
    
    def _get_yield_predictions_data(self, parameters):
        """
        جلب بيانات توقعات الإنتاج
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات توقعات الإنتاج
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT yp.*, f.name as farm_name, c.name as crop_name
            FROM yield_prediction yp
            JOIN farm f ON yp.farm_id = f.id
            JOIN crop c ON yp.crop_id = c.id
            ORDER BY yp.prediction_date DESC
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    predictions = [dict(row) for row in result]
                    return predictions
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات توقعات الإنتاج: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 501,
                    'farm_id': 1,
                    'crop_id': 1,
                    'prediction_date': '2023-01-15',
                    'predicted_yield': 5000,
                    'confidence': 0.9,
                    'farm_name': 'مزرعة النخيل',
                    'crop_name': 'طماطم'
                },
                {
                    'id': 502,
                    'farm_id': 2,
                    'crop_id': 2,
                    'prediction_date': '2023-01-16',
                    'predicted_yield': 3500,
                    'confidence': 0.85,
                    'farm_name': 'مزرعة الواحة',
                    'crop_name': 'خيار'
                }
            ]
    
    def _get_farms_data(self, parameters):
        """
        جلب بيانات المزارع
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات المزارع
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT *
            FROM farm
            ORDER BY name
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    farms = [dict(row) for row in result]
                    return farms
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات المزارع: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 1,
                    'name': 'مزرعة النخيل',
                    'location': 'المنطقة الشرقية',
                    'area': 500,
                    'owner': 'أحمد محمد'
                },
                {
                    'id': 2,
                    'name': 'مزرعة الواحة',
                    'location': 'المنطقة الغربية',
                    'area': 350,
                    'owner': 'محمد علي'
                }
            ]
    
    def _get_crops_data(self, parameters):
        """
        جلب بيانات المحاصيل
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات المحاصيل
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT *
            FROM crop
            ORDER BY name
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    crops = [dict(row) for row in result]
                    return crops
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات المحاصيل: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 1,
                    'name': 'طماطم',
                    'category': 'خضروات',
                    'growing_season': 'صيف',
                    'days_to_harvest': 90
                },
                {
                    'id': 2,
                    'name': 'خيار',
                    'category': 'خضروات',
                    'growing_season': 'صيف',
                    'days_to_harvest': 60
                }
            ]
    
    def _get_soil_analyses_data(self, parameters):
        """
        جلب بيانات تحليل التربة
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات تحليل التربة
        """
        # تحديد الفترة الزمنية
        days = parameters.get('days', 90)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = f"""
            SELECT sa.*, f.name as farm_name, st.name as soil_type_name
            FROM soil_analysis sa
            JOIN farm f ON sa.farm_id = f.id
            JOIN soil_type st ON sa.soil_type_id = st.id
            WHERE sa.analysis_date >= '{start_date.strftime('%Y-%m-%d')}'
            AND sa.analysis_date <= '{end_date.strftime('%Y-%m-%d')}'
            ORDER BY sa.analysis_date DESC
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    analyses = [dict(row) for row in result]
                    return analyses
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات تحليل التربة: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 601,
                    'farm_id': 1,
                    'soil_type_id': 1,
                    'analysis_date': '2023-01-10',
                    'ph': 6.8,
                    'nitrogen': 40,
                    'phosphorus': 30,
                    'potassium': 25,
                    'organic_matter': 3.5,
                    'farm_name': 'مزرعة النخيل',
                    'soil_type_name': 'طينية'
                },
                {
                    'id': 602,
                    'farm_id': 2,
                    'soil_type_id': 2,
                    'analysis_date': '2023-01-15',
                    'ph': 7.2,
                    'nitrogen': 35,
                    'phosphorus': 25,
                    'potassium': 30,
                    'organic_matter': 2.8,
                    'farm_name': 'مزرعة الواحة',
                    'soil_type_name': 'رملية'
                }
            ]
    
    def _get_soil_types_data(self, parameters):
        """
        جلب بيانات أنواع التربة
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            list: بيانات أنواع التربة
        """
        # استعلام البيانات من قاعدة البيانات
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            query = """
            SELECT *
            FROM soil_type
            ORDER BY name
            """
            
            try:
                with self.db_integration.erp_engine.connect() as conn:
                    result = conn.execute(query)
                    soil_types = [dict(row) for row in result]
                    return soil_types
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات أنواع التربة: {str(e)}")
                return []
        else:
            # بيانات تجريبية
            return [
                {
                    'id': 1,
                    'name': 'طينية',
                    'description': 'تربة ذات محتوى عالي من الطين',
                    'characteristics': 'احتفاظ جيد بالماء، تهوية ضعيفة'
                },
                {
                    'id': 2,
                    'name': 'رملية',
                    'description': 'تربة ذات محتوى عالي من الرمل',
                    'characteristics': 'تصريف جيد للماء، تهوية جيدة، احتفاظ ضعيف بالمغذيات'
                }
            ]
    
    def _get_integration_status_data(self, parameters):
        """
        جلب بيانات حالة التكامل
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            dict: بيانات حالة التكامل
        """
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            try:
                # التحقق من حالة الاتصال بقواعد البيانات
                erp_connection_status = False
                ai_connection_status = False
                
                try:
                    with self.db_integration.erp_engine.connect() as conn:
                        conn.execute("SELECT 1")
                        erp_connection_status = True
                except:
                    pass
                
                try:
                    with self.db_integration.ai_engine.connect() as conn:
                        conn.execute("SELECT 1")
                        ai_connection_status = True
                except:
                    pass
                
                # جلب آخر وقت مزامنة
                last_sync = self.db_integration.last_sync
                
                # حساب عدد الجداول المتزامنة
                sync_tables_count = len(self.db_integration.sync_tables)
                
                # إعداد بيانات حالة التكامل
                status_data = {
                    'erp_connection_status': erp_connection_status,
                    'ai_connection_status': ai_connection_status,
                    'last_sync': last_sync,
                    'sync_tables_count': sync_tables_count,
                    'sync_tables': self.db_integration.sync_tables
                }
                
                return status_data
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات حالة التكامل: {str(e)}")
                return {'error': str(e)}
        else:
            # بيانات تجريبية
            return {
                'erp_connection_status': True,
                'ai_connection_status': True,
                'last_sync': {
                    'nurseries': '2023-01-20T10:00:00',
                    'plants': '2023-01-20T10:00:00',
                    'diseases': '2023-01-20T10:00:00',
                    'disease_detections': '2023-01-20T10:00:00',
                    'breeding_requests': '2023-01-20T10:00:00',
                    'breeding_results': '2023-01-20T10:00:00'
                },
                'sync_tables_count': 6,
                'sync_tables': {
                    'nurseries': {
                        'erp_table': 'nursery',
                        'ai_table': 'nurseries',
                        'direction': 'erp_to_ai'
                    },
                    'plants': {
                        'erp_table': 'plant',
                        'ai_table': 'plants',
                        'direction': 'bidirectional'
                    },
                    'diseases': {
                        'erp_table': 'disease',
                        'ai_table': 'diseases',
                        'direction': 'ai_to_erp'
                    },
                    'disease_detections': {
                        'erp_table': 'disease_detection',
                        'ai_table': 'disease_detections',
                        'direction': 'ai_to_erp'
                    },
                    'breeding_requests': {
                        'erp_table': 'breeding_request',
                        'ai_table': 'breeding_requests',
                        'direction': 'erp_to_ai'
                    },
                    'breeding_results': {
                        'erp_table': 'breeding_result',
                        'ai_table': 'breeding_results',
                        'direction': 'ai_to_erp'
                    }
                }
            }
    
    def _get_data_integrity_data(self, parameters):
        """
        جلب بيانات سلامة البيانات
        
        المعلمات:
            parameters (dict): معلمات التقرير
            
        العوائد:
            dict: بيانات سلامة البيانات
        """
        if self.db_integration:
            # استخدام وحدة تكامل قواعد البيانات
            try:
                # التحقق من سلامة البيانات
                integrity_results = self.db_integration.verify_all_tables_integrity()
                return integrity_results
            except Exception as e:
                logger.error(f"خطأ في جلب بيانات سلامة البيانات: {str(e)}")
                return {'error': str(e)}
        else:
            # بيانات تجريبية
            return {
                'nurseries': {
                    'total_records_erp': 10,
                    'total_records_ai': 10,
                    'common_records': 10,
                    'missing_in_ai': [],
                    'missing_in_erp': [],
                    'mismatched_records': [],
                    'integrity_score': 1.0
                },
                'plants': {
                    'total_records_erp': 150,
                    'total_records_ai': 145,
                    'common_records': 145,
                    'missing_in_ai': [146, 147, 148, 149, 150],
                    'missing_in_erp': [],
                    'mismatched_records': [],
                    'integrity_score': 0.97
                },
                'diseases': {
                    'total_records_erp': 50,
                    'total_records_ai': 52,
                    'common_records': 50,
                    'missing_in_ai': [],
                    'missing_in_erp': [51, 52],
                    'mismatched_records': [],
                    'integrity_score': 0.96
                },
                'summary': {
                    'total_tables': 6,
                    'tables_checked': 6,
                    'avg_integrity_score': 0.98
                }
            }
    
    # دوال إنشاء الرسوم البيانية
    
    def _create_disease_distribution_chart(self, report_data):
        """
        إنشاء رسم بياني لتوزيع الأمراض
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات تشخيص الأمراض
            detections = report_data.get('disease_detections', [])
            
            if not detections:
                return None
            
            # حساب توزيع الأمراض
            disease_counts = {}
            
            for detection in detections:
                disease_name = detection.get('disease_name', 'غير معروف')
                disease_counts[disease_name] = disease_counts.get(disease_name, 0) + 1
            
            # إنشاء DataFrame
            df = pd.DataFrame({
                'disease': list(disease_counts.keys()),
                'count': list(disease_counts.values())
            })
            
            # ترتيب البيانات تنازلياً
            df = df.sort_values('count', ascending=False)
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            sns.barplot(x='count', y='disease', data=df)
            plt.title('توزيع الأمراض المكتشفة', fontsize=16)
            plt.xlabel('عدد الحالات', fontsize=12)
            plt.ylabel('المرض', fontsize=12)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'disease_distribution.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتوزيع الأمراض: {str(e)}")
            return None
    
    def _create_detection_timeline_chart(self, report_data):
        """
        إنشاء رسم بياني لتوقيت اكتشاف الأمراض
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات تشخيص الأمراض
            detections = report_data.get('disease_detections', [])
            
            if not detections:
                return None
            
            # تحويل تاريخ الاكتشاف إلى تاريخ
            for detection in detections:
                detection['detection_date'] = pd.to_datetime(detection['detection_date'])
            
            # إنشاء DataFrame
            df = pd.DataFrame(detections)
            
            # حساب عدد الاكتشافات حسب التاريخ
            timeline_data = df.groupby([pd.Grouper(key='detection_date', freq='D'), 'disease_name']).size().reset_index(name='count')
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(12, 6))
            
            # رسم خط لكل مرض
            for disease in timeline_data['disease_name'].unique():
                disease_data = timeline_data[timeline_data['disease_name'] == disease]
                plt.plot(disease_data['detection_date'], disease_data['count'], marker='o', label=disease)
            
            plt.title('توقيت اكتشاف الأمراض', fontsize=16)
            plt.xlabel('التاريخ', fontsize=12)
            plt.ylabel('عدد الحالات', fontsize=12)
            plt.legend(title='المرض')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'detection_timeline.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتوقيت اكتشاف الأمراض: {str(e)}")
            return None
    
    def _create_trait_comparison_chart(self, report_data):
        """
        إنشاء رسم بياني لمقارنة الصفات
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات نتائج التهجين
            results = report_data.get('breeding_results', [])
            
            if not results:
                return None
            
            # تحليل الصفات المتوقعة
            traits_data = []
            
            for result in results:
                # تقسيم الصفات المتوقعة إلى أزواج من الصفة والقيمة
                predicted_traits = result.get('predicted_traits', '')
                traits_pairs = [pair.strip() for pair in predicted_traits.split(',')]
                
                for pair in traits_pairs:
                    if ':' in pair:
                        trait, value = pair.split(':', 1)
                        traits_data.append({
                            'trait': trait.strip(),
                            'value': value.strip(),
                            'request_id': result.get('request_id')
                        })
            
            if not traits_data:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(traits_data)
            
            # تحويل القيم إلى فئات
            value_mapping = {
                'عالية': 3,
                'متوسطة': 2,
                'منخفضة': 1
            }
            
            df['value_numeric'] = df['value'].map(lambda x: value_mapping.get(x, 0))
            
            # حساب متوسط القيم لكل صفة
            trait_avg = df.groupby('trait')['value_numeric'].mean().reset_index()
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            sns.barplot(x='value_numeric', y='trait', data=trait_avg)
            plt.title('مقارنة الصفات المتوقعة', fontsize=16)
            plt.xlabel('متوسط القيمة (1=منخفضة، 2=متوسطة، 3=عالية)', fontsize=12)
            plt.ylabel('الصفة', fontsize=12)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'trait_comparison.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لمقارنة الصفات: {str(e)}")
            return None
    
    def _create_success_rate_chart(self, report_data):
        """
        إنشاء رسم بياني لمعدل نجاح التهجين
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات نتائج التهجين
            results = report_data.get('breeding_results', [])
            
            if not results:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(results)
            
            # تصنيف احتمالية النجاح
            def classify_probability(prob):
                if prob >= 0.8:
                    return 'عالية (>= 80%)'
                elif prob >= 0.6:
                    return 'متوسطة (60-79%)'
                elif prob >= 0.4:
                    return 'متوسطة منخفضة (40-59%)'
                else:
                    return 'منخفضة (< 40%)'
            
            df['probability_category'] = df['success_probability'].apply(classify_probability)
            
            # حساب عدد النتائج في كل فئة
            probability_counts = df['probability_category'].value_counts().reset_index()
            probability_counts.columns = ['category', 'count']
            
            # ترتيب الفئات
            category_order = ['عالية (>= 80%)', 'متوسطة (60-79%)', 'متوسطة منخفضة (40-59%)', 'منخفضة (< 40%)']
            probability_counts['category'] = pd.Categorical(probability_counts['category'], categories=category_order, ordered=True)
            probability_counts = probability_counts.sort_values('category')
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x='category', y='count', data=probability_counts)
            
            # إضافة النسب المئوية
            total = probability_counts['count'].sum()
            for i, p in enumerate(ax.patches):
                percentage = 100 * p.get_height() / total
                ax.annotate(f'{percentage:.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=10)
            
            plt.title('معدل نجاح التهجين', fontsize=16)
            plt.xlabel('احتمالية النجاح', fontsize=12)
            plt.ylabel('عدد النتائج', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'success_rate.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لمعدل نجاح التهجين: {str(e)}")
            return None
    
    def _create_occupancy_rate_chart(self, report_data):
        """
        إنشاء رسم بياني لنسبة إشغال المشاتل
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات المشاتل
            nurseries = report_data.get('nurseries', [])
            
            if not nurseries:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(nurseries)
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(12, 6))
            
            # رسم نسبة الإشغال
            ax = sns.barplot(x='name', y='occupancy_rate', data=df)
            
            # إضافة خط لمتوسط نسبة الإشغال
            avg_occupancy = df['occupancy_rate'].mean()
            plt.axhline(y=avg_occupancy, color='r', linestyle='--', label=f'المتوسط: {avg_occupancy:.1f}%')
            
            # إضافة النسب على الأعمدة
            for i, p in enumerate(ax.patches):
                ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=10)
            
            plt.title('نسبة إشغال المشاتل', fontsize=16)
            plt.xlabel('المشتل', fontsize=12)
            plt.ylabel('نسبة الإشغال (%)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'occupancy_rate.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لنسبة إشغال المشاتل: {str(e)}")
            return None
    
    def _create_variety_distribution_chart(self, report_data):
        """
        إنشاء رسم بياني لتوزيع الأصناف
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات الأصناف
            varieties = report_data.get('varieties', [])
            
            if not varieties:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(varieties)
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(12, 8))
            
            # إنشاء مخطط دائري لكل محصول
            crops = df['name'].unique()
            
            if len(crops) <= 2:
                # إذا كان عدد المحاصيل 2 أو أقل، استخدم تخطيط 1×2
                fig, axes = plt.subplots(1, len(crops), figsize=(12, 6))
                if len(crops) == 1:
                    axes = [axes]  # تحويل إلى قائمة إذا كان هناك محصول واحد فقط
            else:
                # إذا كان عدد المحاصيل أكثر من 2، استخدم تخطيط 2×n
                cols = 2
                rows = (len(crops) + 1) // 2
                fig, axes = plt.subplots(rows, cols, figsize=(12, 6 * rows))
                axes = axes.flatten()
            
            for i, crop in enumerate(crops):
                crop_data = df[df['name'] == crop]
                
                # حساب النسب المئوية
                total = crop_data['count'].sum()
                crop_data['percentage'] = crop_data['count'] / total * 100
                
                # رسم المخطط الدائري
                wedges, texts, autotexts = axes[i].pie(
                    crop_data['count'],
                    labels=crop_data['variety'],
                    autopct='%1.1f%%',
                    startangle=90,
                    wedgeprops={'edgecolor': 'w'}
                )
                
                # تنسيق النص
                for text in texts:
                    text.set_fontsize(10)
                for autotext in autotexts:
                    autotext.set_fontsize(8)
                
                axes[i].set_title(f'توزيع أصناف {crop}')
            
            # إخفاء المحاور الفارغة
            for j in range(i + 1, len(axes)):
                axes[j].axis('off')
            
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'variety_distribution.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتوزيع الأصناف: {str(e)}")
            return None
    
    def _create_yield_comparison_chart(self, report_data):
        """
        إنشاء رسم بياني لمقارنة الإنتاج
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات توقعات الإنتاج
            predictions = report_data.get('yield_predictions', [])
            
            if not predictions:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(predictions)
            
            # حساب متوسط الإنتاج المتوقع لكل محصول
            crop_avg = df.groupby('crop_name')['predicted_yield'].mean().reset_index()
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x='crop_name', y='predicted_yield', data=crop_avg)
            
            # إضافة القيم على الأعمدة
            for i, p in enumerate(ax.patches):
                ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=10)
            
            plt.title('متوسط الإنتاج المتوقع حسب المحصول', fontsize=16)
            plt.xlabel('المحصول', fontsize=12)
            plt.ylabel('الإنتاج المتوقع (كجم)', fontsize=12)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'yield_comparison.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لمقارنة الإنتاج: {str(e)}")
            return None
    
    def _create_prediction_accuracy_chart(self, report_data):
        """
        إنشاء رسم بياني لدقة التنبؤ
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات توقعات الإنتاج
            predictions = report_data.get('yield_predictions', [])
            
            if not predictions:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(predictions)
            
            # تصنيف مستوى الثقة
            def classify_confidence(conf):
                if conf >= 0.9:
                    return 'عالية جداً (>= 90%)'
                elif conf >= 0.8:
                    return 'عالية (80-89%)'
                elif conf >= 0.7:
                    return 'متوسطة (70-79%)'
                elif conf >= 0.6:
                    return 'متوسطة منخفضة (60-69%)'
                else:
                    return 'منخفضة (< 60%)'
            
            df['confidence_category'] = df['confidence'].apply(classify_confidence)
            
            # حساب عدد التنبؤات في كل فئة
            confidence_counts = df['confidence_category'].value_counts().reset_index()
            confidence_counts.columns = ['category', 'count']
            
            # ترتيب الفئات
            category_order = ['عالية جداً (>= 90%)', 'عالية (80-89%)', 'متوسطة (70-79%)', 'متوسطة منخفضة (60-69%)', 'منخفضة (< 60%)']
            confidence_counts['category'] = pd.Categorical(confidence_counts['category'], categories=category_order, ordered=True)
            confidence_counts = confidence_counts.sort_values('category')
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x='category', y='count', data=confidence_counts)
            
            # إضافة النسب المئوية
            total = confidence_counts['count'].sum()
            for i, p in enumerate(ax.patches):
                percentage = 100 * p.get_height() / total
                ax.annotate(f'{percentage:.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=10)
            
            plt.title('دقة التنبؤ بالإنتاج', fontsize=16)
            plt.xlabel('مستوى الثقة', fontsize=12)
            plt.ylabel('عدد التنبؤات', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'prediction_accuracy.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لدقة التنبؤ: {str(e)}")
            return None
    
    def _create_nutrient_levels_chart(self, report_data):
        """
        إنشاء رسم بياني لمستويات العناصر الغذائية
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات تحليل التربة
            analyses = report_data.get('soil_analyses', [])
            
            if not analyses:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(analyses)
            
            # تحديد العناصر الغذائية للرسم البياني
            nutrients = ['nitrogen', 'phosphorus', 'potassium']
            nutrient_names = {'nitrogen': 'النيتروجين', 'phosphorus': 'الفوسفور', 'potassium': 'البوتاسيوم'}
            
            # إعادة تنظيم البيانات
            melted_df = pd.melt(df, id_vars=['farm_name', 'soil_type_name'],
                                value_vars=nutrients,
                                var_name='nutrient', value_name='level')
            
            # تعيين أسماء العناصر الغذائية بالعربية
            melted_df['nutrient'] = melted_df['nutrient'].map(nutrient_names)
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(12, 8))
            
            # رسم مستويات العناصر الغذائية لكل مزرعة
            ax = sns.barplot(x='farm_name', y='level', hue='nutrient', data=melted_df)
            
            plt.title('مستويات العناصر الغذائية حسب المزرعة', fontsize=16)
            plt.xlabel('المزرعة', fontsize=12)
            plt.ylabel('المستوى (جزء في المليون)', fontsize=12)
            plt.legend(title='العنصر الغذائي')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'nutrient_levels.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لمستويات العناصر الغذائية: {str(e)}")
            return None
    
    def _create_ph_distribution_chart(self, report_data):
        """
        إنشاء رسم بياني لتوزيع درجة الحموضة
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات تحليل التربة
            analyses = report_data.get('soil_analyses', [])
            
            if not analyses:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame(analyses)
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(10, 6))
            
            # رسم توزيع درجة الحموضة
            ax = sns.boxplot(x='soil_type_name', y='ph', data=df)
            
            # إضافة النقاط الفردية
            sns.swarmplot(x='soil_type_name', y='ph', data=df, color='black', alpha=0.5)
            
            # إضافة خطوط لنطاق درجة الحموضة المثالية
            plt.axhline(y=6.5, color='g', linestyle='--', label='الحد الأدنى المثالي')
            plt.axhline(y=7.5, color='r', linestyle='--', label='الحد الأعلى المثالي')
            
            plt.title('توزيع درجة الحموضة حسب نوع التربة', fontsize=16)
            plt.xlabel('نوع التربة', fontsize=12)
            plt.ylabel('درجة الحموضة (pH)', fontsize=12)
            plt.legend()
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'ph_distribution.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتوزيع درجة الحموضة: {str(e)}")
            return None
    
    def _create_sync_status_chart(self, report_data):
        """
        إنشاء رسم بياني لحالة المزامنة
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات حالة التكامل
            integration_status = report_data.get('integration_status', {})
            
            if not integration_status or 'error' in integration_status:
                return None
            
            # جلب بيانات المزامنة
            sync_tables = integration_status.get('sync_tables', {})
            
            if not sync_tables:
                return None
            
            # إعداد البيانات للرسم البياني
            table_names = []
            erp_to_ai = []
            ai_to_erp = []
            
            for table_name, table_config in sync_tables.items():
                table_names.append(table_name)
                
                direction = table_config.get('direction', '')
                
                if direction in ['erp_to_ai', 'bidirectional']:
                    erp_to_ai.append(1)
                else:
                    erp_to_ai.append(0)
                
                if direction in ['ai_to_erp', 'bidirectional']:
                    ai_to_erp.append(1)
                else:
                    ai_to_erp.append(0)
            
            # إنشاء DataFrame
            df = pd.DataFrame({
                'table': table_names,
                'ERP -> AI': erp_to_ai,
                'AI -> ERP': ai_to_erp
            })
            
            # إعادة تنظيم البيانات
            melted_df = pd.melt(df, id_vars=['table'], var_name='direction', value_name='enabled')
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(12, 6))
            
            # رسم حالة المزامنة
            ax = sns.barplot(x='table', y='enabled', hue='direction', data=melted_df)
            
            # تعديل الألوان
            colors = {'ERP -> AI': 'blue', 'AI -> ERP': 'green'}
            for i, bar in enumerate(ax.patches):
                bar.set_color(colors['ERP -> AI'] if i < len(table_names) else colors['AI -> ERP'])
            
            plt.title('حالة مزامنة الجداول', fontsize=16)
            plt.xlabel('الجدول', fontsize=12)
            plt.ylabel('الحالة', fontsize=12)
            plt.yticks([0, 1], ['غير مفعل', 'مفعل'])
            plt.legend(title='اتجاه المزامنة')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'sync_status.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لحالة المزامنة: {str(e)}")
            return None
    
    def _create_integrity_score_chart(self, report_data):
        """
        إنشاء رسم بياني لدرجة سلامة البيانات
        
        المعلمات:
            report_data (dict): بيانات التقرير
            
        العوائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # جلب بيانات سلامة البيانات
            integrity_data = report_data.get('data_integrity', {})
            
            if not integrity_data or 'error' in integrity_data:
                return None
            
            # إعداد البيانات للرسم البياني
            table_names = []
            integrity_scores = []
            
            for table_name, table_data in integrity_data.items():
                if table_name == 'summary':
                    continue
                
                table_names.append(table_name)
                integrity_scores.append(table_data.get('integrity_score', 0))
            
            if not table_names:
                return None
            
            # إنشاء DataFrame
            df = pd.DataFrame({
                'table': table_names,
                'integrity_score': integrity_scores
            })
            
            # إنشاء الرسم البياني
            plt.figure(figsize=(12, 6))
            
            # رسم درجة سلامة البيانات
            ax = sns.barplot(x='table', y='integrity_score', data=df)
            
            # تلوين الأعمدة حسب درجة السلامة
            for i, p in enumerate(ax.patches):
                score = p.get_height()
                if score >= 0.9:
                    p.set_color('green')
                elif score >= 0.7:
                    p.set_color('orange')
                else:
                    p.set_color('red')
                
                # إضافة القيم على الأعمدة
                ax.annotate(f'{score:.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=10)
            
            # إضافة خط لمتوسط درجة السلامة
            avg_score = integrity_data.get('summary', {}).get('avg_integrity_score', 0)
            plt.axhline(y=avg_score, color='blue', linestyle='--', label=f'المتوسط: {avg_score:.2f}')
            
            plt.title('درجة سلامة البيانات', fontsize=16)
            plt.xlabel('الجدول', fontsize=12)
            plt.ylabel('درجة السلامة', fontsize=12)
            plt.ylim(0, 1.1)  # تحديد نطاق المحور Y
            plt.legend()
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.reports_dir, 'integrity_score.png')
            plt.savefig(chart_path)
            plt.close()
            
            return chart_path
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لدرجة سلامة البيانات: {str(e)}")
            return None


# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء كائن تكامل التقارير
    report_integration = ReportIntegration()
    
    # إنشاء تقرير
    report_path = report_integration.generate_report('disease_summary', {'days': 30}, 'pdf')
    print(f"تم إنشاء التقرير: {report_path}")
    
    # جدولة التقارير
    report_integration.schedule_reports()
