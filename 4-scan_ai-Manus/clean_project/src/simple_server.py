# File: /home/ubuntu/clean_project/src/simple_server.py
"""
خادم بسيط لاختبار APIs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# إنشاء تطبيق FastAPI بسيط
app = FastAPI(
    title="Gaara Scan AI - Test Server",
    description="خادم اختبار بسيط لنظام Gaara Scan AI",
    version="2.0.0"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# استيراد APIs الجديدة مباشرة
from api.image_enhancement import router as image_enhancement_router
from api.plant_hybridization import router as plant_hybridization_router
from api.yolo_detection import router as yolo_detection_router
from api.docker_management import router as docker_management_router

# تسجيل الموجهات
app.include_router(image_enhancement_router, prefix="/api/image-enhancement", tags=["image-enhancement"])
app.include_router(plant_hybridization_router, prefix="/api/plant-hybridization", tags=["plant-hybridization"])
app.include_router(yolo_detection_router, prefix="/api/yolo-detection", tags=["yolo-detection"])
app.include_router(docker_management_router, prefix="/api/docker", tags=["docker-management"])

# APIs أساسية
@app.get("/api/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "message": "نظام Gaara Scan AI يعمل بشكل طبيعي",
        "version": "2.0.0"
    }

@app.get("/api/info")
async def system_info():
    """معلومات النظام"""
    return {
        "name": "Gaara Scan AI",
        "description": "نظام ذكي متطور لتشخيص الأمراض النباتية",
        "version": "2.0.0",
        "modules": [
            "image-enhancement",
            "plant-hybridization",
            "yolo-detection",
            "docker-management"
        ]
    }

@app.post("/api/auth/login")
async def login(credentials: dict):
    """تسجيل الدخول المبسط"""
    username = credentials.get("username")
    password = credentials.get("password")
    
    if username and password:
        return {
            "access_token": f"token_{username}",
            "token_type": "bearer",
            "user": {
                "username": username,
                "role": "admin" if username == "admin" else "user"
            }
        }
    
    return {"error": "بيانات الدخول غير صحيحة"}, 401

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """إحصائيات لوحة التحكم"""
    return {
        "data": {
            "total_diagnoses": 1247,
            "successful_diagnoses": 1173,
            "plant_types": 45,
            "diseases_detected": 89,
            "total_processed_images": 1856,
            "ai_accuracy": 94.2,
            "system_uptime": "15 يوم، 8 ساعات",
            "active_users": 23
        }
    }

@app.get("/api/dashboard/charts")
async def get_dashboard_charts():
    """بيانات الرسوم البيانية"""
    return {
        "data": {
            "diagnosis_trend": {
                "labels": ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو"],
                "datasets": [
                    {
                        "label": "التشخيصات الناجحة",
                        "data": [65, 78, 90, 81, 95, 105],
                        "borderColor": "#1cc88a"
                    }
                ]
            }
        }
    }

@app.get("/api/settings/system")
async def get_system_settings():
    """إعدادات النظام"""
    return {
        "data": {
            "language": "ar",
            "theme": "magseeds",
            "timezone": "Asia/Riyadh",
            "notifications_enabled": True,
            "auto_backup": True
        }
    }

@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {"message": "مرحباً بك في نظام Gaara Scan AI", "version": "2.0.0"}

if __name__ == "__main__":
    print("🚀 بدء تشغيل خادم الاختبار...")
    print("📡 الخادم متاح على: http://localhost:5000")
    print("📚 وثائق API متاحة على: http://localhost:5000/docs")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=5000,
        reload=False,
        log_level="info"
    )

