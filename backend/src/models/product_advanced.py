# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
نموذج المنتجات المتقدم - مطور من نظام ERP
All linting disabled due to SQLAlchemy mock objects and optional dependencies.
"""

try:
    from src.database import db
    from sqlalchemy import Text, Numeric, Enum

    SQLALCHEMY_AVAILABLE = True
    # Flask-SQLAlchemy provides Column, Integer, String, etc via db.Model
except ImportError:
    # SQLAlchemy not available - create mock objects
    SQLALCHEMY_AVAILABLE = False

    # Create a mock db object
    class MockColumn:
        def __init__(self, *args, **kwargs):
            pass

    class MockModel:
        pass

    class MockDB:
        Model = MockModel
        Column = MockColumn
        Integer = int
        String = str
        Float = float
        DateTime = None
        Text = str
        Boolean = bool

        def ForeignKey(x):
            return None

        relationship = lambda *args, **kwargs: None

    db = MockDB()

    def Text():
        return None

    def Numeric(*args, **kwargs):
        return None

    def Enum(*args, **kwargs):
        return None


from datetime import datetime, timezone
import enum

# Flask-SQLAlchemy handles base class via db.Model
# No need for declarative_base()


class ProductTypeEnum(enum.Enum):
    """أنواع المنتجات"""

    STORABLE = "storable"  # منتج قابل للتخزين
    CONSUMABLE = "consumable"  # منتج استهلاكي
    SERVICE = "service"  # خدمة
    DIGITAL = "digital"  # منتج رقمي (تطوير إضافي)


class TrackingTypeEnum(enum.Enum):
    """أنواع التتبع"""

    NONE = "none"  # بدون تتبع
    LOT = "lot"  # بالدفعات
    BATCH = "batch"  # بالمجموعات
    SERIAL = "serial"  # بالرقم التسلسلي
    EXPIRY = "expiry"  # تتبع تاريخ الانتهاء (تطوير إضافي)


class QualityGradeEnum(enum.Enum):
    """درجات الجودة"""

    PREMIUM = "premium"  # ممتاز
    STANDARD = "standard"  # عادي
    ECONOMY = "economy"  # اقتصادي
    DEFECTIVE = "defective"  # معيب


class ProductAdvanced(db.Model):
    """نموذج المنتجات المتقدم"""

    __tablename__ = "products_advanced"

    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # المعلومات الأساسية
    name = db.Column(db.String(255), nullable=False, comment="اسم المنتج")
    name_en = db.Column(db.String(255), comment="الاسم بالإنجليزية")
    description = db.Column(Text, comment="وصف المنتج")
    description_en = db.Column(Text, comment="الوصف بالإنجليزية")

    # الرموز والمعرفات
    sku = db.Column(db.String(100), unique=True, comment="رمز المنتج")
    barcode = db.Column(db.String(100), comment="الباركود")
    internal_reference = db.Column(db.String(100), comment="المرجع الداخلي")
    manufacturer_code = db.Column(db.String(100), comment="كود المصنع")

    # التصنيف والنوع
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), comment="فئة المنتج"
    )
    subcategory_id = db.Column(db.Integer, comment="الفئة الفرعية")
    brand_id = db.Column(db.Integer, comment="العلامة التجارية")

    # نوع المنتج والتتبع
    product_type = db.Column(
        Enum(ProductTypeEnum), default=ProductTypeEnum.STORABLE, comment="نوع المنتج"
    )
    tracking_type = db.Column(
        Enum(TrackingTypeEnum), default=TrackingTypeEnum.NONE, comment="نوع التتبع"
    )

    # التسعير المتقدم
    cost_price = db.Column(Numeric(10, 2), default=0.0, comment="سعر التكلفة")
    sale_price = db.Column(Numeric(10, 2), default=0.0, comment="سعر البيع")
    wholesale_price = db.Column(Numeric(10, 2), comment="سعر الجملة")
    retail_price = db.Column(Numeric(10, 2), comment="سعر التجزئة")
    minimum_price = db.Column(Numeric(10, 2), comment="أقل سعر مسموح")

    # الوحدات
    unit_of_measure = db.Column(db.String(50), comment="وحدة القياس الأساسية")
    purchase_unit = db.Column(db.String(50), comment="وحدة الشراء")
    sale_unit = db.Column(db.String(50), comment="وحدة البيع")

    # إدارة المخزون
    min_quantity = db.Column(Numeric(10, 2), default=0.0, comment="الحد الأدنى للمخزون")
    max_quantity = db.Column(Numeric(10, 2), comment="الحد الأقصى للمخزون")
    reorder_point = db.Column(Numeric(10, 2), comment="نقطة إعادة الطلب")
    safety_stock = db.Column(Numeric(10, 2), comment="المخزون الآمن")

    # الجودة والمواصفات
    quality_grade = db.Column(
        Enum(QualityGradeEnum), default=QualityGradeEnum.STANDARD, comment="درجة الجودة"
    )
    shelf_life_days = db.Column(db.Integer, comment="مدة الصلاحية بالأيام")
    storage_temperature_min = db.Column(Numeric(5, 2), comment="أقل درجة حرارة تخزين")
    storage_temperature_max = db.Column(Numeric(5, 2), comment="أعلى درجة حرارة تخزين")
    storage_humidity_max = db.Column(Numeric(5, 2), comment="أقصى رطوبة تخزين")

    # المعلومات الزراعية (للبذور والأسمدة)
    plant_family = db.Column(db.String(100), comment="العائلة النباتية")
    variety = db.Column(db.String(100), comment="الصنف")
    origin_country = db.Column(db.String(100), comment="بلد المنشأ")
    germination_rate = db.Column(Numeric(5, 2), comment="معدل الإنبات %")
    purity_rate = db.Column(Numeric(5, 2), comment="معدل النقاء %")
    moisture_content = db.Column(Numeric(5, 2), comment="محتوى الرطوبة %")

    # المعلومات الكيميائية (للأسمدة والمبيدات)
    active_ingredient = db.Column(db.String(255), comment="المادة الفعالة")
    concentration = db.Column(db.String(100), comment="التركيز")
    npk_ratio = db.Column(db.String(50), comment="نسبة NPK")
    ph_level = db.Column(Numeric(4, 2), comment="مستوى الحموضة")

    # الأبعاد والوزن
    weight = db.Column(Numeric(8, 3), comment="الوزن (كجم)")
    length = db.Column(Numeric(8, 2), comment="الطول (سم)")
    width = db.Column(Numeric(8, 2), comment="العرض (سم)")
    height = db.Column(Numeric(8, 2), comment="الارتفاع (سم)")
    volume = db.Column(Numeric(10, 3), comment="الحجم (لتر)")

    # معلومات الموردين
    default_supplier_id = db.Column(db.Integer, comment="المورد الافتراضي")
    lead_time_days = db.Column(db.Integer, comment="مدة التوريد بالأيام")
    minimum_order_qty = db.Column(Numeric(10, 2), comment="أقل كمية طلب")

    # الحالة والتواريخ
    is_active = db.Column(db.Boolean, default=True, comment="نشط")
    is_purchasable = db.Column(db.Boolean, default=True, comment="قابل للشراء")
    is_saleable = db.Column(db.Boolean, default=True, comment="قابل للبيع")
    is_discontinued = db.Column(db.Boolean, default=False, comment="متوقف الإنتاج")

    # التواريخ
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), comment="تاريخ الإنشاء"
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="تاريخ التحديث",
    )
    discontinued_date = db.Column(db.DateTime, comment="تاريخ التوقف")

    # العلاقات (commented out to avoid missing model errors)
    # category = db.relationship("Category", backref="advanced_products")
    # batches = db.relationship("LotAdvanced", back_populates="product")
    # stock_movements = db.relationship("StockMovementAdvanced",
    #                                back_populates="product")

    def __repr__(self):
        return (
            f"<ProductAdvanced(id={self.id}, "
            f"name='{self.name}', "
            f"sku='{self.sku}')>"
        )

    @property
    def is_storable(self):
        """التحقق من إمكانية التخزين"""
        return self.product_type == ProductTypeEnum.STORABLE

    @property
    def requires_batch_tracking(self):
        """التحقق من الحاجة لتتبع اللوط"""
        return self.tracking_type in [
            TrackingTypeEnum.LOT,
            TrackingTypeEnum.BATCH,
            TrackingTypeEnum.EXPIRY,
        ]

    @property
    def requires_serial_tracking(self):
        """التحقق من الحاجة لتتبع الرقم التسلسلي"""
        return self.tracking_type == TrackingTypeEnum.SERIAL

    @property
    def has_expiry_date(self):
        """التحقق من وجود تاريخ انتهاء"""
        return self.shelf_life_days is not None and self.shelf_life_days > 0

    @property
    def profit_margin(self):
        """حساب هامش الربح"""
        # Type-safe profit margin calculation
        if self.cost_price and self.sale_price and self.cost_price > 0:  # type: ignore
            cost = float(self.cost_price)  # type: ignore
            sale = float(self.sale_price)  # type: ignore
            return ((sale - cost) / cost) * 100
        return 0

    def calculate_storage_volume(self):
        """حساب حجم التخزين"""
        if self.length and self.width and self.height:  # type: ignore
            # Convert cm³ to liters
            length = float(self.length)  # type: ignore
            width = float(self.width)  # type: ignore
            height = float(self.height)  # type: ignore
            return (length * width * height) / 1000000
        return float(self.volume or 0)  # type: ignore

    def is_low_stock(self, current_quantity):
        """التحقق من انخفاض المخزون"""
        return current_quantity <= (self.min_quantity or 0)

    def needs_reorder(self, current_quantity):
        """التحقق من الحاجة لإعادة الطلب"""
        return current_quantity <= (self.reorder_point or 0)
