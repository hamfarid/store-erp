"""
نموذج اللوط المتقدم - محدث ومحسّن
Updated: 2025-12-13
"""

from datetime import datetime, date
import enum
from sqlalchemy import event

try:
    from database import db
except ImportError:
    from ..database import db


class LotStatusEnum(enum.Enum):
    """حالات اللوط"""
    ACTIVE = "active"  # نشط
    EXPIRED = "expired"  # منتهي الصلاحية
    QUARANTINE = "quarantine"  # في الحجر الصحي
    RECALLED = "recalled"  # مسحوب
    DAMAGED = "damaged"  # تالف
    RESERVED = "reserved"  # محجوز
    SOLD_OUT = "sold_out"  # نفذت الكمية


class QualityStatusEnum(enum.Enum):
    """حالات الجودة"""
    PENDING = "pending"  # في انتظار الفحص
    APPROVED = "approved"  # معتمد
    REJECTED = "rejected"  # مرفوض
    CONDITIONAL = "conditional"  # مشروط


class LotAdvanced(db.Model):
    """نموذج اللوط المتقدم"""
    __tablename__ = "batches_advanced"
    __table_args__ = {"extend_existing": True}

    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # المعلومات الأساسية
    batch_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    internal_batch_number = db.Column(db.String(100))
    supplier_batch_number = db.Column(db.String(100))
    ministry_batch_number = db.Column(db.String(100), index=True)

    # الربط مع الجداول الأخرى
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id", ondelete="SET NULL"), index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id", ondelete="SET NULL"), index=True)

    # الكميات والأسعار
    quantity = db.Column(db.Integer, nullable=False, default=0)
    original_quantity = db.Column(db.Integer)
    reserved_quantity = db.Column(db.Integer, default=0)
    cost_price = db.Column(db.Numeric(10, 2))
    selling_price = db.Column(db.Numeric(10, 2))

    # التواريخ
    manufacture_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date, index=True)
    received_date = db.Column(db.Date)
    first_sale_date = db.Column(db.Date)
    last_sale_date = db.Column(db.Date)

    # معلومات الجودة (للبذور والأسمدة)
    germination_rate = db.Column(db.Float)  # معدل الإنبات (0-100)
    purity_percentage = db.Column(db.Float)  # نسبة النقاء (0-100)
    moisture_content = db.Column(db.Float)  # نسبة الرطوبة (0-100)
    temperature_storage = db.Column(db.Float)  # درجة حرارة التخزين
    ph_level = db.Column(db.Float)  # مستوى الحموضة
    nutrient_content = db.Column(db.Text)  # محتوى المغذيات (JSON)

    # الحالات
    status = db.Column(db.String(20), default='active', index=True)
    quality_status = db.Column(db.String(20), default='pending', index=True)

    # فحص الجودة
    quality_test_date = db.Column(db.Date)
    quality_test_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    quality_notes = db.Column(db.Text)
    quality_certificate_number = db.Column(db.String(100))
    quality_certificate_url = db.Column(db.String(255))

    # موافقة الوزارة
    ministry_approval_date = db.Column(db.Date)
    ministry_approval_number = db.Column(db.String(100))
    ministry_inspector = db.Column(db.String(200))
    ministry_notes = db.Column(db.Text)
    ministry_certificate_url = db.Column(db.String(255))

    # معلومات إضافية
    storage_location = db.Column(db.String(100))
    storage_conditions = db.Column(db.Text)
    handling_instructions = db.Column(db.Text)
    safety_warnings = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)  # JSON array

    # التدقيق
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))

    def __repr__(self):
        return f"<LotAdvanced(id={self.id}, batch_number='{self.batch_number}', product_id={self.product_id})>"

    @property
    def available_quantity(self):
        """الكمية المتاحة (الكمية - المحجوز)"""
        return max(0, (self.quantity or 0) - (self.reserved_quantity or 0))

    @property
    def is_expired(self):
        """التحقق من انتهاء الصلاحية"""
        if not self.expiry_date:
            return False
        return self.expiry_date < date.today()

    @property
    def days_until_expiry(self):
        """عدد الأيام حتى انتهاء الصلاحية"""
        if not self.expiry_date:
            return None
        delta = self.expiry_date - date.today()
        return delta.days

    @property
    def is_near_expiry(self, warning_days=30):
        """التحقق من قرب انتهاء الصلاحية"""
        days_left = self.days_until_expiry
        return days_left is not None and 0 <= days_left <= warning_days

    @property
    def is_available(self):
        """التحقق من توفر اللوط للبيع"""
        return (
            self.status == 'active' and
            self.quality_status == 'approved' and
            self.available_quantity > 0 and
            not self.is_expired
        )

    def reserve_quantity(self, qty):
        """حجز كمية من اللوط"""
        if qty > self.available_quantity:
            raise ValueError(f"الكمية المطلوبة ({qty}) أكبر من المتاح ({self.available_quantity})")
        self.reserved_quantity = (self.reserved_quantity or 0) + qty
        return True

    def release_quantity(self, qty):
        """إلغاء حجز كمية"""
        if qty > (self.reserved_quantity or 0):
            raise ValueError(f"الكمية المطلوب إلغاؤها ({qty}) أكبر من المحجوز ({self.reserved_quantity})")
        self.reserved_quantity = (self.reserved_quantity or 0) - qty
        return True

    def sell_quantity(self, qty):
        """بيع كمية من اللوط"""
        if qty > self.quantity:
            raise ValueError(f"الكمية المطلوبة ({qty}) أكبر من الموجود ({self.quantity})")
        
        self.quantity -= qty
        
        # تحديث المحجوز إذا كان موجود
        if self.reserved_quantity and self.reserved_quantity >= qty:
            self.reserved_quantity -= qty
        
        # تحديث الحالة إذا نفذت الكمية
        if self.quantity == 0:
            self.status = 'sold_out'
        
        # تحديث تواريخ البيع
        if not self.first_sale_date:
            self.first_sale_date = date.today()
        self.last_sale_date = date.today()
        
        return True

    def add_quantity(self, qty):
        """إضافة كمية للوط (في حالة الإرجاع)"""
        self.quantity += qty
        if self.status == 'sold_out' and self.quantity > 0:
            self.status = 'active'
        return True

    def to_dict(self):
        """تحويل إلى Dictionary"""
        return {
            'id': self.id,
            'batch_number': self.batch_number,
            'internal_batch_number': self.internal_batch_number,
            'supplier_batch_number': self.supplier_batch_number,
            'ministry_batch_number': self.ministry_batch_number,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'supplier_id': self.supplier_id,
            'quantity': self.quantity,
            'original_quantity': self.original_quantity,
            'reserved_quantity': self.reserved_quantity,
            'available_quantity': self.available_quantity,
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'selling_price': float(self.selling_price) if self.selling_price else None,
            'manufacture_date': self.manufacture_date.isoformat() if self.manufacture_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'received_date': self.received_date.isoformat() if self.received_date else None,
            'first_sale_date': self.first_sale_date.isoformat() if self.first_sale_date else None,
            'last_sale_date': self.last_sale_date.isoformat() if self.last_sale_date else None,
            'germination_rate': float(self.germination_rate) if self.germination_rate else None,
            'purity_percentage': float(self.purity_percentage) if self.purity_percentage else None,
            'moisture_content': float(self.moisture_content) if self.moisture_content else None,
            'temperature_storage': float(self.temperature_storage) if self.temperature_storage else None,
            'ph_level': float(self.ph_level) if self.ph_level else None,
            'nutrient_content': self.nutrient_content,
            'status': self.status,
            'quality_status': self.quality_status,
            'quality_test_date': self.quality_test_date.isoformat() if self.quality_test_date else None,
            'quality_test_by': self.quality_test_by,
            'quality_notes': self.quality_notes,
            'quality_certificate_number': self.quality_certificate_number,
            'quality_certificate_url': self.quality_certificate_url,
            'ministry_approval_date': self.ministry_approval_date.isoformat() if self.ministry_approval_date else None,
            'ministry_approval_number': self.ministry_approval_number,
            'ministry_inspector': self.ministry_inspector,
            'ministry_notes': self.ministry_notes,
            'ministry_certificate_url': self.ministry_certificate_url,
            'storage_location': self.storage_location,
            'storage_conditions': self.storage_conditions,
            'handling_instructions': self.handling_instructions,
            'safety_warnings': self.safety_warnings,
            'notes': self.notes,
            'tags': self.tags,
            'is_expired': self.is_expired,
            'is_available': self.is_available,
            'days_until_expiry': self.days_until_expiry,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }


# Event listener للتحديث التلقائي
@event.listens_for(LotAdvanced, 'before_update')
def receive_before_update(mapper, connection, target):
    """تحديث updated_at تلقائياً"""
    target.updated_at = datetime.utcnow()


@event.listens_for(LotAdvanced, 'before_insert')
@event.listens_for(LotAdvanced, 'before_update')
def check_expiry_status(mapper, connection, target):
    """فحص وتحديث حالة الانتهاء تلقائياً"""
    if target.expiry_date and target.expiry_date < date.today() and target.status == 'active':
        target.status = 'expired'
    
    if target.quantity == 0 and target.status == 'active':
        target.status = 'sold_out'
