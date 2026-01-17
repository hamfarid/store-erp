# FILE: backend/src/validators/report_validators.py
# PURPOSE: Pydantic validators for Reports module
# OWNER: Gaara Store Team
# RELATED: contracts/openapi.yaml, backend/src/models/report.py
# LAST-AUDITED: 2025-10-27

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ReportType(str, Enum):
    """Report type enumeration"""

    SALES = "sales"
    INVENTORY = "inventory"
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    REVENUE = "revenue"
    EXPENSE = "expense"


class ReportFormat(str, Enum):
    """Report format enumeration"""

    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"


class ReportStatus(str, Enum):
    """Report status enumeration"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportCreateRequest(BaseModel):
    """Request to create a new report"""

    name: str = Field(..., min_length=1, max_length=100, description="Report name")
    report_type: ReportType = Field(..., description="Type of report")
    format: ReportFormat = Field(default=ReportFormat.PDF, description="Report format")
    start_date: datetime = Field(..., description="Report start date")
    end_date: datetime = Field(..., description="Report end date")
    filters: Optional[dict] = Field(None, description="Additional filters")
    include_summary: bool = Field(default=True, description="Include summary in report")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Monthly Sales Report",
                "report_type": "sales",
                "format": "pdf",
                "start_date": "2025-01-01T00:00:00Z",
                "end_date": "2025-01-31T23:59:59Z",
                "include_summary": True,
            }
        }


class ReportUpdateRequest(BaseModel):
    """Request to update a report"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    format: Optional[ReportFormat] = None
    filters: Optional[dict] = None
    include_summary: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {"name": "Updated Sales Report", "format": "excel"}
        }


class ReportData(BaseModel):
    """Report data structure"""

    total_records: int = Field(..., ge=0, description="Total records in report")
    summary: Optional[dict] = Field(None, description="Report summary")
    details: List[dict] = Field(default_factory=list, description="Report details")


class ReportResponse(BaseModel):
    """Report response"""

    id: str = Field(..., description="Report ID")
    name: str = Field(..., description="Report name")
    report_type: ReportType = Field(..., description="Report type")
    format: ReportFormat = Field(..., description="Report format")
    status: ReportStatus = Field(..., description="Report status")
    start_date: datetime = Field(..., description="Report start date")
    end_date: datetime = Field(..., description="Report end date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: str = Field(..., description="User who created the report")
    file_url: Optional[str] = Field(None, description="URL to download report file")
    data: Optional[ReportData] = Field(None, description="Report data")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "rpt_123456",
                "name": "Monthly Sales Report",
                "report_type": "sales",
                "format": "pdf",
                "status": "completed",
                "start_date": "2025-01-01T00:00:00Z",
                "end_date": "2025-01-31T23:59:59Z",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:35:00Z",
                "created_by": "user_123",
                "file_url": "https://api.gaaragroup.com/reports/rpt_123456/download",
            }
        }


class ReportListResponse(BaseModel):
    """List of reports response"""

    success: bool = Field(default=True)
    message: str = Field(default="Reports retrieved successfully")
    traceId: str = Field(..., description="Trace ID for debugging")
    data: Optional[dict] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Reports retrieved successfully",
                "traceId": "trace_123456",
                "data": {
                    "items": [],
                    "total": 0,
                    "page": 1,
                    "per_page": 10,
                    "pages": 0,
                },
            }
        }


class ReportDownloadRequest(BaseModel):
    """Request to download a report"""

    format: Optional[ReportFormat] = Field(None, description="Download format")

    class Config:
        json_schema_extra = {"example": {"format": "pdf"}}


class ReportScheduleRequest(BaseModel):
    """Request to schedule a recurring report"""

    name: str = Field(..., min_length=1, max_length=100)
    report_type: ReportType = Field(...)
    format: ReportFormat = Field(default=ReportFormat.PDF)
    frequency: str = Field(..., pattern=r"^(daily|weekly|monthly|quarterly|yearly)$")
    email_recipients: List[str] = Field(
        default_factory=list, description="Email recipients"
    )
    is_active: bool = Field(default=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Weekly Sales Report",
                "report_type": "sales",
                "format": "pdf",
                "frequency": "weekly",
                "email_recipients": ["manager@gaaragroup.com"],
                "is_active": True,
            }
        }
