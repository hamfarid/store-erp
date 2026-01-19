#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التقارير المالية والتحليلات

هذا الملف يتضمن وظائف إنشاء وإدارة التقارير المالية والتحليلات للمزارع والمحاصيل،
مع دعم تحليل التكاليف والإيرادات والربحية وتصور البيانات.
"""

import os
import json
import datetime
import logging
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from ..cost_management.cost_calculator import CostCalculator
from ..farm_management.farm_manager import FarmManager
from ..inventory_management.inventory_manager import InventoryManager
from ..audit.audit_manager import AuditManager
from ..utils.config_loader import ConfigLoader

# إعداد السجل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialReportingSystem:
    """نظام التقارير المالية والتحليلات"""
    
    def __init__(self, db_uri: str, config_path: str = None):
        """
        تهيئة نظام التقارير المالية
        
        المعلمات:
            db_uri (str): رابط قاعدة البيانات
            config_path (str): مسار ملف التكوين
        """
        self.db_uri = db_uri
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)
        
        # تحميل التكوين
        self.config = ConfigLoader(config_path).load_config() if config_path else {}
        
        # مدراء النظم المرتبطة
        self.cost_calculator = CostCalculator(db_uri)
        self.farm_manager = FarmManager(db_uri)
        self.inventory_manager = InventoryManager(db_uri)
        self.audit_manager = AuditManager(db_uri)
        
        # إعداد مجلد التقارير
        self.reports_dir = self.config.get('reports_dir', '/home/ubuntu/agricultural_ai_system/reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # إعداد مجلدات التقارير الفرعية
        self.financial_reports_dir = os.path.join(self.reports_dir, 'financial')
        self.farm_reports_dir = os.path.join(self.reports_dir, 'farms')
        self.crop_reports_dir = os.path.join(self.reports_dir, 'crops')
        self.inventory_reports_dir = os.path.join(self.reports_dir, 'inventory')
        
        os.makedirs(self.financial_reports_dir, exist_ok=True)
        os.makedirs(self.farm_reports_dir, exist_ok=True)
        os.makedirs(self.crop_reports_dir, exist_ok=True)
        os.makedirs(self.inventory_reports_dir, exist_ok=True)
    
    def generate_farm_financial_report(self, farm_id: int, 
                                       start_date: Optional[datetime.datetime] = None,
                                       end_date: Optional[datetime.datetime] = None,
                                       format: str = 'pdf') -> str:
        """
        إنشاء تقرير مالي للمزرعة
        
        المعلمات:
            farm_id (int): معرف المزرعة
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            format (str): تنسيق التقرير (pdf، excel، csv، json)
            
        العائد:
            str: مسار ملف التقرير
        """
        try:
            # الحصول على معلومات المزرعة
            farm_info = self.farm_manager.get_farm(farm_id)
            
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # الحصول على تكاليف المزرعة
            farm_costs = self.cost_calculator.get_farm_costs(farm_id, start_date, end_date)
            
            # الحصول على إيرادات المزرعة
            farm_revenues = self.cost_calculator.get_farm_revenues(farm_id, start_date, end_date)
            
            # الحصول على استخدام المخزون
            inventory_usage = self.inventory_manager.get_farm_usage_history(farm_id, start_date, end_date)
            
            # حساب إجمالي التكاليف والإيرادات
            total_costs = sum(cost['amount'] for cost in farm_costs)
            total_revenues = sum(revenue['amount'] for revenue in farm_revenues)
            net_profit = total_revenues - total_costs
            profit_margin = (net_profit / total_revenues * 100) if total_revenues > 0 else 0
            
            # تجميع التكاليف حسب النوع
            cost_by_type = {}
            for cost in farm_costs:
                cost_type = cost['cost_type']
                if cost_type not in cost_by_type:
                    cost_by_type[cost_type] = 0
                cost_by_type[cost_type] += cost['amount']
            
            # تجميع التكاليف حسب المحصول
            cost_by_crop = {}
            for cost in farm_costs:
                if cost['crop_id']:
                    crop_id = cost['crop_id']
                    if crop_id not in cost_by_crop:
                        crop_info = self.farm_manager.get_crop(crop_id)
                        crop_name = crop_info.get('name', f'محصول {crop_id}')
                        cost_by_crop[crop_name] = 0
                    cost_by_crop[crop_name] += cost['amount']
            
            # تجميع الإيرادات حسب المحصول
            revenue_by_crop = {}
            for revenue in farm_revenues:
                if revenue['crop_id']:
                    crop_id = revenue['crop_id']
                    if crop_id not in revenue_by_crop:
                        crop_info = self.farm_manager.get_crop(crop_id)
                        crop_name = crop_info.get('name', f'محصول {crop_id}')
                        revenue_by_crop[crop_name] = 0
                    revenue_by_crop[crop_name] += revenue['amount']
            
            # حساب الربحية حسب المحصول
            profit_by_crop = {}
            for crop_name in set(list(cost_by_crop.keys()) + list(revenue_by_crop.keys())):
                crop_cost = cost_by_crop.get(crop_name, 0)
                crop_revenue = revenue_by_crop.get(crop_name, 0)
                profit_by_crop[crop_name] = crop_revenue - crop_cost
            
            # إنشاء DataFrame للتقرير
            report_data = {
                'معلومات المزرعة': {
                    'اسم المزرعة': farm_info.get('name', f'مزرعة {farm_id}'),
                    'الموقع': farm_info.get('location', 'غير محدد'),
                    'المساحة': f"{farm_info.get('area', 0)} {farm_info.get('area_unit', 'فدان')}",
                    'تاريخ التقرير': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'الفترة': f"{start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}"
                },
                'ملخص مالي': {
                    'إجمالي التكاليف': total_costs,
                    'إجمالي الإيرادات': total_revenues,
                    'صافي الربح': net_profit,
                    'هامش الربح': f"{profit_margin:.2f}%"
                },
                'التكاليف حسب النوع': cost_by_type,
                'التكاليف حسب المحصول': cost_by_crop,
                'الإيرادات حسب المحصول': revenue_by_crop,
                'الربحية حسب المحصول': profit_by_crop,
                'تفاصيل التكاليف': farm_costs,
                'تفاصيل الإيرادات': farm_revenues,
                'استخدام المخزون': inventory_usage.get('usage_records', [])
            }
            
            # إنشاء اسم الملف
            farm_name = farm_info.get('name', f'farm_{farm_id}').replace(' ', '_')
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{farm_name}_financial_report_{timestamp}"
            
            # إنشاء مسار الملف
            file_path = os.path.join(self.farm_reports_dir, filename)
            
            # إنشاء التقرير بالتنسيق المطلوب
            if format.lower() == 'pdf':
                self._generate_pdf_report(report_data, f"{file_path}.pdf", f"التقرير المالي لمزرعة {farm_info.get('name', f'مزرعة {farm_id}')}")
                return f"{file_path}.pdf"
            elif format.lower() == 'excel':
                self._export_to_excel(report_data, f"{file_path}.xlsx")
                return f"{file_path}.xlsx"
            elif format.lower() == 'csv':
                self._export_to_csv(report_data, f"{file_path}.csv")
                return f"{file_path}.csv"
            elif format.lower() == 'json':
                with open(f"{file_path}.json", 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4, default=str)
                return f"{file_path}.json"
            else:
                raise ValueError(f"تنسيق غير مدعوم: {format}")
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء التقرير المالي للمزرعة: {str(e)}")
            raise
    
    def generate_crop_financial_report(self, crop_id: int,
                                       start_date: Optional[datetime.datetime] = None,
                                       end_date: Optional[datetime.datetime] = None,
                                       format: str = 'pdf') -> str:
        """
        إنشاء تقرير مالي للمحصول
        
        المعلمات:
            crop_id (int): معرف المحصول
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            format (str): تنسيق التقرير (pdf، excel، csv، json)
            
        العائد:
            str: مسار ملف التقرير
        """
        try:
            # الحصول على معلومات المحصول
            crop_info = self.farm_manager.get_crop(crop_id)
            
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # الحصول على تكاليف المحصول
            crop_costs = self.cost_calculator.get_crop_costs(crop_id, start_date, end_date)
            
            # الحصول على إيرادات المحصول
            crop_revenues = self.cost_calculator.get_crop_revenues(crop_id, start_date, end_date)
            
            # الحصول على استخدام المخزون
            inventory_usage = self.inventory_manager.get_crop_usage_history(crop_id, start_date, end_date)
            
            # حساب إجمالي التكاليف والإيرادات
            total_costs = sum(cost['amount'] for cost in crop_costs)
            total_revenues = sum(revenue['amount'] for revenue in crop_revenues)
            net_profit = total_revenues - total_costs
            profit_margin = (net_profit / total_revenues * 100) if total_revenues > 0 else 0
            
            # تجميع التكاليف حسب النوع
            cost_by_type = {}
            for cost in crop_costs:
                cost_type = cost['cost_type']
                if cost_type not in cost_by_type:
                    cost_by_type[cost_type] = 0
                cost_by_type[cost_type] += cost['amount']
            
            # تجميع التكاليف حسب المزرعة
            cost_by_farm = {}
            for cost in crop_costs:
                if cost['farm_id']:
                    farm_id = cost['farm_id']
                    if farm_id not in cost_by_farm:
                        farm_info = self.farm_manager.get_farm(farm_id)
                        farm_name = farm_info.get('name', f'مزرعة {farm_id}')
                        cost_by_farm[farm_name] = 0
                    cost_by_farm[farm_name] += cost['amount']
            
            # تجميع الإيرادات حسب المزرعة
            revenue_by_farm = {}
            for revenue in crop_revenues:
                if revenue['farm_id']:
                    farm_id = revenue['farm_id']
                    if farm_id not in revenue_by_farm:
                        farm_info = self.farm_manager.get_farm(farm_id)
                        farm_name = farm_info.get('name', f'مزرعة {farm_id}')
                        revenue_by_farm[farm_name] = 0
                    revenue_by_farm[farm_name] += revenue['amount']
            
            # حساب الربحية حسب المزرعة
            profit_by_farm = {}
            for farm_name in set(list(cost_by_farm.keys()) + list(revenue_by_farm.keys())):
                farm_cost = cost_by_farm.get(farm_name, 0)
                farm_revenue = revenue_by_farm.get(farm_name, 0)
                profit_by_farm[farm_name] = farm_revenue - farm_cost
            
            # إنشاء DataFrame للتقرير
            report_data = {
                'معلومات المحصول': {
                    'اسم المحصول': crop_info.get('name', f'محصول {crop_id}'),
                    'النوع': crop_info.get('type', 'غير محدد'),
                    'الصنف': crop_info.get('variety', 'غير محدد'),
                    'تاريخ التقرير': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'الفترة': f"{start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}"
                },
                'ملخص مالي': {
                    'إجمالي التكاليف': total_costs,
                    'إجمالي الإيرادات': total_revenues,
                    'صافي الربح': net_profit,
                    'هامش الربح': f"{profit_margin:.2f}%"
                },
                'التكاليف حسب النوع': cost_by_type,
                'التكاليف حسب المزرعة': cost_by_farm,
                'الإيرادات حسب المزرعة': revenue_by_farm,
                'الربحية حسب المزرعة': profit_by_farm,
                'تفاصيل التكاليف': crop_costs,
                'تفاصيل الإيرادات': crop_revenues,
                'استخدام المخزون': inventory_usage.get('usage_records', [])
            }
            
            # إنشاء اسم الملف
            crop_name = crop_info.get('name', f'crop_{crop_id}').replace(' ', '_')
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{crop_name}_financial_report_{timestamp}"
            
            # إنشاء مسار الملف
            file_path = os.path.join(self.crop_reports_dir, filename)
            
            # إنشاء التقرير بالتنسيق المطلوب
            if format.lower() == 'pdf':
                self._generate_pdf_report(report_data, f"{file_path}.pdf", f"التقرير المالي لمحصول {crop_info.get('name', f'محصول {crop_id}')}")
                return f"{file_path}.pdf"
            elif format.lower() == 'excel':
                self._export_to_excel(report_data, f"{file_path}.xlsx")
                return f"{file_path}.xlsx"
            elif format.lower() == 'csv':
                self._export_to_csv(report_data, f"{file_path}.csv")
                return f"{file_path}.csv"
            elif format.lower() == 'json':
                with open(f"{file_path}.json", 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4, default=str)
                return f"{file_path}.json"
            else:
                raise ValueError(f"تنسيق غير مدعوم: {format}")
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء التقرير المالي للمحصول: {str(e)}")
            raise
    
    def generate_overall_financial_report(self, 
                                         start_date: Optional[datetime.datetime] = None,
                                         end_date: Optional[datetime.datetime] = None,
                                         format: str = 'pdf') -> str:
        """
        إنشاء تقرير مالي شامل لجميع المزارع والمحاصيل
        
        المعلمات:
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            format (str): تنسيق التقرير (pdf، excel، csv، json)
            
        العائد:
            str: مسار ملف التقرير
        """
        try:
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # الحصول على قائمة المزارع
            farms = self.farm_manager.get_all_farms()
            
            # تجميع البيانات المالية لكل مزرعة
            farm_financials = []
            total_costs = 0
            total_revenues = 0
            total_profit = 0
            
            for farm in farms:
                farm_id = farm['id']
                farm_costs = self.cost_calculator.get_farm_costs(farm_id, start_date, end_date)
                farm_revenues = self.cost_calculator.get_farm_revenues(farm_id, start_date, end_date)
                
                farm_total_costs = sum(cost['amount'] for cost in farm_costs)
                farm_total_revenues = sum(revenue['amount'] for revenue in farm_revenues)
                farm_profit = farm_total_revenues - farm_total_costs
                farm_profit_margin = (farm_profit / farm_total_revenues * 100) if farm_total_revenues > 0 else 0
                
                farm_financials.append({
                    'farm_id': farm_id,
                    'farm_name': farm['name'],
                    'total_costs': farm_total_costs,
                    'total_revenues': farm_total_revenues,
                    'profit': farm_profit,
                    'profit_margin': farm_profit_margin
                })
                
                total_costs += farm_total_costs
                total_revenues += farm_total_revenues
                total_profit += farm_profit
            
            # حساب هامش الربح الإجمالي
            overall_profit_margin = (total_profit / total_revenues * 100) if total_revenues > 0 else 0
            
            # الحصول على قائمة المحاصيل
            crops = self.farm_manager.get_all_crops()
            
            # تجميع البيانات المالية لكل محصول
            crop_financials = []
            
            for crop in crops:
                crop_id = crop['id']
                crop_costs = self.cost_calculator.get_crop_costs(crop_id, start_date, end_date)
                crop_revenues = self.cost_calculator.get_crop_revenues(crop_id, start_date, end_date)
                
                crop_total_costs = sum(cost['amount'] for cost in crop_costs)
                crop_total_revenues = sum(revenue['amount'] for revenue in crop_revenues)
                crop_profit = crop_total_revenues - crop_total_costs
                crop_profit_margin = (crop_profit / crop_total_revenues * 100) if crop_total_revenues > 0 else 0
                
                crop_financials.append({
                    'crop_id': crop_id,
                    'crop_name': crop['name'],
                    'crop_type': crop.get('type', 'غير محدد'),
                    'total_costs': crop_total_costs,
                    'total_revenues': crop_total_revenues,
                    'profit': crop_profit,
                    'profit_margin': crop_profit_margin
                })
            
            # الحصول على قيمة المخزون
            inventory_value = self.inventory_manager.get_inventory_value()
            
            # إنشاء DataFrame للتقرير
            report_data = {
                'معلومات التقرير': {
                    'نوع التقرير': 'تقرير مالي شامل',
                    'تاريخ التقرير': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'الفترة': f"{start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}"
                },
                'ملخص مالي': {
                    'إجمالي التكاليف': total_costs,
                    'إجمالي الإيرادات': total_revenues,
                    'صافي الربح': total_profit,
                    'هامش الربح': f"{overall_profit_margin:.2f}%",
                    'قيمة المخزون': inventory_value.get('total_value', 0)
                },
                'البيانات المالية للمزارع': farm_financials,
                'البيانات المالية للمحاصيل': crop_financials,
                'تفاصيل قيمة المخزون': inventory_value.get('category_breakdown', {})
            }
            
            # إنشاء اسم الملف
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"overall_financial_report_{timestamp}"
            
            # إنشاء مسار الملف
            file_path = os.path.join(self.financial_reports_dir, filename)
            
            # إنشاء التقرير بالتنسيق المطلوب
            if format.lower() == 'pdf':
                self._generate_pdf_report(report_data, f"{file_path}.pdf", "التقرير المالي الشامل")
                return f"{file_path}.pdf"
            elif format.lower() == 'excel':
                self._export_to_excel(report_data, f"{file_path}.xlsx")
                return f"{file_path}.xlsx"
            elif format.lower() == 'csv':
                self._export_to_csv(report_data, f"{file_path}.csv")
                return f"{file_path}.csv"
            elif format.lower() == 'json':
                with open(f"{file_path}.json", 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4, default=str)
                return f"{file_path}.json"
            else:
                raise ValueError(f"تنسيق غير مدعوم: {format}")
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء التقرير المالي الشامل: {str(e)}")
            raise
    
    def generate_cost_per_area_report(self, farm_id: int, 
                                     start_date: Optional[datetime.datetime] = None,
                                     end_date: Optional[datetime.datetime] = None,
                                     format: str = 'pdf') -> str:
        """
        إنشاء تقرير التكلفة لكل وحدة مساحة
        
        المعلمات:
            farm_id (int): معرف المزرعة
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            format (str): تنسيق التقرير (pdf، excel، csv، json)
            
        العائد:
            str: مسار ملف التقرير
        """
        try:
            # الحصول على معلومات المزرعة
            farm_info = self.farm_manager.get_farm(farm_id)
            farm_area = farm_info.get('area', 0)
            farm_area_unit = farm_info.get('area_unit', 'فدان')
            
            if farm_area <= 0:
                raise ValueError(f"مساحة المزرعة غير صالحة: {farm_area}")
            
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # الحصول على تكاليف المزرعة
            farm_costs = self.cost_calculator.get_farm_costs(farm_id, start_date, end_date)
            
            # تجميع التكاليف حسب النوع
            cost_by_type = {}
            for cost in farm_costs:
                cost_type = cost['cost_type']
                if cost_type not in cost_by_type:
                    cost_by_type[cost_type] = 0
                cost_by_type[cost_type] += cost['amount']
            
            # حساب التكلفة لكل وحدة مساحة
            cost_per_area_by_type = {}
            for cost_type, amount in cost_by_type.items():
                cost_per_area_by_type[cost_type] = amount / farm_area
            
            # تجميع التكاليف حسب المحصول
            cost_by_crop = {}
            for cost in farm_costs:
                if cost['crop_id']:
                    crop_id = cost['crop_id']
                    crop_info = self.farm_manager.get_crop(crop_id)
                    crop_name = crop_info.get('name', f'محصول {crop_id}')
                    
                    if crop_name not in cost_by_crop:
                        cost_by_crop[crop_name] = 0
                    cost_by_crop[crop_name] += cost['amount']
            
            # الحصول على مساحة كل محصول
            crop_areas = {}
            for crop_name in cost_by_crop.keys():
                # هنا يمكن الحصول على مساحة المحصول من قاعدة البيانات
                # لكن للتبسيط، سنفترض أن كل محصول يشغل نسبة من المساحة الكلية
                crop_areas[crop_name] = farm_area / len(cost_by_crop)
            
            # حساب التكلفة لكل وحدة مساحة لكل محصول
            cost_per_area_by_crop = {}
            for crop_name, amount in cost_by_crop.items():
                crop_area = crop_areas.get(crop_name, 0)
                if crop_area > 0:
                    cost_per_area_by_crop[crop_name] = amount / crop_area
                else:
                    cost_per_area_by_crop[crop_name] = 0
            
            # الحصول على استخدام المخزون
            inventory_usage = self.inventory_manager.get_farm_usage_history(farm_id, start_date, end_date)
            
            # حساب استخدام المخزون لكل وحدة مساحة
            inventory_per_area = self.inventory_manager.calculate_per_area_usage(
                farm_id, farm_area, farm_area_unit, start_date, end_date
            )
            
            # إنشاء DataFrame للتقرير
            report_data = {
                'معلومات المزرعة': {
                    'اسم المزرعة': farm_info.get('name', f'مزرعة {farm_id}'),
                    'الموقع': farm_info.get('location', 'غير محدد'),
                    'المساحة': f"{farm_area} {farm_area_unit}",
                    'تاريخ التقرير': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'الفترة': f"{start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}"
                },
                'التكلفة الإجمالية': sum(cost['amount'] for cost in farm_costs),
                'التكلفة لكل وحدة مساحة': sum(cost['amount'] for cost in farm_costs) / farm_area,
                'التكلفة حسب النوع': cost_by_type,
                'التكلفة لكل وحدة مساحة حسب النوع': cost_per_area_by_type,
                'التكلفة حسب المحصول': cost_by_crop,
                'التكلفة لكل وحدة مساحة حسب المحصول': cost_per_area_by_crop,
                'استخدام المخزون لكل وحدة مساحة': inventory_per_area
            }
            
            # إنشاء اسم الملف
            farm_name = farm_info.get('name', f'farm_{farm_id}').replace(' ', '_')
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{farm_name}_cost_per_area_report_{timestamp}"
            
            # إنشاء مسار الملف
            file_path = os.path.join(self.farm_reports_dir, filename)
            
            # إنشاء التقرير بالتنسيق المطلوب
            if format.lower() == 'pdf':
                self._generate_pdf_report(report_data, f"{file_path}.pdf", f"تقرير التكلفة لكل وحدة مساحة - {farm_info.get('name', f'مزرعة {farm_id}')}")
                return f"{file_path}.pdf"
            elif format.lower() == 'excel':
                self._export_to_excel(report_data, f"{file_path}.xlsx")
                return f"{file_path}.xlsx"
            elif format.lower() == 'csv':
                self._export_to_csv(report_data, f"{file_path}.csv")
                return f"{file_path}.csv"
            elif format.lower() == 'json':
                with open(f"{file_path}.json", 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4, default=str)
                return f"{file_path}.json"
            else:
                raise ValueError(f"تنسيق غير مدعوم: {format}")
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء تقرير التكلفة لكل وحدة مساحة: {str(e)}")
            raise
    
    def generate_profitability_analysis(self, 
                                       start_date: Optional[datetime.datetime] = None,
                                       end_date: Optional[datetime.datetime] = None,
                                       format: str = 'pdf') -> str:
        """
        إنشاء تحليل الربحية للمحاصيل والمزارع
        
        المعلمات:
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            format (str): تنسيق التقرير (pdf، excel، csv، json)
            
        العائد:
            str: مسار ملف التقرير
        """
        try:
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # الحصول على قائمة المزارع
            farms = self.farm_manager.get_all_farms()
            
            # تحليل ربحية المزارع
            farm_profitability = []
            
            for farm in farms:
                farm_id = farm['id']
                farm_costs = self.cost_calculator.get_farm_costs(farm_id, start_date, end_date)
                farm_revenues = self.cost_calculator.get_farm_revenues(farm_id, start_date, end_date)
                
                farm_total_costs = sum(cost['amount'] for cost in farm_costs)
                farm_total_revenues = sum(revenue['amount'] for revenue in farm_revenues)
                farm_profit = farm_total_revenues - farm_total_costs
                farm_profit_margin = (farm_profit / farm_total_revenues * 100) if farm_total_revenues > 0 else 0
                farm_roi = (farm_profit / farm_total_costs * 100) if farm_total_costs > 0 else 0
                
                # تجميع التكاليف حسب النوع
                cost_by_type = {}
                for cost in farm_costs:
                    cost_type = cost['cost_type']
                    if cost_type not in cost_by_type:
                        cost_by_type[cost_type] = 0
                    cost_by_type[cost_type] += cost['amount']
                
                farm_profitability.append({
                    'farm_id': farm_id,
                    'farm_name': farm['name'],
                    'total_costs': farm_total_costs,
                    'total_revenues': farm_total_revenues,
                    'profit': farm_profit,
                    'profit_margin': farm_profit_margin,
                    'roi': farm_roi,
                    'cost_breakdown': cost_by_type
                })
            
            # ترتيب المزارع حسب الربحية
            farm_profitability.sort(key=lambda x: x['profit_margin'], reverse=True)
            
            # الحصول على قائمة المحاصيل
            crops = self.farm_manager.get_all_crops()
            
            # تحليل ربحية المحاصيل
            crop_profitability = []
            
            for crop in crops:
                crop_id = crop['id']
                crop_costs = self.cost_calculator.get_crop_costs(crop_id, start_date, end_date)
                crop_revenues = self.cost_calculator.get_crop_revenues(crop_id, start_date, end_date)
                
                crop_total_costs = sum(cost['amount'] for cost in crop_costs)
                crop_total_revenues = sum(revenue['amount'] for revenue in crop_revenues)
                crop_profit = crop_total_revenues - crop_total_costs
                crop_profit_margin = (crop_profit / crop_total_revenues * 100) if crop_total_revenues > 0 else 0
                crop_roi = (crop_profit / crop_total_costs * 100) if crop_total_costs > 0 else 0
                
                # تجميع التكاليف حسب النوع
                cost_by_type = {}
                for cost in crop_costs:
                    cost_type = cost['cost_type']
                    if cost_type not in cost_by_type:
                        cost_by_type[cost_type] = 0
                    cost_by_type[cost_type] += cost['amount']
                
                crop_profitability.append({
                    'crop_id': crop_id,
                    'crop_name': crop['name'],
                    'crop_type': crop.get('type', 'غير محدد'),
                    'total_costs': crop_total_costs,
                    'total_revenues': crop_total_revenues,
                    'profit': crop_profit,
                    'profit_margin': crop_profit_margin,
                    'roi': crop_roi,
                    'cost_breakdown': cost_by_type
                })
            
            # ترتيب المحاصيل حسب الربحية
            crop_profitability.sort(key=lambda x: x['profit_margin'], reverse=True)
            
            # إنشاء DataFrame للتقرير
            report_data = {
                'معلومات التقرير': {
                    'نوع التقرير': 'تحليل الربحية',
                    'تاريخ التقرير': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'الفترة': f"{start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}"
                },
                'ربحية المزارع': farm_profitability,
                'ربحية المحاصيل': crop_profitability
            }
            
            # إنشاء اسم الملف
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"profitability_analysis_{timestamp}"
            
            # إنشاء مسار الملف
            file_path = os.path.join(self.financial_reports_dir, filename)
            
            # إنشاء التقرير بالتنسيق المطلوب
            if format.lower() == 'pdf':
                self._generate_pdf_report(report_data, f"{file_path}.pdf", "تحليل الربحية")
                return f"{file_path}.pdf"
            elif format.lower() == 'excel':
                self._export_to_excel(report_data, f"{file_path}.xlsx")
                return f"{file_path}.xlsx"
            elif format.lower() == 'csv':
                self._export_to_csv(report_data, f"{file_path}.csv")
                return f"{file_path}.csv"
            elif format.lower() == 'json':
                with open(f"{file_path}.json", 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4, default=str)
                return f"{file_path}.json"
            else:
                raise ValueError(f"تنسيق غير مدعوم: {format}")
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء تحليل الربحية: {str(e)}")
            raise
    
    def generate_financial_charts(self, 
                                 start_date: Optional[datetime.datetime] = None,
                                 end_date: Optional[datetime.datetime] = None,
                                 output_dir: Optional[str] = None) -> List[str]:
        """
        إنشاء رسوم بيانية مالية
        
        المعلمات:
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            output_dir (str): مجلد الإخراج (اختياري)
            
        العائد:
            List[str]: قائمة مسارات ملفات الرسوم البيانية
        """
        try:
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # تعيين مجلد الإخراج
            if not output_dir:
                output_dir = os.path.join(self.financial_reports_dir, 'charts')
            
            # التأكد من وجود المجلد
            os.makedirs(output_dir, exist_ok=True)
            
            # قائمة مسارات الملفات
            file_paths = []
            
            # 1. رسم بياني للربحية حسب المزرعة
            farms = self.farm_manager.get_all_farms()
            farm_profitability = []
            
            for farm in farms:
                farm_id = farm['id']
                farm_costs = self.cost_calculator.get_farm_costs(farm_id, start_date, end_date)
                farm_revenues = self.cost_calculator.get_farm_revenues(farm_id, start_date, end_date)
                
                farm_total_costs = sum(cost['amount'] for cost in farm_costs)
                farm_total_revenues = sum(revenue['amount'] for revenue in farm_revenues)
                farm_profit = farm_total_revenues - farm_total_costs
                farm_profit_margin = (farm_profit / farm_total_revenues * 100) if farm_total_revenues > 0 else 0
                
                farm_profitability.append({
                    'farm_name': farm['name'],
                    'profit': farm_profit,
                    'profit_margin': farm_profit_margin
                })
            
            if farm_profitability:
                df_farm = pd.DataFrame(farm_profitability)
                
                plt.figure(figsize=(12, 8))
                ax = df_farm.plot(kind='bar', x='farm_name', y='profit', color='green')
                plt.title('الربح حسب المزرعة')
                plt.xlabel('المزرعة')
                plt.ylabel('الربح')
                plt.xticks(rotation=45, ha='right')
                
                # إضافة قيم على الرسم البياني
                for i, v in enumerate(df_farm['profit']):
                    ax.text(i, v, f" {v:.2f}", ha='center', va='bottom')
                
                file_path = os.path.join(output_dir, "farm_profit.png")
                plt.savefig(file_path, bbox_inches='tight')
                plt.close()
                file_paths.append(file_path)
                
                plt.figure(figsize=(12, 8))
                ax = df_farm.plot(kind='bar', x='farm_name', y='profit_margin', color='blue')
                plt.title('هامش الربح حسب المزرعة')
                plt.xlabel('المزرعة')
                plt.ylabel('هامش الربح (%)')
                plt.xticks(rotation=45, ha='right')
                
                # إضافة قيم على الرسم البياني
                for i, v in enumerate(df_farm['profit_margin']):
                    ax.text(i, v, f" {v:.2f}%", ha='center', va='bottom')
                
                file_path = os.path.join(output_dir, "farm_profit_margin.png")
                plt.savefig(file_path, bbox_inches='tight')
                plt.close()
                file_paths.append(file_path)
            
            # 2. رسم بياني للربحية حسب المحصول
            crops = self.farm_manager.get_all_crops()
            crop_profitability = []
            
            for crop in crops:
                crop_id = crop['id']
                crop_costs = self.cost_calculator.get_crop_costs(crop_id, start_date, end_date)
                crop_revenues = self.cost_calculator.get_crop_revenues(crop_id, start_date, end_date)
                
                crop_total_costs = sum(cost['amount'] for cost in crop_costs)
                crop_total_revenues = sum(revenue['amount'] for revenue in crop_revenues)
                crop_profit = crop_total_revenues - crop_total_costs
                crop_profit_margin = (crop_profit / crop_total_revenues * 100) if crop_total_revenues > 0 else 0
                
                crop_profitability.append({
                    'crop_name': crop['name'],
                    'profit': crop_profit,
                    'profit_margin': crop_profit_margin
                })
            
            if crop_profitability:
                df_crop = pd.DataFrame(crop_profitability)
                
                plt.figure(figsize=(12, 8))
                ax = df_crop.plot(kind='bar', x='crop_name', y='profit', color='green')
                plt.title('الربح حسب المحصول')
                plt.xlabel('المحصول')
                plt.ylabel('الربح')
                plt.xticks(rotation=45, ha='right')
                
                # إضافة قيم على الرسم البياني
                for i, v in enumerate(df_crop['profit']):
                    ax.text(i, v, f" {v:.2f}", ha='center', va='bottom')
                
                file_path = os.path.join(output_dir, "crop_profit.png")
                plt.savefig(file_path, bbox_inches='tight')
                plt.close()
                file_paths.append(file_path)
                
                plt.figure(figsize=(12, 8))
                ax = df_crop.plot(kind='bar', x='crop_name', y='profit_margin', color='blue')
                plt.title('هامش الربح حسب المحصول')
                plt.xlabel('المحصول')
                plt.ylabel('هامش الربح (%)')
                plt.xticks(rotation=45, ha='right')
                
                # إضافة قيم على الرسم البياني
                for i, v in enumerate(df_crop['profit_margin']):
                    ax.text(i, v, f" {v:.2f}%", ha='center', va='bottom')
                
                file_path = os.path.join(output_dir, "crop_profit_margin.png")
                plt.savefig(file_path, bbox_inches='tight')
                plt.close()
                file_paths.append(file_path)
            
            # 3. رسم بياني للتكاليف حسب النوع
            session = self.Session()
            try:
                # الحصول على إجمالي التكاليف حسب النوع
                cost_by_type = session.execute(text(f"""
                    SELECT cost_type, SUM(amount) as total_amount
                    FROM farm_costs
                    WHERE date >= '{start_date.strftime('%Y-%m-%d')}'
                    AND date <= '{end_date.strftime('%Y-%m-%d')}'
                    GROUP BY cost_type
                    ORDER BY total_amount DESC
                """)).fetchall()
                
                if cost_by_type:
                    cost_types = [row[0] for row in cost_by_type]
                    cost_amounts = [row[1] for row in cost_by_type]
                    
                    plt.figure(figsize=(12, 8))
                    plt.pie(cost_amounts, labels=cost_types, autopct='%1.1f%%', startangle=90)
                    plt.axis('equal')
                    plt.title('توزيع التكاليف حسب النوع')
                    
                    file_path = os.path.join(output_dir, "cost_distribution_by_type.png")
                    plt.savefig(file_path, bbox_inches='tight')
                    plt.close()
                    file_paths.append(file_path)
            finally:
                session.close()
            
            # 4. رسم بياني للإيرادات والتكاليف الشهرية
            session = self.Session()
            try:
                # الحصول على التكاليف الشهرية
                monthly_costs = session.execute(text(f"""
                    SELECT strftime('%Y-%m', date) as month, SUM(amount) as total_amount
                    FROM farm_costs
                    WHERE date >= '{start_date.strftime('%Y-%m-%d')}'
                    AND date <= '{end_date.strftime('%Y-%m-%d')}'
                    GROUP BY month
                    ORDER BY month
                """)).fetchall()
                
                # الحصول على الإيرادات الشهرية
                monthly_revenues = session.execute(text(f"""
                    SELECT strftime('%Y-%m', date) as month, SUM(amount) as total_amount
                    FROM farm_revenues
                    WHERE date >= '{start_date.strftime('%Y-%m-%d')}'
                    AND date <= '{end_date.strftime('%Y-%m-%d')}'
                    GROUP BY month
                    ORDER BY month
                """)).fetchall()
                
                if monthly_costs or monthly_revenues:
                    # إنشاء DataFrame للتكاليف
                    df_costs = pd.DataFrame(monthly_costs, columns=['month', 'costs'])
                    df_costs.set_index('month', inplace=True)
                    
                    # إنشاء DataFrame للإيرادات
                    df_revenues = pd.DataFrame(monthly_revenues, columns=['month', 'revenues'])
                    df_revenues.set_index('month', inplace=True)
                    
                    # دمج البيانات
                    df_monthly = pd.concat([df_costs, df_revenues], axis=1)
                    df_monthly.fillna(0, inplace=True)
                    
                    # حساب الربح
                    df_monthly['profit'] = df_monthly['revenues'] - df_monthly['costs']
                    
                    plt.figure(figsize=(12, 8))
                    ax = df_monthly.plot(kind='bar', y=['costs', 'revenues', 'profit'], 
                                        color=['red', 'green', 'blue'])
                    plt.title('التكاليف والإيرادات والربح الشهري')
                    plt.xlabel('الشهر')
                    plt.ylabel('المبلغ')
                    plt.xticks(rotation=45, ha='right')
                    plt.legend(['التكاليف', 'الإيرادات', 'الربح'])
                    
                    file_path = os.path.join(output_dir, "monthly_financial_summary.png")
                    plt.savefig(file_path, bbox_inches='tight')
                    plt.close()
                    file_paths.append(file_path)
            finally:
                session.close()
            
            return file_paths
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء الرسوم البيانية المالية: {str(e)}")
            raise
    
    def generate_financial_dashboard(self, 
                                    start_date: Optional[datetime.datetime] = None,
                                    end_date: Optional[datetime.datetime] = None,
                                    output_file: Optional[str] = None) -> str:
        """
        إنشاء لوحة معلومات مالية تفاعلية
        
        المعلمات:
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            output_file (str): مسار ملف الإخراج (اختياري)
            
        العائد:
            str: مسار ملف لوحة المعلومات
        """
        try:
            # تعيين تواريخ افتراضية إذا لم يتم تحديدها
            if not end_date:
                end_date = datetime.datetime.now()
            if not start_date:
                # افتراضيًا، استخدم بداية السنة الحالية
                start_date = datetime.datetime(end_date.year, 1, 1)
            
            # تعيين مسار ملف الإخراج
            if not output_file:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(self.financial_reports_dir, f"financial_dashboard_{timestamp}.html")
            
            # إنشاء الرسوم البيانية
            charts_dir = os.path.join(os.path.dirname(output_file), 'dashboard_charts')
            os.makedirs(charts_dir, exist_ok=True)
            
            chart_files = self.generate_financial_charts(start_date, end_date, charts_dir)
            
            # الحصول على البيانات المالية الإجمالية
            overall_financial_data = self._get_overall_financial_data(start_date, end_date)
            
            # إنشاء ملف HTML للوحة المعلومات
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"""
                <!DOCTYPE html>
                <html dir="rtl" lang="ar">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>لوحة المعلومات المالية</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f5f5f5;
                            color: #333;
                        }}
                        .dashboard {{
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            background-color: #2c3e50;
                            color: white;
                            padding: 20px;
                            border-radius: 5px;
                            margin-bottom: 20px;
                            text-align: center;
                        }}
                        .summary-cards {{
                            display: flex;
                            flex-wrap: wrap;
                            gap: 20px;
                            margin-bottom: 20px;
                        }}
                        .card {{
                            background-color: white;
                            border-radius: 5px;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                            padding: 20px;
                            flex: 1;
                            min-width: 200px;
                        }}
                        .card h3 {{
                            margin-top: 0;
                            color: #2c3e50;
                            border-bottom: 1px solid #eee;
                            padding-bottom: 10px;
                        }}
                        .card .value {{
                            font-size: 24px;
                            font-weight: bold;
                            color: #27ae60;
                        }}
                        .card .negative {{
                            color: #e74c3c;
                        }}
                        .charts {{
                            display: flex;
                            flex-wrap: wrap;
                            gap: 20px;
                            margin-bottom: 20px;
                        }}
                        .chart-container {{
                            background-color: white;
                            border-radius: 5px;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                            padding: 20px;
                            flex: 1 1 calc(50% - 20px);
                            min-width: 300px;
                        }}
                        .chart-container h3 {{
                            margin-top: 0;
                            color: #2c3e50;
                            border-bottom: 1px solid #eee;
                            padding-bottom: 10px;
                        }}
                        .chart-img {{
                            width: 100%;
                            height: auto;
                            margin-top: 10px;
                        }}
                        .footer {{
                            text-align: center;
                            margin-top: 20px;
                            padding: 10px;
                            color: #7f8c8d;
                            font-size: 14px;
                        }}
                        @media (max-width: 768px) {{
                            .chart-container {{
                                flex: 1 1 100%;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="dashboard">
                        <div class="header">
                            <h1>لوحة المعلومات المالية</h1>
                            <p>الفترة: {start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}</p>
                        </div>
                        
                        <div class="summary-cards">
                            <div class="card">
                                <h3>إجمالي التكاليف</h3>
                                <div class="value">{overall_financial_data['total_costs']:.2f}</div>
                            </div>
                            <div class="card">
                                <h3>إجمالي الإيرادات</h3>
                                <div class="value">{overall_financial_data['total_revenues']:.2f}</div>
                            </div>
                            <div class="card">
                                <h3>صافي الربح</h3>
                                <div class="value {'' if overall_financial_data['net_profit'] >= 0 else 'negative'}">{overall_financial_data['net_profit']:.2f}</div>
                            </div>
                            <div class="card">
                                <h3>هامش الربح</h3>
                                <div class="value {'' if overall_financial_data['profit_margin'] >= 0 else 'negative'}">{overall_financial_data['profit_margin']:.2f}%</div>
                            </div>
                        </div>
                        
                        <div class="charts">
                """)
                
                # إضافة الرسوم البيانية
                for i, chart_file in enumerate(chart_files):
                    chart_title = os.path.basename(chart_file).replace('.png', '').replace('_', ' ').title()
                    relative_path = os.path.relpath(chart_file, os.path.dirname(output_file))
                    
                    f.write(f"""
                            <div class="chart-container">
                                <h3>{chart_title}</h3>
                                <img class="chart-img" src="{relative_path}" alt="{chart_title}">
                            </div>
                    """)
                
                f.write(f"""
                        </div>
                        
                        <div class="footer">
                            <p>تم إنشاء هذا التقرير في {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        </div>
                    </div>
                </body>
                </html>
                """)
            
            return output_file
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء لوحة المعلومات المالية: {str(e)}")
            raise
    
    def _get_overall_financial_data(self, start_date: datetime.datetime, end_date: datetime.datetime) -> Dict:
        """
        الحصول على البيانات المالية الإجمالية
        
        المعلمات:
            start_date (datetime): تاريخ البداية
            end_date (datetime): تاريخ النهاية
            
        العائد:
            Dict: البيانات المالية الإجمالية
        """
        session = self.Session()
        try:
            # الحصول على إجمالي التكاليف
            total_costs_result = session.execute(text(f"""
                SELECT SUM(amount) as total_costs
                FROM farm_costs
                WHERE date >= '{start_date.strftime('%Y-%m-%d')}'
                AND date <= '{end_date.strftime('%Y-%m-%d')}'
            """)).fetchone()
            
            total_costs = total_costs_result[0] if total_costs_result and total_costs_result[0] else 0
            
            # الحصول على إجمالي الإيرادات
            total_revenues_result = session.execute(text(f"""
                SELECT SUM(amount) as total_revenues
                FROM farm_revenues
                WHERE date >= '{start_date.strftime('%Y-%m-%d')}'
                AND date <= '{end_date.strftime('%Y-%m-%d')}'
            """)).fetchone()
            
            total_revenues = total_revenues_result[0] if total_revenues_result and total_revenues_result[0] else 0
            
            # حساب صافي الربح وهامش الربح
            net_profit = total_revenues - total_costs
            profit_margin = (net_profit / total_revenues * 100) if total_revenues > 0 else 0
            
            return {
                'total_costs': total_costs,
                'total_revenues': total_revenues,
                'net_profit': net_profit,
                'profit_margin': profit_margin
            }
        
        finally:
            session.close()
    
    def _generate_pdf_report(self, data: Dict, output_file: str, title: str) -> None:
        """
        إنشاء تقرير PDF
        
        المعلمات:
            data (Dict): بيانات التقرير
            output_file (str): مسار ملف الإخراج
            title (str): عنوان التقرير
        """
        try:
            # هنا يمكن استخدام مكتبة مثل ReportLab أو FPDF لإنشاء ملف PDF
            # لكن للتبسيط، سنقوم بتصدير البيانات إلى ملف JSON
            with open(output_file.replace('.pdf', '.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4, default=str)
            
            logger.info(f"تم تصدير البيانات إلى {output_file.replace('.pdf', '.json')}")
            logger.warning("إنشاء ملفات PDF غير مدعوم حاليًا، تم تصدير البيانات إلى ملف JSON بدلاً من ذلك")
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء تقرير PDF: {str(e)}")
            raise
    
    def _export_to_excel(self, data: Dict, output_file: str) -> None:
        """
        تصدير البيانات إلى ملف Excel
        
        المعلمات:
            data (Dict): بيانات التقرير
            output_file (str): مسار ملف الإخراج
        """
        try:
            # إنشاء مصنف Excel
            writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
            
            # تصدير كل قسم إلى ورقة منفصلة
            for section_name, section_data in data.items():
                if isinstance(section_data, dict):
                    # إذا كان القسم عبارة عن قاموس، قم بتحويله إلى DataFrame
                    df = pd.DataFrame(list(section_data.items()), columns=['المفتاح', 'القيمة'])
                    df.to_excel(writer, sheet_name=section_name, index=False)
                elif isinstance(section_data, list):
                    # إذا كان القسم عبارة عن قائمة، قم بتحويله إلى DataFrame
                    df = pd.DataFrame(section_data)
                    df.to_excel(writer, sheet_name=section_name, index=False)
                else:
                    # إذا كان القسم قيمة بسيطة، قم بإنشاء DataFrame بسيط
                    df = pd.DataFrame([[section_data]], columns=[section_name])
                    df.to_excel(writer, sheet_name=section_name, index=False)
            
            # حفظ الملف
            writer.close()
        
        except Exception as e:
            logger.error(f"خطأ في تصدير البيانات إلى Excel: {str(e)}")
            raise
    
    def _export_to_csv(self, data: Dict, output_file: str) -> None:
        """
        تصدير البيانات إلى ملف CSV
        
        المعلمات:
            data (Dict): بيانات التقرير
            output_file (str): مسار ملف الإخراج
        """
        try:
            # تحويل البيانات إلى تنسيق مسطح
            flat_data = []
            
            for section_name, section_data in data.items():
                if isinstance(section_data, dict):
                    for key, value in section_data.items():
                        flat_data.append({
                            'القسم': section_name,
                            'المفتاح': key,
                            'القيمة': value
                        })
                elif isinstance(section_data, list):
                    for item in section_data:
                        if isinstance(item, dict):
                            item_with_section = {'القسم': section_name}
                            item_with_section.update(item)
                            flat_data.append(item_with_section)
                        else:
                            flat_data.append({
                                'القسم': section_name,
                                'القيمة': item
                            })
                else:
                    flat_data.append({
                        'القسم': section_name,
                        'القيمة': section_data
                    })
            
            # إنشاء DataFrame وتصديره إلى CSV
            df = pd.DataFrame(flat_data)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        except Exception as e:
            logger.error(f"خطأ في تصدير البيانات إلى CSV: {str(e)}")
            raise
