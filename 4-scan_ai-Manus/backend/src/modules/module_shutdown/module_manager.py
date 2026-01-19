# /home/ubuntu/ai_web_organized/src/modules/module_shutdown/module_manager.py

"""
from flask import g
مدير المديولات (Module Manager)

هذه الوحدة مسؤولة عن إدارة حالة المديولات وتتبع استهلاك الموارد،
وتوفير واجهة برمجية للتحكم في دورة حياة المديولات.
"""

import json
import logging
import os
import threading
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

import psutil

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('module_manager')


class ModuleState:
    """
    فئة تمثل حالة المديول.
    """
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    STARTING = "starting"
    STOPPING = "stopping"


class ModuleInfo:
    """
    فئة تمثل معلومات المديول.
    """

    def __init__(self,
                 module_id: str,
                 name: str,
                 description: str,
                 priority: int = 5,
                 dependencies: Optional[List[str]] = None,
                 resource_limits: Optional[Dict[str,
                                                float]] = None):
        """
        تهيئة معلومات المديول.

        Args:
            module_id: معرف المديول الفريد
            name: اسم المديول
            description: وصف المديول
            priority: أولوية المديول (1-10، حيث 1 هي الأعلى)
            dependencies: قائمة معرفات المديولات التي يعتمد عليها هذا المديول
            resource_limits: حدود الموارد للمديول (CPU، RAM، إلخ)
        """
        self.module_id = module_id
        self.name = name
        self.description = description
        self.priority = priority
        self.dependencies = dependencies or []
        self.resource_limits = resource_limits or {
            "cpu_percent": 80.0,
            "memory_percent": 70.0,
            "disk_percent": 90.0
        }
        self.state = ModuleState.STOPPED
        self.process_id: Optional[int] = None
        self.start_time: Optional[datetime] = None
        self.stop_time: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.resource_usage = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "disk_percent": 0.0
        }
        self.last_update = datetime.now()


