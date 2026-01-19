#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نماذج وحدة المخزون لنظام Gaara ERP
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

# ===================== النماذج الأساسية =====================

class WarehouseBase(BaseModel):
    """النموذج الأساسي للمستودع"""
    code: str
    name: str
    location: Optional[str] = None
    manager_id: Optional[int] = None
    is_active: bool = True
    branch_id: Optional[int] = None

class WarehouseCreate(WarehouseBase):
    """نموذج إنشاء مستودع جديد"""
    company_id: int

class WarehouseUpdate(BaseModel):
    """نموذج تحديث مستودع"""
    code: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    manager_id: Optional[int] = None
    is_active: Optional[bool] = None
    branch_id: Optional[int] = None

class Warehouse(WarehouseBase):
    """نموذج المستودع الكامل"""
    id: int
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True

# ===================== نماذج فئات المنتجات =====================

class ProductCategoryBase(BaseModel):
    """النموذج الأساسي لفئة المنتجات"""
    code: str
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True

class ProductCategoryCreate(ProductCategoryBase):
    """نموذج إنشاء فئة منتجات جديدة"""
    company_id: int

class ProductCategoryUpdate(BaseModel):
    """نموذج تحديث فئة منتجات"""
    code: Optional[str] = None
    name: Optional[str] = None
    parent_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ProductCategory(ProductCategoryBase):
    """نموذج فئة المنتجات الكامل"""
    id: int
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    subcategories: Optional[List['ProductCategory']] = None

    class Config:
        orm_mode = True

# ===================== نماذج وحدات القياس =====================

class UnitOfMeasureBase(BaseModel):
    """النموذج الأساسي لوحدة القياس"""
    code: str
    name: str
    symbol: Optional[str] = None
    is_base_unit: bool = False
    base_unit_id: Optional[int] = None
    conversion_factor: Decimal = Decimal('1.0')
    is_active: bool = True

class UnitOfMeasureCreate(UnitOfMeasureBase):
    """نموذج إنشاء وحدة قياس جديدة"""
    company_id: int

class UnitOfMeasureUpdate(BaseModel):
    """نموذج تحديث وحدة قياس"""
    code: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    is_base_unit: Optional[bool] = None
    base_unit_id: Optional[int] = None
    conversion_factor: Optional[Decimal] = None
    is_active: Optional[bool] = None

class UnitOfMeasure(UnitOfMeasureBase):
    """نموذج وحدة القياس الكامل"""
    id: int
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True

# ===================== نماذج المنتجات =====================

class ProductBase(BaseModel):
    """النموذج الأساسي للمنتج"""
    code: str
    barcode: Optional[str] = None
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    base_unit_id: int
    purchase_unit_id: Optional[int] = None
    sales_unit_id: Optional[int] = None
    inventory_unit_id: Optional[int] = None
    cost_price: Decimal = Decimal('0.0')
    selling_price: Decimal = Decimal('0.0')
    min_stock_level: Decimal = Decimal('0.0')
    max_stock_level: Decimal = Decimal('0.0')
    reorder_point: Decimal = Decimal('0.0')
    is_stockable: bool = True
    is_purchasable: bool = True
    is_sellable: bool = True
    is_active: bool = True
    tax_group_id: Optional[int] = None
    inventory_account_id: Optional[int] = None
    cogs_account_id: Optional[int] = None
    revenue_account_id: Optional[int] = None

class ProductCreate(ProductBase):
    """نموذج إنشاء منتج جديد"""
    company_id: int

class ProductUpdate(BaseModel):
    """نموذج تحديث منتج"""
    code: Optional[str] = None
    barcode: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    base_unit_id: Optional[int] = None
    purchase_unit_id: Optional[int] = None
    sales_unit_id: Optional[int] = None
    inventory_unit_id: Optional[int] = None
    cost_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None
    min_stock_level: Optional[Decimal] = None
    max_stock_level: Optional[Decimal] = None
    reorder_point: Optional[Decimal] = None
    is_stockable: Optional[bool] = None
    is_purchasable: Optional[bool] = None
    is_sellable: Optional[bool] = None
    is_active: Optional[bool] = None
    tax_group_id: Optional[int] = None
    inventory_account_id: Optional[int] = None
    cogs_account_id: Optional[int] = None
    revenue_account_id: Optional[int] = None

