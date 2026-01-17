# /home/ubuntu/gaara_erp_v12/api_gateway/main.py

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
import jwt
import redis
from typing import Optional
import asyncio
import time
from contextlib import asynccontextmanager

# SECURITY FIX: Load JWT secret from environment variable (No hardcoded secrets)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError(
        "CRITICAL SECURITY ERROR: JWT_SECRET_KEY environment variable not set. "
        "Please set JWT_SECRET_KEY in your .env file or environment variables."
    )

# إعداد Redis للتخزين المؤقت
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# إعداد الخدمات
SERVICES = {
    'ai': os.getenv('AI_SERVICE_URL', 'http://ai_service:8000'),
    'accounting': os.getenv('ACCOUNTING_SERVICE_URL', 'http://accounting_service:8000'),
    'inventory': os.getenv('INVENTORY_SERVICE_URL', 'http://inventory_service:8000'),
    'sales': os.getenv('SALES_SERVICE_URL', 'http://sales_service:8000'),
}

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # بدء تشغيل التطبيق
    print("🚀 API Gateway starting...")
    yield
    # إيقاف التطبيق
    print("🛑 API Gateway shutting down...")

app = FastAPI(
    title="Gaara ERP API Gateway",
    description="مدخل موحد لجميع خدمات نظام Gaara ERP",
    version="12.0.0",
    lifespan=lifespan
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# دالة للتحقق من صحة الرمز المميز
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        # التحقق من الرمز المميز في Redis أولاً
        cached_user = redis_client.get(f"token:{token}")
        if cached_user:
            return {"user_id": cached_user}

        # فك تشفير الرمز المميز (SECURITY FIX: Using env var instead of hardcoded secret)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        # حفظ في التخزين المؤقت
        redis_client.setex(f"token:{token}", 3600, user_id)

        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="انتهت صلاحية الرمز المميز")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="رمز مميز غير صالح")

# دالة لتوجيه الطلبات
async def route_request(service: str, path: str, request: Request, user: dict = None):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="الخدمة غير موجودة")

    service_url = SERVICES[service]
    url = f"{service_url}{path}"

    # إعداد الرؤوس
    headers = dict(request.headers)
    if user:
        headers["X-User-ID"] = str(user["user_id"])

    # إرسال الطلب
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if request.method == "GET":
                response = await client.get(url, headers=headers, params=request.query_params)
            elif request.method == "POST":
                body = await request.body()
                response = await client.post(url, headers=headers, content=body)
            elif request.method == "PUT":
                body = await request.body()
                response = await client.put(url, headers=headers, content=body)
            elif request.method == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise HTTPException(status_code=405, detail="طريقة غير مدعومة")

            return response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="انتهت مهلة الاتصال بالخدمة")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="خطأ في الاتصال بالخدمة")

# نقاط النهاية العامة
@app.get("/")
async def root():
    return {"message": "مرحباً بك في نظام Gaara ERP", "version": "12.0.0"}

@app.get("/health")
async def health_check():
    services_status = {}

    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(f"{service_url}/health")
                services_status[service_name] = "healthy" if response.status_code == 200 else "unhealthy"
            except:
                services_status[service_name] = "unreachable"

    return {
        "status": "healthy",
        "services": services_status,
        "timestamp": time.time()
    }

# توجيه طلبات الذكاء الاصطناعي
@app.api_route("/ai/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def ai_service(path: str, request: Request, user: dict = Depends(verify_token)):
    return await route_request("ai", f"/{path}", request, user)

# توجيه طلبات المحاسبة
@app.api_route("/accounting/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def accounting_service(path: str, request: Request, user: dict = Depends(verify_token)):
    return await route_request("accounting", f"/{path}", request, user)

# توجيه طلبات المخزون
@app.api_route("/inventory/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def inventory_service(path: str, request: Request, user: dict = Depends(verify_token)):
    return await route_request("inventory", f"/{path}", request, user)

# توجيه طلبات المبيعات
@app.api_route("/sales/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def sales_service(path: str, request: Request, user: dict = Depends(verify_token)):
    return await route_request("sales", f"/{path}", request, user)

# نقطة نهاية للمصادقة (بدون توجيه)
@app.post("/auth/login")
async def login(request: Request):
    # هذه نقطة نهاية مؤقتة للمصادقة
    body = await request.json()
    username = body.get("username")
    password = body.get("password")

    # التحقق المؤقت (يجب استبداله بنظام مصادقة حقيقي)
    if username == "admin" and password == "admin":
        # SECURITY FIX: Using env var instead of hardcoded secret
        token = jwt.encode({"user_id": 1, "username": username}, JWT_SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="بيانات اعتماد غير صحيحة")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
