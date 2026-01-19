# a2a_communication Service - Gaara Scan AI
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gaara a2a_communication Service")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "a2a_communication"}

@app.get("/")
def root():
    return {"service": "a2a_communication", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
