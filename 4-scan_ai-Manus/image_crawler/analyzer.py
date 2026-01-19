"""
Image Analyzer - Gaara Scan AI v4.3.1
Intelligent image analysis and description using AI
"""

import logging
from typing import Dict, Optional
from pathlib import Path
import base64
import os

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """Intelligent image analyzer using AI"""
    
    def __init__(self):
        """Initialize analyzer"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_ai = bool(self.openai_api_key)
        
        if not self.use_ai:
            logger.warning("OpenAI API key not found, using rule-based analysis")
    
    async def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze image and extract information
        
        Args:
            image_path: Path to image file
            
        Returns:
            Analysis results dictionary
        """
        try:
            if self.use_ai:
                return await self._analyze_with_ai(image_path)
            else:
                return await self._analyze_rule_based(image_path)
                
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            return self._get_default_analysis(image_path)
    
    async def _analyze_with_ai(self, image_path: str) -> Dict:
        """
        Analyze image using OpenAI Vision API
        
        Args:
            image_path: Path to image file
            
        Returns:
            AI analysis results
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            # Read and encode image
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            # Create prompt for disease identification
            prompt = """Analyze this plant image and provide:
1. Disease name (if any disease is visible)
2. Confidence level (0.0 to 1.0)
3. Plant type (e.g., tomato, wheat, corn)
4. Symptoms observed
5. Severity (mild, moderate, severe)
6. Affected area percentage
7. Description in both English and Arabic

Format your response as JSON with these exact keys:
disease_name, confidence, plant_type, symptoms, severity, affected_area, description_en, description_ar"""
            
            # Call OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Parse response
            import json
            result = json.loads(response.choices[0].message.content)
            
            logger.info(f"AI analysis completed for {image_path}")
            return result
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return await self._analyze_rule_based(image_path)
    
    async def _analyze_rule_based(self, image_path: str) -> Dict:
        """
        Rule-based image analysis (fallback)
        
        Args:
            image_path: Path to image file
            
        Returns:
            Basic analysis results
        """
        try:
            from PIL import Image
            import numpy as np
            
            # Open image
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Basic color analysis
            avg_color = img_array.mean(axis=(0, 1))
            
            # Simple heuristics
            is_green = avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]
            has_brown_spots = avg_color[0] > 100 and avg_color[1] < 100
            
            # Determine disease based on simple rules
            if has_brown_spots:
                disease_name = "leaf_spot"
                confidence = 0.6
                symptoms = ["brown spots", "discoloration"]
            elif not is_green:
                disease_name = "yellowing"
                confidence = 0.5
                symptoms = ["yellowing", "chlorosis"]
            else:
                disease_name = "healthy"
                confidence = 0.7
                symptoms = ["none"]
            
            return {
                "disease_name": disease_name,
                "confidence": confidence,
                "plant_type": "unknown",
                "symptoms": symptoms,
                "severity": "moderate" if disease_name != "healthy" else "none",
                "affected_area": 30 if disease_name != "healthy" else 0,
                "description_en": f"Detected {disease_name} with {int(confidence*100)}% confidence",
                "description_ar": f"تم اكتشاف {disease_name} بنسبة ثقة {int(confidence*100)}%",
                "analysis_method": "rule_based"
            }
            
        except Exception as e:
            logger.error(f"Rule-based analysis failed: {str(e)}")
            return self._get_default_analysis(image_path)
    
    def _get_default_analysis(self, image_path: str) -> Dict:
        """
        Get default analysis when all methods fail
        
        Args:
            image_path: Path to image file
            
        Returns:
            Default analysis
        """
        return {
            "disease_name": "unknown",
            "confidence": 0.0,
            "plant_type": "unknown",
            "symptoms": [],
            "severity": "unknown",
            "affected_area": 0,
            "description_en": "Analysis failed",
            "description_ar": "فشل التحليل",
            "analysis_method": "default",
            "error": True
        }
