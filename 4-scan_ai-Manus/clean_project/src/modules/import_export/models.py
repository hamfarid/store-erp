"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/models.py
الوصف: نماذج قاعدة البيانات لمديول الاستيراد والتصدير
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class JobType(enum.Enum):
    """
    أنواع مهام الاستيراد والتصدير
    """
    IMPORT = "import"
    EXPORT = "export"


class JobStatus(enum.Enum):
    """
    حالات مهام الاستيراد والتصدير
    """
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FileFormat(enum.Enum):
    """
    صيغ الملفات المدعومة للاستيراد والتصدير
    """
    CSV = "csv"
    XLSX = "xlsx"
    JSON = "json"
    XML = "xml"
    ZIP = "zip"


class ImportExportTemplate(Base):  # pylint: disable=too-few-public-methods
    """
    نموذج قالب الاستيراد والتصدير
    """
    __tablename__ = "import_export_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    module_id = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    format = Column(Enum(FileFormat), nullable=False)
    field_mapping = Column(JSON, nullable=False)
    options = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=not-callable
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # pylint: disable=not-callable
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    creator = relationship("User", back_populates="import_export_templates")
    jobs = relationship("ImportExportJob", back_populates="template")


class ImportExportJob(Base):  # pylint: disable=too-few-public-methods
    """
    نموذج مهمة الاستيراد والتصدير
    """
    __tablename__ = "import_export_jobs"

    id = Column(String(36), primary_key=True, index=True)
    job_type = Column(Enum(JobType), nullable=False, index=True)
    module = Column(String(100), nullable=False, index=True)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.PENDING, index=True)
    progress = Column(Float, nullable=True)
    message = Column(Text, nullable=True)
    result = Column(JSON, nullable=True)
    file_path = Column(String(255), nullable=True)
    template_id = Column(Integer, ForeignKey("import_export_templates.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)  # pylint: disable=not-callable
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # pylint: disable=not-callable
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="import_export_jobs")
    template = relationship("ImportExportTemplate", back_populates="jobs")
    activity_logs = relationship("ActivityLog", back_populates="import_export_job")


class ImportExportSettings(Base):  # pylint: disable=too-few-public-methods
    """
    نموذج إعدادات الاستيراد والتصدير
    """
    __tablename__ = "import_export_settings"

    id = Column(Integer, primary_key=True, index=True)
    max_file_size_mb = Column(Integer, nullable=False, default=10)
    allowed_formats = Column(JSON, nullable=False)
    default_batch_size = Column(Integer, nullable=False, default=1000)
    export_expiry_days = Column(Integer, nullable=False, default=7)
    enable_background_processing = Column(Boolean, nullable=False, default=True)
    notify_on_completion = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=not-callable
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # pylint: disable=not-callable
