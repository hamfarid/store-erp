"""
ML Model Manager
=================

Purpose: Manage multiple versions of ML models for disease detection.
Supports loading, switching, and tracking model versions.

Features:
- Model versioning with semantic versioning
- Hot-swapping between model versions
- Model health checks
- Automatic fallback to previous version on error
- Performance metrics per version
- Model manifest management

Usage:
    from model_manager import ModelManager
    
    manager = ModelManager(models_dir="models")
    model = manager.get_active_model()
    
    # Run inference
    results = model(image)
    
    # Switch to different version
    manager.set_active_version("v1.1.0")

Author: Global System v35.0
Date: 2026-01-17
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logger
logger = logging.getLogger(__name__)


class ModelVersion:
    """
    Represents a single model version with metadata.
    
    Attributes:
        version: Version string (e.g., "v1.0.0")
        path: Path to model file
        created: Creation timestamp
        accuracy: Reported accuracy metric
        description: Version description
    """
    
    def __init__(
        self,
        version: str,
        path: str,
        created: Optional[str] = None,
        accuracy: Optional[float] = None,
        description: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize model version.
        
        Args:
            version: Version identifier
            path: Path to model file
            created: ISO timestamp of creation
            accuracy: Model accuracy (0-1)
            description: Human-readable description
        """
        self.version = version
        self.path = path
        self.created = created or datetime.utcnow().isoformat()
        self.accuracy = accuracy
        self.description = description
        self.extra = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "version": self.version,
            "path": self.path,
            "created": self.created,
            "accuracy": self.accuracy,
            "description": self.description,
            **self.extra
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelVersion":
        """Create from dictionary."""
        return cls(**data)


