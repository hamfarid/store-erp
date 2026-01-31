"""
FILE: backend/src/api/v1/analytics.py | PURPOSE: Analytics API routes
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

Analytics API Routes - Advanced Analytics Dashboard

Handles analytics, insights, heatmaps, predictions, and comparative analysis.

Version: 2.0.0 - Added advanced analytics (heatmap, comparative, predictions)
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.diagnosis import Diagnosis
from ...models.disease import Disease
from ...models.farm import Farm
from ...models.sensor import Sensor
from ...models.user import User
from .auth import get_current_user

# Router
router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


# Pydantic Schemas
class DashboardMetrics(BaseModel):
    total_farms: int
    total_diagnoses: int
    active_sensors: int
    diseases_detected: int
    avg_confidence: float
    healthy_percentage: float


class TimeSeriesData(BaseModel):
    date: str
    value: float
    label: str


class DiseaseStats(BaseModel):
    name: str
    count: int
    percentage: float


class SensorStats(BaseModel):
    total: int
    active: int
    warning: int
    error: int


class AnalyticsOverview(BaseModel):
    success: bool = True
    metrics: DashboardMetrics
    period: str
    generated_at: datetime


class DashboardResponse(BaseModel):
    success: bool = True
    metrics: DashboardMetrics
    recent_diagnoses: int
    sensor_alerts: int
    top_diseases: List[DiseaseStats]


# Helper function to get period start date
def get_period_start(period: str) -> datetime:
    now = datetime.utcnow()
    if period == "24h":
        return now - timedelta(hours=24)
    elif period == "7d":
        return now - timedelta(days=7)
    elif period == "30d":
        return now - timedelta(days=30)
    elif period == "90d":
        return now - timedelta(days=90)
    elif period == "1y":
        return now - timedelta(days=365)
    return now - timedelta(days=30)


# Routes
@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard analytics"""
    # Get farm count
    if current_user.role == "ADMIN":
        total_farms = db.query(Farm).filter(Farm.deleted_at.is_(None)).count()
        total_diagnoses = db.query(Diagnosis).filter(Diagnosis.deleted_at.is_(None)).count()
        active_sensors = db.query(Sensor).filter(
            Sensor.deleted_at.is_(None),
            Sensor.status == "active"
        ).count()
    else:
        total_farms = db.query(Farm).filter(
            Farm.owner_id == current_user.id,
            Farm.deleted_at.is_(None)
        ).count()
        total_diagnoses = db.query(Diagnosis).filter(
            Diagnosis.user_id == current_user.id,
            Diagnosis.deleted_at.is_(None)
        ).count()
        active_sensors = db.query(Sensor).filter(
            Sensor.user_id == current_user.id,
            Sensor.deleted_at.is_(None),
            Sensor.status == "active"
        ).count()

    # Get diseases count
    diseases_detected = db.query(Diagnosis).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.disease.isnot(None),
        Diagnosis.disease != "Healthy"
    ).count()

    # Calculate average confidence
    avg_conf_result = db.query(func.avg(Diagnosis.confidence)).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.confidence.isnot(None)
    ).scalar()
    avg_confidence = float(avg_conf_result) if avg_conf_result else 0.0

    # Calculate healthy percentage
    healthy_count = db.query(Diagnosis).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.disease == "Healthy"
    ).count()
    healthy_percentage = (healthy_count / total_diagnoses * 100) if total_diagnoses > 0 else 0.0

    # Recent diagnoses (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_diagnoses = db.query(Diagnosis).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.created_at >= week_ago
    ).count()

    # Sensor alerts
    sensor_alerts = db.query(Sensor).filter(
        Sensor.deleted_at.is_(None),
        Sensor.status.in_(["warning", "error"])
    ).count()

    # Top diseases
    top_diseases_query = db.query(
        Diagnosis.disease,
        func.count(Diagnosis.id).label('count')
    ).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.disease.isnot(None),
        Diagnosis.disease != "Healthy"
    ).group_by(Diagnosis.disease).order_by(func.count(Diagnosis.id).desc()).limit(5).all()

    top_diseases = []
    for disease_name, count in top_diseases_query:
        percentage = (count / diseases_detected * 100) if diseases_detected > 0 else 0.0
        top_diseases.append(DiseaseStats(name=disease_name, count=count, percentage=round(percentage, 1)))

    return DashboardResponse(
        success=True,
        metrics=DashboardMetrics(
            total_farms=total_farms,
            total_diagnoses=total_diagnoses,
            active_sensors=active_sensors,
            diseases_detected=diseases_detected,
            avg_confidence=round(avg_confidence, 2),
            healthy_percentage=round(healthy_percentage, 1)
        ),
        recent_diagnoses=recent_diagnoses,
        sensor_alerts=sensor_alerts,
        top_diseases=top_diseases
    )


