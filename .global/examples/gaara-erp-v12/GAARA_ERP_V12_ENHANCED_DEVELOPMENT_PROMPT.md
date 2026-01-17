# FILE: /home/ubuntu/GAARA_ERP_V12_ENHANCED_DEVELOPMENT_PROMPT.md | PURPOSE: برومبت تطوير شامل محسن لنظام Gaara ERP v12 | OWNER: Manus AI | RELATED: تقرير الفحص الشامل | LAST-AUDITED: 2025-01-01

# برومبت التطوير الشامل المحسن لنظام Gaara ERP v12
## **النسخة 3.0 - الإصدار الكامل**

---

## **🎯 الهدف الاستراتيجي**
تطوير نظام Gaara ERP v12 ليصبح من أفضل 5 أنظمة ERP في العالم، قادر على منافسة Odoo و SAP، مع التركيز على الأسواق الناطقة بالعربية والتوسع عالمياً خلال عامين.

---

## **📊 إطار OSF (الأمثل والآمن أولاً)**

### **معادلة OSF:**
```
OSF_Score = (0.35 × Security) + (0.20 × Correctness) + (0.15 × Reliability) + 
            (0.10 × Maintainability) + (0.08 × Performance) + 
            (0.07 × Usability) + (0.05 × Scalability)
```

### **الأولويات:**
1. **الأمان (35%)** - أولوية قصوى
2. **الصحة (20%)** - دقة الكود والوظائف
3. **الموثوقية (15%)** - استقرار النظام
4. **قابلية الصيانة (10%)** - سهولة التطوير
5. **الأداء (8%)** - سرعة الاستجابة
6. **سهولة الاستخدام (7%)** - تجربة المستخدم
7. **قابلية التوسع (5%)** - النمو المستقبلي

---

## **🔴 الأخطاء الحرجة (يجب إصلاحها فوراً)**

### **1. مشاكل الأمان الحرجة (OSF Security: 35%)**

#### **أ. نقص المصادقة متعددة العوامل:**
```python
# FILE: backend/authentication/mfa.py
from django.contrib.auth.models import User
from django_otp.models import Device
import pyotp
import qrcode
from io import BytesIO
import base64

class MFAManager:
    """إدارة المصادقة متعددة العوامل"""
    
    @staticmethod
    def setup_totp(user: User) -> dict:
        """إعداد TOTP للمستخدم"""
        secret = pyotp.random_base32()
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="Gaara ERP v12"
        )
        
        # إنشاء QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'secret': secret,
            'qr_code': qr_code,
            'backup_codes': MFAManager.generate_backup_codes()
        }
    
    @staticmethod
    def generate_backup_codes() -> list:
        """إنشاء رموز احتياطية"""
        import secrets
        return [secrets.token_hex(4).upper() for _ in range(10)]
    
    @staticmethod
    def verify_totp(user: User, token: str) -> bool:
        """التحقق من رمز TOTP"""
        try:
            device = user.totpdevice_set.get(confirmed=True)
            return device.verify_token(token)
        except:
            return False

# إعدادات MFA إلزامية
MFA_REQUIRED_ROLES = ['ADMIN', 'MANAGER', 'ACCOUNTANT']
MFA_GRACE_PERIOD = 7  # أيام للإعداد
```

#### **ب. تشفير البيانات الحساسة:**
```python
# FILE: backend/security/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
import os
import base64

class DataEncryption:
    """تشفير البيانات الحساسة"""
    
    def __init__(self):
        self.key = self._get_encryption_key()
        self.cipher = Fernet(self.key)
    
    def _get_encryption_key(self) -> bytes:
        """الحصول على مفتاح التشفير من KMS"""
        key = os.environ.get('ENCRYPTION_KEY')
        if not key:
            # إنشاء مفتاح جديد في بيئة التطوير فقط
            if settings.DEBUG:
                key = Fernet.generate_key()
                print(f"Generated new encryption key: {key.decode()}")
            else:
                raise ValueError("ENCRYPTION_KEY must be set in production")
        return key.encode() if isinstance(key, str) else key
    
    def encrypt(self, data: str) -> str:
        """تشفير البيانات"""
        if not data:
            return data
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """فك تشفير البيانات"""
        if not encrypted_data:
            return encrypted_data
        try:
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except:
            return encrypted_data  # البيانات غير مشفرة

# استخدام التشفير في النماذج
from django.db import models

class EncryptedField(models.TextField):
    """حقل مشفر للبيانات الحساسة"""
    
    def __init__(self, *args, **kwargs):
        self.encryptor = DataEncryption()
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.encryptor.decrypt(value)
    
    def to_python(self, value):
        if isinstance(value, str):
            return value
        return self.encryptor.decrypt(value) if value else value
    
    def get_prep_value(self, value):
        return self.encryptor.encrypt(value) if value else value
```

#### **ج. حماية من الهجمات الشائعة:**
```python
# FILE: backend/security/middleware.py
from django.http import HttpResponseForbidden
from django.core.cache import cache
import time
import hashlib

class SecurityMiddleware:
    """حماية شاملة من الهجمات"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Rate Limiting
        if not self.check_rate_limit(request):
            return HttpResponseForbidden("Rate limit exceeded")
        
        # CSRF Protection
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if not self.verify_csrf(request):
                return HttpResponseForbidden("CSRF token missing or invalid")
        
        response = self.get_response(request)
        
        # Security Headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = self.get_csp_header()
        
        return response
    
    def check_rate_limit(self, request) -> bool:
        """فحص حد المعدل"""
        client_ip = self.get_client_ip(request)
        key = f"rate_limit:{client_ip}"
        
        current_requests = cache.get(key, 0)
        if current_requests >= 100:  # 100 طلب في الدقيقة
            return False
        
        cache.set(key, current_requests + 1, 60)  # انتهاء خلال دقيقة
        return True
    
    def get_client_ip(self, request) -> str:
        """الحصول على IP العميل"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_csp_header(self) -> str:
        """إعداد Content Security Policy"""
        return (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
```

### **2. مشاكل الأداء الحرجة (OSF Performance: 8%)**

