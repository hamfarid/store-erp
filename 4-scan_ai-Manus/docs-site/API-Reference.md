# 🔌 API Reference - مرجع واجهات البرمجة

هذا المرجع الشامل لجميع واجهات البرمجة (APIs) المتاحة في نظام Gaara AI للزراعة الذكية.

## 🌐 معلومات عامة

### Base URL
```
Production: https://api.gaara-ai.com
Development: http://localhost:5000
```

### Authentication
يستخدم النظام JWT (JSON Web Tokens) للمصادقة. يجب تضمين التوكن في header لجميع الطلبات المحمية:

```http
Authorization: Bearer YOUR_JWT_TOKEN
```

### Content Type
جميع الطلبات والاستجابات تستخدم JSON:
```http
Content-Type: application/json
```

### Response Format
جميع الاستجابات تتبع التنسيق التالي:
```json
{
  "success": true|false,
  "message": "رسالة وصفية",
  "data": {}, // البيانات المطلوبة
  "error": null|"رسالة الخطأ",
  "timestamp": "2025-01-21T10:30:00Z"
}
```

## 🔐 Authentication APIs

### POST /api/auth/login
تسجيل الدخول للنظام

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "تم تسجيل الدخول بنجاح",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@gaara-ai.com",
      "role": "admin",
      "permissions": ["read", "write", "admin"]
    },
    "expires_in": 3600
  }
}
```

### POST /api/auth/logout
تسجيل الخروج من النظام

**Headers:** `Authorization: Bearer TOKEN`

**Response:**
```json
{
  "success": true,
  "message": "تم تسجيل الخروج بنجاح"
}
```

### POST /api/auth/refresh
تجديد التوكن

**Headers:** `Authorization: Bearer TOKEN`

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_token",
    "expires_in": 3600
  }
}
```

### GET /api/auth/profile
الحصول على معلومات المستخدم الحالي

**Headers:** `Authorization: Bearer TOKEN`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@gaara-ai.com",
    "full_name": "مدير النظام",
    "role": "admin",
    "created_at": "2025-01-01T00:00:00Z",
    "last_login": "2025-01-21T10:30:00Z"
  }
}
```

## 👥 User Management APIs

### GET /api/users
الحصول على قائمة المستخدمين

**Headers:** `Authorization: Bearer TOKEN`

**Query Parameters:**
- `page`: رقم الصفحة (افتراضي: 1)
- `limit`: عدد العناصر في الصفحة (افتراضي: 10)
- `search`: البحث في الاسم أو البريد الإلكتروني
- `role`: تصفية حسب الدور

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@gaara-ai.com",
        "full_name": "مدير النظام",
        "role": "admin",
        "is_active": true,
        "created_at": "2025-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_items": 50,
      "items_per_page": 10
    }
  }
}
```

### POST /api/users
إنشاء مستخدم جديد

**Headers:** `Authorization: Bearer TOKEN`

**Request Body:**
```json
{
  "username": "farmer1",
  "email": "farmer1@example.com",
  "password": "secure_password",
  "full_name": "أحمد المزارع",
  "role": "farmer",
  "phone": "+966501234567",
  "farm_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "تم إنشاء المستخدم بنجاح",
  "data": {
    "id": 2,
    "username": "farmer1",
    "email": "farmer1@example.com",
    "full_name": "أحمد المزارع",
    "role": "farmer"
  }
}
```

### GET /api/users/{id}
الحصول على معلومات مستخدم محدد

