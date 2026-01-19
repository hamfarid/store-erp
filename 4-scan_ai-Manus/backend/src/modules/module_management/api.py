# File: /home/ubuntu/ai_web_organized/src/modules/module_management/api.py
"""
واجهة برمجة التطبيقات لإدارة المديولات
توفر هذه الوحدة واجهات برمجية للتعامل مع المديولات (تشغيل، إيقاف، إعادة تشغيل، مراقبة الحالة)
"""

import json
import logging
import os
from datetime import datetime

from fastapi import APIRouter, HTTPException
from flask import request

# استيراد وحدة التحكم في المديولات
from .module_controller import (
    get_module_cpu_usage,
    get_module_last_started,
    get_module_last_stopped,
    get_module_ram_usage,
    get_module_status,
    module_exists,
    restart_module,
    start_module,
    stop_module,
)

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# إنشاء مخطط للواجهة البرمجية
router = APIRouter(prefix="/api", tags=["api"])

# مسار ملف البيانات المؤقت (في التطبيق الحقيقي سيتم استخدام قاعدة بيانات)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
MODULES_FILE = os.path.join(DATA_DIR, 'modules.json')
MODULES_LOG_FILE = os.path.join(DATA_DIR, 'modules_log.json')

# مسار المديولات
MODULES_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))

# التأكد من وجود مجلد البيانات
os.makedirs(DATA_DIR, exist_ok=True)

# دالة مساعدة لتحميل البيانات من ملف JSON


def load_data(file_path, default_data=None):
    """Load data from JSON file"""
    if default_data is None:
        default_data = {}

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
        return default_data

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default_data

# دالة مساعدة لحفظ البيانات في ملف JSON


