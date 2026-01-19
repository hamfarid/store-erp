"""
FILE: backend/src/api/v1/reports.py | PURPOSE: Reports API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Reports API Routes

Handles report generation and management with async background processing.

Version: 2.0.0 - Added async generation and file download
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.config import get_settings
from ...models.report import Report
from ...models.user import User
from .auth import get_current_user

logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

# Reports directory
REPORTS_DIR = Path("data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# Pydantic Schemas
class ReportCreate(BaseModel):
    title: str
    report_type: str  # farm_summary, diagnosis_history, monthly, annual
    format: str  # pdf, excel, csv, ppt
    farm_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    parameters: Optional[dict] = None


class ReportResponse(BaseModel):
    id: int
    user_id: int
    title: str
    report_type: str
    format: str
    status: str
    progress: int
    file_url: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    success: bool = True
    data: List[ReportResponse]
    total: int


# ===== Background Task for Report Generation =====
async def generate_report_async(report_id: int, db_url: str):
    """
    Background task to generate report
    مهمة خلفية لتوليد التقرير
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    try:
        # إنشاء session جديد للمهمة الخلفية
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()

        try:
            report = db.query(Report).filter(Report.id == report_id).first()
            if not report:
                logger.error(f"Report {report_id} not found")
                return

            # تحديث الحالة إلى processing
            report.status = "processing"
            report.progress = 10
            db.commit()

            # محاكاة توليد التقرير
            import time

            # Step 1: جمع البيانات
            report.progress = 30
            db.commit()
            time.sleep(1)

            # Step 2: معالجة البيانات
            report.progress = 60
            db.commit()
            time.sleep(1)

            # Step 3: إنشاء الملف
            report.progress = 90
            db.commit()

            # إنشاء ملف التقرير
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{report_id}_{timestamp}.{report.format}"
            filepath = REPORTS_DIR / filename

            # كتابة محتوى وهمي (في الإنتاج، استخدم مكتبات PDF/Excel)
            if report.format == "csv":
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("id,title,type,created_at\n")
                    f.write(f"{report.id},{report.title},{report.report_type},{report.created_at}\n")
            else:
                # للـ PDF/Excel - إنشاء ملف نصي مؤقت
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Report: {report.title}\n")
                    f.write(f"Type: {report.report_type}\n")
                    f.write(f"Generated: {datetime.utcnow().isoformat()}\n")

            # تحديث التقرير بمسار الملف
            report.file_url = str(filepath)
            report.status = "completed"
            report.progress = 100
            report.processing_completed_at = datetime.utcnow()
            db.commit()

            logger.info(f"✅ Report {report_id} generated successfully: {filepath}")

        finally:
            db.close()

    except Exception as e:
        logger.error(f"❌ Error generating report {report_id}: {e}")
        # محاولة تحديث حالة الخطأ
        try:
            report = db.query(Report).filter(Report.id == report_id).first()
            if report:
                report.status = "failed"
                report.error_message = str(e)
                db.commit()
        except BaseException:
            pass


# Routes
@router.post("/generate", response_model=ReportResponse,
             status_code=status.HTTP_201_CREATED)
async def generate_report(
    report_data: ReportCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a new report asynchronously
    توليد تقرير جديد بشكل غير متزامن
    """

    # Validate report type
    valid_types = ['farm_summary', 'diagnosis_history', 'monthly', 'annual']
    if report_data.report_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid report type. Must be one of: {', '.join(valid_types)}")

    # Validate format
    valid_formats = ['pdf', 'excel', 'csv', 'ppt']
    if report_data.format not in valid_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid format. Must be one of: {', '.join(valid_formats)}")

    # Create report record
    report = Report(
        user_id=current_user.id,
        title=report_data.title,
        report_type=report_data.report_type,
        format=report_data.format,
        farm_id=report_data.farm_id,
        date_from=report_data.date_from,
        date_to=report_data.date_to,
        parameters=report_data.parameters,
        status="pending",
        progress=0,
        processing_started_at=datetime.utcnow()
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    # Trigger async report generation
    settings = get_settings()
    db_url = str(settings.DATABASE_URL)
    background_tasks.add_task(generate_report_async, report.id, db_url)

    logger.info(f"📋 Report {report.id} queued for generation")

    return report


@router.get("/", response_model=ReportListResponse)
async def list_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all reports for current user
    قائمة جميع التقارير للمستخدم الحالي
    """

    query = db.query(Report).filter(
        Report.user_id == current_user.id,
        Report.deleted_at is None
    )

    if report_type:
        query = query.filter(Report.report_type == report_type)

    if status_filter:
        query = query.filter(Report.status == status_filter)

    total = query.count()
    reports = query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()

    return {
        "success": True,
        "data": reports,
        "total": total
    }


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific report"""

    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id,
        Report.deleted_at is None
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return report


@router.get("/{report_id}/status")
async def get_report_status(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get report generation status (for polling)
    الحصول على حالة توليد التقرير (للاستعلام المتكرر)
    """
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id,
        Report.deleted_at is None
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return {
        "id": report.id,
        "status": report.status,
        "progress": report.progress,
        "is_ready": report.status == "completed",
        "error_message": getattr(report, 'error_message', None)
    }


@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download a report file
    تنزيل ملف التقرير
    """

    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id,
        Report.deleted_at is None
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if report.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Report is not ready for download. Current status: {report.status}"
        )

    if not report.file_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found"
        )

    # التحقق من وجود الملف
    file_path = Path(report.file_url)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file has been deleted or moved"
        )

    # تحديد نوع المحتوى
    content_type_map = {
        "pdf": "application/pdf",
        "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "csv": "text/csv",
        "ppt": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    }

    media_type = content_type_map.get(report.format, "application/octet-stream")
    filename = f"{report.title.replace(' ', '_')}.{report.format}"

    logger.info(f"📥 Downloading report {report_id}: {filename}")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a report (soft delete)"""

    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id,
        Report.deleted_at is None
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    # Soft delete
    report.deleted_at = datetime.utcnow()
    db.commit()

    return None
