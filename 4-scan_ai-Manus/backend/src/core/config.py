"""
إعدادات التطبيق - إدارة متغيرات البيئة والتكوين
Application Configuration - Environment variables and settings management
"""

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class _SimpleDotEnvSettingsSource(PydanticBaseSettingsSource):
    """A minimal .env reader that returns raw strings.

    pydantic-settings 2.1.x tries to JSON-decode complex types (e.g. List[str])
    coming from dotenv/env sources. This project historically used
    comma-separated strings for list fields, and we already have field
    validators that parse those strings. Returning raw strings lets validators
    run before coercion.
    """

    def __init__(self, settings_cls: type[BaseSettings]):
        super().__init__(settings_cls)
        self._data = self._read_dotenv()

    def _read_dotenv(self) -> Dict[str, Any]:
        model_config = getattr(self.settings_cls, "model_config", {}) or {}
        env_file = model_config.get("env_file")
        if not env_file:
            return {}

        env_path = Path(str(env_file))
        if not env_path.is_absolute():
            env_path = Path.cwd() / env_path
        if not env_path.exists() or not env_path.is_file():
            return {}

        data: Dict[str, Any] = {}
        encoding = model_config.get("env_file_encoding", "utf-8")
        for raw_line in env_path.read_text(encoding=encoding).splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].lstrip()
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key:
                continue

            # Strip surrounding quotes if present
            if len(value) >= 2 and (
                (value[0] == value[-1] == '"')
                or (value[0] == value[-1] == "'")
            ):
                value = value[1:-1]

            data[key] = value

        return data

    def get_field_value(self, field: Any, field_name: str) -> tuple[Any, str, bool]:
        if field_name in self._data:
            return self._data[field_name], field_name, False
        return None, field_name, False

    def __call__(self) -> Dict[str, Any]:
        return dict(self._data)


class Settings(BaseSettings):
    """
    إعدادات التطبيق الرئيسية
    Main application settings
    """

    # إعدادات قاعدة البيانات
    # If provided, use this instead of building from POSTGRES_*
    DATABASE_URL: str = "sqlite:///./data/gaara_scan_ai.db"
    POSTGRES_DB: str = "gaara_scan_ai"
    POSTGRES_USER: str = "gaara_user"
    # SECURITY: Password must be set via environment variable in production
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # إعدادات Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    # إعدادات التطبيق
    # SECURITY: SECRET_KEY must be set via environment variable in production
    SECRET_KEY: str = ""
    DEBUG: bool = False
    APP_PORT: int = 4001
    WORKERS: int = 4

    # إعدادات الأمان
    # SECURITY: JWT_SECRET must be set via environment variable in production
    JWT_SECRET: str = ""
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
    # Max request body sizes (helps mitigate large payload attacks / native library crashes)
    # Keep multipart slightly above MAX_FILE_SIZE to allow form-data overhead.
    MAX_JSON_BODY_SIZE: str = "2MB"
    MAX_MULTIPART_BODY_SIZE: str = "60MB"
    # Image safety: limit total pixels to reduce decompression bombs / excessive memory usage.
    MAX_IMAGE_PIXELS: int = 20_000_000  # ~20MP
    ALLOWED_EXTENSIONS: List[str] = [
        "jpg", "jpeg", "png", "gif", "bmp", "tiff"
    ]

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

    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json

            # Try JSON parse first (e.g., '["http://localhost"]')
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [origin.strip() for origin in v.split(',')]
        return v

    @field_validator('ALLOWED_METHODS', mode='before')
    @classmethod
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            import json

            # Try JSON parse first (e.g., '["GET","POST"]')
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [method.strip() for method in v.split(',')]
        return v

    @field_validator('ALLOWED_HEADERS', mode='before')
    @classmethod
    def parse_cors_headers(cls, v):
        if isinstance(v, str):
            import json

            # Try JSON parse first (e.g., '["*"]')
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [header.strip() for header in v.split(',')]
        return v

    @field_validator('ALLOWED_EXTENSIONS', mode='before')
    @classmethod
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
        # If DATABASE_URL is provided, use it
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # Otherwise, build from POSTGRES_* variables
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def redis_url(self) -> str:
        """
        بناء رابط Redis
        Build Redis URL
        """
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:"
                f"{self.REDIS_PORT}/{self.REDIS_DB}"
            )
        return (
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/"
            f"{self.REDIS_DB}"
        )

    @property
    def max_file_size_bytes(self) -> int:
        """
        تحويل حجم الملف الأقصى إلى بايت
        Convert max file size to bytes
        """
        return self._parse_size_to_bytes(self.MAX_FILE_SIZE)

    @staticmethod
    def _parse_size_to_bytes(size_value: str) -> int:
        size_str = str(size_value).strip().upper()
        if size_str.endswith("MB"):
            return int(size_str[:-2]) * 1024 * 1024
        if size_str.endswith("KB"):
            return int(size_str[:-2]) * 1024
        if size_str.endswith("GB"):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        return int(size_str)

    @property
    def max_json_body_bytes(self) -> int:
        return self._parse_size_to_bytes(self.MAX_JSON_BODY_SIZE)

    @property
    def max_multipart_body_bytes(self) -> int:
        return self._parse_size_to_bytes(self.MAX_MULTIPART_BODY_SIZE)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"  # Ignore extra fields in .env
    }

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            _SimpleDotEnvSettingsSource(settings_cls),
            file_secret_settings,
        )


@lru_cache()
def get_settings() -> Settings:
    """
    الحصول على إعدادات التطبيق (مع التخزين المؤقت)
    Get application settings (with caching)
    """
    return Settings()