#### **أ. تحسين استعلامات قاعدة البيانات:**
```python
# FILE: backend/performance/db_optimization.py
from django.db import models
from django.core.cache import cache
from django.db.models import Prefetch
import logging

logger = logging.getLogger(__name__)

class OptimizedQueryManager(models.Manager):
    """مدير استعلامات محسن"""
    
    def get_queryset(self):
        return super().get_queryset().select_related().prefetch_related()
    
    def with_cache(self, cache_key: str, timeout: int = 300):
        """استعلام مع تخزين مؤقت"""
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        result = list(self.get_queryset())
        cache.set(cache_key, result, timeout)
        return result

class DatabaseOptimizer:
    """محسن قاعدة البيانات"""
    
    @staticmethod
    def analyze_slow_queries():
        """تحليل الاستعلامات البطيئة"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT query, mean_time, calls, total_time
                FROM pg_stat_statements
                WHERE mean_time > 100
                ORDER BY mean_time DESC
                LIMIT 10;
            """)
            
            slow_queries = cursor.fetchall()
            for query in slow_queries:
                logger.warning(f"Slow query detected: {query}")
    
    @staticmethod
    def create_indexes():
        """إنشاء فهارس محسنة"""
        indexes = [
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON auth_user(email);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_date ON sales_order(order_date);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_category ON inventory_product(category_id);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transactions_date ON accounting_transaction(transaction_date);",
        ]
        
        from django.db import connection
        with connection.cursor() as cursor:
            for index in indexes:
                try:
                    cursor.execute(index)
                    logger.info(f"Index created: {index}")
                except Exception as e:
                    logger.error(f"Failed to create index: {e}")
```

#### **ب. نظام التخزين المؤقت المتقدم:**
```python
# FILE: backend/performance/caching.py
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from functools import wraps
import hashlib
import json

class CacheManager:
    """مدير التخزين المؤقت المتقدم"""
    
    DEFAULT_TIMEOUT = 300  # 5 دقائق
    LONG_TIMEOUT = 3600   # ساعة واحدة
    SHORT_TIMEOUT = 60    # دقيقة واحدة
    
    @classmethod
    def cache_key(cls, prefix: str, *args, **kwargs) -> str:
        """إنشاء مفتاح تخزين مؤقت فريد"""
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    @classmethod
    def cached_method(cls, timeout: int = DEFAULT_TIMEOUT, key_prefix: str = None):
        """ديكوريتر للتخزين المؤقت للدوال"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # إنشاء مفتاح فريد
                prefix = key_prefix or f"{func.__module__}.{func.__name__}"
                cache_key = cls.cache_key(prefix, *args, **kwargs)
                
                # محاولة الحصول من التخزين المؤقت
                result = cache.get(cache_key)
                if result is not None:
                    return result
                
                # تنفيذ الدالة وحفظ النتيجة
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
                return result
            return wrapper
        return decorator
    
    @classmethod
    def invalidate_pattern(cls, pattern: str):
        """إلغاء التخزين المؤقت بناءً على نمط"""
        # يتطلب Redis مع دعم SCAN
        from django_redis import get_redis_connection
        
        try:
            redis_conn = get_redis_connection("default")
            keys = redis_conn.keys(f"*{pattern}*")
            if keys:
                redis_conn.delete(*keys)
        except Exception as e:
            logger.error(f"Failed to invalidate cache pattern {pattern}: {e}")

# استخدام التخزين المؤقت
@CacheManager.cached_method(timeout=CacheManager.LONG_TIMEOUT, key_prefix="dashboard_stats")
def get_dashboard_statistics(user_id: int, company_id: int):
    """إحصائيات لوحة التحكم مع تخزين مؤقت"""
    # استعلامات معقدة للإحصائيات
    pass
```

---

## **🟡 التطويرات المطلوبة (أولوية عالية)**

### **1. بنية الخدمات المصغرة (Microservices)**

#### **أ. API Gateway:**
```python
# FILE: backend/gateway/api_gateway.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import asyncio
from typing import Dict, Any
import logging

app = FastAPI(title="Gaara ERP API Gateway", version="12.0")

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://gaara-erp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

class APIGateway:
    """بوابة API الموحدة"""
    
    def __init__(self):
        self.services = {
            "auth": "http://auth-service:8001",
            "accounting": "http://accounting-service:8002",
            "inventory": "http://inventory-service:8003",
            "sales": "http://sales-service:8004",
            "hr": "http://hr-service:8005",
        }
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def authenticate_request(self, credentials: HTTPAuthorizationCredentials):
        """مصادقة الطلب"""
        try:
            response = await self.client.post(
                f"{self.services['auth']}/verify-token",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=401, detail="Authentication failed")
    
    async def route_request(self, service: str, path: str, method: str, 
                          headers: Dict, data: Any = None):
        """توجيه الطلب للخدمة المناسبة"""
        if service not in self.services:
            raise HTTPException(status_code=404, detail="Service not found")
        
        url = f"{self.services[service]}{path}"
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=headers,
                json=data if data else None
            )
            return response.json(), response.status_code
        except Exception as e:
            logging.error(f"Service {service} error: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable")

gateway = APIGateway()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """إضافة وقت المعالجة"""
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# توجيه الطلبات
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_service(
    service: str,
    path: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """توجيه الطلبات للخدمات"""
    # مصادقة المستخدم
    user_info = await gateway.authenticate_request(credentials)
    
    # إعداد الهيدرز
    headers = dict(request.headers)
    headers["X-User-ID"] = str(user_info["user_id"])
    headers["X-Company-ID"] = str(user_info["company_id"])
    
    # الحصول على البيانات
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.json()
    
    # توجيه الطلب
    result, status_code = await gateway.route_request(
        service=service,
        path=f"/{path}",
        method=request.method,
        headers=headers,
        data=body
    )
    
    return result
```

