# /home/ubuntu/ai_web_organized/src/modules/module_shutdown/integration_test.py

"""
from flask import g
اختبار تكامل نظام إغلاق المديولات وتعليق الذكاء الصناعي

هذا الملف يحتوي على اختبارات تكامل لجميع مكونات نظام إغلاق المديولات وتعليق الذكاء الصناعي،
بما في ذلك مدير المديولات، محدد الأولويات، منفذ الإغلاق الآمن، مراقب موارد الذكاء الصناعي،
ومدير التعليق والاستئناف.
"""

import logging
import time
import unittest
from datetime import datetime, timedelta
from typing import Any, Callable, Dict

from modules.module_shutdown.ai_resource_monitor import (
    AIResourceMonitor,
    AIResourceType,
    ResourceAlert,
)
from modules.module_shutdown.ai_suspension_manager import (
    AISuspensionManager,
    SuspensionReason,
    SuspensionState,
    SuspensionStrategy,
)

# استيراد المكونات المراد اختبارها
from modules.module_shutdown.module_manager import (
    ModuleInfo,
    ModuleManager,
    ModuleState,
)
from modules.module_shutdown.priority_determiner import (
    PriorityDeterminer,
    ShutdownReason,
)
from modules.module_shutdown.safe_shutdown_executor import (
    SafeShutdownExecutor,
    ShutdownStrategy,
)

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('integration_test')


class MockModule:
    """
    فئة وهمية لمحاكاة مديول.
    """

    def __init__(self, module_id: str, name: str = None, priority: int = 1):
        """
        تهيئة المديول الوهمي.

        Args:
            module_id: معرف المديول
            name: اسم المديول
            priority: أولوية المديول
        """
        self.module_id = module_id
        self.name = name or module_id
        self.priority = priority
        self.state = ModuleState.STOPPED
        self.resources = {
            AIResourceType.CPU: 0.0,
            AIResourceType.MEMORY: 0.0,
            AIResourceType.GPU: 0.0,
            AIResourceType.TOKENS: 0,
            AIResourceType.API_CALLS: 0,
            AIResourceType.STORAGE: 0.0,
            AIResourceType.NETWORK: 0.0
        }
        self.is_running = False
        self.is_paused = False
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.resume_time = None
        self.shutdown_callbacks = []
        self.startup_callbacks = []
        self.pause_callbacks = []
        self.resume_callbacks = []

    def start(self) -> bool:
        """
        بدء تشغيل المديول.

        Returns:
            bool: نجاح العملية
        """
        if self.is_running is not None:
            logger.warning(f"المديول {self.module_id} قيد التشغيل بالفعل")
            return True

        self.is_running = True
        self.is_paused = False
        self.state = ModuleState.RUNNING
        self.start_time = datetime.now()
        self.stop_time = None

        # تنفيذ دوال الاستدعاء لبدء التشغيل
        for callback in self.startup_callbacks:
            try:
                callback(self.module_id)
            except Exception as e:
                logger.error(
                    f"فشل تنفيذ دالة الاستدعاء لبدء التشغيل: {str(e)}")

        logger.info(f"تم بدء تشغيل المديول {self.module_id}")
        return True

    def stop(self) -> bool:
        """
        إيقاف تشغيل المديول.

        Returns:
            bool: نجاح العملية
        """
        if not self.is_running:
            logger.warning(f"المديول {self.module_id} متوقف بالفعل")
            return True

        self.is_running = False
        self.is_paused = False
        self.state = ModuleState.STOPPED
        self.stop_time = datetime.now()

        # تنفيذ دوال الاستدعاء للإيقاف
        for callback in self.shutdown_callbacks:
            try:
                callback(self.module_id)
            except Exception as e:
                logger.error(f"فشل تنفيذ دالة الاستدعاء للإيقاف: {str(e)}")

        logger.info(f"تم إيقاف تشغيل المديول {self.module_id}")
        return True

    def pause(self) -> bool:
        """
        تعليق المديول.

        Returns:
            bool: نجاح العملية
        """
        if not self.is_running:
            logger.warning(f"المديول {self.module_id} متوقف")
            return False

        if self.is_paused is not None:
            logger.warning(f"المديول {self.module_id} معلق بالفعل")
            return True

        self.is_paused = True
        self.state = ModuleState.PAUSED
        self.pause_time = datetime.now()

        # تنفيذ دوال الاستدعاء للتعليق
        for callback in self.pause_callbacks:
            try:
                callback(self.module_id)
            except Exception as e:
                logger.error(f"فشل تنفيذ دالة الاستدعاء للتعليق: {str(e)}")

        logger.info(f"تم تعليق المديول {self.module_id}")
        return True

    def resume(self) -> bool:
        """
        استئناف المديول.

        Returns:
            bool: نجاح العملية
        """
        if not self.is_running:
            logger.warning(f"المديول {self.module_id} متوقف")
            return False

        if not self.is_paused:
            logger.warning(f"المديول {self.module_id} غير معلق")
            return True

        self.is_paused = False
        self.state = ModuleState.RUNNING
        self.resume_time = datetime.now()

        # تنفيذ دوال الاستدعاء للاستئناف
        for callback in self.resume_callbacks:
            try:
                callback(self.module_id)
            except Exception as e:
                logger.error(f"فشل تنفيذ دالة الاستدعاء للاستئناف: {str(e)}")

        logger.info(f"تم استئناف المديول {self.module_id}")
        return True

    def update_resources(self, resources: Dict[str, Any]) -> None:
        """
        تحديث موارد المديول.

        Args:
            resources: الموارد
        """
        for resource_type, value in resources.items():
            if resource_type in self.resources:
                self.resources[resource_type] = value

    def register_shutdown_callback(self, callback: Callable) -> None:
        """
        تسجيل دالة استدعاء للإيقاف.

        Args:
            callback: دالة الاستدعاء
        """
        self.shutdown_callbacks.append(callback)

    def register_startup_callback(self, callback: Callable) -> None:
        """
        تسجيل دالة استدعاء لبدء التشغيل.

        Args:
            callback: دالة الاستدعاء
        """
        self.startup_callbacks.append(callback)

    def register_pause_callback(self, callback: Callable) -> None:
        """
        تسجيل دالة استدعاء للتعليق.

        Args:
            callback: دالة الاستدعاء
        """
        self.pause_callbacks.append(callback)

    def register_resume_callback(self, callback: Callable) -> None:
        """
        تسجيل دالة استدعاء للاستئناف.

        Args:
            callback: دالة الاستدعاء
        """
        self.resume_callbacks.append(callback)


