"""
Module: rag_api.py
Rag Api — part of Global System v26.0.2 Diamond 32.
"""
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add tools directory to path to import RAGEngine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tools")))

try:
    from rag_engine import RAGEngine
except ImportError:
    print("Error: Could not import RAGEngine. Make sure tools/rag_engine.py exists.")
    sys.exit(1)

app = FastAPI(title="RAG API Service", version="1.0.0")

# Initialize RAGEngine (No arguments needed as per new signature)
engine = RAGEngine()

class IngestRequest(BaseModel):
    """
    Ingestrequest implementation.
    """
    file_path: str

class QueryRequest(BaseModel):
    """
    Queryrequest implementation.
    """
    query: str

@app.post("/ingest")
async def ingest_document(request: IngestRequest):
    """
    Ingest document implementation.
    """
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    success = engine.ingest(request.file_path)
    if success:
        return {"status": "success", "message": f"Ingested {request.file_path}"}
    else:
        raise HTTPException(status_code=500, detail="Ingestion failed")

@app.post("/query")
async def query_knowledge(request: QueryRequest):
    """
    Query knowledge implementation.
    """
    results = engine.query(request.query)
    return {"results": results, "count": len(results)}

@app.get("/health")
async def health_check():
    """
    Health check implementation.
    """
    return {"status": "active", "mode": engine.mode}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