#### **ب. خدمة المحاسبة المصغرة:**
```python
# FILE: services/accounting_service/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

app = FastAPI(title="Accounting Service", version="1.0")

class AccountingService:
    """خدمة المحاسبة المصغرة"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_journal_entry(self, entry_data: dict) -> dict:
        """إنشاء قيد يومية"""
        # التحقق من توازن المدين والدائن
        total_debit = sum(line['debit'] for line in entry_data['lines'])
        total_credit = sum(line['credit'] for line in entry_data['lines'])
        
        if total_debit != total_credit:
            raise HTTPException(
                status_code=400,
                detail="Journal entry is not balanced"
            )
        
        # إنشاء القيد
        entry = JournalEntry(
            reference=entry_data['reference'],
            date=entry_data['date'],
            description=entry_data['description'],
            company_id=entry_data['company_id']
        )
        
        self.db.add(entry)
        self.db.flush()
        
        # إضافة بنود القيد
        for line_data in entry_data['lines']:
            line = JournalEntryLine(
                entry_id=entry.id,
                account_id=line_data['account_id'],
                debit=line_data['debit'],
                credit=line_data['credit'],
                description=line_data['description']
            )
            self.db.add(line)
        
        self.db.commit()
        return {"id": entry.id, "status": "created"}
    
    async def get_trial_balance(self, company_id: int, date_from: str, date_to: str):
        """ميزان المراجعة"""
        query = """
        SELECT 
            a.code,
            a.name,
            SUM(jel.debit) as total_debit,
            SUM(jel.credit) as total_credit,
            SUM(jel.debit - jel.credit) as balance
        FROM accounts a
        LEFT JOIN journal_entry_lines jel ON a.id = jel.account_id
        LEFT JOIN journal_entries je ON jel.entry_id = je.id
        WHERE je.company_id = :company_id
        AND je.date BETWEEN :date_from AND :date_to
        GROUP BY a.id, a.code, a.name
        ORDER BY a.code
        """
        
        result = self.db.execute(query, {
            'company_id': company_id,
            'date_from': date_from,
            'date_to': date_to
        })
        
        return [dict(row) for row in result]

@app.post("/journal-entries/")
async def create_journal_entry(entry_data: dict, db: Session = Depends(get_db)):
    service = AccountingService(db)
    return await service.create_journal_entry(entry_data)

@app.get("/trial-balance/")
async def get_trial_balance(
    company_id: int,
    date_from: str,
    date_to: str,
    db: Session = Depends(get_db)
):
    service = AccountingService(db)
    return await service.get_trial_balance(company_id, date_from, date_to)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

### **2. نظام الذكاء الاصطناعي المتقدم**

#### **أ. التنبؤ بالمبيعات:**
```python
# FILE: backend/ai/sales_forecasting.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SalesForecastingModel:
    """نموذج التنبؤ بالمبيعات باستخدام الذكاء الاصطناعي"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'month', 'quarter', 'day_of_week', 'is_weekend',
            'product_category_encoded', 'season_encoded',
            'promotion_active', 'price', 'previous_month_sales',
            'moving_average_3m', 'moving_average_6m'
        ]
    
    def prepare_features(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """تحضير الميزات للنموذج"""
        df = sales_data.copy()
        
        # ميزات زمنية
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # ترميز الفئات
        df['season_encoded'] = df['date'].dt.month.map({
            12: 0, 1: 0, 2: 0,  # شتاء
            3: 1, 4: 1, 5: 1,   # ربيع
            6: 2, 7: 2, 8: 2,   # صيف
            9: 3, 10: 3, 11: 3  # خريف
        })
        
        # ترميز فئة المنتج
        category_mapping = {cat: idx for idx, cat in enumerate(df['product_category'].unique())}
        df['product_category_encoded'] = df['product_category'].map(category_mapping)
        
        # ميزات المبيعات السابقة
        df = df.sort_values(['product_id', 'date'])
        df['previous_month_sales'] = df.groupby('product_id')['sales_amount'].shift(1)
        df['moving_average_3m'] = df.groupby('product_id')['sales_amount'].rolling(3).mean().reset_index(0, drop=True)
        df['moving_average_6m'] = df.groupby('product_id')['sales_amount'].rolling(6).mean().reset_index(0, drop=True)
        
        # ملء القيم المفقودة
        df = df.fillna(0)
        
        return df
    
    def train_model(self, sales_data: pd.DataFrame) -> dict:
        """تدريب النموذج"""
        logger.info("Starting sales forecasting model training...")
        
        # تحضير البيانات
        df = self.prepare_features(sales_data)
        
        # فصل الميزات والهدف
        X = df[self.feature_columns]
        y = df['sales_amount']
        
        # تقسيم البيانات
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=df['product_category']
        )
        
        # تطبيع البيانات
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # تدريب عدة نماذج واختيار الأفضل
        models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        best_model = None
        best_score = float('inf')
        
        for name, model in models.items():
            # التدريب
            model.fit(X_train_scaled, y_train)
            
            # التقييم
            y_pred = model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, y_pred)
            
            logger.info(f"{name} MAE: {mae}")
            
            if mae < best_score:
                best_score = mae
                best_model = model
        
        self.model = best_model
        
        # حفظ النموذج
        model_path = f"models/sales_forecast_{datetime.now().strftime('%Y%m%d')}.joblib"
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, model_path)
        
        return {
            'model_path': model_path,
            'mae': best_score,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_sales(self, product_data: dict, months_ahead: int = 3) -> list:
        """التنبؤ بالمبيعات"""
        if not self.model:
            raise ValueError("Model not trained. Please train the model first.")
        
        predictions = []
        current_date = datetime.now()
        
        for i in range(months_ahead):
            future_date = current_date + timedelta(days=30 * (i + 1))
            
            # إعداد البيانات للتنبؤ
            features = {
                'month': future_date.month,
                'quarter': (future_date.month - 1) // 3 + 1,
                'day_of_week': future_date.weekday(),
                'is_weekend': 1 if future_date.weekday() >= 5 else 0,
                'product_category_encoded': product_data.get('category_encoded', 0),
                'season_encoded': self._get_season(future_date.month),
                'promotion_active': product_data.get('promotion_active', 0),
                'price': product_data.get('price', 0),
                'previous_month_sales': product_data.get('previous_sales', 0),
                'moving_average_3m': product_data.get('avg_3m', 0),
                'moving_average_6m': product_data.get('avg_6m', 0)
            }
            
            # تحويل إلى مصفوفة
            X = np.array([features[col] for col in self.feature_columns]).reshape(1, -1)
            X_scaled = self.scaler.transform(X)
            
            # التنبؤ
            prediction = self.model.predict(X_scaled)[0]
            
            predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_sales': max(0, prediction),  # لا يمكن أن تكون المبيعات سالبة
                'confidence': self._calculate_confidence(X_scaled)
            })
        
        return predictions
    
    def _get_season(self, month: int) -> int:
        """تحديد الموسم"""
        if month in [12, 1, 2]:
            return 0  # شتاء
        elif month in [3, 4, 5]:
            return 1  # ربيع
        elif month in [6, 7, 8]:
            return 2  # صيف
        else:
            return 3  # خريف
    
    def _calculate_confidence(self, X: np.ndarray) -> float:
        """حساب مستوى الثقة في التنبؤ"""
        # حساب بسيط لمستوى الثقة بناءً على تشتت النموذج
        if hasattr(self.model, 'estimators_'):
            predictions = [estimator.predict(X)[0] for estimator in self.model.estimators_]
            std = np.std(predictions)
            confidence = max(0.5, 1 - (std / np.mean(predictions)))
            return min(1.0, confidence)
        return 0.8  # قيمة افتراضية
```

#### **ب. تحليل المشاعر للعملاء:**
```python
# FILE: backend/ai/sentiment_analysis.py
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List
import logging
import re

logger = logging.getLogger(__name__)

class CustomerSentimentAnalyzer:
    """محلل مشاعر العملاء باستخدام الذكاء الاصطناعي"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # تحميل نموذج تحليل المشاعر العربي والإنجليزي
        self.arabic_analyzer = pipeline(
            "sentiment-analysis",
            model="CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment",
            device=0 if torch.cuda.is_available() else -1
        )
        
        self.english_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
    
    def detect_language(self, text: str) -> str:
        """كشف لغة النص"""
        arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)
        
        if len(arabic_chars) > len(english_chars):
            return 'arabic'
        else:
            return 'english'
    
    def analyze_sentiment(self, text: str) -> Dict:
        """تحليل مشاعر النص"""
        if not text or len(text.strip()) < 3:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'language': 'unknown'
            }
        
        # تنظيف النص
        cleaned_text = self.preprocess_text(text)
        
        # كشف اللغة
        language = self.detect_language(cleaned_text)
        
        try:
            # اختيار المحلل المناسب
            if language == 'arabic':
                result = self.arabic_analyzer(cleaned_text)
            else:
                result = self.english_analyzer(cleaned_text)
            
            # توحيد النتائج
            sentiment = self.normalize_sentiment(result[0]['label'])
            confidence = result[0]['score']
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'language': language,
                'original_text': text,
                'processed_text': cleaned_text
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'language': language,
                'error': str(e)
            }
    
    def preprocess_text(self, text: str) -> str:
        """تنظيف وتحضير النص"""
        # إزالة الروابط
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # إزالة الرموز الخاصة (الاحتفاظ بالعربية والإنجليزية والأرقام)
        text = re.sub(r'[^\u0600-\u06FF\w\s]', ' ', text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def normalize_sentiment(self, label: str) -> str:
        """توحيد تسميات المشاعر"""
        label = label.lower()
        
        if label in ['positive', 'pos', 'إيجابي']:
            return 'positive'
        elif label in ['negative', 'neg', 'سلبي']:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """تحليل مجموعة من النصوص"""
        results = []
        
        for text in texts:
            result = self.analyze_sentiment(text)
            results.append(result)
        
        return results
    
    def get_sentiment_summary(self, feedbacks: List[str]) -> Dict:
        """ملخص المشاعر لمجموعة من التعليقات"""
        if not feedbacks:
            return {
                'total_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'average_confidence': 0.0,
                'sentiment_distribution': {}
            }
        
        results = self.analyze_batch(feedbacks)
        
        positive_count = sum(1 for r in results if r['sentiment'] == 'positive')
        negative_count = sum(1 for r in results if r['sentiment'] == 'negative')
        neutral_count = sum(1 for r in results if r['sentiment'] == 'neutral')
        
        total_confidence = sum(r['confidence'] for r in results)
        average_confidence = total_confidence / len(results) if results else 0
        
        return {
            'total_count': len(results),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_percentage': (positive_count / len(results)) * 100,
            'negative_percentage': (negative_count / len(results)) * 100,
            'neutral_percentage': (neutral_count / len(results)) * 100,
            'average_confidence': average_confidence,
            'sentiment_distribution': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count
            },
            'detailed_results': results
        }

