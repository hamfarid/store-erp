# File: /home/ubuntu/clean_project/docker/resnet50/src/resnet50_service.py
"""
خدمة ResNet-50 للرؤية الحاسوبية المتقدمة
نظام Gaara Scan AI - حاوية متخصصة لتحليل الصور الزراعية
"""

import os
import io
import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import json
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Gaara Scan AI - ResNet-50 Service",
    description="خدمة ResNet-50 للرؤية الحاسوبية المتقدمة",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مقاييس Prometheus
PREDICTION_COUNTER = Counter('resnet50_predictions_total', 'Total predictions made')
PREDICTION_DURATION = Histogram('resnet50_prediction_duration_seconds', 'Time spent on predictions')
ERROR_COUNTER = Counter('resnet50_errors_total', 'Total errors', ['error_type'])

# نماذج البيانات
class PredictionRequest(BaseModel):
    image_url: Optional[str] = None
    confidence_threshold: float = 0.5
    top_k: int = 5

class PredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]
    confidence_scores: List[float]
    processing_time: float
    model_version: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    gpu_available: bool
    memory_usage: Dict[str, Any]
    uptime: float

# متغيرات عامة
model = None
device = None
transform = None
redis_client = None
class_labels = None
start_time = datetime.now()

# تحميل تصنيفات ImageNet
IMAGENET_CLASSES = {
    0: "tench", 1: "goldfish", 2: "great_white_shark", 3: "tiger_shark",
    # ... (يمكن إضافة جميع الـ 1000 فئة)
    # للاختصار، سنضع بعض الفئات المهمة للزراعة
    946: "bell_pepper", 947: "cardoon", 948: "artichoke", 949: "head_cabbage",
    950: "broccoli", 951: "cauliflower", 952: "zucchini", 953: "spaghetti_squash",
    954: "acorn_squash", 955: "butternut_squash", 956: "cucumber", 957: "artichoke",
    958: "bell_pepper", 959: "cardoon", 960: "mushroom", 961: "Granny_Smith",
    962: "strawberry", 963: "orange", 964: "lemon", 965: "fig", 966: "pineapple",
    967: "banana", 968: "jackfruit", 969: "custard_apple", 970: "pomegranate"
}

async def initialize_model():
    """تهيئة نموذج ResNet-50"""
    global model, device, transform, redis_client, class_labels
    
    try:
        # تحديد الجهاز (GPU أو CPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")
        
        # تحميل النموذج
        model = models.resnet50(pretrained=True)
        model_path = os.getenv('MODEL_PATH', '/opt/venv/resnet50_pretrained.pth')
        
        if os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path, map_location=device))
            logger.info("Loaded custom ResNet-50 model")
        else:
            logger.info("Using default pretrained ResNet-50 model")
        
        model.to(device)
        model.eval()
        
        # إعداد التحويلات
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # الاتصال بـ Redis
        try:
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True
            )
            redis_client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            redis_client = None
        
        # تحميل تصنيفات الفئات
        class_labels = IMAGENET_CLASSES
        
        logger.info("ResNet-50 model initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise

async def preprocess_image(image_data: bytes) -> torch.Tensor:
    """معالجة الصورة قبل التنبؤ"""
    try:
        # تحويل البيانات إلى صورة PIL
        image = Image.open(io.BytesIO(image_data))
        
        # تحويل إلى RGB إذا لزم الأمر
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # تطبيق التحويلات
        image_tensor = transform(image)
        image_tensor = image_tensor.unsqueeze(0)  # إضافة بُعد الدفعة
        
        return image_tensor.to(device)
        
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        raise HTTPException(status_code=400, detail="فشل في معالجة الصورة")

async def make_prediction(image_tensor: torch.Tensor, top_k: int = 5) -> Dict[str, Any]:
    """إجراء التنبؤ باستخدام النموذج"""
    try:
        start_time = datetime.now()
        
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
        # الحصول على أفضل التنبؤات
        top_prob, top_indices = torch.topk(probabilities, top_k)
        
        predictions = []
        confidence_scores = []
        
        for i in range(top_k):
            class_idx = top_indices[i].item()
            confidence = top_prob[i].item()
            class_name = class_labels.get(class_idx, f"class_{class_idx}")
            
            predictions.append({
                "class_id": class_idx,
                "class_name": class_name,
                "confidence": confidence,
                "percentage": confidence * 100
            })
            confidence_scores.append(confidence)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "predictions": predictions,
            "confidence_scores": confidence_scores,
            "processing_time": processing_time,
            "model_version": "ResNet-50-v2.0",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="فشل في التنبؤ")

async def cache_result(key: str, result: Dict[str, Any], ttl: int = 3600):
    """حفظ النتيجة في التخزين المؤقت"""
    if redis_client:
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: redis_client.setex(key, ttl, json.dumps(result, default=str))
            )
        except Exception as e:
            logger.warning(f"Cache save failed: {e}")

