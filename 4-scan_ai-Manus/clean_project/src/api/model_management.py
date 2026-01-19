# File: /home/ubuntu/clean_project/src/api/model_management.py
"""
واجهة برمجة التطبيقات لإدارة النماذج - AI Model Management API
توفر APIs شاملة لإدارة نماذج الذكاء الاصطناعي

الميزات:
- إدارة دورة حياة النماذج (تدريب، نشر، إيقاف)
- مراقبة أداء النماذج
- إدارة إصدارات النماذج
- تحليل استخدام النماذج
- تحسين وضبط النماذج
"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
import asyncio
from pathlib import Path
import shutil
import uuid

# استيراد النماذج والخدمات
try:
    from ..database import get_db
    from ..core.auth import get_current_user
    from ..database_models import User
    from ..modules.ai_management.db_models import AIModel, AgentTask
    from ..modules.ai_management.model_router import ModelRouter
    from ..modules.ai_management.load_balancer import LoadBalancer
    from ..services.memory_service import get_memory_service
except ImportError:
    # Fallback للاختبار
    pass

# إعداد التسجيل
logger = logging.getLogger(__name__)

# إنشاء router
router = APIRouter(prefix="/api/models", tags=["model_management"])

class ModelStatus(str, Enum):
    """حالات النموذج"""
    TRAINING = "training"
    READY = "ready"
    DEPLOYED = "deployed"
    STOPPED = "stopped"
    ERROR = "error"
    UPDATING = "updating"

class ModelType(str, Enum):
    """أنواع النماذج"""
    CLASSIFICATION = "classification"
    DETECTION = "detection"
    SEGMENTATION = "segmentation"
    GENERATION = "generation"
    LANGUAGE = "language"
    CUSTOM = "custom"

class TrainingStatus(str, Enum):
    """حالات التدريب"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ModelRequest:
    """طلب إنشاء أو تحديث نموذج"""
    def __init__(self,
                 name: str,
                 model_type: ModelType,
                 description: str = "",
                 config: Dict[str, Any] = None,
                 training_data_path: str = None,
                 base_model: str = None):
        self.name = name
        self.model_type = model_type
        self.description = description
        self.config = config or {}
        self.training_data_path = training_data_path
        self.base_model = base_model

@router.get("/")
async def list_models(
    status: Optional[ModelStatus] = Query(None),
    model_type: Optional[ModelType] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على قائمة النماذج"""
    try:
        query = db.query(AIModel)
        
        # تطبيق المرشحات
        if status:
            query = query.filter(AIModel.status == status.value)
        
        if model_type:
            query = query.filter(AIModel.model_type == model_type.value)
        
        # الترقيم
        total = query.count()
        models = query.offset(offset).limit(limit).all()
        
        # تحويل إلى قاموس
        model_list = []
        for model in models:
            model_dict = {
                "id": model.id,
                "name": model.name,
                "model_type": model.model_type,
                "status": model.status,
                "version": getattr(model, 'version', '1.0'),
                "accuracy": getattr(model, 'accuracy', 0.0),
                "created_at": model.created_at.isoformat() if model.created_at else None,
                "last_used": getattr(model, 'last_used', None),
                "usage_count": getattr(model, 'usage_count', 0),
                "description": getattr(model, 'description', '')
            }
            model_list.append(model_dict)
        
        return {
            "models": model_list,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على قائمة النماذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحصول على النماذج: {str(e)}")

@router.get("/{model_id}")
async def get_model_details(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على تفاصيل نموذج محدد"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        # تفاصيل شاملة للنموذج
        model_details = {
            "id": model.id,
            "name": model.name,
            "model_type": model.model_type,
            "status": model.status,
            "version": getattr(model, 'version', '1.0'),
            "description": getattr(model, 'description', ''),
            "created_at": model.created_at.isoformat() if model.created_at else None,
            "updated_at": getattr(model, 'updated_at', None),
            "config": getattr(model, 'config', {}),
            "metrics": {
                "accuracy": getattr(model, 'accuracy', 0.0),
                "precision": getattr(model, 'precision', 0.0),
                "recall": getattr(model, 'recall', 0.0),
                "f1_score": getattr(model, 'f1_score', 0.0)
            },
            "usage_statistics": {
                "total_predictions": getattr(model, 'usage_count', 0),
                "average_response_time": getattr(model, 'avg_response_time', 0.0),
                "success_rate": getattr(model, 'success_rate', 0.0),
                "last_used": getattr(model, 'last_used', None)
            },
            "training_info": {
                "training_data_size": getattr(model, 'training_data_size', 0),
                "training_duration": getattr(model, 'training_duration', 0),
                "epochs": getattr(model, 'epochs', 0),
                "loss": getattr(model, 'final_loss', 0.0)
            }
        }
        
        return model_details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل النموذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحصول على تفاصيل النموذج: {str(e)}")

@router.post("/")
async def create_model(
    name: str,
    model_type: ModelType,
    description: str = "",
    config: Optional[str] = None,
    base_model: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إنشاء نموذج جديد"""
    try:
        # التحقق من عدم وجود نموذج بنفس الاسم
        existing_model = db.query(AIModel).filter(AIModel.name == name).first()
        if existing_model:
            raise HTTPException(status_code=400, detail="يوجد نموذج بهذا الاسم مسبقاً")
        
        # تحليل التكوين
        parsed_config = {}
        if config:
            try:
                parsed_config = json.loads(config)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="صيغة التكوين غير صحيحة")
        
        # إنشاء النموذج
        new_model = AIModel(
            name=name,
            model_type=model_type.value,
            status=ModelStatus.READY.value,
            description=description,
            config=parsed_config,
            created_at=datetime.utcnow(),
            version="1.0",
            accuracy=0.0,
            usage_count=0
        )
        
        # إضافة معلومات إضافية إذا كانت متوفرة
        if base_model:
            new_model.base_model = base_model
        
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        
        logger.info(f"تم إنشاء نموذج جديد: {name}")
        
        return {
            "message": "تم إنشاء النموذج بنجاح",
            "model_id": new_model.id,
            "name": new_model.name,
            "status": new_model.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إنشاء النموذج: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"خطأ في إنشاء النموذج: {str(e)}")