class Product(ProductBase):
    """نموذج المنتج الكامل"""
    id: int
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    category: Optional[ProductCategory] = None
    base_unit: Optional[UnitOfMeasure] = None
    purchase_unit: Optional[UnitOfMeasure] = None
    sales_unit: Optional[UnitOfMeasure] = None
    inventory_unit: Optional[UnitOfMeasure] = None

    class Config:
        orm_mode = True

# ===================== نماذج المخزون =====================

class InventoryBase(BaseModel):
    """النموذج الأساسي للمخزون"""
    product_id: int
    warehouse_id: int
    quantity_on_hand: Decimal = Decimal('0.0')
    quantity_reserved: Decimal = Decimal('0.0')
    last_cost_price: Decimal = Decimal('0.0')
    average_cost: Decimal = Decimal('0.0')
    last_count_date: Optional[datetime] = None

class InventoryCreate(InventoryBase):
    """نموذج إنشاء مخزون جديد"""
    company_id: int

class InventoryUpdate(BaseModel):
    """نموذج تحديث مخزون"""
    quantity_on_hand: Optional[Decimal] = None
    quantity_reserved: Optional[Decimal] = None
    last_cost_price: Optional[Decimal] = None
    average_cost: Optional[Decimal] = None
    last_count_date: Optional[datetime] = None

class Inventory(InventoryBase):
    """نموذج المخزون الكامل"""
    id: int
    quantity_available: Decimal
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    product: Optional[Product] = None
    warehouse: Optional[Warehouse] = None

    class Config:
        orm_mode = True

# ===================== نماذج حركات المخزون =====================

class InventoryTransactionBase(BaseModel):
    """النموذج الأساسي لحركة المخزون"""
    transaction_number: str
    transaction_date: datetime
    transaction_type: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    warehouse_id: int
    source_warehouse_id: Optional[int] = None
    notes: Optional[str] = None
    status: str = "draft"
    branch_id: Optional[int] = None

class InventoryTransactionCreate(InventoryTransactionBase):
    """نموذج إنشاء حركة مخزون جديدة"""
    company_id: int
    items: List[Dict[str, Any]]

class InventoryTransactionUpdate(BaseModel):
    """نموذج تحديث حركة مخزون"""
    transaction_date: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class InventoryTransaction(InventoryTransactionBase):
    """نموذج حركة المخزون الكامل"""
    id: int
    journal_entry_id: Optional[int] = None
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    posted_at: Optional[datetime] = None
    posted_by: Optional[int] = None
    items: List['InventoryTransactionItem'] = []
    warehouse: Optional[Warehouse] = None
    source_warehouse: Optional[Warehouse] = None

    class Config:
        orm_mode = True

class InventoryTransactionItemBase(BaseModel):
    """النموذج الأساسي لبند حركة المخزون"""
    product_id: int
    quantity: Decimal
    unit_id: int
    unit_cost: Decimal = Decimal('0.0')
    total_cost: Decimal = Decimal('0.0')
    lot_number: Optional[str] = None
    expiry_date: Optional[date] = None
    notes: Optional[str] = None

class InventoryTransactionItemCreate(InventoryTransactionItemBase):
    """نموذج إنشاء بند حركة مخزون جديد"""
    transaction_id: int
    company_id: int

class InventoryTransactionItem(InventoryTransactionItemBase):
    """نموذج بند حركة المخزون الكامل"""
    id: int
    transaction_id: int
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    product: Optional[Product] = None
    unit: Optional[UnitOfMeasure] = None

    class Config:
        orm_mode = True

# ===================== نماذج الجرد =====================

class InventoryCountBase(BaseModel):
    """النموذج الأساسي للجرد"""
    count_number: str
    count_date: datetime
    warehouse_id: int
    status: str = "draft"
    notes: Optional[str] = None
    branch_id: Optional[int] = None

class InventoryCountCreate(InventoryCountBase):
    """نموذج إنشاء جرد جديد"""
    company_id: int

class InventoryCountUpdate(BaseModel):
    """نموذج تحديث جرد"""
    count_date: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class InventoryCount(InventoryCountBase):
    """نموذج الجرد الكامل"""
    id: int
    adjustment_transaction_id: Optional[int] = None
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    completed_at: Optional[datetime] = None
    completed_by: Optional[int] = None
    posted_at: Optional[datetime] = None
    posted_by: Optional[int] = None
    items: List['InventoryCountItem'] = []
    warehouse: Optional[Warehouse] = None

    class Config:
        orm_mode = True

