#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام حساب التكلفة للنظام الزراعي
================================
هذه الوحدة مسؤولة عن حساب وتحليل التكاليف المتعلقة بالعمليات الزراعية المختلفة
بما في ذلك تكاليف الزراعة، الري، التسميد، المكافحة، والحصاد.
"""

import os
import json
import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from ..database.database_manager import DatabaseManager
from ..audit.audit_manager import AuditManager
from ..auth.auth_manager import AuthManager

# تحميل متغيرات البيئة
load_dotenv()

class CostCalculator:
    """مدير حساب التكلفة للنظام الزراعي"""
    
    def __init__(self, db_manager=None, audit_manager=None, auth_manager=None):
        """
        تهيئة مدير حساب التكلفة
        
        المعاملات:
            db_manager (DatabaseManager): مدير قاعدة البيانات
            audit_manager (AuditManager): مدير التدقيق
            auth_manager (AuthManager): مدير المصادقة
        """
        self.db_manager = db_manager or DatabaseManager()
        self.audit_manager = audit_manager or AuditManager()
        self.auth_manager = auth_manager or AuthManager()
        
        # تحميل بيانات التكلفة الافتراضية
        self.default_costs = {
            'seeds': {
                'vegetables': {'tomato': 500, 'cucumber': 450, 'pepper': 550},
                'fruits': {'apple': 1200, 'orange': 1000, 'grape': 1500},
                'crops': {'wheat': 300, 'corn': 350, 'rice': 400}
            },
            'fertilizers': {
                'nitrogen': 8.5,  # سعر الكيلوجرام
                'phosphorus': 10.2,
                'potassium': 9.8,
                'organic': 5.0,
                'compound': 12.5
            },
            'pesticides': {
                'insecticide': 120,  # سعر اللتر
                'fungicide': 150,
                'herbicide': 100,
                'biological': 200
            },
            'irrigation': {
                'drip': 0.8,  # تكلفة المتر المكعب
                'sprinkler': 0.9,
                'surface': 0.5
            },
            'labor': {
                'planting': 150,  # تكلفة العامل في اليوم
                'maintenance': 120,
                'harvesting': 180
            },
            'machinery': {
                'tractor': 500,  # تكلفة الساعة
                'harvester': 800,
                'sprayer': 300
            },
            'nursery': {
                'seedling_base': 2.5,  # تكلفة الشتلة الأساسية
                'tray': 15,  # تكلفة الصينية
                'substrate': 50,  # تكلفة وسط الزراعة للمتر المكعب
                'labor_per_1000': 100  # تكلفة العمالة لكل 1000 شتلة
            }
        }
    
    def calculate_crop_cost(self, crop_data, user_id):
        """
        حساب تكلفة زراعة محصول
        
        المعاملات:
            crop_data (dict): بيانات المحصول
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تفاصيل التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_data'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات المحصول
            crop_type = crop_data.get('crop_type', '')  # نوع المحصول (خضروات، فواكه، محاصيل)
            crop_name = crop_data.get('crop_name', '')  # اسم المحصول
            area = crop_data.get('area', 0)  # المساحة بالفدان
            plants_per_acre = crop_data.get('plants_per_acre', 0)  # عدد النباتات في الفدان
            
            # بيانات المدخلات
            seeds_cost = crop_data.get('seeds_cost', self.default_costs['seeds'].get(crop_type, {}).get(crop_name, 0))
            fertilizers = crop_data.get('fertilizers', [])
            pesticides = crop_data.get('pesticides', [])
            irrigation_type = crop_data.get('irrigation_type', 'drip')
            irrigation_amount = crop_data.get('irrigation_amount', 0)  # بالمتر المكعب
            labor_days = crop_data.get('labor_days', {'planting': 0, 'maintenance': 0, 'harvesting': 0})
            machinery_hours = crop_data.get('machinery_hours', {'tractor': 0, 'harvester': 0, 'sprayer': 0})
            
            # حساب تكلفة البذور/الشتلات
            if crop_data.get('use_seedlings', False):
                # استخدام الشتلات
                seedling_cost = crop_data.get('seedling_cost', self.default_costs['nursery']['seedling_base'])
                total_seeds_cost = seedling_cost * plants_per_acre * area
            else:
                # استخدام البذور مباشرة
                total_seeds_cost = seeds_cost * area
            
            # حساب تكلفة الأسمدة
            total_fertilizers_cost = 0
            for fertilizer in fertilizers:
                fert_type = fertilizer.get('type', '')
                amount = fertilizer.get('amount', 0)  # بالكيلوجرام
                price = fertilizer.get('price', self.default_costs['fertilizers'].get(fert_type, 0))
                total_fertilizers_cost += price * amount
            
            # حساب تكلفة المبيدات
            total_pesticides_cost = 0
            for pesticide in pesticides:
                pest_type = pesticide.get('type', '')
                amount = pesticide.get('amount', 0)  # باللتر
                price = pesticide.get('price', self.default_costs['pesticides'].get(pest_type, 0))
                total_pesticides_cost += price * amount
            
            # حساب تكلفة الري
            irrigation_price = self.default_costs['irrigation'].get(irrigation_type, 0)
            total_irrigation_cost = irrigation_price * irrigation_amount
            
            # حساب تكلفة العمالة
            total_labor_cost = 0
            for labor_type, days in labor_days.items():
                labor_price = self.default_costs['labor'].get(labor_type, 0)
                total_labor_cost += labor_price * days
            
            # حساب تكلفة الآلات
            total_machinery_cost = 0
            for machine_type, hours in machinery_hours.items():
                machine_price = self.default_costs['machinery'].get(machine_type, 0)
                total_machinery_cost += machine_price * hours
            
            # حساب التكلفة الإجمالية
            total_cost = (
                total_seeds_cost +
                total_fertilizers_cost +
                total_pesticides_cost +
                total_irrigation_cost +
                total_labor_cost +
                total_machinery_cost
            )
            
            # حساب التكلفة لكل فدان
            cost_per_acre = total_cost / area if area > 0 else 0
            
            # حساب التكلفة لكل نبات
            total_plants = plants_per_acre * area
            cost_per_plant = total_cost / total_plants if total_plants > 0 else 0
            
            # إعداد تفاصيل التكلفة
            cost_details = {
                'success': True,
                'crop_info': {
                    'crop_type': crop_type,
                    'crop_name': crop_name,
                    'area': area,
                    'plants_per_acre': plants_per_acre,
                    'total_plants': total_plants
                },
                'costs': {
                    'seeds_seedlings': total_seeds_cost,
                    'fertilizers': total_fertilizers_cost,
                    'pesticides': total_pesticides_cost,
                    'irrigation': total_irrigation_cost,
                    'labor': total_labor_cost,
                    'machinery': total_machinery_cost,
                    'total': total_cost
                },
                'metrics': {
                    'cost_per_acre': cost_per_acre,
                    'cost_per_plant': cost_per_plant
                },
                'calculation_date': datetime.datetime.now().isoformat()
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='calculate_crop_cost',
                entity_type='crop',
                entity_id=f"{crop_type}_{crop_name}",
                details=f"Calculated cost for {crop_name} ({crop_type}), Area: {area} acres"
            )
            
            return cost_details
            
        except Exception as e:
            return {'success': False, 'message': f'Error calculating crop cost: {str(e)}'}
    
    def calculate_nursery_cost(self, nursery_data, user_id):
        """
        حساب تكلفة إنتاج الشتلات في المشتل
        
        المعاملات:
            nursery_data (dict): بيانات المشتل
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تفاصيل التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_data'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات المشتل
            nursery_name = nursery_data.get('nursery_name', '')
            seedling_type = nursery_data.get('seedling_type', '')
            seedling_count = nursery_data.get('seedling_count', 0)
            batch_id = nursery_data.get('batch_id', '')
            seeds_per_batch = nursery_data.get('seeds_per_batch', 0)
            
            # بيانات المدخلات
            seed_cost = nursery_data.get('seed_cost', 0)
            tray_count = nursery_data.get('tray_count', 0)
            substrate_volume = nursery_data.get('substrate_volume', 0)  # بالمتر المكعب
            fertilizers = nursery_data.get('fertilizers', [])
            pesticides = nursery_data.get('pesticides', [])
            labor_days = nursery_data.get('labor_days', 0)
            
            # حساب تكلفة البذور
            total_seed_cost = seed_cost * seeds_per_batch
            
            # حساب تكلفة الصواني
            tray_price = nursery_data.get('tray_price', self.default_costs['nursery']['tray'])
            total_tray_cost = tray_price * tray_count
            
            # حساب تكلفة وسط الزراعة
            substrate_price = nursery_data.get('substrate_price', self.default_costs['nursery']['substrate'])
            total_substrate_cost = substrate_price * substrate_volume
            
            # حساب تكلفة الأسمدة
            total_fertilizers_cost = 0
            for fertilizer in fertilizers:
                fert_type = fertilizer.get('type', '')
                amount = fertilizer.get('amount', 0)  # بالكيلوجرام
                price = fertilizer.get('price', self.default_costs['fertilizers'].get(fert_type, 0))
                total_fertilizers_cost += price * amount
            
            # حساب تكلفة المبيدات
            total_pesticides_cost = 0
            for pesticide in pesticides:
                pest_type = pesticide.get('type', '')
                amount = pesticide.get('amount', 0)  # باللتر
                price = pesticide.get('price', self.default_costs['pesticides'].get(pest_type, 0))
                total_pesticides_cost += price * amount
            
            # حساب تكلفة العمالة
            labor_price = nursery_data.get('labor_price', self.default_costs['nursery']['labor_per_1000'] / 1000)
            total_labor_cost = labor_price * seedling_count * labor_days
            
            # حساب التكلفة الإجمالية
            total_cost = (
                total_seed_cost +
                total_tray_cost +
                total_substrate_cost +
                total_fertilizers_cost +
                total_pesticides_cost +
                total_labor_cost
            )
            
            # حساب التكلفة لكل شتلة
            cost_per_seedling = total_cost / seedling_count if seedling_count > 0 else 0
            
            # حساب نسبة نجاح الإنبات
            germination_rate = (seedling_count / seeds_per_batch) * 100 if seeds_per_batch > 0 else 0
            
            # إعداد تفاصيل التكلفة
            cost_details = {
                'success': True,
                'nursery_info': {
                    'nursery_name': nursery_name,
                    'seedling_type': seedling_type,
                    'batch_id': batch_id,
                    'seedling_count': seedling_count,
                    'seeds_per_batch': seeds_per_batch,
                    'germination_rate': germination_rate
                },
                'costs': {
                    'seeds': total_seed_cost,
                    'trays': total_tray_cost,
                    'substrate': total_substrate_cost,
                    'fertilizers': total_fertilizers_cost,
                    'pesticides': total_pesticides_cost,
                    'labor': total_labor_cost,
                    'total': total_cost
                },
                'metrics': {
                    'cost_per_seedling': cost_per_seedling
                },
                'calculation_date': datetime.datetime.now().isoformat()
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='calculate_nursery_cost',
                entity_type='nursery_batch',
                entity_id=batch_id,
                details=f"Calculated cost for {seedling_type} seedlings, Batch: {batch_id}, Count: {seedling_count}"
            )
            
            return cost_details
            
        except Exception as e:
            return {'success': False, 'message': f'Error calculating nursery cost: {str(e)}'}
    
    def calculate_treatment_cost(self, treatment_data, user_id):
        """
        حساب تكلفة العلاج
        
        المعاملات:
            treatment_data (dict): بيانات العلاج
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تفاصيل التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_data'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات العلاج
            treatment_name = treatment_data.get('treatment_name', '')
            treatment_type = treatment_data.get('treatment_type', '')  # مبيد، سماد، إلخ
            area = treatment_data.get('area', 0)  # المساحة بالفدان
            plants_count = treatment_data.get('plants_count', 0)
            
            # بيانات المدخلات
            products = treatment_data.get('products', [])
            labor_days = treatment_data.get('labor_days', 0)
            machinery_hours = treatment_data.get('machinery_hours', 0)
            
            # حساب تكلفة المنتجات
            total_products_cost = 0
            for product in products:
                product_type = product.get('type', '')
                amount = product.get('amount', 0)
                unit = product.get('unit', 'kg')  # الوحدة (كجم، لتر)
                price = product.get('price', 0)
                
                # استخدام السعر الافتراضي إذا لم يتم تحديد السعر
                if price == 0:
                    if treatment_type == 'fertilizer':
                        price = self.default_costs['fertilizers'].get(product_type, 0)
                    elif treatment_type == 'pesticide':
                        price = self.default_costs['pesticides'].get(product_type, 0)
                
                total_products_cost += price * amount
            
            # حساب تكلفة العمالة
            labor_price = treatment_data.get('labor_price', self.default_costs['labor'].get('maintenance', 0))
            total_labor_cost = labor_price * labor_days
            
            # حساب تكلفة الآلات
            machinery_price = treatment_data.get('machinery_price', self.default_costs['machinery'].get('sprayer', 0))
            total_machinery_cost = machinery_price * machinery_hours
            
            # حساب التكلفة الإجمالية
            total_cost = total_products_cost + total_labor_cost + total_machinery_cost
            
            # حساب التكلفة لكل فدان
            cost_per_acre = total_cost / area if area > 0 else 0
            
            # حساب التكلفة لكل نبات
            cost_per_plant = total_cost / plants_count if plants_count > 0 else 0
            
            # إعداد تفاصيل التكلفة
            cost_details = {
                'success': True,
                'treatment_info': {
                    'treatment_name': treatment_name,
                    'treatment_type': treatment_type,
                    'area': area,
                    'plants_count': plants_count
                },
                'costs': {
                    'products': total_products_cost,
                    'labor': total_labor_cost,
                    'machinery': total_machinery_cost,
                    'total': total_cost
                },
                'metrics': {
                    'cost_per_acre': cost_per_acre,
                    'cost_per_plant': cost_per_plant
                },
                'calculation_date': datetime.datetime.now().isoformat()
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='calculate_treatment_cost',
                entity_type='treatment',
                entity_id=treatment_name,
                details=f"Calculated cost for {treatment_name} treatment, Area: {area} acres"
            )
            
            return cost_details
            
        except Exception as e:
            return {'success': False, 'message': f'Error calculating treatment cost: {str(e)}'}
    
    def calculate_farm_operation_cost(self, operation_data, user_id):
        """
        حساب تكلفة عملية زراعية
        
        المعاملات:
            operation_data (dict): بيانات العملية
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تفاصيل التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_data'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات العملية
            operation_name = operation_data.get('operation_name', '')
            operation_type = operation_data.get('operation_type', '')  # زراعة، حصاد، إلخ
            area = operation_data.get('area', 0)  # المساحة بالفدان
            
            # بيانات المدخلات
            labor_days = operation_data.get('labor_days', 0)
            machinery_hours = operation_data.get('machinery_hours', 0)
            supplies = operation_data.get('supplies', [])
            
            # حساب تكلفة العمالة
            labor_price = operation_data.get('labor_price', self.default_costs['labor'].get(operation_type, 0))
            total_labor_cost = labor_price * labor_days
            
            # حساب تكلفة الآلات
            machinery_type = operation_data.get('machinery_type', '')
            machinery_price = operation_data.get('machinery_price', self.default_costs['machinery'].get(machinery_type, 0))
            total_machinery_cost = machinery_price * machinery_hours
            
            # حساب تكلفة المستلزمات
            total_supplies_cost = 0
            for supply in supplies:
                supply_name = supply.get('name', '')
                amount = supply.get('amount', 0)
                price = supply.get('price', 0)
                total_supplies_cost += price * amount
            
            # حساب التكلفة الإجمالية
            total_cost = total_labor_cost + total_machinery_cost + total_supplies_cost
            
            # حساب التكلفة لكل فدان
            cost_per_acre = total_cost / area if area > 0 else 0
            
            # إعداد تفاصيل التكلفة
            cost_details = {
                'success': True,
                'operation_info': {
                    'operation_name': operation_name,
                    'operation_type': operation_type,
                    'area': area
                },
                'costs': {
                    'labor': total_labor_cost,
                    'machinery': total_machinery_cost,
                    'supplies': total_supplies_cost,
                    'total': total_cost
                },
                'metrics': {
                    'cost_per_acre': cost_per_acre
                },
                'calculation_date': datetime.datetime.now().isoformat()
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='calculate_operation_cost',
                entity_type='farm_operation',
                entity_id=operation_name,
                details=f"Calculated cost for {operation_name} operation, Area: {area} acres"
            )
            
            return cost_details
            
        except Exception as e:
            return {'success': False, 'message': f'Error calculating operation cost: {str(e)}'}
    
    def calculate_total_farm_cost(self, farm_id, start_date, end_date, user_id):
        """
        حساب التكلفة الإجمالية للمزرعة خلال فترة زمنية
        
        المعاملات:
            farm_id (int): معرف المزرعة
            start_date (str): تاريخ البداية (YYYY-MM-DD)
            end_date (str): تاريخ النهاية (YYYY-MM-DD)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تفاصيل التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_data'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استعلام عن بيانات المزرعة
            farm_query = """
                SELECT name, location, total_area, owner_id
                FROM farms
                WHERE id = %s
            """
            farm_result = self.db_manager.execute_query(farm_query, (farm_id,))
            
            if not farm_result:
                return {'success': False, 'message': 'Farm not found'}
            
            farm_name = farm_result[0][0]
            farm_location = farm_result[0][1]
            farm_area = farm_result[0][2]
            farm_owner = farm_result[0][3]
            
            # استعلام عن تكاليف المحاصيل
            crops_query = """
                SELECT SUM(cost) 
                FROM crop_costs
                WHERE farm_id = %s AND date BETWEEN %s AND %s
            """
            crops_result = self.db_manager.execute_query(crops_query, (farm_id, start_date, end_date))
            total_crops_cost = crops_result[0][0] if crops_result[0][0] else 0
            
            # استعلام عن تكاليف العلاجات
            treatments_query = """
                SELECT SUM(cost) 
                FROM treatment_costs
                WHERE farm_id = %s AND date BETWEEN %s AND %s
            """
            treatments_result = self.db_manager.execute_query(treatments_query, (farm_id, start_date, end_date))
            total_treatments_cost = treatments_result[0][0] if treatments_result[0][0] else 0
            
            # استعلام عن تكاليف العمليات
            operations_query = """
                SELECT SUM(cost) 
                FROM operation_costs
                WHERE farm_id = %s AND date BETWEEN %s AND %s
            """
            operations_result = self.db_manager.execute_query(operations_query, (farm_id, start_date, end_date))
            total_operations_cost = operations_result[0][0] if operations_result[0][0] else 0
            
            # استعلام عن تكاليف أخرى
            other_query = """
                SELECT SUM(cost) 
                FROM other_costs
                WHERE farm_id = %s AND date BETWEEN %s AND %s
            """
            other_result = self.db_manager.execute_query(other_query, (farm_id, start_date, end_date))
            total_other_cost = other_result[0][0] if other_result[0][0] else 0
            
            # حساب التكلفة الإجمالية
            total_cost = total_crops_cost + total_treatments_cost + total_operations_cost + total_other_cost
            
            # حساب التكلفة لكل فدان
            cost_per_acre = total_cost / farm_area if farm_area > 0 else 0
            
            # إعداد تفاصيل التكلفة
            cost_details = {
                'success': True,
                'farm_info': {
                    'farm_id': farm_id,
                    'farm_name': farm_name,
                    'farm_location': farm_location,
                    'farm_area': farm_area,
                    'farm_owner': farm_owner,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    }
                },
                'costs': {
                    'crops': total_crops_cost,
                    'treatments': total_treatments_cost,
                    'operations': total_operations_cost,
                    'other': total_other_cost,
                    'total': total_cost
                },
                'metrics': {
                    'cost_per_acre': cost_per_acre
                },
                'calculation_date': datetime.datetime.now().isoformat()
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='calculate_farm_cost',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Calculated total cost for farm {farm_name} from {start_date} to {end_date}"
            )
            
            return cost_details
            
        except Exception as e:
            return {'success': False, 'message': f'Error calculating farm cost: {str(e)}'}
    
    def update_cost_parameters(self, cost_type, parameters, user_id):
        """
        تحديث معاملات التكلفة
        
        المعاملات:
            cost_type (str): نوع التكلفة (seeds, fertilizers, pesticides, etc.)
            parameters (dict): معاملات التكلفة الجديدة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التحديث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'manage_cost_parameters'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود نوع التكلفة
            if cost_type not in self.default_costs:
                return {'success': False, 'message': f'Invalid cost type: {cost_type}'}
            
            # تحديث معاملات التكلفة
            for key, value in parameters.items():
                if key in self.default_costs[cost_type]:
                    self.default_costs[cost_type][key] = value
            
            # حفظ المعاملات المحدثة في قاعدة البيانات
            self.db_manager.execute_query(
                """
                INSERT INTO cost_parameters (cost_type, parameters, updated_by, updated_at)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                parameters = %s, updated_by = %s, updated_at = %s
                """,
                (
                    cost_type, 
                    json.dumps(self.default_costs[cost_type]), 
                    user_id, 
                    datetime.datetime.now().isoformat(),
                    json.dumps(self.default_costs[cost_type]), 
                    user_id, 
                    datetime.datetime.now().isoformat()
                )
            )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='update_cost_parameters',
                entity_type='cost_parameters',
                entity_id=cost_type,
                details=f"Updated cost parameters for {cost_type}"
            )
            
            return {
                'success': True,
                'message': f'Cost parameters for {cost_type} updated successfully',
                'updated_parameters': self.default_costs[cost_type]
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error updating cost parameters: {str(e)}'}
    
    def get_cost_parameters(self, cost_type, user_id):
        """
        الحصول على معاملات التكلفة
        
        المعاملات:
            cost_type (str): نوع التكلفة (seeds, fertilizers, pesticides, etc.)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: معاملات التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_data'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود نوع التكلفة
            if cost_type not in self.default_costs:
                return {'success': False, 'message': f'Invalid cost type: {cost_type}'}
            
            return {
                'success': True,
                'cost_type': cost_type,
                'parameters': self.default_costs[cost_type]
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting cost parameters: {str(e)}'}
    
    def generate_cost_report(self, report_type, entity_id, start_date, end_date, user_id):
        """
        إنشاء تقرير تكلفة
        
        المعاملات:
            report_type (str): نوع التقرير (crop, nursery, treatment, farm)
            entity_id (int): معرف الكيان
            start_date (str): تاريخ البداية (YYYY-MM-DD)
            end_date (str): تاريخ النهاية (YYYY-MM-DD)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تقرير التكلفة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_cost_reports'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # تحديد جدول التكلفة حسب نوع التقرير
            cost_table = ''
            entity_table = ''
            entity_name_field = ''
            
            if report_type == 'crop':
                cost_table = 'crop_costs'
                entity_table = 'crops'
                entity_name_field = 'name'
            elif report_type == 'nursery':
                cost_table = 'nursery_costs'
                entity_table = 'nurseries'
                entity_name_field = 'name'
            elif report_type == 'treatment':
                cost_table = 'treatment_costs'
                entity_table = 'treatments'
                entity_name_field = 'name'
            elif report_type == 'farm':
                cost_table = 'farm_costs'
                entity_table = 'farms'
                entity_name_field = 'name'
            else:
                return {'success': False, 'message': f'Invalid report type: {report_type}'}
            
            # استعلام عن اسم الكيان
            entity_query = f"""
                SELECT {entity_name_field}
                FROM {entity_table}
                WHERE id = %s
            """
            entity_result = self.db_manager.execute_query(entity_query, (entity_id,))
            
            if not entity_result:
                return {'success': False, 'message': f'{report_type.capitalize()} not found'}
            
            entity_name = entity_result[0][0]
            
            # استعلام عن بيانات التكلفة
            cost_query = f"""
                SELECT date, cost_type, cost, details
                FROM {cost_table}
                WHERE entity_id = %s AND date BETWEEN %s AND %s
                ORDER BY date
            """
            cost_results = self.db_manager.execute_query(cost_query, (entity_id, start_date, end_date))
            
            # تحويل النتائج إلى قائمة من القواميس
            costs = []
            for result in cost_results:
                costs.append({
                    'date': result[0].isoformat() if isinstance(result[0], datetime.date) else result[0],
                    'cost_type': result[1],
                    'cost': result[2],
                    'details': json.loads(result[3]) if result[3] else {}
                })
            
            # حساب إجماليات التكلفة حسب النوع
            cost_by_type = {}
            for cost in costs:
                cost_type = cost['cost_type']
                if cost_type not in cost_by_type:
                    cost_by_type[cost_type] = 0
                cost_by_type[cost_type] += cost['cost']
            
            # حساب التكلفة الإجمالية
            total_cost = sum(cost['cost'] for cost in costs)
            
            # إعداد تقرير التكلفة
            cost_report = {
                'success': True,
                'report_info': {
                    'report_type': report_type,
                    'entity_id': entity_id,
                    'entity_name': entity_name,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    }
                },
                'costs': costs,
                'summary': {
                    'cost_by_type': cost_by_type,
                    'total_cost': total_cost
                },
                'generation_date': datetime.datetime.now().isoformat()
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='generate_cost_report',
                entity_type=report_type,
                entity_id=str(entity_id),
                details=f"Generated cost report for {report_type} {entity_name} from {start_date} to {end_date}"
            )
            
            return cost_report
            
        except Exception as e:
            return {'success': False, 'message': f'Error generating cost report: {str(e)}'}
    
    def export_cost_report(self, report_data, file_format, file_path, user_id):
        """
        تصدير تقرير التكلفة
        
        المعاملات:
            report_data (dict): بيانات التقرير
            file_format (str): صيغة الملف (csv, excel, json)
            file_path (str): مسار الملف
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التصدير
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'export_cost_reports'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من صحة بيانات التقرير
            if not report_data.get('success', False):
                return {'success': False, 'message': 'Invalid report data'}
            
            # تحويل بيانات التكلفة إلى DataFrame
            costs_df = pd.DataFrame(report_data['costs'])
            
            # تصدير التقرير حسب الصيغة المطلوبة
            if file_format == 'csv':
                costs_df.to_csv(file_path, index=False, encoding='utf-8')
            elif file_format == 'excel':
                costs_df.to_excel(file_path, index=False, engine='openpyxl')
            elif file_format == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4)
            else:
                return {'success': False, 'message': f'Invalid file format: {file_format}'}
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='export_cost_report',
                entity_type='cost_report',
                entity_id=f"{report_data['report_info']['report_type']}_{report_data['report_info']['entity_id']}",
                details=f"Exported cost report to {file_path} in {file_format} format"
            )
            
            return {
                'success': True,
                'message': f'Cost report exported successfully to {file_path}',
                'file_path': file_path,
                'file_format': file_format
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error exporting cost report: {str(e)}'}
