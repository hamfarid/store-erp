"""
FILE: backend/src/models/relationships.py
PURPOSE: SQLAlchemy model relationships configuration
OWNER: Backend Team
LAST-AUDITED: 2026-01-19

Defines all ORM relationships between database models.
This file should be imported after all models are defined to avoid circular imports.

Relationship Summary:
- User -> Farms (one-to-many)
- User -> Diagnoses (one-to-many)
- User -> Reports (one-to-many)
- User -> Company (many-to-one)
- Farm -> Crops (many-to-many via FarmCrop)
- Farm -> Diagnoses (one-to-many)
- Farm -> Sensors (one-to-many)
- Farm -> Equipment (one-to-many)
- Farm -> Inventory (one-to-many)
- Crop -> Diseases (many-to-many via CropDisease)
- Diagnosis -> Disease (many-to-one)
- Sensor -> SensorReadings (one-to-many)
- BreedingProgram -> Crops (many-to-many)

Version: 2.0.0
"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.database import Base

# =============================================================================
# Association Tables (Many-to-Many Relationships)
# =============================================================================

# Farm <-> Crop association
farm_crops = Table(
    'farm_crops',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('farm_id', Integer, ForeignKey('farms.id', ondelete='CASCADE'), nullable=False),
    Column('crop_id', Integer, ForeignKey('crops.id', ondelete='CASCADE'), nullable=False),
    Column('planted_date', DateTime),
    Column('expected_harvest_date', DateTime),
    Column('area_allocated', Integer),  # in square meters
    Column('status', String(50), default='active'),  # active, harvested, failed
    Column('created_at', DateTime, default=datetime.utcnow)
)

# Crop <-> Disease association
crop_diseases = Table(
    'crop_diseases',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('crop_id', Integer, ForeignKey('crops.id', ondelete='CASCADE'), nullable=False),
    Column('disease_id', Integer, ForeignKey('diseases.id', ondelete='CASCADE'), nullable=False),
    Column('susceptibility_level', String(20), default='medium'),  # low, medium, high
    Column('created_at', DateTime, default=datetime.utcnow)
)

# BreedingProgram <-> Crop association
breeding_crops = Table(
    'breeding_crops',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('breeding_program_id', Integer, ForeignKey('breeding_programs.id', ondelete='CASCADE'), nullable=False),
    Column('crop_id', Integer, ForeignKey('crops.id', ondelete='CASCADE'), nullable=False),
    Column('role', String(50)),  # parent, child, control
    Column('created_at', DateTime, default=datetime.utcnow)
)


# =============================================================================
# Configure Relationships Function
# =============================================================================

def configure_relationships():
    """
    Configure all SQLAlchemy relationships.
    Call this function after all models are imported.
    """
    from .user import User
    from .farm import Farm
    from .crop import Crop
    from .disease import Disease
    from .diagnosis import Diagnosis
    from .sensor import Sensor, SensorReading
    from .equipment import Equipment
    from .inventory import Inventory
    from .report import Report
    from .company import Company
    from .breeding import BreedingProgram

    # =========================================================================
    # User Relationships
    # =========================================================================
    User.farms = relationship(
        "Farm",
        back_populates="owner",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    User.diagnoses = relationship(
        "Diagnosis",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    User.reports = relationship(
        "Report",
        back_populates="creator",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    User.company = relationship(
        "Company",
        back_populates="users",
        foreign_keys="[User.company_id]"
    )

    # =========================================================================
    # Farm Relationships
    # =========================================================================
    Farm.owner = relationship(
        "User",
        back_populates="farms"
    )
    Farm.diagnoses = relationship(
        "Diagnosis",
        back_populates="farm",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    Farm.sensors = relationship(
        "Sensor",
        back_populates="farm",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    Farm.equipment = relationship(
        "Equipment",
        back_populates="farm",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    Farm.inventory = relationship(
        "Inventory",
        back_populates="farm",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    Farm.crops = relationship(
        "Crop",
        secondary=farm_crops,
        back_populates="farms",
        lazy="dynamic"
    )

    # =========================================================================
    # Crop Relationships
    # =========================================================================
    Crop.farms = relationship(
        "Farm",
        secondary=farm_crops,
        back_populates="crops",
        lazy="dynamic"
    )
    Crop.diseases = relationship(
        "Disease",
        secondary=crop_diseases,
        back_populates="crops",
        lazy="dynamic"
    )
    Crop.breeding_programs = relationship(
        "BreedingProgram",
        secondary=breeding_crops,
        back_populates="crops",
        lazy="dynamic"
    )

    # =========================================================================
    # Disease Relationships
    # =========================================================================
    Disease.crops = relationship(
        "Crop",
        secondary=crop_diseases,
        back_populates="diseases",
        lazy="dynamic"
    )
    Disease.diagnoses = relationship(
        "Diagnosis",
        back_populates="disease_info",
        lazy="dynamic"
    )

    # =========================================================================
    # Diagnosis Relationships
    # =========================================================================
    Diagnosis.user = relationship(
        "User",
        back_populates="diagnoses"
    )
    Diagnosis.farm = relationship(
        "Farm",
        back_populates="diagnoses"
    )
    Diagnosis.disease_info = relationship(
        "Disease",
        back_populates="diagnoses",
        foreign_keys="[Diagnosis.disease_id]"
    )

    # =========================================================================
    # Sensor Relationships
    # =========================================================================
    Sensor.farm = relationship(
        "Farm",
        back_populates="sensors"
    )
    Sensor.readings = relationship(
        "SensorReading",
        back_populates="sensor",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    SensorReading.sensor = relationship(
        "Sensor",
        back_populates="readings"
    )

    # =========================================================================
    # Equipment Relationships
    # =========================================================================
    Equipment.farm = relationship(
        "Farm",
        back_populates="equipment"
    )

    # =========================================================================
    # Inventory Relationships
    # =========================================================================
    Inventory.farm = relationship(
        "Farm",
        back_populates="inventory"
    )

    # =========================================================================
    # Report Relationships
    # =========================================================================
    Report.creator = relationship(
        "User",
        back_populates="reports"
    )
    Report.farm = relationship(
        "Farm"
    )

    # =========================================================================
    # Company Relationships
    # =========================================================================
    Company.users = relationship(
        "User",
        back_populates="company",
        lazy="dynamic"
    )
    Company.farms = relationship(
        "Farm",
        secondary="users",
        viewonly=True
    )

    # =========================================================================
    # Breeding Program Relationships
    # =========================================================================
    BreedingProgram.crops = relationship(
        "Crop",
        secondary=breeding_crops,
        back_populates="breeding_programs",
        lazy="dynamic"
    )


# Export association tables for migrations
__all__ = [
    'farm_crops',
    'crop_diseases',
    'breeding_crops',
    'configure_relationships'
]
