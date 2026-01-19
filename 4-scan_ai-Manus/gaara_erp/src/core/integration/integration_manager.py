#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التكامل مع النظام الزراعي لنظام Gaara ERP
"""

import os
import logging
import json
import requests
import time
import threading
from datetime import datetime

# إعداد التسجيل
logger = logging.getLogger(__name__)

class IntegrationManager:
    """مدير التكامل مع النظام الزراعي لنظام Gaara ERP"""
    
    _instance = None
    
    def __new__(cls):
        """تنفيذ نمط Singleton لضمان وجود نسخة واحدة فقط من مدير التكامل"""
        if cls._instance is None:
            cls._instance = super(IntegrationManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """تهيئة مدير التكامل"""
        if self._initialized:
            return
            
        from .config.config_manager import ConfigManager
        from .database.db_manager import DatabaseManager
        
        # الحصول على مدير التكوين وقاعدة البيانات
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        
        # إعدادات التكامل
        self.integration_enabled = self.config_manager.get('integration.agricultural_system.enabled', True)
        self.api_url = self.config_manager.get('integration.agricultural_system.api_url', 'http://localhost:8000/api')
        self.api_key = self.config_manager.get('integration.agricultural_system.api_key', '')
        self.sync_interval = self.config_manager.get('integration.agricultural_system.sync_interval', 3600)  # بالثواني
        
        # حالة المزامنة
        self.is_syncing = False
        self.last_sync_time = None
        self.sync_thread = None
        
        # بدء المزامنة التلقائية إذا كانت ممكنة
        if self.integration_enabled:
            self.start_auto_sync()
        
        self._initialized = True
        logger.info("تم تهيئة مدير التكامل بنجاح")
    
    def start_auto_sync(self):
        """بدء المزامنة التلقائية"""
        if self.sync_thread is not None and self.sync_thread.is_alive():
            logger.warning("المزامنة التلقائية قيد التشغيل بالفعل")
            return
        
        self.sync_thread = threading.Thread(target=self._auto_sync_worker, daemon=True)
        self.sync_thread.start()
        logger.info("تم بدء المزامنة التلقائية")
    
    def stop_auto_sync(self):
        """إيقاف المزامنة التلقائية"""
        if self.sync_thread is None or not self.sync_thread.is_alive():
            logger.warning("المزامنة التلقائية ليست قيد التشغيل")
            return
        
        self.integration_enabled = False
        self.sync_thread.join(timeout=5)
        self.sync_thread = None
        logger.info("تم إيقاف المزامنة التلقائية")
    
    def _auto_sync_worker(self):
        """عامل المزامنة التلقائية"""
        while self.integration_enabled:
            try:
                # المزامنة
                self.sync_all()
                
                # الانتظار حتى الفاصل الزمني التالي
                time.sleep(self.sync_interval)
            except Exception as e:
                logger.error(f"خطأ في عامل المزامنة التلقائية: {str(e)}")
                time.sleep(60)  # الانتظار لمدة دقيقة قبل المحاولة مرة أخرى
    
    def sync_all(self):
        """مزامنة جميع البيانات"""
        if self.is_syncing:
            logger.warning("المزامنة قيد التنفيذ بالفعل")
            return False
        
        try:
            self.is_syncing = True
            start_time = datetime.now()
            
            # تسجيل بدء المزامنة
            logger.info("بدء مزامنة جميع البيانات")
            
            # مزامنة البيانات من النظام الزراعي
            self.sync_diseases()
            self.sync_nutrients()
            self.sync_plants()
            self.sync_treatments()
            
            # مزامنة البيانات من نظام Gaara ERP
            self.sync_inventory_to_agricultural()
            self.sync_nursery_to_agricultural()
            
            # تحديث وقت آخر مزامنة
            self.last_sync_time = datetime.now()
            duration = (self.last_sync_time - start_time).total_seconds()
            
            # تسجيل اكتمال المزامنة
            logger.info(f"اكتملت مزامنة جميع البيانات في {duration:.2f} ثانية")
            
            # تسجيل المزامنة في قاعدة البيانات
            self._log_sync("all", "success", f"اكتملت المزامنة في {duration:.2f} ثانية")
            
            return True
        except Exception as e:
            logger.error(f"فشل في مزامنة جميع البيانات: {str(e)}")
            self._log_sync("all", "error", str(e))
            return False
        finally:
            self.is_syncing = False
    
    def sync_diseases(self):
        """مزامنة بيانات الأمراض من النظام الزراعي"""
        try:
            # الحصول على بيانات الأمراض من النظام الزراعي
            response = self._api_request("GET", "/diseases")
            
            if response.status_code != 200:
                logger.error(f"فشل في الحصول على بيانات الأمراض: {response.status_code} - {response.text}")
                self._log_sync("diseases", "error", f"فشل في الحصول على البيانات: {response.status_code}")
                return False
            
            diseases = response.json()
            
            # معالجة كل مرض
            for disease in diseases:
                self._process_disease(disease)
            
            logger.info(f"تمت مزامنة {len(diseases)} مرض بنجاح")
            self._log_sync("diseases", "success", f"تمت مزامنة {len(diseases)} مرض")
            return True
        except Exception as e:
            logger.error(f"فشل في مزامنة بيانات الأمراض: {str(e)}")
            self._log_sync("diseases", "error", str(e))
            return False
    
    def _process_disease(self, disease):
        """معالجة بيانات المرض"""
        try:
            # التحقق من وجود المرض في نظام التكامل
            query = """
                SELECT erp_entity_id
                FROM integration.entity_mapping
                WHERE agri_entity_type = 'disease' AND agri_entity_id = %s
            """
            result = self.db_manager.execute_query(query, (str(disease['id']),))
            
            if result:
                # تحديث المرض الموجود
                erp_disease_id = result[0]['erp_entity_id']
                self._update_disease(erp_disease_id, disease)
            else:
                # إنشاء مرض جديد
                erp_disease_id = self._create_disease(disease)
                
                # إضافة تعيين الكيان
                self._add_entity_mapping('disease', str(disease['id']), 'disease', str(erp_disease_id))
            
            return erp_disease_id
        except Exception as e:
            logger.error(f"فشل في معالجة بيانات المرض {disease['id']}: {str(e)}")
            return None
    
    def _create_disease(self, disease):
        """إنشاء مرض جديد في نظام Gaara ERP"""
        # هذه مجرد وظيفة توضيحية، يجب تعديلها حسب هيكل البيانات الفعلي
        return "new_disease_id"
    
    def _update_disease(self, erp_disease_id, disease):
        """تحديث مرض موجود في نظام Gaara ERP"""
        # هذه مجرد وظيفة توضيحية، يجب تعديلها حسب هيكل البيانات الفعلي
        pass
    
    def sync_nutrients(self):
        """مزامنة بيانات العناصر الغذائية من النظام الزراعي"""
        # مشابهة لوظيفة sync_diseases
        return True
    
    def sync_plants(self):
        """مزامنة بيانات النباتات من النظام الزراعي"""
        # مشابهة لوظيفة sync_diseases
        return True
    
    def sync_treatments(self):
        """مزامنة بيانات العلاجات من النظام الزراعي"""
        # مشابهة لوظيفة sync_diseases
        return True
    
    def sync_inventory_to_agricultural(self):
        """مزامنة بيانات المخزون من نظام Gaara ERP إلى النظام الزراعي"""
        try:
            # الحصول على بيانات المخزون التي تحتاج إلى مزامنة
            query = """
                SELECT i.inventory_id, i.product_id, i.quantity, i.last_updated
                FROM erp.inventory i
                JOIN erp.products p ON i.product_id = p.product_id
                WHERE p.is_agricultural = TRUE
                AND (i.last_sync IS NULL OR i.last_updated > i.last_sync)
            """
            inventory_items = self.db_manager.execute_query(query)
            
            if not inventory_items:
                logger.info("لا توجد عناصر مخزون تحتاج إلى مزامنة")
                return True
            
            # مزامنة كل عنصر مخزون
            for item in inventory_items:
                self._sync_inventory_item(item)
            
            logger.info(f"تمت مزامنة {len(inventory_items)} عنصر مخزون بنجاح")
            self._log_sync("inventory_to_agricultural", "success", f"تمت مزامنة {len(inventory_items)} عنصر مخزون")
            return True
        except Exception as e:
            logger.error(f"فشل في مزامنة بيانات المخزون: {str(e)}")
            self._log_sync("inventory_to_agricultural", "error", str(e))
            return False
    
    def _sync_inventory_item(self, item):
        """مزامنة عنصر مخزون واحد"""
        try:
            # الحصول على معرف المنتج في النظام الزراعي
            query = """
                SELECT agri_entity_id
                FROM integration.entity_mapping
                WHERE erp_entity_type = 'product' AND erp_entity_id = %s
            """
            result = self.db_manager.execute_query(query, (str(item['product_id']),))
            
            if not result:
                logger.warning(f"لا يوجد تعيين للمنتج {item['product_id']} في النظام الزراعي")
                return False
            
            agri_product_id = result[0]['agri_entity_id']
            
            # إرسال تحديث المخزون إلى النظام الزراعي
            data = {
                'product_id': agri_product_id,
                'quantity': item['quantity']
            }
            
            response = self._api_request("POST", "/inventory/update", data)
            
            if response.status_code != 200:
                logger.error(f"فشل في تحديث المخزون في النظام الزراعي: {response.status_code} - {response.text}")
                return False
            
            # تحديث وقت آخر مزامنة
            update_query = """
                UPDATE erp.inventory
                SET last_sync = CURRENT_TIMESTAMP
                WHERE inventory_id = %s
            """
            self.db_manager.execute_query(update_query, (item['inventory_id'],), fetch=False)
            
            logger.info(f"تم تحديث المخزون للمنتج {item['product_id']} في النظام الزراعي")
            return True
        except Exception as e:
            logger.error(f"فشل في مزامنة عنصر المخزون {item['inventory_id']}: {str(e)}")
            return False
    
    def sync_nursery_to_agricultural(self):
        """مزامنة بيانات المشاتل من نظام Gaara ERP إلى النظام الزراعي"""
        # مشابهة لوظيفة sync_inventory_to_agricultural
        return True
    
    def _api_request(self, method, endpoint, data=None):
        """إرسال طلب إلى واجهة برمجة التطبيقات للنظام الزراعي"""
        url = f"{self.api_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"طريقة HTTP غير مدعومة: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في طلب API: {str(e)}")
            raise
    
    def _log_sync(self, sync_type, status, message=None):
        """تسجيل عملية المزامنة في قاعدة البيانات"""
        try:
            query = """
                INSERT INTO integration.sync_log
                (sync_type, source_system, target_system, status, message, started_at, completed_at, duration_ms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            started_at = self.last_sync_time or datetime.now()
            completed_at = datetime.now()
            duration_ms = int((completed_at - started_at).total_seconds() * 1000)
            
            params = (
                sync_type,
                'erp',
                'agricultural',
                status,
                message,
                started_at,
                completed_at,
                duration_ms
            )
            
            self.db_manager.execute_query(query, params, fetch=False)
        except Exception as e:
            logger.error(f"فشل في تسجيل المزامنة: {str(e)}")
    
    def _add_entity_mapping(self, agri_entity_type, agri_entity_id, erp_entity_type, erp_entity_id):
        """إضافة تعيين كيان جديد"""
        try:
            query = """
                INSERT INTO integration.entity_mapping
                (agri_entity_type, agri_entity_id, erp_entity_type, erp_entity_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (agri_entity_type, agri_entity_id, erp_entity_type) DO UPDATE
                SET erp_entity_id = EXCLUDED.erp_entity_id, updated_at = CURRENT_TIMESTAMP
            """
            
            params = (agri_entity_type, agri_entity_id, erp_entity_type, erp_entity_id)
            self.db_manager.execute_query(query, params, fetch=False)
            
            logger.info(f"تم إضافة تعيين الكيان: {agri_entity_type}/{agri_entity_id} -> {erp_entity_type}/{erp_entity_id}")
            return True
        except Exception as e:
            logger.error(f"فشل في إضافة تعيين الكيان: {str(e)}")
            return False
    
    def get_sync_status(self):
        """الحصول على حالة المزامنة"""
        try:
            query = """
                SELECT sync_type, status, message, started_at, completed_at, duration_ms
                FROM integration.sync_log
                ORDER BY completed_at DESC
                LIMIT 10
            """
            
            return {
                'is_syncing': self.is_syncing,
                'last_sync_time': self.last_sync_time,
                'integration_enabled': self.integration_enabled,
                'sync_interval': self.sync_interval,
                'recent_logs': self.db_manager.execute_query(query)
            }
        except Exception as e:
            logger.error(f"فشل في الحصول على حالة المزامنة: {str(e)}")
            return {
                'is_syncing': self.is_syncing,
                'last_sync_time': self.last_sync_time,
                'integration_enabled': self.integration_enabled,
                'sync_interval': self.sync_interval,
                'recent_logs': []
            }

# نموذج استخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # تهيئة مدير التكامل
    integration_manager = IntegrationManager()
    
    # مثال على المزامنة
    integration_manager.sync_all()
    
    # مثال على الحصول على حالة المزامنة
    status = integration_manager.get_sync_status()
    print(f"حالة المزامنة: {'قيد التنفيذ' if status['is_syncing'] else 'غير نشطة'}")
    print(f"آخر مزامنة: {status['last_sync_time']}")
    print(f"المزامنة التلقائية: {'ممكّنة' if status['integration_enabled'] else 'معطّلة'}")
    print(f"فاصل المزامنة: {status['sync_interval']} ثانية")
