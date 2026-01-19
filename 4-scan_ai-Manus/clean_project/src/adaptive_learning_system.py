# File: /home/ubuntu/clean_project/src/adaptive_learning_system.py
"""
مسار الملف: /home/ubuntu/clean_project/src/adaptive_learning_system.py

نظام التعلم الآلي التكيفي ومعالجة اللغة الطبيعية
يوفر تعلم مستمر وتحسين النماذج تلقائياً
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import logging
import numpy as np
import sqlite3
from pathlib import Path
import uuid
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import yaml
from event_system import Event, EventTypes, event_bus, create_system_event

# تحميل موارد NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class LearningMode(Enum):
    """أنماط التعلم"""
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    SEMI_SUPERVISED = "semi_supervised"
    ACTIVE_LEARNING = "active_learning"

class FeedbackType(Enum):
    """أنواع التغذية الراجعة"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"
    EXPERT_REVIEW = "expert_review"
    USER_RATING = "user_rating"

class LanguageCode(Enum):
    """رموز اللغات المدعومة"""
    ARABIC = "ar"
    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"

@dataclass
class LearningExample:
    """مثال تعليمي"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_data: Any = None
    expected_output: Any = None
    actual_output: Any = None
    feedback: Optional[FeedbackType] = None
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "user"
    metadata: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0  # وزن المثال في التدريب

@dataclass
class ModelPerformance:
    """أداء النموذج"""
    model_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    timestamp: datetime = field(default_factory=datetime.now)
    sample_size: int = 0
    training_time: float = 0.0

@dataclass
class NLPQuery:
    """استعلام معالجة اللغة الطبيعية"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    language: LanguageCode = LanguageCode.ARABIC
    intent: Optional[str] = None
    entities: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    response: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

