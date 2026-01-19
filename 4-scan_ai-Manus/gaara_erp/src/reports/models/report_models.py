"""
نماذج بيانات وحدة التقارير
يحتوي هذا الملف على تعريف نماذج البيانات اللازمة لوحدة التقارير
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum
from uuid import uuid4


class ReportType(str, Enum):
    """نوع التقرير"""
    SYSTEM = "system"  # تقرير نظام
    FINANCIAL = "financial"  # تقرير مالي
    INVENTORY = "inventory"  # تقرير مخزون
    NURSERY = "nursery"  # تقرير مشاتل
    FARM = "farm"  # تقرير مزارع
    HR = "hr"  # تقرير موارد بشرية
    AI = "ai"  # تقرير ذكاء اصطناعي
    CUSTOM = "custom"  # تقرير مخصص


class ReportFormat(str, Enum):
    """صيغة التقرير"""
    PDF = "pdf"  # PDF
    EXCEL = "excel"  # Excel
    CSV = "csv"  # CSV
    HTML = "html"  # HTML
    JSON = "json"  # JSON


class ReportFrequency(str, Enum):
    """تكرار التقرير"""
    ONCE = "once"  # مرة واحدة
    DAILY = "daily"  # يومي
    WEEKLY = "weekly"  # أسبوعي
    MONTHLY = "monthly"  # شهري
    QUARTERLY = "quarterly"  # ربع سنوي
    YEARLY = "yearly"  # سنوي


class ReportStatus(str, Enum):
    """حالة التقرير"""
    PENDING = "pending"  # قيد الانتظار
    GENERATING = "generating"  # قيد الإنشاء
    COMPLETED = "completed"  # مكتمل
    FAILED = "failed"  # فشل
    SCHEDULED = "scheduled"  # مجدول


class ReportTemplate:
    """قالب التقرير"""
    
    def __init__(
        self,
        name: str,
        description: str,
        report_type: ReportType,
        query_template: str,
        parameters: Dict[str, Any],
        created_by: str,
        template_id: Optional[str] = None,
        is_system: bool = False,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.template_id = template_id or str(uuid4())
        self.name = name
        self.description = description
        self.report_type = report_type
        self.query_template = query_template
        self.parameters = parameters
        self.created_by = created_by
        self.is_system = is_system
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "template_id": self.template_id,
            "name": self.name,
            "description": self.description,
            "report_type": self.report_type,
            "query_template": self.query_template,
            "parameters": self.parameters,
            "created_by": self.created_by,
            "is_system": self.is_system,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReportTemplate':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        if "report_type" in data and isinstance(data["report_type"], str):
            data["report_type"] = ReportType(data["report_type"])
        
        return cls(
            name=data["name"],
            description=data["description"],
            report_type=data["report_type"],
            query_template=data["query_template"],
            parameters=data["parameters"],
            created_by=data["created_by"],
            template_id=data.get("template_id"),
            is_system=data.get("is_system", False),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class Report:
    """تقرير"""
    
    def __init__(
        self,
        template_id: str,
        parameters: Dict[str, Any],
        created_by: str,
        report_id: Optional[str] = None,
        report_format: Optional[ReportFormat] = None,
        status: Optional[ReportStatus] = None,
        file_path: Optional[str] = None,
        error_message: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ):
        self.report_id = report_id or str(uuid4())
        self.template_id = template_id
        self.parameters = parameters
        self.created_by = created_by
        self.report_format = report_format or ReportFormat.PDF
        self.status = status or ReportStatus.PENDING
        self.file_path = file_path
        self.error_message = error_message
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.completed_at = completed_at
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        result = {
            "report_id": self.report_id,
            "template_id": self.template_id,
            "parameters": self.parameters,
            "created_by": self.created_by,
            "report_format": self.report_format,
            "status": self.status,
            "file_path": self.file_path,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        
        if self.completed_at:
            result["completed_at"] = self.completed_at.isoformat()
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Report':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        if "completed_at" in data and isinstance(data["completed_at"], str):
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        
        if "report_format" in data and isinstance(data["report_format"], str):
            data["report_format"] = ReportFormat(data["report_format"])
        
        if "status" in data and isinstance(data["status"], str):
            data["status"] = ReportStatus(data["status"])
        
        return cls(
            template_id=data["template_id"],
            parameters=data["parameters"],
            created_by=data["created_by"],
            report_id=data.get("report_id"),
            report_format=data.get("report_format"),
            status=data.get("status"),
            file_path=data.get("file_path"),
            error_message=data.get("error_message"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            completed_at=data.get("completed_at")
        )


class ScheduledReport:
    """تقرير مجدول"""
    
    def __init__(
        self,
        template_id: str,
        parameters: Dict[str, Any],
        frequency: ReportFrequency,
        created_by: str,
        schedule_id: Optional[str] = None,
        report_format: Optional[ReportFormat] = None,
        is_active: bool = True,
        next_run: Optional[datetime] = None,
        last_run: Optional[datetime] = None,
        last_report_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.schedule_id = schedule_id or str(uuid4())
        self.template_id = template_id
        self.parameters = parameters
        self.frequency = frequency
        self.created_by = created_by
        self.report_format = report_format or ReportFormat.PDF
        self.is_active = is_active
        self.next_run = next_run
        self.last_run = last_run
        self.last_report_id = last_report_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        result = {
            "schedule_id": self.schedule_id,
            "template_id": self.template_id,
            "parameters": self.parameters,
            "frequency": self.frequency,
            "created_by": self.created_by,
            "report_format": self.report_format,
            "is_active": self.is_active,
            "last_report_id": self.last_report_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        
        if self.next_run:
            result["next_run"] = self.next_run.isoformat()
        
        if self.last_run:
            result["last_run"] = self.last_run.isoformat()
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScheduledReport':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        if "next_run" in data and isinstance(data["next_run"], str):
            data["next_run"] = datetime.fromisoformat(data["next_run"])
        
        if "last_run" in data and isinstance(data["last_run"], str):
            data["last_run"] = datetime.fromisoformat(data["last_run"])
        
        if "frequency" in data and isinstance(data["frequency"], str):
            data["frequency"] = ReportFrequency(data["frequency"])
        
        if "report_format" in data and isinstance(data["report_format"], str):
            data["report_format"] = ReportFormat(data["report_format"])
        
        return cls(
            template_id=data["template_id"],
            parameters=data["parameters"],
            frequency=data["frequency"],
            created_by=data["created_by"],
            schedule_id=data.get("schedule_id"),
            report_format=data.get("report_format"),
            is_active=data.get("is_active", True),
            next_run=data.get("next_run"),
            last_run=data.get("last_run"),
            last_report_id=data.get("last_report_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class ReportDashboard:
    """لوحة تحكم التقارير"""
    
    def __init__(
        self,
        name: str,
        description: str,
        layout: Dict[str, Any],
        created_by: str,
        dashboard_id: Optional[str] = None,
        is_public: bool = False,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.dashboard_id = dashboard_id or str(uuid4())
        self.name = name
        self.description = description
        self.layout = layout
        self.created_by = created_by
        self.is_public = is_public
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "dashboard_id": self.dashboard_id,
            "name": self.name,
            "description": self.description,
            "layout": self.layout,
            "created_by": self.created_by,
            "is_public": self.is_public,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReportDashboard':
        """إنشاء كائن من قاموس"""
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        return cls(
            name=data["name"],
            description=data["description"],
            layout=data["layout"],
            created_by=data["created_by"],
            dashboard_id=data.get("dashboard_id"),
            is_public=data.get("is_public", False),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