class ModuleManagerTest(unittest.TestCase):
    """
    اختبار مدير المديولات.
    """

    def setUp(self):
        """
        إعداد الاختبار.
        """
        self.module_manager = ModuleManager()
        self.mock_modules = {}

        # إنشاء مديولات وهمية
        for i in range(1, 6):
            module_id = f"module{i}"
            module_name = f"مديول {i}"
            module_priority = i
            mock_module = MockModule(module_id, module_name, module_priority)
            self.mock_modules[module_id] = mock_module

            # تسجيل المديول في مدير المديولات
            self.module_manager.register_module(ModuleInfo(
                module_id=module_id,
                name=module_name,
                description=f"وصف مديول {i}",
                priority=module_priority
            ))

    def test_register_module(self):
        """
        اختبار تسجيل المديول.
        """
        # التحقق من تسجيل المديولات
        self.assertEqual(len(self.module_manager.modules), 5)
        self.assertIn("module1", self.module_manager.modules)
        self.assertIn("module5", self.module_manager.modules)

    def test_start_stop_module(self):
        """
        اختبار بدء وإيقاف تشغيل المديول.
        """
        module_id = "module1"
        mock_module = self.mock_modules[module_id]

        # تسجيل دوال الاستدعاء
        self.module_manager.register_startup_callback(
            module_id, mock_module.start)
        self.module_manager.register_shutdown_callback(
            module_id, mock_module.stop)

        # بدء تشغيل المديول
        self.assertTrue(self.module_manager.start_module(module_id))
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.RUNNING)
        self.assertTrue(mock_module.is_running)

        # إيقاف تشغيل المديول
        self.assertTrue(self.module_manager.stop_module(module_id))
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.STOPPED)
        self.assertFalse(mock_module.is_running)

    def test_pause_resume_module(self):
        """
        اختبار تعليق واستئناف المديول.
        """
        module_id = "module2"
        mock_module = self.mock_modules[module_id]

        # تسجيل دوال الاستدعاء
        self.module_manager.register_startup_callback(
            module_id, mock_module.start)
        self.module_manager.register_shutdown_callback(
            module_id, mock_module.stop)
        self.module_manager.register_pause_callback(
            module_id, mock_module.pause)
        self.module_manager.register_resume_callback(
            module_id, mock_module.resume)

        # بدء تشغيل المديول
        self.assertTrue(self.module_manager.start_module(module_id))
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.RUNNING)
        self.assertTrue(mock_module.is_running)

        # تعليق المديول
        self.assertTrue(self.module_manager.pause_module(module_id))
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.PAUSED)
        self.assertTrue(mock_module.is_paused)

        # استئناف المديول
        self.assertTrue(self.module_manager.resume_module(module_id))
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.RUNNING)
        self.assertFalse(mock_module.is_paused)

    def test_get_module_info(self):
        """
        اختبار الحصول على معلومات المديول.
        """
        module_id = "module3"
        module_info = self.module_manager.get_module_info(module_id)
        self.assertIsNotNone(module_info)
        self.assertEqual(module_info.module_id, module_id)
        self.assertEqual(module_info.name, "مديول 3")
        self.assertEqual(module_info.priority, 3)

    def test_get_all_modules(self):
        """
        اختبار الحصول على جميع المديولات.
        """
        modules = self.module_manager.get_all_modules()
        self.assertEqual(len(modules), 5)
        self.assertIn("module1", modules)
        self.assertIn("module5", modules)

    def test_get_modules_by_state(self):
        """
        اختبار الحصول على المديولات حسب الحالة.
        """
        # بدء تشغيل بعض المديولات
        self.module_manager.register_startup_callback(
            "module1", self.mock_modules["module1"].start)
        self.module_manager.register_startup_callback(
            "module2", self.mock_modules["module2"].start)
        self.module_manager.start_module("module1")
        self.module_manager.start_module("module2")

        # الحصول على المديولات حسب الحالة
        running_modules = self.module_manager.get_modules_by_state(
            ModuleState.RUNNING)
        stopped_modules = self.module_manager.get_modules_by_state(
            ModuleState.STOPPED)

        self.assertEqual(len(running_modules), 2)
        self.assertEqual(len(stopped_modules), 3)
        self.assertIn("module1", running_modules)
        self.assertIn("module2", running_modules)
        self.assertIn("module3", stopped_modules)
        self.assertIn("module4", stopped_modules)
        self.assertIn("module5", stopped_modules)

    def test_get_modules_by_priority(self):
        """
        اختبار الحصول على المديولات حسب الأولوية.
        """
        # الحصول على المديولات حسب الأولوية
        high_priority_modules = self.module_manager.get_modules_by_priority(
            priority_min=4)
        low_priority_modules = self.module_manager.get_modules_by_priority(
            priority_max=2)

        self.assertEqual(len(high_priority_modules), 2)
        self.assertEqual(len(low_priority_modules), 2)
        self.assertIn("module4", high_priority_modules)
        self.assertIn("module5", high_priority_modules)
        self.assertIn("module1", low_priority_modules)
        self.assertIn("module2", low_priority_modules)

    def tearDown(self):
        """
        تنظيف الاختبار.
        """
        # إيقاف تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            if mock_module.is_running is not None:
                mock_module.stop()


