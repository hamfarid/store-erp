"""
تطبيق Gaara Scan AI الرئيسي المحسن
Enhanced Main Application for Gaara Scan AI System

تم تقسيم الملف إلى وحدات منفصلة لسهولة الصيانة
Split into separate modules for easier maintenance
"""

import os
import sys
from pathlib import Path

# إضافة المسار الجذر للمشروع
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# استيراد الوحدات الأساسية
from src.core.app_factory import create_app
from src.core.config import get_settings
from src.core.logging_config import setup_logging

def main():
    """
    نقطة الدخول الرئيسية للتطبيق
    Main entry point for the application
    """
    # إعداد السجلات
    setup_logging()
    
    # تحميل الإعدادات
    settings = get_settings()
    
    # إنشاء التطبيق
    app = create_app(settings)
    
    return app

# إنشاء مثيل التطبيق
app = main()

if __name__ == "__main__":
    import uvicorn
    from src.core.config import get_settings
    
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )

