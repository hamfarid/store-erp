# تحديث ملف التوجيه الرئيسي لإضافة الخدمات الجديدة
# API Router Update for New Services

# إضافة التوجيهات للخدمات الجديدة في api_router.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import logging

# إعداد التسجيل
logger = logging.getLogger(__name__)

# إنشاء موجه API الرئيسي
api_router = APIRouter(prefix="/api")

# URLs للخدمات الجديدة
YOLO_SERVICE_URL = "http://gaara-yolo-detection:8018"
IMAGE_ENHANCEMENT_URL = "http://gaara-image-enhancement:8019"
GPU_PROCESSING_URL = "http://gaara-gpu-processing:8020"
PLANT_DISEASE_ADVANCED_URL = "http://gaara-plant-disease-advanced:8021"
PLANT_HYBRIDIZATION_URL = "http://gaara-plant-hybridization:8022"

# ==========================================
# YOLO Detection Service Routes
# ==========================================

@api_router.get("/yolo-detection/health")
async def yolo_health():
    """فحص صحة خدمة YOLO"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{YOLO_SERVICE_URL}/health")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الاتصال بخدمة YOLO: {e}")
        raise HTTPException(status_code=503, detail="خدمة YOLO غير متاحة")

@api_router.get("/yolo-detection/models")
async def yolo_models():
    """الحصول على نماذج YOLO المتاحة"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{YOLO_SERVICE_URL}/models")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الحصول على نماذج YOLO: {e}")
        raise HTTPException(status_code=503, detail="فشل في الحصول على النماذج")

@api_router.post("/yolo-detection/detect")
async def yolo_detect(request):
    """كشف الكائنات باستخدام YOLO"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{YOLO_SERVICE_URL}/detect", data=request)
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في كشف الكائنات: {e}")
        raise HTTPException(status_code=500, detail="فشل في كشف الكائنات")

# ==========================================
# Image Enhancement Service Routes
# ==========================================

@api_router.get("/image-enhancement/health")
async def enhancement_health():
    """فحص صحة خدمة تحسين الصور"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{IMAGE_ENHANCEMENT_URL}/health")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الاتصال بخدمة تحسين الصور: {e}")
        raise HTTPException(status_code=503, detail="خدمة تحسين الصور غير متاحة")

@api_router.get("/image-enhancement/methods")
async def enhancement_methods():
    """الحصول على طرق التحسين المتاحة"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{IMAGE_ENHANCEMENT_URL}/methods")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الحصول على طرق التحسين: {e}")
        raise HTTPException(status_code=503, detail="فشل في الحصول على طرق التحسين")

@api_router.post("/image-enhancement/enhance")
async def enhance_image(request):
    """تحسين صورة"""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{IMAGE_ENHANCEMENT_URL}/enhance", data=request)
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في تحسين الصورة: {e}")
        raise HTTPException(status_code=500, detail="فشل في تحسين الصورة")

# ==========================================
# GPU Processing Service Routes
# ==========================================

@api_router.get("/gpu-processing/health")
async def gpu_health():
    """فحص صحة خدمة معالجة GPU"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GPU_PROCESSING_URL}/health")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الاتصال بخدمة GPU: {e}")
        raise HTTPException(status_code=503, detail="خدمة GPU غير متاحة")

@api_router.get("/gpu-processing/status")
async def gpu_status():
    """الحصول على حالة GPU"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GPU_PROCESSING_URL}/status")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الحصول على حالة GPU: {e}")
        raise HTTPException(status_code=503, detail="فشل في الحصول على حالة GPU")

# ==========================================
# Plant Disease Advanced Service Routes
# ==========================================

@api_router.get("/plant-disease-advanced/health")
async def plant_disease_health():
    """فحص صحة خدمة تشخيص الأمراض المتقدمة"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PLANT_DISEASE_ADVANCED_URL}/health")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الاتصال بخدمة تشخيص الأمراض: {e}")
        raise HTTPException(status_code=503, detail="خدمة تشخيص الأمراض غير متاحة")

@api_router.post("/plant-disease-advanced/diagnose")
async def diagnose_plant_disease(request):
    """تشخيص أمراض النباتات المتقدم"""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{PLANT_DISEASE_ADVANCED_URL}/diagnose", data=request)
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في تشخيص المرض: {e}")
        raise HTTPException(status_code=500, detail="فشل في تشخيص المرض")

# ==========================================
# Plant Hybridization Service Routes
# ==========================================

@api_router.get("/plant-hybridization/health")
async def hybridization_health():
    """فحص صحة خدمة تهجين النباتات"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PLANT_HYBRIDIZATION_URL}/health")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الاتصال بخدمة التهجين: {e}")
        raise HTTPException(status_code=503, detail="خدمة التهجين غير متاحة")

@api_router.get("/plant-hybridization/varieties")
async def get_varieties():
    """الحصول على أصناف النباتات"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PLANT_HYBRIDIZATION_URL}/varieties")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الحصول على الأصناف: {e}")
        raise HTTPException(status_code=503, detail="فشل في الحصول على الأصناف")

@api_router.get("/plant-hybridization/traits")
async def get_traits():
    """الحصول على الصفات المتاحة"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PLANT_HYBRIDIZATION_URL}/traits")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الحصول على الصفات: {e}")
        raise HTTPException(status_code=503, detail="فشل في الحصول على الصفات")

@api_router.post("/plant-hybridization/hybridize")
async def hybridize_plants(request):
    """تهجين النباتات"""
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:  # 5 دقائق للتهجين
            response = await client.post(f"{PLANT_HYBRIDIZATION_URL}/hybridize", json=request)
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في التهجين: {e}")
        raise HTTPException(status_code=500, detail="فشل في التهجين")

@api_router.get("/plant-hybridization/history")
async def get_hybridization_history():
    """الحصول على تاريخ التهجين"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PLANT_HYBRIDIZATION_URL}/history")
            return response.json()
    except Exception as e:
        logger.error(f"خطأ في الحصول على التاريخ: {e}")
        raise HTTPException(status_code=503, detail="فشل في الحصول على التاريخ")

# ==========================================
# Health Check for All New Services
# ==========================================

@api_router.get("/services/health-check")
async def services_health_check():
    """فحص صحة جميع الخدمات الجديدة"""
    services_status = {}
    
    services = {
        "yolo_detection": YOLO_SERVICE_URL,
        "image_enhancement": IMAGE_ENHANCEMENT_URL,
        "gpu_processing": GPU_PROCESSING_URL,
        "plant_disease_advanced": PLANT_DISEASE_ADVANCED_URL,
        "plant_hybridization": PLANT_HYBRIDIZATION_URL
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for service_name, service_url in services.items():
            try:
                response = await client.get(f"{service_url}/health")
                services_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": response.elapsed.total_seconds(),
                    "details": response.json() if response.status_code == 200 else None
                }
            except Exception as e:
                services_status[service_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
    
    return {
        "overall_status": "healthy" if all(s["status"] == "healthy" for s in services_status.values()) else "partial",
        "services": services_status,
        "timestamp": "2024-01-01T00:00:00Z"  # سيتم استبدالها بالوقت الفعلي
    }