class PriorityDeterminerTest(unittest.TestCase):
    """
    اختبار محدد الأولويات.
    """

    def setUp(self):
        """
        إعداد الاختبار.
        """
        self.module_manager = ModuleManager()
        self.mock_modules = {}

        # إنشاء مديولات وهمية
        for i in range(1, 6):
            module_id = f"module{i}"
            module_name = f"مديول {i}"
            module_priority = i
            mock_module = MockModule(module_id, module_name, module_priority)
            self.mock_modules[module_id] = mock_module

            # تسجيل المديول في مدير المديولات
            self.module_manager.register_module(ModuleInfo(
                module_id=module_id,
                name=module_name,
                description=f"وصف مديول {i}",
                priority=module_priority
            ))

        # بدء تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            self.module_manager.register_startup_callback(
                module_id, mock_module.start)
            self.module_manager.start_module(module_id)

        # إنشاء محدد الأولويات
        self.priority_determiner = PriorityDeterminer(self.module_manager)

    def test_determine_modules_to_shutdown(self):
        """
        اختبار تحديد المديولات المراد إيقافها.
        """
        # تحديد المديولات المراد إيقافها
        modules_to_shutdown = self.priority_determiner.determine_modules_to_shutdown(
            reason=ShutdownReason.RESOURCE_CRITICAL, count=2)

        # التحقق من عدد المديولات المراد إيقافها
        self.assertEqual(len(modules_to_shutdown), 2)

        # التحقق من أن المديولات المراد إيقافها هي الأقل أولوية
        self.assertIn("module1", modules_to_shutdown)
        self.assertIn("module2", modules_to_shutdown)

    def test_determine_modules_to_shutdown_by_resource(self):
        """
        اختبار تحديد المديولات المراد إيقافها حسب الموارد.
        """
        # تحديث موارد المديولات
        self.mock_modules["module3"].update_resources(
            {AIResourceType.CPU: 80.0})
        self.mock_modules["module4"].update_resources(
            {AIResourceType.MEMORY: 90.0})

        # تحديد المديولات المراد إيقافها حسب الموارد
        modules_to_shutdown = self.priority_determiner.determine_modules_to_shutdown_by_resource(
            reason=ShutdownReason.RESOURCE_CRITICAL, resource_type=AIResourceType.CPU, threshold=70.0)

        # التحقق من عدد المديولات المراد إيقافها
        self.assertEqual(len(modules_to_shutdown), 1)

        # التحقق من أن المديولات المراد إيقافها هي التي تتجاوز العتبة
        self.assertIn("module3", modules_to_shutdown)

    def test_determine_modules_to_shutdown_by_priority(self):
        """
        اختبار تحديد المديولات المراد إيقافها حسب الأولوية.
        """
        # تحديد المديولات المراد إيقافها حسب الأولوية
        modules_to_shutdown = self.priority_determiner.determine_modules_to_shutdown_by_priority(
            reason=ShutdownReason.RESOURCE_CRITICAL, priority_max=3)

        # التحقق من عدد المديولات المراد إيقافها
        self.assertEqual(len(modules_to_shutdown), 3)

        # التحقق من أن المديولات المراد إيقافها هي الأقل أولوية
        self.assertIn("module1", modules_to_shutdown)
        self.assertIn("module2", modules_to_shutdown)
        self.assertIn("module3", modules_to_shutdown)

    def tearDown(self):
        """
        تنظيف الاختبار.
        """
        # إيقاف تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            if mock_module.is_running is not None:
                mock_module.stop()


class SafeShutdownExecutorTest(unittest.TestCase):
    """
    اختبار منفذ الإغلاق الآمن.
    """

    def setUp(self):
        """
        إعداد الاختبار.
        """
        self.module_manager = ModuleManager()
        self.mock_modules = {}

        # إنشاء مديولات وهمية
        for i in range(1, 6):
            module_id = f"module{i}"
            module_name = f"مديول {i}"
            module_priority = i
            mock_module = MockModule(module_id, module_name, module_priority)
            self.mock_modules[module_id] = mock_module

            # تسجيل المديول في مدير المديولات
            self.module_manager.register_module(ModuleInfo(
                module_id=module_id,
                name=module_name,
                description=f"وصف مديول {i}",
                priority=module_priority
            ))

        # بدء تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            self.module_manager.register_startup_callback(
                module_id, mock_module.start)
            self.module_manager.register_shutdown_callback(
                module_id, mock_module.stop)
            self.module_manager.register_pause_callback(
                module_id, mock_module.pause)
            self.module_manager.register_resume_callback(
                module_id, mock_module.resume)
            self.module_manager.start_module(module_id)

        # إنشاء محدد الأولويات
        self.priority_determiner = PriorityDeterminer(self.module_manager)

        # إنشاء منفذ الإغلاق الآمن
        self.shutdown_executor = SafeShutdownExecutor(
            self.module_manager, self.priority_determiner)

    def test_shutdown_module(self):
        """
        اختبار إيقاف تشغيل المديول.
        """
        module_id = "module1"

        # إيقاف تشغيل المديول
        self.assertTrue(self.shutdown_executor.shutdown_module(
            module_id=module_id,
            strategy=ShutdownStrategy.GRACEFUL,
            reason=ShutdownReason.MANUAL
        ))

        # التحقق من حالة المديول
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.STOPPED)
        self.assertFalse(self.mock_modules[module_id].is_running)

    def test_shutdown_modules(self):
        """
        اختبار إيقاف تشغيل مجموعة من المديولات.
        """
        module_ids = ["module1", "module2"]

        # إيقاف تشغيل المديولات
        self.assertTrue(self.shutdown_executor.shutdown_modules(
            module_ids=module_ids,
            strategy=ShutdownStrategy.GRACEFUL,
            reason=ShutdownReason.MANUAL
        ))

        # التحقق من حالة المديولات
        for module_id in module_ids:
            self.assertEqual(
                self.module_manager.modules[module_id].state,
                ModuleState.STOPPED)
            self.assertFalse(self.mock_modules[module_id].is_running)

    def test_shutdown_modules_by_priority(self):
        """
        اختبار إيقاف تشغيل المديولات حسب الأولوية.
        """
        # إيقاف تشغيل المديولات حسب الأولوية
        self.assertTrue(self.shutdown_executor.shutdown_modules_by_priority(
            priority_max=2,
            strategy=ShutdownStrategy.GRACEFUL,
            reason=ShutdownReason.RESOURCE_CRITICAL
        ))

        # التحقق من حالة المديولات
        self.assertEqual(
            self.module_manager.modules["module1"].state,
            ModuleState.STOPPED)
        self.assertEqual(
            self.module_manager.modules["module2"].state,
            ModuleState.STOPPED)
        self.assertEqual(
            self.module_manager.modules["module3"].state,
            ModuleState.RUNNING)
        self.assertEqual(
            self.module_manager.modules["module4"].state,
            ModuleState.RUNNING)
        self.assertEqual(
            self.module_manager.modules["module5"].state,
            ModuleState.RUNNING)

    def test_suspend_resume_module(self):
        """
        اختبار تعليق واستئناف المديول.
        """
        module_id = "module3"

        # تعليق المديول
        self.assertTrue(self.shutdown_executor.suspend_module(
            module_id=module_id,
            strategy=ShutdownStrategy.GRACEFUL,
            reason=ShutdownReason.RESOURCE_CRITICAL
        ))

        # التحقق من حالة المديول
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.PAUSED)
        self.assertTrue(self.mock_modules[module_id].is_paused)

        # استئناف المديول
        self.assertTrue(self.shutdown_executor.resume_module(module_id))

        # التحقق من حالة المديول
        self.assertEqual(
            self.module_manager.modules[module_id].state,
            ModuleState.RUNNING)
        self.assertFalse(self.mock_modules[module_id].is_paused)

    def tearDown(self):
        """
        تنظيف الاختبار.
        """
        # إيقاف تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            if mock_module.is_running is not None:
                mock_module.stop()


