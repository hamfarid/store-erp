#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام التحليل الأولي للصور الزراعية
يقوم بتحويل الصور المقسمة إلى تمثيلات مبسطة لتحسين كفاءة التعلم
"""

import os
import cv2
import numpy as np
import logging
import json
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Any, Optional

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PrimitiveFeatures:
    """فئة لتخزين الميزات الأولية للصورة"""
    
    # ميزات اللون
    dominant_colors: List[List[int]] = field(default_factory=list)  # قائمة بالألوان المهيمنة [R,G,B]
    color_histogram: List[float] = field(default_factory=list)  # مدرج تكراري للألوان
    color_moments: List[float] = field(default_factory=list)  # لحظات اللون (المتوسط، الانحراف المعياري، الالتواء)
    
    # ميزات النسيج
    texture_haralick: List[float] = field(default_factory=list)  # ميزات هاراليك للنسيج
    texture_lbp: List[float] = field(default_factory=list)  # أنماط ثنائية محلية
    texture_glcm: Dict[str, float] = field(default_factory=dict)  # مصفوفة التواجد المكاني للمستوى الرمادي
    
    # ميزات الشكل
    shape_contours: List[List[List[int]]] = field(default_factory=list)  # محيطات الشكل
    shape_moments: List[float] = field(default_factory=list)  # لحظات الشكل
    shape_hu_moments: List[float] = field(default_factory=list)  # لحظات هو للشكل
    shape_area: float = 0.0  # مساحة الشكل
    shape_perimeter: float = 0.0  # محيط الشكل
    
    # ميزات الشذوذ
    anomaly_regions: List[Dict[str, Any]] = field(default_factory=list)  # مناطق الشذوذ
    anomaly_score: float = 0.0  # درجة الشذوذ
    
    # معلومات إضافية
    image_size: Tuple[int, int] = (0, 0)  # حجم الصورة (العرض، الارتفاع)
    segment_count: int = 0  # عدد الأجزاء
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الميزات إلى قاموس"""
        return asdict(self)
    
    def to_json(self) -> str:
        """تحويل الميزات إلى سلسلة JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PrimitiveFeatures':
        """إنشاء كائن من قاموس"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'PrimitiveFeatures':
        """إنشاء كائن من سلسلة JSON"""
        return cls.from_dict(json.loads(json_str))