@router.post("/{model_id}/train")
async def train_model(
    model_id: int,
    background_tasks: BackgroundTasks,
    training_data: UploadFile = File(None),
    epochs: int = Query(10, ge=1, le=1000),
    learning_rate: float = Query(0.001, gt=0, le=1),
    batch_size: int = Query(32, ge=1, le=512),
    validation_split: float = Query(0.2, ge=0.1, le=0.5),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تدريب نموذج"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        if model.status == ModelStatus.TRAINING.value:
            raise HTTPException(status_code=400, detail="النموذج قيد التدريب حالياً")
        
        # حفظ بيانات التدريب إذا تم رفعها
        training_data_path = None
        if training_data:
            # إنشاء مجلد للبيانات
            data_dir = Path("/tmp/training_data")
            data_dir.mkdir(exist_ok=True)
            
            # حفظ الملف
            file_path = data_dir / f"{model_id}_{training_data.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(training_data.file, buffer)
            
            training_data_path = str(file_path)
        
        # تحديث حالة النموذج
        model.status = ModelStatus.TRAINING.value
        db.commit()
        
        # إنشاء مهمة تدريب في الخلفية
        training_config = {
            "model_id": model_id,
            "epochs": epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size,
            "validation_split": validation_split,
            "training_data_path": training_data_path,
            "user_id": current_user.id
        }
        
        background_tasks.add_task(run_model_training, training_config, db)
        
        logger.info(f"بدء تدريب النموذج: {model.name}")
        
        return {
            "message": "تم بدء تدريب النموذج",
            "model_id": model_id,
            "training_config": training_config,
            "estimated_duration": f"{epochs * 2} دقيقة"  # تقدير تقريبي
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في بدء تدريب النموذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في تدريب النموذج: {str(e)}")

async def run_model_training(training_config: Dict[str, Any], db: Session):
    """تشغيل تدريب النموذج في الخلفية"""
    model_id = training_config["model_id"]
    
    try:
        logger.info(f"بدء تدريب النموذج {model_id}")
        
        # محاكاة عملية التدريب
        # في التطبيق الحقيقي، هنا سيتم استدعاء مكتبات التعلم الآلي
        
        epochs = training_config["epochs"]
        
        for epoch in range(epochs):
            # محاكاة تقدم التدريب
            await asyncio.sleep(10)  # محاكاة وقت التدريب
            
            # تحديث تقدم التدريب
            progress = (epoch + 1) / epochs * 100
            logger.info(f"تقدم تدريب النموذج {model_id}: {progress:.1f}%")
            
            # يمكن حفظ التقدم في قاعدة البيانات أو Redis
        
        # تحديث النموذج بعد انتهاء التدريب
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        if model:
            model.status = ModelStatus.READY.value
            model.accuracy = 0.85 + (0.1 * (epochs / 100))  # محاكاة تحسن الدقة
            model.version = f"{float(model.version) + 0.1:.1f}"
            model.updated_at = datetime.utcnow()
            
            # إضافة معلومات التدريب
            model.epochs = epochs
            model.training_duration = epochs * 10  # بالثواني
            model.final_loss = 0.1 - (epochs * 0.001)  # محاكاة انخفاض الخسارة
            
            db.commit()
        
        logger.info(f"انتهى تدريب النموذج {model_id} بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تدريب النموذج {model_id}: {e}")
        
        # تحديث حالة النموذج إلى خطأ
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        if model:
            model.status = ModelStatus.ERROR.value
            db.commit()

@router.post("/{model_id}/deploy")
async def deploy_model(
    model_id: int,
    deployment_config: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """نشر نموذج للإنتاج"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        if model.status != ModelStatus.READY.value:
            raise HTTPException(status_code=400, detail="النموذج غير جاهز للنشر")
        
        # تحليل تكوين النشر
        parsed_config = {}
        if deployment_config:
            try:
                parsed_config = json.loads(deployment_config)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="صيغة تكوين النشر غير صحيحة")
        
        # تحديث حالة النموذج
        model.status = ModelStatus.DEPLOYED.value
        model.deployment_config = parsed_config
        model.deployed_at = datetime.utcnow()
        db.commit()
        
        # إضافة النموذج إلى موجه النماذج
        try:
            model_router = ModelRouter()
            await model_router.register_model(
                model_id=model.id,
                model_name=model.name,
                model_type=model.model_type,
                config=parsed_config
            )
        except Exception as e:
            logger.warning(f"لا يمكن تسجيل النموذج في الموجه: {e}")
        
        logger.info(f"تم نشر النموذج: {model.name}")
        
        return {
            "message": "تم نشر النموذج بنجاح",
            "model_id": model_id,
            "deployment_url": f"/api/models/{model_id}/predict",
            "status": model.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في نشر النموذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في نشر النموذج: {str(e)}")

@router.post("/{model_id}/stop")
async def stop_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إيقاف نموذج"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        # تحديث حالة النموذج
        model.status = ModelStatus.STOPPED.value
        model.stopped_at = datetime.utcnow()
        db.commit()
        
        # إزالة النموذج من الموجه
        try:
            model_router = ModelRouter()
            await model_router.unregister_model(model.id)
        except Exception as e:
            logger.warning(f"لا يمكن إزالة النموذج من الموجه: {e}")
        
        logger.info(f"تم إيقاف النموذج: {model.name}")
        
        return {
            "message": "تم إيقاف النموذج بنجاح",
            "model_id": model_id,
            "status": model.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إيقاف النموذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في إيقاف النموذج: {str(e)}")

@router.post("/{model_id}/predict")
async def predict_with_model(
    model_id: int,
    input_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """التنبؤ باستخدام نموذج"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        if model.status != ModelStatus.DEPLOYED.value:
            raise HTTPException(status_code=400, detail="النموذج غير منشور")
        
        # محاكاة التنبؤ
        # في التطبيق الحقيقي، هنا سيتم استدعاء النموذج الفعلي
        prediction_result = {
            "model_id": model_id,
            "model_name": model.name,
            "prediction": "نتيجة التنبؤ المحاكاة",
            "confidence": 0.85,
            "processing_time": 0.15,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # تحديث إحصائيات الاستخدام
        model.usage_count = (model.usage_count or 0) + 1
        model.last_used = datetime.utcnow()
        db.commit()
        
        logger.info(f"تم التنبؤ باستخدام النموذج: {model.name}")
        
        return prediction_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في التنبؤ: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في التنبؤ: {str(e)}")

@router.get("/{model_id}/performance")
async def get_model_performance(
    model_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على إحصائيات أداء النموذج"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        # حساب إحصائيات الأداء
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # في التطبيق الحقيقي، هذه البيانات ستأتي من سجلات الاستخدام
        performance_data = {
            "model_info": {
                "id": model.id,
                "name": model.name,
                "version": getattr(model, 'version', '1.0'),
                "status": model.status
            },
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": days
            },
            "usage_statistics": {
                "total_predictions": getattr(model, 'usage_count', 0),
                "daily_average": getattr(model, 'usage_count', 0) / days,
                "peak_usage": getattr(model, 'usage_count', 0) // 10,  # محاكاة
                "success_rate": getattr(model, 'success_rate', 95.0)
            },
            "performance_metrics": {
                "average_response_time": getattr(model, 'avg_response_time', 0.15),
                "accuracy": getattr(model, 'accuracy', 0.85),
                "precision": getattr(model, 'precision', 0.83),
                "recall": getattr(model, 'recall', 0.87),
                "f1_score": getattr(model, 'f1_score', 0.85)
            },
            "resource_usage": {
                "cpu_usage": "متوسط",
                "memory_usage": "منخفض",
                "gpu_usage": "عالي" if model.model_type in ["detection", "generation"] else "منخفض"
            }
        }
        
        return performance_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على أداء النموذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحصول على الأداء: {str(e)}")

@router.delete("/{model_id}")
async def delete_model(
    model_id: int,
    force: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف نموذج"""
    try:
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="النموذج غير موجود")
        
        # التحقق من إمكانية الحذف
        if model.status == ModelStatus.DEPLOYED.value and not force:
            raise HTTPException(
                status_code=400, 
                detail="لا يمكن حذف نموذج منشور. استخدم force=true للحذف القسري"
            )
        
        # إيقاف النموذج أولاً إذا كان منشوراً
        if model.status == ModelStatus.DEPLOYED.value:
            try:
                model_router = ModelRouter()
                await model_router.unregister_model(model.id)
            except Exception as e:
                logger.warning(f"لا يمكن إزالة النموذج من الموجه: {e}")
        
        # حذف ملفات النموذج
        try:
            model_path = Path(f"/tmp/models/{model_id}")
            if model_path.exists():
                shutil.rmtree(model_path)
        except Exception as e:
            logger.warning(f"لا يمكن حذف ملفات النموذج: {e}")
        
        # حذف من قاعدة البيانات
        db.delete(model)
        db.commit()
        
        logger.info(f"تم حذف النموذج: {model.name}")
        
        return {
            "message": "تم حذف النموذج بنجاح",
            "model_id": model_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف النموذج: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"خطأ في حذف النموذج: {str(e)}")

@router.get("/statistics/overview")
async def get_models_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على نظرة عامة على النماذج"""
    try:
        # إحصائيات عامة
        total_models = db.query(AIModel).count()
        deployed_models = db.query(AIModel).filter(
            AIModel.status == ModelStatus.DEPLOYED.value
        ).count()
        training_models = db.query(AIModel).filter(
            AIModel.status == ModelStatus.TRAINING.value
        ).count()
        
        # إحصائيات حسب النوع
        model_types = {}
        for model_type in ModelType:
            count = db.query(AIModel).filter(
                AIModel.model_type == model_type.value
            ).count()
            model_types[model_type.value] = count
        
        # إحصائيات الاستخدام
        total_predictions = db.query(AIModel).with_entities(
            db.func.sum(AIModel.usage_count)
        ).scalar() or 0
        
        overview = {
            "summary": {
                "total_models": total_models,
                "deployed_models": deployed_models,
                "training_models": training_models,
                "stopped_models": total_models - deployed_models - training_models,
                "total_predictions": total_predictions
            },
            "model_types_distribution": model_types,
            "system_status": {
                "model_router_active": True,  # يمكن فحصه فعلياً
                "load_balancer_active": True,
                "training_queue_size": training_models
            },
            "recent_activity": {
                "models_created_today": 0,  # يمكن حسابه من قاعدة البيانات
                "models_deployed_today": 0,
                "predictions_today": 0
            }
        }
        
        return overview
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على نظرة عامة النماذج: {e}")
        raise HTTPException(status_code=500, detail=f"خطأ في الحصول على النظرة العامة: {str(e)}")

# إضافة router إلى التطبيق الرئيسي
# app.include_router(router)

