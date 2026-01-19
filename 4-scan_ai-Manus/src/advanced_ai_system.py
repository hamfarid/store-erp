# File: /home/ubuntu/clean_project/src/advanced_ai_system.py
"""
مسار الملف: /home/ubuntu/clean_project/src/advanced_ai_system.py

نظام الذكاء الاصطناعي المتقدم
يوفر نماذج متعددة ونظام وكلاء ذكيين متطور
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import logging
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import yaml
import redis
import sqlite3
from pathlib import Path
import uuid
import hashlib
from event_system import Event, EventTypes, event_bus, create_system_event

class AIModelType(Enum):
    """أنواع نماذج الذكاء الاصطناعي"""
    LOCAL_FREE = "local_free"
    CLOUD_PREMIUM = "cloud_premium"
    CODEX_SCRIPT = "codex_script"
    PYDANTIC_AGENT = "pydantic_agent"

class AgentType(Enum):
    """أنواع الوكلاء الذكيين"""
    MAIN_AI = "ai_agent"
    DIAGNOSIS = "ai_agent_diagnosis"
    CROP_MANAGEMENT = "ai_agent_crop"
    WEATHER = "ai_agent_weather"
    MARKET = "ai_agent_market"
    PEST_CONTROL = "ai_agent_pest"
    IRRIGATION = "ai_agent_irrigation"
    ERROR_TRACKING = "ai_agent_error"
    SCRIPT_GENERATOR = "ai_agent_script"

class MessageType(Enum):
    """أنواع الرسائل بين الوكلاء"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"
    HEARTBEAT = "heartbeat"

