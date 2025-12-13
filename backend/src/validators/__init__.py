# FILE: backend/src/validators/__init__.py | PURPOSE: Pydantic validators
# for API request/response validation | OWNER: Backend | RELATED:
# contracts/openapi.yaml | LAST-AUDITED: 2025-10-27

"""
Pydantic Validators for API Request/Response Validation

This module provides Pydantic schemas for validating API requests and responses.
All schemas are aligned with the OpenAPI specification in contracts/openapi.yaml.

Usage:
    from src.validators import LoginRequestSchema, ProductCreateSchema

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        data = LoginRequestSchema(**request.json)
        # data is now validated and typed
"""

from .auth_validators import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
    RefreshResponseSchema,
    UserSchema,
)

from .mfa_validators import (
    MFASetupResponseSchema,
    MFAVerifyRequestSchema,
    MFADisableRequestSchema,
    MFASetupDataSchema,
)

from .product_validators import (
    ProductSchema,
    ProductCreateRequestSchema,
    ProductUpdateRequestSchema,
    ProductListResponseSchema,
    ProductResponseSchema,
)

from .common_validators import (
    SuccessResponseSchema,
    ErrorResponseSchema,
    PaginationSchema,
)

from .report_validators import (
    ReportType,
    ReportFormat,
    ReportStatus,
    ReportCreateRequest,
    ReportUpdateRequest,
    ReportResponse,
    ReportListResponse,
    ReportDownloadRequest,
    ReportScheduleRequest,
)

from .category_validators import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse,
    CategoryListResponse,
    CategoryTreeNode,
    CategoryBulkCreateRequest,
)

from .user_validators import (
    UserRole,
    UserStatus,
    UserCreateRequest,
    UserUpdateRequest,
    UserPasswordChangeRequest,
    UserResponse,
    UserListResponse,
    UserPermissionRequest,
    UserRoleChangeRequest,
)

from .supplier_validators import (
    SupplierStatus,
    SupplierCreateRequest,
    SupplierUpdateRequest,
    SupplierResponse,
    SupplierListResponse,
)

from .invoice_validators import (
    InvoiceStatus,
    PaymentMethod,
    InvoiceLineItem,
    InvoiceCreateRequest,
    InvoiceUpdateRequest,
    InvoiceResponse,
    InvoiceListResponse,
    InvoicePaymentRequest,
)

__all__ = [
    # Auth
    "LoginRequestSchema",
    "LoginResponseSchema",
    "RefreshRequestSchema",
    "RefreshResponseSchema",
    "UserSchema",
    # MFA
    "MFASetupResponseSchema",
    "MFASetupDataSchema",
    "MFAVerifyRequestSchema",
    "MFADisableRequestSchema",
    # Products
    "ProductSchema",
    "ProductCreateRequestSchema",
    "ProductUpdateRequestSchema",
    "ProductListResponseSchema",
    "ProductResponseSchema",
    # Reports
    "ReportType",
    "ReportFormat",
    "ReportStatus",
    "ReportCreateRequest",
    "ReportUpdateRequest",
    "ReportResponse",
    "ReportListResponse",
    "ReportDownloadRequest",
    "ReportScheduleRequest",
    # Categories
    "CategoryCreateRequest",
    "CategoryUpdateRequest",
    "CategoryResponse",
    "CategoryListResponse",
    "CategoryTreeNode",
    "CategoryBulkCreateRequest",
    # Users
    "UserRole",
    "UserStatus",
    "UserCreateRequest",
    "UserUpdateRequest",
    "UserPasswordChangeRequest",
    "UserResponse",
    "UserListResponse",
    "UserPermissionRequest",
    "UserRoleChangeRequest",
    # Suppliers
    "SupplierStatus",
    "SupplierCreateRequest",
    "SupplierUpdateRequest",
    "SupplierResponse",
    "SupplierListResponse",
    # Invoices
    "InvoiceStatus",
    "PaymentMethod",
    "InvoiceLineItem",
    "InvoiceCreateRequest",
    "InvoiceUpdateRequest",
    "InvoiceResponse",
    "InvoiceListResponse",
    "InvoicePaymentRequest",
    # Common
    "SuccessResponseSchema",
    "ErrorResponseSchema",
    "PaginationSchema",
]
