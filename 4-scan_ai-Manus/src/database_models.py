# File: /home/ubuntu/clean_project/src/database_models.py
"""
مسار الملف: /home/ubuntu/clean_project/src/database_models.py

نماذج قاعدة البيانات لنظام Gaara Scan AI
تحتوي على جميع الجداول والعلاقات المطلوبة للنظام
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import hashlib
import secrets

Base = declarative_base()

class User(Base):
    """نموذج المستخدمين"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # العلاقات
    activity_logs = relationship("ActivityLog", back_populates="user")
    diagnoses = relationship("Diagnosis", back_populates="user")
    
    def set_password(self, password):
        """تشفير كلمة المرور"""
        salt = secrets.token_hex(16)
        self.password_hash = hashlib.pbkdf2_hmac('sha256', 
                                               password.encode('utf-8'), 
                                               salt.encode('utf-8'), 
                                               100000).hex() + ':' + salt
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        try:
            hash_part, salt = self.password_hash.split(':')
            return hash_part == hashlib.pbkdf2_hmac('sha256',
                                                  password.encode('utf-8'),
                                                  salt.encode('utf-8'),
                                                  100000).hex()
        except:
            return False

class Crop(Base):
    """نموذج المحاصيل"""
    __tablename__ = 'crops'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    scientific_name = Column(String(150))
    category = Column(String(50))
    description = Column(Text)
    image_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    diseases = relationship("Disease", back_populates="crop")
    diagnoses = relationship("Diagnosis", back_populates="crop")

class Disease(Base):
    """نموذج الأمراض"""
    __tablename__ = 'diseases'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=False)
    severity = Column(String(20))  # low, medium, high
    symptoms = Column(JSON)  # قائمة الأعراض
    treatment = Column(Text)
    prevention = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    crop = relationship("Crop", back_populates="diseases")
    diagnoses = relationship("Diagnosis", back_populates="disease")

class Diagnosis(Base):
    """نموذج التشخيصات"""
    __tablename__ = 'diagnoses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=False)
    disease_id = Column(Integer, ForeignKey('diseases.id'))
    image_path = Column(String(255), nullable=False)
    confidence = Column(Float)
    status = Column(String(20), default='completed')  # pending, processing, completed, failed
    results = Column(JSON)  # نتائج التشخيص التفصيلية
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # العلاقات
    user = relationship("User", back_populates="diagnoses")
    crop = relationship("Crop", back_populates="diagnoses")
    disease = relationship("Disease", back_populates="diagnoses")

class AIAgent(Base):
    """نموذج الوكلاء الذكيين"""
    __tablename__ = 'ai_agents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # main_coordinator, specialist, monitoring
    status = Column(String(20), default='active')  # active, inactive, error
    capabilities = Column(JSON)  # قائمة القدرات
    configuration = Column(JSON)  # إعدادات الوكيل
    performance_metrics = Column(JSON)  # مقاييس الأداء
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime)
    
    # العلاقات
    tasks = relationship("AgentTask", back_populates="agent")

class AgentTask(Base):
    """نموذج مهام الوكلاء"""
    __tablename__ = 'agent_tasks'
    
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('ai_agents.id'), nullable=False)
    task_type = Column(String(50), nullable=False)
    parameters = Column(JSON)
    status = Column(String(20), default='pending')  # pending, in_progress, completed, failed
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    result = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # العلاقات
    agent = relationship("AIAgent", back_populates="tasks")

class ActivityLog(Base):
    """نموذج سجل النشاط"""
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String(50), nullable=False)  # ai, system, user, diagnosis, error
    level = Column(String(20), nullable=False)  # info, warning, error, success
    message = Column(Text, nullable=False)
    details = Column(JSON)
    source = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="activity_logs")

class AIModel(Base):
    """نموذج النماذج الذكية"""
    __tablename__ = 'ai_models'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    type = Column(String(50))  # CNN, ResNet, YOLO, etc.
    accuracy = Column(Float)
    status = Column(String(20), default='active')  # active, training, inactive
    file_path = Column(String(255))
    training_data_size = Column(Integer)
    training_date = Column(DateTime)
    configuration = Column(JSON)
    performance_metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSettings(Base):
    """نموذج إعدادات النظام"""
    __tablename__ = 'system_settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    category = Column(String(50))
    is_public = Column(Boolean, default=False)  # هل يمكن للمستخدمين العاديين رؤيتها
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Permission(Base):
    """نموذج الصلاحيات"""
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    module = Column(String(50))  # الوحدة التي تنتمي إليها الصلاحية
    action = Column(String(50))  # read, write, delete, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    user_permissions = relationship("UserPermission", back_populates="permission")

