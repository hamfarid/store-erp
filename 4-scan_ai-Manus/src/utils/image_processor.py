#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة معالجة الصور
================

توفر هذه الوحدة وظائف متقدمة لمعالجة الصور وتحليلها لاستخدامها في مكونات النظام المختلفة.
تتضمن وظائف لتحسين الصور، واستخراج الميزات، وتقسيم الصور، وتحليل الألوان.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import logging
from typing import Tuple, List, Dict, Union, Optional, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy import ndimage

# إعداد السجل
logger = logging.getLogger('agricultural_ai.image_processor')

@dataclass
class ImageRegion:
    """فئة تمثل منطقة في الصورة مع خصائصها"""
    x: int
    y: int
    width: int
    height: int
    label: str = ""
    confidence: float = 0.0
    features: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = {}
    
    @property
    def area(self) -> int:
        """حساب مساحة المنطقة"""
        return self.width * self.height
    
    @property
    def center(self) -> Tuple[int, int]:
        """حساب مركز المنطقة"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """إرجاع الإحداثيات كمستطيل محيط"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)

class ImageProcessor:
    """فئة لمعالجة الصور وتحليلها"""
    
    def __init__(self, config: Dict = None):
        """تهيئة معالج الصور
        
        المعاملات:
            config (Dict): تكوين معالج الصور
        """
        self.config = config or {}
        self.default_image_size = self.config.get('default_image_size', (224, 224))
        logger.info("تم تهيئة معالج الصور")
    
    def load_image(self, image_path: str) -> np.ndarray:
        """تحميل صورة من المسار
        
        المعاملات:
            image_path (str): مسار الصورة
            
        الإرجاع:
            np.ndarray: مصفوفة الصورة
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"الصورة غير موجودة: {image_path}")
        
        try:
            # محاولة القراءة باستخدام OpenCV
            image = cv2.imread(image_path)
            if image is None:
                # إذا فشلت القراءة باستخدام OpenCV، جرب PIL
                pil_image = Image.open(image_path)
                image = np.array(pil_image)
                # تحويل من RGB إلى BGR إذا كانت الصورة ملونة
                if len(image.shape) == 3 and image.shape[2] == 3:
                    image = image[:, :, ::-1]
            
            logger.debug(f"تم تحميل الصورة: {image_path}, الشكل: {image.shape}")
            return image
        except Exception as e:
            logger.error(f"فشل في تحميل الصورة {image_path}: {str(e)}")
            raise
    
    def save_image(self, image: np.ndarray, output_path: str) -> bool:
        """حفظ الصورة إلى المسار
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            output_path (str): مسار الحفظ
            
        الإرجاع:
            bool: نجاح العملية
        """
        try:
            directory = os.path.dirname(output_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            cv2.imwrite(output_path, image)
            logger.debug(f"تم حفظ الصورة في: {output_path}")
            return True
        except Exception as e:
            logger.error(f"فشل في حفظ الصورة {output_path}: {str(e)}")
            return False
    
    def resize_image(self, image: np.ndarray, size: Tuple[int, int] = None) -> np.ndarray:
        """تغيير حجم الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            size (Tuple[int, int], optional): الحجم الجديد (العرض، الارتفاع)
            
        الإرجاع:
            np.ndarray: الصورة بعد تغيير الحجم
        """
        if size is None:
            size = self.default_image_size
        
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    
    def enhance_image(self, image: np.ndarray, 
                     contrast: float = 1.0, 
                     brightness: float = 1.0, 
                     sharpness: float = 1.0) -> np.ndarray:
        """تحسين الصورة (التباين، السطوع، الحدة)
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            contrast (float): عامل التباين
            brightness (float): عامل السطوع
            sharpness (float): عامل الحدة
            
        الإرجاع:
            np.ndarray: الصورة المحسنة
        """
        # تحويل من OpenCV (BGR) إلى PIL (RGB)
        if len(image.shape) == 3 and image.shape[2] == 3:
            pil_image = Image.fromarray(image[:, :, ::-1])
        else:
            pil_image = Image.fromarray(image)
        
        # تطبيق التحسينات
        if contrast != 1.0:
            pil_image = ImageEnhance.Contrast(pil_image).enhance(contrast)
        
        if brightness != 1.0:
            pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness)
        
        if sharpness != 1.0:
            pil_image = ImageEnhance.Sharpness(pil_image).enhance(sharpness)
        
        # تحويل مرة أخرى إلى مصفوفة NumPy
        enhanced_image = np.array(pil_image)
        
        # تحويل مرة أخرى إلى BGR إذا كانت الصورة ملونة
        if len(enhanced_image.shape) == 3 and enhanced_image.shape[2] == 3:
            enhanced_image = enhanced_image[:, :, ::-1]
        
        return enhanced_image
    
    def remove_noise(self, image: np.ndarray, method: str = 'gaussian', kernel_size: int = 5) -> np.ndarray:
        """إزالة الضوضاء من الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            method (str): طريقة إزالة الضوضاء ('gaussian', 'median', 'bilateral')
            kernel_size (int): حجم النواة للترشيح
            
        الإرجاع:
            np.ndarray: الصورة بعد إزالة الضوضاء
        """
        if method == 'gaussian':
            return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        elif method == 'median':
            return cv2.medianBlur(image, kernel_size)
        elif method == 'bilateral':
            return cv2.bilateralFilter(image, kernel_size, 75, 75)
        else:
            logger.warning(f"طريقة إزالة الضوضاء غير معروفة: {method}، استخدام الطريقة الافتراضية")
            return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def segment_image(self, image: np.ndarray, method: str = 'kmeans', n_segments: int = 5) -> Tuple[np.ndarray, List[np.ndarray]]:
        """تقسيم الصورة إلى مناطق
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            method (str): طريقة التقسيم ('kmeans', 'watershed', 'grabcut')
            n_segments (int): عدد المناطق المطلوبة (للطرق التي تدعم ذلك)
            
        الإرجاع:
            Tuple[np.ndarray, List[np.ndarray]]: صورة التقسيم وقائمة بالمناطق المقسمة
        """
        if method == 'kmeans':
            # تحويل الصورة إلى مصفوفة ثنائية الأبعاد للتقسيم
            h, w = image.shape[:2]
            reshaped_image = image.reshape((h * w, -1))
            
            # تطبيق خوارزمية K-means
            kmeans = KMeans(n_clusters=n_segments, random_state=42, n_init=10)
            labels = kmeans.fit_predict(reshaped_image)
            
            # إعادة تشكيل التسميات إلى شكل الصورة
            segmented = labels.reshape(h, w)
            
            # إنشاء قائمة بالمناطق المقسمة
            segments = []
            for i in range(n_segments):
                mask = np.zeros((h, w), dtype=np.uint8)
                mask[segmented == i] = 255
                segments.append(mask)
            
            # تحويل التسميات إلى صورة ملونة للعرض
            segmented_image = np.zeros((h, w, 3), dtype=np.uint8)
            colors = [
                (255, 0, 0), (0, 255, 0), (0, 0, 255),
                (255, 255, 0), (255, 0, 255), (0, 255, 255),
                (128, 0, 0), (0, 128, 0), (0, 0, 128),
                (128, 128, 0), (128, 0, 128), (0, 128, 128)
            ]
            
            for i in range(n_segments):
                color_idx = i % len(colors)
                segmented_image[segmented == i] = colors[color_idx]
            
            return segmented_image, segments
            
        elif method == 'watershed':
            # تحويل إلى صورة رمادية إذا كانت ملونة
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # تطبيق عتبة Otsu للحصول على الخلفية والأمامية
            ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # إزالة الضوضاء
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            
            # تحديد المنطقة الخلفية المؤكدة
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            
            # تحديد المنطقة الأمامية المؤكدة
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
            
            # تحديد المنطقة غير المؤكدة
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg, sure_fg)
            
            # وضع علامات للمكونات المتصلة
            ret, markers = cv2.connectedComponents(sure_fg)
            
            # إضافة 1 لجميع التسميات حتى تكون الخلفية 1 بدلاً من 0
            markers = markers + 1
            
            # وضع علامة 0 للمنطقة غير المؤكدة
            markers[unknown == 255] = 0
            
            # تطبيق خوارزمية Watershed
            if len(image.shape) == 3:
                markers = cv2.watershed(image, markers)
            else:
                # تحويل الصورة الرمادية إلى ملونة للتقسيم
                colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                markers = cv2.watershed(colored, markers)
            
            # إنشاء صورة التقسيم
            h, w = markers.shape
            segmented_image = np.zeros((h, w, 3), dtype=np.uint8)
            colors = [
                (255, 0, 0), (0, 255, 0), (0, 0, 255),
                (255, 255, 0), (255, 0, 255), (0, 255, 255),
                (128, 0, 0), (0, 128, 0), (0, 0, 128),
                (128, 128, 0), (128, 0, 128), (0, 128, 128)
            ]
            
            # إنشاء قائمة بالمناطق المقسمة
            segments = []
            for i in range(2, ret + 2):  # بدءًا من 2 لتجاوز الخلفية والحدود
                mask = np.zeros((h, w), dtype=np.uint8)
                mask[markers == i] = 255
                segments.append(mask)
                
                color_idx = (i - 2) % len(colors)
                segmented_image[markers == i] = colors[color_idx]
            
            # وضع علامة على الحدود باللون الأبيض
            segmented_image[markers == -1] = (255, 255, 255)
            
            return segmented_image, segments
            
        elif method == 'grabcut':
            # تطبيق خوارزمية GrabCut
            if len(image.shape) != 3:
                # تحويل الصورة الرمادية إلى ملونة
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            
            # إنشاء مستطيل أولي (يفترض أن الكائن في وسط الصورة)
            h, w = image.shape[:2]
            rect = (w//4, h//4, w//2, h//2)
            
            # إنشاء قناع أولي وخلفية ومقدمة للنموذج
            mask = np.zeros(image.shape[:2], np.uint8)
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            
            # تطبيق GrabCut
            cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
            
            # تعديل القناع
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            
            # إنشاء صورة التقسيم
            segmented_image = image * mask2[:, :, np.newaxis]
            
            # إنشاء قائمة بالمناطق المقسمة (في هذه الحالة منطقة واحدة فقط)
            segments = [mask2 * 255]
            
            return segmented_image, segments
        
        else:
            logger.warning(f"طريقة التقسيم غير معروفة: {method}، استخدام الطريقة الافتراضية")
            return self.segment_image(image, method='kmeans', n_segments=n_segments)
    
    def detect_edges(self, image: np.ndarray, method: str = 'canny', 
                    threshold1: int = 100, threshold2: int = 200) -> np.ndarray:
        """اكتشاف الحواف في الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            method (str): طريقة اكتشاف الحواف ('canny', 'sobel', 'laplacian')
            threshold1 (int): العتبة الأولى (للطرق التي تدعم ذلك)
            threshold2 (int): العتبة الثانية (للطرق التي تدعم ذلك)
            
        الإرجاع:
            np.ndarray: صورة الحواف
        """
        # تحويل إلى صورة رمادية إذا كانت ملونة
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        if method == 'canny':
            return cv2.Canny(gray, threshold1, threshold2)
        
        elif method == 'sobel':
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
            
            # حساب القيمة المطلقة وتحويلها إلى نوع uint8
            abs_sobelx = cv2.convertScaleAbs(sobelx)
            abs_sobely = cv2.convertScaleAbs(sobely)
            
            # دمج النتائج
            return cv2.addWeighted(abs_sobelx, 0.5, abs_sobely, 0.5, 0)
        
        elif method == 'laplacian':
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            return cv2.convertScaleAbs(laplacian)
        
        else:
            logger.warning(f"طريقة اكتشاف الحواف غير معروفة: {method}، استخدام الطريقة الافتراضية")
            return cv2.Canny(gray, threshold1, threshold2)
    
    def analyze_color(self, image: np.ndarray, n_colors: int = 5) -> Dict[str, Any]:
        """تحليل الألوان في الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            n_colors (int): عدد الألوان الرئيسية المراد استخراجها
            
        الإرجاع:
            Dict[str, Any]: نتائج تحليل الألوان
        """
        # التأكد من أن الصورة ملونة
        if len(image.shape) != 3 or image.shape[2] != 3:
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            else:
                logger.error("الصورة ليست ملونة ولا يمكن تحليل الألوان")
                return {"error": "الصورة ليست ملونة"}
        
        # تحويل من BGR إلى RGB للتحليل
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # تغيير شكل الصورة لتطبيق K-means
        pixels = image_rgb.reshape(-1, 3)
        
        # تطبيق K-means لاستخراج الألوان الرئيسية
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # الحصول على الألوان المركزية
        colors = kmeans.cluster_centers_.astype(int)
        
        # حساب نسب الألوان
        labels = kmeans.labels_
        counts = np.bincount(labels)
        percentages = (counts / len(labels)) * 100
        
        # تحويل الألوان إلى تنسيق HEX
        hex_colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in colors]
        
        # إنشاء قاموس النتائج
        color_analysis = {
            "dominant_colors": [],
            "color_distribution": {
                "red": float(np.mean(image_rgb[:, :, 0])),
                "green": float(np.mean(image_rgb[:, :, 1])),
                "blue": float(np.mean(image_rgb[:, :, 2]))
            },
            "average_color": {
                "rgb": [int(np.mean(image_rgb[:, :, 0])), 
                        int(np.mean(image_rgb[:, :, 1])), 
                        int(np.mean(image_rgb[:, :, 2]))],
                "hex": '#%02x%02x%02x' % (
                    int(np.mean(image_rgb[:, :, 0])),
                    int(np.mean(image_rgb[:, :, 1])),
                    int(np.mean(image_rgb[:, :, 2]))
                )
            }
        }
        
        # إضافة الألوان المهيمنة
        for i in range(n_colors):
            color_analysis["dominant_colors"].append({
                "rgb": colors[i].tolist(),
                "hex": hex_colors[i],
                "percentage": float(percentages[i])
            })
        
        # ترتيب الألوان حسب النسبة المئوية
        color_analysis["dominant_colors"] = sorted(
            color_analysis["dominant_colors"],
            key=lambda x: x["percentage"],
            reverse=True
        )
        
        return color_analysis
    
    def extract_features(self, image: np.ndarray) -> Dict[str, Any]:
        """استخراج ميزات من الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            
        الإرجاع:
            Dict[str, Any]: الميزات المستخرجة
        """
        # تحويل إلى صورة رمادية إذا كانت ملونة
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # حساب الهيستوجرام
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist.flatten() / hist.sum()  # تطبيع
        
        # حساب لحظات Hu
        moments = cv2.moments(gray)
        hu_moments = cv2.HuMoments(moments).flatten()
        
        # حساب GLCM (Gray-Level Co-occurrence Matrix) للنسيج
        def extract_glcm_features(gray_img):
            from skimage.feature import graycomatrix, graycoprops
            
            # تقليل مستويات الرمادي لتسريع الحساب
            bins = 16
            gray_img = (gray_img / (256 / bins)).astype(np.uint8)
            
            # حساب GLCM
            distances = [1, 3, 5]
            angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
            glcm = graycomatrix(gray_img, distances=distances, angles=angles, 
                               levels=bins, symmetric=True, normed=True)
            
            # استخراج الخصائص
            contrast = graycoprops(glcm, 'contrast').mean()
            dissimilarity = graycoprops(glcm, 'dissimilarity').mean()
            homogeneity = graycoprops(glcm, 'homogeneity').mean()
            energy = graycoprops(glcm, 'energy').mean()
            correlation = graycoprops(glcm, 'correlation').mean()
            
            return {
                'contrast': float(contrast),
                'dissimilarity': float(dissimilarity),
                'homogeneity': float(homogeneity),
                'energy': float(energy),
                'correlation': float(correlation)
            }
        
        # استخراج ميزات النسيج
        try:
            texture_features = extract_glcm_features(gray)
        except ImportError:
            logger.warning("لم يتم العثور على مكتبة scikit-image، تخطي استخراج ميزات النسيج")
            texture_features = {}
        
        # تجميع جميع الميزات
        features = {
            "basic_stats": {
                "mean": float(gray.mean()),
                "std": float(gray.std()),
                "min": float(gray.min()),
                "max": float(gray.max()),
                "median": float(np.median(gray))
            },
            "histogram": hist.tolist(),
            "hu_moments": hu_moments.tolist(),
            "texture": texture_features
        }
        
        # إضافة تحليل الألوان إذا كانت الصورة ملونة
        if len(image.shape) == 3:
            features["color"] = self.analyze_color(image, n_colors=3)
        
        return features
    
    def detect_regions_of_interest(self, image: np.ndarray, 
                                  method: str = 'contour', 
                                  min_area: int = 100) -> List[ImageRegion]:
        """اكتشاف مناطق الاهتمام في الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            method (str): طريقة الاكتشاف ('contour', 'blob', 'mser')
            min_area (int): الحد الأدنى لمساحة المنطقة
            
        الإرجاع:
            List[ImageRegion]: قائمة بمناطق الاهتمام
        """
        regions = []
        
        # تحويل إلى صورة رمادية إذا كانت ملونة
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        if method == 'contour':
            # تطبيق عتبة تكيفية
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY_INV, 11, 2
            )
            
            # العثور على المحيطات
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            # معالجة كل محيط
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area >= min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    region = ImageRegion(
                        x=x, y=y, width=w, height=h,
                        label=f"region_{i}", confidence=1.0
                    )
                    
                    # استخراج ميزات المنطقة
                    roi = image[y:y+h, x:x+w]
                    if roi.size > 0:  # التأكد من أن المنطقة غير فارغة
                        region.features = self.extract_features(roi)
                    
                    regions.append(region)
        
        elif method == 'blob':
            # إعداد كاشف البقع
            params = cv2.SimpleBlobDetector_Params()
            
            # تعديل المعلمات
            params.minThreshold = 10
            params.maxThreshold = 200
            params.filterByArea = True
            params.minArea = min_area
            params.filterByCircularity = False
            params.filterByConvexity = False
            params.filterByInertia = False
            
            # إنشاء الكاشف
            detector = cv2.SimpleBlobDetector_create(params)
            
            # اكتشاف البقع
            keypoints = detector.detect(gray)
            
            # تحويل النقاط الرئيسية إلى مناطق
            for i, keypoint in enumerate(keypoints):
                x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
                r = int(keypoint.size / 2)
                
                # إنشاء مستطيل محيط
                x1 = max(0, x - r)
                y1 = max(0, y - r)
                x2 = min(image.shape[1], x + r)
                y2 = min(image.shape[0], y + r)
                
                region = ImageRegion(
                    x=x1, y=y1, width=x2-x1, height=y2-y1,
                    label=f"blob_{i}", confidence=keypoint.response
                )
                
                # استخراج ميزات المنطقة
                roi = image[y1:y2, x1:x2]
                if roi.size > 0:  # التأكد من أن المنطقة غير فارغة
                    region.features = self.extract_features(roi)
                
                regions.append(region)
        
        elif method == 'mser':
            # إعداد MSER
            mser = cv2.MSER_create()
            mser.setMinArea(min_area)
            
            # اكتشاف المناطق
            msers, _ = mser.detectRegions(gray)
            
            # تحويل المناطق إلى مستطيلات محيطة
            for i, points in enumerate(msers):
                rect = cv2.boundingRect(points)
                x, y, w, h = rect
                
                region = ImageRegion(
                    x=x, y=y, width=w, height=h,
                    label=f"mser_{i}", confidence=1.0
                )
                
                # استخراج ميزات المنطقة
                roi = image[y:y+h, x:x+w]
                if roi.size > 0:  # التأكد من أن المنطقة غير فارغة
                    region.features = self.extract_features(roi)
                
                regions.append(region)
        
        else:
            logger.warning(f"طريقة اكتشاف المناطق غير معروفة: {method}، استخدام الطريقة الافتراضية")
            return self.detect_regions_of_interest(image, method='contour', min_area=min_area)
        
        return regions
    
    def visualize_regions(self, image: np.ndarray, regions: List[ImageRegion], 
                         output_path: str = None) -> np.ndarray:
        """تصور مناطق الاهتمام على الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            regions (List[ImageRegion]): قائمة بمناطق الاهتمام
            output_path (str, optional): مسار لحفظ الصورة
            
        الإرجاع:
            np.ndarray: الصورة مع تمييز المناطق
        """
        # نسخة من الصورة للرسم عليها
        vis_image = image.copy()
        
        # ألوان عشوائية للمناطق
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (128, 0, 0), (0, 128, 0), (0, 0, 128)
        ]
        
        # رسم كل منطقة
        for i, region in enumerate(regions):
            color = colors[i % len(colors)]
            x, y, w, h = region.x, region.y, region.width, region.height
            
            # رسم المستطيل
            cv2.rectangle(vis_image, (x, y), (x + w, y + h), color, 2)
            
            # إضافة التسمية
            label = f"{region.label}"
            if region.confidence > 0:
                label += f" ({region.confidence:.2f})"
            
            cv2.putText(
                vis_image, label, (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
            )
        
        # حفظ الصورة إذا تم تحديد المسار
        if output_path:
            self.save_image(vis_image, output_path)
        
        return vis_image
    
    def compare_images(self, image1: np.ndarray, image2: np.ndarray) -> Dict[str, float]:
        """مقارنة صورتين وحساب مقاييس التشابه
        
        المعاملات:
            image1 (np.ndarray): مصفوفة الصورة الأولى
            image2 (np.ndarray): مصفوفة الصورة الثانية
            
        الإرجاع:
            Dict[str, float]: مقاييس التشابه
        """
        # التأكد من أن الصورتين لهما نفس الحجم
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        
        # تحويل إلى صور رمادية إذا كانت ملونة
        if len(image1.shape) == 3:
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        else:
            gray1 = image1.copy()
            
        if len(image2.shape) == 3:
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        else:
            gray2 = image2.copy()
        
        # حساب MSE (Mean Squared Error)
        mse = np.mean((gray1.astype(np.float32) - gray2.astype(np.float32)) ** 2)
        
        # حساب PSNR (Peak Signal-to-Noise Ratio)
        if mse == 0:
            psnr = float('inf')
        else:
            psnr = 10 * np.log10((255 ** 2) / mse)
        
        # حساب SSIM (Structural Similarity Index)
        try:
            from skimage.metrics import structural_similarity as ssim
            ssim_value = ssim(gray1, gray2)
        except ImportError:
            logger.warning("لم يتم العثور على مكتبة scikit-image، تخطي حساب SSIM")
            ssim_value = -1
        
        # حساب معامل الارتباط
        correlation = np.corrcoef(gray1.flatten(), gray2.flatten())[0, 1]
        
        # حساب مقياس التشابه بناءً على هيستوجرام الصورة
        hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
        
        # تطبيع الهيستوجرام
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
        
        # حساب تشابه الهيستوجرام
        hist_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        return {
            "mse": float(mse),
            "psnr": float(psnr),
            "ssim": float(ssim_value),
            "correlation": float(correlation),
            "histogram_similarity": float(hist_similarity)
        }
    
    def apply_color_correction(self, image: np.ndarray, 
                              reference_image: np.ndarray = None) -> np.ndarray:
        """تطبيق تصحيح الألوان على الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            reference_image (np.ndarray, optional): صورة مرجعية للتصحيح
            
        الإرجاع:
            np.ndarray: الصورة بعد تصحيح الألوان
        """
        # التأكد من أن الصورة ملونة
        if len(image.shape) != 3 or image.shape[2] != 3:
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            else:
                logger.error("الصورة ليست ملونة ولا يمكن تصحيح الألوان")
                return image
        
        if reference_image is not None:
            # التأكد من أن الصورة المرجعية ملونة
            if len(reference_image.shape) != 3 or reference_image.shape[2] != 3:
                if len(reference_image.shape) == 2:
                    reference_image = cv2.cvtColor(reference_image, cv2.COLOR_GRAY2BGR)
                else:
                    logger.error("الصورة المرجعية ليست ملونة")
                    reference_image = None
        
        if reference_image is not None:
            # تصحيح الألوان باستخدام الصورة المرجعية
            # تحويل إلى LAB
            lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            lab_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2LAB)
            
            # حساب المتوسط والانحراف المعياري
            l_mean_src, a_mean_src, b_mean_src = cv2.split(lab_image)
            l_mean_ref, a_mean_ref, b_mean_ref = cv2.split(lab_reference)
            
            # حساب المتوسط والانحراف المعياري للقنوات
            l_mean_src_val = np.mean(l_mean_src)
            a_mean_src_val = np.mean(a_mean_src)
            b_mean_src_val = np.mean(b_mean_src)
            
            l_mean_ref_val = np.mean(l_mean_ref)
            a_mean_ref_val = np.mean(a_mean_ref)
            b_mean_ref_val = np.mean(b_mean_ref)
            
            l_std_src = np.std(l_mean_src)
            a_std_src = np.std(a_mean_src)
            b_std_src = np.std(b_mean_src)
            
            l_std_ref = np.std(l_mean_ref)
            a_std_ref = np.std(a_mean_ref)
            b_std_ref = np.std(b_mean_ref)
            
            # تعديل القنوات
            l_mean_src = ((l_mean_src - l_mean_src_val) * (l_std_ref / l_std_src)) + l_mean_ref_val
            a_mean_src = ((a_mean_src - a_mean_src_val) * (a_std_ref / a_std_src)) + a_mean_ref_val
            b_mean_src = ((b_mean_src - b_mean_src_val) * (b_std_ref / b_std_src)) + b_mean_ref_val
            
            # دمج القنوات
            lab_result = cv2.merge([l_mean_src, a_mean_src, b_mean_src])
            
            # تحويل مرة أخرى إلى BGR
            corrected_image = cv2.cvtColor(lab_result, cv2.COLOR_LAB2BGR)
            
            return corrected_image
        else:
            # تصحيح الألوان التلقائي
            # تطبيق توازن اللون الأبيض التلقائي
            
            # طريقة Gray World
            bgr = cv2.split(image)
            b_avg = np.mean(bgr[0])
            g_avg = np.mean(bgr[1])
            r_avg = np.mean(bgr[2])
            
            # حساب المتوسط العام
            avg = (b_avg + g_avg + r_avg) / 3
            
            # تعديل كل قناة
            b_gain = avg / b_avg
            g_gain = avg / g_avg
            r_gain = avg / r_avg
            
            # تطبيق التعديل
            bgr[0] = cv2.multiply(bgr[0], b_gain)
            bgr[1] = cv2.multiply(bgr[1], g_gain)
            bgr[2] = cv2.multiply(bgr[2], r_gain)
            
            # دمج القنوات
            corrected_image = cv2.merge(bgr)
            
            return corrected_image
    
    def create_image_pyramid(self, image: np.ndarray, levels: int = 3) -> List[np.ndarray]:
        """إنشاء هرم صور بمستويات مختلفة من التفاصيل
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            levels (int): عدد مستويات الهرم
            
        الإرجاع:
            List[np.ndarray]: قائمة بالصور في مستويات مختلفة
        """
        pyramid = [image]
        current_image = image.copy()
        
        for _ in range(levels - 1):
            current_image = cv2.pyrDown(current_image)
            pyramid.append(current_image)
        
        return pyramid
    
    def apply_clahe(self, image: np.ndarray, clip_limit: float = 2.0, 
                   grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """تطبيق تحسين التباين المحدود تكيفيًا (CLAHE)
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            clip_limit (float): حد القطع
            grid_size (Tuple[int, int]): حجم الشبكة
            
        الإرجاع:
            np.ndarray: الصورة بعد تطبيق CLAHE
        """
        # إنشاء كائن CLAHE
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
        
        # تطبيق CLAHE حسب نوع الصورة
        if len(image.shape) == 2:
            # صورة رمادية
            return clahe.apply(image)
        elif len(image.shape) == 3:
            # صورة ملونة
            # تحويل إلى LAB
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # تطبيق CLAHE على قناة الإضاءة فقط
            cl = clahe.apply(l)
            
            # دمج القنوات
            enhanced_lab = cv2.merge([cl, a, b])
            
            # تحويل مرة أخرى إلى BGR
            return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        else:
            logger.error("نوع الصورة غير مدعوم لتطبيق CLAHE")
            return image
    
    def crop_to_content(self, image: np.ndarray, padding: int = 10) -> np.ndarray:
        """اقتصاص الصورة إلى المحتوى الرئيسي
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            padding (int): التباعد حول المحتوى
            
        الإرجاع:
            np.ndarray: الصورة بعد الاقتصاص
        """
        # تحويل إلى صورة رمادية إذا كانت ملونة
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # تطبيق عتبة لفصل المحتوى عن الخلفية
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # العثور على الإحداثيات غير الصفرية
        coords = cv2.findNonZero(thresh)
        
        if coords is None or len(coords) == 0:
            logger.warning("لم يتم العثور على محتوى في الصورة")
            return image
        
        # الحصول على المستطيل المحيط
        x, y, w, h = cv2.boundingRect(coords)
        
        # إضافة التباعد
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        
        # اقتصاص الصورة
        return image[y:y+h, x:x+w]
    
    def generate_thumbnail(self, image: np.ndarray, size: Tuple[int, int] = (100, 100)) -> np.ndarray:
        """إنشاء صورة مصغرة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            size (Tuple[int, int]): حجم الصورة المصغرة
            
        الإرجاع:
            np.ndarray: الصورة المصغرة
        """
        # تغيير حجم الصورة مع الحفاظ على النسبة
        h, w = image.shape[:2]
        aspect_ratio = w / h
        
        if aspect_ratio > 1:
            # الصورة أعرض من ارتفاعها
            new_w = size[0]
            new_h = int(new_w / aspect_ratio)
        else:
            # الصورة أطول من عرضها
            new_h = size[1]
            new_w = int(new_h * aspect_ratio)
        
        # تغيير الحجم
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # إنشاء صورة فارغة بالحجم المطلوب
        thumbnail = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        
        # حساب موضع الصورة المصغرة
        x_offset = (size[0] - new_w) // 2
        y_offset = (size[1] - new_h) // 2
        
        # نسخ الصورة المصغرة إلى الموضع المحسوب
        if len(image.shape) == 3:
            thumbnail[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        else:
            # تحويل الصورة الرمادية إلى ملونة
            colored = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
            thumbnail[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = colored
        
        return thumbnail
    
    def apply_filters(self, image: np.ndarray, filter_type: str = 'sharpen') -> np.ndarray:
        """تطبيق مرشحات مختلفة على الصورة
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            filter_type (str): نوع المرشح ('sharpen', 'blur', 'emboss', 'edge_enhance')
            
        الإرجاع:
            np.ndarray: الصورة بعد تطبيق المرشح
        """
        if filter_type == 'sharpen':
            # مرشح التحديد
            kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])
            return cv2.filter2D(image, -1, kernel)
        
        elif filter_type == 'blur':
            # مرشح التنعيم
            return cv2.GaussianBlur(image, (5, 5), 0)
        
        elif filter_type == 'emboss':
            # مرشح النقش
            kernel = np.array([[-2, -1, 0],
                              [-1,  1, 1],
                              [ 0,  1, 2]])
            return cv2.filter2D(image, -1, kernel)
        
        elif filter_type == 'edge_enhance':
            # مرشح تعزيز الحواف
            kernel = np.array([[-1, -1, -1],
                              [-1, 8, -1],
                              [-1, -1, -1]])
            edges = cv2.filter2D(image, -1, kernel)
            return cv2.addWeighted(image, 1, edges, 0.5, 0)
        
        else:
            logger.warning(f"نوع المرشح غير معروف: {filter_type}، استخدام المرشح الافتراضي")
            return self.apply_filters(image, filter_type='sharpen')
    
    def analyze_leaf_health(self, image: np.ndarray) -> Dict[str, Any]:
        """تحليل صحة الأوراق النباتية
        
        المعاملات:
            image (np.ndarray): مصفوفة الصورة
            
        الإرجاع:
            Dict[str, Any]: نتائج تحليل صحة الأوراق
        """
        # التأكد من أن الصورة ملونة
        if len(image.shape) != 3 or image.shape[2] != 3:
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            else:
                logger.error("الصورة ليست ملونة ولا يمكن تحليل صحة الأوراق")
                return {"error": "الصورة ليست ملونة"}
        
        # تحويل إلى فضاء HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # تحديد نطاقات الألوان للأوراق الصحية والمريضة
        # نطاق اللون الأخضر (أوراق صحية)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        
        # نطاق اللون الأصفر (أوراق مصابة بنقص العناصر)
        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([35, 255, 255])
        
        # نطاق اللون البني (أوراق مريضة)
        lower_brown = np.array([0, 50, 50])
        upper_brown = np.array([20, 255, 255])
        
        # إنشاء أقنعة للألوان المختلفة
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        
        # حساب نسب الألوان
        total_pixels = image.shape[0] * image.shape[1]
        green_pixels = cv2.countNonZero(mask_green)
        yellow_pixels = cv2.countNonZero(mask_yellow)
        brown_pixels = cv2.countNonZero(mask_brown)
        
        green_percentage = (green_pixels / total_pixels) * 100
        yellow_percentage = (yellow_pixels / total_pixels) * 100
        brown_percentage = (brown_pixels / total_pixels) * 100
        
        # تقدير صحة الورقة
        health_score = green_percentage / (green_percentage + yellow_percentage + brown_percentage + 1e-6) * 100
        
        # تحديد حالة الورقة
        if health_score > 80:
            health_status = "صحية"
        elif health_score > 50:
            health_status = "صحية جزئيًا"
        elif health_score > 20:
            health_status = "مريضة"
        else:
            health_status = "مريضة جدًا"
        
        # تحليل التوزيع المكاني للمناطق المريضة
        # إنشاء قناع للمناطق المريضة
        disease_mask = cv2.bitwise_or(mask_yellow, mask_brown)
        
        # تحديد المكونات المتصلة
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(disease_mask, connectivity=8)
        
        # تجاهل الخلفية (المكون الأول)
        disease_regions = []
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area > 100:  # تجاهل المناطق الصغيرة جدًا
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                
                disease_regions.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": int(area),
                    "center_x": int(centroids[i][0]),
                    "center_y": int(centroids[i][1])
                })
        
        return {
            "health_score": float(health_score),
            "health_status": health_status,
            "color_distribution": {
                "green_percentage": float(green_percentage),
                "yellow_percentage": float(yellow_percentage),
                "brown_percentage": float(brown_percentage)
            },
            "disease_regions": disease_regions,
            "disease_coverage": float((yellow_pixels + brown_pixels) / total_pixels * 100)
        }
