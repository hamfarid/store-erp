#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
خدمات وحدة الحسابات لنظام Gaara ERP
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal

from ..models.accounting_models import (
    Account, FiscalYear, AccountingPeriod, JournalEntry, JournalItem,
    Customer, Supplier, SalesInvoice, SalesInvoiceItem, Payment,
    PaymentApplication, BankAccount, Tax, CostCenter, AccountBalance
)

# إعداد التسجيل
logger = logging.getLogger(__name__)

class AccountService:
    """خدمة إدارة الحسابات"""
    
    def __init__(self, db_manager=None):
        """تهيئة خدمة الحسابات"""
        from src.core.database.db_manager import DatabaseManager
        self.db_manager = db_manager or DatabaseManager()
    
    def get_account_by_id(self, account_id: int, company_id: int) -> Optional[Account]:
        """الحصول على حساب بواسطة المعرف"""
        try:
            query = """
                SELECT * FROM erp.chart_of_accounts
                WHERE account_id = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (account_id, company_id))
            
            if not result:
                return None
            
            account_data = result[0]
            return Account(
                account_id=account_data['account_id'],
                account_code=account_data['account_code'],
                account_name=account_data['account_name'],
                account_type=account_data['account_type'],
                parent_account_id=account_data['parent_account_id'],
                description=account_data['description'],
                is_active=account_data['is_active'],
                created_at=account_data['created_at'],
                updated_at=account_data['updated_at'],
                created_by=account_data['created_by'],
                updated_by=account_data['updated_by'],
                company_id=account_data['company_id'],
                balance_type=account_data['balance_type'],
                level=account_data['level'],
                is_group=account_data['is_group'],
                is_control_account=account_data['is_control_account'],
                is_cash_account=account_data['is_cash_account'],
                is_bank_account=account_data['is_bank_account'],
                is_tax_account=account_data['is_tax_account'],
                is_system=account_data['is_system']
            )
        except Exception as e:
            logger.error(f"فشل في الحصول على الحساب: {str(e)}")
            return None
    
    def get_account_by_code(self, account_code: str, company_id: int) -> Optional[Account]:
        """الحصول على حساب بواسطة الكود"""
        try:
            query = """
                SELECT * FROM erp.chart_of_accounts
                WHERE account_code = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (account_code, company_id))
            
            if not result:
                return None
            
            account_data = result[0]
            return Account(
                account_id=account_data['account_id'],
                account_code=account_data['account_code'],
                account_name=account_data['account_name'],
                account_type=account_data['account_type'],
                parent_account_id=account_data['parent_account_id'],
                description=account_data['description'],
                is_active=account_data['is_active'],
                created_at=account_data['created_at'],
                updated_at=account_data['updated_at'],
                created_by=account_data['created_by'],
                updated_by=account_data['updated_by'],
                company_id=account_data['company_id'],
                balance_type=account_data['balance_type'],
                level=account_data['level'],
                is_group=account_data['is_group'],
                is_control_account=account_data['is_control_account'],
                is_cash_account=account_data['is_cash_account'],
                is_bank_account=account_data['is_bank_account'],
                is_tax_account=account_data['is_tax_account'],
                is_system=account_data['is_system']
            )
        except Exception as e:
            logger.error(f"فشل في الحصول على الحساب: {str(e)}")
            return None
    
    def get_accounts(self, company_id: int, account_type: Optional[str] = None, is_active: bool = True) -> List[Account]:
        """الحصول على قائمة الحسابات"""
        try:
            params = [company_id]
            query = """
                SELECT * FROM erp.chart_of_accounts
                WHERE company_id = %s
            """
            
            if account_type:
                query += " AND account_type = %s"
                params.append(account_type)
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            query += " ORDER BY account_code"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            accounts = []
            for account_data in result:
                account = Account(
                    account_id=account_data['account_id'],
                    account_code=account_data['account_code'],
                    account_name=account_data['account_name'],
                    account_type=account_data['account_type'],
                    parent_account_id=account_data['parent_account_id'],
                    description=account_data['description'],
                    is_active=account_data['is_active'],
                    created_at=account_data['created_at'],
                    updated_at=account_data['updated_at'],
                    created_by=account_data['created_by'],
                    updated_by=account_data['updated_by'],
                    company_id=account_data['company_id'],
                    balance_type=account_data['balance_type'],
                    level=account_data['level'],
                    is_group=account_data['is_group'],
                    is_control_account=account_data['is_control_account'],
                    is_cash_account=account_data['is_cash_account'],
                    is_bank_account=account_data['is_bank_account'],
                    is_tax_account=account_data['is_tax_account'],
                    is_system=account_data['is_system']
                )
                accounts.append(account)
            
            return accounts
        except Exception as e:
            logger.error(f"فشل في الحصول على قائمة الحسابات: {str(e)}")
            return []
    
    def create_account(self, account: Account, user_id: int) -> Optional[int]:
        """إنشاء حساب جديد"""
        try:
            # التحقق من عدم وجود حساب بنفس الكود
            existing_account = self.get_account_by_code(account.account_code, account.company_id)
            if existing_account:
                logger.error(f"يوجد حساب بنفس الكود: {account.account_code}")
                return None
            
            # إذا كان الحساب له أب، تحقق من وجوده
            if account.parent_account_id:
                parent_account = self.get_account_by_id(account.parent_account_id, account.company_id)
                if not parent_account:
                    logger.error(f"الحساب الأب غير موجود: {account.parent_account_id}")
                    return None
                
                # تعيين المستوى بناءً على مستوى الأب
                account.level = parent_account.level + 1
            
            query = """
                INSERT INTO erp.chart_of_accounts (
                    account_code, account_name, account_type, parent_account_id,
                    description, is_active, created_by, updated_by, company_id,
                    balance_type, level, is_group, is_control_account,
                    is_cash_account, is_bank_account, is_tax_account, is_system
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING account_id
            """
            
            params = (
                account.account_code, account.account_name, account.account_type,
                account.parent_account_id, account.description, account.is_active,
                user_id, user_id, account.company_id, account.balance_type,
                account.level, account.is_group, account.is_control_account,
                account.is_cash_account, account.is_bank_account, account.is_tax_account,
                account.is_system
            )
            
            result = self.db_manager.execute_query(query, params)
            
            if result:
                account_id = result[0]['account_id']
                logger.info(f"تم إنشاء الحساب بنجاح: {account_id}")
                return account_id
            
            return None
        except Exception as e:
            logger.error(f"فشل في إنشاء الحساب: {str(e)}")
            return None
    
    def update_account(self, account: Account, user_id: int) -> bool:
        """تحديث حساب"""
        try:
            # التحقق من وجود الحساب
            existing_account = self.get_account_by_id(account.account_id, account.company_id)
            if not existing_account:
                logger.error(f"الحساب غير موجود: {account.account_id}")
                return False
            
            # التحقق من عدم وجود حساب آخر بنفس الكود
            if account.account_code != existing_account.account_code:
                other_account = self.get_account_by_code(account.account_code, account.company_id)
                if other_account and other_account.account_id != account.account_id:
                    logger.error(f"يوجد حساب آخر بنفس الكود: {account.account_code}")
                    return False
            
            # إذا كان الحساب له أب، تحقق من وجوده
            if account.parent_account_id:
                parent_account = self.get_account_by_id(account.parent_account_id, account.company_id)
                if not parent_account:
                    logger.error(f"الحساب الأب غير موجود: {account.parent_account_id}")
                    return False
                
                # تعيين المستوى بناءً على مستوى الأب
                account.level = parent_account.level + 1
            
            query = """
                UPDATE erp.chart_of_accounts SET
                    account_code = %s,
                    account_name = %s,
                    account_type = %s,
                    parent_account_id = %s,
                    description = %s,
                    is_active = %s,
                    updated_by = %s,
                    updated_at = CURRENT_TIMESTAMP,
                    balance_type = %s,
                    level = %s,
                    is_group = %s,
                    is_control_account = %s,
                    is_cash_account = %s,
                    is_bank_account = %s,
                    is_tax_account = %s,
                    is_system = %s
                WHERE account_id = %s AND company_id = %s
            """
            
            params = (
                account.account_code, account.account_name, account.account_type,
                account.parent_account_id, account.description, account.is_active,
                user_id, account.balance_type, account.level, account.is_group,
                account.is_control_account, account.is_cash_account, account.is_bank_account,
                account.is_tax_account, account.is_system, account.account_id, account.company_id
            )
            
            self.db_manager.execute_query(query, params, fetch=False)
            
            logger.info(f"تم تحديث الحساب بنجاح: {account.account_id}")
            return True
        except Exception as e:
            logger.error(f"فشل في تحديث الحساب: {str(e)}")
            return False
    
    def delete_account(self, account_id: int, company_id: int) -> bool:
        """حذف حساب"""
        try:
            # التحقق من وجود الحساب
            existing_account = self.get_account_by_id(account_id, company_id)
            if not existing_account:
                logger.error(f"الحساب غير موجود: {account_id}")
                return False
            
            # التحقق من عدم وجود حسابات فرعية
            query = """
                SELECT COUNT(*) as count FROM erp.chart_of_accounts
                WHERE parent_account_id = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (account_id, company_id))
            
            if result[0]['count'] > 0:
                logger.error(f"لا يمكن حذف الحساب لأنه يحتوي على حسابات فرعية: {account_id}")
                return False
            
            # التحقق من عدم وجود حركات على الحساب
            query = """
                SELECT COUNT(*) as count FROM erp.journal_items
                WHERE account_id = %s
            """
            result = self.db_manager.execute_query(query, (account_id,))
            
            if result[0]['count'] > 0:
                logger.error(f"لا يمكن حذف الحساب لأنه يحتوي على حركات: {account_id}")
                return False
            
            # حذف الحساب
            query = """
                DELETE FROM erp.chart_of_accounts
                WHERE account_id = %s AND company_id = %s
            """
            self.db_manager.execute_query(query, (account_id, company_id), fetch=False)
            
            logger.info(f"تم حذف الحساب بنجاح: {account_id}")
            return True
        except Exception as e:
            logger.error(f"فشل في حذف الحساب: {str(e)}")
            return False
    
    def get_account_balance(self, account_id: int, period_id: int, company_id: int, branch_id: Optional[int] = None, currency_code: str = "USD") -> Optional[AccountBalance]:
        """الحصول على رصيد الحساب"""
        try:
            params = [account_id, period_id, company_id, currency_code]
            query = """
                SELECT * FROM erp.account_balances
                WHERE account_id = %s AND period_id = %s AND company_id = %s AND currency_code = %s
            """
            
            if branch_id:
                query += " AND branch_id = %s"
                params.append(branch_id)
            else:
                query += " AND branch_id IS NULL"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            if not result:
                return None
            
            balance_data = result[0]
            balance = AccountBalance(
                balance_id=balance_data['balance_id'],
                account_id=balance_data['account_id'],
                period_id=balance_data['period_id'],
                opening_debit=balance_data['opening_debit'],
                opening_credit=balance_data['opening_credit'],
                period_debit=balance_data['period_debit'],
                period_credit=balance_data['period_credit'],
                closing_debit=balance_data['closing_debit'],
                closing_credit=balance_data['closing_credit'],
                currency_code=balance_data['currency_code'],
                company_id=balance_data['company_id'],
                branch_id=balance_data['branch_id'],
                created_at=balance_data['created_at'],
                updated_at=balance_data['updated_at']
            )
            
            return balance
        except Exception as e:
            logger.error(f"فشل في الحصول على رصيد الحساب: {str(e)}")
            return None
    
    def get_account_tree(self, company_id: int, is_active: bool = True) -> List[Dict[str, Any]]:
        """الحصول على شجرة الحسابات"""
        try:
            # الحصول على جميع الحسابات
            accounts = self.get_accounts(company_id, is_active=is_active)
            
            # بناء شجرة الحسابات
            account_map = {account.account_id: account.to_dict() for account in accounts}
            
            # إضافة الأبناء لكل حساب
            for account in accounts:
                if account.parent_account_id:
                    parent_dict = account_map.get(account.parent_account_id)
                    if parent_dict:
                        if 'children' not in parent_dict:
                            parent_dict['children'] = []
                        parent_dict['children'].append(account_map[account.account_id])
            
            # الحصول على الحسابات الجذرية (التي ليس لها أب)
            root_accounts = [account_map[account.account_id] for account in accounts if not account.parent_account_id]
            
            return root_accounts
        except Exception as e:
            logger.error(f"فشل في الحصول على شجرة الحسابات: {str(e)}")
            return []


class JournalService:
    """خدمة إدارة قيود اليومية"""
    
    def __init__(self, db_manager=None):
        """تهيئة خدمة قيود اليومية"""
        from src.core.database.db_manager import DatabaseManager
        self.db_manager = db_manager or DatabaseManager()
        self.account_service = AccountService(db_manager)
    
    def get_journal_entry_by_id(self, entry_id: int, company_id: int) -> Optional[JournalEntry]:
        """الحصول على قيد يومية بواسطة المعرف"""
        try:
            # الحصول على بيانات القيد
            query = """
                SELECT * FROM erp.journal_entries
                WHERE entry_id = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (entry_id, company_id))
            
            if not result:
                return None
            
            entry_data = result[0]
            
            # الحصول على بنود القيد
            query = """
                SELECT * FROM erp.journal_items
                WHERE entry_id = %s
            """
            items_result = self.db_manager.execute_query(query, (entry_id,))
            
            # إنشاء كائن قيد اليومية
            entry = JournalEntry(
                entry_id=entry_data['entry_id'],
                entry_number=entry_data['entry_number'],
                entry_date=entry_data['entry_date'],
                posting_date=entry_data['posting_date'],
                reference_number=entry_data['reference_number'],
                source_document=entry_data['source_document'],
                source_id=entry_data['source_id'],
                description=entry_data['description'],
                is_posted=entry_data['is_posted'],
                is_reversed=entry_data['is_reversed'],
                reversed_entry_id=entry_data['reversed_entry_id'],
                company_id=entry_data['company_id'],
                branch_id=entry_data['branch_id'],
                period_id=entry_data['period_id'],
                currency_code=entry_data['currency_code'],
                exchange_rate=entry_data['exchange_rate'],
                total_debit=entry_data['total_debit'],
                total_credit=entry_data['total_credit'],
                created_at=entry_data['created_at'],
                updated_at=entry_data['updated_at'],
                created_by=entry_data['created_by'],
                updated_by=entry_data['updated_by'],
                approved_by=entry_data['approved_by'],
                approved_at=entry_data['approved_at'],
                entry_type=entry_data['entry_type']
            )
            
            # إضافة البنود
            for item_data in items_result:
                item = JournalItem(
                    item_id=item_data['item_id'],
                    entry_id=item_data['entry_id'],
                    account_id=item_data['account_id'],
                    description=item_data['description'],
                    debit=item_data['debit'],
                    credit=item_data['credit'],
                    currency_code=item_data['currency_code'],
                    exchange_rate=item_data['exchange_rate'],
                    debit_foreign=item_data['debit_foreign'],
                    credit_foreign=item_data['credit_foreign'],
                    cost_center_id=item_data['cost_center_id'],
                    project_id=item_data['project_id'],
                    dimension1_id=item_data['dimension1_id'],
                    dimension2_id=item_data['dimension2_id'],
                    created_at=item_data['created_at'],
                    updated_at=item_data['updated_at']
                )
                entry.items.append(item)
            
            return entry
        except Exception as e:
            logger.error(f"فشل في الحصول على قيد اليومية: {str(e)}")
            return None
    
    def get_journal_entries(self, company_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, entry_type: Optional[str] = None, is_posted: Optional[bool] = None) -> List[JournalEntry]:
        """الحصول على قيود اليومية"""
        try:
            params = [company_id]
            query = """
                SELECT * FROM erp.journal_entries
                WHERE company_id = %s
            """
            
            if start_date:
                query += " AND entry_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND entry_date <= %s"
                params.append(end_date)
            
            if entry_type:
                query += " AND entry_type = %s"
                params.append(entry_type)
            
            if is_posted is not None:
                query += " AND is_posted = %s"
                params.append(is_posted)
            
            query += " ORDER BY entry_date DESC, entry_id DESC"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            entries = []
            for entry_data in result:
                # الحصول على بنود القيد
                query = """
                    SELECT * FROM erp.journal_items
                    WHERE entry_id = %s
                """
                items_result = self.db_manager.execute_query(query, (entry_data['entry_id'],))
                
                # إنشاء كائن قيد اليومية
                entry = JournalEntry(
                    entry_id=entry_data['entry_id'],
                    entry_number=entry_data['entry_number'],
                    entry_date=entry_data['entry_date'],
                    posting_date=entry_data['posting_date'],
                    reference_number=entry_data['reference_number'],
                    source_document=entry_data['source_document'],
                    source_id=entry_data['source_id'],
                    description=entry_data['description'],
                    is_posted=entry_data['is_posted'],
                    is_reversed=entry_data['is_reversed'],
                    reversed_entry_id=entry_data['reversed_entry_id'],
                    company_id=entry_data['company_id'],
                    branch_id=entry_data['branch_id'],
                    period_id=entry_data['period_id'],
                    currency_code=entry_data['currency_code'],
                    exchange_rate=entry_data['exchange_rate'],
                    total_debit=entry_data['total_debit'],
                    total_credit=entry_data['total_credit'],
                    created_at=entry_data['created_at'],
                    updated_at=entry_data['updated_at'],
                    created_by=entry_data['created_by'],
                    updated_by=entry_data['updated_by'],
                    approved_by=entry_data['approved_by'],
                    approved_at=entry_data['approved_at'],
                    entry_type=entry_data['entry_type']
                )
                
                # إضافة البنود
                for item_data in items_result:
                    item = JournalItem(
                        item_id=item_data['item_id'],
                        entry_id=item_data['entry_id'],
                        account_id=item_data['account_id'],
                        description=item_data['description'],
                        debit=item_data['debit'],
                        credit=item_data['credit'],
                        currency_code=item_data['currency_code'],
                        exchange_rate=item_data['exchange_rate'],
                        debit_foreign=item_data['debit_foreign'],
                        credit_foreign=item_data['credit_foreign'],
                        cost_center_id=item_data['cost_center_id'],
                        project_id=item_data['project_id'],
                        dimension1_id=item_data['dimension1_id'],
                        dimension2_id=item_data['dimension2_id'],
                        created_at=item_data['created_at'],
                        updated_at=item_data['updated_at']
                    )
                    entry.items.append(item)
                
                entries.append(entry)
            
            return entries
        except Exception as e:
            logger.error(f"فشل في الحصول على قيود اليومية: {str(e)}")
            return []
    
    def create_journal_entry(self, entry: JournalEntry, user_id: int) -> Optional[int]:
        """إنشاء قيد يومية جديد"""
        try:
            # التحقق من توازن القيد
            if not entry.is_balanced():
                logger.error("القيد غير متوازن")
                return None
            
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # إنشاء رقم القيد
                if not entry.entry_number:
                    entry.entry_number = self._generate_entry_number(entry.company_id, entry.entry_type)
                
                # إدخال القيد
                query = """
                    INSERT INTO erp.journal_entries (
                        entry_number, entry_date, posting_date, reference_number,
                        source_document, source_id, description, is_posted,
                        is_reversed, reversed_entry_id, company_id, branch_id,
                        period_id, currency_code, exchange_rate, total_debit,
                        total_credit, created_by, updated_by, entry_type
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING entry_id
                """
                
                params = (
                    entry.entry_number, entry.entry_date, entry.posting_date,
                    entry.reference_number, entry.source_document, entry.source_id,
                    entry.description, entry.is_posted, entry.is_reversed,
                    entry.reversed_entry_id, entry.company_id, entry.branch_id,
                    entry.period_id, entry.currency_code, entry.exchange_rate,
                    entry.total_debit, entry.total_credit, user_id, user_id,
                    entry.entry_type
                )
                
                result = self.db_manager.execute_query(query, params)
                
                if not result:
                    raise Exception("فشل في إنشاء قيد اليومية")
                
                entry_id = result[0]['entry_id']
                
                # إدخال بنود القيد
                for item in entry.items:
                    query = """
                        INSERT INTO erp.journal_items (
                            entry_id, account_id, description, debit, credit,
                            currency_code, exchange_rate, debit_foreign, credit_foreign,
                            cost_center_id, project_id, dimension1_id, dimension2_id
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    
                    params = (
                        entry_id, item.account_id, item.description, item.debit,
                        item.credit, item.currency_code, item.exchange_rate,
                        item.debit_foreign, item.credit_foreign, item.cost_center_id,
                        item.project_id, item.dimension1_id, item.dimension2_id
                    )
                    
                    self.db_manager.execute_query(query, params, fetch=False)
                
                # ترحيل القيد إذا كان مطلوبًا
                if entry.is_posted:
                    self._post_journal_entry(entry_id, user_id)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم إنشاء قيد اليومية بنجاح: {entry_id}")
                return entry_id
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في إنشاء قيد اليومية: {str(e)}")
            return None
    
    def update_journal_entry(self, entry: JournalEntry, user_id: int) -> bool:
        """تحديث قيد يومية"""
        try:
            # التحقق من وجود القيد
            existing_entry = self.get_journal_entry_by_id(entry.entry_id, entry.company_id)
            if not existing_entry:
                logger.error(f"القيد غير موجود: {entry.entry_id}")
                return False
            
            # التحقق من أن القيد غير مرحل
            if existing_entry.is_posted:
                logger.error(f"لا يمكن تحديث قيد مرحل: {entry.entry_id}")
                return False
            
            # التحقق من توازن القيد
            if not entry.is_balanced():
                logger.error("القيد غير متوازن")
                return False
            
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # تحديث القيد
                query = """
                    UPDATE erp.journal_entries SET
                        entry_date = %s,
                        posting_date = %s,
                        reference_number = %s,
                        source_document = %s,
                        source_id = %s,
                        description = %s,
                        is_posted = %s,
                        currency_code = %s,
                        exchange_rate = %s,
                        total_debit = %s,
                        total_credit = %s,
                        updated_by = %s,
                        updated_at = CURRENT_TIMESTAMP,
                        entry_type = %s
                    WHERE entry_id = %s AND company_id = %s
                """
                
                params = (
                    entry.entry_date, entry.posting_date, entry.reference_number,
                    entry.source_document, entry.source_id, entry.description,
                    entry.is_posted, entry.currency_code, entry.exchange_rate,
                    entry.total_debit, entry.total_credit, user_id, entry.entry_type,
                    entry.entry_id, entry.company_id
                )
                
                self.db_manager.execute_query(query, params, fetch=False)
                
                # حذف البنود الحالية
                query = """
                    DELETE FROM erp.journal_items
                    WHERE entry_id = %s
                """
                self.db_manager.execute_query(query, (entry.entry_id,), fetch=False)
                
                # إدخال البنود الجديدة
                for item in entry.items:
                    query = """
                        INSERT INTO erp.journal_items (
                            entry_id, account_id, description, debit, credit,
                            currency_code, exchange_rate, debit_foreign, credit_foreign,
                            cost_center_id, project_id, dimension1_id, dimension2_id
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    
                    params = (
                        entry.entry_id, item.account_id, item.description, item.debit,
                        item.credit, item.currency_code, item.exchange_rate,
                        item.debit_foreign, item.credit_foreign, item.cost_center_id,
                        item.project_id, item.dimension1_id, item.dimension2_id
                    )
                    
                    self.db_manager.execute_query(query, params, fetch=False)
                
                # ترحيل القيد إذا كان مطلوبًا
                if entry.is_posted and not existing_entry.is_posted:
                    self._post_journal_entry(entry.entry_id, user_id)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم تحديث قيد اليومية بنجاح: {entry.entry_id}")
                return True
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في تحديث قيد اليومية: {str(e)}")
            return False
    
    def delete_journal_entry(self, entry_id: int, company_id: int) -> bool:
        """حذف قيد يومية"""
        try:
            # التحقق من وجود القيد
            existing_entry = self.get_journal_entry_by_id(entry_id, company_id)
            if not existing_entry:
                logger.error(f"القيد غير موجود: {entry_id}")
                return False
            
            # التحقق من أن القيد غير مرحل
            if existing_entry.is_posted:
                logger.error(f"لا يمكن حذف قيد مرحل: {entry_id}")
                return False
            
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # حذف البنود
                query = """
                    DELETE FROM erp.journal_items
                    WHERE entry_id = %s
                """
                self.db_manager.execute_query(query, (entry_id,), fetch=False)
                
                # حذف القيد
                query = """
                    DELETE FROM erp.journal_entries
                    WHERE entry_id = %s AND company_id = %s
                """
                self.db_manager.execute_query(query, (entry_id, company_id), fetch=False)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم حذف قيد اليومية بنجاح: {entry_id}")
                return True
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في حذف قيد اليومية: {str(e)}")
            return False
    
    def post_journal_entry(self, entry_id: int, company_id: int, user_id: int) -> bool:
        """ترحيل قيد يومية"""
        try:
            # التحقق من وجود القيد
            existing_entry = self.get_journal_entry_by_id(entry_id, company_id)
            if not existing_entry:
                logger.error(f"القيد غير موجود: {entry_id}")
                return False
            
            # التحقق من أن القيد غير مرحل
            if existing_entry.is_posted:
                logger.error(f"القيد مرحل بالفعل: {entry_id}")
                return False
            
            # التحقق من توازن القيد
            if not existing_entry.is_balanced():
                logger.error(f"القيد غير متوازن: {entry_id}")
                return False
            
            # ترحيل القيد
            return self._post_journal_entry(entry_id, user_id)
        except Exception as e:
            logger.error(f"فشل في ترحيل قيد اليومية: {str(e)}")
            return False
    
    def _post_journal_entry(self, entry_id: int, user_id: int) -> bool:
        """ترحيل قيد يومية (داخلي)"""
        try:
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # الحصول على بيانات القيد
                entry = self.get_journal_entry_by_id(entry_id, None)
                if not entry:
                    raise Exception(f"القيد غير موجود: {entry_id}")
                
                # تحديث أرصدة الحسابات
                for item in entry.items:
                    # الحصول على رصيد الحساب
                    balance = self.account_service.get_account_balance(
                        item.account_id, entry.period_id, entry.company_id,
                        entry.branch_id, item.currency_code
                    )
                    
                    if balance:
                        # تحديث الرصيد
                        query = """
                            UPDATE erp.account_balances SET
                                period_debit = period_debit + %s,
                                period_credit = period_credit + %s,
                                closing_debit = opening_debit + period_debit + %s,
                                closing_credit = opening_credit + period_credit + %s,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE balance_id = %s
                        """
                        
                        params = (
                            item.debit, item.credit, item.debit, item.credit, balance.balance_id
                        )
                        
                        self.db_manager.execute_query(query, params, fetch=False)
                    else:
                        # إنشاء رصيد جديد
                        query = """
                            INSERT INTO erp.account_balances (
                                account_id, period_id, opening_debit, opening_credit,
                                period_debit, period_credit, closing_debit, closing_credit,
                                currency_code, company_id, branch_id
                            ) VALUES (
                                %s, %s, 0, 0, %s, %s, %s, %s, %s, %s, %s
                            )
                        """
                        
                        params = (
                            item.account_id, entry.period_id, item.debit, item.credit,
                            item.debit, item.credit, item.currency_code,
                            entry.company_id, entry.branch_id
                        )
                        
                        self.db_manager.execute_query(query, params, fetch=False)
                
                # تحديث حالة القيد
                query = """
                    UPDATE erp.journal_entries SET
                        is_posted = TRUE,
                        approved_by = %s,
                        approved_at = CURRENT_TIMESTAMP,
                        updated_by = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE entry_id = %s
                """
                
                params = (user_id, user_id, entry_id)
                
                self.db_manager.execute_query(query, params, fetch=False)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم ترحيل قيد اليومية بنجاح: {entry_id}")
                return True
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في ترحيل قيد اليومية: {str(e)}")
            return False
    
    def _generate_entry_number(self, company_id: int, entry_type: str) -> str:
        """توليد رقم قيد جديد"""
        try:
            # الحصول على آخر رقم قيد
            query = """
                SELECT MAX(CAST(SUBSTRING(entry_number FROM '[0-9]+') AS INTEGER)) as last_number
                FROM erp.journal_entries
                WHERE company_id = %s AND entry_type = %s AND entry_number ~ '^[A-Z]+-[0-9]+$'
            """
            
            result = self.db_manager.execute_query(query, (company_id, entry_type))
            
            last_number = result[0]['last_number'] if result[0]['last_number'] else 0
            next_number = last_number + 1
            
            # توليد رقم القيد
            prefix = entry_type.upper()[:3]
            entry_number = f"{prefix}-{next_number:06d}"
            
            return entry_number
        except Exception as e:
            logger.error(f"فشل في توليد رقم قيد جديد: {str(e)}")
            # رقم قيد افتراضي
            return f"{entry_type.upper()[:3]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"


class CustomerService:
    """خدمة إدارة العملاء"""
    
    def __init__(self, db_manager=None):
        """تهيئة خدمة العملاء"""
        from src.core.database.db_manager import DatabaseManager
        self.db_manager = db_manager or DatabaseManager()
    
    def get_customer_by_id(self, customer_id: int, company_id: int) -> Optional[Customer]:
        """الحصول على عميل بواسطة المعرف"""
        try:
            query = """
                SELECT * FROM erp.customers
                WHERE customer_id = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (customer_id, company_id))
            
            if not result:
                return None
            
            customer_data = result[0]
            return Customer(
                customer_id=customer_data['customer_id'],
                customer_code=customer_data['customer_code'],
                customer_name=customer_data['customer_name'],
                contact_person=customer_data['contact_person'],
                phone=customer_data['phone'],
                mobile=customer_data['mobile'],
                email=customer_data['email'],
                address=customer_data['address'],
                city=customer_data['city'],
                state=customer_data['state'],
                country=customer_data['country'],
                postal_code=customer_data['postal_code'],
                tax_id=customer_data['tax_id'],
                credit_limit=customer_data['credit_limit'],
                payment_terms=customer_data['payment_terms'],
                is_active=customer_data['is_active'],
                account_id=customer_data['account_id'],
                company_id=customer_data['company_id'],
                created_at=customer_data['created_at'],
                updated_at=customer_data['updated_at'],
                created_by=customer_data['created_by'],
                updated_by=customer_data['updated_by']
            )
        except Exception as e:
            logger.error(f"فشل في الحصول على العميل: {str(e)}")
            return None
    
    def get_customers(self, company_id: int, is_active: bool = True) -> List[Customer]:
        """الحصول على قائمة العملاء"""
        try:
            params = [company_id]
            query = """
                SELECT * FROM erp.customers
                WHERE company_id = %s
            """
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            query += " ORDER BY customer_name"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            customers = []
            for customer_data in result:
                customer = Customer(
                    customer_id=customer_data['customer_id'],
                    customer_code=customer_data['customer_code'],
                    customer_name=customer_data['customer_name'],
                    contact_person=customer_data['contact_person'],
                    phone=customer_data['phone'],
                    mobile=customer_data['mobile'],
                    email=customer_data['email'],
                    address=customer_data['address'],
                    city=customer_data['city'],
                    state=customer_data['state'],
                    country=customer_data['country'],
                    postal_code=customer_data['postal_code'],
                    tax_id=customer_data['tax_id'],
                    credit_limit=customer_data['credit_limit'],
                    payment_terms=customer_data['payment_terms'],
                    is_active=customer_data['is_active'],
                    account_id=customer_data['account_id'],
                    company_id=customer_data['company_id'],
                    created_at=customer_data['created_at'],
                    updated_at=customer_data['updated_at'],
                    created_by=customer_data['created_by'],
                    updated_by=customer_data['updated_by']
                )
                customers.append(customer)
            
            return customers
        except Exception as e:
            logger.error(f"فشل في الحصول على قائمة العملاء: {str(e)}")
            return []
    
    def create_customer(self, customer: Customer, user_id: int) -> Optional[int]:
        """إنشاء عميل جديد"""
        try:
            # التحقق من عدم وجود عميل بنفس الكود
            query = """
                SELECT customer_id FROM erp.customers
                WHERE customer_code = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (customer.customer_code, customer.company_id))
            
            if result:
                logger.error(f"يوجد عميل بنفس الكود: {customer.customer_code}")
                return None
            
            query = """
                INSERT INTO erp.customers (
                    customer_code, customer_name, contact_person, phone, mobile,
                    email, address, city, state, country, postal_code, tax_id,
                    credit_limit, payment_terms, is_active, account_id, company_id,
                    created_by, updated_by
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING customer_id
            """
            
            params = (
                customer.customer_code, customer.customer_name, customer.contact_person,
                customer.phone, customer.mobile, customer.email, customer.address,
                customer.city, customer.state, customer.country, customer.postal_code,
                customer.tax_id, customer.credit_limit, customer.payment_terms,
                customer.is_active, customer.account_id, customer.company_id,
                user_id, user_id
            )
            
            result = self.db_manager.execute_query(query, params)
            
            if result:
                customer_id = result[0]['customer_id']
                logger.info(f"تم إنشاء العميل بنجاح: {customer_id}")
                return customer_id
            
            return None
        except Exception as e:
            logger.error(f"فشل في إنشاء العميل: {str(e)}")
            return None
    
    def update_customer(self, customer: Customer, user_id: int) -> bool:
        """تحديث عميل"""
        try:
            # التحقق من وجود العميل
            existing_customer = self.get_customer_by_id(customer.customer_id, customer.company_id)
            if not existing_customer:
                logger.error(f"العميل غير موجود: {customer.customer_id}")
                return False
            
            # التحقق من عدم وجود عميل آخر بنفس الكود
            if customer.customer_code != existing_customer.customer_code:
                query = """
                    SELECT customer_id FROM erp.customers
                    WHERE customer_code = %s AND company_id = %s AND customer_id != %s
                """
                result = self.db_manager.execute_query(query, (customer.customer_code, customer.company_id, customer.customer_id))
                
                if result:
                    logger.error(f"يوجد عميل آخر بنفس الكود: {customer.customer_code}")
                    return False
            
            query = """
                UPDATE erp.customers SET
                    customer_code = %s,
                    customer_name = %s,
                    contact_person = %s,
                    phone = %s,
                    mobile = %s,
                    email = %s,
                    address = %s,
                    city = %s,
                    state = %s,
                    country = %s,
                    postal_code = %s,
                    tax_id = %s,
                    credit_limit = %s,
                    payment_terms = %s,
                    is_active = %s,
                    account_id = %s,
                    updated_by = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE customer_id = %s AND company_id = %s
            """
            
            params = (
                customer.customer_code, customer.customer_name, customer.contact_person,
                customer.phone, customer.mobile, customer.email, customer.address,
                customer.city, customer.state, customer.country, customer.postal_code,
                customer.tax_id, customer.credit_limit, customer.payment_terms,
                customer.is_active, customer.account_id, user_id,
                customer.customer_id, customer.company_id
            )
            
            self.db_manager.execute_query(query, params, fetch=False)
            
            logger.info(f"تم تحديث العميل بنجاح: {customer.customer_id}")
            return True
        except Exception as e:
            logger.error(f"فشل في تحديث العميل: {str(e)}")
            return False
    
    def delete_customer(self, customer_id: int, company_id: int) -> bool:
        """حذف عميل"""
        try:
            # التحقق من وجود العميل
            existing_customer = self.get_customer_by_id(customer_id, company_id)
            if not existing_customer:
                logger.error(f"العميل غير موجود: {customer_id}")
                return False
            
            # التحقق من عدم وجود فواتير للعميل
            query = """
                SELECT COUNT(*) as count FROM erp.sales_invoices
                WHERE customer_id = %s
            """
            result = self.db_manager.execute_query(query, (customer_id,))
            
            if result[0]['count'] > 0:
                logger.error(f"لا يمكن حذف العميل لأنه يحتوي على فواتير: {customer_id}")
                return False
            
            # حذف العميل
            query = """
                DELETE FROM erp.customers
                WHERE customer_id = %s AND company_id = %s
            """
            self.db_manager.execute_query(query, (customer_id, company_id), fetch=False)
            
            logger.info(f"تم حذف العميل بنجاح: {customer_id}")
            return True
        except Exception as e:
            logger.error(f"فشل في حذف العميل: {str(e)}")
            return False
    
    def get_customer_balance(self, customer_id: int, company_id: int, as_of_date: Optional[datetime] = None) -> Decimal:
        """الحصول على رصيد العميل"""
        try:
            params = [customer_id]
            query = """
                SELECT
                    COALESCE(SUM(si.total_amount), 0) as total_invoices,
                    COALESCE(SUM(si.paid_amount), 0) as total_payments
                FROM erp.sales_invoices si
                WHERE si.customer_id = %s
            """
            
            if as_of_date:
                query += " AND si.invoice_date <= %s"
                params.append(as_of_date)
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            if not result:
                return Decimal("0.0")
            
            total_invoices = result[0]['total_invoices'] or Decimal("0.0")
            total_payments = result[0]['total_payments'] or Decimal("0.0")
            
            return total_invoices - total_payments
        except Exception as e:
            logger.error(f"فشل في الحصول على رصيد العميل: {str(e)}")
            return Decimal("0.0")
    
    def get_customer_invoices(self, customer_id: int, company_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """الحصول على فواتير العميل"""
        try:
            params = [customer_id]
            query = """
                SELECT
                    si.invoice_id,
                    si.invoice_number,
                    si.invoice_date,
                    si.due_date,
                    si.total_amount,
                    si.paid_amount,
                    si.balance_amount,
                    si.status
                FROM erp.sales_invoices si
                WHERE si.customer_id = %s
            """
            
            if start_date:
                query += " AND si.invoice_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND si.invoice_date <= %s"
                params.append(end_date)
            
            query += " ORDER BY si.invoice_date DESC, si.invoice_number"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            return result
        except Exception as e:
            logger.error(f"فشل في الحصول على فواتير العميل: {str(e)}")
            return []
    
    def get_customer_payments(self, customer_id: int, company_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """الحصول على مدفوعات العميل"""
        try:
            params = [customer_id]
            query = """
                SELECT
                    p.payment_id,
                    p.payment_number,
                    p.payment_date,
                    p.amount,
                    p.reference,
                    p.description
                FROM erp.payments p
                WHERE p.party_type = 'customer' AND p.party_id = %s
            """
            
            if start_date:
                query += " AND p.payment_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND p.payment_date <= %s"
                params.append(end_date)
            
            query += " ORDER BY p.payment_date DESC, p.payment_number"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            return result
        except Exception as e:
            logger.error(f"فشل في الحصول على مدفوعات العميل: {str(e)}")
            return []


class SalesInvoiceService:
    """خدمة إدارة فواتير المبيعات"""
    
    def __init__(self, db_manager=None):
        """تهيئة خدمة فواتير المبيعات"""
        from src.core.database.db_manager import DatabaseManager
        self.db_manager = db_manager or DatabaseManager()
        self.journal_service = JournalService(db_manager)
    
    def get_invoice_by_id(self, invoice_id: int, company_id: int) -> Optional[SalesInvoice]:
        """الحصول على فاتورة بواسطة المعرف"""
        try:
            # الحصول على بيانات الفاتورة
            query = """
                SELECT * FROM erp.sales_invoices
                WHERE invoice_id = %s AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (invoice_id, company_id))
            
            if not result:
                return None
            
            invoice_data = result[0]
            
            # الحصول على بنود الفاتورة
            query = """
                SELECT * FROM erp.sales_invoice_items
                WHERE invoice_id = %s
            """
            items_result = self.db_manager.execute_query(query, (invoice_id,))
            
            # إنشاء كائن الفاتورة
            invoice = SalesInvoice(
                invoice_id=invoice_data['invoice_id'],
                invoice_number=invoice_data['invoice_number'],
                invoice_date=invoice_data['invoice_date'],
                due_date=invoice_data['due_date'],
                customer_id=invoice_data['customer_id'],
                reference=invoice_data['reference'],
                description=invoice_data['description'],
                subtotal=invoice_data['subtotal'],
                tax_amount=invoice_data['tax_amount'],
                discount_amount=invoice_data['discount_amount'],
                total_amount=invoice_data['total_amount'],
                paid_amount=invoice_data['paid_amount'],
                balance_amount=invoice_data['balance_amount'],
                status=invoice_data['status'],
                is_posted=invoice_data['is_posted'],
                journal_entry_id=invoice_data['journal_entry_id'],
                company_id=invoice_data['company_id'],
                branch_id=invoice_data['branch_id'],
                currency_code=invoice_data['currency_code'],
                exchange_rate=invoice_data['exchange_rate'],
                created_at=invoice_data['created_at'],
                updated_at=invoice_data['updated_at'],
                created_by=invoice_data['created_by'],
                updated_by=invoice_data['updated_by']
            )
            
            # إضافة البنود
            for item_data in items_result:
                item = SalesInvoiceItem(
                    item_id=item_data['item_id'],
                    invoice_id=item_data['invoice_id'],
                    product_id=item_data['product_id'],
                    description=item_data['description'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    discount_percent=item_data['discount_percent'],
                    discount_amount=item_data['discount_amount'],
                    tax_percent=item_data['tax_percent'],
                    tax_amount=item_data['tax_amount'],
                    total_amount=item_data['total_amount'],
                    account_id=item_data['account_id'],
                    created_at=item_data['created_at'],
                    updated_at=item_data['updated_at']
                )
                invoice.items.append(item)
            
            return invoice
        except Exception as e:
            logger.error(f"فشل في الحصول على فاتورة المبيعات: {str(e)}")
            return None
    
    def get_invoices(self, company_id: int, customer_id: Optional[int] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, status: Optional[str] = None) -> List[SalesInvoice]:
        """الحصول على قائمة فواتير المبيعات"""
        try:
            params = [company_id]
            query = """
                SELECT * FROM erp.sales_invoices
                WHERE company_id = %s
            """
            
            if customer_id:
                query += " AND customer_id = %s"
                params.append(customer_id)
            
            if start_date:
                query += " AND invoice_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND invoice_date <= %s"
                params.append(end_date)
            
            if status:
                query += " AND status = %s"
                params.append(status)
            
            query += " ORDER BY invoice_date DESC, invoice_number"
            
            result = self.db_manager.execute_query(query, tuple(params))
            
            invoices = []
            for invoice_data in result:
                # الحصول على بنود الفاتورة
                query = """
                    SELECT * FROM erp.sales_invoice_items
                    WHERE invoice_id = %s
                """
                items_result = self.db_manager.execute_query(query, (invoice_data['invoice_id'],))
                
                # إنشاء كائن الفاتورة
                invoice = SalesInvoice(
                    invoice_id=invoice_data['invoice_id'],
                    invoice_number=invoice_data['invoice_number'],
                    invoice_date=invoice_data['invoice_date'],
                    due_date=invoice_data['due_date'],
                    customer_id=invoice_data['customer_id'],
                    reference=invoice_data['reference'],
                    description=invoice_data['description'],
                    subtotal=invoice_data['subtotal'],
                    tax_amount=invoice_data['tax_amount'],
                    discount_amount=invoice_data['discount_amount'],
                    total_amount=invoice_data['total_amount'],
                    paid_amount=invoice_data['paid_amount'],
                    balance_amount=invoice_data['balance_amount'],
                    status=invoice_data['status'],
                    is_posted=invoice_data['is_posted'],
                    journal_entry_id=invoice_data['journal_entry_id'],
                    company_id=invoice_data['company_id'],
                    branch_id=invoice_data['branch_id'],
                    currency_code=invoice_data['currency_code'],
                    exchange_rate=invoice_data['exchange_rate'],
                    created_at=invoice_data['created_at'],
                    updated_at=invoice_data['updated_at'],
                    created_by=invoice_data['created_by'],
                    updated_by=invoice_data['updated_by']
                )
                
                # إضافة البنود
                for item_data in items_result:
                    item = SalesInvoiceItem(
                        item_id=item_data['item_id'],
                        invoice_id=item_data['invoice_id'],
                        product_id=item_data['product_id'],
                        description=item_data['description'],
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        discount_percent=item_data['discount_percent'],
                        discount_amount=item_data['discount_amount'],
                        tax_percent=item_data['tax_percent'],
                        tax_amount=item_data['tax_amount'],
                        total_amount=item_data['total_amount'],
                        account_id=item_data['account_id'],
                        created_at=item_data['created_at'],
                        updated_at=item_data['updated_at']
                    )
                    invoice.items.append(item)
                
                invoices.append(invoice)
            
            return invoices
        except Exception as e:
            logger.error(f"فشل في الحصول على قائمة فواتير المبيعات: {str(e)}")
            return []
    
    def create_invoice(self, invoice: SalesInvoice, user_id: int) -> Optional[int]:
        """إنشاء فاتورة مبيعات جديدة"""
        try:
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # إنشاء رقم الفاتورة
                if not invoice.invoice_number:
                    invoice.invoice_number = self._generate_invoice_number(invoice.company_id)
                
                # حساب إجماليات الفاتورة
                invoice.subtotal = sum(item.total_amount for item in invoice.items)
                invoice.tax_amount = sum(item.tax_amount for item in invoice.items)
                invoice.total_amount = invoice.subtotal + invoice.tax_amount - invoice.discount_amount
                invoice.balance_amount = invoice.total_amount - invoice.paid_amount
                
                # إدخال الفاتورة
                query = """
                    INSERT INTO erp.sales_invoices (
                        invoice_number, invoice_date, due_date, customer_id,
                        reference, description, subtotal, tax_amount,
                        discount_amount, total_amount, paid_amount, balance_amount,
                        status, is_posted, company_id, branch_id,
                        currency_code, exchange_rate, created_by, updated_by
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING invoice_id
                """
                
                params = (
                    invoice.invoice_number, invoice.invoice_date, invoice.due_date,
                    invoice.customer_id, invoice.reference, invoice.description,
                    invoice.subtotal, invoice.tax_amount, invoice.discount_amount,
                    invoice.total_amount, invoice.paid_amount, invoice.balance_amount,
                    invoice.status, invoice.is_posted, invoice.company_id,
                    invoice.branch_id, invoice.currency_code, invoice.exchange_rate,
                    user_id, user_id
                )
                
                result = self.db_manager.execute_query(query, params)
                
                if not result:
                    raise Exception("فشل في إنشاء فاتورة المبيعات")
                
                invoice_id = result[0]['invoice_id']
                
                # إدخال بنود الفاتورة
                for item in invoice.items:
                    query = """
                        INSERT INTO erp.sales_invoice_items (
                            invoice_id, product_id, description, quantity,
                            unit_price, discount_percent, discount_amount,
                            tax_percent, tax_amount, total_amount, account_id
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    
                    params = (
                        invoice_id, item.product_id, item.description, item.quantity,
                        item.unit_price, item.discount_percent, item.discount_amount,
                        item.tax_percent, item.tax_amount, item.total_amount, item.account_id
                    )
                    
                    self.db_manager.execute_query(query, params, fetch=False)
                
                # ترحيل الفاتورة إذا كان مطلوبًا
                if invoice.is_posted:
                    journal_entry_id = self._post_invoice(invoice_id, user_id)
                    
                    if journal_entry_id:
                        # تحديث معرف قيد اليومية
                        query = """
                            UPDATE erp.sales_invoices SET
                                journal_entry_id = %s
                            WHERE invoice_id = %s
                        """
                        self.db_manager.execute_query(query, (journal_entry_id, invoice_id), fetch=False)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم إنشاء فاتورة المبيعات بنجاح: {invoice_id}")
                return invoice_id
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في إنشاء فاتورة المبيعات: {str(e)}")
            return None
    
    def update_invoice(self, invoice: SalesInvoice, user_id: int) -> bool:
        """تحديث فاتورة مبيعات"""
        try:
            # التحقق من وجود الفاتورة
            existing_invoice = self.get_invoice_by_id(invoice.invoice_id, invoice.company_id)
            if not existing_invoice:
                logger.error(f"الفاتورة غير موجودة: {invoice.invoice_id}")
                return False
            
            # التحقق من أن الفاتورة غير مرحلة
            if existing_invoice.is_posted:
                logger.error(f"لا يمكن تحديث فاتورة مرحلة: {invoice.invoice_id}")
                return False
            
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # حساب إجماليات الفاتورة
                invoice.subtotal = sum(item.total_amount for item in invoice.items)
                invoice.tax_amount = sum(item.tax_amount for item in invoice.items)
                invoice.total_amount = invoice.subtotal + invoice.tax_amount - invoice.discount_amount
                invoice.balance_amount = invoice.total_amount - invoice.paid_amount
                
                # تحديث الفاتورة
                query = """
                    UPDATE erp.sales_invoices SET
                        invoice_date = %s,
                        due_date = %s,
                        customer_id = %s,
                        reference = %s,
                        description = %s,
                        subtotal = %s,
                        tax_amount = %s,
                        discount_amount = %s,
                        total_amount = %s,
                        paid_amount = %s,
                        balance_amount = %s,
                        status = %s,
                        is_posted = %s,
                        branch_id = %s,
                        currency_code = %s,
                        exchange_rate = %s,
                        updated_by = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE invoice_id = %s AND company_id = %s
                """
                
                params = (
                    invoice.invoice_date, invoice.due_date, invoice.customer_id,
                    invoice.reference, invoice.description, invoice.subtotal,
                    invoice.tax_amount, invoice.discount_amount, invoice.total_amount,
                    invoice.paid_amount, invoice.balance_amount, invoice.status,
                    invoice.is_posted, invoice.branch_id, invoice.currency_code,
                    invoice.exchange_rate, user_id, invoice.invoice_id, invoice.company_id
                )
                
                self.db_manager.execute_query(query, params, fetch=False)
                
                # حذف البنود الحالية
                query = """
                    DELETE FROM erp.sales_invoice_items
                    WHERE invoice_id = %s
                """
                self.db_manager.execute_query(query, (invoice.invoice_id,), fetch=False)
                
                # إدخال البنود الجديدة
                for item in invoice.items:
                    query = """
                        INSERT INTO erp.sales_invoice_items (
                            invoice_id, product_id, description, quantity,
                            unit_price, discount_percent, discount_amount,
                            tax_percent, tax_amount, total_amount, account_id
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    
                    params = (
                        invoice.invoice_id, item.product_id, item.description, item.quantity,
                        item.unit_price, item.discount_percent, item.discount_amount,
                        item.tax_percent, item.tax_amount, item.total_amount, item.account_id
                    )
                    
                    self.db_manager.execute_query(query, params, fetch=False)
                
                # ترحيل الفاتورة إذا كان مطلوبًا
                if invoice.is_posted and not existing_invoice.is_posted:
                    journal_entry_id = self._post_invoice(invoice.invoice_id, user_id)
                    
                    if journal_entry_id:
                        # تحديث معرف قيد اليومية
                        query = """
                            UPDATE erp.sales_invoices SET
                                journal_entry_id = %s
                            WHERE invoice_id = %s
                        """
                        self.db_manager.execute_query(query, (journal_entry_id, invoice.invoice_id), fetch=False)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم تحديث فاتورة المبيعات بنجاح: {invoice.invoice_id}")
                return True
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في تحديث فاتورة المبيعات: {str(e)}")
            return False
    
    def delete_invoice(self, invoice_id: int, company_id: int) -> bool:
        """حذف فاتورة مبيعات"""
        try:
            # التحقق من وجود الفاتورة
            existing_invoice = self.get_invoice_by_id(invoice_id, company_id)
            if not existing_invoice:
                logger.error(f"الفاتورة غير موجودة: {invoice_id}")
                return False
            
            # التحقق من أن الفاتورة غير مرحلة
            if existing_invoice.is_posted:
                logger.error(f"لا يمكن حذف فاتورة مرحلة: {invoice_id}")
                return False
            
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # حذف البنود
                query = """
                    DELETE FROM erp.sales_invoice_items
                    WHERE invoice_id = %s
                """
                self.db_manager.execute_query(query, (invoice_id,), fetch=False)
                
                # حذف الفاتورة
                query = """
                    DELETE FROM erp.sales_invoices
                    WHERE invoice_id = %s AND company_id = %s
                """
                self.db_manager.execute_query(query, (invoice_id, company_id), fetch=False)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم حذف فاتورة المبيعات بنجاح: {invoice_id}")
                return True
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في حذف فاتورة المبيعات: {str(e)}")
            return False
    
    def post_invoice(self, invoice_id: int, company_id: int, user_id: int) -> bool:
        """ترحيل فاتورة مبيعات"""
        try:
            # التحقق من وجود الفاتورة
            existing_invoice = self.get_invoice_by_id(invoice_id, company_id)
            if not existing_invoice:
                logger.error(f"الفاتورة غير موجودة: {invoice_id}")
                return False
            
            # التحقق من أن الفاتورة غير مرحلة
            if existing_invoice.is_posted:
                logger.error(f"الفاتورة مرحلة بالفعل: {invoice_id}")
                return False
            
            # بدء المعاملة
            self.db_manager.begin_transaction()
            
            try:
                # ترحيل الفاتورة
                journal_entry_id = self._post_invoice(invoice_id, user_id)
                
                if not journal_entry_id:
                    raise Exception(f"فشل في ترحيل الفاتورة: {invoice_id}")
                
                # تحديث حالة الفاتورة
                query = """
                    UPDATE erp.sales_invoices SET
                        is_posted = TRUE,
                        journal_entry_id = %s,
                        status = 'approved',
                        updated_by = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE invoice_id = %s AND company_id = %s
                """
                
                params = (journal_entry_id, user_id, invoice_id, company_id)
                
                self.db_manager.execute_query(query, params, fetch=False)
                
                # إنهاء المعاملة
                self.db_manager.commit_transaction()
                
                logger.info(f"تم ترحيل فاتورة المبيعات بنجاح: {invoice_id}")
                return True
            except Exception as e:
                # التراجع عن المعاملة في حالة حدوث خطأ
                self.db_manager.rollback_transaction()
                raise e
        except Exception as e:
            logger.error(f"فشل في ترحيل فاتورة المبيعات: {str(e)}")
            return False
    
    def _post_invoice(self, invoice_id: int, user_id: int) -> Optional[int]:
        """ترحيل فاتورة مبيعات (داخلي)"""
        try:
            # الحصول على بيانات الفاتورة
            invoice = self.get_invoice_by_id(invoice_id, None)
            if not invoice:
                logger.error(f"الفاتورة غير موجودة: {invoice_id}")
                return None
            
            # الحصول على حساب العميل
            query = """
                SELECT account_id FROM erp.customers
                WHERE customer_id = %s
            """
            result = self.db_manager.execute_query(query, (invoice.customer_id,))
            
            if not result or not result[0]['account_id']:
                logger.error(f"حساب العميل غير موجود: {invoice.customer_id}")
                return None
            
            customer_account_id = result[0]['account_id']
            
            # الحصول على حساب المبيعات
            query = """
                SELECT account_id FROM erp.chart_of_accounts
                WHERE account_code = '4100' AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (invoice.company_id,))
            
            if not result:
                logger.error(f"حساب المبيعات غير موجود")
                return None
            
            sales_account_id = result[0]['account_id']
            
            # الحصول على حساب الضريبة
            query = """
                SELECT account_id FROM erp.chart_of_accounts
                WHERE account_code = '2200' AND company_id = %s
            """
            result = self.db_manager.execute_query(query, (invoice.company_id,))
            
            if not result:
                logger.error(f"حساب الضريبة غير موجود")
                return None
            
            tax_account_id = result[0]['account_id']
            
            # إنشاء قيد اليومية
            journal_entry = JournalEntry(
                entry_date=invoice.invoice_date,
                posting_date=invoice.invoice_date,
                reference_number=invoice.invoice_number,
                source_document="sales_invoice",
                source_id=str(invoice.invoice_id),
                description=f"فاتورة مبيعات: {invoice.invoice_number}",
                company_id=invoice.company_id,
                branch_id=invoice.branch_id,
                currency_code=invoice.currency_code,
                exchange_rate=invoice.exchange_rate,
                entry_type="sales"
            )
            
            # إضافة بند مدين (العميل)
            journal_entry.add_item(JournalItem(
                account_id=customer_account_id,
                description=f"فاتورة مبيعات: {invoice.invoice_number}",
                debit=invoice.total_amount,
                credit=Decimal("0.0"),
                currency_code=invoice.currency_code,
                exchange_rate=invoice.exchange_rate
            ))
            
            # إضافة بند دائن (المبيعات)
            journal_entry.add_item(JournalItem(
                account_id=sales_account_id,
                description=f"فاتورة مبيعات: {invoice.invoice_number}",
                debit=Decimal("0.0"),
                credit=invoice.subtotal,
                currency_code=invoice.currency_code,
                exchange_rate=invoice.exchange_rate
            ))
            
            # إضافة بند دائن (الضريبة) إذا كان هناك ضريبة
            if invoice.tax_amount > Decimal("0.0"):
                journal_entry.add_item(JournalItem(
                    account_id=tax_account_id,
                    description=f"ضريبة فاتورة مبيعات: {invoice.invoice_number}",
                    debit=Decimal("0.0"),
                    credit=invoice.tax_amount,
                    currency_code=invoice.currency_code,
                    exchange_rate=invoice.exchange_rate
                ))
            
            # إنشاء قيد اليومية
            journal_entry_id = self.journal_service.create_journal_entry(journal_entry, user_id)
            
            if not journal_entry_id:
                logger.error(f"فشل في إنشاء قيد اليومية للفاتورة: {invoice_id}")
                return None
            
            # ترحيل قيد اليومية
            if not self.journal_service.post_journal_entry(journal_entry_id, invoice.company_id, user_id):
                logger.error(f"فشل في ترحيل قيد اليومية للفاتورة: {invoice_id}")
                return None
            
            return journal_entry_id
        except Exception as e:
            logger.error(f"فشل في ترحيل فاتورة المبيعات: {str(e)}")
            return None
    
    def _generate_invoice_number(self, company_id: int) -> str:
        """توليد رقم فاتورة جديد"""
        try:
            # الحصول على آخر رقم فاتورة
            query = """
                SELECT MAX(CAST(SUBSTRING(invoice_number FROM '[0-9]+') AS INTEGER)) as last_number
                FROM erp.sales_invoices
                WHERE company_id = %s AND invoice_number ~ '^INV-[0-9]+$'
            """
            
            result = self.db_manager.execute_query(query, (company_id,))
            
            last_number = result[0]['last_number'] if result[0]['last_number'] else 0
            next_number = last_number + 1
            
            # توليد رقم الفاتورة
            invoice_number = f"INV-{next_number:06d}"
            
            return invoice_number
        except Exception as e:
            logger.error(f"فشل في توليد رقم فاتورة جديد: {str(e)}")
            # رقم فاتورة افتراضي
            return f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
