"""
FILE: backend/src/schemas/report.py
PURPOSE: Report Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class ReportBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    report_type: str = Field(..., pattern="^(diagnosis|farm|crop|analytics|custom)$")
    description: Optional[str] = None
    farm_id: Optional[int] = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None


class ReportCreate(ReportBase):
    parameters: Optional[Dict[str, Any]] = None


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class ReportInDB(ReportBase, TimestampMixin, BaseSchema):
    id: int
    creator_id: int
    status: str = "pending"
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    generated_at: Optional[datetime] = None


class ReportResponse(ReportInDB):
    creator_name: Optional[str] = None
    farm_name: Optional[str] = None


class ReportListResponse(BaseModel):
    items: List[ReportResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class ReportGenerateRequest(BaseModel):
    report_type: str
    farm_id: Optional[int] = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    include_sections: List[str] = []
    format: str = Field(default="pdf", pattern="^(pdf|excel|csv)$")


__all__ = ['ReportBase', 'ReportCreate', 'ReportUpdate', 'ReportInDB', 'ReportResponse', 'ReportListResponse', 'ReportGenerateRequest']