**Headers:** `Authorization: Bearer TOKEN`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "username": "farmer1",
    "email": "farmer1@example.com",
    "full_name": "أحمد المزارع",
    "role": "farmer",
    "phone": "+966501234567",
    "farm": {
      "id": 1,
      "name": "مزرعة الأمل"
    },
    "created_at": "2025-01-15T08:00:00Z",
    "last_login": "2025-01-21T09:15:00Z"
  }
}
```

### PUT /api/users/{id}
تحديث معلومات مستخدم

**Headers:** `Authorization: Bearer TOKEN`

**Request Body:**
```json
{
  "full_name": "أحمد المزارع المحدث",
  "email": "new_email@example.com",
  "phone": "+966507654321"
}
```

### DELETE /api/users/{id}
حذف مستخدم

**Headers:** `Authorization: Bearer TOKEN`

**Response:**
```json
{
  "success": true,
  "message": "تم حذف المستخدم بنجاح"
}
```

## 🌾 Farm Management APIs

### GET /api/farms
الحصول على قائمة المزارع

**Headers:** `Authorization: Bearer TOKEN`

**Query Parameters:**
- `page`, `limit`: للصفحات
- `search`: البحث في اسم المزرعة
- `status`: تصفية حسب الحالة (active, inactive)
- `location`: تصفية حسب الموقع

**Response:**
```json
{
  "success": true,
  "data": {
    "farms": [
      {
        "id": 1,
        "name": "مزرعة الأمل",
        "location": "الرياض، السعودية",
        "area": 1000.5,
        "area_unit": "هكتار",
        "status": "active",
        "owner": {
          "id": 2,
          "name": "أحمد المزارع"
        },
        "crops_count": 5,
        "sensors_count": 12,
        "created_at": "2025-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 3,
      "total_items": 25
    }
  }
}
```

### POST /api/farms
إنشاء مزرعة جديدة

**Headers:** `Authorization: Bearer TOKEN`

**Request Body:**
```json
{
  "name": "مزرعة الخير",
  "description": "مزرعة متخصصة في زراعة الخضروات العضوية",
  "location": "جدة، السعودية",
  "latitude": 21.4858,
  "longitude": 39.1925,
  "area": 500.0,
  "area_unit": "هكتار",
  "owner_id": 2,
  "farm_type": "vegetables",
  "irrigation_system": "drip"
}
```

### GET /api/farms/{id}
الحصول على تفاصيل مزرعة محددة

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "مزرعة الأمل",
    "description": "مزرعة حديثة للزراعة الذكية",
    "location": "الرياض، السعودية",
    "coordinates": {
      "latitude": 24.7136,
      "longitude": 46.6753
    },
    "area": 1000.5,
    "area_unit": "هكتار",
    "owner": {
      "id": 2,
      "name": "أحمد المزارع",
      "phone": "+966501234567"
    },
    "crops": [
      {
        "id": 1,
        "name": "طماطم",
        "variety": "شيري",
        "planted_area": 200.0,
        "planting_date": "2025-01-01",
        "expected_harvest": "2025-04-01"
      }
    ],
    "sensors": [
      {
        "id": 1,
        "type": "soil_moisture",
        "location": "القطاع الأول",
        "status": "active",
        "last_reading": {
          "value": 65.5,
          "unit": "%",
          "timestamp": "2025-01-21T10:00:00Z"
        }
      }
    ],
    "statistics": {
      "total_crops": 5,
      "active_sensors": 10,
      "total_harvest": 2500.0,
      "average_yield": 85.2
    }
  }
}
```

## 🤖 AI Diagnosis APIs

### POST /api/ai/diagnose
تشخيص أمراض النباتات باستخدام الذكاء الاصطناعي

**Headers:** 
- `Authorization: Bearer TOKEN`
- `Content-Type: multipart/form-data`

**Request Body (Form Data):**
```
image: [ملف الصورة]
plant_type: "tomato"
symptoms: "أوراق صفراء، بقع بنية"
location: "القطاع الأول"
farm_id: 1
```

**Response:**
```json
{
  "success": true,
  "data": {
    "diagnosis_id": "diag_12345",
    "plant_type": "tomato",
    "detected_diseases": [
      {
        "disease": "Late Blight",
        "arabic_name": "اللفحة المتأخرة",
        "confidence": 0.92,
        "severity": "moderate",
        "description": "مرض فطري يصيب أوراق وثمار الطماطم"
      }
    ],
    "recommendations": [
      {
        "type": "treatment",
        "title": "العلاج الموصى به",
        "description": "استخدام مبيد فطري نحاسي",
        "urgency": "high",
        "estimated_cost": 150.0
      },
      {
        "type": "prevention",
        "title": "الوقاية المستقبلية",
        "description": "تحسين التهوية وتقليل الرطوبة",
        "urgency": "medium"
      }
    ],
    "analysis_details": {
      "image_quality": "good",
      "processing_time": 2.3,
      "model_version": "v2.1.0",
      "analyzed_at": "2025-01-21T10:30:00Z"
    }
  }
}
```

### GET /api/ai/diagnoses
الحصول على تاريخ التشخيصات

**Headers:** `Authorization: Bearer TOKEN`

**Query Parameters:**
- `farm_id`: تصفية حسب المزرعة
- `plant_type`: تصفية حسب نوع النبات
- `date_from`, `date_to`: تصفية حسب التاريخ
- `disease`: تصفية حسب المرض

**Response:**
```json
{
  "success": true,
  "data": {
    "diagnoses": [
      {
        "id": "diag_12345",
        "farm": {
          "id": 1,
          "name": "مزرعة الأمل"
        },
        "plant_type": "tomato",
        "detected_disease": "Late Blight",
        "confidence": 0.92,
        "severity": "moderate",
        "status": "treated",
        "diagnosed_at": "2025-01-21T10:30:00Z",
        "treated_at": "2025-01-21T14:00:00Z"
      }
    ]
  }
}
```

### GET /api/ai/diagnoses/{id}
الحصول على تفاصيل تشخيص محدد

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "diag_12345",
    "original_image": "/uploads/diagnoses/img_12345.jpg",
    "analyzed_image": "/uploads/diagnoses/analyzed_12345.jpg",
    "plant_type": "tomato",
    "symptoms_reported": "أوراق صفراء، بقع بنية",
    "detected_diseases": [...],
    "recommendations": [...],
    "treatment_history": [
      {
        "date": "2025-01-21T14:00:00Z",
        "treatment": "رش مبيد فطري",
        "applied_by": "أحمد المزارع",
        "notes": "تم الرش في الصباح الباكر"
      }
    ],
    "follow_up": {
      "next_check_date": "2025-01-28T00:00:00Z",
      "expected_recovery": "2025-02-05T00:00:00Z",
      "recovery_probability": 0.85
    }
  }
}
```

## 🌐 IoT Sensors APIs

### GET /api/sensors
الحصول على قائمة أجهزة الاستشعار

**Headers:** `Authorization: Bearer TOKEN`

**Query Parameters:**
- `farm_id`: تصفية حسب المزرعة
- `type`: نوع الحساس (soil_moisture, temperature, humidity, etc.)
- `status`: الحالة (active, inactive, maintenance)
- `location`: الموقع في المزرعة

**Response:**
```json
{
  "success": true,
  "data": {
    "sensors": [
      {
        "id": 1,
        "device_id": "GAARA_SENSOR_001",
        "type": "soil_moisture",
        "name": "حساس رطوبة التربة - القطاع 1",
        "farm": {
          "id": 1,
          "name": "مزرعة الأمل"
        },
        "location": "القطاع الأول - صف 3",
        "coordinates": {
          "latitude": 24.7136,
          "longitude": 46.6753
        },
        "status": "active",
        "battery_level": 85,
        "signal_strength": -65,
        "last_reading": {
          "value": 65.5,
          "unit": "%",
          "timestamp": "2025-01-21T10:00:00Z",
          "quality": "good"
        },
        "installed_at": "2025-01-01T00:00:00Z"
      }
    ]
  }
}
```

### POST /api/sensors
إضافة حساس جديد

**Headers:** `Authorization: Bearer TOKEN`

**Request Body:**
```json
{
  "device_id": "GAARA_SENSOR_002",
  "type": "temperature",
  "name": "حساس الحرارة - البيت المحمي 1",
  "farm_id": 1,
  "location": "البيت المحمي الأول",
  "latitude": 24.7140,
  "longitude": 46.6750,
  "configuration": {
    "reading_interval": 300,
    "alert_thresholds": {
      "min": 15.0,
      "max": 35.0
    }
  }
}
```

### GET /api/sensors/{id}/readings
الحصول على قراءات حساس محدد

**Query Parameters:**
- `from_date`, `to_date`: فترة زمنية
- `interval`: فترة التجميع (hour, day, week)
- `limit`: عدد القراءات

**Response:**
```json
{
  "success": true,
  "data": {
    "sensor": {
      "id": 1,
      "name": "حساس رطوبة التربة - القطاع 1",
      "type": "soil_moisture",
      "unit": "%"
    },
    "readings": [
      {
        "timestamp": "2025-01-21T10:00:00Z",
        "value": 65.5,
        "quality": "good"
      },
      {
        "timestamp": "2025-01-21T10:05:00Z",
        "value": 64.8,
        "quality": "good"
      }
    ],
    "statistics": {
      "count": 288,
      "average": 65.2,
      "min": 45.0,
      "max": 85.0,
      "trend": "stable"
    }
  }
}
```

### POST /api/sensors/{id}/readings
إضافة قراءة جديدة (للأجهزة)

**Headers:** 
- `Authorization: Bearer DEVICE_TOKEN`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "value": 67.2,
  "timestamp": "2025-01-21T10:30:00Z",
  "battery_level": 84,
  "signal_strength": -63,
  "metadata": {
    "temperature": 25.5,
    "calibration_offset": 0.2
  }
}
```