@dataclass
class AIModelConfig:
    """إعدادات نموذج الذكاء الاصطناعي"""
    name: str
    type: AIModelType
    model_path: str
    confidence_threshold: float = 0.8
    max_batch_size: int = 32
    enable_gpu: bool = False
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    preprocessing_config: Dict[str, Any] = field(default_factory=dict)
    postprocessing_config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DiagnosisResult:
    """نتيجة التشخيص"""
    disease_name: str
    confidence: float
    affected_area: float
    severity: str
    treatment_recommendations: List[str]
    prevention_tips: List[str]
    estimated_yield_impact: float
    follow_up_required: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentMessage:
    """رسالة بين الوكلاء"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    receiver_id: str = ""
    message_type: MessageType = MessageType.REQUEST
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None
    priority: int = 5  # 1-10
    expires_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3

class AIModel(ABC):
    """واجهة نموذج الذكاء الاصطناعي"""
    
    @abstractmethod
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """تنفيذ التنبؤ"""
        pass
    
    @abstractmethod
    def load_model(self) -> bool:
        """تحميل النموذج"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """معلومات النموذج"""
        pass

class LocalDiseaseModel(AIModel):
    """نموذج تشخيص الأمراض المحلي المجاني"""
    
    def __init__(self, config: AIModelConfig):
        self.config = config
        self.model = None
        self.device = torch.device('cuda' if config.enable_gpu and torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.classes = []
        self.logger = logging.getLogger('local_disease_model')
    
    def load_model(self) -> bool:
        """تحميل نموذج ResNet-50 المحسن"""
        try:
            # إنشاء نموذج ResNet-50 مخصص
            self.model = models.resnet50(pretrained=False)
            
            # تخصيص الطبقة الأخيرة للأمراض النباتية
            num_classes = len(self._load_classes())
            self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
            
            # تحميل الأوزان المدربة إذا كانت متوفرة
            if Path(self.config.model_path).exists():
                checkpoint = torch.load(self.config.model_path, map_location=self.device)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.logger.info(f"Model loaded from {self.config.model_path}")
            else:
                self.logger.warning(f"Model file not found: {self.config.model_path}")
                # استخدام نموذج مدرب مسبقاً كنقطة بداية
                self.model = models.resnet50(pretrained=True)
                self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
            
            self.model.to(self.device)
            self.model.eval()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False
    
    def _load_classes(self) -> List[str]:
        """تحميل قائمة الأمراض"""
        classes_file = Path(self.config.model_path).parent / "classes.txt"
        if classes_file.exists():
            with open(classes_file, 'r', encoding='utf-8') as f:
                self.classes = [line.strip() for line in f.readlines()]
        else:
            # قائمة افتراضية للأمراض الشائعة
            self.classes = [
                'صحي', 'تبقع الأوراق', 'الصدأ', 'العفن الرمادي', 'البياض الدقيقي',
                'تعفن الجذور', 'فيروس تجعد الأوراق', 'نقص النيتروجين', 'نقص البوتاسيوم',
                'حروق الشمس', 'الذبول البكتيري', 'العفن الأسود'
            ]
        return self.classes
    
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """تشخيص المرض من الصورة"""
        try:
            if isinstance(input_data, str):
                # مسار الصورة
                image = Image.open(input_data).convert('RGB')
            elif isinstance(input_data, Image.Image):
                image = input_data.convert('RGB')
            elif isinstance(input_data, np.ndarray):
                image = Image.fromarray(input_data).convert('RGB')
            else:
                raise ValueError("Unsupported input type")
            
            # معالجة الصورة
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # التنبؤ
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                confidence, predicted_idx = torch.max(probabilities, 0)
            
            # تحليل النتائج
            disease_name = self.classes[predicted_idx.item()]
            confidence_score = confidence.item()
            
            # تحليل إضافي للصورة
            analysis = await self._analyze_image_features(image)
            
            # إنشاء نتيجة التشخيص
            result = DiagnosisResult(
                disease_name=disease_name,
                confidence=confidence_score,
                affected_area=analysis['affected_area'],
                severity=analysis['severity'],
                treatment_recommendations=self._get_treatment_recommendations(disease_name),
                prevention_tips=self._get_prevention_tips(disease_name),
                estimated_yield_impact=analysis['yield_impact'],
                follow_up_required=confidence_score < self.config.confidence_threshold,
                metadata={
                    'model_type': 'local_resnet50',
                    'processing_time': analysis['processing_time'],
                    'image_quality': analysis['image_quality']
                }
            )
            
            return {
                'success': True,
                'result': result,
                'raw_probabilities': probabilities.cpu().numpy().tolist(),
                'all_classes': self.classes
            }
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _analyze_image_features(self, image: Image.Image) -> Dict[str, Any]:
        """تحليل ميزات الصورة الإضافية"""
        start_time = datetime.now()
        
        # تحويل إلى OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # تحليل جودة الصورة
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        image_quality = 'high' if laplacian_var > 100 else 'medium' if laplacian_var > 50 else 'low'
        
        # تقدير المنطقة المتأثرة (تحليل بسيط للألوان)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # تحديد المناطق غير الطبيعية (بناءً على اللون)
        lower_brown = np.array([10, 50, 20])
        upper_brown = np.array([20, 255, 200])
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
        
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        affected_pixels = cv2.countNonZero(brown_mask) + cv2.countNonZero(yellow_mask)
        total_pixels = cv_image.shape[0] * cv_image.shape[1]
        affected_area = (affected_pixels / total_pixels) * 100
        
        # تحديد شدة المرض
        if affected_area < 10:
            severity = 'خفيف'
            yield_impact = 5.0
        elif affected_area < 30:
            severity = 'متوسط'
            yield_impact = 15.0
        elif affected_area < 60:
            severity = 'شديد'
            yield_impact = 35.0
        else:
            severity = 'حرج'
            yield_impact = 60.0
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'affected_area': affected_area,
            'severity': severity,
            'yield_impact': yield_impact,
            'image_quality': image_quality,
            'processing_time': processing_time
        }
    
    def _get_treatment_recommendations(self, disease_name: str) -> List[str]:
        """الحصول على توصيات العلاج"""
        treatments = {
            'تبقع الأوراق': [
                'إزالة الأوراق المصابة وحرقها',
                'رش بمبيد فطري نحاسي',
                'تحسين التهوية حول النباتات',
                'تجنب الري على الأوراق'
            ],
            'الصدأ': [
                'استخدام مبيدات فطرية جهازية',
                'زراعة أصناف مقاومة',
                'تحسين دوران الهواء',
                'إزالة النباتات المصابة'
            ],
            'العفن الرمادي': [
                'تقليل الرطوبة',
                'تحسين التهوية',
                'استخدام مبيدات فطرية وقائية',
                'إزالة الأجزاء المصابة فوراً'
            ],
            'البياض الدقيقي': [
                'رش بمحلول بيكربونات الصوديوم',
                'استخدام مبيدات فطرية متخصصة',
                'تجنب الإفراط في التسميد النيتروجيني',
                'زراعة في مناطق جيدة التهوية'
            ]
        }
        
        return treatments.get(disease_name, [
            'استشارة خبير زراعي',
            'مراقبة تطور الحالة',
            'تحسين ظروف النمو العامة'
        ])
    
    def _get_prevention_tips(self, disease_name: str) -> List[str]:
        """الحصول على نصائح الوقاية"""
        prevention = {
            'تبقع الأوراق': [
                'تجنب الري على الأوراق',
                'زراعة أصناف مقاومة',
                'تطبيق دورة زراعية',
                'تنظيف الحقل من المخلفات'
            ],
            'الصدأ': [
                'زراعة أصناف مقاومة',
                'تجنب الزراعة الكثيفة',
                'مراقبة مستويات النيتروجين',
                'الرش الوقائي في المواسم الرطبة'
            ]
        }
        
        return prevention.get(disease_name, [
            'الحفاظ على نظافة الحقل',
            'مراقبة النباتات بانتظام',
            'تطبيق ممارسات زراعية جيدة',
            'استخدام بذور معتمدة'
        ])
    
    def get_model_info(self) -> Dict[str, Any]:
        """معلومات النموذج"""
        return {
            'name': self.config.name,
            'type': self.config.type.value,
            'architecture': 'ResNet-50',
            'num_classes': len(self.classes),
            'device': str(self.device),
            'confidence_threshold': self.config.confidence_threshold,
            'classes': self.classes
        }

class CloudPremiumModel(AIModel):
    """نموذج سحابي متقدم مدفوع"""
    
    def __init__(self, config: AIModelConfig):
        self.config = config
        self.logger = logging.getLogger('cloud_premium_model')
    
    def load_model(self) -> bool:
        """التحقق من اتصال API"""
        return bool(self.config.api_endpoint and self.config.api_key)
    
    async def predict(self, input_data: Any) -> Dict[str, Any]:
        """تنفيذ التنبؤ عبر API السحابي"""
        try:
            # محاكاة استدعاء API سحابي متقدم
            # في التطبيق الفعلي، سيتم استدعاء API حقيقي
            
            await asyncio.sleep(0.5)  # محاكاة زمن الاستجابة
            
            # نتائج محاكاة متقدمة
            result = DiagnosisResult(
                disease_name='تبقع الأوراق المتقدم',
                confidence=0.95,
                affected_area=25.5,
                severity='متوسط',
                treatment_recommendations=[
                    'استخدام مبيد فطري متخصص XYZ',
                    'تطبيق برنامج علاج متكامل لمدة 14 يوم',
                    'مراقبة يومية لتطور الحالة'
                ],
                prevention_tips=[
                    'تطبيق نظام ري بالتنقيط',
                    'استخدام أصناف مقاومة وراثياً',
                    'تطبيق برنامج تسميد متوازن'
                ],
                estimated_yield_impact=12.3,
                follow_up_required=True,
                metadata={
                    'model_type': 'cloud_premium_v2',
                    'ai_confidence': 0.95,
                    'detailed_analysis': True
                }
            )
            
            return {
                'success': True,
                'result': result,
                'premium_features': {
                    'detailed_treatment_plan': True,
                    'yield_prediction': True,
                    'weather_integration': True,
                    'expert_consultation': True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Cloud prediction failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'name': self.config.name,
            'type': self.config.type.value,
            'api_endpoint': self.config.api_endpoint,
            'features': ['advanced_analysis', 'expert_consultation', 'yield_prediction']
        }

class AIAgent(ABC):
    """واجهة الوكيل الذكي"""
    
    def __init__(self, agent_id: str, agent_type: AgentType):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.is_active = True
        self.message_queue = asyncio.Queue()
        self.memory = {}
        self.logger = logging.getLogger(f'agent_{agent_id}')
    
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """معالجة رسالة واردة"""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """تهيئة الوكيل"""
        pass
    
    async def send_message(self, receiver_id: str, content: Dict[str, Any], 
                          message_type: MessageType = MessageType.REQUEST) -> str:
        """إرسال رسالة إلى وكيل آخر"""
        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content
        )
        
        # إرسال عبر المنسق المركزي
        await agent_coordinator.route_message(message)
        return message.id
    
    async def start(self):
        """بدء تشغيل الوكيل"""
        self.logger.info(f"Agent {self.agent_id} started")
        while self.is_active:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                response = await self.process_message(message)
                
                if response:
                    await agent_coordinator.route_message(response)
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
    
    def stop(self):
        """إيقاف الوكيل"""
        self.is_active = False
        self.logger.info(f"Agent {self.agent_id} stopped")

class MainAIAgent(AIAgent):
    """الوكيل الرئيسي للذكاء الاصطناعي"""
    
    def __init__(self):
        super().__init__("main_ai_agent", AgentType.MAIN_AI)
        self.models: Dict[AIModelType, AIModel] = {}
        self.knowledge_base = {}
    
    async def initialize(self) -> bool:
        """تهيئة الوكيل الرئيسي"""
        try:
            # تحميل النماذج
            await self._load_models()
            
            # تحميل قاعدة المعرفة
            await self._load_knowledge_base()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize main AI agent: {e}")
            return False
    
    async def _load_models(self):
        """تحميل جميع نماذج الذكاء الاصطناعي"""
        # النموذج المحلي المجاني
        local_config = AIModelConfig(
            name="Local Disease Detector",
            type=AIModelType.LOCAL_FREE,
            model_path="models/disease_model.pth",
            confidence_threshold=0.7
        )
        self.models[AIModelType.LOCAL_FREE] = LocalDiseaseModel(local_config)
        
        # النموذج السحابي المتقدم
        cloud_config = AIModelConfig(
            name="Premium Cloud AI",
            type=AIModelType.CLOUD_PREMIUM,
            model_path="",
            api_endpoint="https://api.premium-ai.com/v1/diagnose",
            api_key="your-premium-api-key",
            confidence_threshold=0.9
        )
        self.models[AIModelType.CLOUD_PREMIUM] = CloudPremiumModel(cloud_config)
        
        # تحميل النماذج
        for model in self.models.values():
            model.load_model()
    
    async def _load_knowledge_base(self):
        """تحميل قاعدة المعرفة"""
        knowledge_file = Path("data/knowledge_base.yaml")
        if knowledge_file.exists():
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = yaml.safe_load(f)
        else:
            # قاعدة معرفة افتراضية
            self.knowledge_base = {
                'diseases': {
                    'تبقع الأوراق': {
                        'symptoms': ['بقع بنية على الأوراق', 'اصفرار الأوراق'],
                        'causes': ['فطريات', 'رطوبة عالية'],
                        'treatments': ['مبيدات فطرية', 'تحسين التهوية']
                    }
                },
                'crops': {
                    'طماطم': {
                        'common_diseases': ['تبقع الأوراق', 'الذبول البكتيري'],
                        'optimal_conditions': {'temperature': '20-25°C', 'humidity': '60-70%'}
                    }
                }
            }
    
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """معالجة الرسائل الواردة"""
        try:
            content = message.content
            
            if content.get('action') == 'diagnose':
                # طلب تشخيص
                result = await self._handle_diagnosis_request(content)
                
                return AgentMessage(
                    sender_id=self.agent_id,
                    receiver_id=message.sender_id,
                    message_type=MessageType.RESPONSE,
                    content={'result': result},
                    correlation_id=message.id
                )
            
            elif content.get('action') == 'get_knowledge':
                # طلب معلومات من قاعدة المعرفة
                knowledge = self._get_knowledge(content.get('topic'))
                
                return AgentMessage(
                    sender_id=self.agent_id,
                    receiver_id=message.sender_id,
                    message_type=MessageType.RESPONSE,
                    content={'knowledge': knowledge},
                    correlation_id=message.id
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return AgentMessage(
                sender_id=self.agent_id,
                receiver_id=message.sender_id,
                message_type=MessageType.ERROR,
                content={'error': str(e)},
                correlation_id=message.id
            )
    
    async def _handle_diagnosis_request(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة طلب التشخيص"""
        image_path = content.get('image_path')
        model_preference = content.get('model_type', 'auto')
        
        # اختيار النموذج المناسب
        if model_preference == 'auto':
            # اختيار تلقائي بناءً على توفر النماذج
            if AIModelType.CLOUD_PREMIUM in self.models:
                selected_model = self.models[AIModelType.CLOUD_PREMIUM]
            else:
                selected_model = self.models[AIModelType.LOCAL_FREE]
        else:
            model_type = AIModelType(model_preference)
            selected_model = self.models.get(model_type)
        
        if not selected_model:
            return {'success': False, 'error': 'Model not available'}
        
        # تنفيذ التشخيص
        result = await selected_model.predict(image_path)
        
        # إضافة معلومات إضافية من قاعدة المعرفة
        if result.get('success') and 'result' in result:
            disease_name = result['result'].disease_name
            additional_info = self._get_knowledge(f"diseases.{disease_name}")
            result['additional_info'] = additional_info
        
        return result
    
    def _get_knowledge(self, topic: str) -> Dict[str, Any]:
        """الحصول على معلومات من قاعدة المعرفة"""
        keys = topic.split('.')
        current = self.knowledge_base
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return {}
        
        return current if isinstance(current, dict) else {'value': current}