class PrimitiveImageAnalyzer:
    """فئة لتحليل الصور وتحويلها إلى تمثيلات أولية"""
    
    def __init__(self, config=None):
        """
        تهيئة محلل الصور الأولي
        
        المعلمات:
            config (dict): تكوين المحلل
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين الافتراضي
        self.config = {
            'dominant_colors_count': int(os.getenv('PRIMITIVE_DOMINANT_COLORS', 5)),
            'color_histogram_bins': int(os.getenv('PRIMITIVE_COLOR_HISTOGRAM_BINS', 32)),
            'texture_haralick_distances': [1, 2, 3],
            'texture_lbp_points': int(os.getenv('PRIMITIVE_LBP_POINTS', 8)),
            'texture_lbp_radius': int(os.getenv('PRIMITIVE_LBP_RADIUS', 1)),
            'anomaly_threshold': float(os.getenv('PRIMITIVE_ANOMALY_THRESHOLD', 0.7)),
            'output_dir': os.getenv('PRIMITIVE_OUTPUT_DIR', 'data/primitive_features'),
            'segment_method': os.getenv('PRIMITIVE_SEGMENT_METHOD', 'kmeans'),  # 'kmeans', 'watershed', 'grabcut'
            'segment_count': int(os.getenv('PRIMITIVE_SEGMENT_COUNT', 5)),
            'save_segmented_images': os.getenv('PRIMITIVE_SAVE_SEGMENTED', 'true').lower() == 'true'
        }
        
        # دمج التكوين المقدم مع التكوين الافتراضي
        if config:
            self.config.update(config)
            
        # إنشاء مجلد المخرجات إذا لم يكن موجودًا
        os.makedirs(self.config['output_dir'], exist_ok=True)
    
    def _extract_dominant_colors(self, image: np.ndarray) -> List[List[int]]:
        """
        استخراج الألوان المهيمنة من الصورة
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[List[int]]: قائمة بالألوان المهيمنة [R,G,B]
        """
        # تحويل الصورة إلى مصفوفة ثنائية الأبعاد من البكسلات
        pixels = image.reshape(-1, 3).astype(np.float32)
        
        # تحديد عدد الألوان المهيمنة
        k = min(self.config['dominant_colors_count'], len(pixels))
        
        if k <= 0:
            return []
        
        # استخدام K-means لاستخراج الألوان المهيمنة
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # حساب نسبة كل لون
        counts = np.bincount(labels.flatten())
        
        # ترتيب الألوان حسب تكرارها
        indices = np.argsort(counts)[::-1]
        
        # تحويل الألوان إلى قائمة
        dominant_colors = []
        for i in indices:
            if i < len(centers):
                color = centers[i].astype(int).tolist()
                dominant_colors.append(color)
        
        return dominant_colors
    
    def _extract_color_histogram(self, image: np.ndarray) -> List[float]:
        """
        استخراج المدرج التكراري للألوان
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[float]: المدرج التكراري للألوان
        """
        # تحديد عدد الفئات
        bins = self.config['color_histogram_bins']
        
        # حساب المدرج التكراري لكل قناة لون
        hist_b = cv2.calcHist([image], [0], None, [bins], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [bins], [0, 256])
        hist_r = cv2.calcHist([image], [2], None, [bins], [0, 256])
        
        # تطبيع المدرجات التكرارية
        cv2.normalize(hist_b, hist_b, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_g, hist_g, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist_r, hist_r, 0, 1, cv2.NORM_MINMAX)
        
        # دمج المدرجات التكرارية
        hist = np.concatenate([hist_b, hist_g, hist_r]).flatten().tolist()
        
        return hist
    
    def _extract_color_moments(self, image: np.ndarray) -> List[float]:
        """
        استخراج لحظات اللون
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[float]: لحظات اللون (المتوسط، الانحراف المعياري، الالتواء)
        """
        # فصل قنوات اللون
        b, g, r = cv2.split(image)
        
        # حساب اللحظات لكل قناة
        moments = []
        
        for channel in [b, g, r]:
            # اللحظة الأولى (المتوسط)
            mean = np.mean(channel)
            moments.append(float(mean))
            
            # اللحظة الثانية (الانحراف المعياري)
            std = np.std(channel)
            moments.append(float(std))
            
            # اللحظة الثالثة (الالتواء)
            # الالتواء = E[(X - μ)^3] / σ^3
            if std > 0:
                skewness = np.mean(((channel - mean) / std) ** 3)
            else:
                skewness = 0
            moments.append(float(skewness))
        
        return moments
    
    def _extract_texture_haralick(self, image: np.ndarray) -> List[float]:
        """
        استخراج ميزات هاراليك للنسيج
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[float]: ميزات هاراليك للنسيج
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب ميزات هاراليك
        distances = self.config['texture_haralick_distances']
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]  # 0, 45, 90, 135 درجة
        
        features = []
        for distance in distances:
            for angle in angles:
                glcm = self._compute_glcm(gray, distance, angle)
                haralick_features = self._compute_haralick_features(glcm)
                features.extend(haralick_features)
        
        return features
    
    def _compute_glcm(self, gray_image: np.ndarray, distance: int, angle: float) -> np.ndarray:
        """
        حساب مصفوفة التواجد المكاني للمستوى الرمادي
        
        المعلمات:
            gray_image (np.ndarray): صورة بتدرج الرمادي
            distance (int): المسافة
            angle (float): الزاوية
            
        العوائد:
            np.ndarray: مصفوفة GLCM
        """
        # تقليل مستويات الرمادي إلى 8 بت (256 مستوى)
        if gray_image.dtype != np.uint8:
            gray_image = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # حساب مصفوفة GLCM
        dx = int(np.cos(angle) * distance)
        dy = int(np.sin(angle) * distance)
        
        height, width = gray_image.shape
        glcm = np.zeros((256, 256), dtype=np.uint32)
        
        for i in range(height):
            for j in range(width):
                i2 = i + dy
                j2 = j + dx
                
                if 0 <= i2 < height and 0 <= j2 < width:
                    glcm[gray_image[i, j], gray_image[i2, j2]] += 1
        
        # تطبيع المصفوفة
        if glcm.sum() > 0:
            glcm = glcm / glcm.sum()
        
        return glcm
    
    def _compute_haralick_features(self, glcm: np.ndarray) -> List[float]:
        """
        حساب ميزات هاراليك من مصفوفة GLCM
        
        المعلمات:
            glcm (np.ndarray): مصفوفة GLCM
            
        العوائد:
            List[float]: ميزات هاراليك
        """
        # حساب ميزات هاراليك الأساسية
        features = []
        
        # التباين
        i_coords, j_coords = np.meshgrid(np.arange(glcm.shape[0]), np.arange(glcm.shape[1]), indexing='ij')
        contrast = np.sum(glcm * ((i_coords - j_coords) ** 2))
        features.append(float(contrast))
        
        # التجانس
        homogeneity = np.sum(glcm / (1 + np.abs(i_coords - j_coords)))
        features.append(float(homogeneity))
        
        # الطاقة
        energy = np.sum(glcm ** 2)
        features.append(float(energy))
        
        # الترابط
        if glcm.sum() > 0:
            # حساب المتوسطات والانحرافات المعيارية
            i_mean = np.sum(i_coords * glcm)
            j_mean = np.sum(j_coords * glcm)
            
            i_var = np.sum(((i_coords - i_mean) ** 2) * glcm)
            j_var = np.sum(((j_coords - j_mean) ** 2) * glcm)
            
            if i_var > 0 and j_var > 0:
                correlation = np.sum(((i_coords - i_mean) * (j_coords - j_mean) * glcm) / np.sqrt(i_var * j_var))
            else:
                correlation = 0
        else:
            correlation = 0
            
        features.append(float(correlation))
        
        return features
    
    def _extract_texture_lbp(self, image: np.ndarray) -> List[float]:
        """
        استخراج ميزات أنماط ثنائية محلية
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[float]: ميزات LBP
        """
        try:
            from skimage.feature import local_binary_pattern
            
            # تحويل الصورة إلى تدرج الرمادي
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # حساب LBP
            points = self.config['texture_lbp_points']
            radius = self.config['texture_lbp_radius']
            
            lbp = local_binary_pattern(gray, points, radius, method='uniform')
            
            # حساب المدرج التكراري
            n_bins = points + 2
            hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins), density=True)
            
            return hist.tolist()
            
        except ImportError:
            logger.warning("لم يتم العثور على مكتبة scikit-image. لا يمكن استخراج ميزات LBP.")
            return []
    
    def _extract_texture_glcm_features(self, image: np.ndarray) -> Dict[str, float]:
        """
        استخراج ميزات GLCM
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            Dict[str, float]: ميزات GLCM
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب مصفوفة GLCM
        distance = 1
        angle = 0  # 0 درجة
        glcm = self._compute_glcm(gray, distance, angle)
        
        # حساب ميزات GLCM
        features = {}
        
        # التباين
        i_coords, j_coords = np.meshgrid(np.arange(glcm.shape[0]), np.arange(glcm.shape[1]), indexing='ij')
        features['contrast'] = float(np.sum(glcm * ((i_coords - j_coords) ** 2)))
        
        # التجانس
        features['homogeneity'] = float(np.sum(glcm / (1 + np.abs(i_coords - j_coords))))
        
        # الطاقة
        features['energy'] = float(np.sum(glcm ** 2))
        
        # الترابط
        if glcm.sum() > 0:
            # حساب المتوسطات والانحرافات المعيارية
            i_mean = np.sum(i_coords * glcm)
            j_mean = np.sum(j_coords * glcm)
            
            i_var = np.sum(((i_coords - i_mean) ** 2) * glcm)
            j_var = np.sum(((j_coords - j_mean) ** 2) * glcm)
            
            if i_var > 0 and j_var > 0:
                features['correlation'] = float(np.sum(((i_coords - i_mean) * (j_coords - j_mean) * glcm) / np.sqrt(i_var * j_var)))
            else:
                features['correlation'] = 0.0
        else:
            features['correlation'] = 0.0
        
        # التباين
        features['dissimilarity'] = float(np.sum(glcm * np.abs(i_coords - j_coords)))
        
        # الانتروبيا
        mask = glcm > 0
        if mask.any():
            entropy = -np.sum(glcm[mask] * np.log2(glcm[mask]))
        else:
            entropy = 0.0
        features['entropy'] = float(entropy)
        
        return features
    
    def _extract_shape_contours(self, image: np.ndarray) -> Tuple[List[List[List[int]]], float, float]:
        """
        استخراج محيطات الشكل
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            Tuple[List[List[List[int]]], float, float]: محيطات الشكل، المساحة، المحيط
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # تطبيق عتبة ثنائية
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # العثور على المحيطات
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # حساب المساحة والمحيط
        total_area = 0.0
        total_perimeter = 0.0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            total_area += area
            total_perimeter += perimeter
        
        # تحويل المحيطات إلى قائمة
        contours_list = []
        for contour in contours:
            contour_list = contour.reshape(-1, 2).tolist()
            contours_list.append(contour_list)
        
        return contours_list, total_area, total_perimeter
    
    def _extract_shape_moments(self, image: np.ndarray) -> List[float]:
        """
        استخراج لحظات الشكل
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[float]: لحظات الشكل
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب لحظات الصورة
        moments = cv2.moments(gray)
        
        # استخراج اللحظات المهمة
        features = []
        for key in ['m00', 'm10', 'm01', 'm20', 'm11', 'm02', 'm30', 'm21', 'm12', 'm03']:
            features.append(float(moments[key]))
        
        return features
    
    def _extract_shape_hu_moments(self, image: np.ndarray) -> List[float]:
        """
        استخراج لحظات هو للشكل
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            List[float]: لحظات هو للشكل
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # حساب لحظات الصورة
        moments = cv2.moments(gray)
        
        # حساب لحظات هو
        hu_moments = cv2.HuMoments(moments)
        
        # تحويل اللحظات إلى قائمة
        features = [float(np.log(abs(moment) + 1e-10)) for moment in hu_moments.flatten()]
        
        return features
    
    def _extract_anomaly_regions(self, image: np.ndarray) -> Tuple[List[Dict[str, Any]], float]:
        """
        استخراج مناطق الشذوذ
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            Tuple[List[Dict[str, Any]], float]: مناطق الشذوذ، درجة الشذوذ
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # تطبيق مرشح جاوس لتنعيم الصورة
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # تطبيق عتبة تكيفية
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # العثور على المحيطات
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # تحليل المحيطات
        anomaly_regions = []
        total_anomaly_area = 0.0
        total_area = gray.shape[0] * gray.shape[1]
        
        for contour in contours:
            # حساب مساحة المحيط
            area = cv2.contourArea(contour)
            
            # تجاهل المحيطات الصغيرة جدًا
            if area < 50:
                continue
            
            # حساب المستطيل المحيط
            x, y, w, h = cv2.boundingRect(contour)
            
            # حساب نسبة العرض إلى الارتفاع
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # حساب الدائرية
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # حساب درجة الشذوذ
            anomaly_score = 1.0 - circularity
            
            # إضافة المنطقة إذا كانت درجة الشذوذ أعلى من العتبة
            if anomaly_score > self.config['anomaly_threshold']:
                region = {
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'area': float(area),
                    'perimeter': float(perimeter),
                    'aspect_ratio': float(aspect_ratio),
                    'circularity': float(circularity),
                    'anomaly_score': float(anomaly_score)
                }
                
                anomaly_regions.append(region)
                total_anomaly_area += area
        
        # حساب درجة الشذوذ الإجمالية
        overall_anomaly_score = total_anomaly_area / total_area if total_area > 0 else 0
        
        return anomaly_regions, overall_anomaly_score
    
    def _segment_image_kmeans(self, image: np.ndarray) -> np.ndarray:
        """
        تقسيم الصورة باستخدام K-means
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            np.ndarray: صورة مقسمة
        """
        # تحويل الصورة إلى مصفوفة ثنائية الأبعاد من البكسلات
        pixels = image.reshape(-1, 3).astype(np.float32)
        
        # تحديد عدد الأجزاء
        k = self.config['segment_count']
        
        # استخدام K-means للتقسيم
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # إعادة بناء الصورة المقسمة
        segmented_pixels = centers[labels.flatten()]
        segmented_image = segmented_pixels.reshape(image.shape).astype(np.uint8)
        
        return segmented_image
    
    def _segment_image_watershed(self, image: np.ndarray) -> np.ndarray:
        """
        تقسيم الصورة باستخدام Watershed
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            np.ndarray: صورة مقسمة
        """
        # تحويل الصورة إلى تدرج الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # تطبيق عتبة ثنائية
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # تطبيق عمليات مورفولوجية
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # تحديد المنطقة الخلفية
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # تحديد المنطقة الأمامية
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = sure_fg.astype(np.uint8)
        
        # تحديد المنطقة غير المؤكدة
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # وضع علامات للمكونات المتصلة
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        
        # تطبيق Watershed
        markers = cv2.watershed(image, markers)
        
        # إنشاء صورة مقسمة
        segmented_image = np.zeros_like(image)
        
        # تلوين كل جزء بلون مختلف
        for i in range(2, markers.max() + 1):
            mask = markers == i
            color = np.random.randint(0, 256, 3).tolist()
            segmented_image[mask] = color
        
        return segmented_image
    
    def _segment_image_grabcut(self, image: np.ndarray) -> np.ndarray:
        """
        تقسيم الصورة باستخدام GrabCut
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            np.ndarray: صورة مقسمة
        """
        # إنشاء قناع أولي
        mask = np.zeros(image.shape[:2], np.uint8)
        
        # تحديد المستطيل المحيط
        height, width = image.shape[:2]
        rect = (10, 10, width - 20, height - 20)
        
        # إنشاء نماذج مؤقتة
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # تطبيق GrabCut
        cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # تعديل القناع
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # إنشاء صورة مقسمة
        segmented_image = image * mask2[:, :, np.newaxis]
        
        return segmented_image
    
    def _segment_image(self, image: np.ndarray) -> np.ndarray:
        """
        تقسيم الصورة
        
        المعلمات:
            image (np.ndarray): صورة OpenCV
            
        العوائد:
            np.ndarray: صورة مقسمة
        """
        # اختيار طريقة التقسيم
        method = self.config['segment_method'].lower()
        
        if method == 'kmeans':
            return self._segment_image_kmeans(image)
        elif method == 'watershed':
            return self._segment_image_watershed(image)
        elif method == 'grabcut':
            return self._segment_image_grabcut(image)
        else:
            logger.warning(f"طريقة تقسيم غير معروفة: {method}. استخدام K-means بدلاً من ذلك.")
            return self._segment_image_kmeans(image)
    
    def analyze_image(self, image_path: str) -> Tuple[PrimitiveFeatures, np.ndarray]:
        """
        تحليل صورة واستخراج الميزات الأولية
        
        المعلمات:
            image_path (str): مسار الصورة
            
        العوائد:
            Tuple[PrimitiveFeatures, np.ndarray]: الميزات الأولية، الصورة المقسمة
        """
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            
            if image is None:
                raise ValueError(f"فشل قراءة الصورة: {image_path}")
            
            # تقسيم الصورة
            segmented_image = self._segment_image(image)
            
            # إنشاء كائن الميزات
            features = PrimitiveFeatures()
            
            # تخزين حجم الصورة
            features.image_size = (image.shape[1], image.shape[0])
            
            # استخراج ميزات اللون
            features.dominant_colors = self._extract_dominant_colors(segmented_image)
            features.color_histogram = self._extract_color_histogram(segmented_image)
            features.color_moments = self._extract_color_moments(segmented_image)
            
            # استخراج ميزات النسيج
            features.texture_haralick = self._extract_texture_haralick(segmented_image)
            features.texture_lbp = self._extract_texture_lbp(segmented_image)
            features.texture_glcm = self._extract_texture_glcm_features(segmented_image)
            
            # استخراج ميزات الشكل
            contours, area, perimeter = self._extract_shape_contours(segmented_image)
            features.shape_contours = contours
            features.shape_area = area
            features.shape_perimeter = perimeter
            features.shape_moments = self._extract_shape_moments(segmented_image)
            features.shape_hu_moments = self._extract_shape_hu_moments(segmented_image)
            
            # استخراج ميزات الشذوذ
            anomaly_regions, anomaly_score = self._extract_anomaly_regions(segmented_image)
            features.anomaly_regions = anomaly_regions
            features.anomaly_score = anomaly_score
            
            # تحديد عدد الأجزاء
            if self.config['segment_method'] == 'kmeans':
                features.segment_count = self.config['segment_count']
            else:
                # تقدير عدد الأجزاء من عدد المحيطات
                features.segment_count = len(contours) if len(contours) > 0 else 1
            
            return features, segmented_image
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء تحليل الصورة {image_path}: {str(e)}")
            raise
    
    def save_features(self, features: PrimitiveFeatures, image_path: str) -> str:
        """
        حفظ الميزات الأولية
        
        المعلمات:
            features (PrimitiveFeatures): الميزات الأولية
            image_path (str): مسار الصورة
            
        العوائد:
            str: مسار ملف الميزات
        """
        try:
            # إنشاء اسم الملف
            image_name = os.path.basename(image_path)
            base_name = os.path.splitext(image_name)[0]
            features_path = os.path.join(self.config['output_dir'], f"{base_name}_features.json")
            
            # حفظ الميزات
            with open(features_path, 'w', encoding='utf-8') as f:
                f.write(features.to_json())
            
            logger.info(f"تم حفظ الميزات الأولية: {features_path}")
            return features_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء حفظ الميزات الأولية: {str(e)}")
            raise
    
    def save_segmented_image(self, segmented_image: np.ndarray, image_path: str) -> str:
        """
        حفظ الصورة المقسمة
        
        المعلمات:
            segmented_image (np.ndarray): الصورة المقسمة
            image_path (str): مسار الصورة الأصلية
            
        العوائد:
            str: مسار الصورة المقسمة
        """
        try:
            # إنشاء اسم الملف
            image_name = os.path.basename(image_path)
            base_name = os.path.splitext(image_name)[0]
            segmented_path = os.path.join(self.config['output_dir'], f"{base_name}_segmented.png")
            
            # حفظ الصورة
            cv2.imwrite(segmented_path, segmented_image)
            
            logger.info(f"تم حفظ الصورة المقسمة: {segmented_path}")
            return segmented_path
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء حفظ الصورة المقسمة: {str(e)}")
            raise
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        معالجة صورة واحدة
        
        المعلمات:
            image_path (str): مسار الصورة
            
        العوائد:
            Dict[str, Any]: نتائج المعالجة
        """
        try:
            # تحليل الصورة
            features, segmented_image = self.analyze_image(image_path)
            
            # حفظ الميزات
            features_path = self.save_features(features, image_path)
            
            # حفظ الصورة المقسمة إذا تم تمكين ذلك
            segmented_path = None
            if self.config['save_segmented_images']:
                segmented_path = self.save_segmented_image(segmented_image, image_path)
            
            # إنشاء النتائج
            results = {
                'image_path': image_path,
                'features_path': features_path,
                'segmented_path': segmented_path,
                'features': features.to_dict()
            }
            
            return results
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء معالجة الصورة {image_path}: {str(e)}")
            return {
                'image_path': image_path,
                'error': str(e)
            }
    
    def process_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        معالجة مجلد من الصور
        
        المعلمات:
            directory_path (str): مسار المجلد
            
        العوائد:
            Dict[str, Any]: نتائج المعالجة
        """
        try:
            # التحقق من وجود المجلد
            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                raise ValueError(f"المجلد غير موجود: {directory_path}")
            
            # الحصول على قائمة ملفات الصور
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            image_files = [
                os.path.join(directory_path, f) for f in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, f)) and
                os.path.splitext(f)[1].lower() in image_extensions
            ]
            
            # إحصائيات المعالجة
            stats = {
                'total_images': len(image_files),
                'processed_images': 0,
                'failed_images': 0,
                'results': []
            }
            
            # معالجة كل صورة
            for image_path in image_files:
                try:
                    # معالجة الصورة
                    result = self.process_image(image_path)
                    
                    # تحديث الإحصائيات
                    if 'error' in result:
                        stats['failed_images'] += 1
                    else:
                        stats['processed_images'] += 1
                    
                    # إضافة النتيجة
                    stats['results'].append(result)
                    
                except Exception as e:
                    logger.error(f"حدث خطأ أثناء معالجة الصورة {image_path}: {str(e)}")
                    stats['failed_images'] += 1
                    stats['results'].append({
                        'image_path': image_path,
                        'error': str(e)
                    })
            
            logger.info(f"اكتمل معالجة المجلد {directory_path}: {stats['processed_images']} صورة تمت معالجتها، {stats['failed_images']} صورة فشلت")
            return stats
            
        except Exception as e:
            logger.error(f"حدث خطأ أثناء معالجة المجلد {directory_path}: {str(e)}")
            return {
                'directory_path': directory_path,
                'error': str(e),
                'total_images': 0,
                'processed_images': 0,
                'failed_images': 0,
                'results': []
            }


# نموذج استخدام
if __name__ == "__main__":
    import argparse
    
    # إنشاء محلل الوسائط
    parser = argparse.ArgumentParser(description='نظام التحليل الأولي للصور الزراعية')
    parser.add_argument('--input', '-i', required=True, help='مسار الصورة أو المجلد')
    parser.add_argument('--output', '-o', help='مجلد المخرجات')
    parser.add_argument('--method', '-m', choices=['kmeans', 'watershed', 'grabcut'], default='kmeans', help='طريقة التقسيم')
    parser.add_argument('--segments', '-s', type=int, default=5, help='عدد الأجزاء (لـ K-means)')
    parser.add_argument('--save-segmented', action='store_true', help='حفظ الصور المقسمة')
    
    # تحليل الوسائط
    args = parser.parse_args()
    
    # إنشاء التكوين
    config = {
        'segment_method': args.method,
        'segment_count': args.segments,
        'save_segmented_images': args.save_segmented
    }
    
    # تعيين مجلد المخرجات إذا تم تحديده
    if args.output:
        config['output_dir'] = args.output
    
    # إنشاء كائن المحلل
    analyzer = PrimitiveImageAnalyzer(config)
    
    # معالجة الإدخال
    if os.path.isdir(args.input):
        # معالجة مجلد
        results = analyzer.process_directory(args.input)
        print(f"تمت معالجة {results['processed_images']} صورة من أصل {results['total_images']}")
    else:
        # معالجة صورة واحدة
        results = analyzer.process_image(args.input)
        if 'error' in results:
            print(f"فشل معالجة الصورة: {results['error']}")
        else:
            print(f"تمت معالجة الصورة بنجاح")
            print(f"مسار الميزات: {results['features_path']}")
            if results['segmented_path']:
                print(f"مسار الصورة المقسمة: {results['segmented_path']}")
