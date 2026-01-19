"""
FILE: backend/src/schemas/inventory.py
PURPOSE: Inventory Pydantic schemas
OWNER: Backend Team
LAST-AUDITED: 2026-01-19
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .common import BaseSchema, TimestampMixin


class InventoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    item_type: str = Field(..., pattern="^(seed|fertilizer|pesticide|tool|fuel|feed|medicine|other)$")
    sku: Optional[str] = None
    quantity: float = Field(..., ge=0)
    unit: str = Field(default="kg", max_length=20)
    unit_price: Optional[float] = Field(None, ge=0)
    total_value: Optional[float] = None
    min_quantity: Optional[float] = Field(None, ge=0)
    max_quantity: Optional[float] = None
    location: Optional[str] = None
    supplier: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class InventoryCreate(InventoryBase):
    farm_id: int


class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    item_type: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    min_quantity: Optional[float] = None
    max_quantity: Optional[float] = None
    location: Optional[str] = None
    supplier: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None


class InventoryInDB(InventoryBase, TimestampMixin, BaseSchema):
    id: int
    farm_id: int


class InventoryResponse(InventoryInDB):
    farm_name: Optional[str] = None
    is_low_stock: bool = False
    is_expired: bool = False
    days_until_expiry: Optional[int] = None


class InventoryListResponse(BaseModel):
    items: List[InventoryResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class InventoryAdjustment(BaseModel):
    quantity_change: float
    reason: str = Field(..., max_length=500)
    adjustment_type: str = Field(..., pattern="^(add|remove|correction|loss|transfer)$")


class InventoryStats(BaseModel):
    total_items: int
    total_value: float
    low_stock_items: int
    expiring_soon: int
    by_type: dict


__all__ = ['InventoryBase', 'InventoryCreate', 'InventoryUpdate', 'InventoryInDB', 'InventoryResponse', 'InventoryListResponse', 'InventoryAdjustment', 'InventoryStats']