## 🚨 Alerts & Notifications APIs

### GET /api/alerts
الحصول على التنبيهات

**Headers:** `Authorization: Bearer TOKEN`

**Query Parameters:**
- `status`: الحالة (active, resolved, dismissed)
- `severity`: الأهمية (low, medium, high, critical)
- `type`: النوع (sensor, disease, irrigation, weather)
- `farm_id`: تصفية حسب المزرعة

**Response:**
```json
{
  "success": true,
  "data": {
    "alerts": [
      {
        "id": 1,
        "type": "sensor",
        "severity": "high",
        "title": "انخفاض رطوبة التربة",
        "message": "رطوبة التربة في القطاع الأول انخفضت إلى 35%",
        "farm": {
          "id": 1,
          "name": "مزرعة الأمل"
        },
        "sensor": {
          "id": 1,
          "name": "حساس رطوبة التربة - القطاع 1"
        },
        "status": "active",
        "created_at": "2025-01-21T09:30:00Z",
        "actions": [
          {
            "type": "irrigation",
            "title": "تشغيل الري",
            "estimated_duration": 30
          }
        ]
      }
    ]
  }
}
```

### POST /api/alerts/{id}/resolve
حل تنبيه

**Headers:** `Authorization: Bearer TOKEN`

**Request Body:**
```json
{
  "resolution": "تم تشغيل نظام الري لمدة 30 دقيقة",
  "action_taken": "irrigation_activated"
}
```

