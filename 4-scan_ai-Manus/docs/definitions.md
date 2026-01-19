# تعريفات النظام (Definitions)

**تاريخ التوثيق:** 2025-11-15

هذا الملف سيحتوي على جميع تعريفات الكلاسات والدوال والثوابت الهامة في المشروع.


## الواجهة الخلفية (Backend)

### الكلاسات (Classes)

```python
class ReportType(Enum):
class AnalysisType(Enum):
class ChartType(Enum):
class TimeFrame(Enum):
class AnalyticsQuery:
class ChartConfiguration:
class ReportConfiguration:
class AnalyticsResult:
class BaseAnalyzer(ABC):
class ProductionAnalyzer(BaseAnalyzer):
class WeatherAnalyzer(BaseAnalyzer):
class PredictiveAnalyzer(BaseAnalyzer):
class ChartGenerator:
class ReportGenerator:
class ExportFormat(Enum):
class ReportConfig:
class AdvancedReportingSystem:
class SecurityLevel(Enum):
class ThreatType(Enum):
class AlertSeverity(Enum):
class MonitoringType(Enum):
class SecurityEvent:
class UserSession:
class AccessAttempt:
class SystemMetrics:
class EncryptionManager:
class JWTManager:
class ThreatDetector:
class SystemMonitor:
class AuditLogger:
class SecurityManager:
class AgentType(Enum):
class MessageType(Enum):
class AgentStatus(Enum):
class Message:
class AgentCapability:
class BaseAgent(ABC):
class CentralAgent(BaseAgent):
class DiagnosticAgent(BaseAgent):
class TreatmentAgent(BaseAgent):
class ErrorTrackingAgent(BaseAgent):
class UserAssistantAgent(BaseAgent):
class MessageRouter:
class LoadBalancer:
class AIAgentsSystem:
class ImagePreprocessor:
class DeepLearningModel:
class TraditionalMLModel:
class AIPlantDiagnosisEngine:
class DiagnosisResult:
class PlantInfo:
class AIEngineAdvanced:
class DiagnosisConfidence(Enum):
class DiseaseCategory(Enum):
class PlantDiseaseInfo:
class BackupManager:
class Config:
class DevelopmentConfig(Config):
class ProductionConfig(Config):
class TestingConfig(Config):
class OrderStatus(Enum):
class PaymentStatus(Enum):
class ProductCategory(Enum):
class Product:
class Order:
class EcommerceSystem:
class EquipmentStatus(enum.Enum):
class MaintenanceType(enum.Enum):
class Equipment(db.Model):
class EquipmentCategory(db.Model):
class MaintenanceRecord(db.Model):
class EquipmentUsageLog(db.Model):
class EquipmentService:
class FarmType(Enum):
class SoilType(Enum):
class IrrigationType(Enum):
class Location:
class SoilData:
class WeatherData:
class Crop:
class Equipment:
class Worker:
class Farm:
class FarmManagementSystem:
class EmployeeStatus(Enum):
class EmployeeType(Enum):
class LeaveType(Enum):
class AttendanceStatus(Enum):
class PayrollStatus(Enum):
class Employee:
class LeaveRequest:
class AttendanceRecord:
class PayrollRecord:
class PerformanceReview:
class HRManagementSystem:
class InventoryItem(db.Model):
class InventoryCategory(db.Model):
class InventoryLocation(db.Model):
class InventoryMovement(db.Model):
class InventoryTransaction(db.Model):
class Supplier(db.Model):
class Warehouse(db.Model):
class InventoryService:
class SensorType(Enum):
class SensorStatus(Enum):
class ConnectionType(Enum):
class AlertLevel(Enum):
class SensorReading:
class SensorConfiguration:
class Alert:
class BaseSensor(ABC):
class TemperatureHumiditySensor(BaseSensor):
class SoilMoistureSensor(BaseSensor):
class WeatherStation(BaseSensor):
class AlertManager:
class DataLogger:
class IoTSystem:
class IoTSensorsSystem:
class User(db.Model):
class Plant(db.Model):
class Disease(db.Model):
class Diagnosis(db.Model):
class Sensor(db.Model):
class Company(db.Model):
class Permission(db.Model):
class ApiKey(db.Model):
class PermissionManager:
class Permissions:
class Roles:
class PermissionType(Enum):
class Module(Enum):
class DefaultRole(Enum):
class PredictionType(Enum):
class PredictionResult:
class AnalysisResult:
class WeatherPredictor:
class YieldPredictor:
class DiseasePredictor:
class MarketPricePredictor:
class PredictiveAnalyticsSystem:
class SecureConfigManager:
class SecureEnvironmentConfig:
class SecureDatabaseOperations:
class SecurityManager:
class InputValidator:
class SecurityConfig:
class SecurityMiddleware:
class DatabaseConfig:
class BaseModel:
class AdvancedReportsSystem:
class UserRole(Enum):
class AdvancedSecuritySystem:
class InsightType(Enum):
class InsightPriority(Enum):
class ConfidenceLevel(Enum):
class DataPattern:
class Insight:
class PredictionModel:
class AIAnalysisEngine:
class TimeRange(Enum):
class DataPoint:
class ChartData:
class AnalyticsEngine:
class DashboardManager:
class HealthResponse(BaseModel):
class LoginRequest(BaseModel):
class LoginResponse(BaseModel):
class UserInfo(BaseModel):
class ActivityLog(Base):
class ModuleInfo(BaseModel):
class SystemStats(BaseModel):
class BackupType(Enum):
class BackupStatus(Enum):
class CompressionType(Enum):
class BackupConfig:
class BackupRecord:
class CachingMixin:
class CodeCleaner:
class CodeInspector:
class ComplianceStandard(Enum):
class ComplianceLevel(Enum):
class ComplianceRequirement:
class AuditLog:
class ComplianceManager:
class WidgetType(Enum):
class LayoutType(Enum):
class PermissionLevel(Enum):
class WidgetConfig:
class DashboardLayout:
class DashboardTheme:
class DataSourceManager:
class WidgetRenderer:
class EncryptionAlgorithm(Enum):
class KeyType(Enum):
class EncryptionKey:
class EncryptedData:
class EndToEndEncryption:
class ErrorHandler:
class FinalSystemValidator:
class FrontendTester:
class InterfaceIntegrationFixer:
class LibraryCompatibilityChecker:
class MemoryService:
class LanguageDirection(Enum):
class TranslationStatus(Enum):
class ContentType(Enum):
class Language:
class TranslationKey:
class Translation:
class LocalizationContext:
class LanguageDetector:
class TranslationEngine:
class MultilingualManager:
class NotificationType(Enum):
class NotificationPriority(Enum):
class NotificationStatus(Enum):
class NotificationTemplate:
class NotificationRecipient:
class Notification:
class EmailProvider:
class SMSProvider:
class PushNotificationProvider:
class WebSocketNotificationProvider:
class Event:
class Observer(ABC):
class Subject(ABC):
class LoggingObserver(Observer):
class SystemMetrics:
class UserActivity:
class AIAgentUsage:
class AlertRule:
class PerformanceMonitor:
class PrintExportSystem:
class SerializationMixin:
class SingletonMeta(type):
class Singleton(metaclass=SingletonMeta):
class ConfigManager(Singleton):
class SmartCache:
class ReportType(Enum):
class ReportFormat(Enum):
class ReportFrequency(Enum):
class ReportFilter:
class ReportSection:
class ReportTemplate:
class ReportInstance:
class ReportGenerator:
class ComponentType(Enum):
class IntegrationStatus(Enum):
class ComponentHealth(Enum):
class SystemComponent:
class IntegrationIssue:
class RoutingRule:
class ComponentScanner:
class HealthChecker:
class IntegrationManager:
class Status(Enum):
class Priority(Enum):
class Repository(Generic[T]):
```

