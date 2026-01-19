#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التحكم في الحسابات لنظام Gaara ERP
تتعامل مع طلبات واجهة المستخدم وتوجيهها إلى الخدمات المناسبة
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional

from ..services.accounting_services import (
    AccountingService, ChartOfAccountsService, JournalEntryService,
    LedgerService, FinancialReportService, TaxService, BudgetService
)
from ..models.accounting_models import (
    Account, AccountCreate, AccountUpdate,
    JournalEntry, JournalEntryCreate, JournalEntryUpdate,
    Ledger, Budget, BudgetCreate, BudgetUpdate,
    FinancialPeriod, FinancialPeriodCreate, FinancialPeriodUpdate,
    TaxRule, TaxRuleCreate, TaxRuleUpdate
)
from ...core.auth.auth_manager import get_current_user, check_permissions

# إنشاء موجه API للحسابات
router = APIRouter(prefix="/api/accounts", tags=["accounting"])
logger = logging.getLogger(__name__)

# الخدمات
accounting_service = AccountingService()
chart_service = ChartOfAccountsService()
journal_service = JournalEntryService()
ledger_service = LedgerService()
financial_report_service = FinancialReportService()
tax_service = TaxService()
budget_service = BudgetService()

# ===================== إدارة دليل الحسابات =====================

