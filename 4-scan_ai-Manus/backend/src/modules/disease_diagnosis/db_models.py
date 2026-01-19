# File:
# /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/db_models.py

"""
نماذج قاعدة البيانات لتشخيص الأمراض النباتية
توفر هذه الوحدة نماذج قاعدة البيانات للمحاصيل والأمراض النباتية وأعراضها وطرق علاجها
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Constants
PLANT_DISEASES_ID_FK = 'plant_diseases.id'

Base = declarative_base()

# جدول العلاقة بين الأعراض والأمراض
disease_symptom = Table(
    'disease_symptom',
    Base.metadata,
    Column(
        'disease_id',
        Integer,
        ForeignKey(PLANT_DISEASES_ID_FK),
        primary_key=True),
    Column(
        'symptom_id',
        Integer,
        ForeignKey('disease_symptoms.id'),
        primary_key=True))

# جدول العلاقة بين العلاجات والأمراض
disease_treatment = Table(
    'disease_treatment',
    Base.metadata,
    Column(
        'disease_id',
        Integer,
        ForeignKey(PLANT_DISEASES_ID_FK),
        primary_key=True),
    Column(
        'treatment_id',
        Integer,
        ForeignKey('disease_treatments.id'),
        primary_key=True))

# جدول العلاقة بين الوقاية والأمراض
disease_prevention = Table(
    'disease_prevention',
    Base.metadata,
    Column(
        'disease_id',
        Integer,
        ForeignKey(PLANT_DISEASES_ID_FK),
        primary_key=True),
    Column(
        'prevention_id',
        Integer,
        ForeignKey('disease_preventions.id'),
        primary_key=True))

# جدول العلاقة بين الظروف والأمراض
disease_condition = Table(
    'disease_condition',
    Base.metadata,
    Column(
        'disease_id',
        Integer,
        ForeignKey(PLANT_DISEASES_ID_FK),
        primary_key=True),
    Column(
        'condition_id',
        Integer,
        ForeignKey('disease_conditions.id'),
        primary_key=True))


class Crop(Base):
    """نموذج المحصول الزراعي"""
    __tablename__ = 'crops'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    name_en = Column(String(100))
    scientific_name = Column(String(100))
    description = Column(Text)
    image_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    diseases = relationship("Disease", back_populates="crop")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "nameEn": self.name_en,
            "scientificName": self.scientific_name,
            "description": self.description,
            "imagePath": self.image_path,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None}


class Disease(Base):
    """نموذج المرض النباتي"""
    __tablename__ = 'plant_diseases'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100))
    scientific_name = Column(String(100))
    description = Column(Text)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    crop = relationship("Crop", back_populates="diseases")
    images = relationship(
        "DiseaseImage",
        back_populates="disease",
        cascade="all, delete-orphan")
    symptoms = relationship(
        "Symptom",
        secondary=disease_symptom,
        backref="diseases")
    treatments = relationship(
        "Treatment",
        secondary=disease_treatment,
        backref="diseases")
    preventions = relationship(
        "Prevention",
        secondary=disease_prevention,
        backref="diseases")
    conditions = relationship(
        "Condition",
        secondary=disease_condition,
        backref="diseases")
    diagnoses = relationship(
        "Diagnosis",
        back_populates="disease",
        cascade="all, delete-orphan")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "nameEn": self.name_en,
            "scientificName": self.scientific_name,
            "description": self.description,
            "cropId": self.crop_id,
            "cropName": self.crop.name if self.crop else None,
            "symptoms": [symptom.description for symptom in self.symptoms],
            "treatments": [treatment.description for treatment in self.treatments],
            "preventions": [prevention.description for prevention in self.preventions],
            "conditions": [condition.description for condition in self.conditions],
            "images": [image.to_dict() for image in self.images],
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }


class DiseaseImage(Base):
    """نموذج صورة المرض النباتي"""
    __tablename__ = 'disease_images'

    id = Column(Integer, primary_key=True)
    disease_id = Column(
        Integer,
        ForeignKey(PLANT_DISEASES_ID_FK),
        nullable=False)
    file_path = Column(String(255), nullable=False)
    caption = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    disease = relationship("Disease", back_populates="images")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "diseaseId": self.disease_id,
            "filePath": self.file_path,
            "caption": self.caption,
            "createdAt": self.created_at.isoformat() if self.created_at else None}


class Symptom(Base):
    """نموذج أعراض المرض النباتي"""
    __tablename__ = 'disease_symptoms'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, unique=True)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "description": self.description
        }


class Treatment(Base):
    """نموذج علاجات المرض النباتي"""
    __tablename__ = 'disease_treatments'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, unique=True)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "description": self.description
        }


class Prevention(Base):
    """نموذج طرق الوقاية من المرض النباتي"""
    __tablename__ = 'disease_preventions'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, unique=True)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "description": self.description
        }


class Condition(Base):
    """نموذج الظروف المناسبة للمرض النباتي"""
    __tablename__ = 'disease_conditions'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, unique=True)

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "description": self.description
        }


class Diagnosis(Base):
    """نموذج تشخيص المرض النباتي"""
    __tablename__ = 'disease_diagnoses'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    disease_id = Column(
        Integer,
        ForeignKey(PLANT_DISEASES_ID_FK),
        nullable=False)
    confidence = Column(Float, nullable=False)
    symptoms_text = Column(Text)
    image_path = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    disease = relationship("Disease", back_populates="diagnoses")

    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "userId": self.user_id,
            "diseaseId": self.disease_id,
            "diseaseName": self.disease.name if self.disease else None,
            "confidence": self.confidence,
            "symptomsText": self.symptoms_text,
            "imagePath": self.image_path,
            "notes": self.notes,
            "createdAt": self.created_at.isoformat() if self.created_at else None}
