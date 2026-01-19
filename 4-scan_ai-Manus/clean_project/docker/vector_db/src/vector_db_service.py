"""
خدمة قاعدة البيانات الشعاعية المتقدمة
Vector Database Service for Gaara Scan AI

يوفر هذا الملف خدمة شاملة للبحث الشعاعي والتشابه الدلالي
مع دعم متعدد لمحركات البحث المختلفة
"""

import os
import json
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

# FastAPI والمكتبات المساعدة
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# مكتبات الذكاء الاصطناعي
from sentence_transformers import SentenceTransformer
import faiss
import torch

# مكتبات قواعد البيانات
import redis
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# مكتبات المراقبة
from prometheus_client import Counter, Histogram, generate_latest
import structlog

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()

# إعداد التطبيق
app = FastAPI(
    title="Gaara Vector Database Service",
    description="خدمة قاعدة البيانات الشعاعية المتقدمة للبحث الدلالي",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# متغيرات البيئة
VECTOR_MODEL_PATH = os.getenv("VECTOR_MODEL_PATH", "/opt/venv/vector_model")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "/app/data/indices")
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "768"))
MAX_VECTORS = int(os.getenv("MAX_VECTORS", "1000000"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

# مقاييس Prometheus
vector_operations = Counter('vector_operations_total', 'Total vector operations', ['operation'])
vector_search_duration = Histogram('vector_search_duration_seconds', 'Vector search duration')
vector_index_size = Counter('vector_index_size_total', 'Total vectors in index')

# نماذج البيانات
class VectorDocument(BaseModel):
    """نموذج وثيقة شعاعية"""
    id: str = Field(..., description="معرف فريد للوثيقة")
    content: str = Field(..., description="محتوى النص")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="بيانات وصفية")
    category: Optional[str] = Field(None, description="فئة الوثيقة")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="وقت الإنشاء")

class VectorSearchQuery(BaseModel):
    """نموذج استعلام البحث الشعاعي"""
    query: str = Field(..., description="نص الاستعلام")
    top_k: int = Field(default=10, ge=1, le=100, description="عدد النتائج المطلوبة")
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="حد التشابه")
    category_filter: Optional[str] = Field(None, description="تصفية حسب الفئة")
    metadata_filter: Optional[Dict[str, Any]] = Field(None, description="تصفية حسب البيانات الوصفية")

class VectorSearchResult(BaseModel):
    """نموذج نتيجة البحث الشعاعي"""
    id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]
    category: Optional[str]

class VectorBatchOperation(BaseModel):
    """نموذج العمليات المجمعة"""
    documents: List[VectorDocument] = Field(..., description="قائمة الوثائق")
    operation: str = Field(..., description="نوع العملية: add, update, delete")

