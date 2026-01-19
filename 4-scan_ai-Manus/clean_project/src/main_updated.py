# File: /home/ubuntu/clean_project/src/main_updated.py
"""
التطبيق الرئيسي المحدث لنظام Gaara Scan AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

# استيراد الموجه المحدث
from api_router_updated import main_router

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Gaara Scan AI",
    description="نظام ذكي متطور لتشخيص الأمراض النباتية وتحسين الصور",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد CORS للسماح بالوصول من الواجهة الأمامية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج، يجب تحديد النطاقات المسموحة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل موجه APIs
app.include_router(main_router)

# خدمة الملفات الثابتة
if os.path.exists("../frontend"):
    app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# خدمة الصفحة الرئيسية
@app.get("/")
async def serve_frontend():
    """خدمة الصفحة الرئيسية"""
    frontend_path = "../frontend/index.html"
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"message": "مرحباً بك في نظام Gaara Scan AI", "version": "2.0.0"}

# معالج الأخطاء العام
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """معالج الصفحات غير الموجودة"""
    return {"error": "الصفحة غير موجودة", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """معالج الأخطاء الداخلية"""
    return {"error": "خطأ داخلي في الخادم", "status_code": 500}

# نقطة دخول التطبيق
if __name__ == "__main__":
    print("🚀 بدء تشغيل نظام Gaara Scan AI...")
    print("📡 الخادم متاح على: http://localhost:5000")
    print("📚 وثائق API متاحة على: http://localhost:5000/docs")
    
    uvicorn.run(
        "main_updated:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )

