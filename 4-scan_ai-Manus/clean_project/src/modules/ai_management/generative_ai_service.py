# File: /home/ubuntu/clean_project/src/modules/ai_management/generative_ai_service.py
"""
خدمة الذكاء الاصطناعي التوليدي المتقدمة
تتضمن نماذج لغوية كبيرة، نماذج توليد الصور، وتقنيات Diffusion Models
"""

import os
import json
import logging
import asyncio
import aiohttp
import numpy as np
import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    AutoModelForSeq2SeqLM, pipeline,
    BlipProcessor, BlipForConditionalGeneration
)
from diffusers import StableDiffusionPipeline, DiffusionPipeline
from PIL import Image
import io
import base64
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
import threading
import queue
from dataclasses import dataclass

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GenerativeRequest:
    """طلب الذكاء الاصطناعي التوليدي"""
    request_id: str
    request_type: str  # 'text', 'image', 'multimodal'
    prompt: str
    parameters: Dict[str, Any]
    user_id: str
    timestamp: datetime
    priority: int = 1

@dataclass
class GenerativeResponse:
    """استجابة الذكاء الاصطناعي التوليدي"""
    request_id: str
    response_type: str
    content: Union[str, bytes, Dict]
    metadata: Dict[str, Any]
    processing_time: float
    model_used: str
    timestamp: datetime

class LLMManager:
    """مدير النماذج اللغوية الكبيرة"""
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_models()
    
    def load_models(self):
        """تحميل النماذج اللغوية"""
        try:
            # نموذج محلي للمحادثة العامة
            model_name = "microsoft/DialoGPT-medium"
            self.tokenizers['dialog'] = AutoTokenizer.from_pretrained(model_name)
            self.models['dialog'] = AutoModelForCausalLM.from_pretrained(model_name)
            
            # نموذج للتلخيص
            summary_model = "facebook/bart-large-cnn"
            self.tokenizers['summary'] = AutoTokenizer.from_pretrained(summary_model)
            self.models['summary'] = AutoModelForSeq2SeqLM.from_pretrained(summary_model)
            
            # نموذج للترجمة
            translation_model = "Helsinki-NLP/opus-mt-en-ar"
            self.tokenizers['translation'] = AutoTokenizer.from_pretrained(translation_model)
            self.models['translation'] = AutoModelForSeq2SeqLM.from_pretrained(translation_model)
            
            logger.info("تم تحميل النماذج اللغوية بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل النماذج اللغوية: {e}")
    
    async def generate_text(self, prompt: str, model_type: str = "dialog", 
                          max_length: int = 512, temperature: float = 0.7) -> str:
        """توليد النص باستخدام النماذج اللغوية"""
        try:
            if model_type not in self.models:
                raise ValueError(f"نوع النموذج غير مدعوم: {model_type}")
            
            tokenizer = self.tokenizers[model_type]
            model = self.models[model_type]
            
            # ترميز النص
            inputs = tokenizer.encode(prompt, return_tensors="pt")
            
            # توليد النص
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # فك الترميز
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # إزالة النص الأصلي من النتيجة
            if prompt in generated_text:
                generated_text = generated_text.replace(prompt, "").strip()
            
            return generated_text
            
        except Exception as e:
            logger.error(f"خطأ في توليد النص: {e}")
            return f"عذراً، حدث خطأ في توليد النص: {str(e)}"
    
    async def summarize_text(self, text: str, max_length: int = 150) -> str:
        """تلخيص النص"""
        try:
            tokenizer = self.tokenizers['summary']
            model = self.models['summary']
            
            inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
            
            with torch.no_grad():
                summary_ids = model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=30,
                    do_sample=False
                )
            
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
            
        except Exception as e:
            logger.error(f"خطأ في تلخيص النص: {e}")
            return f"عذراً، حدث خطأ في التلخيص: {str(e)}"