## 💧 Irrigation Control APIs

### GET /api/irrigation/zones
الحصول على مناطق الري

**Response:**
```json
{
  "success": true,
  "data": {
    "zones": [
      {
        "id": 1,
        "name": "منطقة الري الأولى",
        "farm_id": 1,
        "area": 250.0,
        "crop_type": "tomato",
        "irrigation_type": "drip",
        "status": "active",
        "schedule": {
          "frequency": "daily",
          "duration": 30,
          "start_time": "06:00",
          "days": ["sunday", "tuesday", "thursday"]
        },
        "sensors": [1, 2, 3],
        "last_irrigation": "2025-01-21T06:00:00Z",
        "next_irrigation": "2025-01-23T06:00:00Z"
      }
    ]
  }
}
```

### POST /api/irrigation/zones/{id}/activate
تشغيل الري لمنطقة محددة

**Request Body:**
```json
{
  "duration": 30,
  "intensity": "medium",
  "reason": "manual_override",
  "notes": "ري إضافي بسبب ارتفاع درجة الحرارة"
}
```

### GET /api/irrigation/history
تاريخ عمليات الري

**Query Parameters:**
- `zone_id`: منطقة الري
- `from_date`, `to_date`: الفترة الزمنية

**Response:**
```json
{
  "success": true,
  "data": {
    "irrigation_events": [
      {
        "id": 1,
        "zone": {
          "id": 1,
          "name": "منطقة الري الأولى"
        },
        "start_time": "2025-01-21T06:00:00Z",
        "end_time": "2025-01-21T06:30:00Z",
        "duration": 30,
        "water_used": 150.5,
        "trigger": "scheduled",
        "initiated_by": "system",
        "effectiveness": 0.85
      }
    ]
  }
}
```

## 📊 Analytics & Reports APIs

### GET /api/analytics/dashboard
بيانات لوحة التحكم

**Headers:** `Authorization: Bearer TOKEN`

