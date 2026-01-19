# event_system Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara event_system Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "event_system"}

@app.get("/")
def root():
    return {"service": "event_system", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
