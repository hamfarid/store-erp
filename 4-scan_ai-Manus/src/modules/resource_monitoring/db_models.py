# File: /home/ubuntu/ai_web_organized/src/modules/resource_monitoring/db_models.py
"""
from flask import g
نماذج قاعدة البيانات لمراقبة الموارد
توفر هذه الوحدة نماذج قاعدة البيانات لتخزين بيانات الموارد التاريخية
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

# Constants for repeated string literals
RESOURCE_METRICS_ID = 'resource_metrics.id'

Base = declarative_base()


class ResourceType(enum.Enum):
    """أنواع الموارد المراقبة"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    DATABASE = "database"
    CUSTOM = "custom"


class ResourceMetric(Base):
    """نموذج قياسات الموارد"""
    __tablename__ = 'resource_metrics'

    id = Column(Integer, primary_key=True)
    resource_type = Column(String(50), nullable=False)
    metric_name = Column(String(100), nullable=False)
    display_name = Column(String(100))
    unit = Column(String(20))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    data_points = relationship("ResourceDataPoint", back_populates="metric", cascade="all, delete-orphan")
    thresholds = relationship("ResourceThreshold", back_populates="metric", cascade="all, delete-orphan")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "resourceType": self.resource_type,
            "metricName": self.metric_name,
            "displayName": self.display_name,
            "unit": self.unit,
            "description": self.description,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat() if hasattr(self, "created_at") and self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if hasattr(self, "updated_at") and self.updated_at else None
        }


class ResourceDataPoint(Base):
    """نموذج نقطة بيانات الموارد"""
    __tablename__ = 'resource_data_points'

    id = Column(Integer, primary_key=True)
    metric_id = Column(Integer, ForeignKey(RESOURCE_METRICS_ID), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    module_name = Column(String(100))
    server_id = Column(String(100))
    extra_data = Column(JSON)

    # العلاقات
    metric = relationship("ResourceMetric", back_populates="data_points")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "metricId": self.metric_id,
            "metricName": self.metric.metric_name if self.metric else None,
            "value": self.value,
            "timestamp": self.timestamp.isoformat() if hasattr(self, "timestamp") and self.timestamp else None,
            "moduleName": self.module_name,
            "serverId": self.server_id,
            "metadata": self.extra_data
        }


class ResourceThreshold(Base):
    """نموذج عتبات الموارد للتنبيهات"""
    __tablename__ = 'resource_thresholds'

    id = Column(Integer, primary_key=True)
    metric_id = Column(Integer, ForeignKey(RESOURCE_METRICS_ID), nullable=False)
    warning_threshold = Column(Float)
    critical_threshold = Column(Float)
    is_active = Column(Boolean, default=True)
    notification_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    metric = relationship("ResourceMetric", back_populates="thresholds")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "metricId": self.metric_id,
            "metricName": self.metric.metric_name if self.metric else None,
            "warningThreshold": self.warning_threshold,
            "criticalThreshold": self.critical_threshold,
            "isActive": self.is_active,
            "notificationEnabled": self.notification_enabled,
            "createdAt": self.created_at.isoformat() if hasattr(self, "created_at") and self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if hasattr(self, "updated_at") and self.updated_at else None
        }


class ResourceAggregation(Base):
    """نموذج تجميع بيانات الموارد"""
    __tablename__ = 'resource_aggregations'

    id = Column(Integer, primary_key=True)
    metric_id = Column(Integer, ForeignKey(RESOURCE_METRICS_ID), nullable=False)
    aggregation_type = Column(String(20), nullable=False)  # hourly, daily, weekly, monthly
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    avg_value = Column(Float)
    count = Column(Integer)
    module_name = Column(String(100))
    server_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "metricId": self.metric_id,
            "aggregationType": self.aggregation_type,
            "startTime": self.start_time.isoformat() if hasattr(self, "start_time") and self.start_time else None,
            "endTime": self.end_time.isoformat() if hasattr(self, "end_time") and self.end_time else None,
            "minValue": self.min_value,
            "maxValue": self.max_value,
            "avgValue": self.avg_value,
            "count": self.count,
            "moduleName": self.module_name,
            "serverId": self.server_id,
            "createdAt": self.created_at.isoformat() if hasattr(self, "created_at") and self.created_at else None
        }


class Server(Base):
    """نموذج الخادم"""
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    server_id = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(50))
    server_type = Column(String(50))
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "serverId": self.server_id,
            "name": self.name,
            "ipAddress": self.ip_address,
            "serverType": self.server_type,
            "location": self.location,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat() if hasattr(self, "created_at") and self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if hasattr(self, "updated_at") and self.updated_at else None
        }


class Module(Base):
    """نموذج المديول"""
    __tablename__ = 'modules'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100))
    description = Column(Text)
    version = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "version": self.version,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat() if hasattr(self, "created_at") and self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if hasattr(self, "updated_at") and self.updated_at else None
        }
