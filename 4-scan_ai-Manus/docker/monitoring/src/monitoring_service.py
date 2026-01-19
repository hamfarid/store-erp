# monitoring Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara monitoring Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "monitoring"}

@app.get("/")
def root():
    return {"service": "monitoring", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
