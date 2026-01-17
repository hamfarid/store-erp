# /home/ubuntu/gaara_erp_v12/ai_service/main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from typing import List, Optional
import redis
import json

app = FastAPI(title="Gaara ERP AI Service", version="1.0.0")

# إعداد Redis
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# تحميل النموذج المدرب
model_path = "/app/models/plant_disease_model.h5"
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
    print("✅ تم تحميل نموذج تشخيص أمراض النباتات")
else:
    model = None
    print("⚠️ لم يتم العثور على نموذج تشخيص أمراض النباتات")

# فئات الأمراض
DISEASE_CLASSES = [
    "apple_scab",
    "corn_common_rust", 
    "grape_black_rot",
    "potato_early_blight",
    "tomato_late_blight"
]

class PredictionRequest(BaseModel):
    image_data: str  # Base64 encoded image

class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    recommendations: List[str]

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    confidence: float

@app.get("/")
async def root():
    return {"message": "خدمة الذكاء الاصطناعي لنظام Gaara ERP"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "redis_connected": redis_client.ping()
    }

@app.post("/predict/plant-disease", response_model=PredictionResponse)
async def predict_plant_disease(file: UploadFile = File(...)):
    """تشخيص أمراض النباتات من الصور"""
    
    if not model:
        raise HTTPException(status_code=503, detail="النموذج غير متاح")
    
    try:
        # قراءة وتحضير الصورة
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        image = image.resize((224, 224))
        
        # تحويل إلى مصفوفة numpy
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        # التنبؤ
        predictions = model.predict(image_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        disease = DISEASE_CLASSES[predicted_class_idx]
        
        # توصيات العلاج
        recommendations = get_treatment_recommendations(disease)
        
        # حفظ النتيجة في التخزين المؤقت
        result = {
            "disease": disease,
            "confidence": confidence,
            "recommendations": recommendations
        }
        redis_client.setex(f"prediction:{file.filename}", 3600, json.dumps(result))
        
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في التنبؤ: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """محادثة مع الذكاء الاصطناعي الزراعي"""
    
    # البحث في التخزين المؤقت أولاً
    cache_key = f"chat:{hash(request.message)}"
    cached_response = redis_client.get(cache_key)
    
    if cached_response:
        return ChatResponse(**json.loads(cached_response))
    
    # معالجة الرسالة (نموذج مبسط)
    response = process_agricultural_query(request.message, request.context)
    
    result = {
        "response": response,
        "confidence": 0.85  # ثقة افتراضية
    }
    
    # حفظ في التخزين المؤقت
    redis_client.setex(cache_key, 1800, json.dumps(result))
    
    return ChatResponse(**result)

@app.get("/analytics/predictions")
async def get_prediction_analytics():
    """إحصائيات التنبؤات"""
    
    # جمع الإحصائيات من Redis
    keys = redis_client.keys("prediction:*")
    
    disease_counts = {}
    total_predictions = len(keys)
    
    for key in keys:
        data = json.loads(redis_client.get(key))
        disease = data["disease"]
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
    
    return {
        "total_predictions": total_predictions,
        "disease_distribution": disease_counts,
        "most_common_disease": max(disease_counts, key=disease_counts.get) if disease_counts else None
    }

def get_treatment_recommendations(disease: str) -> List[str]:
    """الحصول على توصيات العلاج لمرض معين"""
    
    recommendations_db = {
        "apple_scab": [
            "استخدم مبيدات فطرية وقائية قبل موسم الأمطار",
            "قم بإزالة الأوراق المتساقطة المصابة",
            "تحسين التهوية حول الأشجار"
        ],
        "corn_common_rust": [
            "استخدم أصناف مقاومة للصدأ",
            "تطبيق مبيدات فطرية عند الحاجة",
            "تجنب الري العلوي"
        ],
        "grape_black_rot": [
            "إزالة الثمار المصابة والمومياء",
            "استخدام مبيدات فطرية نحاسية",
            "تحسين تصريف التربة"
        ],
        "potato_early_blight": [
            "تطبيق مبيدات فطرية وقائية",
            "تجنب الري على الأوراق",
            "تدوير المحاصيل"
        ],
        "tomato_late_blight": [
            "استخدام مبيدات فطرية جهازية",
            "تحسين التهوية في البيوت المحمية",
            "إزالة النباتات المصابة فوراً"
        ]
    }
    
    return recommendations_db.get(disease, ["استشر خبير زراعي للحصول على توصيات محددة"])

def process_agricultural_query(message: str, context: Optional[str] = None) -> str:
    """معالجة استفسار زراعي (نموذج مبسط)"""
    
    message_lower = message.lower()
    
    if "مرض" in message_lower or "disease" in message_lower:
        return "لتشخيص الأمراض، يرجى رفع صورة واضحة للنبات المصاب. يمكنني تحليل الصورة وتقديم توصيات العلاج المناسبة."
    
    elif "ري" in message_lower or "water" in message_lower:
        return "الري المناسب يعتمد على نوع النبات والمناخ. بشكل عام، تأكد من أن التربة رطبة وليست مشبعة بالماء."
    
    elif "سماد" in message_lower or "fertilizer" in message_lower:
        return "اختيار السماد يعتمد على نوع النبات ومرحلة النمو. أنصح بإجراء تحليل للتربة لتحديد العناصر المطلوبة."
    
    else:
        return "أهلاً بك! أنا مساعد ذكي متخصص في الزراعة. يمكنني مساعدتك في تشخيص أمراض النباتات وتقديم نصائح زراعية. كيف يمكنني مساعدتك؟"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
