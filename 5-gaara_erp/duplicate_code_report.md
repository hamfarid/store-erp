# 🔍 تقرير الكود المكرر - Duplicate Code Report
============================================================

## 📁 الملفات المتطابقة تماماً

### المجموعة 1:
- ./backend/src/__init__.py
- ./repeat_code/backend/src/routes/__init__.py

### المجموعة 2:
- ./backend/src/decorators/__init__.py
- ./repeat_code/backend/src/middleware/__init__.py

## 🔧 الدوال المكررة

### الدالة المكررة 1:
**التوقيع:** __init___self.base_path = Path(base_path) | self.backend_path = self.base_path / "backend" | self.frontend_path = self.base_path / "frontend"
**المواقع:**
- ./comprehensive_system_audit.py (السطر 16)
- ./ultra_deep_system_audit.py (السطر 18)

### الدالة المكررة 2:
**التوقيع:** get_grade_"""تحديد التقدير""" | if score >= 95: return "ممتاز+"
**المواقع:**
- ./comprehensive_system_audit.py (السطر 391)
- ./ultra_deep_system_audit.py (السطر 671)

### الدالة المكررة 3:
**التوقيع:** save_results_"""حفظ النتائج""" | with open(filename, 'w', encoding='utf-8') as f: | print(f"💾 تم حفظ النتائج في: {filename}")
**المواقع:**
- ./comprehensive_system_audit.py (السطر 423)
- ./ultra_deep_system_audit.py (السطر 702)

### الدالة المكررة 4:
**التوقيع:** print_step_print(f"📋 {message}")
**المواقع:**
- ./change_ports_comprehensive.py (السطر 17)
- ./find_duplicate_code.py (السطر 22)
- ./comprehensive_system_test.py (السطر 20)

### الدالة المكررة 5:
**التوقيع:** print_success_print(f"✅ {message}")
**المواقع:**
- ./change_ports_comprehensive.py (السطر 20)
- ./find_duplicate_code.py (السطر 25)
- ./comprehensive_system_test.py (السطر 23)

### الدالة المكررة 6:
**التوقيع:** print_warning_print(f"⚠️  {message}")
**المواقع:**
- ./change_ports_comprehensive.py (السطر 23)
- ./find_duplicate_code.py (السطر 28)
- ./comprehensive_system_test.py (السطر 26)

### الدالة المكررة 7:
**التوقيع:** print_error_print(f"❌ {message}")
**المواقع:**
- ./find_duplicate_code.py (السطر 31)
- ./comprehensive_system_test.py (السطر 29)

### الدالة المكررة 8:
**التوقيع:** _convert_flask_rule_to_openapi_"""Convert Flask style route patterns to OpenAPI path template. | return re.sub(r"<(?:[^:<>]+:)?([^<>]+)>", r"{\1}", path_rule)
**المواقع:**
- ./backend/app.py (السطر 48)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 43)

### الدالة المكررة 9:
**التوقيع:** _extract_path_parameters_"""Return list of parameter objects for {param} placeholders.""" | params = [] | for name in re.findall(r"{([^/{}]+)}", openapi_path):
**المواقع:**
- ./backend/app.py (السطر 59)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 54)

### الدالة المكررة 10:
**التوقيع:** _infer_tags_"""Infer basic tags from path segments: /api/<tag>/... -> <Tag>.""" | parts = [p for p in openapi_path.split('/') if p] | if len(parts) >= 2:
**المواقع:**
- ./backend/app.py (السطر 73)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 68)

### الدالة المكررة 11:
**التوقيع:** generate_openapi_spec_"""Dynamically build a minimal OpenAPI 3.0 specification from registered routes. | paths: dict = {} | try:  # Resilient import; if module path not available continue with empty registry
**المواقع:**
- ./backend/app.py (السطر 87)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 82)

### الدالة المكررة 12:
**التوقيع:** create_app_"""Create and configure Flask application""" | app = Flask(__name__, template_folder=str(src_dir / 'templates')) | app.config['SECRET_KEY'] = os.environ.get(
**المواقع:**
- ./backend/app.py (السطر 199)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 194)

### الدالة المكررة 13:
**التوقيع:** register_blueprints_"""Register all available blueprints""" | blueprints_to_register = [ | registered_count = 0
**المواقع:**
- ./backend/app.py (السطر 250)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 241)

### الدالة المكررة 14:
**التوقيع:** register_error_handlers_"""Register error handlers""" | def not_found(_error): | def internal_error(_error):
**المواقع:**
- ./backend/app.py (السطر 281)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 270)

### الدالة المكررة 15:
**التوقيع:** register_basic_routes_"""Register basic application routes (kept thin).""" | _register_index(app) | _register_health(app)
**المواقع:**
- ./backend/app.py (السطر 340)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 329)

### الدالة المكررة 16:
**التوقيع:** _register_index_def index():  # noqa: D401
**المواقع:**
- ./backend/app.py (السطر 347)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 336)

### الدالة المكررة 17:
**التوقيع:** _register_health_try: | decorator_health = api_meta(summary='Health Check', | decorator_info = api_meta(summary='System information',
**المواقع:**
- ./backend/app.py (السطر 361)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 350)

### الدالة المكررة 18:
**التوقيع:** _register_docs_def openapi_spec(): | def swagger_docs(): | def redoc_docs():
**المواقع:**
- ./backend/app.py (السطر 424)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 413)

### الدالة المكررة 19:
**التوقيع:** not_found_try:
**المواقع:**
- ./backend/app.py (السطر 285)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 274)

### الدالة المكررة 20:
**التوقيع:** internal_error_try:
**المواقع:**
- ./backend/app.py (السطر 304)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 293)

### الدالة المكررة 21:
**التوقيع:** forbidden_try:
**المواقع:**
- ./backend/app.py (السطر 322)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 311)

### الدالة المكررة 22:
**التوقيع:** index_return render_template_string(
**المواقع:**
- ./backend/app.py (السطر 349)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 338)

### الدالة المكررة 23:
**التوقيع:** health_check_return jsonify({
**المواقع:**
- ./backend/app.py (السطر 402)
- ./backend/src/https_server.py (السطر 292)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 391)

### الدالة المكررة 24:
**التوقيع:** system_info_return jsonify({
**المواقع:**
- ./backend/app.py (السطر 413)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 402)

### الدالة المكررة 25:
**التوقيع:** openapi_spec_return jsonify(generate_openapi_spec(app))
**المواقع:**
- ./backend/app.py (السطر 426)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 415)

### الدالة المكررة 26:
**التوقيع:** swagger_docs_return ("""<!DOCTYPE html><html><head><title>Swagger UI - Inventory API</title>
**المواقع:**
- ./backend/app.py (السطر 430)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 419)

### الدالة المكررة 27:
**التوقيع:** redoc_docs_return ("""<!DOCTYPE html><html><head><title>ReDoc - Inventory API</title>
**المواقع:**
- ./backend/app.py (السطر 440)
- ./backend/database_archive/quick_fix_backup_20251004_094710/app.py (السطر 429)

### الدالة المكررة 28:
**التوقيع:** create_admin_"""Create admin user""" | with app.app_context():
**المواقع:**
- ./backend/create_admin_direct.py (السطر 78)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_direct.py (السطر 78)

### الدالة المكررة 29:
**التوقيع:** set_password_"""Set password using SHA-256 (same as the fallback in auth.py)""" | self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
**المواقع:**
- ./backend/create_admin_direct.py (السطر 69)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_direct.py (السطر 69)

### الدالة المكررة 30:
**التوقيع:** check_password_"""Check password using SHA-256""" | return hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password_hash
**المواقع:**
- ./backend/create_admin_direct.py (السطر 73)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_direct.py (السطر 73)

### الدالة المكررة 31:
**التوقيع:** create_admin_user_"""Create a default admin user""" | with app.app_context():
**المواقع:**
- ./backend/create_admin_user.py (السطر 19)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_user.py (السطر 19)

### الدالة المكررة 32:
**التوقيع:** test_login_"""Test the login functionality""" | with app.app_context():
**المواقع:**
- ./backend/create_admin_user.py (السطر 72)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_user.py (السطر 72)

### الدالة المكررة 33:
**التوقيع:** main_"""Main function""" | print("=" * 60) | print("Creating Admin User for Inventory System")
**المواقع:**
- ./backend/create_admin_user.py (السطر 98)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_user.py (السطر 98)

### الدالة المكررة 34:
**التوقيع:** create_database_backup_"""إنشاء نسخة احتياطية من قاعدة البيانات""" | try:
**المواقع:**
- ./backend/database_migration_script.py (السطر 33)
- ./backend/src/routes/admin_panel.py (السطر 469)

### الدالة المكررة 35:
**التوقيع:** __init___self.base_path = Path(".") | self.src_path = self.base_path / "src" | self.fixes_applied = []
**المواقع:**
- ./backend/comprehensive_fix_phase3.py (السطر 15)
- ./backend/final_fix_phase4.py (السطر 15)
- ./backend/quick_fix_original_endpoints.py (السطر 12)

### الدالة المكررة 36:
**التوقيع:** login_"""تسجيل الدخول""" | try:
**المواقع:**
- ./backend/start_server.py (السطر 38)
- ./backend/src/routes/security_system.py (السطر 104)
- ./backend/src/routes/user.py (السطر 161)

### الدالة المكررة 37:
**التوقيع:** wrapper_return func(*args, **kwargs)
**المواقع:**
- ./backend/src/api_meta.py (السطر 57)
- ./backend/src/services/api_documentation.py (السطر 37)

### الدالة المكررة 38:
**التوقيع:** decorator_def decorated_function(*args, **kwargs): | return decorated_function
**المواقع:**
- ./backend/src/auth.py (السطر 342)
- ./backend/src/auth.py (السطر 474)
- ./backend/src/secure_communication.py (السطر 350)
- ./backend/src/decorators/permission_decorators.py (السطر 80)
- ./backend/src/decorators/permission_decorators.py (السطر 158)
- ./backend/src/middleware/rate_limiter.py (السطر 105)
- ./backend/src/middleware/rate_limiter.py (السطر 230)
- ./backend/src/middleware/rate_limiter.py (السطر 308)
- ./backend/src/middleware/rate_limiter.py (السطر 481)
- ./backend/src/routes/user.py (السطر 69)
- ./backend/src/services/error_handler.py (السطر 444)

### الدالة المكررة 39:
**التوقيع:** decorator_def wrapper(*args, **kwargs): | return wrapper
**المواقع:**
- ./backend/src/auth.py (السطر 528)
- ./backend/src/logging_system.py (السطر 230)
- ./backend/src/logging_system.py (السطر 260)
- ./backend/src/services/cache_service.py (السطر 67)

### الدالة المكررة 40:
**التوقيع:** decrypt_user_data_"""فك تشفير بيانات المستخدم""" | decrypted_data = {} | sensitive_fields = ['email', 'phone', 'address', 'national_id']
**المواقع:**
- ./backend/src/database_encryption.py (السطر 265)
- ./backend/src/encryption_manager.py (السطر 393)

### الدالة المكررة 41:
**التوقيع:** __init___pass
**المواقع:**
- ./backend/src/database_encryption.py (السطر 30)
- ./backend/src/database_encryption.py (السطر 66)
- ./backend/src/models/__init__.py (السطر 14)
- ./backend/src/routes/dashboard.py (السطر 18)
- ./backend/src/routes/excel_import.py (السطر 16)
- ./backend/src/routes/excel_import_clean.py (السطر 15)
- ./backend/src/routes/lot_management.py (السطر 18)
- ./backend/src/routes/security_system.py (السطر 15)

### الدالة المكررة 42:
**التوقيع:** get_return None
**المواقع:**
- ./backend/src/database_encryption.py (السطر 69)
- ./backend/src/database_backup.py (السطر 189)
- ./backend/src/models/inventory.py (السطر 94)
- ./backend/database_archive/database_old/__init__.py (السطر 99)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 187)

### الدالة المكررة 43:
**التوقيع:** __init___self.encryption_manager = encryption_manager
**المواقع:**
- ./backend/src/encryption_manager.py (السطر 362)
- ./backend/src/encryption_manager.py (السطر 449)

### الدالة المكررة 44:
**التوقيع:** add_security_headers_try: | return response
**المواقع:**
- ./backend/src/main.py (السطر 234)
- ./backend/src/unified_server.py (السطر 197)

### الدالة المكررة 45:
**التوقيع:** _rate_limit_login_try:
**المواقع:**
- ./backend/src/main.py (السطر 253)
- ./backend/src/unified_server.py (السطر 179)

### الدالة المكررة 46:
**التوقيع:** _set_sqlite_pragma_if isinstance(dbapi_connection, sqlite3.Connection):
**المواقع:**
- ./backend/src/main.py (السطر 397)
- ./backend/src/unified_server.py (السطر 146)
- ./backend/src/unified_server_clean.py (السطر 127)
- ./backend/tools/smoke_sqlite_locktest.py (السطر 23)

### الدالة المكررة 47:
**التوقيع:** index_"""الصفحة الرئيسية""" | try:
**المواقع:**
- ./backend/src/unified_server.py (السطر 250)
- ./backend/src/unified_server_clean.py (السطر 180)

### الدالة المكررة 48:
**التوقيع:** health_check_"""فحص صحة النظام""" | try:
**المواقع:**
- ./backend/src/unified_server.py (السطر 262)
- ./backend/src/unified_server_clean.py (السطر 193)
- ./backend/src/routes/system_status.py (السطر 84)

### الدالة المكررة 49:
**التوقيع:** system_status_"""حالة النظام""" | try:
**المواقع:**
- ./backend/src/unified_server.py (السطر 280)
- ./backend/src/unified_server_clean.py (السطر 211)

### الدالة المكررة 50:
**التوقيع:** init_database_"""تهيئة قاعدة البيانات""" | try:
**المواقع:**
- ./backend/src/unified_server.py (السطر 419)
- ./backend/src/unified_server_clean.py (السطر 260)

### الدالة المكررة 51:
**التوقيع:** CORS_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 57)
- ./backend/src/unified_server_clean.py (السطر 41)

