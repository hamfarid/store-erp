# auto_learning Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara auto_learning Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "auto_learning"}

@app.get("/")
def root():
    return {"service": "auto_learning", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