class AIResourceMonitorTest(unittest.TestCase):
    """
    اختبار مراقب موارد الذكاء الصناعي.
    """

    def setUp(self):
        """
        إعداد الاختبار.
        """
        self.module_manager = ModuleManager()
        self.mock_modules = {}

        # إنشاء مديولات وهمية
        for i in range(1, 6):
            module_id = f"module{i}"
            module_name = f"مديول {i}"
            module_priority = i
            mock_module = MockModule(module_id, module_name, module_priority)
            self.mock_modules[module_id] = mock_module

            # تسجيل المديول في مدير المديولات
            self.module_manager.register_module(ModuleInfo(
                module_id=module_id,
                name=module_name,
                description=f"وصف مديول {i}",
                priority=module_priority
            ))

        # بدء تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            self.module_manager.register_startup_callback(
                module_id, mock_module.start)
            self.module_manager.register_shutdown_callback(
                module_id, mock_module.stop)
            self.module_manager.register_pause_callback(
                module_id, mock_module.pause)
            self.module_manager.register_resume_callback(
                module_id, mock_module.resume)
            self.module_manager.start_module(module_id)

        # إنشاء محدد الأولويات
        self.priority_determiner = PriorityDeterminer(self.module_manager)

        # إنشاء منفذ الإغلاق الآمن
        self.shutdown_executor = SafeShutdownExecutor(
            self.module_manager, self.priority_determiner)

        # إنشاء مراقب موارد الذكاء الصناعي
        self.resource_monitor = AIResourceMonitor(
            module_manager=self.module_manager,
            priority_determiner=self.priority_determiner,
            shutdown_executor=self.shutdown_executor
        )

    def test_register_ai_module(self):
        """
        اختبار تسجيل مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.assertTrue(self.resource_monitor.register_ai_module(
            ai_module_id="ai_module1",
            name="مديول الذكاء الصناعي الأول"
        ))

        # التحقق من تسجيل مديول الذكاء الصناعي
        self.assertIn("ai_module1", self.resource_monitor.ai_resources)
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module1"].name,
            "مديول الذكاء الصناعي الأول")

    def test_update_ai_module_resources(self):
        """
        اختبار تحديث موارد مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module2",
            name="مديول الذكاء الصناعي الثاني"
        )

        # تحديث موارد مديول الذكاء الصناعي
        self.assertTrue(self.resource_monitor.update_ai_module_resources(
            ai_module_id="ai_module2",
            resources={
                AIResourceType.CPU: 50.0,
                AIResourceType.MEMORY: 60.0,
                AIResourceType.GPU: 70.0
            }
        ))

        # التحقق من تحديث موارد مديول الذكاء الصناعي
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module2"].resources[AIResourceType.CPU], 50.0)
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module2"].resources[AIResourceType.MEMORY], 60.0)
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module2"].resources[AIResourceType.GPU], 70.0)

    def test_update_ai_module_limits(self):
        """
        اختبار تحديث حدود موارد مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module3",
            name="مديول الذكاء الصناعي الثالث"
        )

        # تحديث حدود موارد مديول الذكاء الصناعي
        self.assertTrue(self.resource_monitor.update_ai_module_limits(
            ai_module_id="ai_module3",
            limits={
                AIResourceType.CPU: 90.0,
                AIResourceType.MEMORY: 90.0,
                AIResourceType.GPU: 90.0
            }
        ))

        # التحقق من تحديث حدود موارد مديول الذكاء الصناعي
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module3"].limits[AIResourceType.CPU], 90.0)
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module3"].limits[AIResourceType.MEMORY], 90.0)
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module3"].limits[AIResourceType.GPU], 90.0)

    def test_get_ai_module_resources(self):
        """
        اختبار الحصول على موارد مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module4",
            name="مديول الذكاء الصناعي الرابع"
        )

        # تحديث موارد مديول الذكاء الصناعي
        self.resource_monitor.update_ai_module_resources(
            ai_module_id="ai_module4",
            resources={
                AIResourceType.CPU: 50.0,
                AIResourceType.MEMORY: 60.0,
                AIResourceType.GPU: 70.0
            }
        )

        # الحصول على موارد مديول الذكاء الصناعي
        resources = self.resource_monitor.get_ai_module_resources("ai_module4")

        # التحقق من موارد مديول الذكاء الصناعي
        self.assertIsNotNone(resources)
        self.assertEqual(resources["ai_module_id"], "ai_module4")
        self.assertEqual(resources["name"], "مديول الذكاء الصناعي الرابع")
        self.assertEqual(resources["resources"][AIResourceType.CPU], 50.0)
        self.assertEqual(resources["resources"][AIResourceType.MEMORY], 60.0)
        self.assertEqual(resources["resources"][AIResourceType.GPU], 70.0)

    def test_get_all_ai_module_resources(self):
        """
        اختبار الحصول على موارد جميع مديولات الذكاء الصناعي.
        """
        # تسجيل مديولات الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module5",
            name="مديول الذكاء الصناعي الخامس"
        )
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module6",
            name="مديول الذكاء الصناعي السادس"
        )

        # الحصول على موارد جميع مديولات الذكاء الصناعي
        resources = self.resource_monitor.get_all_ai_module_resources()

        # التحقق من موارد جميع مديولات الذكاء الصناعي
        self.assertEqual(len(resources), 2)
        self.assertIn("ai_module5", resources)
        self.assertIn("ai_module6", resources)

    def test_update_token_usage(self):
        """
        اختبار تحديث استهلاك الرموز.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module7",
            name="مديول الذكاء الصناعي السابع"
        )

        # تحديث استهلاك الرموز
        self.assertTrue(self.resource_monitor.update_token_usage(
            ai_module_id="ai_module7",
            tokens=1000
        ))

        # التحقق من تحديث استهلاك الرموز
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module7"].resources[AIResourceType.TOKENS], 1000)

        # تحديث استهلاك الرموز مرة أخرى
        self.assertTrue(self.resource_monitor.update_token_usage(
            ai_module_id="ai_module7",
            tokens=500
        ))

        # التحقق من تحديث استهلاك الرموز
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module7"].resources[AIResourceType.TOKENS], 1500)

    def test_update_api_calls(self):
        """
        اختبار تحديث استدعاءات واجهة برمجة التطبيقات.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module8",
            name="مديول الذكاء الصناعي الثامن"
        )

        # تحديث استدعاءات واجهة برمجة التطبيقات
        self.assertTrue(self.resource_monitor.update_api_calls(
            ai_module_id="ai_module8",
            calls=100
        ))

        # التحقق من تحديث استدعاءات واجهة برمجة التطبيقات
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module8"].resources[AIResourceType.API_CALLS], 100)

        # تحديث استدعاءات واجهة برمجة التطبيقات مرة أخرى
        self.assertTrue(self.resource_monitor.update_api_calls(
            ai_module_id="ai_module8",
            calls=50
        ))

        # التحقق من تحديث استدعاءات واجهة برمجة التطبيقات
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module8"].resources[AIResourceType.API_CALLS], 150)

    def test_reset_token_usage(self):
        """
        اختبار إعادة تعيين استهلاك الرموز.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module9",
            name="مديول الذكاء الصناعي التاسع"
        )

        # تحديث استهلاك الرموز
        self.resource_monitor.update_token_usage(
            ai_module_id="ai_module9",
            tokens=1000
        )

        # إعادة تعيين استهلاك الرموز
        self.assertTrue(self.resource_monitor.reset_token_usage("ai_module9"))

        # التحقق من إعادة تعيين استهلاك الرموز
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module9"].resources[AIResourceType.TOKENS], 0)

    def test_reset_api_calls(self):
        """
        اختبار إعادة تعيين استدعاءات واجهة برمجة التطبيقات.
        """
        # تسجيل مديول الذكاء الصناعي
        self.resource_monitor.register_ai_module(
            ai_module_id="ai_module10",
            name="مديول الذكاء الصناعي العاشر"
        )

        # تحديث استدعاءات واجهة برمجة التطبيقات
        self.resource_monitor.update_api_calls(
            ai_module_id="ai_module10",
            calls=100
        )

        # إعادة تعيين استدعاءات واجهة برمجة التطبيقات
        self.assertTrue(self.resource_monitor.reset_api_calls("ai_module10"))

        # التحقق من إعادة تعيين استدعاءات واجهة برمجة التطبيقات
        self.assertEqual(
            self.resource_monitor.ai_resources["ai_module10"].resources[AIResourceType.API_CALLS], 0)

    def tearDown(self):
        """
        تنظيف الاختبار.
        """
        # إيقاف تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            if mock_module.is_running is not None:
                mock_module.stop()

        # إيقاف المراقبة
        if self.resource_monitor.is_monitoring:
            self.resource_monitor.stop_monitoring()


class AISuspensionManagerTest(unittest.TestCase):
    """
    اختبار مدير التعليق والاستئناف.
    """

    def setUp(self):
        """
        إعداد الاختبار.
        """
        self.module_manager = ModuleManager()
        self.mock_modules = {}

        # إنشاء مديولات وهمية
        for i in range(1, 6):
            module_id = f"module{i}"
            module_name = f"مديول {i}"
            module_priority = i
            mock_module = MockModule(module_id, module_name, module_priority)
            self.mock_modules[module_id] = mock_module

            # تسجيل المديول في مدير المديولات
            self.module_manager.register_module(ModuleInfo(
                module_id=module_id,
                name=module_name,
                description=f"وصف مديول {i}",
                priority=module_priority
            ))

        # بدء تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            self.module_manager.register_startup_callback(
                module_id, mock_module.start)
            self.module_manager.register_shutdown_callback(
                module_id, mock_module.stop)
            self.module_manager.register_pause_callback(
                module_id, mock_module.pause)
            self.module_manager.register_resume_callback(
                module_id, mock_module.resume)
            self.module_manager.start_module(module_id)

        # إنشاء محدد الأولويات
        self.priority_determiner = PriorityDeterminer(self.module_manager)

        # إنشاء منفذ الإغلاق الآمن
        self.shutdown_executor = SafeShutdownExecutor(
            self.module_manager, self.priority_determiner)

        # إنشاء مراقب موارد الذكاء الصناعي
        self.resource_monitor = AIResourceMonitor(
            module_manager=self.module_manager,
            priority_determiner=self.priority_determiner,
            shutdown_executor=self.shutdown_executor
        )

        # إنشاء مدير التعليق والاستئناف
        self.suspension_manager = AISuspensionManager(
            module_manager=self.module_manager,
            priority_determiner=self.priority_determiner,
            shutdown_executor=self.shutdown_executor,
            resource_monitor=self.resource_monitor
        )

    def test_register_ai_module(self):
        """
        اختبار تسجيل مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.assertTrue(self.suspension_manager.register_ai_module(
            ai_module_id="ai_module1",
            name="مديول الذكاء الصناعي الأول"
        ))

        # التحقق من تسجيل مديول الذكاء الصناعي
        self.assertIn("ai_module1", self.suspension_manager.ai_suspensions)
        self.assertEqual(
            self.suspension_manager.ai_suspensions["ai_module1"].name,
            "مديول الذكاء الصناعي الأول")

    def test_suspend_resume_ai_module(self):
        """
        اختبار تعليق واستئناف مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module2",
            name="مديول الذكاء الصناعي الثاني"
        )

        # تعليق مديول الذكاء الصناعي
        self.assertTrue(self.suspension_manager.suspend_ai_module(
            ai_module_id="ai_module2",
            reason=SuspensionReason.MANUAL,
            strategy=SuspensionStrategy.GRACEFUL
        ))

        # التحقق من حالة مديول الذكاء الصناعي
        self.assertEqual(
            self.suspension_manager.ai_suspensions["ai_module2"].state,
            SuspensionState.SUSPENDED)

        # استئناف مديول الذكاء الصناعي
        self.assertTrue(self.suspension_manager.resume_ai_module("ai_module2"))

        # التحقق من حالة مديول الذكاء الصناعي
        self.assertEqual(
            self.suspension_manager.ai_suspensions["ai_module2"].state,
            SuspensionState.ACTIVE)

    def test_get_ai_module_suspension(self):
        """
        اختبار الحصول على بيانات تعليق مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module3",
            name="مديول الذكاء الصناعي الثالث"
        )

        # تعليق مديول الذكاء الصناعي
        self.suspension_manager.suspend_ai_module(
            ai_module_id="ai_module3",
            reason=SuspensionReason.MANUAL,
            strategy=SuspensionStrategy.GRACEFUL
        )

        # الحصول على بيانات تعليق مديول الذكاء الصناعي
        suspension_data = self.suspension_manager.get_ai_module_suspension(
            "ai_module3")

        # التحقق من بيانات تعليق مديول الذكاء الصناعي
        self.assertIsNotNone(suspension_data)
        self.assertEqual(suspension_data["ai_module_id"], "ai_module3")
        self.assertEqual(
            suspension_data["name"],
            "مديول الذكاء الصناعي الثالث")
        self.assertEqual(suspension_data["state"], SuspensionState.SUSPENDED)
        self.assertEqual(suspension_data["reason"], SuspensionReason.MANUAL)
        self.assertEqual(
            suspension_data["strategy"],
            SuspensionStrategy.GRACEFUL)

    def test_get_all_ai_module_suspensions(self):
        """
        اختبار الحصول على بيانات تعليق جميع مديولات الذكاء الصناعي.
        """
        # تسجيل مديولات الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module4",
            name="مديول الذكاء الصناعي الرابع"
        )
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module5",
            name="مديول الذكاء الصناعي الخامس"
        )

        # الحصول على بيانات تعليق جميع مديولات الذكاء الصناعي
        suspensions = self.suspension_manager.get_all_ai_module_suspensions()

        # التحقق من بيانات تعليق جميع مديولات الذكاء الصناعي
        self.assertEqual(len(suspensions), 2)
        self.assertIn("ai_module4", suspensions)
        self.assertIn("ai_module5", suspensions)

    def test_get_suspension_history(self):
        """
        اختبار الحصول على سجل التعليق.
        """
        # تسجيل مديول الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module6",
            name="مديول الذكاء الصناعي السادس"
        )

        # تعليق مديول الذكاء الصناعي
        self.suspension_manager.suspend_ai_module(
            ai_module_id="ai_module6",
            reason=SuspensionReason.MANUAL,
            strategy=SuspensionStrategy.GRACEFUL
        )

        # استئناف مديول الذكاء الصناعي
        self.suspension_manager.resume_ai_module("ai_module6")

        # الحصول على سجل التعليق
        history = self.suspension_manager.get_suspension_history()

        # التحقق من سجل التعليق
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["ai_module_id"], "ai_module6")
        self.assertEqual(history[0]["new_state"], SuspensionState.SUSPENDED)
        self.assertEqual(history[1]["ai_module_id"], "ai_module6")
        self.assertEqual(history[1]["new_state"], SuspensionState.ACTIVE)

    def test_get_ai_modules_by_state(self):
        """
        اختبار الحصول على مديولات الذكاء الصناعي حسب الحالة.
        """
        # تسجيل مديولات الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module7",
            name="مديول الذكاء الصناعي السابع"
        )
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module8",
            name="مديول الذكاء الصناعي الثامن"
        )

        # تعليق مديول الذكاء الصناعي
        self.suspension_manager.suspend_ai_module(
            ai_module_id="ai_module7",
            reason=SuspensionReason.MANUAL,
            strategy=SuspensionStrategy.GRACEFUL
        )

        # الحصول على مديولات الذكاء الصناعي حسب الحالة
        active_modules = self.suspension_manager.get_ai_modules_by_state(
            SuspensionState.ACTIVE)
        suspended_modules = self.suspension_manager.get_ai_modules_by_state(
            SuspensionState.SUSPENDED)

        # التحقق من مديولات الذكاء الصناعي حسب الحالة
        self.assertEqual(len(active_modules), 1)
        self.assertEqual(len(suspended_modules), 1)
        self.assertIn("ai_module8", active_modules)
        self.assertIn("ai_module7", suspended_modules)

    def test_get_suspension_stats(self):
        """
        اختبار الحصول على إحصائيات التعليق.
        """
        # تسجيل مديولات الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module9",
            name="مديول الذكاء الصناعي التاسع"
        )
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module10",
            name="مديول الذكاء الصناعي العاشر"
        )

        # تعليق مديول الذكاء الصناعي
        self.suspension_manager.suspend_ai_module(
            ai_module_id="ai_module9",
            reason=SuspensionReason.MANUAL,
            strategy=SuspensionStrategy.GRACEFUL
        )

        # الحصول على إحصائيات التعليق
        stats = self.suspension_manager.get_suspension_stats()

        # التحقق من إحصائيات التعليق
        self.assertEqual(stats["total_suspensions"], 1)
        self.assertEqual(stats["active_modules"], 1)
        self.assertEqual(stats["suspended_modules"], 1)
        self.assertEqual(
            stats["suspension_reasons"].get(
                SuspensionReason.MANUAL, 0), 1)
        self.assertEqual(
            stats["suspension_strategies"].get(
                SuspensionStrategy.GRACEFUL, 0), 1)

    def test_schedule_suspension(self):
        """
        اختبار جدولة تعليق مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module11",
            name="مديول الذكاء الصناعي الحادي عشر"
        )

        # جدولة تعليق مديول الذكاء الصناعي
        suspend_at = datetime.now() + timedelta(hours=1)
        resume_at = datetime.now() + timedelta(hours=2)
        self.assertTrue(self.suspension_manager.schedule_suspension(
            ai_module_id="ai_module11",
            suspend_at=suspend_at,
            resume_at=resume_at,
            reason=SuspensionReason.SCHEDULED,
            strategy=SuspensionStrategy.GRACEFUL
        ))

        # الحصول على مهام التعليق المجدولة
        scheduled_suspensions = self.suspension_manager.get_scheduled_suspensions(
            "ai_module11")

        # التحقق من مهام التعليق المجدولة
        self.assertEqual(len(scheduled_suspensions), 1)
        self.assertEqual(
            scheduled_suspensions[0]["ai_module_id"],
            "ai_module11")
        self.assertEqual(
            scheduled_suspensions[0]["reason"],
            SuspensionReason.SCHEDULED)
        self.assertEqual(
            scheduled_suspensions[0]["strategy"],
            SuspensionStrategy.GRACEFUL)

    def test_cancel_scheduled_suspension(self):
        """
        اختبار إلغاء جدولة تعليق مديول الذكاء الصناعي.
        """
        # تسجيل مديول الذكاء الصناعي
        self.suspension_manager.register_ai_module(
            ai_module_id="ai_module12",
            name="مديول الذكاء الصناعي الثاني عشر"
        )

        # جدولة تعليق مديول الذكاء الصناعي
        suspend_at = datetime.now() + timedelta(hours=1)
        resume_at = datetime.now() + timedelta(hours=2)
        self.suspension_manager.schedule_suspension(
            ai_module_id="ai_module12",
            suspend_at=suspend_at,
            resume_at=resume_at,
            reason=SuspensionReason.SCHEDULED,
            strategy=SuspensionStrategy.GRACEFUL
        )

        # إلغاء جدولة تعليق مديول الذكاء الصناعي
        self.assertTrue(
            self.suspension_manager.cancel_scheduled_suspension("ai_module12"))

        # الحصول على مهام التعليق المجدولة
        scheduled_suspensions = self.suspension_manager.get_scheduled_suspensions(
            "ai_module12")

        # التحقق من مهام التعليق المجدولة
        self.assertEqual(len(scheduled_suspensions), 0)

    def tearDown(self):
        """
        تنظيف الاختبار.
        """
        # إيقاف تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            if mock_module.is_running is not None:
                mock_module.stop()

        # إيقاف المراقبة
        if self.resource_monitor.is_monitoring:
            self.resource_monitor.stop_monitoring()

        if self.suspension_manager.is_monitoring:
            self.suspension_manager.stop_monitoring()


class IntegrationTest(unittest.TestCase):
    """
    اختبار تكامل جميع المكونات.
    """

    def setUp(self):
        """
        إعداد الاختبار.
        """
        self.module_manager = ModuleManager()
        self.mock_modules = {}

        # إنشاء مديولات وهمية
        for i in range(1, 6):
            module_id = f"module{i}"
            module_name = f"مديول {i}"
            module_priority = i
            mock_module = MockModule(module_id, module_name, module_priority)
            self.mock_modules[module_id] = mock_module

            # تسجيل المديول في مدير المديولات
            self.module_manager.register_module(ModuleInfo(
                module_id=module_id,
                name=module_name,
                description=f"وصف مديول {i}",
                priority=module_priority
            ))

        # بدء تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            self.module_manager.register_startup_callback(
                module_id, mock_module.start)
            self.module_manager.register_shutdown_callback(
                module_id, mock_module.stop)
            self.module_manager.register_pause_callback(
                module_id, mock_module.pause)
            self.module_manager.register_resume_callback(
                module_id, mock_module.resume)
            self.module_manager.start_module(module_id)

        # إنشاء محدد الأولويات
        self.priority_determiner = PriorityDeterminer(self.module_manager)

        # إنشاء منفذ الإغلاق الآمن
        self.shutdown_executor = SafeShutdownExecutor(
            self.module_manager, self.priority_determiner)

        # إنشاء مراقب موارد الذكاء الصناعي
        self.resource_monitor = AIResourceMonitor(
            module_manager=self.module_manager,
            priority_determiner=self.priority_determiner,
            shutdown_executor=self.shutdown_executor
        )

        # إنشاء مدير التعليق والاستئناف
        self.suspension_manager = AISuspensionManager(
            module_manager=self.module_manager,
            priority_determiner=self.priority_determiner,
            shutdown_executor=self.shutdown_executor,
            resource_monitor=self.resource_monitor
        )

        # تسجيل مديولات الذكاء الصناعي
        for i in range(1, 6):
            ai_module_id = f"ai_module{i}"
            ai_module_name = f"مديول الذكاء الصناعي {i}"
            self.resource_monitor.register_ai_module(
                ai_module_id, ai_module_name)
            self.suspension_manager.register_ai_module(
                ai_module_id, ai_module_name)

    def test_resource_critical_to_suspension(self):
        """
        اختبار تحويل حالة الموارد الحرجة إلى تعليق.
        """
        ai_module_id = "ai_module1"

        # تسجيل دالة استدعاء للتنبيهات
        alert_callback_called = False

        def alert_callback(module_id, status, alert):
            nonlocal alert_callback_called
            alert_callback_called = True
            # تعليق مديول الذكاء الصناعي
            self.suspension_manager.suspend_ai_module(
                ai_module_id=module_id,
                reason=SuspensionReason.RESOURCE_CRITICAL,
                strategy=SuspensionStrategy.GRACEFUL
            )

        self.resource_monitor.register_alert_callback(
            ResourceAlert.CRITICAL, alert_callback)

        # تحديث موارد مديول الذكاء الصناعي
        self.resource_monitor.update_ai_module_resources(
            ai_module_id=ai_module_id,
            resources={
                AIResourceType.CPU: 90.0,
                AIResourceType.MEMORY: 90.0,
                AIResourceType.GPU: 90.0
            }
        )

        # التحقق من تنفيذ دالة الاستدعاء
        self.assertTrue(alert_callback_called)

        # التحقق من حالة مديول الذكاء الصناعي
        self.assertEqual(
            self.suspension_manager.ai_suspensions[ai_module_id].state,
            SuspensionState.SUSPENDED)

    def test_shutdown_modules_by_priority_when_resources_critical(self):
        """
        اختبار إيقاف تشغيل المديولات حسب الأولوية عند حالة الموارد الحرجة.
        """
        # تحديد المديولات المراد إيقافها
        modules_to_shutdown = self.priority_determiner.determine_modules_to_shutdown_by_priority(
            priority_max=2, reason=ShutdownReason.RESOURCE_CRITICAL)

        # إيقاف تشغيل المديولات
        self.shutdown_executor.shutdown_modules(
            module_ids=modules_to_shutdown,
            strategy=ShutdownStrategy.GRACEFUL,
            reason=ShutdownReason.RESOURCE_CRITICAL
        )

        # التحقق من حالة المديولات
        self.assertEqual(
            self.module_manager.modules["module1"].state,
            ModuleState.STOPPED)
        self.assertEqual(
            self.module_manager.modules["module2"].state,
            ModuleState.STOPPED)
        self.assertEqual(
            self.module_manager.modules["module3"].state,
            ModuleState.RUNNING)
        self.assertEqual(
            self.module_manager.modules["module4"].state,
            ModuleState.RUNNING)
        self.assertEqual(
            self.module_manager.modules["module5"].state,
            ModuleState.RUNNING)

    def test_auto_resume_suspended_ai_module(self):
        """
        اختبار الاستئناف التلقائي لمديول الذكاء الصناعي المعلق.
        """
        ai_module_id = "ai_module2"

        # تعليق مديول الذكاء الصناعي
        self.suspension_manager.suspend_ai_module(
            ai_module_id=ai_module_id,
            reason=SuspensionReason.MANUAL,
            strategy=SuspensionStrategy.GRACEFUL,
            resume_after=1  # استئناف بعد ثانية واحدة
        )

        # التحقق من حالة مديول الذكاء الصناعي
        self.assertEqual(
            self.suspension_manager.ai_suspensions[ai_module_id].state,
            SuspensionState.SUSPENDED)

        # بدء المراقبة
        self.suspension_manager.start_monitoring()

        # انتظار الاستئناف التلقائي
        time.sleep(2)

        # التحقق من حالة مديول الذكاء الصناعي
        self.assertEqual(
            self.suspension_manager.ai_suspensions[ai_module_id].state,
            SuspensionState.ACTIVE)

        # إيقاف المراقبة
        self.suspension_manager.stop_monitoring()

    def test_resource_monitoring_and_suspension(self):
        """
        اختبار مراقبة الموارد والتعليق.
        """
        ai_module_id = "ai_module3"

        # تسجيل دالة استدعاء للتنبيهات
        alert_callback_called = False

        def alert_callback(module_id, status, alert):
            nonlocal alert_callback_called
            alert_callback_called = True

        self.resource_monitor.register_alert_callback(
            ResourceAlert.CRITICAL, alert_callback)

        # تسجيل دالة استدعاء للتعليق
        suspension_callback_called = False

        def suspension_callback(module_id, state, suspension_data):
            nonlocal suspension_callback_called
            suspension_callback_called = True

        self.suspension_manager.register_suspension_callback(
            SuspensionState.SUSPENDED, suspension_callback)

        # تحديث موارد مديول الذكاء الصناعي
        self.resource_monitor.update_ai_module_resources(
            ai_module_id=ai_module_id,
            resources={
                AIResourceType.CPU: 90.0,
                AIResourceType.MEMORY: 90.0,
                AIResourceType.GPU: 90.0
            }
        )

        # التحقق من تنفيذ دالة الاستدعاء للتنبيهات
        self.assertTrue(alert_callback_called)

        # تعليق مديول الذكاء الصناعي
        self.suspension_manager.suspend_ai_module(
            ai_module_id=ai_module_id,
            reason=SuspensionReason.RESOURCE_CRITICAL,
            strategy=SuspensionStrategy.GRACEFUL
        )

        # التحقق من تنفيذ دالة الاستدعاء للتعليق
        self.assertTrue(suspension_callback_called)

        # التحقق من حالة مديول الذكاء الصناعي
        self.assertEqual(
            self.suspension_manager.ai_suspensions[ai_module_id].state,
            SuspensionState.SUSPENDED)

    def tearDown(self):
        """
        تنظيف الاختبار.
        """
        # إيقاف تشغيل جميع المديولات
        for module_id, mock_module in self.mock_modules.items():
            if mock_module.is_running is not None:
                mock_module.stop()

        # إيقاف المراقبة
        if self.resource_monitor.is_monitoring:
            self.resource_monitor.stop_monitoring()

        if self.suspension_manager.is_monitoring:
            self.suspension_manager.stop_monitoring()


if __name__ == "__main__":
    unittest.main()
