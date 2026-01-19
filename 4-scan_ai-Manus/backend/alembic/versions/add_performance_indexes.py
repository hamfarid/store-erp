"""
Add Performance Indexes

This migration adds database indexes on frequently queried columns
to improve query performance.

Revision ID: add_performance_indexes
Create Date: 2025-12-19
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'add_performance_indexes'
down_revision = None  # Update this to your last migration
branch_labels = None
depends_on = None


def upgrade():
    """Add performance indexes"""
    
    # ===== Users Table =====
    # Index for active users lookup
    op.create_index(
        'ix_users_is_active',
        'users',
        ['is_active'],
        unique=False
    )
    # Index for role-based queries
    op.create_index(
        'ix_users_role',
        'users',
        ['role'],
        unique=False
    )
    # Index for soft delete
    op.create_index(
        'ix_users_deleted_at',
        'users',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Farms Table =====
    op.create_index(
        'ix_farms_user_id',
        'farms',
        ['user_id'],
        unique=False
    )
    op.create_index(
        'ix_farms_deleted_at',
        'farms',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Crops Table =====
    op.create_index(
        'ix_crops_category',
        'crops',
        ['category'],
        unique=False
    )
    op.create_index(
        'ix_crops_deleted_at',
        'crops',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Diseases Table =====
    op.create_index(
        'ix_diseases_category',
        'diseases',
        ['category'],
        unique=False
    )
    op.create_index(
        'ix_diseases_severity',
        'diseases',
        ['severity'],
        unique=False
    )
    op.create_index(
        'ix_diseases_deleted_at',
        'diseases',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Sensors Table =====
    op.create_index(
        'ix_sensors_farm_id',
        'sensors',
        ['farm_id'],
        unique=False
    )
    op.create_index(
        'ix_sensors_type',
        'sensors',
        ['type'],
        unique=False
    )
    op.create_index(
        'ix_sensors_status',
        'sensors',
        ['status'],
        unique=False
    )
    op.create_index(
        'ix_sensors_deleted_at',
        'sensors',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Sensor Readings Table =====
    op.create_index(
        'ix_sensor_readings_sensor_id',
        'sensor_readings',
        ['sensor_id'],
        unique=False
    )
    op.create_index(
        'ix_sensor_readings_timestamp',
        'sensor_readings',
        ['timestamp'],
        unique=False
    )
    # Composite index for time-range queries per sensor
    op.create_index(
        'ix_sensor_readings_sensor_timestamp',
        'sensor_readings',
        ['sensor_id', 'timestamp'],
        unique=False
    )
    
    # ===== Inventory Table =====
    op.create_index(
        'ix_inventory_category',
        'inventory',
        ['category'],
        unique=False
    )
    op.create_index(
        'ix_inventory_deleted_at',
        'inventory',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Equipment Table =====
    op.create_index(
        'ix_equipment_type',
        'equipment',
        ['type'],
        unique=False
    )
    op.create_index(
        'ix_equipment_status',
        'equipment',
        ['status'],
        unique=False
    )
    op.create_index(
        'ix_equipment_deleted_at',
        'equipment',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Diagnoses Table =====
    op.create_index(
        'ix_diagnoses_user_id',
        'diagnoses',
        ['user_id'],
        unique=False
    )
    op.create_index(
        'ix_diagnoses_disease_id',
        'diagnoses',
        ['disease_id'],
        unique=False
    )
    op.create_index(
        'ix_diagnoses_created_at',
        'diagnoses',
        ['created_at'],
        unique=False
    )
    op.create_index(
        'ix_diagnoses_deleted_at',
        'diagnoses',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Breeding Programs Table =====
    op.create_index(
        'ix_breeding_programs_user_id',
        'breeding_programs',
        ['user_id'],
        unique=False
    )
    op.create_index(
        'ix_breeding_programs_status',
        'breeding_programs',
        ['status'],
        unique=False
    )
    op.create_index(
        'ix_breeding_programs_deleted_at',
        'breeding_programs',
        ['deleted_at'],
        unique=False
    )
    
    # ===== Companies Table =====
    op.create_index(
        'ix_companies_type',
        'companies',
        ['type'],
        unique=False
    )
    op.create_index(
        'ix_companies_deleted_at',
        'companies',
        ['deleted_at'],
        unique=False
    )


def downgrade():
    """Remove performance indexes"""
    
    # Users
    op.drop_index('ix_users_is_active', table_name='users')
    op.drop_index('ix_users_role', table_name='users')
    op.drop_index('ix_users_deleted_at', table_name='users')
    
    # Farms
    op.drop_index('ix_farms_user_id', table_name='farms')
    op.drop_index('ix_farms_deleted_at', table_name='farms')
    
    # Crops
    op.drop_index('ix_crops_category', table_name='crops')
    op.drop_index('ix_crops_deleted_at', table_name='crops')
    
    # Diseases
    op.drop_index('ix_diseases_category', table_name='diseases')
    op.drop_index('ix_diseases_severity', table_name='diseases')
    op.drop_index('ix_diseases_deleted_at', table_name='diseases')
    
    # Sensors
    op.drop_index('ix_sensors_farm_id', table_name='sensors')
    op.drop_index('ix_sensors_type', table_name='sensors')
    op.drop_index('ix_sensors_status', table_name='sensors')
    op.drop_index('ix_sensors_deleted_at', table_name='sensors')
    
    # Sensor Readings
    op.drop_index('ix_sensor_readings_sensor_id', table_name='sensor_readings')
    op.drop_index('ix_sensor_readings_timestamp', table_name='sensor_readings')
    op.drop_index('ix_sensor_readings_sensor_timestamp', table_name='sensor_readings')
    
    # Inventory
    op.drop_index('ix_inventory_category', table_name='inventory')
    op.drop_index('ix_inventory_deleted_at', table_name='inventory')
    
    # Equipment
    op.drop_index('ix_equipment_type', table_name='equipment')
    op.drop_index('ix_equipment_status', table_name='equipment')
    op.drop_index('ix_equipment_deleted_at', table_name='equipment')
    
    # Diagnoses
    op.drop_index('ix_diagnoses_user_id', table_name='diagnoses')
    op.drop_index('ix_diagnoses_disease_id', table_name='diagnoses')
    op.drop_index('ix_diagnoses_created_at', table_name='diagnoses')
    op.drop_index('ix_diagnoses_deleted_at', table_name='diagnoses')
    
    # Breeding Programs
    op.drop_index('ix_breeding_programs_user_id', table_name='breeding_programs')
    op.drop_index('ix_breeding_programs_status', table_name='breeding_programs')
    op.drop_index('ix_breeding_programs_deleted_at', table_name='breeding_programs')
    
    # Companies
    op.drop_index('ix_companies_type', table_name='companies')
    op.drop_index('ix_companies_deleted_at', table_name='companies')