### الدالة المكررة 52:
**التوقيع:** jsonify_return {"data": data}
**المواقع:**
- ./backend/src/unified_server.py (السطر 60)
- ./backend/src/unified_server_clean.py (السطر 44)
- ./backend/src/decorators/permission_decorators.py (السطر 13)
- ./backend/src/routes/dashboard.py (السطر 26)
- ./backend/src/routes/excel_import.py (السطر 24)
- ./backend/src/routes/excel_import_clean.py (السطر 23)
- ./backend/src/routes/lot_management.py (السطر 26)
- ./backend/src/routes/security_system.py (السطر 23)

### الدالة المكررة 53:
**التوقيع:** render_template_return "Template not available"
**المواقع:**
- ./backend/src/unified_server.py (السطر 71)
- ./backend/src/unified_server_clean.py (السطر 55)

### الدالة المكررة 54:
**التوقيع:** generate_password_hash_return password
**المواقع:**
- ./backend/src/unified_server.py (السطر 77)
- ./backend/src/unified_server_clean.py (السطر 61)

### الدالة المكررة 55:
**التوقيع:** log_click_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 112)
- ./backend/src/unified_server_clean.py (السطر 95)

### الدالة المكررة 56:
**التوقيع:** log_route_access_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 115)
- ./backend/src/unified_server_clean.py (السطر 98)

### الدالة المكررة 57:
**التوقيع:** log_system_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 118)
- ./backend/src/unified_server_clean.py (السطر 101)

### الدالة المكررة 58:
**التوقيع:** __init___self.config = {}
**المواقع:**
- ./backend/src/unified_server.py (السطر 32)
- ./backend/src/unified_server_clean.py (السطر 27)

### الدالة المكررة 59:
**التوقيع:** route_def decorator(f): | return decorator
**المواقع:**
- ./backend/src/unified_server.py (السطر 35)
- ./backend/src/unified_server_clean.py (السطر 30)
- ./backend/src/routes/batch_management.py (السطر 17)
- ./backend/src/routes/batch_reports.py (السطر 17)
- ./backend/src/routes/dashboard.py (السطر 21)
- ./backend/src/routes/excel_import.py (السطر 19)
- ./backend/src/routes/excel_import_clean.py (السطر 18)
- ./backend/src/routes/lot_management.py (السطر 21)
- ./backend/src/routes/security_system.py (السطر 18)

### الدالة المكررة 60:
**التوقيع:** register_blueprint_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 40)
- ./backend/src/unified_server_clean.py (السطر 35)

### الدالة المكررة 61:
**التوقيع:** run_print("Flask not available - running in mock mode")
**المواقع:**
- ./backend/src/unified_server.py (السطر 43)
- ./backend/src/unified_server_clean.py (السطر 38)

### الدالة المكررة 62:
**التوقيع:** init_app_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 87)
- ./backend/src/unified_server_clean.py (السطر 70)
- ./backend/src/database_backup.py (السطر 165)
- ./backend/database_archive/database_old/__init__.py (السطر 80)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 163)

### الدالة المكررة 63:
**التوقيع:** create_all_pass
**المواقع:**
- ./backend/src/unified_server.py (السطر 90)
- ./backend/src/unified_server_clean.py (السطر 73)
- ./backend/src/database_backup.py (السطر 168)
- ./backend/src/models/inventory.py (السطر 111)
- ./backend/src/routes/admin.py (السطر 27)
- ./backend/src/routes/warehouse_transfer.py (السطر 33)
- ./backend/database_archive/database_old/__init__.py (السطر 72)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 166)

### الدالة المكررة 64:
**التوقيع:** engine_return None
**المواقع:**
- ./backend/src/unified_server.py (السطر 94)
- ./backend/src/unified_server_clean.py (السطر 77)

### الدالة المكررة 65:
**التوقيع:** decorator_return f
**المواقع:**
- ./backend/src/unified_server.py (السطر 36)
- ./backend/src/unified_server.py (السطر 53)
- ./backend/src/unified_server_clean.py (السطر 31)
- ./backend/src/routes/batch_management.py (السطر 18)
- ./backend/src/routes/batch_reports.py (السطر 18)
- ./backend/src/routes/dashboard.py (السطر 60)
- ./backend/src/routes/dashboard.py (السطر 22)
- ./backend/src/routes/excel_import.py (السطر 20)
- ./backend/src/routes/excel_import_clean.py (السطر 19)
- ./backend/src/routes/excel_operations.py (السطر 159)
- ./backend/src/routes/lot_management.py (السطر 22)
- ./backend/src/routes/security_system.py (السطر 55)
- ./backend/src/routes/security_system.py (السطر 19)
- ./backend/src/routes/warehouse_transfer.py (السطر 46)

### الدالة المكررة 66:
**التوقيع:** not_found_"""معالج خطأ 404""" | return jsonify({
**المواقع:**
- ./backend/src/unified_server_clean.py (السطر 241)
- ./backend/src/routes/interactive_dashboard.py (السطر 505)

### الدالة المكررة 67:
**التوقيع:** internal_error_"""معالج خطأ 500""" | return jsonify({
**المواقع:**
- ./backend/src/unified_server_clean.py (السطر 251)
- ./backend/src/routes/interactive_dashboard.py (السطر 514)

### الدالة المكررة 68:
**التوقيع:** configure_database_"""تكوين قاعدة البيانات""" | db_path = Path(__file__).parent.parent / 'instance' / 'inventory.db' | db_path.parent.mkdir(exist_ok=True)
**المواقع:**
- ./backend/src/database_backup.py (السطر 20)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 20)

### الدالة المكررة 69:
**التوقيع:** create_tables_"""إنشاء جداول قاعدة البيانات""" | with app.app_context():
**المواقع:**
- ./backend/src/database_backup.py (السطر 50)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 50)

### الدالة المكررة 70:
**التوقيع:** create_default_data_"""إنشاء البيانات الأساسية""" | try:
**المواقع:**
- ./backend/src/database_backup.py (السطر 71)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 71)

### الدالة المكررة 71:
**التوقيع:** set_sqlite_pragma_if 'sqlite' in str(dbapi_connection):
**المواقع:**
- ./backend/src/database_backup.py (السطر 42)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 42)

### الدالة المكررة 72:
**التوقيع:** configure_database_return db
**المواقع:**
- ./backend/src/database_backup.py (السطر 204)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 202)

### الدالة المكررة 73:
**التوقيع:** create_tables_return True
**المواقع:**
- ./backend/src/database_backup.py (السطر 207)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 205)

### الدالة المكررة 74:
**التوقيع:** create_default_data_pass
**المواقع:**
- ./backend/src/database_backup.py (السطر 210)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 208)

### الدالة المكررة 75:
**التوقيع:** Column_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 122)
- ./backend/src/models/accounting_system.py (السطر 28)
- ./backend/src/models/invoices.py (السطر 21)
- ./backend/src/models/invoices_clean.py (السطر 18)
- ./backend/src/models/lot_advanced.py (السطر 32)
- ./backend/src/models/opening_balances_treasury.py (السطر 21)
- ./backend/src/models/payment_management.py (السطر 20)
- ./backend/src/models/permissions.py (السطر 20)
- ./backend/src/models/pickup_delivery_orders.py (السطر 23)
- ./backend/src/models/product_advanced.py (السطر 21)
- ./backend/src/models/profit_loss_system.py (السطر 23)
- ./backend/src/models/region_warehouse.py (السطر 20)
- ./backend/src/models/returns_management.py (السطر 20)
- ./backend/src/models/sales_advanced.py (السطر 22)
- ./backend/src/models/security_system.py (السطر 23)
- ./backend/src/models/stock_movement_advanced.py (السطر 23)
- ./backend/src/models/system_settings_advanced.py (السطر 23)
- ./backend/src/models/treasury_management.py (السطر 23)
- ./backend/src/models/unified_models.py (السطر 23)
- ./backend/src/models/user_management_advanced.py (السطر 23)
- ./backend/src/models/warehouse_adjustments.py (السطر 23)
- ./backend/src/models/warehouse_advanced.py (السطر 23)
- ./backend/src/models/warehouse_constraints.py (السطر 23)
- ./backend/src/models/warehouse_transfer.py (السطر 23)
- ./backend/src/models/partners.py (السطر 23)
- ./backend/database_archive/database_old/__init__.py (السطر 30)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 120)

### الدالة المكررة 76:
**التوقيع:** Integer_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 126)
- ./backend/src/models/accounting_system.py (السطر 31)
- ./backend/src/models/invoices.py (السطر 24)
- ./backend/src/models/invoices_clean.py (السطر 21)
- ./backend/src/models/lot_advanced.py (السطر 35)
- ./backend/src/models/opening_balances_treasury.py (السطر 24)
- ./backend/src/models/payment_management.py (السطر 22)
- ./backend/src/models/permissions.py (السطر 22)
- ./backend/src/models/pickup_delivery_orders.py (السطر 25)
- ./backend/src/models/product_advanced.py (السطر 24)
- ./backend/src/models/profit_loss_system.py (السطر 25)
- ./backend/src/models/region_warehouse.py (السطر 22)
- ./backend/src/models/returns_management.py (السطر 22)
- ./backend/src/models/sales_advanced.py (السطر 24)
- ./backend/src/models/security_system.py (السطر 25)
- ./backend/src/models/stock_movement_advanced.py (السطر 25)
- ./backend/src/models/system_settings_advanced.py (السطر 25)
- ./backend/src/models/treasury_management.py (السطر 25)
- ./backend/src/models/unified_models.py (السطر 26)
- ./backend/src/models/user_management_advanced.py (السطر 25)
- ./backend/src/models/warehouse_adjustments.py (السطر 26)
- ./backend/src/models/warehouse_advanced.py (السطر 25)
- ./backend/src/models/warehouse_constraints.py (السطر 26)
- ./backend/src/models/warehouse_transfer.py (السطر 26)
- ./backend/src/models/partners.py (السطر 25)
- ./backend/database_archive/database_old/__init__.py (السطر 34)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 124)

