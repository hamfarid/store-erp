# File: /home/ubuntu/clean_project/src/api/plant_hybridization.py
"""
واجهة برمجة التطبيقات لتهجين النباتات
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import uuid
from datetime import datetime

router = APIRouter()

# بيانات وهمية للإحصائيات
hybridization_stats = {
    "total_simulations": 342,
    "successful_crosses": 287,
    "plant_varieties": 45,
    "success_rate": 84
}

# بيانات النباتات المتاحة
available_plants = [
    {
        "id": 1,
        "name": "طماطم شيري",
        "variety": "Solanum lycopersicum var. cerasiforme",
        "image": "/api/images/plants/cherry_tomato.jpg",
        "thumbnail": "/api/images/plants/thumbnails/cherry_tomato.jpg",
        "traits": ["مقاومة الأمراض", "إنتاج عالي", "طعم حلو"],
        "main_traits": ["مقاومة", "إنتاج"]
    },
    {
        "id": 2,
        "name": "طماطم كبيرة",
        "variety": "Solanum lycopersicum var. grandifolium",
        "image": "/api/images/plants/large_tomato.jpg",
        "thumbnail": "/api/images/plants/thumbnails/large_tomato.jpg",
        "traits": ["حجم كبير", "جودة عالية", "مقاومة الحشرات"],
        "main_traits": ["حجم", "جودة"]
    },
    {
        "id": 3,
        "name": "بطاطس حمراء",
        "variety": "Solanum tuberosum var. rubrum",
        "image": "/api/images/plants/red_potato.jpg",
        "thumbnail": "/api/images/plants/thumbnails/red_potato.jpg",
        "traits": ["مقاومة الجفاف", "نضج مبكر", "قيمة غذائية عالية"],
        "main_traits": ["مقاومة", "نضج"]
    },
    {
        "id": 4,
        "name": "ذرة صفراء",
        "variety": "Zea mays var. saccharata",
        "image": "/api/images/plants/yellow_corn.jpg",
        "thumbnail": "/api/images/plants/thumbnails/yellow_corn.jpg",
        "traits": ["إنتاج عالي", "مقاومة الآفات", "طعم حلو"],
        "main_traits": ["إنتاج", "مقاومة"]
    }
]

# سجل التهجينات
hybridization_history = [
    {
        "id": 1,
        "parent1": available_plants[0],
        "parent2": available_plants[1],
        "type": "simple",
        "offspring_count": 12,
        "success_rate": 87,
        "status": "completed",
        "created_at": "2024-01-15T10:30:00Z",
        "settings": {
            "type": "simple",
            "generations": 1,
            "sample_size": "medium"
        }
    },
    {
        "id": 2,
        "parent1": available_plants[2],
        "parent2": available_plants[3],
        "type": "backcross",
        "offspring_count": 8,
        "success_rate": 92,
        "status": "completed",
        "created_at": "2024-01-14T15:45:00Z",
        "settings": {
            "type": "backcross",
            "generations": 2,
            "sample_size": "large"
        }
    }
]


@router.get("/stats")
async def get_hybridization_stats():
    """الحصول على إحصائيات التهجين"""
    return {"data": hybridization_stats}


@router.get("/plants")
async def get_available_plants():
    """الحصول على النباتات المتاحة للتهجين"""
    return {"data": available_plants}


@router.post("/simulate")
async def simulate_hybridization(data: Dict[str, Any]):
    """محاكاة عملية التهجين"""
    try:
        parent1_id = data.get("parent1_id")
        parent2_id = data.get("parent2_id")
        settings = data.get("settings", {})

        # البحث عن النباتات الأبوية
        parent1 = next((p for p in available_plants if p["id"] == parent1_id), None)
        parent2 = next((p for p in available_plants if p["id"] == parent2_id), None)

        if not parent1 or not parent2:
            raise HTTPException(status_code=404, detail="النباتات الأبوية غير موجودة")

        # محاكاة نتائج التهجين
        offspring = []

        # إنشاء نتائج وهمية للنسل
        for i in range(3):  # 3 نتائج محتملة
            offspring_item = {
                "id": i + 1,
                "name": f"هجين {parent1['name']} × {parent2['name']} - النوع {i + 1}",
                "predicted_image": f"/api/images/offspring/hybrid_{uuid.uuid4()}.jpg",
                "probability": 85 - (i * 15),  # احتمالية متناقصة
                "traits": [
                    "مقاومة الأمراض",
                    "إنتاج عالي",
                    "جودة محسنة",
                    "نضج مبكر"
                ][:3-i]  # عدد متناقص من الصفات
            }
            offspring.append(offspring_item)

        result = {
            "simulation_id": str(uuid.uuid4()),
            "parent1": parent1,
            "parent2": parent2,
            "offspring": offspring,
            "success_probability": 87,
            "estimated_time": "3-4 أشهر",
            "processing_time": 1.2,
            "model_accuracy": 91
        }

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في محاكاة التهجين: {str(e)}")


@router.get("/history")
async def get_hybridization_history():
    """الحصول على سجل التهجينات"""
    return {"data": hybridization_history}


@router.post("/save")
async def save_hybridization(data: Dict[str, Any]):
    """حفظ نتائج التهجين"""
    try:
        new_record = {
            "id": len(hybridization_history) + 1,
            "parent1": data.get("parent1"),
            "parent2": data.get("parent2"),
            "type": data.get("settings", {}).get("type", "simple"),
            "offspring_count": len(data.get("result", {}).get("offspring", [])),
            "success_rate": data.get("result", {}).get("success_probability", 0),
            "status": "completed",
            "created_at": datetime.now().isoformat() + "Z",
            "settings": data.get("settings", {})
        }

        hybridization_history.append(new_record)

        return {"message": "تم حفظ نتائج التهجين بنجاح"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في حفظ التهجين: {str(e)}")


@router.delete("/history/{record_id}")
async def delete_hybridization(record_id: int):
    """حذف سجل تهجين"""
    try:
        global hybridization_history
        hybridization_history = [record for record in hybridization_history if record["id"] != record_id]
        return {"message": "تم حذف سجل التهجين بنجاح"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في حذف السجل: {str(e)}")


@router.get("/export/history")
async def export_history():
    """تصدير سجل التهجينات"""
    try:
        # محاكاة تصدير السجل كملف Excel
        return {
            "data": "محتوى ملف Excel",
            "filename": f"hybridization-history-{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تصدير السجل: {str(e)}")


@router.get("/report/{record_id}")
async def download_report(record_id: int):
    """تحميل تقرير التهجين"""
    try:
        record = next((r for r in hybridization_history if r["id"] == record_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="سجل التهجين غير موجود")

        # محاكاة إنشاء تقرير PDF
        return {
            "data": "محتوى ملف PDF",
            "filename": f"hybridization-report-{record_id}.pdf"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تحميل التقرير: {str(e)}")
