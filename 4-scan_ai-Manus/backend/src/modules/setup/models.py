"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/models.py
الوصف: نماذج بيانات مديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.database import Base


class SetupStatus(Base):
    """نموذج حالة الإعداد"""
    __tablename__ = "setup_status"

    id = Column(Integer, primary_key=True, index=True)
    is_completed = Column(Boolean, default=False)
    current_step = Column(String(50), nullable=False)
    completed_steps = Column(JSON, default=list)
    setup_token = Column(String(100), nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class SetupLog(Base):
    """نموذج سجل الإعداد"""
    __tablename__ = "setup_logs"

    id = Column(Integer, primary_key=True, index=True)
    step = Column(String(50), nullable=False)
    # success, error, warning, info
    status = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class Company(Base):
    """نموذج الشركة"""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    legal_name = Column(String(200), nullable=True)
    tax_number = Column(String(50), nullable=True)
    registration_number = Column(String(50), nullable=True)
    address = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    country_code = Column(String(2), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(100), nullable=True)
    logo_path = Column(String(200), nullable=True)
    currency_code = Column(String(3), nullable=False)
    timezone = Column(String(50), nullable=False)
    locale = Column(String(10), nullable=False)
    fiscal_year_start = Column(String(5), nullable=False)  # Format: MM-DD
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    # العلاقات
    branches = relationship("Branch", back_populates="company")


class Branch(Base):
    """نموذج فرع الشركة"""
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    address = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    country_code = Column(String(2), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    is_main = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    # العلاقات
    company = relationship("Company", back_populates="branches")


class SetupIntegration(Base):
    """نموذج تكامل الإعداد مع المديولات الأخرى"""
    __tablename__ = "setup_integrations"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(String(50), nullable=False)
    module_name = Column(String(100), nullable=False)
    integration_type = Column(String(50),
                              nullable=False)  # setup, config, data
    # pending, completed, failed
    integration_status = Column(String(20), nullable=False)
    integration_details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)


class SetupTask(Base):
    """نموذج مهمة الإعداد"""
    __tablename__ = "setup_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(100), nullable=False)
    task_description = Column(Text, nullable=True)
    # pending, in_progress, completed, failed
    task_status = Column(String(20), nullable=False)
    task_order = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    depends_on = Column(JSON, default=list)
    task_details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