### الدالة المكررة 77:
**التوقيع:** String_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 130)
- ./backend/src/models/accounting_system.py (السطر 34)
- ./backend/src/models/invoices.py (السطر 27)
- ./backend/src/models/invoices_clean.py (السطر 24)
- ./backend/src/models/lot_advanced.py (السطر 38)
- ./backend/src/models/opening_balances_treasury.py (السطر 27)
- ./backend/src/models/payment_management.py (السطر 24)
- ./backend/src/models/permissions.py (السطر 24)
- ./backend/src/models/pickup_delivery_orders.py (السطر 27)
- ./backend/src/models/product_advanced.py (السطر 27)
- ./backend/src/models/profit_loss_system.py (السطر 27)
- ./backend/src/models/region_warehouse.py (السطر 24)
- ./backend/src/models/returns_management.py (السطر 24)
- ./backend/src/models/sales_advanced.py (السطر 26)
- ./backend/src/models/security_system.py (السطر 27)
- ./backend/src/models/stock_movement_advanced.py (السطر 27)
- ./backend/src/models/system_settings_advanced.py (السطر 27)
- ./backend/src/models/treasury_management.py (السطر 27)
- ./backend/src/models/unified_models.py (السطر 29)
- ./backend/src/models/user_management_advanced.py (السطر 27)
- ./backend/src/models/warehouse_adjustments.py (السطر 29)
- ./backend/src/models/warehouse_advanced.py (السطر 27)
- ./backend/src/models/warehouse_constraints.py (السطر 29)
- ./backend/src/models/warehouse_transfer.py (السطر 29)
- ./backend/src/models/partners.py (السطر 27)
- ./backend/database_archive/database_old/__init__.py (السطر 38)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 128)

### الدالة المكررة 78:
**التوقيع:** Text_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 134)
- ./backend/src/models/accounting_system.py (السطر 46)
- ./backend/src/models/invoices.py (السطر 30)
- ./backend/src/models/invoices_clean.py (السطر 36)
- ./backend/src/models/opening_balances_treasury.py (السطر 36)
- ./backend/src/models/payment_management.py (السطر 32)
- ./backend/src/models/permissions.py (السطر 32)
- ./backend/src/models/pickup_delivery_orders.py (السطر 35)
- ./backend/src/models/product_advanced.py (السطر 36)
- ./backend/src/models/profit_loss_system.py (السطر 35)
- ./backend/src/models/region_warehouse.py (السطر 32)
- ./backend/src/models/returns_management.py (السطر 32)
- ./backend/src/models/sales_advanced.py (السطر 34)
- ./backend/src/models/security_system.py (السطر 35)
- ./backend/src/models/stock_movement_advanced.py (السطر 35)
- ./backend/src/models/system_settings_advanced.py (السطر 35)
- ./backend/src/models/treasury_management.py (السطر 35)
- ./backend/src/models/unified_models.py (السطر 41)
- ./backend/src/models/user_management_advanced.py (السطر 35)
- ./backend/src/models/warehouse_adjustments.py (السطر 41)
- ./backend/src/models/warehouse_advanced.py (السطر 35)
- ./backend/src/models/warehouse_constraints.py (السطر 41)
- ./backend/src/models/warehouse_transfer.py (السطر 41)
- ./backend/src/models/partners.py (السطر 35)
- ./backend/database_archive/database_old/__init__.py (السطر 42)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 132)

### الدالة المكررة 79:
**التوقيع:** DateTime_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 138)
- ./backend/src/models/accounting_system.py (السطر 40)
- ./backend/src/models/invoices.py (السطر 33)
- ./backend/src/models/invoices_clean.py (السطر 30)
- ./backend/src/models/lot_advanced.py (السطر 41)
- ./backend/src/models/opening_balances_treasury.py (السطر 33)
- ./backend/src/models/payment_management.py (السطر 28)
- ./backend/src/models/permissions.py (السطر 28)
- ./backend/src/models/pickup_delivery_orders.py (السطر 31)
- ./backend/src/models/product_advanced.py (السطر 33)
- ./backend/src/models/profit_loss_system.py (السطر 31)
- ./backend/src/models/region_warehouse.py (السطر 28)
- ./backend/src/models/returns_management.py (السطر 28)
- ./backend/src/models/sales_advanced.py (السطر 30)
- ./backend/src/models/security_system.py (السطر 31)
- ./backend/src/models/stock_movement_advanced.py (السطر 31)
- ./backend/src/models/system_settings_advanced.py (السطر 31)
- ./backend/src/models/treasury_management.py (السطر 31)
- ./backend/src/models/unified_models.py (السطر 35)
- ./backend/src/models/user_management_advanced.py (السطر 31)
- ./backend/src/models/warehouse_adjustments.py (السطر 35)
- ./backend/src/models/warehouse_advanced.py (السطر 31)
- ./backend/src/models/warehouse_constraints.py (السطر 35)
- ./backend/src/models/warehouse_transfer.py (السطر 35)
- ./backend/src/models/partners.py (السطر 31)
- ./backend/database_archive/database_old/__init__.py (السطر 46)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 136)

### الدالة المكررة 80:
**التوقيع:** Boolean_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 142)
- ./backend/src/models/accounting_system.py (السطر 43)
- ./backend/src/models/invoices.py (السطر 36)
- ./backend/src/models/invoices_clean.py (السطر 33)
- ./backend/src/models/lot_advanced.py (السطر 44)
- ./backend/src/models/opening_balances_treasury.py (السطر 39)
- ./backend/src/models/payment_management.py (السطر 30)
- ./backend/src/models/permissions.py (السطر 30)
- ./backend/src/models/pickup_delivery_orders.py (السطر 33)
- ./backend/src/models/product_advanced.py (السطر 39)
- ./backend/src/models/profit_loss_system.py (السطر 33)
- ./backend/src/models/region_warehouse.py (السطر 30)
- ./backend/src/models/returns_management.py (السطر 30)
- ./backend/src/models/sales_advanced.py (السطر 32)
- ./backend/src/models/security_system.py (السطر 33)
- ./backend/src/models/stock_movement_advanced.py (السطر 33)
- ./backend/src/models/system_settings_advanced.py (السطر 33)
- ./backend/src/models/treasury_management.py (السطر 33)
- ./backend/src/models/unified_models.py (السطر 38)
- ./backend/src/models/user_management_advanced.py (السطر 33)
- ./backend/src/models/warehouse_adjustments.py (السطر 38)
- ./backend/src/models/warehouse_advanced.py (السطر 33)
- ./backend/src/models/warehouse_constraints.py (السطر 38)
- ./backend/src/models/warehouse_transfer.py (السطر 38)
- ./backend/src/models/partners.py (السطر 33)
- ./backend/database_archive/database_old/__init__.py (السطر 50)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 140)

### الدالة المكررة 81:
**التوقيع:** Float_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 146)
- ./backend/src/models/accounting_system.py (السطر 37)
- ./backend/src/models/invoices.py (السطر 39)
- ./backend/src/models/invoices_clean.py (السطر 27)
- ./backend/src/models/lot_advanced.py (السطر 47)
- ./backend/src/models/opening_balances_treasury.py (السطر 30)
- ./backend/src/models/payment_management.py (السطر 26)
- ./backend/src/models/permissions.py (السطر 26)
- ./backend/src/models/pickup_delivery_orders.py (السطر 29)
- ./backend/src/models/product_advanced.py (السطر 30)
- ./backend/src/models/profit_loss_system.py (السطر 29)
- ./backend/src/models/region_warehouse.py (السطر 26)
- ./backend/src/models/returns_management.py (السطر 26)
- ./backend/src/models/sales_advanced.py (السطر 28)
- ./backend/src/models/security_system.py (السطر 29)
- ./backend/src/models/stock_movement_advanced.py (السطر 29)
- ./backend/src/models/system_settings_advanced.py (السطر 29)
- ./backend/src/models/treasury_management.py (السطر 29)
- ./backend/src/models/unified_models.py (السطر 32)
- ./backend/src/models/user_management_advanced.py (السطر 29)
- ./backend/src/models/warehouse_adjustments.py (السطر 32)
- ./backend/src/models/warehouse_advanced.py (السطر 29)
- ./backend/src/models/warehouse_constraints.py (السطر 32)
- ./backend/src/models/warehouse_transfer.py (السطر 32)
- ./backend/src/models/partners.py (السطر 29)
- ./backend/database_archive/database_old/__init__.py (السطر 54)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 144)

### الدالة المكررة 82:
**التوقيع:** Date_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 150)
- ./backend/src/models/accounting_system.py (السطر 52)
- ./backend/src/models/invoices.py (السطر 42)
- ./backend/src/models/invoices_clean.py (السطر 42)
- ./backend/src/models/lot_advanced.py (السطر 50)
- ./backend/src/models/payment_management.py (السطر 36)
- ./backend/src/models/permissions.py (السطر 36)
- ./backend/src/models/pickup_delivery_orders.py (السطر 39)
- ./backend/src/models/product_advanced.py (السطر 45)
- ./backend/src/models/profit_loss_system.py (السطر 39)
- ./backend/src/models/region_warehouse.py (السطر 36)
- ./backend/src/models/returns_management.py (السطر 36)
- ./backend/src/models/sales_advanced.py (السطر 38)
- ./backend/src/models/security_system.py (السطر 39)
- ./backend/src/models/stock_movement_advanced.py (السطر 39)
- ./backend/src/models/system_settings_advanced.py (السطر 39)
- ./backend/src/models/treasury_management.py (السطر 39)
- ./backend/src/models/unified_models.py (السطر 47)
- ./backend/src/models/user_management_advanced.py (السطر 39)
- ./backend/src/models/warehouse_adjustments.py (السطر 47)
- ./backend/src/models/warehouse_advanced.py (السطر 39)
- ./backend/src/models/warehouse_constraints.py (السطر 47)
- ./backend/src/models/warehouse_transfer.py (السطر 47)
- ./backend/src/models/partners.py (السطر 39)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 148)

### الدالة المكررة 83:
**التوقيع:** ForeignKey_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 154)
- ./backend/src/models/accounting_system.py (السطر 55)
- ./backend/src/models/invoices.py (السطر 45)
- ./backend/src/models/invoices_clean.py (السطر 45)
- ./backend/src/models/lot_advanced.py (السطر 53)
- ./backend/src/models/opening_balances_treasury.py (السطر 42)
- ./backend/src/models/payment_management.py (السطر 38)
- ./backend/src/models/permissions.py (السطر 38)
- ./backend/src/models/pickup_delivery_orders.py (السطر 41)
- ./backend/src/models/product_advanced.py (السطر 42)
- ./backend/src/models/profit_loss_system.py (السطر 41)
- ./backend/src/models/region_warehouse.py (السطر 38)
- ./backend/src/models/returns_management.py (السطر 38)
- ./backend/src/models/sales_advanced.py (السطر 40)
- ./backend/src/models/security_system.py (السطر 41)
- ./backend/src/models/stock_movement_advanced.py (السطر 41)
- ./backend/src/models/system_settings_advanced.py (السطر 41)
- ./backend/src/models/treasury_management.py (السطر 41)
- ./backend/src/models/unified_models.py (السطر 50)
- ./backend/src/models/user_management_advanced.py (السطر 41)
- ./backend/src/models/warehouse_adjustments.py (السطر 50)
- ./backend/src/models/warehouse_advanced.py (السطر 41)
- ./backend/src/models/warehouse_constraints.py (السطر 50)
- ./backend/src/models/warehouse_transfer.py (السطر 50)
- ./backend/src/models/partners.py (السطر 41)
- ./backend/database_archive/database_old/__init__.py (السطر 58)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 152)

### الدالة المكررة 84:
**التوقيع:** Numeric_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 158)
- ./backend/src/models/accounting_system.py (السطر 58)
- ./backend/src/models/invoices.py (السطر 51)
- ./backend/src/models/invoices_clean.py (السطر 48)
- ./backend/src/models/opening_balances_treasury.py (السطر 48)
- ./backend/src/models/payment_management.py (السطر 40)
- ./backend/src/models/permissions.py (السطر 40)
- ./backend/src/models/pickup_delivery_orders.py (السطر 43)
- ./backend/src/models/product_advanced.py (السطر 48)
- ./backend/src/models/profit_loss_system.py (السطر 43)
- ./backend/src/models/region_warehouse.py (السطر 40)
- ./backend/src/models/returns_management.py (السطر 40)
- ./backend/src/models/sales_advanced.py (السطر 42)
- ./backend/src/models/security_system.py (السطر 43)
- ./backend/src/models/stock_movement_advanced.py (السطر 43)
- ./backend/src/models/system_settings_advanced.py (السطر 43)
- ./backend/src/models/treasury_management.py (السطر 43)
- ./backend/src/models/unified_models.py (السطر 53)
- ./backend/src/models/user_management_advanced.py (السطر 43)
- ./backend/src/models/warehouse_adjustments.py (السطر 53)
- ./backend/src/models/warehouse_advanced.py (السطر 43)
- ./backend/src/models/warehouse_constraints.py (السطر 53)
- ./backend/src/models/warehouse_transfer.py (السطر 53)
- ./backend/src/models/partners.py (السطر 43)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 156)

