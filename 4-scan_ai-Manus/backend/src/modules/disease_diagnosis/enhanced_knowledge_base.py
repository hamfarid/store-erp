# File:
# /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/enhanced_knowledge_base.py
"""
from flask import g
قاعدة المعرفة الزراعية المحسنة
يوفر هذا الملف قاعدة معرفة شاملة للأمراض النباتية والمحاصيل الزراعية
مع دعم المصادر الموثوقة والمراجع العلمية
"""

import json
import logging
import os
from datetime import datetime

import yaml

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EnhancedAgriculturalKnowledgeBase:
    """قاعدة المعرفة الزراعية المحسنة مع دعم المصادر والمراجع"""

    # Constants for commonly used strings
    USE_RESISTANT_VARIETIES = "استخدام أصناف مقاومة"
    WEAR_GLOVES_MASK = "ارتداء قفازات وقناع"
    AVOID_SPRAY_BEFORE_RAIN = "تجنب الرش قبل المطر"
    NUMBERED_LIST_START = "1. **"
    WEBSITE_LABEL = "الموقع الإلكتروني:"
    PRODUCTS_LABEL = "المنتجات:"
    DATABASE_LABEL = "قواعد البيانات:"
    PATHOGEN_LABEL = "المسبب:"
    SYMPTOMS_LABEL = "الأعراض:"
    SOURCE_LABEL = "المصدر:"
    LINK_LABEL = "الرابط:"
    PROPERTIES_LABEL = "الخصائص:"

    def __init__(self, knowledge_dir=None, sources_file=None):
        """
        تهيئة قاعدة المعرفة الزراعية

        المعلمات:
            knowledge_dir (str, optional): مسار مجلد قاعدة المعرفة
            sources_file (str, optional): مسار ملف المصادر
        """
        # مسار مجلد قاعدة المعرفة
        if knowledge_dir:
            self.knowledge_dir = knowledge_dir
        else:
            self.knowledge_dir = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                'knowledge')

        # مسار ملف المصادر
        if sources_file:
            self.sources_file = sources_file
        else:
            self.sources_file = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)),
                'agricultural_sources.md')

        # التأكد من وجود مجلد قاعدة المعرفة
        os.makedirs(self.knowledge_dir, exist_ok=True)

        # قاعدة المعرفة
        self.diseases = {}
        self.crops = {}
        self.treatments = {}
        self.varieties = {}
        self.hybridization = {}

        # المصادر
        self.sources = {
            "scientific_journals": [],
            "seed_companies": [],
            "fertilizer_companies": [],
            "research_labs": [],
            "disease_info": [],
            "crop_varieties": [],
            "hybridization_methods": [],
            "parent_specifications": []
        }

        # تاريخ آخر تحديث
        self.last_updated = None

        # تحميل قاعدة المعرفة
        self._load_knowledge_base()

        # تحميل المصادر
        self._load_sources()

        logger.info("تم تهيئة قاعدة المعرفة الزراعية المحسنة")

    def _load_knowledge_base(self):
        """تحميل قاعدة المعرفة من الملفات"""
        try:
            # تحميل الأمراض
            diseases_file = os.path.join(self.knowledge_dir, 'diseases.yaml')
            if os.path.exists(diseases_file):
                with open(diseases_file, 'r', encoding='utf-8') as f:
                    self.diseases = yaml.safe_load(f)
                logger.info(
                    "تم تحميل %d مرض من %s", len(
                        self.diseases), diseases_file)

            # تحميل المحاصيل
            crops_file = os.path.join(self.knowledge_dir, 'crops.yaml')
            if os.path.exists(crops_file):
                with open(crops_file, 'r', encoding='utf-8') as f:
                    self.crops = yaml.safe_load(f)
                logger.info(
                    "تم تحميل %d محصول من %s", len(
                        self.crops), crops_file)

            # تحميل العلاجات
            treatments_file = os.path.join(
                self.knowledge_dir, 'treatments.yaml')
            if os.path.exists(treatments_file):
                with open(treatments_file, 'r', encoding='utf-8') as f:
                    self.treatments = yaml.safe_load(f)
                logger.info(
                    "تم تحميل %d علاج من %s", len(
                        self.treatments), treatments_file)

            # تحميل الأصناف
            varieties_file = os.path.join(self.knowledge_dir, 'varieties.yaml')
            if os.path.exists(varieties_file):
                with open(varieties_file, 'r', encoding='utf-8') as f:
                    self.varieties = yaml.safe_load(f)
                logger.info(
                    "تم تحميل %d صنف من %s", len(
                        self.varieties), varieties_file)

            # تحميل معلومات التهجين
            hybridization_file = os.path.join(
                self.knowledge_dir, 'hybridization.yaml')
            if os.path.exists(hybridization_file):
                with open(hybridization_file, 'r', encoding='utf-8') as f:
                    self.hybridization = yaml.safe_load(f)
                logger.info(
                    "تم تحميل معلومات التهجين من %s",
                    hybridization_file)

            # تحميل تاريخ آخر تحديث
            last_updated_file = os.path.join(
                self.knowledge_dir, 'last_updated.txt')
            if os.path.exists(last_updated_file):
                with open(last_updated_file, 'r', encoding='utf-8') as f:
                    self.last_updated = f.read().strip()
                logger.info("تاريخ آخر تحديث: %s", self.last_updated)

            # إذا لم تكن قاعدة المعرفة موجودة، إنشاء قاعدة معرفة افتراضية
            if not self.diseases and not self.crops and not self.treatments and not self.varieties and not self.hybridization:
                logger.warning(
                    "قاعدة المعرفة غير موجودة، سيتم إنشاء قاعدة معرفة افتراضية")
                self._create_default_knowledge_base()

        except Exception as e:
            logger.error("خطأ أثناء تحميل قاعدة المعرفة: %s", str(e))
            # إنشاء قاعدة معرفة افتراضية
            self._create_default_knowledge_base()

    def _create_default_knowledge_base(self):
        """إنشاء قاعدة معرفة افتراضية"""
        # الأمراض الافتراضية
        self.diseases = {
            "late_blight": {
                "name": "اللفحة المتأخرة",
                "scientific_name": "Phytophthora infestans",
                "crops": ["potato", "tomato"],
                "symptoms": [
                    "بقع بنية على الأوراق",
                    "تعفن الثمار والدرنات",
                    "نمو أبيض على السطح السفلي للأوراق"
                ],
                "conditions": [
                    "رطوبة عالية",
                    "درجات حرارة معتدلة (15-25 درجة مئوية)"
                ],
                "treatments": ["fungicide_copper", "fungicide_mancozeb"],
                "prevention": [
                    self.USE_RESISTANT_VARIETIES,
                    "تناوب المحاصيل",
                    "تجنب الري العلوي"
                ],
                "source": "مجلة أمراض النبات، المجلد 105، العدد 4، 2021",
                "reference": "https://apsjournals.apsnet.org/doi/10.1094/PDIS-09-20-1932-RE"
            },
            "powdery_mildew_cucurbits": {
                "name": "البياض الدقيقي في القرعيات",
                "scientific_name": "Podosphaera xanthii",
                "crops": ["cucumber", "squash", "melon"],
                "symptoms": [
                    "بقع بيضاء دقيقية على الأوراق",
                    "تشوه النمو",
                    "ضعف النبات"
                ],
                "conditions": [
                    "رطوبة منخفضة",
                    "درجات حرارة معتدلة (20-30 درجة مئوية)"
                ],
                "treatments": ["fungicide_sulfur", "fungicide_potassium_bicarbonate"],
                "prevention": [
                    self.USE_RESISTANT_VARIETIES,
                    "تهوية جيدة",
                    "تجنب الزراعة الكثيفة"
                ],
                "source": "المجلة الأوروبية لأمراض النبات، المجلد 157، 2020",
                "reference": "https://link.springer.com/article/10.1007/s10658-020-02075-w"
            },
            "fusarium_wilt_tomato": {
                "name": "الذبول الفيوزاريومي في الطماطم",
                "scientific_name": "Fusarium oxysporum f. sp. lycopersici",
                "crops": ["tomato"],
                "symptoms": [
                    "اصفرار الأوراق السفلية",
                    "ذبول النبات",
                    "تلون الأوعية الناقلة"
                ],
                "conditions": [
                    "درجات حرارة دافئة (25-30 درجة مئوية)",
                    "تربة حمضية"
                ],
                "treatments": ["fungicide_thiophanate_methyl", "soil_solarization"],
                "prevention": [
                    self.USE_RESISTANT_VARIETIES,
                    "تناوب المحاصيل",
                    "تعقيم التربة"
                ],
                "source": "مجلة علم الفطريات التطبيقي، المجلد 67، 2021",
                "reference": "https://www.sciencedirect.com/science/article/abs/pii/S0953756221000575"
            }
        }

        # المحاصيل الافتراضية
        self.crops = {
            "tomato": {
                "name": "طماطم",
                "scientific_name": "Solanum lycopersicum",
                "family": "Solanaceae",
                "growing_season": ["spring", "summer"],
                "optimal_temperature": {
                    "min": 15,
                    "max": 30
                },
                "water_requirements": "medium",
                "soil_requirements": "well-drained, pH 6.0-6.8",
                "common_diseases": ["late_blight", "fusarium_wilt_tomato", "early_blight"],
                "varieties": ["moneymaker", "beefsteak", "roma"],
                "source": "شركة سينجينتا للبذور",
                "reference": "https://www.syngenta.com/seeds/vegetables/tomatoes"
            },
            "cucumber": {
                "name": "خيار",
                "scientific_name": "Cucumis sativus",
                "family": "Cucurbitaceae",
                "growing_season": ["spring", "summer"],
                "optimal_temperature": {
                    "min": 18,
                    "max": 32
                },
                "water_requirements": "high",
                "soil_requirements": "well-drained, pH 6.0-7.0",
                "common_diseases": ["powdery_mildew_cucurbits", "downy_mildew", "angular_leaf_spot"],
                "varieties": ["beit_alpha", "english", "pickling"],
                "source": "شركة سيمينيس للبذور",
                "reference": "https://seminis.com/global/en/products/cucumber/"
            },
            "wheat": {
                "name": "قمح",
                "scientific_name": "Triticum aestivum",
                "family": "Poaceae",
                "growing_season": ["winter", "spring"],
                "optimal_temperature": {
                    "min": 10,
                    "max": 25
                },
                "water_requirements": "medium",
                "soil_requirements": "loamy, pH 6.0-7.0",
                "common_diseases": ["wheat_rust", "powdery_mildew_wheat", "fusarium_head_blight"],
                "varieties": ["kharif", "durum", "amir"],
                "source": "المركز الدولي لتحسين الذرة والقمح (CIMMYT)",
                "reference": "https://www.cimmyt.org/projects/wheat-varieties/"
            }
        }

        # العلاجات الافتراضية
        self.treatments = {
            "fungicide_copper": {
                "name": "مبيد فطري نحاسي",
                "type": "chemical",
                "active_ingredient": "copper hydroxide",
                "target_diseases": ["late_blight", "early_blight", "bacterial_spot"],
                "application_rate": "2-4 g/L",
                "safety_period": 7,
                "precautions": [
                    self.WEAR_GLOVES_MASK,
                    "تجنب الرش في الطقس الحار",
                    self.AVOID_SPRAY_BEFORE_RAIN
                ],
                "source": "شركة باسف (BASF)",
                "reference": "https://agriculture.basf.com/global/en/business-areas/crop-protection/products.html"
            },
            "fungicide_mancozeb": {
                "name": "مبيد فطري مانكوزيب",
                "type": "chemical",
                "active_ingredient": "mancozeb",
                "target_diseases": ["late_blight", "early_blight", "downy_mildew"],
                "application_rate": "2-3 g/L",
                "safety_period": 14,
                "precautions": [
                    self.WEAR_GLOVES_MASK,
                    "تجنب الرش في الطقس الحار",
                    self.AVOID_SPRAY_BEFORE_RAIN
                ],
                "source": "شركة إف إم سي (FMC)",
                "reference": "https://www.fmcagus.com/en-us/products"
            },
            "fungicide_sulfur": {
                "name": "مبيد فطري كبريتي",
                "type": "chemical",
                "active_ingredient": "sulfur",
                "target_diseases": ["powdery_mildew_cucurbits", "powdery_mildew_wheat"],
                "application_rate": "3-5 g/L",
                "safety_period": 3,
                "precautions": [
                    self.WEAR_GLOVES_MASK,
                    "تجنب الرش في درجات الحرارة العالية (فوق 30 درجة مئوية)",
                    self.AVOID_SPRAY_BEFORE_RAIN
                ],
                "source": "شركة سومي أجرو (Sumitomo Chemical)",
                "reference": "https://www.sumitomo-chem.co.jp/english/products/"
            }
        }

        # الأصناف الافتراضية
        self.varieties = {
            "tomato": {
                "moneymaker": {
                    "name": "مونيميكر",
                    "type": "indeterminate",
                    "fruit_size": "medium",
                    "fruit_color": "red",
                    "days_to_maturity": 75,
                    "disease_resistance": ["fusarium_wilt_tomato", "verticillium_wilt"],
                    "yield_potential": "high",
                    "best_uses": ["fresh", "canning"],
                    "source": "شركة سينجينتا للبذور",
                    "reference": "https://www.syngenta.com/seeds/vegetables/tomatoes"
                },
                "beefsteak": {
                    "name": "بيف ستيك",
                    "type": "indeterminate",
                    "fruit_size": "large",
                    "fruit_color": "red",
                    "days_to_maturity": 85,
                    "disease_resistance": ["fusarium_wilt_tomato"],
                    "yield_potential": "medium",
                    "best_uses": ["fresh", "slicing"],
                    "source": "شركة سيمينيس للبذور",
                    "reference": "https://seminis.com/global/en/products/tomatoes/"
                },
                "roma": {
                    "name": "روما",
                    "type": "determinate",
                    "fruit_size": "medium",
                    "fruit_color": "red",
                    "days_to_maturity": 70,
                    "disease_resistance": ["fusarium_wilt_tomato", "verticillium_wilt", "bacterial_speck"],
                    "yield_potential": "high",
                    "best_uses": ["sauce", "canning", "drying"],
                    "source": "شركة هاينز للبذور",
                    "reference": "https://www.heinzseed.com/tomato-varieties/"
                }
            },
            "wheat": {
                "kharif": {
                    "name": "خريف",
                    "type": "winter",
                    "grain_color": "amber",
                    "days_to_maturity": 120,
                    "disease_resistance": ["wheat_rust", "powdery_mildew_wheat"],
                    "drought_tolerance": "high",
                    "yield_potential": "medium",
                    "best_uses": ["bread", "general purpose"],
                    "source": "المركز الدولي لتحسين الذرة والقمح (CIMMYT)",
                    "reference": "https://www.cimmyt.org/projects/wheat-varieties/"
                },
                "durum": {
                    "name": "دورم",
                    "type": "spring",
                    "grain_color": "amber",
                    "days_to_maturity": 110,
                    "disease_resistance": ["wheat_rust"],
                    "drought_tolerance": "medium",
                    "yield_potential": "medium",
                    "best_uses": ["pasta", "semolina"],
                    "source": "المركز الدولي للبحوث الزراعية في المناطق الجافة (ICARDA)",
                    "reference": "https://www.icarda.org/research/innovations/wheat-varieties"
                },
                "amir": {
                    "name": "أمير",
                    "type": "winter",
                    "grain_color": "red",
                    "days_to_maturity": 130,
                    "disease_resistance": ["wheat_rust", "powdery_mildew_wheat", "fusarium_head_blight"],
                    "drought_tolerance": "high",
                    "yield_potential": "high",
                    "best_uses": ["bread", "general purpose"],
                    "source": "شركة ليماجرين للبذور",
                    "reference": "https://www.limagrain.com/products/wheat-varieties/"
                }
            }
        }

        # معلومات التهجين الافتراضية
        self.hybridization = {
            "methods": {
                "hand_pollination": {
                    "name": "التلقيح اليدوي",
                    "description": "نقل حبوب اللقاح من نبات إلى آخر يدوياً",
                    "suitable_crops": ["tomato", "pepper", "eggplant", "cucumber"],
                    "steps": [
                        "اختيار الأزهار المناسبة",
                        "إزالة الأسدية من الزهرة المستقبلة (الأم)",
                        "جمع حبوب اللقاح من الزهرة المانحة (الأب)",
                        "نقل حبوب اللقاح إلى ميسم الزهرة المستقبلة",
                        "تعليم الزهرة الملقحة"
                    ],
                    "success_rate": "70-90%",
                    "source": "كتاب \"التقنيات الحديثة في تربية النبات\" (2021)",
                    "reference": "https://www.springer.com/gp/book/9783030459550"
                },
                "backcrossing": {
                    "name": "التهجين الرجعي",
                    "description": "تهجين النسل مع أحد الآباء لتثبيت صفة معينة",
                    "suitable_crops": ["wheat", "rice", "corn", "tomato"],
                    "steps": [
                        "إجراء التهجين الأولي بين الأبوين",
                        "اختيار النباتات التي تحمل الصفة المرغوبة من الجيل الأول",
                        "تهجين النباتات المختارة مع الأب المتكرر",
                        "تكرار العملية لعدة أجيال",
                        "اختيار النباتات النهائية"
                    ],
                    "success_rate": "60-80%",
                    "source": "مجلة علوم المحاصيل، المجلد 60، العدد 5، 2020",
                    "reference": "https://acsess.onlinelibrary.wiley.com/doi/abs/10.2135/cropsci2020.02.0082"
                },
                "interspecific_hybridization": {
                    "name": "التهجين بين الأنواع",
                    "description": "تهجين نباتات من أنواع مختلفة لنقل صفات مرغوبة",
                    "suitable_crops": ["wheat", "rice", "cotton", "tomato"],
                    "steps": [
                        "اختيار الأنواع المناسبة",
                        "إجراء التلقيح اليدوي",
                        "استخدام تقنيات مساعدة (إنقاذ الأجنة، مضاعفة الكروموسومات)",
                        "تقييم الهجن الناتجة",
                        "اختيار الهجن المرغوبة"
                    ],
                    "success_rate": "10-30%",
                    "source": "مجلة التكنولوجيا الحيوية النباتية، المجلد 38، 2020",
                    "reference": "https://www.sciencedirect.com/science/article/abs/pii/S1674205220301878"
                }
            },
            "parent_selection": {
                "tomato": {
                    "disease_resistance": {
                        "description": "اختيار آباء مقاومين للأمراض الشائعة",
                        "recommended_parents": ["moneymaker", "roma"],
                        "source": "مجلة تربية النبات، المجلد 39، العدد 4، 2020",
                        "reference": "https://link.springer.com/article/10.1007/s10681-020-2553-7"
                    },
                    "fruit_quality": {
                        "description": "اختيار آباء ذوي جودة ثمار عالية",
                        "recommended_parents": ["beefsteak", "brandywine"],
                        "source": "مجلة علوم البستنة، المجلد 55، العدد 3، 2020",
                        "reference": "https://www.sciencedirect.com/science/article/abs/pii/S0304423820301679"
                    }
                },
                "wheat": {
                    "drought_tolerance": {
                        "description": "اختيار آباء متحملين للجفاف",
                        "recommended_parents": ["kharif", "amir"],
                        "source": "المجلة الأوروبية لتربية النبات، المجلد 139، 2020",
                        "reference": "https://link.springer.com/article/10.1007/s10681-020-2553-7"
                    },
                    "disease_resistance": {
                        "description": "اختيار آباء مقاومين للأمراض الشائعة",
                        "recommended_parents": ["amir", "durum"],
                        "source": "مجلة أمراض النبات، المجلد 104، العدد 7، 2020",
                        "reference": "https://apsjournals.apsnet.org/doi/10.1094/PDIS-11-19-2402-RE"
                    }
                }
            }
        }

        # حفظ قاعدة المعرفة
        self._save_knowledge_base()

        logger.info("تم إنشاء قاعدة معرفة افتراضية")

    def _save_knowledge_base(self):
        """حفظ قاعدة المعرفة في الملفات"""
        try:
            # التأكد من وجود مجلد قاعدة المعرفة
            os.makedirs(self.knowledge_dir, exist_ok=True)

            # حفظ الأمراض
            diseases_file = os.path.join(self.knowledge_dir, 'diseases.yaml')
            with open(diseases_file, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.diseases,
                    f,
                    allow_unicode=True,
                    sort_keys=False)

            # حفظ المحاصيل
            crops_file = os.path.join(self.knowledge_dir, 'crops.yaml')
            with open(crops_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.crops, f, allow_unicode=True, sort_keys=False)

            # حفظ العلاجات
            treatments_file = os.path.join(
                self.knowledge_dir, 'treatments.yaml')
            with open(treatments_file, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.treatments,
                    f,
                    allow_unicode=True,
                    sort_keys=False)

            # حفظ الأصناف
            varieties_file = os.path.join(self.knowledge_dir, 'varieties.yaml')
            with open(varieties_file, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.varieties,
                    f,
                    allow_unicode=True,
                    sort_keys=False)

            # حفظ معلومات التهجين
            hybridization_file = os.path.join(
                self.knowledge_dir, 'hybridization.yaml')
            with open(hybridization_file, 'w', encoding='utf-8') as f:
                yaml.dump(
                    self.hybridization,
                    f,
                    allow_unicode=True,
                    sort_keys=False)

            # تحديث تاريخ آخر تحديث
            self.last_updated = datetime.now().isoformat()
            last_updated_file = os.path.join(
                self.knowledge_dir, 'last_updated.txt')
            with open(last_updated_file, 'w', encoding='utf-8') as f:
                f.write(self.last_updated)

            logger.info("تم حفظ قاعدة المعرفة")
            return True
        except Exception as e:
            logger.error("خطأ أثناء حفظ قاعدة المعرفة: %s", str(e))
            return False

    def _load_sources(self):
        """تحميل المصادر من ملف المصادر"""
        try:
            if os.path.exists(self.sources_file):
                with open(self.sources_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # استخراج المصادر من محتوى الملف
                self._parse_sources(content)

                logger.info("تم تحميل المصادر من %s", self.sources_file)
            else:
                logger.warning("ملف المصادر غير موجود: %s", self.sources_file)
        except Exception as e:
            logger.error("خطأ أثناء تحميل المصادر: %s", str(e))

    def _parse_sources(self, content):
        """
        استخراج المصادر من محتوى الملف

        المعلمات:
            content (str): محتوى ملف المصادر
        """
        try:
            self._parse_scientific_journals(content)
            self._parse_seed_companies(content)
            self._parse_fertilizer_companies(content)
            self._parse_research_labs(content)
            self._parse_disease_info(content)
            self._parse_varieties_info(content)
            self._parse_hybridization_info(content)

        except Exception as e:
            logger.error("خطأ أثناء تحليل المصادر: %s", str(e))

    def _parse_scientific_journals(self, content):
        """استخراج المجلات العلمية"""
        if "## الرسائل العلمية والأبحاث الأكاديمية" in content:
            section = content.split("## الرسائل العلمية والأبحاث الأكاديمية")[
                1].split("##")[0]

            if "### مجلات علمية متخصصة" in section:
                journals_section = section.split("### مجلات علمية متخصصة")[
                    1].split("###")[0]
                journals = []

                for journal in journals_section.split("\n\n"):
                    journal_info = self._parse_journal_entry(journal)
                    if journal_info:
                        journals.append(journal_info)

                self.sources["scientific_journals"] = journals

    def _parse_journal_entry(self, journal):
        """استخراج معلومات مجلة واحدة"""
        if not (journal.strip() and "**" in journal):
            return None

        journal_info = {}
        lines = journal.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                journal_info["name"] = line.split("**")[1].strip()
            elif "الناشر:" in line:
                journal_info["publisher"] = line.split("الناشر:")[1].strip()
            elif self.WEBSITE_LABEL in line:
                journal_info["website"] = line.split(
                    self.WEBSITE_LABEL)[1].strip()
            elif "المجالات:" in line:
                journal_info["fields"] = [
                    field.strip() for field in line.split("المجالات:")[1].strip().split(",")]

        return journal_info if journal_info else None

    def _parse_seed_companies(self, content):
        """استخراج شركات البذور"""
        if "## شركات البذور المعتمدة" in content:
            section = content.split("## شركات البذور المعتمدة")[
                1].split("##")[0]
            companies = []

            for company in section.split("\n\n"):
                company_info = self._parse_company_entry(company)
                if company_info:
                    companies.append(company_info)

            self.sources["seed_companies"] = companies

    def _parse_fertilizer_companies(self, content):
        """استخراج شركات الأسمدة والمبيدات"""
        if "## شركات الأسمدة والمبيدات" in content:
            section = content.split("## شركات الأسمدة والمبيدات")[
                1].split("##")[0]
            companies = []

            for company in section.split("\n\n"):
                company_info = self._parse_company_entry(company)
                if company_info:
                    companies.append(company_info)

            self.sources["fertilizer_companies"] = companies

    def _parse_company_entry(self, company):
        """استخراج معلومات شركة واحدة"""
        if not (company.strip() and "**" in company):
            return None

        company_info = {}
        lines = company.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                company_info["name"] = line.split("**")[1].strip()
            elif self.WEBSITE_LABEL in line:
                company_info["website"] = line.split(
                    self.WEBSITE_LABEL)[1].strip()
            elif self.PRODUCTS_LABEL in line:
                company_info["products"] = [
                    product.strip() for product in line.split(
                        self.PRODUCTS_LABEL)[1].strip().split(",")]
            elif self.DATABASE_LABEL in line:
                company_info["database"] = line.split(
                    self.DATABASE_LABEL)[1].strip()

        return company_info if company_info else None

    def _parse_research_labs(self, content):
        """استخراج المعامل البحثية"""
        if "## المعامل البحثية المتخصصة" in content:
            section = content.split("## المعامل البحثية المتخصصة")[
                1].split("##")[0]
            labs = []

            for lab in section.split("\n\n"):
                lab_info = self._parse_lab_entry(lab)
                if lab_info:
                    labs.append(lab_info)

            self.sources["research_labs"] = labs

    def _parse_lab_entry(self, lab):
        """استخراج معلومات معمل واحد"""
        if not (lab.strip() and "**" in lab):
            return None

        lab_info = {}
        lines = lab.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                lab_info["name"] = line.split("**")[1].strip()
            elif self.WEBSITE_LABEL in line:
                lab_info["website"] = line.split(self.WEBSITE_LABEL)[1].strip()
            elif "مجالات البحث:" in line:
                lab_info["research_fields"] = [
                    field.strip() for field in line.split("مجالات البحث:")[1].strip().split(",")]
            elif self.DATABASE_LABEL in line:
                lab_info["database"] = line.split(
                    self.DATABASE_LABEL)[1].strip()

        return lab_info if lab_info else None

    def _parse_disease_info(self, content):
        """استخراج معلومات الأمراض"""
        if "## معلومات الأمراض وأعراضها" in content:
            section = content.split("## معلومات الأمراض وأعراضها")[
                1].split("##")[0]
            diseases = []

            diseases.extend(
                self._parse_diseases_by_category(
                    section,
                    "### أمراض الخضروات",
                    "vegetables"))
            diseases.extend(
                self._parse_diseases_by_category(
                    section,
                    "### أمراض المحاصيل الحقلية",
                    "field_crops"))
            diseases.extend(
                self._parse_diseases_by_category(
                    section,
                    "### أمراض أشجار الفاكهة",
                    "fruit_trees"))

            self.sources["disease_info"] = diseases

    def _parse_diseases_by_category(
            self,
            section,
            category_header,
            category_name):
        """استخراج أمراض حسب الفئة"""
        diseases = []
        if category_header in section:
            category_section = section.split(category_header)[
                1].split("###")[0]

            for disease in category_section.split("\n\n"):
                disease_info = self._parse_disease_entry(
                    disease, category_name)
                if disease_info:
                    diseases.append(disease_info)

        return diseases

    def _parse_disease_entry(self, disease, category):
        """استخراج معلومات مرض واحد"""
        if not (disease.strip() and "**" in disease):
            return None

        disease_info = {}
        lines = disease.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                disease_info["name"] = line.split("**")[1].strip()
            elif self.PATHOGEN_LABEL in line:
                disease_info["pathogen"] = line.split(
                    self.PATHOGEN_LABEL)[1].strip()
            elif self.SYMPTOMS_LABEL in line:
                disease_info["symptoms"] = line.split(
                    self.SYMPTOMS_LABEL)[1].strip()
            elif self.SOURCE_LABEL in line:
                disease_info["source"] = line.split(
                    self.SOURCE_LABEL)[1].strip()
            elif self.LINK_LABEL in line:
                disease_info["reference"] = line.split(self.LINK_LABEL)[
                    1].strip()

        if disease_info:
            disease_info["category"] = category

        return disease_info if disease_info else None

    def _parse_varieties_info(self, content):
        """استخراج مواصفات الأصناف النباتية"""
        if "## مواصفات الأصناف النباتية" in content:
            section = content.split("## مواصفات الأصناف النباتية")[
                1].split("##")[0]
            varieties = []

            varieties.extend(
                self._parse_varieties_by_crop(
                    section,
                    "### أصناف الطماطم",
                    "tomato"))
            varieties.extend(
                self._parse_varieties_by_crop(
                    section, "### أصناف القمح", "wheat"))
            varieties.extend(
                self._parse_varieties_by_crop(
                    section, "### أصناف الأرز", "rice"))

            self.sources["crop_varieties"] = varieties

    def _parse_varieties_by_crop(self, section, crop_header, crop_name):
        """استخراج أصناف حسب المحصول"""
        varieties = []
        if crop_header in section:
            crop_section = section.split(crop_header)[1].split("###")[0]

            for variety in crop_section.split("\n\n"):
                variety_info = self._parse_variety_entry(variety, crop_name)
                if variety_info:
                    varieties.append(variety_info)

        return varieties

    def _parse_variety_entry(self, variety, crop):
        """استخراج معلومات صنف واحد"""
        if not (variety.strip() and "**" in variety):
            return None

        variety_info = {}
        lines = variety.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                variety_info["name"] = line.split("**")[1].strip()
            elif self.PROPERTIES_LABEL in line:
                variety_info["characteristics"] = line.split(
                    self.PROPERTIES_LABEL)[1].strip()
            elif self.SOURCE_LABEL in line:
                variety_info["source"] = line.split(
                    self.SOURCE_LABEL)[1].strip()
            elif self.LINK_LABEL in line:
                variety_info["reference"] = line.split(self.LINK_LABEL)[
                    1].strip()

        if variety_info:
            variety_info["crop"] = crop

        return variety_info if variety_info else None

    def _parse_hybridization_info(self, content):
        """استخراج طرق التهجين والتزاوج"""
        self._parse_hybridization_methods(content)
        self._parse_parent_specifications(content)

    def _parse_hybridization_methods(self, content):
        """استخراج طرق التهجين"""
        if "## طرق التهجين والتزاوج" in content:
            section = content.split("## طرق التهجين والتزاوج")[
                1].split("##")[0]
            methods = []

            for method in section.split("\n\n"):
                method_info = self._parse_method_entry(method)
                if method_info:
                    methods.append(method_info)

            self.sources["hybridization_methods"] = methods

    def _parse_method_entry(self, method):
        """استخراج معلومات طريقة تهجين واحدة"""
        if not (method.strip() and "**" in method):
            return None

        method_info = {}
        lines = method.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                method_info["name"] = line.split("**")[1].strip()
            elif "الوصف:" in line:
                method_info["description"] = line.split("الوصف:")[1].strip()
            elif self.SOURCE_LABEL in line:
                method_info["source"] = line.split(
                    self.SOURCE_LABEL)[1].strip()
            elif self.LINK_LABEL in line:
                method_info["reference"] = line.split(
                    self.LINK_LABEL)[1].strip()

        return method_info if method_info else None

    def _parse_parent_specifications(self, content):
        """استخراج مواصفات الآباء والأمهات"""
        if "## مواصفات الآباء والأمهات في عمليات التهجين" in content:
            section = content.split("## مواصفات الآباء والأمهات في عمليات التهجين")[
                1].split("##")[0]
            specifications = []

            for spec in section.split("\n\n"):
                spec_info = self._parse_spec_entry(spec)
                if spec_info:
                    specifications.append(spec_info)

            self.sources["parent_specifications"] = specifications

    def _parse_spec_entry(self, spec):
        """استخراج معلومات مواصفة واحدة"""
        if not (spec.strip() and "**" in spec):
            return None

        spec_info = {}
        lines = spec.strip().split("\n")

        for line in lines:
            if line.startswith(self.NUMBERED_LIST_START):
                spec_info["name"] = line.split("**")[1].strip()
            elif "الصفات المرغوبة:" in line:
                spec_info["desired_traits"] = line.split(
                    "الصفات المرغوبة:")[1].strip()
            elif self.SOURCE_LABEL in line:
                spec_info["source"] = line.split(self.SOURCE_LABEL)[1].strip()
            elif self.LINK_LABEL in line:
                spec_info["reference"] = line.split(self.LINK_LABEL)[1].strip()

        return spec_info if spec_info else None

    def update_knowledge_base_from_sources(self):
        """تحديث قاعدة المعرفة من المصادر"""
        try:
            # تحديث الأمراض
            self._update_diseases_from_sources()

            # تحديث المحاصيل
            self._update_crops_from_sources()

            # تحديث الأصناف
            self._update_varieties_from_sources()

            # تحديث معلومات التهجين
            self._update_hybridization_from_sources()

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم تحديث قاعدة المعرفة من المصادر")
            return True
        except Exception as e:
            logger.error(
                "خطأ أثناء تحديث قاعدة المعرفة من المصادر: %s",
                str(e))
            return False

    def _update_diseases_from_sources(self):
        """تحديث الأمراض من المصادر"""
        try:
            # تحديث الأمراض من معلومات الأمراض
            for disease_info in self.sources.get("disease_info", []):
                # استخراج معلومات المرض
                name = disease_info.get("name")
                pathogen = disease_info.get("pathogen")
                symptoms = disease_info.get("symptoms")
                category = disease_info.get("category")
                source = disease_info.get("source")
                reference = disease_info.get("reference")

                if not name or not pathogen:
                    continue

                # إنشاء معرف المرض
                disease_id = name.lower().replace(" ", "_").replace("-", "_")

                # تحديث المرض إذا كان موجوداً
                if disease_id in self.diseases:
                    # تحديث المعلومات
                    if source:
                        self.diseases[disease_id]["source"] = source
                    if reference:
                        self.diseases[disease_id]["reference"] = reference

                    # تحديث الأعراض
                    if symptoms:
                        symptoms_list = [s.strip()
                                         for s in symptoms.split(",")]
                        for symptom in symptoms_list:
                            if symptom not in self.diseases[disease_id].get(
                                    "symptoms", []):
                                if "symptoms" not in self.diseases[disease_id]:
                                    self.diseases[disease_id]["symptoms"] = []
                                self.diseases[disease_id]["symptoms"].append(
                                    symptom)
                else:
                    # إنشاء مرض جديد
                    new_disease = {
                        "name": name,
                        "scientific_name": pathogen,
                        "symptoms": [
                            s.strip() for s in symptoms.split(",")] if symptoms else [],
                        "source": source,
                        "reference": reference}

                    # تحديد المحاصيل المتأثرة بناءً على الفئة
                    if category == "vegetables":
                        new_disease["crops"] = [
                            "tomato", "cucumber", "pepper", "eggplant"]
                    elif category == "field_crops":
                        new_disease["crops"] = [
                            "wheat", "corn", "rice", "barley"]
                    elif category == "fruit_trees":
                        new_disease["crops"] = [
                            "apple", "peach", "citrus", "grape"]

                    # إضافة المرض إلى قاعدة المعرفة
                    self.diseases[disease_id] = new_disease

            logger.info("تم تحديث %d مرض من المصادر", len(self.diseases))
        except Exception as e:
            logger.error("خطأ أثناء تحديث الأمراض من المصادر: %s", str(e))

    def _update_crops_from_sources(self):
        """تحديث المحاصيل من المصادر"""
        try:
            # تحديث المحاصيل من أصناف المحاصيل
            for variety_info in self.sources.get("crop_varieties", []):
                # استخراج معلومات المحصول
                crop_type = variety_info.get("crop")

                if not crop_type:
                    continue

                # تحديث المحصول إذا كان موجوداً
                if crop_type in self.crops:
                    # تحديث المصدر والمرجع
                    source = variety_info.get("source")
                    reference = variety_info.get("reference")

                    if source:
                        self.crops[crop_type]["source"] = source
                    if reference:
                        self.crops[crop_type]["reference"] = reference
                else:
                    # إنشاء محصول جديد
                    new_crop = {
                        "name": crop_type.capitalize(),
                        "source": variety_info.get("source"),
                        "reference": variety_info.get("reference")
                    }

                    # إضافة المحصول إلى قاعدة المعرفة
                    self.crops[crop_type] = new_crop

            logger.info("تم تحديث %d محصول من المصادر", len(self.crops))
        except Exception as e:
            logger.error("خطأ أثناء تحديث المحاصيل من المصادر: %s", str(e))

    def _update_varieties_from_sources(self):
        """تحديث الأصناف من المصادر"""
        try:
            # تحديث الأصناف من أصناف المحاصيل
            for variety_info in self.sources.get("crop_varieties", []):
                # استخراج معلومات الصنف
                name = variety_info.get("name")
                crop_type = variety_info.get("crop")
                characteristics = variety_info.get("characteristics")
                source = variety_info.get("source")
                reference = variety_info.get("reference")

                if not name or not crop_type:
                    continue

                # إنشاء معرف الصنف
                variety_id = name.lower().replace(" ", "_").replace("-", "_")

                # التأكد من وجود المحصول في قاعدة المعرفة
                if crop_type not in self.varieties:
                    self.varieties[crop_type] = {}

                # تحديث الصنف إذا كان موجوداً
                if variety_id in self.varieties[crop_type]:
                    # تحديث المعلومات
                    if source:
                        self.varieties[crop_type][variety_id]["source"] = source
                    if reference:
                        self.varieties[crop_type][variety_id]["reference"] = reference
                    if characteristics:
                        self.varieties[crop_type][variety_id]["characteristics"] = characteristics
                else:
                    # إنشاء صنف جديد
                    new_variety = {
                        "name": name,
                        "characteristics": characteristics,
                        "source": source,
                        "reference": reference
                    }

                    # إضافة الصنف إلى قاعدة المعرفة
                    self.varieties[crop_type][variety_id] = new_variety

            logger.info(
                "تم تحديث أصناف %d محصول من المصادر", len(
                    self.varieties))
        except Exception as e:
            logger.error("خطأ أثناء تحديث الأصناف من المصادر: %s", str(e))

    def _update_hybridization_from_sources(self):
        """تحديث معلومات التهجين من المصادر"""
        try:
            # تحديث طرق التهجين
            if "methods" not in self.hybridization:
                self.hybridization["methods"] = {}

            for method_info in self.sources.get("hybridization_methods", []):
                # استخراج معلومات طريقة التهجين
                name = method_info.get("name")
                description = method_info.get("description")
                source = method_info.get("source")
                reference = method_info.get("reference")

                if not name:
                    continue

                # إنشاء معرف طريقة التهجين
                method_id = name.lower().replace(" ", "_").replace("-", "_")

                # تحديث طريقة التهجين إذا كانت موجودة
                if method_id in self.hybridization["methods"]:
                    # تحديث المعلومات
                    if source:
                        self.hybridization["methods"][method_id]["source"] = source
                    if reference:
                        self.hybridization["methods"][method_id]["reference"] = reference
                    if description:
                        self.hybridization["methods"][method_id]["description"] = description
                else:
                    # إنشاء طريقة تهجين جديدة
                    new_method = {
                        "name": name,
                        "description": description,
                        "source": source,
                        "reference": reference
                    }

                    # إضافة طريقة التهجين إلى قاعدة المعرفة
                    self.hybridization["methods"][method_id] = new_method

            # تحديث مواصفات الآباء والأمهات
            if "parent_selection" not in self.hybridization:
                self.hybridization["parent_selection"] = {}

            for spec_info in self.sources.get("parent_specifications", []):
                # استخراج معلومات مواصفات الآباء والأمهات
                name = spec_info.get("name")
                desired_traits = spec_info.get("desired_traits")
                source = spec_info.get("source")
                reference = spec_info.get("reference")

                if not name:
                    continue

                # استخراج نوع المحصول من الاسم
                crop_type = None
                if "آباء الطماطم" in name:
                    crop_type = "tomato"
                elif "آباء القمح" in name:
                    crop_type = "wheat"
                elif "آباء الأرز" in name:
                    crop_type = "rice"
                elif "آباء الذرة" in name:
                    crop_type = "corn"

                if not crop_type:
                    continue

                # التأكد من وجود المحصول في قاعدة المعرفة
                if crop_type not in self.hybridization["parent_selection"]:
                    self.hybridization["parent_selection"][crop_type] = {}

                # استخراج نوع الصفة من الاسم
                trait_type = None
                if "مقاومة الأمراض" in desired_traits:
                    trait_type = "disease_resistance"
                elif "مقاومة الجفاف" in desired_traits:
                    trait_type = "drought_tolerance"
                elif "جودة الثمار" in desired_traits:
                    trait_type = "fruit_quality"
                elif "محتوى البروتين" in desired_traits:
                    trait_type = "protein_content"

                if not trait_type:
                    trait_type = "general"

                # تحديث مواصفات الآباء والأمهات
                if trait_type in self.hybridization["parent_selection"][crop_type]:
                    # تحديث المعلومات
                    if source:
                        self.hybridization["parent_selection"][crop_type][trait_type]["source"] = source
                    if reference:
                        self.hybridization["parent_selection"][crop_type][trait_type]["reference"] = reference
                    if desired_traits:
                        self.hybridization["parent_selection"][crop_type][trait_type]["description"] = desired_traits
                else:
                    # إنشاء مواصفات جديدة
                    new_spec = {
                        "description": desired_traits,
                        "source": source,
                        "reference": reference
                    }

                    # إضافة المواصفات إلى قاعدة المعرفة
                    self.hybridization["parent_selection"][crop_type][trait_type] = new_spec

            logger.info("تم تحديث معلومات التهجين من المصادر")
        except Exception as e:
            logger.error(
                "خطأ أثناء تحديث معلومات التهجين من المصادر: %s",
                str(e))

    def get_disease_info(self, disease_id=None, crop_type=None, symptoms=None):
        """
        الحصول على معلومات الأمراض

        المعلمات:
            disease_id (str, optional): معرف المرض
            crop_type (str, optional): نوع المحصول
            symptoms (list, optional): قائمة الأعراض

        العائد:
            dict: معلومات الأمراض
        """
        try:
            # إذا تم تحديد معرف المرض
            if disease_id:
                if disease_id in self.diseases:
                    return {
                        "success": True,
                        "disease": self.diseases[disease_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"المرض {disease_id} غير موجود"
                    }

            # إذا تم تحديد نوع المحصول
            if crop_type:
                diseases = {}

                for disease_id, disease_info in self.diseases.items():
                    if crop_type in disease_info.get("crops", []):
                        diseases[disease_id] = disease_info

                return {
                    "success": True,
                    "diseases": diseases
                }

            # إذا تم تحديد الأعراض
            if symptoms:
                diseases = {}

                for disease_id, disease_info in self.diseases.items():
                    # التحقق من تطابق الأعراض
                    disease_symptoms = disease_info.get("symptoms", [])
                    matching_symptoms = [
                        s for s in symptoms if any(
                            s.lower() in ds.lower() for ds in disease_symptoms)]

                    if matching_symptoms:
                        diseases[disease_id] = disease_info
                        diseases[disease_id]["matching_symptoms"] = matching_symptoms
                        diseases[disease_id]["match_score"] = len(
                            matching_symptoms) / len(symptoms)

                # ترتيب الأمراض حسب درجة التطابق
                sorted_diseases = dict(
                    sorted(
                        diseases.items(),
                        key=lambda x: x[1].get(
                            "match_score",
                            0),
                        reverse=True))

                return {
                    "success": True,
                    "diseases": sorted_diseases
                }

            # إذا لم يتم تحديد أي معلمة
            return {
                "success": True,
                "diseases": self.diseases
            }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع معلومات الأمراض: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع معلومات الأمراض: {str(e)}"
            }

    def get_crop_info(self, crop_id=None, disease_id=None):
        """
        الحصول على معلومات المحاصيل

        المعلمات:
            crop_id (str, optional): معرف المحصول
            disease_id (str, optional): معرف المرض

        العائد:
            dict: معلومات المحاصيل
        """
        try:
            # إذا تم تحديد معرف المحصول
            if crop_id:
                if crop_id in self.crops:
                    return {
                        "success": True,
                        "crop": self.crops[crop_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"المحصول {crop_id} غير موجود"
                    }

            # إذا تم تحديد معرف المرض
            if disease_id:
                if disease_id in self.diseases:
                    crops = {}

                    for crop_id in self.diseases[disease_id].get("crops", []):
                        if crop_id in self.crops:
                            crops[crop_id] = self.crops[crop_id]

                    return {
                        "success": True,
                        "crops": crops
                    }
                else:
                    return {
                        "success": False,
                        "error": f"المرض {disease_id} غير موجود"
                    }

            # إذا لم يتم تحديد أي معلمة
            return {
                "success": True,
                "crops": self.crops
            }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع معلومات المحاصيل: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع معلومات المحاصيل: {str(e)}"
            }

    def get_treatment_info(self, treatment_id=None, disease_id=None):
        """
        الحصول على معلومات العلاجات

        المعلمات:
            treatment_id (str, optional): معرف العلاج
            disease_id (str, optional): معرف المرض

        العائد:
            dict: معلومات العلاجات
        """
        try:
            # إذا تم تحديد معرف العلاج
            if treatment_id:
                if treatment_id in self.treatments:
                    return {
                        "success": True,
                        "treatment": self.treatments[treatment_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"العلاج {treatment_id} غير موجود"
                    }

            # إذا تم تحديد معرف المرض
            if disease_id:
                if disease_id in self.diseases:
                    treatments = {}

                    for treatment_id in self.diseases[disease_id].get(
                            "treatments", []):
                        if treatment_id in self.treatments:
                            treatments[treatment_id] = self.treatments[treatment_id]

                    return {
                        "success": True,
                        "treatments": treatments
                    }
                else:
                    return {
                        "success": False,
                        "error": f"المرض {disease_id} غير موجود"
                    }

            # إذا لم يتم تحديد أي معلمة
            return {
                "success": True,
                "treatments": self.treatments
            }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع معلومات العلاجات: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع معلومات العلاجات: {str(e)}"
            }

    def get_variety_info(self, crop_id=None, variety_id=None):
        """
        الحصول على معلومات الأصناف

        المعلمات:
            crop_id (str, optional): معرف المحصول
            variety_id (str, optional): معرف الصنف

        العائد:
            dict: معلومات الأصناف
        """
        try:
            # إذا تم تحديد معرف المحصول والصنف
            if crop_id and variety_id:
                if crop_id in self.varieties and variety_id in self.varieties[crop_id]:
                    return {
                        "success": True,
                        "variety": self.varieties[crop_id][variety_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"الصنف {variety_id} للمحصول {crop_id} غير موجود"}

            # إذا تم تحديد معرف المحصول فقط
            if crop_id:
                if crop_id in self.varieties:
                    return {
                        "success": True,
                        "varieties": self.varieties[crop_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"المحصول {crop_id} غير موجود في قاعدة بيانات الأصناف"}

            # إذا لم يتم تحديد أي معلمة
            return {
                "success": True,
                "varieties": self.varieties
            }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع معلومات الأصناف: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع معلومات الأصناف: {str(e)}"
            }

    def get_hybridization_info(self, method_id=None, crop_id=None):
        """
        الحصول على معلومات التهجين

        المعلمات:
            method_id (str, optional): معرف طريقة التهجين
            crop_id (str, optional): معرف المحصول

        العائد:
            dict: معلومات التهجين
        """
        try:
            # إذا تم تحديد معرف طريقة التهجين
            if method_id:
                if "methods" in self.hybridization and method_id in self.hybridization[
                        "methods"]:
                    return {
                        "success": True,
                        "method": self.hybridization["methods"][method_id]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"طريقة التهجين {method_id} غير موجودة"
                    }

            # إذا تم تحديد معرف المحصول
            if crop_id:
                if "parent_selection" in self.hybridization and crop_id in self.hybridization[
                        "parent_selection"]:
                    return {
                        "success": True,
                        "parent_selection": self.hybridization["parent_selection"][crop_id]}
                else:
                    return {
                        "success": False,
                        "error": f"معلومات اختيار الآباء للمحصول {crop_id} غير موجودة"}

            # إذا لم يتم تحديد أي معلمة
            return {
                "success": True,
                "hybridization": self.hybridization
            }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع معلومات التهجين: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع معلومات التهجين: {str(e)}"
            }

    def get_sources(self, category=None):
        """
        الحصول على المصادر

        المعلمات:
            category (str, optional): فئة المصادر

        العائد:
            dict: المصادر
        """
        try:
            # إذا تم تحديد فئة المصادر
            if category:
                if category in self.sources:
                    return {
                        "success": True,
                        "sources": self.sources[category]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"فئة المصادر {category} غير موجودة"
                    }

            # إذا لم يتم تحديد أي معلمة
            return {
                "success": True,
                "sources": self.sources
            }
        except Exception as e:
            logger.error("خطأ أثناء استرجاع المصادر: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع المصادر: {str(e)}"
            }

    def add_disease(self, disease_id, disease_info):
        """
        إضافة مرض جديد

        المعلمات:
            disease_id (str): معرف المرض
            disease_info (dict): معلومات المرض

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود المرض
            if disease_id in self.diseases:
                logger.warning("المرض %s موجود بالفعل", disease_id)
                return False

            # إضافة المرض
            self.diseases[disease_id] = disease_info

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم إضافة المرض %s", disease_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء إضافة المرض: %s", str(e))
            return False

    def update_disease(self, disease_id, disease_info):
        """
        تحديث مرض

        المعلمات:
            disease_id (str): معرف المرض
            disease_info (dict): معلومات المرض

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود المرض
            if disease_id not in self.diseases:
                logger.warning("المرض %s غير موجود", disease_id)
                return False

            # تحديث المرض
            self.diseases[disease_id] = disease_info

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم تحديث المرض %s", disease_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تحديث المرض: %s", str(e))
            return False

    def add_crop(self, crop_id, crop_info):
        """
        إضافة محصول جديد

        المعلمات:
            crop_id (str): معرف المحصول
            crop_info (dict): معلومات المحصول

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود المحصول
            if crop_id in self.crops:
                logger.warning("المحصول %s موجود بالفعل", crop_id)
                return False

            # إضافة المحصول
            self.crops[crop_id] = crop_info

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم إضافة المحصول %s", crop_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء إضافة المحصول: %s", str(e))
            return False

    def update_crop(self, crop_id, crop_info):
        """
        تحديث محصول

        المعلمات:
            crop_id (str): معرف المحصول
            crop_info (dict): معلومات المحصول

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود المحصول
            if crop_id not in self.crops:
                logger.warning("المحصول %s غير موجود", crop_id)
                return False

            # تحديث المحصول
            self.crops[crop_id] = crop_info

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم تحديث المحصول %s", crop_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تحديث المحصول: %s", str(e))
            return False

    def add_variety(self, crop_id, variety_id, variety_info):
        """
        إضافة صنف جديد

        المعلمات:
            crop_id (str): معرف المحصول
            variety_id (str): معرف الصنف
            variety_info (dict): معلومات الصنف

        العائد:
            bool: نجاح العملية
        """
        try:
            # التأكد من وجود المحصول في قاعدة المعرفة
            if crop_id not in self.varieties:
                self.varieties[crop_id] = {}

            # التحقق من وجود الصنف
            if variety_id in self.varieties[crop_id]:
                logger.warning(
                    "الصنف %s للمحصول %s موجود بالفعل",
                    variety_id,
                    crop_id)
                return False

            # إضافة الصنف
            self.varieties[crop_id][variety_id] = variety_info

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم إضافة الصنف %s للمحصول %s", variety_id, crop_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء إضافة الصنف: %s", str(e))
            return False

    def update_variety(self, crop_id, variety_id, variety_info):
        """
        تحديث صنف

        المعلمات:
            crop_id (str): معرف المحصول
            variety_id (str): معرف الصنف
            variety_info (dict): معلومات الصنف

        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من وجود المحصول والصنف
            if crop_id not in self.varieties or variety_id not in self.varieties[crop_id]:
                logger.warning(
                    "الصنف %s للمحصول %s غير موجود",
                    variety_id,
                    crop_id)
                return False

            # تحديث الصنف
            self.varieties[crop_id][variety_id] = variety_info

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم تحديث الصنف %s للمحصول %s", variety_id, crop_id)
            return True
        except Exception as e:
            logger.error("خطأ أثناء تحديث الصنف: %s", str(e))
            return False

    def get_knowledge_base_stats(self):
        """
        الحصول على إحصائيات قاعدة المعرفة

        العائد:
            dict: إحصائيات قاعدة المعرفة
        """
        try:
            # عدد الأمراض
            num_diseases = len(self.diseases)

            # عدد المحاصيل
            num_crops = len(self.crops)

            # عدد العلاجات
            num_treatments = len(self.treatments)

            # عدد الأصناف
            num_varieties = sum(len(varieties)
                                for varieties in self.varieties.values())

            # عدد طرق التهجين
            num_hybridization_methods = len(
                self.hybridization.get("methods", {}))

            # تاريخ آخر تحديث
            last_updated = self.last_updated

            return {
                "success": True,
                "stats": {
                    "num_diseases": num_diseases,
                    "num_crops": num_crops,
                    "num_treatments": num_treatments,
                    "num_varieties": num_varieties,
                    "num_hybridization_methods": num_hybridization_methods,
                    "last_updated": last_updated
                }
            }
        except Exception as e:
            logger.error(
                "خطأ أثناء استرجاع إحصائيات قاعدة المعرفة: %s",
                str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استرجاع إحصائيات قاعدة المعرفة: {str(e)}"
            }

    def export_knowledge_base(self, export_dir=None):
        """
        تصدير قاعدة المعرفة

        المعلمات:
            export_dir (str, optional): مسار مجلد التصدير

        العائد:
            dict: نتيجة التصدير
        """
        try:
            # تحديد مسار مجلد التصدير
            if not export_dir:
                export_dir = os.path.join(os.path.dirname(
                    os.path.abspath(__file__)), 'export')

            # التأكد من وجود مجلد التصدير
            os.makedirs(export_dir, exist_ok=True)

            # تصدير قاعدة المعرفة كملف JSON
            export_file = os.path.join(export_dir, 'knowledge_base.json')

            # إنشاء قاموس قاعدة المعرفة
            knowledge_base = {
                "diseases": self.diseases,
                "crops": self.crops,
                "treatments": self.treatments,
                "varieties": self.varieties,
                "hybridization": self.hybridization,
                "sources": self.sources,
                "last_updated": self.last_updated
            }

            # حفظ قاعدة المعرفة
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

            logger.info("تم تصدير قاعدة المعرفة إلى %s", export_file)

            return {
                "success": True,
                "export_file": export_file
            }
        except Exception as e:
            logger.error("خطأ أثناء تصدير قاعدة المعرفة: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء تصدير قاعدة المعرفة: {str(e)}"
            }

    def import_knowledge_base(self, import_file):
        """
        استيراد قاعدة المعرفة

        المعلمات:
            import_file (str): مسار ملف الاستيراد

        العائد:
            dict: نتيجة الاستيراد
        """
        try:
            # التحقق من وجود ملف الاستيراد
            if not os.path.exists(import_file):
                logger.error("ملف الاستيراد غير موجود: %s", import_file)
                return {
                    "success": False,
                    "error": f"ملف الاستيراد غير موجود: {import_file}"
                }

            # استيراد قاعدة المعرفة
            with open(import_file, 'r', encoding='utf-8') as f:
                knowledge_base = json.load(f)

            # تحديث قاعدة المعرفة
            if "diseases" in knowledge_base:
                self.diseases = knowledge_base["diseases"]
            if "crops" in knowledge_base:
                self.crops = knowledge_base["crops"]
            if "treatments" in knowledge_base:
                self.treatments = knowledge_base["treatments"]
            if "varieties" in knowledge_base:
                self.varieties = knowledge_base["varieties"]
            if "hybridization" in knowledge_base:
                self.hybridization = knowledge_base["hybridization"]
            if "sources" in knowledge_base:
                self.sources = knowledge_base["sources"]
            if "last_updated" in knowledge_base:
                self.last_updated = knowledge_base["last_updated"]

            # حفظ قاعدة المعرفة
            self._save_knowledge_base()

            logger.info("تم استيراد قاعدة المعرفة من %s", import_file)

            return {
                "success": True,
                "message": f"تم استيراد قاعدة المعرفة من {import_file}"
            }
        except Exception as e:
            logger.error("خطأ أثناء استيراد قاعدة المعرفة: %s", str(e))
            return {
                "success": False,
                "error": f"خطأ أثناء استيراد قاعدة المعرفة: {str(e)}"
            }
