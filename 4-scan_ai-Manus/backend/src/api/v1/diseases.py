"""
FILE: backend/src/api/v1/diseases.py | PURPOSE: Diseases API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Diseases Management API Routes

Handles CRUD operations for plant diseases.

Version: 1.1.0
"""

import json
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.disease import Disease
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/diseases", tags=["diseases"])


# Pydantic Schemas
class DiseaseCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str  # fungal, bacterial, viral, pest, nutritional, environmental
    severity: str = "medium"  # low, medium, high, critical
    symptoms: str
    causes: Optional[str] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None
    affected_crops: Optional[List[str]] = None
    image_url: Optional[str] = None


class DiseaseUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    symptoms: Optional[str] = None
    causes: Optional[str] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None
    affected_crops: Optional[List[str]] = None
    image_url: Optional[str] = None


class DiseaseResponse(BaseModel):
    id: int
    name: str
    name_en: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str
    severity: str
    symptoms: str
    causes: Optional[str] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None
    affected_crops: Optional[List[str]] = None
    image_url: Optional[str] = None
    cases_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiseaseListResponse(BaseModel):
    success: bool = True
    data: List[DiseaseResponse]
    total: int


# Helper function to parse affected_crops
def parse_affected_crops(crops_str: Optional[str]) -> Optional[List[str]]:
    if not crops_str:
        return None
    try:
        return json.loads(crops_str)
    except json.JSONDecodeError:
        return crops_str.split(",") if crops_str else None


# Routes
@router.get("", response_model=DiseaseListResponse)
async def get_diseases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    severity: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of diseases with pagination and filtering"""
    query = db.query(Disease).filter(Disease.deleted_at.is_(None))

    # Apply filters
    if category:
        query = query.filter(Disease.category == category)

    if severity:
        query = query.filter(Disease.severity == severity)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Disease.name.ilike(search_term),
                Disease.name_en.ilike(search_term),
                Disease.scientific_name.ilike(search_term),
                Disease.symptoms.ilike(search_term)
            )
        )

    total = query.count()
    diseases = query.order_by(Disease.name).offset(skip).limit(limit).all()

    # Convert to response format
    response_diseases = []
    for disease in diseases:
        disease_dict = {
            "id": disease.id,
            "name": disease.name,
            "name_en": disease.name_en,
            "scientific_name": disease.scientific_name,
            "category": disease.category,
            "severity": disease.severity,
            "symptoms": disease.symptoms,
            "causes": disease.causes,
            "treatment": disease.treatment,
            "prevention": disease.prevention,
            "affected_crops": parse_affected_crops(disease.affected_crops),
            "image_url": disease.image_url,
            "cases_count": disease.cases_count or 0,
            "created_at": disease.created_at,
            "updated_at": disease.updated_at
        }
        response_diseases.append(DiseaseResponse(**disease_dict))

    return DiseaseListResponse(success=True, data=response_diseases, total=total)


@router.get("/{disease_id}", response_model=DiseaseResponse)
async def get_disease(
    disease_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get disease by ID"""
    disease = db.query(Disease).filter(
        Disease.id == disease_id,
        Disease.deleted_at.is_(None)
    ).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    return DiseaseResponse(
        id=disease.id,
        name=disease.name,
        name_en=disease.name_en,
        scientific_name=disease.scientific_name,
        category=disease.category,
        severity=disease.severity,
        symptoms=disease.symptoms,
        causes=disease.causes,
        treatment=disease.treatment,
        prevention=disease.prevention,
        affected_crops=parse_affected_crops(disease.affected_crops),
        image_url=disease.image_url,
        cases_count=disease.cases_count or 0,
        created_at=disease.created_at,
        updated_at=disease.updated_at
    )


@router.post("", response_model=DiseaseResponse, status_code=status.HTTP_201_CREATED)
async def create_disease(
    disease_data: DiseaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new disease"""
    # Convert affected_crops list to JSON string
    crops_str = None
    if disease_data.affected_crops:
        crops_str = json.dumps(disease_data.affected_crops)

    new_disease = Disease(
        name=disease_data.name,
        name_en=disease_data.name_en,
        scientific_name=disease_data.scientific_name,
        category=disease_data.category,
        severity=disease_data.severity,
        symptoms=disease_data.symptoms,
        causes=disease_data.causes,
        treatment=disease_data.treatment,
        prevention=disease_data.prevention,
        affected_crops=crops_str,
        image_url=disease_data.image_url,
        cases_count=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_disease)
    db.commit()
    db.refresh(new_disease)

    return DiseaseResponse(
        id=new_disease.id,
        name=new_disease.name,
        name_en=new_disease.name_en,
        scientific_name=new_disease.scientific_name,
        category=new_disease.category,
        severity=new_disease.severity,
        symptoms=new_disease.symptoms,
        causes=new_disease.causes,
        treatment=new_disease.treatment,
        prevention=new_disease.prevention,
        affected_crops=disease_data.affected_crops,
        image_url=new_disease.image_url,
        cases_count=new_disease.cases_count or 0,
        created_at=new_disease.created_at,
        updated_at=new_disease.updated_at
    )


@router.put("/{disease_id}", response_model=DiseaseResponse)
async def update_disease(
    disease_id: int,
    disease_data: DiseaseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update disease"""
    disease = db.query(Disease).filter(
        Disease.id == disease_id,
        Disease.deleted_at.is_(None)
    ).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    # Update fields
    update_data = disease_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "affected_crops" and value is not None:
            value = json.dumps(value)
        setattr(disease, field, value)

    disease.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(disease)

    return DiseaseResponse(
        id=disease.id,
        name=disease.name,
        name_en=disease.name_en,
        scientific_name=disease.scientific_name,
        category=disease.category,
        severity=disease.severity,
        symptoms=disease.symptoms,
        causes=disease.causes,
        treatment=disease.treatment,
        prevention=disease.prevention,
        affected_crops=parse_affected_crops(disease.affected_crops),
        image_url=disease.image_url,
        cases_count=disease.cases_count or 0,
        created_at=disease.created_at,
        updated_at=disease.updated_at
    )


@router.delete("/{disease_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_disease(
    disease_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete disease (soft delete)"""
    disease = db.query(Disease).filter(
        Disease.id == disease_id,
        Disease.deleted_at.is_(None)
    ).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    disease.deleted_at = datetime.utcnow()
    disease.updated_at = datetime.utcnow()

    db.commit()

    return None