### الدالة المكررة 85:
**التوقيع:** relationship_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 162)
- ./backend/src/models/accounting_system.py (السطر 61)
- ./backend/src/models/invoices.py (السطر 54)
- ./backend/src/models/invoices_clean.py (السطر 51)
- ./backend/src/models/opening_balances_treasury.py (السطر 51)
- ./backend/src/models/payment_management.py (السطر 42)
- ./backend/src/models/permissions.py (السطر 42)
- ./backend/src/models/pickup_delivery_orders.py (السطر 45)
- ./backend/src/models/product_advanced.py (السطر 54)
- ./backend/src/models/profit_loss_system.py (السطر 45)
- ./backend/src/models/region_warehouse.py (السطر 42)
- ./backend/src/models/returns_management.py (السطر 42)
- ./backend/src/models/sales_advanced.py (السطر 44)
- ./backend/src/models/security_system.py (السطر 45)
- ./backend/src/models/stock_movement_advanced.py (السطر 45)
- ./backend/src/models/system_settings_advanced.py (السطر 45)
- ./backend/src/models/treasury_management.py (السطر 45)
- ./backend/src/models/unified_models.py (السطر 56)
- ./backend/src/models/user_management_advanced.py (السطر 45)
- ./backend/src/models/warehouse_adjustments.py (السطر 56)
- ./backend/src/models/warehouse_advanced.py (السطر 45)
- ./backend/src/models/warehouse_constraints.py (السطر 56)
- ./backend/src/models/warehouse_transfer.py (السطر 56)
- ./backend/src/models/partners.py (السطر 45)
- ./backend/database_archive/database_old/__init__.py (السطر 62)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 160)

### الدالة المكررة 86:
**التوقيع:** filter_return self
**المواقع:**
- ./backend/src/database_backup.py (السطر 174)
- ./backend/src/models/inventory.py (السطر 73)
- ./backend/src/routes/excel_operations.py (السطر 37)
- ./backend/database_archive/database_old/__init__.py (السطر 84)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 172)

### الدالة المكررة 87:
**التوقيع:** filter_by_return self
**المواقع:**
- ./backend/src/database_backup.py (السطر 177)
- ./backend/src/models/inventory.py (السطر 70)
- ./backend/src/routes/admin.py (السطر 92)
- ./backend/src/routes/excel_operations.py (السطر 34)
- ./backend/database_archive/database_old/__init__.py (السطر 87)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 175)

### الدالة المكررة 88:
**التوقيع:** first_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 180)
- ./backend/src/models/inventory.py (السطر 79)
- ./backend/src/routes/admin.py (السطر 95)
- ./backend/src/routes/excel_operations.py (السطر 43)
- ./backend/database_archive/database_old/__init__.py (السطر 90)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 178)

### الدالة المكررة 89:
**التوقيع:** all_return []
**المواقع:**
- ./backend/src/database_backup.py (السطر 183)
- ./backend/src/models/inventory.py (السطر 76)
- ./backend/src/routes/admin.py (السطر 98)
- ./backend/src/routes/excel_operations.py (السطر 40)
- ./backend/database_archive/database_old/__init__.py (السطر 93)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 181)

### الدالة المكررة 90:
**التوقيع:** count_return 0
**المواقع:**
- ./backend/src/database_backup.py (السطر 186)
- ./backend/src/models/inventory.py (السطر 82)
- ./backend/src/routes/admin.py (السطر 106)
- ./backend/src/routes/dashboard.py (السطر 38)
- ./backend/src/routes/excel_operations.py (السطر 46)
- ./backend/src/routes/lot_management.py (السطر 42)
- ./backend/src/routes/security_system.py (السطر 74)
- ./backend/database_archive/database_old/__init__.py (السطر 96)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 184)

### الدالة المكررة 91:
**التوقيع:** get_or_404_return None
**المواقع:**
- ./backend/src/database_backup.py (السطر 192)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 190)

### الدالة المكررة 92:
**التوقيع:** paginate_class MockPagination: | return MockPagination()
**المواقع:**
- ./backend/src/database_backup.py (السطر 195)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 193)

### الدالة المكررة 93:
**التوقيع:** __init___for key, value in kwargs.items():
**المواقع:**
- ./backend/src/database_backup.py (السطر 110)
- ./backend/src/models/accounting_system.py (السطر 79)
- ./backend/src/models/inventory.py (السطر 99)
- ./backend/src/models/invoices.py (السطر 59)
- ./backend/src/models/invoices_clean.py (السطر 111)
- ./backend/src/models/invoices_clean.py (السطر 69)
- ./backend/src/models/lot_advanced.py (السطر 25)
- ./backend/src/models/payment_management.py (السطر 59)
- ./backend/src/models/permissions.py (السطر 59)
- ./backend/src/models/pickup_delivery_orders.py (السطر 62)
- ./backend/src/models/profit_loss_system.py (السطر 62)
- ./backend/src/models/region_warehouse.py (السطر 59)
- ./backend/src/models/returns_management.py (السطر 59)
- ./backend/src/models/sales_advanced.py (السطر 64)
- ./backend/src/models/security_system.py (السطر 62)
- ./backend/src/models/stock_movement_advanced.py (السطر 62)
- ./backend/src/models/system_settings_advanced.py (السطر 62)
- ./backend/src/models/treasury_management.py (السطر 62)
- ./backend/src/models/unified_models.py (السطر 74)
- ./backend/src/models/user_management_advanced.py (السطر 62)
- ./backend/src/models/warehouse_adjustments.py (السطر 74)
- ./backend/src/models/warehouse_advanced.py (السطر 62)
- ./backend/src/models/warehouse_constraints.py (السطر 74)
- ./backend/src/models/partners.py (السطر 59)
- ./backend/src/routes/admin_panel.py (السطر 46)
- ./backend/src/routes/admin_panel.py (السطر 58)
- ./backend/src/routes/admin_panel.py (السطر 67)
- ./backend/src/routes/admin_panel.py (السطر 72)
- ./backend/src/routes/admin_panel.py (السطر 77)
- ./backend/src/routes/excel_import.py (السطر 88)
- ./backend/src/routes/excel_import.py (السطر 93)
- ./backend/src/routes/excel_import.py (السطر 98)
- ./backend/src/routes/excel_import.py (السطر 103)
- ./backend/src/routes/excel_import_clean.py (السطر 64)
- ./backend/src/routes/excel_import_clean.py (السطر 69)
- ./backend/src/routes/excel_import_clean.py (السطر 74)
- ./backend/src/routes/excel_import_clean.py (السطر 79)
- ./backend/src/routes/import_data.py (السطر 59)
- ./backend/src/routes/import_data.py (السطر 64)
- ./backend/src/routes/import_data.py (السطر 69)
- ./backend/src/routes/import_data.py (السطر 74)
- ./backend/src/routes/import_data.py (السطر 84)
- ./backend/src/routes/import_data.py (السطر 89)
- ./backend/src/routes/inventory.py (السطر 24)
- ./backend/src/routes/inventory.py (السطر 29)
- ./backend/src/routes/inventory.py (السطر 34)
- ./backend/src/routes/inventory.py (السطر 39)
- ./backend/src/routes/inventory.py (السطر 44)
- ./backend/src/routes/inventory.py (السطر 49)
- ./backend/src/routes/lot_management.py (السطر 79)
- ./backend/src/routes/security_system.py (السطر 84)
- ./backend/src/routes/accounting_system.py (السطر 57)
- ./backend/src/routes/accounting_system.py (السطر 62)
- ./backend/src/routes/accounting_system.py (السطر 67)
- ./backend/src/routes/accounting_system.py (السطر 72)
- ./backend/src/routes/accounting_system.py (السطر 79)
- ./backend/src/routes/accounting_system.py (السطر 89)
- ./backend/src/routes/accounting_system.py (السطر 94)
- ./backend/database_archive/database_old/__init__.py (السطر 18)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 108)

### الدالة المكررة 94:
**التوقيع:** to_dict_return {}
**المواقع:**
- ./backend/src/database_backup.py (السطر 114)
- ./backend/src/models/accounting_system.py (السطر 83)
- ./backend/src/models/inventory.py (السطر 103)
- ./backend/src/models/invoices.py (السطر 63)
- ./backend/src/models/invoices_clean.py (السطر 115)
- ./backend/src/models/invoices_clean.py (السطر 73)
- ./backend/src/models/lot_advanced.py (السطر 29)
- ./backend/src/models/payment_management.py (السطر 62)
- ./backend/src/models/permissions.py (السطر 62)
- ./backend/src/models/pickup_delivery_orders.py (السطر 65)
- ./backend/src/models/profit_loss_system.py (السطر 65)
- ./backend/src/models/region_warehouse.py (السطر 62)
- ./backend/src/models/returns_management.py (السطر 62)
- ./backend/src/models/sales_advanced.py (السطر 67)
- ./backend/src/models/security_system.py (السطر 65)
- ./backend/src/models/stock_movement_advanced.py (السطر 65)
- ./backend/src/models/system_settings_advanced.py (السطر 65)
- ./backend/src/models/treasury_management.py (السطر 65)
- ./backend/src/models/unified_models.py (السطر 77)
- ./backend/src/models/user_management_advanced.py (السطر 65)
- ./backend/src/models/warehouse_adjustments.py (السطر 78)
- ./backend/src/models/warehouse_advanced.py (السطر 65)
- ./backend/src/models/warehouse_constraints.py (السطر 78)
- ./backend/src/models/partners.py (السطر 62)
- ./backend/src/routes/partners.py (السطر 23)
- ./backend/src/routes/partners.py (السطر 44)
- ./backend/src/routes/region_warehouse.py (السطر 25)
- ./backend/src/routes/region_warehouse.py (السطر 41)
- ./backend/src/routes/accounting_system.py (السطر 83)
- ./backend/database_archive/database_old/__init__.py (السطر 22)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 112)

### الدالة المكررة 95:
**التوقيع:** query_return MockQuery()
**المواقع:**
- ./backend/src/database_backup.py (السطر 118)
- ./backend/src/models/inventory.py (السطر 107)
- ./backend/src/routes/admin.py (السطر 65)
- ./backend/src/routes/admin.py (السطر 86)
- ./backend/src/routes/excel_operations.py (السطر 58)
- ./backend/src/routes/excel_operations.py (السطر 69)
- ./backend/src/routes/excel_operations.py (السطر 80)
- ./backend/src/routes/excel_operations.py (السطر 96)
- ./backend/src/routes/excel_operations.py (السطر 115)
- ./backend/src/routes/excel_operations.py (السطر 128)
- ./backend/database_archive/database_old/__init__.py (السطر 26)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 116)

### الدالة المكررة 96:
**التوقيع:** decorated_function_try:
**المواقع:**
- ./backend/src/decorators/permission_decorators.py (السطر 59)
- ./backend/src/decorators/permission_decorators.py (السطر 124)
- ./backend/src/decorators/permission_decorators.py (السطر 82)
- ./backend/src/decorators/permission_decorators.py (السطر 160)
- ./backend/src/services/error_handler.py (السطر 446)

### الدالة المكررة 97:
**التوقيع:** get_current_user_return None
**المواقع:**
- ./backend/src/decorators/permission_decorators.py (السطر 34)
- ./backend/src/routes/dashboard.py (السطر 70)
- ./backend/src/routes/security_system.py (السطر 65)

