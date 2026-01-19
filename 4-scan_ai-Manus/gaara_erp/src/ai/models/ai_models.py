"""
نماذج بيانات وحدة التكامل مع نظام الذكاء الاصطناعي الزراعي
يحتوي هذا الملف على تعريف نماذج البيانات اللازمة للتكامل مع نظام الذكاء الاصطناعي الزراعي
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
from uuid import uuid4


class DiagnosisStatus(str, Enum):
    """حالة التشخيص"""
    PENDING = "pending"  # قيد الانتظار
    PROCESSING = "processing"  # قيد المعالجة
    COMPLETED = "completed"  # مكتمل
    FAILED = "failed"  # فشل


class BreedingStatus(str, Enum):
    """حالة التهجين"""
    PENDING = "pending"  # قيد الانتظار
    PROCESSING = "processing"  # قيد المعالجة
    COMPLETED = "completed"  # مكتمل
    FAILED = "failed"  # فشل
    ONGOING = "ongoing"  # جاري التنفيذ


class ImageDiagnosisRequest:
    """طلب تشخيص صورة"""
    
    def __init__(
        self,
        image_path: str,
        user_id: str,
        plant_type: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        status: Optional[DiagnosisStatus] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.request_id = request_id or str(uuid4())
        self.image_path = image_path
        self.user_id = user_id
        self.plant_type = plant_type
        self.description = description
        self.metadata = metadata or {}
        self.status = status or DiagnosisStatus.PENDING
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.result = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "request_id": self.request_id,
            "image_path": self.image_path,
            "user_id": self.user_id,
            "plant_type": self.plant_type,
            "description": self.description,
            "metadata": self.metadata,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageDiagnosisRequest':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        if "status" in data and isinstance(data["status"], str):
            data["status"] = DiagnosisStatus(data["status"])
        
        request = cls(
            image_path=data["image_path"],
            user_id=data["user_id"],
            plant_type=data["plant_type"],
            description=data.get("description"),
            metadata=data.get("metadata", {}),
            request_id=data.get("request_id"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
        
        request.result = data.get("result")
        return request


class DiagnosisResult:
    """نتيجة تشخيص"""
    
    def __init__(
        self,
        request_id: str,
        disease_name: Optional[str] = None,
        confidence: Optional[float] = None,
        recommendations: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None,
        result_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.result_id = result_id or str(uuid4())
        self.request_id = request_id
        self.disease_name = disease_name
        self.confidence = confidence
        self.recommendations = recommendations or []
        self.details = details or {}
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "disease_name": self.disease_name,
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "details": self.details,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiagnosisResult':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        return cls(
            request_id=data["request_id"],
            disease_name=data.get("disease_name"),
            confidence=data.get("confidence"),
            recommendations=data.get("recommendations", []),
            details=data.get("details", {}),
            result_id=data.get("result_id"),
            created_at=data.get("created_at")
        )


class BreedingRequest:
    """طلب تهجين"""
    
    def __init__(
        self,
        parent1_id: str,
        parent2_id: str,
        user_id: str,
        breeding_goal: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        status: Optional[BreedingStatus] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.request_id = request_id or str(uuid4())
        self.parent1_id = parent1_id
        self.parent2_id = parent2_id
        self.user_id = user_id
        self.breeding_goal = breeding_goal
        self.description = description
        self.metadata = metadata or {}
        self.status = status or BreedingStatus.PENDING
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.result = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "request_id": self.request_id,
            "parent1_id": self.parent1_id,
            "parent2_id": self.parent2_id,
            "user_id": self.user_id,
            "breeding_goal": self.breeding_goal,
            "description": self.description,
            "metadata": self.metadata,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BreedingRequest':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        if "status" in data and isinstance(data["status"], str):
            data["status"] = BreedingStatus(data["status"])
        
        request = cls(
            parent1_id=data["parent1_id"],
            parent2_id=data["parent2_id"],
            user_id=data["user_id"],
            breeding_goal=data["breeding_goal"],
            description=data.get("description"),
            metadata=data.get("metadata", {}),
            request_id=data.get("request_id"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
        
        request.result = data.get("result")
        return request


class BreedingResult:
    """نتيجة تهجين"""
    
    def __init__(
        self,
        request_id: str,
        offspring_id: str,
        characteristics: Optional[Dict[str, Any]] = None,
        success_rate: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None,
        result_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.result_id = result_id or str(uuid4())
        self.request_id = request_id
        self.offspring_id = offspring_id
        self.characteristics = characteristics or {}
        self.success_rate = success_rate
        self.details = details or {}
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "offspring_id": self.offspring_id,
            "characteristics": self.characteristics,
            "success_rate": self.success_rate,
            "details": self.details,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BreedingResult':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        return cls(
            request_id=data["request_id"],
            offspring_id=data["offspring_id"],
            characteristics=data.get("characteristics", {}),
            success_rate=data.get("success_rate"),
            details=data.get("details", {}),
            result_id=data.get("result_id"),
            created_at=data.get("created_at")
        )


class AISystemStatus:
    """حالة نظام الذكاء الاصطناعي"""
    
    def __init__(
        self,
        is_online: bool,
        version: str,
        last_check: Optional[datetime] = None,
        components_status: Optional[Dict[str, bool]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        status_id: Optional[str] = None
    ):
        self.status_id = status_id or str(uuid4())
        self.is_online = is_online
        self.version = version
        self.last_check = last_check or datetime.now()
        self.components_status = components_status or {}
        self.metrics = metrics or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "status_id": self.status_id,
            "is_online": self.is_online,
            "version": self.version,
            "last_check": self.last_check.isoformat(),
            "components_status": self.components_status,
            "metrics": self.metrics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AISystemStatus':
        """إنشاء كائن من قاموس"""
        if "last_check" in data and isinstance(data["last_check"], str):
            data["last_check"] = datetime.fromisoformat(data["last_check"])
        
        return cls(
            is_online=data["is_online"],
            version=data["version"],
            last_check=data.get("last_check"),
            components_status=data.get("components_status", {}),
            metrics=data.get("metrics", {}),
            status_id=data.get("status_id")
        )


class AIModelInfo:
    """معلومات نموذج الذكاء الاصطناعي"""
    
    def __init__(
        self,
        model_id: str,
        name: str,
        version: str,
        type: str,
        description: Optional[str] = None,
        accuracy: Optional[float] = None,
        training_date: Optional[datetime] = None,
        parameters: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.model_id = model_id
        self.name = name
        self.version = version
        self.type = type
        self.description = description
        self.accuracy = accuracy
        self.training_date = training_date
        self.parameters = parameters or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        result = {
            "model_id": self.model_id,
            "name": self.name,
            "version": self.version,
            "type": self.type,
            "description": self.description,
            "accuracy": self.accuracy,
            "parameters": self.parameters,
            "metadata": self.metadata
        }
        
        if self.training_date:
            result["training_date"] = self.training_date.isoformat()
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIModelInfo':
        """إنشاء كائن من قاموس"""
        training_date = None
        if "training_date" in data and isinstance(data["training_date"], str):
            training_date = datetime.fromisoformat(data["training_date"])
        
        return cls(
            model_id=data["model_id"],
            name=data["name"],
            version=data["version"],
            type=data["type"],
            description=data.get("description"),
            accuracy=data.get("accuracy"),
            training_date=training_date,
            parameters=data.get("parameters", {}),
            metadata=data.get("metadata", {})
        )


class DataSyncJob:
    """مهمة مزامنة البيانات"""
    
    def __init__(
        self,
        source: str,
        destination: str,
        data_type: str,
        status: str,
        records_count: int,
        job_id: Optional[str] = None,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.job_id = job_id or str(uuid4())
        self.source = source
        self.destination = destination
        self.data_type = data_type
        self.status = status
        self.records_count = records_count
        self.started_at = started_at or datetime.now()
        self.completed_at = completed_at
        self.error_message = error_message
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        result = {
            "job_id": self.job_id,
            "source": self.source,
            "destination": self.destination,
            "data_type": self.data_type,
            "status": self.status,
            "records_count": self.records_count,
            "started_at": self.started_at.isoformat(),
            "error_message": self.error_message,
            "metadata": self.metadata
        }
        
        if self.completed_at:
            result["completed_at"] = self.completed_at.isoformat()
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataSyncJob':
        """إنشاء كائن من قاموس"""
        started_at = None
        if "started_at" in data and isinstance(data["started_at"], str):
            started_at = datetime.fromisoformat(data["started_at"])
        
        completed_at = None
        if "completed_at" in data and isinstance(data["completed_at"], str):
            completed_at = datetime.fromisoformat(data["completed_at"])
        
        return cls(
            source=data["source"],
            destination=data["destination"],
            data_type=data["data_type"],
            status=data["status"],
            records_count=data["records_count"],
            job_id=data.get("job_id"),
            started_at=started_at,
            completed_at=completed_at,
            error_message=data.get("error_message"),
            metadata=data.get("metadata", {})
        )