class ImageGenerationManager:
    """مدير توليد الصور"""
    
    def __init__(self):
        self.pipelines = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_models()
    
    def load_models(self):
        """تحميل نماذج توليد الصور"""
        try:
            # نموذج Stable Diffusion
            model_id = "runwayml/stable-diffusion-v1-5"
            self.pipelines['stable_diffusion'] = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            self.pipelines['stable_diffusion'].to(self.device)
            
            # نموذج لتحليل الصور
            self.image_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.image_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            
            logger.info("تم تحميل نماذج توليد الصور بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل نماذج توليد الصور: {e}")
    
    async def generate_image(self, prompt: str, negative_prompt: str = "", 
                           num_inference_steps: int = 50, guidance_scale: float = 7.5,
                           width: int = 512, height: int = 512) -> bytes:
        """توليد صورة من النص"""
        try:
            if 'stable_diffusion' not in self.pipelines:
                raise ValueError("نموذج توليد الصور غير متاح")
            
            pipeline = self.pipelines['stable_diffusion']
            
            # توليد الصورة
            image = pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height
            ).images[0]
            
            # تحويل الصورة إلى bytes
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            return img_bytes
            
        except Exception as e:
            logger.error(f"خطأ في توليد الصورة: {e}")
            raise
    
    async def analyze_image(self, image_bytes: bytes) -> str:
        """تحليل الصورة وإنتاج وصف نصي"""
        try:
            # تحويل bytes إلى صورة
            image = Image.open(io.BytesIO(image_bytes))
            
            # معالجة الصورة
            inputs = self.image_processor(image, return_tensors="pt")
            
            # توليد الوصف
            out = self.image_model.generate(**inputs, max_length=50)
            caption = self.image_processor.decode(out[0], skip_special_tokens=True)
            
            return caption
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الصورة: {e}")
            return f"عذراً، حدث خطأ في تحليل الصورة: {str(e)}"
    
    async def enhance_image_for_training(self, image_bytes: bytes, 
                                       enhancement_type: str = "plant_disease") -> bytes:
        """تحسين الصورة لبيانات التدريب"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # تطبيق تحسينات مختلفة حسب النوع
            if enhancement_type == "plant_disease":
                # تحسينات خاصة بأمراض النباتات
                # زيادة التباين، تحسين الألوان، إزالة الضوضاء
                enhanced_image = self._enhance_plant_disease_image(image)
            else:
                enhanced_image = image
            
            # تحويل إلى bytes
            img_buffer = io.BytesIO()
            enhanced_image.save(img_buffer, format='PNG')
            return img_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"خطأ في تحسين الصورة: {e}")
            raise
    
    def _enhance_plant_disease_image(self, image: Image.Image) -> Image.Image:
        """تحسين صورة مرض النبات"""
        # تطبيق تحسينات أساسية
        # يمكن تطوير هذه الدالة لتشمل تحسينات أكثر تقدماً
        return image

class DiffusionModelManager:
    """مدير نماذج الانتشار المتقدمة"""
    
    def __init__(self):
        self.models = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_models()
    
    def load_models(self):
        """تحميل نماذج الانتشار"""
        try:
            # نموذج للتحليل المتقدم للصور
            self.models['analysis'] = pipeline(
                "image-classification",
                model="google/vit-base-patch16-224"
            )
            
            logger.info("تم تحميل نماذج الانتشار بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل نماذج الانتشار: {e}")
    
    async def advanced_image_analysis(self, image_bytes: bytes) -> Dict[str, Any]:
        """تحليل متقدم للصور باستخدام نماذج الانتشار"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # تحليل التصنيف
            classification_results = self.models['analysis'](image)
            
            # تحليل إضافي للخصائص
            analysis_results = {
                "classification": classification_results,
                "image_properties": {
                    "size": image.size,
                    "mode": image.mode,
                    "format": image.format
                },
                "confidence_scores": [result['score'] for result in classification_results],
                "top_prediction": classification_results[0] if classification_results else None
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"خطأ في التحليل المتقدم للصورة: {e}")
            return {"error": str(e)}