# استخدام محلل المشاعر في النماذج
from django.db import models

class CustomerFeedback(models.Model):
    """نموذج تعليقات العملاء"""
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True)
    sentiment_confidence = models.FloatField(default=0.0)
    language = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # تحليل المشاعر تلقائياً عند الحفظ
        if self.feedback_text and not self.sentiment:
            analyzer = CustomerSentimentAnalyzer()
            result = analyzer.analyze_sentiment(self.feedback_text)
            
            self.sentiment = result['sentiment']
            self.sentiment_confidence = result['confidence']
            self.language = result['language']
        
        super().save(*args, **kwargs)
```

---

## **🟢 الميزات الجديدة المطلوبة**

### **1. نظام إدارة الوثائق المتقدم**

#### **أ. استخراج النص من الوثائق (OCR):**
```python
# FILE: backend/documents/ocr_processor.py
import pytesseract
from PIL import Image
import pdf2image
import cv2
import numpy as np
from typing import Dict, List
import logging
import os

logger = logging.getLogger(__name__)

class DocumentOCRProcessor:
    """معالج استخراج النص من الوثائق"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp']
        
        # إعداد Tesseract للعربية والإنجليزية
        self.languages = 'ara+eng'
        
        # إعدادات OCR محسنة
        self.config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF'
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """تحسين الصورة قبل OCR"""
        # تحويل إلى رمادي
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # تحسين التباين
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # إزالة الضوضاء
        denoised = cv2.medianBlur(enhanced, 3)
        
        # تحسين الحواف
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        return sharpened
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """استخراج النص من صورة"""
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # تحسين الصورة
            processed_image = self.preprocess_image(image)
            
            # استخراج النص
            text = pytesseract.image_to_string(
                processed_image,
                lang=self.languages,
                config=self.config
            )
            
            # استخراج معلومات إضافية
            data = pytesseract.image_to_data(
                processed_image,
                lang=self.languages,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # حساب مستوى الثقة
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'word_count': len(text.split()),
                'language': self.detect_primary_language(text),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            return {
                'text': '',
                'confidence': 0,
                'error': str(e),
                'status': 'failed'
            }
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """استخراج النص من PDF"""
        try:
            # تحويل PDF إلى صور
            pages = pdf2image.convert_from_path(pdf_path, dpi=300)
            
            all_text = []
            total_confidence = 0
            page_count = 0
            
            for i, page in enumerate(pages):
                # حفظ الصفحة كصورة مؤقتة
                temp_image_path = f"/tmp/page_{i}.png"
                page.save(temp_image_path, 'PNG')
                
                # استخراج النص من الصفحة
                result = self.extract_text_from_image(temp_image_path)
                
                if result['status'] == 'success':
                    all_text.append(f"--- صفحة {i+1} ---\n{result['text']}")
                    total_confidence += result['confidence']
                    page_count += 1
                
                # حذف الملف المؤقت
                os.remove(temp_image_path)
            
            combined_text = '\n\n'.join(all_text)
            avg_confidence = total_confidence / page_count if page_count > 0 else 0
            
            return {
                'text': combined_text,
                'confidence': avg_confidence,
                'pages_processed': page_count,
                'total_pages': len(pages),
                'word_count': len(combined_text.split()),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"PDF OCR failed for {pdf_path}: {e}")
            return {
                'text': '',
                'confidence': 0,
                'error': str(e),
                'status': 'failed'
            }
    
    def process_document(self, file_path: str) -> Dict:
        """معالجة وثيقة (تحديد النوع تلقائياً)"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension not in self.supported_formats:
            return {
                'text': '',
                'error': f'Unsupported format: {file_extension}',
                'status': 'failed'
            }
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        else:
            return self.extract_text_from_image(file_path)
    
    def detect_primary_language(self, text: str) -> str:
        """كشف اللغة الأساسية للنص"""
        import re
        
        arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if arabic_chars > english_chars:
            return 'arabic'
        elif english_chars > arabic_chars:
            return 'english'
        else:
            return 'mixed'