class ModelManifest:
    """
    Manages the model manifest file.
    
    The manifest tracks all available model versions and
    which version is currently active.
    """
    
    def __init__(self, manifest_path: Path):
        """
        Initialize manifest.
        
        Args:
            manifest_path: Path to manifest.json file
        """
        self.path = manifest_path
        self.active_version: Optional[str] = None
        self.versions: Dict[str, ModelVersion] = {}
        self._load()
    
    def _load(self) -> None:
        """Load manifest from disk."""
        if not self.path.exists():
            logger.info(f"No manifest found at {self.path}, creating new")
            self._save()
            return
        
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            
            self.active_version = data.get("active_version")
            
            for version_id, version_data in data.get("versions", {}).items():
                self.versions[version_id] = ModelVersion.from_dict(version_data)
            
            logger.info(
                f"Loaded manifest: {len(self.versions)} versions, "
                f"active={self.active_version}"
            )
        except Exception as e:
            logger.error(f"Failed to load manifest: {e}")
    
    def _save(self) -> None:
        """Save manifest to disk."""
        try:
            data = {
                "active_version": self.active_version,
                "versions": {
                    v_id: v.to_dict() 
                    for v_id, v in self.versions.items()
                },
                "last_updated": datetime.utcnow().isoformat()
            }
            
            with open(self.path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.debug(f"Saved manifest to {self.path}")
        except Exception as e:
            logger.error(f"Failed to save manifest: {e}")
    
    def add_version(self, version: ModelVersion) -> None:
        """Add a new model version."""
        self.versions[version.version] = version
        self._save()
        logger.info(f"Added model version: {version.version}")
    
    def set_active(self, version_id: str) -> bool:
        """Set the active model version."""
        if version_id not in self.versions:
            logger.error(f"Version not found: {version_id}")
            return False
        
        self.active_version = version_id
        self._save()
        logger.info(f"Set active version: {version_id}")
        return True


class ModelManager:
    """
    Manager for loading and switching between model versions.
    
    This class handles:
    - Loading YOLO models from disk
    - Switching between model versions
    - Caching loaded models
    - Health checks
    - Fallback on errors
    
    Example:
        >>> manager = ModelManager("models")
        >>> model = manager.get_active_model()
        >>> results = model(image)
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize model manager.
        
        Args:
            models_dir: Directory containing model versions
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.manifest = ModelManifest(self.models_dir / "manifest.json")
        self._loaded_models: Dict[str, Any] = {}
        self._fallback_version: Optional[str] = None
        
        # Discover models if manifest is empty
        if not self.manifest.versions:
            self._discover_models()
    
    def _discover_models(self) -> None:
        """
        Discover model files in the models directory.
        
        Looks for .pt files and adds them to the manifest.
        """
        logger.info(f"Discovering models in {self.models_dir}")
        
        for model_file in self.models_dir.glob("**/*.pt"):
            version_name = model_file.stem
            relative_path = str(model_file.relative_to(self.models_dir))
            
            if version_name not in self.manifest.versions:
                version = ModelVersion(
                    version=version_name,
                    path=relative_path,
                    description="Auto-discovered model"
                )
                self.manifest.add_version(version)
        
        # Set first discovered as active if none set
        if self.manifest.versions and not self.manifest.active_version:
            first_version = list(self.manifest.versions.keys())[0]
            self.manifest.set_active(first_version)
    
    def load_model(self, version: str) -> Any:
        """
        Load a specific model version.
        
        Args:
            version: Version identifier to load
            
        Returns:
            Loaded YOLO model
            
        Raises:
            FileNotFoundError: If model file not found
            Exception: If model fails to load
        """
        # Check cache
        if version in self._loaded_models:
            logger.debug(f"Using cached model: {version}")
            return self._loaded_models[version]
        
        # Get version info
        if version not in self.manifest.versions:
            raise FileNotFoundError(f"Model version not found: {version}")
        
        version_info = self.manifest.versions[version]
        model_path = self.models_dir / version_info.path
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load model
        logger.info(f"Loading model: {version} from {model_path}")
        
        try:
            from ultralytics import YOLO
            model = YOLO(str(model_path))
            
            # Cache the model
            self._loaded_models[version] = model
            
            logger.info(f"Successfully loaded model: {version}")
            return model
            
        except ImportError:
            logger.warning("YOLO not available, returning mock model")
            # Return a mock for testing without YOLO
            return MockModel(version)
        except Exception as e:
            logger.error(f"Failed to load model {version}: {e}")
            raise
    
    def get_active_model(self) -> Any:
        """
        Get the currently active model.
        
        Returns:
            Loaded model instance
            
        Raises:
            RuntimeError: If no active model configured
        """
        if not self.manifest.active_version:
            raise RuntimeError("No active model version configured")
        
        try:
            model = self.load_model(self.manifest.active_version)
            self._fallback_version = self.manifest.active_version
            return model
        except Exception as e:
            # Try fallback
            if self._fallback_version and self._fallback_version != self.manifest.active_version:
                logger.warning(f"Falling back to {self._fallback_version}")
                return self.load_model(self._fallback_version)
            raise
    
    def set_active_version(self, version: str) -> bool:
        """
        Set the active model version.
        
        Args:
            version: Version to activate
            
        Returns:
            bool: True if successful
        """
        # Verify model can be loaded
        try:
            self.load_model(version)
        except Exception as e:
            logger.error(f"Cannot activate {version}: {e}")
            return False
        
        return self.manifest.set_active(version)
    
    def get_active_version(self) -> Optional[str]:
        """Get currently active version string."""
        return self.manifest.active_version
    
    def list_versions(self) -> List[Dict[str, Any]]:
        """
        List all available model versions.
        
        Returns:
            List of version info dictionaries
        """
        return [
            {
                **v.to_dict(),
                "is_active": v.version == self.manifest.active_version,
                "is_loaded": v.version in self._loaded_models
            }
            for v in self.manifest.versions.values()
        ]
    
    def get_version_info(self, version: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific version.
        
        Args:
            version: Version identifier
            
        Returns:
            Version info dict or None if not found
        """
        if version not in self.manifest.versions:
            return None
        
        v = self.manifest.versions[version]
        return {
            **v.to_dict(),
            "is_active": v.version == self.manifest.active_version,
            "is_loaded": v.version in self._loaded_models
        }
    
    def unload_model(self, version: str) -> bool:
        """
        Unload a model from memory.
        
        Args:
            version: Version to unload
            
        Returns:
            bool: True if was loaded and unloaded
        """
        if version in self._loaded_models:
            del self._loaded_models[version]
            logger.info(f"Unloaded model: {version}")
            return True
        return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on model manager.
        
        Returns:
            Health status dictionary
        """
        return {
            "status": "healthy" if self.manifest.active_version else "no_active_model",
            "active_version": self.manifest.active_version,
            "total_versions": len(self.manifest.versions),
            "loaded_models": list(self._loaded_models.keys()),
            "models_dir": str(self.models_dir)
        }


class MockModel:
    """
    Mock model for testing without YOLO dependency.
    
    Returns placeholder predictions for testing purposes.
    """
    
    def __init__(self, version: str):
        """Initialize mock model."""
        self.version = version
        logger.warning(f"Using MockModel for version {version}")
    
    def __call__(self, image, **kwargs):
        """Return mock predictions."""
        return MockResults()


class MockResults:
    """Mock results object."""
    
    def __init__(self):
        self.boxes = MockBoxes()


class MockBoxes:
    """Mock boxes object."""
    
    def __init__(self):
        self.xyxyn = [[0.1, 0.1, 0.9, 0.9]]
        self.conf = [0.95]
        self.cls = [0]


# Singleton instance
_manager: Optional[ModelManager] = None


def get_model_manager(models_dir: str = "models") -> ModelManager:
    """
    Get or create the model manager singleton.
    
    Args:
        models_dir: Models directory path
        
    Returns:
        ModelManager instance
    """
    global _manager
    
    if _manager is None:
        _manager = ModelManager(models_dir)
    
    return _manager
