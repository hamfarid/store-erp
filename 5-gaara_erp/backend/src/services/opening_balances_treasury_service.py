#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/opening_balances_treasury_service.py

خدمة إدارة الأرصدة الافتتاحية والخزنة
تدير جميع العمليات المتعلقة بالأرصدة الافتتاحية والحركات المالية للخزائن
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc, extract
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
import logging
from decimal import Decimal

from models.opening_balances_treasury import (
    OpeningBalance,
    OpeningBalanceDetail,
    BalanceAdjustment,
    Treasury,
    TreasuryTransaction,
    TreasuryReconciliation,
    BalanceType,
    TreasuryTransactionType,
    TreasuryStatus,
)
from models.user import User

logger = logging.getLogger(__name__)


class OpeningBalancesTreasuryService:
    """خدمة إدارة الأرصدة الافتتاحية والخزنة الشاملة"""

    def __init__(self, db_session: Session):
        self.db = db_session

    # ==================== إدارة الأرصدة الافتتاحية ====================

    def create_opening_balance(
        self, balance_data: Dict[str, Any], user_id: int
    ) -> OpeningBalance:
        """
        إنشاء رصيد افتتاحي جديد

        Args:
            balance_data: بيانات الرصيد الافتتاحي
            user_id: معرف المستخدم المنشئ

        Returns:
            OpeningBalance: الرصيد الافتتاحي المنشأ
        """
        try:
            # إنشاء رمز الرصيد
            balance_code = self._generate_balance_code(balance_data.get("balance_type"))

            # إنشاء الرصيد الافتتاحي
            opening_balance = OpeningBalance(
                balance_code=balance_code,
                balance_name=balance_data["balance_name"],
                balance_type=BalanceType(balance_data["balance_type"]),
                fiscal_year=balance_data["fiscal_year"],
                period_start_date=balance_data["period_start_date"],
                period_end_date=balance_data["period_end_date"],
                opening_balance=Decimal(str(balance_data.get("opening_balance", 0))),
                current_balance=Decimal(str(balance_data.get("opening_balance", 0))),
                currency=balance_data.get("currency", "USD"),
                exchange_rate=balance_data.get("exchange_rate", 1.0),
                customer_id=balance_data.get("customer_id"),
                supplier_id=balance_data.get("supplier_id"),
                product_id=balance_data.get("product_id"),
                warehouse_id=balance_data.get("warehouse_id"),
                account_id=balance_data.get("account_id"),
                treasury_id=balance_data.get("treasury_id"),
                description=balance_data.get("description"),
                notes=balance_data.get("notes"),
                reference=balance_data.get("reference"),
                created_by=user_id,
            )

            # حساب المبلغ بالعملة الأساسية
            if opening_balance.currency != "USD":
                opening_balance.base_currency_amount = (
                    opening_balance.opening_balance
                    * Decimal(str(opening_balance.exchange_rate))
                )

            self.db.add(opening_balance)
            self.db.flush()

            # إضافة التفاصيل إذا كانت موجودة
            if balance_data.get("details"):
                self._create_balance_details(
                    opening_balance.id, balance_data["details"]
                )

            self.db.commit()

            logger.info(
                f"تم إنشاء رصيد افتتاحي جديد: {opening_balance.balance_code} - {opening_balance.balance_name}"
            )
            return opening_balance

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء الرصيد الافتتاحي: {str(e)}")
            raise

    def update_opening_balance(
        self, balance_id: int, balance_data: Dict[str, Any], user_id: int
    ) -> OpeningBalance:
        """تحديث الرصيد الافتتاحي"""
        try:
            opening_balance = self.get_opening_balance_by_id(balance_id)
            if not opening_balance:
                raise ValueError(f"الرصيد الافتتاحي غير موجود: {balance_id}")

            if opening_balance.is_posted:
                raise ValueError("لا يمكن تعديل رصيد افتتاحي مرحل")

            # تحديث البيانات
            for key, value in balance_data.items():
                if hasattr(opening_balance, key) and key not in [
                    "id",
                    "balance_code",
                    "created_at",
                    "created_by",
                ]:
                    setattr(opening_balance, key, value)

            opening_balance.updated_at = datetime.utcnow()

            self.db.commit()

            logger.info(f"تم تحديث الرصيد الافتتاحي: {opening_balance.balance_code}")
            return opening_balance

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تحديث الرصيد الافتتاحي: {str(e)}")
            raise

    def confirm_opening_balance(self, balance_id: int, user_id: int) -> bool:
        """تأكيد الرصيد الافتتاحي"""
        try:
            opening_balance = self.get_opening_balance_by_id(balance_id)
            if not opening_balance:
                raise ValueError(f"الرصيد الافتتاحي غير موجود: {balance_id}")

            if opening_balance.confirm_balance(user_id):
                self.db.commit()
                logger.info(
                    f"تم تأكيد الرصيد الافتتاحي: {opening_balance.balance_code}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تأكيد الرصيد الافتتاحي: {str(e)}")
            raise

    def post_opening_balance(self, balance_id: int, user_id: int) -> bool:
        """ترحيل الرصيد الافتتاحي"""
        try:
            opening_balance = self.get_opening_balance_by_id(balance_id)
            if not opening_balance:
                raise ValueError(f"الرصيد الافتتاحي غير موجود: {balance_id}")

            if opening_balance.post_balance(user_id):
                self.db.commit()
                logger.info(
                    f"تم ترحيل الرصيد الافتتاحي: {opening_balance.balance_code}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في ترحيل الرصيد الافتتاحي: {str(e)}")
            raise

    def get_opening_balance_by_id(self, balance_id: int) -> Optional[OpeningBalance]:
        """الحصول على رصيد افتتاحي بالمعرف"""
        return (
            self.db.query(OpeningBalance)
            .filter(OpeningBalance.id == balance_id)
            .first()
        )

    def get_opening_balances_list(
        self, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 50
    ) -> Dict[str, Any]:
        """الحصول على قائمة الأرصدة الافتتاحية مع التصفية والترقيم"""
        try:
            query = self.db.query(OpeningBalance)

            # تطبيق الفلاتر
            if filters:
                if filters.get("balance_type"):
                    query = query.filter(
                        OpeningBalance.balance_type
                        == BalanceType(filters["balance_type"])
                    )

                if filters.get("fiscal_year"):
                    query = query.filter(
                        OpeningBalance.fiscal_year == filters["fiscal_year"]
                    )

                if filters.get("is_confirmed") is not None:
                    query = query.filter(
                        OpeningBalance.is_confirmed == filters["is_confirmed"]
                    )

                if filters.get("is_posted") is not None:
                    query = query.filter(
                        OpeningBalance.is_posted == filters["is_posted"]
                    )

                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            OpeningBalance.balance_name.ilike(search_term),
                            OpeningBalance.balance_code.ilike(search_term),
                            OpeningBalance.description.ilike(search_term),
                        )
                    )

                if filters.get("currency"):
                    query = query.filter(OpeningBalance.currency == filters["currency"])

                if filters.get("customer_id"):
                    query = query.filter(
                        OpeningBalance.customer_id == filters["customer_id"]
                    )

                if filters.get("supplier_id"):
                    query = query.filter(
                        OpeningBalance.supplier_id == filters["supplier_id"]
                    )

                if filters.get("warehouse_id"):
                    query = query.filter(
                        OpeningBalance.warehouse_id == filters["warehouse_id"]
                    )

                if filters.get("balance_min") is not None:
                    query = query.filter(
                        OpeningBalance.opening_balance >= filters["balance_min"]
                    )

                if filters.get("balance_max") is not None:
                    query = query.filter(
                        OpeningBalance.opening_balance <= filters["balance_max"]
                    )

            # الترتيب
            sort_by = (
                filters.get("sort_by", "balance_name") if filters else "balance_name"
            )
            sort_order = filters.get("sort_order", "asc") if filters else "asc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(OpeningBalance, sort_by)))
            else:
                query = query.order_by(asc(getattr(OpeningBalance, sort_by)))

            # العد الإجمالي
            total_count = query.count()

            # الترقيم
            offset = (page - 1) * per_page
            balances = query.offset(offset).limit(per_page).all()

            return {
                "opening_balances": [balance.to_dict() for balance in balances],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total_count,
                    "pages": (total_count + per_page - 1) // per_page,
                },
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة الأرصدة الافتتاحية: {str(e)}")
            raise

    def get_opening_balances_summary(self, fiscal_year: int = None) -> Dict[str, Any]:
        """ملخص الأرصدة الافتتاحية"""
        try:
            query = self.db.query(OpeningBalance)

            if fiscal_year:
                query = query.filter(OpeningBalance.fiscal_year == fiscal_year)

            balances = query.all()

            # إحصائيات عامة
            total_balances = len(balances)
            confirmed_balances = len([b for b in balances if b.is_confirmed])
            posted_balances = len([b for b in balances if b.is_posted])

            # إجمالي الأرصدة
            total_amount = sum(float(b.opening_balance) for b in balances)

            # تحليل حسب النوع
            type_analysis = {}
            for balance_type in BalanceType:
                type_balances = [b for b in balances if b.balance_type == balance_type]
                type_analysis[balance_type.value] = {
                    "count": len(type_balances),
                    "total_amount": sum(
                        float(b.opening_balance) for b in type_balances
                    ),
                    "confirmed_count": len(
                        [b for b in type_balances if b.is_confirmed]
                    ),
                    "posted_count": len([b for b in type_balances if b.is_posted]),
                }

            # تحليل حسب العملة
            currency_analysis = {}
            for balance in balances:
                currency = balance.currency
                if currency not in currency_analysis:
                    currency_analysis[currency] = {"count": 0, "total_amount": 0}
                currency_analysis[currency]["count"] += 1
                currency_analysis[currency]["total_amount"] += float(
                    balance.opening_balance
                )

            return {
                "summary": {
                    "total_balances": total_balances,
                    "confirmed_balances": confirmed_balances,
                    "posted_balances": posted_balances,
                    "pending_confirmation": total_balances - confirmed_balances,
                    "pending_posting": confirmed_balances - posted_balances,
                    "total_amount": total_amount,
                },
                "type_analysis": type_analysis,
                "currency_analysis": currency_analysis,
            }

        except Exception as e:
            logger.error(f"خطأ في ملخص الأرصدة الافتتاحية: {str(e)}")
            raise

    # ==================== إدارة تسويات الأرصدة ====================

    def create_balance_adjustment(
        self, balance_id: int, adjustment_data: Dict[str, Any], user_id: int
    ) -> BalanceAdjustment:
        """إنشاء تسوية رصيد"""
        try:
            opening_balance = self.get_opening_balance_by_id(balance_id)
            if not opening_balance:
                raise ValueError(f"الرصيد الافتتاحي غير موجود: {balance_id}")

            # إنشاء رقم التسوية
            adjustment_number = self._generate_adjustment_number()

            # إنشاء التسوية
            adjustment = BalanceAdjustment(
                opening_balance_id=balance_id,
                adjustment_number=adjustment_number,
                adjustment_date=adjustment_data.get(
                    "adjustment_date", datetime.utcnow()
                ),
                adjustment_amount=Decimal(str(adjustment_data["adjustment_amount"])),
                reason=adjustment_data["reason"],
                description=adjustment_data.get("description"),
                reference=adjustment_data.get("reference"),
                created_by=user_id,
            )

            self.db.add(adjustment)
            self.db.commit()

            logger.info(f"تم إنشاء تسوية رصيد جديدة: {adjustment_number}")
            return adjustment

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء تسوية الرصيد: {str(e)}")
            raise

    def approve_balance_adjustment(self, adjustment_id: int, user_id: int) -> bool:
        """الموافقة على تسوية رصيد"""
        try:
            adjustment = (
                self.db.query(BalanceAdjustment)
                .filter(BalanceAdjustment.id == adjustment_id)
                .first()
            )

            if not adjustment:
                raise ValueError(f"تسوية الرصيد غير موجودة: {adjustment_id}")

            if adjustment.approve(user_id):
                # تحديث الرصيد الافتتاحي
                opening_balance = adjustment.opening_balance
                opening_balance.calculate_closing_balance()

                self.db.commit()
                logger.info(
                    f"تم الموافقة على تسوية الرصيد: {adjustment.adjustment_number}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في الموافقة على تسوية الرصيد: {str(e)}")
            raise

    # ==================== إدارة الخزائن ====================

    def create_treasury(self, treasury_data: Dict[str, Any], user_id: int) -> Treasury:
        """إنشاء خزنة جديدة"""
        try:
            # إنشاء رمز الخزنة
            treasury_code = self._generate_treasury_code(
                treasury_data.get("treasury_type")
            )

            # إنشاء الخزنة
            treasury = Treasury(
                treasury_code=treasury_code,
                treasury_name=treasury_data["treasury_name"],
                treasury_type=treasury_data["treasury_type"],
                description=treasury_data.get("description"),
                location=treasury_data.get("location"),
                responsible_person=treasury_data.get("responsible_person"),
                opening_balance=Decimal(str(treasury_data.get("opening_balance", 0))),
                current_balance=Decimal(str(treasury_data.get("opening_balance", 0))),
                available_balance=Decimal(str(treasury_data.get("opening_balance", 0))),
                currency=treasury_data.get("currency", "USD"),
                daily_limit=Decimal(str(treasury_data.get("daily_limit", 0))),
                monthly_limit=Decimal(str(treasury_data.get("monthly_limit", 0))),
                bank_name=treasury_data.get("bank_name"),
                bank_branch=treasury_data.get("bank_branch"),
                account_number=treasury_data.get("account_number"),
                iban=treasury_data.get("iban"),
                swift_code=treasury_data.get("swift_code"),
                allow_negative_balance=treasury_data.get(
                    "allow_negative_balance", False
                ),
                require_approval=treasury_data.get("require_approval", False),
                auto_reconcile=treasury_data.get("auto_reconcile", False),
                is_default=treasury_data.get("is_default", False),
                created_by=user_id,
            )

            self.db.add(treasury)
            self.db.flush()

            # إضافة حركة الرصيد الافتتاحي إذا كان موجوداً
            if treasury.opening_balance != 0:
                self._add_opening_balance_transaction(treasury, user_id)

            self.db.commit()

            logger.info(
                f"تم إنشاء خزنة جديدة: {treasury.treasury_code} - {treasury.treasury_name}"
            )
            return treasury

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء الخزنة: {str(e)}")
            raise

    def update_treasury(
        self, treasury_id: int, treasury_data: Dict[str, Any], user_id: int
    ) -> Treasury:
        """تحديث بيانات الخزنة"""
        try:
            treasury = self.get_treasury_by_id(treasury_id)
            if not treasury:
                raise ValueError(f"الخزنة غير موجودة: {treasury_id}")

            # تحديث البيانات
            for key, value in treasury_data.items():
                if hasattr(treasury, key) and key not in [
                    "id",
                    "treasury_code",
                    "created_at",
                    "created_by",
                ]:
                    setattr(treasury, key, value)

            treasury.updated_at = datetime.utcnow()

            self.db.commit()

            logger.info(f"تم تحديث الخزنة: {treasury.treasury_code}")
            return treasury

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في تحديث الخزنة: {str(e)}")
            raise

    def get_treasury_by_id(self, treasury_id: int) -> Optional[Treasury]:
        """الحصول على خزنة بالمعرف"""
        return self.db.query(Treasury).filter(Treasury.id == treasury_id).first()

    def get_treasury_by_code(self, treasury_code: str) -> Optional[Treasury]:
        """الحصول على خزنة بالرمز"""
        return (
            self.db.query(Treasury)
            .filter(Treasury.treasury_code == treasury_code)
            .first()
        )

    def get_treasuries_list(
        self, filters: Dict[str, Any] = None, page: int = 1, per_page: int = 50
    ) -> Dict[str, Any]:
        """الحصول على قائمة الخزائن مع التصفية والترقيم"""
        try:
            query = self.db.query(Treasury)

            # تطبيق الفلاتر
            if filters:
                if filters.get("treasury_type"):
                    query = query.filter(
                        Treasury.treasury_type == filters["treasury_type"]
                    )

                if filters.get("status"):
                    query = query.filter(
                        Treasury.status == TreasuryStatus(filters["status"])
                    )

                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.filter(
                        or_(
                            Treasury.treasury_name.ilike(search_term),
                            Treasury.treasury_code.ilike(search_term),
                            Treasury.responsible_person.ilike(search_term),
                        )
                    )

                if filters.get("currency"):
                    query = query.filter(Treasury.currency == filters["currency"])

                if filters.get("location"):
                    query = query.filter(
                        Treasury.location.ilike(f"%{filters['location']}%")
                    )

                if filters.get("balance_min") is not None:
                    query = query.filter(
                        Treasury.current_balance >= filters["balance_min"]
                    )

                if filters.get("balance_max") is not None:
                    query = query.filter(
                        Treasury.current_balance <= filters["balance_max"]
                    )

            # الترتيب
            sort_by = (
                filters.get("sort_by", "treasury_name") if filters else "treasury_name"
            )
            sort_order = filters.get("sort_order", "asc") if filters else "asc"

            if sort_order == "desc":
                query = query.order_by(desc(getattr(Treasury, sort_by)))
            else:
                query = query.order_by(asc(getattr(Treasury, sort_by)))

            # العد الإجمالي
            total_count = query.count()

            # الترقيم
            offset = (page - 1) * per_page
            treasuries = query.offset(offset).limit(per_page).all()

            return {
                "treasuries": [treasury.to_dict() for treasury in treasuries],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total_count,
                    "pages": (total_count + per_page - 1) // per_page,
                },
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة الخزائن: {str(e)}")
            raise

    # ==================== إدارة حركات الخزنة ====================

    def add_treasury_transaction(
        self, treasury_id: int, transaction_data: Dict[str, Any], user_id: int
    ) -> TreasuryTransaction:
        """إضافة حركة خزنة جديدة"""
        try:
            treasury = self.get_treasury_by_id(treasury_id)
            if not treasury:
                raise ValueError(f"الخزنة غير موجودة: {treasury_id}")

            transaction_type = TreasuryTransactionType(
                transaction_data["transaction_type"]
            )
            amount = float(transaction_data["amount"])

            # التحقق من إمكانية معالجة الحركة
            if not treasury.can_process_transaction(amount, transaction_type):
                raise ValueError(
                    "لا يمكن معالجة هذه الحركة - رصيد غير كافي أو خزنة غير نشطة"
                )

            # إنشاء رقم الحركة
            transaction_number = self._generate_treasury_transaction_number()

            # إنشاء الحركة
            transaction = TreasuryTransaction(
                treasury_id=treasury_id,
                transaction_number=transaction_number,
                transaction_type=transaction_type,
                transaction_date=transaction_data.get(
                    "transaction_date", datetime.utcnow()
                ),
                amount=Decimal(str(amount)),
                counterpart_type=transaction_data.get("counterpart_type"),
                counterpart_id=transaction_data.get("counterpart_id"),
                counterpart_name=transaction_data.get("counterpart_name"),
                description=transaction_data["description"],
                reference=transaction_data.get("reference"),
                notes=transaction_data.get("notes"),
                invoice_id=transaction_data.get("invoice_id"),
                payment_id=transaction_data.get("payment_id"),
                voucher_id=transaction_data.get("voucher_id"),
                currency=transaction_data.get("currency", treasury.currency),
                exchange_rate=transaction_data.get("exchange_rate", 1.0),
                is_approved=transaction_data.get(
                    "is_approved", not treasury.require_approval
                ),
                created_by=user_id,
            )

            # حساب المبلغ بالعملة الأساسية
            if transaction.currency != "USD":
                transaction.base_currency_amount = transaction.amount * Decimal(
                    str(transaction.exchange_rate)
                )

            self.db.add(transaction)
            self.db.flush()

            # تحديث رصيد الخزنة
            treasury.calculate_current_balance()

            self.db.commit()

            logger.info(f"تم إضافة حركة خزنة جديدة: {transaction.transaction_number}")
            return transaction

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إضافة حركة الخزنة: {str(e)}")
            raise

    def approve_treasury_transaction(self, transaction_id: int, user_id: int) -> bool:
        """الموافقة على حركة خزنة"""
        try:
            transaction = (
                self.db.query(TreasuryTransaction)
                .filter(TreasuryTransaction.id == transaction_id)
                .first()
            )

            if not transaction:
                raise ValueError(f"حركة الخزنة غير موجودة: {transaction_id}")

            if transaction.approve(user_id):
                # تحديث رصيد الخزنة
                treasury = transaction.treasury
                treasury.calculate_current_balance()

                self.db.commit()
                logger.info(
                    f"تم الموافقة على حركة الخزنة: {transaction.transaction_number}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في الموافقة على حركة الخزنة: {str(e)}")
            raise

    def get_treasury_transactions(
        self,
        treasury_id: int,
        filters: Dict[str, Any] = None,
        page: int = 1,
        per_page: int = 50,
    ) -> Dict[str, Any]:
        """الحصول على حركات الخزنة"""
        try:
            query = self.db.query(TreasuryTransaction).filter(
                TreasuryTransaction.treasury_id == treasury_id
            )

            # تطبيق الفلاتر
            if filters:
                if filters.get("transaction_type"):
                    query = query.filter(
                        TreasuryTransaction.transaction_type
                        == TreasuryTransactionType(filters["transaction_type"])
                    )

                if filters.get("date_from"):
                    query = query.filter(
                        TreasuryTransaction.transaction_date >= filters["date_from"]
                    )

                if filters.get("date_to"):
                    query = query.filter(
                        TreasuryTransaction.transaction_date <= filters["date_to"]
                    )

                if filters.get("counterpart_type"):
                    query = query.filter(
                        TreasuryTransaction.counterpart_type
                        == filters["counterpart_type"]
                    )

                if filters.get("is_approved") is not None:
                    query = query.filter(
                        TreasuryTransaction.is_approved == filters["is_approved"]
                    )

                if filters.get("is_reconciled") is not None:
                    query = query.filter(
                        TreasuryTransaction.is_reconciled == filters["is_reconciled"]
                    )

                if filters.get("amount_min") is not None:
                    query = query.filter(
                        TreasuryTransaction.amount >= filters["amount_min"]
                    )

                if filters.get("amount_max") is not None:
                    query = query.filter(
                        TreasuryTransaction.amount <= filters["amount_max"]
                    )

            # الترتيب
            query = query.order_by(desc(TreasuryTransaction.transaction_date))

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
            logger.error(f"خطأ في الحصول على حركات الخزنة: {str(e)}")
            raise

    def get_treasury_balance_analysis(self, treasury_id: int) -> Dict[str, Any]:
        """تحليل شامل لرصيد الخزنة"""
        try:
            treasury = self.get_treasury_by_id(treasury_id)
            if not treasury:
                raise ValueError(f"الخزنة غير موجودة: {treasury_id}")

            # إحصائيات الحركات
            transactions_stats = self._get_treasury_transactions_statistics(treasury_id)

            # الحركات اليومية
            daily_stats = treasury.get_daily_transactions_total()

            # تحليل الحركات الشهرية
            monthly_stats = self._get_monthly_transactions_analysis(treasury_id)

            return {
                "treasury_info": treasury.to_dict(),
                "balance_summary": {
                    "current_balance": float(treasury.current_balance),
                    "available_balance": float(treasury.available_balance),
                    "reserved_balance": float(treasury.reserved_balance),
                    "daily_limit": float(treasury.daily_limit),
                    "monthly_limit": float(treasury.monthly_limit),
                },
                "transactions_stats": transactions_stats,
                "daily_stats": daily_stats,
                "monthly_stats": monthly_stats,
            }

        except Exception as e:
            logger.error(f"خطأ في تحليل رصيد الخزنة: {str(e)}")
            raise

    # ==================== إدارة تسويات الخزنة ====================

    def create_treasury_reconciliation(
        self, treasury_id: int, reconciliation_data: Dict[str, Any], user_id: int
    ) -> TreasuryReconciliation:
        """إنشاء تسوية خزنة جديدة"""
        try:
            treasury = self.get_treasury_by_id(treasury_id)
            if not treasury:
                raise ValueError(f"الخزنة غير موجودة: {treasury_id}")

            # إنشاء رقم التسوية
            reconciliation_number = self._generate_reconciliation_number()

            # إنشاء التسوية
            reconciliation = TreasuryReconciliation(
                treasury_id=treasury_id,
                reconciliation_number=reconciliation_number,
                reconciliation_date=reconciliation_data.get(
                    "reconciliation_date", datetime.utcnow()
                ),
                period_start=reconciliation_data["period_start"],
                period_end=reconciliation_data["period_end"],
                book_balance=Decimal(str(reconciliation_data["book_balance"])),
                statement_balance=Decimal(
                    str(reconciliation_data["statement_balance"])
                ),
                notes=reconciliation_data.get("notes"),
                created_by=user_id,
            )

            # حساب الفرق
            reconciliation.calculate_difference()

            self.db.add(reconciliation)
            self.db.commit()

            logger.info(f"تم إنشاء تسوية خزنة جديدة: {reconciliation_number}")
            return reconciliation

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء تسوية الخزنة: {str(e)}")
            raise

    def approve_treasury_reconciliation(
        self, reconciliation_id: int, user_id: int
    ) -> bool:
        """الموافقة على تسوية خزنة"""
        try:
            reconciliation = (
                self.db.query(TreasuryReconciliation)
                .filter(TreasuryReconciliation.id == reconciliation_id)
                .first()
            )

            if not reconciliation:
                raise ValueError(f"تسوية الخزنة غير موجودة: {reconciliation_id}")

            if reconciliation.approve(user_id):
                self.db.commit()
                logger.info(
                    f"تم الموافقة على تسوية الخزنة: {reconciliation.reconciliation_number}"
                )
                return True

            return False

        except Exception as e:
            self.db.rollback()
            logger.error(f"خطأ في الموافقة على تسوية الخزنة: {str(e)}")
            raise

    # ==================== الدوال المساعدة ====================

    def _generate_balance_code(self, balance_type: str) -> str:
        """إنشاء رمز رصيد افتتاحي جديد"""
        prefix_map = {
            "customer": "OB-CUST",
            "supplier": "OB-SUPP",
            "inventory": "OB-INV",
            "cash": "OB-CASH",
            "bank": "OB-BANK",
            "asset": "OB-ASSET",
            "liability": "OB-LIAB",
            "equity": "OB-EQ",
        }

        prefix = prefix_map.get(balance_type, "OB")

        # الحصول على آخر رقم
        last_balance = (
            self.db.query(OpeningBalance)
            .filter(OpeningBalance.balance_code.like(f"{prefix}%"))
            .order_by(desc(OpeningBalance.id))
            .first()
        )

        if last_balance:
            last_number = int(last_balance.balance_code.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}-{new_number:06d}"

    def _generate_treasury_code(self, treasury_type: str) -> str:
        """إنشاء رمز خزنة جديد"""
        prefix_map = {"cash": "CASH", "bank": "BANK", "credit_card": "CC"}

        prefix = prefix_map.get(treasury_type, "TREAS")

        # الحصول على آخر رقم
        last_treasury = (
            self.db.query(Treasury)
            .filter(Treasury.treasury_code.like(f"{prefix}%"))
            .order_by(desc(Treasury.id))
            .first()
        )

        if last_treasury:
            last_number = int(last_treasury.treasury_code.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{prefix}-{new_number:04d}"

    def _generate_adjustment_number(self) -> str:
        """إنشاء رقم تسوية رصيد جديد"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # الحصول على آخر رقم لليوم
        last_adjustment = (
            self.db.query(BalanceAdjustment)
            .filter(BalanceAdjustment.adjustment_number.like(f"ADJ-{today}%"))
            .order_by(desc(BalanceAdjustment.id))
            .first()
        )

        if last_adjustment:
            last_number = int(last_adjustment.adjustment_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"ADJ-{today}-{new_number:04d}"

    def _generate_treasury_transaction_number(self) -> str:
        """إنشاء رقم حركة خزنة جديد"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # الحصول على آخر رقم لليوم
        last_transaction = (
            self.db.query(TreasuryTransaction)
            .filter(TreasuryTransaction.transaction_number.like(f"TT-{today}%"))
            .order_by(desc(TreasuryTransaction.id))
            .first()
        )

        if last_transaction:
            last_number = int(last_transaction.transaction_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"TT-{today}-{new_number:04d}"

    def _generate_reconciliation_number(self) -> str:
        """إنشاء رقم تسوية خزنة جديد"""
        today = datetime.utcnow().strftime("%Y%m%d")

        # الحصول على آخر رقم لليوم
        last_reconciliation = (
            self.db.query(TreasuryReconciliation)
            .filter(TreasuryReconciliation.reconciliation_number.like(f"REC-{today}%"))
            .order_by(desc(TreasuryReconciliation.id))
            .first()
        )

        if last_reconciliation:
            last_number = int(last_reconciliation.reconciliation_number.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"REC-{today}-{new_number:04d}"

    def _create_balance_details(
        self, balance_id: int, details_data: List[Dict[str, Any]]
    ):
        """إنشاء تفاصيل الرصيد الافتتاحي"""
        for detail_data in details_data:
            detail = OpeningBalanceDetail(
                opening_balance_id=balance_id,
                detail_code=detail_data["detail_code"],
                detail_name=detail_data["detail_name"],
                description=detail_data.get("description"),
                quantity=Decimal(str(detail_data.get("quantity", 0))),
                unit_cost=Decimal(str(detail_data.get("unit_cost", 0))),
                lot_number=detail_data.get("lot_number"),
                batch_number=detail_data.get("batch_number"),
                expiry_date=detail_data.get("expiry_date"),
                location=detail_data.get("location"),
            )
            detail.calculate_total_amount()
            self.db.add(detail)

    def _add_opening_balance_transaction(self, treasury: Treasury, user_id: int):
        """إضافة حركة الرصيد الافتتاحي للخزنة"""
        transaction = TreasuryTransaction(
            treasury_id=treasury.id,
            transaction_number=self._generate_treasury_transaction_number(),
            transaction_type=TreasuryTransactionType.OPENING_BALANCE,
            transaction_date=datetime.utcnow(),
            amount=abs(treasury.opening_balance),
            description="الرصيد الافتتاحي",
            currency=treasury.currency,
            created_by=user_id,
        )

        self.db.add(transaction)

    def _get_treasury_transactions_statistics(self, treasury_id: int) -> Dict[str, Any]:
        """إحصائيات حركات الخزنة"""
        transactions = (
            self.db.query(TreasuryTransaction)
            .filter(TreasuryTransaction.treasury_id == treasury_id)
            .all()
        )

        total_transactions = len(transactions)
        total_receipts = sum(
            float(t.amount)
            for t in transactions
            if t.transaction_type
            in [
                TreasuryTransactionType.RECEIPT,
                TreasuryTransactionType.TRANSFER_IN,
                TreasuryTransactionType.DEPOSIT,
            ]
        )
        total_payments = sum(
            float(t.amount)
            for t in transactions
            if t.transaction_type
            in [
                TreasuryTransactionType.PAYMENT,
                TreasuryTransactionType.TRANSFER_OUT,
                TreasuryTransactionType.WITHDRAWAL,
            ]
        )

        # إحصائيات حسب النوع
        type_stats = {}
        for transaction_type in TreasuryTransactionType:
            type_transactions = [
                t for t in transactions if t.transaction_type == transaction_type
            ]
            type_stats[transaction_type.value] = {
                "count": len(type_transactions),
                "total_amount": sum(float(t.amount) for t in type_transactions),
            }

        return {
            "total_transactions": total_transactions,
            "total_receipts": total_receipts,
            "total_payments": total_payments,
            "net_amount": total_receipts - total_payments,
            "type_statistics": type_stats,
        }

    def _get_monthly_transactions_analysis(self, treasury_id: int) -> Dict[str, Any]:
        """تحليل الحركات الشهرية"""
        # آخر 12 شهر
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)

        transactions = (
            self.db.query(TreasuryTransaction)
            .filter(
                and_(
                    TreasuryTransaction.treasury_id == treasury_id,
                    TreasuryTransaction.transaction_date >= twelve_months_ago,
                )
            )
            .all()
        )

        # تجميع حسب الشهر
        monthly_data = {}
        for transaction in transactions:
            month_key = transaction.transaction_date.strftime("%Y-%m")

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    "receipts": 0,
                    "payments": 0,
                    "transaction_count": 0,
                }

            monthly_data[month_key]["transaction_count"] += 1

            if transaction.transaction_type in [
                TreasuryTransactionType.RECEIPT,
                TreasuryTransactionType.TRANSFER_IN,
                TreasuryTransactionType.DEPOSIT,
            ]:
                monthly_data[month_key]["receipts"] += float(transaction.amount)
            elif transaction.transaction_type in [
                TreasuryTransactionType.PAYMENT,
                TreasuryTransactionType.TRANSFER_OUT,
                TreasuryTransactionType.WITHDRAWAL,
            ]:
                monthly_data[month_key]["payments"] += float(transaction.amount)

        # حساب صافي الحركة لكل شهر
        for month_data in monthly_data.values():
            month_data["net"] = month_data["receipts"] - month_data["payments"]

        return monthly_data
