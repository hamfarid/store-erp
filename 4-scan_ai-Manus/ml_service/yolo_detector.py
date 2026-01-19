"""
YOLO Detector - Gaara Scan AI v4.3.1
Object detection and disease localization using YOLO
"""

import cv2
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Tuple, Optional
import torch

logger = logging.getLogger(__name__)

class YOLODetector:
    """YOLO-based disease detection and localization"""
    
    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        """
        Initialize YOLO detector
        
        Args:
            model_path: Path to YOLO model weights
            confidence_threshold: Minimum confidence for detections
        """
        self.confidence_threshold = confidence_threshold
        self.model_path = model_path or "models/yolov8n.pt"
        self.model = None
        self.class_names = [
            "healthy_leaf",
            "bacterial_spot",
            "early_blight",
            "late_blight",
            "leaf_mold",
            "septoria_leaf_spot",
            "spider_mites",
            "target_spot",
            "yellow_leaf_curl",
            "mosaic_virus"
        ]
        
        self._load_model()
    
    def _load_model(self):
        """Load YOLO model"""
        try:
            # Try to load YOLOv8 from ultralytics
            try:
                from ultralytics import YOLO
                self.model = YOLO(self.model_path)
                logger.info(f"Loaded YOLOv8 model from {self.model_path}")
            except ImportError:
                logger.warning("ultralytics not installed, using PyTorch Hub")
                # Fallback to YOLOv5 from PyTorch Hub
                self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
                logger.info("Loaded YOLOv5 model from PyTorch Hub")
                
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {str(e)}")
            self.model = None
    
    def detect(self, image_path: str) -> List[Dict]:
        """
        Detect diseases in image
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of detection dictionaries
        """
        if self.model is None:
            logger.error("YOLO model not loaded")
            return []
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            
            # Run inference
            results = self.model(image)
            
            # Parse results
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    confidence = float(box.conf[0])
                    if confidence < self.confidence_threshold:
                        continue
                    
                    class_id = int(box.cls[0])
                    bbox = box.xyxy[0].tolist()
                    
                    detection = {
                        "class_id": class_id,
                        "class_name": self.class_names[class_id] if class_id < len(self.class_names) else "unknown",
                        "confidence": confidence,
                        "bbox": {
                            "x1": bbox[0],
                            "y1": bbox[1],
                            "x2": bbox[2],
                            "y2": bbox[3]
                        }
                    }
                    detections.append(detection)
            
            logger.info(f"Detected {len(detections)} objects in {image_path}")
            return detections
            
        except Exception as e:
            logger.error(f"Detection failed: {str(e)}")
            return []
    
    def detect_from_bytes(self, image_bytes: bytes) -> List[Dict]:
        """
        Detect diseases from image bytes
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            List of detection dictionaries
        """
        if self.model is None:
            logger.error("YOLO model not loaded")
            return []
        
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Failed to decode image")
            
            # Run inference
            results = self.model(image)
            
            # Parse results
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    confidence = float(box.conf[0])
                    if confidence < self.confidence_threshold:
                        continue
                    
                    class_id = int(box.cls[0])
                    bbox = box.xyxy[0].tolist()
                    
                    detection = {
                        "class_id": class_id,
                        "class_name": self.class_names[class_id] if class_id < len(self.class_names) else "unknown",
                        "confidence": confidence,
                        "bbox": {
                            "x1": bbox[0],
                            "y1": bbox[1],
                            "x2": bbox[2],
                            "y2": bbox[3]
                        }
                    }
                    detections.append(detection)
            
            logger.info(f"Detected {len(detections)} objects from bytes")
            return detections
            
        except Exception as e:
            logger.error(f"Detection from bytes failed: {str(e)}")
            return []
    
    def annotate_image(self, image_path: str, output_path: str) -> bool:
        """
        Annotate image with detections
        
        Args:
            image_path: Path to input image
            output_path: Path to save annotated image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            
            # Get detections
            detections = self.detect(image_path)
            
            # Draw bounding boxes
            for det in detections:
                bbox = det["bbox"]
                x1, y1, x2, y2 = int(bbox["x1"]), int(bbox["y1"]), int(bbox["x2"]), int(bbox["y2"])
                
                # Draw rectangle
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{det['class_name']}: {det['confidence']:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Save annotated image
            cv2.imwrite(output_path, image)
            logger.info(f"Saved annotated image to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Image annotation failed: {str(e)}")
            return False

# Global instance
yolo_detector = YOLODetector()
