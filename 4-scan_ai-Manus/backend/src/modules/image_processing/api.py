# File: /home/ubuntu/ai_web_organized/src/modules/image_processing/api.py
"""
واجهة برمجة التطبيقات لنظام معالجة الصور الزراعية
توفر هذه الوحدة واجهات برمجية للتفاعل مع نظام معالجة الصور الزراعية
"""

import os
from typing import Any, Dict

from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from werkzeug.utils import secure_filename

from .image_processor import ImageProcessor

# إنشاء معالج الصور
processor = ImageProcessor()

# إنشاء Blueprint للواجهة البرمجية
router = APIRouter(prefix="/api/image_processing", tags=["image_processing"])

# تحديد المجلدات
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "output")

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# تحديد الامتدادات المسموح بها
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff"}

# Constants for error messages
ERROR_FILENAME_REQUIRED = "يجب تحديد اسم الملف"


def allowed_file(filename: str) -> bool:
    """التحقق من أن امتداد الملف مسموح به"""
    return "." in filename and filename.rsplit(
        ".", 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/upload")
async def upload_image(image: UploadFile = File(...)) -> Dict[str, Any]:
    """تحميل صورة"""
    # التحقق من اسم الملف
    if not image.filename:
        raise HTTPException(status_code=400, detail="لم يتم اختيار أي ملف")

    # التحقق من امتداد الملف
    if not allowed_file(image.filename):
        raise HTTPException(
            status_code=400,
            detail="امتداد الملف غير مسموح به")

    # حفظ الصورة
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(image_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    return {
        "status": "success",
        "message": "تم تحميل الصورة بنجاح",
        "data": {"filename": filename, "path": image_path},
    }


@router.post("/process")
async def process_image(data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """معالجة صورة"""
    if not data or "filename" not in data:
        raise HTTPException(status_code=400, detail=ERROR_FILENAME_REQUIRED)

    filename = data["filename"]
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # التحقق من وجود الصورة
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404,
                            detail=f"الصورة {filename} غير موجودة")

    # تحميل الصورة
    image = processor.load_image(image_path)

    if image is None:
        raise HTTPException(
            status_code=500,
            detail=f"فشل تحميل الصورة {filename}")

    # تحديد العمليات المطلوبة
    operations = data.get("operations", [])
    processed_images = {}

    # تنفيذ العمليات المطلوبة
    for operation in operations:
        op_type = operation.get("type")
        params = operation.get("params", {})

        if op_type == "resize":
            width = params.get("width")
            height = params.get("height")
            processed_images["resize"] = processor.resize_image(
                image, width, height)

        elif op_type == "crop":
            x = params.get("x", 0)
            y = params.get("y", 0)
            width = params.get("width", 100)
            height = params.get("height", 100)
            processed_images["crop"] = processor.crop_image(
                image, x, y, width, height)

        elif op_type == "enhance_contrast":
            clip_limit = params.get("clip_limit", 2.0)
            tile_grid_size = params.get("tile_grid_size", (8, 8))
            processed_images["enhance_contrast"] = processor.enhance_contrast(
                image, clip_limit, tile_grid_size
            )

        elif op_type == "filter":
            filter_type = params.get("filter_type", "gaussian")
            kernel_size = params.get("kernel_size", 5)
            processed_images["filter"] = processor.apply_filters(
                image, filter_type, kernel_size
            )

        elif op_type == "segment":
            threshold = params.get("threshold", 128)
            mask, segmented = processor.segment_image(image, threshold)
            processed_images["segment"] = segmented
            processed_images["mask"] = mask

        elif op_type == "detect_edges":
            threshold1 = params.get("threshold1", 100)
            threshold2 = params.get("threshold2", 200)
            processed_images["edges"] = processor.detect_edges(
                image, threshold1, threshold2
            )

    # حفظ النتائج
    result_files = {}
    for op_name, processed_image in processed_images.items():
        result_filename = f"{os.path.splitext(filename)[0]}_{op_name}.jpg"
        processor.save_image(processed_image, result_filename)
        result_files[op_name] = result_filename

    # استخراج الميزات
    features = processor.extract_features(image)

    # تحليل توزيع الألوان
    color_info = processor.analyze_color_distribution(image)

    return {
        "status": "success",
        "message": "تمت معالجة الصورة بنجاح",
        "data": {
            "original_filename": filename,
            "result_files": result_files,
            "features": features,
            "color_info": color_info,
        },
    }


@router.post("/analyze")
async def analyze_image(data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """تحليل صورة"""
    if not data or "filename" not in data:
        raise HTTPException(status_code=400, detail=ERROR_FILENAME_REQUIRED)

    filename = data["filename"]
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # التحقق من وجود الصورة
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404,
                            detail=f"الصورة {filename} غير موجودة")

    # تحميل الصورة
    image = processor.load_image(image_path)

    if image is None:
        raise HTTPException(
            status_code=500,
            detail=f"فشل تحميل الصورة {filename}")

    # استخراج الميزات
    features = processor.extract_features(image)

    # تحليل توزيع الألوان
    color_info = processor.analyze_color_distribution(image)

    # تحليل الجودة - استخدام الطريقة الداخلية المتوفرة
    quality_metrics = processor._calculate_quality_score(image)

    return {
        "status": "success",
        "message": "تم تحليل الصورة بنجاح",
        "data": {
            "filename": filename,
            "features": features,
            "color_info": color_info,
            "quality_metrics": quality_metrics,
        },
    }


@router.get("/download/{filename}")
async def download_image(filename: str) -> FileResponse:
    """تنزيل صورة معالجة"""
    file_path = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"الملف {filename} غير موجود")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream")


@router.post("/visualize")
async def visualize_image(data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """إنشاء تصور للصورة"""
    if not data or "filename" not in data:
        raise HTTPException(status_code=400, detail=ERROR_FILENAME_REQUIRED)

    filename = data["filename"]
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # التحقق من وجود الصورة
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404,
                            detail=f"الصورة {filename} غير موجودة")

    # تحميل الصورة
    image = processor.load_image(image_path)

    if image is None:
        raise HTTPException(
            status_code=500,
            detail=f"فشل تحميل الصورة {filename}")

    # إنشاء التصور
    visualization_type = data.get("type", "histogram")

    if visualization_type == "histogram":
        # استخدام الطريقة المتوفرة لتحليل توزيع الألوان
        color_info = processor.analyze_color_distribution(image)
        viz_filename = f"{os.path.splitext(filename)[0]}_histogram.json"
        viz_path = os.path.join(OUTPUT_FOLDER, viz_filename)

        # حفظ بيانات الهيستوجرام كملف JSON
        import json
        with open(viz_path, 'w', encoding='utf-8') as f:
            json.dump(color_info, f, ensure_ascii=False, indent=2)

    elif visualization_type == "color_distribution":
        # استخدام الطريقة المتوفرة لتحليل توزيع الألوان
        color_info = processor.analyze_color_distribution(image)
        viz_filename = f"{os.path.splitext(filename)[0]}_color_distribution.json"
        viz_path = os.path.join(OUTPUT_FOLDER, viz_filename)

        # حفظ بيانات توزيع الألوان كملف JSON
        import json
        with open(viz_path, 'w', encoding='utf-8') as f:
            json.dump(color_info, f, ensure_ascii=False, indent=2)

    else:
        raise HTTPException(status_code=400, detail="نوع التصور غير مدعوم")

    return {
        "status": "success",
        "message": "تم إنشاء التصور بنجاح",
        "data": {
            "original_filename": filename,
            "visualization_filename": viz_filename,
            "visualization_type": visualization_type,
        },
    }
