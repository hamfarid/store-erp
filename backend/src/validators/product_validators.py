# FILE: backend/src/validators/product_validators.py | PURPOSE: Pydantic
# schemas for product endpoints | OWNER: Backend | RELATED:
# contracts/openapi.yaml | LAST-AUDITED: 2025-10-27

"""
Product Pydantic Validators

Provides schemas for product endpoints:
- ProductSchema: Product object validation
- ProductCreateRequestSchema: Product creation request
- ProductUpdateRequestSchema: Product update request
- ProductListResponseSchema: Product list response with pagination
- ProductResponseSchema: Single product response
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from .common_validators import PaginationSchema


class ProductSchema(BaseModel):
    """
    Product object schema

    Aligned with OpenAPI spec: #/components/schemas/Product
    """

    id: int = Field(..., ge=1, description="Product ID")
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    sku: str = Field(
        ..., min_length=1, max_length=100, description="Stock Keeping Unit"
    )
    barcode: Optional[str] = Field(None, max_length=100, description="Product barcode")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Selling price")
    cost: Optional[float] = Field(None, ge=0, description="Cost price")
    stock_quantity: int = Field(..., ge=0, description="Current stock quantity")
    min_stock_level: int = Field(0, ge=0, description="Minimum stock level for alerts")
    category_id: Optional[int] = Field(None, ge=1, description="Category ID")
    is_active: bool = Field(True, description="Product active status")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "منتج تجريبي",
                "sku": "PROD-001",
                "barcode": "1234567890123",
                "description": "وصف المنتج",
                "price": 99.99,
                "cost": 50.00,
                "stock_quantity": 100,
                "min_stock_level": 10,
                "category_id": 1,
                "is_active": True,
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
            }
        }


class ProductCreateRequestSchema(BaseModel):
    """
    Product creation request schema

    Aligned with OpenAPI spec: #/components/schemas/ProductCreateRequest
    """

    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    sku: str = Field(
        ..., min_length=1, max_length=100, description="Stock Keeping Unit"
    )
    barcode: Optional[str] = Field(None, max_length=100, description="Product barcode")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Selling price")
    cost: Optional[float] = Field(None, ge=0, description="Cost price")
    stock_quantity: int = Field(0, ge=0, description="Initial stock quantity")
    min_stock_level: int = Field(0, ge=0, description="Minimum stock level for alerts")
    category_id: Optional[int] = Field(None, ge=1, description="Category ID")
    is_active: bool = Field(True, description="Product active status")

    @field_validator("price", "cost")
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        """Validate that price/cost is non-negative"""
        if v is not None and v < 0:
            raise ValueError("Price/cost must be non-negative")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "منتج جديد",
                "sku": "PROD-002",
                "barcode": "1234567890124",
                "description": "وصف المنتج الجديد",
                "price": 149.99,
                "cost": 75.00,
                "stock_quantity": 50,
                "min_stock_level": 5,
                "category_id": 1,
                "is_active": True,
            }
        }


class ProductUpdateRequestSchema(BaseModel):
    """
    Product update request schema

    Aligned with OpenAPI spec: #/components/schemas/ProductUpdateRequest
    All fields are optional for partial updates
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Product name"
    )
    sku: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Stock Keeping Unit"
    )
    barcode: Optional[str] = Field(None, max_length=100, description="Product barcode")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[float] = Field(None, ge=0, description="Selling price")
    cost: Optional[float] = Field(None, ge=0, description="Cost price")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Stock quantity")
    min_stock_level: Optional[int] = Field(
        None, ge=0, description="Minimum stock level"
    )
    category_id: Optional[int] = Field(None, ge=1, description="Category ID")
    is_active: Optional[bool] = Field(None, description="Product active status")

    @field_validator("price", "cost")
    @classmethod
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        """Validate that price/cost is non-negative"""
        if v is not None and v < 0:
            raise ValueError("Price/cost must be non-negative")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "منتج محدث",
                "price": 159.99,
                "stock_quantity": 75,
                "is_active": True,
            }
        }


class ProductListDataSchema(BaseModel):
    """Product list data schema with pagination"""

    items: List[ProductSchema] = Field(..., description="List of products")
    total: int = Field(..., ge=0, description="Total number of products")
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, le=100, description="Items per page")
    pages: int = Field(..., ge=0, description="Total number of pages")


class ProductListResponseSchema(BaseModel):
    """
    Product list response schema

    Aligned with OpenAPI spec: #/components/schemas/ProductListResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: str = Field(..., description="Request trace ID")
    data: ProductListDataSchema = Field(..., description="Product list data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Products retrieved successfully",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "items": [
                        {
                            "id": 1,
                            "name": "منتج 1",
                            "sku": "PROD-001",
                            "price": 99.99,
                            "stock_quantity": 100,
                        }
                    ],
                    "total": 100,
                    "page": 1,
                    "per_page": 20,
                    "pages": 5,
                },
            }
        }


class ProductResponseSchema(BaseModel):
    """
    Single product response schema

    Aligned with OpenAPI spec: #/components/schemas/ProductResponse
    """

    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    traceId: str = Field(..., description="Request trace ID")
    data: ProductSchema = Field(..., description="Product data")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Product retrieved successfully",
                "traceId": "550e8400-e29b-41d4-a716-446655440000",
                "data": {
                    "id": 1,
                    "name": "منتج تجريبي",
                    "sku": "PROD-001",
                    "price": 99.99,
                    "stock_quantity": 100,
                },
            }
        }
