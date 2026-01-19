"""
خدمة YOLO للكشف عن الكائنات والأمراض
YOLO Detection Service for Objects and Plant Diseases
"""

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import io
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import os

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="YOLO Detection Service",
    description="خدمة YOLO للكشف عن الكائنات وأمراض النباتات",
    version="1.0.0"
)

class YOLODetectionService:
    """خدمة YOLO للكشف عن الكائنات"""
    
    def __init__(self):
        """تهيئة خدمة YOLO"""
        self.models = {}
        self.load_models()
        
    def load_models(self):
        """تحميل نماذج YOLO"""
        try:
            # تحميل النماذج المختلفة
            self.models['general'] = YOLO('yolov8n.pt')  # نموذج عام
            self.models['medium'] = YOLO('yolov8s.pt')   # نموذج متوسط
            self.models['large'] = YOLO('yolov8m.pt')    # نموذج كبير
            
            # تحميل نماذج مخصصة إذا كانت متوفرة
            custom_models_path = "/app/models"
            if os.path.exists(custom_models_path):
                for model_file in os.listdir(custom_models_path):
                    if model_file.endswith('.pt'):
                        model_name = model_file.replace('.pt', '')
                        self.models[model_name] = YOLO(os.path.join(custom_models_path, model_file))
                        
            logger.info(f"تم تحميل {len(self.models)} نموذج YOLO")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل نماذج YOLO: {e}")
            
    async def detect_objects(self, image: np.ndarray, model_name: str = 'general', 
                           confidence: float = 0.5) -> Dict[str, Any]:
        """كشف الكائنات في الصورة"""
        try:
            if model_name not in self.models:
                raise HTTPException(status_code=400, detail=f"النموذج {model_name} غير متوفر")
                
            model = self.models[model_name]
            results = model(image, conf=confidence)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        detection = {
                            'class_id': int(box.cls[0]),
                            'class_name': model.names[int(box.cls[0])],
                            'confidence': float(box.conf[0]),
                            'bbox': box.xyxy[0].tolist(),
                            'center': [(box.xyxy[0][0] + box.xyxy[0][2]) / 2, 
                                     (box.xyxy[0][1] + box.xyxy[0][3]) / 2]
                        }
                        detections.append(detection)
                        
            return {
                'detections': detections,
                'count': len(detections),
                'model_used': model_name,
                'confidence_threshold': confidence,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"خطأ في كشف الكائنات: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# إنشاء مثيل الخدمة
yolo_service = YOLODetectionService()

@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "service": "YOLO Detection Service",
        "version": "1.0.0",
        "status": "active",
        "available_models": list(yolo_service.models.keys()),
        "endpoints": ["/health", "/detect", "/models", "/detect_batch"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """فحص صحة الخدمة"""
    return {
        "status": "healthy",
        "models_loaded": len(yolo_service.models),
        "available_models": list(yolo_service.models.keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/detect")
async def detect_objects(
    file: UploadFile = File(...),
    model_name: str = "general",
    confidence: float = 0.5
):
    """كشف الكائنات في صورة واحدة"""
    try:
        # قراءة الصورة
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        # تحويل من RGB إلى BGR للـ OpenCV
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            
        # كشف الكائنات
        results = await yolo_service.detect_objects(image_array, model_name, confidence)
        
        return JSONResponse(content=results)
        
    except Exception as e:
        logger.error(f"خطأ في معالجة الصورة: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def get_available_models():
    """الحصول على النماذج المتاحة"""
    return {
        "available_models": list(yolo_service.models.keys()),
        "total_models": len(yolo_service.models),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "yolo_detection_service:app",
        host="0.0.0.0",
        port=8018,
        reload=False
    )

