"""
وحدة تكامل الذكاء الاصطناعي بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي

هذه الوحدة مسؤولة عن:
1. إدارة طلبات تشخيص الأمراض النباتية
2. إدارة طلبات التهجين النباتي
3. إدارة طلبات تحليل التربة
4. إدارة طلبات توقعات الإنتاج
5. مراقبة أداء نماذج الذكاء الاصطناعي
"""

import os
import json
import logging
import requests
import base64
import time
import threading
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from langfuse import Langfuse
from evidently.model_monitoring import ModelMonitoring
from evidently.metrics import DataDriftTable, DataQualityTable, ClassificationPerformanceTable

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ai_integration")

class AIIntegration:
    """فئة تكامل الذكاء الاصطناعي بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي"""
    
    def __init__(self, config_path=None, db_integration=None):
        """
        تهيئة وحدة تكامل الذكاء الاصطناعي
        
        المعلمات:
            config_path (str): مسار ملف التكوين (اختياري)
            db_integration: كائن تكامل قواعد البيانات (اختياري)
        """
        self.config = self._load_config(config_path)
        self.db_integration = db_integration
        self.api_base_url = self.config.get('api_base_url', 'http://localhost:8000/api')
        self.api_key = self.config.get('api_key', '')
        self.temp_dir = self.config.get('temp_dir', '/tmp/ai_integration')
        
        # إنشاء مجلد مؤقت إذا لم يكن موجوداً
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # إعداد Langfuse لتتبع الأداء
        langfuse_config = self.config.get('langfuse', {})
        self.langfuse = None
        if langfuse_config.get('enabled', False):
            try:
                self.langfuse = Langfuse(
                    public_key=langfuse_config.get('public_key', ''),
                    secret_key=langfuse_config.get('secret_key', ''),
                    host=langfuse_config.get('host', 'https://cloud.langfuse.com')
                )
                logger.info("تم تهيئة Langfuse بنجاح")
            except Exception as e:
                logger.error(f"خطأ في تهيئة Langfuse: {str(e)}")
        
        # إعداد Evidently لمراقبة انحراف البيانات
        evidently_config = self.config.get('evidently', {})
        self.evidently_enabled = evidently_config.get('enabled', False)
        self.evidently_reference_data = {}
        self.evidently_current_data = {}
        
        if self.evidently_enabled:
            try:
                # تحميل بيانات المرجع
                reference_data_path = evidently_config.get('reference_data_path', '')
                if reference_data_path and os.path.exists(reference_data_path):
                    with open(reference_data_path, 'r') as f:
                        self.evidently_reference_data = json.load(f)
                logger.info("تم تهيئة Evidently بنجاح")
            except Exception as e:
                logger.error(f"خطأ في تهيئة Evidently: {str(e)}")
        
        # إعداد مراقبة الأداء
        self.performance_metrics = {
            'disease_detection': {
                'requests': 0,
                'successful': 0,
                'failed': 0,
                'avg_response_time': 0,
                'total_response_time': 0,
                'confidence_scores': []
            },
            'breeding': {
                'requests': 0,
                'successful': 0,
                'failed': 0,
                'avg_response_time': 0,
                'total_response_time': 0,
                'success_probabilities': []
            },
            'soil_analysis': {
                'requests': 0,
                'successful': 0,
                'failed': 0,
                'avg_response_time': 0,
                'total_response_time': 0
            },
            'yield_prediction': {
                'requests': 0,
                'successful': 0,
                'failed': 0,
                'avg_response_time': 0,
                'total_response_time': 0,
                'prediction_errors': []
            }
        }
        
        # قائمة الخيوط النشطة
        self.active_threads = []
        
        logger.info("تم تهيئة وحدة تكامل الذكاء الاصطناعي بنجاح")
    
    def _load_config(self, config_path):
        """
        تحميل ملف التكوين
        
        المعلمات:
            config_path (str): مسار ملف التكوين
            
        العوائد:
            dict: بيانات التكوين
        """
        default_config = {
            'api_base_url': 'http://localhost:8000/api',
            'api_key': '',
            'temp_dir': '/tmp/ai_integration',
            'request_timeout': 60,
            'max_retries': 3,
            'retry_delay': 5,
            'models': {
                'disease_detection': {
                    'free': 'resnet50_basic',
                    'premium': 'efficientnet_advanced',
                    'default': 'resnet50_basic'
                },
                'breeding': {
                    'free': 'pybrops_basic',
                    'premium': 'pybrops_advanced',
                    'default': 'pybrops_basic'
                },
                'soil_analysis': {
                    'free': 'soil_analyzer_basic',
                    'premium': 'soil_analyzer_advanced',
                    'default': 'soil_analyzer_basic'
                },
                'yield_prediction': {
                    'free': 'yield_predictor_basic',
                    'premium': 'yield_predictor_advanced',
                    'default': 'yield_predictor_basic'
                }
            },
            'langfuse': {
                'enabled': False,
                'public_key': '',
                'secret_key': '',
                'host': 'https://cloud.langfuse.com'
            },
            'evidently': {
                'enabled': False,
                'reference_data_path': '',
                'drift_threshold': 0.05,
                'monitoring_interval': 86400  # يوم واحد بالثواني
            },
            'notification': {
                'enabled': True,
                'error_threshold': 0.1,  # نسبة الأخطاء التي تستدعي التنبيه
                'drift_threshold': 0.05,  # نسبة الانحراف التي تستدعي التنبيه
                'recipients': []
            }
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
    
    def _make_api_request(self, endpoint, method='GET', data=None, files=None, params=None):
        """
        إجراء طلب API
        
        المعلمات:
            endpoint (str): نقطة النهاية للطلب
            method (str): طريقة الطلب (GET, POST, PUT, DELETE)
            data (dict): بيانات الطلب (اختياري)
            files (dict): ملفات الطلب (اختياري)
            params (dict): معلمات الطلب (اختياري)
            
        العوائد:
            dict: استجابة API
        """
        url = f"{self.api_base_url}/{endpoint.lstrip('/')}"
        headers = {
            'Authorization': f"Bearer {self.api_key}"
        }
        
        if not files:
            headers['Content-Type'] = 'application/json'
        
        timeout = self.config.get('request_timeout', 60)
        max_retries = self.config.get('max_retries', 3)
        retry_delay = self.config.get('retry_delay', 5)
        
        # تسجيل الطلب في Langfuse
        trace_id = None
        if self.langfuse:
            trace = self.langfuse.trace(
                name=f"api_request_{endpoint}",
                metadata={
                    'endpoint': endpoint,
                    'method': method,
                    'params': params
                }
            )
            trace_id = trace.id
        
        # محاولة إجراء الطلب مع إعادة المحاولة
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                if method == 'GET':
                    response = requests.get(url, headers=headers, params=params, timeout=timeout)
                elif method == 'POST':
                    if files:
                        # إذا كان هناك ملفات، لا نقوم بتحويل البيانات إلى JSON
                        response = requests.post(url, headers=headers, data=data, files=files, params=params, timeout=timeout)
                    else:
                        response = requests.post(url, headers=headers, json=data, params=params, timeout=timeout)
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=data, params=params, timeout=timeout)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=headers, params=params, timeout=timeout)
                else:
                    raise ValueError(f"طريقة غير مدعومة: {method}")
                
                end_time = time.time()
                response_time = end_time - start_time
                
                # تسجيل الاستجابة في Langfuse
                if self.langfuse and trace_id:
                    self.langfuse.span(
                        trace_id=trace_id,
                        name="api_response",
                        start_time=start_time,
                        end_time=end_time,
                        metadata={
                            'status_code': response.status_code,
                            'response_time': response_time
                        }
                    )
                
                # التحقق من نجاح الطلب
                response.raise_for_status()
                
                # تحليل الاستجابة
                if response.content:
                    result = response.json()
                else:
                    result = {'status': 'success'}
                
                logger.info(f"تم إجراء طلب API بنجاح: {endpoint}")
                return result
            
            except requests.exceptions.RequestException as e:
                logger.error(f"خطأ في طلب API ({attempt+1}/{max_retries}): {endpoint} - {str(e)}")
                
                # تسجيل الخطأ في Langfuse
                if self.langfuse and trace_id:
                    self.langfuse.event(
                        trace_id=trace_id,
                        name="api_error",
                        metadata={
                            'error': str(e),
                            'attempt': attempt + 1
                        }
                    )
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    # تسجيل فشل الطلب في Langfuse
                    if self.langfuse and trace_id:
                        self.langfuse.update(
                            trace_id=trace_id,
                            status="failure"
                        )
                    
                    raise
        
        return None
    
    def detect_disease(self, image_path, plant_id=None, user_id=None, use_premium=False):
        """
        تشخيص مرض نباتي من صورة
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            plant_id (int): معرف النبات (اختياري)
            user_id (int): معرف المستخدم (اختياري)
            use_premium (bool): استخدام النموذج المتقدم (اختياري)
            
        العوائد:
            dict: نتيجة التشخيص
        """
        if not os.path.exists(image_path):
            raise ValueError(f"ملف الصورة غير موجود: {image_path}")
        
        # تحديد النموذج المستخدم
        model = self.config['models']['disease_detection']['premium'] if use_premium else self.config['models']['disease_detection']['default']
        
        # إعداد بيانات الطلب
        data = {
            'plant_id': plant_id,
            'user_id': user_id,
            'model': model
        }
        
        # إعداد ملف الصورة
        files = {
            'image': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
        }
        
        # تحديث إحصائيات الأداء
        self.performance_metrics['disease_detection']['requests'] += 1
        
        try:
            # إجراء طلب API
            start_time = time.time()
            result = self._make_api_request('disease/detect', method='POST', data=data, files=files)
            end_time = time.time()
            
            # تحديث إحصائيات الأداء
            response_time = end_time - start_time
            self.performance_metrics['disease_detection']['successful'] += 1
            self.performance_metrics['disease_detection']['total_response_time'] += response_time
            self.performance_metrics['disease_detection']['avg_response_time'] = (
                self.performance_metrics['disease_detection']['total_response_time'] / 
                self.performance_metrics['disease_detection']['successful']
            )
            
            if 'confidence' in result:
                self.performance_metrics['disease_detection']['confidence_scores'].append(result['confidence'])
            
            # حفظ نتيجة التشخيص في قاعدة البيانات
            if self.db_integration and result.get('disease_id') and plant_id:
                self._save_disease_detection(plant_id, result)
            
            # جمع بيانات لمراقبة الانحراف
            if self.evidently_enabled:
                self._collect_data_for_drift_monitoring('disease_detection', result)
            
            logger.info(f"تم تشخيص المرض بنجاح: {result.get('disease_name', 'غير معروف')}")
            return result
        
        except Exception as e:
            # تحديث إحصائيات الأداء
            self.performance_metrics['disease_detection']['failed'] += 1
            
            logger.error(f"خطأ في تشخيص المرض: {str(e)}")
            raise
        finally:
            # إغلاق ملف الصورة
            files['image'][1].close()
    
    def detect_disease_batch(self, image_paths, plant_ids=None, user_id=None, use_premium=False):
        """
        تشخيص أمراض نباتية من مجموعة صور
        
        المعلمات:
            image_paths (list): قائمة مسارات ملفات الصور
            plant_ids (list): قائمة معرفات النباتات (اختياري)
            user_id (int): معرف المستخدم (اختياري)
            use_premium (bool): استخدام النموذج المتقدم (اختياري)
            
        العوائد:
            list: قائمة نتائج التشخيص
        """
        if not image_paths:
            raise ValueError("قائمة مسارات الصور فارغة")
        
        if plant_ids and len(plant_ids) != len(image_paths):
            raise ValueError("عدد معرفات النباتات لا يتطابق مع عدد الصور")
        
        results = []
        
        # إنشاء خيوط لكل صورة
        threads = []
        for i, image_path in enumerate(image_paths):
            plant_id = plant_ids[i] if plant_ids else None
            
            # إنشاء خيط لتشخيص المرض
            thread = threading.Thread(
                target=self._detect_disease_thread,
                args=(image_path, plant_id, user_id, use_premium, results)
            )
            threads.append(thread)
            thread.start()
        
        # انتظار انتهاء جميع الخيوط
        for thread in threads:
            thread.join()
        
        logger.info(f"تم تشخيص {len(results)} مرض بنجاح")
        return results
    
    def _detect_disease_thread(self, image_path, plant_id, user_id, use_premium, results):
        """
        خيط لتشخيص مرض نباتي
        
        المعلمات:
            image_path (str): مسار ملف الصورة
            plant_id (int): معرف النبات
            user_id (int): معرف المستخدم
            use_premium (bool): استخدام النموذج المتقدم
            results (list): قائمة النتائج
        """
        try:
            result = self.detect_disease(image_path, plant_id, user_id, use_premium)
            result['image_path'] = image_path
            result['plant_id'] = plant_id
            results.append(result)
        except Exception as e:
            logger.error(f"خطأ في خيط تشخيص المرض: {str(e)}")
            results.append({
                'image_path': image_path,
                'plant_id': plant_id,
                'error': str(e)
            })
    
    def _save_disease_detection(self, plant_id, detection_result):
        """
        حفظ نتيجة تشخيص المرض في قاعدة البيانات
        
        المعلمات:
            plant_id (int): معرف النبات
            detection_result (dict): نتيجة التشخيص
            
        العوائد:
            bool: نجاح العملية
        """
        try:
            # إعداد بيانات التشخيص
            detection_data = {
                'plant_id': plant_id,
                'disease_id': detection_result.get('disease_id'),
                'detection_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'confidence': detection_result.get('confidence', 0),
                'status': 'pending',
                'details': json.dumps(detection_result)
            }
            
            # إدراج البيانات في قاعدة البيانات
            with self.db_integration.erp_engine.connect() as conn:
                query = """
                INSERT INTO disease_detection (plant_id, disease_id, detection_date, confidence, status, details)
                VALUES (:plant_id, :disease_id, :detection_date, :confidence, :status, :details)
                """
                conn.execute(query, detection_data)
            
            logger.info(f"تم حفظ نتيجة تشخيص المرض للنبات {plant_id}")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في حفظ نتيجة تشخيص المرض: {str(e)}")
            return False
    
    def simulate_breeding(self, parent1_id, parent2_id, target_traits=None, user_id=None, use_premium=False):
        """
        محاكاة عملية تهجين نباتي
        
        المعلمات:
            parent1_id (int): معرف النبات الأول
            parent2_id (int): معرف النبات الثاني
            target_traits (list): قائمة الصفات المستهدفة (اختياري)
            user_id (int): معرف المستخدم (اختياري)
            use_premium (bool): استخدام النموذج المتقدم (اختياري)
            
        العوائد:
            dict: نتيجة التهجين
        """
        # تحديد النموذج المستخدم
        model = self.config['models']['breeding']['premium'] if use_premium else self.config['models']['breeding']['default']
        
        # إعداد بيانات الطلب
        data = {
            'parent1_id': parent1_id,
            'parent2_id': parent2_id,
            'target_traits': target_traits,
            'user_id': user_id,
            'model': model
        }
        
        # تحديث إحصائيات الأداء
        self.performance_metrics['breeding']['requests'] += 1
        
        try:
            # إجراء طلب API
            start_time = time.time()
            result = self._make_api_request('breeding/simulate', method='POST', data=data)
            end_time = time.time()
            
            # تحديث إحصائيات الأداء
            response_time = end_time - start_time
            self.performance_metrics['breeding']['successful'] += 1
            self.performance_metrics['breeding']['total_response_time'] += response_time
            self.performance_metrics['breeding']['avg_response_time'] = (
                self.performance_metrics['breeding']['total_response_time'] / 
                self.performance_metrics['breeding']['successful']
            )
            
            if 'success_probability' in result:
                self.performance_metrics['breeding']['success_probabilities'].append(result['success_probability'])
            
            # حفظ نتيجة التهجين في قاعدة البيانات
            if self.db_integration:
                self._save_breeding_result(parent1_id, parent2_id, target_traits, result)
            
            # جمع بيانات لمراقبة الانحراف
            if self.evidently_enabled:
                self._collect_data_for_drift_monitoring('breeding', result)
            
            logger.info(f"تمت محاكاة التهجين بنجاح: {result.get('offspring_name', 'غير معروف')}")
            return result
        
        except Exception as e:
            # تحديث إحصائيات الأداء
            self.performance_metrics['breeding']['failed'] += 1
            
            logger.error(f"خطأ في محاكاة التهجين: {str(e)}")
            raise
    
    def _save_breeding_result(self, parent1_id, parent2_id, target_traits, breeding_result):
        """
        حفظ نتيجة التهجين في قاعدة البيانات
        
        المعلمات:
            parent1_id (int): معرف النبات الأول
            parent2_id (int): معرف النبات الثاني
            target_traits (list): قائمة الصفات المستهدفة
            breeding_result (dict): نتيجة التهجين
            
        العوائد:
            bool: نجاح العملية
        """
        try:
            # إعداد بيانات طلب التهجين
            request_data = {
                'parent1_id': parent1_id,
                'parent2_id': parent2_id,
                'target_traits': json.dumps(target_traits) if target_traits else None,
                'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'completed'
            }
            
            # إدراج طلب التهجين في قاعدة البيانات
            with self.db_integration.erp_engine.connect() as conn:
                query = """
                INSERT INTO breeding_request (parent1_id, parent2_id, target_traits, request_date, status)
                VALUES (:parent1_id, :parent2_id, :target_traits, :request_date, :status)
                RETURNING id
                """
                result = conn.execute(query, request_data)
                request_id = result.fetchone()[0]
            
            # إعداد بيانات نتيجة التهجين
            result_data = {
                'request_id': request_id,
                'result_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'predicted_traits': breeding_result.get('predicted_traits'),
                'success_probability': breeding_result.get('success_probability', 0),
                'recommendations': breeding_result.get('recommendations'),
                'details': json.dumps(breeding_result)
            }
            
            # إدراج نتيجة التهجين في قاعدة البيانات
            with self.db_integration.erp_engine.connect() as conn:
                query = """
                INSERT INTO breeding_result (request_id, result_date, predicted_traits, success_probability, recommendations, details)
                VALUES (:request_id, :result_date, :predicted_traits, :success_probability, :recommendations, :details)
                """
                conn.execute(query, result_data)
            
            logger.info(f"تم حفظ نتيجة التهجين للطلب {request_id}")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في حفظ نتيجة التهجين: {str(e)}")
            return False
    
    def analyze_soil(self, image_path=None, sample_data=None, farm_id=None, user_id=None, use_premium=False):
        """
        تحليل عينة تربة
        
        المعلمات:
            image_path (str): مسار ملف صورة التربة (اختياري)
            sample_data (dict): بيانات العينة (اختياري)
            farm_id (int): معرف المزرعة (اختياري)
            user_id (int): معرف المستخدم (اختياري)
            use_premium (bool): استخدام النموذج المتقدم (اختياري)
            
        العوائد:
            dict: نتيجة تحليل التربة
        """
        if not image_path and not sample_data:
            raise ValueError("يجب تحديد صورة التربة أو بيانات العينة")
        
        # تحديد النموذج المستخدم
        model = self.config['models']['soil_analysis']['premium'] if use_premium else self.config['models']['soil_analysis']['default']
        
        # إعداد بيانات الطلب
        data = {
            'farm_id': farm_id,
            'user_id': user_id,
            'model': model
        }
        
        if sample_data:
            data['sample_data'] = sample_data
        
        # إعداد ملف الصورة
        files = None
        if image_path:
            if not os.path.exists(image_path):
                raise ValueError(f"ملف الصورة غير موجود: {image_path}")
            
            files = {
                'image': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
            }
        
        # تحديث إحصائيات الأداء
        self.performance_metrics['soil_analysis']['requests'] += 1
        
        try:
            # إجراء طلب API
            start_time = time.time()
            result = self._make_api_request('soil/analyze', method='POST', data=data, files=files)
            end_time = time.time()
            
            # تحديث إحصائيات الأداء
            response_time = end_time - start_time
            self.performance_metrics['soil_analysis']['successful'] += 1
            self.performance_metrics['soil_analysis']['total_response_time'] += response_time
            self.performance_metrics['soil_analysis']['avg_response_time'] = (
                self.performance_metrics['soil_analysis']['total_response_time'] / 
                self.performance_metrics['soil_analysis']['successful']
            )
            
            # حفظ نتيجة تحليل التربة في قاعدة البيانات
            if self.db_integration and farm_id:
                self._save_soil_analysis(farm_id, result)
            
            # جمع بيانات لمراقبة الانحراف
            if self.evidently_enabled:
                self._collect_data_for_drift_monitoring('soil_analysis', result)
            
            logger.info(f"تم تحليل التربة بنجاح: {result.get('soil_type', 'غير معروف')}")
            return result
        
        except Exception as e:
            # تحديث إحصائيات الأداء
            self.performance_metrics['soil_analysis']['failed'] += 1
            
            logger.error(f"خطأ في تحليل التربة: {str(e)}")
            raise
        finally:
            # إغلاق ملف الصورة
            if files and 'image' in files:
                files['image'][1].close()
    
    def _save_soil_analysis(self, farm_id, analysis_result):
        """
        حفظ نتيجة تحليل التربة في قاعدة البيانات
        
        المعلمات:
            farm_id (int): معرف المزرعة
            analysis_result (dict): نتيجة تحليل التربة
            
        العوائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود نوع التربة
            soil_type_id = None
            soil_type_name = analysis_result.get('soil_type')
            
            if soil_type_name:
                # البحث عن نوع التربة في قاعدة البيانات
                with self.db_integration.erp_engine.connect() as conn:
                    query = "SELECT id FROM soil_type WHERE name = :name"
                    result = conn.execute(query, {'name': soil_type_name})
                    row = result.fetchone()
                    
                    if row:
                        soil_type_id = row[0]
                    else:
                        # إنشاء نوع تربة جديد
                        query = """
                        INSERT INTO soil_type (name, description, characteristics)
                        VALUES (:name, :description, :characteristics)
                        RETURNING id
                        """
                        result = conn.execute(query, {
                            'name': soil_type_name,
                            'description': analysis_result.get('soil_description', ''),
                            'characteristics': analysis_result.get('soil_characteristics', '')
                        })
                        soil_type_id = result.fetchone()[0]
            
            # إعداد بيانات تحليل التربة
            analysis_data = {
                'farm_id': farm_id,
                'soil_type_id': soil_type_id,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ph': analysis_result.get('ph', 0),
                'nitrogen': analysis_result.get('nitrogen', 0),
                'phosphorus': analysis_result.get('phosphorus', 0),
                'potassium': analysis_result.get('potassium', 0),
                'organic_matter': analysis_result.get('organic_matter', 0),
                'details': json.dumps(analysis_result)
            }
            
            # إدراج البيانات في قاعدة البيانات
            with self.db_integration.erp_engine.connect() as conn:
                query = """
                INSERT INTO soil_analysis (farm_id, soil_type_id, analysis_date, ph, nitrogen, phosphorus, potassium, organic_matter, details)
                VALUES (:farm_id, :soil_type_id, :analysis_date, :ph, :nitrogen, :phosphorus, :potassium, :organic_matter, :details)
                """
                conn.execute(query, analysis_data)
            
            logger.info(f"تم حفظ نتيجة تحليل التربة للمزرعة {farm_id}")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في حفظ نتيجة تحليل التربة: {str(e)}")
            return False
    
    def predict_yield(self, farm_id, crop_id, planting_date, harvest_date=None, additional_data=None, user_id=None, use_premium=False):
        """
        توقع إنتاج محصول
        
        المعلمات:
            farm_id (int): معرف المزرعة
            crop_id (int): معرف المحصول
            planting_date (str): تاريخ الزراعة
            harvest_date (str): تاريخ الحصاد المتوقع (اختياري)
            additional_data (dict): بيانات إضافية (اختياري)
            user_id (int): معرف المستخدم (اختياري)
            use_premium (bool): استخدام النموذج المتقدم (اختياري)
            
        العوائد:
            dict: نتيجة توقع الإنتاج
        """
        # تحديد النموذج المستخدم
        model = self.config['models']['yield_prediction']['premium'] if use_premium else self.config['models']['yield_prediction']['default']
        
        # إعداد بيانات الطلب
        data = {
            'farm_id': farm_id,
            'crop_id': crop_id,
            'planting_date': planting_date,
            'harvest_date': harvest_date,
            'user_id': user_id,
            'model': model
        }
        
        if additional_data:
            data['additional_data'] = additional_data
        
        # تحديث إحصائيات الأداء
        self.performance_metrics['yield_prediction']['requests'] += 1
        
        try:
            # إجراء طلب API
            start_time = time.time()
            result = self._make_api_request('yield/predict', method='POST', data=data)
            end_time = time.time()
            
            # تحديث إحصائيات الأداء
            response_time = end_time - start_time
            self.performance_metrics['yield_prediction']['successful'] += 1
            self.performance_metrics['yield_prediction']['total_response_time'] += response_time
            self.performance_metrics['yield_prediction']['avg_response_time'] = (
                self.performance_metrics['yield_prediction']['total_response_time'] / 
                self.performance_metrics['yield_prediction']['successful']
            )
            
            # حفظ نتيجة توقع الإنتاج في قاعدة البيانات
            if self.db_integration:
                self._save_yield_prediction(farm_id, crop_id, result)
            
            # جمع بيانات لمراقبة الانحراف
            if self.evidently_enabled:
                self._collect_data_for_drift_monitoring('yield_prediction', result)
            
            logger.info(f"تم توقع إنتاج المحصول بنجاح: {result.get('predicted_yield', 0)} كجم")
            return result
        
        except Exception as e:
            # تحديث إحصائيات الأداء
            self.performance_metrics['yield_prediction']['failed'] += 1
            
            logger.error(f"خطأ في توقع إنتاج المحصول: {str(e)}")
            raise
    
    def _save_yield_prediction(self, farm_id, crop_id, prediction_result):
        """
        حفظ نتيجة توقع الإنتاج في قاعدة البيانات
        
        المعلمات:
            farm_id (int): معرف المزرعة
            crop_id (int): معرف المحصول
            prediction_result (dict): نتيجة توقع الإنتاج
            
        العوائد:
            bool: نجاح العملية
        """
        try:
            # إعداد بيانات توقع الإنتاج
            prediction_data = {
                'farm_id': farm_id,
                'crop_id': crop_id,
                'prediction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'predicted_yield': prediction_result.get('predicted_yield', 0),
                'confidence': prediction_result.get('confidence', 0),
                'details': json.dumps(prediction_result)
            }
            
            # إدراج البيانات في قاعدة البيانات
            with self.db_integration.erp_engine.connect() as conn:
                query = """
                INSERT INTO yield_prediction (farm_id, crop_id, prediction_date, predicted_yield, confidence, details)
                VALUES (:farm_id, :crop_id, :prediction_date, :predicted_yield, :confidence, :details)
                """
                conn.execute(query, prediction_data)
            
            logger.info(f"تم حفظ نتيجة توقع الإنتاج للمزرعة {farm_id} والمحصول {crop_id}")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في حفظ نتيجة توقع الإنتاج: {str(e)}")
            return False
    
    def get_disease_info(self, disease_id=None, disease_name=None):
        """
        الحصول على معلومات مرض
        
        المعلمات:
            disease_id (int): معرف المرض (اختياري)
            disease_name (str): اسم المرض (اختياري)
            
        العوائد:
            dict: معلومات المرض
        """
        if not disease_id and not disease_name:
            raise ValueError("يجب تحديد معرف المرض أو اسم المرض")
        
        # إعداد معلمات الطلب
        params = {}
        if disease_id:
            params['disease_id'] = disease_id
        if disease_name:
            params['disease_name'] = disease_name
        
        try:
            # إجراء طلب API
            result = self._make_api_request('disease/info', method='GET', params=params)
            
            logger.info(f"تم الحصول على معلومات المرض بنجاح: {result.get('name', 'غير معروف')}")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات المرض: {str(e)}")
            raise
    
    def get_treatment_recommendations(self, disease_id=None, disease_name=None, plant_id=None, severity=None):
        """
        الحصول على توصيات العلاج
        
        المعلمات:
            disease_id (int): معرف المرض (اختياري)
            disease_name (str): اسم المرض (اختياري)
            plant_id (int): معرف النبات (اختياري)
            severity (str): شدة الإصابة (اختياري)
            
        العوائد:
            dict: توصيات العلاج
        """
        if not disease_id and not disease_name:
            raise ValueError("يجب تحديد معرف المرض أو اسم المرض")
        
        # إعداد معلمات الطلب
        params = {}
        if disease_id:
            params['disease_id'] = disease_id
        if disease_name:
            params['disease_name'] = disease_name
        if plant_id:
            params['plant_id'] = plant_id
        if severity:
            params['severity'] = severity
        
        try:
            # إجراء طلب API
            result = self._make_api_request('disease/treatment', method='GET', params=params)
            
            logger.info(f"تم الحصول على توصيات العلاج بنجاح للمرض: {disease_id or disease_name}")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على توصيات العلاج: {str(e)}")
            raise
    
    def get_variety_info(self, variety_id=None, variety_name=None):
        """
        الحصول على معلومات صنف
        
        المعلمات:
            variety_id (int): معرف الصنف (اختياري)
            variety_name (str): اسم الصنف (اختياري)
            
        العوائد:
            dict: معلومات الصنف
        """
        if not variety_id and not variety_name:
            raise ValueError("يجب تحديد معرف الصنف أو اسم الصنف")
        
        # إعداد معلمات الطلب
        params = {}
        if variety_id:
            params['variety_id'] = variety_id
        if variety_name:
            params['variety_name'] = variety_name
        
        try:
            # إجراء طلب API
            result = self._make_api_request('variety/info', method='GET', params=params)
            
            logger.info(f"تم الحصول على معلومات الصنف بنجاح: {result.get('name', 'غير معروف')}")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات الصنف: {str(e)}")
            raise
    
    def search_knowledge_base(self, query, category=None, limit=10):
        """
        البحث في قاعدة المعرفة
        
        المعلمات:
            query (str): استعلام البحث
            category (str): فئة البحث (اختياري)
            limit (int): عدد النتائج (اختياري)
            
        العوائد:
            list: نتائج البحث
        """
        # إعداد معلمات الطلب
        params = {
            'query': query,
            'limit': limit
        }
        
        if category:
            params['category'] = category
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/search', method='GET', params=params)
            
            logger.info(f"تم البحث في قاعدة المعرفة بنجاح: {len(result.get('results', []))} نتيجة")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في البحث في قاعدة المعرفة: {str(e)}")
            raise
    
    def get_performance_metrics(self):
        """
        الحصول على مقاييس الأداء
        
        العوائد:
            dict: مقاييس الأداء
        """
        # حساب معدلات النجاح
        metrics = {}
        
        for service, data in self.performance_metrics.items():
            total_requests = data['requests']
            if total_requests > 0:
                success_rate = data['successful'] / total_requests * 100
            else:
                success_rate = 0
            
            metrics[service] = {
                'total_requests': total_requests,
                'successful': data['successful'],
                'failed': data['failed'],
                'success_rate': success_rate,
                'avg_response_time': data['avg_response_time']
            }
            
            # إضافة مقاييس خاصة بكل خدمة
            if service == 'disease_detection' and data['confidence_scores']:
                metrics[service]['avg_confidence'] = sum(data['confidence_scores']) / len(data['confidence_scores'])
            
            if service == 'breeding' and data['success_probabilities']:
                metrics[service]['avg_success_probability'] = sum(data['success_probabilities']) / len(data['success_probabilities'])
        
        return metrics
    
    def _collect_data_for_drift_monitoring(self, service, result):
        """
        جمع بيانات لمراقبة انحراف البيانات
        
        المعلمات:
            service (str): اسم الخدمة
            result (dict): نتيجة الخدمة
        """
        if not self.evidently_enabled:
            return
        
        try:
            # تحويل النتيجة إلى بيانات مناسبة للمراقبة
            if service == 'disease_detection':
                data = {
                    'confidence': result.get('confidence', 0),
                    'disease_id': result.get('disease_id', 0),
                    'timestamp': datetime.now().timestamp()
                }
            elif service == 'breeding':
                data = {
                    'success_probability': result.get('success_probability', 0),
                    'timestamp': datetime.now().timestamp()
                }
            elif service == 'soil_analysis':
                data = {
                    'ph': result.get('ph', 0),
                    'nitrogen': result.get('nitrogen', 0),
                    'phosphorus': result.get('phosphorus', 0),
                    'potassium': result.get('potassium', 0),
                    'organic_matter': result.get('organic_matter', 0),
                    'timestamp': datetime.now().timestamp()
                }
            elif service == 'yield_prediction':
                data = {
                    'predicted_yield': result.get('predicted_yield', 0),
                    'confidence': result.get('confidence', 0),
                    'timestamp': datetime.now().timestamp()
                }
            else:
                return
            
            # إضافة البيانات إلى البيانات الحالية
            if service not in self.evidently_current_data:
                self.evidently_current_data[service] = []
            
            self.evidently_current_data[service].append(data)
            
            # التحقق من الحاجة إلى إجراء تحليل الانحراف
            monitoring_interval = self.config.get('evidently', {}).get('monitoring_interval', 86400)
            if len(self.evidently_current_data[service]) >= 100 or (
                self.evidently_current_data[service] and 
                self.evidently_current_data[service][-1]['timestamp'] - self.evidently_current_data[service][0]['timestamp'] >= monitoring_interval
            ):
                self._analyze_data_drift(service)
        
        except Exception as e:
            logger.error(f"خطأ في جمع بيانات مراقبة الانحراف: {str(e)}")
    
    def _analyze_data_drift(self, service):
        """
        تحليل انحراف البيانات
        
        المعلمات:
            service (str): اسم الخدمة
        """
        if not self.evidently_enabled:
            return
        
        if service not in self.evidently_current_data or not self.evidently_current_data[service]:
            return
        
        if service not in self.evidently_reference_data or not self.evidently_reference_data[service]:
            # استخدام البيانات الحالية كبيانات مرجعية
            self.evidently_reference_data[service] = self.evidently_current_data[service]
            self.evidently_current_data[service] = []
            return
        
        try:
            # تحويل البيانات إلى DataFrame
            reference_df = pd.DataFrame(self.evidently_reference_data[service])
            current_df = pd.DataFrame(self.evidently_current_data[service])
            
            # إنشاء تقرير المراقبة
            monitoring = ModelMonitoring(metrics=[
                DataDriftTable(),
                DataQualityTable()
            ])
            
            # تحليل الانحراف
            monitoring.calculate(reference_df, current_df)
            
            # الحصول على نتائج التحليل
            drift_results = monitoring.as_dict()
            
            # التحقق من وجود انحراف كبير
            drift_detected = False
            drift_threshold = self.config.get('evidently', {}).get('drift_threshold', 0.05)
            
            if 'metrics' in drift_results and 'data_drift' in drift_results['metrics']:
                data_drift = drift_results['metrics']['data_drift']
                if 'data_drift_score' in data_drift and data_drift['data_drift_score'] > drift_threshold:
                    drift_detected = True
            
            # إرسال تنبيه إذا تم اكتشاف انحراف كبير
            if drift_detected:
                self._send_drift_alert(service, drift_results)
            
            # حفظ البيانات الحالية كبيانات مرجعية جديدة
            self.evidently_reference_data[service] = self.evidently_current_data[service]
            self.evidently_current_data[service] = []
            
            logger.info(f"تم تحليل انحراف البيانات للخدمة {service}")
        
        except Exception as e:
            logger.error(f"خطأ في تحليل انحراف البيانات: {str(e)}")
    
    def _send_drift_alert(self, service, drift_results):
        """
        إرسال تنبيه انحراف البيانات
        
        المعلمات:
            service (str): اسم الخدمة
            drift_results (dict): نتائج تحليل الانحراف
        """
        notification_config = self.config.get('notification', {})
        if not notification_config.get('enabled', True):
            return
        
        recipients = notification_config.get('recipients', [])
        if not recipients:
            logger.warning("لا يوجد مستلمين لتنبيه انحراف البيانات")
            return
        
        try:
            # إنشاء رسم بياني للانحراف
            drift_score = drift_results['metrics']['data_drift']['data_drift_score']
            drift_features = drift_results['metrics']['data_drift']['features']
            
            feature_scores = []
            for feature, data in drift_features.items():
                if 'drift_score' in data:
                    feature_scores.append((feature, data['drift_score']))
            
            # ترتيب الميزات حسب درجة الانحراف
            feature_scores.sort(key=lambda x: x[1], reverse=True)
            
            # إنشاء رسم بياني
            plt.figure(figsize=(10, 6))
            features = [f[0] for f in feature_scores]
            scores = [f[1] for f in feature_scores]
            
            plt.bar(features, scores)
            plt.axhline(y=self.config.get('evidently', {}).get('drift_threshold', 0.05), color='r', linestyle='--')
            plt.title(f'انحراف البيانات للخدمة {service}')
            plt.xlabel('الميزة')
            plt.ylabel('درجة الانحراف')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.temp_dir, f'drift_{service}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(chart_path)
            plt.close()
            
            # إعداد رسالة التنبيه
            subject = f"تنبيه: اكتشاف انحراف في بيانات خدمة {service}"
            message = f"""
            تم اكتشاف انحراف كبير في بيانات خدمة {service}.
            
            درجة الانحراف الكلية: {drift_score:.4f}
            عتبة الانحراف: {self.config.get('evidently', {}).get('drift_threshold', 0.05):.4f}
            
            الميزات ذات الانحراف الأعلى:
            """
            
            for feature, score in feature_scores[:5]:
                message += f"- {feature}: {score:.4f}\n"
            
            message += "\nيرجى مراجعة البيانات واتخاذ الإجراء المناسب."
            
            # إرسال التنبيه
            # TODO: تنفيذ آلية إرسال التنبيهات (بريد إلكتروني، رسائل، إلخ)
            
            logger.info(f"تم إرسال تنبيه انحراف البيانات للخدمة {service}")
        
        except Exception as e:
            logger.error(f"خطأ في إرسال تنبيه انحراف البيانات: {str(e)}")
    
    def start_monitoring(self):
        """
        بدء مراقبة أداء الذكاء الاصطناعي
        
        العوائد:
            bool: نجاح العملية
        """
        try:
            # إنشاء خيط لمراقبة الأداء
            monitoring_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True
            )
            monitoring_thread.start()
            
            # إضافة الخيط إلى قائمة الخيوط النشطة
            self.active_threads.append(monitoring_thread)
            
            logger.info("تم بدء مراقبة أداء الذكاء الاصطناعي")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في بدء مراقبة أداء الذكاء الاصطناعي: {str(e)}")
            return False
    
    def _monitoring_loop(self):
        """
        حلقة مراقبة أداء الذكاء الاصطناعي
        """
        while True:
            try:
                # تحليل انحراف البيانات لجميع الخدمات
                if self.evidently_enabled:
                    for service in self.evidently_current_data:
                        if self.evidently_current_data[service]:
                            self._analyze_data_drift(service)
                
                # التحقق من معدلات الأخطاء
                metrics = self.get_performance_metrics()
                error_threshold = self.config.get('notification', {}).get('error_threshold', 0.1)
                
                for service, data in metrics.items():
                    if data['total_requests'] > 10 and data['success_rate'] < (1 - error_threshold) * 100:
                        self._send_error_alert(service, data)
                
                # انتظار قبل التحليل التالي
                time.sleep(3600)  # ساعة واحدة
            
            except Exception as e:
                logger.error(f"خطأ في حلقة المراقبة: {str(e)}")
                time.sleep(300)  # 5 دقائق
    
    def _send_error_alert(self, service, metrics):
        """
        إرسال تنبيه معدل الأخطاء
        
        المعلمات:
            service (str): اسم الخدمة
            metrics (dict): مقاييس الأداء
        """
        notification_config = self.config.get('notification', {})
        if not notification_config.get('enabled', True):
            return
        
        recipients = notification_config.get('recipients', [])
        if not recipients:
            logger.warning("لا يوجد مستلمين لتنبيه معدل الأخطاء")
            return
        
        try:
            # إنشاء رسم بياني لمعدل الأخطاء
            plt.figure(figsize=(8, 6))
            labels = ['ناجح', 'فاشل']
            sizes = [metrics['successful'], metrics['failed']]
            colors = ['green', 'red']
            
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title(f'معدل نجاح خدمة {service}')
            
            # حفظ الرسم البياني
            chart_path = os.path.join(self.temp_dir, f'error_{service}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            plt.savefig(chart_path)
            plt.close()
            
            # إعداد رسالة التنبيه
            subject = f"تنبيه: ارتفاع معدل الأخطاء في خدمة {service}"
            message = f"""
            تم اكتشاف ارتفاع في معدل الأخطاء لخدمة {service}.
            
            إجمالي الطلبات: {metrics['total_requests']}
            الطلبات الناجحة: {metrics['successful']}
            الطلبات الفاشلة: {metrics['failed']}
            معدل النجاح: {metrics['success_rate']:.2f}%
            
            يرجى مراجعة الخدمة واتخاذ الإجراء المناسب.
            """
            
            # إرسال التنبيه
            # TODO: تنفيذ آلية إرسال التنبيهات (بريد إلكتروني، رسائل، إلخ)
            
            logger.info(f"تم إرسال تنبيه معدل الأخطاء للخدمة {service}")
        
        except Exception as e:
            logger.error(f"خطأ في إرسال تنبيه معدل الأخطاء: {str(e)}")
    
    def get_ai_system_status(self):
        """
        الحصول على حالة نظام الذكاء الاصطناعي
        
        العوائد:
            dict: حالة النظام
        """
        try:
            # إجراء طلب API
            result = self._make_api_request('system/status', method='GET')
            
            logger.info("تم الحصول على حالة نظام الذكاء الاصطناعي بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على حالة نظام الذكاء الاصطناعي: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_ai_models_info(self):
        """
        الحصول على معلومات نماذج الذكاء الاصطناعي
        
        العوائد:
            dict: معلومات النماذج
        """
        try:
            # إجراء طلب API
            result = self._make_api_request('models/info', method='GET')
            
            logger.info("تم الحصول على معلومات نماذج الذكاء الاصطناعي بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات نماذج الذكاء الاصطناعي: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_ai_system_usage(self, start_date=None, end_date=None, user_id=None):
        """
        الحصول على إحصائيات استخدام نظام الذكاء الاصطناعي
        
        المعلمات:
            start_date (str): تاريخ البداية (اختياري)
            end_date (str): تاريخ النهاية (اختياري)
            user_id (int): معرف المستخدم (اختياري)
            
        العوائد:
            dict: إحصائيات الاستخدام
        """
        # إعداد معلمات الطلب
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if user_id:
            params['user_id'] = user_id
        
        try:
            # إجراء طلب API
            result = self._make_api_request('system/usage', method='GET', params=params)
            
            logger.info("تم الحصول على إحصائيات استخدام نظام الذكاء الاصطناعي بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على إحصائيات استخدام نظام الذكاء الاصطناعي: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_ai_system_logs(self, level=None, service=None, limit=100):
        """
        الحصول على سجلات نظام الذكاء الاصطناعي
        
        المعلمات:
            level (str): مستوى السجل (اختياري)
            service (str): اسم الخدمة (اختياري)
            limit (int): عدد السجلات (اختياري)
            
        العوائد:
            dict: سجلات النظام
        """
        # إعداد معلمات الطلب
        params = {
            'limit': limit
        }
        if level:
            params['level'] = level
        if service:
            params['service'] = service
        
        try:
            # إجراء طلب API
            result = self._make_api_request('system/logs', method='GET', params=params)
            
            logger.info(f"تم الحصول على {len(result.get('logs', []))} سجل لنظام الذكاء الاصطناعي بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على سجلات نظام الذكاء الاصطناعي: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'logs': []
            }
    
    def train_model(self, model_type, dataset_path=None, parameters=None):
        """
        تدريب نموذج ذكاء اصطناعي
        
        المعلمات:
            model_type (str): نوع النموذج
            dataset_path (str): مسار مجموعة البيانات (اختياري)
            parameters (dict): معلمات التدريب (اختياري)
            
        العوائد:
            dict: نتيجة التدريب
        """
        # إعداد بيانات الطلب
        data = {
            'model_type': model_type
        }
        
        if parameters:
            data['parameters'] = parameters
        
        # إعداد ملف مجموعة البيانات
        files = None
        if dataset_path:
            if not os.path.exists(dataset_path):
                raise ValueError(f"ملف مجموعة البيانات غير موجود: {dataset_path}")
            
            files = {
                'dataset': (os.path.basename(dataset_path), open(dataset_path, 'rb'))
            }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/train', method='POST', data=data, files=files)
            
            logger.info(f"تم بدء تدريب نموذج {model_type} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في تدريب نموذج {model_type}: {str(e)}")
            raise
        finally:
            # إغلاق ملف مجموعة البيانات
            if files and 'dataset' in files:
                files['dataset'][1].close()
    
    def get_training_status(self, training_id):
        """
        الحصول على حالة تدريب نموذج
        
        المعلمات:
            training_id (str): معرف التدريب
            
        العوائد:
            dict: حالة التدريب
        """
        # إعداد معلمات الطلب
        params = {
            'training_id': training_id
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/training-status', method='GET', params=params)
            
            logger.info(f"تم الحصول على حالة تدريب النموذج {training_id} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على حالة تدريب النموذج {training_id}: {str(e)}")
            raise
    
    def cancel_training(self, training_id):
        """
        إلغاء تدريب نموذج
        
        المعلمات:
            training_id (str): معرف التدريب
            
        العوائد:
            dict: نتيجة الإلغاء
        """
        # إعداد بيانات الطلب
        data = {
            'training_id': training_id
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/cancel-training', method='POST', data=data)
            
            logger.info(f"تم إلغاء تدريب النموذج {training_id} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في إلغاء تدريب النموذج {training_id}: {str(e)}")
            raise
    
    def get_model_performance(self, model_id):
        """
        الحصول على أداء نموذج
        
        المعلمات:
            model_id (str): معرف النموذج
            
        العوائد:
            dict: أداء النموذج
        """
        # إعداد معلمات الطلب
        params = {
            'model_id': model_id
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/performance', method='GET', params=params)
            
            logger.info(f"تم الحصول على أداء النموذج {model_id} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على أداء النموذج {model_id}: {str(e)}")
            raise
    
    def export_model(self, model_id, format='onnx'):
        """
        تصدير نموذج
        
        المعلمات:
            model_id (str): معرف النموذج
            format (str): صيغة التصدير (اختياري)
            
        العوائد:
            str: مسار ملف النموذج المصدر
        """
        # إعداد معلمات الطلب
        params = {
            'model_id': model_id,
            'format': format
        }
        
        try:
            # إجراء طلب API
            response = requests.get(
                f"{self.api_base_url}/models/export",
                headers={'Authorization': f"Bearer {self.api_key}"},
                params=params,
                stream=True
            )
            
            # التحقق من نجاح الطلب
            response.raise_for_status()
            
            # استخراج اسم الملف من الاستجابة
            content_disposition = response.headers.get('Content-Disposition', '')
            filename = None
            
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"\'')
            else:
                filename = f"model_{model_id}.{format}"
            
            # حفظ الملف
            output_path = os.path.join(self.temp_dir, filename)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"تم تصدير النموذج {model_id} بنجاح إلى {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"خطأ في تصدير النموذج {model_id}: {str(e)}")
            raise
    
    def import_model(self, model_path, model_type, name=None, description=None):
        """
        استيراد نموذج
        
        المعلمات:
            model_path (str): مسار ملف النموذج
            model_type (str): نوع النموذج
            name (str): اسم النموذج (اختياري)
            description (str): وصف النموذج (اختياري)
            
        العوائد:
            dict: نتيجة الاستيراد
        """
        if not os.path.exists(model_path):
            raise ValueError(f"ملف النموذج غير موجود: {model_path}")
        
        # إعداد بيانات الطلب
        data = {
            'model_type': model_type
        }
        
        if name:
            data['name'] = name
        
        if description:
            data['description'] = description
        
        # إعداد ملف النموذج
        files = {
            'model': (os.path.basename(model_path), open(model_path, 'rb'))
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/import', method='POST', data=data, files=files)
            
            logger.info(f"تم استيراد النموذج {name or model_type} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في استيراد النموذج {name or model_type}: {str(e)}")
            raise
        finally:
            # إغلاق ملف النموذج
            files['model'][1].close()
    
    def get_model_versions(self, model_type):
        """
        الحصول على إصدارات نموذج
        
        المعلمات:
            model_type (str): نوع النموذج
            
        العوائد:
            dict: إصدارات النموذج
        """
        # إعداد معلمات الطلب
        params = {
            'model_type': model_type
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/versions', method='GET', params=params)
            
            logger.info(f"تم الحصول على إصدارات النموذج {model_type} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على إصدارات النموذج {model_type}: {str(e)}")
            raise
    
    def set_default_model(self, model_id, model_type, tier='free'):
        """
        تعيين النموذج الافتراضي
        
        المعلمات:
            model_id (str): معرف النموذج
            model_type (str): نوع النموذج
            tier (str): فئة النموذج (اختياري)
            
        العوائد:
            dict: نتيجة التعيين
        """
        # إعداد بيانات الطلب
        data = {
            'model_id': model_id,
            'model_type': model_type,
            'tier': tier
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('models/set-default', method='POST', data=data)
            
            logger.info(f"تم تعيين النموذج {model_id} كنموذج افتراضي لنوع {model_type} وفئة {tier} بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في تعيين النموذج {model_id} كنموذج افتراضي: {str(e)}")
            raise
    
    def get_knowledge_base_categories(self):
        """
        الحصول على فئات قاعدة المعرفة
        
        العوائد:
            dict: فئات قاعدة المعرفة
        """
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/categories', method='GET')
            
            logger.info("تم الحصول على فئات قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على فئات قاعدة المعرفة: {str(e)}")
            raise
    
    def add_knowledge_base_entry(self, title, content, category, source=None, tags=None):
        """
        إضافة مدخل إلى قاعدة المعرفة
        
        المعلمات:
            title (str): عنوان المدخل
            content (str): محتوى المدخل
            category (str): فئة المدخل
            source (str): مصدر المدخل (اختياري)
            tags (list): وسوم المدخل (اختياري)
            
        العوائد:
            dict: نتيجة الإضافة
        """
        # إعداد بيانات الطلب
        data = {
            'title': title,
            'content': content,
            'category': category
        }
        
        if source:
            data['source'] = source
        
        if tags:
            data['tags'] = tags
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/add', method='POST', data=data)
            
            logger.info(f"تمت إضافة مدخل {title} إلى قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في إضافة مدخل إلى قاعدة المعرفة: {str(e)}")
            raise
    
    def update_knowledge_base_entry(self, entry_id, title=None, content=None, category=None, source=None, tags=None):
        """
        تحديث مدخل في قاعدة المعرفة
        
        المعلمات:
            entry_id (str): معرف المدخل
            title (str): عنوان المدخل (اختياري)
            content (str): محتوى المدخل (اختياري)
            category (str): فئة المدخل (اختياري)
            source (str): مصدر المدخل (اختياري)
            tags (list): وسوم المدخل (اختياري)
            
        العوائد:
            dict: نتيجة التحديث
        """
        # إعداد بيانات الطلب
        data = {
            'entry_id': entry_id
        }
        
        if title:
            data['title'] = title
        
        if content:
            data['content'] = content
        
        if category:
            data['category'] = category
        
        if source:
            data['source'] = source
        
        if tags:
            data['tags'] = tags
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/update', method='PUT', data=data)
            
            logger.info(f"تم تحديث المدخل {entry_id} في قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في تحديث مدخل في قاعدة المعرفة: {str(e)}")
            raise
    
    def delete_knowledge_base_entry(self, entry_id):
        """
        حذف مدخل من قاعدة المعرفة
        
        المعلمات:
            entry_id (str): معرف المدخل
            
        العوائد:
            dict: نتيجة الحذف
        """
        # إعداد معلمات الطلب
        params = {
            'entry_id': entry_id
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/delete', method='DELETE', params=params)
            
            logger.info(f"تم حذف المدخل {entry_id} من قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في حذف مدخل من قاعدة المعرفة: {str(e)}")
            raise
    
    def get_knowledge_base_entry(self, entry_id):
        """
        الحصول على مدخل من قاعدة المعرفة
        
        المعلمات:
            entry_id (str): معرف المدخل
            
        العوائد:
            dict: مدخل قاعدة المعرفة
        """
        # إعداد معلمات الطلب
        params = {
            'entry_id': entry_id
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/entry', method='GET', params=params)
            
            logger.info(f"تم الحصول على المدخل {entry_id} من قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على مدخل من قاعدة المعرفة: {str(e)}")
            raise
    
    def get_knowledge_base_entries(self, category=None, tags=None, limit=100, offset=0):
        """
        الحصول على مدخلات قاعدة المعرفة
        
        المعلمات:
            category (str): فئة المدخلات (اختياري)
            tags (list): وسوم المدخلات (اختياري)
            limit (int): عدد المدخلات (اختياري)
            offset (int): إزاحة المدخلات (اختياري)
            
        العوائد:
            dict: مدخلات قاعدة المعرفة
        """
        # إعداد معلمات الطلب
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if category:
            params['category'] = category
        
        if tags:
            params['tags'] = tags
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/entries', method='GET', params=params)
            
            logger.info(f"تم الحصول على {len(result.get('entries', []))} مدخل من قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على مدخلات قاعدة المعرفة: {str(e)}")
            raise
    
    def import_knowledge_base(self, file_path):
        """
        استيراد قاعدة معرفة
        
        المعلمات:
            file_path (str): مسار ملف قاعدة المعرفة
            
        العوائد:
            dict: نتيجة الاستيراد
        """
        if not os.path.exists(file_path):
            raise ValueError(f"ملف قاعدة المعرفة غير موجود: {file_path}")
        
        # إعداد ملف قاعدة المعرفة
        files = {
            'file': (os.path.basename(file_path), open(file_path, 'rb'))
        }
        
        try:
            # إجراء طلب API
            result = self._make_api_request('knowledge/import', method='POST', files=files)
            
            logger.info("تم استيراد قاعدة المعرفة بنجاح")
            return result
        
        except Exception as e:
            logger.error(f"خطأ في استيراد قاعدة المعرفة: {str(e)}")
            raise
        finally:
            # إغلاق ملف قاعدة المعرفة
            files['file'][1].close()
    
    def export_knowledge_base(self, category=None, format='json'):
        """
        تصدير قاعدة معرفة
        
        المعلمات:
            category (str): فئة المدخلات (اختياري)
            format (str): صيغة التصدير (اختياري)
            
        العوائد:
            str: مسار ملف قاعدة المعرفة المصدرة
        """
        # إعداد معلمات الطلب
        params = {
            'format': format
        }
        
        if category:
            params['category'] = category
        
        try:
            # إجراء طلب API
            response = requests.get(
                f"{self.api_base_url}/knowledge/export",
                headers={'Authorization': f"Bearer {self.api_key}"},
                params=params,
                stream=True
            )
            
            # التحقق من نجاح الطلب
            response.raise_for_status()
            
            # استخراج اسم الملف من الاستجابة
            content_disposition = response.headers.get('Content-Disposition', '')
            filename = None
            
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"\'')
            else:
                filename = f"knowledge_base_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            # حفظ الملف
            output_path = os.path.join(self.temp_dir, filename)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"تم تصدير قاعدة المعرفة بنجاح إلى {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"خطأ في تصدير قاعدة المعرفة: {str(e)}")
            raise


# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء كائن تكامل الذكاء الاصطناعي
    ai_integration = AIIntegration()
    
    # تشخيص مرض نباتي
    try:
        result = ai_integration.detect_disease('/path/to/image.jpg')
        print(f"تم تشخيص المرض: {result.get('disease_name')}")
    except Exception as e:
        print(f"خطأ في تشخيص المرض: {str(e)}")
    
    # بدء مراقبة أداء الذكاء الاصطناعي
    ai_integration.start_monitoring()
