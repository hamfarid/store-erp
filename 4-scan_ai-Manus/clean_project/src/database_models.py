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



# ===== الجداول الجديدة للتقنيات المتقدمة =====

class AIMemory(Base):
    """نموذج ذاكرة الذكاء الاصطناعي"""
    __tablename__ = 'ai_memory'
    
    id = Column(Integer, primary_key=True)
    memory_type = Column(String(50), nullable=False)  # short_term, long_term, episodic, semantic
    content = Column(JSON, nullable=False)
    context = Column(JSON)
    importance_score = Column(Float, default=0.5)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # العلاقات
    memory_associations = relationship("MemoryAssociation", back_populates="memory")

class MemoryAssociation(Base):
    """نموذج الروابط بين الذكريات"""
    __tablename__ = 'memory_associations'
    
    id = Column(Integer, primary_key=True)
    memory_id = Column(Integer, ForeignKey('ai_memory.id'), nullable=False)
    associated_memory_id = Column(Integer, ForeignKey('ai_memory.id'), nullable=False)
    association_type = Column(String(50))  # causal, temporal, semantic, similarity
    strength = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    memory = relationship("AIMemory", foreign_keys=[memory_id], back_populates="memory_associations")
    associated_memory = relationship("AIMemory", foreign_keys=[associated_memory_id])

class GenerativeModel(Base):
    """نموذج النماذج التوليدية"""
    __tablename__ = 'generative_models'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False)  # llm, diffusion, vae, gan
    version = Column(String(20))
    provider = Column(String(50))  # openai, huggingface, local
    model_path = Column(String(255))
    config = Column(JSON)
    performance_metrics = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    
    # العلاقات
    generations = relationship("GeneratedContent", back_populates="model")

class GeneratedContent(Base):
    """نموذج المحتوى المولد"""
    __tablename__ = 'generated_content'
    
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('generative_models.id'), nullable=False)
    content_type = Column(String(50), nullable=False)  # text, image, audio, video
    prompt = Column(Text, nullable=False)
    generated_content = Column(Text)
    file_path = Column(String(255))
    metadata = Column(JSON)
    quality_score = Column(Float)
    user_rating = Column(Integer)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    model = relationship("GenerativeModel", back_populates="generations")

class VisionModel(Base):
    """نموذج نماذج الرؤية المتقدمة"""
    __tablename__ = 'vision_models'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False)  # vit, cnn, transformer, hybrid
    architecture = Column(String(100))
    input_resolution = Column(String(20))
    supported_formats = Column(JSON)  # قائمة الصيغ المدعومة
    accuracy_metrics = Column(JSON)
    model_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    vision_analyses = relationship("VisionAnalysis", back_populates="model")

class VisionAnalysis(Base):
    """نموذج تحليلات الرؤية"""
    __tablename__ = 'vision_analyses'
    
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('vision_models.id'), nullable=False)
    image_path = Column(String(255), nullable=False)
    analysis_type = Column(String(50))  # classification, detection, segmentation, hyperspectral
    results = Column(JSON, nullable=False)
    confidence_scores = Column(JSON)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    model = relationship("VisionModel", back_populates="vision_analyses")

class CollaborativeProject(Base):
    """نموذج المشاريع التعاونية"""
    __tablename__ = 'collaborative_projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    project_type = Column(String(50))  # research, model_training, data_collection
    status = Column(String(20), default='active')  # active, completed, paused
    privacy_level = Column(String(20), default='public')  # public, private, restricted
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    creator = relationship("User")
    participants = relationship("ProjectParticipant", back_populates="project")
    shared_models = relationship("SharedModel", back_populates="project")

class ProjectParticipant(Base):
    """نموذج المشاركين في المشاريع"""
    __tablename__ = 'project_participants'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('collaborative_projects.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String(50), default='contributor')  # owner, admin, contributor, viewer
    contribution_score = Column(Float, default=0.0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    project = relationship("CollaborativeProject", back_populates="participants")
    user = relationship("User")

class SharedModel(Base):
    """نموذج النماذج المشتركة"""
    __tablename__ = 'shared_models'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('collaborative_projects.id'), nullable=False)
    model_name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False)
    version = Column(String(20))
    model_data = Column(JSON)  # معاملات النموذج أو مسار الملف
    performance_metrics = Column(JSON)
    shared_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    download_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    project = relationship("CollaborativeProject", back_populates="shared_models")
    shared_by_user = relationship("User")