async def get_cached_result(key: str) -> Optional[Dict[str, Any]]:
    """استرجاع النتيجة من التخزين المؤقت"""
    if redis_client:
        try:
            cached = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: redis_client.get(key)
            )
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache retrieval failed: {e}")
    return None

# نقاط النهاية (Endpoints)

@app.on_event("startup")
async def startup_event():
    """تهيئة التطبيق عند البدء"""
    await initialize_model()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """فحص صحة الخدمة"""
    try:
        memory_info = {}
        if torch.cuda.is_available():
            memory_info = {
                "gpu_memory_allocated": torch.cuda.memory_allocated(),
                "gpu_memory_cached": torch.cuda.memory_reserved(),
                "gpu_memory_total": torch.cuda.get_device_properties(0).total_memory
            }
        
        uptime = (datetime.now() - start_time).total_seconds()
        
        return HealthResponse(
            status="healthy",
            model_loaded=model is not None,
            gpu_available=torch.cuda.is_available(),
            memory_usage=memory_info,
            uptime=uptime
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="فشل في فحص الصحة")

@app.post("/predict", response_model=PredictionResponse)
async def predict_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    confidence_threshold: float = 0.5,
    top_k: int = 5
):
    """تحليل صورة باستخدام ResNet-50"""
    
    if not model:
        raise HTTPException(status_code=503, detail="النموذج غير محمل")
    
    # التحقق من نوع الملف
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف صورة")
    
    try:
        # قراءة بيانات الصورة
        image_data = await file.read()
        
        # إنشاء مفتاح للتخزين المؤقت
        import hashlib
        cache_key = f"resnet50:{hashlib.md5(image_data).hexdigest()}:{top_k}"
        
        # البحث في التخزين المؤقت
        cached_result = await get_cached_result(cache_key)
        if cached_result:
            PREDICTION_COUNTER.inc()
            return PredictionResponse(**cached_result)
        
        # معالجة الصورة
        with PREDICTION_DURATION.time():
            image_tensor = await preprocess_image(image_data)
            result = await make_prediction(image_tensor, top_k)
        
        # تصفية النتائج حسب عتبة الثقة
        filtered_predictions = [
            pred for pred in result["predictions"] 
            if pred["confidence"] >= confidence_threshold
        ]
        
        result["predictions"] = filtered_predictions
        
        # حفظ في التخزين المؤقت
        background_tasks.add_task(cache_result, cache_key, result)
        
        # تحديث المقاييس
        PREDICTION_COUNTER.inc()
        
        return PredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        ERROR_COUNTER.labels(error_type="prediction_error").inc()
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="خطأ في التنبؤ")

@app.post("/batch_predict")
async def batch_predict(
    files: List[UploadFile] = File(...),
    confidence_threshold: float = 0.5,
    top_k: int = 5
):
    """تحليل متعدد للصور"""
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="الحد الأقصى 10 صور في المرة الواحدة")
    
    results = []
    
    for i, file in enumerate(files):
        try:
            image_data = await file.read()
            image_tensor = await preprocess_image(image_data)
            result = await make_prediction(image_tensor, top_k)
            
            # تصفية النتائج
            filtered_predictions = [
                pred for pred in result["predictions"] 
                if pred["confidence"] >= confidence_threshold
            ]
            
            result["predictions"] = filtered_predictions
            result["file_index"] = i
            result["filename"] = file.filename
            
            results.append(result)
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            results.append({
                "file_index": i,
                "filename": file.filename,
                "error": str(e),
                "predictions": [],
                "confidence_scores": [],
                "processing_time": 0,
                "model_version": "ResNet-50-v2.0",
                "timestamp": datetime.now().isoformat()
            })
    
    PREDICTION_COUNTER.inc(len(files))
    return {"results": results, "total_processed": len(files)}

@app.get("/model_info")
async def get_model_info():
    """معلومات النموذج"""
    return {
        "model_name": "ResNet-50",
        "model_version": "2.0",
        "framework": "PyTorch",
        "input_size": [224, 224, 3],
        "num_classes": len(class_labels),
        "device": str(device),
        "gpu_available": torch.cuda.is_available(),
        "supported_formats": ["JPEG", "PNG", "BMP", "TIFF"]
    }

@app.get("/metrics")
async def get_metrics():
    """مقاييس Prometheus"""
    return Response(generate_latest(), media_type="text/plain")

@app.get("/classes")
async def get_classes():
    """قائمة الفئات المدعومة"""
    return {
        "total_classes": len(class_labels),
        "classes": class_labels
    }

@app.delete("/cache/clear")
async def clear_cache():
    """مسح التخزين المؤقت"""
    if redis_client:
        try:
            keys = redis_client.keys("resnet50:*")
            if keys:
                redis_client.delete(*keys)
            return {"message": f"تم مسح {len(keys)} عنصر من التخزين المؤقت"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"فشل في مسح التخزين المؤقت: {e}")
    else:
        raise HTTPException(status_code=503, detail="التخزين المؤقت غير متاح")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

