"""
Product Validator Module
@file backend/src/validators/product_validator.py

التحقق من صحة بيانات المنتجات
"""

from typing import Dict, List, Any, Optional, Tuple
import re


class ProductValidationError(Exception):
    """خطأ في التحقق من المنتج"""
    
    def __init__(self, message: str, field: str = None, errors: List[Dict] = None):
        self.message = message
        self.field = field
        self.errors = errors or []
        super().__init__(message)


class ProductValidator:
    """مدقق المنتجات"""
    
    VALID_TAX_TYPES = ['vat', 'exempt', 'zero_rated']
    
    # SKU patterns
    SKU_PATTERN = re.compile(r'^[A-Za-z0-9\-_]{3,50}$')
    BARCODE_PATTERN = re.compile(r'^\d{8,14}$')
    
    # Limits
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 200
    SKU_MIN_LENGTH = 3
    SKU_MAX_LENGTH = 50
    MIN_PRICE = 0
    MAX_PRICE = 99999999.99
    MIN_STOCK = 0
    MAX_STOCK = 99999999
    
    def __init__(self):
        self.errors = []
    
    def validate_product(self, data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, List[Dict]]:
        """
        التحقق من صحة بيانات المنتج
        
        Args:
            data: بيانات المنتج
            is_update: هل هذا تحديث (لا يتطلب جميع الحقول)
            
        Returns:
            Tuple[bool, List]: (صالح, قائمة الأخطاء)
        """
        self.errors = []
        
        # Required fields for new products
        if not is_update:
            self._validate_required_fields(data)
        
        # Validate name
        if 'name' in data:
            self._validate_name(data['name'])
        
        # Validate SKU
        if 'sku' in data:
            self._validate_sku(data['sku'])
        
        # Validate barcode
        if 'barcode' in data and data['barcode']:
            self._validate_barcode(data['barcode'])
        
        # Validate prices
        self._validate_prices(data)
        
        # Validate stock levels
        self._validate_stock_levels(data)
        
        # Validate tax type
        if 'tax_type' in data:
            self._validate_tax_type(data['tax_type'])
        
        # Validate category
        if 'category_id' in data and not is_update:
            self._validate_category(data['category_id'])
        
        return len(self.errors) == 0, self.errors
    
    def _validate_required_fields(self, data: Dict[str, Any]):
        """التحقق من الحقول المطلوبة"""
        required = ['name', 'sku', 'category_id', 'selling_price']
        
        for field in required:
            if field not in data or data[field] is None:
                self.errors.append({
                    'field': field,
                    'message': f'الحقل {field} مطلوب',
                    'code': 'required'
                })
            elif isinstance(data[field], str) and not data[field].strip():
                self.errors.append({
                    'field': field,
                    'message': f'الحقل {field} لا يمكن أن يكون فارغاً',
                    'code': 'empty'
                })
    
    def _validate_name(self, name: Any):
        """التحقق من اسم المنتج"""
        if not isinstance(name, str):
            self.errors.append({
                'field': 'name',
                'message': 'اسم المنتج يجب أن يكون نصاً',
                'code': 'invalid_type'
            })
            return
        
        name = name.strip()
        if len(name) < self.NAME_MIN_LENGTH:
            self.errors.append({
                'field': 'name',
                'message': f'اسم المنتج يجب أن يكون {self.NAME_MIN_LENGTH} أحرف على الأقل',
                'code': 'min_length'
            })
        elif len(name) > self.NAME_MAX_LENGTH:
            self.errors.append({
                'field': 'name',
                'message': f'اسم المنتج يجب ألا يتجاوز {self.NAME_MAX_LENGTH} حرف',
                'code': 'max_length'
            })
    
    def _validate_sku(self, sku: Any):
        """التحقق من رمز المنتج"""
        if not isinstance(sku, str):
            self.errors.append({
                'field': 'sku',
                'message': 'رمز المنتج يجب أن يكون نصاً',
                'code': 'invalid_type'
            })
            return
        
        sku = sku.strip()
        if len(sku) < self.SKU_MIN_LENGTH or len(sku) > self.SKU_MAX_LENGTH:
            self.errors.append({
                'field': 'sku',
                'message': f'رمز المنتج يجب أن يكون بين {self.SKU_MIN_LENGTH} و {self.SKU_MAX_LENGTH} حرف',
                'code': 'invalid_length'
            })
        elif not self.SKU_PATTERN.match(sku):
            self.errors.append({
                'field': 'sku',
                'message': 'رمز المنتج يجب أن يحتوي على أحرف وأرقام وشرطات فقط',
                'code': 'invalid_format'
            })
    
    def _validate_barcode(self, barcode: Any):
        """التحقق من الباركود"""
        if not isinstance(barcode, str):
            barcode = str(barcode)
        
        barcode = barcode.strip()
        if barcode and not self.BARCODE_PATTERN.match(barcode):
            self.errors.append({
                'field': 'barcode',
                'message': 'الباركود يجب أن يكون من 8 إلى 14 رقماً',
                'code': 'invalid_format'
            })
    
    def _validate_prices(self, data: Dict[str, Any]):
        """التحقق من الأسعار"""
        price_fields = ['cost_price', 'selling_price']
        
        for field in price_fields:
            if field in data and data[field] is not None:
                try:
                    price = float(data[field])
                    if price < self.MIN_PRICE:
                        self.errors.append({
                            'field': field,
                            'message': 'السعر لا يمكن أن يكون سالباً',
                            'code': 'negative'
                        })
                    elif price > self.MAX_PRICE:
                        self.errors.append({
                            'field': field,
                            'message': f'السعر يجب ألا يتجاوز {self.MAX_PRICE:,.2f}',
                            'code': 'max_exceeded'
                        })
                except (ValueError, TypeError):
                    self.errors.append({
                        'field': field,
                        'message': 'السعر يجب أن يكون رقماً',
                        'code': 'invalid_type'
                    })
        
        # Validate selling price >= cost price (warning, not error)
        if 'cost_price' in data and 'selling_price' in data:
            try:
                cost = float(data.get('cost_price', 0) or 0)
                selling = float(data.get('selling_price', 0) or 0)
                if selling < cost:
                    # This is a warning, not an error - business may allow selling at loss
                    pass
            except (ValueError, TypeError):
                pass
    
    def _validate_stock_levels(self, data: Dict[str, Any]):
        """التحقق من مستويات المخزون"""
        stock_fields = ['min_stock', 'max_stock', 'current_stock']
        
        for field in stock_fields:
            if field in data and data[field] is not None:
                try:
                    stock = float(data[field])
                    if stock < self.MIN_STOCK:
                        self.errors.append({
                            'field': field,
                            'message': 'مستوى المخزون لا يمكن أن يكون سالباً',
                            'code': 'negative'
                        })
                    elif stock > self.MAX_STOCK:
                        self.errors.append({
                            'field': field,
                            'message': f'مستوى المخزون يجب ألا يتجاوز {self.MAX_STOCK:,}',
                            'code': 'max_exceeded'
                        })
                except (ValueError, TypeError):
                    self.errors.append({
                        'field': field,
                        'message': 'مستوى المخزون يجب أن يكون رقماً',
                        'code': 'invalid_type'
                    })
        
        # Validate min_stock < max_stock
        if 'min_stock' in data and 'max_stock' in data:
            try:
                min_s = float(data.get('min_stock', 0) or 0)
                max_s = float(data.get('max_stock', 0) or 0)
                if max_s > 0 and min_s > max_s:
                    self.errors.append({
                        'field': 'min_stock',
                        'message': 'الحد الأدنى يجب أن يكون أقل من الحد الأقصى',
                        'code': 'invalid_range'
                    })
            except (ValueError, TypeError):
                pass
    
    def _validate_tax_type(self, tax_type: Any):
        """التحقق من نوع الضريبة"""
        if tax_type and tax_type not in self.VALID_TAX_TYPES:
            self.errors.append({
                'field': 'tax_type',
                'message': f'نوع الضريبة غير صالح. الأنواع المسموحة: {", ".join(self.VALID_TAX_TYPES)}',
                'code': 'invalid_type'
            })
    
    def _validate_category(self, category_id: Any):
        """التحقق من التصنيف"""
        if category_id is None:
            self.errors.append({
                'field': 'category_id',
                'message': 'التصنيف مطلوب',
                'code': 'required'
            })
        else:
            try:
                cat_id = int(category_id)
                if cat_id <= 0:
                    self.errors.append({
                        'field': 'category_id',
                        'message': 'معرف التصنيف غير صالح',
                        'code': 'invalid_id'
                    })
            except (ValueError, TypeError):
                self.errors.append({
                    'field': 'category_id',
                    'message': 'معرف التصنيف يجب أن يكون رقماً',
                    'code': 'invalid_type'
                })


# Singleton instance
product_validator = ProductValidator()


def validate_product(data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, List[Dict]]:
    """دالة مساعدة للتحقق من المنتج"""
    return product_validator.validate_product(data, is_update)
