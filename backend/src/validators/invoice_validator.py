"""
Invoice Validator Module
@file backend/src/validators/invoice_validator.py

التحقق من صحة بيانات الفواتير
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import re


class InvoiceValidationError(Exception):
    """خطأ في التحقق من الفاتورة"""
    
    def __init__(self, message: str, field: str = None, errors: List[Dict] = None):
        self.message = message
        self.field = field
        self.errors = errors or []
        super().__init__(message)


class InvoiceValidator:
    """مدقق الفواتير"""
    
    VALID_INVOICE_TYPES = ['sale', 'purchase', 'sale_return', 'purchase_return']
    VALID_PAYMENT_METHODS = ['cash', 'card', 'bank_transfer', 'check', 'credit', 'mada', 'visa', 'mastercard']
    VALID_STATUSES = ['draft', 'pending', 'paid', 'partial', 'overdue', 'cancelled']
    
    MAX_ITEMS = 500
    MAX_DISCOUNT_PERCENTAGE = 100
    MIN_QUANTITY = 0.001
    MAX_QUANTITY = 999999
    
    def __init__(self):
        self.errors = []
    
    def validate_invoice(self, data: Dict[str, Any]) -> Tuple[bool, List[Dict]]:
        """
        التحقق من صحة بيانات الفاتورة الكاملة
        
        Args:
            data: بيانات الفاتورة
            
        Returns:
            Tuple[bool, List]: (صالح, قائمة الأخطاء)
        """
        self.errors = []
        
        # Validate required fields
        self._validate_required_fields(data)
        
        # Validate invoice type
        self._validate_invoice_type(data.get('invoice_type'))
        
        # Validate payment method
        self._validate_payment_method(data.get('payment_method'))
        
        # Validate items
        if 'items' in data:
            self._validate_items(data['items'])
        
        # Validate amounts
        self._validate_amounts(data)
        
        # Validate dates
        self._validate_dates(data)
        
        # Validate customer/supplier
        self._validate_parties(data)
        
        return len(self.errors) == 0, self.errors
    
    def _validate_required_fields(self, data: Dict[str, Any]):
        """التحقق من الحقول المطلوبة"""
        required = ['invoice_type', 'items', 'warehouse_id']
        
        for field in required:
            if field not in data or data[field] is None:
                self.errors.append({
                    'field': field,
                    'message': f'الحقل {field} مطلوب',
                    'code': 'required'
                })
            elif field == 'items' and (not isinstance(data[field], list) or len(data[field]) == 0):
                self.errors.append({
                    'field': 'items',
                    'message': 'يجب إضافة عنصر واحد على الأقل',
                    'code': 'min_items'
                })
    
    def _validate_invoice_type(self, invoice_type: Optional[str]):
        """التحقق من نوع الفاتورة"""
        if invoice_type and invoice_type not in self.VALID_INVOICE_TYPES:
            self.errors.append({
                'field': 'invoice_type',
                'message': f'نوع فاتورة غير صالح. الأنواع المسموحة: {", ".join(self.VALID_INVOICE_TYPES)}',
                'code': 'invalid_type'
            })
    
    def _validate_payment_method(self, payment_method: Optional[str]):
        """التحقق من طريقة الدفع"""
        if payment_method and payment_method not in self.VALID_PAYMENT_METHODS:
            self.errors.append({
                'field': 'payment_method',
                'message': f'طريقة دفع غير صالحة. الطرق المسموحة: {", ".join(self.VALID_PAYMENT_METHODS)}',
                'code': 'invalid_payment_method'
            })
    
    def _validate_items(self, items: List[Dict[str, Any]]):
        """التحقق من عناصر الفاتورة"""
        if len(items) > self.MAX_ITEMS:
            self.errors.append({
                'field': 'items',
                'message': f'الحد الأقصى لعدد العناصر هو {self.MAX_ITEMS}',
                'code': 'max_items'
            })
            return
        
        for idx, item in enumerate(items):
            self._validate_item(item, idx)
    
    def _validate_item(self, item: Dict[str, Any], index: int):
        """التحقق من عنصر واحد"""
        prefix = f'items[{index}]'
        
        # Product ID required
        if not item.get('product_id'):
            self.errors.append({
                'field': f'{prefix}.product_id',
                'message': 'معرف المنتج مطلوب',
                'code': 'required'
            })
        
        # Quantity validation
        quantity = item.get('quantity')
        if quantity is None:
            self.errors.append({
                'field': f'{prefix}.quantity',
                'message': 'الكمية مطلوبة',
                'code': 'required'
            })
        else:
            try:
                qty = float(quantity)
                if qty < self.MIN_QUANTITY:
                    self.errors.append({
                        'field': f'{prefix}.quantity',
                        'message': f'الكمية يجب أن تكون أكبر من {self.MIN_QUANTITY}',
                        'code': 'min_quantity'
                    })
                elif qty > self.MAX_QUANTITY:
                    self.errors.append({
                        'field': f'{prefix}.quantity',
                        'message': f'الكمية يجب أن تكون أقل من {self.MAX_QUANTITY}',
                        'code': 'max_quantity'
                    })
            except (ValueError, TypeError):
                self.errors.append({
                    'field': f'{prefix}.quantity',
                    'message': 'الكمية يجب أن تكون رقماً',
                    'code': 'invalid_type'
                })
        
        # Unit price validation
        unit_price = item.get('unit_price')
        if unit_price is not None:
            try:
                price = float(unit_price)
                if price < 0:
                    self.errors.append({
                        'field': f'{prefix}.unit_price',
                        'message': 'السعر لا يمكن أن يكون سالباً',
                        'code': 'negative_price'
                    })
            except (ValueError, TypeError):
                self.errors.append({
                    'field': f'{prefix}.unit_price',
                    'message': 'السعر يجب أن يكون رقماً',
                    'code': 'invalid_type'
                })
        
        # Discount validation
        discount = item.get('discount', 0)
        if discount:
            try:
                disc = float(discount)
                if disc < 0:
                    self.errors.append({
                        'field': f'{prefix}.discount',
                        'message': 'الخصم لا يمكن أن يكون سالباً',
                        'code': 'negative_discount'
                    })
            except (ValueError, TypeError):
                self.errors.append({
                    'field': f'{prefix}.discount',
                    'message': 'الخصم يجب أن يكون رقماً',
                    'code': 'invalid_type'
                })
    
    def _validate_amounts(self, data: Dict[str, Any]):
        """التحقق من المبالغ"""
        # Discount percentage
        if 'discount_percentage' in data:
            try:
                discount = float(data['discount_percentage'])
                if discount < 0 or discount > self.MAX_DISCOUNT_PERCENTAGE:
                    self.errors.append({
                        'field': 'discount_percentage',
                        'message': f'نسبة الخصم يجب أن تكون بين 0 و {self.MAX_DISCOUNT_PERCENTAGE}',
                        'code': 'invalid_range'
                    })
            except (ValueError, TypeError):
                self.errors.append({
                    'field': 'discount_percentage',
                    'message': 'نسبة الخصم يجب أن تكون رقماً',
                    'code': 'invalid_type'
                })
        
        # Paid amount
        if 'paid_amount' in data:
            try:
                paid = float(data['paid_amount'])
                if paid < 0:
                    self.errors.append({
                        'field': 'paid_amount',
                        'message': 'المبلغ المدفوع لا يمكن أن يكون سالباً',
                        'code': 'negative_amount'
                    })
            except (ValueError, TypeError):
                self.errors.append({
                    'field': 'paid_amount',
                    'message': 'المبلغ المدفوع يجب أن يكون رقماً',
                    'code': 'invalid_type'
                })
    
    def _validate_dates(self, data: Dict[str, Any]):
        """التحقق من التواريخ"""
        if 'due_date' in data and data['due_date']:
            try:
                if isinstance(data['due_date'], str):
                    due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                elif isinstance(data['due_date'], (datetime, date)):
                    due_date = data['due_date']
                else:
                    raise ValueError("Invalid date format")
            except (ValueError, TypeError):
                self.errors.append({
                    'field': 'due_date',
                    'message': 'تاريخ الاستحقاق غير صالح',
                    'code': 'invalid_date'
                })
    
    def _validate_parties(self, data: Dict[str, Any]):
        """التحقق من العميل/المورد"""
        invoice_type = data.get('invoice_type', '')
        
        # Sales invoices require customer for credit transactions
        if invoice_type in ['sale', 'sale_return']:
            payment_method = data.get('payment_method', '')
            if payment_method == 'credit' and not data.get('customer_id'):
                self.errors.append({
                    'field': 'customer_id',
                    'message': 'العميل مطلوب للمعاملات الآجلة',
                    'code': 'required_for_credit'
                })
        
        # Purchase invoices require supplier
        if invoice_type in ['purchase', 'purchase_return']:
            if not data.get('supplier_id'):
                self.errors.append({
                    'field': 'supplier_id',
                    'message': 'المورد مطلوب لفواتير المشتريات',
                    'code': 'required'
                })


# Singleton instance
invoice_validator = InvoiceValidator()


def validate_invoice(data: Dict[str, Any]) -> Tuple[bool, List[Dict]]:
    """دالة مساعدة للتحقق من الفاتورة"""
    return invoice_validator.validate_invoice(data)
