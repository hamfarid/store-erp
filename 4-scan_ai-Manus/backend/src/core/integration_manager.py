# File: /home/ubuntu/clean_project/src/core/integration_manager.py
"""
مدير التكامل الشامل - ربط جميع مكونات النظام
يدير التكامل بين الواجهة الأمامية والخلفية وجميع الخدمات المتقدمة
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from ..api.advanced_vision import AdvancedVisionAPI

# Import API modules
from ..api.generative_ai import GenerativeAIAPI
from ..api.model_management import ModelManagementAPI
from ..api.reports import ReportsAPI
from ..modules.ai_management.advanced_vision_service import AdvancedVisionService
from ..modules.ai_management.collaborative_ai_platform import CollaborativeAIPlatform
from ..modules.ai_management.distributed_ai_network import DistributedAINetwork
from ..modules.ai_management.generative_ai_service import GenerativeAIService
from ..modules.ai_management.predictive_diagnosis_system import (
    PredictiveDiagnosisSystem,
)
from ..modules.ai_management.smart_treatment_system import SmartTreatmentSystem

# Import all services
from ..services.memory_service import MemoryService
from .config import Config

# Import core modules
from .error_handling import ErrorHandler, ValidationError

logger = logging.getLogger(__name__)


class IntegrationManager:
    """
    مدير التكامل الشامل للنظام
    يدير جميع الخدمات والواجهات ويضمن التكامل السلس بينها
    """

    def __init__(self, config: Config):
        self.config = config
        self.error_handler = ErrorHandler()
        self.services = {}
        self.apis = {}
        self.status = {
            'system_status': 'initializing',
            'services_status': {},
            'apis_status': {},
            'last_health_check': None,
            'connected_nodes': 0,
            'total_models': 0
        }

        # Initialize logging
        self._setup_logging()

    def _setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/integration.log'),
                logging.StreamHandler()
            ]
        )

    async def initialize_system(self) -> Dict[str, Any]:
        """
        تهيئة النظام الكامل
        """
        try:
            logger.info("بدء تهيئة النظام الشامل...")

            # Initialize core services
            await self._initialize_core_services()

            # Initialize AI services
            await self._initialize_ai_services()

            # Initialize APIs
            await self._initialize_apis()

            # Setup service connections
            await self._setup_service_connections()

            # Perform initial health check
            await self._perform_health_check()

            self.status['system_status'] = 'active'
            logger.info("تم تهيئة النظام بنجاح")

            return {
                'success': True,
                'message': 'تم تهيئة النظام بنجاح',
                'status': self.status,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            error_info = self.error_handler.handle_error(
                e, 'system_initialization')
            self.status['system_status'] = 'error'
            logger.error(f"فشل في تهيئة النظام: {error_info['message']}")
            return {
                'success': False,
                'error': error_info,
                'status': self.status
            }

    async def _initialize_core_services(self):
        """تهيئة الخدمات الأساسية"""
        logger.info("تهيئة الخدمات الأساسية...")

        # Memory Service
        self.services['memory'] = MemoryService(self.config)
        await self.services['memory'].initialize()
        self.status['services_status']['memory'] = 'active'

        logger.info("تم تهيئة الخدمات الأساسية")

    async def _initialize_ai_services(self):
        """تهيئة خدمات الذكاء الاصطناعي"""
        logger.info("تهيئة خدمات الذكاء الاصطناعي...")

        # Generative AI Service
        self.services['generative_ai'] = GenerativeAIService(
            config=self.config,
            memory_service=self.services['memory']
        )
        await self.services['generative_ai'].initialize()
        self.status['services_status']['generative_ai'] = 'active'

        # Advanced Vision Service
        self.services['advanced_vision'] = AdvancedVisionService(
            config=self.config,
            memory_service=self.services['memory']
        )
        await self.services['advanced_vision'].initialize()
        self.status['services_status']['advanced_vision'] = 'active'

        # Collaborative AI Platform
        self.services['collaborative_ai'] = CollaborativeAIPlatform(
            config=self.config,
            memory_service=self.services['memory']
        )
        await self.services['collaborative_ai'].initialize()
        self.status['services_status']['collaborative_ai'] = 'active'

        # Predictive Diagnosis System
        self.services['predictive_diagnosis'] = PredictiveDiagnosisSystem(
            config=self.config,
            memory_service=self.services['memory'],
            vision_service=self.services['advanced_vision']
        )
        await self.services['predictive_diagnosis'].initialize()
        self.status['services_status']['predictive_diagnosis'] = 'active'

        # Smart Treatment System
        self.services['smart_treatment'] = SmartTreatmentSystem(
            config=self.config,
            memory_service=self.services['memory'],
            diagnosis_service=self.services['predictive_diagnosis']
        )
        await self.services['smart_treatment'].initialize()
        self.status['services_status']['smart_treatment'] = 'active'

        # Distributed AI Network
        self.services['distributed_ai'] = DistributedAINetwork(
            config=self.config,
            memory_service=self.services['memory'],
            collaborative_platform=self.services['collaborative_ai']
        )
        await self.services['distributed_ai'].initialize()
        self.status['services_status']['distributed_ai'] = 'active'

        logger.info("تم تهيئة خدمات الذكاء الاصطناعي")

    async def _initialize_apis(self):
        """تهيئة واجهات برمجة التطبيقات"""
        logger.info("تهيئة واجهات برمجة التطبيقات...")

        # Generative AI API
        self.apis['generative_ai'] = GenerativeAIAPI(
            generative_service=self.services['generative_ai']
        )
        self.status['apis_status']['generative_ai'] = 'active'

        # Advanced Vision API
        self.apis['advanced_vision'] = AdvancedVisionAPI(
            vision_service=self.services['advanced_vision']
        )
        self.status['apis_status']['advanced_vision'] = 'active'

        # Reports API
        self.apis['reports'] = ReportsAPI(
            services=self.services
        )
        self.status['apis_status']['reports'] = 'active'

        # Model Management API
        self.apis['model_management'] = ModelManagementAPI(
            services=self.services
        )
        self.status['apis_status']['model_management'] = 'active'

        logger.info("تم تهيئة واجهات برمجة التطبيقات")

    async def _setup_service_connections(self):
        """إعداد الاتصالات بين الخدمات"""
        logger.info("إعداد الاتصالات بين الخدمات...")

        # Connect services for data sharing
        connections = [
            # Memory service connections
            (self.services['generative_ai'], self.services['memory']),
            (self.services['advanced_vision'], self.services['memory']),
            (self.services['collaborative_ai'], self.services['memory']),

            # Cross-service connections
            (self.services['predictive_diagnosis'],
             self.services['advanced_vision']),
            (self.services['smart_treatment'],
             self.services['predictive_diagnosis']),
            (self.services['distributed_ai'],
             self.services['collaborative_ai']),
        ]

        for service1, service2 in connections:
            try:
                await self._establish_service_connection(service1, service2)
            except Exception as e:
                logger.warning(f"فشل في ربط الخدمات: {e}")

        logger.info("تم إعداد الاتصالات بين الخدمات")

    async def _establish_service_connection(self, service1, service2):
        """إنشاء اتصال بين خدمتين"""
        # Implementation for service-to-service communication
        # This would typically involve setting up message queues,
        # shared data structures, or event systems

    async def _perform_health_check(self):
        """فحص صحة النظام"""
        logger.info("إجراء فحص صحة النظام...")

        # Check all services
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'health_check'):
                    health = await service.health_check()
                    self.status['services_status'][service_name] = health.get(
                        'status', 'unknown')
                else:
                    self.status['services_status'][service_name] = 'active'
            except Exception as e:
                self.status['services_status'][service_name] = 'error'
                logger.warning(f"فشل فحص صحة الخدمة {service_name}: {e}")

        # Update system metrics
        await self._update_system_metrics()

        self.status['last_health_check'] = datetime.now().isoformat()
        logger.info("تم إجراء فحص صحة النظام")

    async def _update_system_metrics(self):
        """تحديث مقاييس النظام"""
        try:
            # Count connected nodes from distributed AI
            if 'distributed_ai' in self.services:
                nodes_info = await self.services['distributed_ai'].get_network_status()
                self.status['connected_nodes'] = nodes_info.get(
                    'connected_nodes', 0)

            # Count total available models
            total_models = 0
            if 'generative_ai' in self.services:
                gen_models = await self.services['generative_ai'].get_available_models()
                total_models += len(gen_models.get('models', []))

            if 'advanced_vision' in self.services:
                vision_models = await self.services['advanced_vision'].get_available_models()
                total_models += len(vision_models.get('models', []))

            self.status['total_models'] = total_models

        except Exception as e:
            logger.warning(f"فشل في تحديث مقاييس النظام: {e}")

    async def get_system_status(self) -> Dict[str, Any]:
        """الحصول على حالة النظام"""
        await self._perform_health_check()
        return {
            'success': True,
            'status': self.status,
            'timestamp': datetime.now().isoformat()
        }

    async def restart_service(self, service_name: str) -> Dict[str, Any]:
        """إعادة تشغيل خدمة معينة"""
        try:
            if service_name not in self.services:
                raise ValidationError(f"الخدمة غير موجودة: {service_name}")

            logger.info(f"إعادة تشغيل الخدمة: {service_name}")

            # Stop service
            if hasattr(self.services[service_name], 'stop'):
                await self.services[service_name].stop()

            # Restart service
            if hasattr(self.services[service_name], 'initialize'):
                await self.services[service_name].initialize()

            self.status['services_status'][service_name] = 'active'

            return {
                'success': True,
                'message': f'تم إعادة تشغيل الخدمة {service_name} بنجاح',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            error_info = self.error_handler.handle_error(
                e, f'restart_service_{service_name}')
            return {
                'success': False,
                'error': error_info
            }

    async def get_service_logs(
            self, service_name: str, lines: int = 100) -> Dict[str, Any]:
        """الحصول على سجلات خدمة معينة"""
        try:
            if service_name not in self.services:
                raise ValidationError(f"الخدمة غير موجودة: {service_name}")

            # Read service logs
            log_file = Path(f"logs/{service_name}.log")
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    recent_lines = all_lines[-lines:] if len(
                        all_lines) > lines else all_lines

                return {
                    'success': True,
                    'logs': ''.join(recent_lines),
                    'total_lines': len(all_lines),
                    'returned_lines': len(recent_lines)
                }
            else:
                return {
                    'success': True,
                    'logs': 'لا توجد سجلات متاحة',
                    'total_lines': 0,
                    'returned_lines': 0
                }

        except Exception as e:
            error_info = self.error_handler.handle_error(
                e, f'get_service_logs_{service_name}')
            return {
                'success': False,
                'error': error_info
            }

    async def backup_system_state(self) -> Dict[str, Any]:
        """إنشاء نسخة احتياطية من حالة النظام"""
        try:
            logger.info("إنشاء نسخة احتياطية من حالة النظام...")

            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'system_status': self.status,
                'services_config': {},
                'system_metrics': await self._collect_system_metrics()
            }

            # Collect service configurations
            for service_name, service in self.services.items():
                if hasattr(service, 'get_config'):
                    backup_data['services_config'][service_name] = await service.get_config()

            # Save backup
            backup_file = Path(
                f"backups/system_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            backup_file.parent.mkdir(exist_ok=True)

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)

            logger.info(f"تم إنشاء النسخة الاحتياطية: {backup_file}")

            return {
                'success': True,
                'message': 'تم إنشاء النسخة الاحتياطية بنجاح',
                'backup_file': str(backup_file),
                'timestamp': backup_data['timestamp']
            }

        except Exception as e:
            error_info = self.error_handler.handle_error(
                e, 'backup_system_state')
            return {
                'success': False,
                'error': error_info
            }

    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """جمع مقاييس النظام"""
        metrics = {
            'memory_usage': {},
            'model_performance': {},
            'api_statistics': {},
            'error_counts': {}
        }

        try:
            # Collect memory usage from services
            for service_name, service in self.services.items():
                if hasattr(service, 'get_memory_usage'):
                    metrics['memory_usage'][service_name] = await service.get_memory_usage()

            # Collect model performance metrics
            if 'generative_ai' in self.services:
                gen_metrics = await self.services['generative_ai'].get_performance_metrics()
                metrics['model_performance']['generative_ai'] = gen_metrics

            if 'advanced_vision' in self.services:
                vision_metrics = await self.services['advanced_vision'].get_performance_metrics()
                metrics['model_performance']['advanced_vision'] = vision_metrics

            # Collect API statistics
            for api_name, api in self.apis.items():
                if hasattr(api, 'get_statistics'):
                    metrics['api_statistics'][api_name] = await api.get_statistics()

            # Collect error counts
            metrics['error_counts'] = self.error_handler.get_error_statistics()

        except Exception as e:
            logger.warning(f"فشل في جمع بعض المقاييس: {e}")

        return metrics

    async def shutdown_system(self) -> Dict[str, Any]:
        """إيقاف النظام بشكل آمن"""
        try:
            logger.info("بدء إيقاف النظام...")

            # Create final backup
            await self.backup_system_state()

            # Shutdown services in reverse order
            service_names = list(self.services.keys())
            for service_name in reversed(service_names):
                try:
                    if hasattr(self.services[service_name], 'shutdown'):
                        await self.services[service_name].shutdown()
                    self.status['services_status'][service_name] = 'stopped'
                    logger.info(f"تم إيقاف الخدمة: {service_name}")
                except Exception as e:
                    logger.warning(f"فشل في إيقاف الخدمة {service_name}: {e}")

            self.status['system_status'] = 'stopped'
            logger.info("تم إيقاف النظام بنجاح")

            return {
                'success': True,
                'message': 'تم إيقاف النظام بنجاح',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            error_info = self.error_handler.handle_error(e, 'shutdown_system')
            return {
                'success': False,
                'error': error_info
            }


# Global integration manager instance
integration_manager = None


async def get_integration_manager(config: Config = None) -> IntegrationManager:
    """الحصول على مدير التكامل العام"""
    global integration_manager

    if integration_manager is None:
        if config is None:
            from .config import get_config
            config = get_config()

        integration_manager = IntegrationManager(config)
        await integration_manager.initialize_system()

    return integration_manager


async def initialize_system(config: Config = None) -> Dict[str, Any]:
    """تهيئة النظام الكامل"""
    manager = await get_integration_manager(config)
    return await manager.get_system_status()


async def shutdown_system() -> Dict[str, Any]:
    """إيقاف النظام"""
    global integration_manager

    if integration_manager:
        result = await integration_manager.shutdown_system()
        integration_manager = None
        return result

    return {
        'success': True,
        'message': 'النظام غير مشغل',
        'timestamp': datetime.now().isoformat()
    }
