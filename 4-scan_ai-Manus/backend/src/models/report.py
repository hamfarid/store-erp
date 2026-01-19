"""
FILE: backend/src/models/report.py | PURPOSE: Report database model | OWNER: Backend Team | LAST-AUDITED: 2025-11-18

Report Model

Represents generated reports (PDF, Excel, etc.).

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text

from ..core.database import Base


class Report(Base):
    """Report model for generated documents"""

    __tablename__ = 'reports'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        index=True)
    farm_id = Column(Integer, ForeignKey('farms.id'), index=True)

    # Report Details
    title = Column(String(255), nullable=False)
    title_ar = Column(String(255))
    # farm_summary, diagnosis_history, monthly, annual
    report_type = Column(String(100), nullable=False)
    format = Column(String(20), nullable=False)  # pdf, excel, csv, ppt

    # File Information
    file_url = Column(String(500))
    file_path = Column(String(500))
    file_size = Column(Integer)  # in bytes

    # Report Parameters
    parameters = Column(JSON)  # Report generation parameters
    date_from = Column(DateTime)
    date_to = Column(DateTime)

    # Status
    # pending, processing, completed, failed
    status = Column(String(50), default='pending')
    progress = Column(Integer, default=0)  # 0-100
    error_message = Column(Text)

    # Processing Information
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)
    processing_duration = Column(Float)  # in seconds

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    deleted_at = Column(DateTime)  # Soft delete
    expires_at = Column(DateTime)  # Report expiration date

    # Relationships
    # user = relationship("User", back_populates="reports")
    # farm = relationship("Farm", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, title='{self.title}', type='{self.report_type}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farm_id': self.farm_id,
            'title': self.title,
            'title_ar': self.title_ar,
            'report_type': self.report_type,
            'format': self.format,
            'file_url': self.file_url,
            'file_size': self.file_size,
            'parameters': self.parameters,
            'date_from': self.date_from.isoformat() if self.date_from else None,
            'date_to': self.date_to.isoformat() if self.date_to else None,
            'status': self.status,
            'progress': self.progress,
            'processing_duration': self.processing_duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
        }