**Query Parameters:**
- `farm_id`: تصفية حسب المزرعة
- `period`: الفترة (today, week, month, year)

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_farms": 5,
      "active_sensors": 45,
      "pending_alerts": 3,
      "water_usage_today": 1250.5,
      "diseases_detected": 2
    },
    "charts": {
      "sensor_readings": {
        "labels": ["06:00", "12:00", "18:00"],
        "datasets": [
          {
            "label": "رطوبة التربة",
            "data": [65, 58, 62],
            "color": "#3B82F6"
          }
        ]
      },
      "water_usage": {
        "labels": ["الأحد", "الاثنين", "الثلاثاء"],
        "data": [1200, 1350, 1100]
      }
    },
    "recent_activities": [
      {
        "type": "diagnosis",
        "message": "تم تشخيص مرض في مزرعة الأمل",
        "timestamp": "2025-01-21T10:30:00Z"
      }
    ]
  }
}
```

### GET /api/reports/farm-performance
تقرير أداء المزرعة

**Query Parameters:**
- `farm_id`: معرف المزرعة
- `from_date`, `to_date`: الفترة الزمنية
- `format`: تنسيق التقرير (json, pdf, excel)

**Response:**
```json
{
  "success": true,
  "data": {
    "farm": {
      "id": 1,
      "name": "مزرعة الأمل"
    },
    "period": {
      "from": "2025-01-01T00:00:00Z",
      "to": "2025-01-21T23:59:59Z"
    },
    "performance_metrics": {
      "crop_yield": {
        "total": 2500.0,
        "average_per_hectare": 2.5,
        "compared_to_target": 1.15
      },
      "water_efficiency": {
        "total_usage": 15000.0,
        "efficiency_ratio": 0.92,
        "savings": 1200.0
      },
      "disease_incidents": {
        "total": 8,
        "resolved": 6,
        "prevention_rate": 0.75
      }
    },
    "recommendations": [
      {
        "category": "irrigation",
        "priority": "medium",
        "suggestion": "تحسين جدولة الري في القطاع الثالث"
      }
    ]
  }
}
```

## 🔧 System APIs

### GET /health
فحص صحة النظام

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "3.0.0",
    "uptime": 86400,
    "services": {
      "database": "connected",
      "redis": "connected",
      "ai_engine": "running"
    },
    "timestamp": "2025-01-21T10:30:00Z"
  }
}
```

### GET /api/system/stats
إحصائيات النظام

**Headers:** `Authorization: Bearer ADMIN_TOKEN`

**Response:**
```json
{
  "success": true,
  "data": {
    "users": {
      "total": 150,
      "active": 120,
      "new_this_month": 15
    },
    "farms": {
      "total": 25,
      "active": 23
    },
    "sensors": {
      "total": 300,
      "online": 285,
      "offline": 15
    },
    "api_usage": {
      "requests_today": 15420,
      "average_response_time": 120
    }
  }
}
```

## ❌ Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | طلب غير صحيح |
| 401 | Unauthorized | غير مصرح |
| 403 | Forbidden | ممنوع |
| 404 | Not Found | غير موجود |
| 422 | Validation Error | خطأ في التحقق |
| 429 | Too Many Requests | طلبات كثيرة |
| 500 | Internal Server Error | خطأ داخلي |

### Example Error Response:
```json
{
  "success": false,
  "message": "خطأ في التحقق من البيانات",
  "error": "Validation failed",
  "details": {
    "field": "email",
    "message": "البريد الإلكتروني مطلوب"
  },
  "timestamp": "2025-01-21T10:30:00Z"
}
```

## 📝 Rate Limiting

- **عام**: 1000 طلب/ساعة لكل مستخدم
- **تسجيل الدخول**: 5 محاولات/دقيقة
- **رفع الصور**: 10 صور/دقيقة
- **APIs الإدارية**: 100 طلب/دقيقة

## 🔒 Security Best Practices

1. **استخدم HTTPS دائماً** في الإنتاج
2. **احفظ التوكن بأمان** ولا تشاركه
3. **جدد التوكن بانتظام** قبل انتهاء صلاحيته
4. **تحقق من الصلاحيات** قبل كل طلب
5. **استخدم Rate Limiting** لحماية APIs

---

**📚 هذا المرجع يغطي جميع APIs المتاحة في نظام Gaara AI. للمزيد من التفاصيل، راجع التوثيق التفاعلي على `/docs`**