### الدالة المكررة 98:
**التوقيع:** process_sale_order_"""معالجة أمر بيع وتأثيره على المخزون""" | try:
**المواقع:**
- ./backend/src/integration/system_integration.py (السطر 145)
- ./backend/src/routes/integration_apis.py (السطر 123)

### الدالة المكررة 99:
**التوقيع:** get_user_accessible_warehouses_"""الحصول على المخازن المتاحة للمستخدم""" | try:
**المواقع:**
- ./backend/src/integration/system_integration.py (السطر 240)
- ./backend/src/routes/integration_apis.py (السطر 316)

### الدالة المكررة 100:
**التوقيع:** cleanup_old_data_"""تنظيف البيانات القديمة""" | try:
**المواقع:**
- ./backend/src/middleware/rate_limiter.py (السطر 675)
- ./backend/src/services/performance_optimizer.py (السطر 687)

### الدالة المكررة 101:
**التوقيع:** to_dict_return {
**المواقع:**
- ./backend/src/models/accounting_system.py (السطر 110)
- ./backend/src/models/inventory.py (السطر 190)
- ./backend/src/models/inventory.py (السطر 234)
- ./backend/src/models/inventory.py (السطر 276)
- ./backend/src/models/inventory.py (السطر 302)
- ./backend/src/models/inventory.py (السطر 329)
- ./backend/src/models/invoices.py (السطر 97)
- ./backend/src/models/invoices.py (السطر 127)
- ./backend/src/models/invoices.py (السطر 160)
- ./backend/src/models/invoices.py (السطر 186)
- ./backend/src/models/invoices.py (السطر 213)
- ./backend/src/models/invoices.py (السطر 238)
- ./backend/src/models/invoices.py (السطر 263)
- ./backend/src/models/invoices_clean.py (السطر 102)
- ./backend/src/models/payment_management.py (السطر 159)
- ./backend/src/models/payment_management.py (السطر 260)
- ./backend/src/models/payment_management.py (السطر 333)
- ./backend/src/models/payment_management.py (السطر 378)
- ./backend/src/models/payment_management.py (السطر 421)
- ./backend/src/models/payment_management.py (السطر 466)
- ./backend/src/models/payment_management.py (السطر 503)
- ./backend/src/models/payment_management.py (السطر 532)
- ./backend/src/models/permissions.py (السطر 89)
- ./backend/src/models/pickup_delivery_orders.py (السطر 92)
- ./backend/src/models/profit_loss_system.py (السطر 92)
- ./backend/src/models/region_warehouse.py (السطر 89)
- ./backend/src/models/region_warehouse.py (السطر 113)
- ./backend/src/models/region_warehouse.py (السطر 146)
- ./backend/src/models/returns_management.py (السطر 89)
- ./backend/src/models/sales_advanced.py (السطر 119)
- ./backend/src/models/sales_advanced.py (السطر 167)
- ./backend/src/models/sales_advanced.py (السطر 213)
- ./backend/src/models/sales_advanced.py (السطر 251)
- ./backend/src/models/sales_advanced.py (السطر 281)
- ./backend/src/models/sales_advanced.py (السطر 309)
- ./backend/src/models/security_system.py (السطر 92)
- ./backend/src/models/stock_movement_advanced.py (السطر 92)
- ./backend/src/models/system_settings_advanced.py (السطر 92)
- ./backend/src/models/treasury_management.py (السطر 139)
- ./backend/src/models/treasury_management.py (السطر 215)
- ./backend/src/models/treasury_management.py (السطر 284)
- ./backend/src/models/treasury_management.py (السطر 331)
- ./backend/src/models/treasury_management.py (السطر 377)
- ./backend/src/models/unified_models.py (السطر 132)
- ./backend/src/models/unified_models.py (السطر 149)
- ./backend/src/models/user.py (السطر 37)
- ./backend/src/models/user.py (السطر 225)
- ./backend/src/models/user.py (السطر 270)
- ./backend/src/models/user_management_advanced.py (السطر 92)
- ./backend/src/models/warehouse_adjustments.py (السطر 105)
- ./backend/src/models/warehouse_advanced.py (السطر 92)
- ./backend/src/models/warehouse_constraints.py (السطر 105)
- ./backend/src/models/warehouse_transfer.py (السطر 112)
- ./backend/src/models/warehouse_transfer.py (السطر 185)
- ./backend/src/models/warehouse_transfer.py (السطر 220)
- ./backend/src/models/partners.py (السطر 107)
- ./backend/src/models/partners.py (السطر 139)
- ./backend/src/models/partners.py (السطر 178)

### الدالة المكررة 102:
**التوقيع:** Enum_return None
**المواقع:**
- ./backend/src/models/accounting_system.py (السطر 49)
- ./backend/src/models/invoices_clean.py (السطر 39)
- ./backend/src/models/opening_balances_treasury.py (السطر 45)
- ./backend/src/models/payment_management.py (السطر 34)
- ./backend/src/models/permissions.py (السطر 34)
- ./backend/src/models/pickup_delivery_orders.py (السطر 37)
- ./backend/src/models/product_advanced.py (السطر 51)
- ./backend/src/models/profit_loss_system.py (السطر 37)
- ./backend/src/models/region_warehouse.py (السطر 34)
- ./backend/src/models/returns_management.py (السطر 34)
- ./backend/src/models/sales_advanced.py (السطر 36)
- ./backend/src/models/security_system.py (السطر 37)
- ./backend/src/models/stock_movement_advanced.py (السطر 37)
- ./backend/src/models/system_settings_advanced.py (السطر 37)
- ./backend/src/models/treasury_management.py (السطر 37)
- ./backend/src/models/unified_models.py (السطر 44)
- ./backend/src/models/user_management_advanced.py (السطر 37)
- ./backend/src/models/warehouse_adjustments.py (السطر 44)
- ./backend/src/models/warehouse_advanced.py (السطر 37)
- ./backend/src/models/warehouse_constraints.py (السطر 44)
- ./backend/src/models/warehouse_transfer.py (السطر 44)
- ./backend/src/models/partners.py (السطر 37)

### الدالة المكررة 103:
**التوقيع:** drop_all_pass
**المواقع:**
- ./backend/src/models/inventory.py (السطر 115)
- ./backend/src/routes/admin.py (السطر 31)
- ./backend/src/routes/warehouse_transfer.py (السطر 36)
- ./backend/database_archive/database_old/__init__.py (السطر 76)

### الدالة المكررة 104:
**التوقيع:** declarative_base_class Base: | return Base
**المواقع:**
- ./backend/src/models/opening_balances_treasury.py (السطر 59)
- ./backend/src/models/product_advanced.py (السطر 57)

### الدالة المكررة 105:
**التوقيع:** decorator_return func
**المواقع:**
- ./backend/src/models/opening_balances_treasury.py (السطر 55)
- ./backend/src/routes/automation.py (السطر 45)

### الدالة المكررة 106:
**التوقيع:** get_payment_method_display_"""الحصول على عرض طريقة الدفع باللغة العربية""" | method_map = { | return method_map.get(self.payment_method, 'غير محدد')
**المواقع:**
- ./backend/src/models/payment_management.py (السطر 209)
- ./backend/src/models/payment_management.py (السطر 348)

### الدالة المكررة 107:
**التوقيع:** backref_return None
**المواقع:**
- ./backend/src/models/sales_advanced.py (السطر 46)
- ./backend/database_archive/database_old/__init__.py (السطر 66)

### الدالة المكررة 108:
**التوقيع:** to_dict_"""تحويل النموذج إلى قاموس""" | return {
**المواقع:**
- ./backend/src/models/customer.py (السطر 65)
- ./backend/src/models/supplier.py (السطر 69)
- ./backend/src/models/invoice.py (السطر 59)
- ./backend/src/models/invoice.py (السطر 136)
- ./backend/src/models/invoice.py (السطر 185)

### الدالة المكررة 109:
**التوقيع:** __repr___return f'<Payment {self.amount} for Invoice {self.invoice_id}>'
**المواقع:**
- ./backend/src/models/invoice.py (السطر 182)
- ./backend/src/models/unified_invoice.py (السطر 227)

### الدالة المكررة 110:
**التوقيع:** get_customers_"""الحصول على قائمة العملاء""" | try:
**المواقع:**
- ./backend/src/routes/customers.py (السطر 14)
- ./backend/src/routes/returns_management.py (السطر 588)
- ./backend/src/routes/sales_advanced.py (السطر 192)

### الدالة المكررة 111:
**التوقيع:** get_customer_"""الحصول على عميل محدد""" | try:
**المواقع:**
- ./backend/src/routes/customers.py (السطر 104)
- ./backend/src/routes/partners.py (السطر 280)

### الدالة المكررة 112:
**التوقيع:** create_customer_"""إنشاء عميل جديد""" | try:
**المواقع:**
- ./backend/src/routes/customers.py (السطر 146)
- ./backend/src/routes/partners.py (السطر 242)
- ./backend/src/routes/sales_advanced.py (السطر 242)

### الدالة المكررة 113:
**التوقيع:** get_users_"""الحصول على قائمة المستخدمين""" | try:
**المواقع:**
- ./backend/src/routes/admin.py (السطر 122)
- ./backend/src/routes/security_system.py (السطر 282)
- ./backend/src/routes/user.py (السطر 480)

### الدالة المكررة 114:
**التوقيع:** create_user_"""إنشاء مستخدم جديد""" | try:
**المواقع:**
- ./backend/src/routes/admin.py (السطر 153)
- ./backend/src/routes/admin_panel.py (السطر 265)
- ./backend/src/routes/user.py (السطر 534)
- ./backend/src/routes/user_management_advanced.py (السطر 98)

### الدالة المكررة 115:
**التوقيع:** update_user_"""تحديث بيانات المستخدم""" | try:
**المواقع:**
- ./backend/src/routes/admin.py (السطر 217)
- ./backend/src/routes/admin_panel.py (السطر 349)

### الدالة المكررة 116:
**التوقيع:** delete_user_"""حذف المستخدم""" | try:
**المواقع:**
- ./backend/src/routes/admin.py (السطر 284)
- ./backend/src/routes/admin_panel.py (السطر 421)

### الدالة المكررة 117:
**التوقيع:** get_roles_"""الحصول على قائمة الأدوار""" | try:
**المواقع:**
- ./backend/src/routes/admin.py (السطر 309)
- ./backend/src/routes/permissions.py (السطر 124)
- ./backend/src/routes/user.py (السطر 739)
- ./backend/src/routes/user_management_advanced.py (السطر 437)

### الدالة المكررة 118:
**التوقيع:** create_role_"""إنشاء دور جديد""" | try:
**المواقع:**
- ./backend/src/routes/admin.py (السطر 334)
- ./backend/src/routes/user_management_advanced.py (السطر 455)

### الدالة المكررة 119:
**التوقيع:** add_pass
**المواقع:**
- ./backend/src/routes/admin.py (السطر 37)
- ./backend/src/routes/excel_import.py (السطر 74)
- ./backend/src/routes/excel_import_clean.py (السطر 50)
- ./backend/src/routes/lot_management.py (السطر 63)
- ./backend/src/routes/security_system.py (السطر 92)

### الدالة المكررة 120:
**التوقيع:** commit_pass
**المواقع:**
- ./backend/src/routes/admin.py (السطر 40)
- ./backend/src/routes/excel_import.py (السطر 78)
- ./backend/src/routes/excel_import_clean.py (السطر 54)
- ./backend/src/routes/lot_management.py (السطر 67)
- ./backend/src/routes/security_system.py (السطر 96)

### الدالة المكررة 121:
**التوقيع:** rollback_pass
**المواقع:**
- ./backend/src/routes/admin.py (السطر 43)
- ./backend/src/routes/excel_import.py (السطر 82)
- ./backend/src/routes/excel_import_clean.py (السطر 58)
- ./backend/src/routes/lot_management.py (السطر 71)

### الدالة المكررة 122:
**التوقيع:** and__return True
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 20)
- ./backend/src/routes/dashboard.py (السطر 45)
- ./backend/src/routes/lot_management.py (السطر 49)

### الدالة المكررة 123:
**التوقيع:** or__return True
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 23)
- ./backend/src/routes/dashboard.py (السطر 48)
- ./backend/src/routes/lot_management.py (السطر 52)

### الدالة المكررة 124:
**التوقيع:** login_required_def login_required(f): return f
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 85)
- ./backend/src/routes/export.py (السطر 67)
- ./backend/src/routes/payment_debt_management.py (السطر 107)
- ./backend/src/routes/permissions.py (السطر 26)
- ./backend/src/routes/profit_loss_system.py (السطر 32)
- ./backend/src/routes/region_warehouse.py (السطر 63)
- ./backend/src/routes/sales_advanced.py (السطر 37)
- ./backend/src/routes/settings.py (السطر 16)
- ./backend/src/routes/warehouse_transfer.py (السطر 44)

