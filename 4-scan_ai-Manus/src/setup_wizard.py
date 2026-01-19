"""
صفحة الإعدادات الأولية لنظام Gaara Scan AI
Initial Setup Page for Gaara Scan AI System
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import hashlib
import secrets
from datetime import datetime
import subprocess
import psycopg2
import redis
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# مسارات الملفات
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config', 'system_setup.json')
ENV_FILE = os.path.join(PROJECT_ROOT, '.env')

class SetupWizard:
    def __init__(self):
        self.setup_config = self.load_setup_config()
        
    def load_setup_config(self):
        """تحميل تكوين الإعداد"""
        try:
            with open(SETUP_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_default_config()
    
    def save_setup_config(self):
        """حفظ تكوين الإعداد"""
        with open(SETUP_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.setup_config, f, indent=2, ensure_ascii=False)
    
    def create_default_config(self):
        """إنشاء تكوين افتراضي"""
        return {
            "setup_completed": False,
            "setup_timestamp": None,
            "admin_configured": False,
            "database_initialized": False,
            "services_configured": False,
            "first_run": True,
            "setup_wizard_enabled": True,
            "default_language": "ar",
            "timezone": "Asia/Riyadh",
            "setup_steps": {
                "welcome": False,
                "admin_account": False,
                "database_config": False,
                "services_config": False,
                "security_config": False,
                "completion": False
            }
        }
    
    def is_setup_completed(self):
        """فحص ما إذا كان الإعداد مكتملاً"""
        return self.setup_config.get('setup_completed', False)
    
    def mark_step_completed(self, step_name):
        """تحديد خطوة كمكتملة"""
        self.setup_config['setup_steps'][step_name] = True
        self.save_setup_config()
    
    def get_next_step(self):
        """الحصول على الخطوة التالية"""
        steps = ['welcome', 'admin_account', 'database_config', 'services_config', 'security_config', 'completion']
        for step in steps:
            if not self.setup_config['setup_steps'].get(step, False):
                return step
        return 'completion'
    
    def complete_setup(self):
        """إكمال الإعداد"""
        self.setup_config['setup_completed'] = True
        self.setup_config['setup_timestamp'] = datetime.now().isoformat()
        self.setup_config['first_run'] = False
        self.save_setup_config()

# إنشاء مثيل معالج الإعداد
setup_wizard = SetupWizard()

@app.route('/')
def index():
    """الصفحة الرئيسية - توجيه إلى الإعداد إذا لم يكتمل"""
    if not setup_wizard.is_setup_completed():
        return redirect(url_for('setup_welcome'))
    return redirect(url_for('dashboard'))

@app.route('/setup')
def setup_welcome():
    """صفحة الترحيب بالإعداد"""
    if setup_wizard.is_setup_completed():
        return redirect(url_for('dashboard'))
    
    return render_template('setup/welcome.html', 
                         config=setup_wizard.setup_config,
                         current_step='welcome')

@app.route('/setup/admin', methods=['GET', 'POST'])
def setup_admin():
    """إعداد حساب المدير"""
    if request.method == 'POST':
        data = request.get_json()
        
        # التحقق من صحة البيانات
        if not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'message': 'اسم المستخدم وكلمة المرور مطلوبان'})
        
        if len(data['password']) < 8:
            return jsonify({'success': False, 'message': 'كلمة المرور يجب أن تكون 8 أحرف على الأقل'})
        
        # حفظ بيانات المدير
        admin_data = {
            'username': data['username'],
            'email': data.get('email', ''),
            'password_hash': hashlib.sha256(data['password'].encode()).hexdigest(),
            'created_at': datetime.now().isoformat()
        }
        
        # حفظ في ملف مؤقت (سيتم نقلها لقاعدة البيانات لاحقاً)
        admin_file = os.path.join(PROJECT_ROOT, 'config', 'admin_user.json')
        with open(admin_file, 'w', encoding='utf-8') as f:
            json.dump(admin_data, f, indent=2, ensure_ascii=False)
        
        setup_wizard.mark_step_completed('admin_account')
        setup_wizard.setup_config['admin_configured'] = True
        setup_wizard.save_setup_config()
        
        return jsonify({'success': True, 'next_step': 'database_config'})
    
    return render_template('setup/admin.html', 
                         config=setup_wizard.setup_config,
                         current_step='admin_account')

@app.route('/setup/database', methods=['GET', 'POST'])
def setup_database():
    """إعداد قاعدة البيانات"""
    if request.method == 'POST':
        data = request.get_json()
        
        # اختبار الاتصال بقاعدة البيانات
        try:
            conn = psycopg2.connect(
                host=data.get('host', 'localhost'),
                port=data.get('port', 5432),
                database=data.get('database', 'gaara_scan_ai'),
                user=data.get('username', 'gaara_user'),
                password=data.get('password', '')
            )
            conn.close()
            
            # حفظ تكوين قاعدة البيانات
            db_config = {
                'host': data.get('host', 'localhost'),
                'port': data.get('port', 5432),
                'database': data.get('database', 'gaara_scan_ai'),
                'username': data.get('username', 'gaara_user'),
                'connection_tested': True,
                'tested_at': datetime.now().isoformat()
            }
            
            db_config_file = os.path.join(PROJECT_ROOT, 'config', 'database_config.json')
            with open(db_config_file, 'w', encoding='utf-8') as f:
                json.dump(db_config, f, indent=2, ensure_ascii=False)
            
            setup_wizard.mark_step_completed('database_config')
            setup_wizard.setup_config['database_initialized'] = True
            setup_wizard.save_setup_config()
            
            return jsonify({'success': True, 'next_step': 'services_config'})
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'فشل في الاتصال بقاعدة البيانات: {str(e)}'})
    
    return render_template('setup/database.html', 
                         config=setup_wizard.setup_config,
                         current_step='database_config')

@app.route('/setup/services', methods=['GET', 'POST'])
def setup_services():
    """إعداد الخدمات"""
    if request.method == 'POST':
        data = request.get_json()
        
        # فحص حالة الخدمات
        services_status = {}
        services_to_check = {
            'redis': 'http://localhost:6379',
            'elasticsearch': 'http://localhost:9200',
            'rabbitmq': 'http://localhost:15672',
            'yolo_detection': 'http://localhost:8018/health',
            'image_enhancement': 'http://localhost:8019/health',
            'plant_hybridization': 'http://localhost:8022/health'
        }
        
        for service_name, service_url in services_to_check.items():
            try:
                response = requests.get(service_url, timeout=5)
                services_status[service_name] = {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'response_time': response.elapsed.total_seconds()
                }
            except Exception as e:
                services_status[service_name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        # حفظ حالة الخدمات
        services_config = {
            'services_status': services_status,
            'enabled_services': data.get('enabled_services', []),
            'checked_at': datetime.now().isoformat()
        }
        
        services_config_file = os.path.join(PROJECT_ROOT, 'config', 'services_config.json')
        with open(services_config_file, 'w', encoding='utf-8') as f:
            json.dump(services_config, f, indent=2, ensure_ascii=False)
        
        setup_wizard.mark_step_completed('services_config')
        setup_wizard.setup_config['services_configured'] = True
        setup_wizard.save_setup_config()
        
        return jsonify({'success': True, 'services_status': services_status, 'next_step': 'security_config'})
    
    return render_template('setup/services.html', 
                         config=setup_wizard.setup_config,
                         current_step='services_config')

@app.route('/setup/security', methods=['GET', 'POST'])
def setup_security():
    """إعداد الأمان"""
    if request.method == 'POST':
        data = request.get_json()
        
        # إعداد تكوين الأمان
        security_config = {
            'ssl_enabled': data.get('ssl_enabled', False),
            'two_factor_auth': data.get('two_factor_auth', False),
            'session_timeout': data.get('session_timeout', 30),
            'password_policy': {
                'min_length': data.get('password_min_length', 8),
                'require_uppercase': data.get('require_uppercase', True),
                'require_numbers': data.get('require_numbers', True),
                'require_symbols': data.get('require_symbols', False)
            },
            'configured_at': datetime.now().isoformat()
        }
        
        security_config_file = os.path.join(PROJECT_ROOT, 'config', 'security_config.json')
        with open(security_config_file, 'w', encoding='utf-8') as f:
            json.dump(security_config, f, indent=2, ensure_ascii=False)
        
        setup_wizard.mark_step_completed('security_config')
        setup_wizard.save_setup_config()
        
        return jsonify({'success': True, 'next_step': 'completion'})
    
    return render_template('setup/security.html', 
                         config=setup_wizard.setup_config,
                         current_step='security_config')

@app.route('/setup/complete', methods=['GET', 'POST'])
def setup_complete():
    """إكمال الإعداد"""
    if request.method == 'POST':
        # إكمال الإعداد
        setup_wizard.mark_step_completed('completion')
        setup_wizard.complete_setup()
        
        # إنشاء ملف إشارة الإكمال
        completion_file = os.path.join(PROJECT_ROOT, 'config', 'setup_completed.flag')
        with open(completion_file, 'w') as f:
            f.write(datetime.now().isoformat())
        
        return jsonify({'success': True, 'redirect': '/dashboard'})
    
    return render_template('setup/complete.html', 
                         config=setup_wizard.setup_config,
                         current_step='completion')

@app.route('/dashboard')
def dashboard():
    """لوحة التحكم الرئيسية"""
    if not setup_wizard.is_setup_completed():
        return redirect(url_for('setup_welcome'))
    
    return render_template('dashboard.html')

@app.route('/api/setup/status')
def setup_status():
    """حالة الإعداد"""
    return jsonify({
        'setup_completed': setup_wizard.is_setup_completed(),
        'current_step': setup_wizard.get_next_step(),
        'config': setup_wizard.setup_config
    })

@app.route('/api/setup/reset', methods=['POST'])
def reset_setup():
    """إعادة تعيين الإعداد"""
    setup_wizard.setup_config = setup_wizard.create_default_config()
    setup_wizard.save_setup_config()
    
    # حذف ملفات التكوين
    config_files = [
        'admin_user.json',
        'database_config.json',
        'services_config.json',
        'security_config.json',
        'setup_completed.flag'
    ]
    
    for config_file in config_files:
        file_path = os.path.join(PROJECT_ROOT, 'config', config_file)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    return jsonify({'success': True, 'message': 'تم إعادة تعيين الإعداد بنجاح'})

if __name__ == '__main__':
    # إنشاء مجلد التكوين إذا لم يكن موجوداً
    config_dir = os.path.join(PROJECT_ROOT, 'config')
    os.makedirs(config_dir, exist_ok=True)
    
    # تشغيل التطبيق
    app.run(host='0.0.0.0', port=8000, debug=True)