class InventoryCountItemBase(BaseModel):
    """النموذج الأساسي لبند الجرد"""
    product_id: int
    expected_quantity: Decimal = Decimal('0.0')
    actual_quantity: Optional[Decimal] = None
    unit_id: int
    unit_cost: Decimal = Decimal('0.0')
    notes: Optional[str] = None

class InventoryCountItemCreate(InventoryCountItemBase):
    """نموذج إنشاء بند جرد جديد"""
    count_id: int
    company_id: int

class InventoryCountItemUpdate(BaseModel):
    """نموذج تحديث بند جرد"""
    actual_quantity: Decimal
    notes: Optional[str] = None

class InventoryCountItem(InventoryCountItemBase):
    """نموذج بند الجرد الكامل"""
    id: int
    count_id: int
    variance: Decimal
    variance_cost: Decimal
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    product: Optional[Product] = None
    unit: Optional[UnitOfMeasure] = None

    class Config:
        orm_mode = True

# ===================== نماذج أوامر الشراء =====================

class PurchaseOrderBase(BaseModel):
    """النموذج الأساسي لأمر الشراء"""
    order_number: str
    order_date: datetime
    supplier_id: int
    warehouse_id: int
    expected_delivery_date: Optional[date] = None
    currency_id: int
    exchange_rate: Decimal = Decimal('1.0')
    subtotal: Decimal = Decimal('0.0')
    tax_amount: Decimal = Decimal('0.0')
    discount_amount: Decimal = Decimal('0.0')
    total_amount: Decimal = Decimal('0.0')
    status: str = "draft"
    notes: Optional[str] = None
    payment_terms: Optional[str] = None
    shipping_terms: Optional[str] = None
    branch_id: Optional[int] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    """نموذج إنشاء أمر شراء جديد"""
    company_id: int
    items: List[Dict[str, Any]]

class PurchaseOrderUpdate(BaseModel):
    """نموذج تحديث أمر شراء"""
    order_date: Optional[datetime] = None
    expected_delivery_date: Optional[date] = None
    exchange_rate: Optional[Decimal] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None
    shipping_terms: Optional[str] = None
    status: Optional[str] = None

class PurchaseOrder(PurchaseOrderBase):
    """نموذج أمر الشراء الكامل"""
    id: int
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    items: List['PurchaseOrderItem'] = []

    class Config:
        orm_mode = True

class PurchaseOrderItemBase(BaseModel):
    """النموذج الأساسي لبند أمر الشراء"""
    product_id: int
    description: Optional[str] = None
    quantity: Decimal
    unit_id: int
    unit_price: Decimal
    tax_rate: Decimal = Decimal('0.0')
    tax_amount: Decimal = Decimal('0.0')
    discount_rate: Decimal = Decimal('0.0')
    discount_amount: Decimal = Decimal('0.0')
    total_amount: Decimal = Decimal('0.0')

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    """نموذج إنشاء بند أمر شراء جديد"""
    order_id: int
    company_id: int

class PurchaseOrderItemUpdate(BaseModel):
    """نموذج تحديث بند أمر شراء"""
    description: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    discount_rate: Optional[Decimal] = None

class PurchaseOrderItem(PurchaseOrderItemBase):
    """نموذج بند أمر الشراء الكامل"""
    id: int
    order_id: int
    received_quantity: Decimal = Decimal('0.0')
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    product: Optional[Product] = None
    unit: Optional[UnitOfMeasure] = None

    class Config:
        orm_mode = True

# ===================== نماذج التكامل مع النظام الزراعي =====================

class AgriculturalInventoryIntegrationBase(BaseModel):
    """النموذج الأساسي للتكامل مع النظام الزراعي"""
    agricultural_product_id: int
    erp_product_id: int
    sync_status: str = "pending"
    error_message: Optional[str] = None

class AgriculturalInventoryIntegrationCreate(AgriculturalInventoryIntegrationBase):
    """نموذج إنشاء تكامل جديد مع النظام الزراعي"""
    company_id: int

class AgriculturalInventoryIntegrationUpdate(BaseModel):
    """نموذج تحديث تكامل مع النظام الزراعي"""
    erp_product_id: Optional[int] = None
    sync_status: Optional[str] = None
    error_message: Optional[str] = None

class AgriculturalInventoryIntegration(AgriculturalInventoryIntegrationBase):
    """نموذج التكامل مع النظام الزراعي الكامل"""
    id: int
    last_sync_date: Optional[datetime] = None
    company_id: int
    created_at: datetime
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    product: Optional[Product] = None

    class Config:
        orm_mode = True