@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    period: str = Query("30d", pattern="^(24h|7d|30d|90d|1y)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics overview for the specified period"""
    start_date = get_period_start(period)

    # Build base queries
    if current_user.role == "ADMIN":
        farms_query = db.query(Farm).filter(Farm.deleted_at.is_(None))
        diagnoses_query = db.query(Diagnosis).filter(
            Diagnosis.deleted_at.is_(None),
            Diagnosis.created_at >= start_date
        )
        sensors_query = db.query(Sensor).filter(Sensor.deleted_at.is_(None))
    else:
        farms_query = db.query(Farm).filter(
            Farm.owner_id == current_user.id,
            Farm.deleted_at.is_(None)
        )
        diagnoses_query = db.query(Diagnosis).filter(
            Diagnosis.user_id == current_user.id,
            Diagnosis.deleted_at.is_(None),
            Diagnosis.created_at >= start_date
        )
        sensors_query = db.query(Sensor).filter(
            Sensor.user_id == current_user.id,
            Sensor.deleted_at.is_(None)
        )

    total_farms = farms_query.count()
    total_diagnoses = diagnoses_query.count()
    active_sensors = sensors_query.filter(Sensor.status == "active").count()

    diseases_detected = diagnoses_query.filter(
        Diagnosis.disease.isnot(None),
        Diagnosis.disease != "Healthy"
    ).count()

    avg_conf = diagnoses_query.with_entities(func.avg(Diagnosis.confidence)).scalar()
    avg_confidence = float(avg_conf) if avg_conf else 0.0

    healthy_count = diagnoses_query.filter(Diagnosis.disease == "Healthy").count()
    healthy_percentage = (healthy_count / total_diagnoses * 100) if total_diagnoses > 0 else 0.0

    return AnalyticsOverview(
        success=True,
        metrics=DashboardMetrics(
            total_farms=total_farms,
            total_diagnoses=total_diagnoses,
            active_sensors=active_sensors,
            diseases_detected=diseases_detected,
            avg_confidence=round(avg_confidence, 2),
            healthy_percentage=round(healthy_percentage, 1)
        ),
        period=period,
        generated_at=datetime.utcnow()
    )


@router.get("/crops", response_model=Dict[str, Any])
async def get_crops_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get crop-related analytics"""
    # Get crop distribution from farms
    if current_user.role == "ADMIN":
        crop_stats = db.query(
            Farm.crop_type,
            func.count(Farm.id).label('count'),
            func.sum(Farm.area).label('total_area')
        ).filter(
            Farm.deleted_at.is_(None),
            Farm.crop_type.isnot(None)
        ).group_by(Farm.crop_type).all()
    else:
        crop_stats = db.query(
            Farm.crop_type,
            func.count(Farm.id).label('count'),
            func.sum(Farm.area).label('total_area')
        ).filter(
            Farm.owner_id == current_user.id,
            Farm.deleted_at.is_(None),
            Farm.crop_type.isnot(None)
        ).group_by(Farm.crop_type).all()

    crops_data = []
    for crop_type, count, total_area in crop_stats:
        crops_data.append({
            "crop_type": crop_type,
            "farms_count": count,
            "total_area": float(total_area) if total_area else 0
        })

    return {
        "success": True,
        "data": crops_data,
        "total_crops": len(crops_data)
    }


@router.get("/diseases", response_model=Dict[str, Any])
async def get_diseases_analytics(
    period: str = Query("30d", pattern="^(24h|7d|30d|90d|1y)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get disease statistics"""
    start_date = get_period_start(period)

    # Disease distribution
    disease_stats = db.query(
        Diagnosis.disease,
        func.count(Diagnosis.id).label('count'),
        func.avg(Diagnosis.confidence).label('avg_confidence')
    ).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.created_at >= start_date,
        Diagnosis.disease.isnot(None)
    ).group_by(Diagnosis.disease).order_by(func.count(Diagnosis.id).desc()).all()

    diseases_data = []
    total = sum(count for _, count, _ in disease_stats)
    for disease_name, count, avg_conf in disease_stats:
        diseases_data.append({
            "disease": disease_name,
            "count": count,
            "percentage": round((count / total * 100) if total > 0 else 0, 1),
            "avg_confidence": round(float(avg_conf) if avg_conf else 0, 2)
        })

    return {
        "success": True,
        "data": diseases_data,
        "total_diagnoses": total,
        "period": period
    }


