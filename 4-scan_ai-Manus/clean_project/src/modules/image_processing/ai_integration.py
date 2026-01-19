# File: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/image_processing/ai_integration.py
"""
وحدة تكامل الذكاء الاصطناعي مع معالجة الصور

هذه الوحدة مسؤولة عن ربط وحدة معالجة الصور بخدمات الذكاء الاصطناعي،
مما يسمح باستخدام نماذج الذكاء الاصطناعي لتحليل ومعالجة الصور.
"""

import logging
from typing import Dict, List, Optional, Any
import os
import base64

# استيراد وحدات النظام
from src.modules.ai_management.service import AIModelService
from src.modules.ai_management.models import ModelType
from src.modules.ai_management.schemas import ModelRequest

# إعداد السجل
logger = logging.getLogger(__name__)


class ImageAIIntegration:
    """
    فئة تكامل الذكاء الاصطناعي مع معالجة الصور

    توفر هذه الفئة واجهة موحدة لوحدة معالجة الصور للتفاعل مع خدمات الذكاء الاصطناعي،
    بما في ذلك تحليل الصور وتصنيفها واكتشاف الكائنات فيها.
    """

    def __init__(self, ai_model_service: Optional[AIModelService] = None):
        """
        تهيئة فئة تكامل الذكاء الاصطناعي

        Args:
            ai_model_service: خدمة نماذج الذكاء الاصطناعي، إذا لم يتم توفيرها سيتم إنشاء مثيل جديد
        """
        self.ai_model_service = ai_model_service or AIModelService()
        logger.info("تم تهيئة تكامل الذكاء الاصطناعي مع معالجة الصور")
        self.available_models = self._get_available_models()

    def _get_available_models(self) -> Dict[str, Any]:
        """الحصول على النماذج المتاحة"""
        return {
            "classification": ["resnet50", "vgg16", "inception_v3"],
            "detection": ["yolo_v5", "faster_rcnn", "ssd"],
            "segmentation": ["unet", "mask_rcnn", "deeplab"],
            "enhancement": ["super_resolution", "denoising", "colorization"],
            "analysis": ["face_detection", "object_recognition", "scene_understanding"],
            "description": ["image_captioning", "visual_qa", "image_understanding"]
        }

    async def get_available_image_models(self, model_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        الحصول على قائمة بنماذج الذكاء الاصطناعي المتاحة لمعالجة الصور

        Args:
            model_type: نوع النموذج (اختياري، مثل "classification", "detection", "segmentation")

        Returns:
            قائمة بالنماذج المتاحة مع بياناتها الوصفية
        """
        try:
            # تحديد أنواع النماذج المطلوبة
            model_types = []
            if model_type:
                if model_type == "classification":
                    model_types = [ModelType.IMAGE_CLASSIFICATION]
                elif model_type == "detection":
                    model_types = [ModelType.OBJECT_DETECTION]
                elif model_type == "segmentation":
                    model_types = [ModelType.IMAGE_SEGMENTATION]
                elif model_type == "all":
                    model_types = [
                        ModelType.IMAGE_CLASSIFICATION,
                        ModelType.OBJECT_DETECTION,
                        ModelType.IMAGE_SEGMENTATION
                    ]
            else:
                # افتراضياً، استرجاع جميع أنواع نماذج الصور
                model_types = [
                    ModelType.IMAGE_CLASSIFICATION,
                    ModelType.OBJECT_DETECTION,
                    ModelType.IMAGE_SEGMENTATION
                ]

            # استرجاع النماذج المتاحة
            models = await self.ai_model_service.get_available_models(model_types=model_types)

            # تحويل النماذج إلى قائمة من القواميس
            result = []
            for model in models:
                result.append({
                    "id": model.id,
                    "name": model.name,
                    "type": model.type.value,
                    "description": model.description,
                    "version": model.version,
                    "capabilities": model.capabilities,
                    "metadata": model.metadata
                })

            logger.info(f"تم استرجاع {len(result)} نموذج متاح لمعالجة الصور")
            return result
        except Exception as e:
            logger.error(f"فشل في استرجاع نماذج معالجة الصور المتاحة: {str(e)}")
            raise

    async def classify_image(
        self,
        image_path: str,
        model_id: Optional[str] = None,
        confidence_threshold: float = 0.5,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        تصنيف صورة باستخدام نموذج الذكاء الاصطناعي

        Args:
            image_path: مسار الصورة المراد تصنيفها
            model_id: معرف النموذج المراد استخدامه (اختياري، سيتم استخدام النموذج الافتراضي إذا لم يتم توفيره)
            confidence_threshold: عتبة الثقة الدنيا للنتائج
            max_results: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بالتصنيفات المكتشفة مع درجات الثقة
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"الصورة غير موجودة في المسار: {image_path}")

            # تحميل الصورة وتحويلها إلى Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # إعداد طلب النموذج
            request_data = {
                "image": image_data,
                "confidence_threshold": confidence_threshold,
                "max_results": max_results
            }

            # إذا لم يتم توفير معرف النموذج، استخدم النموذج الافتراضي
            if not model_id:
                # استرجاع النماذج المتاحة للتصنيف
                available_models = await self.get_available_image_models("classification")
                if not available_models:
                    raise ValueError("لا توجد نماذج تصنيف متاحة")

                # استخدام أول نموذج متاح
                model_id = available_models[0]["id"]
                logger.info(f"استخدام النموذج الافتراضي للتصنيف: {model_id}")

            # إنشاء طلب النموذج
            model_request = ModelRequest(
                model_id=model_id,
                data=request_data
            )

            # استدعاء النموذج
            response = await self.ai_model_service.invoke_model(model_request)

            # معالجة الاستجابة
            if response.status == "success" and response.result:
                classifications = response.result.get("classifications", [])
                logger.info(f"تم تصنيف الصورة بنجاح، تم العثور على {len(classifications)} تصنيف")
                return classifications
            else:
                logger.warning(f"فشل في تصنيف الصورة: {response.error}")
                return []
        except Exception as e:
            logger.error(f"فشل في تصنيف الصورة: {str(e)}")
            raise

    async def detect_objects(
        self,
        image_path: str,
        model_id: Optional[str] = None,
        confidence_threshold: float = 0.5,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        اكتشاف الكائنات في صورة باستخدام نموذج الذكاء الاصطناعي

        Args:
            image_path: مسار الصورة المراد تحليلها
            model_id: معرف النموذج المراد استخدامه (اختياري، سيتم استخدام النموذج الافتراضي إذا لم يتم توفيره)
            confidence_threshold: عتبة الثقة الدنيا للنتائج
            max_results: الحد الأقصى لعدد النتائج

        Returns:
            قائمة بالكائنات المكتشفة مع مواقعها ودرجات الثقة
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"الصورة غير موجودة في المسار: {image_path}")

            # تحميل الصورة وتحويلها إلى Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # إعداد طلب النموذج
            request_data = {
                "image": image_data,
                "confidence_threshold": confidence_threshold,
                "max_results": max_results
            }

            # إذا لم يتم توفير معرف النموذج، استخدم النموذج الافتراضي
            if not model_id:
                # استرجاع النماذج المتاحة لاكتشاف الكائنات
                available_models = await self.get_available_image_models("detection")
                if not available_models:
                    raise ValueError("لا توجد نماذج اكتشاف كائنات متاحة")

                # استخدام أول نموذج متاح
                model_id = available_models[0]["id"]
                logger.info(f"استخدام النموذج الافتراضي لاكتشاف الكائنات: {model_id}")

            # إنشاء طلب النموذج
            model_request = ModelRequest(
                model_id=model_id,
                data=request_data
            )

            # استدعاء النموذج
            response = await self.ai_model_service.invoke_model(model_request)

            # معالجة الاستجابة
            if response.status == "success" and response.result:
                objects = response.result.get("objects", [])
                logger.info(f"تم اكتشاف الكائنات في الصورة بنجاح، تم العثور على {len(objects)} كائن")
                return objects
            else:
                logger.warning(f"فشل في اكتشاف الكائنات في الصورة: {response.error}")
                return []
        except Exception as e:
            logger.error(f"فشل في اكتشاف الكائنات في الصورة: {str(e)}")
            raise

    async def segment_image(
        self,
        image_path: str,
        model_id: Optional[str] = None,
        confidence_threshold: float = 0.5,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        تقسيم الصورة إلى مناطق دلالية باستخدام نموذج الذكاء الاصطناعي

        Args:
            image_path: مسار الصورة المراد تقسيمها
            model_id: معرف النموذج المراد استخدامه (اختياري، سيتم استخدام النموذج الافتراضي إذا لم يتم توفيره)
            confidence_threshold: عتبة الثقة الدنيا للنتائج
            output_path: مسار حفظ صورة التقسيم (اختياري)

        Returns:
            معلومات التقسيم مع مسار صورة التقسيم إذا تم توفير output_path
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"الصورة غير موجودة في المسار: {image_path}")

            # تحميل الصورة وتحويلها إلى Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # إعداد طلب النموذج
            request_data = {
                "image": image_data,
                "confidence_threshold": confidence_threshold,
                "return_visualization": output_path is not None
            }

            # إذا لم يتم توفير معرف النموذج، استخدم النموذج الافتراضي
            if not model_id:
                # استرجاع النماذج المتاحة للتقسيم
                available_models = await self.get_available_image_models("segmentation")
                if not available_models:
                    raise ValueError("لا توجد نماذج تقسيم صور متاحة")

                # استخدام أول نموذج متاح
                model_id = available_models[0]["id"]
                logger.info(f"استخدام النموذج الافتراضي لتقسيم الصور: {model_id}")

            # إنشاء طلب النموذج
            model_request = ModelRequest(
                model_id=model_id,
                data=request_data
            )

            # استدعاء النموذج
            response = await self.ai_model_service.invoke_model(model_request)

            # معالجة الاستجابة
            if response.status == "success" and response.result:
                result = response.result

                # إذا تم طلب التصور وتم توفير مسار الإخراج
                if output_path and "visualization" in result:
                    # فك ترميز صورة التصور من Base64
                    visualization_data = base64.b64decode(result["visualization"])

                    # حفظ صورة التصور
                    with open(output_path, "wb") as output_file:
                        output_file.write(visualization_data)

                    # إضافة مسار الإخراج إلى النتيجة
                    result["visualization_path"] = output_path

                    # حذف بيانات التصور الكبيرة من النتيجة
                    del result["visualization"]

                logger.info(f"تم تقسيم الصورة بنجاح، تم العثور على {len(result.get('segments', []))} منطقة")
                return result
            else:
                logger.warning(f"فشل في تقسيم الصورة: {response.error}")
                return {"error": response.error, "segments": []}
        except Exception as e:
            logger.error(f"فشل في تقسيم الصورة: {str(e)}")
            raise

    async def enhance_image(
        self,
        image_path: str,
        enhancement_type: str,
        model_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        تحسين الصورة باستخدام نموذج الذكاء الاصطناعي

        Args:
            image_path: مسار الصورة المراد تحسينها
            enhancement_type: نوع التحسين (مثل "super_resolution", "denoising", "colorization")
            model_id: معرف النموذج المراد استخدامه (اختياري، سيتم استخدام النموذج الافتراضي إذا لم يتم توفيره)
            parameters: معلمات إضافية للتحسين (اختياري)
            output_path: مسار حفظ الصورة المحسنة (اختياري، سيتم إنشاء مسار تلقائي إذا لم يتم توفيره)

        Returns:
            مسار الصورة المحسنة
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"الصورة غير موجودة في المسار: {image_path}")

            # إنشاء مسار الإخراج إذا لم يتم توفيره
            if not output_path:
                # استخراج اسم الملف وامتداده
                image_filename = os.path.basename(image_path)
                image_name, image_ext = os.path.splitext(image_filename)

                # إنشاء مسار الإخراج في مجلد النتائج
                output_dir = os.path.join(os.path.dirname(os.path.dirname(image_path)), "results")
                os.makedirs(output_dir, exist_ok=True)

                # إنشاء اسم ملف الإخراج
                output_filename = f"{image_name}_{enhancement_type}{image_ext}"
                output_path = os.path.join(output_dir, output_filename)

            # تحميل الصورة وتحويلها إلى Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # إعداد طلب النموذج
            request_data = {
                "image": image_data,
                "enhancement_type": enhancement_type
            }

            # إضافة المعلمات إذا تم توفيرها
            if parameters:
                request_data["parameters"] = parameters

            # إذا لم يتم توفير معرف النموذج، استخدم النموذج الافتراضي
            if not model_id:
                # استرجاع النماذج المتاحة لتحسين الصور
                available_models = await self.get_available_image_models("enhancement")
                if not available_models:
                    raise ValueError("لا توجد نماذج تحسين صور متاحة")

                # استخدام أول نموذج متاح
                model_id = available_models[0]["id"]
                logger.info(f"استخدام النموذج الافتراضي لتحسين الصور: {model_id}")

            # إنشاء طلب النموذج
            model_request = ModelRequest(
                model_id=model_id,
                data=request_data
            )

            # استدعاء النموذج
            response = await self.ai_model_service.invoke_model(model_request)

            # معالجة الاستجابة
            if response.status == "success" and response.result:
                # فك ترميز الصورة المحسنة من Base64
                enhanced_image_data = base64.b64decode(response.result["enhanced_image"])

                # حفظ الصورة المحسنة
                with open(output_path, "wb") as output_file:
                    output_file.write(enhanced_image_data)

                logger.info(f"تم تحسين الصورة بنجاح، تم حفظ النتيجة في: {output_path}")
                return output_path
            else:
                logger.warning(f"فشل في تحسين الصورة: {response.error}")
                raise ValueError(f"فشل في تحسين الصورة: {response.error}")
        except Exception as e:
            logger.error(f"فشل في تحسين الصورة: {str(e)}")
            raise

    async def analyze_image(
        self,
        image_path: str,
        analysis_types: List[str],
        model_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        تحليل شامل للصورة باستخدام نموذج الذكاء الاصطناعي

        Args:
            image_path: مسار الصورة المراد تحليلها
            analysis_types: أنواع التحليل المطلوبة (مثل ["classification", "objects", "text", "faces", "colors"])
            model_id: معرف النموذج المراد استخدامه (اختياري، سيتم استخدام النموذج الافتراضي إذا لم يتم توفيره)

        Returns:
            نتائج التحليل الشامل
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"الصورة غير موجودة في المسار: {image_path}")

            # تحميل الصورة وتحويلها إلى Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # إعداد طلب النموذج
            request_data = {
                "image": image_data,
                "analysis_types": analysis_types
            }

            # إذا لم يتم توفير معرف النموذج، استخدم النموذج الافتراضي
            if not model_id:
                # استرجاع النماذج المتاحة للتحليل الشامل
                available_models = await self.get_available_image_models("analysis")
                if not available_models:
                    raise ValueError("لا توجد نماذج تحليل صور متاحة")

                # استخدام أول نموذج متاح
                model_id = available_models[0]["id"]
                logger.info(f"استخدام النموذج الافتراضي لتحليل الصور: {model_id}")

            # إنشاء طلب النموذج
            model_request = ModelRequest(
                model_id=model_id,
                data=request_data
            )

            # استدعاء النموذج
            response = await self.ai_model_service.invoke_model(model_request)

            # معالجة الاستجابة
            if response.status == "success" and response.result:
                logger.info(f"تم تحليل الصورة بنجاح، تم إجراء {len(analysis_types)} نوع من التحليل")
                return response.result
            else:
                logger.warning(f"فشل في تحليل الصورة: {response.error}")
                return {"error": response.error}
        except Exception as e:
            logger.error(f"فشل في تحليل الصورة: {str(e)}")
            raise

    async def generate_image_description(
        self,
        image_path: str,
        language: str = "ar",
        detail_level: str = "medium",
        model_id: Optional[str] = None
    ) -> str:
        """
        توليد وصف للصورة باستخدام نموذج الذكاء الاصطناعي

        Args:
            image_path: مسار الصورة المراد وصفها
            language: لغة الوصف (افتراضياً "ar" للعربية)
            detail_level: مستوى التفاصيل ("low", "medium", "high")
            model_id: معرف النموذج المراد استخدامه (اختياري، سيتم استخدام النموذج الافتراضي إذا لم يتم توفيره)

        Returns:
            وصف الصورة
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"الصورة غير موجودة في المسار: {image_path}")

            # تحميل الصورة وتحويلها إلى Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            # إعداد طلب النموذج
            request_data = {
                "image": image_data,
                "language": language,
                "detail_level": detail_level
            }

            # إذا لم يتم توفير معرف النموذج، استخدم النموذج الافتراضي
            if not model_id:
                # استرجاع النماذج المتاحة لوصف الصور
                available_models = await self.get_available_image_models("description")
                if not available_models:
                    raise ValueError("لا توجد نماذج وصف صور متاحة")

                # استخدام أول نموذج متاح
                model_id = available_models[0]["id"]
                logger.info(f"استخدام النموذج الافتراضي لوصف الصور: {model_id}")

            # إنشاء طلب النموذج
            model_request = ModelRequest(
                model_id=model_id,
                data=request_data
            )

            # استدعاء النموذج
            response = await self.ai_model_service.invoke_model(model_request)

            # معالجة الاستجابة
            if response.status == "success" and response.result:
                description = response.result.get("description", "")
                logger.info("تم توليد وصف للصورة بنجاح")
                return description
            else:
                logger.warning(f"فشل في توليد وصف للصورة: {response.error}")
                return ""
        except Exception as e:
            logger.error(f"فشل في توليد وصف للصورة: {str(e)}")
            raise

