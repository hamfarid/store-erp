#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المزارع
===============
هذه الوحدة مسؤولة عن إدارة المزارع، بما في ذلك تتبع المساحات المزروعة،
تواريخ الزراعة والحصاد، مواعيد الري والتسميد، وتكاليف الإنتاج.
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
from ..cost_management.cost_calculator import CostCalculator

# تحميل متغيرات البيئة
load_dotenv()

class FarmManager:
    """مدير إدارة المزارع"""
    
    def __init__(self, db_manager=None, audit_manager=None, auth_manager=None):
        """
        تهيئة مدير إدارة المزارع
        
        المعاملات:
            db_manager (DatabaseManager): مدير قاعدة البيانات
            audit_manager (AuditManager): مدير التدقيق
            auth_manager (AuthManager): مدير المصادقة
        """
        self.db_manager = db_manager or DatabaseManager()
        self.audit_manager = audit_manager or AuditManager()
        self.auth_manager = auth_manager or AuthManager()
        self.cost_calculator = CostCalculator(db_manager, audit_manager, auth_manager)
        
        # تحميل بيانات المزارع
        self.farms = self._load_farms()
        
        # تحميل بيانات المحاصيل
        self.crops = self._load_crops()
    
    def _load_farms(self):
        """
        تحميل بيانات المزارع
        
        العائد:
            dict: بيانات المزارع
        """
        try:
            query = """
                SELECT id, name, location, total_area, owner_id, 
                       creation_date, status
                FROM farms
            """
            results = self.db_manager.execute_query(query)
            
            farms = {}
            for row in results:
                farm_id = row[0]
                farms[farm_id] = {
                    'id': farm_id,
                    'name': row[1],
                    'location': row[2],
                    'total_area': row[3],
                    'owner_id': row[4],
                    'creation_date': row[5],
                    'status': row[6]
                }
            
            return farms
            
        except Exception as e:
            print(f"Error loading farms: {str(e)}")
            return {}
    
    def _load_crops(self):
        """
        تحميل بيانات المحاصيل
        
        العائد:
            dict: بيانات المحاصيل
        """
        try:
            query = """
                SELECT id, name, type, family, growth_duration, 
                       planting_season, harvesting_season
                FROM crops
            """
            results = self.db_manager.execute_query(query)
            
            crops = {}
            for row in results:
                crop_id = row[0]
                crops[crop_id] = {
                    'id': crop_id,
                    'name': row[1],
                    'type': row[2],
                    'family': row[3],
                    'growth_duration': row[4],
                    'planting_season': row[5],
                    'harvesting_season': row[6]
                }
            
            return crops
            
        except Exception as e:
            print(f"Error loading crops: {str(e)}")
            return {}
    
    def create_farm(self, farm_data, user_id):
        """
        إنشاء مزرعة جديدة
        
        المعاملات:
            farm_data (dict): بيانات المزرعة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإنشاء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'create_farm'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات المزرعة
            name = farm_data.get('name', '')
            location = farm_data.get('location', '')
            total_area = farm_data.get('total_area', 0)
            owner_id = farm_data.get('owner_id', user_id)
            status = farm_data.get('status', 'active')
            
            # إدخال بيانات المزرعة
            query = """
                INSERT INTO farms
                (name, location, total_area, owner_id, creation_date, status, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    name, location, total_area, owner_id, 
                    datetime.datetime.now().isoformat(), status, user_id
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to create farm'}
            
            farm_id = result[0][0]
            
            # تحديث قائمة المزارع
            self.farms[farm_id] = {
                'id': farm_id,
                'name': name,
                'location': location,
                'total_area': total_area,
                'owner_id': owner_id,
                'creation_date': datetime.datetime.now().isoformat(),
                'status': status
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='create_farm',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Created new farm: {name}"
            )
            
            return {
                'success': True,
                'farm_id': farm_id,
                'message': 'Farm created successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error creating farm: {str(e)}'}
    
    def update_farm(self, farm_id, farm_data, user_id):
        """
        تحديث بيانات مزرعة
        
        المعاملات:
            farm_id (int): معرف المزرعة
            farm_data (dict): بيانات المزرعة المحدثة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التحديث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'update_farm'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # استخراج بيانات المزرعة
            name = farm_data.get('name', self.farms[farm_id]['name'])
            location = farm_data.get('location', self.farms[farm_id]['location'])
            total_area = farm_data.get('total_area', self.farms[farm_id]['total_area'])
            owner_id = farm_data.get('owner_id', self.farms[farm_id]['owner_id'])
            status = farm_data.get('status', self.farms[farm_id]['status'])
            
            # تحديث بيانات المزرعة
            query = """
                UPDATE farms
                SET name = %s, location = %s, total_area = %s, owner_id = %s, 
                    status = %s, updated_at = %s, updated_by = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                query, 
                (
                    name, location, total_area, owner_id, status, 
                    datetime.datetime.now().isoformat(), user_id, farm_id
                )
            )
            
            # تحديث قائمة المزارع
            self.farms[farm_id].update({
                'name': name,
                'location': location,
                'total_area': total_area,
                'owner_id': owner_id,
                'status': status
            })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='update_farm',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Updated farm: {name}"
            )
            
            return {
                'success': True,
                'farm_id': farm_id,
                'message': 'Farm updated successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error updating farm: {str(e)}'}
    
    def get_farm(self, farm_id, user_id):
        """
        الحصول على بيانات مزرعة
        
        المعاملات:
            farm_id (int): معرف المزرعة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: بيانات المزرعة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_farm'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # الحصول على بيانات المزرعة
            farm = self.farms[farm_id]
            
            # الحصول على بيانات الزراعات في المزرعة
            plantings_query = """
                SELECT id, crop_id, area, planting_date, expected_harvest_date, 
                       status, notes
                FROM farm_plantings
                WHERE farm_id = %s
                ORDER BY planting_date DESC
            """
            plantings_result = self.db_manager.execute_query(plantings_query, (farm_id,))
            
            plantings = []
            for row in plantings_result:
                planting_id = row[0]
                crop_id = row[1]
                
                # الحصول على بيانات المحصول
                crop_name = self.crops.get(crop_id, {}).get('name', 'Unknown')
                
                # الحصول على بيانات الحصاد
                harvests_query = """
                    SELECT id, harvest_date, yield_amount, yield_unit, quality_rating, notes
                    FROM farm_harvests
                    WHERE planting_id = %s
                    ORDER BY harvest_date
                """
                harvests_result = self.db_manager.execute_query(harvests_query, (planting_id,))
                
                harvests = []
                for harvest_row in harvests_result:
                    harvests.append({
                        'id': harvest_row[0],
                        'harvest_date': harvest_row[1],
                        'yield_amount': harvest_row[2],
                        'yield_unit': harvest_row[3],
                        'quality_rating': harvest_row[4],
                        'notes': harvest_row[5]
                    })
                
                plantings.append({
                    'id': planting_id,
                    'crop_id': crop_id,
                    'crop_name': crop_name,
                    'area': row[2],
                    'planting_date': row[3],
                    'expected_harvest_date': row[4],
                    'status': row[5],
                    'notes': row[6],
                    'harvests': harvests
                })
            
            # الحصول على بيانات الري
            irrigation_query = """
                SELECT id, planting_id, irrigation_date, water_amount, 
                       irrigation_type, duration, notes
                FROM farm_irrigations
                WHERE farm_id = %s
                ORDER BY irrigation_date DESC
                LIMIT 100
            """
            irrigation_result = self.db_manager.execute_query(irrigation_query, (farm_id,))
            
            irrigations = []
            for row in irrigation_result:
                irrigations.append({
                    'id': row[0],
                    'planting_id': row[1],
                    'irrigation_date': row[2],
                    'water_amount': row[3],
                    'irrigation_type': row[4],
                    'duration': row[5],
                    'notes': row[6]
                })
            
            # الحصول على بيانات التسميد
            fertilization_query = """
                SELECT id, planting_id, fertilization_date, fertilizer_id, 
                       fertilizer_name, amount, application_method, notes
                FROM farm_fertilizations
                WHERE farm_id = %s
                ORDER BY fertilization_date DESC
                LIMIT 100
            """
            fertilization_result = self.db_manager.execute_query(fertilization_query, (farm_id,))
            
            fertilizations = []
            for row in fertilization_result:
                fertilizations.append({
                    'id': row[0],
                    'planting_id': row[1],
                    'fertilization_date': row[2],
                    'fertilizer_id': row[3],
                    'fertilizer_name': row[4],
                    'amount': row[5],
                    'application_method': row[6],
                    'notes': row[7]
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_farm',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Viewed farm: {farm['name']}"
            )
            
            return {
                'success': True,
                'farm': farm,
                'plantings': plantings,
                'irrigations': irrigations,
                'fertilizations': fertilizations
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting farm: {str(e)}'}
    
    def list_farms(self, filters, user_id):
        """
        الحصول على قائمة المزارع
        
        المعاملات:
            filters (dict): معايير التصفية
            user_id (int): معرف المستخدم
            
        العائد:
            dict: قائمة المزارع
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'list_farms'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج معايير التصفية
            owner_id = filters.get('owner_id')
            status = filters.get('status')
            location = filters.get('location')
            
            # بناء استعلام قائمة المزارع
            query = "SELECT id, name, location, total_area, owner_id, creation_date, status FROM farms WHERE 1=1"
            params = []
            
            if owner_id:
                query += " AND owner_id = %s"
                params.append(owner_id)
            
            if status:
                query += " AND status = %s"
                params.append(status)
            
            if location:
                query += " AND location LIKE %s"
                params.append(f"%{location}%")
            
            query += " ORDER BY name"
            
            # تنفيذ الاستعلام
            results = self.db_manager.execute_query(query, tuple(params))
            
            # تحضير قائمة المزارع
            farms = []
            for row in results:
                farms.append({
                    'id': row[0],
                    'name': row[1],
                    'location': row[2],
                    'total_area': row[3],
                    'owner_id': row[4],
                    'creation_date': row[5],
                    'status': row[6]
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='list_farms',
                entity_type='farms',
                entity_id='all',
                details=f"Listed farms with filters: {json.dumps(filters)}"
            )
            
            return {
                'success': True,
                'farms': farms,
                'count': len(farms)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error listing farms: {str(e)}'}
    
    def add_planting(self, planting_data, user_id):
        """
        إضافة زراعة جديدة
        
        المعاملات:
            planting_data (dict): بيانات الزراعة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_planting'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات الزراعة
            farm_id = planting_data.get('farm_id')
            crop_id = planting_data.get('crop_id')
            area = planting_data.get('area', 0)
            planting_date = planting_data.get('planting_date')
            expected_harvest_date = planting_data.get('expected_harvest_date')
            status = planting_data.get('status', 'active')
            notes = planting_data.get('notes', '')
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # التحقق من وجود المحصول
            if crop_id not in self.crops:
                return {'success': False, 'message': 'Crop not found'}
            
            # التحقق من المساحة المتاحة
            farm_area = self.farms[farm_id]['total_area']
            
            # حساب المساحة المزروعة حالياً
            planted_area_query = """
                SELECT SUM(area)
                FROM farm_plantings
                WHERE farm_id = %s AND status = 'active'
            """
            planted_area_result = self.db_manager.execute_query(planted_area_query, (farm_id,))
            
            planted_area = planted_area_result[0][0] if planted_area_result[0][0] else 0
            
            # التحقق من توفر المساحة
            if planted_area + area > farm_area:
                return {
                    'success': False, 
                    'message': f'Insufficient area. Available: {farm_area - planted_area}, Requested: {area}'
                }
            
            # إدخال بيانات الزراعة
            query = """
                INSERT INTO farm_plantings
                (farm_id, crop_id, area, planting_date, expected_harvest_date, 
                 status, notes, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    farm_id, crop_id, area, planting_date, expected_harvest_date, 
                    status, notes, user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add planting'}
            
            planting_id = result[0][0]
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_planting',
                entity_type='planting',
                entity_id=str(planting_id),
                details=f"Added planting of crop {crop_id} in farm {farm_id}"
            )
            
            return {
                'success': True,
                'planting_id': planting_id,
                'message': 'Planting added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding planting: {str(e)}'}
    
    def update_planting(self, planting_id, planting_data, user_id):
        """
        تحديث بيانات زراعة
        
        المعاملات:
            planting_id (int): معرف الزراعة
            planting_data (dict): بيانات الزراعة المحدثة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التحديث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'update_planting'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود الزراعة
            planting_query = """
                SELECT farm_id, crop_id, area, planting_date, expected_harvest_date, 
                       status, notes
                FROM farm_plantings
                WHERE id = %s
            """
            planting_result = self.db_manager.execute_query(planting_query, (planting_id,))
            
            if not planting_result:
                return {'success': False, 'message': 'Planting not found'}
            
            # استخراج بيانات الزراعة الحالية
            current_farm_id = planting_result[0][0]
            current_crop_id = planting_result[0][1]
            current_area = planting_result[0][2]
            current_planting_date = planting_result[0][3]
            current_expected_harvest_date = planting_result[0][4]
            current_status = planting_result[0][5]
            current_notes = planting_result[0][6]
            
            # استخراج بيانات الزراعة المحدثة
            farm_id = planting_data.get('farm_id', current_farm_id)
            crop_id = planting_data.get('crop_id', current_crop_id)
            area = planting_data.get('area', current_area)
            planting_date = planting_data.get('planting_date', current_planting_date)
            expected_harvest_date = planting_data.get('expected_harvest_date', current_expected_harvest_date)
            status = planting_data.get('status', current_status)
            notes = planting_data.get('notes', current_notes)
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # التحقق من وجود المحصول
            if crop_id not in self.crops:
                return {'success': False, 'message': 'Crop not found'}
            
            # التحقق من المساحة المتاحة إذا تم تغيير المزرعة أو المساحة
            if farm_id != current_farm_id or area > current_area:
                farm_area = self.farms[farm_id]['total_area']
                
                # حساب المساحة المزروعة حالياً
                planted_area_query = """
                    SELECT SUM(area)
                    FROM farm_plantings
                    WHERE farm_id = %s AND status = 'active' AND id != %s
                """
                planted_area_result = self.db_manager.execute_query(planted_area_query, (farm_id, planting_id))
                
                planted_area = planted_area_result[0][0] if planted_area_result[0][0] else 0
                
                # التحقق من توفر المساحة
                if planted_area + area > farm_area:
                    return {
                        'success': False, 
                        'message': f'Insufficient area. Available: {farm_area - planted_area}, Requested: {area}'
                    }
            
            # تحديث بيانات الزراعة
            query = """
                UPDATE farm_plantings
                SET farm_id = %s, crop_id = %s, area = %s, planting_date = %s, 
                    expected_harvest_date = %s, status = %s, notes = %s, 
                    updated_by = %s, updated_at = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                query, 
                (
                    farm_id, crop_id, area, planting_date, expected_harvest_date, 
                    status, notes, user_id, datetime.datetime.now().isoformat(), planting_id
                )
            )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='update_planting',
                entity_type='planting',
                entity_id=str(planting_id),
                details=f"Updated planting {planting_id}"
            )
            
            return {
                'success': True,
                'planting_id': planting_id,
                'message': 'Planting updated successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error updating planting: {str(e)}'}
    
    def add_harvest(self, harvest_data, user_id):
        """
        إضافة حصاد جديد
        
        المعاملات:
            harvest_data (dict): بيانات الحصاد
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_harvest'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات الحصاد
            planting_id = harvest_data.get('planting_id')
            harvest_date = harvest_data.get('harvest_date')
            yield_amount = harvest_data.get('yield_amount', 0)
            yield_unit = harvest_data.get('yield_unit', 'kg')
            quality_rating = harvest_data.get('quality_rating', 0)
            notes = harvest_data.get('notes', '')
            
            # التحقق من وجود الزراعة
            planting_query = """
                SELECT farm_id, crop_id, status
                FROM farm_plantings
                WHERE id = %s
            """
            planting_result = self.db_manager.execute_query(planting_query, (planting_id,))
            
            if not planting_result:
                return {'success': False, 'message': 'Planting not found'}
            
            farm_id = planting_result[0][0]
            crop_id = planting_result[0][1]
            planting_status = planting_result[0][2]
            
            # التحقق من حالة الزراعة
            if planting_status != 'active':
                return {'success': False, 'message': 'Cannot add harvest to inactive planting'}
            
            # إدخال بيانات الحصاد
            query = """
                INSERT INTO farm_harvests
                (planting_id, farm_id, crop_id, harvest_date, yield_amount, 
                 yield_unit, quality_rating, notes, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    planting_id, farm_id, crop_id, harvest_date, yield_amount, 
                    yield_unit, quality_rating, notes, user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add harvest'}
            
            harvest_id = result[0][0]
            
            # تحديث حالة الزراعة إذا كان هذا الحصاد النهائي
            if harvest_data.get('is_final', False):
                update_query = """
                    UPDATE farm_plantings
                    SET status = 'harvested', updated_by = %s, updated_at = %s
                    WHERE id = %s
                """
                self.db_manager.execute_query(
                    update_query, 
                    (user_id, datetime.datetime.now().isoformat(), planting_id)
                )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_harvest',
                entity_type='harvest',
                entity_id=str(harvest_id),
                details=f"Added harvest for planting {planting_id}"
            )
            
            return {
                'success': True,
                'harvest_id': harvest_id,
                'message': 'Harvest added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding harvest: {str(e)}'}
    
    def add_irrigation(self, irrigation_data, user_id):
        """
        إضافة ري جديد
        
        المعاملات:
            irrigation_data (dict): بيانات الري
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_irrigation'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات الري
            farm_id = irrigation_data.get('farm_id')
            planting_id = irrigation_data.get('planting_id')
            irrigation_date = irrigation_data.get('irrigation_date')
            water_amount = irrigation_data.get('water_amount', 0)
            irrigation_type = irrigation_data.get('irrigation_type', 'drip')
            duration = irrigation_data.get('duration', 0)
            notes = irrigation_data.get('notes', '')
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # التحقق من وجود الزراعة إذا تم تحديدها
            if planting_id:
                planting_query = """
                    SELECT farm_id, status
                    FROM farm_plantings
                    WHERE id = %s
                """
                planting_result = self.db_manager.execute_query(planting_query, (planting_id,))
                
                if not planting_result:
                    return {'success': False, 'message': 'Planting not found'}
                
                planting_farm_id = planting_result[0][0]
                planting_status = planting_result[0][1]
                
                # التحقق من تطابق المزرعة
                if planting_farm_id != farm_id:
                    return {'success': False, 'message': 'Planting does not belong to the specified farm'}
                
                # التحقق من حالة الزراعة
                if planting_status != 'active':
                    return {'success': False, 'message': 'Cannot add irrigation to inactive planting'}
            
            # إدخال بيانات الري
            query = """
                INSERT INTO farm_irrigations
                (farm_id, planting_id, irrigation_date, water_amount, 
                 irrigation_type, duration, notes, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    farm_id, planting_id, irrigation_date, water_amount, 
                    irrigation_type, duration, notes, user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add irrigation'}
            
            irrigation_id = result[0][0]
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_irrigation',
                entity_type='irrigation',
                entity_id=str(irrigation_id),
                details=f"Added irrigation for farm {farm_id}" + (f", planting {planting_id}" if planting_id else "")
            )
            
            return {
                'success': True,
                'irrigation_id': irrigation_id,
                'message': 'Irrigation added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding irrigation: {str(e)}'}
    
    def add_fertilization(self, fertilization_data, user_id):
        """
        إضافة تسميد جديد
        
        المعاملات:
            fertilization_data (dict): بيانات التسميد
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_fertilization'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات التسميد
            farm_id = fertilization_data.get('farm_id')
            planting_id = fertilization_data.get('planting_id')
            fertilization_date = fertilization_data.get('fertilization_date')
            fertilizer_id = fertilization_data.get('fertilizer_id')
            fertilizer_name = fertilization_data.get('fertilizer_name', '')
            amount = fertilization_data.get('amount', 0)
            application_method = fertilization_data.get('application_method', 'broadcast')
            notes = fertilization_data.get('notes', '')
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # التحقق من وجود الزراعة إذا تم تحديدها
            if planting_id:
                planting_query = """
                    SELECT farm_id, status
                    FROM farm_plantings
                    WHERE id = %s
                """
                planting_result = self.db_manager.execute_query(planting_query, (planting_id,))
                
                if not planting_result:
                    return {'success': False, 'message': 'Planting not found'}
                
                planting_farm_id = planting_result[0][0]
                planting_status = planting_result[0][1]
                
                # التحقق من تطابق المزرعة
                if planting_farm_id != farm_id:
                    return {'success': False, 'message': 'Planting does not belong to the specified farm'}
                
                # التحقق من حالة الزراعة
                if planting_status != 'active':
                    return {'success': False, 'message': 'Cannot add fertilization to inactive planting'}
            
            # إدخال بيانات التسميد
            query = """
                INSERT INTO farm_fertilizations
                (farm_id, planting_id, fertilization_date, fertilizer_id, 
                 fertilizer_name, amount, application_method, notes, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    farm_id, planting_id, fertilization_date, fertilizer_id, 
                    fertilizer_name, amount, application_method, notes, 
                    user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add fertilization'}
            
            fertilization_id = result[0][0]
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_fertilization',
                entity_type='fertilization',
                entity_id=str(fertilization_id),
                details=f"Added fertilization for farm {farm_id}" + (f", planting {planting_id}" if planting_id else "")
            )
            
            return {
                'success': True,
                'fertilization_id': fertilization_id,
                'message': 'Fertilization added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding fertilization: {str(e)}'}
    
    def get_farm_schedule(self, farm_id, start_date, end_date, user_id):
        """
        الحصول على جدول المزرعة
        
        المعاملات:
            farm_id (int): معرف المزرعة
            start_date (str): تاريخ البداية (YYYY-MM-DD)
            end_date (str): تاريخ النهاية (YYYY-MM-DD)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: جدول المزرعة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_farm_schedule'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # الحصول على بيانات الزراعات
            plantings_query = """
                SELECT id, crop_id, area, planting_date, expected_harvest_date, status
                FROM farm_plantings
                WHERE farm_id = %s AND 
                      (planting_date BETWEEN %s AND %s OR 
                       expected_harvest_date BETWEEN %s AND %s OR
                       (planting_date <= %s AND expected_harvest_date >= %s))
            """
            plantings_result = self.db_manager.execute_query(
                plantings_query, 
                (farm_id, start_date, end_date, start_date, end_date, start_date, end_date)
            )
            
            plantings = []
            for row in plantings_result:
                planting_id = row[0]
                crop_id = row[1]
                
                # الحصول على بيانات المحصول
                crop_name = self.crops.get(crop_id, {}).get('name', 'Unknown')
                
                plantings.append({
                    'id': planting_id,
                    'crop_id': crop_id,
                    'crop_name': crop_name,
                    'area': row[2],
                    'planting_date': row[3],
                    'expected_harvest_date': row[4],
                    'status': row[5],
                    'event_type': 'planting'
                })
            
            # الحصول على بيانات الحصاد
            harvests_query = """
                SELECT h.id, h.planting_id, p.crop_id, h.harvest_date, h.yield_amount, h.yield_unit
                FROM farm_harvests h
                JOIN farm_plantings p ON h.planting_id = p.id
                WHERE h.farm_id = %s AND h.harvest_date BETWEEN %s AND %s
            """
            harvests_result = self.db_manager.execute_query(
                harvests_query, 
                (farm_id, start_date, end_date)
            )
            
            harvests = []
            for row in harvests_result:
                harvest_id = row[0]
                planting_id = row[1]
                crop_id = row[2]
                
                # الحصول على بيانات المحصول
                crop_name = self.crops.get(crop_id, {}).get('name', 'Unknown')
                
                harvests.append({
                    'id': harvest_id,
                    'planting_id': planting_id,
                    'crop_id': crop_id,
                    'crop_name': crop_name,
                    'harvest_date': row[3],
                    'yield_amount': row[4],
                    'yield_unit': row[5],
                    'event_type': 'harvest'
                })
            
            # الحصول على بيانات الري
            irrigations_query = """
                SELECT id, planting_id, irrigation_date, water_amount, irrigation_type
                FROM farm_irrigations
                WHERE farm_id = %s AND irrigation_date BETWEEN %s AND %s
            """
            irrigations_result = self.db_manager.execute_query(
                irrigations_query, 
                (farm_id, start_date, end_date)
            )
            
            irrigations = []
            for row in irrigations_result:
                irrigations.append({
                    'id': row[0],
                    'planting_id': row[1],
                    'irrigation_date': row[2],
                    'water_amount': row[3],
                    'irrigation_type': row[4],
                    'event_type': 'irrigation'
                })
            
            # الحصول على بيانات التسميد
            fertilizations_query = """
                SELECT id, planting_id, fertilization_date, fertilizer_name, amount
                FROM farm_fertilizations
                WHERE farm_id = %s AND fertilization_date BETWEEN %s AND %s
            """
            fertilizations_result = self.db_manager.execute_query(
                fertilizations_query, 
                (farm_id, start_date, end_date)
            )
            
            fertilizations = []
            for row in fertilizations_result:
                fertilizations.append({
                    'id': row[0],
                    'planting_id': row[1],
                    'fertilization_date': row[2],
                    'fertilizer_name': row[3],
                    'amount': row[4],
                    'event_type': 'fertilization'
                })
            
            # دمج جميع الأحداث وترتيبها حسب التاريخ
            all_events = []
            
            for planting in plantings:
                all_events.append({
                    'date': planting['planting_date'],
                    'event_type': 'planting',
                    'event_id': planting['id'],
                    'details': planting
                })
                
                all_events.append({
                    'date': planting['expected_harvest_date'],
                    'event_type': 'expected_harvest',
                    'event_id': planting['id'],
                    'details': planting
                })
            
            for harvest in harvests:
                all_events.append({
                    'date': harvest['harvest_date'],
                    'event_type': 'harvest',
                    'event_id': harvest['id'],
                    'details': harvest
                })
            
            for irrigation in irrigations:
                all_events.append({
                    'date': irrigation['irrigation_date'],
                    'event_type': 'irrigation',
                    'event_id': irrigation['id'],
                    'details': irrigation
                })
            
            for fertilization in fertilizations:
                all_events.append({
                    'date': fertilization['fertilization_date'],
                    'event_type': 'fertilization',
                    'event_id': fertilization['id'],
                    'details': fertilization
                })
            
            # ترتيب الأحداث حسب التاريخ
            all_events.sort(key=lambda x: x['date'])
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_farm_schedule',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Viewed schedule for farm {farm_id} from {start_date} to {end_date}"
            )
            
            return {
                'success': True,
                'farm_id': farm_id,
                'farm_name': self.farms[farm_id]['name'],
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'events': all_events,
                'event_counts': {
                    'plantings': len(plantings),
                    'harvests': len(harvests),
                    'irrigations': len(irrigations),
                    'fertilizations': len(fertilizations),
                    'total': len(all_events)
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting farm schedule: {str(e)}'}
    
    def get_farm_statistics(self, farm_id, year, user_id):
        """
        الحصول على إحصائيات المزرعة
        
        المعاملات:
            farm_id (int): معرف المزرعة
            year (int): السنة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: إحصائيات المزرعة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_farm_statistics'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # تحديد نطاق التاريخ
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            
            # الحصول على إحصائيات الزراعات
            plantings_query = """
                SELECT COUNT(*), SUM(area)
                FROM farm_plantings
                WHERE farm_id = %s AND planting_date BETWEEN %s AND %s
            """
            plantings_result = self.db_manager.execute_query(
                plantings_query, 
                (farm_id, start_date, end_date)
            )
            
            plantings_count = plantings_result[0][0] if plantings_result[0][0] else 0
            planted_area = plantings_result[0][1] if plantings_result[0][1] else 0
            
            # الحصول على إحصائيات المحاصيل المزروعة
            crops_query = """
                SELECT crop_id, SUM(area)
                FROM farm_plantings
                WHERE farm_id = %s AND planting_date BETWEEN %s AND %s
                GROUP BY crop_id
            """
            crops_result = self.db_manager.execute_query(
                crops_query, 
                (farm_id, start_date, end_date)
            )
            
            crops_data = []
            for row in crops_result:
                crop_id = row[0]
                crop_area = row[1]
                
                # الحصول على بيانات المحصول
                crop_name = self.crops.get(crop_id, {}).get('name', 'Unknown')
                
                crops_data.append({
                    'crop_id': crop_id,
                    'crop_name': crop_name,
                    'area': crop_area
                })
            
            # الحصول على إحصائيات الحصاد
            harvests_query = """
                SELECT COUNT(*), SUM(yield_amount)
                FROM farm_harvests
                WHERE farm_id = %s AND harvest_date BETWEEN %s AND %s
            """
            harvests_result = self.db_manager.execute_query(
                harvests_query, 
                (farm_id, start_date, end_date)
            )
            
            harvests_count = harvests_result[0][0] if harvests_result[0][0] else 0
            total_yield = harvests_result[0][1] if harvests_result[0][1] else 0
            
            # الحصول على إحصائيات الحصاد حسب المحصول
            crop_yields_query = """
                SELECT h.crop_id, SUM(h.yield_amount), h.yield_unit
                FROM farm_harvests h
                WHERE h.farm_id = %s AND h.harvest_date BETWEEN %s AND %s
                GROUP BY h.crop_id, h.yield_unit
            """
            crop_yields_result = self.db_manager.execute_query(
                crop_yields_query, 
                (farm_id, start_date, end_date)
            )
            
            crop_yields = []
            for row in crop_yields_result:
                crop_id = row[0]
                crop_yield = row[1]
                yield_unit = row[2]
                
                # الحصول على بيانات المحصول
                crop_name = self.crops.get(crop_id, {}).get('name', 'Unknown')
                
                crop_yields.append({
                    'crop_id': crop_id,
                    'crop_name': crop_name,
                    'yield': crop_yield,
                    'unit': yield_unit
                })
            
            # الحصول على إحصائيات الري
            irrigation_query = """
                SELECT COUNT(*), SUM(water_amount)
                FROM farm_irrigations
                WHERE farm_id = %s AND irrigation_date BETWEEN %s AND %s
            """
            irrigation_result = self.db_manager.execute_query(
                irrigation_query, 
                (farm_id, start_date, end_date)
            )
            
            irrigation_count = irrigation_result[0][0] if irrigation_result[0][0] else 0
            total_water = irrigation_result[0][1] if irrigation_result[0][1] else 0
            
            # الحصول على إحصائيات التسميد
            fertilization_query = """
                SELECT COUNT(*), SUM(amount)
                FROM farm_fertilizations
                WHERE farm_id = %s AND fertilization_date BETWEEN %s AND %s
            """
            fertilization_result = self.db_manager.execute_query(
                fertilization_query, 
                (farm_id, start_date, end_date)
            )
            
            fertilization_count = fertilization_result[0][0] if fertilization_result[0][0] else 0
            total_fertilizer = fertilization_result[0][1] if fertilization_result[0][1] else 0
            
            # الحصول على إحصائيات التكلفة
            cost_result = self.cost_calculator.calculate_total_farm_cost(
                farm_id, start_date, end_date, user_id
            )
            
            total_cost = cost_result.get('costs', {}).get('total', 0) if cost_result.get('success', False) else 0
            cost_per_acre = cost_result.get('metrics', {}).get('cost_per_acre', 0) if cost_result.get('success', False) else 0
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_farm_statistics',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Viewed statistics for farm {farm_id} for year {year}"
            )
            
            return {
                'success': True,
                'farm_id': farm_id,
                'farm_name': self.farms[farm_id]['name'],
                'year': year,
                'plantings': {
                    'count': plantings_count,
                    'total_area': planted_area,
                    'crops': crops_data
                },
                'harvests': {
                    'count': harvests_count,
                    'total_yield': total_yield,
                    'crop_yields': crop_yields
                },
                'irrigation': {
                    'count': irrigation_count,
                    'total_water': total_water
                },
                'fertilization': {
                    'count': fertilization_count,
                    'total_fertilizer': total_fertilizer
                },
                'costs': {
                    'total_cost': total_cost,
                    'cost_per_acre': cost_per_acre
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting farm statistics: {str(e)}'}
    
    def generate_farm_report(self, farm_id, start_date, end_date, report_type, user_id):
        """
        إنشاء تقرير للمزرعة
        
        المعاملات:
            farm_id (int): معرف المزرعة
            start_date (str): تاريخ البداية (YYYY-MM-DD)
            end_date (str): تاريخ النهاية (YYYY-MM-DD)
            report_type (str): نوع التقرير (summary, detailed, financial)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تقرير المزرعة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'generate_farm_report'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المزرعة
            if farm_id not in self.farms:
                return {'success': False, 'message': 'Farm not found'}
            
            # الحصول على بيانات المزرعة
            farm = self.farms[farm_id]
            
            # إنشاء التقرير حسب النوع
            if report_type == 'summary':
                # الحصول على ملخص الزراعات
                plantings_query = """
                    SELECT COUNT(*), SUM(area)
                    FROM farm_plantings
                    WHERE farm_id = %s AND planting_date BETWEEN %s AND %s
                """
                plantings_result = self.db_manager.execute_query(
                    plantings_query, 
                    (farm_id, start_date, end_date)
                )
                
                plantings_count = plantings_result[0][0] if plantings_result[0][0] else 0
                planted_area = plantings_result[0][1] if plantings_result[0][1] else 0
                
                # الحصول على ملخص الحصاد
                harvests_query = """
                    SELECT COUNT(*), SUM(yield_amount)
                    FROM farm_harvests
                    WHERE farm_id = %s AND harvest_date BETWEEN %s AND %s
                """
                harvests_result = self.db_manager.execute_query(
                    harvests_query, 
                    (farm_id, start_date, end_date)
                )
                
                harvests_count = harvests_result[0][0] if harvests_result[0][0] else 0
                total_yield = harvests_result[0][1] if harvests_result[0][1] else 0
                
                # الحصول على ملخص الري
                irrigation_query = """
                    SELECT COUNT(*), SUM(water_amount)
                    FROM farm_irrigations
                    WHERE farm_id = %s AND irrigation_date BETWEEN %s AND %s
                """
                irrigation_result = self.db_manager.execute_query(
                    irrigation_query, 
                    (farm_id, start_date, end_date)
                )
                
                irrigation_count = irrigation_result[0][0] if irrigation_result[0][0] else 0
                total_water = irrigation_result[0][1] if irrigation_result[0][1] else 0
                
                # الحصول على ملخص التسميد
                fertilization_query = """
                    SELECT COUNT(*), SUM(amount)
                    FROM farm_fertilizations
                    WHERE farm_id = %s AND fertilization_date BETWEEN %s AND %s
                """
                fertilization_result = self.db_manager.execute_query(
                    fertilization_query, 
                    (farm_id, start_date, end_date)
                )
                
                fertilization_count = fertilization_result[0][0] if fertilization_result[0][0] else 0
                total_fertilizer = fertilization_result[0][1] if fertilization_result[0][1] else 0
                
                # إعداد التقرير
                report = {
                    'farm': farm,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    },
                    'summary': {
                        'plantings': {
                            'count': plantings_count,
                            'total_area': planted_area
                        },
                        'harvests': {
                            'count': harvests_count,
                            'total_yield': total_yield
                        },
                        'irrigation': {
                            'count': irrigation_count,
                            'total_water': total_water
                        },
                        'fertilization': {
                            'count': fertilization_count,
                            'total_fertilizer': total_fertilizer
                        }
                    }
                }
                
            elif report_type == 'detailed':
                # الحصول على تفاصيل الزراعات
                plantings_query = """
                    SELECT id, crop_id, area, planting_date, expected_harvest_date, 
                           status, notes
                    FROM farm_plantings
                    WHERE farm_id = %s AND planting_date BETWEEN %s AND %s
                    ORDER BY planting_date
                """
                plantings_result = self.db_manager.execute_query(
                    plantings_query, 
                    (farm_id, start_date, end_date)
                )
                
                plantings = []
                for row in plantings_result:
                    planting_id = row[0]
                    crop_id = row[1]
                    
                    # الحصول على بيانات المحصول
                    crop_name = self.crops.get(crop_id, {}).get('name', 'Unknown')
                    
                    # الحصول على بيانات الحصاد
                    harvests_query = """
                        SELECT id, harvest_date, yield_amount, yield_unit, quality_rating, notes
                        FROM farm_harvests
                        WHERE planting_id = %s
                        ORDER BY harvest_date
                    """
                    harvests_result = self.db_manager.execute_query(harvests_query, (planting_id,))
                    
                    harvests = []
                    for harvest_row in harvests_result:
                        harvests.append({
                            'id': harvest_row[0],
                            'harvest_date': harvest_row[1],
                            'yield_amount': harvest_row[2],
                            'yield_unit': harvest_row[3],
                            'quality_rating': harvest_row[4],
                            'notes': harvest_row[5]
                        })
                    
                    plantings.append({
                        'id': planting_id,
                        'crop_id': crop_id,
                        'crop_name': crop_name,
                        'area': row[2],
                        'planting_date': row[3],
                        'expected_harvest_date': row[4],
                        'status': row[5],
                        'notes': row[6],
                        'harvests': harvests
                    })
                
                # الحصول على تفاصيل الري
                irrigation_query = """
                    SELECT id, planting_id, irrigation_date, water_amount, 
                           irrigation_type, duration, notes
                    FROM farm_irrigations
                    WHERE farm_id = %s AND irrigation_date BETWEEN %s AND %s
                    ORDER BY irrigation_date
                """
                irrigation_result = self.db_manager.execute_query(
                    irrigation_query, 
                    (farm_id, start_date, end_date)
                )
                
                irrigations = []
                for row in irrigation_result:
                    irrigations.append({
                        'id': row[0],
                        'planting_id': row[1],
                        'irrigation_date': row[2],
                        'water_amount': row[3],
                        'irrigation_type': row[4],
                        'duration': row[5],
                        'notes': row[6]
                    })
                
                # الحصول على تفاصيل التسميد
                fertilization_query = """
                    SELECT id, planting_id, fertilization_date, fertilizer_id, 
                           fertilizer_name, amount, application_method, notes
                    FROM farm_fertilizations
                    WHERE farm_id = %s AND fertilization_date BETWEEN %s AND %s
                    ORDER BY fertilization_date
                """
                fertilization_result = self.db_manager.execute_query(
                    fertilization_query, 
                    (farm_id, start_date, end_date)
                )
                
                fertilizations = []
                for row in fertilization_result:
                    fertilizations.append({
                        'id': row[0],
                        'planting_id': row[1],
                        'fertilization_date': row[2],
                        'fertilizer_id': row[3],
                        'fertilizer_name': row[4],
                        'amount': row[5],
                        'application_method': row[6],
                        'notes': row[7]
                    })
                
                # إعداد التقرير
                report = {
                    'farm': farm,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    },
                    'details': {
                        'plantings': plantings,
                        'irrigations': irrigations,
                        'fertilizations': fertilizations
                    }
                }
                
            elif report_type == 'financial':
                # الحصول على التقرير المالي
                cost_result = self.cost_calculator.calculate_total_farm_cost(
                    farm_id, start_date, end_date, user_id
                )
                
                if not cost_result.get('success', False):
                    return {'success': False, 'message': 'Failed to generate financial report'}
                
                # إعداد التقرير
                report = {
                    'farm': farm,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    },
                    'financial': cost_result
                }
                
            else:
                return {'success': False, 'message': f'Invalid report type: {report_type}'}
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='generate_farm_report',
                entity_type='farm',
                entity_id=str(farm_id),
                details=f"Generated {report_type} report for farm {farm_id} from {start_date} to {end_date}"
            )
            
            return {
                'success': True,
                'report_type': report_type,
                'report': report,
                'generation_date': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error generating farm report: {str(e)}'}
    
    def export_farm_report(self, report_data, file_format, file_path, user_id):
        """
        تصدير تقرير المزرعة
        
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
            if not self.auth_manager.has_permission(user_id, 'export_farm_report'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من صحة بيانات التقرير
            if not report_data.get('success', False):
                return {'success': False, 'message': 'Invalid report data'}
            
            report_type = report_data.get('report_type')
            report = report_data.get('report', {})
            
            if report_type == 'summary':
                # تصدير تقرير الملخص
                summary = report.get('summary', {})
                
                # تحويل البيانات إلى DataFrame
                summary_data = {
                    'Category': ['Plantings', 'Harvests', 'Irrigation', 'Fertilization'],
                    'Count': [
                        summary.get('plantings', {}).get('count', 0),
                        summary.get('harvests', {}).get('count', 0),
                        summary.get('irrigation', {}).get('count', 0),
                        summary.get('fertilization', {}).get('count', 0)
                    ],
                    'Total': [
                        summary.get('plantings', {}).get('total_area', 0),
                        summary.get('harvests', {}).get('total_yield', 0),
                        summary.get('irrigation', {}).get('total_water', 0),
                        summary.get('fertilization', {}).get('total_fertilizer', 0)
                    ],
                    'Unit': ['acres', 'kg', 'm³', 'kg']
                }
                
                df = pd.DataFrame(summary_data)
                
                # تصدير التقرير حسب الصيغة المطلوبة
                if file_format == 'csv':
                    df.to_csv(file_path, index=False, encoding='utf-8')
                elif file_format == 'excel':
                    df.to_excel(file_path, index=False, engine='openpyxl')
                elif file_format == 'json':
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(report_data, f, ensure_ascii=False, indent=4)
                else:
                    return {'success': False, 'message': f'Invalid file format: {file_format}'}
                
            elif report_type == 'detailed':
                # تصدير تقرير التفاصيل
                details = report.get('details', {})
                
                # تحويل بيانات الزراعات إلى DataFrame
                plantings = details.get('plantings', [])
                plantings_data = []
                
                for planting in plantings:
                    plantings_data.append({
                        'ID': planting.get('id'),
                        'Crop': planting.get('crop_name'),
                        'Area': planting.get('area'),
                        'Planting Date': planting.get('planting_date'),
                        'Expected Harvest Date': planting.get('expected_harvest_date'),
                        'Status': planting.get('status'),
                        'Notes': planting.get('notes')
                    })
                
                plantings_df = pd.DataFrame(plantings_data)
                
                # تحويل بيانات الري إلى DataFrame
                irrigations = details.get('irrigations', [])
                irrigations_data = []
                
                for irrigation in irrigations:
                    irrigations_data.append({
                        'ID': irrigation.get('id'),
                        'Planting ID': irrigation.get('planting_id'),
                        'Date': irrigation.get('irrigation_date'),
                        'Water Amount': irrigation.get('water_amount'),
                        'Type': irrigation.get('irrigation_type'),
                        'Duration': irrigation.get('duration'),
                        'Notes': irrigation.get('notes')
                    })
                
                irrigations_df = pd.DataFrame(irrigations_data)
                
                # تحويل بيانات التسميد إلى DataFrame
                fertilizations = details.get('fertilizations', [])
                fertilizations_data = []
                
                for fertilization in fertilizations:
                    fertilizations_data.append({
                        'ID': fertilization.get('id'),
                        'Planting ID': fertilization.get('planting_id'),
                        'Date': fertilization.get('fertilization_date'),
                        'Fertilizer': fertilization.get('fertilizer_name'),
                        'Amount': fertilization.get('amount'),
                        'Method': fertilization.get('application_method'),
                        'Notes': fertilization.get('notes')
                    })
                
                fertilizations_df = pd.DataFrame(fertilizations_data)
                
                # تصدير التقرير حسب الصيغة المطلوبة
                if file_format == 'csv':
                    # تصدير كل جدول إلى ملف منفصل
                    plantings_df.to_csv(f"{file_path}_plantings.csv", index=False, encoding='utf-8')
                    irrigations_df.to_csv(f"{file_path}_irrigations.csv", index=False, encoding='utf-8')
                    fertilizations_df.to_csv(f"{file_path}_fertilizations.csv", index=False, encoding='utf-8')
                elif file_format == 'excel':
                    # تصدير جميع الجداول إلى ملف Excel واحد
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        plantings_df.to_excel(writer, sheet_name='Plantings', index=False)
                        irrigations_df.to_excel(writer, sheet_name='Irrigations', index=False)
                        fertilizations_df.to_excel(writer, sheet_name='Fertilizations', index=False)
                elif file_format == 'json':
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(report_data, f, ensure_ascii=False, indent=4)
                else:
                    return {'success': False, 'message': f'Invalid file format: {file_format}'}
                
            elif report_type == 'financial':
                # تصدير التقرير المالي
                financial = report.get('financial', {})
                
                # تحويل بيانات التكاليف إلى DataFrame
                costs = financial.get('costs', {})
                
                costs_data = {
                    'Category': list(costs.keys()),
                    'Cost': list(costs.values())
                }
                
                costs_df = pd.DataFrame(costs_data)
                
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
                
            else:
                return {'success': False, 'message': f'Invalid report type: {report_type}'}
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='export_farm_report',
                entity_type='farm_report',
                entity_id=f"{report.get('farm', {}).get('id')}_{report_type}",
                details=f"Exported {report_type} report to {file_path} in {file_format} format"
            )
            
            return {
                'success': True,
                'message': f'Farm report exported successfully to {file_path}',
                'file_path': file_path,
                'file_format': file_format
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error exporting farm report: {str(e)}'}
