"""
خدمة تحسين الصور المتقدمة
Advanced Image Enhancement Service
"""

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
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
    title="Image Enhancement Service",
    description="خدمة تحسين الصور المتقدمة",
    version="1.0.0"
)

class ImageEnhancementService:
    """خدمة تحسين الصور"""
    
    def __init__(self):
        """تهيئة خدمة تحسين الصور"""
        self.enhancement_methods = {
            'brightness': self.adjust_brightness,
            'contrast': self.adjust_contrast,
            'saturation': self.adjust_saturation,
            'sharpness': self.adjust_sharpness,
            'denoise': self.denoise_image,
            'blur': self.blur_image,
            'edge_enhance': self.enhance_edges,
            'histogram_eq': self.histogram_equalization,
            'gamma_correction': self.gamma_correction,
            'auto_enhance': self.auto_enhance
        }
        logger.info("تم تهيئة خدمة تحسين الصور")
        
    def adjust_brightness(self, image: Image.Image, factor: float = 1.2) -> Image.Image:
        """تعديل السطوع"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
        
    def adjust_contrast(self, image: Image.Image, factor: float = 1.2) -> Image.Image:
        """تعديل التباين"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
        
    def adjust_saturation(self, image: Image.Image, factor: float = 1.2) -> Image.Image:
        """تعديل التشبع"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
        
    def adjust_sharpness(self, image: Image.Image, factor: float = 1.2) -> Image.Image:
        """تعديل الحدة"""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
        
    def denoise_image(self, image: Image.Image, **kwargs) -> Image.Image:
        """إزالة الضوضاء"""
        # تحويل إلى OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        denoised = cv2.fastNlMeansDenoisingColored(cv_image, None, 10, 10, 7, 21)
        # تحويل مرة أخرى إلى PIL
        return Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
        
    def blur_image(self, image: Image.Image, radius: float = 2.0) -> Image.Image:
        """تطبيق تأثير الضبابية"""
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
        
    def enhance_edges(self, image: Image.Image, **kwargs) -> Image.Image:
        """تحسين الحواف"""
        return image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
    def histogram_equalization(self, image: Image.Image, **kwargs) -> Image.Image:
        """معادلة الهيستوجرام"""
        # تحويل إلى OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # تحويل إلى LAB
        lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
        # تطبيق CLAHE على قناة L
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        # تحويل مرة أخرى
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
        
    def gamma_correction(self, image: Image.Image, gamma: float = 1.2) -> Image.Image:
        """تصحيح جاما"""
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # بناء جدول البحث
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        # تطبيق تصحيح جاما
        corrected = cv2.LUT(cv_image, table)
        return Image.fromarray(cv2.cvtColor(corrected, cv2.COLOR_BGR2RGB))
        
    def auto_enhance(self, image: Image.Image, **kwargs) -> Image.Image:
        """تحسين تلقائي شامل"""
        # تطبيق عدة تحسينات تلقائياً
        enhanced = self.adjust_contrast(image, 1.1)
        enhanced = self.adjust_brightness(enhanced, 1.05)
        enhanced = self.adjust_sharpness(enhanced, 1.1)
        enhanced = self.histogram_equalization(enhanced)
        return enhanced

# إنشاء مثيل الخدمة
enhancement_service = ImageEnhancementService()

@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "service": "Image Enhancement Service",
        "version": "1.0.0",
        "status": "active",
        "available_methods": list(enhancement_service.enhancement_methods.keys()),
        "endpoints": ["/health", "/enhance", "/methods", "/batch_enhance"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """فحص صحة الخدمة"""
    return {
        "status": "healthy",
        "available_methods": len(enhancement_service.enhancement_methods),
        "methods": list(enhancement_service.enhancement_methods.keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/enhance")
async def enhance_image(
    file: UploadFile = File(...),
    method: str = Query("auto_enhance", description="طريقة التحسين"),
    factor: float = Query(1.2, description="معامل التحسين"),
    return_base64: bool = Query(False, description="إرجاع الصورة كـ base64")
):
    """تحسين صورة واحدة"""
    try:
        if method not in enhancement_service.enhancement_methods:
            raise HTTPException(
                status_code=400, 
                detail=f"طريقة التحسين {method} غير متوفرة"
            )
            
        # قراءة الصورة
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # تطبيق التحسين
        if method in ['brightness', 'contrast', 'saturation', 'sharpness']:
            enhanced_image = enhancement_service.enhancement_methods[method](image, factor)
        elif method == 'blur':
            enhanced_image = enhancement_service.enhancement_methods[method](image, factor)
        elif method == 'gamma_correction':
            enhanced_image = enhancement_service.enhancement_methods[method](image, factor)
        else:
            enhanced_image = enhancement_service.enhancement_methods[method](image)
            
        # إعداد الاستجابة
        if return_base64:
            # تحويل إلى base64
            buffer = io.BytesIO()
            enhanced_image.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return JSONResponse(content={
                "enhanced_image": img_str,
                "method_used": method,
                "factor": factor,
                "format": "base64",
                "timestamp": datetime.now().isoformat()
            })
        else:
            # إرجاع الصورة مباشرة
            buffer = io.BytesIO()
            enhanced_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            return StreamingResponse(
                io.BytesIO(buffer.getvalue()),
                media_type="image/png",
                headers={"Content-Disposition": f"attachment; filename=enhanced_{file.filename}"}
            )
            
    except Exception as e:
        logger.error(f"خطأ في تحسين الصورة: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/methods")
async def get_available_methods():
    """الحصول على طرق التحسين المتاحة"""
    return {
        "available_methods": list(enhancement_service.enhancement_methods.keys()),
        "total_methods": len(enhancement_service.enhancement_methods),
        "descriptions": {
            "brightness": "تعديل السطوع",
            "contrast": "تعديل التباين",
            "saturation": "تعديل التشبع",
            "sharpness": "تعديل الحدة",
            "denoise": "إزالة الضوضاء",
            "blur": "تطبيق الضبابية",
            "edge_enhance": "تحسين الحواف",
            "histogram_eq": "معادلة الهيستوجرام",
            "gamma_correction": "تصحيح جاما",
            "auto_enhance": "تحسين تلقائي شامل"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "image_enhancement_service:app",
        host="0.0.0.0",
        port=8019,
        reload=False
    )

