# cloud_integration Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara cloud_integration Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "cloud_integration"}

@app.get("/")
def root():
    return {"service": "cloud_integration", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