# نموذج الوثائق مع OCR
class Document(models.Model):
    """نموذج الوثائق مع استخراج النص التلقائي"""
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True)
    ocr_confidence = models.FloatField(default=0.0)
    language = models.CharField(max_length=20, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # معالجة OCR في الخلفية
        if self.file and not self.processed:
            from .tasks import process_document_ocr
            process_document_ocr.delay(self.id)

# مهمة Celery لمعالجة OCR
from celery import shared_task

@shared_task
def process_document_ocr(document_id: int):
    """مهمة معالجة OCR في الخلفية"""
    try:
        document = Document.objects.get(id=document_id)
        processor = DocumentOCRProcessor()
        
        result = processor.process_document(document.file.path)
        
        document.extracted_text = result.get('text', '')
        document.ocr_confidence = result.get('confidence', 0.0)
        document.language = result.get('language', '')
        document.processed = True
        document.save()
        
        logger.info(f"OCR completed for document {document_id}")
        
    except Exception as e:
        logger.error(f"OCR task failed for document {document_id}: {e}")
```

#### **ب. نظام إدارة الإصدارات:**
```python
# FILE: backend/documents/version_control.py
from django.db import models
from django.contrib.auth.models import User
import hashlib
import os
from typing import List, Dict

class DocumentVersion(models.Model):
    """إصدارات الوثائق"""
    
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=20)
    file = models.FileField(upload_to='documents/versions/')
    file_hash = models.CharField(max_length=64)  # SHA-256
    file_size = models.BigIntegerField()
    changes_summary = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['document', 'version_number']
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # حساب hash الملف
        if self.file:
            self.file_hash = self.calculate_file_hash()
            self.file_size = self.file.size
        
        # تحديث الإصدار الحالي
        if self.is_current:
            DocumentVersion.objects.filter(
                document=self.document,
                is_current=True
            ).update(is_current=False)
        
        super().save(*args, **kwargs)
    
    def calculate_file_hash(self) -> str:
        """حساب hash الملف"""
        hash_sha256 = hashlib.sha256()
        
        self.file.seek(0)
        for chunk in iter(lambda: self.file.read(4096), b""):
            hash_sha256.update(chunk)
        self.file.seek(0)
        
        return hash_sha256.hexdigest()

class DocumentVersionManager:
    """مدير إصدارات الوثائق"""
    
    @staticmethod
    def create_version(document, file, changes_summary: str, user: User) -> DocumentVersion:
        """إنشاء إصدار جديد"""
        # الحصول على آخر رقم إصدار
        last_version = DocumentVersion.objects.filter(
            document=document
        ).first()
        
        if last_version:
            # زيادة رقم الإصدار
            version_parts = last_version.version_number.split('.')
            major, minor = int(version_parts[0]), int(version_parts[1])
            
            # زيادة الإصدار الفرعي
            minor += 1
            if minor >= 100:  # إعادة تعيين عند 100
                major += 1
                minor = 0
            
            new_version = f"{major}.{minor}"
        else:
            new_version = "1.0"
        
        # إنشاء الإصدار الجديد
        version = DocumentVersion.objects.create(
            document=document,
            version_number=new_version,
            file=file,
            changes_summary=changes_summary,
            created_by=user,
            is_current=True
        )
        
        return version
    
    @staticmethod
    def compare_versions(version1_id: int, version2_id: int) -> Dict:
        """مقارنة إصدارين"""
        try:
            v1 = DocumentVersion.objects.get(id=version1_id)
            v2 = DocumentVersion.objects.get(id=version2_id)
            
            # مقارنة أساسية
            comparison = {
                'version1': {
                    'number': v1.version_number,
                    'created_at': v1.created_at,
                    'created_by': v1.created_by.get_full_name(),
                    'file_size': v1.file_size,
                    'file_hash': v1.file_hash,
                    'changes': v1.changes_summary
                },
                'version2': {
                    'number': v2.version_number,
                    'created_at': v2.created_at,
                    'created_by': v2.created_by.get_full_name(),
                    'file_size': v2.file_size,
                    'file_hash': v2.file_hash,
                    'changes': v2.changes_summary
                },
                'differences': {
                    'size_change': v2.file_size - v1.file_size,
                    'time_difference': (v2.created_at - v1.created_at).total_seconds(),
                    'same_content': v1.file_hash == v2.file_hash
                }
            }
            
            return comparison
            
        except DocumentVersion.DoesNotExist:
            return {'error': 'Version not found'}
    
    @staticmethod
    def rollback_to_version(document, version_id: int, user: User) -> bool:
        """العودة إلى إصدار سابق"""
        try:
            target_version = DocumentVersion.objects.get(
                id=version_id,
                document=document
            )
            
            # إنشاء إصدار جديد من الإصدار المستهدف
            new_version = DocumentVersionManager.create_version(
                document=document,
                file=target_version.file,
                changes_summary=f"Rollback to version {target_version.version_number}",
                user=user
            )
            
            return True
            
        except DocumentVersion.DoesNotExist:
            return False
    
    @staticmethod
    def get_version_history(document) -> List[Dict]:
        """الحصول على تاريخ الإصدارات"""
        versions = DocumentVersion.objects.filter(document=document)
        
        history = []
        for version in versions:
            history.append({
                'id': version.id,
                'version_number': version.version_number,
                'created_at': version.created_at,
                'created_by': version.created_by.get_full_name(),
                'changes_summary': version.changes_summary,
                'file_size': version.file_size,
                'is_current': version.is_current
            })
        
        return history
