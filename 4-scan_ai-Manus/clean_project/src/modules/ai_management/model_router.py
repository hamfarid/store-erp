# File: /home/ubuntu/ai_web_organized/src/modules/ai_management/model_router.py
"""
موجه نماذج الذكاء الاصطناعي
يوفر هذا الملف آلية لتوجيه الطلبات بين نماذج الذكاء الاصطناعي المختلفة
"""

import os
import json
import logging
import time
from datetime import datetime
import threading
import queue

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AIModelRouter:
    """موجه نماذج الذكاء الاصطناعي"""

    # Constants for repeated string literals
    MODELS_SECTION_NOT_FOUND = "قسم النماذج غير موجود"

    # أنواع النماذج المدعومة
    MODEL_TYPES = {
        "local": "نموذج محلي",
        "cloud": "نموذج سحابي",
        "codex": "نموذج Codex",
        "pydantic": "نموذج Pydantic AI"
    }

    def __init__(self, config_path=None):
        """
        تهيئة موجه النماذج

        المعلمات:
            config_path (str, optional): مسار ملف التكوين
        """
        # مسار ملف التكوين
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                'config',
                'models_config.json')

        # التأكد من وجود مجلد التكوين
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # تكوين النماذج
        self.models_config = {}

        # النماذج المتاحة
        self.available_models = {}

        # قائمة انتظار الطلبات
        self.request_queue = queue.Queue()

        # سجل الطلبات
        self.request_history = []

        # تحميل التكوين
        self._load_config()

        # تهيئة النماذج
        self._initialize_models()

        # بدء معالج الطلبات
        self._start_request_processor()

        logger.info("تم تهيئة موجه نماذج الذكاء الاصطناعي")

    def _load_config(self):
        """تحميل تكوين النماذج من الملف"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.models_config = json.load(f)
                logger.info("تم تحميل تكوين النماذج من %s", self.config_path)
            else:
                logger.warning("ملف تكوين النماذج غير موجود: %s", self.config_path)
                # إنشاء تكوين افتراضي
                self._create_default_config()
        except Exception as e:
            logger.error("خطأ أثناء تحميل تكوين النماذج: %s", str(e))
            # إنشاء تكوين افتراضي
            self._create_default_config()

    def _create_default_config(self):
        """إنشاء تكوين افتراضي للنماذج"""
        self.models_config = {
            "models": {
                "local_general": {
                    "name": "النموذج المحلي العام",
                    "type": "local",
                    "description": "نموذج محلي للاستخدام العام",
                    "capabilities": [
                        "text_generation",
                        "question_answering",
                        "summarization"],
                    "max_tokens": 4096,
                    "enabled": True,
                    "priority": 1,
                    "cost_per_token": 0,
                    "model_path": "models/local_general",
                    "api_key_required": False},
                "cloud_advanced": {
                    "name": "النموذج السحابي المتقدم",
                    "type": "cloud",
                    "description": "نموذج سحابي متقدم للمهام المعقدة",
                    "capabilities": [
                        "text_generation",
                        "question_answering",
                        "summarization",
                        "code_generation",
                        "image_analysis"],
                    "max_tokens": 16384,
                    "enabled": True,
                    "priority": 2,
                    "cost_per_token": 0.0001,
                    "api_endpoint": "https://api.example.com/v1/completions",
                    "api_key_required": True},
                "codex_script": {
                    "name": "نموذج Codex للسكربتات",
                    "type": "codex",
                            "description": "نموذج متخصص لتحليل إجراءات المزارع وتوليد سكربتات",
                            "capabilities": [
                                "code_generation",
                                "script_analysis",
                                "process_automation"],
                    "max_tokens": 8192,
                    "enabled": True,
                    "priority": 3,
                    "cost_per_token": 0.0002,
                    "api_endpoint": "https://api.example.com/v1/codex",
                    "api_key_required": True},
                "pydantic_complex": {
                    "name": "نموذج Pydantic للمهام المعقدة",
                    "type": "pydantic",
                    "description": "نموذج متخصص للمهام المعقدة متعددة الخطوات",
                    "capabilities": [
                        "complex_problem_solving",
                        "multi_step_reasoning",
                        "structured_output"],
                    "max_tokens": 16384,
                    "enabled": True,
                    "priority": 4,
                    "cost_per_token": 0.0003,
                    "api_endpoint": "https://api.example.com/v1/pydantic",
                    "api_key_required": True}},
            "routing_rules": {
                "default_model": "local_general",
                "capability_mapping": {
                    "text_generation": [
                        "local_general",
                        "cloud_advanced"],
                    "question_answering": [
                        "local_general",
                        "cloud_advanced"],
                    "summarization": [
                        "local_general",
                        "cloud_advanced"],
                    "code_generation": [
                        "codex_script",
                        "cloud_advanced"],
                    "script_analysis": ["codex_script"],
                    "process_automation": [
                        "codex_script",
                        "pydantic_complex"],
                    "complex_problem_solving": [
                        "pydantic_complex",
                        "cloud_advanced"],
                    "multi_step_reasoning": ["pydantic_complex"],
                    "structured_output": ["pydantic_complex"],
                    "image_analysis": ["cloud_advanced"]},
                "token_thresholds": {
                    "local_general": 4000,
                    "cloud_advanced": 16000,
                    "codex_script": 8000,
                    "pydantic_complex": 16000},
                "cost_thresholds": {
                    "free": ["local_general"],
                    "low_cost": ["cloud_advanced"],
                    "medium_cost": ["codex_script"],
                    "high_cost": ["pydantic_complex"]},
                "user_preferences": {}}}

        # حفظ التكوين
        self._save_config()

        logger.info("تم إنشاء تكوين افتراضي للنماذج")

    def _save_config(self):
        """حفظ تكوين النماذج في الملف"""
        try:
            # التأكد من وجود مجلد التكوين
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            # حفظ التكوين
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.models_config, f, ensure_ascii=False, indent=2)

            logger.info("تم حفظ تكوين النماذج في %s", self.config_path)
            return True
        except Exception as e:
            logger.error("خطأ أثناء حفظ تكوين النماذج: %s", str(e))
            return False

    def _initialize_models(self):
        """تهيئة النماذج المتاحة"""
        try:
            # مسح قائمة النماذج المتاحة
            self.available_models = {}

            # تهيئة النماذج المفعلة
            for model_id, model_config in self.models_config.get(
                    "models", {}).items():
                if model_config.get("enabled", False):
                    try:
                        # إضافة النموذج إلى القائمة
                        self.available_models[model_id] = {
                            "id": model_id,
                            "name": model_config.get("name", model_id),
                            "type": model_config.get("type", "unknown"),
                            "description": model_config.get("description", ""),
                            "capabilities": model_config.get("capabilities", []),
                            "max_tokens": model_config.get("max_tokens", 0),
                            "priority": model_config.get("priority", 0),
                            "cost_per_token": model_config.get("cost_per_token", 0),
                            "status": "ready",
                            "last_used": None,
                            "total_requests": 0,
                            "total_tokens": 0,
                            "total_cost": 0
                        }

                        logger.info("تم تهيئة النموذج %s", model_id)
                    except Exception as e:
                        logger.error("خطأ أثناء تهيئة النموذج %s: %s", model_id, str(e))

            logger.info("تم تهيئة %s نموذج", len(self.available_models))
        except Exception as e:
            logger.error("خطأ أثناء تهيئة النماذج: %s", str(e))

    def _start_request_processor(self):
        """بدء معالج الطلبات في خلفية"""
        self.processor_thread = threading.Thread(
            target=self._process_requests, daemon=True)
        self.processor_thread.start()
        logger.info("تم بدء معالج الطلبات")

    def _process_requests(self):
        """معالجة الطلبات في قائمة الانتظار"""
        while True:
            try:
                # استخراج طلب من قائمة الانتظار
                request = self.request_queue.get()

                # معالجة الطلب
                self._handle_request(request)

                # تحديد انتهاء معالجة الطلب
                self.request_queue.task_done()
            except Exception as e:
                logger.error("خطأ أثناء معالجة الطلبات: %s", str(e))

            # انتظار قصير
            time.sleep(0.1)

    def _handle_request(self, request):
        """
        معالجة طلب

        المعلمات:
            request (dict): بيانات الطلب
        """
        try:
            # استخراج معلومات الطلب
            request_id = request.get("request_id")
            model_id = request.get("model_id")
            callback = request.get("callback")

            # التحقق من وجود النموذج
            if model_id not in self.available_models:
                error_message = f"النموذج {model_id} غير موجود"
                logger.error(error_message)

                # استدعاء دالة الاستجابة مع الخطأ
                if callback:
                    callback({
                        "success": False,
                        "error": error_message,
                        "request_id": request_id
                    })

                return

            # تحديث حالة النموذج
            self.available_models[model_id]["status"] = "busy"
            self.available_models[model_id]["last_used"] = datetime.now(
            ).isoformat()
            self.available_models[model_id]["total_requests"] += 1

            # محاكاة معالجة الطلب
            logger.info("معالجة الطلب %s باستخدام النموذج {model_id}", request_id)

            # محاكاة وقت المعالجة
            time.sleep(1)

            # إنشاء استجابة
            input_text = request.get("input", {}).get("text", "")
            input_tokens = len(input_text.split())
            output_text = f"استجابة من النموذج {model_id} للطلب {request_id}: {input_text}"
            output_tokens = len(output_text.split())
            total_tokens = input_tokens + output_tokens

            # تحديث إحصائيات النموذج
            self.available_models[model_id]["total_tokens"] += total_tokens
            self.available_models[model_id]["total_cost"] += total_tokens * \
                self.available_models[model_id]["cost_per_token"]

            # إنشاء استجابة
            response = {
                "success": True,
                "request_id": request_id,
                "model_id": model_id,
                "output": {
                    "text": output_text,
                    "tokens": output_tokens},
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "cost": total_tokens
                    * self.available_models[model_id]["cost_per_token"]},
                "timestamp": datetime.now().isoformat()}

            # إضافة الطلب إلى السجل
            self.request_history.append({
                "request_id": request_id,
                "model_id": model_id,
                "input": request.get("input"),
                "output": response.get("output"),
                "usage": response.get("usage"),
                "timestamp": response.get("timestamp")
            })

            # تحديث حالة النموذج
            self.available_models[model_id]["status"] = "ready"

            # استدعاء دالة الاستجابة
            if callback:
                callback(response)

            logger.info("تم معالجة الطلب %s بنجاح", request_id)
        except Exception as e:
            error_message = f"خطأ أثناء معالجة الطلب {request.get('request_id')}: {str(e)}"
            logger.error(error_message)

            # تحديث حالة النموذج
            if model_id in self.available_models:
                self.available_models[model_id]["status"] = "ready"

            # استدعاء دالة الاستجابة مع الخطأ
            if callback:
                callback({
                    "success": False,
                    "error": error_message,
                    "request_id": request.get("request_id")
                })

    def get_available_models(self, capability=None, user_id=None):
        """
        الحصول على قائمة النماذج المتاحة

        المعلمات:
            capability (str, optional): القدرة المطلوبة
            user_id (str, optional): معرف المستخدم

        العائد:
            list: قائمة النماذج المتاحة
        """
        try:
            # استخراج النماذج المتاحة
            models = []

            for model_id, model_info in self.available_models.items():
                # التحقق من القدرة المطلوبة
                if capability and capability not in model_info.get(
                        "capabilities", []):
                    continue

                # التحقق من تفضيلات المستخدم
                if user_id:
                    user_preferences = self.models_config.get(
                        "routing_rules",
                        {}).get(
                        "user_preferences",
                        {}).get(
                        user_id,
                        {})
                    if "excluded_models" in user_preferences and model_id in user_preferences[
                            "excluded_models"]:
                        continue

                # إضافة النموذج إلى القائمة
                models.append({
                    "id": model_id,
                    "name": model_info.get("name"),
                    "type": model_info.get("type"),
                    "description": model_info.get("description"),
                    "capabilities": model_info.get("capabilities"),
                    "status": model_info.get("status")
                })

            # ترتيب النماذج حسب الأولوية
            models.sort(
                key=lambda x: self.available_models[x["id"]]["priority"])

            return models
        except Exception as e:
            logger.error("خطأ أثناء استرجاع النماذج المتاحة: %s", str(e))
            return []

    def select_model(self, request_info):
        """
        اختيار النموذج المناسب للطلب

        المعلمات:
            request_info (dict): معلومات الطلب

        العائد:
            str: معرف النموذج المختار
        """
        try:
            # استخراج معلومات الطلب
            capabilities = request_info.get("capabilities", [])
            token_count = request_info.get("token_count", 0)
            user_id = request_info.get("user_id")
            cost_level = request_info.get("cost_level", "free")

            # الحصول على قواعد التوجيه
            routing_rules = self.models_config.get("routing_rules", {})
            default_model = routing_rules.get("default_model")
            capability_mapping = routing_rules.get("capability_mapping", {})
            token_thresholds = routing_rules.get("token_thresholds", {})
            cost_thresholds = routing_rules.get("cost_thresholds", {})

            # الحصول على تفضيلات المستخدم
            user_preferences = routing_rules.get(
                "user_preferences", {}).get(
                user_id, {})
            preferred_model = user_preferences.get("preferred_model")

            # التحقق من النموذج المفضل للمستخدم
            if preferred_model and preferred_model in self.available_models:
                model_info = self.available_models[preferred_model]

                # التحقق من القدرات المطلوبة
                if all(capability in model_info.get("capabilities", [])
                       for capability in capabilities):
                    # التحقق من حد الرموز
                    if token_count <= model_info.get("max_tokens", 0):
                        return preferred_model

            # إنشاء قائمة النماذج المرشحة
            candidate_models = []

            # إضافة النماذج التي تدعم جميع القدرات المطلوبة
            for capability in capabilities:
                if capability in capability_mapping:
                    models_for_capability = capability_mapping[capability]

                    if not candidate_models:
                        candidate_models = models_for_capability
                    else:
                        candidate_models = [
                            model for model in candidate_models if model in models_for_capability]

            # إذا لم يتم العثور على نماذج مرشحة، استخدام النموذج الافتراضي
            if not candidate_models:
                return default_model

            # تصفية النماذج حسب حد الرموز
            candidate_models = [
                model for model in candidate_models if model in token_thresholds and token_count <= token_thresholds[model]]

            # إذا لم يتم العثور على نماذج مرشحة، استخدام النموذج الافتراضي
            if not candidate_models:
                return default_model

            # تصفية النماذج حسب مستوى التكلفة
            if cost_level in cost_thresholds:
                cost_models = cost_thresholds[cost_level]
                candidate_models = [
                    model for model in candidate_models if model in cost_models]

            # إذا لم يتم العثور على نماذج مرشحة، استخدام النموذج الافتراضي
            if not candidate_models:
                return default_model

            # ترتيب النماذج المرشحة حسب الأولوية
            candidate_models.sort(
                key=lambda x: self.available_models[x]["priority"] if x in self.available_models else float('inf'))

            # اختيار النموذج الأول
            if candidate_models:
                return candidate_models[0]

            # استخدام النموذج الافتراضي
            return default_model
        except Exception as e:
            logger.error("خطأ أثناء اختيار النموذج: %s", str(e))
            # استخدام النموذج الافتراضي
            return self.models_config.get(
                "routing_rules", {}).get("default_model")

    def submit_request(self, request_info, callback=None):
        """
        تقديم طلب للمعالجة

        المعلمات:
            request_info (dict): معلومات الطلب
            callback (function, optional): دالة الاستجابة

        العائد:
            dict: معلومات الطلب
        """
        try:
            # إنشاء معرف الطلب
            request_id = f"req_{int(time.time())}_{hash(str(request_info)) % 10000}"

            # اختيار النموذج المناسب
            model_id = request_info.get("model_id")

            if not model_id:
                model_id = self.select_model(request_info)

            # التحقق من وجود النموذج
            if model_id not in self.available_models:
                error_message = f"النموذج {model_id} غير موجود"
                logger.error(error_message)

                if callback:
                    callback({
                        "success": False,
                        "error": error_message,
                        "request_id": request_id
                    })

                return {
                    "success": False,
                    "error": error_message,
                    "request_id": request_id
                }

            # إنشاء طلب
            request = {
                "request_id": request_id,
                "model_id": model_id,
                "input": request_info.get("input", {}),
                "parameters": request_info.get("parameters", {}),
                "user_id": request_info.get("user_id"),
                "timestamp": datetime.now().isoformat(),
                "callback": callback
            }

            # إضافة الطلب إلى قائمة الانتظار
            self.request_queue.put(request)

            logger.info("تم تقديم الطلب %s للمعالجة باستخدام النموذج {model_id}", request_id)

            return {
                "success": True,
                "request_id": request_id,
                "model_id": model_id,
                "status": "pending",
                "timestamp": request["timestamp"]
            }
        except Exception as e:
            error_message = f"خطأ أثناء تقديم الطلب: {str(e)}"
            logger.error(error_message)

            if callback:
                callback({
                    "success": False,
                    "error": error_message,
                    "request_id": f"error_{int(time.time())}"
                })

            return {
                "success": False,
                "error": error_message,
                "request_id": f"error_{int(time.time())}"
            }

    def get_model_stats(self, model_id=None):
        """
        الحصول على إحصائيات النموذج

        المعلمات:
            model_id (str, optional): معرف النموذج

        العائد:
            dict: إحصائيات النموذج
        """
        try:
            if model_id:
                # التحقق من وجود النموذج
                if model_id not in self.available_models:
                    return {
                        "success": False,
                        "error": f"النموذج {model_id} غير موجود"
                    }

                # استخراج إحصائيات النموذج
                model_info = self.available_models[model_id]

                return {
                    "success": True,
                    "model_id": model_id,
                    "name": model_info.get("name"),
                    "type": model_info.get("type"),
                    "status": model_info.get("status"),
                    "last_used": model_info.get("last_used"),
                    "total_requests": model_info.get("total_requests"),
                    "total_tokens": model_info.get("total_tokens"),
                    "total_cost": model_info.get("total_cost")
                }
            else:
                # استخراج إحصائيات جميع النماذج
                stats = {}

                for model_id, model_info in self.available_models.items():
                    stats[model_id] = {
                        "name": model_info.get("name"),
                        "type": model_info.get("type"),
                        "status": model_info.get("status"),
                        "last_used": model_info.get("last_used"),
                        "total_requests": model_info.get("total_requests"),
                        "total_tokens": model_info.get("total_tokens"),
                        "total_cost": model_info.get("total_cost")
                    }

                return {
                    "success": True,
                    "stats": stats
                }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع إحصائيات النموذج: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع إحصائيات النموذج: {str(e)}"
            }

    def get_request_history(self, limit=10, user_id=None):
        """
        الحصول على سجل الطلبات

        المعلمات:
            limit (int, optional): عدد الطلبات المراد استرجاعها
            user_id (str, optional): معرف المستخدم

        العائد:
            list: سجل الطلبات
        """
        try:
            # تصفية الطلبات حسب المستخدم
            if user_id:
                filtered_history = [
                    request for request in self.request_history if request.get("user_id") == user_id]
            else:
                filtered_history = self.request_history

            # ترتيب الطلبات حسب التاريخ (من الأحدث إلى الأقدم)
            sorted_history = sorted(
                filtered_history, key=lambda x: x.get(
                    "timestamp", ""), reverse=True)

            # تحديد عدد الطلبات المراد استرجاعها
            limited_history = sorted_history[:limit]

            return limited_history
        except Exception as e:
            logger.error("خطأ أثناء استرجاع سجل الطلبات: %s", str(e))
            return []

    def update_user_preferences(self, user_id, preferences):
        """
        تحديث تفضيلات المستخدم

        المعلمات:
            user_id (str): معرف المستخدم
            preferences (dict): تفضيلات المستخدم

        العائد:
            bool: نجاح العملية
        """
        try:
            # التأكد من وجود قسم تفضيلات المستخدم
            if "routing_rules" not in self.models_config:
                self.models_config["routing_rules"] = {}

            if "user_preferences" not in self.models_config["routing_rules"]:
                self.models_config["routing_rules"]["user_preferences"] = {}

            # تحديث تفضيلات المستخدم
            self.models_config["routing_rules"]["user_preferences"][user_id] = preferences

            # حفظ التكوين
            self._save_config()

            logger.info("تم تحديث تفضيلات المستخدم %s", user_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تحديث تفضيلات المستخدم: %s", str(e))
            return False

    def update_model_config(self, model_id, config):
        """
        تحديث تكوين النموذج

        المعلمات:
            model_id (str): معرف النموذج
            config (dict): تكوين النموذج

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود قسم النماذج
            if "models" not in self.models_config:
                self.models_config["models"] = {}

            # تحديث تكوين النموذج
            self.models_config["models"][model_id] = config

            # حفظ التكوين
            self._save_config()

            # إعادة تهيئة النماذج
            self._initialize_models()

            logger.info("تم تحديث تكوين النموذج %s", model_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تحديث تكوين النموذج: %s", str(e))
            return False

    def update_routing_rules(self, rules):
        """
        تحديث قواعد التوجيه

        المعلمات:
            rules (dict): قواعد التوجيه

        العائد:
            bool: نجاح العملية
        """
        try:
            # تحديث قواعد التوجيه
            self.models_config["routing_rules"] = rules

            # حفظ التكوين
            self._save_config()

            logger.info("تم تحديث قواعد التوجيه")
            return True
        except Exception as e:
            logger.error("خطأ أثناء تحديث قواعد التوجيه: %s", str(e))
            return False

    def add_model(self, model_id, config):
        """
        إضافة نموذج جديد

        المعلمات:
            model_id (str): معرف النموذج
            config (dict): تكوين النموذج

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود قسم النماذج
            if "models" not in self.models_config:
                self.models_config["models"] = {}

            # التحقق من وجود النموذج
            if model_id in self.models_config["models"]:
                logger.warning("النموذج %s موجود بالفعل", model_id)
                return False

            # إضافة النموذج
            self.models_config["models"][model_id] = config

            # حفظ التكوين
            self._save_config()

            # إعادة تهيئة النماذج
            self._initialize_models()

            logger.info("تم إضافة النموذج %s", model_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء إضافة النموذج: %s", str(e))
            return False

    def remove_model(self, model_id):
        """
        إزالة نموذج

        المعلمات:
            model_id (str): معرف النموذج

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود قسم النماذج
            if "models" not in self.models_config:
                logger.warning("قسم النماذج غير موجود")
                return False

            # التحقق من وجود النموذج
            if model_id not in self.models_config["models"]:
                logger.warning("النموذج %s غير موجود", model_id)
                return False

            # إزالة النموذج
            del self.models_config["models"][model_id]

            # حفظ التكوين
            self._save_config()

            # إعادة تهيئة النماذج
            self._initialize_models()

            logger.info("تم إزالة النموذج %s", model_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء إزالة النموذج: %s", str(e))
            return False

    def enable_model(self, model_id):
        """
        تفعيل نموذج

        المعلمات:
            model_id (str): معرف النموذج

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود قسم النماذج
            if "models" not in self.models_config:
                logger.warning("قسم النماذج غير موجود")
                return False

            # التحقق من وجود النموذج
            if model_id not in self.models_config["models"]:
                logger.warning("النموذج %s غير موجود", model_id)
                return False

            # تفعيل النموذج
            self.models_config["models"][model_id]["enabled"] = True

            # حفظ التكوين
            self._save_config()

            # إعادة تهيئة النماذج
            self._initialize_models()

            logger.info("تم تفعيل النموذج %s", model_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تفعيل النموذج: %s", str(e))
            return False

    def disable_model(self, model_id):
        """
        تعطيل نموذج

        المعلمات:
            model_id (str): معرف النموذج

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود قسم النماذج
            if "models" not in self.models_config:
                logger.warning("قسم النماذج غير موجود")
                return False

            # التحقق من وجود النموذج
            if model_id not in self.models_config["models"]:
                logger.warning("النموذج %s غير موجود", model_id)
                return False

            # تعطيل النموذج
            self.models_config["models"][model_id]["enabled"] = False

            # حفظ التكوين
            self._save_config()

            # إعادة تهيئة النماذج
            self._initialize_models()

            logger.info("تم تعطيل النموذج %s", model_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تعطيل النموذج: %s", str(e))
            return False
