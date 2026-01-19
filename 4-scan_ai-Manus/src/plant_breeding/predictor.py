#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التنبؤ بنتائج التهجين وتزاوج النباتات
=========================================

توفر هذه الوحدة وظائف لتحليل خصائص السلالات النباتية والتنبؤ بنتائج التهجين،
مع دعم البحث عن معلومات إضافية من مصادر موثوقة.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import json
import logging
import random
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

# استيراد وحدات أخرى (سيتم إنشاؤها لاحقًا)
# from src.data_collection.web_scraper import WebScraper
# from src.database.manager import DatabaseManager

# إعداد السجل
logger = logging.getLogger("agricultural_ai.breeding_predictor")

class BreedingPredictor:
    """فئة للتنبؤ بنتائج تهجين النباتات"""
    
    def __init__(self, config: Dict):
        """تهيئة متنبئ التهجين
        
        المعاملات:
            config (Dict): تكوين متنبئ التهجين
        """
        self.config = config
        self.model_base_path = self.config.get("model_path", "models/plant_breeding")
        self.database_config = self.config.get("database", {})
        self.web_search_config = self.config.get("web_search", {})
        self.simulation_config = self.config.get("simulation", {})
        
        # تهيئة مكونات أخرى (سيتم تفعيلها لاحقًا)
        # self.db_manager = DatabaseManager(self.database_config)
        # self.web_scraper = WebScraper(self.web_search_config) if self.web_search_config.get("enable") else None
        
        # تحميل بيانات السلالات (مثال باستخدام ملف JSON)
        self.strains_data = self._load_strains_data()
        
        logger.info("تم تهيئة متنبئ التهجين")

    def _load_strains_data(self) -> Dict:
        """تحميل بيانات السلالات من قاعدة البيانات (ملف JSON كمثال)"""
        strains_data = {}
        db_path = self.database_config.get("strains_db", "database/plant_strains.db").replace(".db", ".json")
        if os.path.exists(db_path):
            try:
                with open(db_path, "r", encoding="utf-8") as f:
                    strains_data = json.load(f)
                logger.info(f"تم تحميل بيانات السلالات من: {db_path}")
            except Exception as e:
                logger.error(f"فشل في تحميل بيانات السلالات من {db_path}: {str(e)}")
        else:
            logger.warning(f"ملف بيانات السلالات غير موجود: {db_path}")
        return strains_data

    def get_strain_info(self, strain_name: str) -> Optional[Dict]:
        """الحصول على معلومات سلالة معينة"""
        return self.strains_data.get(strain_name)

    def _predict_mendelian_trait(self, parent1_genotype: str, parent2_genotype: str) -> Dict[str, float]:
        """التنبؤ بنتيجة تهجين صفة مندلية بسيطة (مثال)
        
        المعاملات:
            parent1_genotype (str): التركيب الوراثي للأب 1 (مثل AA, Aa, aa)
            parent2_genotype (str): التركيب الوراثي للأب 2
            
        الإرجاع:
            Dict[str, float]: احتمالات التراكيب الوراثية للجيل الأول
        """
        if len(parent1_genotype) != 2 or len(parent2_genotype) != 2:
            raise ValueError("التركيب الوراثي يجب أن يتكون من حرفين")
            
        # الحصول على الأليلات من كل أب
        alleles1 = list(parent1_genotype)
        alleles2 = list(parent2_genotype)
        
        # إنشاء مربع بانيت
        offspring_genotypes = {}
        total_combinations = 0
        
        for allele1 in alleles1:
            for allele2 in alleles2:
                # ترتيب الأليلات (الحرف الكبير أولاً)
                genotype = "".join(sorted([allele1, allele2], key=lambda x: x.islower()))
                offspring_genotypes[genotype] = offspring_genotypes.get(genotype, 0) + 1
                total_combinations += 1
        
        # حساب الاحتمالات
        probabilities = {geno: count / total_combinations for geno, count in offspring_genotypes.items()}
        return probabilities

    def _predict_quantitative_trait(self, parent1_value: float, parent2_value: float, heritability: float = 0.5) -> float:
        """التنبؤ بقيمة صفة كمية في الجيل الأول (مثال بسيط)
        
        المعاملات:
            parent1_value (float): قيمة الصفة للأب 1
            parent2_value (float): قيمة الصفة للأب 2
            heritability (float): معامل التوريث (0-1)
            
        الإرجاع:
            float: القيمة المتوقعة للصفة في الجيل الأول
        """
        # نموذج بسيط يعتمد على المتوسط ومعامل التوريث
        mid_parent_value = (parent1_value + parent2_value) / 2
        # التنبؤ يمكن أن يكون أكثر تعقيدًا، هذا مجرد مثال
        predicted_value = mid_parent_value # أبسط تنبؤ هو المتوسط
        # يمكن إضافة تأثير التوريث والتباين الوراثي
        # predicted_value = population_mean + heritability * (mid_parent_value - population_mean)
        return predicted_value

    def predict_hybridization(self, parent1_name: str, parent2_name: str) -> Dict[str, Any]:
        """التنبؤ بنتائج تهجين سلالتين
        
        المعاملات:
            parent1_name (str): اسم السلالة الأولى
            parent2_name (str): اسم السلالة الثانية
            
        الإرجاع:
            Dict[str, Any]: نتائج التنبؤ المتوقعة
        """
        parent1_info = self.get_strain_info(parent1_name)
        parent2_info = self.get_strain_info(parent2_name)
        
        if not parent1_info or not parent2_info:
            missing = []
            if not parent1_info: missing.append(parent1_name)
            if not parent2_info: missing.append(parent2_name)
            return {"error": f"لم يتم العثور على معلومات للسلالات: {', '.join(missing)}"}
        
        predictions = {
            "parent1": parent1_info,
            "parent2": parent2_info,
            "predicted_offspring": {
                "mendelian_traits": {},
                "quantitative_traits": {}
            },
            "simulation_results": None,
            "external_info": None
        }
        
        # التنبؤ بالصفات المندلية (مثال لصفة واحدة)
        trait_name_mendelian = "Flower Color" # مثال
        geno1 = parent1_info.get("genotypes", {}).get(trait_name_mendelian)
        geno2 = parent2_info.get("genotypes", {}).get(trait_name_mendelian)
        
        if geno1 and geno2:
            try:
                mendelian_prediction = self._predict_mendelian_trait(geno1, geno2)
                predictions["predicted_offspring"]["mendelian_traits"][trait_name_mendelian] = mendelian_prediction
            except ValueError as e:
                logger.warning(f"خطأ في التنبؤ بالصفة المندلية ", {trait_name_mendelian}": {e}")
        
        # التنبؤ بالصفات الكمية (مثال لصفة واحدة)
        trait_name_quantitative = "Yield" # مثال
        value1 = parent1_info.get("phenotypes", {}).get(trait_name_quantitative)
        value2 = parent2_info.get("phenotypes", {}).get(trait_name_quantitative)
        heritability = parent1_info.get("heritability", {}).get(trait_name_quantitative, 0.5) # استخدام قيمة افتراضية
        
        if value1 is not None and value2 is not None:
            quantitative_prediction = self._predict_quantitative_trait(value1, value2, heritability)
            predictions["predicted_offspring"]["quantitative_traits"][trait_name_quantitative] = quantitative_prediction
            
        # إجراء محاكاة مونت كارلو (إذا تم تكوينها)
        if self.simulation_config.get("monte_carlo_iterations", 0) > 0:
            predictions["simulation_results"] = self._run_monte_carlo_simulation(parent1_info, parent2_info)
            
        # البحث عن معلومات إضافية من الويب (إذا تم تفعيله)
        # if self.web_scraper:
        #     query = f"hybridization results {parent1_name} x {parent2_name}"
        #     search_results = self.web_scraper.search(query, max_results=self.web_search_config.get("max_results", 10))
        #     predictions["external_info"] = search_results
        # else:
        #     predictions["external_info"] = "Web search is disabled."
        
        return predictions

    def _run_monte_carlo_simulation(self, parent1_info: Dict, parent2_info: Dict) -> Dict:
        """إجراء محاكاة مونت كارلو لنتائج التهجين"""
        iterations = self.simulation_config.get("monte_carlo_iterations", 1000)
        confidence_interval = self.simulation_config.get("confidence_interval", 0.95)
        
        simulation_results = {
            "iterations": iterations,
            "quantitative_traits_distribution": {}
        }
        
        # محاكاة صفة كمية واحدة كمثال
        trait_name = "Yield"
        value1 = parent1_info.get("phenotypes", {}).get(trait_name)
        value2 = parent2_info.get("phenotypes", {}).get(trait_name)
        # افتراض وجود تباين حول القيمة المتوسطة
        std_dev1 = parent1_info.get("phenotype_std_dev", {}).get(trait_name, value1 * 0.1 if value1 else 0)
        std_dev2 = parent2_info.get("phenotype_std_dev", {}).get(trait_name, value2 * 0.1 if value2 else 0)
        heritability = parent1_info.get("heritability", {}).get(trait_name, 0.5)
        
        if value1 is not None and value2 is not None:
            offspring_values = []
            for _ in range(iterations):
                # اختيار قيم عشوائية للآباء بناءً على التوزيع الطبيعي
                sim_parent1_val = np.random.normal(value1, std_dev1)
                sim_parent2_val = np.random.normal(value2, std_dev2)
                
                # التنبؤ بقيمة الجيل الأول (باستخدام نموذج بسيط)
                mid_parent = (sim_parent1_val + sim_parent2_val) / 2
                # إضافة تباين بيئي ووراثي
                environmental_variance = (1 - heritability) * np.mean([std_dev1**2, std_dev2**2])
                genetic_variance = heritability * np.var([sim_parent1_val, sim_parent2_val]) # تقدير بسيط
                total_variance = environmental_variance + genetic_variance
                
                sim_offspring_val = np.random.normal(mid_parent, np.sqrt(total_variance))
                offspring_values.append(sim_offspring_val)
            
            # حساب الإحصائيات
            mean_value = np.mean(offspring_values)
            std_dev_value = np.std(offspring_values)
            # حساب فترة الثقة
            alpha = 1.0 - confidence_interval
            z_score = np.abs(np.percentile(np.random.standard_normal(10000), alpha / 2 * 100))
            margin_of_error = z_score * (std_dev_value / np.sqrt(iterations))
            ci_lower = mean_value - margin_of_error
            ci_upper = mean_value + margin_of_error
            
            simulation_results["quantitative_traits_distribution"][trait_name] = {
                "mean": float(mean_value),
                "std_dev": float(std_dev_value),
                "min": float(np.min(offspring_values)),
                "max": float(np.max(offspring_values)),
                "confidence_interval": [float(ci_lower), float(ci_upper)],
                "confidence_level": confidence_interval
            }
            
        return simulation_results

    def suggest_breeding_pairs(self, target_trait: str, target_value: float, 
                              num_suggestions: int = 5) -> List[Dict]:
        """اقتراح أزواج تهجين لتحقيق صفة مستهدفة"""
        suggestions = []
        available_strains = list(self.strains_data.keys())
        
        if len(available_strains) < 2:
            return {"error": "لا توجد سلالات كافية لتقديم اقتراحات"}
        
        # تقييم جميع الأزواج الممكنة
        pair_scores = []
        for i in range(len(available_strains)):
            for j in range(i + 1, len(available_strains)):
                parent1_name = available_strains[i]
                parent2_name = available_strains[j]
                
                parent1_info = self.strains_data[parent1_name]
                parent2_info = self.strains_data[parent2_name]
                
                # الحصول على قيم الصفة المستهدفة للآباء
                value1 = parent1_info.get("phenotypes", {}).get(target_trait)
                value2 = parent2_info.get("phenotypes", {}).get(target_trait)
                heritability = parent1_info.get("heritability", {}).get(target_trait, 0.5)
                
                if value1 is not None and value2 is not None:
                    # التنبؤ بالقيمة المتوقعة للجيل الأول
                    predicted_value = self._predict_quantitative_trait(value1, value2, heritability)
                    
                    # حساب درجة القرب من القيمة المستهدفة
                    score = abs(predicted_value - target_value)
                    pair_scores.append({
                        "parent1": parent1_name,
                        "parent2": parent2_name,
                        "predicted_value": predicted_value,
                        "score": score
                    })
        
        # ترتيب الأزواج حسب القرب من الهدف
        pair_scores = sorted(pair_scores, key=lambda x: x["score"])
        
        # إرجاع أفضل الاقتراحات
        return pair_scores[:num_suggestions]

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "model_path": "../../models/plant_breeding", # مسار نسبي
        "database": {
            "strains_db": "../../database/plant_strains.db" # مسار نسبي
        },
        "web_search": {
            "enable": False # تعطيل البحث على الويب في المثال
        },
        "simulation": {
            "monte_carlo_iterations": 1000,
            "confidence_interval": 0.95
        }
    }
    
    # إنشاء مجلدات وهمية وقاعدة بيانات (للتجربة فقط)
    os.makedirs("../../models/plant_breeding", exist_ok=True)
    os.makedirs("../../database", exist_ok=True)
    
    # إنشاء ملف قاعدة بيانات سلالات وهمي (JSON)
    strains_db_data = {
        "Strain A": {
            "genotypes": {"Flower Color": "AA"},
            "phenotypes": {"Yield": 100, "Height": 50},
            "phenotype_std_dev": {"Yield": 10, "Height": 5},
            "heritability": {"Yield": 0.6, "Height": 0.8}
        },
        "Strain B": {
            "genotypes": {"Flower Color": "aa"},
            "phenotypes": {"Yield": 150, "Height": 60},
            "phenotype_std_dev": {"Yield": 15, "Height": 6},
            "heritability": {"Yield": 0.6, "Height": 0.8}
        },
        "Strain C": {
            "genotypes": {"Flower Color": "Aa"},
            "phenotypes": {"Yield": 120, "Height": 55},
            "phenotype_std_dev": {"Yield": 12, "Height": 5.5},
            "heritability": {"Yield": 0.6, "Height": 0.8}
        }
    }
    db_path_json = dummy_config["database"]["strains_db"].replace(".db", ".json")
    with open(db_path_json, "w", encoding="utf-8") as f:
        json.dump(strains_db_data, f, ensure_ascii=False, indent=4)
        
    # تهيئة المتنبئ
    predictor = BreedingPredictor(dummy_config)
    
    # التنبؤ بتهجين سلالتين
    parent1 = "Strain A"
    parent2 = "Strain B"
    prediction_results = predictor.predict_hybridization(parent1, parent2)
    
    print(f"\nنتائج التنبؤ لتهجين {parent1} x {parent2}:")
    print(json.dumps(prediction_results, indent=4, ensure_ascii=False))
    
    # اقتراح أزواج تهجين
    target_trait = "Yield"
    target_value = 130
    suggestions = predictor.suggest_breeding_pairs(target_trait, target_value)
    
    print(f"\nأفضل أزواج التهجين المقترحة للحصول على {target_trait} قريب من {target_value}:")
    print(json.dumps(suggestions, indent=4, ensure_ascii=False))
    
    # تنظيف الملفات الوهمية (اختياري)
    # import shutil
    # shutil.rmtree("../../models")
    # shutil.rmtree("../../database")
    # logger.info("تم حذف الملفات والمجلدات الوهمية")