### الدوال (Functions)

```python
def get_available_reports():
def generate_report():
def export_report():
def get_report_templates():
def add_sample_data():
def authenticate(username, password, ip_address, user_agent):
def validate_token(token):
def logout(session_id):
def check_input_security(input_data, ip_address):
def get_security_status():
def encrypt_data(data):
def decrypt_data(encrypted_data):
def require_auth(f):
def require_permission(permission):
def get_agents_status():
def create_sample_data():
def home():
def health_check():
def api_status():
def main():
def init_database(app):
def create_tables(app):
def seed_database(app):
def backup_database(app, backup_path=None):
def restore_database(app, backup_path):
def get_database_info(app):
def reset_database(app):
def optimize_database(app):
def add_product():
def get_products():
def add_to_cart():
def create_order():
def process_payment(order_id):
def track_order(order_id):
def add_review(product_id):
def farmer_dashboard():
def init_sample_data():
def get_equipment():
def create_equipment():
def schedule_maintenance():
def log_equipment_usage():
def get_maintenance_due():
def get_equipment_statistics():
def register_equipment_routes(app):
def get_inventory_items():
def create_inventory_item():
def update_item_stock():
def get_low_stock_alerts():
def get_expired_items():
def get_inventory_valuation():
def get_inventory_movements():
def register_inventory_routes(app):
def add_sensor_config(config):
def get_iot_status():
def get_sensor_data(sensor_id):
def get_active_alerts():
def setup_default_sensors():
def create_app():
def make_celery(app):
def admin_required(f):
def handle_errors(f):
def allowed_file(filename):
def index():
def register():
def login():
def get_profile():
def get_farms():
def create_farm():
def get_farm(farm_id):
def get_plants():
def create_plant():
def get_diseases():
def create_diagnosis():
def get_diagnosis(diagnosis_id):
def get_user_diagnoses():
def create_sensor():
def add_sensor_reading(sensor_id):
def get_dashboard_stats():
def uploaded_file(filename):
def analyze_plant_image(diagnosis_id, image_path):
def not_found(error):
def internal_error(error):
def forbidden(error):
def unauthorized(error):
def setup_secure_logging():
def create_secure_app():
def make_secure_celery(app):
def validate_input(data, required_fields, max_lengths=None):
def sanitize_filename(filename):
def safe_query(query_string, params=None):
def get_user_safe(user_id):
def log_activity(activity_type):
def security_health():
def create_tables_secure():
def not_found_secure(error):
def internal_error_secure(error):
def forbidden_secure(error):
def unauthorized_secure(error):
def ratelimit_handler(e):
def init_db(app):
def create_default_permissions():
def create_default_admin():
def get_current_user():
def require_any_permission(*permission_names):
def require_all_permissions(*permission_names):
def require_role(role_name):
def require_admin():
def require_owner_or_permission(permission_name, owner_field=\'user_id\'):
def log_permission_check(permission_name, success=True):
def get_user_permissions_list(user_id):
def check_module_access(user_id, module_name):
def get_accessible_modules(user_id):
def require_ownership_or_admin(resource_model, resource_id_param=\'id\', owner_field=\'owner_id\'):
def get_user_permissions(user_id):
def has_permission(user_id, permission_name):
def assign_role_to_user(user_id, role_name):
def remove_role_from_user(user_id, role_name):
def get_user_roles(user_id):
def init_permissions():
def permission_required(permission_name):
def update_profile():
def get_users():
def create_user():
def get_user(user_id):
def update_user(user_id):
def delete_user(user_id):
def get_companies():
def create_company():
def update_farm(farm_id):
def delete_farm(farm_id):
def get_plant(plant_id):
def get_disease(disease_id):
def get_diagnoses():
def system_health():
def system_info():
def register_routes(app):
def get_farms_report():
def get_config(key, default=None):
def is_production():
def is_development():
def get_database_url():
def get_secret_key():
def get_jwt_secret_key():
def get_secure_db_operations():
def validate_sql_input(input_value):
def sanitize_sql_string(input_string):
def secure_file_upload(file, upload_type=\'images\'):
def rate_limit_decorator(max_attempts=5, window_minutes=15):
def validate_email_change(new_email, user_id):
def verify_email_token(user_id, token):
def hash_password(password):
def verify_password(password, hashed_password):
def validate_password_strength(password):
def sanitize_input(data):
def log_security_event(event_type, details, user_id=None, ip_address=None):
def rate_limit(limit):
def init_security(app):
def validate_request_data(required_fields, data=None):
def validate_email(email):
def validate_phone(phone):
def validate_coordinates(latitude, longitude):
def handle_file_upload(file, upload_type=\'general\', max_size=None):
def get_file_info(file_path):
def generate_api_key():
def hash_api_key(api_key):
def verify_api_key(api_key, key_hash):
def generate_secure_token(length=32):
def check_permission(user, permission_name):
def paginate_query(query, page=1, per_page=20, max_per_page=100):
def format_response(data=None, message=None, status=\'success\', status_code=200):
def format_error_response(error_message, status_code=400, error_code=None):
def format_validation_error(errors):
def parse_date(date_string, format=\'%Y-%m-%d\'):
def parse_datetime(datetime_string, format=\'%Y-%m-%d %H:%M:%S\'):
def format_date(date_obj, format=\'%Y-%m-%d\'):
def format_datetime(datetime_obj, format=\'%Y-%m-%d %H:%M:%S\'):
def get_time_ago(datetime_obj):
def safe_json_loads(json_string, default=None):
def safe_json_dumps(data, default=None):
def clean_dict(data, remove_none=True, remove_empty=False):
def sanitize_text(text, max_length=None):
def generate_slug(text, max_length=50):
def calculate_percentage(part, total):
def calculate_growth_rate(old_value, new_value):
def get_trend_direction(values):
def validate_image_file(file):
def validate_coordinates_bounds(latitude, longitude, bounds=None):
def generate_cache_key(*args):
def cache_response(cache, key, data, timeout=300):
def get_cached_response(cache, key):
def log_user_action(user_id, action, details=None):
def log_api_request(endpoint, method, user_id=None, ip_address=None):
def export_to_csv(data, filename, headers=None):
def export_to_excel(data, filename, sheet_name=\'Sheet1\'):
def send_notification(user_id, title, message, notification_type=\'info\'):
def send_email_notification(email, subject, body, html_body=None):
def get_client_ip():
def get_user_agent():
def is_mobile_request():
def register_error_handlers(app):
def get_db():
def verify_token(credentials):
def create_access_token(data, expires_delta):
def create_default_data(db):
def log_compliance_event(user_id, action, resource, details, ip_address, risk_level):
def get_compliance_status():
def encrypt_sensitive_data(data, purpose):
def decrypt_sensitive_data(encrypted_data):
def handle_http_exception(request, exc):
def handle_general_exception(request, exc):
def create_404_error(message):
def create_500_error(message):
def create_503_error(message):
def t(key, language_code, namespace, **kwargs):
def set_language(language_code):
def get_current_language():
def format_number(number, language_code):
def format_currency(amount, language_code, currency_code):
def format_date(date, language_code, format_type):
def send_email_notification(recipient_email, subject, body, user_id, priority):
def send_sms_notification(recipient_phone, message, user_id, priority):
def start_monitoring():
def stop_monitoring():
def get_monitor():
def cache_result(ttl, namespace):
def get_cache_stats():
def clear_all_cache():
def initialize_integration_manager(base_path):
def index():
def list_models():
def view_model(model_name):
def validate_model_data(model_name):
def list_tables():
def view_table(table_name):
def validate_table_data(table_name):
def api_list_models():
def api_get_model(model_name):
def api_validate_model_data(model_name):
def api_list_tables():
def api_get_table(table_name):
def api_validate_table_data(table_name):
def api_validate_all_tables():
def register_blueprint(app):
def upload_image():
def process_image():
def analyze_image():
def download_image(filename):
def visualize_image():
def get_keyword_service(db):
def get_search_engine_service(db):
def get_source_service(db):
def get_notifications():
def get_notification(notification_id):
def create_notification():
def mark_as_read(notification_id):
def mark_as_unread(notification_id):
def archive_notification(notification_id):
def unarchive_notification(notification_id):
def delete_notification(notification_id):
def bulk_action():
def get_templates():
def get_template(template_id):
def create_template():
def update_template(template_id):
def delete_template(template_id):
def get_preferences():
def update_preference():
def create_scheduled_notification():
def process_scheduled_notifications():
def get_webhook_subscriptions():
def create_webhook_subscription():
def update_webhook_subscription(subscription_id):
def delete_webhook_subscription(subscription_id):
def send_test_notification():
```


