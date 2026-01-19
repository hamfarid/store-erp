# File: /home/ubuntu/clean_project/src/api/yolo_detection.py
"""
واجهة برمجة التطبيقات لكشف الكائنات باستخدام YOLO
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import json
import uuid
from datetime import datetime
import os

router = APIRouter()

# مجلد حفظ نتائج الكشف
DETECTION_RESULTS_DIR = "/tmp/yolo_detection"
os.makedirs(DETECTION_RESULTS_DIR, exist_ok=True)

# بيانات وهمية للإحصائيات
detection_stats = {
    "total_detections": 1856,
    "objects_detected": 4729,
    "accuracy_rate": 92,
    "avg_processing_time": 145
}

# سجل عمليات الكشف
detection_history = [
    {
        "id": 1,
        "image_thumbnail": "/api/images/thumbnails/detection_001.jpg",
        "original_image_url": "/api/images/original/detection_001.jpg",
        "model_name": "YOLOv8m",
        "objects_count": 5,
        "avg_confidence": 0.87,
        "processing_time": 142,
        "status": "completed",
        "created_at": "2024-01-15T10:30:00Z",
        "settings": {
            "model": "yolov8m",
            "confidence_threshold": 0.5,
            "iou_threshold": 0.45
        }
    },
    {
        "id": 2,
        "image_thumbnail": "/api/images/thumbnails/detection_002.jpg",
        "original_image_url": "/api/images/original/detection_002.jpg",
        "model_name": "YOLOv8l",
        "objects_count": 3,
        "avg_confidence": 0.94,
        "processing_time": 198,
        "status": "completed",
        "created_at": "2024-01-14T15:45:00Z",
        "settings": {
            "model": "yolov8l",
            "confidence_threshold": 0.6,
            "iou_threshold": 0.4
        }
    }
]


@router.get("/stats")
async def get_detection_stats():
    """الحصول على إحصائيات الكشف"""
    return {"data": detection_stats}


@router.post("/detect")
async def detect_objects(
    image: UploadFile = File(...),
    settings: str = Form(...)
):
    """كشف الكائنات في الصورة باستخدام YOLO"""
    try:
        # تحليل الإعدادات
        detection_settings = json.loads(settings)

        # قراءة الصورة
        image_data = await image.read()

        # محاكاة عملية الكشف
        # في التطبيق الحقيقي، هنا سيتم استخدام نموذج YOLO

        # إنشاء معرف فريد للكشف
        detection_id = str(uuid.uuid4())

        # حفظ الصورة الأصلية (محاكاة)
        original_path = f"{DETECTION_RESULTS_DIR}/original_{detection_id}.jpg"
        with open(original_path, "wb") as f:
            f.write(image_data)

        # محاكاة نتائج الكشف
        detected_objects = [
            {
                "class_name": "شخص",
                "confidence": 0.89,
                "bbox": {
                    "x": 120,
                    "y": 80,
                    "width": 150,
                    "height": 300
                }
            },
            {
                "class_name": "سيارة",
                "confidence": 0.76,
                "bbox": {
                    "x": 300,
                    "y": 200,
                    "width": 200,
                    "height": 120
                }
            },
            {
                "class_name": "كلب",
                "confidence": 0.92,
                "bbox": {
                    "x": 50,
                    "y": 350,
                    "width": 80,
                    "height": 60
                }
            }
        ]

        # تصفية الكائنات حسب حد الثقة
        confidence_threshold = detection_settings.get("confidence_threshold", 0.5)
        filtered_objects = [
            obj for obj in detected_objects
            if obj["confidence"] >= confidence_threshold
        ]

        # إنشاء URL للصورة المعلمة
        annotated_image_url = f"/api/images/annotated/annotated_{detection_id}.jpg"

        result = {
            "detection_id": detection_id,
            "objects": filtered_objects,
            "annotated_image_url": annotated_image_url,
            "processing_time": 145,
            "model_accuracy": 92,
            "total_objects": len(filtered_objects),
            "model_used": detection_settings.get("model", "yolov8m")
        }

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في كشف الكائنات: {str(e)}")


@router.get("/history")
async def get_detection_history():
    """الحصول على سجل عمليات الكشف"""
    return {"data": detection_history}


@router.post("/save")
async def save_detection(data: Dict[str, Any]):
    """حفظ نتائج الكشف"""
    try:
        new_record = {
            "id": len(detection_history) + 1,
            "image_thumbnail": data.get("original_image"),
            "original_image_url": data.get("original_image"),
            "model_name": data.get("results", {}).get("model_used", "YOLOv8"),
            "objects_count": data.get("results", {}).get("total_objects", 0),
            "avg_confidence": sum(obj.get("confidence", 0) for obj in data.get("results", {}).get("objects", [])) / max(len(data.get("results", {}).get("objects", [])), 1),
            "processing_time": data.get("results", {}).get("processing_time", 0),
            "status": "completed",
            "created_at": datetime.now().isoformat() + "Z",
            "settings": data.get("settings", {})
        }

        detection_history.append(new_record)

        return {"message": "تم حفظ نتائج الكشف بنجاح"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في حفظ الكشف: {str(e)}")


@router.delete("/history/{detection_id}")
async def delete_detection(detection_id: int):
    """حذف عملية كشف"""
    try:
        global detection_history
        detection_history = [record for record in detection_history if record["id"] != detection_id]
        return {"message": "تم حذف عملية الكشف بنجاح"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في حذف العملية: {str(e)}")


@router.get("/export/history")
async def export_history():
    """تصدير سجل عمليات الكشف"""
    try:
        # محاكاة تصدير السجل كملف Excel
        return {
            "data": "محتوى ملف Excel",
            "filename": f"yolo-detection-history-{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تصدير السجل: {str(e)}")


@router.get("/results/{detection_id}")
async def download_results(detection_id: int):
    """تحميل نتائج الكشف"""
    try:
        record = next((r for r in detection_history if r["id"] == detection_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="عملية الكشف غير موجودة")

        # محاكاة إنشاء ملف ZIP للنتائج
        return {
            "data": "محتوى ملف ZIP",
            "filename": f"detection-{detection_id}.zip"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تحميل النتائج: {str(e)}")
