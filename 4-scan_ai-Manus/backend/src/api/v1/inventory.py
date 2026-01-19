"""
FILE: backend/src/api/v1/inventory.py | PURPOSE: Inventory API routes | OWNER: Backend Team | LAST-AUDITED: 2025-12-19

Inventory Management API Routes

Handles CRUD operations for inventory items.

Version: 1.1.0
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, field_validator
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.inventory import Inventory
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


# Pydantic Schemas
class InventoryCreate(BaseModel):
    name: str
    category: str  # seeds, fertilizers, pesticides, tools, fuel, parts, other
    sku: Optional[str] = None
    quantity: float
    unit: str = "kg"  # kg, g, l, ml, pcs, box, bag
    min_quantity: Optional[float] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    location: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    min_quantity: Optional[float] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    location: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class InventoryResponse(BaseModel):
    id: int
    name: str
    category: str
    sku: Optional[str] = None
    quantity: float
    unit: str
    min_quantity: Optional[float] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    location: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None
    is_low_stock: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @field_validator('is_low_stock', mode='before')
    @classmethod
    def set_is_low_stock(cls, v):
        """Handle None value for is_low_stock"""
        if v is None:
            return False
        return v


class InventoryListResponse(BaseModel):
    success: bool = True
    data: List[InventoryResponse]
    total: int
    low_stock_count: int = 0


# Routes
@router.get("", response_model=InventoryListResponse)
async def get_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    low_stock: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of inventory items with pagination and filtering"""
    query = db.query(Inventory).filter(Inventory.deleted_at.is_(None))

    # Apply filters
    if category:
        query = query.filter(Inventory.category == category)

    if low_stock:
        query = query.filter(
            Inventory.min_quantity.isnot(None),
            Inventory.quantity <= Inventory.min_quantity
        )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Inventory.name.ilike(search_term),
                Inventory.sku.ilike(search_term),
                Inventory.supplier.ilike(search_term)
            )
        )

    total = query.count()

    # Count low stock items
    low_stock_query = db.query(Inventory).filter(
        Inventory.deleted_at.is_(None),
        Inventory.min_quantity.isnot(None),
        Inventory.quantity <= Inventory.min_quantity
    )
    low_stock_count = low_stock_query.count()

    items = query.order_by(Inventory.created_at.desc()).offset(skip).limit(limit).all()

    # Add is_low_stock flag to each item
    response_items = []
    for item in items:
        item_dict = {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "sku": item.sku,
            "quantity": item.quantity,
            "unit": item.unit,
            "min_quantity": item.min_quantity,
            "price": item.price,
            "supplier": item.supplier,
            "location": item.location,
            "expiry_date": item.expiry_date,
            "notes": item.notes,
            "is_low_stock": item.min_quantity and item.quantity <= item.min_quantity,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        }
        response_items.append(InventoryResponse(**item_dict))

    return InventoryListResponse(
        success=True,
        data=response_items,
        total=total,
        low_stock_count=low_stock_count
    )


@router.get("/{item_id}", response_model=InventoryResponse)
async def get_inventory_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get inventory item by ID"""
    item = db.query(Inventory).filter(
        Inventory.id == item_id,
        Inventory.deleted_at.is_(None)
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    return item


@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    item_data: InventoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new inventory item"""
    # Check for duplicate SKU
    if item_data.sku:
        existing = db.query(Inventory).filter(Inventory.sku == item_data.sku).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")

    new_item = Inventory(
        name=item_data.name,
        category=item_data.category,
        sku=item_data.sku,
        quantity=item_data.quantity,
        unit=item_data.unit,
        min_quantity=item_data.min_quantity,
        price=item_data.price,
        supplier=item_data.supplier,
        location=item_data.location,
        expiry_date=item_data.expiry_date,
        notes=item_data.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.put("/{item_id}", response_model=InventoryResponse)
async def update_inventory_item(
    item_id: int,
    item_data: InventoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update inventory item"""
    item = db.query(Inventory).filter(
        Inventory.id == item_id,
        Inventory.deleted_at.is_(None)
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    # Check SKU uniqueness if being updated
    if item_data.sku and item_data.sku != item.sku:
        existing = db.query(Inventory).filter(Inventory.sku == item_data.sku).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already in use")

    # Update fields
    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    item.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete inventory item (soft delete)"""
    item = db.query(Inventory).filter(
        Inventory.id == item_id,
        Inventory.deleted_at.is_(None)
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    item.deleted_at = datetime.utcnow()
    item.updated_at = datetime.utcnow()

    db.commit()

    return None
