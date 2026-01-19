"""
Image Crawler API Endpoints - Gaara Scan AI v4.3.1
API endpoints for image crawler service
"""

import logging
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...services.crawler_service import crawler_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/crawler", tags=["Image Crawler"])

# Models


class CrawlRequest(BaseModel):
    """Crawl request model"""
    query: str
    max_images: int = 50
    languages: List[str] = ["en", "ar"]
    sources: List[str] = ["google", "bing"]


@router.post("/start")
async def start_crawl(request: CrawlRequest):
    """
    Start image crawling task

    - **query**: Search query (e.g., "tomato leaf disease")
    - **max_images**: Maximum number of images to download (default: 50)
    - **languages**: Languages for search (default: ["en", "ar"])
    - **sources**: Image sources (default: ["google", "bing"])
    """
    try:
        result = await crawler_client.start_crawl(
            query=request.query,
            max_images=request.max_images,
            languages=request.languages,
            sources=request.sources
        )

        return {
            "success": True,
            "data": result,
            "message": "Crawl task started successfully"
        }

    except Exception as e:
        logger.error(f"Failed to start crawl: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{task_id}")
async def get_crawl_status(task_id: str):
    """
    Get crawl task status

    - **task_id**: Task ID from start_crawl response
    """
    try:
        result = await crawler_client.get_crawl_status(task_id)

        return {
            "success": True,
            "data": result,
            "message": "Status retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Failed to get crawl status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge/stats")
async def get_knowledge_stats():
    """
    Get knowledge base statistics

    Returns statistics about collected disease images and knowledge
    """
    try:
        result = await crawler_client.get_knowledge_stats()

        return {
            "success": True,
            "data": result.get("data", {}),
            "message": "Knowledge stats retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Failed to get knowledge stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diseases")
async def list_diseases():
    """
    List all diseases in knowledge base

    Returns a list of all diseases with their statistics
    """
    try:
        result = await crawler_client.list_diseases()

        return {
            "success": True,
            "data": result.get("data", []),
            "message": "Diseases list retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Failed to list diseases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diseases/{disease_name}")
async def get_disease_info(disease_name: str):
    """
    Get detailed information about a specific disease

    - **disease_name**: Name of the disease
    """
    try:
        result = await crawler_client.get_disease_info(disease_name)

        return {
            "success": True,
            "data": result.get("data", {}),
            "message": "Disease information retrieved successfully"
        }

    except Exception as e:
        logger.error(f"Failed to get disease info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def check_crawler_health():
    """
    Check image crawler service health

    Returns health status of the crawler service
    """
    try:
        result = await crawler_client.health_check()

        return {
            "success": result.get("status") == "healthy",
            "data": result,
            "message": "Health check completed"
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "success": False,
            "data": {"status": "unhealthy", "error": str(e)},
            "message": "Health check failed"
        }
