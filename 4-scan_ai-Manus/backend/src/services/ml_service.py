"""
ML Service Client - Gaara Scan AI v4.3.1
Client for communicating with ML service
"""

import logging
from typing import Dict, List, Optional

import httpx
from fastapi import UploadFile

logger = logging.getLogger(__name__)


class MLServiceClient:
    """Client for ML Service communication"""

    def __init__(self, ml_service_url: str = "http://ml_service:8000"):
        """
        Initialize ML Service Client

        Args:
            ml_service_url: Base URL of ML service
        """
        self.base_url = ml_service_url
        self.timeout = 30.0

    async def diagnose_disease(
        self,
        symptoms: List[str],
        crop_type: str,
        environmental_conditions: Optional[Dict] = None
    ) -> Dict:
        """
        Diagnose disease based on symptoms

        Args:
            symptoms: List of observed symptoms
            crop_type: Type of crop
            environmental_conditions: Optional environmental data

        Returns:
            Diagnosis result dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/diagnose",
                    json={
                        "symptoms": symptoms,
                        "crop_type": crop_type,
                        "environmental_conditions": environmental_conditions
                    }
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"ML Service request failed: {str(e)}")
            raise Exception(f"Failed to communicate with ML service: {str(e)}")

    async def analyze_image(self, file: UploadFile) -> Dict:
        """
        Analyze image for disease detection

        Args:
            file: Uploaded image file

        Returns:
            Analysis result dictionary
        """
        try:
            # Read file content
            content = await file.read()

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                files = {
                    "file": (file.filename, content, file.content_type)
                }
                response = await client.post(
                    f"{self.base_url}/api/v1/analyze-image",
                    files=files
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Image analysis request failed: {str(e)}")
            raise Exception(f"Failed to analyze image: {str(e)}")
        finally:
            # Reset file pointer
            await file.seek(0)

    async def list_models(self) -> Dict:
        """
        List available ML models

        Returns:
            Dictionary with available models
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/v1/models")
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to list models: {str(e)}")
            raise Exception(f"Failed to get models list: {str(e)}")

    async def health_check(self) -> Dict:
        """
        Check ML service health

        Returns:
            Health status dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"ML service health check failed: {str(e)}")
            return {"status": "unhealthy", "error": str(e)}


# Global instance
ml_client = MLServiceClient()