class ModuleManager:
    """
    فئة مدير المديولات المسؤولة عن إدارة حالة المديولات وتتبع استهلاك الموارد.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        تهيئة مدير المديولات.

        Args:
            config_path: مسار ملف التكوين
        """
        self.modules: Dict[str, ModuleInfo] = {}
        if config_path is None:
            self.config_path = "/home/ubuntu/ai_web_organized/config/modules.json"
        else:
            self.config_path = config_path
        self.monitoring_interval = 5  # ثواني
        self.monitoring_thread = None
        self.is_monitoring = False
        self.lock = threading.Lock()
        self.callbacks = {
            'startup': {},
            'shutdown': {},
            'pause': {},
            'resume': {}
        }

        # تحميل التكوين
        self._load_config()

        logger.info("تم تهيئة مدير المديولات بنجاح")

    def _load_config(self) -> bool:
        """
        تحميل تكوين المديولات من ملف.

        Returns:
            bool: نجاح العملية
        """
        try:
            if not os.path.exists(self.config_path):
                # إنشاء ملف تكوين افتراضي إذا لم يكن موجودًا
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump({"modules": {}}, f, ensure_ascii=False, indent=4)
                logger.info(
                    f"تم إنشاء ملف تكوين افتراضي في {self.config_path}")
                return True

            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            for module_id, module_config in config.get("modules", {}).items():
                module_info = ModuleInfo(
                    module_id=module_id,
                    name=module_config.get("name", module_id),
                    description=module_config.get("description", ""),
                    priority=module_config.get("priority", 5),
                    dependencies=module_config.get("dependencies", []),
                    resource_limits=module_config.get("resource_limits", {})
                )
                self.modules[module_id] = module_info

            logger.info(f"تم تحميل تكوين المديولات من {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"فشل تحميل تكوين المديولات: {str(e)}")
            return False

    def _save_config(self) -> bool:
        """
        حفظ تكوين المديولات إلى ملف.

        Returns:
            bool: نجاح العملية
        """
        try:
            config = {"modules": {}}

            for module_id, module_info in self.modules.items():
                config["modules"][module_id] = {
                    "name": module_info.name,
                    "description": module_info.description,
                    "priority": module_info.priority,
                    "dependencies": module_info.dependencies,
                    "resource_limits": module_info.resource_limits
                }

            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            logger.info(f"تم حفظ تكوين المديولات إلى {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"فشل حفظ تكوين المديولات: {str(e)}")
            return False

    def register_module(self, module_info: ModuleInfo) -> bool:
        """
        تسجيل مديول جديد.

        Args:
            module_info: معلومات المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_info.module_id in self.modules:
                logger.warning(f"المديول {module_info.module_id} مسجل بالفعل")
                return False

            self.modules[module_info.module_id] = module_info
            self._save_config()
            logger.info(f"تم تسجيل المديول {module_info.module_id} بنجاح")
            return True

    def unregister_module(self, module_id: str) -> bool:
        """
        إلغاء تسجيل مديول.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            # التحقق من عدم وجود مديولات تعتمد على هذا المديول
            for other_id, other_info in self.modules.items():
                if module_id in other_info.dependencies:
                    logger.error(
                        f"لا يمكن إلغاء تسجيل المديول {module_id} لأن المديول {other_id} يعتمد عليه")
                    return False

            # إيقاف المديول إذا كان قيد التشغيل
            if self.modules[module_id].state == ModuleState.RUNNING:
                self.stop_module(module_id)

            del self.modules[module_id]
            self._save_config()
            logger.info(f"تم إلغاء تسجيل المديول {module_id} بنجاح")
            return True

    def update_module_info(self, module_id: str, **kwargs) -> bool:
        """
        تحديث معلومات المديول.

        Args:
            module_id: معرف المديول
            **kwargs: المعلومات المراد تحديثها

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            module_info = self.modules[module_id]

            # تحديث المعلومات
            for key, value in kwargs.items():
                if hasattr(module_info, key):
                    setattr(module_info, key, value)

            self._save_config()
            logger.info(f"تم تحديث معلومات المديول {module_id} بنجاح")
            return True

    def get_module_info(self, module_id: str) -> Optional[ModuleInfo]:
        """
        الحصول على معلومات المديول.

        Args:
            module_id: معرف المديول

        Returns:
            Optional[ModuleInfo]: معلومات المديول أو None إذا لم يكن موجودًا
        """
        return self.modules.get(module_id)

    def get_all_modules(self) -> Dict[str, ModuleInfo]:
        """
        الحصول على جميع المديولات.

        Returns:
            Dict[str, ModuleInfo]: قاموس المديولات
        """
        return self.modules.copy()

    def start_module(self, module_id: str) -> bool:
        """
        بدء تشغيل المديول.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            module_info = self.modules[module_id]

            # التحقق من حالة المديول
            if module_info.state in [
                    ModuleState.RUNNING,
                    ModuleState.STARTING]:
                logger.warning(f"المديول {module_id} قيد التشغيل بالفعل")
                return True

            # التحقق من تشغيل المديولات التي يعتمد عليها
            for dep_id in module_info.dependencies:
                if dep_id not in self.modules:
                    logger.error(
                        f"المديول {dep_id} الذي يعتمد عليه {module_id} غير مسجل")
                    return False

                dep_info = self.modules[dep_id]
                if dep_info.state != ModuleState.RUNNING:
                    logger.info(
                        f"بدء تشغيل المديول {dep_id} الذي يعتمد عليه {module_id}")
                    if not self.start_module(dep_id):
                        logger.error(
                            f"فشل بدء تشغيل المديول {dep_id} الذي يعتمد عليه {module_id}")
                        return False

            # تحديث حالة المديول
            module_info.state = ModuleState.STARTING
            module_info.start_time = datetime.now()
            module_info.error_message = None

            try:
                # هنا يمكن تنفيذ الكود الفعلي لبدء تشغيل المديول
                # على سبيل المثال، يمكن استدعاء دالة بدء التشغيل الخاصة
                # بالمديول

                # تمثيل بدء تشغيل المديول (يجب استبدال هذا بالكود الفعلي)
                logger.info(f"بدء تشغيل المديول {module_id}")
                time.sleep(1)  # تمثيل وقت بدء التشغيل

                # تحديث حالة المديول
                module_info.state = ModuleState.RUNNING
                module_info.process_id = os.getpid()  # يجب استبدال هذا بمعرف العملية الفعلي
                module_info.last_update = datetime.now()

                logger.info(f"تم بدء تشغيل المديول {module_id} بنجاح")
                return True
            except Exception as e:
                # تحديث حالة المديول في حالة الخطأ
                module_info.state = ModuleState.ERROR
                module_info.error_message = str(e)
                module_info.last_update = datetime.now()

                logger.error(f"فشل بدء تشغيل المديول {module_id}: {str(e)}")
                return False

    def stop_module(self, module_id: str, force: bool = False) -> bool:
        """
        إيقاف تشغيل المديول.

        Args:
            module_id: معرف المديول
            force: إجبار الإيقاف حتى لو كانت هناك مديولات تعتمد عليه

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            module_info = self.modules[module_id]

            # التحقق من حالة المديول
            if module_info.state in [
                    ModuleState.STOPPED,
                    ModuleState.STOPPING]:
                logger.warning(f"المديول {module_id} متوقف بالفعل")
                return True

            # التحقق من عدم وجود مديولات قيد التشغيل تعتمد على هذا المديول
            if not force:
                dependent_modules = []
                for other_id, other_info in self.modules.items():
                    if module_id in other_info.dependencies and other_info.state == ModuleState.RUNNING:
                        dependent_modules.append(other_id)

                if dependent_modules:
                    logger.error(
                        f"لا يمكن إيقاف المديول {module_id} لأن المديولات التالية تعتمد عليه: {', '.join(dependent_modules)}")
                    return False

            # تحديث حالة المديول
            module_info.state = ModuleState.STOPPING

            try:
                # هنا يمكن تنفيذ الكود الفعلي لإيقاف تشغيل المديول
                # على سبيل المثال، يمكن استدعاء دالة إيقاف التشغيل الخاصة
                # بالمديول

                # تمثيل إيقاف تشغيل المديول (يجب استبدال هذا بالكود الفعلي)
                logger.info(f"إيقاف تشغيل المديول {module_id}")
                time.sleep(1)  # تمثيل وقت إيقاف التشغيل

                # تحديث حالة المديول
                module_info.state = ModuleState.STOPPED
                module_info.stop_time = datetime.now()
                module_info.process_id = None
                module_info.last_update = datetime.now()

                logger.info(f"تم إيقاف تشغيل المديول {module_id} بنجاح")
                return True
            except Exception as e:
                # تحديث حالة المديول في حالة الخطأ
                module_info.state = ModuleState.ERROR
                module_info.error_message = str(e)
                module_info.last_update = datetime.now()

                logger.error(f"فشل إيقاف تشغيل المديول {module_id}: {str(e)}")
                return False

    def pause_module(self, module_id: str) -> bool:
        """
        إيقاف مؤقت للمديول.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            module_info = self.modules[module_id]

            # التحقق من حالة المديول
            if module_info.state != ModuleState.RUNNING:
                logger.warning(f"المديول {module_id} ليس قيد التشغيل")
                return False

            try:
                # هنا يمكن تنفيذ الكود الفعلي لإيقاف المديول مؤقتًا
                # على سبيل المثال، يمكن استدعاء دالة الإيقاف المؤقت الخاصة
                # بالمديول

                # تمثيل الإيقاف المؤقت للمديول (يجب استبدال هذا بالكود الفعلي)
                logger.info(f"إيقاف مؤقت للمديول {module_id}")
                time.sleep(1)  # تمثيل وقت الإيقاف المؤقت

                # تحديث حالة المديول
                module_info.state = ModuleState.PAUSED
                module_info.last_update = datetime.now()

                logger.info(f"تم إيقاف المديول {module_id} مؤقتًا بنجاح")
                return True
            except Exception as e:
                # تحديث حالة المديول في حالة الخطأ
                module_info.state = ModuleState.ERROR
                module_info.error_message = str(e)
                module_info.last_update = datetime.now()

                logger.error(f"فشل إيقاف المديول {module_id} مؤقتًا: {str(e)}")
                return False

    def resume_module(self, module_id: str) -> bool:
        """
        استئناف تشغيل المديول بعد الإيقاف المؤقت.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            module_info = self.modules[module_id]

            # التحقق من حالة المديول
            if module_info.state != ModuleState.PAUSED:
                logger.warning(f"المديول {module_id} ليس في حالة إيقاف مؤقت")
                return False

            try:
                # هنا يمكن تنفيذ الكود الفعلي لاستئناف تشغيل المديول
                # على سبيل المثال، يمكن استدعاء دالة الاستئناف الخاصة بالمديول

                # تمثيل استئناف تشغيل المديول (يجب استبدال هذا بالكود الفعلي)
                logger.info(f"استئناف تشغيل المديول {module_id}")
                time.sleep(1)  # تمثيل وقت الاستئناف

                # تحديث حالة المديول
                module_info.state = ModuleState.RUNNING
                module_info.last_update = datetime.now()

                logger.info(f"تم استئناف تشغيل المديول {module_id} بنجاح")
                return True
            except Exception as e:
                # تحديث حالة المديول في حالة الخطأ
                module_info.state = ModuleState.ERROR
                module_info.error_message = str(e)
                module_info.last_update = datetime.now()

                logger.error(
                    f"فشل استئناف تشغيل المديول {module_id}: {str(e)}")
                return False

    def restart_module(self, module_id: str) -> bool:
        """
        إعادة تشغيل المديول.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            # إيقاف المديول
            if not self.stop_module(module_id):
                logger.error(
                    f"فشل إيقاف المديول {module_id} أثناء إعادة التشغيل")
                return False

            # بدء تشغيل المديول
            if not self.start_module(module_id):
                logger.error(
                    f"فشل بدء تشغيل المديول {module_id} أثناء إعادة التشغيل")
                return False

            logger.info(f"تم إعادة تشغيل المديول {module_id} بنجاح")
            return True

    def start_monitoring(self) -> bool:
        """
        بدء مراقبة استهلاك الموارد للمديولات.

        Returns:
            bool: نجاح العملية
        """
        if self.is_monitoring is not None:
            logger.warning("المراقبة قيد التشغيل بالفعل")
            return True

        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

        logger.info("تم بدء مراقبة استهلاك الموارد للمديولات")
        return True

    def stop_monitoring(self) -> bool:
        """
        إيقاف مراقبة استهلاك الموارد للمديولات.

        Returns:
            bool: نجاح العملية
        """
        if not self.is_monitoring:
            logger.warning("المراقبة متوقفة بالفعل")
            return True

        self.is_monitoring = False
        if self.monitoring_thread is not None:
            self.monitoring_thread.join(timeout=5)
            self.monitoring_thread = None

        logger.info("تم إيقاف مراقبة استهلاك الموارد للمديولات")
        return True

    def _monitoring_loop(self) -> None:
        """
        حلقة مراقبة استهلاك الموارد للمديولات.
        """
        logger.info("بدء حلقة مراقبة استهلاك الموارد للمديولات")

        while self.is_monitoring:
            try:
                self._update_resource_usage()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"خطأ في حلقة المراقبة: {str(e)}")
                time.sleep(self.monitoring_interval)

        logger.info("انتهاء حلقة مراقبة استهلاك الموارد للمديولات")

    def _update_resource_usage(self) -> None:
        """
        تحديث استهلاك الموارد للمديولات.
        """
        with self.lock:
            for module_id, module_info in self.modules.items():
                if module_info.state == ModuleState.RUNNING and module_info.process_id:
                    try:
                        # الحصول على استهلاك الموارد للعملية
                        process = psutil.Process(module_info.process_id)

                        # تحديث استهلاك الموارد
                        module_info.resource_usage["cpu_percent"] = process.cpu_percent(
                            interval=0.1)
                        module_info.resource_usage["memory_percent"] = process.memory_percent(
                        )

                        # تحديث وقت آخر تحديث
                        module_info.last_update = datetime.now()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                        logger.warning(
                            f"خطأ في تحديث استهلاك الموارد للمديول {module_id}: {str(e)}")

                        # تحديث حالة المديول في حالة عدم وجود العملية
                        if isinstance(e, psutil.NoSuchProcess):
                            module_info.state = ModuleState.ERROR
                            module_info.error_message = f"العملية غير موجودة: {str(e)}"
                            module_info.process_id = None

    def get_resource_usage(self, module_id: str) -> Optional[Dict[str, float]]:
        """
        الحصول على استهلاك الموارد للمديول.

        Args:
            module_id: معرف المديول

        Returns:
            Optional[Dict[str, float]]: استهلاك الموارد أو None إذا لم يكن المديول موجودًا
        """
        if module_id not in self.modules:
            logger.warning(f"المديول {module_id} غير مسجل")
            return None

        return self.modules[module_id].resource_usage.copy()

    def get_system_resource_usage(self) -> Dict[str, float]:
        """
        الحصول على استهلاك موارد النظام.

        Returns:
            Dict[str, float]: استهلاك موارد النظام
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "disk_percent": disk_percent
            }
        except Exception as e:
            logger.error(f"خطأ في الحصول على استهلاك موارد النظام: {str(e)}")
            return {
                "cpu_percent": 0.0,
                "memory_percent": 0.0,
                "disk_percent": 0.0
            }

    def is_resource_critical(
            self, module_id: str) -> Tuple[bool, Dict[str, bool]]:
        """
        التحقق مما إذا كان استهلاك الموارد للمديول حرجًا.

        Args:
            module_id: معرف المديول

        Returns:
            Tuple[bool, Dict[str, bool]]: (استهلاك الموارد حرج، تفاصيل الموارد الحرجة)
        """
        if module_id not in self.modules:
            logger.warning(f"المديول {module_id} غير مسجل")
            return False, {}

        module_info = self.modules[module_id]
        resource_usage = module_info.resource_usage
        resource_limits = module_info.resource_limits

        critical_resources = {}

        for resource, usage in resource_usage.items():
            limit = resource_limits.get(resource, float('inf'))
            critical_resources[resource] = usage >= limit

        is_critical = any(critical_resources.values())

        return is_critical, critical_resources

    def get_modules_by_state(self, state: str) -> List[str]:
        """
        الحصول على قائمة المديولات حسب الحالة.

        Args:
            state: حالة المديول

        Returns:
            List[str]: قائمة معرفات المديولات
        """
        return [
            module_id for module_id,
            module_info in self.modules.items() if module_info.state == state]

    def get_modules_by_priority(
            self,
            min_priority: int = 1,
            max_priority: int = 10) -> List[str]:
        """
        الحصول على قائمة المديولات حسب الأولوية.

        Args:
            min_priority: الحد الأدنى للأولوية
            max_priority: الحد الأقصى للأولوية

        Returns:
            List[str]: قائمة معرفات المديولات
        """
        return [
            module_id for module_id, module_info in self.modules.items()
            if min_priority <= module_info.priority <= max_priority
        ]

    def get_dependent_modules(self, module_id: str) -> List[str]:
        """
        الحصول على قائمة المديولات التي تعتمد على المديول المحدد.

        Args:
            module_id: معرف المديول

        Returns:
            List[str]: قائمة معرفات المديولات
        """
        return [
            other_id for other_id, other_info in self.modules.items()
            if module_id in other_info.dependencies
        ]

    def get_dependency_tree(self, module_id: str) -> Dict[str, List[str]]:
        """
        الحصول على شجرة الاعتماد للمديول.

        Args:
            module_id: معرف المديول

        Returns:
            Dict[str, List[str]]: شجرة الاعتماد
        """
        if module_id not in self.modules:
            logger.warning(f"المديول {module_id} غير مسجل")
            return {}

        tree = {}
        self._build_dependency_tree(module_id, tree)
        return tree

    def _build_dependency_tree(
            self, module_id: str, tree: Dict[str, List[str]]) -> None:
        """
        بناء شجرة الاعتماد للمديول.

        Args:
            module_id: معرف المديول
            tree: شجرة الاعتماد
        """
        if module_id not in self.modules:
            return

        module_info = self.modules[module_id]
        tree[module_id] = module_info.dependencies

        for dep_id in module_info.dependencies:
            if dep_id not in tree:
                self._build_dependency_tree(dep_id, tree)

    def register_startup_callback(
            self,
            module_id: str,
            callback: Callable) -> None:
        """
        Register a startup callback for a module.
        """
        if module_id not in self.callbacks['startup']:
            self.callbacks['startup'][module_id] = []
        self.callbacks['startup'][module_id].append(callback)

    def register_shutdown_callback(
            self,
            module_id: str,
            callback: Callable) -> None:
        """
        Register a shutdown callback for a module.
        """
        if module_id not in self.callbacks['shutdown']:
            self.callbacks['shutdown'][module_id] = []
        self.callbacks['shutdown'][module_id].append(callback)

    def register_pause_callback(
            self,
            module_id: str,
            callback: Callable) -> None:
        """
        Register a pause callback for a module.
        """
        if module_id not in self.callbacks['pause']:
            self.callbacks['pause'][module_id] = []
        self.callbacks['pause'][module_id].append(callback)

    def register_resume_callback(
            self,
            module_id: str,
            callback: Callable) -> None:
        """
        Register a resume callback for a module.
        """
        if module_id not in self.callbacks['resume']:
            self.callbacks['resume'][module_id] = []
        self.callbacks['resume'][module_id].append(callback)


# مثال على الاستخدام
if __name__ == "__main__":
    # إنشاء مدير المديولات
    manager = ModuleManager()

    # تسجيل بعض المديولات
    manager.register_module(ModuleInfo(
        module_id="module1",
        name="المديول الأول",
        description="وصف المديول الأول",
        priority=1
    ))

    manager.register_module(ModuleInfo(
        module_id="module2",
        name="المديول الثاني",
        description="وصف المديول الثاني",
        priority=2,
        dependencies=["module1"]
    ))

    # بدء تشغيل المديولات
    manager.start_module("module2")  # سيبدأ تشغيل module1 تلقائيًا

    # بدء المراقبة
    manager.start_monitoring()

    # انتظار بعض الوقت
    time.sleep(10)

    # إيقاف المراقبة
    manager.stop_monitoring()

    # إيقاف تشغيل المديولات
    manager.stop_module("module2")
    manager.stop_module("module1")