```

---

## **📋 خطة التنفيذ المرحلية المحدثة**

### **المرحلة الأولى (شهر 1-3): الإصلاحات الحرجة - OSF Score Target: 0.7**
```python
# مهام المرحلة الأولى
PHASE_1_TASKS = {
    "security_fixes": {
        "priority": "CRITICAL",
        "tasks": [
            "تطبيق MFA إلزامي",
            "تشفير البيانات الحساسة",
            "حماية من SQL Injection/XSS/CSRF",
            "تطبيق Security Headers",
            "إعداد Rate Limiting"
        ],
        "osf_impact": 0.35,  # Security weight
        "deadline": "Month 1"
    },
    "performance_optimization": {
        "priority": "HIGH",
        "tasks": [
            "تحسين استعلامات قاعدة البيانات",
            "إضافة فهارس محسنة",
            "تطبيق Redis Caching",
            "تحسين Connection Pooling"
        ],
        "osf_impact": 0.08,  # Performance weight
        "deadline": "Month 2"
    },
    "reliability_improvements": {
        "priority": "HIGH",
        "tasks": [
            "إضافة Error Handling شامل",
            "تطبيق Logging متقدم",
            "إعداد Health Checks",
            "تحسين Exception Management"
        ],
        "osf_impact": 0.15,  # Reliability weight
        "deadline": "Month 3"
    }
}
```

### **المرحلة الثانية (شهر 4-6): تحسين الواجهات - OSF Score Target: 0.8**
```python
PHASE_2_TASKS = {
    "ui_redesign": {
        "priority": "HIGH",
        "tasks": [
            "إعادة تصميم بـ React 18+",
            "تطبيق Design System موحد",
            "تحسين Responsive Design",
            "تطوير PWA",
            "تحسين RTL للعربية"
        ],
        "osf_impact": 0.07,  # Usability weight
        "deadline": "Month 5"
    },
    "maintainability": {
        "priority": "MEDIUM",
        "tasks": [
            "توحيد Code Standards",
            "تحسين Documentation",
            "إضافة Unit Tests",
            "تطبيق CI/CD Pipeline"
        ],
        "osf_impact": 0.10,  # Maintainability weight
        "deadline": "Month 6"
    }
}
```

### **المرحلة الثالثة (شهر 7-9): الميزات المتقدمة - OSF Score Target: 0.85**
```python
PHASE_3_TASKS = {
    "microservices": {
        "priority": "MEDIUM",
        "tasks": [
            "تطبيق API Gateway",
            "تطوير خدمات مصغرة",
            "إعداد Service Discovery",
            "تطبيق Load Balancing"
        ],
        "osf_impact": 0.05,  # Scalability weight
        "deadline": "Month 8"
    },
    "ai_features": {
        "priority": "MEDIUM",
        "tasks": [
            "تطوير Sales Forecasting",
            "تطبيق Sentiment Analysis",
            "إضافة OCR للوثائق",
            "تطوير Recommendation Engine"
        ],
        "osf_impact": 0.07,  # Usability enhancement
        "deadline": "Month 9"
    }
}
```

### **المرحلة الرابعة (شهر 10-12): التحسينات النهائية - OSF Score Target: 0.9+**
```python
PHASE_4_TASKS = {
    "final_optimizations": {
        "priority": "LOW",
        "tasks": [
            "اختبارات الأداء الشاملة",
            "Security Penetration Testing",
            "Load Testing",
            "User Acceptance Testing"
        ],
        "osf_impact": 0.20,  # Overall correctness
        "deadline": "Month 11"
    },
    "deployment_preparation": {
        "priority": "LOW",
        "tasks": [
            "إعداد Production Environment",
            "تدريب المستخدمين",
            "إنشاء Documentation النهائي",
            "إطلاق النسخة النهائية"
        ],
        "osf_impact": 0.10,  # Maintainability
        "deadline": "Month 12"
    }
}
```

---

## **🧪 متطلبات الاختبار المحسنة**

### **1. اختبارات الأمان (Security Testing):**
```python
# FILE: tests/security/test_security.py
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
import requests

