# /home/ubuntu/ai_web_organized/src/modules/module_shutdown/priority_determiner.py

"""
from flask import g
محدد الأولويات (Priority Determiner)

هذه الوحدة مسؤولة عن تحديد المديولات التي يمكن إغلاقها عند الحاجة،
بناءً على استهلاك الموارد، الأولوية، والاعتمادية.
"""

import json
import logging
import os
import threading
import time
from typing import Any, Dict, List, Tuple

# استيراد مدير المديولات
from modules.module_shutdown.module_manager import (
    ModuleInfo,
    ModuleManager,
    ModuleState,
)

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('priority_determiner')


class ShutdownReason:
    """
    فئة تمثل أسباب إغلاق المديول.
    """
    RESOURCE_CRITICAL = "resource_critical"
    LOW_PRIORITY = "low_priority"
    MANUAL_REQUEST = "manual_request"
    DEPENDENCY_SHUTDOWN = "dependency_shutdown"
    SYSTEM_SHUTDOWN = "system_shutdown"
    ERROR = "error"


class ResourceType:
    """
    فئة تمثل أنواع الموارد.
    """
    CPU = "cpu_percent"
    MEMORY = "memory_percent"
    DISK = "disk_percent"
    NETWORK = "network_percent"


class PriorityDeterminer:
    """
    فئة محدد الأولويات المسؤولة عن تحديد المديولات التي يمكن إغلاقها عند الحاجة.
    """

    def __init__(self, module_manager: ModuleManager, config_path: str = None):
        """
        تهيئة محدد الأولويات.

        Args:
            module_manager: مدير المديولات
            config_path: مسار ملف التكوين
        """
        self.module_manager = module_manager
        self.config_path = config_path or "/home/ubuntu/ai_web_organized/config/priority_determiner.json"
        self.config = {
            "system_resource_thresholds": {
                "cpu_percent": 80.0,
                "memory_percent": 80.0,
                "disk_percent": 90.0
            },
            "critical_modules": [],
            "shutdown_order": [
                {"priority": 10, "resource_usage": "high"},
                {"priority": 9, "resource_usage": "high"},
                {"priority": 8, "resource_usage": "high"},
                {"priority": 10, "resource_usage": "medium"},
                {"priority": 7, "resource_usage": "high"},
                {"priority": 9, "resource_usage": "medium"},
                {"priority": 6, "resource_usage": "high"},
                {"priority": 8, "resource_usage": "medium"},
                {"priority": 10, "resource_usage": "low"},
                {"priority": 5, "resource_usage": "high"},
                {"priority": 7, "resource_usage": "medium"},
                {"priority": 9, "resource_usage": "low"},
                {"priority": 4, "resource_usage": "high"},
                {"priority": 6, "resource_usage": "medium"},
                {"priority": 8, "resource_usage": "low"},
                {"priority": 3, "resource_usage": "high"},
                {"priority": 5, "resource_usage": "medium"},
                {"priority": 7, "resource_usage": "low"},
                {"priority": 2, "resource_usage": "high"},
                {"priority": 4, "resource_usage": "medium"},
                {"priority": 6, "resource_usage": "low"},
                {"priority": 1, "resource_usage": "high"},
                {"priority": 3, "resource_usage": "medium"},
                {"priority": 5, "resource_usage": "low"},
                {"priority": 2, "resource_usage": "medium"},
                {"priority": 4, "resource_usage": "low"},
                {"priority": 1, "resource_usage": "medium"},
                {"priority": 3, "resource_usage": "low"},
                {"priority": 2, "resource_usage": "low"},
                {"priority": 1, "resource_usage": "low"}
            ],
            "resource_usage_thresholds": {
                "high": {
                    "cpu_percent": 70.0,
                    "memory_percent": 70.0,
                    "disk_percent": 80.0
                },
                "medium": {
                    "cpu_percent": 40.0,
                    "memory_percent": 40.0,
                    "disk_percent": 60.0
                },
                "low": {
                    "cpu_percent": 10.0,
                    "memory_percent": 10.0,
                    "disk_percent": 30.0
                }
            },
            "check_interval": 30,  # ثواني
            "auto_shutdown": True
        }

        # تحميل التكوين
        self._load_config()

        # حالة المراقبة
        self.is_monitoring = False
        self.monitoring_thread = None
        self.lock = threading.Lock()

        logger.info("تم تهيئة محدد الأولويات بنجاح")

    def _load_config(self) -> bool:
        """
        تحميل تكوين محدد الأولويات من ملف.

        Returns:
            bool: نجاح العملية
        """
        try:
            if not os.path.exists(self.config_path):
                # إنشاء ملف تكوين افتراضي إذا لم يكن موجودًا
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
                logger.info(
                    f"تم إنشاء ملف تكوين افتراضي في {self.config_path}")
                return True

            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)

            # دمج التكوين المحمل مع التكوين الافتراضي
            for key, value in loaded_config.items():
                self.config[key] = value

            logger.info(f"تم تحميل تكوين محدد الأولويات من {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"فشل تحميل تكوين محدد الأولويات: {str(e)}")
            return False

    def _save_config(self) -> bool:
        """
        حفظ تكوين محدد الأولويات إلى ملف.

        Returns:
            bool: نجاح العملية
        """
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)

            logger.info(f"تم حفظ تكوين محدد الأولويات إلى {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"فشل حفظ تكوين محدد الأولويات: {str(e)}")
            return False

    def update_config(self, **kwargs) -> bool:
        """
        تحديث تكوين محدد الأولويات.

        Args:
            **kwargs: المعلومات المراد تحديثها

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            # تحديث التكوين
            for key, value in kwargs.items():
                if key in self.config:
                    self.config[key] = value

            # حفظ التكوين
            return self._save_config()

    def start_monitoring(self) -> bool:
        """
        بدء مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها.

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

        logger.info(
            "تم بدء مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها")
        return True

    def stop_monitoring(self) -> bool:
        """
        إيقاف مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها.

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

        logger.info(
            "تم إيقاف مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها")
        return True

    def _monitoring_loop(self) -> None:
        """
        حلقة مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها.
        """
        logger.info(
            "بدء حلقة مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها")

        while self.is_monitoring:
            try:
                # التحقق من استهلاك موارد النظام
                system_resources = self.module_manager.get_system_resource_usage()

                # التحقق مما إذا كان استهلاك موارد النظام حرجًا
                is_system_critical, critical_resources = self._is_system_resource_critical(
                    system_resources)

                if is_system_critical:
                    logger.warning(
                        f"استهلاك موارد النظام حرج: {critical_resources}")

                    # تحديد المديولات التي يمكن إغلاقها
                    modules_to_shutdown = self.determine_modules_to_shutdown(
                        critical_resources)

                    # إغلاق المديولات تلقائيًا إذا كان مفعلًا
                    if self.config.get(
                        "auto_shutdown",
                            True) and modules_to_shutdown:
                        logger.info(
                            f"إغلاق المديولات تلقائيًا: {modules_to_shutdown}")
                        for module_id, reason in modules_to_shutdown.items():
                            self.module_manager.stop_module(module_id)

                # انتظار الفاصل الزمني
                time.sleep(self.config.get("check_interval", 30))
            except Exception as e:
                logger.error(f"خطأ في حلقة المراقبة: {str(e)}")
                time.sleep(self.config.get("check_interval", 30))

        logger.info(
            "انتهاء حلقة مراقبة استهلاك الموارد وتحديد المديولات التي يمكن إغلاقها")

    def _is_system_resource_critical(
            self, system_resources: Dict[str, float]) -> Tuple[bool, Dict[str, bool]]:
        """
        التحقق مما إذا كان استهلاك موارد النظام حرجًا.

        Args:
            system_resources: استهلاك موارد النظام

        Returns:
            Tuple[bool, Dict[str, bool]]: (استهلاك الموارد حرج، تفاصيل الموارد الحرجة)
        """
        thresholds = self.config.get("system_resource_thresholds", {})
        critical_resources = {}

        for resource, usage in system_resources.items():
            threshold = thresholds.get(resource, float('inf'))
            critical_resources[resource] = usage >= threshold

        is_critical = any(critical_resources.values())

        return is_critical, critical_resources

    def _get_resource_usage_level(
            self, resource_usage: Dict[str, float]) -> str:
        """
        الحصول على مستوى استهلاك الموارد (مرتفع، متوسط، منخفض).

        Args:
            resource_usage: استهلاك الموارد

        Returns:
            str: مستوى استهلاك الموارد
        """
        thresholds = self.config.get("resource_usage_thresholds", {})

        # التحقق من المستوى المرتفع
        high_thresholds = thresholds.get("high", {})
        for resource, usage in resource_usage.items():
            threshold = high_thresholds.get(resource, float('inf'))
            if usage >= threshold:
                return "high"

        # التحقق من المستوى المتوسط
        medium_thresholds = thresholds.get("medium", {})
        for resource, usage in resource_usage.items():
            threshold = medium_thresholds.get(resource, float('inf'))
            if usage >= threshold:
                return "medium"

        # المستوى المنخفض
        return "low"

    def determine_modules_to_shutdown(
            self, critical_resources: Dict[str, bool] = None) -> Dict[str, str]:
        """
        تحديد المديولات التي يمكن إغلاقها عند الحاجة.

        Args:
            critical_resources: الموارد الحرجة

        Returns:
            Dict[str, str]: قاموس المديولات التي يمكن إغلاقها مع سبب الإغلاق
        """
        with self.lock:
            # الحصول على جميع المديولات
            all_modules = self.module_manager.get_all_modules()

            # تصفية المديولات قيد التشغيل
            running_modules = {
                module_id: module_info for module_id,
                module_info in all_modules.items() if module_info.state == ModuleState.RUNNING}

            # استبعاد المديولات الحرجة
            critical_module_ids = set(self.config.get("critical_modules", []))
            non_critical_modules = {
                module_id: module_info for module_id,
                module_info in running_modules.items() if module_id not in critical_module_ids}

            # تصنيف المديولات حسب الأولوية ومستوى استهلاك الموارد
            modules_by_priority_and_usage = {}
            for module_id, module_info in non_critical_modules.items():
                priority = module_info.priority
                resource_usage = self._get_resource_usage_level(
                    module_info.resource_usage)

                key = (priority, resource_usage)
                if key not in modules_by_priority_and_usage:
                    modules_by_priority_and_usage[key] = []

                modules_by_priority_and_usage[key].append(module_id)

            # تحديد المديولات التي يمكن إغلاقها حسب ترتيب الإغلاق
            modules_to_shutdown = {}
            shutdown_order = self.config.get("shutdown_order", [])

            for order_item in shutdown_order:
                priority = order_item.get("priority")
                resource_usage = order_item.get("resource_usage")

                key = (priority, resource_usage)
                if key in modules_by_priority_and_usage:
                    for module_id in modules_by_priority_and_usage[key]:
                        # التحقق من عدم وجود مديولات تعتمد على هذا المديول
                        dependent_modules = self.module_manager.get_dependent_modules(
                            module_id)
                        running_dependent_modules = [
                            dep_id for dep_id in dependent_modules
                            if dep_id in running_modules and dep_id not in modules_to_shutdown
                        ]

                        if not running_dependent_modules:
                            # تحديد سبب الإغلاق
                            reason = ShutdownReason.LOW_PRIORITY
                            if critical_resources:
                                reason = ShutdownReason.RESOURCE_CRITICAL

                            modules_to_shutdown[module_id] = reason

            return modules_to_shutdown

    def get_shutdown_candidates(self, count: int = 1) -> Dict[str, str]:
        """
        الحصول على المديولات المرشحة للإغلاق.

        Args:
            count: عدد المديولات المطلوبة

        Returns:
            Dict[str, str]: قاموس المديولات المرشحة للإغلاق مع سبب الإغلاق
        """
        with self.lock:
            # تحديد المديولات التي يمكن إغلاقها
            modules_to_shutdown = self.determine_modules_to_shutdown()

            # اختيار العدد المطلوب من المديولات
            return dict(list(modules_to_shutdown.items())[:count])

    def get_module_shutdown_impact(self, module_id: str) -> Dict[str, Any]:
        """
        الحصول على تأثير إغلاق المديول.

        Args:
            module_id: معرف المديول

        Returns:
            Dict[str, Any]: تأثير إغلاق المديول
        """
        with self.lock:
            if module_id not in self.module_manager.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return {}

            # الحصول على المديولات التي تعتمد على هذا المديول
            dependent_modules = self.module_manager.get_dependent_modules(
                module_id)

            # الحصول على المديولات التي يعتمد عليها هذا المديول
            module_info = self.module_manager.modules[module_id]
            dependencies = module_info.dependencies

            # تحديد تأثير الإغلاق
            impact = {
                "module_id": module_id,
                "priority": module_info.priority,
                "resource_usage": module_info.resource_usage,
                "dependent_modules": dependent_modules,
                "dependencies": dependencies,
                "can_shutdown": len(dependent_modules) == 0
            }

            return impact

    def get_shutdown_plan(
            self, resource_type: str = None) -> List[Dict[str, Any]]:
        """
        الحصول على خطة إغلاق المديولات.

        Args:
            resource_type: نوع المورد (CPU، الذاكرة، القرص)

        Returns:
            List[Dict[str, Any]]: خطة إغلاق المديولات
        """
        with self.lock:
            # الحصول على جميع المديولات
            all_modules = self.module_manager.get_all_modules()

            # تحديد المديولات التي يمكن إغلاقها
            modules_to_shutdown = self.determine_modules_to_shutdown()

            # إنشاء خطة الإغلاق
            shutdown_plan = []

            for module_id, reason in modules_to_shutdown.items():
                module_info = all_modules[module_id]

                # تحديد تأثير الإغلاق
                impact = self.get_module_shutdown_impact(module_id)

                # إضافة المديول إلى خطة الإغلاق
                shutdown_plan.append({
                    "module_id": module_id,
                    "name": module_info.name,
                    "priority": module_info.priority,
                    "resource_usage": module_info.resource_usage,
                    "reason": reason,
                    "impact": impact
                })

            # ترتيب خطة الإغلاق حسب الأولوية ومستوى استهلاك الموارد
            if resource_type:
                shutdown_plan.sort(
                    key=lambda x: x["resource_usage"].get(
                        resource_type, 0), reverse=True)
            else:
                shutdown_plan.sort(key=lambda x: x["priority"])

            return shutdown_plan

    def add_critical_module(self, module_id: str) -> bool:
        """
        إضافة مديول إلى قائمة المديولات الحرجة.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            if module_id not in self.module_manager.modules:
                logger.warning(f"المديول {module_id} غير مسجل")
                return False

            critical_modules = set(self.config.get("critical_modules", []))

            if module_id in critical_modules:
                logger.warning(
                    f"المديول {module_id} موجود بالفعل في قائمة المديولات الحرجة")
                return True

            critical_modules.add(module_id)
            self.config["critical_modules"] = list(critical_modules)

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info(
                    f"تم إضافة المديول {module_id} إلى قائمة المديولات الحرجة")

            return result

    def remove_critical_module(self, module_id: str) -> bool:
        """
        إزالة مديول من قائمة المديولات الحرجة.

        Args:
            module_id: معرف المديول

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            critical_modules = set(self.config.get("critical_modules", []))

            if module_id not in critical_modules:
                logger.warning(
                    f"المديول {module_id} غير موجود في قائمة المديولات الحرجة")
                return True

            critical_modules.remove(module_id)
            self.config["critical_modules"] = list(critical_modules)

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info(
                    f"تم إزالة المديول {module_id} من قائمة المديولات الحرجة")

            return result

    def is_critical_module(self, module_id: str) -> bool:
        """
        التحقق مما إذا كان المديول حرجًا.

        Args:
            module_id: معرف المديول

        Returns:
            bool: المديول حرج
        """
        critical_modules = set(self.config.get("critical_modules", []))
        return module_id in critical_modules

    def get_critical_modules(self) -> List[str]:
        """
        الحصول على قائمة المديولات الحرجة.

        Returns:
            List[str]: قائمة المديولات الحرجة
        """
        return list(self.config.get("critical_modules", []))

    def update_system_resource_thresholds(self, **kwargs) -> bool:
        """
        تحديث عتبات موارد النظام.

        Args:
            **kwargs: العتبات المراد تحديثها

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            thresholds = self.config.get("system_resource_thresholds", {})

            # تحديث العتبات
            for key, value in kwargs.items():
                thresholds[key] = value

            self.config["system_resource_thresholds"] = thresholds

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info(f"تم تحديث عتبات موارد النظام: {kwargs}")

            return result

    def get_system_resource_thresholds(self) -> Dict[str, float]:
        """
        الحصول على عتبات موارد النظام.

        Returns:
            Dict[str, float]: عتبات موارد النظام
        """
        return self.config.get("system_resource_thresholds", {}).copy()

    def update_resource_usage_thresholds(self, level: str, **kwargs) -> bool:
        """
        تحديث عتبات استهلاك الموارد.

        Args:
            level: مستوى الاستهلاك (مرتفع، متوسط، منخفض)
            **kwargs: العتبات المراد تحديثها

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            thresholds = self.config.get("resource_usage_thresholds", {})

            if level not in thresholds:
                logger.warning(f"مستوى الاستهلاك {level} غير موجود")
                return False

            # تحديث العتبات
            for key, value in kwargs.items():
                thresholds[level][key] = value

            self.config["resource_usage_thresholds"] = thresholds

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info(
                    f"تم تحديث عتبات استهلاك الموارد لمستوى {level}: {kwargs}")

            return result

    def get_resource_usage_thresholds(
            self, level: str = None) -> Dict[str, Any]:
        """
        الحصول على عتبات استهلاك الموارد.

        Args:
            level: مستوى الاستهلاك (مرتفع، متوسط، منخفض)

        Returns:
            Dict[str, Any]: عتبات استهلاك الموارد
        """
        thresholds = self.config.get("resource_usage_thresholds", {}).copy()

        if level:
            return thresholds.get(level, {}).copy()

        return thresholds

    def update_shutdown_order(
            self, shutdown_order: List[Dict[str, Any]]) -> bool:
        """
        تحديث ترتيب إغلاق المديولات.

        Args:
            shutdown_order: ترتيب إغلاق المديولات

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            self.config["shutdown_order"] = shutdown_order

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info("تم تحديث ترتيب إغلاق المديولات")

            return result

    def get_shutdown_order(self) -> List[Dict[str, Any]]:
        """
        الحصول على ترتيب إغلاق المديولات.

        Returns:
            List[Dict[str, Any]]: ترتيب إغلاق المديولات
        """
        return self.config.get("shutdown_order", []).copy()

    def set_auto_shutdown(self, auto_shutdown: bool) -> bool:
        """
        تعيين الإغلاق التلقائي.

        Args:
            auto_shutdown: الإغلاق التلقائي

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            self.config["auto_shutdown"] = auto_shutdown

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info(f"تم تعيين الإغلاق التلقائي: {auto_shutdown}")

            return result

    def get_auto_shutdown(self) -> bool:
        """
        الحصول على حالة الإغلاق التلقائي.

        Returns:
            bool: الإغلاق التلقائي
        """
        return self.config.get("auto_shutdown", True)

    def set_check_interval(self, interval: int) -> bool:
        """
        تعيين الفاصل الزمني للتحقق.

        Args:
            interval: الفاصل الزمني بالثواني

        Returns:
            bool: نجاح العملية
        """
        with self.lock:
            self.config["check_interval"] = interval

            # حفظ التكوين
            result = self._save_config()

            if result:
                logger.info(f"تم تعيين الفاصل الزمني للتحقق: {interval} ثانية")

            return result

    def get_check_interval(self) -> int:
        """
        الحصول على الفاصل الزمني للتحقق.

        Returns:
            int: الفاصل الزمني بالثواني
        """
        return self.config.get("check_interval", 30)


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

    manager.register_module(ModuleInfo(
        module_id="module3",
        name="المديول الثالث",
        description="وصف المديول الثالث",
        priority=3
    ))

    # بدء تشغيل المديولات
    manager.start_module("module1")
    manager.start_module("module2")
    manager.start_module("module3")

    # إنشاء محدد الأولويات
    determiner = PriorityDeterminer(manager)

    # إضافة مديول حرج
    determiner.add_critical_module("module1")

    # الحصول على المديولات المرشحة للإغلاق
    candidates = determiner.get_shutdown_candidates(2)
    print(f"المديولات المرشحة للإغلاق: {candidates}")

    # الحصول على خطة إغلاق المديولات
    plan = determiner.get_shutdown_plan()
    print(f"خطة إغلاق المديولات: {plan}")

    # بدء المراقبة
    determiner.start_monitoring()

    # انتظار بعض الوقت
    time.sleep(10)

    # إيقاف المراقبة
    determiner.stop_monitoring()
