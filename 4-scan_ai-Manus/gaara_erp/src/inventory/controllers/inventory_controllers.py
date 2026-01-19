#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة تحكم المخزون لنظام Gaara ERP

هذه الوحدة تحتوي على واجهات API للتعامل مع عمليات المخزون
وتعمل كوسيط بين واجهة المستخدم وخدمات المخزون
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any

from ..services.inventory_services import InventoryService
from ..models.inventory_models import (
    Item, ItemCreate, ItemUpdate, 
    Warehouse, WarehouseCreate, WarehouseUpdate,
    StockMovement, StockMovementCreate,
    InventoryCount, InventoryCountCreate,
    ItemCategory, ItemCategoryCreate
)
from ....core.auth.auth_manager import get_current_user, check_permissions

# إعداد السجل
logger = logging.getLogger(__name__)

# إنشاء موجه API
router = APIRouter(prefix="/api/inventory", tags=["inventory"])

# إنشاء خدمة المخزون
inventory_service = InventoryService()

# ===================== واجهات API للأصناف =====================

@router.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """إنشاء صنف جديد في المخزون"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:create_item")
    
    try:
        # تسجيل العملية
        logger.info(f"إنشاء صنف جديد: {item.name} بواسطة المستخدم: {current_user['username']}")
        
        # إنشاء الصنف
        return inventory_service.create_item(item, current_user["id"])
    except Exception as e:
        logger.error(f"خطأ في إنشاء الصنف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء إنشاء الصنف: {str(e)}"
        )

@router.get("/items/", response_model=List[Item])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    warehouse_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على قائمة الأصناف مع إمكانية التصفية والبحث"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_items")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن الأصناف بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على الأصناف
        return inventory_service.get_items(
            skip=skip,
            limit=limit,
            category_id=category_id,
            warehouse_id=warehouse_id,
            search=search
        )
    except Exception as e:
        logger.error(f"خطأ في استعلام الأصناف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام الأصناف: {str(e)}"
        )

@router.get("/items/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على تفاصيل صنف محدد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_items")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن الصنف رقم {item_id} بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على الصنف
        item = inventory_service.get_item(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الصنف رقم {item_id} غير موجود"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في استعلام الصنف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام الصنف: {str(e)}"
        )

@router.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """تحديث بيانات صنف محدد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:update_item")
    
    try:
        # تسجيل العملية
        logger.info(f"تحديث الصنف رقم {item_id} بواسطة المستخدم: {current_user['username']}")
        
        # التحقق من وجود الصنف
        existing_item = inventory_service.get_item(item_id)
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الصنف رقم {item_id} غير موجود"
            )
        
        # تحديث الصنف
        return inventory_service.update_item(item_id, item_update, current_user["id"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في تحديث الصنف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء تحديث الصنف: {str(e)}"
        )

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """حذف صنف محدد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:delete_item")
    
    try:
        # تسجيل العملية
        logger.info(f"حذف الصنف رقم {item_id} بواسطة المستخدم: {current_user['username']}")
        
        # التحقق من وجود الصنف
        existing_item = inventory_service.get_item(item_id)
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الصنف رقم {item_id} غير موجود"
            )
        
        # حذف الصنف
        inventory_service.delete_item(item_id, current_user["id"])
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في حذف الصنف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء حذف الصنف: {str(e)}"
        )

# ===================== واجهات API للمستودعات =====================

@router.post("/warehouses/", response_model=Warehouse, status_code=status.HTTP_201_CREATED)
async def create_warehouse(
    warehouse: WarehouseCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """إنشاء مستودع جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:create_warehouse")
    
    try:
        # تسجيل العملية
        logger.info(f"إنشاء مستودع جديد: {warehouse.name} بواسطة المستخدم: {current_user['username']}")
        
        # إنشاء المستودع
        return inventory_service.create_warehouse(warehouse, current_user["id"])
    except Exception as e:
        logger.error(f"خطأ في إنشاء المستودع: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء إنشاء المستودع: {str(e)}"
        )

@router.get("/warehouses/", response_model=List[Warehouse])
async def get_warehouses(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على قائمة المستودعات مع إمكانية البحث"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_warehouses")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن المستودعات بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على المستودعات
        return inventory_service.get_warehouses(skip=skip, limit=limit, search=search)
    except Exception as e:
        logger.error(f"خطأ في استعلام المستودعات: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام المستودعات: {str(e)}"
        )

# ===================== واجهات API لحركات المخزون =====================

@router.post("/movements/", response_model=StockMovement, status_code=status.HTTP_201_CREATED)
async def create_stock_movement(
    movement: StockMovementCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """تسجيل حركة مخزون جديدة (استلام، صرف، تحويل)"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:create_movement")
    
    try:
        # تسجيل العملية
        logger.info(f"تسجيل حركة مخزون جديدة من نوع {movement.movement_type} بواسطة المستخدم: {current_user['username']}")
        
        # تسجيل حركة المخزون
        return inventory_service.create_stock_movement(movement, current_user["id"])
    except Exception as e:
        logger.error(f"خطأ في تسجيل حركة المخزون: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء تسجيل حركة المخزون: {str(e)}"
        )

@router.get("/movements/", response_model=List[StockMovement])
async def get_stock_movements(
    skip: int = 0,
    limit: int = 100,
    item_id: Optional[int] = None,
    warehouse_id: Optional[int] = None,
    movement_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على قائمة حركات المخزون مع إمكانية التصفية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_movements")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن حركات المخزون بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على حركات المخزون
        return inventory_service.get_stock_movements(
            skip=skip,
            limit=limit,
            item_id=item_id,
            warehouse_id=warehouse_id,
            movement_type=movement_type,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        logger.error(f"خطأ في استعلام حركات المخزون: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام حركات المخزون: {str(e)}"
        )

# ===================== واجهات API لجرد المخزون =====================

@router.post("/inventory-counts/", response_model=InventoryCount, status_code=status.HTTP_201_CREATED)
async def create_inventory_count(
    inventory_count: InventoryCountCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """إنشاء عملية جرد مخزون جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:create_inventory_count")
    
    try:
        # تسجيل العملية
        logger.info(f"إنشاء عملية جرد مخزون جديدة للمستودع {inventory_count.warehouse_id} بواسطة المستخدم: {current_user['username']}")
        
        # إنشاء عملية الجرد
        return inventory_service.create_inventory_count(inventory_count, current_user["id"])
    except Exception as e:
        logger.error(f"خطأ في إنشاء عملية جرد المخزون: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء إنشاء عملية جرد المخزون: {str(e)}"
        )

@router.get("/inventory-counts/", response_model=List[InventoryCount])
async def get_inventory_counts(
    skip: int = 0,
    limit: int = 100,
    warehouse_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على قائمة عمليات جرد المخزون مع إمكانية التصفية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_inventory_counts")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن عمليات جرد المخزون بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على عمليات الجرد
        return inventory_service.get_inventory_counts(
            skip=skip,
            limit=limit,
            warehouse_id=warehouse_id,
            status=status,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        logger.error(f"خطأ في استعلام عمليات جرد المخزون: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام عمليات جرد المخزون: {str(e)}"
        )

# ===================== واجهات API لفئات الأصناف =====================

@router.post("/categories/", response_model=ItemCategory, status_code=status.HTTP_201_CREATED)
async def create_item_category(
    category: ItemCategoryCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """إنشاء فئة أصناف جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:create_category")
    
    try:
        # تسجيل العملية
        logger.info(f"إنشاء فئة أصناف جديدة: {category.name} بواسطة المستخدم: {current_user['username']}")
        
        # إنشاء الفئة
        return inventory_service.create_item_category(category, current_user["id"])
    except Exception as e:
        logger.error(f"خطأ في إنشاء فئة الأصناف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء إنشاء فئة الأصناف: {str(e)}"
        )

@router.get("/categories/", response_model=List[ItemCategory])
async def get_item_categories(
    skip: int = 0,
    limit: int = 100,
    parent_id: Optional[int] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على قائمة فئات الأصناف مع إمكانية التصفية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_categories")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن فئات الأصناف بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على الفئات
        return inventory_service.get_item_categories(skip=skip, limit=limit, parent_id=parent_id)
    except Exception as e:
        logger.error(f"خطأ في استعلام فئات الأصناف: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام فئات الأصناف: {str(e)}"
        )

# ===================== واجهات API للتقارير =====================

@router.get("/reports/stock-status")
async def get_stock_status_report(
    warehouse_id: Optional[int] = None,
    category_id: Optional[int] = None,
    below_min_stock: Optional[bool] = False,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على تقرير حالة المخزون"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_reports")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن تقرير حالة المخزون بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على التقرير
        return inventory_service.get_stock_status_report(
            warehouse_id=warehouse_id,
            category_id=category_id,
            below_min_stock=below_min_stock
        )
    except Exception as e:
        logger.error(f"خطأ في استعلام تقرير حالة المخزون: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام تقرير حالة المخزون: {str(e)}"
        )

@router.get("/reports/movement-summary")
async def get_movement_summary_report(
    start_date: str,
    end_date: str,
    warehouse_id: Optional[int] = None,
    item_id: Optional[int] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على تقرير ملخص حركات المخزون"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_reports")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن تقرير ملخص حركات المخزون بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على التقرير
        return inventory_service.get_movement_summary_report(
            start_date=start_date,
            end_date=end_date,
            warehouse_id=warehouse_id,
            item_id=item_id
        )
    except Exception as e:
        logger.error(f"خطأ في استعلام تقرير ملخص حركات المخزون: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام تقرير ملخص حركات المخزون: {str(e)}"
        )

# ===================== واجهات API للتكامل مع النظام الزراعي =====================

@router.get("/integration/agricultural-items")
async def get_agricultural_items(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """الحصول على الأصناف من النظام الزراعي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:view_integration")
    
    try:
        # تسجيل العملية
        logger.info(f"استعلام عن الأصناف من النظام الزراعي بواسطة المستخدم: {current_user['username']}")
        
        # الحصول على الأصناف من النظام الزراعي
        return inventory_service.get_agricultural_items()
    except Exception as e:
        logger.error(f"خطأ في استعلام الأصناف من النظام الزراعي: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء استعلام الأصناف من النظام الزراعي: {str(e)}"
        )

@router.post("/integration/sync-agricultural-items")
async def sync_agricultural_items(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """مزامنة الأصناف مع النظام الزراعي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, "inventory:manage_integration")
    
    try:
        # تسجيل العملية
        logger.info(f"مزامنة الأصناف مع النظام الزراعي بواسطة المستخدم: {current_user['username']}")
        
        # مزامنة الأصناف مع النظام الزراعي
        result = inventory_service.sync_agricultural_items(current_user["id"])
        return {
            "message": "تمت مزامنة الأصناف مع النظام الزراعي بنجاح",
            "details": result
        }
    except Exception as e:
        logger.error(f"خطأ في مزامنة الأصناف مع النظام الزراعي: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء مزامنة الأصناف مع النظام الزراعي: {str(e)}"
        )