class GenerativeAIService:
    """الخدمة الرئيسية للذكاء الاصطناعي التوليدي"""
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.image_manager = ImageGenerationManager()
        self.diffusion_manager = DiffusionModelManager()
        self.request_queue = queue.PriorityQueue()
        self.response_cache = {}
        self.is_running = False
        self.worker_thread = None
    
    def start_service(self):
        """بدء الخدمة"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._process_requests)
            self.worker_thread.start()
            logger.info("تم بدء خدمة الذكاء الاصطناعي التوليدي")
    
    def stop_service(self):
        """إيقاف الخدمة"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join()
        logger.info("تم إيقاف خدمة الذكاء الاصطناعي التوليدي")
    
    def _process_requests(self):
        """معالجة الطلبات في الخلفية"""
        while self.is_running:
            try:
                # الحصول على طلب من القائمة
                priority, request = self.request_queue.get(timeout=1)
                
                # معالجة الطلب
                response = asyncio.run(self._handle_request(request))
                
                # حفظ الاستجابة في الذاكرة المؤقتة
                self.response_cache[request.request_id] = response
                
                self.request_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"خطأ في معالجة الطلب: {e}")
    
    async def _handle_request(self, request: GenerativeRequest) -> GenerativeResponse:
        """معالجة طلب واحد"""
        start_time = datetime.now()
        
        try:
            if request.request_type == "text":
                content = await self._handle_text_request(request)
                response_type = "text"
                model_used = "llm"
                
            elif request.request_type == "image":
                content = await self._handle_image_request(request)
                response_type = "image"
                model_used = "diffusion"
                
            elif request.request_type == "multimodal":
                content = await self._handle_multimodal_request(request)
                response_type = "multimodal"
                model_used = "multimodal"
                
            else:
                raise ValueError(f"نوع الطلب غير مدعوم: {request.request_type}")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return GenerativeResponse(
                request_id=request.request_id,
                response_type=response_type,
                content=content,
                metadata={"success": True},
                processing_time=processing_time,
                model_used=model_used,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"خطأ في معالجة الطلب {request.request_id}: {e}")
            
            return GenerativeResponse(
                request_id=request.request_id,
                response_type="error",
                content=str(e),
                metadata={"success": False, "error": str(e)},
                processing_time=processing_time,
                model_used="none",
                timestamp=datetime.now()
            )
    
    async def _handle_text_request(self, request: GenerativeRequest) -> str:
        """معالجة طلب نصي"""
        task_type = request.parameters.get("task_type", "generate")
        
        if task_type == "generate":
            return await self.llm_manager.generate_text(
                request.prompt,
                request.parameters.get("model_type", "dialog"),
                request.parameters.get("max_length", 512),
                request.parameters.get("temperature", 0.7)
            )
        elif task_type == "summarize":
            return await self.llm_manager.summarize_text(
                request.prompt,
                request.parameters.get("max_length", 150)
            )
        else:
            raise ValueError(f"نوع المهمة النصية غير مدعوم: {task_type}")
    
    async def _handle_image_request(self, request: GenerativeRequest) -> Union[bytes, Dict]:
        """معالجة طلب صورة"""
        task_type = request.parameters.get("task_type", "generate")
        
        if task_type == "generate":
            return await self.image_manager.generate_image(
                request.prompt,
                request.parameters.get("negative_prompt", ""),
                request.parameters.get("num_inference_steps", 50),
                request.parameters.get("guidance_scale", 7.5),
                request.parameters.get("width", 512),
                request.parameters.get("height", 512)
            )
        elif task_type == "analyze":
            image_data = request.parameters.get("image_data")
            if not image_data:
                raise ValueError("بيانات الصورة مطلوبة للتحليل")
            
            # تحويل base64 إلى bytes إذا لزم الأمر
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data)
            
            analysis = await self.diffusion_manager.advanced_image_analysis(image_data)
            caption = await self.image_manager.analyze_image(image_data)
            
            return {
                "analysis": analysis,
                "caption": caption
            }
        else:
            raise ValueError(f"نوع مهمة الصورة غير مدعوم: {task_type}")
    
    async def _handle_multimodal_request(self, request: GenerativeRequest) -> Dict:
        """معالجة طلب متعدد الوسائط"""
        # دمج النص والصورة في تحليل شامل
        text_response = await self._handle_text_request(request)
        
        if "image_data" in request.parameters:
            image_response = await self._handle_image_request(request)
            return {
                "text": text_response,
                "image_analysis": image_response
            }
        else:
            return {"text": text_response}
    
    def submit_request(self, request: GenerativeRequest) -> str:
        """إرسال طلب للمعالجة"""
        self.request_queue.put((request.priority, request))
        return request.request_id
    
    def get_response(self, request_id: str) -> Optional[GenerativeResponse]:
        """الحصول على استجابة طلب"""
        return self.response_cache.get(request_id)
    
    def get_service_status(self) -> Dict[str, Any]:
        """الحصول على حالة الخدمة"""
        return {
            "is_running": self.is_running,
            "queue_size": self.request_queue.qsize(),
            "cache_size": len(self.response_cache),
            "device": str(self.llm_manager.device),
            "models_loaded": {
                "llm": len(self.llm_manager.models),
                "image": len(self.image_manager.pipelines),
                "diffusion": len(self.diffusion_manager.models)
            }
        }