### الدالة المكررة 125:
**التوقيع:** has_permission_def decorator(f): return f | return decorator
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 87)
- ./backend/src/routes/export.py (السطر 69)
- ./backend/src/routes/payment_debt_management.py (السطر 110)
- ./backend/src/routes/permissions.py (السطر 28)
- ./backend/src/routes/profit_loss_system.py (السطر 33)
- ./backend/src/routes/region_warehouse.py (السطر 65)
- ./backend/src/routes/sales_advanced.py (السطر 39)
- ./backend/src/routes/settings.py (السطر 17)

### الدالة المكررة 126:
**التوقيع:** create_all_def create_all(): pass
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 39)
- ./backend/src/routes/excel_operations.py (السطر 146)
- ./backend/src/routes/export.py (السطر 91)
- ./backend/src/routes/financial_reports.py (السطر 25)
- ./backend/src/routes/partners.py (السطر 66)
- ./backend/src/routes/payment_management.py (السطر 25)
- ./backend/src/routes/permissions.py (السطر 17)
- ./backend/src/routes/profit_loss_system.py (السطر 19)
- ./backend/src/routes/region_warehouse.py (السطر 54)
- ./backend/src/routes/sales_advanced.py (السطر 28)
- ./backend/src/routes/settings.py (السطر 33)
- ./backend/src/routes/treasury_management.py (السطر 28)
- ./backend/src/routes/user.py (السطر 27)
- ./backend/src/routes/reports.py (السطر 39)

### الدالة المكررة 127:
**التوقيع:** drop_all_def drop_all(): pass
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 41)
- ./backend/src/routes/excel_operations.py (السطر 148)
- ./backend/src/routes/export.py (السطر 93)
- ./backend/src/routes/financial_reports.py (السطر 27)
- ./backend/src/routes/partners.py (السطر 68)
- ./backend/src/routes/payment_management.py (السطر 27)
- ./backend/src/routes/permissions.py (السطر 19)
- ./backend/src/routes/profit_loss_system.py (السطر 21)
- ./backend/src/routes/region_warehouse.py (السطر 56)
- ./backend/src/routes/sales_advanced.py (السطر 30)
- ./backend/src/routes/settings.py (السطر 35)
- ./backend/src/routes/treasury_management.py (السطر 30)
- ./backend/src/routes/user.py (السطر 29)
- ./backend/src/routes/reports.py (السطر 41)

### الدالة المكررة 128:
**التوقيع:** decorator_def decorator(f): return f
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 88)
- ./backend/src/routes/export.py (السطر 70)
- ./backend/src/routes/payment_debt_management.py (السطر 111)
- ./backend/src/routes/payment_debt_management.py (السطر 115)
- ./backend/src/routes/payment_debt_management.py (السطر 102)
- ./backend/src/routes/permissions.py (السطر 29)
- ./backend/src/routes/profit_loss_system.py (السطر 34)
- ./backend/src/routes/region_warehouse.py (السطر 66)
- ./backend/src/routes/sales_advanced.py (السطر 40)
- ./backend/src/routes/settings.py (السطر 18)

### الدالة المكررة 129:
**التوقيع:** authenticate_def authenticate(username, password): return True
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 96)
- ./backend/src/routes/export.py (السطر 78)
- ./backend/src/routes/payment_debt_management.py (السطر 123)
- ./backend/src/routes/permissions.py (السطر 37)
- ./backend/src/routes/profit_loss_system.py (السطر 40)
- ./backend/src/routes/region_warehouse.py (السطر 74)
- ./backend/src/routes/sales_advanced.py (السطر 48)
- ./backend/src/routes/settings.py (السطر 24)
- ./backend/src/routes/warehouse_transfer.py (السطر 53)

### الدالة المكررة 130:
**التوقيع:** start_scheduler_"""بدء مجدول المهام""" | try:
**المواقع:**
- ./backend/src/routes/automation.py (السطر 290)
- ./backend/src/services/automation_service.py (السطر 129)

### الدالة المكررة 131:
**التوقيع:** stop_scheduler_"""إيقاف مجدول المهام""" | try:
**المواقع:**
- ./backend/src/routes/automation.py (السطر 317)
- ./backend/src/services/automation_service.py (السطر 144)

### الدالة المكررة 132:
**التوقيع:** __init___self.name = name
**المواقع:**
- ./backend/src/routes/batch_management.py (السطر 14)
- ./backend/src/routes/batch_reports.py (السطر 14)

### الدالة المكررة 133:
**التوقيع:** allowed_file_"""Check if file extension is allowed""" | return '.' in filename and \
**المواقع:**
- ./backend/src/routes/company_settings.py (السطر 53)
- ./backend/src/routes/import_export_advanced.py (السطر 58)

### الدالة المكررة 134:
**التوقيع:** login_required_return f
**المواقع:**
- ./backend/src/routes/company_settings.py (السطر 29)
- ./backend/src/routes/excel_operations.py (السطر 155)
- ./backend/src/routes/financial_reports_advanced.py (السطر 18)
- ./backend/src/routes/import_export_advanced.py (السطر 18)

### الدالة المكررة 135:
**التوقيع:** __init___self.id = 1 | self.is_authenticated = True
**المواقع:**
- ./backend/src/routes/company_settings.py (السطر 33)
- ./backend/src/routes/financial_reports_advanced.py (السطر 22)
- ./backend/src/routes/import_export_advanced.py (السطر 22)

### الدالة المكررة 136:
**التوقيع:** require_permission_def decorator(f): | return decorator
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 59)
- ./backend/src/routes/security_system.py (السطر 54)

### الدالة المكررة 137:
**التوقيع:** sum_return 0
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 42)
- ./backend/src/routes/lot_management.py (السطر 46)

### الدالة المكررة 138:
**التوقيع:** upload_excel_"""رفع ملف Excel""" | try:
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 111)
- ./backend/src/routes/excel_import_clean.py (السطر 87)

### الدالة المكررة 139:
**التوقيع:** preview_excel_"""معاينة محتوى ملف Excel""" | try:
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 166)
- ./backend/src/routes/excel_import_clean.py (السطر 140)

### الدالة المكررة 140:
**التوقيع:** import_products_"""استيراد المنتجات من Excel""" | try:
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 205)
- ./backend/src/routes/excel_import_clean.py (السطر 179)

### الدالة المكررة 141:
**التوقيع:** export_products_"""تصدير المنتجات إلى Excel""" | try:
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 269)
- ./backend/src/routes/excel_import_clean.py (السطر 242)

### الدالة المكررة 142:
**التوقيع:** get_templates_"""الحصول على قوالب Excel""" | try:
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 320)
- ./backend/src/routes/excel_import_clean.py (السطر 292)

### الدالة المكررة 143:
**التوقيع:** iterrows_return enumerate(self.data)
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 45)
- ./backend/src/routes/import_data.py (السطر 31)

### الدالة المكررة 144:
**التوقيع:** to_dict_return self.data
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 48)
- ./backend/src/routes/import_data.py (السطر 34)

### الدالة المكررة 145:
**التوقيع:** to_excel_"""Mock to_excel method""" | pass
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 51)
- ./backend/src/routes/import_data.py (السطر 37)

### الدالة المكررة 146:
**التوقيع:** read_excel_raise ImportError("pandas is not installed")
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 59)
- ./backend/src/routes/import_data.py (السطر 49)

### الدالة المكررة 147:
**التوقيع:** has_permission_def decorator(f): | return decorator
**المواقع:**
- ./backend/src/routes/excel_operations.py (السطر 158)
- ./backend/src/routes/warehouse_transfer.py (السطر 45)

### الدالة المكررة 148:
**التوقيع:** add_"""Mock add method""" | pass
**المواقع:**
- ./backend/src/routes/import_data.py (السطر 98)
- ./backend/src/routes/inventory.py (السطر 58)
- ./backend/src/routes/accounting_system.py (السطر 30)

### الدالة المكررة 149:
**التوقيع:** commit_"""Mock commit method""" | pass
**المواقع:**
- ./backend/src/routes/import_data.py (السطر 102)
- ./backend/src/routes/inventory.py (السطر 62)
- ./backend/src/routes/accounting_system.py (السطر 34)

### الدالة المكررة 150:
**التوقيع:** rollback_"""Mock rollback method""" | pass
**المواقع:**
- ./backend/src/routes/import_data.py (السطر 106)
- ./backend/src/routes/inventory.py (السطر 66)
- ./backend/src/routes/accounting_system.py (السطر 38)

### الدالة المكررة 151:
**التوقيع:** create_all_"""Mock create_all method""" | pass
**المواقع:**
- ./backend/src/routes/import_data.py (السطر 118)
- ./backend/src/routes/inventory.py (السطر 74)
- ./backend/src/routes/accounting_system.py (السطر 46)

### الدالة المكررة 152:
**التوقيع:** drop_all_"""Mock drop_all method""" | pass
**المواقع:**
- ./backend/src/routes/import_data.py (السطر 123)
- ./backend/src/routes/inventory.py (السطر 79)
- ./backend/src/routes/accounting_system.py (السطر 51)

### الدالة المكررة 153:
**التوقيع:** get_widget_data_""" | try:
**المواقع:**
- ./backend/src/routes/interactive_dashboard.py (السطر 70)
- ./backend/src/services/interactive_dashboard_service.py (السطر 595)

### الدالة المكررة 154:
**التوقيع:** create_custom_dashboard_""" | try:
**المواقع:**
- ./backend/src/routes/interactive_dashboard.py (السطر 103)
- ./backend/src/services/interactive_dashboard_service.py (السطر 542)

### الدالة المكررة 155:
**التوقيع:** create_warehouse_"""إنشاء مخزن جديد""" | try:
**المواقع:**
- ./backend/src/routes/inventory.py (السطر 485)
- ./backend/src/routes/region_warehouse.py (السطر 311)

### الدالة المكررة 156:
**التوقيع:** create_product_advanced_"""إنشاء منتج متقدم جديد""" | try:
**المواقع:**
- ./backend/src/routes/inventory_advanced.py (السطر 87)
- ./backend/src/routes/products_advanced.py (السطر 175)

### الدالة المكررة 157:
**التوقيع:** get_expiring_batches_"""الحصول على اللوط قريبة الانتهاء""" | try:
**المواقع:**
- ./backend/src/routes/inventory_advanced.py (السطر 203)
- ./backend/src/services/inventory_service_advanced.py (السطر 234)

### الدالة المكررة 158:
**التوقيع:** get_stock_valuation_report_"""تقرير تقييم المخزون""" | try:
**المواقع:**
- ./backend/src/routes/inventory_advanced.py (السطر 339)
- ./backend/src/services/inventory_service_advanced.py (السطر 268)

### الدالة المكررة 159:
**التوقيع:** get_low_stock_report_"""تقرير المنتجات منخفضة المخزون""" | try:
**المواقع:**
- ./backend/src/routes/inventory_advanced.py (السطر 389)
- ./backend/src/services/inventory_service_advanced.py (السطر 306)

### الدالة المكررة 160:
**التوقيع:** get_suppliers_"""الحصول على قائمة الموردين""" | try:
**المواقع:**
- ./backend/src/routes/suppliers.py (السطر 14)
- ./backend/src/routes/returns_management.py (السطر 604)

### الدالة المكررة 161:
**التوقيع:** get_supplier_"""الحصول على مورد محدد""" | try:
**المواقع:**
- ./backend/src/routes/suppliers.py (السطر 106)
- ./backend/src/routes/partners.py (السطر 144)

