#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة المستخدم لاستعراض وتحرير مجموعات الصور
"""

import os
import sys
import json
import shutil
import logging
import datetime
from pathlib import Path
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QPushButton, QFileDialog, QListWidget,
                            QListWidgetItem, QComboBox, QProgressBar, QMessageBox,
                            QSplitter, QFrame, QTextEdit, QCheckBox, QSpinBox, QLineEdit,
                            QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize

# استيراد المكونات الأخرى
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_crawler.crawler import PlantDiseaseImageCrawler
from image_crawler.classifier import PlantDiseaseImageClassifier
from image_crawler.filter import PlantDiseaseImageFilter
from image_crawler.encoder import PlantDiseaseImageEncoder
from image_crawler.archiver import PlantDiseaseImageArchiver

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WorkerThread(QThread):
    """خيط عمل لتنفيذ المهام في الخلفية"""
    
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str)
    task_completed = pyqtSignal(dict)
    
    def __init__(self, task_type, params=None):
        """
        تهيئة خيط العمل
        
        المعلمات:
            task_type (str): نوع المهمة
            params (dict): معلمات المهمة
        """
        super().__init__()
        self.task_type = task_type
        self.params = params or {}
    
    def run(self):
        """تنفيذ المهمة"""
        try:
            if self.task_type == 'crawl':
                self._run_crawler()
            elif self.task_type == 'classify':
                self._run_classifier()
            elif self.task_type == 'filter':
                self._run_filter()
            elif self.task_type == 'encode':
                self._run_encoder()
            elif self.task_type == 'archive':
                self._run_archiver()
            else:
                self.update_status.emit(f"نوع مهمة غير معروف: {self.task_type}")
        except Exception as e:
            self.update_status.emit(f"حدث خطأ أثناء تنفيذ المهمة: {str(e)}")
    
    def _run_crawler(self):
        """تنفيذ مهمة الزحف"""
        self.update_status.emit("بدء عملية زحف الويب لجمع الصور...")
        
        # إنشاء كائن الزاحف
        crawler = PlantDiseaseImageCrawler(self.params.get('config'))
        
        # الحصول على قائمة المصادر
        sources = self.params.get('sources', [])
        
        # زحف المصادر
        total_sources = len(sources)
        for i, source in enumerate(sources):
            self.update_status.emit(f"جاري زحف المصدر {i+1}/{total_sources}: {source.get('url')}")
            crawler.crawl_website(
                source.get('url'),
                source.get('category', 'unclassified'),
                source.get('max_depth', 2)
            )
            progress = int((i + 1) / total_sources * 100)
            self.update_progress.emit(progress)
        
        # إكمال المهمة
        stats = crawler.crawl_multiple_sources(sources)
        self.update_status.emit(f"اكتمل زحف الويب: تم تنزيل {stats['total_images']} صورة")
        self.task_completed.emit(stats)
    
    def _run_classifier(self):
        """تنفيذ مهمة التصنيف"""
        self.update_status.emit("بدء عملية تصنيف الصور...")
        
        # إنشاء كائن المصنف
        classifier = PlantDiseaseImageClassifier(self.params.get('config'))
        
        # تصنيف الصور
        input_dir = self.params.get('input_dir')
        stats = classifier.classify_directory(input_dir)
        
        # إكمال المهمة
        self.update_status.emit(f"اكتمل تصنيف الصور: تم تصنيف {stats['classified_images']} صورة من أصل {stats['total_images']}")
        self.update_progress.emit(100)
        self.task_completed.emit(stats)
    
    def _run_filter(self):
        """تنفيذ مهمة التنقية"""
        self.update_status.emit("بدء عملية تنقية الصور...")
        
        # إنشاء كائن المرشح
        image_filter = PlantDiseaseImageFilter(self.params.get('config'))
        
        # تنقية الصور
        stats = image_filter.filter_all_categories()
        
        # إكمال المهمة
        self.update_status.emit(f"اكتمل تنقية الصور: تم قبول {stats['accepted_images']} صورة ورفض {stats['rejected_images']} صورة من أصل {stats['total_images']}")
        self.update_progress.emit(100)
        self.task_completed.emit(stats)
    
    def _run_encoder(self):
        """تنفيذ مهمة الترميز"""
        self.update_status.emit("بدء عملية ترميز الصور...")
        
        # إنشاء كائن المرمز
        encoder = PlantDiseaseImageEncoder(self.params.get('config'))
        
        # ترميز الصور
        stats = encoder.encode_all_categories()
        
        # إكمال المهمة
        self.update_status.emit(f"اكتمل ترميز الصور: تم ترميز {stats['encoded_images']} صورة من أصل {stats['total_images']}")
        self.update_progress.emit(100)
        self.task_completed.emit(stats)
    
    def _run_archiver(self):
        """تنفيذ مهمة الأرشفة"""
        self.update_status.emit("بدء عملية أرشفة الصور...")
        
        # إنشاء كائن المؤرشف
        archiver = PlantDiseaseImageArchiver(self.params.get('config'))
        
        # أرشفة الصور
        delete_originals = self.params.get('delete_originals', False)
        stats = archiver.archive_all_categories(delete_originals)
        
        # إكمال المهمة
        self.update_status.emit(f"اكتمل أرشفة الصور: تم أرشفة {stats['archived_images']} صورة في {stats['total_archives']} أرشيف")
        self.update_progress.emit(100)
        self.task_completed.emit(stats)

class ImageGalleryWidget(QWidget):
    """واجهة معرض الصور"""
    
    def __init__(self, parent=None):
        """
        تهيئة واجهة معرض الصور
        
        المعلمات:
            parent (QWidget): الواجهة الأم
        """
        super().__init__(parent)
        
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين
        self.config = {
            'images_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'categories': ['vegetables', 'fruits', 'crops', 'unclassified', 'rejected']
        }
        
        # إنشاء واجهة المستخدم
        self._init_ui()
        
        # تحديث قائمة الفئات
        self._update_category_list()
    
    def _init_ui(self):
        """إنشاء واجهة المستخدم"""
        # التخطيط الرئيسي
        main_layout = QHBoxLayout()
        
        # الجزء الأيسر: قائمة الفئات والصور
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # قائمة الفئات
        category_label = QLabel("الفئات:")
        self.category_list = QListWidget()
        self.category_list.currentItemChanged.connect(self._on_category_changed)
        
        # قائمة الصور
        image_label = QLabel("الصور:")
        self.image_list = QListWidget()
        self.image_list.currentItemChanged.connect(self._on_image_changed)
        self.image_list.setIconSize(QSize(64, 64))
        
        # إضافة العناصر إلى التخطيط الأيسر
        left_layout.addWidget(category_label)
        left_layout.addWidget(self.category_list)
        left_layout.addWidget(image_label)
        left_layout.addWidget(self.image_list)
        left_panel.setLayout(left_layout)
        
        # الجزء الأيمن: عرض الصورة والمعلومات
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # عرض الصورة
        self.image_view = QLabel()
        self.image_view.setAlignment(Qt.AlignCenter)
        self.image_view.setMinimumSize(400, 400)
        self.image_view.setFrameShape(QFrame.Box)
        
        # معلومات الصورة
        info_label = QLabel("معلومات الصورة:")
        self.image_info = QTextEdit()
        self.image_info.setReadOnly(True)
        
        # أزرار الإجراءات
        actions_layout = QHBoxLayout()
        self.delete_button = QPushButton("حذف")
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.move_button = QPushButton("نقل إلى فئة أخرى")
        self.move_button.clicked.connect(self._on_move_clicked)
        self.export_button = QPushButton("تصدير")
        self.export_button.clicked.connect(self._on_export_clicked)
        
        actions_layout.addWidget(self.delete_button)
        actions_layout.addWidget(self.move_button)
        actions_layout.addWidget(self.export_button)
        
        # إضافة العناصر إلى التخطيط الأيمن
        right_layout.addWidget(self.image_view)
        right_layout.addWidget(info_label)
        right_layout.addWidget(self.image_info)
        right_layout.addLayout(actions_layout)
        right_panel.setLayout(right_layout)
        
        # إضافة اللوحات إلى التخطيط الرئيسي
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([200, 600])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def _update_category_list(self):
        """تحديث قائمة الفئات"""
        self.category_list.clear()
        
        # إضافة الفئات
        for category in self.config['categories']:
            category_dir = os.path.join(self.config['images_dir'], category)
            
            # التحقق من وجود المجلد
            if os.path.exists(category_dir) and os.path.isdir(category_dir):
                # الحصول على عدد الصور في الفئة
                image_count = len([
                    f for f in os.listdir(category_dir)
                    if os.path.isfile(os.path.join(category_dir, f)) and
                    os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg', '.png', '.webp']
                ])
                
                # إضافة الفئة إلى القائمة
                item = QListWidgetItem(f"{category} ({image_count})")
                item.setData(Qt.UserRole, category)
                self.category_list.addItem(item)
    
    def _update_image_list(self, category):
        """
        تحديث قائمة الصور
        
        المعلمات:
            category (str): الفئة
        """
        self.image_list.clear()
        
        # الحصول على مسار مجلد الفئة
        category_dir = os.path.join(self.config['images_dir'], category)
        
        # التحقق من وجود المجلد
        if not os.path.exists(category_dir) or not os.path.isdir(category_dir):
            return
        
        # الحصول على قائمة ملفات الصور
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        image_files = [
            f for f in os.listdir(category_dir)
            if os.path.isfile(os.path.join(category_dir, f)) and
            os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # إضافة الصور إلى القائمة
        for image_file in sorted(image_files):
            image_path = os.path.join(category_dir, image_file)
            
            # إنشاء صورة مصغرة
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # إضافة الصورة إلى القائمة
                item = QListWidgetItem(QIcon(pixmap), image_file)
                item.setData(Qt.UserRole, image_path)
                self.image_list.addItem(item)
    
    def _display_image(self, image_path):
        """
        عرض الصورة
        
        المعلمات:
            image_path (str): مسار الصورة
        """
        # التحقق من وجود الملف
        if not os.path.exists(image_path) or not os.path.isfile(image_path):
            self.image_view.clear()
            self.image_info.clear()
            return
        
        # عرض الصورة
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # تغيير حجم الصورة للعرض
            pixmap = pixmap.scaled(
                self.image_view.width(), self.image_view.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_view.setPixmap(pixmap)
            
            # عرض معلومات الصورة
            file_info = os.stat(image_path)
            file_size = file_info.st_size
            file_modified = datetime.datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # الحصول على أبعاد الصورة
            image = QImage(image_path)
            width = image.width()
            height = image.height()
            
            # عرض المعلومات
            info_text = f"اسم الملف: {os.path.basename(image_path)}\n"
            info_text += f"المسار: {image_path}\n"
            info_text += f"الحجم: {self._format_size(file_size)}\n"
            info_text += f"الأبعاد: {width}×{height}\n"
            info_text += f"تاريخ التعديل: {file_modified}\n"
            
            # البحث عن البيانات الوصفية
            metadata_file = os.path.join(self.config['images_dir'], 'metadata.csv')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if image_path in line:
                            parts = line.strip().split(',')
                            if len(parts) >= 7:
                                info_text += f"\nالبيانات الوصفية:\n"
                                info_text += f"الاسم الأصلي: {parts[1]}\n"
                                info_text += f"الفئة: {parts[2]}\n"
                                info_text += f"نوع المرض: {parts[3]}\n"
                                info_text += f"نوع النبات: {parts[4]}\n"
                                info_text += f"تاريخ الإضافة: {parts[5]}\n"
                                info_text += f"الهاش: {parts[6]}\n"
                            break
            
            self.image_info.setText(info_text)
        else:
            self.image_view.clear()
            self.image_info.setText(f"لا يمكن عرض الصورة: {image_path}")
    
    def _format_size(self, size_bytes):
        """
        تنسيق حجم الملف
        
        المعلمات:
            size_bytes (int): حجم الملف بالبايت
            
        العوائد:
            str: حجم الملف المنسق
        """
        if size_bytes < 1024:
            return f"{size_bytes} بايت"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} كيلوبايت"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} ميجابايت"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} جيجابايت"
    
    def _on_category_changed(self, current, previous):
        """
        معالجة تغيير الفئة
        
        المعلمات:
            current (QListWidgetItem): العنصر الحالي
            previous (QListWidgetItem): العنصر السابق
        """
        if current:
            category = current.data(Qt.UserRole)
            self._update_image_list(category)
    
    def _on_image_changed(self, current, previous):
        """
        معالجة تغيير الصورة
        
        المعلمات:
            current (QListWidgetItem): العنصر الحالي
            previous (QListWidgetItem): العنصر السابق
        """
        if current:
            image_path = current.data(Qt.UserRole)
            self._display_image(image_path)
    
    def _on_delete_clicked(self):
        """معالجة النقر على زر الحذف"""
        # الحصول على الصورة الحالية
        current_item = self.image_list.currentItem()
        if not current_item:
            return
        
        image_path = current_item.data(Qt.UserRole)
        
        # تأكيد الحذف
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف الصورة؟\n{os.path.basename(image_path)}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # حذف الصورة
                os.remove(image_path)
                
                # تحديث القائمة
                self.image_list.takeItem(self.image_list.row(current_item))
                
                # تحديث قائمة الفئات
                self._update_category_list()
                
                # مسح عرض الصورة
                self.image_view.clear()
                self.image_info.clear()
                
                QMessageBox.information(self, "تم الحذف", "تم حذف الصورة بنجاح.")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حذف الصورة:\n{str(e)}")
    
    def _on_move_clicked(self):
        """معالجة النقر على زر النقل"""
        # الحصول على الصورة الحالية
        current_item = self.image_list.currentItem()
        if not current_item:
            return
        
        image_path = current_item.data(Qt.UserRole)
        
        # الحصول على الفئة الحالية
        current_category_item = self.category_list.currentItem()
        if not current_category_item:
            return
        
        current_category = current_category_item.data(Qt.UserRole)
        
        # إنشاء قائمة الفئات المتاحة
        available_categories = [
            cat for cat in self.config['categories']
            if cat != current_category
        ]
        
        if not available_categories:
            QMessageBox.information(self, "لا توجد فئات", "لا توجد فئات أخرى متاحة للنقل إليها.")
            return
        
        # إنشاء مربع حوار للاختيار
        from PyQt5.QtWidgets import QInputDialog
        new_category, ok = QInputDialog.getItem(
            self, "اختر الفئة", "اختر الفئة الجديدة:",
            available_categories, 0, False
        )
        
        if ok and new_category:
            try:
                # إنشاء مسار الملف الجديد
                new_dir = os.path.join(self.config['images_dir'], new_category)
                os.makedirs(new_dir, exist_ok=True)
                
                new_path = os.path.join(new_dir, os.path.basename(image_path))
                
                # نقل الصورة
                shutil.move(image_path, new_path)
                
                # تحديث القائمة
                self.image_list.takeItem(self.image_list.row(current_item))
                
                # تحديث قائمة الفئات
                self._update_category_list()
                
                # مسح عرض الصورة
                self.image_view.clear()
                self.image_info.clear()
                
                QMessageBox.information(self, "تم النقل", f"تم نقل الصورة بنجاح إلى الفئة {new_category}.")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء نقل الصورة:\n{str(e)}")
    
    def _on_export_clicked(self):
        """معالجة النقر على زر التصدير"""
        # الحصول على الصورة الحالية
        current_item = self.image_list.currentItem()
        if not current_item:
            return
        
        image_path = current_item.data(Qt.UserRole)
        
        # اختيار مسار الحفظ
        save_path, _ = QFileDialog.getSaveFileName(
            self, "تصدير الصورة", os.path.basename(image_path),
            "صور (*.jpg *.jpeg *.png *.webp)"
        )
        
        if save_path:
            try:
                # نسخ الصورة
                shutil.copy2(image_path, save_path)
                
                QMessageBox.information(self, "تم التصدير", f"تم تصدير الصورة بنجاح إلى:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تصدير الصورة:\n{str(e)}")

class CrawlerWidget(QWidget):
    """واجهة زاحف الويب"""
    
    def __init__(self, parent=None):
        """
        تهيئة واجهة زاحف الويب
        
        المعلمات:
            parent (QWidget): الواجهة الأم
        """
        super().__init__(parent)
        
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين
        self.config = {
            'output_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'max_images_per_source': int(os.getenv('MAX_IMAGES_PER_SOURCE', 100)),
            'delay_between_requests': float(os.getenv('DELAY_BETWEEN_REQUESTS', 1.0)),
            'min_image_size': 10 * 1024,  # 10 KB
            'max_threads': int(os.getenv('MAX_CRAWLER_THREADS', 5))
        }
        
        # قائمة المصادر
        self.sources = []
        
        # إنشاء واجهة المستخدم
        self._init_ui()
    
    def _init_ui(self):
        """إنشاء واجهة المستخدم"""
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        
        # قسم التكوين
        config_group = QFrame()
        config_group.setFrameShape(QFrame.StyledPanel)
        config_layout = QVBoxLayout()
        
        config_title = QLabel("إعدادات الزاحف:")
        config_title.setStyleSheet("font-weight: bold;")
        
        # إعدادات المخرجات
        output_layout = QHBoxLayout()
        output_label = QLabel("مجلد المخرجات:")
        self.output_dir_edit = QLineEdit(self.config['output_dir'])
        self.output_dir_button = QPushButton("تصفح...")
        self.output_dir_button.clicked.connect(self._on_browse_output_dir)
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(self.output_dir_button)
        
        # إعدادات أخرى
        other_config_layout = QHBoxLayout()
        
        max_images_label = QLabel("الحد الأقصى للصور لكل مصدر:")
        self.max_images_spin = QSpinBox()
        self.max_images_spin.setRange(10, 1000)
        self.max_images_spin.setValue(self.config['max_images_per_source'])
        
        delay_label = QLabel("التأخير بين الطلبات (ثانية):")
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0.1, 10.0)
        self.delay_spin.setValue(self.config['delay_between_requests'])
        
        threads_label = QLabel("عدد الخيوط:")
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 10)
        self.threads_spin.setValue(self.config['max_threads'])
        
        other_config_layout.addWidget(max_images_label)
        other_config_layout.addWidget(self.max_images_spin)
        other_config_layout.addWidget(delay_label)
        other_config_layout.addWidget(self.delay_spin)
        other_config_layout.addWidget(threads_label)
        other_config_layout.addWidget(self.threads_spin)
        
        # إضافة العناصر إلى تخطيط التكوين
        config_layout.addWidget(config_title)
        config_layout.addLayout(output_layout)
        config_layout.addLayout(other_config_layout)
        config_group.setLayout(config_layout)
        
        # قسم المصادر
        sources_group = QFrame()
        sources_group.setFrameShape(QFrame.StyledPanel)
        sources_layout = QVBoxLayout()
        
        sources_title = QLabel("مصادر الصور:")
        sources_title.setStyleSheet("font-weight: bold;")
        
        # قائمة المصادر
        self.sources_list = QListWidget()
        
        # أزرار المصادر
        sources_buttons_layout = QHBoxLayout()
        self.add_source_button = QPushButton("إضافة مصدر")
        self.add_source_button.clicked.connect(self._on_add_source)
        self.edit_source_button = QPushButton("تعديل")
        self.edit_source_button.clicked.connect(self._on_edit_source)
        self.remove_source_button = QPushButton("حذف")
        self.remove_source_button.clicked.connect(self._on_remove_source)
        
        sources_buttons_layout.addWidget(self.add_source_button)
        sources_buttons_layout.addWidget(self.edit_source_button)
        sources_buttons_layout.addWidget(self.remove_source_button)
        
        # إضافة العناصر إلى تخطيط المصادر
        sources_layout.addWidget(sources_title)
        sources_layout.addWidget(self.sources_list)
        sources_layout.addLayout(sources_buttons_layout)
        sources_group.setLayout(sources_layout)
        
        # قسم التنفيذ
        execution_group = QFrame()
        execution_group.setFrameShape(QFrame.StyledPanel)
        execution_layout = QVBoxLayout()
        
        # شريط التقدم
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        # حالة التنفيذ
        self.status_label = QLabel("جاهز للبدء")
        
        # زر البدء
        self.start_button = QPushButton("بدء الزحف")
        self.start_button.clicked.connect(self._on_start_crawl)
        
        # إضافة العناصر إلى تخطيط التنفيذ
        execution_layout.addWidget(self.progress_bar)
        execution_layout.addWidget(self.status_label)
        execution_layout.addWidget(self.start_button)
        execution_group.setLayout(execution_layout)
        
        # إضافة الأقسام إلى التخطيط الرئيسي
        main_layout.addWidget(config_group)
        main_layout.addWidget(sources_group)
        main_layout.addWidget(execution_group)
        
        self.setLayout(main_layout)
    
    def _on_browse_output_dir(self):
        """معالجة النقر على زر تصفح مجلد المخرجات"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "اختر مجلد المخرجات", self.output_dir_edit.text()
        )
        
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def _on_add_source(self):
        """معالجة النقر على زر إضافة مصدر"""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        
        # إنشاء مربع حوار
        dialog = QDialog(self)
        dialog.setWindowTitle("إضافة مصدر جديد")
        
        # التخطيط
        layout = QFormLayout()
        
        # حقول الإدخال
        url_edit = QLineEdit()
        url_edit.setPlaceholderText("https://example.com/plant-diseases")
        
        category_combo = QComboBox()
        category_combo.addItems(['vegetables', 'fruits', 'crops', 'unclassified'])
        
        depth_spin = QSpinBox()
        depth_spin.setRange(1, 5)
        depth_spin.setValue(2)
        
        # إضافة الحقول إلى التخطيط
        layout.addRow("عنوان URL:", url_edit)
        layout.addRow("الفئة:", category_combo)
        layout.addRow("عمق الزحف:", depth_spin)
        
        # أزرار
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addRow(buttons)
        dialog.setLayout(layout)
        
        # عرض مربع الحوار
        if dialog.exec_() == QDialog.Accepted:
            # إضافة المصدر
            url = url_edit.text().strip()
            if url:
                source = {
                    'url': url,
                    'category': category_combo.currentText(),
                    'max_depth': depth_spin.value()
                }
                
                self.sources.append(source)
                self._update_sources_list()
    
    def _on_edit_source(self):
        """معالجة النقر على زر تعديل مصدر"""
        # الحصول على المصدر الحالي
        current_item = self.sources_list.currentItem()
        if not current_item:
            return
        
        index = current_item.data(Qt.UserRole)
        source = self.sources[index]
        
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        
        # إنشاء مربع حوار
        dialog = QDialog(self)
        dialog.setWindowTitle("تعديل المصدر")
        
        # التخطيط
        layout = QFormLayout()
        
        # حقول الإدخال
        url_edit = QLineEdit(source['url'])
        
        category_combo = QComboBox()
        category_combo.addItems(['vegetables', 'fruits', 'crops', 'unclassified'])
        category_combo.setCurrentText(source['category'])
        
        depth_spin = QSpinBox()
        depth_spin.setRange(1, 5)
        depth_spin.setValue(source['max_depth'])
        
        # إضافة الحقول إلى التخطيط
        layout.addRow("عنوان URL:", url_edit)
        layout.addRow("الفئة:", category_combo)
        layout.addRow("عمق الزحف:", depth_spin)
        
        # أزرار
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addRow(buttons)
        dialog.setLayout(layout)
        
        # عرض مربع الحوار
        if dialog.exec_() == QDialog.Accepted:
            # تحديث المصدر
            url = url_edit.text().strip()
            if url:
                self.sources[index] = {
                    'url': url,
                    'category': category_combo.currentText(),
                    'max_depth': depth_spin.value()
                }
                
                self._update_sources_list()
    
    def _on_remove_source(self):
        """معالجة النقر على زر حذف مصدر"""
        # الحصول على المصدر الحالي
        current_item = self.sources_list.currentItem()
        if not current_item:
            return
        
        index = current_item.data(Qt.UserRole)
        
        # تأكيد الحذف
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف المصدر؟\n{self.sources[index]['url']}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # حذف المصدر
            del self.sources[index]
            self._update_sources_list()
    
    def _update_sources_list(self):
        """تحديث قائمة المصادر"""
        self.sources_list.clear()
        
        # إضافة المصادر
        for i, source in enumerate(self.sources):
            item = QListWidgetItem(f"{source['url']} ({source['category']}, عمق: {source['max_depth']})")
            item.setData(Qt.UserRole, i)
            self.sources_list.addItem(item)
    
    def _on_start_crawl(self):
        """معالجة النقر على زر بدء الزحف"""
        # التحقق من وجود مصادر
        if not self.sources:
            QMessageBox.warning(self, "لا توجد مصادر", "يرجى إضافة مصادر قبل بدء الزحف.")
            return
        
        # تحديث التكوين
        self.config['output_dir'] = self.output_dir_edit.text()
        self.config['max_images_per_source'] = self.max_images_spin.value()
        self.config['delay_between_requests'] = self.delay_spin.value()
        self.config['max_threads'] = self.threads_spin.value()
        
        # إنشاء المجلدات
        os.makedirs(self.config['output_dir'], exist_ok=True)
        for category in ['vegetables', 'fruits', 'crops', 'unclassified']:
            os.makedirs(os.path.join(self.config['output_dir'], category), exist_ok=True)
        
        # تعطيل عناصر واجهة المستخدم
        self.start_button.setEnabled(False)
        self.add_source_button.setEnabled(False)
        self.edit_source_button.setEnabled(False)
        self.remove_source_button.setEnabled(False)
        
        # إنشاء خيط العمل
        self.worker = WorkerThread('crawl', {
            'config': self.config,
            'sources': self.sources
        })
        
        # ربط الإشارات
        self.worker.update_progress.connect(self.progress_bar.setValue)
        self.worker.update_status.connect(self.status_label.setText)
        self.worker.task_completed.connect(self._on_crawl_completed)
        
        # بدء الخيط
        self.worker.start()
    
    def _on_crawl_completed(self, stats):
        """
        معالجة اكتمال الزحف
        
        المعلمات:
            stats (dict): إحصائيات الزحف
        """
        # تمكين عناصر واجهة المستخدم
        self.start_button.setEnabled(True)
        self.add_source_button.setEnabled(True)
        self.edit_source_button.setEnabled(True)
        self.remove_source_button.setEnabled(True)
        
        # عرض النتائج
        message = f"اكتمل زحف الويب بنجاح!\n\n"
        message += f"إجمالي المصادر: {stats['total_sources']}\n"
        message += f"المصادر الناجحة: {stats['successful_sources']}\n"
        message += f"المصادر الفاشلة: {stats['failed_sources']}\n"
        message += f"إجمالي الصور: {stats['total_images']}\n\n"
        
        message += "الصور حسب الفئة:\n"
        for category, count in stats['images_by_category'].items():
            if count > 0:
                message += f"- {category}: {count}\n"
        
        QMessageBox.information(self, "اكتمل الزحف", message)

