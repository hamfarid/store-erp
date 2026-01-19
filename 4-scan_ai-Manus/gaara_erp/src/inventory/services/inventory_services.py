#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
خدمات وحدة المخزون لنظام Gaara ERP
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal

from ..models.inventory_models import (
    Warehouse, WarehouseCreate, WarehouseUpdate,
    ProductCategory, ProductCategoryCreate, ProductCategoryUpdate,
    UnitOfMeasure, UnitOfMeasureCreate, UnitOfMeasureUpdate,
    Product, ProductCreate, ProductUpdate,
    Inventory, InventoryCreate, InventoryUpdate,
    InventoryTransaction, InventoryTransactionCreate, InventoryTransactionUpdate,
    InventoryTransactionItem, InventoryTransactionItemCreate,
    InventoryCount, InventoryCountCreate, InventoryCountUpdate,
    InventoryCountItem, InventoryCountItemCreate, InventoryCountItemUpdate,
    PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate,
    PurchaseOrderItem, PurchaseOrderItemCreate,
    AgriculturalInventoryIntegration, AgriculturalInventoryIntegrationCreate
)
from ...core.database.db_manager import DatabaseManager
from ...accounts.services.accounting_services import JournalEntryService

logger = logging.getLogger(__name__)

class WarehouseService:
    """خدمة إدارة المستودعات"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_warehouse(self, warehouse: WarehouseCreate, user_id: int) -> Warehouse:
        """إنشاء مستودع جديد"""
        query = """
        INSERT INTO warehouses (code, name, location, manager_id, is_active, company_id, branch_id, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, code, name, location, manager_id, is_active, company_id, branch_id, created_at, created_by
        """
        params = (
            warehouse.code, warehouse.name, warehouse.location, warehouse.manager_id,
            warehouse.is_active, warehouse.company_id, warehouse.branch_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        return Warehouse(**result)
    
    def get_warehouses(self, company_id: int, is_active: bool = True) -> List[Warehouse]:
        """الحصول على قائمة المستودعات"""
        query = """
        SELECT id, code, name, location, manager_id, is_active, company_id, branch_id, 
               created_at, created_by, updated_at, updated_by
        FROM warehouses
        WHERE company_id = %s AND is_active = %s
        ORDER BY name
        """
        params = (company_id, is_active)
        results = self.db.execute_query(query, params)
        return [Warehouse(**row) for row in results]
    
    def get_warehouse_by_id(self, warehouse_id: int) -> Optional[Warehouse]:
        """الحصول على مستودع بواسطة المعرف"""
        query = """
        SELECT id, code, name, location, manager_id, is_active, company_id, branch_id, 
               created_at, created_by, updated_at, updated_by
        FROM warehouses
        WHERE id = %s
        """
        params = (warehouse_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result:
            return Warehouse(**result)
        return None
    
    def update_warehouse(self, warehouse_id: int, warehouse: WarehouseUpdate, user_id: int) -> Optional[Warehouse]:
        """تحديث مستودع"""
        # التحقق من وجود المستودع
        existing_warehouse = self.get_warehouse_by_id(warehouse_id)
        if not existing_warehouse:
            return None
        
        # بناء استعلام التحديث ديناميكيًا
        update_fields = []
        params = []
        
        if warehouse.code is not None:
            update_fields.append("code = %s")
            params.append(warehouse.code)
        
        if warehouse.name is not None:
            update_fields.append("name = %s")
            params.append(warehouse.name)
        
        if warehouse.location is not None:
            update_fields.append("location = %s")
            params.append(warehouse.location)
        
        if warehouse.manager_id is not None:
            update_fields.append("manager_id = %s")
            params.append(warehouse.manager_id)
        
        if warehouse.is_active is not None:
            update_fields.append("is_active = %s")
            params.append(warehouse.is_active)
        
        if warehouse.branch_id is not None:
            update_fields.append("branch_id = %s")
            params.append(warehouse.branch_id)
        
        if not update_fields:
            return existing_warehouse
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_by = %s")
        params.append(user_id)
        
        # إضافة معرف المستودع إلى المعلمات
        params.append(warehouse_id)
        
        query = f"""
        UPDATE warehouses
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING id, code, name, location, manager_id, is_active, company_id, branch_id, 
                 created_at, created_by, updated_at, updated_by
        """
        
        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        if result:
            return Warehouse(**result)
        return None
    
    def delete_warehouse(self, warehouse_id: int, user_id: int) -> bool:
        """حذف مستودع (تعطيل)"""
        query = """
        UPDATE warehouses
        SET is_active = FALSE, updated_at = %s, updated_by = %s
        WHERE id = %s
        RETURNING id
        """
        params = (datetime.now(), user_id, warehouse_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        return result is not None


class ProductCategoryService:
    """خدمة إدارة فئات المنتجات"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_category(self, category: ProductCategoryCreate, user_id: int) -> ProductCategory:
        """إنشاء فئة منتجات جديدة"""
        query = """
        INSERT INTO product_categories (code, name, parent_id, description, is_active, company_id, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, code, name, parent_id, description, is_active, company_id, created_at, created_by
        """
        params = (
            category.code, category.name, category.parent_id, category.description,
            category.is_active, category.company_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        return ProductCategory(**result)
    
    def get_categories(self, company_id: int, parent_id: Optional[int] = None, is_active: bool = True) -> List[ProductCategory]:
        """الحصول على قائمة فئات المنتجات"""
        if parent_id is None:
            query = """
            SELECT id, code, name, parent_id, description, is_active, company_id, 
                   created_at, created_by, updated_at, updated_by
            FROM product_categories
            WHERE company_id = %s AND is_active = %s
            ORDER BY name
            """
            params = (company_id, is_active)
        else:
            query = """
            SELECT id, code, name, parent_id, description, is_active, company_id, 
                   created_at, created_by, updated_at, updated_by
            FROM product_categories
            WHERE company_id = %s AND parent_id = %s AND is_active = %s
            ORDER BY name
            """
            params = (company_id, parent_id, is_active)
        
        results = self.db.execute_query(query, params)
        categories = [ProductCategory(**row) for row in results]
        
        # إضافة الفئات الفرعية لكل فئة
        for category in categories:
            if parent_id is None:  # نقوم بهذا فقط للفئات الرئيسية لتجنب الاستعلامات المتكررة
                subcategories = self.get_categories(company_id, category.id, is_active)
                category.subcategories = subcategories
        
        return categories
    
    def get_category_by_id(self, category_id: int) -> Optional[ProductCategory]:
        """الحصول على فئة منتجات بواسطة المعرف"""
        query = """
        SELECT id, code, name, parent_id, description, is_active, company_id, 
               created_at, created_by, updated_at, updated_by
        FROM product_categories
        WHERE id = %s
        """
        params = (category_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result:
            category = ProductCategory(**result)
            # إضافة الفئات الفرعية
            subcategories = self.get_categories(category.company_id, category.id)
            category.subcategories = subcategories
            return category
        return None
    
    def update_category(self, category_id: int, category: ProductCategoryUpdate, user_id: int) -> Optional[ProductCategory]:
        """تحديث فئة منتجات"""
        # التحقق من وجود الفئة
        existing_category = self.get_category_by_id(category_id)
        if not existing_category:
            return None
        
        # بناء استعلام التحديث ديناميكيًا
        update_fields = []
        params = []
        
        if category.code is not None:
            update_fields.append("code = %s")
            params.append(category.code)
        
        if category.name is not None:
            update_fields.append("name = %s")
            params.append(category.name)
        
        if category.parent_id is not None:
            # التحقق من عدم تعيين الفئة كفئة فرعية لنفسها
            if category.parent_id == category_id:
                raise ValueError("لا يمكن تعيين الفئة كفئة فرعية لنفسها")
            update_fields.append("parent_id = %s")
            params.append(category.parent_id)
        
        if category.description is not None:
            update_fields.append("description = %s")
            params.append(category.description)
        
        if category.is_active is not None:
            update_fields.append("is_active = %s")
            params.append(category.is_active)
        
        if not update_fields:
            return existing_category
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_by = %s")
        params.append(user_id)
        
        # إضافة معرف الفئة إلى المعلمات
        params.append(category_id)
        
        query = f"""
        UPDATE product_categories
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING id, code, name, parent_id, description, is_active, company_id, 
                 created_at, created_by, updated_at, updated_by
        """
        
        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        if result:
            category = ProductCategory(**result)
            # إضافة الفئات الفرعية
            subcategories = self.get_categories(category.company_id, category.id)
            category.subcategories = subcategories
            return category
        return None
    
    def delete_category(self, category_id: int, user_id: int) -> bool:
        """حذف فئة منتجات (تعطيل)"""
        # التحقق من عدم وجود فئات فرعية نشطة
        query = """
        SELECT COUNT(*) as count
        FROM product_categories
        WHERE parent_id = %s AND is_active = TRUE
        """
        params = (category_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result and result['count'] > 0:
            raise ValueError("لا يمكن حذف الفئة لأنها تحتوي على فئات فرعية نشطة")
        
        # التحقق من عدم وجود منتجات نشطة في هذه الفئة
        query = """
        SELECT COUNT(*) as count
        FROM products
        WHERE category_id = %s AND is_active = TRUE
        """
        result = self.db.execute_query(query, params, fetch_one=True)
        if result and result['count'] > 0:
            raise ValueError("لا يمكن حذف الفئة لأنها تحتوي على منتجات نشطة")
        
        # تعطيل الفئة
        query = """
        UPDATE product_categories
        SET is_active = FALSE, updated_at = %s, updated_by = %s
        WHERE id = %s
        RETURNING id
        """
        params = (datetime.now(), user_id, category_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        return result is not None


class UnitOfMeasureService:
    """خدمة إدارة وحدات القياس"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_unit(self, unit: UnitOfMeasureCreate, user_id: int) -> UnitOfMeasure:
        """إنشاء وحدة قياس جديدة"""
        # التحقق من صحة البيانات
        if unit.is_base_unit and unit.base_unit_id is not None:
            raise ValueError("الوحدة الأساسية لا يمكن أن يكون لها وحدة أساسية أخرى")
        
        if not unit.is_base_unit and unit.base_unit_id is None:
            raise ValueError("الوحدة غير الأساسية يجب أن يكون لها وحدة أساسية")
        
        query = """
        INSERT INTO units_of_measure (code, name, symbol, is_base_unit, base_unit_id, conversion_factor, is_active, company_id, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, code, name, symbol, is_base_unit, base_unit_id, conversion_factor, is_active, company_id, created_at, created_by
        """
        params = (
            unit.code, unit.name, unit.symbol, unit.is_base_unit, unit.base_unit_id,
            unit.conversion_factor, unit.is_active, unit.company_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        return UnitOfMeasure(**result)
    
    def get_units(self, company_id: int, is_base_unit: Optional[bool] = None, is_active: bool = True) -> List[UnitOfMeasure]:
        """الحصول على قائمة وحدات القياس"""
        if is_base_unit is None:
            query = """
            SELECT id, code, name, symbol, is_base_unit, base_unit_id, conversion_factor, is_active, company_id, 
                   created_at, created_by, updated_at, updated_by
            FROM units_of_measure
            WHERE company_id = %s AND is_active = %s
            ORDER BY name
            """
            params = (company_id, is_active)
        else:
            query = """
            SELECT id, code, name, symbol, is_base_unit, base_unit_id, conversion_factor, is_active, company_id, 
                   created_at, created_by, updated_at, updated_by
            FROM units_of_measure
            WHERE company_id = %s AND is_base_unit = %s AND is_active = %s
            ORDER BY name
            """
            params = (company_id, is_base_unit, is_active)
        
        results = self.db.execute_query(query, params)
        return [UnitOfMeasure(**row) for row in results]
    
    def get_unit_by_id(self, unit_id: int) -> Optional[UnitOfMeasure]:
        """الحصول على وحدة قياس بواسطة المعرف"""
        query = """
        SELECT id, code, name, symbol, is_base_unit, base_unit_id, conversion_factor, is_active, company_id, 
               created_at, created_by, updated_at, updated_by
        FROM units_of_measure
        WHERE id = %s
        """
        params = (unit_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result:
            return UnitOfMeasure(**result)
        return None
    
    def update_unit(self, unit_id: int, unit: UnitOfMeasureUpdate, user_id: int) -> Optional[UnitOfMeasure]:
        """تحديث وحدة قياس"""
        # التحقق من وجود الوحدة
        existing_unit = self.get_unit_by_id(unit_id)
        if not existing_unit:
            return None
        
        # التحقق من صحة البيانات
        is_base_unit = unit.is_base_unit if unit.is_base_unit is not None else existing_unit.is_base_unit
        base_unit_id = unit.base_unit_id if unit.base_unit_id is not None else existing_unit.base_unit_id
        
        if is_base_unit and base_unit_id is not None:
            raise ValueError("الوحدة الأساسية لا يمكن أن يكون لها وحدة أساسية أخرى")
        
        if not is_base_unit and base_unit_id is None:
            raise ValueError("الوحدة غير الأساسية يجب أن يكون لها وحدة أساسية")
        
        # بناء استعلام التحديث ديناميكيًا
        update_fields = []
        params = []
        
        if unit.code is not None:
            update_fields.append("code = %s")
            params.append(unit.code)
        
        if unit.name is not None:
            update_fields.append("name = %s")
            params.append(unit.name)
        
        if unit.symbol is not None:
            update_fields.append("symbol = %s")
            params.append(unit.symbol)
        
        if unit.is_base_unit is not None:
            update_fields.append("is_base_unit = %s")
            params.append(unit.is_base_unit)
        
        if unit.base_unit_id is not None:
            update_fields.append("base_unit_id = %s")
            params.append(unit.base_unit_id)
        
        if unit.conversion_factor is not None:
            update_fields.append("conversion_factor = %s")
            params.append(unit.conversion_factor)
        
        if unit.is_active is not None:
            update_fields.append("is_active = %s")
            params.append(unit.is_active)
        
        if not update_fields:
            return existing_unit
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_by = %s")
        params.append(user_id)
        
        # إضافة معرف الوحدة إلى المعلمات
        params.append(unit_id)
        
        query = f"""
        UPDATE units_of_measure
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING id, code, name, symbol, is_base_unit, base_unit_id, conversion_factor, is_active, company_id, 
                 created_at, created_by, updated_at, updated_by
        """
        
        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        if result:
            return UnitOfMeasure(**result)
        return None
    
    def delete_unit(self, unit_id: int, user_id: int) -> bool:
        """حذف وحدة قياس (تعطيل)"""
        # التحقق من عدم وجود وحدات أخرى تعتمد على هذه الوحدة
        query = """
        SELECT COUNT(*) as count
        FROM units_of_measure
        WHERE base_unit_id = %s AND is_active = TRUE
        """
        params = (unit_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result and result['count'] > 0:
            raise ValueError("لا يمكن حذف الوحدة لأنها مستخدمة كوحدة أساسية لوحدات أخرى")
        
        # التحقق من عدم وجود منتجات تستخدم هذه الوحدة
        query = """
        SELECT COUNT(*) as count
        FROM products
        WHERE (base_unit_id = %s OR purchase_unit_id = %s OR sales_unit_id = %s OR inventory_unit_id = %s) AND is_active = TRUE
        """
        params = (unit_id, unit_id, unit_id, unit_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result and result['count'] > 0:
            raise ValueError("لا يمكن حذف الوحدة لأنها مستخدمة في منتجات نشطة")
        
        # تعطيل الوحدة
        query = """
        UPDATE units_of_measure
        SET is_active = FALSE, updated_at = %s, updated_by = %s
        WHERE id = %s
        RETURNING id
        """
        params = (datetime.now(), user_id, unit_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        return result is not None


class ProductService:
    """خدمة إدارة المنتجات"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.category_service = ProductCategoryService()
        self.unit_service = UnitOfMeasureService()
    
    def create_product(self, product: ProductCreate, user_id: int) -> Product:
        """إنشاء منتج جديد"""
        query = """
        INSERT INTO products (
            code, barcode, name, description, category_id, base_unit_id, purchase_unit_id, sales_unit_id, inventory_unit_id,
            cost_price, selling_price, min_stock_level, max_stock_level, reorder_point, is_stockable, is_purchasable, is_sellable,
            is_active, tax_group_id, inventory_account_id, cogs_account_id, revenue_account_id, company_id, created_by
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, code, barcode, name, description, category_id, base_unit_id, purchase_unit_id, sales_unit_id, inventory_unit_id,
                 cost_price, selling_price, min_stock_level, max_stock_level, reorder_point, is_stockable, is_purchasable, is_sellable,
                 is_active, tax_group_id, inventory_account_id, cogs_account_id, revenue_account_id, company_id, created_at, created_by
        """
        params = (
            product.code, product.barcode, product.name, product.description, product.category_id,
            product.base_unit_id, product.purchase_unit_id, product.sales_unit_id, product.inventory_unit_id,
            product.cost_price, product.selling_price, product.min_stock_level, product.max_stock_level, product.reorder_point,
            product.is_stockable, product.is_purchasable, product.is_sellable, product.is_active,
            product.tax_group_id, product.inventory_account_id, product.cogs_account_id, product.revenue_account_id,
            product.company_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        product_obj = Product(**result)
        
        # إضافة معلومات إضافية
        if product_obj.category_id:
            product_obj.category = self.category_service.get_category_by_id(product_obj.category_id)
        
        if product_obj.base_unit_id:
            product_obj.base_unit = self.unit_service.get_unit_by_id(product_obj.base_unit_id)
        
        if product_obj.purchase_unit_id:
            product_obj.purchase_unit = self.unit_service.get_unit_by_id(product_obj.purchase_unit_id)
        
        if product_obj.sales_unit_id:
            product_obj.sales_unit = self.unit_service.get_unit_by_id(product_obj.sales_unit_id)
        
        if product_obj.inventory_unit_id:
            product_obj.inventory_unit = self.unit_service.get_unit_by_id(product_obj.inventory_unit_id)
        
        # إذا كان المنتج قابل للتخزين، قم بإنشاء سجلات المخزون لجميع المستودعات
        if product.is_stockable:
            warehouse_service = WarehouseService()
            warehouses = warehouse_service.get_warehouses(product.company_id)
            for warehouse in warehouses:
                inventory_create = InventoryCreate(
                    product_id=product_obj.id,
                    warehouse_id=warehouse.id,
                    company_id=product.company_id
                )
                self._create_inventory_record(inventory_create, user_id)
        
        return product_obj
    
    def _create_inventory_record(self, inventory: InventoryCreate, user_id: int) -> Inventory:
        """إنشاء سجل مخزون جديد"""
        query = """
        INSERT INTO inventory (product_id, warehouse_id, quantity_on_hand, quantity_reserved, last_cost_price, average_cost, company_id, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, product_id, warehouse_id, quantity_on_hand, quantity_reserved, quantity_available, last_cost_price, average_cost, last_count_date, company_id, created_at, created_by
        """
        params = (
            inventory.product_id, inventory.warehouse_id, inventory.quantity_on_hand, inventory.quantity_reserved,
            inventory.last_cost_price, inventory.average_cost, inventory.company_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        return Inventory(**result)
    
    def get_products(self, company_id: int, category_id: Optional[int] = None, is_active: bool = True) -> List[Product]:
        """الحصول على قائمة المنتجات"""
        if category_id is None:
            query = """
            SELECT id, code, barcode, name, description, category_id, base_unit_id, purchase_unit_id, sales_unit_id, inventory_unit_id,
                   cost_price, selling_price, min_stock_level, max_stock_level, reorder_point, is_stockable, is_purchasable, is_sellable,
                   is_active, tax_group_id, inventory_account_id, cogs_account_id, revenue_account_id, company_id, created_at, created_by, updated_at, updated_by
            FROM products
            WHERE company_id = %s AND is_active = %s
            ORDER BY name
            """
            params = (company_id, is_active)
        else:
            query = """
            SELECT id, code, barcode, name, description, category_id, base_unit_id, purchase_unit_id, sales_unit_id, inventory_unit_id,
                   cost_price, selling_price, min_stock_level, max_stock_level, reorder_point, is_stockable, is_purchasable, is_sellable,
                   is_active, tax_group_id, inventory_account_id, cogs_account_id, revenue_account_id, company_id, created_at, created_by, updated_at, updated_by
            FROM products
            WHERE company_id = %s AND category_id = %s AND is_active = %s
            ORDER BY name
            """
            params = (company_id, category_id, is_active)
        
        results = self.db.execute_query(query, params)
        products = []
        
        for row in results:
            product = Product(**row)
            
            # إضافة معلومات إضافية
            if product.category_id:
                product.category = self.category_service.get_category_by_id(product.category_id)
            
            if product.base_unit_id:
                product.base_unit = self.unit_service.get_unit_by_id(product.base_unit_id)
            
            if product.purchase_unit_id:
                product.purchase_unit = self.unit_service.get_unit_by_id(product.purchase_unit_id)
            
            if product.sales_unit_id:
                product.sales_unit = self.unit_service.get_unit_by_id(product.sales_unit_id)
            
            if product.inventory_unit_id:
                product.inventory_unit = self.unit_service.get_unit_by_id(product.inventory_unit_id)
            
            products.append(product)
        
        return products
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """الحصول على منتج بواسطة المعرف"""
        query = """
        SELECT id, code, barcode, name, description, category_id, base_unit_id, purchase_unit_id, sales_unit_id, inventory_unit_id,
               cost_price, selling_price, min_stock_level, max_stock_level, reorder_point, is_stockable, is_purchasable, is_sellable,
               is_active, tax_group_id, inventory_account_id, cogs_account_id, revenue_account_id, company_id, created_at, created_by, updated_at, updated_by
        FROM products
        WHERE id = %s
        """
        params = (product_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        
        if result:
            product = Product(**result)
            
            # إضافة معلومات إضافية
            if product.category_id:
                product.category = self.category_service.get_category_by_id(product.category_id)
            
            if product.base_unit_id:
                product.base_unit = self.unit_service.get_unit_by_id(product.base_unit_id)
            
            if product.purchase_unit_id:
                product.purchase_unit = self.unit_service.get_unit_by_id(product.purchase_unit_id)
            
            if product.sales_unit_id:
                product.sales_unit = self.unit_service.get_unit_by_id(product.sales_unit_id)
            
            if product.inventory_unit_id:
                product.inventory_unit = self.unit_service.get_unit_by_id(product.inventory_unit_id)
            
            return product
        
        return None
    
    def update_product(self, product_id: int, product: ProductUpdate, user_id: int) -> Optional[Product]:
        """تحديث منتج"""
        # التحقق من وجود المنتج
        existing_product = self.get_product_by_id(product_id)
        if not existing_product:
            return None
        
        # بناء استعلام التحديث ديناميكيًا
        update_fields = []
        params = []
        
        if product.code is not None:
            update_fields.append("code = %s")
            params.append(product.code)
        
        if product.barcode is not None:
            update_fields.append("barcode = %s")
            params.append(product.barcode)
        
        if product.name is not None:
            update_fields.append("name = %s")
            params.append(product.name)
        
        if product.description is not None:
            update_fields.append("description = %s")
            params.append(product.description)
        
        if product.category_id is not None:
            update_fields.append("category_id = %s")
            params.append(product.category_id)
        
        if product.base_unit_id is not None:
            update_fields.append("base_unit_id = %s")
            params.append(product.base_unit_id)
        
        if product.purchase_unit_id is not None:
            update_fields.append("purchase_unit_id = %s")
            params.append(product.purchase_unit_id)
        
        if product.sales_unit_id is not None:
            update_fields.append("sales_unit_id = %s")
            params.append(product.sales_unit_id)
        
        if product.inventory_unit_id is not None:
            update_fields.append("inventory_unit_id = %s")
            params.append(product.inventory_unit_id)
        
        if product.cost_price is not None:
            update_fields.append("cost_price = %s")
            params.append(product.cost_price)
        
        if product.selling_price is not None:
            update_fields.append("selling_price = %s")
            params.append(product.selling_price)
        
        if product.min_stock_level is not None:
            update_fields.append("min_stock_level = %s")
            params.append(product.min_stock_level)
        
        if product.max_stock_level is not None:
            update_fields.append("max_stock_level = %s")
            params.append(product.max_stock_level)
        
        if product.reorder_point is not None:
            update_fields.append("reorder_point = %s")
            params.append(product.reorder_point)
        
        if product.is_stockable is not None:
            update_fields.append("is_stockable = %s")
            params.append(product.is_stockable)
            
            # إذا تم تغيير المنتج ليكون قابل للتخزين، قم بإنشاء سجلات المخزون
            if product.is_stockable and not existing_product.is_stockable:
                warehouse_service = WarehouseService()
                warehouses = warehouse_service.get_warehouses(existing_product.company_id)
                for warehouse in warehouses:
                    inventory_create = InventoryCreate(
                        product_id=product_id,
                        warehouse_id=warehouse.id,
                        company_id=existing_product.company_id
                    )
                    self._create_inventory_record(inventory_create, user_id)
        
        if product.is_purchasable is not None:
            update_fields.append("is_purchasable = %s")
            params.append(product.is_purchasable)
        
        if product.is_sellable is not None:
            update_fields.append("is_sellable = %s")
            params.append(product.is_sellable)
        
        if product.is_active is not None:
            update_fields.append("is_active = %s")
            params.append(product.is_active)
        
        if product.tax_group_id is not None:
            update_fields.append("tax_group_id = %s")
            params.append(product.tax_group_id)
        
        if product.inventory_account_id is not None:
            update_fields.append("inventory_account_id = %s")
            params.append(product.inventory_account_id)
        
        if product.cogs_account_id is not None:
            update_fields.append("cogs_account_id = %s")
            params.append(product.cogs_account_id)
        
        if product.revenue_account_id is not None:
            update_fields.append("revenue_account_id = %s")
            params.append(product.revenue_account_id)
        
        if not update_fields:
            return existing_product
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_by = %s")
        params.append(user_id)
        
        # إضافة معرف المنتج إلى المعلمات
        params.append(product_id)
        
        query = f"""
        UPDATE products
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING id, code, barcode, name, description, category_id, base_unit_id, purchase_unit_id, sales_unit_id, inventory_unit_id,
                 cost_price, selling_price, min_stock_level, max_stock_level, reorder_point, is_stockable, is_purchasable, is_sellable,
                 is_active, tax_group_id, inventory_account_id, cogs_account_id, revenue_account_id, company_id, created_at, created_by, updated_at, updated_by
        """
        
        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        if result:
            product = Product(**result)
            
            # إضافة معلومات إضافية
            if product.category_id:
                product.category = self.category_service.get_category_by_id(product.category_id)
            
            if product.base_unit_id:
                product.base_unit = self.unit_service.get_unit_by_id(product.base_unit_id)
            
            if product.purchase_unit_id:
                product.purchase_unit = self.unit_service.get_unit_by_id(product.purchase_unit_id)
            
            if product.sales_unit_id:
                product.sales_unit = self.unit_service.get_unit_by_id(product.sales_unit_id)
            
            if product.inventory_unit_id:
                product.inventory_unit = self.unit_service.get_unit_by_id(product.inventory_unit_id)
            
            return product
        
        return None
    
    def delete_product(self, product_id: int, user_id: int) -> bool:
        """حذف منتج (تعطيل)"""
        # التحقق من عدم وجود حركات مخزون نشطة للمنتج
        query = """
        SELECT COUNT(*) as count
        FROM inventory_transaction_items iti
        JOIN inventory_transactions it ON iti.transaction_id = it.id
        WHERE iti.product_id = %s AND it.status != 'cancelled'
        """
        params = (product_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        if result and result['count'] > 0:
            raise ValueError("لا يمكن حذف المنتج لأنه مستخدم في حركات مخزون")
        
        # تعطيل المنتج
        query = """
        UPDATE products
        SET is_active = FALSE, updated_at = %s, updated_by = %s
        WHERE id = %s
        RETURNING id
        """
        params = (datetime.now(), user_id, product_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        return result is not None
    
    def get_product_inventory(self, product_id: int, warehouse_id: Optional[int] = None) -> List[Inventory]:
        """الحصول على مخزون المنتج"""
        if warehouse_id is None:
            query = """
            SELECT i.id, i.product_id, i.warehouse_id, i.quantity_on_hand, i.quantity_reserved, i.quantity_available,
                   i.last_cost_price, i.average_cost, i.last_count_date, i.company_id, i.created_at, i.created_by, i.updated_at, i.updated_by
            FROM inventory i
            WHERE i.product_id = %s
            """
            params = (product_id,)
        else:
            query = """
            SELECT i.id, i.product_id, i.warehouse_id, i.quantity_on_hand, i.quantity_reserved, i.quantity_available,
                   i.last_cost_price, i.average_cost, i.last_count_date, i.company_id, i.created_at, i.created_by, i.updated_at, i.updated_by
            FROM inventory i
            WHERE i.product_id = %s AND i.warehouse_id = %s
            """
            params = (product_id, warehouse_id)
        
        results = self.db.execute_query(query, params)
        inventory_list = []
        
        for row in results:
            inventory = Inventory(**row)
            
            # إضافة معلومات إضافية
            inventory.product = self.get_product_by_id(inventory.product_id)
            
            warehouse_service = WarehouseService()
            inventory.warehouse = warehouse_service.get_warehouse_by_id(inventory.warehouse_id)
            
            inventory_list.append(inventory)
        
        return inventory_list


class InventoryTransactionService:
    """خدمة إدارة حركات المخزون"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.product_service = ProductService()
        self.warehouse_service = WarehouseService()
        self.journal_service = JournalEntryService()
    
    def create_transaction(self, transaction: InventoryTransactionCreate, user_id: int) -> InventoryTransaction:
        """إنشاء حركة مخزون جديدة"""
        # بدء المعاملة
        self.db.begin_transaction()
        
        try:
            # إنشاء حركة المخزون
            query = """
            INSERT INTO inventory_transactions (
                transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                warehouse_id, source_warehouse_id, notes, status, company_id, branch_id, created_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                     warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                     created_at, created_by, updated_at, updated_by, posted_at, posted_by
            """
            params = (
                transaction.transaction_number, transaction.transaction_date, transaction.transaction_type,
                transaction.reference_type, transaction.reference_id, transaction.warehouse_id,
                transaction.source_warehouse_id, transaction.notes, transaction.status,
                transaction.company_id, transaction.branch_id, user_id
            )
            result = self.db.execute_query(query, params, fetch_one=True)
            transaction_obj = InventoryTransaction(**result)
            
            # إنشاء بنود حركة المخزون
            items = []
            for item_data in transaction.items:
                item_create = InventoryTransactionItemCreate(
                    transaction_id=transaction_obj.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_id=item_data['unit_id'],
                    unit_cost=item_data.get('unit_cost', Decimal('0.0')),
                    total_cost=item_data.get('total_cost', Decimal('0.0')),
                    lot_number=item_data.get('lot_number'),
                    expiry_date=item_data.get('expiry_date'),
                    notes=item_data.get('notes'),
                    company_id=transaction.company_id
                )
                item = self._create_transaction_item(item_create, user_id)
                items.append(item)
            
            transaction_obj.items = items
            
            # إضافة معلومات إضافية
            transaction_obj.warehouse = self.warehouse_service.get_warehouse_by_id(transaction_obj.warehouse_id)
            
            if transaction_obj.source_warehouse_id:
                transaction_obj.source_warehouse = self.warehouse_service.get_warehouse_by_id(transaction_obj.source_warehouse_id)
            
            # تأكيد المعاملة
            self.db.commit_transaction()
            
            return transaction_obj
        
        except Exception as e:
            # التراجع عن المعاملة في حالة حدوث خطأ
            self.db.rollback_transaction()
            logger.error(f"Error creating inventory transaction: {str(e)}")
            raise
    
    def _create_transaction_item(self, item: InventoryTransactionItemCreate, user_id: int) -> InventoryTransactionItem:
        """إنشاء بند حركة مخزون"""
        query = """
        INSERT INTO inventory_transaction_items (
            transaction_id, product_id, quantity, unit_id, unit_cost, total_cost,
            lot_number, expiry_date, notes, company_id, created_by
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, transaction_id, product_id, quantity, unit_id, unit_cost, total_cost,
                 lot_number, expiry_date, notes, company_id, created_at, created_by, updated_at, updated_by
        """
        params = (
            item.transaction_id, item.product_id, item.quantity, item.unit_id,
            item.unit_cost, item.total_cost, item.lot_number, item.expiry_date,
            item.notes, item.company_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        item_obj = InventoryTransactionItem(**result)
        
        # إضافة معلومات إضافية
        item_obj.product = self.product_service.get_product_by_id(item_obj.product_id)
        
        unit_service = UnitOfMeasureService()
        item_obj.unit = unit_service.get_unit_by_id(item_obj.unit_id)
        
        return item_obj
    
    def get_transactions(self, company_id: int, transaction_type: Optional[str] = None, status: Optional[str] = None) -> List[InventoryTransaction]:
        """الحصول على قائمة حركات المخزون"""
        if transaction_type is None and status is None:
            query = """
            SELECT id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                   warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                   created_at, created_by, updated_at, updated_by, posted_at, posted_by
            FROM inventory_transactions
            WHERE company_id = %s
            ORDER BY transaction_date DESC
            """
            params = (company_id,)
        elif transaction_type is not None and status is None:
            query = """
            SELECT id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                   warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                   created_at, created_by, updated_at, updated_by, posted_at, posted_by
            FROM inventory_transactions
            WHERE company_id = %s AND transaction_type = %s
            ORDER BY transaction_date DESC
            """
            params = (company_id, transaction_type)
        elif transaction_type is None and status is not None:
            query = """
            SELECT id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                   warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                   created_at, created_by, updated_at, updated_by, posted_at, posted_by
            FROM inventory_transactions
            WHERE company_id = %s AND status = %s
            ORDER BY transaction_date DESC
            """
            params = (company_id, status)
        else:
            query = """
            SELECT id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                   warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                   created_at, created_by, updated_at, updated_by, posted_at, posted_by
            FROM inventory_transactions
            WHERE company_id = %s AND transaction_type = %s AND status = %s
            ORDER BY transaction_date DESC
            """
            params = (company_id, transaction_type, status)
        
        results = self.db.execute_query(query, params)
        transactions = []
        
        for row in results:
            transaction = InventoryTransaction(**row)
            
            # إضافة معلومات إضافية
            transaction.warehouse = self.warehouse_service.get_warehouse_by_id(transaction.warehouse_id)
            
            if transaction.source_warehouse_id:
                transaction.source_warehouse = self.warehouse_service.get_warehouse_by_id(transaction.source_warehouse_id)
            
            # إضافة بنود الحركة
            transaction.items = self.get_transaction_items(transaction.id)
            
            transactions.append(transaction)
        
        return transactions
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[InventoryTransaction]:
        """الحصول على حركة مخزون بواسطة المعرف"""
        query = """
        SELECT id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
               warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
               created_at, created_by, updated_at, updated_by, posted_at, posted_by
        FROM inventory_transactions
        WHERE id = %s
        """
        params = (transaction_id,)
        result = self.db.execute_query(query, params, fetch_one=True)
        
        if result:
            transaction = InventoryTransaction(**result)
            
            # إضافة معلومات إضافية
            transaction.warehouse = self.warehouse_service.get_warehouse_by_id(transaction.warehouse_id)
            
            if transaction.source_warehouse_id:
                transaction.source_warehouse = self.warehouse_service.get_warehouse_by_id(transaction.source_warehouse_id)
            
            # إضافة بنود الحركة
            transaction.items = self.get_transaction_items(transaction.id)
            
            return transaction
        
        return None
    
    def get_transaction_items(self, transaction_id: int) -> List[InventoryTransactionItem]:
        """الحصول على بنود حركة مخزون"""
        query = """
        SELECT id, transaction_id, product_id, quantity, unit_id, unit_cost, total_cost,
               lot_number, expiry_date, notes, company_id, created_at, created_by, updated_at, updated_by
        FROM inventory_transaction_items
        WHERE transaction_id = %s
        """
        params = (transaction_id,)
        results = self.db.execute_query(query, params)
        items = []
        
        for row in results:
            item = InventoryTransactionItem(**row)
            
            # إضافة معلومات إضافية
            item.product = self.product_service.get_product_by_id(item.product_id)
            
            unit_service = UnitOfMeasureService()
            item.unit = unit_service.get_unit_by_id(item.unit_id)
            
            items.append(item)
        
        return items
    
    def update_transaction(self, transaction_id: int, transaction: InventoryTransactionUpdate, user_id: int) -> Optional[InventoryTransaction]:
        """تحديث حركة مخزون"""
        # التحقق من وجود الحركة
        existing_transaction = self.get_transaction_by_id(transaction_id)
        if not existing_transaction:
            return None
        
        # التحقق من أن الحركة لم يتم ترحيلها بعد
        if existing_transaction.status != 'draft':
            raise ValueError("لا يمكن تحديث حركة مخزون تم ترحيلها أو إلغاؤها")
        
        # بناء استعلام التحديث ديناميكيًا
        update_fields = []
        params = []
        
        if transaction.transaction_date is not None:
            update_fields.append("transaction_date = %s")
            params.append(transaction.transaction_date)
        
        if transaction.notes is not None:
            update_fields.append("notes = %s")
            params.append(transaction.notes)
        
        if transaction.status is not None:
            update_fields.append("status = %s")
            params.append(transaction.status)
        
        if not update_fields:
            return existing_transaction
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_by = %s")
        params.append(user_id)
        
        # إضافة معرف الحركة إلى المعلمات
        params.append(transaction_id)
        
        query = f"""
        UPDATE inventory_transactions
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                 warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                 created_at, created_by, updated_at, updated_by, posted_at, posted_by
        """
        
        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        if result:
            transaction = InventoryTransaction(**result)
            
            # إضافة معلومات إضافية
            transaction.warehouse = self.warehouse_service.get_warehouse_by_id(transaction.warehouse_id)
            
            if transaction.source_warehouse_id:
                transaction.source_warehouse = self.warehouse_service.get_warehouse_by_id(transaction.source_warehouse_id)
            
            # إضافة بنود الحركة
            transaction.items = self.get_transaction_items(transaction.id)
            
            return transaction
        
        return None
    
    def post_transaction(self, transaction_id: int, user_id: int) -> Optional[InventoryTransaction]:
        """ترحيل حركة مخزون"""
        # التحقق من وجود الحركة
        transaction = self.get_transaction_by_id(transaction_id)
        if not transaction:
            return None
        
        # التحقق من أن الحركة لم يتم ترحيلها بعد
        if transaction.status != 'draft':
            raise ValueError("لا يمكن ترحيل حركة مخزون تم ترحيلها أو إلغاؤها بالفعل")
        
        # بدء المعاملة
        self.db.begin_transaction()
        
        try:
            # تحديث المخزون بناءً على نوع الحركة
            if transaction.transaction_type == 'purchase':
                self._process_purchase_transaction(transaction)
            elif transaction.transaction_type == 'sale':
                self._process_sale_transaction(transaction)
            elif transaction.transaction_type == 'transfer':
                self._process_transfer_transaction(transaction)
            elif transaction.transaction_type == 'adjustment':
                self._process_adjustment_transaction(transaction)
            elif transaction.transaction_type == 'return':
                self._process_return_transaction(transaction)
            else:
                raise ValueError(f"نوع الحركة غير معروف: {transaction.transaction_type}")
            
            # إنشاء قيد محاسبي للحركة
            journal_entry_id = self._create_accounting_entry(transaction, user_id)
            
            # تحديث حالة الحركة إلى "مرحلة"
            query = """
            UPDATE inventory_transactions
            SET status = 'posted', posted_at = %s, posted_by = %s, journal_entry_id = %s
            WHERE id = %s
            RETURNING id, transaction_number, transaction_date, transaction_type, reference_type, reference_id,
                     warehouse_id, source_warehouse_id, notes, status, journal_entry_id, company_id, branch_id,
                     created_at, created_by, updated_at, updated_by, posted_at, posted_by
            """
            params = (datetime.now(), user_id, journal_entry_id, transaction_id)
            result = self.db.execute_query(query, params, fetch_one=True)
            
            # تأكيد المعاملة
            self.db.commit_transaction()
            
            if result:
                updated_transaction = InventoryTransaction(**result)
                
                # إضافة معلومات إضافية
                updated_transaction.warehouse = self.warehouse_service.get_warehouse_by_id(updated_transaction.warehouse_id)
                
                if updated_transaction.source_warehouse_id:
                    updated_transaction.source_warehouse = self.warehouse_service.get_warehouse_by_id(updated_transaction.source_warehouse_id)
                
                # إضافة بنود الحركة
                updated_transaction.items = self.get_transaction_items(updated_transaction.id)
                
                return updated_transaction
            
            return None
        
        except Exception as e:
            # التراجع عن المعاملة في حالة حدوث خطأ
            self.db.rollback_transaction()
            logger.error(f"Error posting inventory transaction: {str(e)}")
            raise
    
    def _process_purchase_transaction(self, transaction: InventoryTransaction) -> None:
        """معالجة حركة شراء"""
        for item in transaction.items:
            # تحديث المخزون
            self._update_inventory(
                product_id=item.product_id,
                warehouse_id=transaction.warehouse_id,
                quantity=item.quantity,
                cost=item.unit_cost,
                is_increase=True
            )
    
    def _process_sale_transaction(self, transaction: InventoryTransaction) -> None:
        """معالجة حركة بيع"""
        for item in transaction.items:
            # تحديث المخزون
            self._update_inventory(
                product_id=item.product_id,
                warehouse_id=transaction.warehouse_id,
                quantity=item.quantity,
                cost=item.unit_cost,
                is_increase=False
            )
    
    def _process_transfer_transaction(self, transaction: InventoryTransaction) -> None:
        """معالجة حركة تحويل"""
        if not transaction.source_warehouse_id:
            raise ValueError("يجب تحديد المستودع المصدر لحركة التحويل")
        
        for item in transaction.items:
            # تخفيض المخزون من المستودع المصدر
            self._update_inventory(
                product_id=item.product_id,
                warehouse_id=transaction.source_warehouse_id,
                quantity=item.quantity,
                cost=item.unit_cost,
                is_increase=False
            )
            
            # زيادة المخزون في المستودع الوجهة
            self._update_inventory(
                product_id=item.product_id,
                warehouse_id=transaction.warehouse_id,
                quantity=item.quantity,
                cost=item.unit_cost,
                is_increase=True
            )
    
    def _process_adjustment_transaction(self, transaction: InventoryTransaction) -> None:
        """معالجة حركة تسوية"""
        for item in transaction.items:
            # الحصول على الكمية الحالية في المخزون
            inventory = self._get_inventory(item.product_id, transaction.warehouse_id)
            if not inventory:
                raise ValueError(f"المنتج {item.product_id} غير موجود في المستودع {transaction.warehouse_id}")
            
            # حساب الفرق بين الكمية الحالية والكمية المطلوبة
            difference = item.quantity - inventory.quantity_on_hand
            
            # تحديث المخزون
            if difference != 0:
                self._update_inventory(
                    product_id=item.product_id,
                    warehouse_id=transaction.warehouse_id,
                    quantity=abs(difference),
                    cost=item.unit_cost,
                    is_increase=(difference > 0)
                )
    
    def _process_return_transaction(self, transaction: InventoryTransaction) -> None:
        """معالجة حركة مرتجع"""
        # المرتجعات يمكن أن تكون مرتجعات مبيعات (زيادة المخزون) أو مرتجعات مشتريات (تخفيض المخزون)
        is_sales_return = transaction.reference_type == 'sales_return'
        
        for item in transaction.items:
            # تحديث المخزون
            self._update_inventory(
                product_id=item.product_id,
                warehouse_id=transaction.warehouse_id,
                quantity=item.quantity,
                cost=item.unit_cost,
                is_increase=is_sales_return  # زيادة للمرتجعات المبيعات، تخفيض لمرتجعات المشتريات
            )
    
    def _update_inventory(self, product_id: int, warehouse_id: int, quantity: Decimal, cost: Decimal, is_increase: bool) -> None:
        """تحديث المخزون"""
        # الحصول على سجل المخزون
        inventory = self._get_inventory(product_id, warehouse_id)
        if not inventory:
            # إنشاء سجل مخزون جديد إذا لم يكن موجودًا
            product = self.product_service.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"المنتج {product_id} غير موجود")
            
            inventory_create = InventoryCreate(
                product_id=product_id,
                warehouse_id=warehouse_id,
                company_id=product.company_id
            )
            inventory = self.product_service._create_inventory_record(inventory_create, 1)  # استخدام معرف مستخدم النظام
        
        # حساب الكمية الجديدة والتكلفة المتوسطة الجديدة
        old_quantity = inventory.quantity_on_hand
        old_cost = inventory.average_cost
        
        if is_increase:
            # زيادة المخزون
            new_quantity = old_quantity + quantity
            
            # حساب التكلفة المتوسطة الجديدة
            if new_quantity > 0:
                new_cost = ((old_quantity * old_cost) + (quantity * cost)) / new_quantity
            else:
                new_cost = cost
            
            # تحديث المخزون
            query = """
            UPDATE inventory
            SET quantity_on_hand = %s, last_cost_price = %s, average_cost = %s, updated_at = %s
            WHERE product_id = %s AND warehouse_id = %s
            """
            params = (new_quantity, cost, new_cost, datetime.now(), product_id, warehouse_id)
        else:
            # تخفيض المخزون
            if old_quantity < quantity:
                raise ValueError(f"الكمية المتاحة ({old_quantity}) أقل من الكمية المطلوبة ({quantity})")
            
            new_quantity = old_quantity - quantity
            
            # تحديث المخزون
            query = """
            UPDATE inventory
            SET quantity_on_hand = %s, updated_at = %s
            WHERE product_id = %s AND warehouse_id = %s
            """
            params = (new_quantity, datetime.now(), product_id, warehouse_id)
        
        self.db.execute_query(query, params)
    
    def _get_inventory(self, product_id: int, warehouse_id: int) -> Optional[Inventory]:
        """الحصول على سجل المخزون"""
        query = """
        SELECT id, product_id, warehouse_id, quantity_on_hand, quantity_reserved, quantity_available,
               last_cost_price, average_cost, last_count_date, company_id, created_at, created_by, updated_at, updated_by
        FROM inventory
        WHERE product_id = %s AND warehouse_id = %s
        """
        params = (product_id, warehouse_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        
        if result:
            return Inventory(**result)
        
        return None
    
    def _create_accounting_entry(self, transaction: InventoryTransaction, user_id: int) -> int:
        """إنشاء قيد محاسبي للحركة"""
        # تنفيذ هذه الوظيفة بناءً على نوع الحركة ومتطلبات المحاسبة
        # هذه مجرد وظيفة وهمية، يجب تنفيذها بشكل صحيح في التطبيق الفعلي
        
        # في هذا المثال، نفترض أن لدينا خدمة قيود اليومية تقوم بإنشاء القيود المحاسبية
        # ونقوم بإنشاء قيد محاسبي بسيط للحركة
        
        # الحصول على الحسابات المحاسبية للمنتجات
        accounts = {}
        total_amount = Decimal('0.0')
        
        for item in transaction.items:
            product = self.product_service.get_product_by_id(item.product_id)
            if not product:
                continue
            
            # حساب المبلغ الإجمالي للبند
            amount = item.quantity * item.unit_cost
            total_amount += amount
            
            # تخزين معرفات الحسابات المحاسبية للمنتج
            if product.id not in accounts:
                accounts[product.id] = {
                    'inventory_account_id': product.inventory_account_id,
                    'cogs_account_id': product.cogs_account_id,
                    'revenue_account_id': product.revenue_account_id,
                    'amount': amount
                }
            else:
                accounts[product.id]['amount'] += amount
        
        # إنشاء قيد محاسبي وهمي
        # في التطبيق الفعلي، يجب إنشاء قيد محاسبي حقيقي باستخدام خدمة قيود اليومية
        
        # نفترض أن لدينا وظيفة تقوم بإنشاء قيد محاسبي وتعيد معرف القيد
        # journal_entry_id = self.journal_service.create_journal_entry(...)
        
        # في هذا المثال، نعيد قيمة وهمية
        return 1


class AgriculturalIntegrationService:
    """خدمة التكامل مع النظام الزراعي"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.product_service = ProductService()
    
    def create_integration(self, integration: AgriculturalInventoryIntegrationCreate, user_id: int) -> AgriculturalInventoryIntegration:
        """إنشاء تكامل جديد مع النظام الزراعي"""
        query = """
        INSERT INTO agricultural_inventory_integration (
            agricultural_product_id, erp_product_id, sync_status, error_message, company_id, created_by
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, agricultural_product_id, erp_product_id, last_sync_date, sync_status, error_message, company_id, created_at, created_by, updated_at, updated_by
        """
        params = (
            integration.agricultural_product_id, integration.erp_product_id,
            integration.sync_status, integration.error_message, integration.company_id, user_id
        )
        result = self.db.execute_query(query, params, fetch_one=True)
        integration_obj = AgriculturalInventoryIntegration(**result)
        
        # إضافة معلومات إضافية
        integration_obj.product = self.product_service.get_product_by_id(integration_obj.erp_product_id)
        
        return integration_obj
    
    def get_integrations(self, company_id: int, sync_status: Optional[str] = None) -> List[AgriculturalInventoryIntegration]:
        """الحصول على قائمة التكاملات مع النظام الزراعي"""
        if sync_status is None:
            query = """
            SELECT id, agricultural_product_id, erp_product_id, last_sync_date, sync_status, error_message, company_id, created_at, created_by, updated_at, updated_by
            FROM agricultural_inventory_integration
            WHERE company_id = %s
            ORDER BY agricultural_product_id
            """
            params = (company_id,)
        else:
            query = """
            SELECT id, agricultural_product_id, erp_product_id, last_sync_date, sync_status, error_message, company_id, created_at, created_by, updated_at, updated_by
            FROM agricultural_inventory_integration
            WHERE company_id = %s AND sync_status = %s
            ORDER BY agricultural_product_id
            """
            params = (company_id, sync_status)
        
        results = self.db.execute_query(query, params)
        integrations = []
        
        for row in results:
            integration = AgriculturalInventoryIntegration(**row)
            
            # إضافة معلومات إضافية
            integration.product = self.product_service.get_product_by_id(integration.erp_product_id)
            
            integrations.append(integration)
        
        return integrations
    
    def get_integration_by_agricultural_product_id(self, agricultural_product_id: int, company_id: int) -> Optional[AgriculturalInventoryIntegration]:
        """الحصول على تكامل بواسطة معرف المنتج الزراعي"""
        query = """
        SELECT id, agricultural_product_id, erp_product_id, last_sync_date, sync_status, error_message, company_id, created_at, created_by, updated_at, updated_by
        FROM agricultural_inventory_integration
        WHERE agricultural_product_id = %s AND company_id = %s
        """
        params = (agricultural_product_id, company_id)
        result = self.db.execute_query(query, params, fetch_one=True)
        
        if result:
            integration = AgriculturalInventoryIntegration(**result)
            
            # إضافة معلومات إضافية
            integration.product = self.product_service.get_product_by_id(integration.erp_product_id)
            
            return integration
        
        return None
    
    def update_integration(self, integration_id: int, integration: AgriculturalInventoryIntegrationUpdate, user_id: int) -> Optional[AgriculturalInventoryIntegration]:
        """تحديث تكامل مع النظام الزراعي"""
        # بناء استعلام التحديث ديناميكيًا
        update_fields = []
        params = []
        
        if integration.erp_product_id is not None:
            update_fields.append("erp_product_id = %s")
            params.append(integration.erp_product_id)
        
        if integration.sync_status is not None:
            update_fields.append("sync_status = %s")
            params.append(integration.sync_status)
        
        if integration.error_message is not None:
            update_fields.append("error_message = %s")
            params.append(integration.error_message)
        
        if not update_fields:
            # الحصول على التكامل الحالي
            query = """
            SELECT id, agricultural_product_id, erp_product_id, last_sync_date, sync_status, error_message, company_id, created_at, created_by, updated_at, updated_by
            FROM agricultural_inventory_integration
            WHERE id = %s
            """
            params = (integration_id,)
            result = self.db.execute_query(query, params, fetch_one=True)
            
            if result:
                integration = AgriculturalInventoryIntegration(**result)
                
                # إضافة معلومات إضافية
                integration.product = self.product_service.get_product_by_id(integration.erp_product_id)
                
                return integration
            
            return None
        
        # تحديث تاريخ المزامنة
        update_fields.append("last_sync_date = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_at = %s")
        params.append(datetime.now())
        
        update_fields.append("updated_by = %s")
        params.append(user_id)
        
        # إضافة معرف التكامل إلى المعلمات
        params.append(integration_id)
        
        query = f"""
        UPDATE agricultural_inventory_integration
        SET {", ".join(update_fields)}
        WHERE id = %s
        RETURNING id, agricultural_product_id, erp_product_id, last_sync_date, sync_status, error_message, company_id, created_at, created_by, updated_at, updated_by
        """
        
        result = self.db.execute_query(query, tuple(params), fetch_one=True)
        if result:
            integration = AgriculturalInventoryIntegration(**result)
            
            # إضافة معلومات إضافية
            integration.product = self.product_service.get_product_by_id(integration.erp_product_id)
            
            return integration
        
        return None
    
    def sync_agricultural_products(self, company_id: int, user_id: int) -> Dict[str, int]:
        """مزامنة المنتجات من النظام الزراعي"""
        # في هذا المثال، نفترض أن لدينا وظيفة تقوم بالحصول على المنتجات من النظام الزراعي
        # agricultural_products = self._get_agricultural_products()
        
        # في هذا المثال، نعيد قيم وهمية
        return {
            'total': 0,
            'created': 0,
            'updated': 0,
            'failed': 0
        }
    
    def _get_agricultural_products(self) -> List[Dict[str, Any]]:
        """الحصول على المنتجات من النظام الزراعي"""
        # في هذا المثال، نفترض أن لدينا وظيفة تقوم بالاتصال بالنظام الزراعي والحصول على المنتجات
        # في التطبيق الفعلي، يجب تنفيذ هذه الوظيفة بشكل صحيح
        
        # نعيد قائمة وهمية من المنتجات
        return []
