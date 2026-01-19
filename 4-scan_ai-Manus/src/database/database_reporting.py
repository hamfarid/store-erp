#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التقارير والتحليلات لقواعد البيانات
يوفر أدوات لإنشاء وتخصيص التقارير وتحليل البيانات المخزنة في قواعد البيانات
"""

import os
import json
import logging
import datetime
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import io
import base64
from jinja2 import Template
import csv
import xlsxwriter
from dotenv import load_dotenv
import re

# تحميل متغيرات البيئة
load_dotenv()

class DatabaseReporting:
    """نظام التقارير والتحليلات لقواعد البيانات"""
    
    def __init__(self, db_manager, config_path=None):
        """تهيئة نظام التقارير"""
        self.logger = logging.getLogger(__name__)
        self.db_manager = db_manager
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'reporting.json')
        self.reports_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')
        self.templates_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
        
        # إنشاء المجلدات اللازمة
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # تحميل التكوين
        self.config = self._load_config()
        
        # إنشاء جداول التقارير
        self._create_report_tables()
    
    def _load_config(self):
        """تحميل ملف التكوين"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # إنشاء ملف تكوين افتراضي
                config = {
                    'reporting': {
                        'default_format': 'html',
                        'available_formats': ['html', 'pdf', 'csv', 'excel', 'json'],
                        'chart_theme': 'default',
                        'default_locale': 'ar',
                        'date_format': '%Y-%m-%d',
                        'time_format': '%H:%M:%S',
                        'scheduled_reports': []
                    },
                    'analytics': {
                        'enable_trend_analysis': True,
                        'enable_predictive_analytics': True,
                        'prediction_horizon_days': 30,
                        'confidence_interval': 0.95,
                        'min_data_points': 10
                    },
                    'templates': {
                        'default_template': 'default',
                        'custom_templates': []
                    },
                    'export': {
                        'excel': {
                            'sheet_name': 'البيانات',
                            'include_charts': True
                        },
                        'pdf': {
                            'page_size': 'A4',
                            'orientation': 'portrait'
                        }
                    }
                }
                
                # حفظ التكوين الافتراضي
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                return config
        except Exception as e:
            self.logger.error(f"خطأ في تحميل ملف التكوين: {e}")
            # إعداد تكوين افتراضي
            return {
                'reporting': {
                    'default_format': 'html',
                    'available_formats': ['html', 'pdf', 'csv', 'excel', 'json'],
                    'chart_theme': 'default',
                    'default_locale': 'ar',
                    'date_format': '%Y-%m-%d',
                    'time_format': '%H:%M:%S',
                    'scheduled_reports': []
                },
                'analytics': {
                    'enable_trend_analysis': True,
                    'enable_predictive_analytics': True,
                    'prediction_horizon_days': 30,
                    'confidence_interval': 0.95,
                    'min_data_points': 10
                },
                'templates': {
                    'default_template': 'default',
                    'custom_templates': []
                },
                'export': {
                    'excel': {
                        'sheet_name': 'البيانات',
                        'include_charts': True
                    },
                    'pdf': {
                        'page_size': 'A4',
                        'orientation': 'portrait'
                    }
                }
            }
    
    def _create_report_tables(self):
        """إنشاء جداول التقارير في قاعدة البيانات التشغيلية"""
        try:
            # جدول تعريفات التقارير
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS report_definitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    query TEXT NOT NULL,
                    parameters TEXT,
                    chart_type TEXT,
                    chart_options TEXT,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    created_by TEXT,
                    category TEXT,
                    is_template INTEGER DEFAULT 0,
                    is_public INTEGER DEFAULT 0
                )
            ''')
            
            # جدول التقارير المجدولة
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS scheduled_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id INTEGER NOT NULL,
                    schedule_type TEXT NOT NULL,
                    schedule_value TEXT NOT NULL,
                    recipients TEXT,
                    format TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    last_run TIMESTAMP,
                    next_run TIMESTAMP,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (report_id) REFERENCES report_definitions (id)
                )
            ''')
            
            # جدول سجل تشغيل التقارير
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS report_execution_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id INTEGER NOT NULL,
                    execution_time TIMESTAMP NOT NULL,
                    duration_ms INTEGER,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    parameters TEXT,
                    output_format TEXT,
                    output_path TEXT,
                    executed_by TEXT,
                    FOREIGN KEY (report_id) REFERENCES report_definitions (id)
                )
            ''')
            
            # جدول تفضيلات المستخدم للتقارير
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS user_report_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    report_id INTEGER NOT NULL,
                    preferred_format TEXT,
                    chart_preferences TEXT,
                    filter_preferences TEXT,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (report_id) REFERENCES report_definitions (id)
                )
            ''')
            
            # جدول قوالب التقارير
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS report_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    html_template TEXT,
                    css_style TEXT,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    created_by TEXT,
                    is_default INTEGER DEFAULT 0
                )
            ''')
            
            # إنشاء قوالب افتراضية
            self._create_default_templates()
            
            # إنشاء تقارير افتراضية
            self._create_default_reports()
            
            self.logger.info("تم إنشاء جداول التقارير بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء جداول التقارير: {e}")
            raise
    
    def _create_default_templates(self):
        """إنشاء قوالب تقارير افتراضية"""
        try:
            # التحقق من وجود قوالب افتراضية
            default_template = self.db_manager.fetch_one('operational', 
                "SELECT id FROM report_templates WHERE is_default = 1")
            
            if not default_template:
                # إنشاء قالب افتراضي
                default_html = '''
                <!DOCTYPE html>
                <html dir="rtl" lang="ar">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{{ report_title }}</title>
                    <style>
                        {{ css_style }}
                    </style>
                </head>
                <body>
                    <div class="report-container">
                        <div class="report-header">
                            <h1>{{ report_title }}</h1>
                            <p class="report-description">{{ report_description }}</p>
                            <div class="report-meta">
                                <p>تاريخ التقرير: {{ report_date }}</p>
                                <p>تم إنشاؤه بواسطة: {{ report_author }}</p>
                            </div>
                        </div>
                        
                        <div class="report-parameters">
                            <h3>معايير التقرير:</h3>
                            <ul>
                                {% for param_name, param_value in report_parameters.items() %}
                                <li><strong>{{ param_name }}:</strong> {{ param_value }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                        
                        <div class="report-content">
                            {% if report_charts %}
                            <div class="report-charts">
                                {% for chart in report_charts %}
                                <div class="chart-container">
                                    <h3>{{ chart.title }}</h3>
                                    <img src="data:image/png;base64,{{ chart.image }}" alt="{{ chart.title }}">
                                </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                            
                            {% if report_tables %}
                            <div class="report-tables">
                                {% for table in report_tables %}
                                <div class="table-container">
                                    <h3>{{ table.title }}</h3>
                                    <table>
                                        <thead>
                                            <tr>
                                                {% for header in table.headers %}
                                                <th>{{ header }}</th>
                                                {% endfor %}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {% for row in table.rows %}
                                            <tr>
                                                {% for cell in row %}
                                                <td>{{ cell }}</td>
                                                {% endfor %}
                                            </tr>
                                            {% endfor %}
                                        </tbody>
                                    </table>
                                </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                            
                            {% if report_summary %}
                            <div class="report-summary">
                                <h3>ملخص التقرير</h3>
                                <div class="summary-content">
                                    {{ report_summary }}
                                </div>
                            </div>
                            {% endif %}
                        </div>
                        
                        <div class="report-footer">
                            <p>نظام الذكاء الاصطناعي الزراعي المتكامل</p>
                            <p>تم إنشاء هذا التقرير في {{ report_datetime }}</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
                
                default_css = '''
                body {
                    font-family: Arial, Tahoma, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                    color: #333;
                }
                
                .report-container {
                    max-width: 1200px;
                    margin: 20px auto;
                    background-color: #fff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    border-radius: 5px;
                    padding: 20px;
                }
                
                .report-header {
                    border-bottom: 2px solid #4CAF50;
                    padding-bottom: 20px;
                    margin-bottom: 20px;
                }
                
                .report-header h1 {
                    color: #2E7D32;
                    margin: 0 0 10px 0;
                }
                
                .report-description {
                    color: #555;
                    font-style: italic;
                }
                
                .report-meta {
                    font-size: 0.9em;
                    color: #777;
                }
                
                .report-parameters {
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
                
                .report-parameters h3 {
                    margin-top: 0;
                    color: #2E7D32;
                }
                
                .report-parameters ul {
                    margin: 0;
                    padding-right: 20px;
                }
                
                .chart-container {
                    margin-bottom: 30px;
                }
                
                .chart-container h3 {
                    color: #2E7D32;
                }
                
                .chart-container img {
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                
                .table-container {
                    margin-bottom: 30px;
                    overflow-x: auto;
                }
                
                .table-container h3 {
                    color: #2E7D32;
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                
                table th, table td {
                    padding: 12px 15px;
                    text-align: right;
                    border-bottom: 1px solid #ddd;
                }
                
                table th {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                }
                
                table tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                
                table tr:hover {
                    background-color: #e9f5e9;
                }
                
                .report-summary {
                    background-color: #e8f5e9;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 20px;
                }
                
                .report-summary h3 {
                    color: #2E7D32;
                    margin-top: 0;
                }
                
                .report-footer {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    font-size: 0.9em;
                    color: #777;
                }
                
                @media print {
                    body {
                        background-color: #fff;
                    }
                    
                    .report-container {
                        box-shadow: none;
                        margin: 0;
                        max-width: none;
                    }
                }
                '''
                
                # إدخال القالب الافتراضي
                self.db_manager.insert('operational', 'report_templates', {
                    'name': 'القالب الافتراضي',
                    'description': 'قالب التقارير الافتراضي للنظام',
                    'html_template': default_html,
                    'css_style': default_css,
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat(),
                    'created_by': 'system',
                    'is_default': 1
                })
                
                self.logger.info("تم إنشاء القالب الافتراضي بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء القوالب الافتراضية: {e}")
    
    def _create_default_reports(self):
        """إنشاء تقارير افتراضية"""
        try:
            # التحقق من وجود تقارير افتراضية
            default_reports = self.db_manager.fetch_all('operational', 
                "SELECT id FROM report_definitions WHERE created_by = 'system'")
            
            if not default_reports:
                # تقرير إحصائيات النظام
                self.db_manager.insert('operational', 'report_definitions', {
                    'name': 'إحصائيات النظام',
                    'description': 'تقرير إحصائي عن حالة النظام وأدائه',
                    'query': '''
                        SELECT 
                            metric_type, 
                            AVG(metric_value) as avg_value, 
                            MAX(metric_value) as max_value, 
                            MIN(metric_value) as min_value,
                            COUNT(*) as count
                        FROM performance_metrics
                        WHERE db_name = 'system' 
                        AND timestamp BETWEEN :start_date AND :end_date
                        GROUP BY metric_type
                    ''',
                    'parameters': json.dumps({
                        'start_date': {'type': 'date', 'default': 'today-7d'},
                        'end_date': {'type': 'date', 'default': 'today'}
                    }),
                    'chart_type': 'bar',
                    'chart_options': json.dumps({
                        'x_axis': 'metric_type',
                        'y_axis': 'avg_value',
                        'title': 'متوسط مقاييس النظام',
                        'color': '#4CAF50'
                    }),
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat(),
                    'created_by': 'system',
                    'category': 'system',
                    'is_template': 1,
                    'is_public': 1
                })
                
                # تقرير حالة قواعد البيانات
                self.db_manager.insert('operational', 'report_definitions', {
                    'name': 'حالة قواعد البيانات',
                    'description': 'تقرير عن حالة قواعد البيانات وحجمها',
                    'query': '''
                        SELECT 
                            db_name,
                            metric_type,
                            MAX(timestamp) as last_update,
                            metric_value
                        FROM performance_metrics
                        WHERE metric_type = 'db_size_mb'
                        AND timestamp BETWEEN :start_date AND :end_date
                        GROUP BY db_name
                    ''',
                    'parameters': json.dumps({
                        'start_date': {'type': 'date', 'default': 'today-7d'},
                        'end_date': {'type': 'date', 'default': 'today'}
                    }),
                    'chart_type': 'pie',
                    'chart_options': json.dumps({
                        'labels': 'db_name',
                        'values': 'metric_value',
                        'title': 'توزيع حجم قواعد البيانات'
                    }),
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat(),
                    'created_by': 'system',
                    'category': 'database',
                    'is_template': 1,
                    'is_public': 1
                })
                
                # تقرير الاستعلامات البطيئة
                self.db_manager.insert('operational', 'report_definitions', {
                    'name': 'الاستعلامات البطيئة',
                    'description': 'تقرير عن الاستعلامات البطيئة في النظام',
                    'query': '''
                        SELECT 
                            db_name,
                            query,
                            execution_time_ms,
                            timestamp
                        FROM slow_queries
                        WHERE timestamp BETWEEN :start_date AND :end_date
                        ORDER BY execution_time_ms DESC
                        LIMIT 20
                    ''',
                    'parameters': json.dumps({
                        'start_date': {'type': 'date', 'default': 'today-7d'},
                        'end_date': {'type': 'date', 'default': 'today'}
                    }),
                    'chart_type': 'bar',
                    'chart_options': json.dumps({
                        'x_axis': 'db_name',
                        'y_axis': 'execution_time_ms',
                        'title': 'وقت تنفيذ الاستعلامات البطيئة',
                        'color': '#FF5722'
                    }),
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat(),
                    'created_by': 'system',
                    'category': 'performance',
                    'is_template': 1,
                    'is_public': 1
                })
                
                self.logger.info("تم إنشاء التقارير الافتراضية بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء التقارير الافتراضية: {e}")
    
    def create_report_definition(self, name, description, query, parameters=None, chart_type=None, 
                                chart_options=None, category=None, is_template=False, is_public=False, 
                                created_by=None):
        """إنشاء تعريف تقرير جديد"""
        try:
            report_id = self.db_manager.insert('operational', 'report_definitions', {
                'name': name,
                'description': description,
                'query': query,
                'parameters': json.dumps(parameters) if parameters else None,
                'chart_type': chart_type,
                'chart_options': json.dumps(chart_options) if chart_options else None,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat(),
                'created_by': created_by,
                'category': category,
                'is_template': 1 if is_template else 0,
                'is_public': 1 if is_public else 0
            })
            
            self.logger.info(f"تم إنشاء تعريف التقرير '{name}' بنجاح (ID: {report_id})")
            return report_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تعريف التقرير: {e}")
            raise
    
    def update_report_definition(self, report_id, name=None, description=None, query=None, 
                                parameters=None, chart_type=None, chart_options=None, 
                                category=None, is_template=None, is_public=None):
        """تحديث تعريف تقرير"""
        try:
            # بناء قاموس التحديثات
            updates = {'updated_at': datetime.datetime.now().isoformat()}
            
            if name is not None:
                updates['name'] = name
            if description is not None:
                updates['description'] = description
            if query is not None:
                updates['query'] = query
            if parameters is not None:
                updates['parameters'] = json.dumps(parameters)
            if chart_type is not None:
                updates['chart_type'] = chart_type
            if chart_options is not None:
                updates['chart_options'] = json.dumps(chart_options)
            if category is not None:
                updates['category'] = category
            if is_template is not None:
                updates['is_template'] = 1 if is_template else 0
            if is_public is not None:
                updates['is_public'] = 1 if is_public else 0
            
            # تحديث التقرير
            self.db_manager.update('operational', 'report_definitions', updates, {'id': report_id})
            
            self.logger.info(f"تم تحديث تعريف التقرير (ID: {report_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تحديث تعريف التقرير: {e}")
            return False
    
    def delete_report_definition(self, report_id):
        """حذف تعريف تقرير"""
        try:
            # التحقق من وجود تقارير مجدولة مرتبطة
            scheduled = self.db_manager.fetch_one('operational', 
                "SELECT id FROM scheduled_reports WHERE report_id = ?", (report_id,))
            
            if scheduled:
                # إلغاء تنشيط التقارير المجدولة المرتبطة
                self.db_manager.update('operational', 'scheduled_reports', 
                    {'is_active': 0}, {'report_id': report_id})
            
            # حذف التقرير
            self.db_manager.delete('operational', 'report_definitions', {'id': report_id})
            
            self.logger.info(f"تم حذف تعريف التقرير (ID: {report_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف تعريف التقرير: {e}")
            return False
    
    def get_report_definition(self, report_id):
        """الحصول على تعريف تقرير"""
        try:
            report = self.db_manager.fetch_one('operational', 
                "SELECT * FROM report_definitions WHERE id = ?", (report_id,))
            
            if report:
                # تحويل البيانات المخزنة بتنسيق JSON
                report_dict = dict(report)
                if report_dict.get('parameters'):
                    report_dict['parameters'] = json.loads(report_dict['parameters'])
                if report_dict.get('chart_options'):
                    report_dict['chart_options'] = json.loads(report_dict['chart_options'])
                
                return report_dict
            else:
                return None
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على تعريف التقرير: {e}")
            return None
    
    def list_report_definitions(self, category=None, created_by=None, is_template=None, is_public=None):
        """قائمة تعريفات التقارير"""
        try:
            query = "SELECT id, name, description, category, created_by, created_at, is_template, is_public FROM report_definitions"
            params = []
            conditions = []
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if created_by:
                conditions.append("created_by = ?")
                params.append(created_by)
            
            if is_template is not None:
                conditions.append("is_template = ?")
                params.append(1 if is_template else 0)
            
            if is_public is not None:
                conditions.append("is_public = ?")
                params.append(1 if is_public else 0)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY category, name"
            
            reports = self.db_manager.fetch_all('operational', query, tuple(params))
            return [dict(report) for report in reports]
        except Exception as e:
            self.logger.error(f"خطأ في قائمة تعريفات التقارير: {e}")
            return []
    
    def schedule_report(self, report_id, schedule_type, schedule_value, recipients, format='pdf'):
        """جدولة تقرير"""
        try:
            # التحقق من صحة نوع الجدولة
            valid_types = ['daily', 'weekly', 'monthly', 'custom']
            if schedule_type not in valid_types:
                raise ValueError(f"نوع الجدولة غير صالح. القيم المسموح بها: {', '.join(valid_types)}")
            
            # التحقق من صحة تنسيق التقرير
            valid_formats = self.config['reporting']['available_formats']
            if format not in valid_formats:
                raise ValueError(f"تنسيق التقرير غير صالح. القيم المسموح بها: {', '.join(valid_formats)}")
            
            # حساب موعد التشغيل التالي
            next_run = self._calculate_next_run(schedule_type, schedule_value)
            
            # إدخال التقرير المجدول
            schedule_id = self.db_manager.insert('operational', 'scheduled_reports', {
                'report_id': report_id,
                'schedule_type': schedule_type,
                'schedule_value': schedule_value,
                'recipients': json.dumps(recipients) if isinstance(recipients, list) else recipients,
                'format': format,
                'is_active': 1,
                'last_run': None,
                'next_run': next_run.isoformat() if next_run else None,
                'created_at': datetime.datetime.now().isoformat()
            })
            
            self.logger.info(f"تم جدولة التقرير (ID: {report_id}) بنجاح (Schedule ID: {schedule_id})")
            return schedule_id
        except Exception as e:
            self.logger.error(f"خطأ في جدولة التقرير: {e}")
            raise
    
    def _calculate_next_run(self, schedule_type, schedule_value):
        """حساب موعد التشغيل التالي للتقرير المجدول"""
        now = datetime.datetime.now()
        
        if schedule_type == 'daily':
            # القيمة هي الوقت بتنسيق HH:MM
            try:
                hour, minute = map(int, schedule_value.split(':'))
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if next_run <= now:
                    next_run += datetime.timedelta(days=1)
            except:
                next_run = now + datetime.timedelta(days=1)
        
        elif schedule_type == 'weekly':
            # القيمة هي اليوم والوقت بتنسيق DAY,HH:MM
            try:
                day_str, time_str = schedule_value.split(',')
                day_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 
                          'friday': 4, 'saturday': 5, 'sunday': 6}
                day = day_map.get(day_str.lower(), 0)
                
                hour, minute = map(int, time_str.split(':'))
                
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                days_ahead = day - now.weekday()
                if days_ahead <= 0 or (days_ahead == 0 and next_run <= now):
                    days_ahead += 7
                next_run += datetime.timedelta(days=days_ahead)
            except:
                next_run = now + datetime.timedelta(days=7)
        
        elif schedule_type == 'monthly':
            # القيمة هي اليوم والوقت بتنسيق DAY,HH:MM
            try:
                day_str, time_str = schedule_value.split(',')
                day = int(day_str)
                hour, minute = map(int, time_str.split(':'))
                
                next_run = now.replace(day=1, hour=hour, minute=minute, second=0, microsecond=0)
                next_run = next_run.replace(month=now.month + 1 if now.month < 12 else 1)
                if now.month == 12:
                    next_run = next_run.replace(year=now.year + 1)
                
                # التعامل مع الأيام غير الموجودة في بعض الشهور
                last_day = (next_run.replace(month=next_run.month + 1 if next_run.month < 12 else 1, day=1) - 
                           datetime.timedelta(days=1)).day
                next_run = next_run.replace(day=min(day, last_day))
            except:
                next_run = now + datetime.timedelta(days=30)
        
        elif schedule_type == 'custom':
            # القيمة هي تعبير cron
            try:
                # تنفيذ تعبير cron (هذا مبسط، قد تحتاج إلى مكتبة متخصصة)
                next_run = now + datetime.timedelta(hours=1)
            except:
                next_run = now + datetime.timedelta(days=1)
        
        else:
            next_run = now + datetime.timedelta(days=1)
        
        return next_run
    
    def update_schedule(self, schedule_id, schedule_type=None, schedule_value=None, 
                       recipients=None, format=None, is_active=None):
        """تحديث جدولة تقرير"""
        try:
            # بناء قاموس التحديثات
            updates = {}
            
            if schedule_type is not None:
                # التحقق من صحة نوع الجدولة
                valid_types = ['daily', 'weekly', 'monthly', 'custom']
                if schedule_type not in valid_types:
                    raise ValueError(f"نوع الجدولة غير صالح. القيم المسموح بها: {', '.join(valid_types)}")
                updates['schedule_type'] = schedule_type
            
            if schedule_value is not None:
                updates['schedule_value'] = schedule_value
            
            if recipients is not None:
                updates['recipients'] = json.dumps(recipients) if isinstance(recipients, list) else recipients
            
            if format is not None:
                # التحقق من صحة تنسيق التقرير
                valid_formats = self.config['reporting']['available_formats']
                if format not in valid_formats:
                    raise ValueError(f"تنسيق التقرير غير صالح. القيم المسموح بها: {', '.join(valid_formats)}")
                updates['format'] = format
            
            if is_active is not None:
                updates['is_active'] = 1 if is_active else 0
            
            # إذا تم تغيير نوع الجدولة أو قيمتها، إعادة حساب موعد التشغيل التالي
            if schedule_type is not None or schedule_value is not None:
                # الحصول على البيانات الحالية
                current = self.db_manager.fetch_one('operational', 
                    "SELECT schedule_type, schedule_value FROM scheduled_reports WHERE id = ?", (schedule_id,))
                
                if current:
                    current_type = schedule_type if schedule_type is not None else current['schedule_type']
                    current_value = schedule_value if schedule_value is not None else current['schedule_value']
                    
                    next_run = self._calculate_next_run(current_type, current_value)
                    updates['next_run'] = next_run.isoformat() if next_run else None
            
            # تحديث الجدولة
            if updates:
                self.db_manager.update('operational', 'scheduled_reports', updates, {'id': schedule_id})
                
                self.logger.info(f"تم تحديث جدولة التقرير (ID: {schedule_id}) بنجاح")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"خطأ في تحديث جدولة التقرير: {e}")
            return False
    
    def delete_schedule(self, schedule_id):
        """حذف جدولة تقرير"""
        try:
            self.db_manager.delete('operational', 'scheduled_reports', {'id': schedule_id})
            
            self.logger.info(f"تم حذف جدولة التقرير (ID: {schedule_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف جدولة التقرير: {e}")
            return False
    
    def list_scheduled_reports(self, is_active=None):
        """قائمة التقارير المجدولة"""
        try:
            query = """
                SELECT sr.*, rd.name as report_name
                FROM scheduled_reports sr
                JOIN report_definitions rd ON sr.report_id = rd.id
            """
            params = []
            
            if is_active is not None:
                query += " WHERE sr.is_active = ?"
                params.append(1 if is_active else 0)
            
            query += " ORDER BY sr.next_run"
            
            schedules = self.db_manager.fetch_all('operational', query, tuple(params))
            
            result = []
            for schedule in schedules:
                schedule_dict = dict(schedule)
                if schedule_dict.get('recipients'):
                    try:
                        schedule_dict['recipients'] = json.loads(schedule_dict['recipients'])
                    except:
                        pass
                result.append(schedule_dict)
            
            return result
        except Exception as e:
            self.logger.error(f"خطأ في قائمة التقارير المجدولة: {e}")
            return []
    
    def run_report(self, report_id, parameters=None, output_format=None, executed_by=None):
        """تشغيل تقرير"""
        start_time = datetime.datetime.now()
        
        try:
            # الحصول على تعريف التقرير
            report_def = self.get_report_definition(report_id)
            if not report_def:
                raise ValueError(f"تعريف التقرير غير موجود (ID: {report_id})")
            
            # تحديد تنسيق الإخراج
            if not output_format:
                output_format = self.config['reporting']['default_format']
            
            # تسجيل بدء تنفيذ التقرير
            execution_id = self.db_manager.insert('operational', 'report_execution_log', {
                'report_id': report_id,
                'execution_time': start_time.isoformat(),
                'status': 'running',
                'parameters': json.dumps(parameters) if parameters else None,
                'output_format': output_format,
                'executed_by': executed_by
            })
            
            # تحضير المعلمات
            query_params = self._prepare_parameters(report_def, parameters)
            
            # تنفيذ الاستعلام
            db_name = 'operational'  # يمكن تغييره حسب نوع التقرير
            data = self.db_manager.fetch_all(db_name, report_def['query'], query_params)
            
            if not data:
                # تحديث سجل التنفيذ
                duration = (datetime.datetime.now() - start_time).total_seconds() * 1000
                self.db_manager.update('operational', 'report_execution_log', {
                    'duration_ms': duration,
                    'status': 'completed',
                    'error_message': 'لا توجد بيانات'
                }, {'id': execution_id})
                
                return {
                    'success': True,
                    'message': 'تم تنفيذ التقرير بنجاح ولكن لا توجد بيانات',
                    'data': [],
                    'execution_id': execution_id
                }
            
            # تحويل البيانات إلى DataFrame
            df = pd.DataFrame([dict(row) for row in data])
            
            # إنشاء الرسوم البيانية إذا كان مطلوبًا
            charts = []
            if report_def.get('chart_type') and report_def.get('chart_options'):
                chart_data = self._create_chart(df, report_def['chart_type'], report_def['chart_options'])
                if chart_data:
                    charts.append(chart_data)
            
            # إنشاء ملخص للبيانات
            summary = self._create_summary(df)
            
            # إنشاء التقرير بالتنسيق المطلوب
            output_path = self._generate_report_output(
                report_def, df, charts, summary, output_format, parameters, executed_by
            )
            
            # تحديث سجل التنفيذ
            duration = (datetime.datetime.now() - start_time).total_seconds() * 1000
            self.db_manager.update('operational', 'report_execution_log', {
                'duration_ms': duration,
                'status': 'completed',
                'output_path': output_path
            }, {'id': execution_id})
            
            return {
                'success': True,
                'message': 'تم تنفيذ التقرير بنجاح',
                'data': df.to_dict('records'),
                'charts': charts,
                'summary': summary,
                'output_path': output_path,
                'execution_id': execution_id
            }
        except Exception as e:
            # تسجيل الخطأ
            self.logger.error(f"خطأ في تنفيذ التقرير: {e}")
            
            # تحديث سجل التنفيذ
            try:
                duration = (datetime.datetime.now() - start_time).total_seconds() * 1000
                self.db_manager.update('operational', 'report_execution_log', {
                    'duration_ms': duration,
                    'status': 'error',
                    'error_message': str(e)
                }, {'id': execution_id})
            except:
                pass
            
            return {
                'success': False,
                'message': f'حدث خطأ أثناء تنفيذ التقرير: {str(e)}',
                'error': str(e)
            }
    
    def _prepare_parameters(self, report_def, user_params):
        """تحضير معلمات الاستعلام"""
        if not report_def.get('parameters'):
            return {}
        
        try:
            param_defs = report_def['parameters']
            params = {}
            
            for param_name, param_def in param_defs.items():
                # استخدام القيمة المقدمة من المستخدم أو القيمة الافتراضية
                if user_params and param_name in user_params:
                    value = user_params[param_name]
                elif 'default' in param_def:
                    value = param_def['default']
                else:
                    continue
                
                # معالجة القيم الخاصة للتواريخ
                if param_def.get('type') == 'date':
                    if isinstance(value, str):
                        if value.startswith('today'):
                            # مثال: today, today-7d, today+1m
                            today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                            
                            if value == 'today':
                                value = today
                            else:
                                # استخراج الفارق الزمني
                                match = re.match(r'today([+-])(\d+)([dmy])', value)
                                if match:
                                    op, num, unit = match.groups()
                                    num = int(num)
                                    
                                    if op == '-':
                                        num = -num
                                    
                                    if unit == 'd':
                                        value = today + datetime.timedelta(days=num)
                                    elif unit == 'm':
                                        # تقريبي: شهر = 30 يوم
                                        value = today + datetime.timedelta(days=num * 30)
                                    elif unit == 'y':
                                        # تقريبي: سنة = 365 يوم
                                        value = today + datetime.timedelta(days=num * 365)
                        
                        # تحويل التاريخ إلى نص بتنسيق ISO
                        if isinstance(value, datetime.datetime):
                            value = value.isoformat()
                
                params[param_name] = value
            
            return params
        except Exception as e:
            self.logger.error(f"خطأ في تحضير معلمات الاستعلام: {e}")
            return {}
    
    def _create_chart(self, df, chart_type, chart_options):
        """إنشاء رسم بياني"""
        try:
            plt.figure(figsize=(10, 6))
            
            # تعيين نمط الرسم البياني
            sns.set_theme(style="whitegrid")
            
            title = chart_options.get('title', 'الرسم البياني')
            
            if chart_type == 'bar':
                x_axis = chart_options.get('x_axis')
                y_axis = chart_options.get('y_axis')
                
                if not x_axis or not y_axis or x_axis not in df.columns or y_axis not in df.columns:
                    return None
                
                color = chart_options.get('color', '#4CAF50')
                ax = sns.barplot(x=x_axis, y=y_axis, data=df, color=color)
                
                # تدوير التسميات إذا كانت طويلة
                if df[x_axis].astype(str).str.len().max() > 10:
                    plt.xticks(rotation=45, ha='right')
            
            elif chart_type == 'line':
                x_axis = chart_options.get('x_axis')
                y_axis = chart_options.get('y_axis')
                
                if not x_axis or not y_axis or x_axis not in df.columns or y_axis not in df.columns:
                    return None
                
                color = chart_options.get('color', '#2196F3')
                ax = sns.lineplot(x=x_axis, y=y_axis, data=df, color=color)
            
            elif chart_type == 'pie':
                labels = chart_options.get('labels')
                values = chart_options.get('values')
                
                if not labels or not values or labels not in df.columns or values not in df.columns:
                    return None
                
                plt.pie(df[values], labels=df[labels], autopct='%1.1f%%', startangle=90)
                plt.axis('equal')
            
            elif chart_type == 'scatter':
                x_axis = chart_options.get('x_axis')
                y_axis = chart_options.get('y_axis')
                
                if not x_axis or not y_axis or x_axis not in df.columns or y_axis not in df.columns:
                    return None
                
                color = chart_options.get('color', '#9C27B0')
                ax = sns.scatterplot(x=x_axis, y=y_axis, data=df, color=color)
            
            else:
                return None
            
            plt.title(title)
            plt.tight_layout()
            
            # حفظ الرسم البياني كصورة في الذاكرة
            img_data = io.BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            
            # تحويل الصورة إلى Base64
            img_base64 = base64.b64encode(img_data.read()).decode()
            
            plt.close()
            
            return {
                'title': title,
                'type': chart_type,
                'image': img_base64
            }
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء الرسم البياني: {e}")
            plt.close()
            return None
    
    def _create_summary(self, df):
        """إنشاء ملخص للبيانات"""
        try:
            summary = []
            
            # عدد الصفوف
            summary.append(f"عدد السجلات: {len(df)}")
            
            # ملخص للأعمدة الرقمية
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                summary.append(f"إحصائيات {col}:")
                summary.append(f"  المتوسط: {df[col].mean():.2f}")
                summary.append(f"  الحد الأدنى: {df[col].min():.2f}")
                summary.append(f"  الحد الأقصى: {df[col].max():.2f}")
                summary.append(f"  الانحراف المعياري: {df[col].std():.2f}")
            
            # ملخص للأعمدة النصية
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if len(df[col].unique()) <= 10:  # فقط للأعمدة ذات القيم المحدودة
                    summary.append(f"توزيع {col}:")
                    value_counts = df[col].value_counts()
                    for value, count in value_counts.items():
                        summary.append(f"  {value}: {count} ({count/len(df)*100:.1f}%)")
            
            return "<br>".join(summary)
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء ملخص البيانات: {e}")
            return "لا يمكن إنشاء ملخص البيانات"
    
    def _generate_report_output(self, report_def, df, charts, summary, output_format, parameters, executed_by):
        """إنشاء ملف الإخراج للتقرير"""
        try:
            # إنشاء اسم الملف
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_base = f"report_{report_def['id']}_{timestamp}"
            
            if output_format == 'html':
                return self._generate_html_report(report_def, df, charts, summary, parameters, executed_by, filename_base)
            elif output_format == 'pdf':
                return self._generate_pdf_report(report_def, df, charts, summary, parameters, executed_by, filename_base)
            elif output_format == 'csv':
                return self._generate_csv_report(df, filename_base)
            elif output_format == 'excel':
                return self._generate_excel_report(report_def, df, charts, filename_base)
            elif output_format == 'json':
                return self._generate_json_report(report_def, df, charts, summary, parameters, filename_base)
            else:
                raise ValueError(f"تنسيق الإخراج غير مدعوم: {output_format}")
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء ملف الإخراج للتقرير: {e}")
            raise
    
    def _generate_html_report(self, report_def, df, charts, summary, parameters, executed_by, filename_base):
        """إنشاء تقرير بتنسيق HTML"""
        try:
            # الحصول على القالب
            template_id = self.config['templates']['default_template']
            template_data = self.db_manager.fetch_one('operational', 
                "SELECT * FROM report_templates WHERE is_default = 1 OR id = ? ORDER BY is_default DESC LIMIT 1", 
                (template_id,))
            
            if not template_data:
                raise ValueError("قالب التقرير غير موجود")
            
            # تحضير بيانات القالب
            template_vars = {
                'report_title': report_def['name'],
                'report_description': report_def['description'],
                'report_date': datetime.datetime.now().strftime(self.config['reporting']['date_format']),
                'report_datetime': datetime.datetime.now().strftime(
                    f"{self.config['reporting']['date_format']} {self.config['reporting']['time_format']}"),
                'report_author': executed_by or 'النظام',
                'report_parameters': parameters or {},
                'report_charts': charts,
                'report_summary': summary,
                'css_style': template_data['css_style'],
                'report_tables': []
            }
            
            # إضافة الجداول
            if not df.empty:
                table_data = {
                    'title': 'بيانات التقرير',
                    'headers': df.columns.tolist(),
                    'rows': df.values.tolist()
                }
                template_vars['report_tables'].append(table_data)
            
            # تطبيق القالب
            template = Template(template_data['html_template'])
            html_content = template.render(**template_vars)
            
            # حفظ الملف
            output_path = os.path.join(self.reports_dir, f"{filename_base}.html")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تقرير HTML: {e}")
            raise
    
    def _generate_pdf_report(self, report_def, df, charts, summary, parameters, executed_by, filename_base):
        """إنشاء تقرير بتنسيق PDF"""
        try:
            # إنشاء تقرير HTML أولاً
            html_path = self._generate_html_report(report_def, df, charts, summary, parameters, executed_by, filename_base)
            
            # تحويل HTML إلى PDF
            output_path = os.path.join(self.reports_dir, f"{filename_base}.pdf")
            
            # استخدام مكتبة weasyprint أو wkhtmltopdf (يجب تثبيتها)
            try:
                from weasyprint import HTML
                HTML(html_path).write_pdf(output_path)
            except ImportError:
                # استخدام wkhtmltopdf كبديل
                import subprocess
                subprocess.run(['wkhtmltopdf', html_path, output_path], check=True)
            
            return output_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تقرير PDF: {e}")
            # إرجاع تقرير HTML كبديل
            return self._generate_html_report(report_def, df, charts, summary, parameters, executed_by, filename_base)
    
    def _generate_csv_report(self, df, filename_base):
        """إنشاء تقرير بتنسيق CSV"""
        try:
            output_path = os.path.join(self.reports_dir, f"{filename_base}.csv")
            df.to_csv(output_path, index=False, encoding='utf-8')
            return output_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تقرير CSV: {e}")
            raise
    
    def _generate_excel_report(self, report_def, df, charts, filename_base):
        """إنشاء تقرير بتنسيق Excel"""
        try:
            output_path = os.path.join(self.reports_dir, f"{filename_base}.xlsx")
            
            # إنشاء ملف Excel
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                # كتابة البيانات
                sheet_name = self.config['export']['excel']['sheet_name']
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # تنسيق الورقة
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                
                # تنسيق العناوين
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })
                
                # تطبيق التنسيق على العناوين
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # ضبط عرض الأعمدة
                for i, col in enumerate(df.columns):
                    column_width = max(df[col].astype(str).str.len().max(), len(col)) + 2
                    worksheet.set_column(i, i, column_width)
                
                # إضافة الرسوم البيانية إذا كان مطلوبًا
                if self.config['export']['excel']['include_charts'] and charts:
                    chart_sheet = workbook.add_worksheet('الرسوم البيانية')
                    
                    for i, chart_data in enumerate(charts):
                        # تحويل الصورة من Base64 إلى ملف مؤقت
                        img_data = base64.b64decode(chart_data['image'])
                        img_path = os.path.join(self.reports_dir, f"temp_chart_{i}.png")
                        
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                        
                        # إضافة الصورة إلى ورقة العمل
                        chart_sheet.insert_image(i * 20, 0, img_path)
                        
                        # حذف الملف المؤقت
                        os.remove(img_path)
            
            return output_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تقرير Excel: {e}")
            # محاولة إنشاء تقرير CSV كبديل
            return self._generate_csv_report(df, filename_base)
    
    def _generate_json_report(self, report_def, df, charts, summary, parameters, filename_base):
        """إنشاء تقرير بتنسيق JSON"""
        try:
            output_path = os.path.join(self.reports_dir, f"{filename_base}.json")
            
            # إعداد بيانات التقرير
            report_data = {
                'report_id': report_def['id'],
                'report_name': report_def['name'],
                'report_description': report_def['description'],
                'generated_at': datetime.datetime.now().isoformat(),
                'parameters': parameters,
                'data': df.to_dict('records'),
                'charts': charts,
                'summary': summary
            }
            
            # حفظ الملف
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            return output_path
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تقرير JSON: {e}")
            raise
    
    def get_report_execution_log(self, execution_id=None, report_id=None, limit=100):
        """الحصول على سجل تنفيذ التقارير"""
        try:
            query = """
                SELECT rel.*, rd.name as report_name
                FROM report_execution_log rel
                JOIN report_definitions rd ON rel.report_id = rd.id
            """
            params = []
            conditions = []
            
            if execution_id:
                conditions.append("rel.id = ?")
                params.append(execution_id)
            
            if report_id:
                conditions.append("rel.report_id = ?")
                params.append(report_id)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY rel.execution_time DESC LIMIT ?"
            params.append(limit)
            
            logs = self.db_manager.fetch_all('operational', query, tuple(params))
            
            result = []
            for log in logs:
                log_dict = dict(log)
                if log_dict.get('parameters'):
                    try:
                        log_dict['parameters'] = json.loads(log_dict['parameters'])
                    except:
                        pass
                result.append(log_dict)
            
            return result
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على سجل تنفيذ التقارير: {e}")
            return []
    
    def get_report_output(self, execution_id):
        """الحصول على ملف إخراج التقرير"""
        try:
            log = self.db_manager.fetch_one('operational', 
                "SELECT output_path FROM report_execution_log WHERE id = ?", (execution_id,))
            
            if log and log['output_path'] and os.path.exists(log['output_path']):
                return log['output_path']
            else:
                return None
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على ملف إخراج التقرير: {e}")
            return None
    
    def create_report_template(self, name, description, html_template, css_style, created_by=None, is_default=False):
        """إنشاء قالب تقرير جديد"""
        try:
            # إذا كان القالب الجديد هو الافتراضي، إلغاء تعيين القوالب الافتراضية الأخرى
            if is_default:
                self.db_manager.update('operational', 'report_templates', 
                    {'is_default': 0}, {'is_default': 1})
            
            template_id = self.db_manager.insert('operational', 'report_templates', {
                'name': name,
                'description': description,
                'html_template': html_template,
                'css_style': css_style,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat(),
                'created_by': created_by,
                'is_default': 1 if is_default else 0
            })
            
            self.logger.info(f"تم إنشاء قالب التقرير '{name}' بنجاح (ID: {template_id})")
            return template_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء قالب التقرير: {e}")
            raise
    
    def update_report_template(self, template_id, name=None, description=None, 
                              html_template=None, css_style=None, is_default=None):
        """تحديث قالب تقرير"""
        try:
            # بناء قاموس التحديثات
            updates = {'updated_at': datetime.datetime.now().isoformat()}
            
            if name is not None:
                updates['name'] = name
            if description is not None:
                updates['description'] = description
            if html_template is not None:
                updates['html_template'] = html_template
            if css_style is not None:
                updates['css_style'] = css_style
            
            # إذا كان القالب الجديد هو الافتراضي، إلغاء تعيين القوالب الافتراضية الأخرى
            if is_default is not None:
                updates['is_default'] = 1 if is_default else 0
                if is_default:
                    self.db_manager.update('operational', 'report_templates', 
                        {'is_default': 0}, {'is_default': 1})
            
            # تحديث القالب
            self.db_manager.update('operational', 'report_templates', updates, {'id': template_id})
            
            self.logger.info(f"تم تحديث قالب التقرير (ID: {template_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تحديث قالب التقرير: {e}")
            return False
    
    def delete_report_template(self, template_id):
        """حذف قالب تقرير"""
        try:
            # التحقق من أن القالب ليس هو الافتراضي
            template = self.db_manager.fetch_one('operational', 
                "SELECT is_default FROM report_templates WHERE id = ?", (template_id,))
            
            if template and template['is_default']:
                raise ValueError("لا يمكن حذف القالب الافتراضي")
            
            # حذف القالب
            self.db_manager.delete('operational', 'report_templates', {'id': template_id})
            
            self.logger.info(f"تم حذف قالب التقرير (ID: {template_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف قالب التقرير: {e}")
            return False
    
    def list_report_templates(self):
        """قائمة قوالب التقارير"""
        try:
            templates = self.db_manager.fetch_all('operational', 
                "SELECT id, name, description, created_at, updated_at, created_by, is_default FROM report_templates ORDER BY is_default DESC, name")
            
            return [dict(template) for template in templates]
        except Exception as e:
            self.logger.error(f"خطأ في قائمة قوالب التقارير: {e}")
            return []
    
    def get_report_template(self, template_id):
        """الحصول على قالب تقرير"""
        try:
            template = self.db_manager.fetch_one('operational', 
                "SELECT * FROM report_templates WHERE id = ?", (template_id,))
            
            return dict(template) if template else None
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قالب التقرير: {e}")
            return None
    
    def set_user_report_preferences(self, user_id, report_id, preferred_format=None, 
                                   chart_preferences=None, filter_preferences=None):
        """تعيين تفضيلات المستخدم للتقرير"""
        try:
            # التحقق من وجود تفضيلات سابقة
            existing = self.db_manager.fetch_one('operational', 
                "SELECT id FROM user_report_preferences WHERE user_id = ? AND report_id = ?", 
                (user_id, report_id))
            
            if existing:
                # تحديث التفضيلات الموجودة
                updates = {'updated_at': datetime.datetime.now().isoformat()}
                
                if preferred_format is not None:
                    updates['preferred_format'] = preferred_format
                if chart_preferences is not None:
                    updates['chart_preferences'] = json.dumps(chart_preferences)
                if filter_preferences is not None:
                    updates['filter_preferences'] = json.dumps(filter_preferences)
                
                self.db_manager.update('operational', 'user_report_preferences', updates, {'id': existing['id']})
                
                self.logger.info(f"تم تحديث تفضيلات المستخدم للتقرير (User: {user_id}, Report: {report_id})")
                return existing['id']
            else:
                # إنشاء تفضيلات جديدة
                pref_id = self.db_manager.insert('operational', 'user_report_preferences', {
                    'user_id': user_id,
                    'report_id': report_id,
                    'preferred_format': preferred_format,
                    'chart_preferences': json.dumps(chart_preferences) if chart_preferences else None,
                    'filter_preferences': json.dumps(filter_preferences) if filter_preferences else None,
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat()
                })
                
                self.logger.info(f"تم إنشاء تفضيلات المستخدم للتقرير (User: {user_id}, Report: {report_id})")
                return pref_id
        except Exception as e:
            self.logger.error(f"خطأ في تعيين تفضيلات المستخدم للتقرير: {e}")
            raise
    
    def get_user_report_preferences(self, user_id, report_id=None):
        """الحصول على تفضيلات المستخدم للتقرير"""
        try:
            query = "SELECT * FROM user_report_preferences WHERE user_id = ?"
            params = [user_id]
            
            if report_id:
                query += " AND report_id = ?"
                params.append(report_id)
            
            prefs = self.db_manager.fetch_all('operational', query, tuple(params))
            
            result = []
            for pref in prefs:
                pref_dict = dict(pref)
                if pref_dict.get('chart_preferences'):
                    try:
                        pref_dict['chart_preferences'] = json.loads(pref_dict['chart_preferences'])
                    except:
                        pass
                if pref_dict.get('filter_preferences'):
                    try:
                        pref_dict['filter_preferences'] = json.loads(pref_dict['filter_preferences'])
                    except:
                        pass
                result.append(pref_dict)
            
            return result[0] if report_id and result else result
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على تفضيلات المستخدم للتقرير: {e}")
            return [] if not report_id else None
    
    def run_scheduled_reports(self):
        """تنفيذ التقارير المجدولة المستحقة"""
        try:
            now = datetime.datetime.now()
            
            # الحصول على التقارير المجدولة المستحقة
            scheduled = self.db_manager.fetch_all('operational', """
                SELECT sr.*, rd.name as report_name
                FROM scheduled_reports sr
                JOIN report_definitions rd ON sr.report_id = rd.id
                WHERE sr.is_active = 1 AND sr.next_run <= ?
            """, (now.isoformat(),))
            
            results = []
            
            for schedule in scheduled:
                try:
                    # تنفيذ التقرير
                    report_result = self.run_report(
                        schedule['report_id'],
                        None,  # يمكن استخدام معلمات مخزنة
                        schedule['format'],
                        'scheduler'
                    )
                    
                    # تحديث موعد التشغيل التالي
                    next_run = self._calculate_next_run(schedule['schedule_type'], schedule['schedule_value'])
                    
                    self.db_manager.update('operational', 'scheduled_reports', {
                        'last_run': now.isoformat(),
                        'next_run': next_run.isoformat() if next_run else None
                    }, {'id': schedule['id']})
                    
                    # إرسال التقرير إلى المستلمين
                    if schedule['recipients'] and report_result.get('success') and report_result.get('output_path'):
                        recipients = json.loads(schedule['recipients']) if isinstance(schedule['recipients'], str) else schedule['recipients']
                        self._send_report_to_recipients(recipients, report_result['output_path'], schedule['report_name'])
                    
                    results.append({
                        'schedule_id': schedule['id'],
                        'report_id': schedule['report_id'],
                        'report_name': schedule['report_name'],
                        'success': report_result.get('success', False),
                        'message': report_result.get('message', ''),
                        'next_run': next_run.isoformat() if next_run else None
                    })
                except Exception as e:
                    self.logger.error(f"خطأ في تنفيذ التقرير المجدول (ID: {schedule['id']}): {e}")
                    results.append({
                        'schedule_id': schedule['id'],
                        'report_id': schedule['report_id'],
                        'report_name': schedule.get('report_name', ''),
                        'success': False,
                        'message': f"خطأ: {str(e)}",
                        'next_run': None
                    })
            
            return results
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ التقارير المجدولة: {e}")
            return []
    
    def _send_report_to_recipients(self, recipients, report_path, report_name):
        """إرسال التقرير إلى المستلمين"""
        try:
            # هذه وظيفة تمثيلية، يمكن تنفيذها باستخدام SMTP أو API أخرى
            self.logger.info(f"إرسال التقرير '{report_name}' إلى {len(recipients)} مستلم")
            
            # يمكن تنفيذ الإرسال الفعلي هنا
            # مثال: إرسال بريد إلكتروني باستخدام SMTP
            # import smtplib
            # from email.mime.multipart import MIMEMultipart
            # from email.mime.base import MIMEBase
            # from email.mime.text import MIMEText
            # from email.utils import formatdate
            # from email import encoders
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في إرسال التقرير إلى المستلمين: {e}")
            return False
    
    def analyze_data_trends(self, query, date_column, value_column, start_date=None, end_date=None, 
                           group_by=None, db_name='operational'):
        """تحليل اتجاهات البيانات"""
        try:
            if not self.config['analytics']['enable_trend_analysis']:
                return {
                    'success': False,
                    'message': 'تحليل الاتجاهات غير مفعل في التكوين'
                }
            
            # تنفيذ الاستعلام
            params = {}
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
            
            data = self.db_manager.fetch_all(db_name, query, params)
            
            if not data:
                return {
                    'success': False,
                    'message': 'لا توجد بيانات للتحليل'
                }
            
            # تحويل البيانات إلى DataFrame
            df = pd.DataFrame([dict(row) for row in data])
            
            # التأكد من وجود الأعمدة المطلوبة
            if date_column not in df.columns or value_column not in df.columns:
                return {
                    'success': False,
                    'message': f'الأعمدة المطلوبة غير موجودة: {date_column}, {value_column}'
                }
            
            # تحويل عمود التاريخ
            df[date_column] = pd.to_datetime(df[date_column])
            df = df.sort_values(by=date_column)
            
            # تجميع البيانات إذا كان مطلوبًا
            if group_by:
                if group_by not in df.columns:
                    return {
                        'success': False,
                        'message': f'عمود التجميع غير موجود: {group_by}'
                    }
                
                groups = df[group_by].unique()
                trends = {}
                
                for group in groups:
                    group_df = df[df[group_by] == group]
                    trends[group] = self._calculate_trend(group_df, date_column, value_column)
                
                return {
                    'success': True,
                    'message': 'تم تحليل الاتجاهات بنجاح',
                    'trends': trends
                }
            else:
                trend = self._calculate_trend(df, date_column, value_column)
                
                return {
                    'success': True,
                    'message': 'تم تحليل الاتجاهات بنجاح',
                    'trend': trend
                }
        except Exception as e:
            self.logger.error(f"خطأ في تحليل اتجاهات البيانات: {e}")
            return {
                'success': False,
                'message': f'خطأ في تحليل الاتجاهات: {str(e)}'
            }
    
    def _calculate_trend(self, df, date_column, value_column):
        """حساب اتجاه البيانات"""
        try:
            # التأكد من وجود بيانات كافية
            min_data_points = self.config['analytics']['min_data_points']
            if len(df) < min_data_points:
                return {
                    'status': 'insufficient_data',
                    'message': f'عدد نقاط البيانات غير كافٍ ({len(df)} < {min_data_points})'
                }
            
            # حساب الإحصائيات الأساسية
            stats = {
                'count': len(df),
                'min': df[value_column].min(),
                'max': df[value_column].max(),
                'mean': df[value_column].mean(),
                'median': df[value_column].median(),
                'std': df[value_column].std(),
                'first_date': df[date_column].min().isoformat(),
                'last_date': df[date_column].max().isoformat()
            }
            
            # حساب التغيير
            first_value = df[value_column].iloc[0]
            last_value = df[value_column].iloc[-1]
            change = last_value - first_value
            change_percent = (change / first_value) * 100 if first_value != 0 else float('inf')
            
            # تحديد الاتجاه
            if change_percent > 5:
                trend_direction = 'up'
            elif change_percent < -5:
                trend_direction = 'down'
            else:
                trend_direction = 'stable'
            
            # حساب معدل النمو
            days = (df[date_column].max() - df[date_column].min()).days
            if days > 0:
                daily_growth_rate = (((last_value / first_value) ** (1 / days)) - 1) * 100 if first_value != 0 else float('inf')
            else:
                daily_growth_rate = 0
            
            # التنبؤ بالقيم المستقبلية إذا كان مفعلاً
            predictions = None
            if self.config['analytics']['enable_predictive_analytics'] and len(df) >= 2 * min_data_points:
                predictions = self._predict_future_values(df, date_column, value_column)
            
            return {
                'status': 'success',
                'stats': stats,
                'change': change,
                'change_percent': change_percent,
                'trend_direction': trend_direction,
                'daily_growth_rate': daily_growth_rate,
                'predictions': predictions
            }
        except Exception as e:
            self.logger.error(f"خطأ في حساب اتجاه البيانات: {e}")
            return {
                'status': 'error',
                'message': f'خطأ في حساب الاتجاه: {str(e)}'
            }
    
    def _predict_future_values(self, df, date_column, value_column):
        """التنبؤ بالقيم المستقبلية"""
        try:
            # إنشاء مؤشر زمني
            df = df.set_index(date_column)
            
            # تحديد عدد الأيام للتنبؤ
            prediction_days = self.config['analytics']['prediction_horizon_days']
            
            # استخدام نموذج بسيط للتنبؤ (يمكن استبداله بنماذج أكثر تعقيدًا)
            from sklearn.linear_model import LinearRegression
            import numpy as np
            
            # إعداد البيانات
            X = np.array(range(len(df))).reshape(-1, 1)
            y = df[value_column].values
            
            # تدريب النموذج
            model = LinearRegression()
            model.fit(X, y)
            
            # التنبؤ بالقيم المستقبلية
            future_X = np.array(range(len(df), len(df) + prediction_days)).reshape(-1, 1)
            future_y = model.predict(future_X)
            
            # إنشاء تواريخ مستقبلية
            last_date = df.index[-1]
            future_dates = [last_date + datetime.timedelta(days=i+1) for i in range(prediction_days)]
            
            # إنشاء قاموس النتائج
            predictions = {
                'dates': [d.isoformat() for d in future_dates],
                'values': future_y.tolist(),
                'model': 'linear_regression',
                'confidence': self.config['analytics']['confidence_interval']
            }
            
            return predictions
        except Exception as e:
            self.logger.error(f"خطأ في التنبؤ بالقيم المستقبلية: {e}")
            return None
    
    def create_dashboard(self, name, description, reports, layout=None, created_by=None):
        """إنشاء لوحة معلومات"""
        try:
            # التحقق من وجود التقارير
            for report_id in reports:
                report = self.get_report_definition(report_id)
                if not report:
                    raise ValueError(f"التقرير غير موجود (ID: {report_id})")
            
            # إنشاء جدول لوحات المعلومات إذا لم يكن موجودًا
            self.db_manager.execute('operational', '''
                CREATE TABLE IF NOT EXISTS dashboards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    reports TEXT NOT NULL,
                    layout TEXT,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    created_by TEXT,
                    is_public INTEGER DEFAULT 0
                )
            ''')
            
            # إدخال لوحة المعلومات
            dashboard_id = self.db_manager.insert('operational', 'dashboards', {
                'name': name,
                'description': description,
                'reports': json.dumps(reports),
                'layout': json.dumps(layout) if layout else None,
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat(),
                'created_by': created_by,
                'is_public': 0
            })
            
            self.logger.info(f"تم إنشاء لوحة المعلومات '{name}' بنجاح (ID: {dashboard_id})")
            return dashboard_id
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء لوحة المعلومات: {e}")
            raise
    
    def update_dashboard(self, dashboard_id, name=None, description=None, reports=None, layout=None, is_public=None):
        """تحديث لوحة معلومات"""
        try:
            # بناء قاموس التحديثات
            updates = {'updated_at': datetime.datetime.now().isoformat()}
            
            if name is not None:
                updates['name'] = name
            if description is not None:
                updates['description'] = description
            if reports is not None:
                # التحقق من وجود التقارير
                for report_id in reports:
                    report = self.get_report_definition(report_id)
                    if not report:
                        raise ValueError(f"التقرير غير موجود (ID: {report_id})")
                updates['reports'] = json.dumps(reports)
            if layout is not None:
                updates['layout'] = json.dumps(layout)
            if is_public is not None:
                updates['is_public'] = 1 if is_public else 0
            
            # تحديث لوحة المعلومات
            self.db_manager.update('operational', 'dashboards', updates, {'id': dashboard_id})
            
            self.logger.info(f"تم تحديث لوحة المعلومات (ID: {dashboard_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في تحديث لوحة المعلومات: {e}")
            return False
    
    def delete_dashboard(self, dashboard_id):
        """حذف لوحة معلومات"""
        try:
            self.db_manager.delete('operational', 'dashboards', {'id': dashboard_id})
            
            self.logger.info(f"تم حذف لوحة المعلومات (ID: {dashboard_id}) بنجاح")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في حذف لوحة المعلومات: {e}")
            return False
    
    def get_dashboard(self, dashboard_id):
        """الحصول على لوحة معلومات"""
        try:
            dashboard = self.db_manager.fetch_one('operational', 
                "SELECT * FROM dashboards WHERE id = ?", (dashboard_id,))
            
            if dashboard:
                dashboard_dict = dict(dashboard)
                if dashboard_dict.get('reports'):
                    dashboard_dict['reports'] = json.loads(dashboard_dict['reports'])
                if dashboard_dict.get('layout'):
                    dashboard_dict['layout'] = json.loads(dashboard_dict['layout'])
                
                return dashboard_dict
            else:
                return None
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على لوحة المعلومات: {e}")
            return None
    
    def list_dashboards(self, created_by=None, is_public=None):
        """قائمة لوحات المعلومات"""
        try:
            query = "SELECT id, name, description, created_at, updated_at, created_by, is_public FROM dashboards"
            params = []
            conditions = []
            
            if created_by:
                conditions.append("created_by = ?")
                params.append(created_by)
            
            if is_public is not None:
                conditions.append("is_public = ?")
                params.append(1 if is_public else 0)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY name"
            
            dashboards = self.db_manager.fetch_all('operational', query, tuple(params))
            return [dict(dashboard) for dashboard in dashboards]
        except Exception as e:
            self.logger.error(f"خطأ في قائمة لوحات المعلومات: {e}")
            return []
    
    def render_dashboard(self, dashboard_id, parameters=None):
        """عرض لوحة معلومات"""
        try:
            # الحصول على لوحة المعلومات
            dashboard = self.get_dashboard(dashboard_id)
            if not dashboard:
                raise ValueError(f"لوحة المعلومات غير موجودة (ID: {dashboard_id})")
            
            # تنفيذ التقارير
            reports_data = []
            for report_id in dashboard['reports']:
                report_result = self.run_report(report_id, parameters)
                if report_result.get('success'):
                    reports_data.append({
                        'report_id': report_id,
                        'report_name': self.get_report_definition(report_id)['name'],
                        'data': report_result.get('data', []),
                        'charts': report_result.get('charts', []),
                        'summary': report_result.get('summary', '')
                    })
            
            # إنشاء HTML للوحة المعلومات
            dashboard_html = self._generate_dashboard_html(dashboard, reports_data)
            
            # حفظ الملف
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.reports_dir, f"dashboard_{dashboard_id}_{timestamp}.html")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(dashboard_html)
            
            return {
                'success': True,
                'message': 'تم عرض لوحة المعلومات بنجاح',
                'dashboard_name': dashboard['name'],
                'reports_count': len(reports_data),
                'output_path': output_path
            }
        except Exception as e:
            self.logger.error(f"خطأ في عرض لوحة المعلومات: {e}")
            return {
                'success': False,
                'message': f'خطأ في عرض لوحة المعلومات: {str(e)}'
            }
    
    def _generate_dashboard_html(self, dashboard, reports_data):
        """إنشاء HTML للوحة المعلومات"""
        try:
            # قالب HTML للوحة المعلومات
            dashboard_template = """
            <!DOCTYPE html>
            <html dir="rtl" lang="ar">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ dashboard_name }}</title>
                <style>
                    body {
                        font-family: Arial, Tahoma, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f5f5f5;
                        color: #333;
                    }
                    
                    .dashboard-container {
                        max-width: 1200px;
                        margin: 20px auto;
                        padding: 20px;
                    }
                    
                    .dashboard-header {
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }
                    
                    .dashboard-header h1 {
                        margin: 0;
                    }
                    
                    .dashboard-description {
                        margin-top: 10px;
                        font-style: italic;
                    }
                    
                    .dashboard-meta {
                        font-size: 0.9em;
                        margin-top: 10px;
                    }
                    
                    .dashboard-content {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                        gap: 20px;
                    }
                    
                    .report-card {
                        background-color: white;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        padding: 20px;
                        margin-bottom: 20px;
                    }
                    
                    .report-header {
                        border-bottom: 2px solid #4CAF50;
                        padding-bottom: 10px;
                        margin-bottom: 15px;
                    }
                    
                    .report-header h2 {
                        margin: 0;
                        color: #2E7D32;
                    }
                    
                    .chart-container {
                        margin-bottom: 20px;
                    }
                    
                    .chart-container img {
                        max-width: 100%;
                        height: auto;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                    
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }
                    
                    table th, table td {
                        padding: 12px 15px;
                        text-align: right;
                        border-bottom: 1px solid #ddd;
                    }
                    
                    table th {
                        background-color: #4CAF50;
                        color: white;
                        font-weight: bold;
                    }
                    
                    table tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    
                    .report-summary {
                        background-color: #e8f5e9;
                        padding: 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                    }
                    
                    .dashboard-footer {
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        text-align: center;
                        font-size: 0.9em;
                        color: #777;
                    }
                    
                    @media (max-width: 768px) {
                        .dashboard-content {
                            grid-template-columns: 1fr;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="dashboard-container">
                    <div class="dashboard-header">
                        <h1>{{ dashboard_name }}</h1>
                        <div class="dashboard-description">{{ dashboard_description }}</div>
                        <div class="dashboard-meta">
                            <p>تاريخ التحديث: {{ dashboard_date }}</p>
                        </div>
                    </div>
                    
                    <div class="dashboard-content">
                        {% for report in reports %}
                        <div class="report-card">
                            <div class="report-header">
                                <h2>{{ report.report_name }}</h2>
                            </div>
                            
                            {% if report.charts %}
                            <div class="chart-container">
                                {% for chart in report.charts %}
                                <h3>{{ chart.title }}</h3>
                                <img src="data:image/png;base64,{{ chart.image }}" alt="{{ chart.title }}">
                                {% endfor %}
                            </div>
                            {% endif %}
                            
                            {% if report.data %}
                            <div class="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            {% for header in report.headers %}
                                            <th>{{ header }}</th>
                                            {% endfor %}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for row in report.rows %}
                                        <tr>
                                            {% for cell in row %}
                                            <td>{{ cell }}</td>
                                            {% endfor %}
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            {% endif %}
                            
                            {% if report.summary %}
                            <div class="report-summary">
                                <h3>ملخص</h3>
                                <div class="summary-content">
                                    {{ report.summary|safe }}
                                </div>
                            </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                    
                    <div class="dashboard-footer">
                        <p>نظام الذكاء الاصطناعي الزراعي المتكامل</p>
                        <p>تم إنشاء لوحة المعلومات في {{ dashboard_datetime }}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # تحضير بيانات التقارير
            reports = []
            for report in reports_data:
                if report.get('data'):
                    df = pd.DataFrame(report['data'])
                    headers = df.columns.tolist()
                    rows = df.values.tolist()
                else:
                    headers = []
                    rows = []
                
                reports.append({
                    'report_name': report['report_name'],
                    'charts': report.get('charts', []),
                    'headers': headers,
                    'rows': rows,
                    'summary': report.get('summary', '')
                })
            
            # تطبيق القالب
            template = Template(dashboard_template)
            html_content = template.render(
                dashboard_name=dashboard['name'],
                dashboard_description=dashboard['description'],
                dashboard_date=datetime.datetime.now().strftime(self.config['reporting']['date_format']),
                dashboard_datetime=datetime.datetime.now().strftime(
                    f"{self.config['reporting']['date_format']} {self.config['reporting']['time_format']}"),
                reports=reports
            )
            
            return html_content
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء HTML للوحة المعلومات: {e}")
            raise


# مثال على الاستخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # استيراد مدير قواعد البيانات
    from database_manager import DatabaseManager
    
    # إنشاء مدير قواعد البيانات
    db_manager = DatabaseManager()
    
    # إنشاء نظام التقارير
    reporting = DatabaseReporting(db_manager)
    
    # إنشاء تقرير جديد
    report_id = reporting.create_report_definition(
        name="تقرير أداء النظام",
        description="تقرير عن أداء النظام خلال الفترة المحددة",
        query="""
            SELECT 
                metric_type, 
                AVG(metric_value) as avg_value, 
                MAX(metric_value) as max_value, 
                MIN(metric_value) as min_value
            FROM performance_metrics
            WHERE db_name = 'system' 
            AND timestamp BETWEEN :start_date AND :end_date
            GROUP BY metric_type
        """,
        parameters={
            'start_date': {'type': 'date', 'default': 'today-7d'},
            'end_date': {'type': 'date', 'default': 'today'}
        },
        chart_type="bar",
        chart_options={
            'x_axis': 'metric_type',
            'y_axis': 'avg_value',
            'title': 'متوسط مقاييس النظام'
        },
        category="system",
        is_template=False,
        is_public=True,
        created_by="admin"
    )
    
    print(f"تم إنشاء التقرير بنجاح (ID: {report_id})")
    
    # تنفيذ التقرير
    result = reporting.run_report(
        report_id=report_id,
        parameters={
            'start_date': (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat(),
            'end_date': datetime.datetime.now().isoformat()
        },
        output_format="html",
        executed_by="admin"
    )
    
    print(f"تنفيذ التقرير: {result['success']}, {result.get('message')}")
    if result.get('output_path'):
        print(f"مسار الإخراج: {result['output_path']}")
