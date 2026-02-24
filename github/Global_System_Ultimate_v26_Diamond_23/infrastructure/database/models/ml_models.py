from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class FeatureGroup(Base):
    __tablename__ = 'feature_groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = Column(String(100), nullable=False)
    tags = Column(JSON)
    
    features = relationship("Feature", back_populates="group")

class Feature(Base):
    __tablename__ = 'features'
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('feature_groups.id'))
    name = Column(String(255), nullable=False)
    data_type = Column(String(50), nullable=False)
    description = Column(Text)
    is_categorical = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    group = relationship("FeatureGroup", back_populates="features")

class Model(Base):
    __tablename__ = 'models'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    framework = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    versions = relationship("ModelVersion", back_populates="model")

class ModelVersion(Base):
    __tablename__ = 'model_versions'
    
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    version = Column(String(50), nullable=False)
    s3_path = Column(String(512), nullable=False)
    metrics = Column(JSON)
    parameters = Column(JSON)
    status = Column(String(50), default='staging')
    deployed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    model = relationship("Model", back_populates="versions")
