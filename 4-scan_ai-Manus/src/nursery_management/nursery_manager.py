#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المشاتل
===============
هذه الوحدة مسؤولة عن إدارة المشاتل، بما في ذلك تتبع الشتلات،
تواريخ الزراعة والحجز والتسليم، وإدارة الطاقة الاستيعابية للمشتل.
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

class NurseryManager:
    """مدير إدارة المشاتل"""
    
    def __init__(self, db_manager=None, audit_manager=None, auth_manager=None):
        """
        تهيئة مدير إدارة المشاتل
        
        المعاملات:
            db_manager (DatabaseManager): مدير قاعدة البيانات
            audit_manager (AuditManager): مدير التدقيق
            auth_manager (AuthManager): مدير المصادقة
        """
        self.db_manager = db_manager or DatabaseManager()
        self.audit_manager = audit_manager or AuditManager()
        self.auth_manager = auth_manager or AuthManager()
        self.cost_calculator = CostCalculator(db_manager, audit_manager, auth_manager)
        
        # تحميل بيانات المشاتل
        self.nurseries = self._load_nurseries()
        
        # تحميل بيانات أنواع الشتلات
        self.seedling_types = self._load_seedling_types()
        
        # تحميل بيانات المواسم
        self.seasons = {
            'summer': {'name': 'صيف', 'months': [4, 5, 6, 7, 8, 9]},
            'winter': {'name': 'شتاء', 'months': [10, 11, 12, 1, 2, 3]}
        }
    
    def _load_nurseries(self):
        """
        تحميل بيانات المشاتل
        
        العائد:
            dict: بيانات المشاتل
        """
        try:
            query = """
                SELECT id, name, location, total_capacity, current_capacity, 
                       manager_id, creation_date, status
                FROM nurseries
            """
            results = self.db_manager.execute_query(query)
            
            nurseries = {}
            for row in results:
                nursery_id = row[0]
                nurseries[nursery_id] = {
                    'id': nursery_id,
                    'name': row[1],
                    'location': row[2],
                    'total_capacity': row[3],
                    'current_capacity': row[4],
                    'manager_id': row[5],
                    'creation_date': row[6],
                    'status': row[7]
                }
            
            return nurseries
            
        except Exception as e:
            print(f"Error loading nurseries: {str(e)}")
            return {}
    
    def _load_seedling_types(self):
        """
        تحميل بيانات أنواع الشتلات
        
        العائد:
            dict: بيانات أنواع الشتلات
        """
        try:
            query = """
                SELECT id, name, category, growth_duration_summer, growth_duration_winter, 
                       description, space_required
                FROM seedling_types
            """
            results = self.db_manager.execute_query(query)
            
            seedling_types = {}
            for row in results:
                seedling_type_id = row[0]
                seedling_types[seedling_type_id] = {
                    'id': seedling_type_id,
                    'name': row[1],
                    'category': row[2],
                    'growth_duration_summer': row[3],
                    'growth_duration_winter': row[4],
                    'description': row[5],
                    'space_required': row[6]
                }
            
            return seedling_types
            
        except Exception as e:
            print(f"Error loading seedling types: {str(e)}")
            return {}
    
    def create_nursery(self, nursery_data, user_id):
        """
        إنشاء مشتل جديد
        
        المعاملات:
            nursery_data (dict): بيانات المشتل
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإنشاء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'create_nursery'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات المشتل
            name = nursery_data.get('name', '')
            location = nursery_data.get('location', '')
            total_capacity = nursery_data.get('total_capacity', 0)
            manager_id = nursery_data.get('manager_id', user_id)
            status = nursery_data.get('status', 'active')
            
            # إدخال بيانات المشتل
            query = """
                INSERT INTO nurseries
                (name, location, total_capacity, current_capacity, manager_id, 
                 creation_date, status, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    name, location, total_capacity, 0, manager_id, 
                    datetime.datetime.now().isoformat(), status, user_id
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to create nursery'}
            
            nursery_id = result[0][0]
            
            # تحديث قائمة المشاتل
            self.nurseries[nursery_id] = {
                'id': nursery_id,
                'name': name,
                'location': location,
                'total_capacity': total_capacity,
                'current_capacity': 0,
                'manager_id': manager_id,
                'creation_date': datetime.datetime.now().isoformat(),
                'status': status
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='create_nursery',
                entity_type='nursery',
                entity_id=str(nursery_id),
                details=f"Created new nursery: {name}"
            )
            
            return {
                'success': True,
                'nursery_id': nursery_id,
                'message': 'Nursery created successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error creating nursery: {str(e)}'}
    
    def update_nursery(self, nursery_id, nursery_data, user_id):
        """
        تحديث بيانات مشتل
        
        المعاملات:
            nursery_id (int): معرف المشتل
            nursery_data (dict): بيانات المشتل المحدثة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التحديث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'update_nursery'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # استخراج بيانات المشتل
            name = nursery_data.get('name', self.nurseries[nursery_id]['name'])
            location = nursery_data.get('location', self.nurseries[nursery_id]['location'])
            total_capacity = nursery_data.get('total_capacity', self.nurseries[nursery_id]['total_capacity'])
            manager_id = nursery_data.get('manager_id', self.nurseries[nursery_id]['manager_id'])
            status = nursery_data.get('status', self.nurseries[nursery_id]['status'])
            
            # التحقق من إمكانية تقليل الطاقة الاستيعابية
            current_capacity = self.nurseries[nursery_id]['current_capacity']
            if total_capacity < current_capacity:
                return {
                    'success': False, 
                    'message': f'Cannot reduce capacity below current usage. Current: {current_capacity}, Requested: {total_capacity}'
                }
            
            # تحديث بيانات المشتل
            query = """
                UPDATE nurseries
                SET name = %s, location = %s, total_capacity = %s, manager_id = %s, 
                    status = %s, updated_at = %s, updated_by = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                query, 
                (
                    name, location, total_capacity, manager_id, status, 
                    datetime.datetime.now().isoformat(), user_id, nursery_id
                )
            )
            
            # تحديث قائمة المشاتل
            self.nurseries[nursery_id].update({
                'name': name,
                'location': location,
                'total_capacity': total_capacity,
                'manager_id': manager_id,
                'status': status
            })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='update_nursery',
                entity_type='nursery',
                entity_id=str(nursery_id),
                details=f"Updated nursery: {name}"
            )
            
            return {
                'success': True,
                'nursery_id': nursery_id,
                'message': 'Nursery updated successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error updating nursery: {str(e)}'}
    
    def get_nursery(self, nursery_id, user_id):
        """
        الحصول على بيانات مشتل
        
        المعاملات:
            nursery_id (int): معرف المشتل
            user_id (int): معرف المستخدم
            
        العائد:
            dict: بيانات المشتل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_nursery'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # الحصول على بيانات المشتل
            nursery = self.nurseries[nursery_id]
            
            # الحصول على بيانات دفعات الشتلات في المشتل
            batches_query = """
                SELECT id, seedling_type_id, quantity, planting_date, expected_ready_date, 
                       actual_ready_date, status, season, notes
                FROM seedling_batches
                WHERE nursery_id = %s
                ORDER BY planting_date DESC
            """
            batches_result = self.db_manager.execute_query(batches_query, (nursery_id,))
            
            batches = []
            for row in batches_result:
                batch_id = row[0]
                seedling_type_id = row[1]
                
                # الحصول على بيانات نوع الشتلة
                seedling_type_name = self.seedling_types.get(seedling_type_id, {}).get('name', 'Unknown')
                seedling_category = self.seedling_types.get(seedling_type_id, {}).get('category', 'Unknown')
                
                # الحصول على بيانات الحجوزات
                reservations_query = """
                    SELECT id, customer_id, customer_name, quantity, reservation_date, 
                           delivery_date, status, notes
                    FROM seedling_reservations
                    WHERE batch_id = %s
                    ORDER BY reservation_date
                """
                reservations_result = self.db_manager.execute_query(reservations_query, (batch_id,))
                
                reservations = []
                for res_row in reservations_result:
                    reservations.append({
                        'id': res_row[0],
                        'customer_id': res_row[1],
                        'customer_name': res_row[2],
                        'quantity': res_row[3],
                        'reservation_date': res_row[4],
                        'delivery_date': res_row[5],
                        'status': res_row[6],
                        'notes': res_row[7]
                    })
                
                batches.append({
                    'id': batch_id,
                    'seedling_type_id': seedling_type_id,
                    'seedling_type_name': seedling_type_name,
                    'seedling_category': seedling_category,
                    'quantity': row[2],
                    'planting_date': row[3],
                    'expected_ready_date': row[4],
                    'actual_ready_date': row[5],
                    'status': row[6],
                    'season': row[7],
                    'notes': row[8],
                    'reservations': reservations
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_nursery',
                entity_type='nursery',
                entity_id=str(nursery_id),
                details=f"Viewed nursery: {nursery['name']}"
            )
            
            return {
                'success': True,
                'nursery': nursery,
                'batches': batches
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting nursery: {str(e)}'}
    
    def list_nurseries(self, filters, user_id):
        """
        الحصول على قائمة المشاتل
        
        المعاملات:
            filters (dict): معايير التصفية
            user_id (int): معرف المستخدم
            
        العائد:
            dict: قائمة المشاتل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'list_nurseries'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج معايير التصفية
            manager_id = filters.get('manager_id')
            status = filters.get('status')
            location = filters.get('location')
            
            # بناء استعلام قائمة المشاتل
            query = "SELECT id, name, location, total_capacity, current_capacity, manager_id, creation_date, status FROM nurseries WHERE 1=1"
            params = []
            
            if manager_id:
                query += " AND manager_id = %s"
                params.append(manager_id)
            
            if status:
                query += " AND status = %s"
                params.append(status)
            
            if location:
                query += " AND location LIKE %s"
                params.append(f"%{location}%")
            
            query += " ORDER BY name"
            
            # تنفيذ الاستعلام
            results = self.db_manager.execute_query(query, tuple(params))
            
            # تحضير قائمة المشاتل
            nurseries = []
            for row in results:
                nurseries.append({
                    'id': row[0],
                    'name': row[1],
                    'location': row[2],
                    'total_capacity': row[3],
                    'current_capacity': row[4],
                    'manager_id': row[5],
                    'creation_date': row[6],
                    'status': row[7],
                    'capacity_percentage': round((row[4] / row[3]) * 100, 2) if row[3] > 0 else 0
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='list_nurseries',
                entity_type='nurseries',
                entity_id='all',
                details=f"Listed nurseries with filters: {json.dumps(filters)}"
            )
            
            return {
                'success': True,
                'nurseries': nurseries,
                'count': len(nurseries)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error listing nurseries: {str(e)}'}
    
    def create_seedling_type(self, seedling_type_data, user_id):
        """
        إنشاء نوع شتلة جديد
        
        المعاملات:
            seedling_type_data (dict): بيانات نوع الشتلة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإنشاء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'create_seedling_type'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات نوع الشتلة
            name = seedling_type_data.get('name', '')
            category = seedling_type_data.get('category', '')
            growth_duration_summer = seedling_type_data.get('growth_duration_summer', 0)
            growth_duration_winter = seedling_type_data.get('growth_duration_winter', 0)
            description = seedling_type_data.get('description', '')
            space_required = seedling_type_data.get('space_required', 1)
            
            # إدخال بيانات نوع الشتلة
            query = """
                INSERT INTO seedling_types
                (name, category, growth_duration_summer, growth_duration_winter, 
                 description, space_required, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    name, category, growth_duration_summer, growth_duration_winter, 
                    description, space_required, user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to create seedling type'}
            
            seedling_type_id = result[0][0]
            
            # تحديث قائمة أنواع الشتلات
            self.seedling_types[seedling_type_id] = {
                'id': seedling_type_id,
                'name': name,
                'category': category,
                'growth_duration_summer': growth_duration_summer,
                'growth_duration_winter': growth_duration_winter,
                'description': description,
                'space_required': space_required
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='create_seedling_type',
                entity_type='seedling_type',
                entity_id=str(seedling_type_id),
                details=f"Created new seedling type: {name}"
            )
            
            return {
                'success': True,
                'seedling_type_id': seedling_type_id,
                'message': 'Seedling type created successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error creating seedling type: {str(e)}'}
    
    def list_seedling_types(self, filters, user_id):
        """
        الحصول على قائمة أنواع الشتلات
        
        المعاملات:
            filters (dict): معايير التصفية
            user_id (int): معرف المستخدم
            
        العائد:
            dict: قائمة أنواع الشتلات
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'list_seedling_types'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج معايير التصفية
            category = filters.get('category')
            name_search = filters.get('name_search')
            
            # بناء استعلام قائمة أنواع الشتلات
            query = """
                SELECT id, name, category, growth_duration_summer, growth_duration_winter, 
                       description, space_required
                FROM seedling_types
                WHERE 1=1
            """
            params = []
            
            if category:
                query += " AND category = %s"
                params.append(category)
            
            if name_search:
                query += " AND name LIKE %s"
                params.append(f"%{name_search}%")
            
            query += " ORDER BY category, name"
            
            # تنفيذ الاستعلام
            results = self.db_manager.execute_query(query, tuple(params))
            
            # تحضير قائمة أنواع الشتلات
            seedling_types = []
            for row in results:
                seedling_types.append({
                    'id': row[0],
                    'name': row[1],
                    'category': row[2],
                    'growth_duration_summer': row[3],
                    'growth_duration_winter': row[4],
                    'description': row[5],
                    'space_required': row[6]
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='list_seedling_types',
                entity_type='seedling_types',
                entity_id='all',
                details=f"Listed seedling types with filters: {json.dumps(filters)}"
            )
            
            return {
                'success': True,
                'seedling_types': seedling_types,
                'count': len(seedling_types)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error listing seedling types: {str(e)}'}
    
    def add_seedling_batch(self, batch_data, user_id):
        """
        إضافة دفعة شتلات جديدة
        
        المعاملات:
            batch_data (dict): بيانات دفعة الشتلات
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_seedling_batch'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات دفعة الشتلات
            nursery_id = batch_data.get('nursery_id')
            seedling_type_id = batch_data.get('seedling_type_id')
            quantity = batch_data.get('quantity', 0)
            planting_date = batch_data.get('planting_date')
            season = batch_data.get('season', self._determine_season(planting_date))
            notes = batch_data.get('notes', '')
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # التحقق من وجود نوع الشتلة
            if seedling_type_id not in self.seedling_types:
                return {'success': False, 'message': 'Seedling type not found'}
            
            # التحقق من حالة المشتل
            if self.nurseries[nursery_id]['status'] != 'active':
                return {'success': False, 'message': 'Nursery is not active'}
            
            # حساب المساحة المطلوبة
            space_required = self.seedling_types[seedling_type_id]['space_required'] * quantity
            
            # التحقق من توفر المساحة
            nursery_capacity = self.nurseries[nursery_id]['total_capacity']
            current_capacity = self.nurseries[nursery_id]['current_capacity']
            
            if current_capacity + space_required > nursery_capacity:
                return {
                    'success': False, 
                    'message': f'Insufficient capacity. Available: {nursery_capacity - current_capacity}, Required: {space_required}'
                }
            
            # حساب تاريخ الجاهزية المتوقع
            growth_duration = self.seedling_types[seedling_type_id]['growth_duration_summer'] if season == 'summer' else self.seedling_types[seedling_type_id]['growth_duration_winter']
            
            planting_date_obj = datetime.datetime.fromisoformat(planting_date.replace('Z', '+00:00'))
            expected_ready_date = (planting_date_obj + datetime.timedelta(days=growth_duration)).isoformat()
            
            # إدخال بيانات دفعة الشتلات
            query = """
                INSERT INTO seedling_batches
                (nursery_id, seedling_type_id, quantity, planting_date, expected_ready_date, 
                 status, season, notes, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    nursery_id, seedling_type_id, quantity, planting_date, expected_ready_date, 
                    'growing', season, notes, user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add seedling batch'}
            
            batch_id = result[0][0]
            
            # تحديث السعة الحالية للمشتل
            update_nursery_query = """
                UPDATE nurseries
                SET current_capacity = current_capacity + %s, 
                    updated_at = %s, updated_by = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                update_nursery_query, 
                (space_required, datetime.datetime.now().isoformat(), user_id, nursery_id)
            )
            
            # تحديث بيانات المشتل في الذاكرة
            self.nurseries[nursery_id]['current_capacity'] += space_required
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_seedling_batch',
                entity_type='seedling_batch',
                entity_id=str(batch_id),
                details=f"Added seedling batch of type {seedling_type_id} to nursery {nursery_id}"
            )
            
            return {
                'success': True,
                'batch_id': batch_id,
                'expected_ready_date': expected_ready_date,
                'message': 'Seedling batch added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding seedling batch: {str(e)}'}
    
    def update_seedling_batch(self, batch_id, batch_data, user_id):
        """
        تحديث بيانات دفعة شتلات
        
        المعاملات:
            batch_id (int): معرف دفعة الشتلات
            batch_data (dict): بيانات دفعة الشتلات المحدثة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التحديث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'update_seedling_batch'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود دفعة الشتلات
            batch_query = """
                SELECT nursery_id, seedling_type_id, quantity, planting_date, 
                       expected_ready_date, actual_ready_date, status, season, notes
                FROM seedling_batches
                WHERE id = %s
            """
            batch_result = self.db_manager.execute_query(batch_query, (batch_id,))
            
            if not batch_result:
                return {'success': False, 'message': 'Seedling batch not found'}
            
            # استخراج بيانات دفعة الشتلات الحالية
            current_nursery_id = batch_result[0][0]
            current_seedling_type_id = batch_result[0][1]
            current_quantity = batch_result[0][2]
            current_planting_date = batch_result[0][3]
            current_expected_ready_date = batch_result[0][4]
            current_actual_ready_date = batch_result[0][5]
            current_status = batch_result[0][6]
            current_season = batch_result[0][7]
            current_notes = batch_result[0][8]
            
            # استخراج بيانات دفعة الشتلات المحدثة
            nursery_id = batch_data.get('nursery_id', current_nursery_id)
            seedling_type_id = batch_data.get('seedling_type_id', current_seedling_type_id)
            quantity = batch_data.get('quantity', current_quantity)
            planting_date = batch_data.get('planting_date', current_planting_date)
            actual_ready_date = batch_data.get('actual_ready_date', current_actual_ready_date)
            status = batch_data.get('status', current_status)
            season = batch_data.get('season', current_season)
            notes = batch_data.get('notes', current_notes)
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # التحقق من وجود نوع الشتلة
            if seedling_type_id not in self.seedling_types:
                return {'success': False, 'message': 'Seedling type not found'}
            
            # حساب المساحة المطلوبة الجديدة
            new_space_required = self.seedling_types[seedling_type_id]['space_required'] * quantity
            
            # حساب المساحة المطلوبة الحالية
            current_space_required = self.seedling_types[current_seedling_type_id]['space_required'] * current_quantity
            
            # التحقق من توفر المساحة إذا كان هناك تغيير في المشتل أو الكمية أو نوع الشتلة
            if nursery_id != current_nursery_id or new_space_required > current_space_required:
                nursery_capacity = self.nurseries[nursery_id]['total_capacity']
                current_capacity = self.nurseries[nursery_id]['current_capacity']
                
                # إذا كان هناك تغيير في المشتل، نحتاج إلى التحقق من توفر المساحة الكاملة
                if nursery_id != current_nursery_id:
                    if current_capacity + new_space_required > nursery_capacity:
                        return {
                            'success': False, 
                            'message': f'Insufficient capacity in new nursery. Available: {nursery_capacity - current_capacity}, Required: {new_space_required}'
                        }
                # إذا كان هناك تغيير في الكمية أو نوع الشتلة، نحتاج إلى التحقق من توفر المساحة الإضافية
                else:
                    additional_space = new_space_required - current_space_required
                    if current_capacity + additional_space > nursery_capacity:
                        return {
                            'success': False, 
                            'message': f'Insufficient capacity for additional seedlings. Available: {nursery_capacity - current_capacity}, Required additional: {additional_space}'
                        }
            
            # حساب تاريخ الجاهزية المتوقع الجديد إذا تم تغيير تاريخ الزراعة أو نوع الشتلة أو الموسم
            if planting_date != current_planting_date or seedling_type_id != current_seedling_type_id or season != current_season:
                growth_duration = self.seedling_types[seedling_type_id]['growth_duration_summer'] if season == 'summer' else self.seedling_types[seedling_type_id]['growth_duration_winter']
                
                planting_date_obj = datetime.datetime.fromisoformat(planting_date.replace('Z', '+00:00'))
                expected_ready_date = (planting_date_obj + datetime.timedelta(days=growth_duration)).isoformat()
            else:
                expected_ready_date = current_expected_ready_date
            
            # تحديث بيانات دفعة الشتلات
            query = """
                UPDATE seedling_batches
                SET nursery_id = %s, seedling_type_id = %s, quantity = %s, 
                    planting_date = %s, expected_ready_date = %s, actual_ready_date = %s, 
                    status = %s, season = %s, notes = %s, updated_by = %s, updated_at = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                query, 
                (
                    nursery_id, seedling_type_id, quantity, planting_date, 
                    expected_ready_date, actual_ready_date, status, season, notes, 
                    user_id, datetime.datetime.now().isoformat(), batch_id
                )
            )
            
            # تحديث السعة الحالية للمشاتل
            if nursery_id != current_nursery_id:
                # تقليل السعة في المشتل القديم
                update_old_nursery_query = """
                    UPDATE nurseries
                    SET current_capacity = current_capacity - %s, 
                        updated_at = %s, updated_by = %s
                    WHERE id = %s
                """
                self.db_manager.execute_query(
                    update_old_nursery_query, 
                    (current_space_required, datetime.datetime.now().isoformat(), user_id, current_nursery_id)
                )
                
                # زيادة السعة في المشتل الجديد
                update_new_nursery_query = """
                    UPDATE nurseries
                    SET current_capacity = current_capacity + %s, 
                        updated_at = %s, updated_by = %s
                    WHERE id = %s
                """
                self.db_manager.execute_query(
                    update_new_nursery_query, 
                    (new_space_required, datetime.datetime.now().isoformat(), user_id, nursery_id)
                )
                
                # تحديث بيانات المشاتل في الذاكرة
                self.nurseries[current_nursery_id]['current_capacity'] -= current_space_required
                self.nurseries[nursery_id]['current_capacity'] += new_space_required
            else:
                # تحديث السعة في نفس المشتل
                space_difference = new_space_required - current_space_required
                
                if space_difference != 0:
                    update_nursery_query = """
                        UPDATE nurseries
                        SET current_capacity = current_capacity + %s, 
                            updated_at = %s, updated_by = %s
                        WHERE id = %s
                    """
                    self.db_manager.execute_query(
                        update_nursery_query, 
                        (space_difference, datetime.datetime.now().isoformat(), user_id, nursery_id)
                    )
                    
                    # تحديث بيانات المشتل في الذاكرة
                    self.nurseries[nursery_id]['current_capacity'] += space_difference
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='update_seedling_batch',
                entity_type='seedling_batch',
                entity_id=str(batch_id),
                details=f"Updated seedling batch {batch_id}"
            )
            
            return {
                'success': True,
                'batch_id': batch_id,
                'expected_ready_date': expected_ready_date,
                'message': 'Seedling batch updated successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error updating seedling batch: {str(e)}'}
    
    def get_seedling_batch(self, batch_id, user_id):
        """
        الحصول على بيانات دفعة شتلات
        
        المعاملات:
            batch_id (int): معرف دفعة الشتلات
            user_id (int): معرف المستخدم
            
        العائد:
            dict: بيانات دفعة الشتلات
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_seedling_batch'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # الحصول على بيانات دفعة الشتلات
            batch_query = """
                SELECT b.nursery_id, b.seedling_type_id, b.quantity, b.planting_date, 
                       b.expected_ready_date, b.actual_ready_date, b.status, b.season, 
                       b.notes, n.name as nursery_name, s.name as seedling_type_name, 
                       s.category as seedling_category
                FROM seedling_batches b
                JOIN nurseries n ON b.nursery_id = n.id
                JOIN seedling_types s ON b.seedling_type_id = s.id
                WHERE b.id = %s
            """
            batch_result = self.db_manager.execute_query(batch_query, (batch_id,))
            
            if not batch_result:
                return {'success': False, 'message': 'Seedling batch not found'}
            
            # استخراج بيانات دفعة الشتلات
            nursery_id = batch_result[0][0]
            seedling_type_id = batch_result[0][1]
            quantity = batch_result[0][2]
            planting_date = batch_result[0][3]
            expected_ready_date = batch_result[0][4]
            actual_ready_date = batch_result[0][5]
            status = batch_result[0][6]
            season = batch_result[0][7]
            notes = batch_result[0][8]
            nursery_name = batch_result[0][9]
            seedling_type_name = batch_result[0][10]
            seedling_category = batch_result[0][11]
            
            # الحصول على بيانات الحجوزات
            reservations_query = """
                SELECT id, customer_id, customer_name, quantity, reservation_date, 
                       delivery_date, status, notes
                FROM seedling_reservations
                WHERE batch_id = %s
                ORDER BY reservation_date
            """
            reservations_result = self.db_manager.execute_query(reservations_query, (batch_id,))
            
            reservations = []
            for row in reservations_result:
                reservations.append({
                    'id': row[0],
                    'customer_id': row[1],
                    'customer_name': row[2],
                    'quantity': row[3],
                    'reservation_date': row[4],
                    'delivery_date': row[5],
                    'status': row[6],
                    'notes': row[7]
                })
            
            # حساب الكمية المحجوزة
            reserved_quantity = sum(res['quantity'] for res in reservations if res['status'] != 'cancelled')
            
            # حساب الكمية المتاحة
            available_quantity = quantity - reserved_quantity
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_seedling_batch',
                entity_type='seedling_batch',
                entity_id=str(batch_id),
                details=f"Viewed seedling batch {batch_id}"
            )
            
            return {
                'success': True,
                'batch': {
                    'id': batch_id,
                    'nursery_id': nursery_id,
                    'nursery_name': nursery_name,
                    'seedling_type_id': seedling_type_id,
                    'seedling_type_name': seedling_type_name,
                    'seedling_category': seedling_category,
                    'quantity': quantity,
                    'planting_date': planting_date,
                    'expected_ready_date': expected_ready_date,
                    'actual_ready_date': actual_ready_date,
                    'status': status,
                    'season': season,
                    'notes': notes,
                    'reserved_quantity': reserved_quantity,
                    'available_quantity': available_quantity
                },
                'reservations': reservations
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting seedling batch: {str(e)}'}
    
    def list_seedling_batches(self, filters, user_id):
        """
        الحصول على قائمة دفعات الشتلات
        
        المعاملات:
            filters (dict): معايير التصفية
            user_id (int): معرف المستخدم
            
        العائد:
            dict: قائمة دفعات الشتلات
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'list_seedling_batches'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج معايير التصفية
            nursery_id = filters.get('nursery_id')
            seedling_type_id = filters.get('seedling_type_id')
            status = filters.get('status')
            season = filters.get('season')
            category = filters.get('category')
            ready_before = filters.get('ready_before')
            ready_after = filters.get('ready_after')
            
            # بناء استعلام قائمة دفعات الشتلات
            query = """
                SELECT b.id, b.nursery_id, b.seedling_type_id, b.quantity, b.planting_date, 
                       b.expected_ready_date, b.actual_ready_date, b.status, b.season, 
                       n.name as nursery_name, s.name as seedling_type_name, 
                       s.category as seedling_category
                FROM seedling_batches b
                JOIN nurseries n ON b.nursery_id = n.id
                JOIN seedling_types s ON b.seedling_type_id = s.id
                WHERE 1=1
            """
            params = []
            
            if nursery_id:
                query += " AND b.nursery_id = %s"
                params.append(nursery_id)
            
            if seedling_type_id:
                query += " AND b.seedling_type_id = %s"
                params.append(seedling_type_id)
            
            if status:
                query += " AND b.status = %s"
                params.append(status)
            
            if season:
                query += " AND b.season = %s"
                params.append(season)
            
            if category:
                query += " AND s.category = %s"
                params.append(category)
            
            if ready_before:
                query += " AND b.expected_ready_date <= %s"
                params.append(ready_before)
            
            if ready_after:
                query += " AND b.expected_ready_date >= %s"
                params.append(ready_after)
            
            query += " ORDER BY b.expected_ready_date"
            
            # تنفيذ الاستعلام
            results = self.db_manager.execute_query(query, tuple(params))
            
            # تحضير قائمة دفعات الشتلات
            batches = []
            for row in results:
                batch_id = row[0]
                
                # الحصول على بيانات الحجوزات
                reservations_query = """
                    SELECT SUM(quantity)
                    FROM seedling_reservations
                    WHERE batch_id = %s AND status != 'cancelled'
                """
                reservations_result = self.db_manager.execute_query(reservations_query, (batch_id,))
                
                reserved_quantity = reservations_result[0][0] if reservations_result[0][0] else 0
                
                batches.append({
                    'id': batch_id,
                    'nursery_id': row[1],
                    'nursery_name': row[9],
                    'seedling_type_id': row[2],
                    'seedling_type_name': row[10],
                    'seedling_category': row[11],
                    'quantity': row[3],
                    'planting_date': row[4],
                    'expected_ready_date': row[5],
                    'actual_ready_date': row[6],
                    'status': row[7],
                    'season': row[8],
                    'reserved_quantity': reserved_quantity,
                    'available_quantity': row[3] - reserved_quantity
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='list_seedling_batches',
                entity_type='seedling_batches',
                entity_id='all',
                details=f"Listed seedling batches with filters: {json.dumps(filters)}"
            )
            
            return {
                'success': True,
                'batches': batches,
                'count': len(batches)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error listing seedling batches: {str(e)}'}
    
    def add_seedling_reservation(self, reservation_data, user_id):
        """
        إضافة حجز شتلات جديد
        
        المعاملات:
            reservation_data (dict): بيانات الحجز
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_seedling_reservation'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج بيانات الحجز
            batch_id = reservation_data.get('batch_id')
            customer_id = reservation_data.get('customer_id')
            customer_name = reservation_data.get('customer_name', '')
            quantity = reservation_data.get('quantity', 0)
            reservation_date = reservation_data.get('reservation_date', datetime.datetime.now().isoformat())
            delivery_date = reservation_data.get('delivery_date')
            notes = reservation_data.get('notes', '')
            
            # التحقق من وجود دفعة الشتلات
            batch_query = """
                SELECT nursery_id, seedling_type_id, quantity, expected_ready_date, status
                FROM seedling_batches
                WHERE id = %s
            """
            batch_result = self.db_manager.execute_query(batch_query, (batch_id,))
            
            if not batch_result:
                return {'success': False, 'message': 'Seedling batch not found'}
            
            nursery_id = batch_result[0][0]
            seedling_type_id = batch_result[0][1]
            batch_quantity = batch_result[0][2]
            expected_ready_date = batch_result[0][3]
            batch_status = batch_result[0][4]
            
            # التحقق من حالة دفعة الشتلات
            if batch_status not in ['growing', 'ready']:
                return {'success': False, 'message': f'Cannot reserve from batch with status: {batch_status}'}
            
            # الحصول على بيانات الحجوزات الحالية
            reservations_query = """
                SELECT SUM(quantity)
                FROM seedling_reservations
                WHERE batch_id = %s AND status != 'cancelled'
            """
            reservations_result = self.db_manager.execute_query(reservations_query, (batch_id,))
            
            reserved_quantity = reservations_result[0][0] if reservations_result[0][0] else 0
            
            # التحقق من توفر الكمية المطلوبة
            available_quantity = batch_quantity - reserved_quantity
            
            if quantity > available_quantity:
                return {
                    'success': False, 
                    'message': f'Insufficient quantity. Available: {available_quantity}, Requested: {quantity}'
                }
            
            # التحقق من تاريخ التسليم
            if delivery_date and delivery_date < expected_ready_date:
                return {
                    'success': False, 
                    'message': f'Delivery date cannot be before expected ready date: {expected_ready_date}'
                }
            
            # إدخال بيانات الحجز
            query = """
                INSERT INTO seedling_reservations
                (batch_id, nursery_id, seedling_type_id, customer_id, customer_name, 
                 quantity, reservation_date, delivery_date, status, notes, 
                 created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    batch_id, nursery_id, seedling_type_id, customer_id, customer_name, 
                    quantity, reservation_date, delivery_date, 'pending', notes, 
                    user_id, datetime.datetime.now().isoformat()
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add seedling reservation'}
            
            reservation_id = result[0][0]
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_seedling_reservation',
                entity_type='seedling_reservation',
                entity_id=str(reservation_id),
                details=f"Added seedling reservation for batch {batch_id}, customer {customer_name}"
            )
            
            return {
                'success': True,
                'reservation_id': reservation_id,
                'message': 'Seedling reservation added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding seedling reservation: {str(e)}'}
    
    def update_seedling_reservation(self, reservation_id, reservation_data, user_id):
        """
        تحديث بيانات حجز شتلات
        
        المعاملات:
            reservation_id (int): معرف الحجز
            reservation_data (dict): بيانات الحجز المحدثة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التحديث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'update_seedling_reservation'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود الحجز
            reservation_query = """
                SELECT batch_id, customer_id, customer_name, quantity, 
                       reservation_date, delivery_date, status, notes
                FROM seedling_reservations
                WHERE id = %s
            """
            reservation_result = self.db_manager.execute_query(reservation_query, (reservation_id,))
            
            if not reservation_result:
                return {'success': False, 'message': 'Seedling reservation not found'}
            
            # استخراج بيانات الحجز الحالية
            current_batch_id = reservation_result[0][0]
            current_customer_id = reservation_result[0][1]
            current_customer_name = reservation_result[0][2]
            current_quantity = reservation_result[0][3]
            current_reservation_date = reservation_result[0][4]
            current_delivery_date = reservation_result[0][5]
            current_status = reservation_result[0][6]
            current_notes = reservation_result[0][7]
            
            # استخراج بيانات الحجز المحدثة
            batch_id = reservation_data.get('batch_id', current_batch_id)
            customer_id = reservation_data.get('customer_id', current_customer_id)
            customer_name = reservation_data.get('customer_name', current_customer_name)
            quantity = reservation_data.get('quantity', current_quantity)
            reservation_date = reservation_data.get('reservation_date', current_reservation_date)
            delivery_date = reservation_data.get('delivery_date', current_delivery_date)
            status = reservation_data.get('status', current_status)
            notes = reservation_data.get('notes', current_notes)
            
            # إذا تم تغيير دفعة الشتلات أو الكمية، نحتاج إلى التحقق من توفر الكمية
            if batch_id != current_batch_id or quantity != current_quantity:
                # التحقق من وجود دفعة الشتلات
                batch_query = """
                    SELECT nursery_id, seedling_type_id, quantity, expected_ready_date, status
                    FROM seedling_batches
                    WHERE id = %s
                """
                batch_result = self.db_manager.execute_query(batch_query, (batch_id,))
                
                if not batch_result:
                    return {'success': False, 'message': 'Seedling batch not found'}
                
                nursery_id = batch_result[0][0]
                seedling_type_id = batch_result[0][1]
                batch_quantity = batch_result[0][2]
                expected_ready_date = batch_result[0][3]
                batch_status = batch_result[0][4]
                
                # التحقق من حالة دفعة الشتلات
                if batch_status not in ['growing', 'ready']:
                    return {'success': False, 'message': f'Cannot reserve from batch with status: {batch_status}'}
                
                # الحصول على بيانات الحجوزات الحالية
                reservations_query = """
                    SELECT SUM(quantity)
                    FROM seedling_reservations
                    WHERE batch_id = %s AND status != 'cancelled' AND id != %s
                """
                reservations_result = self.db_manager.execute_query(reservations_query, (batch_id, reservation_id))
                
                reserved_quantity = reservations_result[0][0] if reservations_result[0][0] else 0
                
                # التحقق من توفر الكمية المطلوبة
                available_quantity = batch_quantity - reserved_quantity
                
                if quantity > available_quantity:
                    return {
                        'success': False, 
                        'message': f'Insufficient quantity. Available: {available_quantity}, Requested: {quantity}'
                    }
                
                # التحقق من تاريخ التسليم
                if delivery_date and delivery_date < expected_ready_date:
                    return {
                        'success': False, 
                        'message': f'Delivery date cannot be before expected ready date: {expected_ready_date}'
                    }
            else:
                # إذا لم يتم تغيير دفعة الشتلات، نستخدم البيانات الحالية
                batch_query = """
                    SELECT nursery_id, seedling_type_id
                    FROM seedling_batches
                    WHERE id = %s
                """
                batch_result = self.db_manager.execute_query(batch_query, (batch_id,))
                
                nursery_id = batch_result[0][0]
                seedling_type_id = batch_result[0][1]
            
            # تحديث بيانات الحجز
            query = """
                UPDATE seedling_reservations
                SET batch_id = %s, nursery_id = %s, seedling_type_id = %s, 
                    customer_id = %s, customer_name = %s, quantity = %s, 
                    reservation_date = %s, delivery_date = %s, status = %s, 
                    notes = %s, updated_by = %s, updated_at = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                query, 
                (
                    batch_id, nursery_id, seedling_type_id, customer_id, customer_name, 
                    quantity, reservation_date, delivery_date, status, notes, 
                    user_id, datetime.datetime.now().isoformat(), reservation_id
                )
            )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='update_seedling_reservation',
                entity_type='seedling_reservation',
                entity_id=str(reservation_id),
                details=f"Updated seedling reservation {reservation_id}"
            )
            
            return {
                'success': True,
                'reservation_id': reservation_id,
                'message': 'Seedling reservation updated successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error updating seedling reservation: {str(e)}'}
    
    def get_seedling_reservation(self, reservation_id, user_id):
        """
        الحصول على بيانات حجز شتلات
        
        المعاملات:
            reservation_id (int): معرف الحجز
            user_id (int): معرف المستخدم
            
        العائد:
            dict: بيانات الحجز
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_seedling_reservation'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # الحصول على بيانات الحجز
            reservation_query = """
                SELECT r.batch_id, r.nursery_id, r.seedling_type_id, r.customer_id, 
                       r.customer_name, r.quantity, r.reservation_date, r.delivery_date, 
                       r.status, r.notes, n.name as nursery_name, 
                       s.name as seedling_type_name, s.category as seedling_category,
                       b.expected_ready_date, b.actual_ready_date, b.status as batch_status
                FROM seedling_reservations r
                JOIN nurseries n ON r.nursery_id = n.id
                JOIN seedling_types s ON r.seedling_type_id = s.id
                JOIN seedling_batches b ON r.batch_id = b.id
                WHERE r.id = %s
            """
            reservation_result = self.db_manager.execute_query(reservation_query, (reservation_id,))
            
            if not reservation_result:
                return {'success': False, 'message': 'Seedling reservation not found'}
            
            # استخراج بيانات الحجز
            batch_id = reservation_result[0][0]
            nursery_id = reservation_result[0][1]
            seedling_type_id = reservation_result[0][2]
            customer_id = reservation_result[0][3]
            customer_name = reservation_result[0][4]
            quantity = reservation_result[0][5]
            reservation_date = reservation_result[0][6]
            delivery_date = reservation_result[0][7]
            status = reservation_result[0][8]
            notes = reservation_result[0][9]
            nursery_name = reservation_result[0][10]
            seedling_type_name = reservation_result[0][11]
            seedling_category = reservation_result[0][12]
            expected_ready_date = reservation_result[0][13]
            actual_ready_date = reservation_result[0][14]
            batch_status = reservation_result[0][15]
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_seedling_reservation',
                entity_type='seedling_reservation',
                entity_id=str(reservation_id),
                details=f"Viewed seedling reservation {reservation_id}"
            )
            
            return {
                'success': True,
                'reservation': {
                    'id': reservation_id,
                    'batch_id': batch_id,
                    'nursery_id': nursery_id,
                    'nursery_name': nursery_name,
                    'seedling_type_id': seedling_type_id,
                    'seedling_type_name': seedling_type_name,
                    'seedling_category': seedling_category,
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'quantity': quantity,
                    'reservation_date': reservation_date,
                    'delivery_date': delivery_date,
                    'status': status,
                    'notes': notes,
                    'batch_info': {
                        'expected_ready_date': expected_ready_date,
                        'actual_ready_date': actual_ready_date,
                        'status': batch_status
                    }
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting seedling reservation: {str(e)}'}
    
    def list_seedling_reservations(self, filters, user_id):
        """
        الحصول على قائمة حجوزات الشتلات
        
        المعاملات:
            filters (dict): معايير التصفية
            user_id (int): معرف المستخدم
            
        العائد:
            dict: قائمة حجوزات الشتلات
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'list_seedling_reservations'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استخراج معايير التصفية
            nursery_id = filters.get('nursery_id')
            batch_id = filters.get('batch_id')
            seedling_type_id = filters.get('seedling_type_id')
            customer_id = filters.get('customer_id')
            customer_name = filters.get('customer_name')
            status = filters.get('status')
            delivery_before = filters.get('delivery_before')
            delivery_after = filters.get('delivery_after')
            
            # بناء استعلام قائمة حجوزات الشتلات
            query = """
                SELECT r.id, r.batch_id, r.nursery_id, r.seedling_type_id, r.customer_id, 
                       r.customer_name, r.quantity, r.reservation_date, r.delivery_date, 
                       r.status, n.name as nursery_name, s.name as seedling_type_name, 
                       s.category as seedling_category, b.expected_ready_date
                FROM seedling_reservations r
                JOIN nurseries n ON r.nursery_id = n.id
                JOIN seedling_types s ON r.seedling_type_id = s.id
                JOIN seedling_batches b ON r.batch_id = b.id
                WHERE 1=1
            """
            params = []
            
            if nursery_id:
                query += " AND r.nursery_id = %s"
                params.append(nursery_id)
            
            if batch_id:
                query += " AND r.batch_id = %s"
                params.append(batch_id)
            
            if seedling_type_id:
                query += " AND r.seedling_type_id = %s"
                params.append(seedling_type_id)
            
            if customer_id:
                query += " AND r.customer_id = %s"
                params.append(customer_id)
            
            if customer_name:
                query += " AND r.customer_name LIKE %s"
                params.append(f"%{customer_name}%")
            
            if status:
                query += " AND r.status = %s"
                params.append(status)
            
            if delivery_before:
                query += " AND r.delivery_date <= %s"
                params.append(delivery_before)
            
            if delivery_after:
                query += " AND r.delivery_date >= %s"
                params.append(delivery_after)
            
            query += " ORDER BY r.delivery_date"
            
            # تنفيذ الاستعلام
            results = self.db_manager.execute_query(query, tuple(params))
            
            # تحضير قائمة حجوزات الشتلات
            reservations = []
            for row in results:
                reservations.append({
                    'id': row[0],
                    'batch_id': row[1],
                    'nursery_id': row[2],
                    'seedling_type_id': row[3],
                    'customer_id': row[4],
                    'customer_name': row[5],
                    'quantity': row[6],
                    'reservation_date': row[7],
                    'delivery_date': row[8],
                    'status': row[9],
                    'nursery_name': row[10],
                    'seedling_type_name': row[11],
                    'seedling_category': row[12],
                    'expected_ready_date': row[13]
                })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='list_seedling_reservations',
                entity_type='seedling_reservations',
                entity_id='all',
                details=f"Listed seedling reservations with filters: {json.dumps(filters)}"
            )
            
            return {
                'success': True,
                'reservations': reservations,
                'count': len(reservations)
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error listing seedling reservations: {str(e)}'}
    
    def get_nursery_schedule(self, nursery_id, start_date, end_date, user_id):
        """
        الحصول على جدول المشتل
        
        المعاملات:
            nursery_id (int): معرف المشتل
            start_date (str): تاريخ البداية (YYYY-MM-DD)
            end_date (str): تاريخ النهاية (YYYY-MM-DD)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: جدول المشتل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_nursery_schedule'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # الحصول على بيانات دفعات الشتلات
            batches_query = """
                SELECT id, seedling_type_id, quantity, planting_date, expected_ready_date, 
                       actual_ready_date, status, season
                FROM seedling_batches
                WHERE nursery_id = %s AND 
                      (planting_date BETWEEN %s AND %s OR 
                       expected_ready_date BETWEEN %s AND %s OR
                       (planting_date <= %s AND expected_ready_date >= %s))
            """
            batches_result = self.db_manager.execute_query(
                batches_query, 
                (nursery_id, start_date, end_date, start_date, end_date, start_date, end_date)
            )
            
            batches = []
            for row in batches_result:
                batch_id = row[0]
                seedling_type_id = row[1]
                
                # الحصول على بيانات نوع الشتلة
                seedling_type_name = self.seedling_types.get(seedling_type_id, {}).get('name', 'Unknown')
                
                batches.append({
                    'id': batch_id,
                    'seedling_type_id': seedling_type_id,
                    'seedling_type_name': seedling_type_name,
                    'quantity': row[2],
                    'planting_date': row[3],
                    'expected_ready_date': row[4],
                    'actual_ready_date': row[5],
                    'status': row[6],
                    'season': row[7],
                    'event_type': 'batch'
                })
            
            # الحصول على بيانات الحجوزات
            reservations_query = """
                SELECT r.id, r.batch_id, r.seedling_type_id, r.customer_name, 
                       r.quantity, r.reservation_date, r.delivery_date, r.status,
                       s.name as seedling_type_name
                FROM seedling_reservations r
                JOIN seedling_types s ON r.seedling_type_id = s.id
                WHERE r.nursery_id = %s AND 
                      (r.reservation_date BETWEEN %s AND %s OR 
                       r.delivery_date BETWEEN %s AND %s)
            """
            reservations_result = self.db_manager.execute_query(
                reservations_query, 
                (nursery_id, start_date, end_date, start_date, end_date)
            )
            
            reservations = []
            for row in reservations_result:
                reservations.append({
                    'id': row[0],
                    'batch_id': row[1],
                    'seedling_type_id': row[2],
                    'customer_name': row[3],
                    'quantity': row[4],
                    'reservation_date': row[5],
                    'delivery_date': row[6],
                    'status': row[7],
                    'seedling_type_name': row[8],
                    'event_type': 'reservation'
                })
            
            # دمج جميع الأحداث وترتيبها حسب التاريخ
            all_events = []
            
            for batch in batches:
                all_events.append({
                    'date': batch['planting_date'],
                    'event_type': 'planting',
                    'event_id': batch['id'],
                    'details': batch
                })
                
                all_events.append({
                    'date': batch['expected_ready_date'],
                    'event_type': 'expected_ready',
                    'event_id': batch['id'],
                    'details': batch
                })
                
                if batch['actual_ready_date']:
                    all_events.append({
                        'date': batch['actual_ready_date'],
                        'event_type': 'actual_ready',
                        'event_id': batch['id'],
                        'details': batch
                    })
            
            for reservation in reservations:
                all_events.append({
                    'date': reservation['reservation_date'],
                    'event_type': 'reservation',
                    'event_id': reservation['id'],
                    'details': reservation
                })
                
                if reservation['delivery_date']:
                    all_events.append({
                        'date': reservation['delivery_date'],
                        'event_type': 'delivery',
                        'event_id': reservation['id'],
                        'details': reservation
                    })
            
            # ترتيب الأحداث حسب التاريخ
            all_events.sort(key=lambda x: x['date'])
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_nursery_schedule',
                entity_type='nursery',
                entity_id=str(nursery_id),
                details=f"Viewed schedule for nursery {nursery_id} from {start_date} to {end_date}"
            )
            
            return {
                'success': True,
                'nursery_id': nursery_id,
                'nursery_name': self.nurseries[nursery_id]['name'],
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'events': all_events,
                'event_counts': {
                    'batches': len(batches),
                    'reservations': len(reservations),
                    'total': len(all_events)
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting nursery schedule: {str(e)}'}
    
    def get_nursery_statistics(self, nursery_id, year, user_id):
        """
        الحصول على إحصائيات المشتل
        
        المعاملات:
            nursery_id (int): معرف المشتل
            year (int): السنة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: إحصائيات المشتل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_nursery_statistics'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # تحديد نطاق التاريخ
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            
            # الحصول على إحصائيات دفعات الشتلات
            batches_query = """
                SELECT COUNT(*), SUM(quantity)
                FROM seedling_batches
                WHERE nursery_id = %s AND planting_date BETWEEN %s AND %s
            """
            batches_result = self.db_manager.execute_query(
                batches_query, 
                (nursery_id, start_date, end_date)
            )
            
            batches_count = batches_result[0][0] if batches_result[0][0] else 0
            total_seedlings = batches_result[0][1] if batches_result[0][1] else 0
            
            # الحصول على إحصائيات دفعات الشتلات حسب الموسم
            season_query = """
                SELECT season, COUNT(*), SUM(quantity)
                FROM seedling_batches
                WHERE nursery_id = %s AND planting_date BETWEEN %s AND %s
                GROUP BY season
            """
            season_result = self.db_manager.execute_query(
                season_query, 
                (nursery_id, start_date, end_date)
            )
            
            seasons_data = {}
            for row in season_result:
                season = row[0]
                count = row[1]
                quantity = row[2] if row[2] else 0
                
                seasons_data[season] = {
                    'count': count,
                    'quantity': quantity
                }
            
            # الحصول على إحصائيات دفعات الشتلات حسب نوع الشتلة
            seedling_type_query = """
                SELECT b.seedling_type_id, s.name, s.category, COUNT(*), SUM(b.quantity)
                FROM seedling_batches b
                JOIN seedling_types s ON b.seedling_type_id = s.id
                WHERE b.nursery_id = %s AND b.planting_date BETWEEN %s AND %s
                GROUP BY b.seedling_type_id, s.name, s.category
            """
            seedling_type_result = self.db_manager.execute_query(
                seedling_type_query, 
                (nursery_id, start_date, end_date)
            )
            
            seedling_types_data = []
            for row in seedling_type_result:
                seedling_type_id = row[0]
                seedling_type_name = row[1]
                category = row[2]
                count = row[3]
                quantity = row[4] if row[4] else 0
                
                seedling_types_data.append({
                    'seedling_type_id': seedling_type_id,
                    'seedling_type_name': seedling_type_name,
                    'category': category,
                    'count': count,
                    'quantity': quantity
                })
            
            # الحصول على إحصائيات الحجوزات
            reservations_query = """
                SELECT COUNT(*), SUM(quantity)
                FROM seedling_reservations
                WHERE nursery_id = %s AND reservation_date BETWEEN %s AND %s
            """
            reservations_result = self.db_manager.execute_query(
                reservations_query, 
                (nursery_id, start_date, end_date)
            )
            
            reservations_count = reservations_result[0][0] if reservations_result[0][0] else 0
            reserved_seedlings = reservations_result[0][1] if reservations_result[0][1] else 0
            
            # الحصول على إحصائيات الحجوزات حسب الحالة
            status_query = """
                SELECT status, COUNT(*), SUM(quantity)
                FROM seedling_reservations
                WHERE nursery_id = %s AND reservation_date BETWEEN %s AND %s
                GROUP BY status
            """
            status_result = self.db_manager.execute_query(
                status_query, 
                (nursery_id, start_date, end_date)
            )
            
            status_data = {}
            for row in status_result:
                status = row[0]
                count = row[1]
                quantity = row[2] if row[2] else 0
                
                status_data[status] = {
                    'count': count,
                    'quantity': quantity
                }
            
            # الحصول على إحصائيات التكلفة
            cost_result = self.cost_calculator.calculate_total_nursery_cost(
                nursery_id, start_date, end_date, user_id
            )
            
            total_cost = cost_result.get('costs', {}).get('total', 0) if cost_result.get('success', False) else 0
            cost_per_seedling = cost_result.get('metrics', {}).get('cost_per_seedling', 0) if cost_result.get('success', False) else 0
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='view_nursery_statistics',
                entity_type='nursery',
                entity_id=str(nursery_id),
                details=f"Viewed statistics for nursery {nursery_id} for year {year}"
            )
            
            return {
                'success': True,
                'nursery_id': nursery_id,
                'nursery_name': self.nurseries[nursery_id]['name'],
                'year': year,
                'batches': {
                    'count': batches_count,
                    'total_seedlings': total_seedlings,
                    'by_season': seasons_data,
                    'by_seedling_type': seedling_types_data
                },
                'reservations': {
                    'count': reservations_count,
                    'reserved_seedlings': reserved_seedlings,
                    'by_status': status_data
                },
                'costs': {
                    'total_cost': total_cost,
                    'cost_per_seedling': cost_per_seedling
                },
                'capacity': {
                    'total': self.nurseries[nursery_id]['total_capacity'],
                    'current': self.nurseries[nursery_id]['current_capacity'],
                    'available': self.nurseries[nursery_id]['total_capacity'] - self.nurseries[nursery_id]['current_capacity'],
                    'utilization_percentage': round((self.nurseries[nursery_id]['current_capacity'] / self.nurseries[nursery_id]['total_capacity']) * 100, 2) if self.nurseries[nursery_id]['total_capacity'] > 0 else 0
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error getting nursery statistics: {str(e)}'}
    
    def generate_nursery_report(self, nursery_id, start_date, end_date, report_type, user_id):
        """
        إنشاء تقرير للمشتل
        
        المعاملات:
            nursery_id (int): معرف المشتل
            start_date (str): تاريخ البداية (YYYY-MM-DD)
            end_date (str): تاريخ النهاية (YYYY-MM-DD)
            report_type (str): نوع التقرير (summary, detailed, financial)
            user_id (int): معرف المستخدم
            
        العائد:
            dict: تقرير المشتل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'generate_nursery_report'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود المشتل
            if nursery_id not in self.nurseries:
                return {'success': False, 'message': 'Nursery not found'}
            
            # الحصول على بيانات المشتل
            nursery = self.nurseries[nursery_id]
            
            # إنشاء التقرير حسب النوع
            if report_type == 'summary':
                # الحصول على ملخص دفعات الشتلات
                batches_query = """
                    SELECT COUNT(*), SUM(quantity)
                    FROM seedling_batches
                    WHERE nursery_id = %s AND planting_date BETWEEN %s AND %s
                """
                batches_result = self.db_manager.execute_query(
                    batches_query, 
                    (nursery_id, start_date, end_date)
                )
                
                batches_count = batches_result[0][0] if batches_result[0][0] else 0
                total_seedlings = batches_result[0][1] if batches_result[0][1] else 0
                
                # الحصول على ملخص الحجوزات
                reservations_query = """
                    SELECT COUNT(*), SUM(quantity)
                    FROM seedling_reservations
                    WHERE nursery_id = %s AND reservation_date BETWEEN %s AND %s
                """
                reservations_result = self.db_manager.execute_query(
                    reservations_query, 
                    (nursery_id, start_date, end_date)
                )
                
                reservations_count = reservations_result[0][0] if reservations_result[0][0] else 0
                reserved_seedlings = reservations_result[0][1] if reservations_result[0][1] else 0
                
                # الحصول على ملخص التسليمات
                deliveries_query = """
                    SELECT COUNT(*), SUM(quantity)
                    FROM seedling_reservations
                    WHERE nursery_id = %s AND delivery_date BETWEEN %s AND %s AND status = 'delivered'
                """
                deliveries_result = self.db_manager.execute_query(
                    deliveries_query, 
                    (nursery_id, start_date, end_date)
                )
                
                deliveries_count = deliveries_result[0][0] if deliveries_result[0][0] else 0
                delivered_seedlings = deliveries_result[0][1] if deliveries_result[0][1] else 0
                
                # إعداد التقرير
                report = {
                    'nursery': nursery,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    },
                    'summary': {
                        'batches': {
                            'count': batches_count,
                            'total_seedlings': total_seedlings
                        },
                        'reservations': {
                            'count': reservations_count,
                            'reserved_seedlings': reserved_seedlings
                        },
                        'deliveries': {
                            'count': deliveries_count,
                            'delivered_seedlings': delivered_seedlings
                        },
                        'capacity': {
                            'total': nursery['total_capacity'],
                            'current': nursery['current_capacity'],
                            'available': nursery['total_capacity'] - nursery['current_capacity'],
                            'utilization_percentage': round((nursery['current_capacity'] / nursery['total_capacity']) * 100, 2) if nursery['total_capacity'] > 0 else 0
                        }
                    }
                }
                
            elif report_type == 'detailed':
                # الحصول على تفاصيل دفعات الشتلات
                batches_query = """
                    SELECT b.id, b.seedling_type_id, s.name as seedling_type_name, 
                           s.category, b.quantity, b.planting_date, b.expected_ready_date, 
                           b.actual_ready_date, b.status, b.season, b.notes
                    FROM seedling_batches b
                    JOIN seedling_types s ON b.seedling_type_id = s.id
                    WHERE b.nursery_id = %s AND b.planting_date BETWEEN %s AND %s
                    ORDER BY b.planting_date
                """
                batches_result = self.db_manager.execute_query(
                    batches_query, 
                    (nursery_id, start_date, end_date)
                )
                
                batches = []
                for row in batches_result:
                    batch_id = row[0]
                    
                    # الحصول على بيانات الحجوزات
                    reservations_query = """
                        SELECT id, customer_id, customer_name, quantity, 
                               reservation_date, delivery_date, status, notes
                        FROM seedling_reservations
                        WHERE batch_id = %s
                        ORDER BY reservation_date
                    """
                    reservations_result = self.db_manager.execute_query(reservations_query, (batch_id,))
                    
                    reservations = []
                    for res_row in reservations_result:
                        reservations.append({
                            'id': res_row[0],
                            'customer_id': res_row[1],
                            'customer_name': res_row[2],
                            'quantity': res_row[3],
                            'reservation_date': res_row[4],
                            'delivery_date': res_row[5],
                            'status': res_row[6],
                            'notes': res_row[7]
                        })
                    
                    batches.append({
                        'id': batch_id,
                        'seedling_type_id': row[1],
                        'seedling_type_name': row[2],
                        'category': row[3],
                        'quantity': row[4],
                        'planting_date': row[5],
                        'expected_ready_date': row[6],
                        'actual_ready_date': row[7],
                        'status': row[8],
                        'season': row[9],
                        'notes': row[10],
                        'reservations': reservations
                    })
                
                # الحصول على تفاصيل الحجوزات
                reservations_query = """
                    SELECT r.id, r.batch_id, r.seedling_type_id, s.name as seedling_type_name, 
                           r.customer_id, r.customer_name, r.quantity, r.reservation_date, 
                           r.delivery_date, r.status, r.notes
                    FROM seedling_reservations r
                    JOIN seedling_types s ON r.seedling_type_id = s.id
                    WHERE r.nursery_id = %s AND r.reservation_date BETWEEN %s AND %s
                    ORDER BY r.reservation_date
                """
                reservations_result = self.db_manager.execute_query(
                    reservations_query, 
                    (nursery_id, start_date, end_date)
                )
                
                reservations = []
                for row in reservations_result:
                    reservations.append({
                        'id': row[0],
                        'batch_id': row[1],
                        'seedling_type_id': row[2],
                        'seedling_type_name': row[3],
                        'customer_id': row[4],
                        'customer_name': row[5],
                        'quantity': row[6],
                        'reservation_date': row[7],
                        'delivery_date': row[8],
                        'status': row[9],
                        'notes': row[10]
                    })
                
                # إعداد التقرير
                report = {
                    'nursery': nursery,
                    'period': {
                        'start_date': start_date,
                        'end_date': end_date
                    },
                    'details': {
                        'batches': batches,
                        'reservations': reservations
                    }
                }
                
            elif report_type == 'financial':
                # الحصول على التقرير المالي
                cost_result = self.cost_calculator.calculate_total_nursery_cost(
                    nursery_id, start_date, end_date, user_id
                )
                
                if not cost_result.get('success', False):
                    return {'success': False, 'message': 'Failed to generate financial report'}
                
                # إعداد التقرير
                report = {
                    'nursery': nursery,
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
                action_type='generate_nursery_report',
                entity_type='nursery',
                entity_id=str(nursery_id),
                details=f"Generated {report_type} report for nursery {nursery_id} from {start_date} to {end_date}"
            )
            
            return {
                'success': True,
                'report_type': report_type,
                'report': report,
                'generation_date': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error generating nursery report: {str(e)}'}
    
    def export_nursery_report(self, report_data, file_format, file_path, user_id):
        """
        تصدير تقرير المشتل
        
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
            if not self.auth_manager.has_permission(user_id, 'export_nursery_report'):
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
                    'Category': ['Batches', 'Reservations', 'Deliveries'],
                    'Count': [
                        summary.get('batches', {}).get('count', 0),
                        summary.get('reservations', {}).get('count', 0),
                        summary.get('deliveries', {}).get('count', 0)
                    ],
                    'Quantity': [
                        summary.get('batches', {}).get('total_seedlings', 0),
                        summary.get('reservations', {}).get('reserved_seedlings', 0),
                        summary.get('deliveries', {}).get('delivered_seedlings', 0)
                    ]
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
                
                # تحويل بيانات دفعات الشتلات إلى DataFrame
                batches = details.get('batches', [])
                batches_data = []
                
                for batch in batches:
                    batches_data.append({
                        'ID': batch.get('id'),
                        'Seedling Type': batch.get('seedling_type_name'),
                        'Category': batch.get('category'),
                        'Quantity': batch.get('quantity'),
                        'Planting Date': batch.get('planting_date'),
                        'Expected Ready Date': batch.get('expected_ready_date'),
                        'Actual Ready Date': batch.get('actual_ready_date'),
                        'Status': batch.get('status'),
                        'Season': batch.get('season'),
                        'Notes': batch.get('notes')
                    })
                
                batches_df = pd.DataFrame(batches_data)
                
                # تحويل بيانات الحجوزات إلى DataFrame
                reservations = details.get('reservations', [])
                reservations_data = []
                
                for reservation in reservations:
                    reservations_data.append({
                        'ID': reservation.get('id'),
                        'Batch ID': reservation.get('batch_id'),
                        'Seedling Type': reservation.get('seedling_type_name'),
                        'Customer': reservation.get('customer_name'),
                        'Quantity': reservation.get('quantity'),
                        'Reservation Date': reservation.get('reservation_date'),
                        'Delivery Date': reservation.get('delivery_date'),
                        'Status': reservation.get('status'),
                        'Notes': reservation.get('notes')
                    })
                
                reservations_df = pd.DataFrame(reservations_data)
                
                # تصدير التقرير حسب الصيغة المطلوبة
                if file_format == 'csv':
                    # تصدير كل جدول إلى ملف منفصل
                    batches_df.to_csv(f"{file_path}_batches.csv", index=False, encoding='utf-8')
                    reservations_df.to_csv(f"{file_path}_reservations.csv", index=False, encoding='utf-8')
                elif file_format == 'excel':
                    # تصدير جميع الجداول إلى ملف Excel واحد
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        batches_df.to_excel(writer, sheet_name='Batches', index=False)
                        reservations_df.to_excel(writer, sheet_name='Reservations', index=False)
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
                action_type='export_nursery_report',
                entity_type='nursery_report',
                entity_id=f"{report.get('nursery', {}).get('id')}_{report_type}",
                details=f"Exported {report_type} report to {file_path} in {file_format} format"
            )
            
            return {
                'success': True,
                'message': f'Nursery report exported successfully to {file_path}',
                'file_path': file_path,
                'file_format': file_format
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error exporting nursery report: {str(e)}'}
    
    def _determine_season(self, date_str):
        """
        تحديد الموسم بناءً على التاريخ
        
        المعاملات:
            date_str (str): التاريخ (YYYY-MM-DD)
            
        العائد:
            str: الموسم (summer, winter)
        """
        try:
            date_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            month = date_obj.month
            
            if month in self.seasons['summer']['months']:
                return 'summer'
            else:
                return 'winter'
        except:
            # في حالة حدوث خطأ، نعيد الموسم الافتراضي
            return 'summer'