@router.post("/accounts/", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(
    account: AccountCreate,
    current_user: Dict = Depends(get_current_user)
):
    """إنشاء حساب جديد في دليل الحسابات"""
    check_permissions(current_user, "accounts:create")
    return chart_service.create_account(account, current_user["id"])

@router.get("/accounts/", response_model=List[Account])
async def get_accounts(
    parent_id: Optional[int] = None,
    account_type: Optional[str] = None,
    is_active: bool = True,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على قائمة الحسابات مع إمكانية التصفية"""
    check_permissions(current_user, "accounts:view")
    return chart_service.get_accounts(parent_id, account_type, is_active)

@router.get("/accounts/{account_id}", response_model=Account)
async def get_account(
    account_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على تفاصيل حساب محدد"""
    check_permissions(current_user, "accounts:view")
    account = chart_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الحساب غير موجود"
        )
    return account

@router.put("/accounts/{account_id}", response_model=Account)
async def update_account(
    account_id: int,
    account_update: AccountUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """تحديث بيانات حساب محدد"""
    check_permissions(current_user, "accounts:update")
    account = chart_service.update_account(account_id, account_update, current_user["id"])
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الحساب غير موجود"
        )
    return account

@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """حذف حساب محدد (تعطيل)"""
    check_permissions(current_user, "accounts:delete")
    success = chart_service.delete_account(account_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الحساب غير موجود أو لا يمكن حذفه"
        )
    return {"detail": "تم حذف الحساب بنجاح"}

# ===================== إدارة قيود اليومية =====================

@router.post("/journal-entries/", response_model=JournalEntry, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    entry: JournalEntryCreate,
    current_user: Dict = Depends(get_current_user)
):
    """إنشاء قيد يومية جديد"""
    check_permissions(current_user, "journal:create")
    return journal_service.create_journal_entry(entry, current_user["id"])

@router.get("/journal-entries/", response_model=List[JournalEntry])
async def get_journal_entries(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    entry_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على قائمة قيود اليومية مع إمكانية التصفية"""
    check_permissions(current_user, "journal:view")
    return journal_service.get_journal_entries(start_date, end_date, entry_type, status)

@router.get("/journal-entries/{entry_id}", response_model=JournalEntry)
async def get_journal_entry(
    entry_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على تفاصيل قيد يومية محدد"""
    check_permissions(current_user, "journal:view")
    entry = journal_service.get_journal_entry_by_id(entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="قيد اليومية غير موجود"
        )
    return entry

@router.put("/journal-entries/{entry_id}", response_model=JournalEntry)
async def update_journal_entry(
    entry_id: int,
    entry_update: JournalEntryUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """تحديث قيد يومية محدد (قبل الترحيل فقط)"""
    check_permissions(current_user, "journal:update")
    entry = journal_service.update_journal_entry(entry_id, entry_update, current_user["id"])
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="قيد اليومية غير موجود أو تم ترحيله بالفعل"
        )
    return entry

@router.post("/journal-entries/{entry_id}/post", response_model=JournalEntry)
async def post_journal_entry(
    entry_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """ترحيل قيد يومية إلى دفتر الأستاذ"""
    check_permissions(current_user, "journal:post")
    entry = journal_service.post_journal_entry(entry_id, current_user["id"])
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="قيد اليومية غير موجود أو تم ترحيله بالفعل"
        )
    return entry

# ===================== التقارير المالية =====================

@router.get("/reports/trial-balance")
async def get_trial_balance(
    as_of_date: str,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على ميزان المراجعة"""
    check_permissions(current_user, "reports:view")
    return financial_report_service.get_trial_balance(as_of_date)

@router.get("/reports/income-statement")
async def get_income_statement(
    start_date: str,
    end_date: str,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على قائمة الدخل"""
    check_permissions(current_user, "reports:view")
    return financial_report_service.get_income_statement(start_date, end_date)

@router.get("/reports/balance-sheet")
async def get_balance_sheet(
    as_of_date: str,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على الميزانية العمومية"""
    check_permissions(current_user, "reports:view")
    return financial_report_service.get_balance_sheet(as_of_date)

@router.get("/reports/cash-flow")
async def get_cash_flow(
    start_date: str,
    end_date: str,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على قائمة التدفقات النقدية"""
    check_permissions(current_user, "reports:view")
    return financial_report_service.get_cash_flow(start_date, end_date)

# ===================== إدارة الميزانيات =====================

@router.post("/budgets/", response_model=Budget, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget: BudgetCreate,
    current_user: Dict = Depends(get_current_user)
):
    """إنشاء ميزانية تقديرية جديدة"""
    check_permissions(current_user, "budgets:create")
    return budget_service.create_budget(budget, current_user["id"])

@router.get("/budgets/", response_model=List[Budget])
async def get_budgets(
    year: Optional[int] = None,
    status: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على قائمة الميزانيات التقديرية"""
    check_permissions(current_user, "budgets:view")
    return budget_service.get_budgets(year, status)

@router.get("/budgets/{budget_id}", response_model=Budget)
async def get_budget(
    budget_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على تفاصيل ميزانية تقديرية محددة"""
    check_permissions(current_user, "budgets:view")
    budget = budget_service.get_budget_by_id(budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الميزانية غير موجودة"
        )
    return budget

@router.put("/budgets/{budget_id}", response_model=Budget)
async def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """تحديث ميزانية تقديرية محددة"""
    check_permissions(current_user, "budgets:update")
    budget = budget_service.update_budget(budget_id, budget_update, current_user["id"])
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الميزانية غير موجودة"
        )
    return budget

@router.get("/budgets/{budget_id}/variance")
async def get_budget_variance(
    budget_id: int,
    as_of_date: str,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على تحليل الانحرافات للميزانية التقديرية"""
    check_permissions(current_user, "budgets:view")
    return budget_service.get_budget_variance(budget_id, as_of_date)

# ===================== إدارة الفترات المالية =====================

@router.post("/financial-periods/", response_model=FinancialPeriod, status_code=status.HTTP_201_CREATED)
async def create_financial_period(
    period: FinancialPeriodCreate,
    current_user: Dict = Depends(get_current_user)
):
    """إنشاء فترة مالية جديدة"""
    check_permissions(current_user, "financial_periods:create")
    return accounting_service.create_financial_period(period, current_user["id"])

@router.get("/financial-periods/", response_model=List[FinancialPeriod])
async def get_financial_periods(
    year: Optional[int] = None,
    status: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على قائمة الفترات المالية"""
    check_permissions(current_user, "financial_periods:view")
    return accounting_service.get_financial_periods(year, status)

@router.post("/financial-periods/{period_id}/close")
async def close_financial_period(
    period_id: int,
    current_user: Dict = Depends(get_current_user)
):
    """إغلاق فترة مالية محددة"""
    check_permissions(current_user, "financial_periods:close")
    success = accounting_service.close_financial_period(period_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="لا يمكن إغلاق الفترة المالية"
        )
    return {"detail": "تم إغلاق الفترة المالية بنجاح"}

# ===================== التكامل مع النظام الزراعي =====================

@router.get("/integration/agricultural-expenses")
async def get_agricultural_expenses(
    start_date: str,
    end_date: str,
    crop_type: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """الحصول على مصاريف النظام الزراعي للتكامل مع النظام المالي"""
    check_permissions(current_user, "integration:view")
    return accounting_service.get_agricultural_expenses(start_date, end_date, crop_type)

@router.post("/integration/sync-agricultural-transactions")
async def sync_agricultural_transactions(
    current_user: Dict = Depends(get_current_user)
):
    """مزامنة المعاملات من النظام الزراعي إلى النظام المالي"""
    check_permissions(current_user, "integration:sync")
    result = accounting_service.sync_agricultural_transactions(current_user["id"])
    return {"detail": f"تمت المزامنة بنجاح. {result['created']} معاملات جديدة، {result['updated']} معاملات محدثة."}
