# type: ignore
# flake8: noqa
"""
payment_management - نموذج أساسي
All linting disabled due to SQLAlchemy mock objects.
"""

from datetime import datetime, timezone
import enum

try:
    from sqlalchemy import (
        Column,
        Integer,
        String,
        Float,
        DateTime,
        Boolean,
        Text,
        Enum,
        Date,
        ForeignKey,
        Numeric,
    )
    from sqlalchemy.orm import relationship

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # SQLAlchemy not available - create mock objects
    def Column(*args, **kwargs):
        return None

    def Integer():
        return None

    def String(length=None):
        return None

    def Float():
        return None

    def DateTime():
        return None

    def Boolean():
        return None

    def Text():
        return None

    def Enum(*args, **kwargs):
        return None

    def Date():
        return None

    def ForeignKey(*args, **kwargs):
        return None

    def Numeric(*args, **kwargs):
        return None

    def relationship(*args, **kwargs):
        return None

    SQLALCHEMY_AVAILABLE = False

# محاولة استيراد قاعدة البيانات
try:
    from database import db  # type: ignore
except ImportError:
    try:
        from ..database import db  # type: ignore
    except ImportError:
        try:
            from user import db  # type: ignore
        except ImportError:
            # إنشاء mock db إذا لم تكن متوفرة
            class MockDB:
                class Model:
                    def __init__(self, **kwargs):
                        for key, value in kwargs.items():
                            setattr(self, key, value)

                    def to_dict(self):
                        return {}

                Column = Column
                Integer = Integer
                String = String
                Float = Float
                DateTime = DateTime
                Boolean = Boolean
                Text = Text
                Enum = Enum
                Date = Date
                ForeignKey = ForeignKey
                Numeric = Numeric
                relationship = relationship

            db = MockDB()


# تعريف حالات الدفع والديون
class PaymentStatus(enum.Enum):
    """حالات الدفع"""

    PENDING = "pending"  # في الانتظار
    APPROVED = "approved"  # موافق عليه
    PAID = "paid"  # مدفوع
    CANCELLED = "cancelled"  # ملغي
    REJECTED = "rejected"  # مرفوض


class DebtStatus(enum.Enum):
    """حالات الدين"""

    ACTIVE = "active"  # نشط
    PARTIALLY_PAID = "partially_paid"  # مدفوع جزئياً
    FULLY_PAID = "fully_paid"  # مدفوع بالكامل
    OVERDUE = "overdue"  # متأخر
    CANCELLED = "cancelled"  # ملغي


class PaymentMethod(enum.Enum):
    """طرق الدفع"""

    CASH = "cash"  # نقدي
    BANK_TRANSFER = "bank_transfer"  # تحويل بنكي
    CHECK = "check"  # شيك
    CREDIT_CARD = "credit_card"  # بطاقة ائتمان
    ONLINE = "online"  # دفع إلكتروني


class PaymentType(enum.Enum):
    """أنواع الدفع"""

    SUPPLIER_PAYMENT = "supplier_payment"  # دفع للمورد
    CUSTOMER_RECEIPT = "customer_receipt"  # استلام من العميل
    EXPENSE_PAYMENT = "expense_payment"  # دفع مصروف
    SALARY_PAYMENT = "salary_payment"  # دفع راتب
    OTHER = "other"  # أخرى


