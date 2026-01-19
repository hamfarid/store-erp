"""
Image Crawler Service Client - Gaara Scan AI v4.3.1
Backend client for communicating with Image Crawler service
"""

import logging
from typing import Dict, List

import httpx

logger = logging.getLogger(__name__)


class CrawlerServiceClient:
    """Client for Image Crawler service"""

    def __init__(self, base_url: str = "http://image_crawler:8001"):
        """
        Initialize crawler service client

        Args:
            base_url: Base URL of crawler service
        """
        self.base_url = base_url
        self.timeout = 30.0

    async def start_crawl(
        self,
        query: str,
        max_images: int = 50,
        languages: List[str] = ["en", "ar"],
        sources: List[str] = ["google", "bing"]
    ) -> Dict:
        """
        Start image crawling task

        Args:
            query: Search query
            max_images: Maximum number of images
            languages: Languages for search
            sources: Image sources

        Returns:
            Crawl response dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/crawl",
                    json={
                        "query": query,
                        "max_images": max_images,
                        "languages": languages,
                        "sources": sources
                    }
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error in start_crawl: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in start_crawl: {str(e)}")
            raise

    async def get_crawl_status(self, task_id: str) -> Dict:
        """
        Get crawl task status

        Args:
            task_id: Task ID

        Returns:
            Status dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/crawl/{task_id}"
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error in get_crawl_status: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in get_crawl_status: {str(e)}")
            raise

    async def get_knowledge_stats(self) -> Dict:
        """
        Get knowledge base statistics

        Returns:
            Statistics dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/knowledge"
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error in get_knowledge_stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in get_knowledge_stats: {str(e)}")
            raise

    async def list_diseases(self) -> Dict:
        """
        List all diseases in knowledge base

        Returns:
            Diseases list dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/diseases"
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error in list_diseases: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in list_diseases: {str(e)}")
            raise

    async def get_disease_info(self, disease_name: str) -> Dict:
        """
        Get detailed disease information

        Args:
            disease_name: Disease name

        Returns:
            Disease information dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/diseases/{disease_name}"
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error in get_disease_info: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in get_disease_info: {str(e)}")
            raise

    async def health_check(self) -> Dict:
        """
        Check crawler service health

        Returns:
            Health status dictionary
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global instance
crawler_client = CrawlerServiceClient()
