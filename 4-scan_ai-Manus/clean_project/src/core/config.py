"""
إعدادات التطبيق - إدارة متغيرات البيئة والتكوين
Application Configuration - Environment variables and settings management
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache

class Settings(BaseSettings):
    """
    إعدادات التطبيق الرئيسية
    Main application settings
    """
    
    # إعدادات قاعدة البيانات
    POSTGRES_DB: str = "gaara_scan_ai"
    POSTGRES_USER: str = "gaara_user"
    POSTGRES_PASSWORD: str = "gaara_secure_2024"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # إعدادات Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # إعدادات التطبيق
    SECRET_KEY: str = "gaara_secret_key_2024"
    DEBUG: bool = False
    APP_PORT: int = 8000
    WORKERS: int = 4
    
    # إعدادات الأمان
    JWT_SECRET: str = "gaara_jwt_secret_2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # إعدادات CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000"]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # إعدادات السجلات
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "./logs/gaara_scan_ai.log"
    
    # إعدادات الملفات
    UPLOAD_DIR: str = "./data/uploads"
    RESULTS_DIR: str = "./data/results"
    MAX_FILE_SIZE: str = "50MB"
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]
    
    # إعدادات الأداء
    MAX_CONNECTIONS: int = 1000
    TIMEOUT: int = 30
    KEEP_ALIVE: int = 2
    
    # إعدادات التخزين المؤقت
    CACHE_TTL: int = 3600
    CACHE_MAX_SIZE: int = 1000
    
    # إعدادات المراقبة
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    HEALTH_CHECK_INTERVAL: int = 30
    
    @validator('ALLOWED_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('ALLOWED_METHODS', pre=True)
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(',')]
        return v
    
    @validator('ALLOWED_EXTENSIONS', pre=True)
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(',')]
        return v
    
    @property
    def database_url(self) -> str:
        """
        بناء رابط قاعدة البيانات
        Build database URL
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def redis_url(self) -> str:
        """
        بناء رابط Redis
        Build Redis URL
        """
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    @property
    def max_file_size_bytes(self) -> int:
        """
        تحويل حجم الملف الأقصى إلى بايت
        Convert max file size to bytes
        """
        size_str = self.MAX_FILE_SIZE.upper()
        if size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    الحصول على إعدادات التطبيق (مع التخزين المؤقت)
    Get application settings (with caching)
    """
    return Settings()