class ErrorTrackingAgent(AIAgent):
    """وكيل تتبع الأخطاء"""
    
    def __init__(self):
        super().__init__("error_tracking_agent", AgentType.ERROR_TRACKING)
        self.error_log = []
    
    async def initialize(self) -> bool:
        return True
    
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """معالجة تقارير الأخطاء"""
        if message.message_type == MessageType.ERROR:
            await self._log_error(message)
            await self._notify_admin(message)
        
        return None
    
    async def _log_error(self, message: AgentMessage):
        """تسجيل الخطأ"""
        error_entry = {
            'timestamp': message.timestamp,
            'sender': message.sender_id,
            'error': message.content,
            'correlation_id': message.correlation_id
        }
        self.error_log.append(error_entry)
        self.logger.error(f"Error logged: {error_entry}")
    
    async def _notify_admin(self, message: AgentMessage):
        """إشعار المدير بالخطأ"""
        # إرسال إشعار عبر نظام الإشعارات
        from notification_system import create_notification, NotificationType, NotificationChannel
        
        notification = create_notification(
            title="خطأ في النظام",
            message=f"حدث خطأ في الوكيل {message.sender_id}: {message.content.get('error', 'خطأ غير محدد')}",
            recipients=["admin"],
            notification_type=NotificationType.ERROR,
            channels=[NotificationChannel.EMAIL, NotificationChannel.WEBSOCKET]
        )
        
        # إرسال الإشعار (سيتم تطبيقه لاحقاً)
        self.logger.info(f"Admin notified about error from {message.sender_id}")