class PredictiveAlert(Base):
    """نموذج التنبيهات الاستباقية"""
    __tablename__ = 'predictive_alerts'
    
    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50), nullable=False)  # disease_risk, weather_warning, treatment_reminder
    severity = Column(String(20))  # low, medium, high, critical
    crop_id = Column(Integer, ForeignKey('crops.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    prediction_data = Column(JSON, nullable=False)
    confidence = Column(Float)
    status = Column(String(20), default='active')  # active, acknowledged, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # العلاقات
    crop = relationship("Crop")
    user = relationship("User")

class TreatmentPlan(Base):
    """نموذج خطط العلاج الذكية"""
    __tablename__ = 'treatment_plans'
    
    id = Column(Integer, primary_key=True)
    diagnosis_id = Column(Integer, ForeignKey('diagnoses.id'), nullable=False)
    plan_type = Column(String(50))  # preventive, curative, maintenance
    treatments = Column(JSON, nullable=False)  # قائمة العلاجات المقترحة
    schedule = Column(JSON)  # جدولة العلاجات
    estimated_cost = Column(Float)
    estimated_duration = Column(Integer)  # بالأيام
    success_probability = Column(Float)
    status = Column(String(20), default='pending')  # pending, active, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    diagnosis = relationship("Diagnosis")
    progress_logs = relationship("TreatmentProgress", back_populates="treatment_plan")

class TreatmentProgress(Base):
    """نموذج تقدم العلاج"""
    __tablename__ = 'treatment_progress'
    
    id = Column(Integer, primary_key=True)
    treatment_plan_id = Column(Integer, ForeignKey('treatment_plans.id'), nullable=False)
    progress_date = Column(DateTime, default=datetime.utcnow)
    progress_notes = Column(Text)
    effectiveness_score = Column(Float)  # 0-1
    side_effects = Column(JSON)
    images = Column(JSON)  # مسارات الصور
    next_action = Column(String(100))
    recorded_by = Column(Integer, ForeignKey('users.id'))
    
    # العلاقات
    treatment_plan = relationship("TreatmentPlan", back_populates="progress_logs")
    recorder = relationship("User")

class DistributedNode(Base):
    """نموذج العقد الموزعة"""
    __tablename__ = 'distributed_nodes'
    
    id = Column(Integer, primary_key=True)
    node_id = Column(String(100), unique=True, nullable=False)
    node_name = Column(String(100))
    node_type = Column(String(50))  # farm, research_center, cloud, edge
    location = Column(JSON)  # معلومات الموقع الجغرافي
    capabilities = Column(JSON)  # قدرات العقدة
    status = Column(String(20), default='active')  # active, inactive, maintenance
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    performance_metrics = Column(JSON)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    owner = relationship("User")
    federated_sessions = relationship("FederatedLearningSession", back_populates="node")

class FederatedLearningSession(Base):
    """نموذج جلسات التعلم الفيدرالي"""
    __tablename__ = 'federated_learning_sessions'
    
    id = Column(Integer, primary_key=True)
    session_name = Column(String(100), nullable=False)
    model_type = Column(String(50), nullable=False)
    coordinator_node_id = Column(Integer, ForeignKey('distributed_nodes.id'), nullable=False)
    participant_nodes = Column(JSON)  # قائمة العقد المشاركة
    global_model_version = Column(Integer, default=1)
    current_round = Column(Integer, default=1)
    max_rounds = Column(Integer, default=10)
    status = Column(String(20), default='preparing')  # preparing, training, completed, failed
    aggregation_method = Column(String(50), default='fedavg')
    privacy_budget = Column(Float)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    node = relationship("DistributedNode", back_populates="federated_sessions")
    model_updates = relationship("ModelUpdate", back_populates="session")

class ModelUpdate(Base):
    """نموذج تحديثات النماذج"""
    __tablename__ = 'model_updates'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('federated_learning_sessions.id'), nullable=False)
    node_id = Column(Integer, ForeignKey('distributed_nodes.id'), nullable=False)
    round_number = Column(Integer, nullable=False)
    model_weights = Column(JSON)  # أوزان النموذج أو مسار الملف
    training_metrics = Column(JSON)
    data_size = Column(Integer)  # حجم البيانات المستخدمة
    training_time = Column(Float)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    session = relationship("FederatedLearningSession", back_populates="model_updates")
    node = relationship("DistributedNode")

class SystemMetrics(Base):
    """نموذج مقاييس النظام"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    metric_type = Column(String(50), nullable=False)  # performance, usage, error, resource
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    unit = Column(String(20))
    context = Column(JSON)  # معلومات إضافية
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
class APIUsage(Base):
    """نموذج استخدام واجهات برمجة التطبيقات"""
    __tablename__ = 'api_usage'
    
    id = Column(Integer, primary_key=True)
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    response_time = Column(Float)
    status_code = Column(Integer)
    request_size = Column(Integer)
    response_size = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    user = relationship("User")

# ===== إعداد قاعدة البيانات =====

def create_database_engine(database_url: str):
    """إنشاء محرك قاعدة البيانات"""
    engine = create_engine(database_url, echo=False)
    return engine

def create_all_tables(engine):
    """إنشاء جميع الجداول"""
    Base.metadata.create_all(engine)

def get_session_maker(engine):
    """إنشاء صانع الجلسات"""
    return sessionmaker(bind=engine)

def init_database(database_url: str = "sqlite:///gaara_scan_ai.db"):
    """تهيئة قاعدة البيانات"""
    engine = create_database_engine(database_url)
    create_all_tables(engine)
    SessionMaker = get_session_maker(engine)
    return engine, SessionMaker

# ===== دوال مساعدة =====

def get_or_create(session, model, **kwargs):
    """الحصول على كائن أو إنشاؤه إذا لم يكن موجوداً"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance, True

def bulk_insert_or_update(session, model, data_list):
    """إدراج أو تحديث مجموعة من البيانات"""
    for data in data_list:
        instance = session.query(model).filter_by(id=data.get('id')).first()
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
        else:
            instance = model(**data)
            session.add(instance)
    session.commit()

def cleanup_old_records(session, model, days_old: int = 30):
    """تنظيف السجلات القديمة"""
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    
    if hasattr(model, 'created_at'):
        old_records = session.query(model).filter(model.created_at < cutoff_date).all()
        for record in old_records:
            session.delete(record)
        session.commit()
        return len(old_records)
    return 0

