"""
وحدة التكامل بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي
يحتوي هذا الملف على الوظائف اللازمة لتكامل النظامين
"""

import os
import json
import logging
import requests
import shutil
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import time
import threading
from pathlib import Path

from ..core.config.config_manager import ConfigManager
from ..core.database.db_manager import DBManager
from ..ai.models.ai_models import DiagnosisRequest, DiagnosisResult, BreedingRequest, BreedingResult, DataSyncJob


class AISystemIntegration:
    """فئة التكامل مع نظام الذكاء الاصطناعي الزراعي"""
    
    def __init__(self, config_manager: ConfigManager, db_manager: DBManager):
        """تهيئة فئة التكامل"""
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        
        # الحصول على إعدادات التكامل
        self.ai_system_config = self.config_manager.get_config("ai_system")
        
        # عنوان API لنظام الذكاء الاصطناعي
        self.api_base_url = self.ai_system_config.get("api_base_url", "http://localhost:8000/api")
        
        # مفتاح API لنظام الذكاء الاصطناعي
        self.api_key = self.ai_system_config.get("api_key", "")
        
        # مسار مجلد الصور المؤقت
        self.temp_images_dir = self.ai_system_config.get("temp_images_dir", "/tmp/ai_images")
        os.makedirs(self.temp_images_dir, exist_ok=True)
        
        # مسار مجلد البيانات المشترك
        self.shared_data_dir = self.ai_system_config.get("shared_data_dir", "/tmp/shared_data")
        os.makedirs(self.shared_data_dir, exist_ok=True)
        
        # فترة الاستطلاع (بالثواني)
        self.poll_interval = self.ai_system_config.get("poll_interval", 60)
        
        # حالة المزامن
        self.sync_running = False
        self.sync_thread = None
    
    def start_sync_service(self):
        """بدء خدمة المزامنة"""
        if self.sync_thread is not None and self.sync_thread.is_alive():
            self.logger.warning("خدمة المزامنة قيد التشغيل بالفعل")
            return False
        
        self.sync_running = True
        self.sync_thread = threading.Thread(target=self._sync_service_loop, daemon=True)
        self.sync_thread.start()
        
        self.logger.info("تم بدء خدمة المزامنة")
        return True
    
    def stop_sync_service(self):
        """إيقاف خدمة المزامنة"""
        if self.sync_thread is None or not self.sync_thread.is_alive():
            self.logger.warning("خدمة المزامنة ليست قيد التشغيل")
            return False
        
        self.sync_running = False
        self.sync_thread.join(timeout=10)
        
        self.logger.info("تم إيقاف خدمة المزامنة")
        return True
    
    def _sync_service_loop(self):
        """حلقة خدمة المزامنة"""
        self.logger.info("بدء حلقة خدمة المزامنة")
        
        while self.sync_running:
            try:
                # مزامنة طلبات التشخيص
                self._sync_diagnosis_requests()
                
                # مزامنة نتائج التشخيص
                self._sync_diagnosis_results()
                
                # مزامنة طلبات التهجين
                self._sync_breeding_requests()
                
                # مزامنة نتائج التهجين
                self._sync_breeding_results()
                
                # مزامنة البيانات المشتركة
                self._sync_shared_data()
            except Exception as e:
                self.logger.error(f"خطأ في حلقة خدمة المزامنة: {str(e)}")
            
            # انتظار فترة الاستطلاع
            for _ in range(self.poll_interval):
                if not self.sync_running:
                    break
                time.sleep(1)
    
    def _sync_diagnosis_requests(self):
        """مزامنة طلبات التشخيص"""
        try:
            # الحصول على طلبات التشخيص المعلقة
            query = """
                SELECT request_id, image_path, plant_type, description, metadata
                FROM ai_diagnosis_requests
                WHERE status = 'pending'
            """
            
            results = self.db_manager.execute_query(query)
            
            for result in results:
                request_id, image_path, plant_type, description, metadata = result
                
                # التحقق من وجود الصورة
                if not os.path.exists(image_path):
                    self.logger.error(f"الصورة غير موجودة: {image_path}")
                    self._update_diagnosis_request_status(request_id, "failed", "الصورة غير موجودة")
                    continue
                
                # إرسال طلب التشخيص إلى نظام الذكاء الاصطناعي
                try:
                    response = self._send_diagnosis_request(request_id, image_path, plant_type, description, metadata)
                    
                    if response.get("success"):
                        self._update_diagnosis_request_status(request_id, "processing")
                    else:
                        self._update_diagnosis_request_status(request_id, "failed", response.get("error", "فشل في إرسال طلب التشخيص"))
                except Exception as e:
                    self.logger.error(f"خطأ في إرسال طلب التشخيص: {str(e)}")
                    self._update_diagnosis_request_status(request_id, "failed", str(e))
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة طلبات التشخيص: {str(e)}")
    
    def _send_diagnosis_request(self, request_id: str, image_path: str, plant_type: str, description: Optional[str], metadata: Optional[str]) -> Dict[str, Any]:
        """إرسال طلب تشخيص إلى نظام الذكاء الاصطناعي"""
        try:
            # إعداد البيانات
            data = {
                "request_id": request_id,
                "plant_type": plant_type
            }
            
            if description:
                data["description"] = description
            
            if metadata:
                try:
                    data["metadata"] = json.loads(metadata)
                except json.JSONDecodeError:
                    pass
            
            # إعداد الملفات
            files = {
                "image": (os.path.basename(image_path), open(image_path, "rb"))
            }
            
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.post(
                f"{self.api_base_url}/diagnosis/submit",
                data=data,
                files=files,
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في إرسال طلب التشخيص: {response.status_code} - {response.text}")
                return {"success": False, "error": f"فشل في إرسال طلب التشخيص: {response.status_code}"}
        except Exception as e:
            self.logger.error(f"خطأ في إرسال طلب التشخيص: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            # إغلاق الملفات
            if "files" in locals() and "image" in files:
                files["image"][1].close()
    
    def _update_diagnosis_request_status(self, request_id: str, status: str, error_message: Optional[str] = None):
        """تحديث حالة طلب التشخيص"""
        try:
            # بناء الاستعلام
            query = """
                UPDATE ai_diagnosis_requests
                SET status = %s, updated_at = %s
            """
            
            params = [status, datetime.now()]
            
            # إضافة رسالة الخطأ إذا تم توفيرها
            if error_message is not None:
                query += ", error_message = %s"
                params.append(error_message)
            
            # إضافة شرط المعرف
            query += " WHERE request_id = %s"
            params.append(request_id)
            
            # تنفيذ الاستعلام
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة طلب التشخيص: {str(e)}")
    
    def _sync_diagnosis_results(self):
        """مزامنة نتائج التشخيص"""
        try:
            # الحصول على طلبات التشخيص قيد المعالجة
            query = """
                SELECT request_id
                FROM ai_diagnosis_requests
                WHERE status = 'processing'
            """
            
            results = self.db_manager.execute_query(query)
            
            for result in results:
                request_id = result[0]
                
                # التحقق من حالة طلب التشخيص في نظام الذكاء الاصطناعي
                try:
                    response = self._check_diagnosis_status(request_id)
                    
                    if response.get("success"):
                        status = response.get("status")
                        
                        if status == "completed":
                            # الحصول على نتيجة التشخيص
                            diagnosis_result = response.get("result")
                            
                            # حفظ نتيجة التشخيص
                            self._save_diagnosis_result(request_id, diagnosis_result)
                            
                            # تحديث حالة طلب التشخيص
                            self._update_diagnosis_request_status(request_id, "completed")
                        elif status == "failed":
                            # تحديث حالة طلب التشخيص
                            self._update_diagnosis_request_status(request_id, "failed", response.get("error", "فشل في معالجة طلب التشخيص"))
                    else:
                        self.logger.error(f"فشل في التحقق من حالة طلب التشخيص: {response.get('error')}")
                except Exception as e:
                    self.logger.error(f"خطأ في التحقق من حالة طلب التشخيص: {str(e)}")
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة نتائج التشخيص: {str(e)}")
    
    def _check_diagnosis_status(self, request_id: str) -> Dict[str, Any]:
        """التحقق من حالة طلب التشخيص في نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/diagnosis/{request_id}/status",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في التحقق من حالة طلب التشخيص: {response.status_code} - {response.text}")
                return {"success": False, "error": f"فشل في التحقق من حالة طلب التشخيص: {response.status_code}"}
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من حالة طلب التشخيص: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _save_diagnosis_result(self, request_id: str, diagnosis_result: Dict[str, Any]):
        """حفظ نتيجة التشخيص"""
        try:
            # استخراج البيانات
            result_id = diagnosis_result.get("result_id")
            disease_name = diagnosis_result.get("disease_name")
            confidence = diagnosis_result.get("confidence")
            diagnosis_details = json.dumps(diagnosis_result.get("details", {}))
            treatment_recommendations = json.dumps(diagnosis_result.get("treatment_recommendations", []))
            result_images = json.dumps(diagnosis_result.get("result_images", []))
            
            # حفظ نتيجة التشخيص
            query = """
                INSERT INTO ai_diagnosis_results (
                    result_id, request_id, disease_name, confidence,
                    diagnosis_details, treatment_recommendations, result_images,
                    created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                result_id,
                request_id,
                disease_name,
                confidence,
                diagnosis_details,
                treatment_recommendations,
                result_images,
                datetime.now()
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ نتيجة التشخيص: {str(e)}")
            raise
    
    def _sync_breeding_requests(self):
        """مزامنة طلبات التهجين"""
        try:
            # الحصول على طلبات التهجين المعلقة
            query = """
                SELECT request_id, parent_varieties, breeding_goals, constraints, parameters
                FROM ai_breeding_requests
                WHERE status = 'pending'
            """
            
            results = self.db_manager.execute_query(query)
            
            for result in results:
                request_id, parent_varieties, breeding_goals, constraints, parameters = result
                
                # إرسال طلب التهجين إلى نظام الذكاء الاصطناعي
                try:
                    # تحضير البيانات
                    breeding_data = {
                        "request_id": request_id,
                        "parent_varieties": json.loads(parent_varieties) if parent_varieties else [],
                        "breeding_goals": json.loads(breeding_goals) if breeding_goals else [],
                        "constraints": json.loads(constraints) if constraints else {},
                        "parameters": json.loads(parameters) if parameters else {}
                    }
                    
                    response = self._send_breeding_request(breeding_data)
                    
                    if response.get("success"):
                        self._update_breeding_request_status(request_id, "processing")
                    else:
                        self._update_breeding_request_status(request_id, "failed", response.get("error", "فشل في إرسال طلب التهجين"))
                except Exception as e:
                    self.logger.error(f"خطأ في إرسال طلب التهجين: {str(e)}")
                    self._update_breeding_request_status(request_id, "failed", str(e))
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة طلبات التهجين: {str(e)}")
    
    def _send_breeding_request(self, breeding_data: Dict[str, Any]) -> Dict[str, Any]:
        """إرسال طلب تهجين إلى نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # إرسال الطلب
            response = requests.post(
                f"{self.api_base_url}/breeding/submit",
                json=breeding_data,
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في إرسال طلب التهجين: {response.status_code} - {response.text}")
                return {"success": False, "error": f"فشل في إرسال طلب التهجين: {response.status_code}"}
        except Exception as e:
            self.logger.error(f"خطأ في إرسال طلب التهجين: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _update_breeding_request_status(self, request_id: str, status: str, error_message: Optional[str] = None):
        """تحديث حالة طلب التهجين"""
        try:
            # بناء الاستعلام
            query = """
                UPDATE ai_breeding_requests
                SET status = %s, updated_at = %s
            """
            
            params = [status, datetime.now()]
            
            # إضافة رسالة الخطأ إذا تم توفيرها
            if error_message is not None:
                query += ", error_message = %s"
                params.append(error_message)
            
            # إضافة شرط المعرف
            query += " WHERE request_id = %s"
            params.append(request_id)
            
            # تنفيذ الاستعلام
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة طلب التهجين: {str(e)}")
    
    def _sync_breeding_results(self):
        """مزامنة نتائج التهجين"""
        try:
            # الحصول على طلبات التهجين قيد المعالجة
            query = """
                SELECT request_id
                FROM ai_breeding_requests
                WHERE status = 'processing'
            """
            
            results = self.db_manager.execute_query(query)
            
            for result in results:
                request_id = result[0]
                
                # التحقق من حالة طلب التهجين في نظام الذكاء الاصطناعي
                try:
                    response = self._check_breeding_status(request_id)
                    
                    if response.get("success"):
                        status = response.get("status")
                        
                        if status == "completed":
                            # الحصول على نتيجة التهجين
                            breeding_result = response.get("result")
                            
                            # حفظ نتيجة التهجين
                            self._save_breeding_result(request_id, breeding_result)
                            
                            # تحديث حالة طلب التهجين
                            self._update_breeding_request_status(request_id, "completed")
                        elif status == "failed":
                            # تحديث حالة طلب التهجين
                            self._update_breeding_request_status(request_id, "failed", response.get("error", "فشل في معالجة طلب التهجين"))
                    else:
                        self.logger.error(f"فشل في التحقق من حالة طلب التهجين: {response.get('error')}")
                except Exception as e:
                    self.logger.error(f"خطأ في التحقق من حالة طلب التهجين: {str(e)}")
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة نتائج التهجين: {str(e)}")
    
    def _check_breeding_status(self, request_id: str) -> Dict[str, Any]:
        """التحقق من حالة طلب التهجين في نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/breeding/{request_id}/status",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في التحقق من حالة طلب التهجين: {response.status_code} - {response.text}")
                return {"success": False, "error": f"فشل في التحقق من حالة طلب التهجين: {response.status_code}"}
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من حالة طلب التهجين: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _save_breeding_result(self, request_id: str, breeding_result: Dict[str, Any]):
        """حفظ نتيجة التهجين"""
        try:
            # استخراج البيانات
            result_id = breeding_result.get("result_id")
            recommended_crosses = json.dumps(breeding_result.get("recommended_crosses", []))
            predicted_traits = json.dumps(breeding_result.get("predicted_traits", {}))
            simulation_details = json.dumps(breeding_result.get("simulation_details", {}))
            
            # حفظ نتيجة التهجين
            query = """
                INSERT INTO ai_breeding_results (
                    result_id, request_id, recommended_crosses, predicted_traits,
                    simulation_details, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                result_id,
                request_id,
                recommended_crosses,
                predicted_traits,
                simulation_details,
                datetime.now()
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ نتيجة التهجين: {str(e)}")
            raise
    
    def _sync_shared_data(self):
        """مزامنة البيانات المشتركة"""
        try:
            # مزامنة بيانات المشاتل
            self._sync_nursery_data()
            
            # مزامنة بيانات المزارع
            self._sync_farm_data()
            
            # مزامنة بيانات الأصناف
            self._sync_variety_data()
            
            # مزامنة بيانات الأمراض
            self._sync_disease_data()
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة البيانات المشتركة: {str(e)}")
    
    def _sync_nursery_data(self):
        """مزامنة بيانات المشاتل"""
        try:
            # الحصول على بيانات المشاتل
            query = """
                SELECT n.nursery_id, n.name, n.location, n.capacity, n.current_occupancy,
                       n.manager_id, n.description, n.created_at, n.updated_at,
                       JSON_ARRAYAGG(
                           JSON_OBJECT(
                               'stock_id', s.stock_id,
                               'variety_id', s.variety_id,
                               'quantity', s.quantity,
                               'status', s.status,
                               'planting_date', s.planting_date,
                               'expected_harvest_date', s.expected_harvest_date
                           )
                       ) AS stocks
                FROM nurseries n
                LEFT JOIN nursery_stocks s ON n.nursery_id = s.nursery_id
                GROUP BY n.nursery_id
            """
            
            results = self.db_manager.execute_query(query)
            
            # تحضير البيانات
            nursery_data = []
            for result in results:
                nursery_id, name, location, capacity, current_occupancy, manager_id, description, created_at, updated_at, stocks = result
                
                nursery = {
                    "nursery_id": nursery_id,
                    "name": name,
                    "location": location,
                    "capacity": capacity,
                    "current_occupancy": current_occupancy,
                    "manager_id": manager_id,
                    "description": description,
                    "created_at": created_at.isoformat() if created_at else None,
                    "updated_at": updated_at.isoformat() if updated_at else None,
                    "stocks": json.loads(stocks) if stocks else []
                }
                
                nursery_data.append(nursery)
            
            # حفظ البيانات في ملف
            nursery_file = os.path.join(self.shared_data_dir, "nursery_data.json")
            with open(nursery_file, "w") as f:
                json.dump(nursery_data, f, indent=2)
            
            # نسخ الملف إلى مجلد Docker
            docker_data_dir = self.ai_system_config.get("docker_data_dir")
            if docker_data_dir:
                docker_nursery_file = os.path.join(docker_data_dir, "nursery_data.json")
                os.makedirs(os.path.dirname(docker_nursery_file), exist_ok=True)
                shutil.copy2(nursery_file, docker_nursery_file)
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة بيانات المشاتل: {str(e)}")
    
    def _sync_farm_data(self):
        """مزامنة بيانات المزارع"""
        try:
            # الحصول على بيانات المزارع
            query = """
                SELECT f.farm_id, f.name, f.location, f.area, f.soil_type,
                       f.manager_id, f.description, f.created_at, f.updated_at,
                       JSON_ARRAYAGG(
                           JSON_OBJECT(
                               'plot_id', p.plot_id,
                               'name', p.name,
                               'area', p.area,
                               'crop_type', p.crop_type,
                               'variety_id', p.variety_id,
                               'planting_date', p.planting_date,
                               'expected_harvest_date', p.expected_harvest_date,
                               'status', p.status
                           )
                       ) AS plots
                FROM farms f
                LEFT JOIN farm_plots p ON f.farm_id = p.farm_id
                GROUP BY f.farm_id
            """
            
            results = self.db_manager.execute_query(query)
            
            # تحضير البيانات
            farm_data = []
            for result in results:
                farm_id, name, location, area, soil_type, manager_id, description, created_at, updated_at, plots = result
                
                farm = {
                    "farm_id": farm_id,
                    "name": name,
                    "location": location,
                    "area": area,
                    "soil_type": soil_type,
                    "manager_id": manager_id,
                    "description": description,
                    "created_at": created_at.isoformat() if created_at else None,
                    "updated_at": updated_at.isoformat() if updated_at else None,
                    "plots": json.loads(plots) if plots else []
                }
                
                farm_data.append(farm)
            
            # حفظ البيانات في ملف
            farm_file = os.path.join(self.shared_data_dir, "farm_data.json")
            with open(farm_file, "w") as f:
                json.dump(farm_data, f, indent=2)
            
            # نسخ الملف إلى مجلد Docker
            docker_data_dir = self.ai_system_config.get("docker_data_dir")
            if docker_data_dir:
                docker_farm_file = os.path.join(docker_data_dir, "farm_data.json")
                os.makedirs(os.path.dirname(docker_farm_file), exist_ok=True)
                shutil.copy2(farm_file, docker_farm_file)
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة بيانات المزارع: {str(e)}")
    
    def _sync_variety_data(self):
        """مزامنة بيانات الأصناف"""
        try:
            # الحصول على بيانات الأصناف
            query = """
                SELECT v.variety_id, v.name, v.crop_type, v.description,
                       v.growth_duration, v.optimal_temperature, v.optimal_humidity,
                       v.disease_resistance, v.yield_potential, v.created_at, v.updated_at
                FROM plant_varieties v
            """
            
            results = self.db_manager.execute_query(query)
            
            # تحضير البيانات
            variety_data = []
            for result in results:
                variety_id, name, crop_type, description, growth_duration, optimal_temperature, optimal_humidity, disease_resistance, yield_potential, created_at, updated_at = result
                
                variety = {
                    "variety_id": variety_id,
                    "name": name,
                    "crop_type": crop_type,
                    "description": description,
                    "growth_duration": growth_duration,
                    "optimal_temperature": optimal_temperature,
                    "optimal_humidity": optimal_humidity,
                    "disease_resistance": json.loads(disease_resistance) if disease_resistance else {},
                    "yield_potential": yield_potential,
                    "created_at": created_at.isoformat() if created_at else None,
                    "updated_at": updated_at.isoformat() if updated_at else None
                }
                
                variety_data.append(variety)
            
            # حفظ البيانات في ملف
            variety_file = os.path.join(self.shared_data_dir, "variety_data.json")
            with open(variety_file, "w") as f:
                json.dump(variety_data, f, indent=2)
            
            # نسخ الملف إلى مجلد Docker
            docker_data_dir = self.ai_system_config.get("docker_data_dir")
            if docker_data_dir:
                docker_variety_file = os.path.join(docker_data_dir, "variety_data.json")
                os.makedirs(os.path.dirname(docker_variety_file), exist_ok=True)
                shutil.copy2(variety_file, docker_variety_file)
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة بيانات الأصناف: {str(e)}")
    
    def _sync_disease_data(self):
        """مزامنة بيانات الأمراض"""
        try:
            # الحصول على بيانات الأمراض
            query = """
                SELECT d.disease_id, d.name, d.pathogen_type, d.description,
                       d.symptoms, d.affected_crops, d.treatment_methods,
                       d.prevention_methods, d.created_at, d.updated_at
                FROM plant_diseases d
            """
            
            results = self.db_manager.execute_query(query)
            
            # تحضير البيانات
            disease_data = []
            for result in results:
                disease_id, name, pathogen_type, description, symptoms, affected_crops, treatment_methods, prevention_methods, created_at, updated_at = result
                
                disease = {
                    "disease_id": disease_id,
                    "name": name,
                    "pathogen_type": pathogen_type,
                    "description": description,
                    "symptoms": json.loads(symptoms) if symptoms else [],
                    "affected_crops": json.loads(affected_crops) if affected_crops else [],
                    "treatment_methods": json.loads(treatment_methods) if treatment_methods else [],
                    "prevention_methods": json.loads(prevention_methods) if prevention_methods else [],
                    "created_at": created_at.isoformat() if created_at else None,
                    "updated_at": updated_at.isoformat() if updated_at else None
                }
                
                disease_data.append(disease)
            
            # حفظ البيانات في ملف
            disease_file = os.path.join(self.shared_data_dir, "disease_data.json")
            with open(disease_file, "w") as f:
                json.dump(disease_data, f, indent=2)
            
            # نسخ الملف إلى مجلد Docker
            docker_data_dir = self.ai_system_config.get("docker_data_dir")
            if docker_data_dir:
                docker_disease_file = os.path.join(docker_data_dir, "disease_data.json")
                os.makedirs(os.path.dirname(docker_disease_file), exist_ok=True)
                shutil.copy2(disease_file, docker_disease_file)
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة بيانات الأمراض: {str(e)}")
    
    def import_ai_system_data(self):
        """استيراد البيانات من نظام الذكاء الاصطناعي"""
        try:
            # استيراد بيانات الأمراض
            self._import_disease_data()
            
            # استيراد بيانات التشخيص
            self._import_diagnosis_data()
            
            # استيراد بيانات التهجين
            self._import_breeding_data()
            
            return True
        except Exception as e:
            self.logger.error(f"خطأ في استيراد البيانات من نظام الذكاء الاصطناعي: {str(e)}")
            return False
    
    def _import_disease_data(self):
        """استيراد بيانات الأمراض من نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/diseases",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                diseases = response.json().get("data", [])
                
                # حفظ البيانات في قاعدة البيانات
                for disease in diseases:
                    # التحقق من وجود المرض
                    query = """
                        SELECT COUNT(*)
                        FROM plant_diseases
                        WHERE disease_id = %s
                    """
                    
                    result = self.db_manager.execute_query(query, (disease.get("disease_id"),), fetch_one=True)
                    
                    if result[0] > 0:
                        # تحديث المرض
                        query = """
                            UPDATE plant_diseases
                            SET name = %s, pathogen_type = %s, description = %s,
                                symptoms = %s, affected_crops = %s, treatment_methods = %s,
                                prevention_methods = %s, updated_at = %s
                            WHERE disease_id = %s
                        """
                        
                        params = (
                            disease.get("name"),
                            disease.get("pathogen_type"),
                            disease.get("description"),
                            json.dumps(disease.get("symptoms", [])),
                            json.dumps(disease.get("affected_crops", [])),
                            json.dumps(disease.get("treatment_methods", [])),
                            json.dumps(disease.get("prevention_methods", [])),
                            datetime.now(),
                            disease.get("disease_id")
                        )
                        
                        self.db_manager.execute_query(query, params)
                    else:
                        # إضافة المرض
                        query = """
                            INSERT INTO plant_diseases (
                                disease_id, name, pathogen_type, description,
                                symptoms, affected_crops, treatment_methods,
                                prevention_methods, created_at, updated_at
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                            )
                        """
                        
                        params = (
                            disease.get("disease_id"),
                            disease.get("name"),
                            disease.get("pathogen_type"),
                            disease.get("description"),
                            json.dumps(disease.get("symptoms", [])),
                            json.dumps(disease.get("affected_crops", [])),
                            json.dumps(disease.get("treatment_methods", [])),
                            json.dumps(disease.get("prevention_methods", [])),
                            datetime.now(),
                            datetime.now()
                        )
                        
                        self.db_manager.execute_query(query, params)
            else:
                self.logger.error(f"فشل في استيراد بيانات الأمراض: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"خطأ في استيراد بيانات الأمراض: {str(e)}")
            raise
    
    def _import_diagnosis_data(self):
        """استيراد بيانات التشخيص من نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/diagnosis/recent",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                diagnoses = response.json().get("data", [])
                
                # حفظ البيانات في قاعدة البيانات
                for diagnosis in diagnoses:
                    # التحقق من وجود التشخيص
                    query = """
                        SELECT COUNT(*)
                        FROM ai_diagnosis_results
                        WHERE result_id = %s
                    """
                    
                    result = self.db_manager.execute_query(query, (diagnosis.get("result_id"),), fetch_one=True)
                    
                    if result[0] == 0:
                        # إضافة التشخيص
                        query = """
                            INSERT INTO ai_diagnosis_results (
                                result_id, request_id, disease_name, confidence,
                                diagnosis_details, treatment_recommendations, result_images,
                                created_at
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s
                            )
                        """
                        
                        params = (
                            diagnosis.get("result_id"),
                            diagnosis.get("request_id"),
                            diagnosis.get("disease_name"),
                            diagnosis.get("confidence"),
                            json.dumps(diagnosis.get("details", {})),
                            json.dumps(diagnosis.get("treatment_recommendations", [])),
                            json.dumps(diagnosis.get("result_images", [])),
                            datetime.now()
                        )
                        
                        self.db_manager.execute_query(query, params)
                        
                        # تحديث حالة طلب التشخيص
                        query = """
                            UPDATE ai_diagnosis_requests
                            SET status = 'completed', updated_at = %s
                            WHERE request_id = %s
                        """
                        
                        params = (
                            datetime.now(),
                            diagnosis.get("request_id")
                        )
                        
                        self.db_manager.execute_query(query, params)
            else:
                self.logger.error(f"فشل في استيراد بيانات التشخيص: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"خطأ في استيراد بيانات التشخيص: {str(e)}")
            raise
    
    def _import_breeding_data(self):
        """استيراد بيانات التهجين من نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/breeding/recent",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                breedings = response.json().get("data", [])
                
                # حفظ البيانات في قاعدة البيانات
                for breeding in breedings:
                    # التحقق من وجود التهجين
                    query = """
                        SELECT COUNT(*)
                        FROM ai_breeding_results
                        WHERE result_id = %s
                    """
                    
                    result = self.db_manager.execute_query(query, (breeding.get("result_id"),), fetch_one=True)
                    
                    if result[0] == 0:
                        # إضافة التهجين
                        query = """
                            INSERT INTO ai_breeding_results (
                                result_id, request_id, recommended_crosses, predicted_traits,
                                simulation_details, created_at
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s
                            )
                        """
                        
                        params = (
                            breeding.get("result_id"),
                            breeding.get("request_id"),
                            json.dumps(breeding.get("recommended_crosses", [])),
                            json.dumps(breeding.get("predicted_traits", {})),
                            json.dumps(breeding.get("simulation_details", {})),
                            datetime.now()
                        )
                        
                        self.db_manager.execute_query(query, params)
                        
                        # تحديث حالة طلب التهجين
                        query = """
                            UPDATE ai_breeding_requests
                            SET status = 'completed', updated_at = %s
                            WHERE request_id = %s
                        """
                        
                        params = (
                            datetime.now(),
                            breeding.get("request_id")
                        )
                        
                        self.db_manager.execute_query(query, params)
            else:
                self.logger.error(f"فشل في استيراد بيانات التهجين: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"خطأ في استيراد بيانات التهجين: {str(e)}")
            raise
    
    def check_ai_system_status(self) -> Dict[str, Any]:
        """التحقق من حالة نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/system/status",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في التحقق من حالة نظام الذكاء الاصطناعي: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"فشل في التحقق من حالة نظام الذكاء الاصطناعي: {response.status_code}"
                }
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من حالة نظام الذكاء الاصطناعي: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_ai_system_models(self) -> Dict[str, Any]:
        """الحصول على نماذج نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/models",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في الحصول على نماذج نظام الذكاء الاصطناعي: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"فشل في الحصول على نماذج نظام الذكاء الاصطناعي: {response.status_code}"
                }
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على نماذج نظام الذكاء الاصطناعي: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_ai_system_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات نظام الذكاء الاصطناعي"""
        try:
            # إعداد الرؤوس
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # إرسال الطلب
            response = requests.get(
                f"{self.api_base_url}/statistics",
                headers=headers
            )
            
            # التحقق من الاستجابة
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"فشل في الحصول على إحصائيات نظام الذكاء الاصطناعي: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"فشل في الحصول على إحصائيات نظام الذكاء الاصطناعي: {response.status_code}"
                }
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على إحصائيات نظام الذكاء الاصطناعي: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
