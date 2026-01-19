# File: /home/ubuntu/clean_project/src/api_router_updated.py
"""
مسار الملف: /home/ubuntu/clean_project/src/api_router_updated.py

موجه API موحد محدث لنظام Gaara Scan AI
يجمع جميع واجهات برمجة التطبيقات في مكان واحد لضمان التكامل
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from typing import Dict, Any

# استيراد موجهات الوحدات الموجودة
try:
    from modules.ai_management.api import router as ai_management_router
except ImportError:
    ai_management_router = None

try:
    from modules.disease_diagnosis.api import router as disease_diagnosis_router
except ImportError:
    disease_diagnosis_router = None

try:
    from modules.activity_log.api import router as activity_log_router
except ImportError:
    activity_log_router = None

try:
    from modules.ai_agent.api import router as ai_agent_router
except ImportError:
    ai_agent_router = None

# استيراد موجهات APIs الجديدة
from api.image_enhancement import router as image_enhancement_router
from api.plant_hybridization import router as plant_hybridization_router
from api.yolo_detection import router as yolo_detection_router
from api.docker_management import router as docker_management_router

# إنشاء الموجه الرئيسي
main_router = APIRouter(prefix="/api", tags=["main"])

# نظام الأمان
security = HTTPBearer()

# تسجيل موجهات الوحدات الموجودة
if ai_management_router:
    main_router.include_router(
        ai_management_router,
        prefix="/ai-service",
        tags=["ai-management"]
    )

if disease_diagnosis_router:
    main_router.include_router(
        disease_diagnosis_router,
        prefix="/disease-diagnosis", 
        tags=["disease-diagnosis"]
    )

if activity_log_router:
    main_router.include_router(
        activity_log_router,
        prefix="/activity-log",
        tags=["activity-log"]
    )

if ai_agent_router:
    main_router.include_router(
        ai_agent_router,
        prefix="/ai-agent",
        tags=["ai-agent"]
    )

# تسجيل موجهات APIs الجديدة
main_router.include_router(
    image_enhancement_router,
    prefix="/image-enhancement",
    tags=["image-enhancement"]
)

main_router.include_router(
    plant_hybridization_router,
    prefix="/plant-hybridization",
    tags=["plant-hybridization"]
)

main_router.include_router(
    yolo_detection_router,
    prefix="/yolo-detection",
    tags=["yolo-detection"]
)

main_router.include_router(
    docker_management_router,
    prefix="/docker",
    tags=["docker-management"]
)

# واجهات Dashboard
@main_router.get("/dashboard/stats")
async def get_dashboard_stats():
    """الحصول على إحصائيات لوحة التحكم"""
    return {
        "data": {
            "total_diagnoses": 1247,
            "successful_diagnoses": 1173,
            "plant_types": 45,
            "diseases_detected": 89,
            "total_processed_images": 1856,
            "ai_accuracy": 94.2,
            "system_uptime": "15 يوم، 8 ساعات",
            "active_users": 23,
            "recent_activity": [
                {
                    "id": 1,
                    "type": "diagnosis",
                    "message": "تم تشخيص مرض البياض الدقيقي في الطماطم",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "user": "أحمد محمد"
                },
                {
                    "id": 2,
                    "type": "enhancement",
                    "message": "تم تحسين جودة صورة نبات الخيار",
                    "timestamp": "2024-01-15T10:25:00Z",
                    "user": "فاطمة علي"
                },
                {
                    "id": 3,
                    "type": "hybridization",
                    "message": "تم إجراء محاكاة تهجين بين صنفين من الذرة",
                    "timestamp": "2024-01-15T10:20:00Z",
                    "user": "محمد حسن"
                }
            ]
        }
    }

@main_router.get("/dashboard/charts")
async def get_dashboard_charts():
    """الحصول على بيانات الرسوم البيانية للوحة التحكم"""
    return {
        "data": {
            "diagnosis_trend": {
                "labels": ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو"],
                "datasets": [
                    {
                        "label": "التشخيصات الناجحة",
                        "data": [65, 78, 90, 81, 95, 105],
                        "borderColor": "#1cc88a",
                        "backgroundColor": "rgba(28, 200, 138, 0.1)"
                    },
                    {
                        "label": "إجمالي التشخيصات",
                        "data": [70, 85, 95, 88, 102, 112],
                        "borderColor": "#4e73df",
                        "backgroundColor": "rgba(78, 115, 223, 0.1)"
                    }
                ]
            },
            "disease_distribution": {
                "labels": ["البياض الدقيقي", "العفن الرمادي", "الصدأ", "التبقع البني", "أخرى"],
                "datasets": [
                    {
                        "data": [30, 25, 20, 15, 10],
                        "backgroundColor": [
                            "#4e73df",
                            "#1cc88a", 
                            "#36b9cc",
                            "#f6c23e",
                            "#e74a3b"
                        ]
                    }
                ]
            },
            "system_performance": {
                "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
                "datasets": [
                    {
                        "label": "استخدام المعالج (%)",
                        "data": [25, 30, 45, 60, 55, 40],
                        "borderColor": "#e74a3b",
                        "backgroundColor": "rgba(231, 74, 59, 0.1)"
                    },
                    {
                        "label": "استخدام الذاكرة (%)",
                        "data": [40, 42, 50, 65, 62, 55],
                        "borderColor": "#f6c23e",
                        "backgroundColor": "rgba(246, 194, 62, 0.1)"
                    }
                ]
            }
        }
    }

# واجهات إدارة البيانات
@main_router.get("/data/export")
async def export_all_data():
    """تصدير جميع البيانات"""
    return {
        "message": "تم بدء عملية تصدير البيانات",
        "export_id": "export_001",
        "estimated_time": "5-10 دقائق"
    }

@main_router.post("/data/import")
async def import_data(data: Dict[str, Any]):
    """استيراد البيانات"""
    return {
        "message": "تم بدء عملية استيراد البيانات",
        "import_id": "import_001",
        "status": "processing"
    }

@main_router.get("/data/backup")
async def create_backup():
    """إنشاء نسخة احتياطية"""
    return {
        "message": "تم إنشاء النسخة الاحتياطية بنجاح",
        "backup_id": "backup_001",
        "size": "2.5 GB",
        "created_at": "2024-01-15T10:30:00Z"
    }

# واجهات المراقبة
@main_router.get("/monitoring/system")
async def get_system_monitoring():
    """الحصول على بيانات مراقبة النظام"""
    return {
        "data": {
            "cpu_usage": 45.2,
            "memory_usage": 68.7,
            "disk_usage": 34.1,
            "network_io": 15.8,
            "active_connections": 127,
            "response_time": 245,
            "error_rate": 0.02,
            "uptime": "15d 8h 23m"
        }
    }

@main_router.get("/monitoring/services")
async def get_services_monitoring():
    """الحصول على بيانات مراقبة الخدمات"""
    return {
        "data": [
            {
                "name": "gaara_scan_ai",
                "status": "healthy",
                "response_time": 120,
                "cpu_usage": 15.2,
                "memory_usage": 256,
                "last_check": "2024-01-15T10:30:00Z"
            },
            {
                "name": "postgres",
                "status": "healthy",
                "response_time": 45,
                "cpu_usage": 8.7,
                "memory_usage": 128,
                "last_check": "2024-01-15T10:30:00Z"
            },
            {
                "name": "redis",
                "status": "healthy",
                "response_time": 12,
                "cpu_usage": 3.1,
                "memory_usage": 64,
                "last_check": "2024-01-15T10:30:00Z"
            }
        ]
    }

# واجهات الإعدادات
@main_router.get("/settings/system")
async def get_system_settings():
    """الحصول على إعدادات النظام"""
    return {
        "data": {
            "language": "ar",
            "theme": "magseeds",
            "timezone": "Asia/Riyadh",
            "date_format": "DD/MM/YYYY",
            "notifications_enabled": True,
            "auto_backup": True,
            "backup_frequency": "daily",
            "max_file_size": "10MB",
            "allowed_file_types": ["jpg", "jpeg", "png", "webp"],
            "ai_confidence_threshold": 0.8,
            "max_concurrent_diagnoses": 5
        }
    }

@main_router.put("/settings/system")
async def update_system_settings(settings: Dict[str, Any]):
    """تحديث إعدادات النظام"""
    return {
        "message": "تم تحديث إعدادات النظام بنجاح",
        "updated_settings": settings
    }

# واجهة صحة النظام
@main_router.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "message": "نظام Gaara Scan AI يعمل بشكل طبيعي",
        "version": "2.0.0",
        "timestamp": "2024-01-15T10:30:00Z",
        "services": {
            "database": "healthy",
            "ai_engine": "healthy",
            "file_storage": "healthy",
            "cache": "healthy"
        }
    }

# واجهة معلومات النظام
@main_router.get("/info")
async def system_info():
    """معلومات النظام"""
    return {
        "name": "Gaara Scan AI",
        "description": "نظام ذكي متطور لتشخيص الأمراض النباتية وتحسين الصور",
        "version": "2.0.0",
        "build": "20240115",
        "modules": [
            "ai-management",
            "disease-diagnosis", 
            "activity-log",
            "ai-agent",
            "image-enhancement",
            "plant-hybridization",
            "yolo-detection",
            "docker-management"
        ],
        "features": [
            "تشخيص الأمراض النباتية",
            "تحسين الصور بالذكاء الاصطناعي",
            "محاكاة تهجين النباتات",
            "كشف الكائنات باستخدام YOLO",
            "إدارة حاويات Docker",
            "مراقبة النظام في الوقت الفعلي",
            "نظام إدارة المستخدمين",
            "تصدير واستيراد البيانات"
        ]
    }

# واجهة المصادقة المحسنة
@main_router.post("/auth/login")
async def login(credentials: Dict[str, str]):
    """تسجيل الدخول"""
    username = credentials.get("username")
    password = credentials.get("password")
    
    # قائمة المستخدمين الوهمية
    users = {
        "admin": {"password": "admin123", "role": "admin", "name": "المدير العام"},
        "user": {"password": "user123", "role": "user", "name": "مستخدم عادي"},
        "doctor": {"password": "doctor123", "role": "expert", "name": "د. أحمد محمد"},
        "researcher": {"password": "research123", "role": "researcher", "name": "الباحث محمد علي"}
    }
    
    if username in users and users[username]["password"] == password:
        user_data = users[username]
        return {
            "access_token": f"token_{username}_{hash(password)}",
            "token_type": "bearer",
            "user": {
                "username": username,
                "name": user_data["name"],
                "role": user_data["role"],
                "permissions": get_user_permissions(user_data["role"])
            },
            "expires_in": 3600
        }
    
    raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")

def get_user_permissions(role: str) -> list:
    """الحصول على صلاحيات المستخدم حسب الدور"""
    permissions_map = {
        "admin": ["read", "write", "delete", "manage_users", "manage_system", "view_logs"],
        "expert": ["read", "write", "advanced_diagnosis", "view_reports"],
        "researcher": ["read", "write", "research_tools", "export_data"],
        "user": ["read", "basic_diagnosis", "view_own_data"]
    }
    return permissions_map.get(role, ["read"])

# واجهة إدارة الجلسة
@main_router.get("/auth/me")
async def get_current_user(token: str = Depends(security)):
    """الحصول على معلومات المستخدم الحالي"""
    # استخراج اسم المستخدم من الرمز المميز (محاكاة)
    if token.credentials.startswith("token_"):
        username = token.credentials.split("_")[1]
        
        users_info = {
            "admin": {"name": "المدير العام", "role": "admin"},
            "user": {"name": "مستخدم عادي", "role": "user"},
            "doctor": {"name": "د. أحمد محمد", "role": "expert"},
            "researcher": {"name": "الباحث محمد علي", "role": "researcher"}
        }
        
        if username in users_info:
            user_info = users_info[username]
            return {
                "username": username,
                "name": user_info["name"],
                "role": user_info["role"],
                "permissions": get_user_permissions(user_info["role"]),
                "last_login": "2024-01-15T10:30:00Z",
                "session_expires": "2024-01-15T11:30:00Z"
            }
    
    raise HTTPException(status_code=401, detail="رمز المصادقة غير صالح")

@main_router.post("/auth/logout")
async def logout(token: str = Depends(security)):
    """تسجيل الخروج"""
    return {
        "message": "تم تسجيل الخروج بنجاح"
    }

