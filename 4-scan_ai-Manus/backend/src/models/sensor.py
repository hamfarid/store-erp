"""
FILE: backend/src/models/sensor.py | PURPOSE: Sensor database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Sensor Model

Represents IoT sensors and their readings.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from ..core.database import Base


class Sensor(Base):
    """Sensor model for IoT sensors"""

    __tablename__ = 'sensors'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    farm_id = Column(
        Integer,
        ForeignKey('farms.id'),
        nullable=True,
        index=True)

    # Basic Information
    name = Column(String(255), nullable=False)
    # temperature, humidity, soil_moisture, light, wind, ph
    type = Column(String(100), nullable=False, index=True)
    serial_number = Column(String(100), unique=True, index=True)
    location = Column(String(255))

    # Configuration
    min_threshold = Column(Float)
    max_threshold = Column(Float)
    unit = Column(String(50))  # celsius, fahrenheit, percent, lux, etc.

    # Status
    # active, inactive, maintenance, error
    status = Column(String(50), default='active')
    battery_level = Column(Integer)  # 0-100

    # Current Reading
    value = Column(Float)
    last_update = Column(DateTime)

    # Additional Information
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)  # Soft delete

    # Relationships
    # farm = relationship("Farm", back_populates="sensors")
    # readings = relationship("SensorReading", back_populates="sensor")

    def __repr__(self):
        return f"<Sensor(id={self.id}, name='{self.name}', type='{self.type}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'name': self.name,
            'type': self.type,
            'serial_number': self.serial_number,
            'location': self.location,
            'min_threshold': self.min_threshold,
            'max_threshold': self.max_threshold,
            'unit': self.unit,
            'status': self.status,
            'battery_level': self.battery_level,
            'value': self.value,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class SensorReading(Base):
    """Sensor reading model for historical data"""

    __tablename__ = 'sensor_readings'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    sensor_id = Column(
        Integer,
        ForeignKey('sensors.id'),
        nullable=False,
        index=True)

    # Reading Data
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True)

    # Metadata
    quality = Column(String(50))  # good, warning, error
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    # sensor = relationship("Sensor", back_populates="readings")

    def __repr__(self):
        return f"<SensorReading(id={self.id}, sensor_id={self.sensor_id}, value={self.value})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'quality': self.quality,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
