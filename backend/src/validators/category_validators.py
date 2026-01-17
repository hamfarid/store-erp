# FILE: backend/src/validators/category_validators.py
# PURPOSE: Pydantic validators for Categories module
# OWNER: Gaara Store Team
# RELATED: contracts/openapi.yaml, backend/src/models/category.py
# LAST-AUDITED: 2025-10-27

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryCreateRequest(BaseModel):
    """Request to create a new category"""

    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    name_ar: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Category name in Arabic"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Category description"
    )
    description_ar: Optional[str] = Field(
        None, max_length=500, description="Category description in Arabic"
    )
    parent_id: Optional[str] = Field(
        None, description="Parent category ID for subcategories"
    )
    icon: Optional[str] = Field(
        None, max_length=100, description="Category icon URL or name"
    )
    color: Optional[str] = Field(
        None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Category color (hex)"
    )
    is_active: bool = Field(default=True, description="Is category active")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Electronics",
                "name_ar": "الإلكترونيات",
                "description": "Electronic products and devices",
                "description_ar": "المنتجات والأجهزة الإلكترونية",
                "icon": "electronics",
                "color": "#FF5733",
                "is_active": True,
            }
        }


class CategoryUpdateRequest(BaseModel):
    """Request to update a category"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_ar: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    description_ar: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {"name": "Updated Electronics", "color": "#FF5733"}
        }


class CategoryResponse(BaseModel):
    """Category response"""

    id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    name_ar: Optional[str] = Field(None, description="Category name in Arabic")
    description: Optional[str] = Field(None, description="Category description")
    description_ar: Optional[str] = Field(
        None, description="Category description in Arabic"
    )
    parent_id: Optional[str] = Field(None, description="Parent category ID")
    icon: Optional[str] = Field(None, description="Category icon")
    color: Optional[str] = Field(None, description="Category color")
    is_active: bool = Field(..., description="Is category active")
    product_count: int = Field(default=0, description="Number of products in category")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cat_123456",
                "name": "Electronics",
                "name_ar": "الإلكترونيات",
                "description": "Electronic products and devices",
                "description_ar": "المنتجات والأجهزة الإلكترونية",
                "icon": "electronics",
                "color": "#FF5733",
                "is_active": True,
                "product_count": 45,
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-15T15:30:00Z",
            }
        }


class CategoryListResponse(BaseModel):
    """List of categories response"""

    success: bool = Field(default=True)
    message: str = Field(default="Categories retrieved successfully")
    traceId: str = Field(..., description="Trace ID for debugging")
    data: Optional[dict] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Categories retrieved successfully",
                "traceId": "trace_123456",
                "data": {
                    "items": [],
                    "total": 0,
                    "page": 1,
                    "per_page": 10,
                    "pages": 0,
                },
            }
        }


class CategoryTreeNode(BaseModel):
    """Category tree node for hierarchical display"""

    id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    name_ar: Optional[str] = Field(None, description="Category name in Arabic")
    icon: Optional[str] = Field(None, description="Category icon")
    color: Optional[str] = Field(None, description="Category color")
    product_count: int = Field(default=0, description="Number of products")
    children: List["CategoryTreeNode"] = Field(
        default_factory=list, description="Subcategories"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cat_123456",
                "name": "Electronics",
                "name_ar": "الإلكترونيات",
                "icon": "electronics",
                "color": "#FF5733",
                "product_count": 45,
                "children": [],
            }
        }


CategoryTreeNode.model_rebuild()


class CategoryBulkCreateRequest(BaseModel):
    """Request to create multiple categories"""

    categories: List[CategoryCreateRequest] = Field(..., min_items=1, max_items=100)

    class Config:
        json_schema_extra = {
            "example": {
                "categories": [
                    {
                        "name": "Electronics",
                        "name_ar": "الإلكترونيات",
                        "is_active": True,
                    },
                    {"name": "Clothing", "name_ar": "الملابس", "is_active": True},
                ]
            }
        }