@router.get("/sensors", response_model=Dict[str, Any])
async def get_sensors_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sensor statistics"""
    if current_user.role == "ADMIN":
        base_query = db.query(Sensor).filter(Sensor.deleted_at.is_(None))
    else:
        base_query = db.query(Sensor).filter(
            Sensor.user_id == current_user.id,
            Sensor.deleted_at.is_(None)
        )

    total = base_query.count()
    active = base_query.filter(Sensor.status == "active").count()
    warning = base_query.filter(Sensor.status == "warning").count()
    error = base_query.filter(Sensor.status == "error").count()
    inactive = base_query.filter(Sensor.status == "inactive").count()

    # Sensor type distribution
    type_stats = base_query.with_entities(
        Sensor.type,
        func.count(Sensor.id)
    ).group_by(Sensor.type).all()

    return {
        "success": True,
        "summary": {
            "total": total,
            "active": active,
            "warning": warning,
            "error": error,
            "inactive": inactive
        },
        "by_type": {sensor_type: count for sensor_type, count in type_stats}
    }


@router.get("/trends", response_model=Dict[str, Any])
async def get_trends(
    period: str = Query("30d", pattern="^(7d|30d|90d)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get diagnosis trends over time"""
    start_date = get_period_start(period)

    # Group by date
    daily_stats = db.query(
        func.date(Diagnosis.created_at).label('date'),
        func.count(Diagnosis.id).label('count')
    ).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.created_at >= start_date
    ).group_by(func.date(Diagnosis.created_at)).order_by(func.date(Diagnosis.created_at)).all()

    trends = []
    for date, count in daily_stats:
        trends.append({
            "date": str(date),
            "diagnoses": count
        })

    return {
        "success": True,
        "data": trends,
        "period": period
    }


# ============================================
# Advanced Analytics Endpoints
# ============================================

