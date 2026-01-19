#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة المستخدم لنظام التحليل الأولي للصور الزراعية
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import cv2
import numpy as np
from PIL import Image, ImageTk
from pathlib import Path
from dotenv import load_dotenv
import logging

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# استيراد المكونات الأخرى
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_analysis.primitive.analyzer import PrimitiveImageAnalyzer
from image_analysis.comparator import ImageAnalysisComparator

class PrimitiveAnalysisUI:
    """واجهة المستخدم الرسومية لنظام التحليل الأولي للصور الزراعية"""
    
    def __init__(self, root):
        """
        تهيئة واجهة المستخدم
        
        المعلمات:
            root: نافذة الجذر
        """
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # تهيئة النافذة الرئيسية
        self.root = root
        self.root.title("نظام التحليل الأولي للصور الزراعية")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # تكوين النظام
        self.config = {
            'primitive_output_dir': os.getenv('PRIMITIVE_OUTPUT_DIR', 'data/primitive_features'),
            'standard_output_dir': os.getenv('STANDARD_OUTPUT_DIR', 'data/standard_features'),
            'comparison_output_dir': os.getenv('COMPARISON_OUTPUT_DIR', 'data/comparison_results'),
            'visualization_output_dir': os.getenv('VISUALIZATION_OUTPUT_DIR', 'data/visualizations'),
            'segment_method': os.getenv('PRIMITIVE_SEGMENT_METHOD', 'kmeans'),
            'segment_count': int(os.getenv('PRIMITIVE_SEGMENT_COUNT', 5)),
            'save_segmented_images': os.getenv('PRIMITIVE_SAVE_SEGMENTED', 'true').lower() == 'true'
        }
        
        # إنشاء مجلدات المخرجات إذا لم تكن موجودة
        for dir_path in [
            self.config['primitive_output_dir'],
            self.config['standard_output_dir'],
            self.config['comparison_output_dir'],
            self.config['visualization_output_dir']
        ]:
            os.makedirs(dir_path, exist_ok=True)
        
        # إنشاء محلل الصور الأولي
        self.primitive_analyzer = PrimitiveImageAnalyzer({
            'output_dir': self.config['primitive_output_dir'],
            'segment_method': self.config['segment_method'],
            'segment_count': self.config['segment_count'],
            'save_segmented_images': self.config['save_segmented_images']
        })
        
        # إنشاء مقارن التحليل
        self.comparator = ImageAnalysisComparator({
            'primitive_output_dir': self.config['primitive_output_dir'],
            'standard_output_dir': self.config['standard_output_dir'],
            'comparison_output_dir': self.config['comparison_output_dir'],
            'visualization_output_dir': self.config['visualization_output_dir'],
            'save_visualizations': True
        })
        
        # متغيرات الحالة
        self.current_image_path = None
        self.current_segmented_image = None
        self.current_features = None
        self.current_comparison_result = None
        
        # إنشاء واجهة المستخدم
        self._create_ui()
    
    def _create_ui(self):
        """إنشاء عناصر واجهة المستخدم"""
        # إنشاء إطار رئيسي
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إنشاء شريط القوائم
        self._create_menu()
        
        # إنشاء شريط الأدوات
        self._create_toolbar(main_frame)
        
        # إنشاء إطار المحتوى
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # تقسيم إطار المحتوى إلى جزأين
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)
        
        # إنشاء إطار الصور
        image_frame = ttk.LabelFrame(content_frame, text="الصور")
        image_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        
        # إنشاء إطار التفاصيل
        details_frame = ttk.LabelFrame(content_frame, text="التفاصيل")
        details_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        
        # إنشاء عناصر إطار الصور
        self._create_image_frame(image_frame)
        
        # إنشاء عناصر إطار التفاصيل
        self._create_details_frame(details_frame)
        
        # إنشاء شريط الحالة
        self._create_status_bar()
    
    def _create_menu(self):
        """إنشاء شريط القوائم"""
        # إنشاء شريط القوائم
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="فتح صورة...", command=self._open_image)
        file_menu.add_command(label="فتح مجلد...", command=self._open_directory)
        file_menu.add_separator()
        file_menu.add_command(label="حفظ النتائج...", command=self._save_results)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.root.quit)
        
        # قائمة التحليل
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="تحليل", menu=analysis_menu)
        analysis_menu.add_command(label="تحليل الصورة الحالية", command=self._analyze_current_image)
        analysis_menu.add_command(label="مقارنة مع التحليل القياسي", command=self._compare_current_image)
        analysis_menu.add_separator()
        analysis_menu.add_command(label="تحليل جميع الصور في المجلد", command=self._analyze_directory)
        
        # قائمة الإعدادات
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="إعدادات", menu=settings_menu)
        settings_menu.add_command(label="إعدادات التحليل الأولي...", command=self._show_settings)
        
        # قائمة المساعدة
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        help_menu.add_command(label="حول...", command=self._show_about)
    
    def _create_toolbar(self, parent):
        """
        إنشاء شريط الأدوات
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار شريط الأدوات
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # زر فتح صورة
        open_button = ttk.Button(toolbar_frame, text="فتح صورة", command=self._open_image)
        open_button.pack(side=tk.LEFT, padx=2)
        
        # زر فتح مجلد
        open_dir_button = ttk.Button(toolbar_frame, text="فتح مجلد", command=self._open_directory)
        open_dir_button.pack(side=tk.LEFT, padx=2)
        
        # فاصل
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # زر تحليل
        analyze_button = ttk.Button(toolbar_frame, text="تحليل", command=self._analyze_current_image)
        analyze_button.pack(side=tk.LEFT, padx=2)
        
        # زر مقارنة
        compare_button = ttk.Button(toolbar_frame, text="مقارنة", command=self._compare_current_image)
        compare_button.pack(side=tk.LEFT, padx=2)
        
        # فاصل
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # قائمة منسدلة لطريقة التقسيم
        ttk.Label(toolbar_frame, text="طريقة التقسيم:").pack(side=tk.LEFT, padx=2)
        
        self.segment_method_var = tk.StringVar(value=self.config['segment_method'])
        segment_method_combo = ttk.Combobox(toolbar_frame, textvariable=self.segment_method_var, width=10)
        segment_method_combo['values'] = ('kmeans', 'watershed', 'grabcut')
        segment_method_combo.pack(side=tk.LEFT, padx=2)
        segment_method_combo.bind('<<ComboboxSelected>>', self._update_segment_method)
        
        # مدخل لعدد الأجزاء
        ttk.Label(toolbar_frame, text="عدد الأجزاء:").pack(side=tk.LEFT, padx=2)
        
        self.segment_count_var = tk.StringVar(value=str(self.config['segment_count']))
        segment_count_entry = ttk.Entry(toolbar_frame, textvariable=self.segment_count_var, width=5)
        segment_count_entry.pack(side=tk.LEFT, padx=2)
        segment_count_entry.bind('<Return>', self._update_segment_count)
        segment_count_entry.bind('<FocusOut>', self._update_segment_count)
    
    def _create_image_frame(self, parent):
        """
        إنشاء إطار الصور
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار الصور
        image_frame = ttk.Frame(parent)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        # تقسيم إطار الصور إلى صفين
        image_frame.rowconfigure(0, weight=1)
        image_frame.rowconfigure(1, weight=1)
        image_frame.columnconfigure(0, weight=1)
        
        # إنشاء إطار الصورة الأصلية
        original_frame = ttk.LabelFrame(image_frame, text="الصورة الأصلية")
        original_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # إنشاء إطار الصورة المقسمة
        segmented_frame = ttk.LabelFrame(image_frame, text="الصورة المقسمة")
        segmented_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # إنشاء عناصر إطار الصورة الأصلية
        self.original_canvas = tk.Canvas(original_frame, bg="white")
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # إنشاء عناصر إطار الصورة المقسمة
        self.segmented_canvas = tk.Canvas(segmented_frame, bg="white")
        self.segmented_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_details_frame(self, parent):
        """
        إنشاء إطار التفاصيل
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء دفتر التبويب
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء تبويب الميزات
        features_frame = ttk.Frame(self.notebook)
        self.notebook.add(features_frame, text="الميزات")
        
        # إنشاء تبويب المقارنة
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text="المقارنة")
        
        # إنشاء تبويب التصور المرئي
        visualization_frame = ttk.Frame(self.notebook)
        self.notebook.add(visualization_frame, text="التصور المرئي")
        
        # إنشاء عناصر تبويب الميزات
        self._create_features_tab(features_frame)
        
        # إنشاء عناصر تبويب المقارنة
        self._create_comparison_tab(comparison_frame)
        
        # إنشاء عناصر تبويب التصور المرئي
        self._create_visualization_tab(visualization_frame)
    
    def _create_features_tab(self, parent):
        """
        إنشاء تبويب الميزات
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء دفتر تبويب داخلي
        features_notebook = ttk.Notebook(parent)
        features_notebook.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء تبويب ميزات اللون
        color_frame = ttk.Frame(features_notebook)
        features_notebook.add(color_frame, text="اللون")
        
        # إنشاء تبويب ميزات النسيج
        texture_frame = ttk.Frame(features_notebook)
        features_notebook.add(texture_frame, text="النسيج")
        
        # إنشاء تبويب ميزات الشكل
        shape_frame = ttk.Frame(features_notebook)
        features_notebook.add(shape_frame, text="الشكل")
        
        # إنشاء تبويب ميزات الشذوذ
        anomaly_frame = ttk.Frame(features_notebook)
        features_notebook.add(anomaly_frame, text="الشذوذ")
        
        # إنشاء تبويب JSON
        json_frame = ttk.Frame(features_notebook)
        features_notebook.add(json_frame, text="JSON")
        
        # إنشاء عناصر تبويب ميزات اللون
        self._create_color_features_tab(color_frame)
        
        # إنشاء عناصر تبويب ميزات النسيج
        self._create_texture_features_tab(texture_frame)
        
        # إنشاء عناصر تبويب ميزات الشكل
        self._create_shape_features_tab(shape_frame)
        
        # إنشاء عناصر تبويب ميزات الشذوذ
        self._create_anomaly_features_tab(anomaly_frame)
        
        # إنشاء عناصر تبويب JSON
        self._create_json_tab(json_frame)
    
    def _create_color_features_tab(self, parent):
        """
        إنشاء تبويب ميزات اللون
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التمرير
        scroll_frame = ttk.Frame(parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء شريط التمرير
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إنشاء مربع النص
        self.color_features_text = tk.Text(scroll_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.color_features_text.pack(fill=tk.BOTH, expand=True)
        
        # ربط شريط التمرير بمربع النص
        scrollbar.config(command=self.color_features_text.yview)
        
        # تعطيل التحرير
        self.color_features_text.config(state=tk.DISABLED)
    
    def _create_texture_features_tab(self, parent):
        """
        إنشاء تبويب ميزات النسيج
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التمرير
        scroll_frame = ttk.Frame(parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء شريط التمرير
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إنشاء مربع النص
        self.texture_features_text = tk.Text(scroll_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.texture_features_text.pack(fill=tk.BOTH, expand=True)
        
        # ربط شريط التمرير بمربع النص
        scrollbar.config(command=self.texture_features_text.yview)
        
        # تعطيل التحرير
        self.texture_features_text.config(state=tk.DISABLED)
    
    def _create_shape_features_tab(self, parent):
        """
        إنشاء تبويب ميزات الشكل
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التمرير
        scroll_frame = ttk.Frame(parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء شريط التمرير
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إنشاء مربع النص
        self.shape_features_text = tk.Text(scroll_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.shape_features_text.pack(fill=tk.BOTH, expand=True)
        
        # ربط شريط التمرير بمربع النص
        scrollbar.config(command=self.shape_features_text.yview)
        
        # تعطيل التحرير
        self.shape_features_text.config(state=tk.DISABLED)
    
    def _create_anomaly_features_tab(self, parent):
        """
        إنشاء تبويب ميزات الشذوذ
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التمرير
        scroll_frame = ttk.Frame(parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء شريط التمرير
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إنشاء مربع النص
        self.anomaly_features_text = tk.Text(scroll_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.anomaly_features_text.pack(fill=tk.BOTH, expand=True)
        
        # ربط شريط التمرير بمربع النص
        scrollbar.config(command=self.anomaly_features_text.yview)
        
        # تعطيل التحرير
        self.anomaly_features_text.config(state=tk.DISABLED)
    
    def _create_json_tab(self, parent):
        """
        إنشاء تبويب JSON
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التمرير
        scroll_frame = ttk.Frame(parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء شريط التمرير
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إنشاء مربع النص
        self.json_text = tk.Text(scroll_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.json_text.pack(fill=tk.BOTH, expand=True)
        
        # ربط شريط التمرير بمربع النص
        scrollbar.config(command=self.json_text.yview)
        
        # تعطيل التحرير
        self.json_text.config(state=tk.DISABLED)
    
    def _create_comparison_tab(self, parent):
        """
        إنشاء تبويب المقارنة
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التمرير
        scroll_frame = ttk.Frame(parent)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء شريط التمرير
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إنشاء مربع النص
        self.comparison_text = tk.Text(scroll_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.comparison_text.pack(fill=tk.BOTH, expand=True)
        
        # ربط شريط التمرير بمربع النص
        scrollbar.config(command=self.comparison_text.yview)
        
        # تعطيل التحرير
        self.comparison_text.config(state=tk.DISABLED)
    
    def _create_visualization_tab(self, parent):
        """
        إنشاء تبويب التصور المرئي
        
        المعلمات:
            parent: العنصر الأب
        """
        # إنشاء إطار التصور المرئي
        self.visualization_canvas = tk.Canvas(parent, bg="white")
        self.visualization_canvas.pack(fill=tk.BOTH, expand=True)
    
    def _create_status_bar(self):
        """إنشاء شريط الحالة"""
        # إنشاء شريط الحالة
        self.status_var = tk.StringVar()
        self.status_var.set("جاهز")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _open_image(self):
        """فتح صورة"""
        # فتح مربع حوار اختيار الملف
        file_path = filedialog.askopenfilename(
            title="اختر صورة",
            filetypes=[
                ("ملفات الصور", "*.jpg *.jpeg *.png *.webp"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        # التحقق من اختيار ملف
        if not file_path:
            return
        
        # تحميل الصورة
        self._load_image(file_path)
    
    def _open_directory(self):
        """فتح مجلد"""
        # فتح مربع حوار اختيار المجلد
        dir_path = filedialog.askdirectory(title="اختر مجلد")
        
        # التحقق من اختيار مجلد
        if not dir_path:
            return
        
        # تحديث شريط الحالة
        self.status_var.set(f"تم اختيار المجلد: {dir_path}")
        
        # عرض مربع حوار التأكيد
        if messagebox.askyesno("تحليل المجلد", "هل تريد تحليل جميع الصور في المجلد؟"):
            self._analyze_directory(dir_path)
    
    def _load_image(self, image_path):
        """
        تحميل صورة
        
        المعلمات:
            image_path: مسار الصورة
        """
        try:
            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                raise ValueError(f"الصورة غير موجودة: {image_path}")
            
            # قراءة الصورة
            image = cv2.imread(image_path)
            
            if image is None:
                raise ValueError(f"فشل قراءة الصورة: {image_path}")
            
            # تحويل الصورة من BGR إلى RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # تحويل الصورة إلى كائن PhotoImage
            pil_image = Image.fromarray(image_rgb)
            
            # تحجيم الصورة لتناسب الإطار
            self._resize_and_display_image(pil_image, self.original_canvas)
            
            # تحديث المسار الحالي
            self.current_image_path = image_path
            
            # تحديث شريط الحالة
            self.status_var.set(f"تم تحميل الصورة: {os.path.basename(image_path)}")
            
            # مسح الصورة المقسمة والميزات
            self.segmented_canvas.delete("all")
            self._clear_features()
            
            # التحقق من وجود ملف ميزات
            features_path = os.path.join(
                self.config['primitive_output_dir'],
                f"{os.path.splitext(os.path.basename(image_path))[0]}_features.json"
            )
            
            if os.path.exists(features_path):
                # تحميل الميزات
                with open(features_path, 'r', encoding='utf-8') as f:
                    self.current_features = json.load(f)
                
                # عرض الميزات
                self._display_features(self.current_features)
                
                # التحقق من وجود صورة مقسمة
                segmented_path = os.path.join(
                    self.config['primitive_output_dir'],
                    f"{os.path.splitext(os.path.basename(image_path))[0]}_segmented.png"
                )
                
                if os.path.exists(segmented_path):
                    # تحميل الصورة المقسمة
                    segmented_image = cv2.imread(segmented_path)
                    segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
                    
                    # تحويل الصورة إلى كائن PhotoImage
                    pil_segmented = Image.fromarray(segmented_image_rgb)
                    
                    # تحجيم الصورة لتناسب الإطار
                    self._resize_and_display_image(pil_segmented, self.segmented_canvas)
                    
                    # تحديث الصورة المقسمة الحالية
                    self.current_segmented_image = segmented_image_rgb
            
            # التحقق من وجود ملف نتائج المقارنة
            comparison_path = os.path.join(
                self.config['comparison_output_dir'],
                f"{os.path.splitext(os.path.basename(image_path))[0]}_comparison.json"
            )
            
            if os.path.exists(comparison_path):
                # تحميل نتائج المقارنة
                with open(comparison_path, 'r', encoding='utf-8') as f:
                    self.current_comparison_result = json.load(f)
                
                # عرض نتائج المقارنة
                self._display_comparison(self.current_comparison_result)
                
                # التحقق من وجود تصور مرئي
                visualization_path = os.path.join(
                    self.config['visualization_output_dir'],
                    f"{os.path.splitext(os.path.basename(image_path))[0]}_comparison.png"
                )
                
                if os.path.exists(visualization_path):
                    # تحميل التصور المرئي
                    self._display_visualization(visualization_path)
            
        except Exception as e:
            # عرض رسالة الخطأ
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحميل الصورة: {str(e)}")
            logger.error(f"حدث خطأ أثناء تحميل الصورة {image_path}: {str(e)}")
    
    def _resize_and_display_image(self, pil_image, canvas):
        """
        تحجيم وعرض صورة على لوحة
        
        المعلمات:
            pil_image: كائن صورة PIL
            canvas: لوحة العرض
        """
        # الحصول على أبعاد اللوحة
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # التحقق من أبعاد اللوحة
        if canvas_width <= 1 or canvas_height <= 1:
            # تأجيل العرض حتى يتم تحديث أبعاد اللوحة
            canvas.after(100, lambda: self._resize_and_display_image(pil_image, canvas))
            return
        
        # الحصول على أبعاد الصورة
        image_width, image_height = pil_image.size
        
        # حساب نسبة التحجيم
        width_ratio = canvas_width / image_width
        height_ratio = canvas_height / image_height
        
        # اختيار النسبة الأصغر للحفاظ على نسبة العرض إلى الارتفاع
        scale_ratio = min(width_ratio, height_ratio)
        
        # حساب الأبعاد الجديدة
        new_width = int(image_width * scale_ratio)
        new_height = int(image_height * scale_ratio)
        
        # تحجيم الصورة
        resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        
        # تحويل الصورة إلى كائن PhotoImage
        photo_image = ImageTk.PhotoImage(resized_image)
        
        # مسح اللوحة
        canvas.delete("all")
        
        # حساب موضع الصورة
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        # عرض الصورة
        canvas.create_image(x, y, anchor=tk.NW, image=photo_image)
        
        # الاحتفاظ بمرجع للصورة
        canvas.image = photo_image
    
    def _analyze_current_image(self):
        """تحليل الصورة الحالية"""
        # التحقق من وجود صورة
        if self.current_image_path is None:
            messagebox.showwarning("تحذير", "يرجى فتح صورة أولاً")
            return
        
        # تحديث شريط الحالة
        self.status_var.set("جارٍ تحليل الصورة...")
        
        # تحديث تكوين المحلل
        self.primitive_analyzer.config['segment_method'] = self.config['segment_method']
        self.primitive_analyzer.config['segment_count'] = self.config['segment_count']
        
        # إنشاء مؤشر تقدم
        progress = ttk.Progressbar(self.root, mode='indeterminate')
        progress.pack(fill=tk.X, padx=10, pady=5)
        progress.start()
        
        # تحليل الصورة في مؤشر ترابط منفصل
        def analyze_thread():
            try:
                # تحليل الصورة
                result = self.primitive_analyzer.process_image(self.current_image_path)
                
                # التحقق من نجاح التحليل
                if 'error' in result:
                    raise ValueError(f"فشل التحليل: {result['error']}")
                
                # تحديث واجهة المستخدم في المؤشر الرئيسي
                self.root.after(0, lambda: self._update_analysis_result(result))
                
            except Exception as e:
                # عرض رسالة الخطأ
                self.root.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ أثناء التحليل: {str(e)}"))
                logger.error(f"حدث خطأ أثناء تحليل الصورة {self.current_image_path}: {str(e)}")
                
            finally:
                # إيقاف وإزالة مؤشر التقدم
                self.root.after(0, lambda: progress.stop())
                self.root.after(0, lambda: progress.destroy())
                
                # تحديث شريط الحالة
                self.root.after(0, lambda: self.status_var.set("اكتمل التحليل"))
        
        # بدء المؤشر الترابطي
        threading.Thread(target=analyze_thread).start()
    
    def _update_analysis_result(self, result):
        """
        تحديث نتائج التحليل
        
        المعلمات:
            result: نتائج التحليل
        """
        # تحديث الميزات الحالية
        self.current_features = result['features']
        
        # عرض الميزات
        self._display_features(self.current_features)
        
        # تحميل الصورة المقسمة إذا كانت متاحة
        if result['segmented_path']:
            # تحميل الصورة المقسمة
            segmented_image = cv2.imread(result['segmented_path'])
            segmented_image_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)
            
            # تحويل الصورة إلى كائن PhotoImage
            pil_segmented = Image.fromarray(segmented_image_rgb)
            
            # تحجيم الصورة لتناسب الإطار
            self._resize_and_display_image(pil_segmented, self.segmented_canvas)
            
            # تحديث الصورة المقسمة الحالية
            self.current_segmented_image = segmented_image_rgb
    
    def _compare_current_image(self):
        """مقارنة الصورة الحالية مع التحليل القياسي"""
        # التحقق من وجود صورة
        if self.current_image_path is None:
            messagebox.showwarning("تحذير", "يرجى فتح صورة أولاً")
            return
        
        # تحديث شريط الحالة
        self.status_var.set("جارٍ مقارنة الصورة...")
        
        # إنشاء مؤشر تقدم
        progress = ttk.Progressbar(self.root, mode='indeterminate')
        progress.pack(fill=tk.X, padx=10, pady=5)
        progress.start()
        
        # مقارنة الصورة في مؤشر ترابط منفصل
        def compare_thread():
            try:
                # مقارنة الصورة
                result = self.comparator.compare_image(self.current_image_path)
                
                # التحقق من نجاح المقارنة
                if 'error' in result.notes:
                    raise ValueError(f"فشل المقارنة: {result.notes['error']}")
                
                # تحديث واجهة المستخدم في المؤشر الرئيسي
                self.root.after(0, lambda: self._update_comparison_result(result))
                
            except Exception as e:
                # عرض رسالة الخطأ
                self.root.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ أثناء المقارنة: {str(e)}"))
                logger.error(f"حدث خطأ أثناء مقارنة الصورة {self.current_image_path}: {str(e)}")
                
            finally:
                # إيقاف وإزالة مؤشر التقدم
                self.root.after(0, lambda: progress.stop())
                self.root.after(0, lambda: progress.destroy())
                
                # تحديث شريط الحالة
                self.root.after(0, lambda: self.status_var.set("اكتملت المقارنة"))
        
        # بدء المؤشر الترابطي
        threading.Thread(target=compare_thread).start()
    
    def _update_comparison_result(self, result):
        """
        تحديث نتائج المقارنة
        
        المعلمات:
            result: نتائج المقارنة
        """
        # تحديث نتائج المقارنة الحالية
        self.current_comparison_result = result.to_dict()
        
        # عرض نتائج المقارنة
        self._display_comparison(self.current_comparison_result)
        
        # تحميل التصور المرئي إذا كان متاحًا
        visualization_path = os.path.join(
            self.config['visualization_output_dir'],
            f"{os.path.splitext(os.path.basename(self.current_image_path))[0]}_comparison.png"
        )
        
        if os.path.exists(visualization_path):
            # تحميل التصور المرئي
            self._display_visualization(visualization_path)
    
    def _analyze_directory(self, directory_path=None):
        """
        تحليل جميع الصور في مجلد
        
        المعلمات:
            directory_path: مسار المجلد (اختياري)
        """
        # إذا لم يتم تحديد مجلد، فتح مربع حوار اختيار المجلد
        if directory_path is None:
            directory_path = filedialog.askdirectory(title="اختر مجلد")
            
            # التحقق من اختيار مجلد
            if not directory_path:
                return
        
        # تحديث شريط الحالة
        self.status_var.set(f"جارٍ تحليل الصور في المجلد: {directory_path}")
        
        # تحديث تكوين المحلل
        self.primitive_analyzer.config['segment_method'] = self.config['segment_method']
        self.primitive_analyzer.config['segment_count'] = self.config['segment_count']
        
        # إنشاء مؤشر تقدم
        progress = ttk.Progressbar(self.root, mode='indeterminate')
        progress.pack(fill=tk.X, padx=10, pady=5)
        progress.start()
        
        # تحليل المجلد في مؤشر ترابط منفصل
        def analyze_directory_thread():
            try:
                # تحليل المجلد
                results = self.primitive_analyzer.process_directory(directory_path)
                
                # التحقق من نجاح التحليل
                if 'error' in results:
                    raise ValueError(f"فشل تحليل المجلد: {results['error']}")
                
                # تحديث واجهة المستخدم في المؤشر الرئيسي
                self.root.after(0, lambda: self._update_directory_analysis_result(results))
                
            except Exception as e:
                # عرض رسالة الخطأ
                self.root.after(0, lambda: messagebox.showerror("خطأ", f"حدث خطأ أثناء تحليل المجلد: {str(e)}"))
                logger.error(f"حدث خطأ أثناء تحليل المجلد {directory_path}: {str(e)}")
                
            finally:
                # إيقاف وإزالة مؤشر التقدم
                self.root.after(0, lambda: progress.stop())
                self.root.after(0, lambda: progress.destroy())
                
                # تحديث شريط الحالة
                self.root.after(0, lambda: self.status_var.set("اكتمل تحليل المجلد"))
        
        # بدء المؤشر الترابطي
        threading.Thread(target=analyze_directory_thread).start()
    
    def _update_directory_analysis_result(self, results):
        """
        تحديث نتائج تحليل المجلد
        
        المعلمات:
            results: نتائج التحليل
        """
        # عرض ملخص النتائج
        message = f"اكتمل تحليل المجلد:\n\n"
        message += f"إجمالي الصور: {results['total_images']}\n"
        message += f"الصور التي تمت معالجتها: {results['processed_images']}\n"
        message += f"الصور التي فشلت: {results['failed_images']}\n\n"
        
        # إذا كانت هناك صور فشلت، عرض قائمة بها
        if results['failed_images'] > 0:
            message += "الصور التي فشلت:\n"
            for result in results['results']:
                if 'error' in result:
                    message += f"- {os.path.basename(result['image_path'])}: {result['error']}\n"
        
        # عرض رسالة النجاح
        messagebox.showinfo("اكتمل تحليل المجلد", message)
        
        # إذا كانت هناك صور تمت معالجتها، سؤال المستخدم عما إذا كان يريد فتح أول صورة
        if results['processed_images'] > 0:
            # البحث عن أول صورة تمت معالجتها بنجاح
            for result in results['results']:
                if 'error' not in result:
                    # سؤال المستخدم
                    if messagebox.askyesno("فتح صورة", f"هل تريد فتح الصورة {os.path.basename(result['image_path'])}؟"):
                        # فتح الصورة
                        self._load_image(result['image_path'])
                    break
    
    def _display_features(self, features):
        """
        عرض ميزات الصورة
        
        المعلمات:
            features: ميزات الصورة
        """
        # عرض ميزات اللون
        self._display_color_features(features)
        
        # عرض ميزات النسيج
        self._display_texture_features(features)
        
        # عرض ميزات الشكل
        self._display_shape_features(features)
        
        # عرض ميزات الشذوذ
        self._display_anomaly_features(features)
        
        # عرض JSON
        self._display_json(features)
    
    def _display_color_features(self, features):
        """
        عرض ميزات اللون
        
        المعلمات:
            features: ميزات الصورة
        """
        # تمكين التحرير
        self.color_features_text.config(state=tk.NORMAL)
        
        # مسح النص
        self.color_features_text.delete(1.0, tk.END)
        
        # إضافة ميزات اللون
        self.color_features_text.insert(tk.END, "الألوان المهيمنة:\n")
        
        for i, color in enumerate(features.get('dominant_colors', [])):
            self.color_features_text.insert(tk.END, f"{i+1}. RGB: {color}\n")
        
        self.color_features_text.insert(tk.END, "\nالمدرج التكراري للألوان:\n")
        
        color_histogram = features.get('color_histogram', [])
        if color_histogram:
            # تقسيم المدرج التكراري إلى ثلاثة أجزاء (R, G, B)
            bins = len(color_histogram) // 3
            
            self.color_features_text.insert(tk.END, f"الأحمر (أول {bins} قيمة):\n")
            self.color_features_text.insert(tk.END, f"{color_histogram[:bins]}\n\n")
            
            self.color_features_text.insert(tk.END, f"الأخضر (القيم {bins} إلى {2*bins-1}):\n")
            self.color_features_text.insert(tk.END, f"{color_histogram[bins:2*bins]}\n\n")
            
            self.color_features_text.insert(tk.END, f"الأزرق (القيم {2*bins} إلى {3*bins-1}):\n")
            self.color_features_text.insert(tk.END, f"{color_histogram[2*bins:3*bins]}\n")
        
        self.color_features_text.insert(tk.END, "\nلحظات اللون:\n")
        
        color_moments = features.get('color_moments', [])
        if color_moments:
            # تقسيم لحظات اللون إلى ثلاثة أجزاء (R, G, B)
            moments_per_channel = len(color_moments) // 3
            
            self.color_features_text.insert(tk.END, "الأحمر:\n")
            self.color_features_text.insert(tk.END, f"المتوسط: {color_moments[0]:.4f}\n")
            self.color_features_text.insert(tk.END, f"الانحراف المعياري: {color_moments[1]:.4f}\n")
            self.color_features_text.insert(tk.END, f"الالتواء: {color_moments[2]:.4f}\n\n")
            
            self.color_features_text.insert(tk.END, "الأخضر:\n")
            self.color_features_text.insert(tk.END, f"المتوسط: {color_moments[3]:.4f}\n")
            self.color_features_text.insert(tk.END, f"الانحراف المعياري: {color_moments[4]:.4f}\n")
            self.color_features_text.insert(tk.END, f"الالتواء: {color_moments[5]:.4f}\n\n")
            
            self.color_features_text.insert(tk.END, "الأزرق:\n")
            self.color_features_text.insert(tk.END, f"المتوسط: {color_moments[6]:.4f}\n")
            self.color_features_text.insert(tk.END, f"الانحراف المعياري: {color_moments[7]:.4f}\n")
            self.color_features_text.insert(tk.END, f"الالتواء: {color_moments[8]:.4f}\n")
        
        # تعطيل التحرير
        self.color_features_text.config(state=tk.DISABLED)
    
    def _display_texture_features(self, features):
        """
        عرض ميزات النسيج
        
        المعلمات:
            features: ميزات الصورة
        """
        # تمكين التحرير
        self.texture_features_text.config(state=tk.NORMAL)
        
        # مسح النص
        self.texture_features_text.delete(1.0, tk.END)
        
        # إضافة ميزات النسيج
        self.texture_features_text.insert(tk.END, "ميزات هاراليك للنسيج:\n")
        
        texture_haralick = features.get('texture_haralick', [])
        if texture_haralick:
            for i, value in enumerate(texture_haralick):
                self.texture_features_text.insert(tk.END, f"{i+1}. {value:.4f}\n")
        
        self.texture_features_text.insert(tk.END, "\nميزات أنماط ثنائية محلية (LBP):\n")
        
        texture_lbp = features.get('texture_lbp', [])
        if texture_lbp:
            for i, value in enumerate(texture_lbp):
                self.texture_features_text.insert(tk.END, f"{i+1}. {value:.4f}\n")
        
        self.texture_features_text.insert(tk.END, "\nميزات مصفوفة التواجد المكاني للمستوى الرمادي (GLCM):\n")
        
        texture_glcm = features.get('texture_glcm', {})
        if texture_glcm:
            for key, value in texture_glcm.items():
                self.texture_features_text.insert(tk.END, f"{key}: {value:.4f}\n")
        
        # تعطيل التحرير
        self.texture_features_text.config(state=tk.DISABLED)
    
    def _display_shape_features(self, features):
        """
        عرض ميزات الشكل
        
        المعلمات:
            features: ميزات الصورة
        """
        # تمكين التحرير
        self.shape_features_text.config(state=tk.NORMAL)
        
        # مسح النص
        self.shape_features_text.delete(1.0, tk.END)
        
        # إضافة ميزات الشكل
        self.shape_features_text.insert(tk.END, f"المساحة: {features.get('shape_area', 0):.2f}\n")
        self.shape_features_text.insert(tk.END, f"المحيط: {features.get('shape_perimeter', 0):.2f}\n")
        
        self.shape_features_text.insert(tk.END, "\nلحظات الشكل:\n")
        
        shape_moments = features.get('shape_moments', [])
        if shape_moments:
            for i, moment in enumerate(shape_moments):
                self.shape_features_text.insert(tk.END, f"{i+1}. {moment:.4f}\n")
        
        self.shape_features_text.insert(tk.END, "\nلحظات هو للشكل:\n")
        
        shape_hu_moments = features.get('shape_hu_moments', [])
        if shape_hu_moments:
            for i, moment in enumerate(shape_hu_moments):
                self.shape_features_text.insert(tk.END, f"{i+1}. {moment:.4f}\n")
        
        self.shape_features_text.insert(tk.END, "\nمحيطات الشكل:\n")
        
        shape_contours = features.get('shape_contours', [])
        if shape_contours:
            self.shape_features_text.insert(tk.END, f"عدد المحيطات: {len(shape_contours)}\n")
            
            for i, contour in enumerate(shape_contours[:5]):  # عرض أول 5 محيطات فقط
                self.shape_features_text.insert(tk.END, f"محيط {i+1}: {len(contour)} نقطة\n")
            
            if len(shape_contours) > 5:
                self.shape_features_text.insert(tk.END, f"... و{len(shape_contours) - 5} محيطات أخرى\n")
        
        # تعطيل التحرير
        self.shape_features_text.config(state=tk.DISABLED)
    
    def _display_anomaly_features(self, features):
        """
        عرض ميزات الشذوذ
        
        المعلمات:
            features: ميزات الصورة
        """
        # تمكين التحرير
        self.anomaly_features_text.config(state=tk.NORMAL)
        
        # مسح النص
        self.anomaly_features_text.delete(1.0, tk.END)
        
        # إضافة ميزات الشذوذ
        self.anomaly_features_text.insert(tk.END, f"درجة الشذوذ: {features.get('anomaly_score', 0):.4f}\n\n")
        
        self.anomaly_features_text.insert(tk.END, "مناطق الشذوذ:\n")
        
        anomaly_regions = features.get('anomaly_regions', [])
        if anomaly_regions:
            for i, region in enumerate(anomaly_regions):
                self.anomaly_features_text.insert(tk.END, f"منطقة {i+1}:\n")
                self.anomaly_features_text.insert(tk.END, f"الموقع: ({region.get('x', 0)}, {region.get('y', 0)})\n")
                self.anomaly_features_text.insert(tk.END, f"الأبعاد: {region.get('width', 0)} × {region.get('height', 0)}\n")
                self.anomaly_features_text.insert(tk.END, f"المساحة: {region.get('area', 0):.2f}\n")
                self.anomaly_features_text.insert(tk.END, f"المحيط: {region.get('perimeter', 0):.2f}\n")
                self.anomaly_features_text.insert(tk.END, f"نسبة العرض إلى الارتفاع: {region.get('aspect_ratio', 0):.2f}\n")
                self.anomaly_features_text.insert(tk.END, f"الدائرية: {region.get('circularity', 0):.4f}\n")
                self.anomaly_features_text.insert(tk.END, f"درجة الشذوذ: {region.get('anomaly_score', 0):.4f}\n\n")
        else:
            self.anomaly_features_text.insert(tk.END, "لا توجد مناطق شذوذ\n")
        
        # تعطيل التحرير
        self.anomaly_features_text.config(state=tk.DISABLED)
    
    def _display_json(self, features):
        """
        عرض JSON
        
        المعلمات:
            features: ميزات الصورة
        """
        # تمكين التحرير
        self.json_text.config(state=tk.NORMAL)
        
        # مسح النص
        self.json_text.delete(1.0, tk.END)
        
        # إضافة JSON
        json_str = json.dumps(features, ensure_ascii=False, indent=2)
        self.json_text.insert(tk.END, json_str)
        
        # تعطيل التحرير
        self.json_text.config(state=tk.DISABLED)
    
    def _display_comparison(self, comparison_result):
        """
        عرض نتائج المقارنة
        
        المعلمات:
            comparison_result: نتائج المقارنة
        """
        # تمكين التحرير
        self.comparison_text.config(state=tk.NORMAL)
        
        # مسح النص
        self.comparison_text.delete(1.0, tk.END)
        
        # إضافة نتائج المقارنة
        self.comparison_text.insert(tk.END, "نتائج المقارنة بين التحليل الأولي والتحليل القياسي:\n\n")
        
        self.comparison_text.insert(tk.END, "درجات التشابه:\n")
        self.comparison_text.insert(tk.END, f"تشابه اللون: {comparison_result.get('color_similarity', 0):.4f}\n")
        self.comparison_text.insert(tk.END, f"تشابه النسيج: {comparison_result.get('texture_similarity', 0):.4f}\n")
        self.comparison_text.insert(tk.END, f"تشابه الشكل: {comparison_result.get('shape_similarity', 0):.4f}\n")
        self.comparison_text.insert(tk.END, f"تشابه الشذوذ: {comparison_result.get('anomaly_similarity', 0):.4f}\n")
        self.comparison_text.insert(tk.END, f"التشابه الإجمالي: {comparison_result.get('overall_similarity', 0):.4f}\n\n")
        
        self.comparison_text.insert(tk.END, "إحصائيات الأداء:\n")
        self.comparison_text.insert(tk.END, f"وقت معالجة التحليل الأولي: {comparison_result.get('primitive_processing_time', 0):.4f} ثانية\n")
        self.comparison_text.insert(tk.END, f"وقت معالجة التحليل القياسي: {comparison_result.get('standard_processing_time', 0):.4f} ثانية\n")
        self.comparison_text.insert(tk.END, f"استخدام الذاكرة للتحليل الأولي: {comparison_result.get('primitive_memory_usage', 0):.2f} ميجابايت\n")
        self.comparison_text.insert(tk.END, f"استخدام الذاكرة للتحليل القياسي: {comparison_result.get('standard_memory_usage', 0):.2f} ميجابايت\n\n")
        
        # إضافة ملاحظات
        notes = comparison_result.get('notes', {})
        if notes:
            self.comparison_text.insert(tk.END, "ملاحظات:\n")
            for key, value in notes.items():
                self.comparison_text.insert(tk.END, f"{key}: {value}\n")
        
        # تعطيل التحرير
        self.comparison_text.config(state=tk.DISABLED)
        
        # تبديل إلى تبويب المقارنة
        self.notebook.select(1)
    
    def _display_visualization(self, visualization_path):
        """
        عرض التصور المرئي
        
        المعلمات:
            visualization_path: مسار ملف التصور المرئي
        """
        try:
            # تحميل الصورة
            pil_image = Image.open(visualization_path)
            
            # تحجيم الصورة لتناسب الإطار
            self._resize_and_display_image(pil_image, self.visualization_canvas)
            
            # تبديل إلى تبويب التصور المرئي
            self.notebook.select(2)
            
        except Exception as e:
            # عرض رسالة الخطأ
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحميل التصور المرئي: {str(e)}")
            logger.error(f"حدث خطأ أثناء تحميل التصور المرئي {visualization_path}: {str(e)}")
    
    def _clear_features(self):
        """مسح الميزات"""
        # مسح الميزات الحالية
        self.current_features = None
        
        # مسح نتائج المقارنة الحالية
        self.current_comparison_result = None
        
        # مسح النصوص
        for text_widget in [
            self.color_features_text,
            self.texture_features_text,
            self.shape_features_text,
            self.anomaly_features_text,
            self.json_text,
            self.comparison_text
        ]:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.config(state=tk.DISABLED)
        
        # مسح التصور المرئي
        self.visualization_canvas.delete("all")
    
    def _update_segment_method(self, event):
        """
        تحديث طريقة التقسيم
        
        المعلمات:
            event: حدث التغيير
        """
        # الحصول على القيمة الجديدة
        method = self.segment_method_var.get()
        
        # تحديث التكوين
        self.config['segment_method'] = method
        
        # تحديث شريط الحالة
        self.status_var.set(f"تم تغيير طريقة التقسيم إلى: {method}")
    
    def _update_segment_count(self, event):
        """
        تحديث عدد الأجزاء
        
        المعلمات:
            event: حدث التغيير
        """
        try:
            # الحصول على القيمة الجديدة
            count = int(self.segment_count_var.get())
            
            # التحقق من صحة القيمة
            if count < 2:
                raise ValueError("يجب أن يكون عدد الأجزاء 2 على الأقل")
            
            # تحديث التكوين
            self.config['segment_count'] = count
            
            # تحديث شريط الحالة
            self.status_var.set(f"تم تغيير عدد الأجزاء إلى: {count}")
            
        except ValueError as e:
            # عرض رسالة الخطأ
            messagebox.showerror("خطأ", f"قيمة غير صالحة: {str(e)}")
            
            # إعادة تعيين القيمة
            self.segment_count_var.set(str(self.config['segment_count']))
    
    def _save_results(self):
        """حفظ النتائج"""
        # التحقق من وجود ميزات
        if self.current_features is None:
            messagebox.showwarning("تحذير", "لا توجد نتائج للحفظ")
            return
        
        # فتح مربع حوار اختيار المجلد
        dir_path = filedialog.askdirectory(title="اختر مجلد الحفظ")
        
        # التحقق من اختيار مجلد
        if not dir_path:
            return
        
        try:
            # إنشاء اسم الملف
            if self.current_image_path:
                base_name = os.path.splitext(os.path.basename(self.current_image_path))[0]
            else:
                base_name = "features"
            
            # حفظ الميزات
            features_path = os.path.join(dir_path, f"{base_name}_features.json")
            with open(features_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_features, f, ensure_ascii=False, indent=2)
            
            # حفظ نتائج المقارنة إذا كانت متاحة
            comparison_saved = False
            if self.current_comparison_result:
                comparison_path = os.path.join(dir_path, f"{base_name}_comparison.json")
                with open(comparison_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_comparison_result, f, ensure_ascii=False, indent=2)
                comparison_saved = True
            
            # حفظ الصورة المقسمة إذا كانت متاحة
            segmented_saved = False
            if self.current_segmented_image is not None:
                segmented_path = os.path.join(dir_path, f"{base_name}_segmented.png")
                cv2.imwrite(segmented_path, cv2.cvtColor(self.current_segmented_image, cv2.COLOR_RGB2BGR))
                segmented_saved = True
            
            # عرض رسالة النجاح
            message = f"تم حفظ الميزات: {features_path}"
            if comparison_saved:
                message += f"\nتم حفظ نتائج المقارنة: {comparison_path}"
            if segmented_saved:
                message += f"\nتم حفظ الصورة المقسمة: {segmented_path}"
            
            messagebox.showinfo("تم الحفظ", message)
            
            # تحديث شريط الحالة
            self.status_var.set("تم حفظ النتائج")
            
        except Exception as e:
            # عرض رسالة الخطأ
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ النتائج: {str(e)}")
            logger.error(f"حدث خطأ أثناء حفظ النتائج: {str(e)}")
    
    def _show_settings(self):
        """عرض إعدادات التحليل الأولي"""
        # إنشاء نافذة الإعدادات
        settings_window = tk.Toplevel(self.root)
        settings_window.title("إعدادات التحليل الأولي")
        settings_window.geometry("500x400")
        settings_window.minsize(400, 300)
        settings_window.grab_set()  # جعل النافذة مشغولة
        
        # إنشاء إطار الإعدادات
        settings_frame = ttk.Frame(settings_window, padding=10)
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # إعدادات طريقة التقسيم
        ttk.Label(settings_frame, text="طريقة التقسيم:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        segment_method_var = tk.StringVar(value=self.config['segment_method'])
        segment_method_combo = ttk.Combobox(settings_frame, textvariable=segment_method_var, width=15)
        segment_method_combo['values'] = ('kmeans', 'watershed', 'grabcut')
        segment_method_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # إعدادات عدد الأجزاء
        ttk.Label(settings_frame, text="عدد الأجزاء:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        segment_count_var = tk.StringVar(value=str(self.config['segment_count']))
        segment_count_entry = ttk.Entry(settings_frame, textvariable=segment_count_var, width=5)
        segment_count_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # إعدادات حفظ الصور المقسمة
        ttk.Label(settings_frame, text="حفظ الصور المقسمة:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        save_segmented_var = tk.BooleanVar(value=self.config['save_segmented_images'])
        save_segmented_check = ttk.Checkbutton(settings_frame, variable=save_segmented_var)
        save_segmented_check.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # إعدادات مجلدات المخرجات
        ttk.Label(settings_frame, text="مجلد ميزات التحليل الأولي:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        primitive_output_var = tk.StringVar(value=self.config['primitive_output_dir'])
        primitive_output_entry = ttk.Entry(settings_frame, textvariable=primitive_output_var, width=30)
        primitive_output_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(settings_frame, text="...", width=3, command=lambda: self._browse_directory(primitive_output_var)).grid(row=3, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(settings_frame, text="مجلد ميزات التحليل القياسي:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        standard_output_var = tk.StringVar(value=self.config['standard_output_dir'])
        standard_output_entry = ttk.Entry(settings_frame, textvariable=standard_output_var, width=30)
        standard_output_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(settings_frame, text="...", width=3, command=lambda: self._browse_directory(standard_output_var)).grid(row=4, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(settings_frame, text="مجلد نتائج المقارنة:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        comparison_output_var = tk.StringVar(value=self.config['comparison_output_dir'])
        comparison_output_entry = ttk.Entry(settings_frame, textvariable=comparison_output_var, width=30)
        comparison_output_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(settings_frame, text="...", width=3, command=lambda: self._browse_directory(comparison_output_var)).grid(row=5, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(settings_frame, text="مجلد التصورات المرئية:").grid(row=6, column=0, sticky=tk.W, pady=5)
        
        visualization_output_var = tk.StringVar(value=self.config['visualization_output_dir'])
        visualization_output_entry = ttk.Entry(settings_frame, textvariable=visualization_output_var, width=30)
        visualization_output_entry.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(settings_frame, text="...", width=3, command=lambda: self._browse_directory(visualization_output_var)).grid(row=6, column=2, sticky=tk.W, pady=5)
        
        # إنشاء إطار الأزرار
        buttons_frame = ttk.Frame(settings_window)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # زر حفظ
        def save_settings():
            try:
                # التحقق من صحة القيم
                segment_count = int(segment_count_var.get())
                if segment_count < 2:
                    raise ValueError("يجب أن يكون عدد الأجزاء 2 على الأقل")
                
                # تحديث التكوين
                self.config['segment_method'] = segment_method_var.get()
                self.config['segment_count'] = segment_count
                self.config['save_segmented_images'] = save_segmented_var.get()
                self.config['primitive_output_dir'] = primitive_output_var.get()
                self.config['standard_output_dir'] = standard_output_var.get()
                self.config['comparison_output_dir'] = comparison_output_var.get()
                self.config['visualization_output_dir'] = visualization_output_var.get()
                
                # إنشاء المجلدات إذا لم تكن موجودة
                for dir_path in [
                    self.config['primitive_output_dir'],
                    self.config['standard_output_dir'],
                    self.config['comparison_output_dir'],
                    self.config['visualization_output_dir']
                ]:
                    os.makedirs(dir_path, exist_ok=True)
                
                # تحديث تكوين المحلل
                self.primitive_analyzer.config['segment_method'] = self.config['segment_method']
                self.primitive_analyzer.config['segment_count'] = self.config['segment_count']
                self.primitive_analyzer.config['save_segmented_images'] = self.config['save_segmented_images']
                self.primitive_analyzer.config['output_dir'] = self.config['primitive_output_dir']
                
                # تحديث تكوين المقارن
                self.comparator.config['primitive_output_dir'] = self.config['primitive_output_dir']
                self.comparator.config['standard_output_dir'] = self.config['standard_output_dir']
                self.comparator.config['comparison_output_dir'] = self.config['comparison_output_dir']
                self.comparator.config['visualization_output_dir'] = self.config['visualization_output_dir']
                
                # تحديث واجهة المستخدم
                self.segment_method_var.set(self.config['segment_method'])
                self.segment_count_var.set(str(self.config['segment_count']))
                
                # تحديث شريط الحالة
                self.status_var.set("تم حفظ الإعدادات")
                
                # إغلاق النافذة
                settings_window.destroy()
                
            except ValueError as e:
                # عرض رسالة الخطأ
                messagebox.showerror("خطأ", f"قيمة غير صالحة: {str(e)}")
        
        save_button = ttk.Button(buttons_frame, text="حفظ", command=save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # زر إلغاء
        cancel_button = ttk.Button(buttons_frame, text="إلغاء", command=settings_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _browse_directory(self, var):
        """
        اختيار مجلد
        
        المعلمات:
            var: متغير لتخزين المسار
        """
        # فتح مربع حوار اختيار المجلد
        dir_path = filedialog.askdirectory(title="اختر مجلد")
        
        # التحقق من اختيار مجلد
        if dir_path:
            var.set(dir_path)
    
    def _show_about(self):
        """عرض معلومات حول البرنامج"""
        # إنشاء نافذة المعلومات
        about_window = tk.Toplevel(self.root)
        about_window.title("حول البرنامج")
        about_window.geometry("400x300")
        about_window.minsize(300, 200)
        about_window.grab_set()  # جعل النافذة مشغولة
        
        # إنشاء إطار المعلومات
        about_frame = ttk.Frame(about_window, padding=10)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        # عنوان البرنامج
        title_label = ttk.Label(about_frame, text="نظام التحليل الأولي للصور الزراعية", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # وصف البرنامج
        description_text = """
        نظام متكامل لتحليل الصور الزراعية باستخدام تقنيات التحليل الأولي.
        
        يقوم النظام بتحويل الصور إلى تمثيلات مبسطة تتضمن ميزات اللون والنسيج والشكل والشذوذ.
        
        يمكن مقارنة نتائج التحليل الأولي مع نتائج التحليل القياسي لتقييم أداء النظام.
        """
        
        description_label = ttk.Label(about_frame, text=description_text, wraplength=350, justify=tk.CENTER)
        description_label.pack(pady=10)
        
        # معلومات الإصدار
        version_label = ttk.Label(about_frame, text="الإصدار: 1.0.0")
        version_label.pack()
        
        # زر إغلاق
        close_button = ttk.Button(about_frame, text="إغلاق", command=about_window.destroy)
        close_button.pack(pady=10)


# نموذج استخدام
if __name__ == "__main__":
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    
    # إنشاء واجهة المستخدم
    app = PrimitiveAnalysisUI(root)
    
    # بدء حلقة الأحداث
    root.mainloop()