# فئة إدارة قاعدة البيانات الشعاعية
class VectorDatabaseManager:
    """مدير قاعدة البيانات الشعاعية المتقدم"""
    
    def __init__(self):
        self.model = None
        self.faiss_index = None
        self.redis_client = None
        self.document_store = {}
        self.metadata_store = {}
        self.category_index = {}
        
    async def initialize(self):
        """تهيئة النظام"""
        try:
            # تحميل نموذج التضمين
            logger.info("Loading sentence transformer model...")
            self.model = SentenceTransformer(VECTOR_MODEL_PATH)
            
            # تهيئة فهرس FAISS
            logger.info("Initializing FAISS index...")
            self.faiss_index = faiss.IndexFlatIP(VECTOR_DIMENSION)
            
            # تهيئة Redis
            logger.info("Connecting to Redis...")
            self.redis_client = redis.Redis(
                host=os.getenv("REDIS_HOST", "redis"),
                port=int(os.getenv("REDIS_PORT", "6379")),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
            )
            
            # تحميل البيانات المحفوظة
            await self.load_existing_data()
            
            logger.info("Vector database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {e}")
            raise
    
    async def load_existing_data(self):
        """تحميل البيانات الموجودة"""
        try:
            # تحميل الفهرس من الملف إذا كان موجوداً
            index_file = Path(FAISS_INDEX_PATH) / "main_index.bin"
            if index_file.exists():
                self.faiss_index = faiss.read_index(str(index_file))
                logger.info(f"Loaded existing FAISS index with {self.faiss_index.ntotal} vectors")
            
            # تحميل البيانات الوصفية من Redis
            stored_docs = self.redis_client.hgetall("vector_documents")
            for doc_id, doc_data in stored_docs.items():
                self.document_store[doc_id] = json.loads(doc_data)
            
            logger.info(f"Loaded {len(self.document_store)} documents from storage")
            
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
    
    async def save_data(self):
        """حفظ البيانات"""
        try:
            # حفظ فهرس FAISS
            os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
            index_file = Path(FAISS_INDEX_PATH) / "main_index.bin"
            faiss.write_index(self.faiss_index, str(index_file))
            
            # حفظ البيانات الوصفية في Redis
            for doc_id, doc_data in self.document_store.items():
                self.redis_client.hset("vector_documents", doc_id, json.dumps(doc_data))
            
            logger.info("Data saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    def encode_text(self, text: str) -> np.ndarray:
        """تحويل النص إلى شعاع"""
        try:
            vector = self.model.encode([text], normalize_embeddings=True)
            return vector[0]
        except Exception as e:
            logger.error(f"Failed to encode text: {e}")
            raise
    
    async def add_document(self, document: VectorDocument) -> bool:
        """إضافة وثيقة جديدة"""
        try:
            # تحويل النص إلى شعاع
            vector = self.encode_text(document.content)
            
            # إضافة الشعاع إلى الفهرس
            self.faiss_index.add(vector.reshape(1, -1))
            
            # حفظ البيانات الوصفية
            doc_data = {
                "content": document.content,
                "metadata": document.metadata,
                "category": document.category,
                "timestamp": document.timestamp.isoformat() if document.timestamp else None,
                "vector_id": self.faiss_index.ntotal - 1
            }
            
            self.document_store[document.id] = doc_data
            
            # تحديث فهرس الفئات
            if document.category:
                if document.category not in self.category_index:
                    self.category_index[document.category] = []
                self.category_index[document.category].append(document.id)
            
            # تحديث المقاييس
            vector_operations.labels(operation='add').inc()
            vector_index_size.inc()
            
            logger.info(f"Added document {document.id} to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add document {document.id}: {e}")
            return False
    
    async def search_similar(self, query: VectorSearchQuery) -> List[VectorSearchResult]:
        """البحث عن الوثائق المشابهة"""
        try:
            with vector_search_duration.time():
                # تحويل الاستعلام إلى شعاع
                query_vector = self.encode_text(query.query)
                
                # البحث في الفهرس
                scores, indices = self.faiss_index.search(
                    query_vector.reshape(1, -1), 
                    min(query.top_k * 2, self.faiss_index.ntotal)  # البحث عن عدد أكبر للتصفية
                )
                
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx == -1:  # لا توجد نتائج أكثر
                        break
                    
                    if score < query.similarity_threshold:
                        continue
                    
                    # العثور على الوثيقة المقابلة
                    doc_id = None
                    for doc_id, doc_data in self.document_store.items():
                        if doc_data.get("vector_id") == idx:
                            break
                    
                    if not doc_id:
                        continue
                    
                    doc_data = self.document_store[doc_id]
                    
                    # تطبيق التصفية
                    if query.category_filter and doc_data.get("category") != query.category_filter:
                        continue
                    
                    if query.metadata_filter:
                        metadata_match = all(
                            doc_data.get("metadata", {}).get(k) == v 
                            for k, v in query.metadata_filter.items()
                        )
                        if not metadata_match:
                            continue
                    
                    result = VectorSearchResult(
                        id=doc_id,
                        content=doc_data["content"],
                        similarity_score=float(score),
                        metadata=doc_data.get("metadata", {}),
                        category=doc_data.get("category")
                    )
                    results.append(result)
                    
                    if len(results) >= query.top_k:
                        break
                
                # تحديث المقاييس
                vector_operations.labels(operation='search').inc()
                
                logger.info(f"Found {len(results)} similar documents for query")
                return results
                
        except Exception as e:
            logger.error(f"Failed to search similar documents: {e}")
            raise HTTPException(status_code=500, detail=f"Search failed: {e}")
    
    async def delete_document(self, document_id: str) -> bool:
        """حذف وثيقة"""
        try:
            if document_id not in self.document_store:
                return False
            
            doc_data = self.document_store[document_id]
            
            # إزالة من فهرس الفئات
            if doc_data.get("category"):
                category = doc_data["category"]
                if category in self.category_index:
                    self.category_index[category].remove(document_id)
                    if not self.category_index[category]:
                        del self.category_index[category]
            
            # إزالة من المخزن
            del self.document_store[document_id]
            
            # ملاحظة: FAISS لا يدعم الحذف المباشر، نحتاج لإعادة بناء الفهرس
            # في بيئة الإنتاج، يمكن استخدام حل أكثر تطوراً
            
            vector_operations.labels(operation='delete').inc()
            logger.info(f"Deleted document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """إحصائيات قاعدة البيانات"""
        return {
            "total_documents": len(self.document_store),
            "total_vectors": self.faiss_index.ntotal if self.faiss_index else 0,
            "categories": list(self.category_index.keys()),
            "vector_dimension": VECTOR_DIMENSION,
            "memory_usage": f"{self.faiss_index.ntotal * VECTOR_DIMENSION * 4 / 1024 / 1024:.2f} MB" if self.faiss_index else "0 MB"
        }

# إنشاء مثيل المدير
vector_manager = VectorDatabaseManager()

# نقاط النهاية
@app.on_event("startup")
async def startup_event():
    """تهيئة التطبيق عند البدء"""
    await vector_manager.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    """حفظ البيانات عند الإغلاق"""
    await vector_manager.save_data()

@app.get("/health")
async def health_check():
    """فحص صحة الخدمة"""
    return {
        "status": "healthy",
        "service": "vector_database",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.post("/documents", response_model=Dict[str, Any])
async def add_document(document: VectorDocument):
    """إضافة وثيقة جديدة"""
    success = await vector_manager.add_document(document)
    if success:
        return {"message": "Document added successfully", "document_id": document.id}
    else:
        raise HTTPException(status_code=500, detail="Failed to add document")

@app.post("/search", response_model=List[VectorSearchResult])
async def search_documents(query: VectorSearchQuery):
    """البحث في الوثائق"""
    return await vector_manager.search_similar(query)

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """حذف وثيقة"""
    success = await vector_manager.delete_document(document_id)
    if success:
        return {"message": "Document deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Document not found")

@app.post("/batch", response_model=Dict[str, Any])
async def batch_operation(operation: VectorBatchOperation, background_tasks: BackgroundTasks):
    """عمليات مجمعة"""
    async def process_batch():
        results = {"success": 0, "failed": 0, "errors": []}
        
        for document in operation.documents:
            try:
                if operation.operation == "add":
                    success = await vector_manager.add_document(document)
                elif operation.operation == "delete":
                    success = await vector_manager.delete_document(document.id)
                else:
                    success = False
                    results["errors"].append(f"Unknown operation: {operation.operation}")
                
                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Document {document.id}: {str(e)}")
        
        logger.info(f"Batch operation completed: {results}")
    
    background_tasks.add_task(process_batch)
    return {"message": "Batch operation started", "total_documents": len(operation.documents)}

@app.get("/statistics")
async def get_statistics():
    """إحصائيات قاعدة البيانات"""
    return await vector_manager.get_statistics()

@app.get("/categories")
async def get_categories():
    """قائمة الفئات المتاحة"""
    return {"categories": list(vector_manager.category_index.keys())}

@app.get("/metrics")
async def get_metrics():
    """مقاييس Prometheus"""
    return generate_latest()

if __name__ == "__main__":
    uvicorn.run(
        "vector_db_service:app",
        host="0.0.0.0",
        port=8006,
        reload=False,
        workers=1
    )

