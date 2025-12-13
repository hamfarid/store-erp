# FILE: backend/src/validators/invoice_validators.py
# PURPOSE: Pydantic validators for Invoices module
# OWNER: Gaara Store Team
# RELATED: contracts/openapi.yaml, backend/src/models/invoice.py
# LAST-AUDITED: 2025-10-27

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class InvoiceStatus(str, Enum):
    """Invoice status enumeration"""

    DRAFT = "draft"
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Payment method enumeration"""

    CASH = "cash"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    OTHER = "other"


class InvoiceLineItem(BaseModel):
    """Invoice line item"""

    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    quantity: float = Field(..., gt=0, description="Quantity")
    unit_price: float = Field(..., gt=0, description="Unit price")
    discount_percent: float = Field(
        default=0.0, ge=0, le=100, description="Discount percentage"
    )
    tax_percent: float = Field(default=0.0, ge=0, le=100, description="Tax percentage")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod_123",
                "product_name": "Laptop",
                "quantity": 2,
                "unit_price": 1000.00,
                "discount_percent": 10.0,
                "tax_percent": 15.0,
            }
        }


class InvoiceCreateRequest(BaseModel):
    """Request to create a new invoice"""

    customer_id: str = Field(..., description="Customer ID")
    invoice_date: datetime = Field(..., description="Invoice date")
    due_date: datetime = Field(..., description="Due date")
    items: List[InvoiceLineItem] = Field(
        ..., min_items=1, description="Invoice line items"
    )
    notes: Optional[str] = Field(None, max_length=500, description="Invoice notes")
    payment_method: Optional[PaymentMethod] = None
    discount_percent: float = Field(
        default=0.0, ge=0, le=100, description="Overall discount"
    )
    tax_percent: float = Field(default=0.0, ge=0, le=100, description="Overall tax")

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "cust_123",
                "invoice_date": "2025-01-15T00:00:00Z",
                "due_date": "2025-02-15T00:00:00Z",
                "items": [
                    {
                        "product_id": "prod_123",
                        "product_name": "Laptop",
                        "quantity": 2,
                        "unit_price": 1000.00,
                        "discount_percent": 10.0,
                        "tax_percent": 15.0,
                    }
                ],
                "notes": "Thank you for your business",
                "discount_percent": 5.0,
                "tax_percent": 15.0,
            }
        }


class InvoiceUpdateRequest(BaseModel):
    """Request to update an invoice"""

    due_date: Optional[datetime] = None
    items: Optional[List[InvoiceLineItem]] = None
    notes: Optional[str] = Field(None, max_length=500)
    payment_method: Optional[PaymentMethod] = None
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    tax_percent: Optional[float] = Field(None, ge=0, le=100)

    class Config:
        json_schema_extra = {
            "example": {"due_date": "2025-02-20T00:00:00Z", "notes": "Updated notes"}
        }


class InvoiceResponse(BaseModel):
    """Invoice response"""

    id: str = Field(..., description="Invoice ID")
    invoice_number: str = Field(..., description="Invoice number")
    customer_id: str = Field(..., description="Customer ID")
    customer_name: str = Field(..., description="Customer name")
    invoice_date: datetime = Field(..., description="Invoice date")
    due_date: datetime = Field(..., description="Due date")
    status: InvoiceStatus = Field(..., description="Invoice status")
    items: List[InvoiceLineItem] = Field(..., description="Line items")
    subtotal: float = Field(..., ge=0, description="Subtotal")
    discount_amount: float = Field(default=0.0, ge=0, description="Discount amount")
    tax_amount: float = Field(default=0.0, ge=0, description="Tax amount")
    total: float = Field(..., ge=0, description="Total amount")
    paid_amount: float = Field(default=0.0, ge=0, description="Paid amount")
    remaining_amount: float = Field(..., ge=0, description="Remaining amount")
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "inv_123456",
                "invoice_number": "INV-2025-001",
                "customer_id": "cust_123",
                "customer_name": "Ahmed Al-Rashid",
                "invoice_date": "2025-01-15T00:00:00Z",
                "due_date": "2025-02-15T00:00:00Z",
                "status": "pending",
                "items": [],
                "subtotal": 2000.00,
                "discount_amount": 100.00,
                "tax_amount": 285.00,
                "total": 2185.00,
                "paid_amount": 0.00,
                "remaining_amount": 2185.00,
                "created_at": "2025-01-15T10:00:00Z",
                "updated_at": "2025-01-15T10:00:00Z",
            }
        }


class InvoiceListResponse(BaseModel):
    """List of invoices response"""

    success: bool = Field(default=True)
    message: str = Field(default="Invoices retrieved successfully")
    traceId: str = Field(..., description="Trace ID for debugging")
    data: Optional[dict] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Invoices retrieved successfully",
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


class InvoicePaymentRequest(BaseModel):
    """Request to record invoice payment"""

    amount: float = Field(..., gt=0, description="Payment amount")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    reference: Optional[str] = Field(
        None, max_length=100, description="Payment reference"
    )
    notes: Optional[str] = Field(None, max_length=500, description="Payment notes")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 2185.00,
                "payment_method": "bank_transfer",
                "reference": "TRF-2025-001",
                "notes": "Payment received",
            }
        }