class ProcessingWidget(QWidget):
    """واجهة معالجة الصور"""
    
    def __init__(self, parent=None):
        """
        تهيئة واجهة معالجة الصور
        
        المعلمات:
            parent (QWidget): الواجهة الأم
        """
        super().__init__(parent)
        
        # تحميل متغيرات البيئة
        load_dotenv()
        
        # التكوين
        self.config = {
            'images_dir': os.getenv('IMAGE_OUTPUT_DIR', 'data/images'),
            'categories': ['vegetables', 'fruits', 'crops', 'unclassified']
        }
        
        # إنشاء واجهة المستخدم
        self._init_ui()
    
    def _init_ui(self):
        """إنشاء واجهة المستخدم"""
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        
        # قسم التصنيف
        classify_group = QFrame()
        classify_group.setFrameShape(QFrame.StyledPanel)
        classify_layout = QVBoxLayout()
        
        classify_title = QLabel("تصنيف الصور:")
        classify_title.setStyleSheet("font-weight: bold;")
        
        classify_desc = QLabel("تصنيف الصور غير المصنفة إلى فئات (خضروات، فواكه، محاصيل) بناءً على خصائصها.")
        
        classify_button = QPushButton("تصنيف الصور")
        classify_button.clicked.connect(self._on_classify_clicked)
        
        classify_layout.addWidget(classify_title)
        classify_layout.addWidget(classify_desc)
        classify_layout.addWidget(classify_button)
        classify_group.setLayout(classify_layout)
        
        # قسم التنقية
        filter_group = QFrame()
        filter_group.setFrameShape(QFrame.StyledPanel)
        filter_layout = QVBoxLayout()
        
        filter_title = QLabel("تنقية الصور:")
        filter_title.setStyleSheet("font-weight: bold;")
        
        filter_desc = QLabel("إزالة الصور غير المناسبة (مشوشة، منخفضة الدقة، مكررة) ونقلها إلى مجلد الصور المرفوضة.")
        
        filter_button = QPushButton("تنقية الصور")
        filter_button.clicked.connect(self._on_filter_clicked)
        
        filter_layout.addWidget(filter_title)
        filter_layout.addWidget(filter_desc)
        filter_layout.addWidget(filter_button)
        filter_group.setLayout(filter_layout)
        
        # قسم الترميز
        encode_group = QFrame()
        encode_group.setFrameShape(QFrame.StyledPanel)
        encode_layout = QVBoxLayout()
        
        encode_title = QLabel("ترميز الصور:")
        encode_title.setStyleSheet("font-weight: bold;")
        
        encode_desc = QLabel("إعادة تسمية الصور وإضافة البيانات الوصفية (نوع المرض، نوع النبات) بناءً على محتوى الصورة.")
        
        encode_button = QPushButton("ترميز الصور")
        encode_button.clicked.connect(self._on_encode_clicked)
        
        encode_layout.addWidget(encode_title)
        encode_layout.addWidget(encode_desc)
        encode_layout.addWidget(encode_button)
        encode_group.setLayout(encode_layout)
        
        # قسم الأرشفة
        archive_group = QFrame()
        archive_group.setFrameShape(QFrame.StyledPanel)
        archive_layout = QVBoxLayout()
        
        archive_title = QLabel("أرشفة الصور:")
        archive_title.setStyleSheet("font-weight: bold;")
        
        archive_desc = QLabel("ضغط الصور وحفظها في أرشيفات مع البيانات الوصفية.")
        
        self.delete_originals_check = QCheckBox("حذف الصور الأصلية بعد الأرشفة")
        
        archive_button = QPushButton("أرشفة الصور")
        archive_button.clicked.connect(self._on_archive_clicked)
        
        archive_layout.addWidget(archive_title)
        archive_layout.addWidget(archive_desc)
        archive_layout.addWidget(self.delete_originals_check)
        archive_layout.addWidget(archive_button)
        archive_group.setLayout(archive_layout)
        
        # قسم التنفيذ
        execution_group = QFrame()
        execution_group.setFrameShape(QFrame.StyledPanel)
        execution_layout = QVBoxLayout()
        
        # شريط التقدم
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        # حالة التنفيذ
        self.status_label = QLabel("جاهز للبدء")
        
        # إضافة العناصر إلى تخطيط التنفيذ
        execution_layout.addWidget(self.progress_bar)
        execution_layout.addWidget(self.status_label)
        execution_group.setLayout(execution_layout)
        
        # إضافة الأقسام إلى التخطيط الرئيسي
        main_layout.addWidget(classify_group)
        main_layout.addWidget(filter_group)
        main_layout.addWidget(encode_group)
        main_layout.addWidget(archive_group)
        main_layout.addWidget(execution_group)
        
        self.setLayout(main_layout)
    
    def _on_classify_clicked(self):
        """معالجة النقر على زر التصنيف"""
        # تأكيد العملية
        reply = QMessageBox.question(
            self, "تأكيد التصنيف",
            "هل أنت متأكد من بدء عملية تصنيف الصور؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # إنشاء خيط العمل
            self.worker = WorkerThread('classify', {
                'config': {
                    'input_dir': os.path.join(self.config['images_dir'], 'unclassified'),
                    'output_base_dir': self.config['images_dir']
                }
            })
            
            # ربط الإشارات
            self.worker.update_progress.connect(self.progress_bar.setValue)
            self.worker.update_status.connect(self.status_label.setText)
            self.worker.task_completed.connect(self._on_classify_completed)
            
            # بدء الخيط
            self.worker.start()
    
    def _on_classify_completed(self, stats):
        """
        معالجة اكتمال التصنيف
        
        المعلمات:
            stats (dict): إحصائيات التصنيف
        """
        # عرض النتائج
        message = f"اكتمل تصنيف الصور بنجاح!\n\n"
        message += f"إجمالي الصور: {stats['total_images']}\n"
        message += f"الصور المصنفة: {stats['classified_images']}\n"
        message += f"الصور الفاشلة: {stats['failed_images']}\n\n"
        
        message += "التصنيف حسب الفئة:\n"
        for category, count in stats['classification_by_category'].items():
            if count > 0:
                message += f"- {category}: {count}\n"
        
        QMessageBox.information(self, "اكتمل التصنيف", message)
    
    def _on_filter_clicked(self):
        """معالجة النقر على زر التنقية"""
        # تأكيد العملية
        reply = QMessageBox.question(
            self, "تأكيد التنقية",
            "هل أنت متأكد من بدء عملية تنقية الصور؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # إنشاء خيط العمل
            self.worker = WorkerThread('filter', {
                'config': {
                    'input_base_dir': self.config['images_dir'],
                    'rejected_dir': os.path.join(self.config['images_dir'], 'rejected')
                }
            })
            
            # ربط الإشارات
            self.worker.update_progress.connect(self.progress_bar.setValue)
            self.worker.update_status.connect(self.status_label.setText)
            self.worker.task_completed.connect(self._on_filter_completed)
            
            # بدء الخيط
            self.worker.start()
    
    def _on_filter_completed(self, stats):
        """
        معالجة اكتمال التنقية
        
        المعلمات:
            stats (dict): إحصائيات التنقية
        """
        # عرض النتائج
        message = f"اكتمل تنقية الصور بنجاح!\n\n"
        message += f"إجمالي الصور: {stats['total_images']}\n"
        message += f"الصور المقبولة: {stats['accepted_images']}\n"
        message += f"الصور المرفوضة: {stats['rejected_images']}\n\n"
        
        if stats['rejection_reasons']:
            message += "أسباب الرفض:\n"
            for reason, count in stats['rejection_reasons'].items():
                message += f"- {reason}: {count}\n"
        
        QMessageBox.information(self, "اكتمل التنقية", message)
    
    def _on_encode_clicked(self):
        """معالجة النقر على زر الترميز"""
        # تأكيد العملية
        reply = QMessageBox.question(
            self, "تأكيد الترميز",
            "هل أنت متأكد من بدء عملية ترميز الصور؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # إنشاء خيط العمل
            self.worker = WorkerThread('encode', {
                'config': {
                    'input_base_dir': self.config['images_dir'],
                    'metadata_file': os.path.join(self.config['images_dir'], 'metadata.csv')
                }
            })
            
            # ربط الإشارات
            self.worker.update_progress.connect(self.progress_bar.setValue)
            self.worker.update_status.connect(self.status_label.setText)
            self.worker.task_completed.connect(self._on_encode_completed)
            
            # بدء الخيط
            self.worker.start()
    
    def _on_encode_completed(self, stats):
        """
        معالجة اكتمال الترميز
        
        المعلمات:
            stats (dict): إحصائيات الترميز
        """
        # عرض النتائج
        message = f"اكتمل ترميز الصور بنجاح!\n\n"
        message += f"إجمالي الصور: {stats['total_images']}\n"
        message += f"الصور المرمزة: {stats['encoded_images']}\n"
        message += f"الصور الفاشلة: {stats['failed_images']}\n\n"
        
        if 'categories' in stats:
            message += "الترميز حسب الفئة:\n"
            for category, cat_stats in stats['categories'].items():
                if cat_stats['total_images'] > 0:
                    message += f"- {category}: {cat_stats['encoded_images']} من {cat_stats['total_images']}\n"
        
        QMessageBox.information(self, "اكتمل الترميز", message)
    
    def _on_archive_clicked(self):
        """معالجة النقر على زر الأرشفة"""
        # تأكيد العملية
        reply = QMessageBox.question(
            self, "تأكيد الأرشفة",
            "هل أنت متأكد من بدء عملية أرشفة الصور؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # إنشاء خيط العمل
            self.worker = WorkerThread('archive', {
                'config': {
                    'input_base_dir': self.config['images_dir'],
                    'archive_dir': os.path.join(self.config['images_dir'], '../archives'),
                    'metadata_file': os.path.join(self.config['images_dir'], 'metadata.csv')
                },
                'delete_originals': self.delete_originals_check.isChecked()
            })
            
            # ربط الإشارات
            self.worker.update_progress.connect(self.progress_bar.setValue)
            self.worker.update_status.connect(self.status_label.setText)
            self.worker.task_completed.connect(self._on_archive_completed)
            
            # بدء الخيط
            self.worker.start()
    
    def _on_archive_completed(self, stats):
        """
        معالجة اكتمال الأرشفة
        
        المعلمات:
            stats (dict): إحصائيات الأرشفة
        """
        # عرض النتائج
        message = f"اكتمل أرشفة الصور بنجاح!\n\n"
        message += f"إجمالي الصور: {stats['total_images']}\n"
        message += f"الصور المؤرشفة: {stats['archived_images']}\n"
        message += f"الصور الفاشلة: {stats['failed_images']}\n"
        message += f"عدد الأرشيفات: {stats['total_archives']}\n"
        
        if 'total_archive_size' in stats:
            size_mb = stats['total_archive_size'] / (1024 * 1024)
            message += f"حجم الأرشيفات: {size_mb:.2f} ميجابايت\n\n"
        
        if 'categories' in stats:
            message += "الأرشفة حسب الفئة:\n"
            for category, cat_stats in stats['categories'].items():
                if cat_stats['total_images'] > 0:
                    message += f"- {category}: {cat_stats['archived_images']} من {cat_stats['total_images']}\n"
        
        QMessageBox.information(self, "اكتمل الأرشفة", message)

class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        """تهيئة النافذة الرئيسية"""
        super().__init__()
        
        # إعداد النافذة
        self.setWindowTitle("نظام جمع وتصنيف صور الأمراض الزراعية")
        self.setMinimumSize(800, 600)
        
        # إنشاء علامات التبويب
        self.tabs = QTabWidget()
        
        # إضافة علامات التبويب
        self.gallery_widget = ImageGalleryWidget()
        self.tabs.addTab(self.gallery_widget, "معرض الصور")
        
        self.crawler_widget = CrawlerWidget()
        self.tabs.addTab(self.crawler_widget, "زاحف الويب")
        
        self.processing_widget = ProcessingWidget()
        self.tabs.addTab(self.processing_widget, "معالجة الصور")
        
        # تعيين علامات التبويب كعنصر مركزي
        self.setCentralWidget(self.tabs)

# نموذج استخدام
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
