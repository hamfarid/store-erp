"""
AI Trainer - Gaara Scan AI v4.3.1
Automatic training system for disease detection models
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class AITrainer:
    """Automatic AI training system"""
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize trainer
        
        Args:
            models_dir: Directory to save trained models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.training_history = []
    
    async def train_model(
        self,
        images_dir: str,
        model_name: str = "disease_detector",
        epochs: int = 10,
        batch_size: int = 32
    ) -> Dict:
        """
        Train disease detection model
        
        Args:
            images_dir: Directory containing training images
            model_name: Name for the trained model
            epochs: Number of training epochs
            batch_size: Training batch size
            
        Returns:
            Training results dictionary
        """
        logger.info(f"Starting model training: {model_name}")
        
        try:
            # Prepare dataset
            dataset = await self._prepare_dataset(images_dir)
            
            if len(dataset) < 10:
                raise ValueError("Insufficient training data (minimum 10 images required)")
            
            # Build model
            model = await self._build_model(dataset)
            
            # Train model
            history = await self._train(model, dataset, epochs, batch_size)

            # Save model
            model_path = self.models_dir / f"{model_name}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.h5"
            await self._save_model(model, model_path)

            # Record training history
            training_record = {
                "model_name": model_name,
                "model_path": str(model_path),
                "dataset_size": len(dataset),
                "epochs": epochs,
                "batch_size": batch_size,
                "history": history,
                "trained_at": datetime.now(timezone.utc).isoformat()
            }
            self.training_history.append(training_record)
            
            logger.info(f"Model training completed: {model_path}")
            
            return {
                "success": True,
                "model_path": str(model_path),
                "accuracy": history.get("accuracy", 0.0),
                "loss": history.get("loss", 0.0),
                "message": "Model trained successfully"
            }
            
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Model training failed"
            }
    
    async def _prepare_dataset(self, images_dir: str) -> List[Dict]:
        """
        Prepare training dataset
        
        Args:
            images_dir: Directory containing images
            
        Returns:
            List of image data dictionaries
        """
        try:
            from PIL import Image
            import numpy as np
            
            images_path = Path(images_dir)
            dataset = []
            
            # Load images
            for img_file in images_path.glob("*.jpg"):
                try:
                    # Load image
                    img = Image.open(img_file)
                    img = img.resize((224, 224))  # Standard size for CNN
                    img_array = np.array(img) / 255.0  # Normalize
                    
                    # Extract label from filename or metadata
                    label = self._extract_label(img_file)
                    
                    dataset.append({
                        "image": img_array,
                        "label": label,
                        "path": str(img_file)
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to load image {img_file}: {str(e)}")
                    continue
            
            logger.info(f"Prepared dataset with {len(dataset)} images")
            return dataset
            
        except Exception as e:
            logger.error(f"Dataset preparation failed: {str(e)}")
            raise
    
    def _extract_label(self, image_path: Path) -> str:
        """
        Extract label from image filename or metadata
        
        Args:
            image_path: Path to image file
            
        Returns:
            Label string
        """
        # Try to extract from filename
        # Format: disease_name_timestamp_hash.jpg
        parts = image_path.stem.split("_")
        if len(parts) >= 2:
            return parts[0]
        return "unknown"
    
    async def _build_model(self, dataset: List[Dict]) -> object:
        """
        Build CNN model for disease detection
        
        Args:
            dataset: Training dataset
            
        Returns:
            Compiled model
        """
        try:
            import tensorflow as tf
            from tensorflow import keras
            from tensorflow.keras import layers
            
            # Get unique labels
            labels = list(set([d["label"] for d in dataset]))
            num_classes = len(labels)
            
            # Build model
            model = keras.Sequential([
                layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.Flatten(),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.5),
                layers.Dense(num_classes, activation='softmax')
            ])
            
            # Compile model
            model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            logger.info(f"Built model for {num_classes} classes")
            return model
            
        except Exception as e:
            logger.error(f"Model building failed: {str(e)}")
            raise
    
    async def _train(
        self,
        model: object,
        dataset: List[Dict],
        epochs: int,
        batch_size: int
    ) -> Dict:
        """
        Train the model
        
        Args:
            model: Model to train
            dataset: Training dataset
            epochs: Number of epochs
            batch_size: Batch size
            
        Returns:
            Training history
        """
        try:
            import numpy as np
            
            # Prepare data
            X = np.array([d["image"] for d in dataset])
            y = np.array([self._label_to_int(d["label"]) for d in dataset])
            
            # Split train/validation
            split_idx = int(len(X) * 0.8)
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]
            
            # Train model
            history = model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                verbose=1
            )
            
            # Get final metrics
            final_metrics = {
                "accuracy": float(history.history['accuracy'][-1]),
                "val_accuracy": float(history.history['val_accuracy'][-1]),
                "loss": float(history.history['loss'][-1]),
                "val_loss": float(history.history['val_loss'][-1])
            }
            
            logger.info(f"Training completed: accuracy={final_metrics['accuracy']:.4f}")
            return final_metrics
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise
    
    def _label_to_int(self, label: str) -> int:
        """Convert label string to integer"""
        # Simple hash-based conversion
        return hash(label) % 100
    
    async def _save_model(self, model: object, model_path: Path):
        """
        Save trained model
        
        Args:
            model: Trained model
            model_path: Path to save model
        """
        try:
            model.save(model_path)
            logger.info(f"Model saved to {model_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {str(e)}")
            raise
    
    def get_training_history(self) -> List[Dict]:
        """Get training history"""
        return self.training_history

# Global instance
trainer = AITrainer()
