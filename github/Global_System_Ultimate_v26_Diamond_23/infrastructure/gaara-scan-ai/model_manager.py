import os
import torch
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
from ultralytics import YOLO
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GPU/CPU Fallback
device = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f"Using device: {device}")

# Load Models
try:
    yolo_model = YOLO('yolov8n.pt')  # Load a pretrained YOLOv8n model
    yolo_model.to(device)
    logger.info("YOLO model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load YOLO model: {e}")
    yolo_model = None

# Placeholder for CNN model loading
cnn_model = None 

@app.post("/predict/yolo")
async def predict_yolo(file: UploadFile = File(...)):
    if not yolo_model:
        return {"error": "YOLO model not available"}
    
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    results = yolo_model(image)
    predictions = []
    for result in results:
        for box in result.boxes:
            predictions.append({
                "class": int(box.cls),
                "confidence": float(box.conf),
                "bbox": box.xywh.tolist()
            })
            
    return {"predictions": predictions, "device": device}

@app.get("/health")
def health_check():
    return {"status": "healthy", "device": device}
