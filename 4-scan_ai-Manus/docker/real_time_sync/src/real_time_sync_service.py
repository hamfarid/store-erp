# real_time_sync Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara real_time_sync Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "real_time_sync"}

@app.get("/")
def root():
    return {"service": "real_time_sync", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
