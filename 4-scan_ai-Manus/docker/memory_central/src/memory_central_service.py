# memory_central Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara memory_central Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "memory_central"}

@app.get("/")
def root():
    return {"service": "memory_central", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