class UserPermission(Base):
    """نموذج صلاحيات المستخدمين"""
    __tablename__ = 'user_permissions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    granted_by = Column(Integer, ForeignKey('users.id'))
    granted_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    permission = relationship("Permission", back_populates="user_permissions")

# إعداد قاعدة البيانات
def create_database(database_url="sqlite:///gaara_scan_ai.db"):
    """إنشاء قاعدة البيانات والجداول"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """الحصول على جلسة قاعدة البيانات"""
    Session = sessionmaker(bind=engine)
    return Session()

def init_default_data(session):
    """إدراج البيانات الافتراضية"""
    
    # إنشاء مستخدم إداري افتراضي
    admin_user = User(
        username="admin",
        email="admin@gaara-ai.com",
        full_name="مدير النظام",
        is_admin=True
    )
    admin_user.set_password("admin123")
    session.add(admin_user)
    
    # إضافة محاصيل افتراضية
    crops = [
        Crop(name="الطماطم", scientific_name="Solanum lycopersicum", category="خضروات"),
        Crop(name="البطاطس", scientific_name="Solanum tuberosum", category="خضروات"),
        Crop(name="الذرة", scientific_name="Zea mays", category="حبوب"),
        Crop(name="القمح", scientific_name="Triticum aestivum", category="حبوب"),
    ]
    session.add_all(crops)
    session.commit()
    
    # إضافة أمراض افتراضية
    diseases = [
        Disease(
            name="اللفحة المبكرة",
            crop_id=1,  # الطماطم
            severity="medium",
            symptoms=["بقع بنية على الأوراق", "ذبول الأوراق السفلية"],
            treatment="استخدام مبيدات فطرية نحاسية",
            prevention="تحسين التهوية وتجنب الري المفرط"
        ),
        Disease(
            name="اللفحة المتأخرة",
            crop_id=2,  # البطاطس
            severity="high",
            symptoms=["بقع مائية على الأوراق", "عفن الدرنات"],
            treatment="مبيدات فطرية جهازية",
            prevention="زراعة أصناف مقاومة"
        ),
    ]
    session.add_all(diseases)
    
    # إضافة وكلاء ذكيين افتراضيين
    agents = [
        AIAgent(
            name="الوكيل الرئيسي",
            type="main_coordinator",
            capabilities=["task_coordination", "resource_management", "decision_making"],
            configuration={"max_concurrent_tasks": 10, "timeout_seconds": 30}
        ),
        AIAgent(
            name="وكيل التشخيص",
            type="specialist",
            capabilities=["disease_detection", "image_analysis", "treatment_recommendation"],
            configuration={"confidence_threshold": 0.85, "max_concurrent_tasks": 5}
        ),
    ]
    session.add_all(agents)
    
    # إضافة صلاحيات افتراضية
    permissions = [
        Permission(name="users.read", description="قراءة المستخدمين", module="users", action="read"),
        Permission(name="users.write", description="إدارة المستخدمين", module="users", action="write"),
        Permission(name="users.admin", description="إدارة كاملة للمستخدمين", module="users", action="admin"),
        Permission(name="diagnosis.read", description="قراءة التشخيصات", module="diagnosis", action="read"),
        Permission(name="diagnosis.write", description="إنشاء تشخيصات", module="diagnosis", action="write"),
        Permission(name="ai.read", description="قراءة معلومات الذكاء الاصطناعي", module="ai", action="read"),
        Permission(name="ai.admin", description="إدارة الذكاء الاصطناعي", module="ai", action="admin"),
    ]
    session.add_all(permissions)
    
    # إضافة إعدادات النظام الافتراضية
    settings = [
        SystemSettings(key="system.name", value="نظام Gaara Scan AI", description="اسم النظام"),
        SystemSettings(key="system.version", value="1.0.0", description="إصدار النظام"),
        SystemSettings(key="ai.confidence_threshold", value="0.85", description="حد الثقة للذكاء الاصطناعي"),
        SystemSettings(key="upload.max_file_size", value="10485760", description="الحد الأقصى لحجم الملف (بايت)"),
        SystemSettings(key="upload.allowed_extensions", value="jpg,jpeg,png,gif", description="امتدادات الملفات المسموحة"),
    ]
    session.add_all(settings)
    
    session.commit()
    print("تم إنشاء البيانات الافتراضية بنجاح")

if __name__ == "__main__":
    # إنشاء قاعدة البيانات
    engine = create_database()
    session = get_session(engine)
    
    # إدراج البيانات الافتراضية
    init_default_data(session)
    
    session.close()
    print("تم إنشاء قاعدة البيانات بنجاح")