class AdaptiveLearningEngine:
    """محرك التعلم التكيفي"""
    
    def __init__(self, model_id: str, learning_mode: LearningMode = LearningMode.SUPERVISED):
        self.model_id = model_id
        self.learning_mode = learning_mode
        self.examples: List[LearningExample] = []
        self.performance_history: List[ModelPerformance] = []
        self.model = None
        self.is_training = False
        self.last_training = None
        self.training_threshold = 100  # عدد الأمثلة المطلوبة لإعادة التدريب
        self.performance_threshold = 0.8  # حد الأداء المطلوب
        self.logger = logging.getLogger(f'adaptive_learning_{model_id}')
        
        # إعدادات التعلم التكيفي
        self.adaptation_config = {
            'auto_retrain': True,
            'retrain_interval_hours': 24,
            'min_examples_for_training': 50,
            'performance_decay_threshold': 0.05,
            'feedback_weight_multiplier': 2.0,
            'expert_feedback_weight': 5.0
        }
    
    async def add_example(self, example: LearningExample) -> bool:
        """إضافة مثال تعليمي جديد"""
        try:
            # تحديد وزن المثال بناءً على نوع التغذية الراجعة
            if example.feedback == FeedbackType.EXPERT_REVIEW:
                example.weight = self.adaptation_config['expert_feedback_weight']
            elif example.feedback in [FeedbackType.CORRECT, FeedbackType.INCORRECT]:
                example.weight = self.adaptation_config['feedback_weight_multiplier']
            
            self.examples.append(example)
            self.logger.info(f"Added learning example {example.id}")
            
            # التحقق من الحاجة لإعادة التدريب
            if await self._should_retrain():
                await self._schedule_retraining()
            
            # إرسال حدث
            event = create_system_event(
                EventTypes.AI_MODEL_UPDATED,
                f"New learning example added to model {self.model_id}",
                model_id=self.model_id,
                example_count=len(self.examples)
            )
            await event_bus.publish(event)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add example: {e}")
            return False
    
    async def _should_retrain(self) -> bool:
        """تحديد ما إذا كان النموذج يحتاج إعادة تدريب"""
        if not self.adaptation_config['auto_retrain']:
            return False
        
        # عدد الأمثلة الجديدة
        if len(self.examples) >= self.adaptation_config['min_examples_for_training']:
            return True
        
        # انخفاض الأداء
        if self.performance_history:
            latest_performance = self.performance_history[-1]
            if len(self.performance_history) > 1:
                previous_performance = self.performance_history[-2]
                performance_decay = previous_performance.accuracy - latest_performance.accuracy
                if performance_decay > self.adaptation_config['performance_decay_threshold']:
                    return True
        
        # فترة زمنية محددة
        if self.last_training:
            hours_since_training = (datetime.now() - self.last_training).total_seconds() / 3600
            if hours_since_training >= self.adaptation_config['retrain_interval_hours']:
                return True
        
        return False
    
    async def _schedule_retraining(self):
        """جدولة إعادة التدريب"""
        if self.is_training:
            self.logger.info("Training already in progress, skipping")
            return
        
        self.logger.info(f"Scheduling retraining for model {self.model_id}")
        asyncio.create_task(self._retrain_model())
    
    async def _retrain_model(self):
        """إعادة تدريب النموذج"""
        if self.is_training:
            return
        
        self.is_training = True
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Starting retraining for model {self.model_id}")
            
            # تحضير البيانات
            X, y, weights = self._prepare_training_data()
            
            if len(X) < self.adaptation_config['min_examples_for_training']:
                self.logger.warning("Not enough examples for training")
                return
            
            # تقسيم البيانات
            X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
                X, y, weights, test_size=0.2, random_state=42, stratify=y
            )
            
            # تدريب النموذج
            if self.model is None:
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    random_state=42,
                    class_weight='balanced'
                )
            
            self.model.fit(X_train, y_train, sample_weight=w_train)
            
            # تقييم الأداء
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # حفظ معلومات الأداء
            performance = ModelPerformance(
                model_id=self.model_id,
                accuracy=accuracy,
                precision=0.0,  # سيتم حسابها لاحقاً
                recall=0.0,
                f1_score=0.0,
                confusion_matrix=[],
                sample_size=len(X),
                training_time=(datetime.now() - start_time).total_seconds()
            )
            
            self.performance_history.append(performance)
            self.last_training = datetime.now()
            
            # حفظ النموذج
            await self._save_model()
            
            self.logger.info(f"Model retrained successfully. Accuracy: {accuracy:.3f}")
            
            # إرسال حدث
            event = create_system_event(
                EventTypes.AI_MODEL_UPDATED,
                f"Model {self.model_id} retrained successfully",
                model_id=self.model_id,
                accuracy=accuracy,
                training_time=performance.training_time
            )
            await event_bus.publish(event)
            
        except Exception as e:
            self.logger.error(f"Retraining failed: {e}")
        finally:
            self.is_training = False
    
    def _prepare_training_data(self) -> Tuple[List[Any], List[Any], List[float]]:
        """تحضير بيانات التدريب"""
        X, y, weights = [], [], []
        
        for example in self.examples:
            if example.expected_output is not None:
                X.append(example.input_data)
                y.append(example.expected_output)
                weights.append(example.weight)
        
        return X, y, weights
    
    async def _save_model(self):
        """حفظ النموذج"""
        try:
            model_dir = Path("models/adaptive")
            model_dir.mkdir(parents=True, exist_ok=True)
            
            model_path = model_dir / f"{self.model_id}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            # حفظ الأمثلة والأداء
            data = {
                'examples': [example.__dict__ for example in self.examples],
                'performance_history': [perf.__dict__ for perf in self.performance_history],
                'config': self.adaptation_config
            }
            
            data_path = model_dir / f"{self.model_id}_data.json"
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"Model saved to {model_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save model: {e}")
    
    async def load_model(self) -> bool:
        """تحميل النموذج"""
        try:
            model_path = Path(f"models/adaptive/{self.model_id}.pkl")
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                # تحميل البيانات
                data_path = Path(f"models/adaptive/{self.model_id}_data.json")
                if data_path.exists():
                    with open(data_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # استعادة الأمثلة
                    self.examples = [
                        LearningExample(**example) for example in data.get('examples', [])
                    ]
                    
                    # استعادة تاريخ الأداء
                    self.performance_history = [
                        ModelPerformance(**perf) for perf in data.get('performance_history', [])
                    ]
                    
                    # استعادة الإعدادات
                    self.adaptation_config.update(data.get('config', {}))
                
                self.logger.info(f"Model loaded from {model_path}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """الحصول على مقاييس الأداء"""
        if not self.performance_history:
            return {}
        
        latest = self.performance_history[-1]
        return {
            'current_accuracy': latest.accuracy,
            'training_examples': len(self.examples),
            'last_training': self.last_training,
            'performance_trend': self._calculate_performance_trend(),
            'model_age_hours': (datetime.now() - latest.timestamp).total_seconds() / 3600
        }
    
    def _calculate_performance_trend(self) -> str:
        """حساب اتجاه الأداء"""
        if len(self.performance_history) < 2:
            return "insufficient_data"
        
        recent_performances = [p.accuracy for p in self.performance_history[-5:]]
        if len(recent_performances) < 2:
            return "insufficient_data"
        
        trend = np.polyfit(range(len(recent_performances)), recent_performances, 1)[0]
        
        if trend > 0.01:
            return "improving"
        elif trend < -0.01:
            return "declining"
        else:
            return "stable"

class NLPProcessor:
    """معالج اللغة الطبيعية"""
    
    def __init__(self):
        self.supported_languages = [lang.value for lang in LanguageCode]
        self.stemmer = SnowballStemmer('arabic')
        self.stop_words = set(stopwords.words('arabic'))
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=list(self.stop_words))
        self.intent_classifier = None
        self.entity_patterns = {}
        self.knowledge_base = {}
        self.logger = logging.getLogger('nlp_processor')
        
        # تحميل قوالب الكيانات
        self._load_entity_patterns()
        
        # تحميل قاعدة المعرفة
        self._load_knowledge_base()
    
    def _load_entity_patterns(self):
        """تحميل قوالب استخراج الكيانات"""
        self.entity_patterns = {
            'crop_name': [
                r'\b(طماطم|بندورة|خيار|فلفل|باذنجان|كوسا|بطاطس|جزر|بصل|ثوم)\b',
                r'\b(قمح|شعير|ذرة|أرز|عدس|حمص|فول|لوبيا)\b',
                r'\b(تفاح|برتقال|ليمون|عنب|موز|مانجو|خوخ|مشمش)\b'
            ],
            'disease_name': [
                r'\b(تبقع الأوراق|الصدأ|العفن الرمادي|البياض الدقيقي|تعفن الجذور)\b',
                r'\b(الذبول البكتيري|فيروس تجعد الأوراق|العفن الأسود|حروق الشمس)\b'
            ],
            'symptom': [
                r'\b(اصفرار|ذبول|تبقع|تجعد|تعفن|جفاف|سقوط)\b.*\b(أوراق|ثمار|جذور|ساق)\b',
                r'\b(بقع|لطخ|خطوط|ثقوب|تشققات)\b.*\b(بنية|صفراء|سوداء|بيضاء)\b'
            ],
            'location': [
                r'\b(حقل|مزرعة|بيت محمي|صوبة|حديقة|أرض)\b',
                r'\b(شمال|جنوب|شرق|غرب|وسط)\b.*\b(المملكة|السعودية|الرياض|جدة|الدمام)\b'
            ],
            'time': [
                r'\b(اليوم|أمس|غداً|هذا الأسبوع|الشهر الماضي|العام الماضي)\b',
                r'\b(صباح|مساء|ظهر|ليل)\b',
                r'\b(يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\b'
            ]
        }
    
    def _load_knowledge_base(self):
        """تحميل قاعدة المعرفة للإجابة على الأسئلة"""
        self.knowledge_base = {
            'diseases': {
                'تبقع الأوراق': {
                    'description': 'مرض فطري يصيب أوراق النباتات ويسبب ظهور بقع بنية أو سوداء',
                    'symptoms': ['بقع بنية على الأوراق', 'اصفرار الأوراق', 'سقوط الأوراق المبكر'],
                    'causes': ['الرطوبة العالية', 'سوء التهوية', 'الري على الأوراق'],
                    'treatment': ['استخدام مبيدات فطرية', 'تحسين التهوية', 'تجنب الري على الأوراق'],
                    'prevention': ['زراعة أصناف مقاومة', 'تطبيق دورة زراعية', 'تنظيف الحقل']
                },
                'الصدأ': {
                    'description': 'مرض فطري يسبب ظهور بقع صدئية اللون على الأوراق',
                    'symptoms': ['بقع برتقالية أو بنية', 'مسحوق صدئي على الأوراق'],
                    'causes': ['الرطوبة العالية', 'درجات الحرارة المعتدلة'],
                    'treatment': ['مبيدات فطرية جهازية', 'إزالة الأجزاء المصابة'],
                    'prevention': ['زراعة أصناف مقاومة', 'تحسين دوران الهواء']
                }
            },
            'crops': {
                'طماطم': {
                    'optimal_conditions': {
                        'temperature': '20-25°C',
                        'humidity': '60-70%',
                        'ph': '6.0-6.8'
                    },
                    'common_diseases': ['تبقع الأوراق', 'الذبول البكتيري', 'العفن الرمادي'],
                    'planting_season': 'الربيع والخريف',
                    'harvest_time': '75-85 يوم من الزراعة'
                },
                'خيار': {
                    'optimal_conditions': {
                        'temperature': '18-24°C',
                        'humidity': '70-80%',
                        'ph': '6.0-7.0'
                    },
                    'common_diseases': ['البياض الدقيقي', 'العفن الرمادي'],
                    'planting_season': 'الربيع والصيف',
                    'harvest_time': '50-60 يوم من الزراعة'
                }
            },
            'general_advice': {
                'irrigation': 'اسق النباتات في الصباح الباكر أو المساء لتجنب تبخر الماء',
                'fertilization': 'استخدم الأسمدة العضوية لتحسين بنية التربة',
                'pest_control': 'راقب النباتات بانتظام للكشف المبكر عن الآفات',
                'soil_preparation': 'احرث التربة جيداً وأضف المواد العضوية قبل الزراعة'
            }
        }
    
    async def process_query(self, query: NLPQuery) -> NLPQuery:
        """معالجة استعلام اللغة الطبيعية"""
        try:
            # تنظيف النص
            cleaned_text = self._clean_text(query.text)
            
            # استخراج الكيانات
            entities = self._extract_entities(cleaned_text)
            query.entities = entities
            
            # تحديد النية
            intent = await self._classify_intent(cleaned_text, entities)
            query.intent = intent
            
            # توليد الإجابة
            response = await self._generate_response(query)
            query.response = response
            
            self.logger.info(f"Processed NLP query: {query.id}")
            return query
            
        except Exception as e:
            self.logger.error(f"Failed to process query: {e}")
            query.response = "عذراً، حدث خطأ في معالجة استفسارك. يرجى المحاولة مرة أخرى."
            return query
    
    def _clean_text(self, text: str) -> str:
        """تنظيف النص"""
        # إزالة الرموز غير المرغوبة
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """استخراج الكيانات من النص"""
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, text, re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                entities[entity_type] = list(set(matches))  # إزالة التكرار
        
        return entities
    
    async def _classify_intent(self, text: str, entities: Dict[str, List[str]]) -> str:
        """تصنيف نية المستخدم"""
        # قوالب النوايا
        intent_patterns = {
            'disease_diagnosis': [
                r'\b(ما هو|ما هذا|تشخيص|مرض|مشكلة|علة)\b.*\b(نبات|محصول|زرع)\b',
                r'\b(أوراق|ثمار|جذور)\b.*\b(مريضة|مصابة|تالفة|ذابلة)\b'
            ],
            'treatment_advice': [
                r'\b(كيف|ماذا)\b.*\b(علاج|معالجة|حل|إصلاح)\b',
                r'\b(علاج|دواء|مبيد|رش)\b.*\b(مرض|آفة|حشرة)\b'
            ],
            'prevention_tips': [
                r'\b(كيف|ماذا)\b.*\b(وقاية|منع|تجنب|حماية)\b',
                r'\b(وقاية|منع|حماية)\b.*\b(مرض|آفة|مشكلة)\b'
            ],
            'crop_information': [
                r'\b(معلومات|تفاصيل|خصائص)\b.*\b(محصول|نبات|زراعة)\b',
                r'\b(متى|كيف|أين)\b.*\b(زراعة|غرس|بذر)\b'
            ],
            'general_question': [
                r'\b(ما هو|ما هي|كيف|متى|أين|لماذا|ماذا)\b',
                r'\b(سؤال|استفسار|معلومة|نصيحة)\b'
            ]
        }
        
        # تسجيل نقاط لكل نية
        intent_scores = {}
        
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            
            # إضافة نقاط بناءً على الكيانات المستخرجة
            if intent == 'disease_diagnosis' and 'disease_name' in entities:
                score += 2
            elif intent == 'crop_information' and 'crop_name' in entities:
                score += 2
            elif intent == 'treatment_advice' and ('disease_name' in entities or 'symptom' in entities):
                score += 2
            
            intent_scores[intent] = score
        
        # اختيار النية ذات أعلى نقاط
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            if intent_scores[best_intent] > 0:
                return best_intent
        
        return 'general_question'
    
    async def _generate_response(self, query: NLPQuery) -> str:
        """توليد الإجابة"""
        intent = query.intent
        entities = query.entities
        text = query.text
        
        if intent == 'disease_diagnosis':
            return self._generate_diagnosis_response(entities, text)
        elif intent == 'treatment_advice':
            return self._generate_treatment_response(entities, text)
        elif intent == 'prevention_tips':
            return self._generate_prevention_response(entities, text)
        elif intent == 'crop_information':
            return self._generate_crop_info_response(entities, text)
        else:
            return self._generate_general_response(text)
    
    def _generate_diagnosis_response(self, entities: Dict[str, List[str]], text: str) -> str:
        """توليد إجابة للتشخيص"""
        if 'disease_name' in entities:
            disease = entities['disease_name'][0]
            if disease in self.knowledge_base['diseases']:
                disease_info = self.knowledge_base['diseases'][disease]
                return f"""
مرض {disease}:

الوصف: {disease_info['description']}

الأعراض:
{chr(10).join(f"• {symptom}" for symptom in disease_info['symptoms'])}

الأسباب:
{chr(10).join(f"• {cause}" for cause in disease_info['causes'])}

للحصول على تشخيص دقيق، يرجى رفع صورة واضحة للنبات المصاب.
                """.strip()
        
        if 'symptom' in entities:
            return """
بناءً على الأعراض المذكورة، أنصحك بـ:

1. رفع صورة واضحة للنبات المصاب للحصول على تشخيص دقيق
2. فحص النباتات المجاورة للتأكد من عدم انتشار المشكلة
3. تجنب الري المفرط أو نقص الري
4. التأكد من جودة التهوية حول النباتات

يمكنني مساعدتك بشكل أفضل إذا قمت برفع صورة للنبات.
            """.strip()
        
        return """
لتشخيص مشكلة النبات بدقة، أحتاج إلى:

1. صورة واضحة للنبات المصاب
2. وصف مفصل للأعراض
3. نوع النبات أو المحصول
4. الظروف البيئية (الري، التسميد، الطقس)

يرجى رفع صورة وسأقوم بتحليلها فوراً.
        """.strip()
    
    def _generate_treatment_response(self, entities: Dict[str, List[str]], text: str) -> str:
        """توليد إجابة للعلاج"""
        if 'disease_name' in entities:
            disease = entities['disease_name'][0]
            if disease in self.knowledge_base['diseases']:
                treatments = self.knowledge_base['diseases'][disease]['treatment']
                return f"""
علاج {disease}:

{chr(10).join(f"{i+1}. {treatment}" for i, treatment in enumerate(treatments))}

نصائح إضافية:
• اتبع تعليمات استخدام المبيدات بدقة
• كرر العلاج حسب الحاجة
• راقب تحسن الحالة بعد العلاج
• استشر خبير زراعي في الحالات الشديدة
                """.strip()
        
        return """
للحصول على نصائح علاجية مناسبة، أحتاج إلى معرفة:

1. نوع المرض أو المشكلة
2. نوع النبات المصاب
3. شدة الإصابة
4. الأعراض الظاهرة

يرجى تقديم المزيد من التفاصيل أو رفع صورة للنبات.
        """.strip()
    
    def _generate_prevention_response(self, entities: Dict[str, List[str]], text: str) -> str:
        """توليد إجابة للوقاية"""
        if 'disease_name' in entities:
            disease = entities['disease_name'][0]
            if disease in self.knowledge_base['diseases']:
                prevention = self.knowledge_base['diseases'][disease]['prevention']
                return f"""
الوقاية من {disease}:

{chr(10).join(f"• {tip}" for tip in prevention)}

نصائح عامة للوقاية:
• فحص النباتات بانتظام
• الحفاظ على نظافة الحقل
• استخدام بذور معتمدة
• تطبيق ممارسات زراعية جيدة
                """.strip()
        
        return """
نصائح عامة للوقاية من أمراض النباتات:

1. اختيار أصناف مقاومة للأمراض
2. تطبيق دورة زراعية مناسبة
3. تحسين تصريف التربة والتهوية
4. تجنب الإفراط في الري والتسميد
5. إزالة المخلفات النباتية المصابة
6. استخدام مبيدات وقائية عند الحاجة
7. مراقبة النباتات بانتظام

الوقاية خير من العلاج!
        """.strip()
    
    def _generate_crop_info_response(self, entities: Dict[str, List[str]], text: str) -> str:
        """توليد إجابة لمعلومات المحاصيل"""
        if 'crop_name' in entities:
            crop = entities['crop_name'][0]
            if crop in self.knowledge_base['crops']:
                crop_info = self.knowledge_base['crops'][crop]
                return f"""
معلومات عن زراعة {crop}:

الظروف المثلى:
• درجة الحرارة: {crop_info['optimal_conditions']['temperature']}
• الرطوبة: {crop_info['optimal_conditions']['humidity']}
• حموضة التربة: {crop_info['optimal_conditions']['ph']}

موسم الزراعة: {crop_info['planting_season']}
وقت الحصاد: {crop_info['harvest_time']}

الأمراض الشائعة:
{chr(10).join(f"• {disease}" for disease in crop_info['common_diseases'])}
                """.strip()
        
        return """
يرجى تحديد نوع المحصول للحصول على معلومات مفصلة عن:

• الظروف المثلى للزراعة
• مواسم الزراعة والحصاد
• الأمراض والآفات الشائعة
• نصائح الرعاية والصيانة
• متطلبات التربة والري
        """.strip()
    
    def _generate_general_response(self, text: str) -> str:
        """توليد إجابة عامة"""
        # البحث في قاعدة المعرفة العامة
        for topic, advice in self.knowledge_base['general_advice'].items():
            if any(keyword in text for keyword in [topic, advice.split()[0]]):
                return f"نصيحة حول {topic}:\n\n{advice}"
        
        return """
أهلاً بك في نظام Gaara Scan AI للزراعة الذكية!

يمكنني مساعدتك في:

🔍 تشخيص أمراض النباتات (ارفع صورة)
💊 نصائح العلاج والوقاية
🌱 معلومات عن المحاصيل المختلفة
📊 تحليل حالة المزرعة
🤖 استشارات زراعية ذكية

كيف يمكنني مساعدتك اليوم؟
        """.strip()

class AdaptiveLearningManager:
    """مدير التعلم التكيفي"""
    
    def __init__(self):
        self.learning_engines: Dict[str, AdaptiveLearningEngine] = {}
        self.nlp_processor = NLPProcessor()
        self.feedback_queue = asyncio.Queue()
        self.logger = logging.getLogger('adaptive_learning_manager')
    
    def create_learning_engine(self, model_id: str, learning_mode: LearningMode = LearningMode.SUPERVISED) -> AdaptiveLearningEngine:
        """إنشاء محرك تعلم جديد"""
        engine = AdaptiveLearningEngine(model_id, learning_mode)
        self.learning_engines[model_id] = engine
        self.logger.info(f"Created learning engine for model {model_id}")
        return engine
    
    async def process_feedback(self, model_id: str, input_data: Any, expected_output: Any, 
                             actual_output: Any, feedback_type: FeedbackType, 
                             confidence: float = 0.0, metadata: Dict[str, Any] = None) -> bool:
        """معالجة التغذية الراجعة"""
        if model_id not in self.learning_engines:
            self.logger.warning(f"Learning engine not found for model {model_id}")
            return False
        
        example = LearningExample(
            input_data=input_data,
            expected_output=expected_output,
            actual_output=actual_output,
            feedback=feedback_type,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        engine = self.learning_engines[model_id]
        return await engine.add_example(example)
    
    async def process_nlp_query(self, text: str, language: LanguageCode = LanguageCode.ARABIC, 
                               context: Dict[str, Any] = None) -> NLPQuery:
        """معالجة استعلام اللغة الطبيعية"""
        query = NLPQuery(
            text=text,
            language=language,
            context=context or {}
        )
        
        return await self.nlp_processor.process_query(query)
    
    def get_all_performance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """الحصول على مقاييس الأداء لجميع المحركات"""
        metrics = {}
        for model_id, engine in self.learning_engines.items():
            metrics[model_id] = engine.get_performance_metrics()
        return metrics
    
    async def initialize_all_engines(self) -> bool:
        """تهيئة جميع محركات التعلم"""
        try:
            for engine in self.learning_engines.values():
                await engine.load_model()
            
            self.logger.info(f"Initialized {len(self.learning_engines)} learning engines")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize learning engines: {e}")
            return False

# مثيل عام لمدير التعلم التكيفي
adaptive_learning_manager = AdaptiveLearningManager()

# دوال مساعدة
async def initialize_adaptive_learning():
    """تهيئة نظام التعلم التكيفي"""
    try:
        # إنشاء محركات التعلم للنماذج المختلفة
        adaptive_learning_manager.create_learning_engine("disease_diagnosis", LearningMode.SUPERVISED)
        adaptive_learning_manager.create_learning_engine("crop_recommendation", LearningMode.SUPERVISED)
        adaptive_learning_manager.create_learning_engine("yield_prediction", LearningMode.SUPERVISED)
        
        # تهيئة جميع المحركات
        await adaptive_learning_manager.initialize_all_engines()
        
        # إرسال حدث
        event = create_system_event(
            EventTypes.AI_MODEL_LOADED,
            "Adaptive learning system initialized"
        )
        await event_bus.publish(event)
        
        return True
        
    except Exception as e:
        logging.error(f"Failed to initialize adaptive learning: {e}")
        return False

async def submit_feedback(model_id: str, input_data: Any, expected_output: Any, 
                         actual_output: Any, feedback_type: str, confidence: float = 0.0) -> bool:
    """تقديم تغذية راجعة للنموذج"""
    try:
        feedback_enum = FeedbackType(feedback_type)
        return await adaptive_learning_manager.process_feedback(
            model_id, input_data, expected_output, actual_output, 
            feedback_enum, confidence
        )
    except ValueError:
        logging.error(f"Invalid feedback type: {feedback_type}")
        return False

async def ask_ai_question(question: str, language: str = "ar") -> Dict[str, Any]:
    """طرح سؤال على نظام الذكاء الاصطناعي"""
    try:
        lang_enum = LanguageCode(language)
        query = await adaptive_learning_manager.process_nlp_query(question, lang_enum)
        
        return {
            'success': True,
            'question': query.text,
            'answer': query.response,
            'intent': query.intent,
            'entities': query.entities,
            'confidence': query.confidence
        }
        
    except Exception as e:
        logging.error(f"Failed to process AI question: {e}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # مثال على الاستخدام
    async def main():
        # تهيئة النظام
        await initialize_adaptive_learning()
        
        # مثال على معالجة سؤال
        result = await ask_ai_question("ما هو علاج تبقع الأوراق في الطماطم؟")
        print(f"AI Response: {result}")
        
        # مثال على تقديم تغذية راجعة
        feedback_result = await submit_feedback(
            "disease_diagnosis",
            "image_data",
            "تبقع الأوراق",
            "تبقع الأوراق",
            "correct",
            0.95
        )
        print(f"Feedback submitted: {feedback_result}")
    
    asyncio.run(main())