def save_data(file_path, data):
    """Save data to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# دالة لتسجيل عمليات المديول


def log_module_operation(module_name, operation):
    """تسجيل عملية على المديول"""
    try:
        logs = load_data(MODULES_LOG_FILE, {"logs": []})
        logs["logs"].append({
            "module": module_name,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "user": "admin"  # في التطبيق الحقيقي، سيتم استخدام المستخدم الفعلي
        })
        save_data(MODULES_LOG_FILE, logs)
    except Exception as e:
        logger.error(f"Error logging module operation: {str(e)}")

# دالة لاكتشاف المديولات المتاحة


def discover_modules():
    """اكتشاف المديولات المتاحة في النظام"""
    modules = []
    try:
        for item in os.listdir(MODULES_DIR):
            if os.path.isdir(os.path.join(MODULES_DIR, item)
                             ) and not item.startswith('__'):
                module_info = {
                    "id": item,
                    "nameAr": get_module_display_name(item, 'ar'),
                    "nameEn": get_module_display_name(item, 'en'),
                    "status": get_module_status(item),
                    "descriptionAr": get_module_description(item, 'ar'),
                    "descriptionEn": get_module_description(item, 'en'),
                    "version": "1.0.0",
                    "dependencies": get_module_dependencies(item),
                    "cpuUsage": get_module_cpu_usage(item),
                    "ramUsage": get_module_ram_usage(item),
                    "lastStarted": get_module_last_started(item),
                    "lastStopped": get_module_last_stopped(item)
                }
                modules.append(module_info)
    except Exception as e:
        logger.error(f"Error discovering modules: {str(e)}")

    return modules

# دالة للحصول على اسم العرض للمديول


def get_module_display_name(module_name, language):
    """الحصول على اسم العرض للمديول"""
    module_names = {
        "performance_monitoring": {"ar": "مراقبة الأداء", "en": "Performance Monitoring"},
        "data_validation": {"ar": "التحقق من البيانات", "en": "Data Validation"},
        "backup_module": {"ar": "النسخ الاحتياطي", "en": "Backup Module"},
        "module_shutdown": {"ar": "إغلاق المديولات", "en": "Module Shutdown"},
        "ai_management": {"ar": "إدارة الذكاء الصناعي", "en": "AI Management"},
        "disease_diagnosis": {"ar": "تشخيص الأمراض النباتية", "en": "Plant Disease Diagnosis"},
        "image_processing": {"ar": "معالجة الصور", "en": "Image Processing"},
        "plant_hybridization": {"ar": "محاكاة التهجين النباتي", "en": "Plant Hybridization Simulation"},
        "module_management": {"ar": "إدارة المديولات", "en": "Module Management"},
        "resource_monitoring": {"ar": "مراقبة الموارد", "en": "Resource Monitoring"},
        "alert_management": {"ar": "إدارة التنبيهات", "en": "Alert Management"},
        "integration_tests": {"ar": "اختبارات التكامل", "en": "Integration Tests"},
        "ai_usage_reports": {"ar": "تقارير استخدام الذكاء الصناعي", "en": "AI Usage Reports"}
    }

    if module_name in module_names and language in module_names[module_name]:
        return module_names[module_name][language]
    return module_name

# دالة للحصول على وصف المديول


def get_module_description(module_name, language):
    """الحصول على وصف المديول"""
    module_descriptions = {
        "performance_monitoring": {
            "ar": "مراقبة أداء النظام والمديولات واستهلاك الموارد",
            "en": "Monitor system and module performance and resource usage"
        },
        "data_validation": {
            "ar": "التحقق من صحة البيانات المدخلة والمخرجة",
            "en": "Validate input and output data"
        },
        "backup_module": {
            "ar": "إدارة النسخ الاحتياطي واستعادة البيانات",
            "en": "Manage backup and data recovery"
        },
        "module_shutdown": {
            "ar": "إدارة إغلاق المديولات بشكل آمن",
            "en": "Manage safe module shutdown"
        },
        "ai_management": {
            "ar": "إدارة وكلاء الذكاء الصناعي وإحصائياتهم وإعداداتهم وصلاحياتهم",
            "en": "Manage AI agents, statistics, settings, and permissions"
        },
        "disease_diagnosis": {
            "ar": "تشخيص الأمراض النباتية باستخدام الذكاء الصناعي",
            "en": "Diagnose plant diseases using AI"
        },
        "image_processing": {
            "ar": "معالجة الصور الزراعية وتحليلها",
            "en": "Process and analyze agricultural images"
        },
        "plant_hybridization": {
            "ar": "محاكاة عمليات التهجين النباتي والتنبؤ بالصفات الوراثية",
            "en": "Simulate plant hybridization processes and predict genetic traits"
        },
        "module_management": {
            "ar": "إدارة المديولات (تشغيل، إيقاف، إعادة تشغيل، مراقبة الحالة)",
            "en": "Manage modules (start, stop, restart, monitor status)"
        },
        "resource_monitoring": {
            "ar": "مراقبة موارد النظام (المعالج، الذاكرة، القرص، الشبكة)",
            "en": "Monitor system resources (CPU, memory, disk, network)"
        },
        "alert_management": {
            "ar": "إدارة التنبيهات والإشعارات",
            "en": "Manage alerts and notifications"
        },
        "integration_tests": {
            "ar": "اختبارات التكامل بين المديولات المختلفة",
            "en": "Integration tests between different modules"
        },
        "ai_usage_reports": {
            "ar": "إنشاء وعرض تقارير استخدام الذكاء الصناعي",
            "en": "Generate and display AI usage reports"
        }
    }

    if module_name in module_descriptions and language in module_descriptions[module_name]:
        return module_descriptions[module_name][language]
    return ""

# دالة للحصول على اعتماديات المديول


def get_module_dependencies(module_name):
    """الحصول على اعتماديات المديول"""
    module_dependencies = {
        "performance_monitoring": [],
        "data_validation": [],
        "backup_module": [],
        "module_shutdown": ["performance_monitoring"],
        "ai_management": [],
        "disease_diagnosis": ["image_processing"],
        "image_processing": [],
        "plant_hybridization": [],
        "module_management": [],
        "resource_monitoring": [],
        "alert_management": [],
        "integration_tests": [
            "performance_monitoring",
            "data_validation",
            "module_shutdown",
            "ai_management",
            "disease_diagnosis",
            "image_processing",
            "plant_hybridization"],
        "ai_usage_reports": ["ai_management"]}

    if module_name in module_dependencies:
        return module_dependencies[module_name]
    return []

# تهيئة البيانات الافتراضية إذا لم تكن موجودة


def init_default_data():
    """تهيئة البيانات الافتراضية"""
    # اكتشاف المديولات المتاحة
    modules = discover_modules()

    # حفظ البيانات
    save_data(MODULES_FILE, {"modules": modules})

    # تهيئة سجل العمليات إذا لم يكن موجوداً
    if not os.path.exists(MODULES_LOG_FILE):
        save_data(MODULES_LOG_FILE, {"logs": []})


# تهيئة البيانات الافتراضية
init_default_data()

# واجهات برمجة التطبيقات للمديولات


@router.get("/")
def get_modules():
    """الحصول على قائمة المديولات"""
    # تحديث البيانات قبل الإرجاع
    modules = discover_modules()
    save_data(MODULES_FILE, {"modules": modules})

    return modules


@router.get("/")
def get_module(module_id):
    """الحصول على تفاصيل مديول محدد"""
    modules = discover_modules()
    module = next((m for m in modules if m['id'] == module_id), None)

    if module:
        return module
    else:
        raise HTTPException(status_code=404, detail="Module not found")


@router.get("/")
def start_module_api(module_id):
    """تشغيل مديول"""
    # التحقق من وجود المديول
    if not module_exists(module_id):
        return {
            "success": False,
            "message": f"Module {module_id} not found"
        }, 404

    # تشغيل المديول
    result = start_module(module_id)

    if result:
        # تسجيل العملية
        log_module_operation(module_id, 'start')

        # تحديث البيانات
        modules = discover_modules()
        save_data(MODULES_FILE, {"modules": modules})

        # الحصول على المديول المحدث
        module = next((m for m in modules if m['id'] == module_id), None)

        return {
            "success": True,
            "message": f"Module {module_id} started successfully",
            "module": module
        }
    else:
        return {
            "success": False,
            "message": f"Failed to start module {module_id}"
        }, 500


@router.get("/")
def stop_module_api(module_id):
    """إيقاف مديول"""
    # التحقق من وجود المديول
    if not module_exists(module_id):
        return {
            "success": False,
            "message": f"Module {module_id} not found"
        }, 404

    # إيقاف المديول
    result = stop_module(module_id)

    if result:
        # تسجيل العملية
        log_module_operation(module_id, 'stop')

        # تحديث البيانات
        modules = discover_modules()
        save_data(MODULES_FILE, {"modules": modules})

        # الحصول على المديول المحدث
        module = next((m for m in modules if m['id'] == module_id), None)

        return {
            "success": True,
            "message": f"Module {module_id} stopped successfully",
            "module": module
        }
    else:
        return {
            "success": False,
            "message": f"Failed to stop module {module_id}"
        }, 500


@router.get("/")
def restart_module_api(module_id):
    """إعادة تشغيل مديول"""
    # التحقق من وجود المديول
    if not module_exists(module_id):
        return {
            "success": False,
            "message": f"Module {module_id} not found"
        }, 404

    # إعادة تشغيل المديول
    result = restart_module(module_id)

    if result:
        # تسجيل العملية
        log_module_operation(module_id, 'restart')

        # تحديث البيانات
        modules = discover_modules()
        save_data(MODULES_FILE, {"modules": modules})

        # الحصول على المديول المحدث
        module = next((m for m in modules if m['id'] == module_id), None)

        return {
            "success": True,
            "message": f"Module {module_id} restarted successfully",
            "module": module
        }
    else:
        return {
            "success": False,
            "message": f"Failed to restart module {module_id}"
        }, 500


@router.get("/")
def get_module_logs():
    """الحصول على سجلات المديولات"""
    # الحصول على معلمات الاستعلام
    module_id = request.args.get('module_id')
    operation = request.args.get('operation')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit')

    # تحميل السجلات
    logs_data = load_data(MODULES_LOG_FILE, {"logs": []})
    logs = logs_data.get("logs", [])

    # تطبيق المرشحات
    if module_id:
        logs = [log for log in logs if log.get('module') == module_id]

    if operation:
        logs = [log for log in logs if log.get('operation') == operation]

    if start_date:
        logs = [log for log in logs if log.get('timestamp', '') >= start_date]

    if end_date:
        logs = [log for log in logs if log.get('timestamp', '') <= end_date]

    # تطبيق الحد الأقصى
    if limit:
        try:
            limit = int(limit)
            logs = logs[-limit:]  # أحدث السجلات
        except ValueError:
            pass

    return {"logs": logs}


@router.get("/")
def get_modules_health():
    """فحص صحة جميع المديولات"""
    modules = discover_modules()

    health_status = {
        "overall_status": "healthy",
        "modules": modules,
        "summary": {
            "total": len(modules),
            "running": len([m for m in modules if m['status'] == 'running']),
            "stopped": len([m for m in modules if m['status'] == 'stopped']),
            "error": len([m for m in modules if m['status'] == 'error'])
        },
        "timestamp": datetime.now().isoformat()
    }

    # تحديد الحالة العامة
    if health_status["summary"]["error"] > 0:
        health_status["overall_status"] = "error"
    elif health_status["summary"]["running"] == 0:
        health_status["overall_status"] = "warning"

    return health_status


@router.get("/")
def batch_module_operations():
    """تنفيذ عمليات متعددة على المديولات"""
    data = request.get_json()

    if not data or 'operations' not in data:
        raise HTTPException(status_code=400, detail="Missing operations data")

    operations = data['operations']
    results = []

    for operation in operations:
        module_id = operation.get('module_id')
        action = operation.get('action')

        if not module_id or not action:
            results.append({
                "module_id": module_id,
                "action": action,
                "success": False,
                "message": "Missing module_id or action"
            })
            continue

        # التحقق من وجود المديول
        if not module_exists(module_id):
            results.append({
                "module_id": module_id,
                "action": action,
                "success": False,
                "message": f"Module {module_id} not found"
            })
            continue

        # تنفيذ العملية
        try:
            if action == 'start':
                result = start_module(module_id)
            elif action == 'stop':
                result = stop_module(module_id)
            elif action == 'restart':
                result = restart_module(module_id)
            else:
                results.append({
                    "module_id": module_id,
                    "action": action,
                    "success": False,
                    "message": f"Unknown action: {action}"
                })
                continue

            if result:
                # تسجيل العملية
                log_module_operation(module_id, action)

                results.append({
                    "module_id": module_id,
                    "action": action,
                    "success": True,
                    "message": f"Module {module_id} {action} successful"
                })
            else:
                results.append({
                    "module_id": module_id,
                    "action": action,
                    "success": False,
                    "message": f"Failed to {action} module {module_id}"
                })

        except Exception as e:
            results.append({
                "module_id": module_id,
                "action": action,
                "success": False,
                "message": f"Error: {str(e)}"
            })

    return {
        "results": results,
        "summary": {
            "total": len(operations),
            "successful": len([r for r in results if r['success']]),
            "failed": len([r for r in results if not r['success']])
        },
        "timestamp": datetime.now().isoformat()
    }

# تسجيل البلوبرنت في التطبيق