### الدالة المكررة 162:
**التوقيع:** create_supplier_"""إنشاء مورد جديد""" | try:
**المواقع:**
- ./backend/src/routes/suppliers.py (السطر 149)
- ./backend/src/routes/partners.py (السطر 106)

### الدالة المكررة 163:
**التوقيع:** create_lot_"""إنشاء لوط جديد""" | try:
**المواقع:**
- ./backend/src/routes/lot_management.py (السطر 162)
- ./backend/src/services/inventory_service_advanced.py (السطر 159)

### الدالة المكررة 164:
**التوقيع:** create_stock_movement_"""إنشاء حركة مخزون جديدة""" | try:
**المواقع:**
- ./backend/src/routes/partners.py (السطر 384)
- ./backend/src/services/inventory_service_advanced.py (السطر 66)

### الدالة المكررة 165:
**التوقيع:** require_permission_def decorator(f): return f | return decorator
**المواقع:**
- ./backend/src/routes/payment_debt_management.py (السطر 114)
- ./backend/src/routes/payment_debt_management.py (السطر 101)

### الدالة المكررة 166:
**التوقيع:** get_products_"""الحصول على قائمة المنتجات""" | try:
**المواقع:**
- ./backend/src/routes/products.py (السطر 14)
- ./backend/src/routes/returns_management.py (السطر 620)
- ./backend/src/routes/warehouse_adjustments.py (السطر 475)

### الدالة المكررة 167:
**التوقيع:** get_overdue_summary_"""ملخص المتأخرات""" | try:
**المواقع:**
- ./backend/src/routes/profit_loss_system.py (السطر 385)
- ./backend/src/routes/accounting_system.py (السطر 629)

### الدالة المكررة 168:
**التوقيع:** get_warehouses_"""الحصول على قائمة المخازن""" | try:
**المواقع:**
- ./backend/src/routes/region_warehouse.py (السطر 255)
- ./backend/src/routes/warehouse_adjustments.py (السطر 459)

### الدالة المكررة 169:
**التوقيع:** logout_"""تسجيل الخروج""" | try:
**المواقع:**
- ./backend/src/routes/security_system.py (السطر 151)
- ./backend/src/routes/user.py (السطر 283)
- ./backend/src/routes/auth_routes.py (السطر 172)

### الدالة المكررة 170:
**التوقيع:** register_"""تسجيل مستخدم جديد""" | try:
**المواقع:**
- ./backend/src/routes/security_system.py (السطر 169)
- ./backend/src/routes/auth_routes.py (السطر 216)

### الدالة المكررة 171:
**التوقيع:** change_password_"""تغيير كلمة المرور""" | try:
**المواقع:**
- ./backend/src/routes/security_system.py (السطر 218)
- ./backend/src/routes/user.py (السطر 404)

### الدالة المكررة 172:
**التوقيع:** get_inventory_settings_"""الحصول على إعدادات المخزون""" | try:
**المواقع:**
- ./backend/src/routes/settings.py (السطر 46)
- ./backend/src/services/settings_service.py (السطر 21)

### الدالة المكررة 173:
**التوقيع:** update_inventory_settings_"""تحديث إعدادات المخزون""" | try:
**المواقع:**
- ./backend/src/routes/settings.py (السطر 70)
- ./backend/src/services/settings_service.py (السطر 56)