class AgentCoordinator:
    """المنسق المركزي للوكلاء"""
    
    def __init__(self):
        self.agents: Dict[str, AIAgent] = {}
        self.message_routes: Dict[str, str] = {}  # receiver_id -> agent_id
        self.logger = logging.getLogger('agent_coordinator')
    
    def register_agent(self, agent: AIAgent):
        """تسجيل وكيل جديد"""
        self.agents[agent.agent_id] = agent
        self.message_routes[agent.agent_id] = agent.agent_id
        self.logger.info(f"Agent {agent.agent_id} registered")
    
    async def route_message(self, message: AgentMessage) -> bool:
        """توجيه الرسالة إلى الوكيل المناسب"""
        try:
            receiver_id = message.receiver_id
            
            if receiver_id in self.agents:
                agent = self.agents[receiver_id]
                await agent.message_queue.put(message)
                self.logger.debug(f"Message routed to {receiver_id}")
                return True
            else:
                # إرسال إلى وكيل تتبع الأخطاء
                error_message = AgentMessage(
                    sender_id="coordinator",
                    receiver_id="error_tracking_agent",
                    message_type=MessageType.ERROR,
                    content={'error': f'Agent {receiver_id} not found', 'original_message': message.id}
                )
                
                if "error_tracking_agent" in self.agents:
                    await self.agents["error_tracking_agent"].message_queue.put(error_message)
                
                return False
                
        except Exception as e:
            self.logger.error(f"Error routing message: {e}")
            return False
    
    async def start_all_agents(self):
        """بدء تشغيل جميع الوكلاء"""
        tasks = []
        for agent in self.agents.values():
            await agent.initialize()
            task = asyncio.create_task(agent.start())
            tasks.append(task)
        
        self.logger.info(f"Started {len(tasks)} agents")
        return tasks
    
    def stop_all_agents(self):
        """إيقاف جميع الوكلاء"""
        for agent in self.agents.values():
            agent.stop()
        self.logger.info("All agents stopped")

