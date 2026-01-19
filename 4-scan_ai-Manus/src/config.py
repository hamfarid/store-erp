# File: /home/ubuntu/clean_project/src/config.py
"""
مسار الملف: /home/ubuntu/clean_project/src/config.py

إعدادات النظام الشاملة
تتضمن إعدادات قاعدة البيانات، الأمان، والتطبيق
"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class DatabaseSettings:
    """إعدادات قاعدة البيانات"""
    url: str = "sqlite:///gaara_scan.db"
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20

@dataclass
class SecuritySettings:
    """إعدادات الأمان"""
    secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    max_login_attempts: int = 5
    session_timeout_hours: int = 24

@dataclass
class FileSettings:
    """إعدادات الملفات"""
    upload_folder: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10 MB
    allowed_extensions: list = None
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'csv']

@dataclass
class AppSettings:
    """إعدادات التطبيق"""
    name: str = "Gaara Scan AI"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]

@dataclass
class AISettings:
    """إعدادات الذكاء الاصطناعي"""
    model_path: str = "models"
    confidence_threshold: float = 0.8
    max_batch_size: int = 32
    enable_gpu: bool = False

@dataclass
class MonitoringSettings:
    """إعدادات المراقبة"""
    enable_monitoring: bool = True
    metrics_interval: int = 60  # seconds
    log_level: str = "INFO"
    log_file: str = "app.log"
    max_log_size: int = 10 * 1024 * 1024  # 10 MB

class Settings:
    """إعدادات النظام الشاملة"""
    
    def __init__(self):
        self.database = DatabaseSettings()
        self.security = SecuritySettings()
        self.files = FileSettings()
        self.app = AppSettings()
        self.ai = AISettings()
        self.monitoring = MonitoringSettings()
        
        # تحميل الإعدادات من متغيرات البيئة
        self.load_from_env()
    
    def load_from_env(self):
        """تحميل الإعدادات من متغيرات البيئة"""
        # إعدادات قاعدة البيانات
        if os.getenv("DATABASE_URL"):
            self.database.url = os.getenv("DATABASE_URL")
        
        if os.getenv("DATABASE_ECHO"):
            self.database.echo = os.getenv("DATABASE_ECHO").lower() == "true"
        
        # إعدادات الأمان
        if os.getenv("SECRET_KEY"):
            self.security.secret_key = os.getenv("SECRET_KEY")
        
        if os.getenv("JWT_EXPIRATION_HOURS"):
            self.security.jwt_expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS"))
        
        # إعدادات التطبيق
        if os.getenv("APP_DEBUG"):
            self.app.debug = os.getenv("APP_DEBUG").lower() == "true"
        
        if os.getenv("APP_HOST"):
            self.app.host = os.getenv("APP_HOST")
        
        if os.getenv("APP_PORT"):
            self.app.port = int(os.getenv("APP_PORT"))
        
        # إعدادات الملفات
        if os.getenv("UPLOAD_FOLDER"):
            self.files.upload_folder = os.getenv("UPLOAD_FOLDER")
        
        if os.getenv("MAX_FILE_SIZE"):
            self.files.max_file_size = int(os.getenv("MAX_FILE_SIZE"))
        
        # إعدادات الذكاء الاصطناعي
        if os.getenv("AI_MODEL_PATH"):
            self.ai.model_path = os.getenv("AI_MODEL_PATH")
        
        if os.getenv("AI_CONFIDENCE_THRESHOLD"):
            self.ai.confidence_threshold = float(os.getenv("AI_CONFIDENCE_THRESHOLD"))
        
        if os.getenv("AI_ENABLE_GPU"):
            self.ai.enable_gpu = os.getenv("AI_ENABLE_GPU").lower() == "true"
        
        # إعدادات المراقبة
        if os.getenv("LOG_LEVEL"):
            self.monitoring.log_level = os.getenv("LOG_LEVEL")
        
        if os.getenv("ENABLE_MONITORING"):
            self.monitoring.enable_monitoring = os.getenv("ENABLE_MONITORING").lower() == "true"
    
    def get_database_url(self) -> str:
        """الحصول على رابط قاعدة البيانات"""
        return self.database.url
    
    def is_production(self) -> bool:
        """فحص ما إذا كان النظام في بيئة الإنتاج"""
        return not self.app.debug
    
    def get_cors_origins(self) -> list:
        """الحصول على قائمة المصادر المسموحة لـ CORS"""
        return self.app.cors_origins
    
    def get_upload_path(self) -> str:
        """الحصول على مسار رفع الملفات"""
        upload_path = os.path.abspath(self.files.upload_folder)
        os.makedirs(upload_path, exist_ok=True)
        return upload_path
    
    def get_model_path(self) -> str:
        """الحصول على مسار نماذج الذكاء الاصطناعي"""
        model_path = os.path.abspath(self.ai.model_path)
        os.makedirs(model_path, exist_ok=True)
        return model_path
    
    def validate_settings(self) -> bool:
        """التحقق من صحة الإعدادات"""
        errors = []
        
        # فحص المفتاح السري
        if self.security.secret_key == "your-secret-key-change-in-production":
            errors.append("يجب تغيير المفتاح السري في بيئة الإنتاج")
        
        # فحص طول كلمة المرور
        if self.security.password_min_length < 6:
            errors.append("الحد الأدنى لطول كلمة المرور يجب أن يكون 6 أحرف على الأقل")
        
        # فحص حجم الملف
        if self.files.max_file_size > 100 * 1024 * 1024:  # 100 MB
            errors.append("الحد الأقصى لحجم الملف كبير جداً")
        
        # فحص عتبة الثقة
        if not 0.0 <= self.ai.confidence_threshold <= 1.0:
            errors.append("عتبة الثقة يجب أن تكون بين 0.0 و 1.0")
        
        if errors:
            print("أخطاء في الإعدادات:")
            for error in errors:
                print(f"- {error}")
            return False
        
        return True
    
    def to_dict(self) -> dict:
        """تحويل الإعدادات إلى قاموس"""
        return {
            "database": {
                "url": self.database.url,
                "echo": self.database.echo,
                "pool_size": self.database.pool_size,
                "max_overflow": self.database.max_overflow
            },
            "security": {
                "jwt_algorithm": self.security.jwt_algorithm,
                "jwt_expiration_hours": self.security.jwt_expiration_hours,
                "password_min_length": self.security.password_min_length,
                "max_login_attempts": self.security.max_login_attempts,
                "session_timeout_hours": self.security.session_timeout_hours
            },
            "files": {
                "upload_folder": self.files.upload_folder,
                "max_file_size": self.files.max_file_size,
                "allowed_extensions": self.files.allowed_extensions
            },
            "app": {
                "name": self.app.name,
                "version": self.app.version,
                "debug": self.app.debug,
                "host": self.app.host,
                "port": self.app.port,
                "cors_origins": self.app.cors_origins
            },
            "ai": {
                "model_path": self.ai.model_path,
                "confidence_threshold": self.ai.confidence_threshold,
                "max_batch_size": self.ai.max_batch_size,
                "enable_gpu": self.ai.enable_gpu
            },
            "monitoring": {
                "enable_monitoring": self.monitoring.enable_monitoring,
                "metrics_interval": self.monitoring.metrics_interval,
                "log_level": self.monitoring.log_level,
                "log_file": self.monitoring.log_file,
                "max_log_size": self.monitoring.max_log_size
            }
        }

# مثيل عام للإعدادات
settings = Settings()

# التحقق من صحة الإعدادات عند التحميل
if not settings.validate_settings():
    print("تحذير: توجد مشاكل في الإعدادات")

if __name__ == "__main__":
    # اختبار الإعدادات
    print("إعدادات النظام:")
    print(f"اسم التطبيق: {settings.app.name}")
    print(f"إصدار التطبيق: {settings.app.version}")
    print(f"قاعدة البيانات: {settings.database.url}")
    print(f"مجلد الرفع: {settings.get_upload_path()}")
    print(f"مجلد النماذج: {settings.get_model_path()}")
    print(f"بيئة الإنتاج: {settings.is_production()}")
    
    # عرض جميع الإعدادات
    import json
    print("\nجميع الإعدادات:")
    print(json.dumps(settings.to_dict(), ensure_ascii=False, indent=2))

