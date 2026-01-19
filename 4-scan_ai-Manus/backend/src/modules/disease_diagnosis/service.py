#!/usr/bin/env python3
"""
Disease Diagnosis Service
Provides a service wrapper for disease diagnosis functionality
"""

import logging
from typing import Any, Dict, List, Optional

from .db_service import init_db
from .diagnosis_engine import DiagnosisEngine

# Setup logging
logger = logging.getLogger(__name__)


class DiseaseDiagnosisService:
    """Service wrapper for disease diagnosis functionality"""

    def __init__(self):
        """Initialize the disease diagnosis service"""
        self.diagnosis_engine = None
        self.is_initialized = False
        self.db_initialized = False

        try:
            # Try to initialize database (may fail if DB is not available)
            try:
                init_db()
                self.db_initialized = True
                logger.info("Database initialized successfully")
            except Exception as db_error:
                logger.warning(
                    "Database initialization failed: %s",
                    str(db_error))
                logger.warning("Service will run with limited functionality")

            # Initialize diagnosis engine (can work without DB)
            self.diagnosis_engine = DiagnosisEngine()
            self.is_initialized = True

            logger.info("Disease Diagnosis Service initialized successfully")
        except Exception as e:
            logger.error(
                "Failed to initialize Disease Diagnosis Service: %s",
                str(e))
            self.is_initialized = False

    def is_ready(self) -> bool:
        """Check if the service is ready"""
        return self.is_initialized

    def get_version(self) -> str:
        """Get service version"""
        return "1.0.0"

    def diagnose(self, image_path: str,
                 crop_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Diagnose plant disease from image

        Args:
            image_path: Path to the image file
            crop_name: Optional crop name for better diagnosis

        Returns:
            Diagnosis results
        """
        if not self.is_initialized:
            return {
                "success": False,
                "error": "Service not initialized"
            }

        try:
            # Use diagnosis engine
            if self.diagnosis_engine:
                results = self.diagnosis_engine.diagnose(image_path, crop_name)
                return {
                    "success": True,
                    "results": results
                }
            else:
                return {
                    "success": False,
                    "error": "Diagnosis engine not available"
                }
        except Exception as e:
            logger.error("Error during diagnosis: %s", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def get_crop_diseases(self, crop_name: str) -> List[Dict[str, Any]]:
        """
        Get all diseases for a specific crop

        Args:
            crop_name: Name of the crop

        Returns:
            List of diseases
        """
        if not self.is_initialized:
            return []

        try:
            from .db_service import get_crop_by_name, get_diseases_by_crop

            crop = get_crop_by_name(crop_name)
            if crop:
                diseases = get_diseases_by_crop(crop['id'])
                return diseases
            return []
        except Exception as e:
            logger.error("Error getting crop diseases: %s", str(e))
            return []

    def get_all_crops(self) -> List[Dict[str, Any]]:
        """
        Get all available crops

        Returns:
            List of crops
        """
        if not self.is_initialized:
            return []

        try:
            from .db_service import get_all_crops
            return get_all_crops()
        except Exception as e:
            logger.error("Error getting crops: %s", str(e))
            return []