### الدالة المكررة 174:
**التوقيع:** bad_request_"""معالجة خطأ 400""" | return jsonify({
**المواقع:**
- ./backend/src/routes/system_settings_advanced.py (السطر 582)
- ./backend/src/routes/user_management_advanced.py (السطر 583)

### الدالة المكررة 175:
**التوقيع:** unauthorized_"""معالجة خطأ 401""" | return jsonify({
**المواقع:**
- ./backend/src/routes/system_settings_advanced.py (السطر 591)
- ./backend/src/routes/user_management_advanced.py (السطر 592)

### الدالة المكررة 176:
**التوقيع:** forbidden_"""معالجة خطأ 403""" | return jsonify({
**المواقع:**
- ./backend/src/routes/system_settings_advanced.py (السطر 600)
- ./backend/src/routes/user_management_advanced.py (السطر 601)

### الدالة المكررة 177:
**التوقيع:** not_found_"""معالجة خطأ 404""" | return jsonify({
**المواقع:**
- ./backend/src/routes/system_settings_advanced.py (السطر 609)
- ./backend/src/routes/user_management_advanced.py (السطر 610)

### الدالة المكررة 178:
**التوقيع:** internal_error_"""معالجة خطأ 500""" | return jsonify({
**المواقع:**
- ./backend/src/routes/system_settings_advanced.py (السطر 618)
- ./backend/src/routes/user_management_advanced.py (السطر 619)

### الدالة المكررة 179:
**التوقيع:** create_treasury_"""إنشاء خزنة جديدة""" | try:
**المواقع:**
- ./backend/src/routes/treasury_management.py (السطر 57)
- ./backend/src/services/opening_balances_treasury_service.py (السطر 402)

### الدالة المكررة 180:
**التوقيع:** delete_user_"""حذف مستخدم""" | try:
**المواقع:**
- ./backend/src/routes/user.py (السطر 685)
- ./backend/src/routes/user_management_advanced.py (السطر 161)

### الدالة المكررة 181:
**التوقيع:** __init___self.db = db_session
**المواقع:**
- ./backend/src/services/customer_supplier_accounts_service.py (السطر 42)
- ./backend/src/services/inventory_service_advanced.py (السطر 16)
- ./backend/src/services/opening_balances_treasury_service.py (السطر 38)
- ./backend/src/services/warehouse_constraints_service.py (السطر 30)

### الدالة المكررة 182:
**التوقيع:** __init___"""تهيئة الخدمة""" | self.logger = logger
**المواقع:**
- ./backend/src/services/interactive_dashboard_service.py (السطر 37)
- ./backend/src/services/user_management_advanced_service.py (السطر 40)

## 📦 الفئات المكررة

### الفئة المكررة 1:
**التوقيع:** Role_
**المواقع:**
- ./backend/create_admin_direct.py (السطر 43)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_direct.py (السطر 43)

### الفئة المكررة 2:
**التوقيع:** User_set_password,check_password
**المواقع:**
- ./backend/create_admin_direct.py (السطر 55)
- ./backend/init_db.py (السطر 43)
- ./backend/database_archive/quick_fix_backup_20251004_094710/create_admin_direct.py (السطر 55)

### الفئة المكررة 3:
**التوقيع:** Category_
**المواقع:**
- ./backend/init_db.py (السطر 64)
- ./backend/src/unified_server.py (السطر 105)
- ./backend/src/unified_server_clean.py (السطر 88)
- ./backend/src/routes/dashboard.py (السطر 91)
- ./backend/src/services/automation_service.py (السطر 71)

### الفئة المكررة 4:
**التوقيع:** Product_
**المواقع:**
- ./backend/init_db.py (السطر 73)
- ./backend/src/unified_server.py (السطر 102)
- ./backend/src/unified_server_clean.py (السطر 85)
- ./backend/src/routes/dashboard.py (السطر 88)
- ./backend/src/routes/lot_management.py (السطر 83)
- ./backend/src/services/automation_service.py (السطر 68)

### الفئة المكررة 5:
**التوقيع:** Permissions_
**المواقع:**
- ./backend/src/auth.py (السطر 376)
- ./backend/src/routes/admin_panel.py (السطر 91)
- ./backend/src/routes/dashboard.py (السطر 64)
- ./backend/src/routes/excel_operations.py (السطر 163)
- ./backend/src/routes/export.py (السطر 73)
- ./backend/src/routes/payment_debt_management.py (السطر 118)
- ./backend/src/routes/permissions.py (السطر 32)
- ./backend/src/routes/profit_loss_system.py (السطر 36)
- ./backend/src/routes/region_warehouse.py (السطر 69)
- ./backend/src/routes/sales_advanced.py (السطر 43)
- ./backend/src/routes/security_system.py (السطر 59)
- ./backend/src/routes/settings.py (السطر 20)
- ./backend/src/routes/user.py (السطر 84)
- ./backend/src/routes/warehouse_transfer.py (السطر 49)

### الفئة المكررة 6:
**التوقيع:** request_
**المواقع:**
- ./backend/src/unified_server.py (السطر 63)
- ./backend/src/unified_server_clean.py (السطر 47)
- ./backend/src/routes/dashboard.py (السطر 29)
- ./backend/src/routes/excel_import.py (السطر 27)
- ./backend/src/routes/excel_import_clean.py (السطر 26)
- ./backend/src/routes/lot_management.py (السطر 29)
- ./backend/src/routes/security_system.py (السطر 26)

### الفئة المكررة 7:
**التوقيع:** MockDB_init_app,create_all,engine
**المواقع:**
- ./backend/src/unified_server.py (السطر 86)
- ./backend/src/unified_server_clean.py (السطر 69)

### الفئة المكررة 8:
**التوقيع:** User_
**المواقع:**
- ./backend/src/unified_server.py (السطر 99)
- ./backend/src/unified_server_clean.py (السطر 82)
- ./backend/src/routes/dashboard.py (السطر 109)
- ./backend/src/routes/lot_management.py (السطر 98)
- ./backend/src/services/automation_service.py (السطر 102)

### الفئة المكررة 9:
**التوقيع:** MockDB_Column,Integer,String,Text,DateTime
**المواقع:**
- ./backend/src/database_backup.py (السطر 108)
- ./backend/database_archive/database_old/__init__.py (السطر 16)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 106)

### الفئة المكررة 10:
**التوقيع:** MockQuery_filter,filter_by,first,all,count
**المواقع:**
- ./backend/src/database_backup.py (السطر 173)
- ./backend/database_archive/database_old/__init__.py (السطر 83)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 171)

### الفئة المكررة 11:
**التوقيع:** Model___init__,to_dict,query
**المواقع:**
- ./backend/src/database_backup.py (السطر 109)
- ./backend/src/models/inventory.py (السطر 98)
- ./backend/database_archive/database_old/__init__.py (السطر 17)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 107)

### الفئة المكررة 12:
**التوقيع:** MockPagination_
**المواقع:**
- ./backend/src/database_backup.py (السطر 196)
- ./backend/database_archive/quick_fix_backup_20251004_094710/database.py (السطر 194)

### الفئة المكررة 13:
**التوقيع:** BasicModel_to_dict
**المواقع:**
- ./backend/src/models/accounting_system.py (السطر 101)
- ./backend/src/models/invoices_clean.py (السطر 93)
- ./backend/src/models/payment_management.py (السطر 523)
- ./backend/src/models/permissions.py (السطر 80)
- ./backend/src/models/pickup_delivery_orders.py (السطر 83)
- ./backend/src/models/profit_loss_system.py (السطر 83)
- ./backend/src/models/region_warehouse.py (السطر 80)
- ./backend/src/models/returns_management.py (السطر 80)
- ./backend/src/models/sales_advanced.py (السطر 110)
- ./backend/src/models/security_system.py (السطر 83)
- ./backend/src/models/stock_movement_advanced.py (السطر 83)
- ./backend/src/models/system_settings_advanced.py (السطر 83)
- ./backend/src/models/treasury_management.py (السطر 368)
- ./backend/src/models/unified_models.py (السطر 140)
- ./backend/src/models/user_management_advanced.py (السطر 83)
- ./backend/src/models/warehouse_adjustments.py (السطر 96)
- ./backend/src/models/warehouse_advanced.py (السطر 83)
- ./backend/src/models/warehouse_constraints.py (السطر 96)
- ./backend/src/models/warehouse_transfer.py (السطر 211)
- ./backend/src/models/partners.py (السطر 98)

### الفئة المكررة 14:
**التوقيع:** MockDB_
**المواقع:**
- ./backend/src/models/accounting_system.py (السطر 77)
- ./backend/src/models/invoices.py (السطر 57)
- ./backend/src/models/invoices_clean.py (السطر 67)
- ./backend/src/models/payment_management.py (السطر 57)
- ./backend/src/models/permissions.py (السطر 57)
- ./backend/src/models/pickup_delivery_orders.py (السطر 60)
- ./backend/src/models/profit_loss_system.py (السطر 60)
- ./backend/src/models/region_warehouse.py (السطر 57)
- ./backend/src/models/returns_management.py (السطر 57)
- ./backend/src/models/sales_advanced.py (السطر 62)
- ./backend/src/models/security_system.py (السطر 60)
- ./backend/src/models/stock_movement_advanced.py (السطر 60)
- ./backend/src/models/system_settings_advanced.py (السطر 60)
- ./backend/src/models/treasury_management.py (السطر 60)
- ./backend/src/models/unified_models.py (السطر 72)
- ./backend/src/models/user_management_advanced.py (السطر 60)
- ./backend/src/models/warehouse_adjustments.py (السطر 72)
- ./backend/src/models/warehouse_advanced.py (السطر 60)
- ./backend/src/models/warehouse_constraints.py (السطر 72)
- ./backend/src/models/partners.py (السطر 57)
- ./backend/src/models/unified_invoice.py (السطر 42)
- ./backend/src/services/automation_service.py (السطر 108)

### الفئة المكررة 15:
**التوقيع:** Model___init__,to_dict
**المواقع:**
- ./backend/src/models/accounting_system.py (السطر 78)
- ./backend/src/models/invoices.py (السطر 58)
- ./backend/src/models/invoices_clean.py (السطر 68)
- ./backend/src/models/lot_advanced.py (السطر 24)
- ./backend/src/models/payment_management.py (السطر 58)
- ./backend/src/models/permissions.py (السطر 58)
- ./backend/src/models/pickup_delivery_orders.py (السطر 61)
- ./backend/src/models/profit_loss_system.py (السطر 61)
- ./backend/src/models/region_warehouse.py (السطر 58)
- ./backend/src/models/returns_management.py (السطر 58)
- ./backend/src/models/sales_advanced.py (السطر 63)
- ./backend/src/models/security_system.py (السطر 61)
- ./backend/src/models/stock_movement_advanced.py (السطر 61)
- ./backend/src/models/system_settings_advanced.py (السطر 61)
- ./backend/src/models/treasury_management.py (السطر 61)
- ./backend/src/models/unified_models.py (السطر 73)
- ./backend/src/models/user_management_advanced.py (السطر 61)
- ./backend/src/models/warehouse_adjustments.py (السطر 73)
- ./backend/src/models/warehouse_advanced.py (السطر 61)
- ./backend/src/models/warehouse_constraints.py (السطر 73)
- ./backend/src/models/partners.py (السطر 58)

### الفئة المكررة 16:
**التوقيع:** MockQuery_filter_by,filter,all,first,count
**المواقع:**
- ./backend/src/models/inventory.py (السطر 69)
- ./backend/src/routes/excel_operations.py (السطر 33)

### الفئة المكررة 17:
**التوقيع:** MockDB_create_all,drop_all
**المواقع:**
- ./backend/src/models/inventory.py (السطر 97)
- ./backend/src/routes/admin.py (السطر 22)
- ./backend/src/routes/admin_panel.py (السطر 36)
- ./backend/src/routes/excel_operations.py (السطر 143)
- ./backend/src/routes/export.py (السطر 88)
- ./backend/src/routes/financial_reports.py (السطر 22)
- ./backend/src/routes/import_data.py (السطر 114)
- ./backend/src/routes/partners.py (السطر 51)
- ./backend/src/routes/payment_management.py (السطر 22)
- ./backend/src/routes/permissions.py (السطر 14)
- ./backend/src/routes/profit_loss_system.py (السطر 16)
- ./backend/src/routes/region_warehouse.py (السطر 51)
- ./backend/src/routes/sales_advanced.py (السطر 25)
- ./backend/src/routes/settings.py (السطر 30)
- ./backend/src/routes/treasury_management.py (السطر 25)
- ./backend/src/routes/user.py (السطر 24)
- ./backend/src/routes/warehouse_transfer.py (السطر 30)
- ./backend/src/routes/accounting_system.py (السطر 42)
- ./backend/src/routes/reports.py (السطر 36)

### الفئة المكررة 18:
**التوقيع:** ExchangeRate_to_dict
**المواقع:**
- ./backend/src/models/invoices.py (السطر 226)
- ./backend/src/models/partners.py (السطر 166)

### الفئة المكررة 19:
**التوقيع:** TransactionType_
**المواقع:**
- ./backend/src/models/opening_balances_treasury.py (السطر 81)
- ./backend/src/models/treasury_management.py (السطر 91)

### الفئة المكررة 20:
**التوقيع:** Base_
**المواقع:**
- ./backend/src/models/opening_balances_treasury.py (السطر 60)
- ./backend/src/models/product_advanced.py (السطر 58)

### الفئة المكررة 21:
**التوقيع:** PaymentStatus_
**المواقع:**
- ./backend/src/models/payment_management.py (السطر 80)
- ./backend/src/models/sales_advanced.py (السطر 90)
- ./backend/src/models/partners.py (السطر 88)

### الفئة المكررة 22:
**التوقيع:** PaymentMethod_
**المواقع:**
- ./backend/src/models/payment_management.py (السطر 98)
- ./backend/src/models/unified_invoice.py (السطر 69)

### الفئة المكررة 23:
**التوقيع:** InvoiceType_
**المواقع:**
- ./backend/src/models/sales_advanced.py (السطر 103)
- ./backend/src/models/unified_invoice.py (السطر 48)

### الفئة المكررة 24:
**التوقيع:** SalesEngineerStatus_
**المواقع:**
- ./backend/src/models/sales_advanced.py (السطر 97)
- ./backend/src/models/partners.py (السطر 82)

### الفئة المكررة 25:
**التوقيع:** UserRole_
**المواقع:**
- ./backend/src/models/unified_models.py (السطر 95)
- ./backend/src/models/__init__.py (السطر 66)

### الفئة المكررة 26:
**التوقيع:** CustomerType_
**المواقع:**
- ./backend/src/models/unified_models.py (السطر 101)
- ./backend/src/models/partners.py (السطر 160)
- ./backend/src/routes/partners.py (السطر 35)

### الفئة المكررة 27:
**التوقيع:** ProductType_
**المواقع:**
- ./backend/src/models/unified_models.py (السطر 106)
- ./backend/src/models/__init__.py (السطر 71)

### الفئة المكررة 28:
**التوقيع:** MovementType_
**المواقع:**
- ./backend/src/models/unified_models.py (السطر 111)
- ./backend/src/models/__init__.py (السطر 76)

### الفئة المكررة 29:
**التوقيع:** InvoiceStatus_
**المواقع:**
- ./backend/src/models/unified_models.py (السطر 116)
- ./backend/src/models/unified_invoice.py (السطر 58)

### الفئة المكررة 30:
**التوقيع:** Model_
**المواقع:**
- ./backend/src/models/__init__.py (السطر 12)
- ./backend/src/models/unified_invoice.py (السطر 43)
- ./backend/src/services/automation_service.py (السطر 109)

### الفئة المكررة 31:
**التوقيع:** MockSession_add,commit,rollback,delete
**المواقع:**
- ./backend/src/routes/admin.py (السطر 35)
- ./backend/src/routes/excel_operations.py (السطر 137)

### الفئة المكررة 32:
**التوقيع:** User___init__,query
**المواقع:**
- ./backend/src/routes/admin.py (السطر 69)
- ./backend/src/routes/admin_panel.py (السطر 45)

### الفئة المكررة 33:
**التوقيع:** AuthManager_authenticate
**المواقع:**
- ./backend/src/routes/admin_panel.py (السطر 94)
- ./backend/src/routes/excel_operations.py (السطر 166)
- ./backend/src/routes/export.py (السطر 76)
- ./backend/src/routes/payment_debt_management.py (السطر 121)
- ./backend/src/routes/permissions.py (السطر 35)
- ./backend/src/routes/profit_loss_system.py (السطر 38)
- ./backend/src/routes/region_warehouse.py (السطر 72)
- ./backend/src/routes/sales_advanced.py (السطر 46)
- ./backend/src/routes/settings.py (السطر 22)
- ./backend/src/routes/warehouse_transfer.py (السطر 51)

### الفئة المكررة 34:
**التوقيع:** MockBlueprint___init__,route
**المواقع:**
- ./backend/src/routes/batch_management.py (السطر 13)
- ./backend/src/routes/batch_reports.py (السطر 13)

### الفئة المكررة 35:
**التوقيع:** DummyUser___init__
**المواقع:**
- ./backend/src/routes/company_settings.py (السطر 22)
- ./backend/src/routes/company_settings.py (السطر 32)
- ./backend/src/routes/financial_reports_advanced.py (السطر 21)
- ./backend/src/routes/import_export_advanced.py (السطر 21)

### الفئة المكررة 36:
**التوقيع:** Blueprint___init__,route
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 17)
- ./backend/src/routes/excel_import.py (السطر 15)
- ./backend/src/routes/excel_import_clean.py (السطر 14)
- ./backend/src/routes/lot_management.py (السطر 17)
- ./backend/src/routes/security_system.py (السطر 14)

### الفئة المكررة 37:
**التوقيع:** func_count,sum
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 36)
- ./backend/src/routes/lot_management.py (السطر 40)

### الفئة المكررة 38:
**التوقيع:** AuthManager_get_current_user
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 68)
- ./backend/src/routes/security_system.py (السطر 63)

### الفئة المكررة 39:
**التوقيع:** Supplier_
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 94)
- ./backend/src/routes/lot_management.py (السطر 92)
- ./backend/src/routes/partners.py (السطر 29)
- ./backend/src/services/automation_service.py (السطر 86)

### الفئة المكررة 40:
**التوقيع:** Customer_
**المواقع:**
- ./backend/src/routes/dashboard.py (السطر 97)
- ./backend/src/routes/partners.py (السطر 26)
- ./backend/src/services/automation_service.py (السطر 84)

### الفئة المكررة 41:
**التوقيع:** MockPandas_read_excel
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 55)
- ./backend/src/routes/import_data.py (السطر 45)

### الفئة المكررة 42:
**التوقيع:** MockDB_add,commit,rollback
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 70)
- ./backend/src/routes/excel_import_clean.py (السطر 46)
- ./backend/src/routes/lot_management.py (السطر 59)

### الفئة المكررة 43:
**التوقيع:** Product___init__
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 87)
- ./backend/src/routes/excel_import_clean.py (السطر 63)
- ./backend/src/routes/import_data.py (السطر 68)
- ./backend/src/routes/inventory.py (السطر 28)

### الفئة المكررة 44:
**التوقيع:** Category___init__
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 92)
- ./backend/src/routes/excel_import_clean.py (السطر 68)
- ./backend/src/routes/import_data.py (السطر 58)
- ./backend/src/routes/inventory.py (السطر 23)

### الفئة المكررة 45:
**التوقيع:** Supplier___init__
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 97)
- ./backend/src/routes/excel_import_clean.py (السطر 73)
- ./backend/src/routes/import_data.py (السطر 88)

### الفئة المكررة 46:
**التوقيع:** Customer___init__
**المواقع:**
- ./backend/src/routes/excel_import.py (السطر 102)
- ./backend/src/routes/excel_import_clean.py (السطر 78)
- ./backend/src/routes/import_data.py (السطر 83)

### الفئة المكررة 47:
**التوقيع:** Warehouse___init__
**المواقع:**
- ./backend/src/routes/import_data.py (السطر 73)
- ./backend/src/routes/inventory.py (السطر 43)

### الفئة المكررة 48:
**التوقيع:** MockSession_add,commit,rollback
**المواقع:**
- ./backend/src/routes/inventory.py (السطر 57)
- ./backend/src/routes/accounting_system.py (السطر 29)

## 📦 الملفات المنقولة إلى repeat_code
- **الأصلي:** ./backend/src/__init__.py
  **المنقول:** repeat_code/repeat_code/backend/src/routes/__init__.py
  **المصدر:** ./repeat_code/backend/src/routes/__init__.py

- **الأصلي:** ./backend/src/decorators/__init__.py
  **المنقول:** repeat_code/repeat_code/backend/src/middleware/__init__.py
  **المصدر:** ./repeat_code/backend/src/middleware/__init__.py


## 📊 الإحصائيات
- **الملفات المتطابقة:** 2 مجموعة
- **الدوال المكررة:** 182 دالة
- **الفئات المكررة:** 48 فئة
- **الملفات المنقولة:** 2 ملف