# مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/ml_services/model_selector.py
# الوصف: خدمة اختيار النموذج المناسب لكل طلب
# المؤلف: فريق تطوير Gaara ERP
# تاريخ الإنشاء: 30 مايو 2025

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Tuple

import redis
import requests
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/app/logs/model_selector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("model_selector")

app = Flask(__name__)

# إعداد الاتصال بقاعدة البيانات
db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)

# إعداد الاتصال بـ Redis
redis_url = os.environ.get("REDIS_URL")
redis_client = redis.from_url(redis_url)

# عناوين خدمات النماذج
LOCAL_ML_URL = os.environ.get("LOCAL_ML_URL", "http://local_ml_service:5030")
PREMIUM_ML_URL = os.environ.get(
    "PREMIUM_ML_URL",
    "http://premium_ml_service:5031")
CODEX_URL = os.environ.get("CODEX_URL", "http://codex_service:5032")
PYDANTIC_URL = os.environ.get(
    "PYDANTIC_URL",
    "http://pydantic_ai_service:5033")

# تكوين النماذج وأولوياتها
MODEL_CONFIG = {
    "disease_detection": {
        "default": "local",
        "models": {
            "local": {"url": LOCAL_ML_URL, "endpoint": "/predict/disease", "priority": 1},
            "premium": {"url": PREMIUM_ML_URL, "endpoint": "/predict/disease", "priority": 2}
        }
    },
    "plant_identification": {
        "default": "local",
        "models": {
            "local": {"url": LOCAL_ML_URL, "endpoint": "/predict/plant", "priority": 1},
            "premium": {"url": PREMIUM_ML_URL, "endpoint": "/predict/plant", "priority": 2}
        }
    },
    "script_generation": {
        "default": "codex",
        "models": {
            "codex": {"url": CODEX_URL, "endpoint": "/generate/script", "priority": 1}
        }
    },
    "complex_problem_solving": {
        "default": "pydantic",
        "models": {
            "pydantic": {"url": PYDANTIC_URL, "endpoint": "/solve", "priority": 1}
        }
    },
    "image_search": {
        "default": "local",
        "models": {
            "local": {"url": LOCAL_ML_URL, "endpoint": "/search/image", "priority": 1},
            "premium": {"url": PREMIUM_ML_URL, "endpoint": "/search/image", "priority": 2}
        }
    }
}


def get_user_subscription(user_id: int) -> str:
    """
    الحصول على نوع اشتراك المستخدم من قاعدة البيانات
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT subscription_type FROM user_subscriptions WHERE user_id = :user_id"), {
                    "user_id": user_id}).fetchone()

            if result:
                return result[0]
            return "free"  # الاشتراك الافتراضي هو المجاني
    except Exception as e:
        logger.error(f"Error getting user subscription: {e}")
        return "free"


def get_model_for_task(task_type: str, user_id: int) -> Tuple[str, str, str]:
    """
    تحديد النموذج المناسب للمهمة بناءً على نوع المهمة واشتراك المستخدم
    """
    if task_type not in MODEL_CONFIG:
        logger.warning(f"Unknown task type: {task_type}, using default")
        task_type = "disease_detection"  # استخدام نوع مهمة افتراضي

    task_config = MODEL_CONFIG[task_type]
    subscription = get_user_subscription(user_id)

    # اختيار النموذج بناءً على الاشتراك
    if subscription == "premium" and "premium" in task_config["models"]:
        model_key = "premium"
    else:
        model_key = task_config["default"]

    model_info = task_config["models"][model_key]
    return model_key, model_info["url"], model_info["endpoint"]


def log_model_usage(user_id: int,
                    task_type: str,
                    model_key: str,
                    request_data: Dict[str,
                                       Any],
                    response_data: Dict[str,
                                        Any]) -> None:
    """
    تسجيل استخدام النموذج في قاعدة البيانات
    """
    try:
        with engine.connect() as connection:
            connection.execute(
                text("""
                INSERT INTO model_usage_logs
                (user_id, task_type, model_key, request_data, response_data, created_at)
                VALUES (:user_id, :task_type, :model_key, :request_data, :response_data, :created_at)
                """),
                {
                    "user_id": user_id,
                    "task_type": task_type,
                    "model_key": model_key,
                    "request_data": json.dumps(request_data),
                    "response_data": json.dumps(response_data),
                    "created_at": datetime.now()
                }
            )
            connection.commit()
    except Exception as e:
        logger.error(f"Error logging model usage: {e}")


@app.route("/health", methods=["GET"])
def health_check():
    """
    فحص صحة الخدمة
    """
    return jsonify({"status": "healthy", "service": "model_selector"}), 200


@app.route("/select", methods=["POST"])
def select_model():
    """
    اختيار النموذج المناسب وتوجيه الطلب إليه
    """
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    task_type = data.get("task_type")
    user_id = data.get("user_id")
    request_data = data.get("data", {})

    if not task_type or not user_id:
        return jsonify(
            {"error": "Missing required fields: task_type, user_id"}), 400

    try:
        # تحديد النموذج المناسب
        model_key, model_url, endpoint = get_model_for_task(task_type, user_id)

        # توجيه الطلب إلى النموذج المناسب
        full_url = f"{model_url}{endpoint}"
        response = requests.post(full_url, json=request_data, timeout=30)

        if response.status_code != 200:
            logger.error(f"Error from model service: {response.text}")
            return jsonify(
                {"error": f"Model service error: {response.text}"}), response.status_code

        response_data = response.json()

        # تسجيل استخدام النموذج
        log_model_usage(
            user_id,
            task_type,
            model_key,
            request_data,
            response_data)

        # إضافة معلومات النموذج المستخدم إلى الاستجابة
        response_data["model_info"] = {
            "model_key": model_key,
            "task_type": task_type
        }

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error in model selection: {e}")
        return jsonify({"error": f"Model selection error: {str(e)}"}), 500


@app.route("/models", methods=["GET"])
def list_models():
    """
    الحصول على قائمة النماذج المتاحة
    """
    return jsonify(MODEL_CONFIG), 200


@app.route("/models/status", methods=["GET"])
def check_models_status():
    """
    التحقق من حالة جميع النماذج
    """
    status = {}

    for task_type, task_config in MODEL_CONFIG.items():
        status[task_type] = {}

        for model_key, model_info in task_config["models"].items():
            try:
                health_url = f"{model_info['url']}/health"
                response = requests.get(health_url, timeout=5)
                status[task_type][model_key] = {
                    "status": "available" if response.status_code == 200 else "error",
                    "details": response.json() if response.status_code == 200 else {
                        "error": response.text}}
            except Exception as e:
                status[task_type][model_key] = {
                    "status": "unavailable",
                    "details": {"error": str(e)}
                }

    return jsonify(status), 200


if __name__ == "__main__":
    port = int(os.environ.get("SELECTOR_PORT", 5034))
    app.run(host="0.0.0.0", port=port)
