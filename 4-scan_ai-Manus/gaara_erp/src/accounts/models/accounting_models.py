#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نماذج وحدة الحسابات لنظام Gaara ERP
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from decimal import Decimal

@dataclass
class Account:
    """نموذج الحساب في مخطط الحسابات"""
    account_id: Optional[int] = None
    account_code: str = ""
    account_name: str = ""
    account_type: str = ""  # asset, liability, equity, income, expense
    parent_account_id: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    company_id: Optional[int] = None
    balance_type: str = "debit"  # debit, credit
    level: int = 1
    is_group: bool = False
    is_control_account: bool = False
    is_cash_account: bool = False
    is_bank_account: bool = False
    is_tax_account: bool = False
    is_system: bool = False
    
    @property
    def full_name(self) -> str:
        """الحصول على الاسم الكامل للحساب مع الكود"""
        return f"{self.account_code} - {self.account_name}"
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الحساب إلى قاموس"""
        return {
            "account_id": self.account_id,
            "account_code": self.account_code,
            "account_name": self.account_name,
            "account_type": self.account_type,
            "parent_account_id": self.parent_account_id,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "company_id": self.company_id,
            "balance_type": self.balance_type,
            "level": self.level,
            "is_group": self.is_group,
            "is_control_account": self.is_control_account,
            "is_cash_account": self.is_cash_account,
            "is_bank_account": self.is_bank_account,
            "is_tax_account": self.is_tax_account,
            "is_system": self.is_system,
            "full_name": self.full_name
        }

@dataclass
class FiscalYear:
    """نموذج السنة المالية"""
    fiscal_year_id: Optional[int] = None
    company_id: Optional[int] = None
    year_name: str = ""
    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    is_closed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل السنة المالية إلى قاموس"""
        return {
            "fiscal_year_id": self.fiscal_year_id,
            "company_id": self.company_id,
            "year_name": self.year_name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "is_closed": self.is_closed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class AccountingPeriod:
    """نموذج الفترة المحاسبية"""
    period_id: Optional[int] = None
    fiscal_year_id: Optional[int] = None
    period_name: str = ""
    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime = field(default_factory=datetime.now)
    is_closed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الفترة المحاسبية إلى قاموس"""
        return {
            "period_id": self.period_id,
            "fiscal_year_id": self.fiscal_year_id,
            "period_name": self.period_name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_closed": self.is_closed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class JournalEntry:
    """نموذج قيد اليومية"""
    entry_id: Optional[int] = None
    entry_number: str = ""
    entry_date: datetime = field(default_factory=datetime.now)
    posting_date: datetime = field(default_factory=datetime.now)
    reference_number: Optional[str] = None
    source_document: Optional[str] = None
    source_id: Optional[str] = None
    description: Optional[str] = None
    is_posted: bool = False
    is_reversed: bool = False
    reversed_entry_id: Optional[int] = None
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    period_id: Optional[int] = None
    currency_code: str = "USD"
    exchange_rate: Decimal = Decimal("1.0")
    total_debit: Decimal = Decimal("0.0")
    total_credit: Decimal = Decimal("0.0")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    entry_type: str = "manual"  # manual, sales, purchase, payment, receipt, etc.
    items: List["JournalItem"] = field(default_factory=list)
    
    def add_item(self, item: "JournalItem") -> None:
        """إضافة بند إلى قيد اليومية"""
        self.items.append(item)
        self.total_debit += item.debit
        self.total_credit += item.credit
    
    def is_balanced(self) -> bool:
        """التحقق من توازن قيد اليومية"""
        return self.total_debit == self.total_credit
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل قيد اليومية إلى قاموس"""
        return {
            "entry_id": self.entry_id,
            "entry_number": self.entry_number,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
            "posting_date": self.posting_date.isoformat() if self.posting_date else None,
            "reference_number": self.reference_number,
            "source_document": self.source_document,
            "source_id": self.source_id,
            "description": self.description,
            "is_posted": self.is_posted,
            "is_reversed": self.is_reversed,
            "reversed_entry_id": self.reversed_entry_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "period_id": self.period_id,
            "currency_code": self.currency_code,
            "exchange_rate": float(self.exchange_rate),
            "total_debit": float(self.total_debit),
            "total_credit": float(self.total_credit),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "entry_type": self.entry_type,
            "items": [item.to_dict() for item in self.items],
            "is_balanced": self.is_balanced()
        }

@dataclass
class JournalItem:
    """نموذج بند قيد اليومية"""
    item_id: Optional[int] = None
    entry_id: Optional[int] = None
    account_id: Optional[int] = None
    description: Optional[str] = None
    debit: Decimal = Decimal("0.0")
    credit: Decimal = Decimal("0.0")
    currency_code: str = "USD"
    exchange_rate: Decimal = Decimal("1.0")
    debit_foreign: Decimal = Decimal("0.0")
    credit_foreign: Decimal = Decimal("0.0")
    cost_center_id: Optional[int] = None
    project_id: Optional[int] = None
    dimension1_id: Optional[int] = None
    dimension2_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل بند قيد اليومية إلى قاموس"""
        return {
            "item_id": self.item_id,
            "entry_id": self.entry_id,
            "account_id": self.account_id,
            "description": self.description,
            "debit": float(self.debit),
            "credit": float(self.credit),
            "currency_code": self.currency_code,
            "exchange_rate": float(self.exchange_rate),
            "debit_foreign": float(self.debit_foreign),
            "credit_foreign": float(self.credit_foreign),
            "cost_center_id": self.cost_center_id,
            "project_id": self.project_id,
            "dimension1_id": self.dimension1_id,
            "dimension2_id": self.dimension2_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

@dataclass
class Customer:
    """نموذج العميل"""
    customer_id: Optional[int] = None
    customer_code: str = ""
    customer_name: str = ""
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    tax_id: Optional[str] = None
    credit_limit: Decimal = Decimal("0.0")
    payment_terms: int = 0
    is_active: bool = True
    account_id: Optional[int] = None
    company_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل العميل إلى قاموس"""
        return {
            "customer_id": self.customer_id,
            "customer_code": self.customer_code,
            "customer_name": self.customer_name,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "mobile": self.mobile,
            "email": self.email,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "postal_code": self.postal_code,
            "tax_id": self.tax_id,
            "credit_limit": float(self.credit_limit),
            "payment_terms": self.payment_terms,
            "is_active": self.is_active,
            "account_id": self.account_id,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class Supplier:
    """نموذج المورد"""
    supplier_id: Optional[int] = None
    supplier_code: str = ""
    supplier_name: str = ""
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    tax_id: Optional[str] = None
    payment_terms: int = 0
    is_active: bool = True
    account_id: Optional[int] = None
    company_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل المورد إلى قاموس"""
        return {
            "supplier_id": self.supplier_id,
            "supplier_code": self.supplier_code,
            "supplier_name": self.supplier_name,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "mobile": self.mobile,
            "email": self.email,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "postal_code": self.postal_code,
            "tax_id": self.tax_id,
            "payment_terms": self.payment_terms,
            "is_active": self.is_active,
            "account_id": self.account_id,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class SalesInvoice:
    """نموذج فاتورة المبيعات"""
    invoice_id: Optional[int] = None
    invoice_number: str = ""
    invoice_date: datetime = field(default_factory=datetime.now)
    due_date: datetime = field(default_factory=datetime.now)
    customer_id: Optional[int] = None
    reference: Optional[str] = None
    description: Optional[str] = None
    subtotal: Decimal = Decimal("0.0")
    tax_amount: Decimal = Decimal("0.0")
    discount_amount: Decimal = Decimal("0.0")
    total_amount: Decimal = Decimal("0.0")
    paid_amount: Decimal = Decimal("0.0")
    balance_amount: Decimal = Decimal("0.0")
    status: str = "draft"  # draft, approved, paid, cancelled
    is_posted: bool = False
    journal_entry_id: Optional[int] = None
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    currency_code: str = "USD"
    exchange_rate: Decimal = Decimal("1.0")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    items: List["SalesInvoiceItem"] = field(default_factory=list)
    
    def add_item(self, item: "SalesInvoiceItem") -> None:
        """إضافة بند إلى فاتورة المبيعات"""
        self.items.append(item)
        self.subtotal += item.total_amount
        self.recalculate_totals()
    
    def recalculate_totals(self) -> None:
        """إعادة حساب إجماليات الفاتورة"""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.balance_amount = self.total_amount - self.paid_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل فاتورة المبيعات إلى قاموس"""
        return {
            "invoice_id": self.invoice_id,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date.isoformat() if self.invoice_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "customer_id": self.customer_id,
            "reference": self.reference,
            "description": self.description,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "discount_amount": float(self.discount_amount),
            "total_amount": float(self.total_amount),
            "paid_amount": float(self.paid_amount),
            "balance_amount": float(self.balance_amount),
            "status": self.status,
            "is_posted": self.is_posted,
            "journal_entry_id": self.journal_entry_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "currency_code": self.currency_code,
            "exchange_rate": float(self.exchange_rate),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "items": [item.to_dict() for item in self.items]
        }

@dataclass
class SalesInvoiceItem:
    """نموذج بند فاتورة المبيعات"""
    item_id: Optional[int] = None
    invoice_id: Optional[int] = None
    product_id: Optional[int] = None
    description: str = ""
    quantity: Decimal = Decimal("0.0")
    unit_price: Decimal = Decimal("0.0")
    discount_percent: Decimal = Decimal("0.0")
    discount_amount: Decimal = Decimal("0.0")
    tax_percent: Decimal = Decimal("0.0")
    tax_amount: Decimal = Decimal("0.0")
    total_amount: Decimal = Decimal("0.0")
    account_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calculate_amounts(self) -> None:
        """حساب المبالغ"""
        # حساب مبلغ الخصم
        self.discount_amount = (self.quantity * self.unit_price) * (self.discount_percent / Decimal("100.0"))
        
        # حساب المبلغ قبل الضريبة
        pre_tax_amount = (self.quantity * self.unit_price) - self.discount_amount
        
        # حساب مبلغ الضريبة
        self.tax_amount = pre_tax_amount * (self.tax_percent / Decimal("100.0"))
        
        # حساب المبلغ الإجمالي
        self.total_amount = pre_tax_amount + self.tax_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل بند فاتورة المبيعات إلى قاموس"""
        return {
            "item_id": self.item_id,
            "invoice_id": self.invoice_id,
            "product_id": self.product_id,
            "description": self.description,
            "quantity": float(self.quantity),
            "unit_price": float(self.unit_price),
            "discount_percent": float(self.discount_percent),
            "discount_amount": float(self.discount_amount),
            "tax_percent": float(self.tax_percent),
            "tax_amount": float(self.tax_amount),
            "total_amount": float(self.total_amount),
            "account_id": self.account_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

@dataclass
class Payment:
    """نموذج المدفوعات"""
    payment_id: Optional[int] = None
    payment_number: str = ""
    payment_date: datetime = field(default_factory=datetime.now)
    payment_type: str = ""  # receipt, payment
    amount: Decimal = Decimal("0.0")
    reference: Optional[str] = None
    description: Optional[str] = None
    party_type: str = ""  # customer, supplier
    party_id: Optional[int] = None
    account_id: Optional[int] = None
    is_posted: bool = False
    journal_entry_id: Optional[int] = None
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    currency_code: str = "USD"
    exchange_rate: Decimal = Decimal("1.0")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    applications: List["PaymentApplication"] = field(default_factory=list)
    
    def add_application(self, application: "PaymentApplication") -> None:
        """إضافة تطبيق للمدفوعات"""
        self.applications.append(application)
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل المدفوعات إلى قاموس"""
        return {
            "payment_id": self.payment_id,
            "payment_number": self.payment_number,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "payment_type": self.payment_type,
            "amount": float(self.amount),
            "reference": self.reference,
            "description": self.description,
            "party_type": self.party_type,
            "party_id": self.party_id,
            "account_id": self.account_id,
            "is_posted": self.is_posted,
            "journal_entry_id": self.journal_entry_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "currency_code": self.currency_code,
            "exchange_rate": float(self.exchange_rate),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "applications": [app.to_dict() for app in self.applications]
        }

@dataclass
class PaymentApplication:
    """نموذج تطبيق المدفوعات"""
    application_id: Optional[int] = None
    payment_id: Optional[int] = None
    invoice_type: str = ""  # sales, purchase
    invoice_id: Optional[int] = None
    amount: Decimal = Decimal("0.0")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل تطبيق المدفوعات إلى قاموس"""
        return {
            "application_id": self.application_id,
            "payment_id": self.payment_id,
            "invoice_type": self.invoice_type,
            "invoice_id": self.invoice_id,
            "amount": float(self.amount),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

@dataclass
class BankAccount:
    """نموذج الحساب البنكي"""
    bank_account_id: Optional[int] = None
    account_id: Optional[int] = None
    bank_name: str = ""
    account_number: str = ""
    branch_name: Optional[str] = None
    iban: Optional[str] = None
    swift_code: Optional[str] = None
    currency_code: str = "USD"
    is_active: bool = True
    company_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الحساب البنكي إلى قاموس"""
        return {
            "bank_account_id": self.bank_account_id,
            "account_id": self.account_id,
            "bank_name": self.bank_name,
            "account_number": self.account_number,
            "branch_name": self.branch_name,
            "iban": self.iban,
            "swift_code": self.swift_code,
            "currency_code": self.currency_code,
            "is_active": self.is_active,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class Tax:
    """نموذج الضريبة"""
    tax_id: Optional[int] = None
    tax_code: str = ""
    tax_name: str = ""
    tax_rate: Decimal = Decimal("0.0")
    account_id: Optional[int] = None
    is_active: bool = True
    company_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الضريبة إلى قاموس"""
        return {
            "tax_id": self.tax_id,
            "tax_code": self.tax_code,
            "tax_name": self.tax_name,
            "tax_rate": float(self.tax_rate),
            "account_id": self.account_id,
            "is_active": self.is_active,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class CostCenter:
    """نموذج مركز التكلفة"""
    cost_center_id: Optional[int] = None
    cost_center_code: str = ""
    cost_center_name: str = ""
    parent_cost_center_id: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True
    company_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل مركز التكلفة إلى قاموس"""
        return {
            "cost_center_id": self.cost_center_id,
            "cost_center_code": self.cost_center_code,
            "cost_center_name": self.cost_center_name,
            "parent_cost_center_id": self.parent_cost_center_id,
            "description": self.description,
            "is_active": self.is_active,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }

@dataclass
class AccountBalance:
    """نموذج رصيد الحساب"""
    balance_id: Optional[int] = None
    account_id: Optional[int] = None
    period_id: Optional[int] = None
    opening_debit: Decimal = Decimal("0.0")
    opening_credit: Decimal = Decimal("0.0")
    period_debit: Decimal = Decimal("0.0")
    period_credit: Decimal = Decimal("0.0")
    closing_debit: Decimal = Decimal("0.0")
    closing_credit: Decimal = Decimal("0.0")
    currency_code: str = "USD"
    company_id: Optional[int] = None
    branch_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def calculate_closing_balance(self) -> None:
        """حساب الرصيد الختامي"""
        self.closing_debit = self.opening_debit + self.period_debit
        self.closing_credit = self.opening_credit + self.period_credit
    
    def get_net_balance(self) -> Decimal:
        """الحصول على صافي الرصيد"""
        return self.closing_debit - self.closing_credit
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل رصيد الحساب إلى قاموس"""
        return {
            "balance_id": self.balance_id,
            "account_id": self.account_id,
            "period_id": self.period_id,
            "opening_debit": float(self.opening_debit),
            "opening_credit": float(self.opening_credit),
            "period_debit": float(self.period_debit),
            "period_credit": float(self.period_credit),
            "closing_debit": float(self.closing_debit),
            "closing_credit": float(self.closing_credit),
            "currency_code": self.currency_code,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "net_balance": float(self.get_net_balance())
        }