class SecurityTestSuite(TestCase):
    """مجموعة اختبارات الأمان الشاملة"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!',
            email='test@example.com'
        )
    
    def test_sql_injection_protection(self):
        """اختبار الحماية من SQL Injection"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'/*",
            "1; DELETE FROM users WHERE 1=1; --"
        ]
        
        for payload in malicious_inputs:
            response = self.client.post('/api/login/', {
                'username': payload,
                'password': 'password'
            })
            
            # يجب أن يفشل تسجيل الدخول
            self.assertNotEqual(response.status_code, 200)
            
            # التحقق من عدم تنفيذ SQL
            self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_xss_protection(self):
        """اختبار الحماية من XSS"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        self.client.login(username='testuser', password='TestPass123!')
        
        for payload in xss_payloads:
            response = self.client.post('/api/products/', {
                'name': payload,
                'description': 'Test product'
            })
            
            # التحقق من تنظيف المدخلات
            if response.status_code == 201:
                product_id = response.json()['id']
                product_response = self.client.get(f'/api/products/{product_id}/')
                
                # يجب ألا يحتوي الرد على الكود الضار
                self.assertNotIn('<script>', product_response.content.decode())
                self.assertNotIn('javascript:', product_response.content.decode())
    
    def test_csrf_protection(self):
        """اختبار الحماية من CSRF"""
        # محاولة طلب POST بدون CSRF token
        response = self.client.post('/api/users/', {
            'username': 'newuser',
            'password': 'password123'
        })
        
        # يجب أن يفشل الطلب
        self.assertEqual(response.status_code, 403)
    
    def test_rate_limiting(self):
        """اختبار حد المعدل"""
        # إرسال طلبات متعددة بسرعة
        for i in range(105):  # أكثر من الحد المسموح (100)
            response = self.client.post('/api/login/', {
                'username': 'testuser',
                'password': 'wrongpassword'
            })
        
        # يجب أن يتم حظر الطلبات الزائدة
        self.assertEqual(response.status_code, 429)
    
    def test_authentication_security(self):
        """اختبار أمان المصادقة"""
        # اختبار كلمات مرور ضعيفة
        weak_passwords = ['123456', 'password', 'admin', '12345678']
        
        for weak_pass in weak_passwords:
            response = self.client.post('/api/register/', {
                'username': 'weakuser',
                'password': weak_pass,
                'email': 'weak@example.com'
            })
            
            # يجب رفض كلمات المرور الضعيفة
            self.assertNotEqual(response.status_code, 201)
    
    def test_mfa_enforcement(self):
        """اختبار إنفاذ MFA"""
        # إنشاء مستخدم بدور يتطلب MFA
        admin_user = User.objects.create_user(
            username='admin',
            password='AdminPass123!',
            email='admin@example.com'
        )
        
        # محاولة الوصول لصفحة حساسة بدون MFA
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.get('/api/admin/users/')
        
        # يجب إعادة توجيه لإعداد MFA
        self.assertIn(response.status_code, [302, 403])
```

### **2. اختبارات الأداء (Performance Testing):**
```python
# FILE: tests/performance/test_performance.py
import time
import pytest
from django.test import TestCase
from django.test.utils import override_settings
from django.db import connection
from locust import HttpUser, task, between

class PerformanceTestSuite(TestCase):
    """مجموعة اختبارات الأداء"""
    
    def test_database_query_performance(self):
        """اختبار أداء استعلامات قاعدة البيانات"""
        # إنشاء بيانات اختبار
        from inventory.models import Product, Category
        
        category = Category.objects.create(name='Test Category')
        
        # إنشاء 1000 منتج
        products = []
        for i in range(1000):
            products.append(Product(
                name=f'Product {i}',
                category=category,
                price=100.00
            ))
        Product.objects.bulk_create(products)
        
        # اختبار استعلام مع قياس الوقت
        start_time = time.time()
        
        # استعلام محسن مع select_related
        products_list = list(Product.objects.select_related('category').all())
        
        end_time = time.time()
        query_time = end_time - start_time
        
        # يجب أن يكون الاستعلام سريعاً (أقل من ثانية واحدة)
        self.assertLess(query_time, 1.0)
        
        # التحقق من عدد الاستعلامات
        with self.assertNumQueries(1):
            list(Product.objects.select_related('category').all()[:10])
    
    def test_api_response_time(self):
        """اختبار زمن استجابة API"""
        from django.contrib.auth.models import User
        
        user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        
        self.client.login(username='testuser', password='testpass')
        
        # اختبار عدة endpoints
        endpoints = [
            '/api/dashboard/',
            '/api/products/',
            '/api/customers/',
            '/api/orders/'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # يجب أن يكون زمن الاستجابة أقل من 200ms
            self.assertLess(response_time, 0.2)
            self.assertEqual(response.status_code, 200)

class LoadTestUser(HttpUser):
    """مستخدم اختبار الحمولة"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """تسجيل الدخول عند البدء"""
        response = self.client.post("/api/auth/login/", {
            "username": "testuser",
            "password": "testpass"
        })
        
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
    
    @task(3)
    def view_dashboard(self):
        """عرض لوحة التحكم"""
        self.client.get("/api/dashboard/")
    
    @task(2)
    def view_products(self):
        """عرض المنتجات"""
        self.client.get("/api/products/")
    
    @task(1)
    def create_order(self):
        """إنشاء طلب"""
        self.client.post("/api/orders/", json={
            "customer_id": 1,
            "items": [
                {"product_id": 1, "quantity": 2}
            ]
        })
    
    @task(1)
    def search_products(self):
        """البحث في المنتجات"""
        self.client.get("/api/products/?search=test")
```

---

## **📚 متطلبات التوثيق المحسنة**

### **1. التوثيق التقني:**
```markdown
# FILE: docs/API_Documentation.md

# Gaara ERP v12 API Documentation

## Authentication

### JWT Token Authentication
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "SecurePassword123!"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 900,
    "user": {
        "id": 1,
        "username": "user@example.com",
        "company_id": 1,
        "roles": ["USER"]
    }
}
```

### MFA Setup
```http
POST /api/auth/mfa/setup/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
    "secret": "JBSWY3DPEHPK3PXP",
    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "backup_codes": ["A1B2C3D4", "E5F6G7H8", ...]
}
```

## Products API

### List Products
```http
GET /api/products/
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)
- `search`: Search term
- `category`: Category ID
- `active`: Filter by active status (true/false)

**Response:**
```json
{
    "data": [
        {
            "id": 1,
            "name": "Product Name",
            "sku": "PRD-001",
            "category": {
                "id": 1,
                "name": "Category Name"
            },
            "price": 99.99,
            "stock_quantity": 100,
            "active": true,
            "created_at": "2025-01-01T00:00:00Z"
        }
    ],
    "meta": {
        "page": 1,
        "limit": 20,
        "total": 150,
        "pages": 8
    }
}
```

### Create Product
```http
POST /api/products/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "New Product",
    "sku": "PRD-002",
    "category_id": 1,
    "price": 149.99,
    "cost": 75.00,
    "stock_quantity": 50,
    "description": "Product description",
    "active": true
}
```

## Error Handling

All API endpoints return errors in a consistent format:

```json
{
    "code": "VALIDATION_ERROR",
    "message": "The provided data is invalid",
    "details": {
        "name": ["This field is required"],
        "price": ["Must be a positive number"]
    },
    "trace_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-01-01T00:00:00Z"
}
```

### Common Error Codes
- `AUTHENTICATION_REQUIRED`: 401 - Authentication required
- `PERMISSION_DENIED`: 403 - Insufficient permissions
- `NOT_FOUND`: 404 - Resource not found
- `VALIDATION_ERROR`: 400 - Invalid input data
- `RATE_LIMIT_EXCEEDED`: 429 - Too many requests
- `INTERNAL_ERROR`: 500 - Server error
```

### **2. دليل المستخدم:**
```markdown
# FILE: docs/User_Guide.md

# دليل المستخدم - نظام Gaara ERP v12

## البدء السريع

### 1. تسجيل الدخول
1. افتح المتصفح وانتقل إلى رابط النظام
2. أدخل اسم المستخدم وكلمة المرور
3. أدخل رمز المصادقة الثنائية (إذا كان مفعلاً)
4. انقر على "تسجيل الدخول"

### 2. لوحة التحكم الرئيسية
بعد تسجيل الدخول، ستظهر لك لوحة التحكم التي تحتوي على:
- **الإحصائيات السريعة**: المبيعات، المشتريات، المخزون
- **التنبيهات**: المهام المعلقة والتنبيهات المهمة
- **الاختصارات**: روابط سريعة للوظائف الأكثر استخداماً

### 3. إدارة المنتجات

#### إضافة منتج جديد:
1. انتقل إلى قائمة "المخزون" → "المنتجات"
2. انقر على زر "إضافة منتج جديد"
3. املأ البيانات المطلوبة:
   - **اسم المنتج**: اسم واضح ومميز
   - **الرمز**: رمز فريد للمنتج (SKU)
   - **الفئة**: اختر الفئة المناسبة
   - **السعر**: سعر البيع
   - **التكلفة**: تكلفة المنتج
   - **الكمية**: الكمية المتوفرة في المخزون
4. انقر على "حفظ"

#### البحث عن المنتجات:
- استخدم مربع البحث في أعلى قائمة المنتجات
- يمكنك البحث بالاسم أو الرمز أو الوصف
- استخدم الفلاتر لتضييق نتائج البحث

### 4. إدارة العملاء

#### إضافة عميل جديد:
1. انتقل إلى "المبيعات" → "العملاء"
2. انقر على "إضافة عميل جديد"
3. املأ بيانات العميل:
   - **الاسم الكامل**
   - **رقم الهاتف**
   - **البريد الإلكتروني**
   - **العنوان**
   - **نوع العميل**: فرد أو شركة
4. احفظ البيانات

### 5. إنشاء فاتورة مبيعات

#### خطوات إنشاء الفاتورة:
1. انتقل إلى "المبيعات" → "الفواتير"
2. انقر على "فاتورة جديدة"
3. اختر العميل من القائمة
4. أضف المنتجات:
   - ابحث عن المنتج واختره
   - حدد الكمية
   - سيتم حساب الإجمالي تلقائياً
5. راجع تفاصيل الفاتورة
6. انقر على "حفظ وطباعة"

### 6. التقارير

#### تقرير المبيعات:
1. انتقل إلى "التقارير" → "تقارير المبيعات"
2. حدد الفترة الزمنية
3. اختر نوع التقرير:
   - تقرير يومي
   - تقرير شهري
   - تقرير سنوي
4. انقر على "إنشاء التقرير"
5. يمكنك تصدير التقرير بصيغة PDF أو Excel

### 7. الإعدادات

#### تغيير كلمة المرور:
1. انقر على اسمك في الزاوية العلوية
2. اختر "الإعدادات الشخصية"
3. انقر على "تغيير كلمة المرور"
4. أدخل كلمة المرور الحالية والجديدة
5. احفظ التغييرات

#### إعداد المصادقة الثنائية:
1. انتقل إلى "الإعدادات الشخصية"
2. انقر على "المصادقة الثنائية"
3. امسح رمز QR بتطبيق Google Authenticator
4. أدخل الرمز للتأكيد
5. احفظ رموز النسخ الاحتياطي في مكان آمن

## الأسئلة الشائعة

### س: كيف يمكنني استرداد كلمة المرور؟
ج: انقر على "نسيت كلمة المرور" في صفحة تسجيل الدخول، وأدخل بريدك الإلكتروني لتلقي رابط الاسترداد.

### س: ماذا أفعل إذا فقدت جهاز المصادقة الثنائية؟
ج: استخدم أحد رموز النسخ الاحتياطي، أو تواصل مع مدير النظام لإعادة تعيين المصادقة الثنائية.

### س: كيف يمكنني تصدير البيانات؟
ج: معظم التقارير والقوائم تحتوي على خيار "تصدير" يتيح لك حفظ البيانات بصيغة Excel أو PDF.
```

---

## **✅ معايير القبول المحدثة**

### **1. معايير الأمان (OSF: 35%):**
- **MFA إلزامي**: 100% من المستخدمين المميزين
- **تشفير البيانات**: AES-256 لجميع البيانات الحساسة
- **Security Headers**: تقييم A+ في Security Headers
- **Penetration Testing**: اجتياز اختبار اختراق شامل
- **OWASP Top 10**: حماية من جميع الثغرات الأساسية

### **2. معايير الأداء (OSF: 8%):**
- **زمن الاستجابة**: < 200ms للصفحات الأساسية
- **زمن تحميل الصفحة**: < 2 ثانية
- **معدل النقل**: > 1000 طلب/ثانية
- **استهلاك الذاكرة**: < 512MB لكل عملية
- **استعلامات قاعدة البيانات**: < 50ms للاستعلامات المعقدة

### **3. معايير الموثوقية (OSF: 15%):**
- **Uptime**: 99.9% أو أعلى
- **MTTR**: < 15 دقيقة لاستعادة الخدمة
- **Error Rate**: < 0.1% من إجمالي الطلبات
- **Data Integrity**: 100% دقة البيانات
- **Backup Success**: 100% نجاح النسخ الاحتياطية

### **4. معايير قابلية الصيانة (OSF: 10%):**
- **Code Coverage**: > 80% تغطية الاختبارات
- **Documentation**: 100% توثيق للAPI والوظائف
- **Code Quality**: تقييم A في SonarQube
- **Deployment Time**: < 10 دقائق للنشر
- **Rollback Time**: < 5 دقائق للعودة للإصدار السابق

### **5. معايير سهولة الاستخدام (OSF: 7%):**
- **User Satisfaction**: > 4.5/5 في استطلاعات المستخدمين
- **Task Completion Rate**: > 95% للمهام الأساسية
- **Learning Curve**: < 2 ساعة للمستخدم الجديد
- **Accessibility**: WCAG 2.1 AA compliance
- **Mobile Responsiveness**: 100% على جميع الأجهزة

### **6. معايير قابلية التوسع (OSF: 5%):**
- **Horizontal Scaling**: دعم 10x زيادة في المستخدمين
- **Database Scaling**: دعم 100M+ سجل
- **API Throughput**: > 10,000 طلب/ثانية
- **Storage Scalability**: دعم PB-scale data
- **Geographic Distribution**: دعم multi-region deployment

---

## **🎯 المؤشرات المستهدفة النهائية**

```python
# FILE: metrics/target_kpis.py

TARGET_METRICS = {
    "security": {
        "osf_weight": 0.35,
        "targets": {
            "mfa_adoption": 100,  # %
            "security_score": 95,  # /100
            "vulnerability_count": 0,  # critical/high
            "penetration_test_score": 90,  # /100
            "compliance_score": 95  # /100
        }
    },
    "performance": {
        "osf_weight": 0.08,
        "targets": {
            "response_time_p95": 200,  # ms
            "page_load_time": 2000,  # ms
            "throughput": 1000,  # req/sec
            "cpu_usage": 70,  # %
            "memory_usage": 80  # %
        }
    },
    "reliability": {
        "osf_weight": 0.15,
        "targets": {
            "uptime": 99.9,  # %
            "mttr": 15,  # minutes
            "error_rate": 0.1,  # %
            "data_accuracy": 100,  # %
            "backup_success": 100  # %
        }
    },
    "business": {
        "targets": {
            "market_share_mena": 15,  # % في المنطقة العربية
            "user_satisfaction": 4.5,  # /5
            "customer_retention": 95,  # %
            "revenue_growth": 200,  # % خلال عامين
            "competitive_ranking": 5  # top 5 globally
        }
    }
}

def calculate_osf_score(metrics: dict) -> float:
    """حساب نقاط OSF الإجمالية"""
    security_score = metrics.get('security_score', 0) / 100
    performance_score = metrics.get('performance_score', 0) / 100
    reliability_score = metrics.get('reliability_score', 0) / 100
    maintainability_score = metrics.get('maintainability_score', 0) / 100
    usability_score = metrics.get('usability_score', 0) / 100
    scalability_score = metrics.get('scalability_score', 0) / 100
    correctness_score = metrics.get('correctness_score', 0) / 100
    
    osf_score = (
        0.35 * security_score +
        0.20 * correctness_score +
        0.15 * reliability_score +
        0.10 * maintainability_score +
        0.08 * performance_score +
        0.07 * usability_score +
        0.05 * scalability_score
    )
    
    return osf_score

# الهدف النهائي: OSF Score > 0.9
TARGET_OSF_SCORE = 0.9
```

---

## **🚀 الخلاصة والبدء**

هذا البرومبت الشامل المحسن يوفر خارطة طريق مفصلة لتطوير نظام Gaara ERP v12 ليصبح من أفضل 5 أنظمة ERP في العالم. يركز على:

1. **الأمان أولاً** (35% من الأولوية)
2. **الجودة والصحة** (20% من الأولوية)  
3. **الموثوقية والاستقرار** (15% من الأولوية)
4. **سهولة الصيانة والتطوير** (10% من الأولوية)
5. **الأداء والسرعة** (8% من الأولوية)
6. **تجربة المستخدم** (7% من الأولوية)
7. **قابلية التوسع** (5% من الأولوية)

### **البدء الفوري:**
1. ابدأ بالمرحلة الأولى (الإصلاحات الحرجة)
2. طبق إطار OSF في جميع القرارات
3. اتبع خطة التنفيذ المرحلية
4. قس التقدم باستخدام المؤشرات المحددة
5. استهدف OSF Score > 0.9 للوصول للمستوى العالمي

**الهدف النهائي**: تحويل Gaara ERP v12 إلى نظام عالمي المستوى قادر على منافسة Odoo و SAP خلال عامين.