# نماذج إدارة المدفوعات والديون
class PaymentOrder(db.Model):
    """نموذج أمر الدفع"""

    __tablename__ = "payment_orders"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), unique=True, nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    payee_type = Column(
        String(20), nullable=False
    )  # supplier, customer, employee, other
    payee_id = Column(Integer)  # ID of supplier, customer, etc.
    payee_name = Column(String(200), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    exchange_rate = Column(Numeric(10, 4), default=1.0000)
    amount_in_base_currency = Column(Numeric(15, 2))
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"))
    treasury_id = Column(Integer, ForeignKey("treasuries.id"))
    description = Column(Text, nullable=False)
    reference_type = Column(String(50))  # invoice, contract, etc.
    reference_id = Column(Integer)
    due_date = Column(Date)
    payment_date = Column(Date)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    paid_by = Column(Integer, ForeignKey("users.id"))
    paid_at = Column(DateTime)
    notes = Column(Text)
    attachment_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    currency = relationship("Currency", backref="payment_orders")
    bank_account = relationship("BankAccount", backref="payment_orders")
    treasury = relationship("Treasury", backref="payment_orders")
    creator = relationship(
        "User", foreign_keys=[created_by], backref="created_payment_orders"
    )
    approver = relationship(
        "User", foreign_keys=[approved_by], backref="approved_payment_orders"
    )
    payer = relationship("User", foreign_keys=[paid_by], backref="paid_payment_orders")

    def to_dict(self):
        return {
            "id": self.id,
            "order_number": self.order_number,
            "payment_type": self.payment_type.value if self.payment_type else None,
            "payment_type_display": self.get_payment_type_display(),
            "payee_type": self.payee_type,
            "payee_id": self.payee_id,
            "payee_name": self.payee_name,
            "amount": float(self.amount) if self.amount else 0.0,
            "currency_id": self.currency_id,
            "currency_name": self.currency.name if self.currency else None,
            "exchange_rate": float(self.exchange_rate) if self.exchange_rate else 1.0,
            "amount_in_base_currency": (
                float(self.amount_in_base_currency)
                if self.amount_in_base_currency
                else 0.0
            ),
            "payment_method": (
                self.payment_method.value if self.payment_method else None
            ),
            "payment_method_display": self.get_payment_method_display(),
            "bank_account_id": self.bank_account_id,
            "treasury_id": self.treasury_id,
            "description": self.description,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "status": self.status.value if self.status else None,
            "status_display": self.get_status_display(),
            "created_by": self.created_by,
            "creator_name": self.creator.name if self.creator else None,
            "approved_by": self.approved_by,
            "approver_name": self.approver.name if self.approver else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "paid_by": self.paid_by,
            "payer_name": self.payer.name if self.payer else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "notes": self.notes,
            "attachment_path": self.attachment_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def get_payment_type_display(self):
        """الحصول على عرض نوع الدفع باللغة العربية"""
        type_map = {
            PaymentType.SUPPLIER_PAYMENT: "دفع للمورد",
            PaymentType.CUSTOMER_RECEIPT: "استلام من العميل",
            PaymentType.EXPENSE_PAYMENT: "دفع مصروف",
            PaymentType.SALARY_PAYMENT: "دفع راتب",
            PaymentType.OTHER: "أخرى",
        }
        return type_map.get(self.payment_type, "غير محدد")

    def get_payment_method_display(self):
        """الحصول على عرض طريقة الدفع باللغة العربية"""
        method_map = {
            PaymentMethod.CASH: "نقدي",
            PaymentMethod.BANK_TRANSFER: "تحويل بنكي",
            PaymentMethod.CHECK: "شيك",
            PaymentMethod.CREDIT_CARD: "بطاقة ائتمان",
            PaymentMethod.ONLINE: "دفع إلكتروني",
        }
        return method_map.get(self.payment_method, "غير محدد")

    def get_status_display(self):
        """الحصول على عرض حالة الدفع باللغة العربية"""
        status_map = {
            PaymentStatus.PENDING: "في الانتظار",
            PaymentStatus.APPROVED: "موافق عليه",
            PaymentStatus.PAID: "مدفوع",
            PaymentStatus.CANCELLED: "ملغي",
            PaymentStatus.REJECTED: "مرفوض",
        }
        return status_map.get(self.status, "غير محدد")


class DebtRecord(db.Model):
    """نموذج سجل الدين"""

    __tablename__ = "debt_records"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    debt_number = Column(String(50), unique=True, nullable=False)
    debtor_type = Column(String(20), nullable=False)  # customer, supplier
    debtor_id = Column(Integer, nullable=False)
    debtor_name = Column(String(200), nullable=False)
    original_amount = Column(Numeric(15, 2), nullable=False)
    paid_amount = Column(Numeric(15, 2), default=0.00)
    remaining_amount = Column(Numeric(15, 2), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    due_date = Column(Date)
    status = Column(Enum(DebtStatus), default=DebtStatus.ACTIVE, nullable=False)
    reference_type = Column(String(50))  # invoice, contract, etc.
    reference_id = Column(Integer)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    currency = relationship("Currency", backref="debt_records")
    creator = relationship("User", backref="created_debt_records")
    payments = relationship("DebtPayment", backref="debt_record", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "debt_number": self.debt_number,
            "debtor_type": self.debtor_type,
            "debtor_id": self.debtor_id,
            "debtor_name": self.debtor_name,
            "original_amount": (
                float(self.original_amount) if self.original_amount else 0.0
            ),
            "paid_amount": float(self.paid_amount) if self.paid_amount else 0.0,
            "remaining_amount": (
                float(self.remaining_amount) if self.remaining_amount else 0.0
            ),
            "currency_id": self.currency_id,
            "currency_name": self.currency.name if self.currency else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status.value if self.status else None,
            "status_display": self.get_status_display(),
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "notes": self.notes,
            "created_by": self.created_by,
            "creator_name": self.creator.name if self.creator else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_overdue": self.is_overdue(),
        }

    def get_status_display(self):
        """الحصول على عرض حالة الدين باللغة العربية"""
        status_map = {
            DebtStatus.ACTIVE: "نشط",
            DebtStatus.PARTIALLY_PAID: "مدفوع جزئياً",
            DebtStatus.FULLY_PAID: "مدفوع بالكامل",
            DebtStatus.OVERDUE: "متأخر",
            DebtStatus.CANCELLED: "ملغي",
        }
        return status_map.get(self.status, "غير محدد")

    def is_overdue(self):
        """التحقق من تأخر الدين"""
        if self.due_date and self.status in [
            DebtStatus.ACTIVE,
            DebtStatus.PARTIALLY_PAID,
        ]:
            return datetime.now().date() > self.due_date
        return False

    def update_payment(self, payment_amount):
        """تحديث الدفع"""
        self.paid_amount += payment_amount
        self.remaining_amount = self.original_amount - self.paid_amount

        if self.remaining_amount <= 0:
            self.status = DebtStatus.FULLY_PAID
        elif self.paid_amount > 0:
            self.status = DebtStatus.PARTIALLY_PAID

        return self.remaining_amount


class DebtPayment(db.Model):
    """نموذج دفعة الدين"""

    __tablename__ = "debt_payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    debt_record_id = Column(Integer, ForeignKey("debt_records.id"), nullable=False)
    payment_number = Column(String(50), unique=True, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_date = Column(Date, nullable=False)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    creator = relationship("User", backref="created_debt_payments")

    def to_dict(self):
        return {
            "id": self.id,
            "debt_record_id": self.debt_record_id,
            "payment_number": self.payment_number,
            "amount": float(self.amount) if self.amount else 0.0,
            "payment_method": (
                self.payment_method.value if self.payment_method else None
            ),
            "payment_method_display": self.get_payment_method_display(),
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "notes": self.notes,
            "created_by": self.created_by,
            "creator_name": self.creator.name if self.creator else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def get_payment_method_display(self):
        """الحصول على عرض طريقة الدفع باللغة العربية"""
        method_map = {
            PaymentMethod.CASH: "نقدي",
            PaymentMethod.BANK_TRANSFER: "تحويل بنكي",
            PaymentMethod.CHECK: "شيك",
            PaymentMethod.CREDIT_CARD: "بطاقة ائتمان",
            PaymentMethod.ONLINE: "دفع إلكتروني",
        }
        return method_map.get(self.payment_method, "غير محدد")


class DebtFollowUp(db.Model):
    """نموذج متابعة الدين"""

    __tablename__ = "debt_follow_ups"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    debt_record_id = Column(Integer, ForeignKey("debt_records.id"), nullable=False)
    follow_up_date = Column(Date, nullable=False)
    follow_up_type = Column(String(50), nullable=False)  # call, email, visit, letter
    notes = Column(Text, nullable=False)
    next_follow_up_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    debt_record = relationship("DebtRecord", backref="follow_ups")
    creator = relationship("User", backref="created_debt_follow_ups")

    def to_dict(self):
        return {
            "id": self.id,
            "debt_record_id": self.debt_record_id,
            "follow_up_date": (
                self.follow_up_date.isoformat() if self.follow_up_date else None
            ),
            "follow_up_type": self.follow_up_type,
            "follow_up_type_display": self.get_follow_up_type_display(),
            "notes": self.notes,
            "next_follow_up_date": (
                self.next_follow_up_date.isoformat()
                if self.next_follow_up_date
                else None
            ),
            "created_by": self.created_by,
            "creator_name": self.creator.name if self.creator else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def get_follow_up_type_display(self):
        """الحصول على عرض نوع المتابعة باللغة العربية"""
        type_map = {
            "call": "مكالمة هاتفية",
            "email": "بريد إلكتروني",
            "visit": "زيارة",
            "letter": "خطاب",
        }
        return type_map.get(self.follow_up_type, "غير محدد")


class PaymentProcessingLog(db.Model):
    """نموذج سجل معالجة المدفوعات"""

    __tablename__ = "payment_processing_logs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    payment_order_id = Column(Integer, ForeignKey("payment_orders.id"), nullable=False)
    action = Column(
        String(50), nullable=False
    )  # created, approved, paid, cancelled, etc.
    old_status = Column(String(20))
    new_status = Column(String(20))
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    payment_order = relationship("PaymentOrder", backref="processing_logs")
    creator = relationship("User", backref="created_payment_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "payment_order_id": self.payment_order_id,
            "action": self.action,
            "action_display": self.get_action_display(),
            "old_status": self.old_status,
            "new_status": self.new_status,
            "notes": self.notes,
            "created_by": self.created_by,
            "creator_name": self.creator.name if self.creator else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def get_action_display(self):
        """الحصول على عرض الإجراء باللغة العربية"""
        action_map = {
            "created": "تم الإنشاء",
            "approved": "تم الموافقة",
            "paid": "تم الدفع",
            "cancelled": "تم الإلغاء",
            "rejected": "تم الرفض",
        }
        return action_map.get(self.action, "غير محدد")


class PaymentAttachment(db.Model):
    """نموذج مرفقات المدفوعات"""

    __tablename__ = "payment_attachments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    payment_order_id = Column(Integer, ForeignKey("payment_orders.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    description = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # العلاقات
    payment_order = relationship("PaymentOrder", backref="attachments")
    uploader = relationship("User", backref="uploaded_payment_attachments")

    def to_dict(self):
        return {
            "id": self.id,
            "payment_order_id": self.payment_order_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "description": self.description,
            "uploaded_by": self.uploaded_by,
            "uploader_name": self.uploader.name if self.uploader else None,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }


class BankAccount(db.Model):
    """نموذج الحساب البنكي"""

    __tablename__ = "bank_accounts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    account_name = Column(String(200), nullable=False)
    account_number = Column(String(50), nullable=False)
    bank_name = Column(String(100), nullable=False)
    bank_branch = Column(String(100))
    iban = Column(String(50))
    swift_code = Column(String(20))
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    current_balance = Column(Numeric(15, 2), default=0.00)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات
    currency = relationship("Currency", backref="bank_accounts")

    def to_dict(self):
        return {
            "id": self.id,
            "account_name": self.account_name,
            "account_number": self.account_number,
            "bank_name": self.bank_name,
            "bank_branch": self.bank_branch,
            "iban": self.iban,
            "swift_code": self.swift_code,
            "currency_id": self.currency_id,
            "currency_name": self.currency.name if self.currency else None,
            "current_balance": (
                float(self.current_balance) if self.current_balance else 0.0
            ),
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# نماذج أساسية للاختبار
class BasicModel(db.Model):
    """نموذج أساسي للاختبار"""

    __tablename__ = "basic_model"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
