# File: /home/ubuntu/clean_project/src/api_router.py
"""
مسار الملف: /home/ubuntu/clean_project/src/api_router.py

موجه API موحد لنظام Gaara Scan AI
يجمع جميع واجهات برمجة التطبيقات في مكان واحد لضمان التكامل
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from typing import Dict, Any

# استيراد موجهات الوحدات
from modules.ai_management.api import router as ai_management_router
from modules.disease_diagnosis.api import router as disease_diagnosis_router
from modules.activity_log.api import router as activity_log_router
from modules.ai_agent.api import router as ai_agent_router

# إنشاء الموجه الرئيسي
main_router = APIRouter(prefix="/api", tags=["main"])

# نظام الأمان
security = HTTPBearer()

# تسجيل جميع الموجهات
main_router.include_router(
    ai_management_router,
    prefix="/ai-service",
    tags=["ai-management"]
)

main_router.include_router(
    disease_diagnosis_router,
    prefix="/disease-diagnosis", 
    tags=["disease-diagnosis"]
)

main_router.include_router(
    activity_log_router,
    prefix="/activity-log",
    tags=["activity-log"]
)

main_router.include_router(
    ai_agent_router,
    prefix="/ai-agent",
    tags=["ai-agent"]
)

# واجهة صحة النظام
@main_router.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "message": "نظام Gaara Scan AI يعمل بشكل طبيعي",
        "version": "1.0.0"
    }

# واجهة معلومات النظام
@main_router.get("/info")
async def system_info():
    """معلومات النظام"""
    return {
        "name": "Gaara Scan AI",
        "description": "نظام ذكي لتشخيص الأمراض النباتية",
        "version": "1.0.0",
        "modules": [
            "ai-management",
            "disease-diagnosis", 
            "activity-log",
            "ai-agent"
        ]
    }

# واجهة المصادقة المبسطة
@main_router.post("/auth/login")
async def login(credentials: Dict[str, str]):
    """تسجيل الدخول المبسط"""
    # TODO: تنفيذ نظام مصادقة حقيقي
    username = credentials.get("username")
    password = credentials.get("password")
    
    if username and password:
        return {
            "access_token": f"token_{username}",
            "token_type": "bearer",
            "user": {
                "username": username,
                "role": "user"
            }
        }
    
    raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")

# واجهة إدارة الجلسة
@main_router.get("/auth/me")
async def get_current_user(token: str = Depends(security)):
    """الحصول على معلومات المستخدم الحالي"""
    # TODO: تنفيذ التحقق من الرمز المميز
    return {
        "username": "user",
        "role": "user",
        "permissions": ["read", "write"]
    }