@router.get("/heatmap", response_model=Dict[str, Any])
async def get_disease_heatmap(
    period: str = Query("30d", pattern="^(7d|30d|90d|1y)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get disease heatmap data by location/farm.
    Returns geographic distribution of diseases for visualization.
    """
    start_date = get_period_start(period)

    # Get disease counts by farm location
    heatmap_data = db.query(
        Farm.name.label('farm_name'),
        Farm.latitude,
        Farm.longitude,
        func.count(Diagnosis.id).label('diagnosis_count'),
        func.sum(
            func.case(
                (Diagnosis.disease != "Healthy", 1),
                else_=0
            )
        ).label('disease_count')
    ).join(
        Diagnosis, Diagnosis.farm_id == Farm.id, isouter=True
    ).filter(
        Farm.deleted_at.is_(None),
        Diagnosis.created_at >= start_date
    ).group_by(
        Farm.id, Farm.name, Farm.latitude, Farm.longitude
    ).all()

    points = []
    for farm_name, lat, lng, diag_count, disease_count in heatmap_data:
        if lat and lng:
            intensity = min(1.0, (disease_count or 0) / 10)
            points.append({
                "farm": farm_name,
                "lat": float(lat),
                "lng": float(lng),
                "diagnoses": diag_count or 0,
                "diseases": disease_count or 0,
                "intensity": round(intensity, 2)
            })

    return {
        "success": True,
        "data": points,
        "period": period,
        "total_points": len(points)
    }


@router.get("/comparative", response_model=Dict[str, Any])
async def get_comparative_analysis(
    period: str = Query("30d", pattern="^(7d|30d|90d)$"),
    compare_by: str = Query("farm", pattern="^(farm|crop|month)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comparative analysis across farms, crops, or time periods.
    Useful for identifying best/worst performing areas.
    """
    start_date = get_period_start(period)

    if compare_by == "farm":
        # Compare farms by health metrics
        stats = db.query(
            Farm.name.label('category'),
            func.count(Diagnosis.id).label('total_diagnoses'),
            func.avg(Diagnosis.confidence).label('avg_confidence'),
            func.sum(
                func.case((Diagnosis.disease == "Healthy", 1), else_=0)
            ).label('healthy_count')
        ).join(
            Diagnosis, Diagnosis.farm_id == Farm.id, isouter=True
        ).filter(
            Farm.deleted_at.is_(None),
            Diagnosis.created_at >= start_date
        ).group_by(Farm.id, Farm.name).all()

    elif compare_by == "crop":
        # Compare by crop type
        stats = db.query(
            Farm.crop_type.label('category'),
            func.count(Diagnosis.id).label('total_diagnoses'),
            func.avg(Diagnosis.confidence).label('avg_confidence'),
            func.sum(
                func.case((Diagnosis.disease == "Healthy", 1), else_=0)
            ).label('healthy_count')
        ).join(
            Diagnosis, Diagnosis.farm_id == Farm.id, isouter=True
        ).filter(
            Farm.deleted_at.is_(None),
            Farm.crop_type.isnot(None),
            Diagnosis.created_at >= start_date
        ).group_by(Farm.crop_type).all()

    else:  # month
        # Compare by month
        stats = db.query(
            func.strftime('%Y-%m', Diagnosis.created_at).label('category'),
            func.count(Diagnosis.id).label('total_diagnoses'),
            func.avg(Diagnosis.confidence).label('avg_confidence'),
            func.sum(
                func.case((Diagnosis.disease == "Healthy", 1), else_=0)
            ).label('healthy_count')
        ).filter(
            Diagnosis.deleted_at.is_(None),
            Diagnosis.created_at >= start_date
        ).group_by(
            func.strftime('%Y-%m', Diagnosis.created_at)
        ).order_by(
            func.strftime('%Y-%m', Diagnosis.created_at)
        ).all()

    comparison = []
    for category, total, avg_conf, healthy in stats:
        if category:
            health_rate = (healthy / total * 100) if total > 0 else 0
            comparison.append({
                "category": category,
                "total_diagnoses": total or 0,
                "avg_confidence": round(float(avg_conf or 0), 2),
                "healthy_count": healthy or 0,
                "health_rate": round(health_rate, 1)
            })

    # Sort by health rate descending
    comparison.sort(key=lambda x: x["health_rate"], reverse=True)

    return {
        "success": True,
        "compare_by": compare_by,
        "data": comparison,
        "period": period,
        "best_performer": comparison[0] if comparison else None,
        "worst_performer": comparison[-1] if comparison else None
    }


@router.get("/predictions", response_model=Dict[str, Any])
async def get_yield_predictions(
    farm_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get yield predictions based on historical data and current health.
    Uses simple trend analysis for predictions.
    """
    # Get historical diagnosis data
    base_query = db.query(Diagnosis).filter(Diagnosis.deleted_at.is_(None))

    if farm_id:
        base_query = base_query.filter(Diagnosis.farm_id == farm_id)
    elif current_user.role != "ADMIN":
        base_query = base_query.filter(Diagnosis.user_id == current_user.id)

    # Last 90 days data
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    recent_data = base_query.filter(
        Diagnosis.created_at >= ninety_days_ago
    ).all()

    # Calculate health trend
    total_diagnoses = len(recent_data)
    healthy_count = sum(1 for d in recent_data if d.disease == "Healthy")
    current_health_rate = (healthy_count / total_diagnoses * 100) if total_diagnoses > 0 else 0

    # Simple prediction based on health rate
    # Higher health rate = better yield prediction
    base_yield = 100  # Baseline yield percentage
    health_factor = current_health_rate / 100
    predicted_yield = base_yield * (0.5 + 0.5 * health_factor)

    # Risk assessment
    if current_health_rate >= 80:
        risk_level = "low"
        risk_label = "منخفض"
    elif current_health_rate >= 60:
        risk_level = "medium"
        risk_label = "متوسط"
    else:
        risk_level = "high"
        risk_label = "مرتفع"

    # Monthly trend
    monthly_health = []
    for i in range(3):
        month_start = datetime.utcnow() - timedelta(days=30 * (i + 1))
        month_end = datetime.utcnow() - timedelta(days=30 * i)
        month_data = [
            d for d in recent_data
            if month_start <= d.created_at < month_end
        ]
        month_healthy = sum(1 for d in month_data if d.disease == "Healthy")
        month_rate = (month_healthy / len(month_data) * 100) if month_data else 0
        monthly_health.append({
            "month": month_start.strftime("%Y-%m"),
            "health_rate": round(month_rate, 1),
            "diagnoses": len(month_data)
        })

    return {
        "success": True,
        "predictions": {
            "current_health_rate": round(current_health_rate, 1),
            "predicted_yield_percentage": round(predicted_yield, 1),
            "risk_level": risk_level,
            "risk_label": risk_label,
            "confidence": 0.75 if total_diagnoses >= 50 else 0.5
        },
        "trend": monthly_health,
        "recommendations": get_recommendations(current_health_rate, risk_level),
        "data_points": total_diagnoses
    }


def get_recommendations(health_rate: float, risk_level: str) -> List[Dict]:
    """Generate recommendations based on health metrics."""
    recommendations = []

    if risk_level == "high":
        recommendations.extend([
            {
                "priority": "high",
                "message": "Immediate disease inspection recommended",
                "message_ar": "يُنصح بفحص الأمراض فوراً"
            },
            {
                "priority": "high",
                "message": "Consider preventive treatment application",
                "message_ar": "فكر في تطبيق العلاج الوقائي"
            }
        ])
    elif risk_level == "medium":
        recommendations.extend([
            {
                "priority": "medium",
                "message": "Schedule regular health monitoring",
                "message_ar": "جدولة مراقبة صحية منتظمة"
            },
            {
                "priority": "medium",
                "message": "Review irrigation and nutrition plans",
                "message_ar": "مراجعة خطط الري والتغذية"
            }
        ])
    else:
        recommendations.extend([
            {
                "priority": "low",
                "message": "Maintain current practices",
                "message_ar": "حافظ على الممارسات الحالية"
            },
            {
                "priority": "low",
                "message": "Continue regular monitoring",
                "message_ar": "استمر في المراقبة المنتظمة"
            }
        ])

    return recommendations


@router.get("/summary-report", response_model=Dict[str, Any])
async def get_summary_report(
    period: str = Query("30d", pattern="^(7d|30d|90d|1y)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive summary report for the specified period.
    Combines all analytics into a single report.
    """
    start_date = get_period_start(period)

    # Build base queries based on user role
    is_admin = current_user.role == "ADMIN"

    # Farm stats
    farms_query = db.query(Farm).filter(Farm.deleted_at.is_(None))
    if not is_admin:
        farms_query = farms_query.filter(Farm.owner_id == current_user.id)
    total_farms = farms_query.count()

    # Diagnosis stats
    diag_query = db.query(Diagnosis).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.created_at >= start_date
    )
    if not is_admin:
        diag_query = diag_query.filter(Diagnosis.user_id == current_user.id)

    total_diagnoses = diag_query.count()
    healthy_count = diag_query.filter(Diagnosis.disease == "Healthy").count()
    disease_count = diag_query.filter(
        Diagnosis.disease.isnot(None),
        Diagnosis.disease != "Healthy"
    ).count()

    # Sensor stats
    sensor_query = db.query(Sensor).filter(Sensor.deleted_at.is_(None))
    if not is_admin:
        sensor_query = sensor_query.filter(Sensor.user_id == current_user.id)

    total_sensors = sensor_query.count()
    active_sensors = sensor_query.filter(Sensor.status == "active").count()
    alert_sensors = sensor_query.filter(
        Sensor.status.in_(["warning", "error"])
    ).count()

    # Top diseases
    top_diseases = db.query(
        Diagnosis.disease,
        func.count(Diagnosis.id).label('count')
    ).filter(
        Diagnosis.deleted_at.is_(None),
        Diagnosis.created_at >= start_date,
        Diagnosis.disease.isnot(None),
        Diagnosis.disease != "Healthy"
    ).group_by(Diagnosis.disease).order_by(
        func.count(Diagnosis.id).desc()
    ).limit(5).all()

    # Calculate metrics
    health_rate = (healthy_count / total_diagnoses * 100) if total_diagnoses > 0 else 0
    disease_rate = (disease_count / total_diagnoses * 100) if total_diagnoses > 0 else 0

    return {
        "success": True,
        "report": {
            "period": period,
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_farms": total_farms,
                "total_diagnoses": total_diagnoses,
                "health_rate": round(health_rate, 1),
                "disease_rate": round(disease_rate, 1)
            },
            "sensors": {
                "total": total_sensors,
                "active": active_sensors,
                "alerts": alert_sensors
            },
            "top_diseases": [
                {"name": name, "count": count}
                for name, count in top_diseases
            ],
            "health_status": (
                "excellent" if health_rate >= 90 else
                "good" if health_rate >= 70 else
                "fair" if health_rate >= 50 else
                "poor"
            ),
            "health_status_ar": (
                "ممتاز" if health_rate >= 90 else
                "جيد" if health_rate >= 70 else
                "مقبول" if health_rate >= 50 else
                "ضعيف"
            )
        }
    }