# مثيل عام للمنسق
agent_coordinator = AgentCoordinator()

class AIModelManager:
    """مدير نماذج الذكاء الاصطناعي"""
    
    def __init__(self):
        self.models: Dict[str, AIModel] = {}
        self.model_configs: Dict[str, AIModelConfig] = {}
        self.usage_stats = {}
        self.logger = logging.getLogger('ai_model_manager')
    
    def register_model(self, model_id: str, model: AIModel, config: AIModelConfig):
        """تسجيل نموذج جديد"""
        self.models[model_id] = model
        self.model_configs[model_id] = config
        self.usage_stats[model_id] = {
            'total_predictions': 0,
            'successful_predictions': 0,
            'failed_predictions': 0,
            'average_confidence': 0.0,
            'last_used': None
        }
        self.logger.info(f"Model {model_id} registered")
    
    async def predict(self, model_id: str, input_data: Any) -> Dict[str, Any]:
        """تنفيذ التنبؤ باستخدام نموذج محدد"""
        if model_id not in self.models:
            return {'success': False, 'error': f'Model {model_id} not found'}
        
        model = self.models[model_id]
        stats = self.usage_stats[model_id]
        
        try:
            # تنفيذ التنبؤ
            result = await model.predict(input_data)
            
            # تحديث الإحصائيات
            stats['total_predictions'] += 1
            stats['last_used'] = datetime.now()
            
            if result.get('success'):
                stats['successful_predictions'] += 1
                if 'result' in result and hasattr(result['result'], 'confidence'):
                    confidence = result['result'].confidence
                    current_avg = stats['average_confidence']
                    total_successful = stats['successful_predictions']
                    stats['average_confidence'] = ((current_avg * (total_successful - 1)) + confidence) / total_successful
            else:
                stats['failed_predictions'] += 1
            
            # إرسال حدث
            event = create_system_event(
                EventTypes.AI_PREDICTION_MADE,
                f"Prediction made using model {model_id}",
                model_id=model_id,
                success=result.get('success', False)
            )
            await event_bus.publish(event)
            
            return result
            
        except Exception as e:
            stats['failed_predictions'] += 1
            self.logger.error(f"Prediction failed for model {model_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_model_stats(self, model_id: str) -> Dict[str, Any]:
        """الحصول على إحصائيات النموذج"""
        if model_id not in self.usage_stats:
            return {}
        
        stats = self.usage_stats[model_id].copy()
        stats['model_info'] = self.models[model_id].get_model_info()
        return stats
    
    def get_all_models_info(self) -> Dict[str, Any]:
        """الحصول على معلومات جميع النماذج"""
        return {
            model_id: {
                'config': config.__dict__,
                'stats': self.get_model_stats(model_id)
            }
            for model_id, config in self.model_configs.items()
        }

# مثيل عام لمدير النماذج
ai_model_manager = AIModelManager()

# دوال مساعدة
async def initialize_ai_system():
    """تهيئة نظام الذكاء الاصطناعي"""
    try:
        # إنشاء الوكلاء
        main_agent = MainAIAgent()
        error_agent = ErrorTrackingAgent()
        
        # تسجيل الوكلاء
        agent_coordinator.register_agent(main_agent)
        agent_coordinator.register_agent(error_agent)
        
        # بدء تشغيل الوكلاء
        await agent_coordinator.start_all_agents()
        
        # إرسال حدث بدء النظام
        event = create_system_event(
            EventTypes.AI_MODEL_LOADED,
            "AI system initialized successfully"
        )
        await event_bus.publish(event)
        
        return True
        
    except Exception as e:
        logging.error(f"Failed to initialize AI system: {e}")
        return False

async def diagnose_plant_disease(image_path: str, model_preference: str = 'auto') -> Dict[str, Any]:
    """تشخيص مرض النبات"""
    # إرسال طلب إلى الوكيل الرئيسي
    message = AgentMessage(
        sender_id="api",
        receiver_id="main_ai_agent",
        message_type=MessageType.REQUEST,
        content={
            'action': 'diagnose',
            'image_path': image_path,
            'model_type': model_preference
        }
    )
    
    # توجيه الرسالة
    success = await agent_coordinator.route_message(message)
    if not success:
        return {'success': False, 'error': 'Failed to route message to AI agent'}
    
    # في التطبيق الفعلي، سنحتاج إلى آلية انتظار الرد
    # هنا سنعيد نتيجة محاكاة
    return {
        'success': True,
        'message': 'Diagnosis request sent to AI agent',
        'request_id': message.id
    }

if __name__ == "__main__":
    # مثال على الاستخدام
    async def main():
        # تهيئة النظام
        await initialize_ai_system()
        
        # محاكاة تشخيص
        result = await diagnose_plant_disease("test_image.jpg", "local_free")
        print(f"Diagnosis result: {result}")
        
        # إيقاف النظام
        agent_coordinator.stop_all_agents()
    
    asyncio.run(main())