## الواجهة الأمامية (Frontend)

### المكونات (Components)

```jsx
const AuthContext = createContext();
const AuthProvider = ({ children }) => {};
const AppContext = createContext();
const AppProvider = ({ children }) => {};
const ProtectedRoute = ({ children }) => {};
const Layout = ({ children }) => {};
const App = () => {};
const AdvancedAnalytics = () => {};
const Footer = () => {};
const Navbar = () => {};
const Sidebar = () => {};
const AppRouter = () => {};
const ErrorFallback = ({ error, resetErrorBoundary }) => {};
const LoadingSpinner = ({ size = 'medium', text = null, fullScreen = false }) => {};
const CarouselContext = React.createContext(null);
const ChartContext = React.createContext(null);
const ChartStyle = ({ ... });
const ChartTooltip = RechartsPrimitive.Tooltip;
const ChartLegend = RechartsPrimitive.Legend;
const Form = FormProvider;
const FormFieldContext = React.createContext({});
const FormField = ({ ... });
const FormItemContext = React.createContext({});
const Toaster = ({ ... });
const ToggleGroupContext = React.createContext({});
const DataContext = createContext();
const Analytics = () => {};
const Breeding = () => {};
const Companies = () => {};
const Crops = () => {};
const Diagnosis = () => {};
const Diseases = () => {};
const Equipment = () => {};
const Farms = () => {};
const Inventory = () => {};
const Login = () => {};
const Profile = () => {};
const Reports = () => {};
const Sensors = () => {};
const SetupWizard = () => {};
const Users = () => {};
const Dashboard = () => {};
const DashboardComplete = () => {};
const EnhancedDashboard = () => {};
```

### الثوابت (Constants)

```js
const SIDEBAR_COOKIE_NAME = "sidebar_state";
const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 7;
const SIDEBAR_WIDTH = "16rem";
const SIDEBAR_WIDTH_MOBILE = "18rem";
const SIDEBAR_WIDTH_ICON = "3rem";
const SIDEBAR_KEYBOARD_SHORTCUT = "b";
const THEMES = { ... };
```
