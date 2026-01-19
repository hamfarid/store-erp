"""
نظام إدارة مصادر البيانات للأمراض والإصابات
Data Sources Management System for Plant Diseases
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class DataSource:
    """مصدر بيانات واحد"""

    def __init__(
        self,
        name: str,
        url: str,
        source_type: str,
        language: str = "en",
        reliability: float = 0.8,
        update_frequency: str = "weekly"
    ):
        self.name = name
        self.url = url
        self.source_type = source_type  # academic, government, commercial, community
        self.language = language
        self.reliability = reliability
        self.update_frequency = update_frequency
        self.last_updated = None


# المصادر الموثوقة للأمراض والإصابات
TRUSTED_DATA_SOURCES = [
    # المصادر الأكاديمية والبحثية
    DataSource(
        name="PlantVillage",
        url="https://plantvillage.psu.edu/",
        source_type="academic",
        language="en",
        reliability=0.95,
        update_frequency="monthly"
    ),
    DataSource(
        name="CABI - Centre for Agriculture and Bioscience International",
        url="https://www.cabi.org/isc/",
        source_type="academic",
        language="en",
        reliability=0.98,
        update_frequency="monthly"
    ),
    DataSource(
        name="EPPO - European and Mediterranean Plant Protection Organization",
        url="https://www.eppo.int/",
        source_type="government",
        language="en",
        reliability=0.97,
        update_frequency="monthly"
    ),
    DataSource(
        name="FAO - Food and Agriculture Organization",
        url="https://www.fao.org/plant-health/",
        source_type="government",
        language="en",
        reliability=0.98,
        update_frequency="quarterly"
    ),

    # المصادر الحكومية
    DataSource(
        name="USDA - United States Department of Agriculture",
        url="https://www.ars.usda.gov/",
        source_type="government",
        language="en",
        reliability=0.97,
        update_frequency="monthly"
    ),
    DataSource(
        name="Cornell University - Plant Disease Diagnostic Clinic",
        url="https://plantclinic.cornell.edu/",
        source_type="academic",
        language="en",
        reliability=0.96,
        update_frequency="weekly"
    ),
    DataSource(
        name="University of California IPM",
        url="http://ipm.ucanr.edu/",
        source_type="academic",
        language="en",
        reliability=0.95,
        update_frequency="monthly"
    ),

    # قواعد البيانات المتخصصة
    DataSource(
        name="Invasive Species Compendium",
        url="https://www.cabi.org/isc/",
        source_type="academic",
        language="en",
        reliability=0.96,
        update_frequency="monthly"
    ),
    DataSource(
        name="PaDIL - Pests and Diseases Image Library",
        url="https://www.padil.gov.au/",
        source_type="government",
        language="en",
        reliability=0.94,
        update_frequency="monthly"
    ),
    DataSource(
        name="Bugwood Images",
        url="https://www.forestryimages.org/",
        source_type="academic",
        language="en",
        reliability=0.93,
        update_frequency="weekly"
    ),

    # مصادر عربية
    DataSource(
        name="المنظمة العربية للتنمية الزراعية",
        url="https://www.aoad.org/",
        source_type="government",
        language="ar",
        reliability=0.90,
        update_frequency="quarterly"
    ),
    DataSource(
        name="المركز الدولي للبحوث الزراعية في المناطق الجافة (إيكاردا)",
        url="https://www.icarda.org/",
        source_type="academic",
        language="ar",
        reliability=0.92,
        update_frequency="monthly"
    ),

    # مصادر الصور
    DataSource(
        name="Google Images - Plant Diseases",
        url="https://www.google.com/imghp",
        source_type="commercial",
        language="en",
        reliability=0.70,
        update_frequency="daily"
    ),
    DataSource(
        name="Bing Images - Plant Diseases",
        url="https://www.bing.com/images",
        source_type="commercial",
        language="en",
        reliability=0.70,
        update_frequency="daily"
    ),
    DataSource(
        name="Unsplash - Agriculture",
        url="https://unsplash.com/s/photos/plant-disease",
        source_type="community",
        language="en",
        reliability=0.65,
        update_frequency="daily"
    ),
    DataSource(
        name="Flickr - Plant Pathology",
        url="https://www.flickr.com/search/?text=plant%20disease",
        source_type="community",
        language="en",
        reliability=0.65,
        update_frequency="daily"
    ),

    # مصادر نقص العناصر
    DataSource(
        name="Plant Nutrient Deficiency Symptoms",
        url="https://extension.psu.edu/plant-nutrient-deficiency-symptoms",
        source_type="academic",
        language="en",
        reliability=0.94,
        update_frequency="yearly"
    ),
    DataSource(
        name="Nutrient Deficiencies in Plants",
        url="https://www.agric.wa.gov.au/",
        source_type="government",
        language="en",
        reliability=0.93,
        update_frequency="yearly"
    ),
]


class DataSourceManager:
    """مدير مصادر البيانات"""

    def __init__(self):
        self.sources = TRUSTED_DATA_SOURCES
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def get_sources_by_type(self, source_type: str) -> List[DataSource]:
        """الحصول على المصادر حسب النوع"""
        return [s for s in self.sources if s.source_type == source_type]

    def get_sources_by_language(self, language: str) -> List[DataSource]:
        """الحصول على المصادر حسب اللغة"""
        return [s for s in self.sources if s.language == language]

    def get_high_reliability_sources(self, min_reliability: float = 0.9) -> List[DataSource]:
        """الحصول على المصادر عالية الموثوقية"""
        return [s for s in self.sources if s.reliability >= min_reliability]

    async def check_source_availability(self, source: DataSource) -> bool:
        """التحقق من توفر المصدر"""
        try:
            async with self.session.get(source.url, timeout=10) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Error checking source {source.name}: {e}")
            return False

    async def fetch_disease_info(
        self,
        disease_name: str,
        source: DataSource
    ) -> Optional[Dict]:
        """جلب معلومات المرض من مصدر محدد"""
        try:
            # هذه دالة عامة، يجب تخصيصها لكل مصدر
            search_url = f"{source.url}/search?q={disease_name}"

            async with self.session.get(search_url, timeout=15) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # استخراج المعلومات (يجب تخصيصها لكل موقع)
                    return {
                        "source": source.name,
                        "url": search_url,
                        "disease_name": disease_name,
                        "fetched_at": datetime.utcnow().isoformat(),
                        "reliability": source.reliability,
                        "raw_html": html[:1000]  # أول 1000 حرف
                    }
        except Exception as e:
            logger.error(f"Error fetching from {source.name}: {e}")
            return None

    def get_recommended_sources_for_disease(
        self,
        disease_name: str,
        max_sources: int = 5
    ) -> List[DataSource]:
        """الحصول على المصادر الموصى بها لمرض معين"""
        # ترتيب المصادر حسب الموثوقية
        sorted_sources = sorted(
            self.sources,
            key=lambda x: x.reliability,
            reverse=True
        )

        # إعطاء الأولوية للمصادر الأكاديمية والحكومية
        academic_gov = [
            s for s in sorted_sources
            if s.source_type in ["academic", "government"]
        ]

        return academic_gov[:max_sources]

    def get_image_sources(self) -> List[DataSource]:
        """الحصول على مصادر الصور"""
        return [
            s for s in self.sources
            if "image" in s.name.lower() or s.source_type == "community"
        ]

    def export_sources_list(self) -> List[Dict]:
        """تصدير قائمة المصادر"""
        return [
            {
                "name": s.name,
                "url": s.url,
                "type": s.source_type,
                "language": s.language,
                "reliability": s.reliability,
                "update_frequency": s.update_frequency
            }
            for s in self.sources
        ]


# دالة مساعدة للحصول على المدير
def get_data_source_manager() -> DataSourceManager:
    """الحصول على مدير مصادر البيانات"""
    return DataSourceManager()


# قائمة الأمراض الشائعة للبحث
COMMON_PLANT_DISEASES = [
    # أمراض فطرية
    "Powdery Mildew", "البياض الدقيقي",
    "Downy Mildew", "البياض الزغبي",
    "Rust", "الصدأ",
    "Leaf Spot", "بقعة الأوراق",
    "Anthracnose", "أنثراكنوز",
    "Blight", "اللفحة",
    "Root Rot", "تعفن الجذور",
    "Fusarium Wilt", "ذبول الفيوزاريوم",
    "Verticillium Wilt", "ذبول الفيرتيسيليوم",

    # أمراض بكتيرية
    "Bacterial Leaf Spot", "البقعة البكتيرية",
    "Bacterial Wilt", "الذبول البكتيري",
    "Fire Blight", "اللفحة النارية",
    "Crown Gall", "التاج المتورم",

    # أمراض فيروسية
    "Mosaic Virus", "فيروس الموزاييك",
    "Leaf Curl", "تجعد الأوراق",
    "Yellow Dwarf", "التقزم الأصفر",

    # نقص العناصر
    "Nitrogen Deficiency", "نقص النيتروجين",
    "Phosphorus Deficiency", "نقص الفوسفور",
    "Potassium Deficiency", "نقص البوتاسيوم",
    "Iron Deficiency", "نقص الحديد",
    "Magnesium Deficiency", "نقص المغنيسيوم",
    "Calcium Deficiency", "نقص الكالسيوم",
    "Zinc Deficiency", "نقص الزنك",
    "Manganese Deficiency", "نقص المنجنيز",
]


# قائمة المحاصيل الرئيسية
MAJOR_CROPS = [
    "Tomato", "طماطم",
    "Potato", "بطاطس",
    "Wheat", "قمح",
    "Corn", "ذرة",
    "Rice", "أرز",
    "Soybean", "فول الصويا",
    "Cotton", "قطن",
    "Apple", "تفاح",
    "Grape", "عنب",
    "Citrus", "حمضيات",
    "Cucumber", "خيار",
    "Pepper", "فلفل",
    "Lettuce", "خس",
    "Strawberry", "فراولة",
]
