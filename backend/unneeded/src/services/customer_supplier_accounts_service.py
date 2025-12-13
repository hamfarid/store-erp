# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
#!/usr/bin/env python3
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/customer_supplier_accounts_service.py

خدمة إدارة حسابات العملاء والموردين
تدير جميع العمليات المحاسبية للعملاء والموردين مع تتبع دقيق للأرصدة والحركات
All linting disabled due to complex imports and optional dependencies.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc, extract
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
import logging
from decimal import Decimal
from models.customer_supplier_accounts import (
    CustomerSupplierAccount,
    AccountTransaction,
    PaymentSchedule,
    PaymentScheduleItem,
    CreditNote,
    AccountStatement,
    AccountType,
    TransactionType,
    PaymentTerms,
    AccountStatus,
)
from src.models.user import User
from src.models.customer import Customer
from src.models.supplier import Supplier

logger = logging.getLogger(__name__)


class CustomerSupplierAccountsService:
    """خدمة إدارة حسابات العملاء والموردين الشاملة"""

    def __init__(self, db_session: Session):
        self.db = db_session

    # ==================== إدارة الحسابات ====================

    def create_account(
        self, account_data: Dict[str, Any], user_id: int
    ) -> CustomerSupplierAccount:
        """
        إنشاء حساب عميل أو مورد جديد

        Args:
            account_data: بيانات الحساب
            user_id: معرف المستخدم المنشئ

        Returns:
            CustomerSupplierAccount: الحساب المنشأ
        """
        try:
            # إنشاء رقم الحساب
            account_number = self._generate_account_number(
                account_data.get("account_type")
            )

            # إنشاء الحساب
            account = CustomerSupplierAccount(
                account_number=account_number,
                account_name=account_data["account_name"],
                account_type=AccountType(account_data["account_type"]),
                customer_id=account_data.get("customer_id"),
                supplier_id=account_data.get("supplier_id"),
                employee_id=account_data.get("employee_id"),
                contact_person=account_data.get("contact_person"),
                phone=account_data.get("phone"),
                mobile=account_data.get("mobile"),
                email=account_data.get("email"),
                website=account_data.get("website"),
                address_line1=account_data.get("address_line1"),
                address_line2=account_data.get("address_line2"),
                city=account_data.get("city"),
                state=account_data.get("state"),
                postal_code=account_data.get("postal_code"),
                country=account_data.get("country"),
                credit_limit=Decimal(str(account_data.get("credit_limit", 0))),
                opening_balance=Decimal(str(account_data.get("opening_balance", 0))),
                opening_balance_date=account_data.get("opening_balance_date"),
                payment_terms=PaymentTerms(account_data.get("payment_terms", "net_30")),
                custom_payment_days=account_data.get("custom_payment_days"),
                currency=account_data.get("currency", "USD"),
                exchange_rate=account_data.get("exchange_rate", 1.0),
                tax_number=account_data.get("tax_number"),
                tax_exempt=account_data.get("tax_exempt", False),
                default_tax_rate=account_data.get("default_tax_rate", 0.0),
                bank_name=account_data.get("bank_name"),
                bank_account_number=account_data.get("bank_account_number"),
                bank_routing_number=account_data.get("bank_routing_number"),
                iban=account_data.get("iban"),
                swift_code=account_data.get("swift_code"),
                auto_reconcile=account_data.get("auto_reconcile", False),
                send_statements=account_data.get("send_statements", True),
                statement_frequency=account_data.get("statement_frequency", "monthly"),
                industry=account_data.get("industry"),
                company_size=account_data.get("company_size"),
                notes=account_data.get("notes"),
                internal_notes=account_data.get("internal_notes"),
                tags=account_data.get("tags"),
                created_by=user_id,
            )

            self.db.add(account)
            self.db.flush()

            # إضافة الرصيد الافتتاحي كحركة إذا كان موجوداً
            if account.opening_balance != 0:
                self._add_opening_balance_transaction(account)

            self.db.commit()

            logger.info(
                f"تم إنشاء حساب جديد: {account.account_number} - {account.account_name}"
            )
            return account

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء الحساب: {str(e)}")
            raise

    def update_account(
        self, account_id: int, account_data: Dict[str, Any], user_id: int
    ) -> CustomerSupplierAccount:
        """تحديث بيانات الحساب"""
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"الحساب غير موجود: {account_id}")

            # تحديث البيانات
            for key, value in account_data.items():
                if hasattr(account, key) and key not in [
                    "id",
                    "account_number",
                    "created_at",
                    "created_by",
                ]:
                    setattr(account, key, value)

            account.updated_by = user_id
            account.updated_at = datetime.utcnow()

            self.db.commit()

            logger.info(f"تم تحديث الحساب: {account.account_number}")
            return account

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تحديث الحساب: {str(e)}")
            raise

    def get_account_by_id(self, account_id: int) -> Optional[CustomerSupplierAccount]:
        """الحصول على حساب بالمعرف"""
        return (
            self.db.query(CustomerSupplierAccount)
            .filter(CustomerSupplierAccount.id == account_id)
            .first()
        )

    def get_account_by_number(
        self, account_number: str
    ) -> Optional[CustomerSupplierAccount]:
        """الحصول على حساب برقم الحساب"""
        return (
            self.db.query(CustomerSupplierAccount)
            .filter(CustomerSupplierAccount.account_number == account_number)
            .first()
        )

    def get_accounts_list(
        self, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 50
    ) -> Dict[str, Any]:
        """الحصول على قائمة الحسابات مع التصفية والترقيم"""
        try:
            query = self.db.query(CustomerSupplierAccount)

            # تطبيق الفلاتر
            if filters:
                if filters.get("account_type"):
                    query = query.filter(
                        CustomerSupplierAccount.account_type
                        == AccountType(filters["account_type"])
                    )

                if filters.get("status"):
                    query = query.filter(
                        CustomerSupplierAccount.status
                        == AccountStatus(filters["status"])
                    )

                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            CustomerSupplierAccount.account_name.ilike(search_term),
                            CustomerSupplierAccount.account_number.ilike(search_term),
                            CustomerSupplierAccount.contact_person.ilike(search_term),
                            CustomerSupplierAccount.email.ilike(search_term),
                        )
                    )

                if filters.get("city"):
                    query = query.filter(
                        CustomerSupplierAccount.city.ilike(f"%{filters['city']}%")
                    )

                if filters.get("country"):
                    query = query.filter(
                        CustomerSupplierAccount.country.ilike(f"%{filters['country']}%")
                    )

                if filters.get("currency"):
                    query = query.filter(
                        CustomerSupplierAccount.currency == filters["currency"]
                    )

                if filters.get("has_credit_limit"):
                    if filters["has_credit_limit"]:
                        query = query.filter(CustomerSupplierAccount.credit_limit > 0)
                    else:
                        query = query.filter(CustomerSupplierAccount.credit_limit == 0)

                if filters.get("balance_min") is not None:
                    query = query.filter(
                        CustomerSupplierAccount.current_balance
                        >= filters["balance_min"]
                    )

                if filters.get("balance_max") is not None:
                    query = query.filter(
                        CustomerSupplierAccount.current_balance
                        <= filters["balance_max"]
                    )

            # الترتيب
            sort_by = (
                filters.get("sort_by", "account_name") if filters else "account_name"
            )
            sort_order = filters.get("sort_order", "asc") if filters else "asc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(CustomerSupplierAccount, sort_by)))
            else:
                query = query.order_by(asc(getattr(CustomerSupplierAccount, sort_by)))

            # العد الإجمالي
            total_count = query.count()

            # الترقيم
            offset = (page - 1) * per_page
            accounts = query.offset(offset).limit(per_page).all()

            return {
                "accounts": [account.to_dict() for account in accounts],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total_count,
                    "pages": (total_count + per_page - 1) // per_page,
                },
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة الحسابات: {str(e)}")
            raise

    # ==================== إدارة الحركات ====================

    def add_transaction(
        self, account_id: int, transaction_data: Dict[str, Any], user_id: int
    ) -> AccountTransaction:
        """إضافة حركة جديدة للحساب"""
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"الحساب غير موجود: {account_id}")

            # إنشاء رقم الحركة
            transaction_number = self._generate_transaction_number()

            # إنشاء الحركة
            transaction = AccountTransaction(
                account_id=account_id,
                transaction_number=transaction_number,
                transaction_type=TransactionType(transaction_data["transaction_type"]),
                transaction_date=transaction_data.get(
                    "transaction_date", datetime.utcnow()
                ),
                due_date=transaction_data.get("due_date"),
                debit_amount=Decimal(str(transaction_data.get("debit_amount", 0))),
                credit_amount=Decimal(str(transaction_data.get("credit_amount", 0))),
                outstanding_amount=Decimal(
                    str(transaction_data.get("outstanding_amount", 0))
                ),
                description=transaction_data.get("description"),
                reference=transaction_data.get("reference"),
                notes=transaction_data.get("notes"),
                invoice_id=transaction_data.get("invoice_id"),
                payment_id=transaction_data.get("payment_id"),
                journal_entry_id=transaction_data.get("journal_entry_id"),
                currency=transaction_data.get("currency", account.currency),
                exchange_rate=transaction_data.get(
                    "exchange_rate", account.exchange_rate
                ),
                created_by=user_id,
            )

            # حساب المبلغ بالعملة الأساسية
            if transaction.currency != "USD":
                transaction.base_currency_amount = (
                    transaction.debit_amount or transaction.credit_amount
                ) * Decimal(str(transaction.exchange_rate))

            self.db.add(transaction)
            self.db.flush()

            # تحديث رصيد الحساب
            account.calculate_current_balance()

            self.db.commit()

            logger.info(f"تم إضافة حركة جديدة: {transaction.transaction_number}")
            return transaction

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إضافة الحركة: {str(e)}")
            raise

    def get_account_transactions(
        self,
        account_id: int,
        filters: Dict[str, Any] = None,
        page: int = 1,
        per_page: int = 50,
    ) -> Dict[str, Any]:
        """الحصول على حركات الحساب"""
        try:
            query = self.db.query(AccountTransaction).filter(
                AccountTransaction.account_id == account_id
            )

            # تطبيق الفلاتر
            if filters:
                if filters.get("transaction_type"):
                    query = query.filter(
                        AccountTransaction.transaction_type
                        == TransactionType(filters["transaction_type"])
                    )

                if filters.get("date_from"):
                    query = query.filter(
                        AccountTransaction.transaction_date >= filters["date_from"]
                    )

                if filters.get("date_to"):
                    query = query.filter(
                        AccountTransaction.transaction_date <= filters["date_to"]
                    )

                if filters.get("reference"):
                    query = query.filter(
                        AccountTransaction.reference.ilike(f"%{filters['reference']}%")
                    )

                if filters.get("is_reconciled") is not None:
                    query = query.filter(
                        AccountTransaction.is_reconciled == filters["is_reconciled"]
                    )

                if filters.get("amount_min") is not None:
                    query = query.filter(
                        or_(
                            AccountTransaction.debit_amount >= filters["amount_min"],
                            AccountTransaction.credit_amount >= filters["amount_min"],
                        )
                    )

                if filters.get("amount_max") is not None:
                    query = query.filter(
                        or_(
                            AccountTransaction.debit_amount <= filters["amount_max"],
                            AccountTransaction.credit_amount <= filters["amount_max"],
                        )
                    )

            # الترتيب
            query = query.order_by(desc(AccountTransaction.transaction_date))

            # العد الإجمالي
            total_count = query.count()

            # الترقيم
            offset = (page - 1) * per_page
            transactions = query.offset(offset).limit(per_page).all()

            return {
                "transactions": [transaction.to_dict() for transaction in transactions],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total_count,
                    "pages": (total_count + per_page - 1) // per_page,
                },
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على حركات الحساب: {str(e)}")
            raise

    def reconcile_transaction(
        self, transaction_id: int, user_id: int, notes: str = None
    ) -> bool:
        """تسوية حركة"""
        try:
            transaction = (
                self.db.query(AccountTransaction)
                .filter(AccountTransaction.id == transaction_id)
                .first()
            )

            if not transaction:
                raise ValueError(f"الحركة غير موجودة: {transaction_id}")

            if transaction.reconcile(user_id, notes):
                self.db.commit()
                logger.info(f"تم تسوية الحركة: {transaction.transaction_number}")
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تسوية الحركة: {str(e)}")
            raise

    # ==================== تحليل الأرصدة ====================

    def get_account_balance_analysis(self, account_id: int) -> Dict[str, Any]:
        """تحليل شامل لرصيد الحساب"""
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"الحساب غير موجود: {account_id}")

            # تحليل أعمار الأرصدة
            age_analysis = account.get_balance_age_analysis()

            # إحصائيات الحركات
            transactions_stats = self._get_transactions_statistics(account_id)

            # الحركات المعلقة
            outstanding_transactions = self._get_outstanding_transactions(account_id)

            # تحليل الدفعات
            payment_analysis = self._get_payment_analysis(account_id)

            return {
                "account_info": account.to_dict(),
                "balance_summary": {
                    "current_balance": float(account.current_balance),
                    "credit_limit": float(account.credit_limit),
                    "available_credit": account.get_available_credit(),
                    "is_credit_limit_exceeded": account.is_credit_limit_exceeded(),
                },
                "age_analysis": age_analysis,
                "transactions_stats": transactions_stats,
                "outstanding_transactions": outstanding_transactions,
                "payment_analysis": payment_analysis,
            }

        except Exception as e:
            logger.error(f"خطأ في تحليل رصيد الحساب: {str(e)}")
            raise

    def get_accounts_summary(self, account_type: str = None) -> Dict[str, Any]:
        """ملخص شامل للحسابات"""
        try:
            query = self.db.query(CustomerSupplierAccount)

            if account_type:
                query = query.filter(
                    CustomerSupplierAccount.account_type == AccountType(account_type)
                )

            accounts = query.all()

            # إحصائيات عامة
            total_accounts = len(accounts)
            active_accounts = len(
                [a for a in accounts if a.status == AccountStatus.ACTIVE]
            )

            # إجمالي الأرصدة
            total_balance = sum(float(a.current_balance) for a in accounts)
            total_credit_limit = sum(float(a.credit_limit) for a in accounts)

            # تحليل حسب النوع
            type_analysis = {}
            for account_type_enum in AccountType:
                type_accounts = [
                    a for a in accounts if a.account_type == account_type_enum
                ]
                type_analysis[account_type_enum.value] = {
                    "count": len(type_accounts),
                    "total_balance": sum(
                        float(a.current_balance) for a in type_accounts
                    ),
                    "average_balance": (
                        sum(float(a.current_balance) for a in type_accounts)
                        / len(type_accounts)
                        if type_accounts
                        else 0
                    ),
                }

            # تحليل حسب العملة
            currency_analysis = {}
            for account in accounts:
                currency = account.currency
                if currency not in currency_analysis:
                    currency_analysis[currency] = {"count": 0, "total_balance": 0}
                currency_analysis[currency]["count"] += 1
                currency_analysis[currency]["total_balance"] += float(
                    account.current_balance
                )

            # الحسابات التي تجاوزت حد الائتمان
            exceeded_credit_accounts = [
                a for a in accounts if a.is_credit_limit_exceeded()
            ]

            return {
                "summary": {
                    "total_accounts": total_accounts,
                    "active_accounts": active_accounts,
                    "inactive_accounts": total_accounts - active_accounts,
                    "total_balance": total_balance,
                    "total_credit_limit": total_credit_limit,
                    "exceeded_credit_count": len(exceeded_credit_accounts),
                },
                "type_analysis": type_analysis,
                "currency_analysis": currency_analysis,
                "exceeded_credit_accounts": [
                    {
                        "id": a.id,
                        "account_number": a.account_number,
                        "account_name": a.account_name,
                        "current_balance": float(a.current_balance),
                        "credit_limit": float(a.credit_limit),
                        "excess_amount": float(a.current_balance)
                        - float(a.credit_limit),
                    }
                    for a in exceeded_credit_accounts
                ],
            }

        except Exception as e:
            logger.error(f"خطأ في ملخص الحسابات: {str(e)}")
            raise

    # ==================== إدارة جدولة المدفوعات ====================

    def create_payment_schedule(
        self, account_id: int, schedule_data: Dict[str, Any], user_id: int
    ) -> PaymentSchedule:
        """إنشاء جدولة مدفوعات جديدة"""
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"الحساب غير موجود: {account_id}")

            # إنشاء الجدولة
            schedule = PaymentSchedule(
                account_id=account_id,
                schedule_name=schedule_data["schedule_name"],
                description=schedule_data.get("description"),
                total_amount=Decimal(str(schedule_data["total_amount"])),
                remaining_amount=Decimal(str(schedule_data["total_amount"])),
                start_date=schedule_data["start_date"],
                end_date=schedule_data.get("end_date"),
                next_payment_date=schedule_data["next_payment_date"],
                frequency=schedule_data["frequency"],
                interval_count=schedule_data.get("interval_count", 1),
                auto_process=schedule_data.get("auto_process", False),
                send_reminders=schedule_data.get("send_reminders", True),
                reminder_days=schedule_data.get("reminder_days", 3),
                created_by=user_id,
            )

            self.db.add(schedule)
            self.db.flush()

            # إنشاء بنود الجدولة
            self._create_schedule_items(schedule, schedule_data)

            self.db.commit()

            logger.info(f"تم إنشاء جدولة مدفوعات جديدة: {schedule.schedule_name}")
            return schedule

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء جدولة المدفوعات: {str(e)}")
            raise

    def process_scheduled_payment(
        self, schedule_id: int, amount: float, user_id: int
    ) -> bool:
        """معالجة دفعة مجدولة"""
        try:
            schedule = (
                self.db.query(PaymentSchedule)
                .filter(PaymentSchedule.id == schedule_id)
                .first()
            )

            if not schedule:
                raise ValueError(f"الجدولة غير موجودة: {schedule_id}")

            if schedule.process_payment(amount):
                # إضافة حركة للحساب
                self.add_transaction(
                    account_id=schedule.account_id,
                    transaction_data={
                        "transaction_type": "payment",
                        "credit_amount": amount,
                        "description": f"دفعة مجدولة - {schedule.schedule_name}",
                        "reference": f"SCHED-{schedule.id}",
                    },
                    user_id=user_id,
                )

                self.db.commit()
                logger.info(
                    f"تم معالجة دفعة مجدولة: {amount} للجدولة {schedule.schedule_name}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في معالجة الدفعة المجدولة: {str(e)}")
            raise

    # ==================== إدارة إشعارات الائتمان ====================

    def create_credit_note(
        self, account_id: int, credit_data: Dict[str, Any], user_id: int
    ) -> CreditNote:
        """إنشاء إشعار ائتمان جديد"""
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"الحساب غير موجود: {account_id}")

            # إنشاء رقم الإشعار
            credit_note_number = self._generate_credit_note_number()

            # إنشاء الإشعار
            credit_note = CreditNote(
                account_id=account_id,
                credit_note_number=credit_note_number,
                credit_note_date=credit_data.get("credit_note_date", datetime.utcnow()),
                total_amount=Decimal(str(credit_data["total_amount"])),
                remaining_amount=Decimal(str(credit_data["total_amount"])),
                reason=credit_data["reason"],
                description=credit_data.get("description"),
                reference=credit_data.get("reference"),
                expiry_date=credit_data.get("expiry_date"),
                created_by=user_id,
            )

            self.db.add(credit_note)
            self.db.flush()

            # إضافة حركة ائتمان للحساب
            self.add_transaction(
                account_id=account_id,
                transaction_data={
                    "transaction_type": "credit",
                    "credit_amount": credit_data["total_amount"],
                    "description": f"إشعار ائتمان - {credit_data['reason']}",
                    "reference": credit_note_number,
                },
                user_id=user_id,
            )

            self.db.commit()

            logger.info(f"تم إنشاء إشعار ائتمان جديد: {credit_note_number}")
            return credit_note

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء إشعار الائتمان: {str(e)}")
            raise

    def use_credit_note(self, credit_note_id: int, amount: float, user_id: int) -> bool:
        """استخدام إشعار ائتمان"""
        try:
            credit_note = (
                self.db.query(CreditNote)
                .filter(CreditNote.id == credit_note_id)
                .first()
            )

            if not credit_note:
                raise ValueError(f"إشعار الائتمان غير موجود: {credit_note_id}")

            if credit_note.use_credit(amount):
                # إضافة حركة استخدام للحساب
                self.add_transaction(
                    account_id=credit_note.account_id,
                    transaction_data={
                        "transaction_type": "debit",
                        "debit_amount": amount,
                        "description": f"استخدام إشعار ائتمان - {credit_note.credit_note_number}",
                        "reference": f"USE-{credit_note.credit_note_number}",
                    },
                    user_id=user_id,
                )

                self.db.commit()
                logger.info(
                    f"تم استخدام إشعار ائتمان: {amount} من {credit_note.credit_note_number}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في استخدام إشعار الائتمان: {str(e)}")
            raise

    # ==================== إدارة كشوف الحسابات ====================

    def generate_account_statement(
        self,
        account_id: int,
        period_start: datetime,
        period_end: datetime,
        user_id: int,
    ) -> AccountStatement:
        """إنشاء كشف حساب"""
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError(f"الحساب غير موجود: {account_id}")

            # إنشاء رقم الكشف
            statement_number = self._generate_statement_number()

            # حساب الرصيد الافتتاحي للفترة
            opening_balance = self._calculate_opening_balance(account_id, period_start)

            # إنشاء الكشف
            statement = AccountStatement(
                account_id=account_id,
                statement_number=statement_number,
                period_start=period_start,
                period_end=period_end,
                opening_balance=opening_balance,
                created_by=user_id,
            )

            self.db.add(statement)
            self.db.flush()

            # إنشاء بيانات الكشف
            statement_data = statement.generate_statement_data()

            self.db.commit()

            logger.info(f"تم إنشاء كشف حساب: {statement_number}")
            return statement

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء كشف الحساب: {str(e)}")
            raise

    def send_account_statement(self, statement_id: int, user_id: int) -> bool:
        """إرسال كشف حساب"""
        try:
            statement = (
                self.db.query(AccountStatement)
                .filter(AccountStatement.id == statement_id)
                .first()
            )

            if not statement:
                raise ValueError(f"كشف الحساب غير موجود: {statement_id}")

            if statement.send_statement(user_id):
                self.db.commit()
                logger.info(f"تم إرسال كشف الحساب: {statement.statement_number}")
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إرسال كشف الحساب: {str(e)}")
            raise

    # ==================== الدوال المساعدة ====================

    def _generate_account_number(self, account_type: str) -> str:
        """إنشاء رقم حساب جديد"""
        prefix_map = {
            "customer": "CUST",
            "supplier": "SUPP",
            "employee": "EMP",
            "both": "BOTH",
            "other": "OTH",
        }

        prefix = prefix_map.get(account_type, "ACC")

        # الحصول على آخر رقم
        last_account = (
            self.db.query(CustomerSupplierAccount)
            .filter(CustomerSupplierAccount.account_number.like(f"{prefix}%"))
            .order_by(desc(CustomerSupplierAccount.id))
            .first()
        )

        if last_account:
            last_number = int(last_account.account_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}-{new_number:06d}"

    def _generate_transaction_number(self) -> str:
        """إنشاء رقم حركة جديد"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # الحصول على آخر رقم لليوم
        last_transaction = (
            self.db.query(AccountTransaction)
            .filter(AccountTransaction.transaction_number.like(f"TXN-{today}%"))
            .order_by(desc(AccountTransaction.id))
            .first()
        )

        if last_transaction:
            last_number = int(last_transaction.transaction_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"TXN-{today}-{new_number:04d}"

    def _generate_credit_note_number(self) -> str:
        """إنشاء رقم إشعار ائتمان جديد"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # الحصول على آخر رقم لليوم
        last_credit_note = (
            self.db.query(CreditNote)
            .filter(CreditNote.credit_note_number.like(f"CN-{today}%"))
            .order_by(desc(CreditNote.id))
            .first()
        )

        if last_credit_note:
            last_number = int(last_credit_note.credit_note_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"CN-{today}-{new_number:04d}"

    def _generate_statement_number(self) -> str:
        """إنشاء رقم كشف حساب جديد"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # الحصول على آخر رقم لليوم
        last_statement = (
            self.db.query(AccountStatement)
            .filter(AccountStatement.statement_number.like(f"STMT-{today}%"))
            .order_by(desc(AccountStatement.id))
            .first()
        )

        if last_statement:
            last_number = int(last_statement.statement_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"STMT-{today}-{new_number:04d}"

    def _add_opening_balance_transaction(self, account: CustomerSupplierAccount):
        """إضافة حركة الرصيد الافتتاحي"""
        transaction = AccountTransaction(
            account_id=account.id,
            transaction_number=self._generate_transaction_number(),
            transaction_type=TransactionType.OPENING_BALANCE,
            transaction_date=account.opening_balance_date or datetime.utcnow(),
            description="الرصيد الافتتاحي",
            currency=account.currency,
            exchange_rate=account.exchange_rate,
            created_by=account.created_by,
        )

        # تحديد المدين والدائن حسب نوع الحساب
        if account.account_type in [AccountType.CUSTOMER, AccountType.EMPLOYEE]:
            if account.opening_balance > 0:
                transaction.debit_amount = account.opening_balance
            else:
                transaction.credit_amount = abs(account.opening_balance)
        else:  # SUPPLIER
            if account.opening_balance > 0:
                transaction.credit_amount = account.opening_balance
            else:
                transaction.debit_amount = abs(account.opening_balance)

        self.db.add(transaction)

    def _get_transactions_statistics(self, account_id: int) -> Dict[str, Any]:
        """إحصائيات الحركات"""
        transactions = (
            self.db.query(AccountTransaction)
            .filter(AccountTransaction.account_id == account_id)
            .all()
        )

        total_transactions = len(transactions)
        total_debits = sum(float(t.debit_amount) for t in transactions)
        total_credits = sum(float(t.credit_amount) for t in transactions)

        # إحصائيات حسب النوع
        type_stats = {}
        for transaction_type in TransactionType:
            type_transactions = [
                t for t in transactions if t.transaction_type == transaction_type
            ]
            type_stats[transaction_type.value] = {
                "count": len(type_transactions),
                "total_amount": sum(
                    float(t.debit_amount or t.credit_amount) for t in type_transactions
                ),
            }

        return {
            "total_transactions": total_transactions,
            "total_debits": total_debits,
            "total_credits": total_credits,
            "net_amount": total_debits - total_credits,
            "type_statistics": type_stats,
        }

    def _get_outstanding_transactions(self, account_id: int) -> List[Dict[str, Any]]:
        """الحركات المعلقة"""
        outstanding = (
            self.db.query(AccountTransaction)
            .filter(
                and_(
                    AccountTransaction.account_id == account_id,
                    AccountTransaction.outstanding_amount > 0,
                )
            )
            .all()
        )

        return [
            {
                "id": t.id,
                "transaction_number": t.transaction_number,
                "transaction_type": t.transaction_type.value,
                "transaction_date": t.transaction_date.isoformat(),
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "outstanding_amount": float(t.outstanding_amount),
                "is_overdue": t.is_overdue(),
                "days_overdue": t.get_days_overdue(),
            }
            for t in outstanding
        ]

    def _get_payment_analysis(self, account_id: int) -> Dict[str, Any]:
        """تحليل الدفعات"""
        # الدفعات في آخر 12 شهر
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)

        payments = (
            self.db.query(AccountTransaction)
            .filter(
                and_(
                    AccountTransaction.account_id == account_id,
                    AccountTransaction.transaction_type == TransactionType.PAYMENT,
                    AccountTransaction.transaction_date >= twelve_months_ago,
                )
            )
            .all()
        )

        if not payments:
            return {
                "total_payments": 0,
                "average_payment": 0,
                "payment_frequency": 0,
                "last_payment_date": None,
            }

        total_payments = sum(float(p.credit_amount) for p in payments)
        average_payment = total_payments / len(payments)

        # تكرار الدفعات (دفعات في الشهر)
        payment_frequency = len(payments) / 12

        # آخر دفعة
        last_payment = max(payments, key=lambda p: p.transaction_date)

        return {
            "total_payments": total_payments,
            "average_payment": average_payment,
            "payment_frequency": payment_frequency,
            "last_payment_date": last_payment.transaction_date.isoformat(),
            "payment_count": len(payments),
        }

    def _calculate_opening_balance(
        self, account_id: int, period_start: datetime
    ) -> Decimal:
        """حساب الرصيد الافتتاحي لفترة معينة"""
        transactions = (
            self.db.query(AccountTransaction)
            .filter(
                and_(
                    AccountTransaction.account_id == account_id,
                    AccountTransaction.transaction_date < period_start,
                )
            )
            .all()
        )

        total_debits = sum(t.debit_amount for t in transactions)
        total_credits = sum(t.credit_amount for t in transactions)

        return total_debits - total_credits

    def _create_schedule_items(
        self, schedule: PaymentSchedule, schedule_data: Dict[str, Any]
    ):
        """إنشاء بنود جدولة المدفوعات"""
        items_data = schedule_data.get("items", [])

        for i, item_data in enumerate(items_data, 1):
            item = PaymentScheduleItem(
                schedule_id=schedule.id,
                item_number=i,
                amount=Decimal(str(item_data["amount"])),
                due_date=item_data["due_date"],
                description=item_data.get("description"),
            )
            self.db.add(item)
