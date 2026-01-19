"""
خدمات التكامل مع نظام الذكاء الاصطناعي الزراعي
يحتوي هذا الملف على خدمات التكامل مع نظام الذكاء الاصطناعي الزراعي
"""

import os
import json
import requests
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import shutil
import base64
from uuid import uuid4

from ..models.ai_models import (
    ImageDiagnosisRequest, DiagnosisResult, DiagnosisStatus,
    BreedingRequest, BreedingResult, BreedingStatus,
    AISystemStatus, AIModelInfo, DataSyncJob
)


class AIIntegrationService:
    """خدمة التكامل مع نظام الذكاء الاصطناعي"""
    
    def __init__(self, db_manager, config=None):
        """تهيئة خدمة التكامل مع نظام الذكاء الاصطناعي"""
        self.db_manager = db_manager
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # الحصول على عنوان API من التكوين
        self.api_base_url = self.config.get("ai_api_base_url", "http://localhost:8000/api")
        self.api_key = self.config.get("ai_api_key", "")
        
        # مسار حفظ الصور
        self.upload_dir = self.config.get("upload_dir", "/tmp/uploads")
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def _make_api_request(self, method: str, endpoint: str, data=None, files=None) -> Dict[str, Any]:
        """إجراء طلب API إلى نظام الذكاء الاصطناعي"""
        url = f"{self.api_base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            if method.lower() == "get":
                response = requests.get(url, headers=headers, params=data)
            elif method.lower() == "post":
                if files:
                    response = requests.post(url, headers=headers, data=data, files=files)
                else:
                    headers["Content-Type"] = "application/json"
                    response = requests.post(url, headers=headers, json=data)
            elif method.lower() == "put":
                headers["Content-Type"] = "application/json"
                response = requests.put(url, headers=headers, json=data)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"طريقة HTTP غير مدعومة: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"خطأ في طلب API: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def check_system_status(self) -> AISystemStatus:
        """التحقق من حالة نظام الذكاء الاصطناعي"""
        try:
            response = self._make_api_request("get", "system/status")
            
            if response.get("success", False):
                status_data = response.get("data", {})
                return AISystemStatus.from_dict(status_data)
            else:
                # إنشاء حالة نظام غير متصل
                return AISystemStatus(
                    is_online=False,
                    version="unknown",
                    components_status={"error": True},
                    metrics={"error_message": response.get("error", "خطأ غير معروف")}
                )
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من حالة النظام: {str(e)}")
            return AISystemStatus(
                is_online=False,
                version="unknown",
                components_status={"error": True},
                metrics={"error_message": str(e)}
            )
    
    def get_available_models(self) -> List[AIModelInfo]:
        """الحصول على النماذج المتاحة"""
        try:
            response = self._make_api_request("get", "models")
            
            if response.get("success", False):
                models_data = response.get("data", [])
                return [AIModelInfo.from_dict(model_data) for model_data in models_data]
            else:
                self.logger.error(f"فشل في الحصول على النماذج المتاحة: {response.get('error', 'خطأ غير معروف')}")
                return []
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على النماذج المتاحة: {str(e)}")
            return []
    
    def create_diagnosis_request(self, request_data: Dict[str, Any]) -> ImageDiagnosisRequest:
        """إنشاء طلب تشخيص جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["image_path", "user_id", "plant_type"]
        for field in required_fields:
            if field not in request_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # إنشاء طلب تشخيص جديد
        diagnosis_request = ImageDiagnosisRequest(
            image_path=request_data["image_path"],
            user_id=request_data["user_id"],
            plant_type=request_data["plant_type"],
            description=request_data.get("description"),
            metadata=request_data.get("metadata", {})
        )
        
        # حفظ طلب التشخيص في قاعدة البيانات
        self._save_diagnosis_request(diagnosis_request)
        
        return diagnosis_request
    
    def _save_diagnosis_request(self, diagnosis_request: ImageDiagnosisRequest) -> None:
        """حفظ طلب تشخيص في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            request_dict = diagnosis_request.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO ai_diagnosis_requests (
                    request_id, image_path, user_id, plant_type, description,
                    metadata, status, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                request_dict["request_id"],
                request_dict["image_path"],
                request_dict["user_id"],
                request_dict["plant_type"],
                request_dict["description"],
                json.dumps(request_dict["metadata"]),
                request_dict["status"],
                request_dict["created_at"],
                request_dict["updated_at"]
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ طلب التشخيص: {str(e)}")
            raise
    
    def get_diagnosis_request(self, request_id: str) -> Optional[ImageDiagnosisRequest]:
        """الحصول على طلب تشخيص بواسطة المعرف"""
        try:
            query = """
                SELECT request_id, image_path, user_id, plant_type, description,
                       metadata, status, created_at, updated_at, result
                FROM ai_diagnosis_requests
                WHERE request_id = %s
            """
            
            result = self.db_manager.execute_query(query, (request_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            request_dict = {
                "request_id": result[0],
                "image_path": result[1],
                "user_id": result[2],
                "plant_type": result[3],
                "description": result[4],
                "metadata": json.loads(result[5]) if result[5] else {},
                "status": result[6],
                "created_at": result[7],
                "updated_at": result[8],
                "result": json.loads(result[9]) if result[9] else None
            }
            
            return ImageDiagnosisRequest.from_dict(request_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على طلب التشخيص: {str(e)}")
            return None
    
    def get_all_diagnosis_requests(
        self,
        user_id: Optional[str] = None,
        status: Optional[DiagnosisStatus] = None,
        plant_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ImageDiagnosisRequest], int]:
        """الحصول على جميع طلبات التشخيص"""
        try:
            # بناء الاستعلام
            query = """
                SELECT request_id, image_path, user_id, plant_type, description,
                       metadata, status, created_at, updated_at, result
                FROM ai_diagnosis_requests
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM ai_diagnosis_requests
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if user_id:
                query += " AND user_id = %s"
                count_query += " AND user_id = %s"
                params.append(user_id)
            
            if status:
                query += " AND status = %s"
                count_query += " AND status = %s"
                params.append(status.value)
            
            if plant_type:
                query += " AND plant_type = %s"
                count_query += " AND plant_type = %s"
                params.append(plant_type)
            
            # إضافة الترتيب والحد
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # تنفيذ استعلام العدد
            count_result = self.db_manager.execute_query(count_query, params[:-2], fetch_one=True)
            total = count_result[0] if count_result else 0
            
            # تنفيذ استعلام البيانات
            results = self.db_manager.execute_query(query, params)
            
            # تحويل النتائج إلى كائنات
            requests = []
            for result in results:
                request_dict = {
                    "request_id": result[0],
                    "image_path": result[1],
                    "user_id": result[2],
                    "plant_type": result[3],
                    "description": result[4],
                    "metadata": json.loads(result[5]) if result[5] else {},
                    "status": result[6],
                    "created_at": result[7],
                    "updated_at": result[8],
                    "result": json.loads(result[9]) if result[9] else None
                }
                
                requests.append(ImageDiagnosisRequest.from_dict(request_dict))
            
            return requests, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على طلبات التشخيص: {str(e)}")
            return [], 0
    
    def submit_diagnosis_request(self, request_id: str) -> bool:
        """إرسال طلب تشخيص إلى نظام الذكاء الاصطناعي"""
        try:
            # الحصول على طلب التشخيص
            diagnosis_request = self.get_diagnosis_request(request_id)
            if not diagnosis_request:
                self.logger.error(f"لم يتم العثور على طلب التشخيص بالمعرف {request_id}")
                return False
            
            # تحديث حالة الطلب إلى قيد المعالجة
            diagnosis_request.status = DiagnosisStatus.PROCESSING
            diagnosis_request.updated_at = datetime.now()
            self._update_diagnosis_request_status(request_id, DiagnosisStatus.PROCESSING)
            
            # التحقق من وجود الصورة
            image_path = diagnosis_request.image_path
            if not os.path.exists(image_path):
                self.logger.error(f"لم يتم العثور على الصورة في المسار {image_path}")
                self._update_diagnosis_request_status(request_id, DiagnosisStatus.FAILED)
                return False
            
            # إرسال الطلب إلى نظام الذكاء الاصطناعي
            with open(image_path, "rb") as image_file:
                files = {"image": (os.path.basename(image_path), image_file, "image/jpeg")}
                data = {
                    "request_id": request_id,
                    "plant_type": diagnosis_request.plant_type,
                    "description": diagnosis_request.description or "",
                    "metadata": json.dumps(diagnosis_request.metadata)
                }
                
                response = self._make_api_request("post", "diagnosis", data=data, files=files)
            
            if response.get("success", False):
                # تحديث حالة الطلب إلى مكتمل
                self._update_diagnosis_request_status(request_id, DiagnosisStatus.COMPLETED)
                
                # حفظ نتيجة التشخيص
                result_data = response.get("data", {})
                diagnosis_result = DiagnosisResult(
                    request_id=request_id,
                    disease_name=result_data.get("disease_name"),
                    confidence=result_data.get("confidence"),
                    recommendations=result_data.get("recommendations", []),
                    details=result_data.get("details", {})
                )
                
                self._save_diagnosis_result(diagnosis_result)
                return True
            else:
                # تحديث حالة الطلب إلى فشل
                self._update_diagnosis_request_status(request_id, DiagnosisStatus.FAILED)
                self.logger.error(f"فشل في إرسال طلب التشخيص: {response.get('error', 'خطأ غير معروف')}")
                return False
        except Exception as e:
            self.logger.error(f"خطأ في إرسال طلب التشخيص: {str(e)}")
            self._update_diagnosis_request_status(request_id, DiagnosisStatus.FAILED)
            return False
    
    def _update_diagnosis_request_status(self, request_id: str, status: DiagnosisStatus) -> None:
        """تحديث حالة طلب تشخيص"""
        try:
            query = """
                UPDATE ai_diagnosis_requests
                SET status = %s, updated_at = %s
                WHERE request_id = %s
            """
            
            params = (status.value, datetime.now(), request_id)
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة طلب التشخيص: {str(e)}")
            raise
    
    def _save_diagnosis_result(self, diagnosis_result: DiagnosisResult) -> None:
        """حفظ نتيجة تشخيص في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            result_dict = diagnosis_result.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO ai_diagnosis_results (
                    result_id, request_id, disease_name, confidence,
                    recommendations, details, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                result_dict["result_id"],
                result_dict["request_id"],
                result_dict["disease_name"],
                result_dict["confidence"],
                json.dumps(result_dict["recommendations"]),
                json.dumps(result_dict["details"]),
                result_dict["created_at"]
            )
            
            self.db_manager.execute_query(query, params)
            
            # تحديث نتيجة التشخيص في طلب التشخيص
            query = """
                UPDATE ai_diagnosis_requests
                SET result = %s
                WHERE request_id = %s
            """
            
            params = (json.dumps(result_dict), result_dict["request_id"])
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ نتيجة التشخيص: {str(e)}")
            raise
    
    def get_diagnosis_result(self, result_id: str) -> Optional[DiagnosisResult]:
        """الحصول على نتيجة تشخيص بواسطة المعرف"""
        try:
            query = """
                SELECT result_id, request_id, disease_name, confidence,
                       recommendations, details, created_at
                FROM ai_diagnosis_results
                WHERE result_id = %s
            """
            
            result = self.db_manager.execute_query(query, (result_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            result_dict = {
                "result_id": result[0],
                "request_id": result[1],
                "disease_name": result[2],
                "confidence": result[3],
                "recommendations": json.loads(result[4]) if result[4] else [],
                "details": json.loads(result[5]) if result[5] else {},
                "created_at": result[6]
            }
            
            return DiagnosisResult.from_dict(result_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على نتيجة التشخيص: {str(e)}")
            return None
    
    def get_diagnosis_results_by_request(self, request_id: str) -> List[DiagnosisResult]:
        """الحصول على نتائج التشخيص بواسطة معرف الطلب"""
        try:
            query = """
                SELECT result_id, request_id, disease_name, confidence,
                       recommendations, details, created_at
                FROM ai_diagnosis_results
                WHERE request_id = %s
                ORDER BY created_at DESC
            """
            
            results = self.db_manager.execute_query(query, (request_id,))
            
            # تحويل النتائج إلى كائنات
            diagnosis_results = []
            for result in results:
                result_dict = {
                    "result_id": result[0],
                    "request_id": result[1],
                    "disease_name": result[2],
                    "confidence": result[3],
                    "recommendations": json.loads(result[4]) if result[4] else [],
                    "details": json.loads(result[5]) if result[5] else {},
                    "created_at": result[6]
                }
                
                diagnosis_results.append(DiagnosisResult.from_dict(result_dict))
            
            return diagnosis_results
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على نتائج التشخيص: {str(e)}")
            return []
    
    def upload_image(self, image_data: bytes, file_name: Optional[str] = None) -> str:
        """رفع صورة إلى النظام"""
        try:
            # إنشاء اسم ملف فريد إذا لم يتم توفيره
            if not file_name:
                file_name = f"{uuid4()}.jpg"
            
            # التأكد من أن اسم الملف آمن
            file_name = os.path.basename(file_name)
            
            # إنشاء مسار الملف
            file_path = os.path.join(self.upload_dir, file_name)
            
            # حفظ الصورة
            with open(file_path, "wb") as f:
                f.write(image_data)
            
            return file_path
        except Exception as e:
            self.logger.error(f"خطأ في رفع الصورة: {str(e)}")
            raise
    
    def create_breeding_request(self, request_data: Dict[str, Any]) -> BreedingRequest:
        """إنشاء طلب تهجين جديد"""
        # التحقق من البيانات المطلوبة
        required_fields = ["parent1_id", "parent2_id", "user_id", "breeding_goal"]
        for field in required_fields:
            if field not in request_data:
                raise ValueError(f"الحقل {field} مطلوب")
        
        # إنشاء طلب تهجين جديد
        breeding_request = BreedingRequest(
            parent1_id=request_data["parent1_id"],
            parent2_id=request_data["parent2_id"],
            user_id=request_data["user_id"],
            breeding_goal=request_data["breeding_goal"],
            description=request_data.get("description"),
            metadata=request_data.get("metadata", {})
        )
        
        # حفظ طلب التهجين في قاعدة البيانات
        self._save_breeding_request(breeding_request)
        
        return breeding_request
    
    def _save_breeding_request(self, breeding_request: BreedingRequest) -> None:
        """حفظ طلب تهجين في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            request_dict = breeding_request.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO ai_breeding_requests (
                    request_id, parent1_id, parent2_id, user_id, breeding_goal,
                    description, metadata, status, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                request_dict["request_id"],
                request_dict["parent1_id"],
                request_dict["parent2_id"],
                request_dict["user_id"],
                request_dict["breeding_goal"],
                request_dict["description"],
                json.dumps(request_dict["metadata"]),
                request_dict["status"],
                request_dict["created_at"],
                request_dict["updated_at"]
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ طلب التهجين: {str(e)}")
            raise
    
    def get_breeding_request(self, request_id: str) -> Optional[BreedingRequest]:
        """الحصول على طلب تهجين بواسطة المعرف"""
        try:
            query = """
                SELECT request_id, parent1_id, parent2_id, user_id, breeding_goal,
                       description, metadata, status, created_at, updated_at, result
                FROM ai_breeding_requests
                WHERE request_id = %s
            """
            
            result = self.db_manager.execute_query(query, (request_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            request_dict = {
                "request_id": result[0],
                "parent1_id": result[1],
                "parent2_id": result[2],
                "user_id": result[3],
                "breeding_goal": result[4],
                "description": result[5],
                "metadata": json.loads(result[6]) if result[6] else {},
                "status": result[7],
                "created_at": result[8],
                "updated_at": result[9],
                "result": json.loads(result[10]) if result[10] else None
            }
            
            return BreedingRequest.from_dict(request_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على طلب التهجين: {str(e)}")
            return None
    
    def get_all_breeding_requests(
        self,
        user_id: Optional[str] = None,
        status: Optional[BreedingStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[BreedingRequest], int]:
        """الحصول على جميع طلبات التهجين"""
        try:
            # بناء الاستعلام
            query = """
                SELECT request_id, parent1_id, parent2_id, user_id, breeding_goal,
                       description, metadata, status, created_at, updated_at, result
                FROM ai_breeding_requests
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM ai_breeding_requests
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if user_id:
                query += " AND user_id = %s"
                count_query += " AND user_id = %s"
                params.append(user_id)
            
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
            requests = []
            for result in results:
                request_dict = {
                    "request_id": result[0],
                    "parent1_id": result[1],
                    "parent2_id": result[2],
                    "user_id": result[3],
                    "breeding_goal": result[4],
                    "description": result[5],
                    "metadata": json.loads(result[6]) if result[6] else {},
                    "status": result[7],
                    "created_at": result[8],
                    "updated_at": result[9],
                    "result": json.loads(result[10]) if result[10] else None
                }
                
                requests.append(BreedingRequest.from_dict(request_dict))
            
            return requests, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على طلبات التهجين: {str(e)}")
            return [], 0
    
    def submit_breeding_request(self, request_id: str) -> bool:
        """إرسال طلب تهجين إلى نظام الذكاء الاصطناعي"""
        try:
            # الحصول على طلب التهجين
            breeding_request = self.get_breeding_request(request_id)
            if not breeding_request:
                self.logger.error(f"لم يتم العثور على طلب التهجين بالمعرف {request_id}")
                return False
            
            # تحديث حالة الطلب إلى قيد المعالجة
            breeding_request.status = BreedingStatus.PROCESSING
            breeding_request.updated_at = datetime.now()
            self._update_breeding_request_status(request_id, BreedingStatus.PROCESSING)
            
            # إرسال الطلب إلى نظام الذكاء الاصطناعي
            data = {
                "request_id": request_id,
                "parent1_id": breeding_request.parent1_id,
                "parent2_id": breeding_request.parent2_id,
                "breeding_goal": breeding_request.breeding_goal,
                "description": breeding_request.description or "",
                "metadata": breeding_request.metadata
            }
            
            response = self._make_api_request("post", "breeding", data=data)
            
            if response.get("success", False):
                # تحديث حالة الطلب إلى جاري التنفيذ
                self._update_breeding_request_status(request_id, BreedingStatus.ONGOING)
                return True
            else:
                # تحديث حالة الطلب إلى فشل
                self._update_breeding_request_status(request_id, BreedingStatus.FAILED)
                self.logger.error(f"فشل في إرسال طلب التهجين: {response.get('error', 'خطأ غير معروف')}")
                return False
        except Exception as e:
            self.logger.error(f"خطأ في إرسال طلب التهجين: {str(e)}")
            self._update_breeding_request_status(request_id, BreedingStatus.FAILED)
            return False
    
    def _update_breeding_request_status(self, request_id: str, status: BreedingStatus) -> None:
        """تحديث حالة طلب تهجين"""
        try:
            query = """
                UPDATE ai_breeding_requests
                SET status = %s, updated_at = %s
                WHERE request_id = %s
            """
            
            params = (status.value, datetime.now(), request_id)
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في تحديث حالة طلب التهجين: {str(e)}")
            raise
    
    def check_breeding_status(self, request_id: str) -> Dict[str, Any]:
        """التحقق من حالة طلب تهجين"""
        try:
            # الحصول على طلب التهجين
            breeding_request = self.get_breeding_request(request_id)
            if not breeding_request:
                return {"success": False, "error": f"لم يتم العثور على طلب التهجين بالمعرف {request_id}"}
            
            # إذا كانت الحالة مكتملة أو فشل، إرجاع الحالة الحالية
            if breeding_request.status in [BreedingStatus.COMPLETED, BreedingStatus.FAILED]:
                return {
                    "success": True,
                    "status": breeding_request.status.value,
                    "result": breeding_request.result
                }
            
            # التحقق من حالة الطلب في نظام الذكاء الاصطناعي
            response = self._make_api_request("get", f"breeding/{request_id}/status")
            
            if response.get("success", False):
                status_data = response.get("data", {})
                current_status = status_data.get("status")
                
                # تحديث حالة الطلب إذا تغيرت
                if current_status and current_status != breeding_request.status.value:
                    new_status = BreedingStatus(current_status)
                    self._update_breeding_request_status(request_id, new_status)
                    
                    # إذا كانت الحالة مكتملة، حفظ النتيجة
                    if new_status == BreedingStatus.COMPLETED and "result" in status_data:
                        result_data = status_data["result"]
                        breeding_result = BreedingResult(
                            request_id=request_id,
                            offspring_id=result_data.get("offspring_id"),
                            characteristics=result_data.get("characteristics", {}),
                            success_rate=result_data.get("success_rate"),
                            details=result_data.get("details", {})
                        )
                        
                        self._save_breeding_result(breeding_result)
                
                return {
                    "success": True,
                    "status": current_status,
                    "progress": status_data.get("progress"),
                    "estimated_completion": status_data.get("estimated_completion"),
                    "result": status_data.get("result")
                }
            else:
                return {
                    "success": False,
                    "error": response.get("error", "خطأ غير معروف"),
                    "status": breeding_request.status.value
                }
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من حالة طلب التهجين: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _save_breeding_result(self, breeding_result: BreedingResult) -> None:
        """حفظ نتيجة تهجين في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            result_dict = breeding_result.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO ai_breeding_results (
                    result_id, request_id, offspring_id, characteristics,
                    success_rate, details, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                result_dict["result_id"],
                result_dict["request_id"],
                result_dict["offspring_id"],
                json.dumps(result_dict["characteristics"]),
                result_dict["success_rate"],
                json.dumps(result_dict["details"]),
                result_dict["created_at"]
            )
            
            self.db_manager.execute_query(query, params)
            
            # تحديث نتيجة التهجين في طلب التهجين
            query = """
                UPDATE ai_breeding_requests
                SET result = %s
                WHERE request_id = %s
            """
            
            params = (json.dumps(result_dict), result_dict["request_id"])
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ نتيجة التهجين: {str(e)}")
            raise
    
    def get_breeding_result(self, result_id: str) -> Optional[BreedingResult]:
        """الحصول على نتيجة تهجين بواسطة المعرف"""
        try:
            query = """
                SELECT result_id, request_id, offspring_id, characteristics,
                       success_rate, details, created_at
                FROM ai_breeding_results
                WHERE result_id = %s
            """
            
            result = self.db_manager.execute_query(query, (result_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            result_dict = {
                "result_id": result[0],
                "request_id": result[1],
                "offspring_id": result[2],
                "characteristics": json.loads(result[3]) if result[3] else {},
                "success_rate": result[4],
                "details": json.loads(result[5]) if result[5] else {},
                "created_at": result[6]
            }
            
            return BreedingResult.from_dict(result_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على نتيجة التهجين: {str(e)}")
            return None
    
    def get_breeding_results_by_request(self, request_id: str) -> List[BreedingResult]:
        """الحصول على نتائج التهجين بواسطة معرف الطلب"""
        try:
            query = """
                SELECT result_id, request_id, offspring_id, characteristics,
                       success_rate, details, created_at
                FROM ai_breeding_results
                WHERE request_id = %s
                ORDER BY created_at DESC
            """
            
            results = self.db_manager.execute_query(query, (request_id,))
            
            # تحويل النتائج إلى كائنات
            breeding_results = []
            for result in results:
                result_dict = {
                    "result_id": result[0],
                    "request_id": result[1],
                    "offspring_id": result[2],
                    "characteristics": json.loads(result[3]) if result[3] else {},
                    "success_rate": result[4],
                    "details": json.loads(result[5]) if result[5] else {},
                    "created_at": result[6]
                }
                
                breeding_results.append(BreedingResult.from_dict(result_dict))
            
            return breeding_results
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على نتائج التهجين: {str(e)}")
            return []
    
    def sync_data_to_ai_system(self, data_type: str, data: List[Dict[str, Any]]) -> DataSyncJob:
        """مزامنة البيانات إلى نظام الذكاء الاصطناعي"""
        try:
            # إنشاء مهمة مزامنة جديدة
            sync_job = DataSyncJob(
                source="erp",
                destination="ai_system",
                data_type=data_type,
                status="in_progress",
                records_count=len(data)
            )
            
            # حفظ مهمة المزامنة في قاعدة البيانات
            self._save_data_sync_job(sync_job)
            
            # إرسال البيانات إلى نظام الذكاء الاصطناعي
            response = self._make_api_request("post", f"data/sync/{data_type}", data={"data": data})
            
            if response.get("success", False):
                # تحديث حالة المهمة إلى مكتملة
                sync_job.status = "completed"
                sync_job.completed_at = datetime.now()
                self._update_data_sync_job(sync_job)
            else:
                # تحديث حالة المهمة إلى فشل
                sync_job.status = "failed"
                sync_job.error_message = response.get("error", "خطأ غير معروف")
                self._update_data_sync_job(sync_job)
            
            return sync_job
        except Exception as e:
            self.logger.error(f"خطأ في مزامنة البيانات: {str(e)}")
            
            # إنشاء مهمة مزامنة فاشلة
            sync_job = DataSyncJob(
                source="erp",
                destination="ai_system",
                data_type=data_type,
                status="failed",
                records_count=len(data) if data else 0,
                error_message=str(e)
            )
            
            # حفظ مهمة المزامنة في قاعدة البيانات
            self._save_data_sync_job(sync_job)
            
            return sync_job
    
    def _save_data_sync_job(self, sync_job: DataSyncJob) -> None:
        """حفظ مهمة مزامنة البيانات في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            job_dict = sync_job.to_dict()
            
            # حفظ في قاعدة البيانات
            query = """
                INSERT INTO ai_data_sync_jobs (
                    job_id, source, destination, data_type, status,
                    records_count, started_at, completed_at, error_message, metadata
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                job_dict["job_id"],
                job_dict["source"],
                job_dict["destination"],
                job_dict["data_type"],
                job_dict["status"],
                job_dict["records_count"],
                job_dict["started_at"],
                job_dict.get("completed_at"),
                job_dict["error_message"],
                json.dumps(job_dict["metadata"])
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ مهمة مزامنة البيانات: {str(e)}")
            raise
    
    def _update_data_sync_job(self, sync_job: DataSyncJob) -> None:
        """تحديث مهمة مزامنة البيانات في قاعدة البيانات"""
        try:
            # تحويل الكائن إلى قاموس
            job_dict = sync_job.to_dict()
            
            # تحديث في قاعدة البيانات
            query = """
                UPDATE ai_data_sync_jobs
                SET status = %s, completed_at = %s, error_message = %s
                WHERE job_id = %s
            """
            
            params = (
                job_dict["status"],
                job_dict.get("completed_at"),
                job_dict["error_message"],
                job_dict["job_id"]
            )
            
            self.db_manager.execute_query(query, params)
        except Exception as e:
            self.logger.error(f"خطأ في تحديث مهمة مزامنة البيانات: {str(e)}")
            raise
    
    def get_data_sync_job(self, job_id: str) -> Optional[DataSyncJob]:
        """الحصول على مهمة مزامنة البيانات بواسطة المعرف"""
        try:
            query = """
                SELECT job_id, source, destination, data_type, status,
                       records_count, started_at, completed_at, error_message, metadata
                FROM ai_data_sync_jobs
                WHERE job_id = %s
            """
            
            result = self.db_manager.execute_query(query, (job_id,), fetch_one=True)
            
            if not result:
                return None
            
            # تحويل النتيجة إلى قاموس
            job_dict = {
                "job_id": result[0],
                "source": result[1],
                "destination": result[2],
                "data_type": result[3],
                "status": result[4],
                "records_count": result[5],
                "started_at": result[6],
                "completed_at": result[7],
                "error_message": result[8],
                "metadata": json.loads(result[9]) if result[9] else {}
            }
            
            return DataSyncJob.from_dict(job_dict)
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على مهمة مزامنة البيانات: {str(e)}")
            return None
    
    def get_all_data_sync_jobs(
        self,
        data_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[DataSyncJob], int]:
        """الحصول على جميع مهام مزامنة البيانات"""
        try:
            # بناء الاستعلام
            query = """
                SELECT job_id, source, destination, data_type, status,
                       records_count, started_at, completed_at, error_message, metadata
                FROM ai_data_sync_jobs
                WHERE 1=1
            """
            
            count_query = """
                SELECT COUNT(*)
                FROM ai_data_sync_jobs
                WHERE 1=1
            """
            
            params = []
            
            # إضافة شروط البحث
            if data_type:
                query += " AND data_type = %s"
                count_query += " AND data_type = %s"
                params.append(data_type)
            
            if status:
                query += " AND status = %s"
                count_query += " AND status = %s"
                params.append(status)
            
            # إضافة الترتيب والحد
            query += " ORDER BY started_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            # تنفيذ استعلام العدد
            count_result = self.db_manager.execute_query(count_query, params[:-2], fetch_one=True)
            total = count_result[0] if count_result else 0
            
            # تنفيذ استعلام البيانات
            results = self.db_manager.execute_query(query, params)
            
            # تحويل النتائج إلى كائنات
            jobs = []
            for result in results:
                job_dict = {
                    "job_id": result[0],
                    "source": result[1],
                    "destination": result[2],
                    "data_type": result[3],
                    "status": result[4],
                    "records_count": result[5],
                    "started_at": result[6],
                    "completed_at": result[7],
                    "error_message": result[8],
                    "metadata": json.loads(result[9]) if result[9] else {}
                }
                
                jobs.append(DataSyncJob.from_dict(job_dict))
            
            return jobs, total
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على مهام مزامنة البيانات: {str(e)}")
            return [], 0