# إنشاء مثيل عام للخدمة
generative_ai_service = GenerativeAIService()

# دوال مساعدة للاستخدام السهل
async def generate_text(prompt: str, **kwargs) -> str:
    """دالة مساعدة لتوليد النص"""
    request = GenerativeRequest(
        request_id=f"text_{datetime.now().timestamp()}",
        request_type="text",
        prompt=prompt,
        parameters=kwargs,
        user_id=kwargs.get("user_id", "system"),
        timestamp=datetime.now()
    )
    
    request_id = generative_ai_service.submit_request(request)
    
    # انتظار النتيجة
    while True:
        response = generative_ai_service.get_response(request_id)
        if response:
            return response.content
        await asyncio.sleep(0.1)

async def generate_image(prompt: str, **kwargs) -> bytes:
    """دالة مساعدة لتوليد الصور"""
    request = GenerativeRequest(
        request_id=f"image_{datetime.now().timestamp()}",
        request_type="image",
        prompt=prompt,
        parameters={**kwargs, "task_type": "generate"},
        user_id=kwargs.get("user_id", "system"),
        timestamp=datetime.now()
    )
    
    request_id = generative_ai_service.submit_request(request)
    
    # انتظار النتيجة
    while True:
        response = generative_ai_service.get_response(request_id)
        if response:
            return response.content
        await asyncio.sleep(0.1)

async def analyze_image(image_data: bytes, **kwargs) -> Dict:
    """دالة مساعدة لتحليل الصور"""
    request = GenerativeRequest(
        request_id=f"analyze_{datetime.now().timestamp()}",
        request_type="image",
        prompt="تحليل الصورة",
        parameters={**kwargs, "task_type": "analyze", "image_data": image_data},
        user_id=kwargs.get("user_id", "system"),
        timestamp=datetime.now()
    )
    
    request_id = generative_ai_service.submit_request(request)
    
    # انتظار النتيجة
    while True:
        response = generative_ai_service.get_response(request_id)
        if response:
            return response.content
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    # اختبار الخدمة
    async def test_service():
        generative_ai_service.start_service()
        
        # اختبار توليد النص
        text_result = await generate_text("ما هي أفضل طرق العناية بالنباتات؟")
        print(f"نتيجة النص: {text_result}")
        
        # اختبار حالة الخدمة
        status = generative_ai_service.get_service_status()
        print(f"حالة الخدمة: {status}")
        
        generative_ai_service.stop_service()
    
    # تشغيل الاختبار
    asyncio.run(test_service())

