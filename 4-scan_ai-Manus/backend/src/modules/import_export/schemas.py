"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/schemas.py
الوصف: مخططات البيانات لمديول الاستيراد والتصدير
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class JobType(str, Enum):
    """
    أنواع مهام الاستيراد والتصدير
    """
    IMPORT = "import"
    EXPORT = "export"


class JobStatus(str, Enum):
    """
    حالات مهام الاستيراد والتصدير
    """
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FileFormat(str, Enum):
    """
    صيغ الملفات المدعومة للاستيراد والتصدير
    """
    CSV = "csv"
    XLSX = "xlsx"
    JSON = "json"
    XML = "xml"
    ZIP = "zip"


class ModuleInfo(BaseModel):
    """
    معلومات المديول المتاح للاستيراد والتصدير
    """
    id: str
    name: str
    description: Optional[str] = None
    supports_import: bool = True
    supports_export: bool = True
    fields: List[Dict[str, Any]]
    required_fields: List[str] = []
    unique_fields: List[str] = []
    relations: List[Dict[str, Any]] = []

    class Config:
        orm_mode = True


class ImportExportTemplateBase(BaseModel):
    """
    النموذج الأساسي لقالب الاستيراد والتصدير
    """
    name: str
    description: Optional[str] = None
    module_id: str
    type: str
    format: FileFormat
    field_mapping: Dict[str, str]
    options: Optional[Dict[str, Any]] = None


class ImportExportTemplateCreate(ImportExportTemplateBase):
    """
    نموذج إنشاء قالب استيراد وتصدير
    """


class ImportExportTemplateUpdate(BaseModel):
    """
    نموذج تحديث قالب استيراد وتصدير
    """
    name: Optional[str] = None
    description: Optional[str] = None
    field_mapping: Optional[Dict[str, str]] = None
    options: Optional[Dict[str, Any]] = None


class ImportExportTemplate(ImportExportTemplateBase):
    """
    نموذج قالب استيراد وتصدير كامل
    """
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int

    class Config:
        orm_mode = True


class ImportRequest(BaseModel):
    """
    نموذج طلب استيراد
    """
    module: str
    template_id: Optional[int] = None
    options: Optional[Dict[str, Any]] = None


class ExportRequest(BaseModel):
    """
    نموذج طلب تصدير
    """
    module: str
    format: FileFormat
    template_id: Optional[int] = None
    filters: Optional[Dict[str, Any]] = None
    fields: Optional[List[str]] = None
    options: Optional[Dict[str, Any]] = None


class ImportResult(BaseModel):
    """
    نموذج نتيجة الاستيراد
    """
    job_id: str
    status: JobStatus
    message: str
    imported_count: Optional[int] = None
    error_count: Optional[int] = None
    warnings: Optional[List[str]] = None
    details: Optional[Dict[str, Any]] = None


class ExportResult(BaseModel):
    """
    نموذج نتيجة التصدير
    """
    job_id: str
    status: JobStatus
    message: str
    exported_count: Optional[int] = None
    download_url: Optional[str] = None
    filename: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class JobStatusDetail(BaseModel):
    """
    نموذج تفاصيل حالة المهمة
    """
    job_id: str
    job_type: JobType
    module: str
    status: JobStatus
    progress: Optional[float] = None
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    user_id: int
    result: Optional[Union[ImportResult, ExportResult]] = None

    class Config:
        orm_mode = True


class PaginatedImportExportJobs(BaseModel):
    """
    نموذج قائمة مهام الاستيراد والتصدير المقسمة إلى صفحات
    """
    items: List[JobStatusDetail]
    total: int
    page: int
    page_size: int
    total_pages: int


class ImportExportSettingsBase(BaseModel):
    """
    النموذج الأساسي لإعدادات الاستيراد والتصدير
    """
    max_file_size_mb: int = Field(10, ge=1, le=100)
    allowed_formats: List[FileFormat] = [
        FileFormat.CSV, FileFormat.XLSX, FileFormat.JSON]
    default_batch_size: int = Field(1000, ge=100, le=10000)
    export_expiry_days: int = Field(7, ge=1, le=30)
    enable_background_processing: bool = True
    notify_on_completion: bool = True


class ImportExportSettingsUpdate(ImportExportSettingsBase):
    """
    نموذج تحديث إعدادات الاستيراد والتصدير
    """


class ImportExportSettings(ImportExportSettingsBase):
    """
    نموذج إعدادات الاستيراد والتصدير الكامل
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ValidationRequest(BaseModel):
    """
    نموذج طلب التحقق من صحة تعيين الحقول
    """
    module: str
    field_mapping: Dict[str, str]
    sample_data: Optional[List[Dict[str, Any]]] = None


class ValidationResult(BaseModel):
    """
    نموذج نتيجة التحقق من صحة تعيين الحقول
    """
    is_valid: bool
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    details: Optional[Dict[str, Any]] = None


class DeleteResponse(BaseModel):
    """
    نموذج استجابة الحذف
    """
    success: bool
    message: str
